# Codespaces Startup

This repo includes a devcontainer configuration for GitHub Codespaces.

Codespaces opens in `examples/rivt-example-01` so users land in the example
project first.

## What happens on startup

- Uses a stable Debian Bookworm base devcontainer image.
- Installs Python 3.14 using the official devcontainer Python feature.
- Initializes submodules, including `examples/rivt-example-01`.
- Creates a repo-local virtual environment at `/workspaces/rivtlib/.venv`.
- Installs this repository from `pyproject.toml` using `python -m pip install -e .`.
- Verifies the package import when the workspace is attached.

## Open in Codespaces

1. Push this repository to GitHub.
2. In GitHub, click **Code** > **Codespaces** > **Create codespace on main**.
3. Wait for container setup to finish.
4. Confirm startup output shows: `rivtlib loaded from local source in Codespaces`.

## Run the bundled example

After startup completes, run:

```bash
bash scripts/run-rivt-example.sh
```

This executes `examples/rivt-example-01/rivt-report/rv001-doc-example01.py`
using this repository's local `rivtlib` install.

Or use one click in VS Code:

- Terminal -> Run Task -> `Run rivt example (uses local rivtlib)`
