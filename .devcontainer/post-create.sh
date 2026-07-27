#!/usr/bin/env bash
set -euo pipefail

# Build a repo-local environment so Codespaces uses pyproject.toml from this checkout.
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .

python -c "import rivtlib; print('Installed:', rivtlib.__file__)"
