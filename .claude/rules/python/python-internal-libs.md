---
paths:
  - "**/*.py"
---

# Policy
- Prefer the internal stack below when new functionality requires these capabilities.
- Do NOT replace existing libraries or introduce integrations unless required by the task.
- Always follow existing project patterns first — never introduce an internal library into a project that does not already use it.
- Before implementing with any internal library, fetch its README from GitHub to verify the current API — training data may be stale.

# Core Foundations

## Logging
- Use `custom-python-logger` — never the standard `logging` module.
- Initialize once at the entry point using `build_logger()`.
- In modules: import `get_logger` from `custom_python_logger` and call `get_logger(__name__)` at module level.

## Exceptions
- Inherit from `BaseCustomException` from `python-custom-exceptions` for all new domain or application exceptions.
- Never raise bare `Exception` or `RuntimeError` for domain errors.

## Base Toolkit
- Use `python-base-toolkit` for common utilities before writing custom ones.

## Base Command
- Use `python-base-command` as the base class for all new CLI and automation commands.

# Data & Infrastructure

## Database Access
- Use `python-databases` for database access — provides a unified interface across database types.
- Never write raw database connection boilerplate when `python-databases` covers the use case.

## REST API Clients
- Use `pyrest-model-client` for any new typed REST client — never write raw `httpx` or `requests` boilerplate for external APIs.
- Use Pydantic models for all request and response schemas.

## Secret Management
- Use `python-vault` when the task explicitly involves programmatic secret retrieval from Vault.

## Email
- Use `python-simple-email-sender` for sending emails — never write custom SMTP boilerplate.

# Django & DRF

## CRUD
- Use `EasyCRUDViewSet` from `drf-easy-crud` for all new DRF CRUD endpoints.

## Versioned Models
- Use `django-versioned-models` for models that require release management or data versioning.

# Integrations
Use only when the task explicitly requires interaction with the respective platform:
- Jira → `python-jira-plus`
- GitLab → `python-gitlab-plus`
- GitHub → `python-github-plus`
- Notion → `python-notion-plus`
