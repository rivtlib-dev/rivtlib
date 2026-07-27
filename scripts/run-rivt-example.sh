#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXAMPLE_DIR="${ROOT_DIR}/rivt-example-01/rivt-report"

if [[ ! -d "${EXAMPLE_DIR}" ]]; then
    echo "Missing example files. Check that rivt-example-01 was copied into the repo root."
    exit 1
fi

if [[ ! -x "${ROOT_DIR}/.venv/bin/python" ]]; then
    echo "Missing .venv. Run: bash .devcontainer/post-create.sh"
    exit 1
fi

cd "${EXAMPLE_DIR}"
"${ROOT_DIR}/.venv/bin/python" rv001-doc-example01.py
