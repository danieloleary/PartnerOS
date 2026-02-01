#!/usr/bin/env python3
"""
Partner Agent - AI-powered assistant for running partnership playbooks.

Usage:
    python agent.py                           # Interactive mode
    python agent.py --playbook recruit        # Run specific playbook
    python agent.py --resume acme-corp        # Resume saved session
    python agent.py --status                  # View all partners
"""

import os
import sys
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional
import argparse

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
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class OllamaClient:
    """Local Ollama LLM client."""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        self.endpoint = endpoint.rstrip('/')
        self.model = model
    
    def chat(self, messages: list, system_prompt: str = None) -> str:
        """Send chat request to local Ollama."""
        ollama_messages = []
        
        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})
        
        ollama_messages.extend(messages)
        
        try:
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json={
                    "model": self.model,
                    "messages": ollama_messages,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "[No response]")
        except Exception as e:
            return f"[Ollama error: {e}]"


class PartnerAgent:
    """Main agent class for running partnership playbooks."""

    def __init__(self, config_path: str = "config.yaml"):
        self.base_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.templates_dir = self.base_dir / self.config.get("templates_dir", "../../partner_blueprint")
        self.state_dir = self.base_dir / self.config.get("state_dir", "./state")
        self.playbooks_dir = self.base_dir / "playbooks"
        self.llm_client = self._init_llm()

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        config_file = self.base_dir / config_path
        if config_file.exists():
            with open(config_file) as f:
                return yaml.safe_load(f)
        return {
            "provider": "anthropic",
            "model": "claude-sonnet-4-20250514",
            "templates_dir": "../../partner_blueprint",
            "state_dir": "./state",
        }

    def _init_llm(self):
        """Initialize LLM client based on configuration."""
        provider = self.config.get("provider", "anthropic")
        ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

        # Try Ollama first if available
        if provider == "ollama" or (provider == "auto" and REQUESTS_AVAILABLE):
            try:
                # Quick health check
                resp = requests.get(f"{ollama_endpoint}/api/tags", timeout=5)
                if resp.status_code == 200:
                    self._print_success(f"Using local Ollama: {ollama_model}")
                    return OllamaClient(endpoint=ollama_endpoint, model=ollama_model)
            except:
                pass

        if provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                self._print_error("anthropic package not installed. Run: pip install anthropic")
                return None
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                self._print_warning("ANTHROPIC_API_KEY not set. LLM features disabled.")
                return None
            return anthropic.Anthropic(api_key=api_key)

        elif provider == "github":
            # GitHub Models via Anthropic SDK with custom base URL
            if not ANTHROPIC_AVAILABLE:
                self._print_error("anthropic package not installed. Run: pip install anthropic")
                return None
            api_key = os.environ.get("GITHUB_TOKEN")
            if not api_key:
                self._print_warning("GITHUB_TOKEN not set. LLM features disabled.")
                return None
            # GitHub Models endpoint
            return anthropic.Anthropic(
                api_key=api_key,
                base_url="https://models.inference.ai.azure.com"
            )

        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                self._print_error("openai package not installed. Run: pip install openai")
                return None
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                self._print_warning("OPENAI_API_KEY not set. LLM features disabled.")
                return None
            return openai.OpenAI(api_key=api_key)

        return None

    def _print(self, text: str, style: str = None):
        """Print with optional rich formatting."""
        if RICH_AVAILABLE and console:
            console.print(text, style=style)
        else:
            print(text)

    def _print_error(self, text: str):
        self._print(f"Error: {text}", style="red bold")

    def _print_warning(self, text: str):
        self._print(f"Warning: {text}", style="yellow")

    def _print_success(self, text: str):
        self._print(f"✓ {text}", style="green")

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
            result = input(f"{message} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
            if not result:
                return default
            return result in ('y', 'yes')

    def load_playbook(self, name: str) -> dict:
        """Load a playbook definition."""
        playbook_file = self.playbooks_dir / f"{name}.yaml"
        if not playbook_file.exists():
            raise FileNotFoundError(f"Playbook not found: {name}")
        with open(playbook_file) as f:
            return yaml.safe_load(f)

    def chat_completion(self, user_message: str, conversation_context: list = None, system_prompt: str = None) -> str:
        """
        Get a chat completion from the LLM.
        
        Args:
            user_message: The user's current message
            conversation_context: List of previous messages in {"role": "...", "content": "..."} format
            system_prompt: Optional custom system prompt
        
        Returns:
            The assistant's response text
        """
        if not self.llm_client:
            return "[LLM client not initialized]"
        
        provider = self.config.get("provider", "anthropic")
        default_model = self.config.get("model", "claude-3.5-sonnet")
        
        # Build messages list
        messages = conversation_context.copy() if conversation_context else []
        messages.append({"role": "user", "content": user_message})
        
        # Default system prompt
        if not system_prompt:
            system_prompt = """You are the PartnerOS Partner Agent, an expert in partner ecosystem strategy.
Your role is to help users understand partner program fundamentals, generate customized partnership templates,
and provide strategic guidance. Be conversational, actionable, and reference PartnerOS frameworks when applicable."""
        
        try:
            if isinstance(self.llm_client, anthropic.Anthropic):
                # Anthropic API (includes GitHub Models)
                response = self.llm_client.messages.create(
                    model=default_model,
                    max_tokens=2048,
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text
            
            elif isinstance(self.llm_client, openai.OpenAI):
                # OpenAI API
                response = self.llm_client.chat.completions.create(
                    model=default_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *messages
                    ],
                    max_tokens=2048
                )
                return response.choices[0].message.content
            
            elif isinstance(self.llm_client, OllamaClient):
                # Ollama
                return self.llm_client.chat(messages, system_prompt)
            
            else:
                return "[Unknown LLM client type]"
        
        except Exception as e:
            return f"[LLM Error: {str(e)}]"

    def list_playbooks(self) -> list:
        """List available playbooks."""
        playbooks = []
        if self.playbooks_dir.exists():
            for f in self.playbooks_dir.glob("*.yaml"):
                with open(f) as pf:
                    data = yaml.safe_load(pf)
                    playbooks.append({
                        "name": f.stem,
                        "title": data.get("name", f.stem),
                        "description": data.get("description", ""),
                        "steps": len(data.get("steps", []))
                    })
        return playbooks

    def load_template(self, template_path: str) -> dict:
        """Load and parse a template file."""
        full_path = self.templates_dir / template_path
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
            "placeholders": placeholders
        }

    def _extract_placeholders(self, content: str) -> list:
        """Extract fillable placeholders from template content."""
        patterns = [
            r'\[([^\]]+)\]',           # [Your Company], [Partner Name]
            r'\$\[?(\w+)\]?',          # $X, $[Amount]
            r'<([^>]+)>',              # <insert value>
            r'_+([^_]+)_+',            # ___field___
        ]
        placeholders = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            placeholders.update(matches)
        return list(placeholders)

    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

    def get_partner_state(self, partner: str) -> dict:
        """Load saved state for a partner."""
        slug = self.slugify(partner)
        state_file = self.state_dir / slug / "metadata.json"
        if state_file.exists():
            with open(state_file) as f:
                return json.load(f)
        return {
            "name": partner,
            "slug": slug,
            "created": datetime.now().isoformat(),
            "playbooks": {}
        }

    def save_partner_state(self, partner: str, state: dict):
        """Save partner state to disk."""
        slug = self.slugify(partner)
        partner_dir = self.state_dir / slug
        partner_dir.mkdir(parents=True, exist_ok=True)
        state_file = partner_dir / "metadata.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

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

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """Send messages to LLM and get response."""
        if not self.llm_client:
            return "[LLM not available - please set API key]"

        provider = self.config.get("provider", "anthropic")
        model = self.config.get("model", "claude-sonnet-4-20250514")

        # Handle Ollama
        if isinstance(self.llm_client, OllamaClient):
            return self.llm_client.chat(messages, system_prompt)

        if provider == "anthropic":
            response = self.llm_client.messages.create(
                model=model,
                max_tokens=4096,
                system=system_prompt or self._get_system_prompt(),
                messages=messages
            )
            return response.content[0].text

        elif provider == "openai":
            msgs = []
            if system_prompt:
                msgs.append({"role": "system", "content": system_prompt})
            msgs.extend(messages)
            response = self.llm_client.chat.completions.create(
                model=model,
                messages=msgs
            )
            return response.choices[0].message.content

        return "[Unknown provider]"

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        company = self.config.get("company", {})
        return f"""You are a Partnership Expert Agent helping to run partnership playbooks.

Your role is to guide users through filling out partnership templates by:
1. Asking relevant questions about the partner and situation
2. Providing expert recommendations based on best practices
3. Filling in template sections with the information gathered
4. Highlighting areas that need more information

Company context:
- Company: {company.get('name', '[Your Company]')}
- Product: {company.get('product', '[Your Product]')}
- Value Prop: {company.get('value_prop', '[Your Value Proposition]')}

Be concise and actionable. Ask one question at a time.
When you have enough information for a section, fill it in and move to the next.
Format filled sections in markdown."""

    def run_playbook_step(self, playbook: dict, step_index: int, partner: str, context: dict) -> dict:
        """Run a single step of a playbook."""
        step = playbook["steps"][step_index]
        template = self.load_template(step["template"])

        # Build conversation
        messages = context.get("messages", [])
        messages.append({
            "role": "user",
            "content": f"""We're working on: {playbook['name']}
Partner: {partner}
Current step: {step['name']}

Template: {template['frontmatter'].get('title', step['name'])}
Description: {template['frontmatter'].get('description', '')}

Placeholders to fill: {', '.join(template['placeholders'][:10])}

{step.get('prompt', 'Guide me through filling out this template.')}"""
        })

        response = self.chat(messages)
        messages.append({"role": "assistant", "content": response})

        return {
            "step": step_index,
            "step_name": step["name"],
            "template": step["template"],
            "messages": messages,
            "response": response
        }

    def interactive_mode(self):
        """Run the agent in interactive mode."""
        self._print("\n" + "=" * 50)
        self._print("Partner Agent v1.0", style="bold blue")
        self._print("=" * 50 + "\n")

        while True:
            self._print("\nWhat would you like to do?")
            self._print("1. Start a new playbook")
            self._print("2. Continue existing playbook")
            self._print("3. View partner status")
            self._print("4. List templates")
            self._print("5. Exit")

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
                self._print("\nGoodbye!", style="blue")
                break
            else:
                self._print("Invalid choice", style="red")

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

        partner = self._prompt("Partner name")
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
            "completed": False
        }
        self.save_partner_state(partner, state)

        # Run through steps
        context = {"messages": []}
        for i, step in enumerate(playbook["steps"]):
            self._print(f"\n--- Step {i+1}/{len(playbook['steps'])}: {step['name']} ---\n")

            result = self.run_playbook_step(playbook, i, partner, context)
            context = {"messages": result["messages"]}

            if RICH_AVAILABLE:
                console.print(Markdown(result["response"]))
            else:
                self._print(result["response"])

            # Save progress
            state["playbooks"][playbook_name]["current_step"] = i + 1
            self.save_partner_state(partner, state)

            if i < len(playbook["steps"]) - 1:
                if not self._confirm("\nContinue to next step?"):
                    self._print("Progress saved. Resume anytime.")
                    return

        state["playbooks"][playbook_name]["completed"] = True
        state["playbooks"][playbook_name]["completed_at"] = datetime.now().isoformat()
        self.save_partner_state(partner, state)
        self._print_success(f"\nPlaybook '{playbook['name']}' completed for {partner}!")

    def _continue_playbook_interactive(self):
        """Continue an existing playbook."""
        partners = self.list_partners()
        if not partners:
            self._print("No saved partners found.")
            return

        self._print("\nSaved partners:")
        for i, p in enumerate(partners, 1):
            active = [k for k, v in p.get("playbooks", {}).items() if not v.get("completed")]
            self._print(f"  {i}. {p['name']}")
            if active:
                self._print(f"     Active: {', '.join(active)}", style="yellow")

        choice = self._prompt("Select partner number")
        try:
            partner = partners[int(choice) - 1]
        except (ValueError, IndexError):
            self._print_error("Invalid selection")
            return

        # Find incomplete playbooks
        incomplete = {k: v for k, v in partner.get("playbooks", {}).items()
                      if not v.get("completed")}
        if not incomplete:
            self._print("No incomplete playbooks for this partner.")
            return

        self._print(f"\nIncomplete playbooks for {partner['name']}:")
        for name, data in incomplete.items():
            self._print(f"  - {name}: Step {data['current_step']}")

        # Resume first incomplete
        playbook_name = list(incomplete.keys())[0]
        playbook = self.load_playbook(playbook_name)
        step = incomplete[playbook_name]["current_step"]

        self._print(f"\nResuming '{playbook_name}' at step {step + 1}...")
        # Continue from saved step...

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
                active = [k for k, v in p.get("playbooks", {}).items() if not v.get("completed")]
                completed = [k for k, v in p.get("playbooks", {}).items() if v.get("completed")]
                stage = completed[-1] if completed else "New"
                table.add_row(
                    p["name"],
                    stage,
                    ", ".join(active) or "-",
                    p.get("created", "")[:10]
                )
            console.print(table)
        else:
            self._print("\nPartner Status:")
            for p in partners:
                self._print(f"  {p['name']}")
                for pb, data in p.get("playbooks", {}).items():
                    status = "✓" if data.get("completed") else f"Step {data['current_step']}"
                    self._print(f"    - {pb}: {status}")

    def _list_templates(self):
        """List all available templates."""
        self._print("\nAvailable Templates:\n")
        for section in ["I_Partner_Strategy_Templates", "II_Partner_Recruitment_Templates",
                        "III_Partner_Enablement_Templates"]:
            section_path = self.templates_dir / section
            if section_path.exists():
                self._print(f"{section.replace('_', ' ')}:", style="bold")
                for f in sorted(section_path.glob("*.md")):
                    if f.name != "README.md":
                        self._print(f"  - {f.name}")
                self._print("")


def main():
    parser = argparse.ArgumentParser(description="Partner Agent - AI-powered partnership playbooks")
    parser.add_argument("--playbook", "-p", help="Run specific playbook")
    parser.add_argument("--partner", help="Partner name")
    parser.add_argument("--resume", "-r", help="Resume saved session")
    parser.add_argument("--status", "-s", action="store_true", help="Show partner status")
    parser.add_argument("--config", "-c", default="config.yaml", help="Config file path")

    args = parser.parse_args()

    agent = PartnerAgent(config_path=args.config)

    if args.status:
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
