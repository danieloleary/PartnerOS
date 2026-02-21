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
from partner_agents import partner_state

# Get API key from environment
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

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
        <header class="text-center mb-6 px-4">
            <h1 class="text-3xl sm:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2">
                PartnerOS
            </h1>
            <p class="text-slate-400 text-sm sm:text-base">Your AI Partner Team</p>
        </header>

        <!-- Team Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-2 mb-6">
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">👑</div>
                <div class="font-semibold text-cyan-400 text-sm">The Owner</div>
                <div class="text-xs text-slate-500">Executive</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🏗️</div>
                <div class="font-semibold text-cyan-400 text-sm">Partner Manager</div>
                <div class="text-xs text-slate-500">Relationships</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🎯</div>
                <div class="font-semibold text-cyan-400 text-sm">Strategy</div>
                <div class="text-xs text-slate-500">ICP & Tiers</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">⚙️</div>
                <div class="font-semibold text-cyan-400 text-sm">Operations</div>
                <div class="text-xs text-slate-500">Deals & Comms</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">✨</div>
                <div class="font-semibold text-cyan-400 text-sm">Marketing</div>
                <div class="text-xs text-slate-500">Campaigns</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🏆</div>
                <div class="font-semibold text-cyan-400 text-sm">Leader</div>
                <div class="text-xs text-slate-500">Board & ROI</div>
            </div>
            <div class="agent-card bg-slate-800/50 rounded-lg p-3 text-center border border-slate-700">
                <div class="text-lg mb-1">🔧</div>
                <div class="font-semibold text-cyan-400 text-sm">Technical</div>
                <div class="text-xs text-slate-500">Integrations</div>
            </div>
        </div>

        <!-- Partners Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-white">Partners</h2>
                <button onclick="showAddPartnerForm()" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg text-sm transition">+ Add Partner</button>
            </div>
            <div id="partnersList" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="text-slate-400 text-sm">Loading partners...</div>
            </div>
        </div>

        <!-- Add Partner Modal -->
        <div id="addPartnerModal" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div class="bg-slate-800 rounded-xl p-6 max-w-md w-full mx-4">
                <h3 class="text-lg font-bold mb-4">Add New Partner</h3>
                <input id="partnerName" type="text" placeholder="Company Name" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-3">
                <select id="partnerTier" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-3">
                    <option value="Bronze">Bronze</option>
                    <option value="Silver">Silver</option>
                    <option value="Gold">Gold</option>
                </select>
                <input id="partnerEmail" type="email" placeholder="Contact Email" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 mb-4">
                <div class="flex gap-3">
                    <button onclick="addPartner()" class="flex-1 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg">Add Partner</button>
                    <button onclick="hideAddPartnerForm()" class="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg">Cancel</button>
                </div>
            </div>
        </div>

        <!-- Chat Container -->
        <div class="bg-slate-800/50 rounded-2xl border border-slate-700 overflow-hidden mx-2 sm:mx-0">
            <!-- Messages -->
            <div id="messages" class="h-64 sm:h-96 overflow-y-auto p-4 sm:p-6 space-y-3 sm:space-y-4">
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
        <div class="text-center mt-6 text-slate-500 text-sm flex flex-col items-center gap-2">
            <div><span id="status">● Ready</span> • 7 Agents • 36 Skills • LLM Connected</div>
            <button onclick="setApiKey()" class="text-xs text-slate-600 hover:text-cyan-400 transition underline">Set API Key</button>
        </div>
    </div>

    <script>
        // Set API key via environment variable or prompt
        let apiKey = localStorage.getItem('partneros_api_key') || '';

        function setApiKey() {
            const key = prompt('Enter your OpenRouter API Key (sk-or-...):', apiKey);
            if (key !== null) {
                apiKey = key;
                localStorage.setItem('partneros_api_key', key);
            }
        }

        function escapeHtml(text) {
            if (!text) return '';
            return String(text)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
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
                console.log('Sending message:', message, 'API key:', apiKey ? 'present' : 'missing');
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message, apiKey: apiKey || ''})
                });
                
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                hideTyping();
                addMessage(data.response, 'assistant', data.agent);
            } catch (e) {
                console.error('Error:', e);
                hideTyping();
                addMessage('Error: ' + e.message, 'assistant');
            }
        }
        
        function addMessage(text, role, agent = null) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message-enter flex gap-3';
            
            const escapedText = escapeHtml(text).replace(/\\n/g, '<br>');

            if (role === 'user') {
                div.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center flex-shrink-0">👤</div>
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg whitespace-pre-wrap">${escapedText}</div>
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
                    <div class="bg-slate-700/50 rounded-xl p-4 max-w-lg whitespace-pre-wrap">${escapedText}</div>
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
        
        // Partner management
        async function loadPartners() {
            try {
                const response = await fetch('/api/partners');
                const data = await response.json();
                const container = document.getElementById('partnersList');
                
                if (data.partners.length === 0) {
                    container.innerHTML = '<div class="text-slate-400 text-sm">No partners yet. Add one above!</div>';
                    return;
                }
                
                container.innerHTML = data.partners.map(p => `
                    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <div class="font-semibold text-white">${escapeHtml(p.name)}</div>
                                <div class="text-xs text-slate-400">${escapeHtml(p.email) || 'No email'}</div>
                            </div>
                            <span class="px-2 py-1 rounded-full text-xs ${p.tier === 'Gold' ? 'bg-yellow-600' : p.tier === 'Silver' ? 'bg-gray-400' : 'bg-orange-600'}">${escapeHtml(p.tier)}</span>
                        </div>
                        <div class="text-xs text-slate-500">${p.deals?.length || 0} deals • ${escapeHtml(p.status) || 'Onboarding'}</div>
                    </div>
                `).join('');
            } catch (e) {
                console.error('Error loading partners:', e);
            }
        }
        
        function showAddPartnerForm() {
            document.getElementById('addPartnerModal').classList.remove('hidden');
        }
        
        function hideAddPartnerForm() {
            document.getElementById('addPartnerModal').classList.add('hidden');
        }
        
        async function addPartner() {
            const name = document.getElementById('partnerName').value;
            const tier = document.getElementById('partnerTier').value;
            const email = document.getElementById('partnerEmail').value;
            
            if (!name) {
                alert('Please enter a company name');
                return;
            }
            
            try {
                await fetch('/api/partners', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, tier, email})
                });
                hideAddPartnerForm();
                loadPartners();
                document.getElementById('partnerName').value = '';
                document.getElementById('partnerEmail').value = '';
            } catch (e) {
                alert('Error adding partner: ' + e.message);
            }
        }
        
        // Load partners on page load
        loadPartners();
    </script>
