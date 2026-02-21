# Sentinel's Journal - Critical Security Learnings

## 2025-05-15 - Hardcoded Credentials and Frontend XSS in Partner Web Agent
**Vulnerability:** Found a hardcoded OpenRouter API key (`sk-or-v1-...`) in `scripts/partner_agents/web.py` and multiple XSS vectors where user input and agent responses were rendered via `innerHTML`.
**Learning:** Prototyping scripts often bypass standard security controls (like `.env` usage) for convenience, leading to credential leakage and insecure rendering patterns when they evolve into shared tools.
**Prevention:** Enforce environment variable usage for all secrets regardless of script "status". Use strict HTML escaping or `textContent` for dynamic DOM updates to prevent XSS.
