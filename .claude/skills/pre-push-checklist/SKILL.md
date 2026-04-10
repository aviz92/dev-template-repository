---
name: pre-push-checklist
description: >
  End-of-session pre-push verification checklist. Runs five checks: pre-commit,
  tests, README, CHANGELOG, and pyproject.toml version bump.
disable-model-invocation: true
allowed-tools: Bash(uv run *) Bash(pre-commit *) Bash(git *) Bash(pytest *) Bash(grep *) Bash(find *) Bash(head *) Read
---

# Pre-push checklist

A structured end-of-session verification gate before `git push`.
Runs five checks in order, reports status for each, and summarizes what needs attention.

## Step 0 — Understand context

```bash
pwd
git rev-parse --show-toplevel 2>/dev/null || echo "NOT A GIT REPO"
git status --short
git log --oneline -5
```

If this is not a git repository, stop and tell the user.

## Check 1 — Tests: created & passing

### 1a — Detect new test files

```bash
git diff --name-only HEAD 2>/dev/null | grep -E "test_|_test\.py" | head -20
git diff --name-only origin/main 2>/dev/null | grep -E "test_|_test\.py" | head -20
find . -name "test_*.py" -o -name "*_test.py" 2>/dev/null | grep -v ".git" | grep -v "__pycache__" | sort
```

### 1b — Run the test suite

```bash
uv run pytest --tb=short -q 2>/dev/null || pytest --tb=short -q
```

- ✅ New tests found AND all pass → continue
- ⚠️ No new tests → warn, don't block
- ❌ Tests fail → print failures; do NOT continue until user acknowledges

## Check 2 — README updated

```bash
git diff origin/main -- README.md 2>/dev/null | grep "^+" | grep -v "^+++" | wc -l
```

- ✅ Meaningful added lines (new sections, usage examples, feature docs) → continue
- ⚠️ Only whitespace/formatting → warn, show diff
- ❌ Not changed → ask if the new feature needs documentation

## Check 3 — CHANGELOG updated

```bash
git diff origin/main -- CHANGELOG.md 2>/dev/null | grep "^+" | grep -v "^+++" | wc -l
head -40 CHANGELOG.md 2>/dev/null || echo "CHANGELOG.md NOT FOUND"
```

- ✅ New meaningful entry (Added/Changed/Fixed bullets) → continue
- ⚠️ Touched but no real entry → warn, show diff
- ❌ Not changed → offer to draft entry based on git diff
- ❌ File missing → offer to create in `Keep a Changelog` format

If drafting an entry:
```bash
git diff origin/main --stat 2>/dev/null
git log --oneline origin/main..HEAD 2>/dev/null
```

## Check 4 — pyproject.toml version bump

```bash
git diff --name-only origin/main 2>/dev/null | grep "pyproject.toml"
grep -E "^version" pyproject.toml 2>/dev/null
git diff --stat origin/main 2>/dev/null
```

Heuristics:
- New public functions/classes/CLI commands → **minor** bump
- Bug fixes only → **patch** bump
- Breaking API changes → **major** bump
- Internal refactoring/tests/docs only → may not need a bump

- ✅ Version was incremented → continue
- ⚠️ Not modified but bump seems warranted → ask user, offer to bump

## Check 5 — Pre-commit

```bash
uv run pre-commit run --all-files 2>/dev/null || pre-commit run --all-files
```

- ✅ All hooks passed → proceed to summary
- ❌ Any hook failed → report which, offer auto-fixes (`ruff --fix`, `black`, `isort`)
- ⚠️ pre-commit not installed → warn, don't block

## Final summary

```
╔══════════════════════════════════════════════════════╗
║           PRE-PUSH CHECKLIST SUMMARY                ║
╠══════════════════╦═══════════════════════════════════╣
║ Check            ║ Status                            ║
╠══════════════════╬═══════════════════════════════════╣
║ Pre-Commit       ║ ✅ / ❌                           ║
║ Tests            ║ ✅ / ⚠️ / ❌                      ║
║ README           ║ ✅ / ⚠️ / ❌                      ║
║ CHANGELOG        ║ ✅ / ⚠️ / ❌                      ║
║ pyproject.toml   ║ ✅ / ⚠️                           ║
╚══════════════════╩═══════════════════════════════════╝

🟢 All checks passed — safe to push!
🔴 X issue(s) require attention before pushing.
```

Only "safe to push" if there are **no ❌ statuses**.

## Notes

- Always run checks in order (1 → 5); ❌ on tests pauses the flow.
- Never auto-push. This skill only verifies. The user pushes manually.
- For monorepos, ask which sub-package to check.
