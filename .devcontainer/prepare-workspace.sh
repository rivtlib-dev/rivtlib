#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# Ensure the bundled example exists before VS Code opens the configured workspace folder.
git submodule update --init --recursive

# Remove Claude Code from the example workspace recommendations.
python - <<'PY'
import json
from pathlib import Path

p = Path('/workspaces/rivtlib/examples/rivt-example-01/.vscode/extensions.json')
if p.exists():
    data = json.loads(p.read_text(encoding='utf-8'))
    recs = data.get('recommendations', [])
    data['recommendations'] = [
        ext for ext in recs if ext != 'anthropic.claude-code'
    ]
    p.write_text(json.dumps(data, indent=4) + '\n', encoding='utf-8')
PY
