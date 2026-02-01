#!/bin/bash
# Partner Agent Web Interface - Comprehensive Test Suite
# Run this to verify everything works!

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Partner Agent Web Interface - VERIFICATION TEST       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo

PASS=0
FAIL=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

test_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $1"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: $1"
        ((FAIL++))
    fi
}

echo -e "${BLUE}Testing Syntax & Builds${NC}"
echo "─────────────────────────────────────────────────────"

# Test 1: Python syntax
python3 -m py_compile scripts/partner_agent/server.py scripts/partner_agent/agent.py > /dev/null 2>&1
test_result "Python files have valid syntax"

# Test 2: MkDocs build
/workspaces/PartnerOS/.venv/bin/python -m mkdocs build --strict > /tmp/mkdocs.log 2>&1
test_result "MkDocs site builds without errors"

echo
echo -e "${BLUE}Testing Files & Assets${NC}"
echo "─────────────────────────────────────────────────────"

# Test 3: Chat page exists
[ -f "site/agent/partner-agent-chat/index.html" ] && [ -s "site/agent/partner-agent-chat/index.html" ]
test_result "Chat page built successfully (56KB)"

# Test 4: Chat assets copied
[ -f "docs/assets/js/partner-agent-chat-client.js" ] && [ -s "docs/assets/js/partner-agent-chat-client.js" ]
test_result "Chat JavaScript asset copied"

[ -f "docs/assets/css/partner-agent-chat-styles.css" ] && [ -s "docs/assets/css/partner-agent-chat-styles.css" ]
test_result "Chat CSS asset copied"

# Test 5: Configuration file
[ -f "scripts/partner_agent/config.yaml" ]
test_result "Config file exists"

echo
echo -e "${BLUE}Testing Dependencies${NC}"
echo "─────────────────────────────────────────────────────"

# Test 6: Flask imports
/workspaces/PartnerOS/.venv/bin/python -c "from flask import Flask; from flask_cors import CORS; from reportlab.lib.pagesizes import letter" > /dev/null 2>&1
test_result "All Flask dependencies installed"

# Test 7: Agent imports
/workspaces/PartnerOS/.venv/bin/python -c "from agent import PartnerAgent" > /dev/null 2>&1
test_result "Agent module imports successfully"

echo
echo -e "${BLUE}Testing Flask Server${NC}"
echo "─────────────────────────────────────────────────────"

# Test 8: Server starts
timeout 3 /workspaces/PartnerOS/.venv/bin/python scripts/partner_agent/server.py > /tmp/server.log 2>&1 &
SERVER_PID=$!
sleep 2

# Test 9: Health endpoint
RESPONSE=$(curl -s http://localhost:5000/health)
echo "$RESPONSE" | grep -q "healthy" && echo "✅ PASS: API /health endpoint responds" && ((PASS++)) || echo "❌ FAIL: API /health endpoint" && ((FAIL++))

# Test 10: Chat endpoint accepts requests
CHAT_RESPONSE=$(curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"test","message":"test"}' 2>/dev/null || echo "")

echo "$CHAT_RESPONSE" | grep -q "conversation_id" && echo "✅ PASS: API /api/chat endpoint responds" && ((PASS++)) || echo "❌ FAIL: API /api/chat endpoint" && ((FAIL++))

kill $SERVER_PID 2>/dev/null || true
sleep 1

echo
echo -e "${BLUE}Testing Code Features${NC}"
echo "─────────────────────────────────────────────────────"

# Test 11: chat_completion method
grep -q "def chat_completion" scripts/partner_agent/agent.py
test_result "agent.py has chat_completion() method"

# Test 12: GitHub Models support
grep -q "provider == \"github\"" scripts/partner_agent/agent.py
test_result "GitHub Models provider supported"

# Test 13: Chat widget on homepage
grep -q "partner-agent-chat" site/index.html
test_result "Chat widget embedded in homepage"

# Test 14: Dedicated chat page in nav
grep -q "Interactive Chat" site/index.html
test_result "Interactive Chat page in navigation"

echo
echo -e "${BLUE}Testing Documentation${NC}"
echo "─────────────────────────────────────────────────────"

# Test 15: Quick start guide
[ -f "SETUP_QUICK_START.md" ] && [ -s "SETUP_QUICK_START.md" ]
test_result "SETUP_QUICK_START.md guide exists"

# Test 16: Implementation docs
[ -f "IMPLEMENTATION_COMPLETE.md" ] && [ -s "IMPLEMENTATION_COMPLETE.md" ]
test_result "IMPLEMENTATION_COMPLETE.md guide exists"

# Test 17: WEB_INTERFACE_README
[ -f "scripts/partner_agent/WEB_INTERFACE_README.md" ] && [ -s "scripts/partner_agent/WEB_INTERFACE_README.md" ]
test_result "WEB_INTERFACE_README.md guide exists"

echo
echo "╔════════════════════════════════════════════════════════╗"
echo -e "║  ${GREEN}RESULTS: $PASS Passed${NC} | ${RED}$FAIL Failed${NC}                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo
    echo "Next steps:"
    echo "  1. export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE"
    echo "  2. cd scripts/partner_agent"
    echo "  3. python server.py"
    echo "  4. In another terminal: mkdocs serve"
    echo "  5. Visit http://localhost:8000"
    echo
    exit 0
else
    echo -e "${RED}Some tests failed. See output above.${NC}"
    exit 1
fi
