#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/ana/Research/hub/iconocracy-corpus"
CHECKER="$HOME/.hermes/scripts/iconocracy_corpus_check.py"
SCHEMA_SCRIPT="$REPO/tools/scripts/validate_schemas.py"
RECORDS="$REPO/data/processed/records.jsonl"
MASTER_RECORD="master-record"
REPORT_DIR="$REPO/logs/corpus-watchdog"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT="$REPORT_DIR/$TS.jsonl"
CURRENT_BRANCH="$(git -C "$REPO" branch --show-current 2>/dev/null || echo 'unknown')"
STATUS="OK"
ERRORS=()
WARNINGS=()

mkdir -p "$REPORT_DIR"

# C1 checker
if [ ! -f "$CHECKER" ]; then
  ERRORS+=("missing_checker:$CHECKER")
else
  if ! python3 "$CHECKER" > "$REPORT_DIR/c1-$TS.json"; then
    ERRORS+=("c1_check_failed")
  fi
fi

# Schema validation
if [ ! -f "$SCHEMA_SCRIPT" ] || [ ! -f "$RECORDS" ]; then
  WARNINGS+=("schema_validation_skipped:missing_inputs")
else
  SCHEMA_OUT="$REPORT_DIR/schema-$TS.txt"
  if ! python3 "$SCHEMA_SCRIPT" "$RECORDS" --schema "$MASTER_RECORD" --verbose > "$SCHEMA_OUT" 2>&1; then
    STATUS="ERROR"
    ERRORS+=("schema_validation_failed")
  elif grep -qiE "(error|invalid|missing|failed|^[0-9]+/[0-9]+)" "$SCHEMA_OUT" && ! grep -qiE "All records are valid" "$SCHEMA_OUT"; then
    STATUS="WARNING"
    WARNINGS+=("schema_validation_warnings")
  fi
fi

json_array() {
  local first=1
  printf '['
  for item in "$@"; do
    if [ $first -eq 1 ]; then
      first=0
    else
      printf ','
    fi
    printf '"%s"' "$item"
  done
  printf ']'
}

# Summary JSONL
{
  printf '{"timestamp":"%s","status":"%s","branch":"%s","errors":%s,"warnings":%s,"artifacts":%s}\n' \
    "$TS" "$STATUS" "$CURRENT_BRANCH" \
    "$(json_array "${ERRORS[@]+"${ERRORS[@]}"}")" \
    "$(json_array "${WARNINGS[@]+"${WARNINGS[@]}"}")" \
    "$(json_array "c1-$TS.json" "schema-$TS.txt")"
} > "$REPORT"

if [ "$STATUS" = "ERROR" ]; then
  echo "corpus-watchdog: ERROR — see $REPORT_DIR"
  exit 1
fi

echo "corpus-watchdog: $STATUS — $REPORT"
exit 0
