#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# Build a repo-local environment so Codespaces uses pyproject.toml from this checkout.
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .

python -c "import rivtlib; print('Installed:', rivtlib.__file__)"

# Add a one-click VS Code task in the example workspace.
EXAMPLE_VSCODE_DIR="${ROOT_DIR}/examples/rivt-example-01/.vscode"
mkdir -p "${EXAMPLE_VSCODE_DIR}"
cat > "${EXAMPLE_VSCODE_DIR}/tasks.json" <<'EOF'
{
	"version": "2.0.0",
	"tasks": [
		{
			"label": "Run rivt example (uses local rivtlib)",
			"type": "shell",
			"command": "bash /workspaces/rivtlib/scripts/run-rivt-example.sh",
			"group": {
				"kind": "build",
				"isDefault": true
			},
			"presentation": {
				"reveal": "always",
				"panel": "shared"
			},
			"problemMatcher": []
		}
	]
}
EOF
