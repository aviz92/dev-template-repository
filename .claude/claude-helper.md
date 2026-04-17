# Claude Code — Commands Reference

Personal reference for built-in, bundled, and custom slash commands.

> **Tip:** Type `/` in any session to see all available commands (built-in + custom + MCP-connected).

---

## Built-in Commands

| Command | Purpose | Notes |
|---|---|---|
| `/help` | List all available commands | Includes custom + MCP commands |
| `/clear` | Wipe conversation history, start fresh | No summary kept — hard reset |
| `/compact` | Compress history into a summary, continue session | Best for long sessions hitting token limits |
| `/model <model-string>` | Switch the active model mid-session | See model strings below |
| `/init` | Create or update `CLAUDE.md` for the current project | Run once per new project |
| `/review` | Run a code review on current changes | Also invokable via Skill tool |
| `/security-review` | Run a security-focused code review | OWASP-style analysis |
| `/permissions` | View and manage tool permissions | Control what Claude can touch |
| `/install-github-app` | Connect Claude Code to GitHub for PR auto-review | Adds `claude-code-review.yml` |

---

## Bundled Skills

Skills that ship with Claude Code and are available as slash commands out of the box.

| Command | Purpose |
|---|---|
| `/debug` | Structured debugging session |
| `/simplify` | Refactor and simplify selected/current code |

> Bundled skills live alongside built-in commands in the `/help` output, marked as **Skill**.

---

### `/model opusplan` — Hybrid Plan/Execute Mode
**What it does:** Switches to a two-phase workflow:
- **Plan mode** → uses `claude-opus-4-6` (deep reasoning for architecture decisions)
- **Execution mode** → automatically switches to `claude-sonnet-4-20250514` (fast, cost-efficient for writing code)

---

### `/compact` *(Built-in)*
**What it does:** Compresses the full conversation history into a structured summary, keeping a high-level context in the window without the full token cost of the original messages.

---

### `/unit-test-expand` — Expand Unit Test Coverage
**What it does:** Analyzes the target module/function and generates additional unit tests covering edge cases, error paths, and boundary conditions not yet tested.

---

### Before pushing a PR
```
/review                    → general code review
/security-review           → security pass
/unit-test-expand <file>   → expand test coverage on changed files
```
