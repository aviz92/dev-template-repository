---
paths:
  - "**/Dockerfile"
  - "**/Dockerfile.*"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/.dockerignore"
---

# Image Hygiene
- Use minimal base images — prefer `python:3.x-slim` or `distroless` over full images.
- Always pin base image versions — never use `latest` in production.
- Add a `.dockerignore` — exclude `.env`, `__pycache__`, `.git`, secrets, and dev artifacts.

# Runtime Security
- Run containers as a non-root user — always add `USER` directive with a named non-root user.
- Drop unnecessary Linux capabilities — use `--cap-drop=ALL` and add back only what's needed.
- Mount secrets at runtime via environment variables or secret managers — never `COPY` them into the image.

# Build Practices
- Never hardcode secrets in `ENV`, `ARG`, or `RUN` instructions — they persist in image layers.
- Use multi-stage builds to keep build tools and intermediate artifacts out of the final image.
- Combine `RUN` instructions to reduce layers and avoid caching sensitive intermediate steps.

# Compose
- Never use `privileged: true` unless strictly necessary and documented.
- Explicitly define resource limits (`mem_limit`, `cpus`) — never leave them unbounded.
- Use named volumes over bind-mounting sensitive host paths.
- Scope exposed ports — bind to `127.0.0.1` for services not meant to be externally reachable.
