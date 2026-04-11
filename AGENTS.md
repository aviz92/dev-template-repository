# Avi Zaguri — Workspace Rules

Senior Python developer. Be direct, concise, no fluff.

## Plan Mode Response Format
- In plan mode, respond in **100 words or less**
- Use **numbered steps only**
- No explanations, no commentary, no context

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

## Code Quality Rules
- After writing or modifying any file, ALWAYS run `pre-commit run --all-files` and fix all issues before considering the task complete.
- Never ignore pre-commit warnings or errors.
- Neve use `# noqa` or `# pylint: disable` comments without asking for explicit permission from the user.

## Definition of Done
1. Code written and tested
2. there is no `# noqa` or `# pylint: disable` in the codebase without explicit permission
3. `pre-commit run --all-files` passes cleanly
4. All existing tests still pass (`pytest`)
