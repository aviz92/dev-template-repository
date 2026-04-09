---
name: pre-push-checklist
description: >
  End-of-session pre-push verification checklist for Python projects.
  Trigger this skill whenever the user says things like "ready to push",
  "before I push", "end of session check", "trigger pre-push", "run pre-push",
  "let's do the pre-push checklist", "check before push", or any similar phrase
  indicating they are about to git push and want to verify the project is in good shape.
  This skill runs a structured, step-by-step audit covering: pre-commit hooks,
  test creation and passing, README update, CHANGELOG update, and pyproject.toml version bump.
  Always use this skill at the end of a development session before pushing to remote.
---

# Pre-Push Checklist Skill

A structured end-of-session verification gate before `git push`.
Runs five checks in order, reports status for each, and summarizes what still needs attention.

---

## Step 0 — Understand Context

Before running anything, orient yourself:

```bash
# Where are we?
pwd
git rev-parse --show-toplevel 2>/dev/null || echo "NOT A GIT REPO"
git status --short
git log --oneline -5
```

If this is not a git repository, stop and tell the user.

---

## Check 1 — Tests: Created & Passing

**Goal**: Verify that new tests were added as part of this session's work, and that the full test suite passes.

### 1a — Detect new test files in this commit/diff

```bash
# New test files not yet committed (untracked or modified)
git status --short | grep -E "^\?\?.*test|^\?\?.*_test|^[AM].*test" | head -20

# Test files changed vs main/master/HEAD
git diff --name-only HEAD 2>/dev/null | grep -E "test_|_test\.py" | head -20
git diff --name-only origin/main 2>/dev/null | grep -E "test_|_test\.py" | head -20
git diff --name-only origin/master 2>/dev/null | grep -E "test_|_test\.py" | head -20

# All test files in the project (for awareness)
find . -name "test_*.py" -o -name "*_test.py" 2>/dev/null | grep -v ".git" | grep -v "__pycache__" | sort
```

### 1b — Run the test suite

```bash
# Run via uv
uv run pytest --tb=short -q 2>/dev/null

# Fallback: plain pytest
pytest --tb=short -q 2>/dev/null
```

**Status logic:**
- ✅ New test files found AND all tests pass → continue
- ⚠️ No new test files found → warn ("No new tests detected — was this intentional?"), but don't block
- ❌ Tests fail → print failing test names and tracebacks; do NOT continue to the next checks until the user acknowledges or fixes them

---

## Check 2 — README Updated

**Goal**: Verify that `README.md` has meaningful new content — not just whitespace or formatting tweaks.

```bash
# Show the actual diff of README (not just whether it was touched)
git diff origin/main -- README.md 2>/dev/null || git diff HEAD~1 -- README.md 2>/dev/null

# Count added lines (lines starting with +, excluding the diff header)
git diff origin/main -- README.md 2>/dev/null | grep "^+" | grep -v "^+++" | wc -l
```

**Status logic:**
- ✅ README.md has meaningful added lines (new sections, new usage examples, new feature docs) → continue
- ⚠️ README was touched but only whitespace / formatting changed → warn: "README was modified but no meaningful content was added — does the new feature need to be documented?" Show the diff so user can judge
- ❌ README was not changed at all → ask: "README was not updated — does the new feature/fix need to be documented there?" If user says no, note it and continue

When assessing "meaningful", look for: new headings, new code blocks, new paragraphs, new bullet points describing features. Ignore: punctuation fixes, whitespace, badge URL updates.

---

## Check 3 — CHANGELOG Updated

**Goal**: Verify that `CHANGELOG.md` has a real new entry — not just a date change or whitespace fix.

```bash
# Show the actual diff of CHANGELOG
git diff origin/main -- CHANGELOG.md 2>/dev/null || git diff HEAD~1 -- CHANGELOG.md 2>/dev/null

# Count added lines
git diff origin/main -- CHANGELOG.md 2>/dev/null | grep "^+" | grep -v "^+++" | wc -l

# Show the top of CHANGELOG to see the current format
head -40 CHANGELOG.md 2>/dev/null || echo "CHANGELOG.md NOT FOUND"
```

