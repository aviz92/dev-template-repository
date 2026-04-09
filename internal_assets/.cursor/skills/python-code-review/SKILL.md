---
name: python-code-review
description: >
  Review Python code for correctness, quality, and adherence to Avi's workspace
  conventions. Use this skill whenever the user asks to review, check, audit, or
  give feedback on Python code — even if phrased as "look at this", "is this
  correct", "what do you think of this", or "PR review". Always use this skill
  when the task is to evaluate existing code rather than write new code.
---

# Python Code Review

---

## Step 0 — Before Touching Anything

1. Read `.claude/CLAUDE.md` (workspace rules). If absent, proceed with this skill.
2. Identify which of Avi's libraries appear in the changed files, then fetch their
   - docs from GitHub before reviewing any code that uses them at https://github.com/aviz92/<library_name>.
   - you can use the following script to fetch the name of all Avi's libraries: `scripts/get_all_aviz_pypi_packages.py`.
3. Identify the type of code being reviewed and apply the matching skill conventions:
   - CLI code → apply `build-cli-tool` conventions.
   - Test code → apply `build-tests` conventions.

---

## Step 1 — Pre-commit

Run pre-commit on all changed files:

```bash
pre-commit run --files <changed_files>
```

If pre-commit fails — report the full output, mark each violation as **Critical**,
and **stop**. Do not proceed to the code review until the code is clean.

---

## Step 2 — Run Relevant Tests

Identify relevant tests by these heuristics (in order):
1. A test file whose name mirrors the changed file — `services/user.py` → `tests/services/test_user.py`.
2. Test files that import from the changed module.
3. The closest `tests/` directory to the changed file.

Run the identified tests:

```bash
uv run pytest <relevant_test_paths> -v --better-report
```

- If tests fail → report the failures and mark each as **Critical**.
- If no tests exist for the changed code → flag as **Major** (missing test coverage).

---

## Step 3 — Code Review

Review against workspace rules, Avi's library conventions, and the focus areas below.
Be strict but concise — flag real issues, skip obvious ones.

### Stack-specific checks

**If reviewing CLI code:**
- `python-base-command` used (not argparse or raw Typer).
- `handle()` contains zero business logic — delegates entirely to a service.
- Errors raised as `CommandError`; service errors via `python-custom-exceptions`.
- `self.set_project_version()` called so `--version` is accurate.
- `self.logger` used — never `print()`.

**If reviewing service/library code:**
- `get_logger(__name__)` from `custom-python-logger` — never `print()` or `logging.getLogger()`.
- Exceptions raised from `python-custom-exceptions` — not bare `Exception` or `ValueError`.
- No CLI imports (`typer`, `argparse`, `sys.exit`) in service modules.

**If reviewing test code:**
- `pytest.raises` used with `match=` on all failure cases.
- `parametrize_func` functions live under `tests/parameterize_functions/`.
- `--better-report` present in `pytest.ini` used for test output.
- `--depends-on` present in `pytest.ini` if `depends_on` markers are used.
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

---

## Step 4 — Logic Review

- Does the code do what it is supposed to do?
- Are all edge cases handled: empty input, `None`, zero, negative values, large datasets?
- Are conditionals correct and in the right order?
- Are there off-by-one errors or boundary issues?
- Does the error handling cover realistic failure scenarios?
- Are there hidden assumptions about input that could break in production?

---

## Severity Levels

| Level | Definition | Blocks merge? |
|---|---|---|
| **Critical** | Security issue, broken functionality, failing tests, missing type hints on public-facing functions and methods | Yes |
| **Major** | Structural violation, missing test coverage, wrong library usage, performance issue, missing type hints on private/internal functions | Yes |
| **Minor** | Style, naming, documentation | No |
| **Suggestion** | Optional improvement, alternative approach | No |

---

## Output Format

**Summary**

One paragraph: overall quality, pre-commit status, test results, what was done well.

**Issues**

```
[SEVERITY] Short title
📍 Location: file.py, line X
🔍 Problem: what's wrong and why it matters
💡 Fix: concrete description of the correction
```

Group issues by severity (Critical first). Omit sections with no issues.

**Verdict**

| Verdict | When |
|---|---|
| `APPROVED` | No Critical or Major issues |
| `APPROVED WITH COMMENTS` | Minor/Suggestion issues only — can merge, should address |
| `CHANGES REQUESTED` | At least one Critical or Major issue |

---

## What NOT to Flag

- Anything already caught and reported by pre-commit in Step 1 — do not repeat it.
- Formatting, whitespace, or import ordering — these are linter/formatter concerns, not review concerns.
- Issues outside the scope of the changed files — review only what changed.

---

## Tone

Strict but constructive. One sentence per issue where possible.
Never explain what the code does — only what is wrong and how to fix it.
