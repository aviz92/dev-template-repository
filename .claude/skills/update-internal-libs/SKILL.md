---
description: Regenerate the python-internal-libs rules with all the available package names
disable-model-invocation: true
allowed-tools: Bash(python scripts/fetch_pypi_packages.py)
---

Current internal library versions from PyPI:
!`python scripts/fetch_pypi_packages.py`

Rewrite `.claude/rules/python/python-internal-libs.md` using the available package names above.
Keep all existing rule content — only update new package names references.
