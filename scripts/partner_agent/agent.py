#!/usr/bin/env python3
"""
Partner Agent - AI-powered assistant for running partnership playbooks.
Version: 1.1 (2026-02-02) - Fixed and improved

Usage:
    python agent.py                           # Interactive mode
    python agent.py --playbook recruit        # Run specific playbook
    python agent.py --resume acme-corp        # Resume saved session
    python agent.py --status                  # View all partners
    python agent.py --reload                  # Reload config without restart
    python agent.py --verbose                 # Enable debug logging
"""

import os
import sys
import json
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
import argparse
import time

import yaml

# Optional rich formatting
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table

    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

# LLM clients
try:
    import anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI as OpenAIClient

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from partner_state import PartnerState


# Configure logging
logger = logging.getLogger(__name__)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class RetryConfig:
    """Configuration for API retry behavior."""

    def __init__(
        self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 10.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay


class OllamaClient:
    """Local Ollama LLM client with retry support."""

    def __init__(
        self,
        endpoint: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
        retry_config: RetryConfig = None,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.retry_config = retry_config or RetryConfig()

    def _retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry."""
        last_exception = None
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.retry_config.max_retries:
                    delay = min(
                        self.retry_config.base_delay * (2**attempt),
                        self.retry_config.max_delay,
                    )
                    logger.warning(
                        f"API call failed (attempt {attempt + 1}), retrying in {delay}s: {e}"
                    )
                    time.sleep(delay)
        raise last_exception

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """Send chat request to local Ollama with retry."""
        ollama_messages = []

        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})

        ollama_messages.extend(messages)

        def make_request():
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json={
                    "model": self.model,
                    "messages": ollama_messages,
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "[No response]")

        return self._retry_with_backoff(make_request)


class PartnerAgent:
    """Main agent class for running partnership playbooks."""

    # Class constant for valid models (as of Feb 2026)
    VALID_MODELS = {
        "anthropic": ["sonnet-4-20250514", "haiku-3-20250514"],
        "openai": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
        "ollama": ["llama3.2:3b", "qwen2.5:7b", "mistral:7b"],
    }

    def __init__(self, config_path: str = "config.yaml", verbose: bool = False):
        self.verbose = verbose
        self._setup_logging()
        self.base_dir = Path(__file__).parent
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.templates_dir = self.base_dir / self.config.get(
            "templates_dir", "../../docs"
        )
        self.state_dir = self.base_dir / self.config.get("state_dir", "./state")
        self.playbooks_dir = self.base_dir / "playbooks"
        self.llm_client = self._init_llm()
        logger.info("PartnerAgent initialized successfully")

    def _setup_logging(self):
        """Configure logging based on verbosity."""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level, format=LOG_FORMAT)
        logger.setLevel(level)

    def _validate_path(self, path: Path, base_dir: Path) -> bool:
        """
        Validate that path is within base directory.
        Prevents path traversal attacks.
        """
        try:
            resolved_path = (base_dir / path).resolve()
            resolved_base = base_dir.resolve()
            return resolved_path.is_file() and resolved_base in resolved_path.parents
        except (OSError, ValueError):
            return False

    def _sanitize_partner_name(self, name: str) -> str:
        """
        Sanitize partner name for safe directory/file usage.
        - Max 100 characters
        - Only alphanumeric, dash, underscore
        - No path traversal characters
        - No leading/trailing whitespace
        """
        if not name or not name.strip():
            raise ValueError("Partner name cannot be empty")

        name = name.strip()

        if len(name) > 100:
            raise ValueError("Partner name exceeds 100 characters")

        # Check for path traversal attempts
        if any(char in name for char in ["/", "\\", "..", "."]):
            raise ValueError("Partner name contains invalid characters")

        # Only allow alphanumeric, spaces, dashes, underscores
        if not re.match(r"^[\w\s-]+$", name):
            raise ValueError("Partner name contains invalid characters")

        return name

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file with validation."""
        config_file = self.base_dir / config_path
        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f)

                # Validate model if specified
                provider = config.get("provider", "anthropic")
                model = config.get("model")
                if model and model not in self.VALID_MODELS.get(provider, []):
                    logger.warning(
                        f"Model '{model}' may not exist. Valid models for {provider}: {self.VALID_MODELS.get(provider, [])}"
                    )

                return config

        # Default configuration
        return {
            "provider": "anthropic",
            "model": "sonnet-4-20250514",  # Changed from speculative name
            "templates_dir": "../../docs",
            "state_dir": "./state",
        }

    def reload_config(self):
        """Reload configuration from disk without restarting."""
        logger.info("Reloading configuration...")
        self.config = self._load_config(self.config_path)
        logger.info("Configuration reloaded successfully")

    def _init_llm(self):
        """Initialize LLM client based on configuration."""
        provider = self.config.get("provider", "anthropic")
        ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
        retry_config = RetryConfig()

        # Try Ollama first if available
        if provider == "ollama" or (provider == "auto" and REQUESTS_AVAILABLE):
            try:
                resp = requests.get(f"{ollama_endpoint}/api/tags", timeout=5)
                if resp.status_code == 200:
                    self._print_success(f"Using local Ollama: {ollama_model}")
                    return OllamaClient(
                        endpoint=ollama_endpoint,
                        model=ollama_model,
                        retry_config=retry_config,
                    )
            except Exception as e:
                logger.warning(f"Ollama health check failed: {e}")
                pass

        if provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                self._print_error(
                    "anthropic package not installed. Run: pip install anthropic"
                )
                return None
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                self._print_warning("ANTHROPIC_API_KEY not set. LLM features disabled.")
                return None
            return anthropic.Anthropic(api_key=api_key)

        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                self._print_error(
                    "openai package not installed. Run: pip install openai"
                )
                return None
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                self._print_warning("OPENAI_API_KEY not set. LLM features disabled.")
                return None
            # Fixed: Use OpenAIClient (v1.x syntax)
            return OpenAIClient(api_key=api_key)

        return None

    def _print(self, text: str, style: str = None):
        """Print with optional rich formatting - all output goes through here."""
        if RICH_AVAILABLE and console:
            console.print(text, style=style)
        else:
            print(text)
        logger.info(f"Output: {text[:100]}..." if len(text) > 100 else text)

    def _print_error(self, text: str):
        self._print(f"Error: {text}", style="red bold")
        logger.error(text)

    def _print_warning(self, text: str):
        self._print(f"Warning: {text}", style="yellow")
        logger.warning(text)

    def _print_success(self, text: str):
        self._print(f"✓ {text}", style="green")
        logger.info(text)

    def _prompt(self, message: str, default: str = None) -> str:
        """Get user input."""
        if RICH_AVAILABLE:
            return Prompt.ask(message, default=default)
        else:
            if default:
                result = input(f"{message} [{default}]: ").strip()
                return result if result else default
            return input(f"{message}: ").strip()

    def _confirm(self, message: str, default: bool = True) -> bool:
        """Get yes/no confirmation."""
        if RICH_AVAILABLE:
            return Confirm.ask(message, default=default)
        else:
            result = (
                input(f"{message} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
            )
            if not result:
                return default
            return result in ("y", "yes")

    def load_playbook(self, name: str) -> dict:
        """Load a playbook definition with path validation."""
        playbook_file = self.playbooks_dir / f"{name}.yaml"

        # Validate path before loading
        if not self._validate_path(playbook_file, self.playbooks_dir):
            raise ValueError(f"Invalid playbook path: {name}")

        if not playbook_file.exists():
            raise FileNotFoundError(f"Playbook not found: {name}")

        with open(playbook_file) as f:
            return yaml.safe_load(f)

    def list_playbooks(self) -> list:
        """List available playbooks."""
        playbooks = []
        if self.playbooks_dir.exists():
            for f in self.playbooks_dir.glob("*.yaml"):
                with open(f) as pf:
                    data = yaml.safe_load(pf)
                    playbooks.append(
                        {
                            "name": f.stem,
                            "title": data.get("name", f.stem),
                            "description": data.get("description", ""),
                            "steps": len(data.get("steps", [])),
                        }
                    )
        return playbooks

    def load_template(self, template_path: str) -> dict:
        """
        Load and parse a template file with security validation.

        Security: Validates that template_path doesn't escape templates_dir.
        """
        full_path = self.templates_dir / template_path

        # Validate path before loading - prevents path traversal
        if not self._validate_path(template_path, self.templates_dir):
            raise ValueError(f"Invalid template path: {template_path}")

        if not full_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(full_path) as f:
            content = f.read()

        # Parse YAML frontmatter
        frontmatter = {}
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()

        # Extract placeholders
        placeholders = self._extract_placeholders(body)

        return {
            "path": template_path,
            "frontmatter": frontmatter,
            "body": body,
            "placeholders": placeholders,
        }

    def _extract_placeholders(self, content: str) -> list:
        """Extract fillable placeholders from template content."""
        patterns = [
            r"\[([^\]]+)\]",  # [Your Company], [Partner Name]
            r"\$\[?(\w+)\]?",  # $X, $[Amount]
            r"<([^>]+)>",  # <insert value>
            r"_+([^_]+)_+",  # ___field___
        ]
        placeholders = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            placeholders.update(matches)
        return list(placeholders)

    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug with sanitization."""
        # First sanitize the input
        text = self._sanitize_partner_name(text)
        # Then slugify
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    def get_partner_state(self, partner: str) -> dict:
        """Load saved state for a partner."""
        # Sanitize partner name first
        partner = self._sanitize_partner_name(partner)
        slug = self.slugify(partner)
        state_file = self.state_dir / slug / "metadata.json"

        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
            # Back-fill new fields for existing state files
            state.setdefault("tier", None)
            state.setdefault("vertical", None)
            state.setdefault("health_score", None)
            state.setdefault("rm", None)
            state.setdefault("notes", [])
            state.setdefault("milestones", [])
            return state

        return {
            "name": partner,
            "slug": slug,
            "created": datetime.now().isoformat(),
            "tier": None,  # Registered / Silver / Gold / Strategic
            "vertical": None,  # SaaS, Healthcare, etc.
            "health_score": None,  # 0-100
            "rm": None,  # Relationship Manager name
            "notes": [],  # [{"ts": iso, "text": str}]
            "milestones": [],  # [{"ts": iso, "name": str}]
            "playbooks": {},
        }

    def save_partner_state(self, partner: str, state: dict):
        """Save partner state to disk with validation."""
        # Sanitize partner name
        partner = self._sanitize_partner_name(partner)
        slug = self.slugify(partner)
        partner_dir = self.state_dir / slug
        partner_dir.mkdir(parents=True, exist_ok=True)
        state_file = partner_dir / "metadata.json"

        # Ensure state matches sanitized partner name
        state["name"] = partner
        state["slug"] = slug

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

        logger.info(f"Saved state for partner: {partner}")

    def list_partners(self) -> list:
        """List all tracked partners."""
        partners = []
        if self.state_dir.exists():
            for partner_dir in self.state_dir.iterdir():
                if partner_dir.is_dir():
                    meta_file = partner_dir / "metadata.json"
                    if meta_file.exists():
                        with open(meta_file) as f:
                            partners.append(json.load(f))
        return partners

    # -------------------------------------------------------------------------
    # Agent Superpowers
    # -------------------------------------------------------------------------

    PLAYBOOK_NEXT_STEPS: Dict[str, List[str]] = {
        "recruit": ["onboard"],
        "onboard": ["qbr", "co-marketing"],
        "qbr": ["expand"],
        "expand": ["co-marketing"],
        "co-marketing": ["qbr"],
        "support-escalation": ["qbr"],
    }

    TIER_EXTRA_PLAYBOOKS: Dict[str, List[str]] = {
        "Gold": ["co-marketing", "expand"],
        "Strategic": ["co-marketing", "expand", "qbr"],
    }

    def recommend_templates(self, partner_data: dict) -> List[str]:
        """
        Return an ordered list of recommended next playbooks for a partner
        based on completed playbooks and their tier.
        """
        completed = {
            k
            for k, v in partner_data.get("playbooks", {}).items()
            if v.get("completed")
        }
        tier = partner_data.get("tier") or ""
        recommended: List[str] = []

        # Follow natural progression from completed playbooks
        for pb in completed:
            for nxt in self.PLAYBOOK_NEXT_STEPS.get(pb, []):
                if nxt not in completed and nxt not in recommended:
                    recommended.append(nxt)

        # Add tier-specific extras
        for pb in self.TIER_EXTRA_PLAYBOOKS.get(tier, []):
            if pb not in completed and pb not in recommended:
                recommended.append(pb)

        # Default: start with recruit if nothing done yet
        if not recommended and not completed:
            recommended = ["recruit"]
        elif not recommended:
            recommended = ["qbr", "expand"]

        return recommended

    def generate_email(self, partner_data: dict, situation: str) -> str:
        """
        Generate a contextual partner email using the LLM.
        Returns the full email text (Subject + body).
        """
        company = self.config.get("company", {})
        system = self._get_system_prompt(partner_data)
        messages = [
            {
                "role": "user",
                "content": (
                    f"Write a professional partner email for the following situation.\n\n"
                    f"Sender company: {company.get('name', '[Your Company]')}\n"
                    f"Recipient partner: {partner_data.get('name')}\n"
                    f"Partner tier: {partner_data.get('tier') or 'Unclassified'}\n"
                    f"Situation: {situation}\n\n"
                    "Format: Subject line first, then a blank line, then the full email body "
                    "with greeting, body paragraphs, and a professional sign-off."
                ),
            }
        ]
        return self.chat(messages, system_prompt=system)

    def add_note(self, partner_data: dict, text: str) -> dict:
        """Append a timestamped note to a partner's record and save state."""
        partner_data.setdefault("notes", [])
        partner_data["notes"].append(
            {"ts": datetime.now().isoformat(), "text": text.strip()}
        )
        self.save_partner_state(partner_data["name"], partner_data)
        return partner_data

    def add_milestone(self, partner_data: dict, name: str) -> dict:
        """Record a partner milestone and save state."""
        partner_data.setdefault("milestones", [])
        partner_data["milestones"].append(
            {"ts": datetime.now().isoformat(), "name": name.strip()}
        )
        self.save_partner_state(partner_data["name"], partner_data)
        return partner_data

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """Send messages to LLM and get response."""
        if not self.llm_client:
            return "[LLM not available - please set API key]"

        provider = self.config.get("provider", "anthropic")
        model = self.config.get("model", "sonnet-4-20250514")

        # Handle Ollama
        if isinstance(self.llm_client, OllamaClient):
            return self.llm_client.chat(messages, system_prompt)

        if provider == "anthropic":
            response = self.llm_client.messages.create(
                model=model,
                max_tokens=4096,
                system=system_prompt or self._get_system_prompt(),
                messages=messages,
            )
            return response.content[0].text

        elif provider == "openai":
            msgs = []
            if system_prompt:
                msgs.append({"role": "system", "content": system_prompt})
            msgs.extend(messages)
            response = self.llm_client.chat.completions.create(
                model=model, messages=msgs
            )
            return response.choices[0].message.content

        return "[Unknown provider]"

    def _get_system_prompt(self, partner_data: dict = None) -> str:
        """Get the system prompt for the agent, optionally enriched with partner context."""
        company = self.config.get("company", {})
        tiers = {t["name"]: t for t in self.config.get("tiers", [])}
        qbr_freq = self.config.get("qbr_frequency", {})

        partner_section = ""
        if partner_data:
            tier_name = partner_data.get("tier") or "Unclassified"
            tier_cfg = tiers.get(tier_name, {})
            health = partner_data.get("health_score")
            health_str = f"{health}/100" if health is not None else "Not assessed"
            recent_notes = partner_data.get("notes", [])[-3:]
            notes_str = (
                "; ".join(n["text"] for n in recent_notes) if recent_notes else "None"
            )
            milestones = [m["name"] for m in partner_data.get("milestones", [])]

            tier_details = ""
            if tier_cfg:
                tier_details = (
                    f"\n  Revenue threshold: ${tier_cfg.get('revenue_threshold', 0):,}"
                    f"\n  Certification required: {tier_cfg.get('certification_required', False)}"
                    f"\n  QBR cadence: {qbr_freq.get(tier_name, 'annually')}"
                )

            partner_section = f"""
Partner context:
- Partner: {partner_data.get("name")}
- Tier: {tier_name}{tier_details}
- Vertical: {partner_data.get("vertical") or "Unknown"}
- Health score: {health_str}
- Relationship manager: {partner_data.get("rm") or "Unassigned"}
- Completed milestones: {", ".join(milestones) if milestones else "None"}
- Recent notes: {notes_str}

Tailor your advice to the partner's tier. {tier_name} partners get {qbr_freq.get(tier_name, "annual")} QBRs.
"""

        return f"""You are a Partnership Expert Agent helping to run partnership playbooks.

Your role is to guide users through filling out partnership templates by:
1. Asking relevant questions about the partner and situation
2. Providing expert recommendations based on best practices
3. Filling in template sections with the information gathered
4. Highlighting areas that need more information

Company context:
- Company: {company.get("name", "[Your Company]")}
- Product: {company.get("product", "[Your Product]")}
- Value Prop: {company.get("value_prop", "[Your Value Proposition]")}
{partner_section}
Be concise and actionable. Ask one question at a time.
When you have enough information for a section, fill it in and move to the next.
Format filled sections in markdown."""

    def run_playbook_step(
        self,
        playbook: dict,
        step_index: int,
        partner: str,
        context: dict,
        partner_data: dict = None,
    ) -> dict:
        """Run a single step of a playbook."""
        step = playbook["steps"][step_index]
        template = self.load_template(step["template"])

        # Build conversation
        messages = context.get("messages", [])
        messages.append(
            {
                "role": "user",
                "content": f"""We're working on: {playbook["name"]}
Partner: {partner}
Current step: {step["name"]}

Template: {template["frontmatter"].get("title", step["name"])}
Description: {template["frontmatter"].get("description", "")}

Placeholders to fill: {", ".join(template["placeholders"][:10])}

{step.get("prompt", "Guide me through filling out this template.")}""",
            }
        )

        system = self._get_system_prompt(partner_data)
        response = self.chat(messages, system_prompt=system)
        messages.append({"role": "assistant", "content": response})

        return {
            "step": step_index,
            "step_name": step["name"],
            "template": step["template"],
            "messages": messages,
            "response": response,
        }

    def interactive_mode(self):
        """Run the agent in interactive mode."""
        self._print("\n" + "=" * 50)
        self._print("Partner Agent v1.2", style="bold blue")
        self._print("=" * 50 + "\n")

        while True:
            self._print("\nWhat would you like to do?")
            self._print("1. Start a new playbook")
            self._print("2. Continue existing playbook")
            self._print("3. View partner status")
            self._print("4. List templates")
            self._print("5. Get next-step recommendations")
            self._print("6. Generate partner email")
            self._print("7. Add note to partner")
            self._print("8. Exit")

            choice = self._prompt("\nSelect option", default="1")

            if choice == "1":
                self._start_playbook_interactive()
            elif choice == "2":
                self._continue_playbook_interactive()
            elif choice == "3":
                self._show_status()
            elif choice == "4":
                self._list_templates()
            elif choice == "5":
                self._show_recommendations()
            elif choice == "6":
                self._generate_email_interactive()
            elif choice == "7":
                self._add_note_interactive()
            elif choice == "8":
                self._print("\nGoodbye!", style="blue")
                break
            else:
                self._print("Invalid choice", style="red")

    def _pick_partner(self) -> Optional[dict]:
        """Helper: let user pick an existing partner; returns partner_data or None."""
        partners = self.list_partners()
        if not partners:
            self._print("No saved partners found.")
            return None
        self._print("\nSaved partners:")
        for i, p in enumerate(partners, 1):
            tier = p.get("tier") or "Unclassified"
            self._print(f"  {i}. {p['name']}  [{tier}]")
        choice = self._prompt("Select partner number")
        try:
            return partners[int(choice) - 1]
        except (ValueError, IndexError):
            self._print_error("Invalid selection")
            return None

    def _show_recommendations(self):
        """Show next-step playbook recommendations for a partner."""
        partner_data = self._pick_partner()
        if not partner_data:
            return
        recs = self.recommend_templates(partner_data)
        if recs:
            self._print(f"\nRecommended next steps for {partner_data['name']}:")
            for pb in recs:
                self._print(f"  → {pb}", style="green")
        else:
            self._print("No further playbook recommendations — partner looks complete!")

    def _generate_email_interactive(self):
        """Generate a partner email interactively."""
        partner_data = self._pick_partner()
        if not partner_data:
            return
        self._print(
            "\nExamples: 'QBR invite', 'follow-up after missed target', 'co-marketing proposal'"
        )
        situation = self._prompt("Describe the email situation")
        if not situation.strip():
            self._print_error("Situation required")
            return
        self._print("\nGenerating email...\n")
        result = self.generate_email(partner_data, situation)
        if RICH_AVAILABLE:
            console.print(Markdown(result))
        else:
            self._print(result)

    def _add_note_interactive(self):
        """Add a note to a partner record."""
        partner_data = self._pick_partner()
        if not partner_data:
            return
        note = self._prompt("Note text")
        if not note.strip():
            self._print_error("Note cannot be empty")
            return
        self.add_note(partner_data, note)
        self._print_success(f"Note added to {partner_data['name']}")

    def _start_playbook_interactive(self):
        """Start a new playbook interactively."""
        playbooks = self.list_playbooks()
        if not playbooks:
            self._print_error("No playbooks found. Create playbooks in ./playbooks/")
            return

        self._print("\nAvailable playbooks:")
        for i, pb in enumerate(playbooks, 1):
            self._print(f"  {i}. {pb['title']} ({pb['steps']} steps)")
            self._print(f"     {pb['description']}", style="dim")

        choice = self._prompt("\nSelect playbook number", default="1")
        try:
            playbook_idx = int(choice) - 1
            playbook_name = playbooks[playbook_idx]["name"]
        except (ValueError, IndexError):
            self._print_error("Invalid selection")
            return

        # Partner name with sanitization
        while True:
            partner = self._prompt("Partner name")
            try:
                partner = self._sanitize_partner_name(partner)
                break
            except ValueError as e:
                self._print_error(str(e))

        if not partner:
            self._print_error("Partner name required")
            return

        playbook = self.load_playbook(playbook_name)
        self._print(f"\nStarting '{playbook['name']}' for {partner}...\n")

        # Initialize state
        state = self.get_partner_state(partner)
        state["playbooks"][playbook_name] = {
            "started": datetime.now().isoformat(),
            "current_step": 0,
            "completed": False,
            "context": {"messages": []},  # Added context storage
        }
        self.save_partner_state(partner, state)

        # Run through steps
        context = {"messages": []}
        for i, step in enumerate(playbook["steps"]):
            self._print(
                f"\n--- Step {i + 1}/{len(playbook['steps'])}: {step['name']} ---\n"
            )

            result = self.run_playbook_step(
                playbook, i, partner, context, partner_data=state
            )
            context = {"messages": result["messages"]}

            if RICH_AVAILABLE:
                console.print(Markdown(result["response"]))
            else:
                self._print(result["response"])

            # Save progress
            state["playbooks"][playbook_name]["current_step"] = i + 1
            state["playbooks"][playbook_name]["context"] = context
            self.save_partner_state(partner, state)

            if i < len(playbook["steps"]) - 1:
                if not self._confirm("\nContinue to next step?"):
                    self._print("Progress saved. Resume anytime.")
                    return

        state["playbooks"][playbook_name]["completed"] = True
        state["playbooks"][playbook_name]["completed_at"] = datetime.now().isoformat()

        # Record milestone using PartnerState
        state_mgr = PartnerState(partner, state_dir=str(self.state_dir))
        state_mgr.record_playbook_complete(playbook_name)
        state_mgr.save()

        self.save_partner_state(partner, state)
        self._print_success(f"\nPlaybook '{playbook['name']}' completed for {partner}!")
        # Surface next-step recommendations immediately after completion
        recs = self.recommend_templates(state)
        if recs:
            self._print("\nSuggested next playbooks:")
            for r in recs:
                self._print(f"  → {r}", style="green")

    def _continue_playbook_interactive(self):
        """Continue an existing playbook - NOW COMPLETE."""
        partners = self.list_partners()
        if not partners:
            self._print("No saved partners found.")
            return

        self._print("\nSaved partners:")
        for i, p in enumerate(partners, 1):
            active = [
                k for k, v in p.get("playbooks", {}).items() if not v.get("completed")
            ]
            self._print(f"  {i}. {p['name']}")
            if active:
                self._print(f"     Active: {', '.join(active)}", style="yellow")

        choice = self._prompt("Select partner number")
        try:
            partner_data = partners[int(choice) - 1]
        except (ValueError, IndexError):
            self._print_error("Invalid selection")
            return

        # Find incomplete playbooks
        incomplete = {
            k: v
            for k, v in partner_data.get("playbooks", {}).items()
            if not v.get("completed")
        }
        if not incomplete:
            self._print("No incomplete playbooks for this partner.")
            return

        self._print(f"\nIncomplete playbooks for {partner_data['name']}:")
        for name, data in incomplete.items():
            self._print(f"  - {name}: Step {data['current_step']}")

        # Resume first incomplete
        playbook_name = list(incomplete.keys())[0]
        playbook = self.load_playbook(playbook_name)
        step = incomplete[playbook_name]["current_step"]

        self._print(f"\nResuming '{playbook_name}' at step {step + 1}...")

        # Load saved context
        context = incomplete[playbook_name].get("context", {"messages": []})

        # Continue from saved step
        for i in range(step, len(playbook["steps"])):
            self._print(
                f"\n--- Step {i + 1}/{len(playbook['steps'])}: {playbook['steps'][i]['name']} ---\n"
            )

            result = self.run_playbook_step(playbook, i, partner_data["name"], context)
            context = {"messages": result["messages"]}

            if RICH_AVAILABLE:
                console.print(Markdown(result["response"]))
            else:
                self._print(result["response"])

            # Save progress
            partner_data["playbooks"][playbook_name]["current_step"] = i + 1
            partner_data["playbooks"][playbook_name]["context"] = context
            self.save_partner_state(partner_data["name"], partner_data)

            if i < len(playbook["steps"]) - 1:
                if not self._confirm("\nContinue to next step?"):
                    self._print("Progress saved. Resume anytime.")
                    return

        partner_data["playbooks"][playbook_name]["completed"] = True
        partner_data["playbooks"][playbook_name]["completed_at"] = (
            datetime.now().isoformat()
        )

        # Record milestone using PartnerState
        state_mgr = PartnerState(partner_data["name"], state_dir=str(self.state_dir))
        state_mgr.record_playbook_complete(playbook_name)
        state_mgr.save()

        self.save_partner_state(partner_data["name"], partner_data)
        self._print_success(
            f"\nPlaybook '{playbook_name}' completed for {partner_data['name']}!"
        )

    def _show_status(self):
        """Show status of all partners."""
        partners = self.list_partners()
        if not partners:
            self._print("No partners tracked yet.")
            return

        if RICH_AVAILABLE:
            table = Table(title="Partner Status")
            table.add_column("Partner")
            table.add_column("Stage")
            table.add_column("Active Playbooks")
            table.add_column("Last Updated")

            for p in partners:
                active = [
                    k
                    for k, v in p.get("playbooks", {}).items()
                    if not v.get("completed")
                ]
                completed = [
                    k for k, v in p.get("playbooks", {}).items() if v.get("completed")
                ]
                stage = completed[-1] if completed else "New"
                table.add_row(
                    p["name"],
                    stage,
                    ", ".join(active) or "-",
                    p.get("created", "")[:10],
                )
            console.print(table)
        else:
            self._print("\nPartner Status:")
            for p in partners:
                self._print(f"  {p['name']}")
                for pb, data in p.get("playbooks", {}).items():
                    status = (
                        "✓" if data.get("completed") else f"Step {data['current_step']}"
                    )
                    self._print(f"    - {pb}: {status}")

    def _list_templates(self):
        """List all available templates."""
        self._print("\nAvailable Templates:\n")
        for section in ["strategy", "recruitment", "enablement"]:
            section_path = self.templates_dir / section
            if section_path.exists():
                self._print(f"{section.title()} Templates:", style="bold")
                for f in sorted(section_path.glob("*.md")):
                    if f.name != "index.md":
                        self._print(f"  - {f.name}")
                self._print("")


def main():
    parser = argparse.ArgumentParser(
        description="Partner Agent v1.1 - AI-powered partnership playbooks"
    )
    parser.add_argument("--playbook", "-p", help="Run specific playbook")
    parser.add_argument("--partner", help="Partner name")
    parser.add_argument("--resume", "-r", help="Resume saved session")
    parser.add_argument(
        "--status", "-s", action="store_true", help="Show partner status"
    )
    parser.add_argument(
        "--config", "-c", default="config.yaml", help="Config file path"
    )
    parser.add_argument(
        "--reload", action="store_true", help="Reload config without restarting"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    agent = PartnerAgent(config_path=args.config, verbose=args.verbose)

    if args.reload:
        agent.reload_config()
    elif args.status:
        agent._show_status()
    elif args.playbook and args.partner:
        # Direct playbook execution
        playbook = agent.load_playbook(args.playbook)
        agent._print(f"Starting '{playbook['name']}' for {args.partner}...")
        context = {"messages": []}
        for i, step in enumerate(playbook["steps"]):
            result = agent.run_playbook_step(playbook, i, args.partner, context)
            agent._print(f"\n--- {step['name']} ---\n")
            agent._print(result["response"])
            context = {"messages": result["messages"]}
    else:
        # Interactive mode
        agent.interactive_mode()


if __name__ == "__main__":
    main()
