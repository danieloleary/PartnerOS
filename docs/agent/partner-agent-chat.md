# Partner Agent

!!! info "API Server Required"
    This page requires the Flask API server to be running. See [Setup Instructions](#setup) below.

!!! info "AI-Powered Template Generation"
    The Partner Agent is an interactive AI assistant that helps you generate, customize, and refine partnership templates in real-time using our partner ecosystem framework.

## Interactive Chat

Start a conversation with the Partner Agent to generate templates tailored to your partner needs. You can:

- **Generate templates** for any stage of the partner lifecycle
- **Refine outputs** through multi-turn conversations
- **Export results** as PDF documents
- **Reference frameworks** from the complete PartnerOS platform

<div id="agent-chat-container" data-partner-agent-chat data-api-url="/api"></div>

## Setup

### Local Development

To use the Partner Agent locally:

1. **Get an API Key** (choose one):
   - [Anthropic Claude](https://console.anthropic.com) - Recommended
   - [GitHub Models](https://github.com/settings/tokens) - Free tier available
   - [OpenAI](https://platform.openai.com/api/keys)

2. **Start Flask Server**:
   ```bash
   cd scripts/partner_agent
   export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE  # Or GITHUB_TOKEN, OPENAI_API_KEY
   pip install -r requirements.txt
   python server.py
   ```

3. **Start Website** (in another terminal):
   ```bash
   mkdocs serve
   ```

4. **Visit**: http://localhost:8000

### Production Deployment

For deploying to production, you'll need to:

1. Deploy the Flask server to a hosting provider (Heroku, AWS, DigitalOcean, etc.)
2. Update the API URL in the chat configuration
3. Set environment variables for your API keys

See the setup guides in `scripts/partner_agent/` directory for detailed deployment instructions.

---

### Basic Workflow

1. **Start a conversation** - Describe your partner type and needs
2. **Get template suggestions** - The agent will recommend relevant templates
3. **Refine together** - Ask follow-up questions to customize templates
4. **Export** - Download the conversation and templates as PDF

### Example Prompts

=== "Recruitment"

    ```
    I'm building a recruitment program for technology partners. We 
    focus on SaaS integrations and need a playbook for identifying 
    and onboarding new partners. Can you help create a recruitment 
    strategy template?
    ```

=== "Enablement"

    ```
    We have 20 enterprise partners at different maturity levels. 
    Create an enablement framework that scales from basic to advanced, 
    with concrete training steps for each stage.
    ```

=== "Strategy"

    ```
    Our partner program is starting. Create an ICP (Ideal Customer 
    Profile) for partners and a business case for why we should 
    invest in partnerships.
    ```

=== "Custom"

    ```
    I have this draft partner agreement. Can you help refine it 
    to be more balanced and fair? Here's the current version: [paste]
    ```

## Features

- **Conversation Memory**: The agent remembers your full conversation context
- **Template Generation**: Outputs are formatted as ready-to-use markdown
- **PDF Export**: Download conversations and templates for sharing
- **Framework Integration**: References PartnerOS templates, playbooks, and best practices
- **Multi-Turn Refinement**: Iteratively improve templates through dialogue

## Templates Reference

The Partner Agent can generate or help refine these templates:

### Strategy
- Partner Business Case
- Ideal Partner Profile (ICP)
- Partner Program Architecture
- Competitive Differentiation Analysis
- Internal Alignment Checklist

### Recruitment
- Email Outreach Sequences
- Discovery Call Playbooks
- Qualification Frameworks
- Pitch Decks
- Partner Proposals
- Onboarding Plans

### Enablement
- Training Programs
- Certification Frameworks
- QBR (Quarterly Business Review) Templates
- Co-marketing Plans
- Technical Integration Guides

### Performance
- Success Metrics & KPIs
- Maturity Model Progression
- Partner Tier Evaluation
- Revenue Tracking

## FAQ

**Q: Can I use templates from my own documents?**  
A: Yes! Paste any document into the chat and ask the agent to refine or adapt it using PartnerOS frameworks.

**Q: Can I export just the templates without conversation history?**  
A: Yes, when exporting to PDF, you can choose to exclude the conversation history.

**Q: Is my data private?**  
A: Conversations are stored temporarily for your session. For production use, [contact us](../getting-started/quick-start.md) about data handling.

**Q: What if the agent doesn't understand my question?**  
A: Try being more specific about:
  - Partner type (tech, reseller, distribution, service, etc.)
  - Program stage (recruitment, enablement, scaling, etc.)
  - Specific outcomes you're looking for

---

## Architecture

The Partner Agent consists of:

- **Backend API** - Flask server handling chat requests, template generation, and PDF export
- **LLM Integration** - Supports GitHub Models, Anthropic Claude, and OpenAI
- **Conversation Engine** - Maintains context across multi-turn interactions
- **Export Pipeline** - Converts templates to formatted PDF documents

## API Documentation

For developers integrating the Partner Agent into custom applications:

```javascript
// Initialize chat interface
const agent = new PartnerAgentChat('#my-chat-container', {
    apiBaseUrl: '/api'
});
```

### Endpoints

- `POST /api/chat` - Send message, get response and generated templates
- `GET /api/conversations/<id>` - Retrieve conversation history
- `POST /api/conversations/<id>/export/pdf` - Export to PDF
- `GET /api/templates` - List available templates
- `GET /health` - API health check

See the [agent configuration](../agent/configuration.md) documentation for setup details.

---

**Ready to build your partner program?** Start chatting with the Partner Agent above! 👆

<script src="/assets/js/partner-agent-chat-client.js"></script>
<link rel="stylesheet" href="/assets/css/partner-agent-chat-styles.css">
