---
name: python-build-tests
description: >
  Write pytest tests following workspace conventions. Use when asked to write, add,
  generate, or improve tests — including "cover this function" or "add test cases".
allowed-tools: Bash(uv run *) Bash(pre-commit *) Read Grep
---

# Build tests

## Step 1 — Clarification

If no code is provided, ask: **which module or feature should be covered?**
One question only.

## Running tests

```bash
uv run pytest
```

## What to cover

For every function or class, write tests for:
- **Happy path** — expected input produces expected output.
- **Edge cases** — empty input, `None`, zero, boundary values.
- **Failure cases** — use `pytest.raises` with `match=` to assert the exception message.

## Test naming

Follow `test_<function_or_method>_<scenario>_<expected_outcome>`.
Consistent naming is critical — `pytest-depends-on` matches dependencies by test name.

## Parameterization

Default to `@pytest.mark.parametrize`. Only use `@pytest.mark.parametrize_func`
when parameters are genuinely dynamic or external (config, DB, API, file).

### `pytest-dynamic-parameterize` rules
- Parameter function signature: `def my_params(config, **kwargs) -> list[tuple]`.
- Place parameter functions under `tests/parameterize_functions/`.
- Return `NOT_SET_PARAMETERS` (from the plugin) when the param set is empty — not `[]`.
- Pass kwargs via the marker arguments.
- Multiple `parametrize_func` markers on one test are supported for cross-product parameterization.

## Test dependencies

Use `pytest-depends-on` only when a test **logically cannot pass** if a prerequisite
failed. Do not use it as a substitute for test isolation.

- Enable with `--depends-on` and `--depends-on-reorder` in `pytest.ini`.
- Default dependency expects the parent to have passed. Use `status=Status.FAILED` for other outcomes.
- Use `allowed_not_run=True` for soft dependencies where the parent may not have run.

## pytest-plugins flags

Enable in `pytest.ini` based on project needs:

| Flag | When to use |
|---|---|
| `--better-report` | Always — JSON and MD reports under `results_output/` |
| `--maxfail-streak=N` | Stop after N consecutive failures in long suites |
| `--fail2skip` | Convert failures to skips for `@pytest.mark.fail2skip` tests |
| `--verbose-param-ids` | Human-readable parameterized test IDs |
| `--require-tests` | Fail (exit code 4) if zero tests collected |
| `--add-parameters` | Include test parameters in JSON report |
| `--md-report` | Add Markdown report alongside JSON |
| `--traceback` | Include full traceback in report |

Add CI flags (`--pr-number`, `--mr-number`, `--pipeline-number`, `--commit`) in CI pipelines.

## Fixtures

### Placement

| Fixture scope | Where it lives |
|---|---|
| Single test module only | Inline in that test file |
| Shared within a directory | `conftest.py` in that directory |
| Truly global (cross-module) | Root `conftest.py` |
| `pytest_addoption` | Subdirectory `conftest.py` unless genuinely global |

### Scope

Prefer the narrowest scope that keeps tests isolated: `function` (default) → `module` → `session`.

## Logging

Never use `print()` in tests or fixtures. Use `get_logger(__name__)` from `custom-python-logger`.

## Plugin development

- Prefix all `pytest_addoption` options with a project-specific prefix.
- Use `pytest_configure` for init, `pytest_sessionfinish` for cleanup/reporting.
- Register via `[project.entry-points.pytest11]` in `pyproject.toml`.
- Use `tryfirst=True` / `trylast=True` when hook execution order matters.
- Store plugin state on the `config` object — never in module globals.

## After writing tests

```bash
pre-commit run --files <new_test_files>
```

Fix all failures and re-run. **Never present tests that fail pre-commit.**

## Definition of done

- [ ] Happy path, edge cases, and failure cases covered
- [ ] `pytest.raises` with `match=` on all failure cases
- [ ] Test names follow `test_<function>_<scenario>_<expected_outcome>`
- [ ] Test classes subclass `BaseClassTest` with `component` property set
- [ ] Static params → `@pytest.mark.parametrize`; runtime → `@pytest.mark.parametrize_func`
- [ ] `parametrize_func` functions in `tests/parameterize_functions/`
- [ ] `pytest-depends-on` used only for logical prerequisites
- [ ] Fixture at narrowest correct scope; `conftest.py` at narrowest correct level
- [ ] No `print()` — only `custom-python-logger`
- [ ] pre-commit passes cleanly
