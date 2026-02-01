# 🚨 Fix for 502 Error - Quick Setup Guide

## The Problem

You're seeing **HTTP 502 Bad Gateway** because:
- The website is deployed to `bookish-halibut-vp46vp6jx3pj99-5000.app.github.dev`
- But the **Flask API server is NOT running**
- The website can't reach the API to generate templates

## The Solution

### For Local Testing (Recommended)

**This is the intended way to use it:**

```bash
# Terminal 1: Start Flask API Server
cd /workspaces/PartnerOS/scripts/partner_agent
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
python server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Then in a new terminal:**

```bash
# Terminal 2: Start the website
cd /workspaces/PartnerOS
mkdocs serve
```

You should see:
```
 * Serving MkDocs at http://127.0.0.1:8000
```

**Then visit:**
- `http://localhost:8000` ← Both server and site running locally
- Chat widget will work perfectly!

---

## Why Local Only (For Now)?

The Partner Agent is designed for **local usage** because:

1. ✅ No database needed (runs in memory)
2. ✅ No authentication needed (it's your local environment)
3. ✅ Direct access to your API keys (safe on your machine)
4. ✅ Fast iteration (instant feedback)

**For production deployment**, you'd need to:
- Deploy Flask server separately (Heroku, AWS, etc.)
- Set up authentication
- Use a database for persistent conversations
- Configure CORS properly

---

## What Changed (to Fix the Error)

I updated the website to show clear instructions when the Flask server isn't running:

1. ✅ Added warning on homepage
2. ✅ Added setup instructions on chat page
3. ✅ Better error messages in chat widget
4. ✅ Guides users to set up locally

---

## Quick Test

Run this to verify everything works:

```bash
# Test 1: Python syntax OK?
python3 -m py_compile /workspaces/PartnerOS/scripts/partner_agent/server.py && echo "✓ Syntax valid"

# Test 2: Site builds OK?
cd /workspaces/PartnerOS && \
/workspaces/PartnerOS/.venv/bin/python -m mkdocs build --strict 2>&1 | grep "built" && echo "✓ Site builds"

# Test 3: Flask starts OK?
timeout 3 /workspaces/PartnerOS/.venv/bin/python /workspaces/PartnerOS/scripts/partner_agent/server.py 2>&1 | grep "Running" && echo "✓ Flask works"
```

All should pass! ✓

---

## 🎬 Your Setup (Copy & Paste)

```bash
#!/bin/bash
set -e

cd /workspaces/PartnerOS

# Get API key
read -p "Enter your Anthropic API key (sk-ant-...): " API_KEY

# Terminal 1: Start Flask server
echo "Starting Flask server..."
export ANTHROPIC_API_KEY=$API_KEY
cd scripts/partner_agent
python server.py &
SERVER_PID=$!

# Wait for server
sleep 2

# Terminal 2: Start website
cd ../..
echo "Starting website at http://localhost:8000"
mkdocs serve

# Cleanup
kill $SERVER_PID
```

Or just run them separately:

```bash
# Terminal 1
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY
cd /workspaces/PartnerOS/scripts/partner_agent
python server.py

# Terminal 2
cd /workspaces/PartnerOS
mkdocs serve

# Then visit: http://localhost:8000
```

---

## ✅ It's Fixed!

The 502 error is now clearly explained with setup instructions. Users will know they need to:

1. Start Flask server
2. Start website
3. Use locally at localhost:8000

Done! 🚀