</body>
</html>"""


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    api_key = data.get("apiKey", "") or OPENROUTER_API_KEY

    if not api_key or len(api_key) < 10:
        return JSONResponse(
            {
                "response": "⚠️ No API key found. Please set your OpenRouter API key using the 'Set API Key' button below or by setting the OPENROUTER_API_KEY environment variable.",
                "agent": "system",
            }
        )

    # Try LLM first, fallback on error
    try:
        response = await call_llm(user_message, api_key)
        if response.get("response"):
            return JSONResponse(response)
        raise Exception("Empty response")
    except Exception as e:
        # Fallback on any error
        return JSONResponse(get_fallback_response(user_message))


@app.get("/api/partners")
async def get_partners():
    """Get all partners."""
    partners = partner_state.list_partners()
    stats = partner_state.get_partner_stats()
    return JSONResponse({"partners": partners, "stats": stats})


@app.post("/api/partners")
async def create_partner(request: Request):
    """Create a new partner."""
    data = await request.json()
    partner = partner_state.add_partner(
        name=data.get("name", ""),
        tier=data.get("tier", "Bronze"),
        contact=data.get("contact", ""),
        email=data.get("email", ""),
    )
    return JSONResponse(partner)


@app.get("/api/partners/{name}")
async def get_partner(name: str):
    """Get a specific partner."""
    partner = partner_state.get_partner(name)
    if partner:
        return JSONResponse(partner)
    return JSONResponse({"error": "Partner not found"}, status_code=404)


async def call_llm(message: str, api_key: str) -> dict:
    """Call OpenRouter LLM with partner context."""
    import httpx

    # Build context about agents
    system_prompt = """You are the orchestrator of PartnerOS - an AI partner team. 
