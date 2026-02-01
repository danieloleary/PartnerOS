# Partner Agent Web Server Setup

The Partner Agent runs as a web-based service that powers the chat interface on the PartnerOS website. Follow these steps to get it running locally or deploy it.

## Local Setup

### 1. Install Dependencies

```bash
cd scripts/partner_agent
pip install -r requirements.txt
```

### 2. Configure Provider

Edit `config.yaml` and set your preferred LLM provider:

```yaml
provider: anthropic  # or: github, openai, ollama
model: claude-3.5-sonnet
```

### 3. Set Environment Variable

For **Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

For **GitHub Models:**
```bash
export GITHUB_TOKEN=github_pat_...
```

For **OpenAI:**
```bash
export OPENAI_API_KEY=sk-...
```

For **Ollama** (local):
```bash
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
```

### 4. Start the Server

```bash
python server.py
```

Server runs at `http://localhost:5000`

### 5. Test the API

```bash
# Health check
curl http://localhost:5000/health

# Send a chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-1",
    "message": "Generate a partner recruitment playbook"
  }'
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY scripts/partner_agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/partner_agent . 

ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "server.py"]
```

Build and run:
```bash
docker build -t partner-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 5000:5000 partner-agent
```

### Production with Gunicorn

```bash
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Integration with PartnerOS Website

1. Deploy Flask server to your hosting (Heroku, AWS, Digital Ocean, etc.)
2. Update homepage to point to deployed API:
   ```html
   <div id="agent-chat" data-partner-agent-chat data-api-url="https://your-domain/api"></div>
   ```
3. Update `mkdocs.yml` with deployed API URL in extra config
4. Rebuild and deploy MkDocs site

## API Endpoints

### POST /api/chat

Send a message and get AI response.

**Request:**
```json
{
  "conversation_id": "unique-id",
  "message": "User query",
  "templates": ["recruitment", "enablement"]
}
```

**Response:**
```json
{
  "conversation_id": "unique-id",
  "response": "AI response text",
  "generated_template": {
    "name": "Template Name",
    "content": "Markdown content",
    "format": "markdown"
  },
  "conversation_length": 2,
  "timestamp": "2025-01-31T12:00:00"
}
```

### GET /api/conversations/<id>

Retrieve full conversation history.

**Response:**
```json
{
  "created_at": "2025-01-31T12:00:00",
  "messages": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
  ],
  "templates_generated": [...]
}
```

### POST /api/conversations/<id>/export/pdf

Export conversation and templates as PDF.

**Request:**
```json
{
  "title": "Partner Templates - Acme Corp",
  "partner_name": "Acme Corp",
  "include_conversation": true
}
```

**Response:** PDF file (binary)

### GET /api/templates

List available templates.

**Response:**
```json
{
  "templates": [
    {
      "name": "Partner_Business_Case",
      "filename": "01_Partner_Business_Case.md",
      "path": "partner_blueprint/..."
    }
  ]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "provider": "anthropic"
}
```

## Configuration

Edit `config.yaml`:

```yaml
# Provider: anthropic, github, openai, ollama
provider: anthropic

# Model name
model: claude-3.5-sonnet

# Company context for templates
company:
  name: "Your Company"
  industry: "SaaS"
  size: "Enterprise"

# Partner tiers
partner_tiers:
  - name: "Reseller"
    revenue_share: "20%"
  - name: "Technology"
    revenue_share: "15%"

# Templates directory
templates_dir: "../../partner_blueprint"

# State directory
state_dir: "./state"
```

## Troubleshooting

**No module named 'flask'**
```bash
pip install flask flask-cors
```

**LLM API errors**
- Verify API key is set correctly: `echo $ANTHROPIC_API_KEY`
- Check API key has appropriate permissions
- For GitHub Models, ensure GITHUB_TOKEN has `repo` scope

**CORS errors (if serving from different domain)**
- CORS is enabled by default in server.py
- For additional security, modify `CORS(app)` to restrict origins

**Memory issues with Ollama**
- Reduce conversation history: modify `MAX_CONVERSATIONS` in server.py
- Use a lighter model: `export OLLAMA_MODEL=neural-chat:7b`

## Support

For issues or questions, refer to:
- [Agent Configuration](configuration.md)
- [Playbook Guide](playbooks.md)
- [Enterprise Framework](enterprise-partner-framework.md)
