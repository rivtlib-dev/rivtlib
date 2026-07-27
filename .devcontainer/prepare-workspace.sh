#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# Ensure the copied example workspace is present before VS Code opens it.
if [[ ! -d "${ROOT_DIR}/rivt-example-01" ]]; then
    echo "Missing copied example workspace: rivt-example-01"
    exit 1
fi

# Remove Claude Code from the example workspace recommendations.
python - <<'PY'
import json
from pathlib import Path

p = Path('/workspaces/rivtlib/rivt-example-01/.vscode/extensions.json')
if p.exists():
    data = json.loads(p.read_text(encoding='utf-8'))
    recs = data.get('recommendations', [])
    data['recommendations'] = [
        ext for ext in recs if ext != 'anthropic.claude-code'
    ]
    p.write_text(json.dumps(data, indent=4) + '\n', encoding='utf-8')
PY
