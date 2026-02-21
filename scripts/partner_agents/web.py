#!/usr/bin/env python3
"""
PartnerOS Web Interface
A beautiful web UI for the multi-agent partner team.
"""

import os
import sys

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx

from partner_agents.drivers import (
    DanAgent,
    ArchitectAgent,
    StrategistAgent,
    EngineAgent,
    SparkAgent,
    ChampionAgent,
    BuilderAgent,
)
from partner_agents import Orchestrator

# Get API key from environment
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

app = FastAPI(title="PartnerOS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
agents = {
    "dan": DanAgent(),
    "architect": ArchitectAgent(),
    "strategist": StrategistAgent(),
    "engine": EngineAgent(),
    "spark": SparkAgent(),
    "champion": ChampionAgent(),
    "builder": BuilderAgent(),
}

orchestrator = Orchestrator()
for name, agent in agents.items():
    orchestrator.register_driver(agent)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PartnerOS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .gradient-bg {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }
        .agent-card { transition: all 0.2s ease; }
        .agent-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
        .typing-indicator span {
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        .message-enter { animation: slideIn 0.3s ease; }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body class="gradient-bg min-h-screen text-white">
    <div class="max-w-6xl mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2">
                PartnerOS
            </h1>
            <p class="text-slate-400">Your AI Partner Team</p>
        </header>

        <!-- Team Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-8">
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">👑</div>
                <div class="font-semibold text-cyan-400">DAN</div>
                <div class="text-xs text-slate-500">The Owner</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">🏗️</div>
                <div class="font-semibold text-cyan-400">ARCHITECT</div>
                <div class="text-xs text-slate-500">Program Manager</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">🎯</div>
                <div class="font-semibold text-cyan-400">STRATEGIST</div>
                <div class="text-xs text-slate-500">Strategy</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">⚙️</div>
                <div class="font-semibold text-cyan-400">ENGINE</div>
                <div class="text-xs text-slate-500">Operations</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">✨</div>
                <div class="font-semibold text-cyan-400">SPARK</div>
                <div class="text-xs text-slate-500">Marketing</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">🏆</div>
                <div class="font-semibold text-cyan-400">CHAMPION</div>
                <div class="text-xs text-slate-500">Leader</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-xl p-4 text-center border border-slate-700">
                <div class="text-2xl mb-1">🔧</div>
                <div class="font-semibold text-cyan-400">BUILDER</div>
                <div class="text-xs text-slate-500">Technical</div>
            </div>
        </div>

        <!-- Chat Container -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 overflow-hidden">
            <!-- Messages -->
            <div id="messages" class="h-96 overflow-y-auto p-6 space-y-4">
                <div class="message-enter flex gap-3">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">🤖</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">
                        <p class="text-sm">Welcome to PartnerOS! 👋</p>
                        <p class="text-sm mt-2 text-slate-300">I'm connected to your AI partner team. What would you like to do?</p>
                        <div class="mt-3 flex flex-wrap gap-2">
                            <button onclick="sendMessage('Onboard Acme Corp as Gold partner')" class="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 rounded-full text-xs transition">Onboard partner</button>
                            <button onclick="sendMessage('Register a deal for TechCorp, $50000')" class="px-3 py-1 bg-purple-600 hover:bg-purple-500 rounded-full text-xs transition">Register deal</button>
                            <button onclick="sendMessage('Launch a welcome campaign')" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 rounded-full text-xs transition">Launch campaign</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input -->
            <div class="border-t border-slate-700 p-4">
                <div class="flex gap-3">
                    <input 
                        id="messageInput"
                        type="text" 
                        placeholder="Type your message..." 
                        class="flex-1 bg-slate-700/50 border border-slate-600 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-500 transition"
                        onkeypress="if(event.key==='Enter')sendMessage()"
                    >
                    <button 
                        onclick="sendMessage()"
                        class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-xl font-semibold hover:opacity-90 transition"
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>

        <!-- Status -->
        <div class="text-center mt-6 text-slate-500 text-sm">
            <span id="status">● Ready</span> • 7 Agents • 36 Skills • LLM Connected
        </div>
    </div>

    <script>
        let apiKey = localStorage.getItem('minimax_api_key') || '';
        
        if (!apiKey) {
            apiKey = prompt('Enter your Minimax API key:');
            if (apiKey) localStorage.setItem('minimax_api_key', apiKey);
        }

        async function sendMessage(text) {
            const input = document.getElementById('messageInput');
            const message = text || input.value.trim();
            if (!message) return;
            
            input.value = '';
            
            // Add user message
            addMessage(message, 'user');
            
            // Show typing
            showTyping();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message, apiKey})
                });
                
                const data = await response.json();
                hideTyping();
                addMessage(data.response, 'assistant', data.agent);
            } catch (e) {
                hideTyping();
                addMessage('Error: ' + e.message, 'assistant');
            }
        }
        
        function addMessage(text, role, agent = null) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message-enter flex gap-3';
            
            if (role === 'user') {
                div.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center flex-shrink-0">👤</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">${text}</div>
                `;
            } else {
                const emoji = agent === 'ARCHITECT' ? '🏗️' : 
                              agent === 'ENGINE' ? '⚙️' : 
                              agent === 'SPARK' ? '✨' : 
                              agent === 'CHAMPION' ? '🏆' : 
                              agent === 'BUILDER' ? '🔧' : 
                              agent === 'STRATEGIST' ? '🎯' : '👑';
                div.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">${emoji}</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg">${text}</div>
                `;
            }
            
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function showTyping() {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.id = 'typing';
            div.className = 'message-enter flex gap-3';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center flex-shrink-0">🤖</div>
                <div class="bg-slate-700/50 rounded-xl p-4">
                    <div class="typing-indicator flex gap-1">
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                        <span class="w-2 h-2 bg-slate-400 rounded-full"></span>
                    </div>
                </div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
    </script>
</body>
</html>"""


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    api_key = data.get("apiKey", MINIMAX_API_KEY)

    if not api_key:
        return JSONResponse(
            {
                "response": "⚠️ No API key configured. Set MINIMAX_API_KEY environment variable.",
                "agent": "system",
            }
        )

    # Route to LLM
    try:
        response = await call_llm(user_message, api_key)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}", "agent": "system"})


async def call_llm(message: str, api_key: str) -> dict:
    """Call Minimax LLM with partner context."""
    import httpx

    # Build context about agents
    system_prompt = """You are the orchestrator of PartnerOS - an AI partner team. 
You have 7 specialized agents:
- DAN: The Owner (runs everything, makes decisions)
- ARCHITECT: Partner Program Manager (owns relationships, onboarding)
- STRATEGIST: Partner Strategy (ICP, tiers, selection)
- ENGINE: Partner Operations (deals, commissions, portal)
- SPARK: Partner Marketing (campaigns, leads, content)
- CHAMPION: Partner Leader (board decks, ROI, exec comms)
- BUILDER: Partner Technical (integrations, APIs, docs)

When user asks something, respond as the most appropriate agent(s).
Be helpful, concise, and actionable. Format responses nicely."""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.minimax.chat/v1/text/chatcompletion_pro",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "abab6.5s-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                return {
                    "response": f"API Error: {response.text[:200]}",
                    "agent": "system",
                }

            result = response.json()
            reply = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response")
            )

            return {"response": reply, "agent": "CHAMPION"}

        except Exception as e:
            return {"response": f"LLM Error: {str(e)}", "agent": "system"}


if __name__ == "__main__":
    print("🚀 Starting PartnerOS Web Interface...")
    print("   Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
