# Codespaces Startup

This repo includes a devcontainer configuration for GitHub Codespaces.

## What happens on startup

- Uses a Python 3.14 container image.
- Creates a repo-local virtual environment at `.venv`.
- Installs this repository from `pyproject.toml` using `python -m pip install -e .`.
- Verifies the package import when the workspace is attached.

## Open in Codespaces

1. Push this repository to GitHub.
2. In GitHub, click **Code** > **Codespaces** > **Create codespace on main**.
3. Wait for container setup to finish.
4. Confirm startup output shows: `rivtlib loaded from local source in Codespaces`.
