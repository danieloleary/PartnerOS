"""
Partner Agent Web Server - REST API for chat-based template generation
Supports multi-turn conversations with template refinement
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import yaml
from datetime import datetime
from pathlib import Path
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from agent import PartnerAgent

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = None
CONVERSATION_HISTORY = {}  # In-memory conversation storage (can use session/DB for production)
MAX_CONVERSATIONS = 100  # Memory limit


def init_agent():
    """Initialize the Partner Agent with config"""
    global agent
    config_path = Path(__file__).parent / "config.yaml"
    
    # PartnerAgent expects a path string, not a dict
    agent = PartnerAgent(str(config_path.name))
    
    # Check for environment overrides
    provider = os.getenv("PARTNER_AGENT_PROVIDER", agent.config.get("provider", "anthropic"))
    agent.config["provider"] = provider
    agent.llm_client = agent._init_llm()  # Reinitialize with new provider if overridden
    
    return agent


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "provider": agent.config.get("provider", "unknown")})


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint - accept user message and return AI response
    
    Request body:
    {
        "conversation_id": "unique-id" (optional, generates if not provided),
        "message": "User message",
        "templates": ["recruitment", "enablement"] (optional),
        "api_key": "user's API key" (optional - for GitHub Models or other providers)
    }
    
    Response:
    {
        "conversation_id": "unique-id",
        "response": "AI response",
        "templates_referenced": ["template_name"],
        "generated_template": {...} (if a template was generated),
        "conversation_length": 5
    }
    """
    try:
        data = request.get_json()
        conversation_id = data.get("conversation_id", f"conv_{datetime.now().timestamp()}")
        user_message = data.get("message", "")
        template_filters = data.get("templates", [])
        user_api_key = data.get("api_key")  # Get user's API key if provided
        
        if not user_message:
            return jsonify({"error": "Message required"}), 400
        
        # Initialize conversation if new
        if conversation_id not in CONVERSATION_HISTORY:
            if len(CONVERSATION_HISTORY) >= MAX_CONVERSATIONS:
                # Clear oldest conversation (simple FIFO)
                oldest = next(iter(CONVERSATION_HISTORY))
                del CONVERSATION_HISTORY[oldest]
            
            CONVERSATION_HISTORY[conversation_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "templates_generated": []
            }
        
        conv = CONVERSATION_HISTORY[conversation_id]
        
        # Add user message to history
        conv["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Use user's API key if provided, otherwise use default agent
        llm_client = agent.llm_client
        if user_api_key:
            # Create temporary LLM client with user's API key
            llm_client = _create_temp_llm_client(user_api_key, agent.config.get("provider", "anthropic"))
        
        if not llm_client:
            return jsonify({"error": "LLM not configured. Provide an API key or configure environment variables."}), 500
        
        # Get AI response
        system_prompt = _build_system_prompt(template_filters)
        response_text = _get_chat_response(
            llm_client,
            user_message,
            conv["messages"][:-1],  # Exclude current message
            system_prompt,
            agent.config
        )
        
        # Add assistant response to history
        conv["messages"].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Try to extract template if AI generated one
        generated_template = _extract_template_from_response(response_text)
        if generated_template:
            conv["templates_generated"].append(generated_template)
        
        return jsonify({
            "conversation_id": conversation_id,
            "response": response_text,
            "generated_template": generated_template,
            "conversation_length": len(conv["messages"]),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/conversations/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    """Retrieve full conversation history"""
    if conversation_id not in CONVERSATION_HISTORY:
        return jsonify({"error": "Conversation not found"}), 404
    
    return jsonify(CONVERSATION_HISTORY[conversation_id])


@app.route("/api/conversations/<conversation_id>/export/pdf", methods=["POST"])
def export_pdf(conversation_id):
    """
    Export conversation + generated templates as PDF
    
    Request body:
    {
        "title": "Partner Program: Acme Corp",
        "partner_name": "Acme Corp",
        "include_conversation": true
    }
    """
    try:
        if conversation_id not in CONVERSATION_HISTORY:
            return jsonify({"error": "Conversation not found"}), 404
        
        data = request.get_json() or {}
        conv = CONVERSATION_HISTORY[conversation_id]
        
        # Generate PDF
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = data.get("title", f"Partner Templates - {conversation_id}")
        elements.append(Paragraph(title, styles["Heading1"]))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Partner name if provided
        if data.get("partner_name"):
            elements.append(Paragraph(f"<b>Partner:</b> {data['partner_name']}", styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))
        
        # Generated timestamp
        elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Include conversation if requested
        if data.get("include_conversation", False):
            elements.append(Paragraph("Conversation History", styles["Heading2"]))
            elements.append(Spacer(1, 0.2 * inch))
            
            for msg in conv["messages"]:
                role = msg["role"].upper()
                content = msg["content"]
                elements.append(Paragraph(f"<b>{role}:</b> {content}", styles["Normal"]))
                elements.append(Spacer(1, 0.15 * inch))
            
            elements.append(PageBreak())
        
        # Generated templates
        if conv["templates_generated"]:
            elements.append(Paragraph("Generated Templates", styles["Heading2"]))
            elements.append(Spacer(1, 0.2 * inch))
            
            for i, template in enumerate(conv["templates_generated"], 1):
                elements.append(Paragraph(f"Template {i}: {template.get('name', 'Unnamed')}", styles["Heading3"]))
                elements.append(Spacer(1, 0.1 * inch))
                
                content = template.get("content", "")
                elements.append(Paragraph(content.replace("\n", "<br/>"), styles["Normal"]))
                elements.append(Spacer(1, 0.2 * inch))
        
        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        filename = f"partner-templates-{conversation_id[:8]}.pdf"
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/templates", methods=["GET"])
def list_templates():
    """List available templates that agent can work with"""
    try:
        templates_dir = Path(__file__).parent.parent.parent / "partner_blueprint"
        templates = []
        
        for md_file in templates_dir.glob("*.md"):
            if md_file.name.startswith("_") or md_file.name.startswith("."):
                continue
            templates.append({
                "name": md_file.stem,
                "filename": md_file.name,
                "path": str(md_file.relative_to(templates_dir.parent))
            })
        
        return jsonify({"templates": sorted(templates, key=lambda x: x["name"])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _create_temp_llm_client(api_key, provider="anthropic"):
    """Create a temporary LLM client with user-provided API key"""
    try:
        if provider == "github":
            import anthropic
            return anthropic.Anthropic(
                api_key=api_key,
                base_url="https://models.inference.ai.azure.com"
            )
        elif provider == "anthropic":
            import anthropic
            return anthropic.Anthropic(api_key=api_key)
        elif provider == "openai":
            import openai
            return openai.OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Error creating LLM client: {e}")
        return None


def _get_chat_response(llm_client, user_message, conversation_context, system_prompt, config):
    """Get response from LLM using provided client"""
    import anthropic
    import openai
    
    provider = config.get("provider", "anthropic")
    default_model = config.get("model", "claude-3.5-sonnet")
    
    messages = conversation_context.copy() if conversation_context else []
    messages.append({"role": "user", "content": user_message})
    
    try:
        if isinstance(llm_client, anthropic.Anthropic):
            response = llm_client.messages.create(
                model=default_model,
                max_tokens=2048,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        elif isinstance(llm_client, openai.OpenAI):
            response = llm_client.chat.completions.create(
                model=default_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages
                ],
                max_tokens=2048
            )
            return response.choices[0].message.content
        else:
            return "[Unknown LLM client type]"
    except Exception as e:
        return f"[LLM Error: {str(e)}]"


def _build_system_prompt(template_filters):
    """Build system prompt for the agent based on context"""
    prompt = """You are the PartnerOS Partner Agent, an expert in partner ecosystem strategy.
Your role is to help users:
1. Understand partner program fundamentals
2. Generate customized partnership templates and playbooks
3. Refine templates through conversation
4. Provide strategic guidance on partner relationships

When generating templates or content:
- Be specific and actionable
- Reference relevant PartnerOS frameworks where applicable
- Ask clarifying questions to ensure output matches the user's needs
- Offer to refine or iterate on templates until satisfied

You have access to the full PartnerOS framework and templates. You can:
- Reference templates from the partner_blueprint
- Suggest modifications based on user feedback
- Generate new variations of templates
- Provide strategic context from the enablement/strategy docs

Be conversational and helpful. When appropriate, format output as markdown for easy copying/pasting."""
    
    if template_filters:
        prompt += f"\n\nFocus on these template areas: {', '.join(template_filters)}"
    
    return prompt


def _extract_template_from_response(response_text):
    """
    Try to extract a template structure from AI response
    Looks for markdown code blocks or structured content
    """
    import re
    
    # Look for markdown code blocks
    code_blocks = re.findall(r"```(?:markdown)?\n(.*?)\n```", response_text, re.DOTALL)
    
    if code_blocks:
        return {
            "name": "Generated Template",
            "content": code_blocks[0],
            "format": "markdown"
        }
    
    # Look for structured sections
    sections = re.split(r"^#+\s+", response_text, flags=re.MULTILINE)
    if len(sections) > 1:
        return {
            "name": "Generated Template",
            "content": response_text,
            "format": "markdown"
        }
    
    return None


if __name__ == "__main__":
    init_agent()
    app.run(debug=True, host="0.0.0.0", port=5000)
