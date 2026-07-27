#!/usr/bin/env bash
set -euo pipefail

# Build and (optionally) upload wheel-only releases with twine.
# Defaults to TestPyPI for safer first-time usage.

MODE="testpypi"
UPLOAD="false"
CLEAN="false"

usage() {
    cat <<'EOF'
Usage: bash scripts/release-wheel.sh [options]

Options:
  --testpypi   Upload to TestPyPI (default)
  --pypi       Upload to PyPI
  --upload     Upload after build + twine check
  --clean      Remove dist/ before build
  -h, --help   Show this help

Examples:
  bash scripts/release-wheel.sh --clean
  bash scripts/release-wheel.sh --clean --upload --testpypi
  bash scripts/release-wheel.sh --upload --pypi

Notes:
  - Uploads wheel files only: dist/rivtlib-*.whl
  - Twine auth can use environment variables (recommended):
      TWINE_USERNAME=__token__
      TWINE_PASSWORD=<pypi-token>
EOF
}

for arg in "$@"; do
    case "$arg" in
        --testpypi)
            MODE="testpypi"
            ;;
        --pypi)
            MODE="pypi"
            ;;
        --upload)
            UPLOAD="true"
            ;;
        --clean)
            CLEAN="true"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            usage
            exit 1
            ;;
    esac
done

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [[ "${CLEAN}" == "true" ]]; then
    rm -rf dist
fi

python -m pip install --upgrade build twine
python -m build --sdist --wheel
python -m twine check dist/*

WHEELS=(dist/rivtlib-*.whl)
if [[ ! -e "${WHEELS[0]}" ]]; then
    echo "No wheel files found in dist/."
    exit 1
fi

if [[ "${UPLOAD}" == "true" ]]; then
    if [[ "${MODE}" == "testpypi" ]]; then
        python -m twine upload --repository testpypi "${WHEELS[@]}"
    else
        python -m twine upload "${WHEELS[@]}"
    fi
else
    echo "Build complete. Upload skipped (--upload not set)."
    echo "Wheel files:"
    ls -1 "${WHEELS[@]}"
fi
