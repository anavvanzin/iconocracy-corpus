#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

DIR="$CLAUDE_PROJECT_DIR"

echo "=== Iconocracy Corpus — Environment Check ==="

# 1. Python dependencies
echo "[1/5] Installing Python dependencies..."
pip install -q -r "$DIR/requirements.txt"
pip install -q pylint pytest

# 2. Verify required directories exist
echo "[2/5] Checking directory structure..."
REQUIRED_DIRS=(
  "data/raw"
  "data/interim"
  "data/processed"
  "data/docs"
  "sources"
  "corpus"
  "tese/manuscrito"
  "tese/pesquisa"
  "tese/revisoes"
  "tools/scripts"
  "tools/schemas"
  "vault/tese"
  "examples"
)
MISSING=0
for d in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$DIR/$d" ]; then
    echo "  MISSING: $d"
    MISSING=$((MISSING + 1))
  fi
done
if [ "$MISSING" -eq 0 ]; then
  echo "  All $((${#REQUIRED_DIRS[@]})) directories present."
else
  echo "  WARNING: $MISSING directory(ies) missing."
fi

# 3. Verify key data files
echo "[3/5] Checking key data files..."
KEY_FILES=(
  "corpus/corpus-data.json"
  "data/processed/corpus_dataset.csv"
  "vault/tese/references.bib"
  "tools/schemas/master-record.schema.json"
  "tools/schemas/iconocode-output.schema.json"
)
for f in "${KEY_FILES[@]}"; do
  if [ -f "$DIR/$f" ]; then
    echo "  OK: $f"
  else
    echo "  MISSING: $f"
  fi
done

# 4. Validate corpus JSON
echo "[4/5] Validating corpus data..."
if python -c "import json; json.load(open('$DIR/corpus/corpus-data.json'))" 2>/dev/null; then
  ITEMS=$(python -c "import json; print(len(json.load(open('$DIR/corpus/corpus-data.json'))))")
  echo "  corpus-data.json: $ITEMS items, valid JSON."
else
  echo "  WARNING: corpus-data.json is invalid or missing."
fi

# 5. Check external tools
echo "[5/5] Checking external tools..."
for cmd in python3 git pandoc; do
  if command -v "$cmd" &>/dev/null; then
    echo "  $cmd: $($cmd --version 2>&1 | head -1)"
  else
    echo "  $cmd: NOT FOUND"
  fi
done

echo "=== Environment check complete ==="
