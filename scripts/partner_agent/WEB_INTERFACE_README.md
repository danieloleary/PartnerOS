# Partner Agent - Web Interface

## Overview

The Partner Agent is now available as a **web-based chat interface** integrated directly into the PartnerOS website. Users can generate, customize, and refine partnership templates through conversational AI without leaving the browser.

## Features

✨ **Interactive Chat Interface**
- Multi-turn conversations with full context memory
- Real-time template generation
- Copy-to-clipboard for generated templates

📄 **Template Export**
- Export templates + conversation history as PDF
- Download formatted markdown
- Share templates with team members

🤖 **AI-Powered**
- Supports GitHub Models, Anthropic Claude, OpenAI, and Ollama
- Context-aware responses based on PartnerOS framework
- Multi-turn refinement of templates

🚀 **Easy Deployment**
- Standalone Flask web server
- Docker support
- Production-ready with Gunicorn
- CORS enabled for website integration

## Quick Start

### For Website Users

1. Visit the **PartnerOS website**
2. Go to **Partner Agent** section or use the chat widget on the homepage
3. Start typing your request
4. Generate templates through conversation
5. Export as PDF or copy individual templates

### For Developers/Self-Hosting

#### 1. Install Dependencies
```bash
cd scripts/partner_agent
pip install -r requirements.txt
```

#### 2. Configure LLM Provider

Set one of:
```bash
# Anthropic Claude (recommended)
export ANTHROPIC_API_KEY=sk-ant-...

# GitHub Models
export GITHUB_TOKEN=github_pat_...

# OpenAI
export OPENAI_API_KEY=sk-...
```

#### 3. Start the Server
```bash
python server.py
```

Server runs on `http://localhost:5000`

#### 4. Test
```bash
# Health check
curl http://localhost:5000/health

# Send a message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test",
    "message": "Create a partner recruitment playbook"
  }'
```

## Architecture

```
┌─────────────────────────────────────────┐
│  PartnerOS Website (MkDocs)             │
│  ├─ Homepage with chat widget           │
│  ├─ /agent/partner-agent-chat page      │
│  └─ Full documentation                  │
└──────────────┬──────────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────────┐
│  Flask Web Server (server.py)           │
│  ├─ /api/chat - Main chat endpoint      │
│  ├─ /api/conversations - History        │
│  ├─ /api/templates - Available templates│
│  └─ /api/export/pdf - PDF generation    │
└──────────────┬──────────────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
   Anthropic  OpenAI  Ollama
```

## File Structure

```
scripts/partner_agent/
├── agent.py              # Core agent logic + chat_completion method
├── server.py             # Flask web server with API endpoints
├── chat-client.js        # Frontend chat widget (embedded in site)
├── chat-styles.css       # Styling for chat interface
├── config.yaml           # Configuration (provider, company context, etc)
├── requirements.txt      # Python dependencies
├── SERVER_SETUP.md       # Detailed server setup guide
└── state/                # Conversation state (local storage)

docs/
├── agent/
│   └── partner-agent-chat.md  # Interactive chat page
├── assets/
│   ├── js/
│   │   └── partner-agent-chat-client.js
│   └── css/
│       └── partner-agent-chat-styles.css
└── index.md              # Updated homepage with chat widget
```

## API Endpoints

### POST /api/chat
Send a message, get response and generated templates.

**Request:**
```json
{
  "conversation_id": "unique-conv-id",
  "message": "Generate a recruitment playbook",
  "templates": ["recruitment", "enablement"]
}
```

**Response:**
```json
{
  "conversation_id": "unique-conv-id",
  "response": "Here's a recruitment playbook...",
  "generated_template": {
    "name": "Recruitment Playbook",
    "content": "# Recruitment Playbook\n...",
    "format": "markdown"
  },
  "conversation_length": 1,
  "timestamp": "2025-01-31T12:00:00"
}
```

### GET /api/conversations/<id>
Retrieve full conversation history.