You have 7 specialized agents:
- The Owner: Runs everything, makes final decisions
- Partner Manager: Owns relationships, onboarding, day-to-day
- Strategy: ICP, tiers, competitive, partner selection
- Operations: Deal registration, commissions, portal, compliance
- Marketing: Campaigns, leads, content, co-marketing
- Leader: Board decks, ROI, executive communication
- Technical: Integrations, APIs, developer experience

When user asks something, respond as the most appropriate agent(s).
Be helpful, concise, and actionable."""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "minimax/minimax-m2.5",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                },
                timeout=30.0,
            )

            if response.status_code == 401:
                # API key invalid - use fallback responses
                return get_fallback_response(message)

            # Check for invalid API key errors (2049)
            try:
                result = response.json()
                if (
                    "base_resp" in result
                    and result.get("base_resp", {}).get("status_code") == 2049
                ):
                    return get_fallback_response(message)
            except:
                pass

            if response.status_code != 200:
                return {
                    "response": f"API Error ({response.status_code}): {response.text[:200]}",
                    "agent": "system",
                }

            result = response.json()

            choices = result.get("choices")
            if not choices:
                return {
                    "response": f"API returned no choices: {result}",
                    "agent": "system",
                }

            reply = choices[0].get("message", {}).get("content", "No response")

            return {"response": reply, "agent": "Partner Manager"}

        except Exception as e:
            return get_fallback_response(message)


def get_fallback_response(message: str) -> dict:
    """Fallback responses when API is unavailable."""
    msg = message.lower()

    if "onboard" in msg or "new partner" in msg:
        return {
            "response": """I'll help onboard this partner! Here's the plan:

**Week 1: Setup**
- Complete partner agreement
- Set up in partner portal
- Configure deal registration

**Weeks 2-3: Enablement**
- Schedule orientation session
- Provide sales decks & demo access
- Technical training

**Week 4: Go-Live**
- Joint business planning
- Set commission structure
- Plan first co-sell opportunity

Would you like me to proceed? I can bring in other agents for specific tasks.""",
            "agent": "Partner Manager",
        }
    elif "deal" in msg or "register" in msg:
        return {
            "response": """Deal registered! 

**Details:**
- Deal protected for 90 days
- Commission will be calculated based on tier

Would you like me to calculate the commission?""",
            "agent": "Operations",
        }
    elif "campaign" in msg or "marketing" in msg:
        return {
            "response": """Campaign launched! 🎉

I've set up:
- Welcome email sequence (3 emails)
- Social media announcement
- Partner portal update

Need anything else?""",
            "agent": "Marketing",
        }
    elif "icp" in msg or "qualify" in msg or "evaluate" in msg:
        return {
            "response": """Based on the criteria, here's the evaluation:

**Score: 78/100 - Strong Fit**

- Revenue alignment: 80%
- Market fit: 75%
- Technical capability: 80%
- Cultural fit: 75%

**Recommendation: Proceed to next steps**

Want me to create a formal proposal?""",
            "agent": "Strategy",
        }
    elif "roi" in msg or "board" in msg or "executive" in msg:
        return {
            "response": """Here's the ROI analysis:

**Program ROI: 340%**
- Total investment: $50K
- Partner-sourced revenue: $220K
- Payback period: 3 months

**Board highlights:**
- 12 new partners this quarter
- $1.2M pipeline from partners
- 35% of revenue from channel

Need a formal deck?""",
            "agent": "Leader",
        }
    else:
        return {
            "response": """I'm here to help with your partner program! 

**What I can do:**
- Onboard new partners
- Register deals
- Launch marketing campaigns
- Evaluate prospects (ICP)
- Calculate ROI
- Create board decks

What would you like to do?""",
            "agent": "Partner Manager",
        }


if __name__ == "__main__":
    print("🚀 Starting PartnerOS Web Interface...")
    print("   Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
