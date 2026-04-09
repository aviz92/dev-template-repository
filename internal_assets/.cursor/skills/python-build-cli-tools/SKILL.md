---
name: build-cli-tool
description: >
  Build a production-ready Python CLI tool following Avi's workspace conventions.
  Use this skill whenever the user asks to build, scaffold, create, or add a CLI
  tool, CLI command, command-line script, or any runnable entry point — even if
  phrased as "add a script", "make it runnable from the terminal", "add a manage
  command", or "write an automation command". Always use this skill when the
  output is a CLI entry point of any kind.
---

# Build CLI Tool

---

## Step 0 — Before Writing Any Code

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

If requirements are unclear, ask **ONE focused question** before starting.

---

## Framework

All CLI tools use **`python-base-command`** — a Django-style `BaseCommand` framework
for standalone Python commands.

---

## Entry Point Choice

Choose based on the project shape:

| Situation | Use |
|---|---|
| Multiple commands in a `commands/` folder | `Runner` (auto-discovery) |
| Single command or explicit registration needed | `CommandRegistry` |

Both expose the same `run()` interface and share the same `BaseCommand` API.
Set `PYTHON_BASE_COMMAND_PROJECT_NAME` env var to control the log file name.
Register the entry point in `pyproject.toml` under `[project.scripts]`.
Entry point signature must always be `def main(argv: list[str] | None = None) -> None:`.

---

## Command Class Choice

| Situation | Use |
|---|---|
| Command operates on named options/flags | `BaseCommand` |
| Command accepts one or more positional labels (files, IDs, names…) | `LabelCommand` |

For `LabelCommand`: implement `handle_label(label, **kwargs)` instead of `handle()`.

---

## Conventions

### Structure
- One `Command` class per file under `commands/`.
- Business logic lives in a service module or private method — never in `handle()`.
- `handle()` is responsible for: validating args, calling the service, and handling errors.

### Version
Call `self.set_project_version()` inside `handle()` (or `__init__`) so that the
built-in `--version` flag returns the real version from `pyproject.toml`, not `"unknown"`.

### Logging
- Inside commands: use `self.logger` — it is built-in, no setup required.
- In service modules: `logger = get_logger(__name__)` at module level.
- Never use `print()`.
- Available levels: `debug`, `info`, `step`, `warning`, `error`, `exception`.
- Use `step` for major milestones; `exception` when catching with a full traceback.

### Error Handling
- CLI layer → raise `CommandError` (caught by the runner; exits cleanly with returncode).
- Service layer → raise from `python-custom-exceptions` (typed, structured exceptions).
- `handle()` catches service exceptions and re-raises as `CommandError`.

---

## Testing

Test two concerns separately:

1. **Command logic** — use `call_command(Command, **kwargs)`.
   `CommandError` propagates normally through `call_command()`; assert with `pytest.raises`.

2. **Service logic** — test service functions in isolation, without the command layer.

---

## After Writing

```bash
pre-commit run --files <new_files>
```

Fix all failures and re-run. **Never present code that fails pre-commit.**

---

## Definition of Done

- [ ] Library docs fetched from GitHub before writing any code
- [ ] Entry point uses `Runner` or `CommandRegistry` — justified by project shape
- [ ] `BaseCommand` or `LabelCommand` — justified by argument shape
- [ ] `self.set_project_version()` called so `--version` returns the real version
- [ ] Entry point registered in `pyproject.toml` under `[project.scripts]`
- [ ] `handle()` contains zero business logic
- [ ] No `print()` anywhere — only `custom-python-logger`
- [ ] Errors raised as `CommandError`; service errors via `python-custom-exceptions`
- [ ] `call_command()` used in tests; `CommandError` cases covered with `pytest.raises`
- [ ] `PYTHON_BASE_COMMAND_PROJECT_NAME` set or documented
- [ ] pre-commit passes cleanly
