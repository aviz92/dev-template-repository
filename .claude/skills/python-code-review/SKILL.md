---
name: python-code-review
description: >
  Review Python code for correctness, quality, and workspace conventions.
  Use when asked to review, check, audit, or give feedback on code, including PR reviews.
allowed-tools: Bash(uv run *) Bash(pre-commit *) Bash(git *) Read Grep
---

# Python code review

## Step 1 — Pre-commit

Run pre-commit on all changed files:

```bash
pre-commit run --files <changed_files>
```

If pre-commit fails — report the full output, mark each violation as **Critical**,
and **stop**. Do not proceed to the code review until the code is clean.

## Step 2 — Run relevant tests

Identify relevant tests by these heuristics (in order):
1. A test file whose name mirrors the changed file — `services/user.py` → `tests/services/test_user.py`.
2. Test files that import from the changed module.
3. The closest `tests/` directory to the changed file.

```bash
uv run pytest <relevant_test_paths> -v --better-report
```

- Tests fail → report failures, mark as **Critical**.
- No tests exist → flag as **Major** (missing test coverage).

## Step 3 — Code review

Review against workspace rules, Avi's library conventions, and the focus areas below.

### Stack-specific checks

**CLI code:**
- `python-base-command` used (not argparse or raw Typer).
- `handle()` contains zero business logic — delegates to a service.
- Errors raised as `CommandError`; service errors via `python-custom-exceptions`.
- `self.set_project_version()` called so `--version` is accurate.
- `self.logger` used — never `print()`.

**Service/library code:**
- `get_logger(__name__)` from `custom-python-logger` — never `print()` or `logging.getLogger()`.
- Exceptions from `python-custom-exceptions` — not bare `Exception` or `ValueError`.
- No CLI imports (`typer`, `argparse`, `sys.exit`) in service modules.

**Test code:**
- `pytest.raises` with `match=` on all failure cases.
- `parametrize_func` functions live under `tests/parameterize_functions/`.
- `--better-report` and `--depends-on` present in `pytest.ini` when relevant.
- Fixtures at narrowest correct scope and `conftest.py` at narrowest correct level.

### General focus areas

- **Type hints** — all parameters and return types annotated; no bare `Any`.
- **Single responsibility** — functions do one thing; services contain business logic only.
- **Error handling** — specific exceptions, clear messages, always logged with context.
- **Logging** — `custom-python-logger` only; correct level (`step` for milestones, `exception` with traceback).
- **No `print()`** anywhere in production or test code.
- **No hardcoded secrets or magic numbers** — use constants or config.
- **Testability** — dependency injection, no hidden side effects, no global state mutation.
- **N+1 queries and unnecessary computation** — flag in any data-access layer.

## Step 4 — Logic review

- Does the code do what it's supposed to do?
- Are all edge cases handled: empty input, `None`, zero, negative values, large datasets?
- Are conditionals correct and in the right order?
- Off-by-one errors or boundary issues?
- Hidden assumptions about input that could break in production?

## Severity levels

| Level | Definition | Blocks merge? |
|---|---|---|
| **Critical** | Security, broken functionality, failing tests, missing public type hints | Yes |
| **Major** | Structural violation, missing coverage, wrong library usage, performance | Yes |
| **Minor** | Style, naming, documentation | No |
| **Suggestion** | Optional improvement, alternative approach | No |

## Output format

**Summary** — one paragraph: overall quality, pre-commit status, test results, what was done well.

**Issues:**
```
[SEVERITY] Short title
📍 Location: file.py, line X
🔍 Problem: what's wrong and why
💡 Fix: concrete correction
```

Group by severity (Critical first). Omit empty sections.

**Verdict:** `APPROVED` / `APPROVED WITH COMMENTS` / `CHANGES REQUESTED`

## What NOT to flag

- Anything already caught by pre-commit in Step 1.
- Formatting, whitespace, or import ordering — linter/formatter concerns.
- Issues outside the scope of the changed files.

## Tone

Strict but constructive. One sentence per issue where possible.
Never explain what the code does — only what is wrong and how to fix it.
