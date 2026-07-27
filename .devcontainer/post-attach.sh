#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/workspaces/rivtlib"

# Auto-activate venv in terminal and for all new bash sessions
if [[ -x "${ROOT_DIR}/.venv/bin/python" ]]; then
    source "${ROOT_DIR}/.venv/bin/activate"
    
    # Add venv activation to .bashrc so it's active in all new terminals
    if ! grep -q "source ${ROOT_DIR}/.venv/bin/activate" ~/.bashrc 2>/dev/null; then
        echo "source ${ROOT_DIR}/.venv/bin/activate" >> ~/.bashrc
    fi
    
    "${ROOT_DIR}/.venv/bin/python" -c "import rivtlib; print('rivtlib loaded from local source in Codespaces')"
else
    python -c "import rivtlib; print('rivtlib loaded in Codespaces')"
fi
