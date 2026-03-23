#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python pip dependencies
pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt"

# Install pylint (used as the project linter, listed in environment.yml)
pip install -q pylint
