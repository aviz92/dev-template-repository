---
name: python-build-cli-tool
description: >
  Build a production-ready Python CLI tool using python-base-command.
  Use when asked to build, scaffold, or add a CLI tool, command, or entry point.
disable-model-invocation: true
allowed-tools: Bash(uv run *) Bash(pre-commit *) Read Grep
argument-hint: "[command-name]"
---

# Build CLI tool

## Step 1 — Clarification

If requirements are unclear, ask **one focused question** before starting.

## Framework

All CLI tools use **`python-base-command`** — a Django-style `BaseCommand` framework
for standalone Python commands.

## Entry point choice

| Situation | Use |
|---|---|
| Multiple commands in a `commands/` folder | `Runner` (auto-discovery) |
| Single command or explicit registration | `CommandRegistry` |

Both expose the same `run()` interface and share the same `BaseCommand` API.
Set `PYTHON_BASE_COMMAND_PROJECT_NAME` env var to control the log file name.
Register the entry point in `pyproject.toml` under `[project.scripts]`.
Entry point signature: `def main(argv: list[str] | None = None) -> None:`.

## Command class choice

| Situation | Use |
|---|---|
| Named options/flags | `BaseCommand` |
| Positional labels (files, IDs, names…) | `LabelCommand` |

For `LabelCommand`: implement `handle_label(label, **kwargs)` instead of `handle()`.

## Conventions

### Structure
- One `Command` class per file under `commands/`.
- Business logic lives in a service module or private method — never in `handle()`.
- `handle()`: validate args, call the service, handle errors.

### Version
Call `self.set_project_version()` inside `handle()` (or `__init__`) so `--version`
returns the real version from `pyproject.toml`.

### Logging
- Inside commands: `self.logger` — built-in, no setup required.
- In service modules: `logger = get_logger(__name__)` at module level.
- Never use `print()`.
- Levels: `debug`, `info`, `step`, `warning`, `error`, `exception`.
- Use `step` for major milestones; `exception` when catching with full traceback.

### Error handling
- CLI layer → raise `CommandError` (caught by the runner; exits cleanly).
- Service layer → raise from `python-custom-exceptions`.
- `handle()` catches service exceptions and re-raises as `CommandError`.

## Testing

Test two concerns separately:
1. **Command logic** — use `call_command(Command, **kwargs)`. `CommandError` propagates normally; assert with `pytest.raises`.
2. **Service logic** — test service functions in isolation, without the command layer.

## After writing

```bash
pre-commit run --files <new_files>
```

Fix all failures. **Never present code that fails pre-commit.**

## Definition of done

- [ ] Library docs fetched from GitHub before writing any code
- [ ] Entry point uses `Runner` or `CommandRegistry` — justified by project shape
- [ ] `BaseCommand` or `LabelCommand` — justified by argument shape
- [ ] `self.set_project_version()` called
- [ ] Entry point registered in `pyproject.toml` under `[project.scripts]`
- [ ] `handle()` contains zero business logic
- [ ] No `print()` — only `custom-python-logger`
- [ ] Errors: `CommandError` in CLI, `python-custom-exceptions` in services
- [ ] `call_command()` in tests; `CommandError` cases covered with `pytest.raises`
- [ ] `PYTHON_BASE_COMMAND_PROJECT_NAME` set or documented
- [ ] pre-commit passes cleanly
