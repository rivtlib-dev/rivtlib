#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/workspaces/rivtlib"

if [[ -x "${ROOT_DIR}/.venv/bin/python" ]]; then
    "${ROOT_DIR}/.venv/bin/python" -c "import rivtlib; print('rivtlib loaded from local source in Codespaces')"
else
    python -c "import rivtlib; print('rivtlib loaded in Codespaces')"
fi
