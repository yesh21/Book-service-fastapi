#!/bin/bash
set -euo pipefail


SKIP_INSTALL=false

# Check for the --skip-install argument
for arg in "$@"; do
    if [[ "$arg" == "--skip-install" ]]; then
        SKIP_INSTALL=true
    fi
done

# Create and activate virtual environment if not already present
if [[ ! -d .venv ]]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# Install dependencies unless --skip-install is used
if [[ "$SKIP_INSTALL" != true ]]; then
    pip install -r requirements.txt
fi

# Lint with flake8
flake8 --exit-zero --verbose

# Run tests with coverage
coverage run -m pytest tests/ -v
coverage report -m

# Optionally generate HTML coverage report
coverage html -d htmlcov

# run the app
uvicorn app.main:app --reload