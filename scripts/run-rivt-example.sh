#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXAMPLE_DIR="${ROOT_DIR}/examples/rivt-example-01/rivt-report"

if [[ ! -d "${EXAMPLE_DIR}" ]]; then
    echo "Missing example files. Run: git submodule update --init --recursive"
    exit 1
fi

if [[ ! -x "${ROOT_DIR}/.venv/bin/python" ]]; then
    echo "Missing .venv. Run: bash .devcontainer/post-create.sh"
    exit 1
fi

cd "${EXAMPLE_DIR}"
"${ROOT_DIR}/.venv/bin/python" rv001-doc-example01.py