### POST /api/conversations/<id>/export/pdf
Export conversation + templates as PDF.

**Request:**
```json
{
  "title": "Partner Templates - Acme Corp",
  "partner_name": "Acme Corp",
  "include_conversation": true
}
```

### GET /api/templates
List available templates.

### GET /health
Health check - returns provider and status.

## Configuration

Edit `config.yaml`:

```yaml
# LLM Provider: anthropic, github, openai, ollama
provider: anthropic

# Model to use
model: claude-3.5-sonnet

# Company context for personalized templates
company:
  name: "Your Company"
  industry: "SaaS"
  size: "Enterprise"

# Partner program tiers
partner_tiers:
  - name: "Reseller"
    revenue_share: "20%"
    support_level: "Standard"
  - name: "Technology"
    revenue_share: "15%"
    support_level: "Premium"

# Directories
templates_dir: "../../partner_blueprint"
state_dir: "./state"
```

## Usage Examples

### Example 1: Generate Recruitment Strategy
```
User: "We're a B2B SaaS platform. Create a recruitment playbook 
to find and qualify technology partners."

Agent: [Generates recruitment playbook with qualification criteria, 
outreach templates, discovery call scripts, etc.]

User: "Can you make the qualification criteria more focused on 
companies with existing customer bases?"

Agent: [Refines the playbook with updated criteria]
```

### Example 2: Refine Existing Template
```
User: "Here's our current partner agreement. Can you review it 
using PartnerOS best practices?"

[User pastes agreement]

Agent: [Reviews and provides recommendations]

User: "Export this conversation and the updated agreement."

Agent: [Generates PDF with conversation history + refined agreement]
```

### Example 3: Build Enablement Program
```
User: "Create an enablement roadmap for scaling from 5 to 50 
technology partners."

Agent: [Creates roadmap with stages, training programs, metrics]

User: "Add certification framework"

Agent: [Adds certification module to roadmap]

User: "Download as PDF"

Agent: [Exports complete enablement program]
```

## Deployment

### Local Development
```bash
python server.py
# Access at http://localhost:5000
```

### Docker
```bash
docker build -t partner-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 5000:5000 partner-agent
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Cloud Platforms

**Heroku:**
```bash
git push heroku main
```

**AWS Lambda:**
- Use Zappa or similar WSGI adapter
- Configure environment variables in Lambda

**Docker on EC2/DigitalOcean:**
```bash
docker run -d \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -p 80:5000 \
  partner-agent
```

## Troubleshooting

### Chat returns errors
- **"LLM client not initialized"** → Set API key (ANTHROPIC_API_KEY, GITHUB_TOKEN, etc.)
- **"Provider not recognized"** → Check config.yaml `provider` field
- **"API Error"** → Verify API key has correct permissions

### Cannot access from website
- Check CORS is enabled (it is by default in server.py)
- Verify API URL in frontend points to correct server
- Check firewall/security group allows incoming connections

### Templates not generating
- Ensure agent has conversation context (multi-turn conversation)
- Try more specific prompts about template type and partner type
- Check that templates directory exists: `../../partner_blueprint`

### Slow responses
- Reduce `MAX_CONVERSATIONS` in server.py to free memory
- Use a faster model (e.g., claude-3-haiku instead of sonnet)
- For Ollama, use a smaller model

## Next Steps

1. **Deploy the server** - Follow deployment guide above
2. **Configure the LLM provider** - Set ANTHROPIC_API_KEY or other provider
3. **Test the API** - Use curl to verify endpoints work
4. **Update website** - Point chat widget to deployed server
5. **Monitor usage** - Watch logs for errors and performance metrics

## Support & Feedback

For issues or questions:
- Check [Agent Configuration](agent/configuration.md) docs
- Review [Playbook Guide](agent/playbooks.md)
- See [Enterprise Framework](agent/enterprise-partner-framework.md)
- Open an issue on [GitHub](https://github.com/danieloleary/PartnerOS)

---

**Built with ❤️ for partnership teams**
