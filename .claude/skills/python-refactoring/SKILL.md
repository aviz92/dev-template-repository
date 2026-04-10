---
name: python-refactoring
description: >
  Refactor Python code following workspace conventions and safety rules.
  Use when asked to refactor, clean up, restructure, simplify, rename, extract, or improve existing code.
allowed-tools: Bash(uv run *) Bash(pre-commit *) Bash(git *) Read Grep
---

# Python refactoring

## Step 1 — Understand before touching

1. Read the full file. Identify the exact scope — which function, class, or module is affected.
2. Search the codebase for all call sites of every function or class being changed.
3. Identify tests that cover the code. Note explicitly if coverage is missing.
4. **State your plan in chat before making any edits:**
   - What changes and why.
   - What stays unchanged.
   - Which call sites are affected.
   - Which tests will validate the result.

**If the plan requires changing more than 3 call sites or touches more than one
module boundary — stop and confirm with the user before proceeding.**

## Step 2 — Classify the refactor

| Category | Examples |
|---|---|
| **Extract** | Long function → atomic helpers |
| **Rename** | Unclear names → intention-revealing names |
| **Restructure** | Move to correct module; fix layering violation |
| **Simplify** | Remove dead code; flatten nesting; replace loops with comprehensions |
| **Type Safety** | Add missing type hints; narrow `Any` |
| **Pattern Apply** | Factory, Strategy, Repository, etc. |

One refactor = one category. Do not mix categories in a single edit.

## Step 3 — Rules

### Scope
- Fix only what the task requires, plus obvious violations **within the same function or class**. Never touch unrelated functions.
- One logical change per edit block.

### Signatures
- Never change a public function signature without explicit instruction.
- If a signature must change: list every affected call site in chat first, wait for confirmation.
- If a renamed function appears in `pytest-depends-on` markers (`depends_on`), update the marker references.

### Stack-specific rules

**Extracting logging:** Use `get_logger(__name__)` from `custom-python-logger`. Never introduce `print()` or `logging.getLogger()`.

**Extracting exceptions:** Use `python-custom-exceptions`. Never introduce bare `Exception` or `ValueError`.

**Moving logic to a service layer:** The receiving module must contain zero CLI imports (`sys.exit`, `typer`, `argparse`). CLI layer calls service; service raises typed exceptions; CLI catches and re-raises as `CommandError`.

**Refactoring test code:** Fixtures must remain at narrowest correct scope. `conftest.py` placement must follow `build-tests` conventions. Do not change test names without updating all `depends_on` references.

## Step 4 — Validate

**Logic equivalence** — verify before considering complete:
- Same return values for the same inputs.
- Same exceptions raised under the same conditions.
- Same side effects (file writes, DB calls, network calls).
- No new code paths introduced that didn't exist before.

```bash
uv run pre-commit run --files <changed_files>
uv run pytest <relevant_test_paths> -v
```

If no tests exist for the refactored code, flag it:
> ⚠️ No tests found for `<function_name>`. Consider adding coverage before merging.

## Output format

```
## Refactor summary

**Type**: <category>
**Files changed**: <list>
**What changed**: <short description>
**Why**: <reason>
**Call sites updated**: <count and list>
**Interface preserved**: ✅ / ⚠️ <what changed and why>
**depends_on markers updated**: ✅ / N/A
**Tests**: passing / missing / added
**Pre-commit**: ✅ / ❌
```
