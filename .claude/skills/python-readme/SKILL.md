---
name: readme
description: >
  Generate or update a project README from actual codebase content.
  Use when asked to create, write, or update a README, or when a project has no README.md.
allowed-tools: Read Grep
---

# README generator

## Steps
1. Read `pyproject.toml`, `src/`, entry points, `env.template`
2. Detect project type:
   - **Library** (has PyPI publish config) → install via `uv add <lib-name>`
   - **Template/App** (clone-based) → install via `git clone + uv sync`
3. Generate README using the template in [template.md](assets/template.md) — real content only

## Rules
- Never leave `<placeholder>` — fill everything from actual code
- Usage examples must be real and runnable — read source files first
- Features must reflect actual functionality — no fluff
- Omit PyPI badges for non-published projects
- Omit Configuration section if no env vars exist
- Tone: professional, concise, emoji-prefixed sections
