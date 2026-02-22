---
title: Sentinel's Journal - Critical Security Learnings
keywords: ["partner management vulnerability", "application was vulnerable", "monolithic string within", "csrf like attacks", "rendered using innerhtml", "partners json"]
---
# Sentinel's Journal - Critical Security Learnings

## 2025-05-15 - Stored XSS in Partner Management
**Vulnerability:** The application was vulnerable to Stored Cross-Site Scripting (XSS). User-provided partner names and emails were stored unsanitized in `partners.json` and rendered using `innerHTML` in the FastAPI-based web interface (`web.py`).
**Learning:** Embedding complex HTML/JS as a monolithic string within a Python file (`web.py`) obscures vulnerabilities from standard static analysis tools and makes manual review harder. Developers may mistakenly trust backend data when it's easily accessible via a shared state module like `partner_state.py`.
**Prevention:** Always escape dynamic content on both the backend (producer) and frontend (consumer). Use `textContent` or similar DOM-safe methods instead of `innerHTML` for dynamic values. Implement input validation and sanitization at the API boundary.

## 2025-05-15 - Insecure CORS Configuration
**Vulnerability:** `CORSMiddleware` was configured with `allow_origins=["*"]` and `allow_credentials=True`.
**Learning:** This is an insecure combination that is rejected by modern browsers and can lead to CSRF-like attacks if sensitive data is involved.
**Prevention:** When using wildcard origins (`*`), always set `allow_credentials=False`. If credentials are required, specific origins must be listed.
