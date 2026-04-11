---
description: Regenerate the python-internal-libs rules with latest PyPI versions
disable-model-invocation: true
allowed-tools: Bash(python scripts/fetch_pypi_packages.py)
---

Current internal library versions from PyPI:
!`python scripts/fetch_pypi_packages.py`

Rewrite `.claude/rules/python/python-internal-libs.md` using the versions above.
Keep all existing rule content — only update version references.
