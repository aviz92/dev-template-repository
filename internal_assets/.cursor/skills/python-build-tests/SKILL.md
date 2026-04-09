---
name: build-tests
description: >
  Write pytest tests for Python code following Avi's workspace conventions.
  Use this skill whenever the user asks to write, add, generate, or improve
  tests — even if phrased as "cover this function", "add test cases", "test this
  module", or "make sure this works". Always use this skill when the output
  includes pytest test files, conftest fixtures, or pytest plugins.
---

# Build Tests

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

## Step 1 — Clarification

If no code is provided, ask: **which module or feature should be covered?**
One question only.

---

## Running Tests

```bash
uv run pytest
```

---

## What to Cover

For every function or class, write tests for:
- **Happy path** — expected input produces expected output.
- **Edge cases** — empty input, `None`, zero, boundary values.
- **Failure cases** — use `pytest.raises` with `match=` to assert the exception message.

---

## Test Naming

Follow `test_<function_or_method>_<scenario>_<expected_outcome>`.
Consistent naming is critical — `pytest-depends-on` matches dependencies by test name.

---

## Parameterization

Default to `@pytest.mark.parametrize`. Only use `@pytest.mark.parametrize_func`
when parameters are genuinely dynamic or external (config, DB, API, file).

### `pytest-dynamic-parameterize` rules
- Parameter function signature: `def my_params(config, **kwargs) -> list[tuple]`.
- Place parameter functions under `tests/parameterize_functions/`.
- Return `NOT_SET_PARAMETERS` (from the plugin) when the param set is empty — not `[]`.
- Pass kwargs via the marker arguments.
- Multiple `parametrize_func` markers on one test are supported for cross-product parameterization.

---

## Test Dependencies

Use `pytest-depends-on` only when a test **logically cannot pass** if a prerequisite
failed. Do not use it as a substitute for test isolation.

- Enable with `--depends-on` and `--depends-on-reorder` in `pytest.ini` — without these flags all markers are silently ignored.
- Default dependency expects the parent to have passed. Use `status=Status.FAILED` (from `pytest_depends_on.consts.status`) to depend on a different outcome.
- Use `allowed_not_run=True` for soft dependencies where the parent may not have run.

---

## pytest-plugins

Enable in `pytest.ini` based on project needs:

| Flag | When to use |
|---|---|
| `--better-report` | Always — generates JSON and MD test reports under `results_output/` |
| `--maxfail-streak=N` | Stop after N consecutive failures in long suites |
| `--fail2skip` | Convert failures to skips for tests marked `@pytest.mark.fail2skip` |
| `--verbose-param-ids` | Makes parameterized test IDs human-readable |
| `--require-tests` | Fail (exit code 4) if zero tests were collected |
| `--add-parameters` | Include test parameters as fields in the JSON report |
| `--md-report` | Add Markdown report alongside JSON |
| `--traceback` | Include full traceback in the report |

Add CI-specific flags (`--pr-number`, `--mr-number`, `--pipeline-number`, `--commit`)
when running inside a CI pipeline.

---

## Fixtures

### Placement

| Fixture scope | Where it lives |
|---|---|
| Used by a single test module only | Inline in that test file |
| Shared within a directory | `conftest.py` in that directory |
| Truly global (cross-module) | Root `conftest.py` |
| `pytest_addoption` | Subdirectory `conftest.py` unless the option is genuinely global |

### Scope

Prefer the narrowest scope that keeps tests isolated.

| Scope | Use when |
|---|---|
| `function` (default) | Fixture must be fresh per test |
| `module` | Setup is expensive and safe to share within a file |
| `session` | Setup is expensive and safe to share across the entire run |

---

## Logging

Never use `print()` in tests or fixtures. Use `get_logger(__name__)` from
`custom-python-logger` for any diagnostic output.

---

## Plugin Development

- Prefix all `pytest_addoption` options with a project-specific prefix to avoid conflicts.
- Use `pytest_configure` for initialization, `pytest_sessionfinish` for cleanup and reporting.
- Register via `[project.entry-points.pytest11]` in `pyproject.toml`.
- Use `tryfirst=True` / `trylast=True` when hook execution order matters.
- Store plugin state on the `config` object — never in module globals.

---

## After Writing Tests

```bash
pre-commit run --files <new_test_files>
```

Fix all failures and re-run. **Never present tests that fail pre-commit.**

---

## Definition of Done

- [ ] Library docs fetched from GitHub before writing any code
- [ ] Happy path, edge cases, and failure cases covered for every function/class
- [ ] `pytest.raises` used with `match=` on all failure cases
- [ ] Test names follow `test_<function>_<scenario>_<expected_outcome>` convention
- [ ] Test classes subclass `BaseClassTest` with `component` property set
- [ ] Static params → `@pytest.mark.parametrize`; runtime params → `@pytest.mark.parametrize_func`
- [ ] `parametrize_func` functions live under `tests/parameterize_functions/`
- [ ] `pytest-depends-on` used only for logical prerequisites, not ordering hacks
- [ ] `--depends-on` and `--depends-on-reorder` in `pytest.ini` if `depends_on` markers are used
- [ ] `pytest-plugins` flags enabled in `pytest.ini` appropriate to the project
- [ ] Fixture at narrowest correct scope; `conftest.py` at narrowest correct level
- [ ] No `print()` anywhere — only `custom-python-logger`
- [ ] pre-commit passes cleanly
