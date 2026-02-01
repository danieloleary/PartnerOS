/**
 * Partner Agent Chat Component
 * Embeddable chat interface for template generation and refinement
 * Supports MkDocs integration and standalone use
 */

class PartnerAgentChat {
    constructor(containerSelector, options = {}) {
        this.container = document.querySelector(containerSelector);
        // Try to detect API server - check for custom URL first, then check if /api is available
        this.apiBaseUrl = options.apiBaseUrl || this.detectApiUrl() || '/api';
        this.conversationId = null;
        this.messages = [];
        this.isLoading = false;
        
        if (this.container) {
            this.init();
        }
    }
    
    detectApiUrl() {
        // Try common local development URLs
        const possibleUrls = [
            'http://localhost:5000/api',
            'http://127.0.0.1:5000/api',
            window.location.origin + '/api'
        ];
        
        // Check if we're in production (has long domain)
        if (window.location.hostname.includes('app.github.dev') || window.location.hostname.includes('vercel.app')) {
            // For production deploys, return /api and let the user configure it
            return null;
        }
        
        return null; // Default to relative URL
    }
    
    init() {
        this.render();
        this.attachEventListeners();
        this.generateConversationId();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="partner-agent-chat">
                <div class="chat-header">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3>Partner Agent</h3>
                            <p class="chat-subtitle">Generate & refine partnership templates</p>
                        </div>
                        <button id="settingsBtn" class="btn-settings" title="Settings">⚙️</button>
                    </div>
                    <div id="settingsPanel" class="settings-panel" style="display: none;">
                        <div class="settings-group">
                            <label for="githubToken">GitHub Token (your own):</label>
                            <input type="password" id="githubToken" placeholder="github_pat_..." value="">
                            <small>Your personal GitHub token for GitHub Models API</small>
                            <button id="saveSettings" class="btn-save-settings">Save</button>
                        </div>
                    </div>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message assistant-message">
                        <div class="message-content">
                            <p>👋 Hi! I'm the PartnerOS Partner Agent. I can help you generate, customize, and refine partnership templates.</p>
                            <p>Try asking me things like:</p>
                            <ul>
                                <li>"Generate a recruitment playbook for a new SaaS partner"</li>
                                <li>"Create an enablement plan for enterprise partners"</li>
                                <li>"Help me refine this partner agreement"</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-area">
                    <form id="chatForm" class="chat-form">
                        <textarea 
                            id="messageInput" 
                            class="chat-input" 
                            placeholder="Ask me about partner templates..."
                            rows="3"></textarea>
                        <div class="chat-actions">
                            <button type="submit" class="btn-send">Send</button>
                            <button type="button" class="btn-export" id="exportBtn" style="display:none;">
                                📄 Export as PDF
                            </button>
                        </div>
                    </form>
                </div>
                
                <div class="chat-status" id="chatStatus"></div>
            </div>
        `;
    }
    
    attachEventListeners() {
        const form = document.getElementById('chatForm');
        const input = document.getElementById('messageInput');
        const exportBtn = document.getElementById('exportBtn');
        const settingsBtn = document.getElementById('settingsBtn');
        const settingsPanel = document.getElementById('settingsPanel');
        const saveSettingsBtn = document.getElementById('saveSettings');
        const githubTokenInput = document.getElementById('githubToken');
        
        // Load saved GitHub token
        this.githubToken = localStorage.getItem('partner_agent_github_token') || '';
        if (githubTokenInput && this.githubToken) {
            githubTokenInput.value = this.githubToken;
        }
        
        // Settings toggle
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => {
                settingsPanel.style.display = settingsPanel.style.display === 'none' ? 'block' : 'none';
            });
        }
        
        // Save settings
        if (saveSettingsBtn) {
            saveSettingsBtn.addEventListener('click', () => {
                this.githubToken = githubTokenInput.value;
                localStorage.setItem('partner_agent_github_token', this.githubToken);
                alert('GitHub token saved!');
                settingsPanel.style.display = 'none';
            });
        }
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Auto-resize textarea
        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 150) + 'px';
        });
        
        // Export functionality
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportPdf());
        }
    }
    
    generateConversationId() {
        this.conversationId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        this.isLoading = true;
        input.disabled = true;
        
        // Add user message to UI
        this.addMessage('user', message);
        input.value = '';
        input.style.height = 'auto';
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    conversation_id: this.conversationId,
                    message: message,
                    templates: [],
                    api_key: this.githubToken || undefined  // Pass user's GitHub token if provided
                })
            });
            
            if (!response.ok) {
                if (response.status === 502 || response.status === 503) {
                    throw new Error(`API server not responding. Make sure Flask server is running at ${this.apiBaseUrl}`);
                }
                throw new Error(`API error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add assistant response
            this.addMessage('assistant', data.response);
            
            // Show generated template if available
            if (data.generated_template) {
                this.addTemplate(data.generated_template);
                document.getElementById('exportBtn').style.display = 'inline-block';
            }
            
            // Store in messages history
            this.messages.push({
                role: 'user',
                content: message
            });
            this.messages.push({
                role: 'assistant',
                content: data.response
            });
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('assistant', `❌ Error: ${error.message}\n\n**Setup Required:**\n1. Make sure Flask server is running\n2. Run: \`python scripts/partner_agent/server.py\`\n3. Configure the API URL in settings if deployed`);
        } finally {
            this.isLoading = false;
            input.disabled = false;
            input.focus();
        }
    }
    
    addMessage(role, content) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}-message`;
        
        // Parse markdown-style formatting (simple)
        let formattedContent = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br/>');
        
        messageEl.innerHTML = `
            <div class="message-content">
                ${formattedContent}
            </div>
        `;
        
        messagesContainer.appendChild(messageEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    addTemplate(template) {
        const messagesContainer = document.getElementById('chatMessages');
        const templateEl = document.createElement('div');
        templateEl.className = 'message template-message';
        
        const content = template.content
            .replace(/\n/g, '<br/>')
            .replace(/^#+\s+(.*)$/gm, '<h4>$1</h4>');
        
        templateEl.innerHTML = `
            <div class="template-content">
                <div class="template-header">
                    <strong>📋 Generated Template</strong>
                    <button class="btn-copy" onclick="this.parentElement.parentElement.parentElement.copyTemplate()">Copy</button>
                </div>
                <div class="template-body">
                    ${content}
                </div>
            </div>
        `;
        
        templateEl.copyTemplate = () => {
            const text = template.content;
            navigator.clipboard.writeText(text).then(() => {
                alert('Template copied to clipboard!');
            });
        };
        
        messagesContainer.appendChild(templateEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    async exportPdf() {
        if (!this.conversationId) {
            alert('No conversation to export');
            return;
        }
        
        const partnerName = prompt('Enter partner name (optional):');
        
        try {
            const response = await fetch(
                `${this.apiBaseUrl}/conversations/${this.conversationId}/export/pdf`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        title: partnerName ? `Partner Templates - ${partnerName}` : 'Partner Templates',
                        partner_name: partnerName,
                        include_conversation: confirm('Include conversation history in PDF?')
                    })
                }
            );
            
            if (!response.ok) {
                throw new Error(`Export failed: ${response.status}`);
            }
            
            // Download PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `partner-templates-${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
        } catch (error) {
            console.error('Export error:', error);
            alert('Failed to export PDF: ' + error.message);
        }
    }
}

// Auto-initialize if element with data-partner-agent-chat attribute exists
document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('[data-partner-agent-chat]');
    elements.forEach(el => {
        const apiUrl = el.getAttribute('data-api-url') || '/api';
        new PartnerAgentChat(`#${el.id || 'partner-agent-' + Date.now()}`, {
            apiBaseUrl: apiUrl
        });
    });
});