**Status logic:**
- ✅ CHANGELOG.md has a new meaningful entry (Added / Changed / Fixed bullets under a version or `[Unreleased]` block) → continue
- ⚠️ CHANGELOG was touched but no real entry was added (e.g., only a date or version header with no bullets) → warn and show the diff; ask if they want to add proper entries
- ❌ CHANGELOG was not changed at all → warn: "CHANGELOG was not updated." Ask if they want Claude to draft an entry based on the git diff
- ❌ CHANGELOG.md does not exist → offer to create one in `Keep a Changelog` format

**If user wants Claude to draft a CHANGELOG entry:**
```bash
# Get a diff summary to base the entry on
git diff origin/main --stat 2>/dev/null || git diff HEAD~1 --stat 2>/dev/null
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline -10
```

Then draft a proper entry in `Keep a Changelog` format with real bullet points:
```markdown
## [Unreleased]

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Removed
- ...
```

---

## Check 4 — pyproject.toml Updated (if needed)

**Goal**: Detect whether a version bump or dependency change is warranted and whether it was done.

### 4a — Detect if pyproject.toml was touched

```bash
# Check if pyproject.toml was modified
git diff --name-only HEAD 2>/dev/null | grep "pyproject.toml"
git diff --name-only origin/main 2>/dev/null | grep "pyproject.toml"
git diff --name-only origin/master 2>/dev/null | grep "pyproject.toml"

# Show current version
grep -E "^version" pyproject.toml 2>/dev/null || echo "pyproject.toml NOT FOUND"
```

### 4b — Assess whether a bump is needed

Heuristics that suggest a version bump IS needed:
- New public functions, classes, or CLI commands were added → likely **minor** bump
- Bug fixes only → likely **patch** bump
- Breaking changes to public API → likely **major** bump
- Only internal refactoring / tests / docs → may not need a bump

```bash
# Summarize what changed in this session
git diff --stat origin/main 2>/dev/null || git diff --stat HEAD~1 2>/dev/null
```

**Status logic:**
- ✅ pyproject.toml was modified and version was incremented → continue
- ⚠️ pyproject.toml was NOT modified → assess using heuristics above. If a bump seems warranted, warn and ask: "The version in pyproject.toml was not bumped. Based on the changes, this looks like at least a patch/minor release — want me to bump it?"
- If user says yes: read the current version, apply the bump (patch/minor/major as appropriate), update `pyproject.toml`

**Bump helper (if user confirms):**
```bash
# Read current version
grep "^version" pyproject.toml

# Preferred: bump2version via uv
uv run bump2version patch   # or minor / major

# Fallback: manual sed / str_replace on pyproject.toml
```

---

## Check 5 — Pre-Commit

**Goal**: Run pre-commit hooks last — after all content checks — so linting/formatting is the final gate before push.

```bash
# Check if pre-commit is available via uv
uv run pre-commit --version 2>/dev/null || pre-commit --version 2>/dev/null || echo "PRE_COMMIT_NOT_INSTALLED"

# Run on all files
uv run pre-commit run --all-files 2>/dev/null || pre-commit run --all-files
```

**Status logic:**
- ✅ All hooks passed → proceed to summary
- ❌ Any hook failed → print which hooks failed + their output; ask user if they want Claude to attempt auto-fixes (e.g., `ruff --fix`, `black`, `isort`) and re-run
- ⚠️ pre-commit not installed → warn but don't block; note in final summary

---

## Final Summary

After all five checks complete, print a clean summary table:

```
╔══════════════════════════════════════════════════════╗
║           PRE-PUSH CHECKLIST SUMMARY                ║
╠══════════╦═══════════════════════════════════════════╣
║ Check    ║ Status                                    ║
╠══════════╬═══════════════════════════════════════════╣
║ Pre-Commit    ║ ✅ All hooks passed                 ║
║ Tests         ║ ✅ 12 passed, 2 new test files      ║
║ README        ║ ⚠️  Not updated (user confirmed OK) ║
║ CHANGELOG     ║ ✅ Entry added                      ║
║ pyproject.toml║ ✅ Bumped to 1.2.1                  ║
╚══════════╩═══════════════════════════════════════════╝

🟢 All checks passed — safe to push!
OR
🔴 X issue(s) require attention before pushing.
```

Only declare "safe to push" if there are **no ❌ (error) statuses**.
⚠️ (warnings) that the user has acknowledged are acceptable.

---

## Notes

- Always run checks **in order** (1 → 5); a ❌ on tests should pause the flow.
- Never auto-push. This skill only verifies. The user pushes manually.
- For monorepos, ask the user which sub-package to check.
