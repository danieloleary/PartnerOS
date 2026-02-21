# Review of Last 3 Commits

## Scope
Reviewed commits:
1. `0ae1d5f` — **feat: Add partner persistence and management UI**
2. `060bc78` — **docs: Update BACKLOG - LLM working, add partner onboarding**
3. `7ace257` — **feat: Use hardcoded API key, LLM now working**

## Executive Summary
- The direction is good: partner CRUD and UI are meaningful product progress.
- The biggest issue is a **hardcoded live API key** in frontend-delivered code and default server config, which is a critical credential exposure risk.
- Persistence is functional but currently fragile (broad exception handling, no validation/locking) and may break under concurrent writes.

## Commit-by-Commit Review

### 1) `0ae1d5f` — Partner persistence + management UI
**What improved**
- Added a persistent store (`partners.json`) and helper functions for listing/adding/updating partner records.
- Added API routes for listing and creating partners.
- Added a simple in-page partner management UI and modal workflow.

**Strengths**
- Fast path to demonstrable value with low complexity.
- Reasonable separation via `partner_state.py` instead of bloating route handlers.

**Concerns**
- Uses broad bare `except:` in state loading; this can hide data corruption and operational failures.
- File-based storage has no lock/atomic-write behavior, which risks data loss with concurrent requests.
- API endpoints currently accept input without robust validation (e.g., empty name).
- Response surface does not clearly distinguish duplicate create from successful create.

**Recommended next steps**
- Replace bare `except:` with explicit exception types and logging.
- Add pydantic request models for `/api/partners` input validation.
- Use atomic write pattern (temp file + rename) or lightweight DB.
- Return explicit status semantics (e.g., 201 on create, 409 on duplicate).

### 2) `060bc78` — BACKLOG updates
**What improved**
- BACKLOG reflects current product direction and captures follow-up priorities.

**Concerns**
- No major technical concerns; this is a straightforward documentation maintenance commit.

### 3) `7ace257` — hardcoded API key + LLM flow changes
**What improved**
- LLM-first behavior with fallback improves user experience when LLM succeeds.

**Critical concerns**
- Hardcoded OpenRouter key in browser JavaScript exposes the credential to any user.
- Default key fallback in server config means accidental leakage can propagate into deployments.
- Once committed, the key should be treated as compromised and rotated.

**Recommended immediate actions**
1. Revoke/rotate the exposed key immediately.
2. Remove key literals from frontend and backend defaults.
3. Read secret from environment only; fail closed if missing.
4. Add a pre-commit or CI secret scan gate.

## Risk Ranking
1. **Critical**: credential exposure via hardcoded API key.
2. **Medium**: file persistence race/corruption risk.
3. **Low**: input validation/HTTP semantics gaps.

## Overall Assessment
- Product momentum is positive, but security hygiene around secrets must be corrected before broader use.
- With the key handling fixed and basic persistence hardening, this branch is on a solid trajectory.
