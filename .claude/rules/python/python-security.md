---
paths:
  - "**/*.py"
---

# Secrets
- Never hardcode secrets, API keys, tokens, or passwords — use `.env` or `python-vault`.
- Never commit `.env` files — always add to `.gitignore`.
- Environment variables must be `UPPER_SNAKE_CASE`.
- If a secret is accidentally committed — rotate it immediately, do not just delete it.

# Input Validation
- Validate and sanitize all external inputs at system boundaries (APIs, CLI, file input).
- Reject invalid input early — fail fast before any side effects occur.
- Never trust user input — treat all external data as untrusted.
- Use Pydantic models for structured input validation at API boundaries.

# Authentication & Authorization
- Never implement custom auth logic — use established libraries and frameworks.
- Always check authorization at the service layer, not just the route handler.
- Apply least privilege — grant minimum necessary permissions for all services, users, and roles.
- Never expose internal user IDs or sensitive identifiers in public APIs.

# Code Practices
- Never log sensitive data — no passwords, tokens, or PII in logs.
- Use parameterized queries — never string-format SQL.
- Avoid `eval()`, `exec()`, and dynamic code execution with untrusted input.
- Never use `pickle.loads()` with untrusted or user-supplied data — use `json` or `msgpack` instead.
- Never use `subprocess` with `shell=True` and any user-controlled input.
- Set timeouts on all external calls — never wait indefinitely.
- Configure CORS explicitly — never use wildcard origins (`*`) in production FastAPI/Django apps.

# Dependencies
- Pin dependency versions in production — avoid floating versions (`>=`, `*`).
- Remove unused dependencies — every dependency is an attack surface.
