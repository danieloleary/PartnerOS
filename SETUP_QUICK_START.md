# Partner Agent - Quick Start Guide

## 🎯 You now have a web-based AI partner template generator!

The chat interface lets users generate partnership templates directly on the PartnerOS website.

## ⚡ 5-Minute Setup

### 1. Get an API Key (Pick One)

**Anthropic Claude** (Recommended):
- Go to https://console.anthropic.com
- Create API key
- `export ANTHROPIC_API_KEY=sk-ant-...`

**GitHub Models** (Free for some):
- Go to https://github.com/settings/tokens
- Create token with `repo` scope
- `export GITHUB_TOKEN=github_pat_...`

**OpenAI**:
- Go to https://platform.openai.com/api/keys
- Create API key
- `export OPENAI_API_KEY=sk-...`

### 2. Install & Start

```bash
cd scripts/partner_agent
pip install -r requirements.txt
python server.py
```

Server runs at: `http://localhost:5000`

### 3. Test It

```bash
# Health check
curl http://localhost:5000/health

# Send a chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"test","message":"Create a partner recruitment plan"}'
```

### 4. Preview Site with Chat

```bash
cd /workspaces/PartnerOS
mkdocs serve
```

Visit: `http://localhost:8000` → See chat widget on homepage!

## 📖 Full Documentation

- **Setup Details:** `scripts/partner_agent/SERVER_SETUP.md`
- **Web Interface:** `scripts/partner_agent/WEB_INTERFACE_README.md`
- **Implementation:** `PARTNER_AGENT_WEB_IMPLEMENTATION.md`

## 🚀 Deploy to Production

### Docker
```bash
docker build -t partner-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 5000:5000 partner-agent
```

### Heroku
```bash
git push heroku main
```

### Update Website
In `docs/index.md`, change:
```javascript
data-api-url="YOUR_DEPLOYED_API_URL"
```

## 🎨 What Users Can Do

✅ Chat with AI on the homepage
✅ Generate partnership templates
✅ Refine templates through conversation
✅ Export as PDF
✅ Copy templates to clipboard
✅ Dark mode support
✅ Mobile friendly

## 🏗️ Architecture

```
📱 Website
 ├─ Homepage (chat widget)
 └─ /agent/partner-agent-chat (full interface)
        ↓
🌐 Flask API Server (server.py)
        ↓
🤖 LLM Provider
    ├─ Anthropic Claude
    ├─ GitHub Models
    ├─ OpenAI
    └─ Ollama (local)
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `server.py` | Flask API server |
| `agent.py` | Core agent + chat_completion() |
| `chat-client.js` | Chat widget |
| `config.yaml` | Configuration |
| `requirements.txt` | Dependencies |

## ❓ FAQ

**Q: Do I need a database?**  
A: No, uses in-memory storage. Add one for production if needed.

**Q: Can I use my own LLM?**  
A: Yes, supports Ollama for local models.

**Q: Is it production-ready?**  
A: Yes! Docker support, CORS enabled, error handling included.

**Q: How many conversations can it handle?**  
A: In-memory storage for 100 conversations. Upgrade to DB for more.

**Q: Can users see each other's templates?**  
A: No, conversations are isolated by conversation_id.

## 📞 Support

Check the docs:
- `SERVER_SETUP.md` → Server configuration
- `WEB_INTERFACE_README.md` → Features & API
- `PARTNER_AGENT_WEB_IMPLEMENTATION.md` → Full implementation details

## 🎉 That's it!

You have a fully functional web-based AI partner template generator. Start the server and visit the site to see it in action!

```bash
python scripts/partner_agent/server.py &
mkdocs serve
```

Then visit: `http://localhost:8000` 🚀
