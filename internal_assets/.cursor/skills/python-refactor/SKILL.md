---
name: python-refactoring
description: >
  Refactor Python code following Avi's workspace conventions and safety rules.
  Use this skill whenever the user asks to refactor, clean up, restructure,
  simplify, rename, extract, or improve existing Python code — even if phrased
  as "this is too long", "move this", "clean this up", or "fix the structure".
  Always use this skill before making structural edits to existing code.
---

# Python Refactoring

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

## Step 1 — Understand Before Touching

1. Read the full file. Identify the exact scope of the refactor — which function,
   class, or module is affected.
2. Search the codebase for all call sites of every function or class being changed.
3. Identify tests that cover the code. Note explicitly if coverage is missing.
4. **State your plan in chat before making any edits:**
   - What changes and why.
   - What stays unchanged.
   - Which call sites are affected.
   - Which tests will validate the result.

**If the plan requires changing more than 3 call sites or touches more than one
module boundary — stop and confirm with the user before proceeding.**

---

## Step 2 — Classify the Refactor

| Category | Examples |
|---|---|
| **Extract** | Long function → atomic helpers |
| **Rename** | Unclear names → intention-revealing names |
| **Restructure** | Move to correct module; fix layering violation |
| **Simplify** | Remove dead code; flatten nesting; replace loops with comprehensions |
| **Type Safety** | Add missing type hints; narrow `Any` |
| **Pattern Apply** | Factory, Strategy, Repository, etc. |

One refactor = one category. Do not mix categories in a single edit.

---

## Step 3 — Rules

### Scope
- Fix only what the task requires, plus obvious violations **within the same
  function or class being changed**. Never touch unrelated functions in the file.
- One logical change per edit block — rename is one edit, extract is a separate edit.

### Signatures
- Never change a public function signature without explicit instruction.
- If a signature must change: list every affected call site in chat first,
  then wait for confirmation before editing.
- If a renamed function appears in `pytest-depends-on` markers (`depends_on`),
  update the marker references — otherwise dependent tests will silently skip forever.

### Stack-specific rules

**When extracting logging:**
Use `get_logger(__name__)` from `custom-python-logger`. Never introduce `print()`
or `logging.getLogger()` during a refactor.

**When extracting exceptions:**
Use `python-custom-exceptions`. Never introduce bare `Exception` or `ValueError`
during a refactor.

**When moving logic to a service layer:**
The receiving module must contain zero CLI imports (`sys.exit`, `typer`, `argparse`).
CLI layer calls service; service raises typed exceptions; CLI catches and re-raises
as `CommandError`.

**When refactoring test code:**
Fixtures must remain at the narrowest correct scope. `conftest.py` placement must
follow `build-tests` conventions. Do not change test names without updating all
`depends_on` references.

---

## Step 4 — Validate

**Logic equivalence** — before considering the refactor complete, verify:
- Same return values for the same inputs.
- Same exceptions raised under the same conditions.
- Same side effects (file writes, DB calls, network calls).
- No new code paths introduced that didn't exist before.

Run pre-commit on changed files:

```bash
uv run pre-commit run --files <changed_files>
```

Run affected tests:

```bash
uv run pytest <relevant_test_paths> -v
```

If no tests exist for the refactored code, flag it before finishing:
> ⚠️ No tests found for `<function_name>`. Consider adding coverage before merging.

---

## Output Format

```
## Refactor Summary

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
