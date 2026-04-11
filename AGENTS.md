# Avi Zaguri — Workspace Rules

Senior Python developer. Be direct, concise, no fluff.

## Before using my libraries
Fetch docs from https://github.com/aviz92/<library_name> before writing code that uses them.

## Behavior
- Act autonomously on small-to-medium tasks
- Ask before architectural changes or multi-file refactors
- Proactively flag tech debt, performance, and security issues

## Environment
- Package manager: `uv` exclusively — never pip
- Python: >=3.12

## Security
- Never read/write .env, secrets/, credentials, token files
- Never commit API keys or passwords
- Always use parameterized queries

## Git
- Conventional Commits (feat:, fix:, refactor:, test:, chore:, docs:)
- Branches: feature/, fix/, chore/ prefixes
- Pre-commit must pass before committing
