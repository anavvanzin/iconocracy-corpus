#!/usr/bin/env bash
# run-corpus-batch.sh — Headless batch runner for corpus operations
#
# Runs heavy corpus tasks via Claude Code headless mode with checkpointing.
# Designed to be kicked off and left alone — logs progress, resumes on interrupt.
#
# Usage:
#   ./tools/run-corpus-batch.sh scout          # Run corpus scouting campaign
#   ./tools/run-corpus-batch.sh iconocode      # Batch IconoCode analysis on pending items
#   ./tools/run-corpus-batch.sh download       # Download missing corpus images
#   ./tools/run-corpus-batch.sh validate       # Schema validation + gap analysis
#   ./tools/run-corpus-batch.sh full           # All of the above in sequence
#
# Options:
#   --dry-run       Show what would run without executing
#   --batch-size N  Items per batch (default: 5)
#   --resume        Resume from last checkpoint
#   --country XX    Filter by country prefix (e.g., FR, BR)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGS_DIR="$REPO_ROOT/logs/batch"
CHECKPOINT_FILE="$LOGS_DIR/.checkpoint"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# Defaults
BATCH_SIZE=5
DRY_RUN=false
RESUME=false
COUNTRY=""
COMMAND=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        scout|iconocode|download|validate|full) COMMAND="$1" ;;
        --dry-run)      DRY_RUN=true ;;
        --batch-size)   BATCH_SIZE="$2"; shift ;;
        --resume)       RESUME=true ;;
        --country)      COUNTRY="$2"; shift ;;
        -h|--help)
            sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

if [[ -z "$COMMAND" ]]; then
    echo "Usage: $0 {scout|iconocode|download|validate|full} [options]"
    exit 1
fi

# Setup
mkdir -p "$LOGS_DIR"
LOG_FILE="$LOGS_DIR/${COMMAND}_${TIMESTAMP}.log"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
save_checkpoint() { echo "$1" > "$CHECKPOINT_FILE"; }
load_checkpoint() { [[ -f "$CHECKPOINT_FILE" ]] && cat "$CHECKPOINT_FILE" || echo ""; }

# Preflight checks
preflight() {
    log "=== Preflight checks ==="
    local ok=true

    # Python environment
    if ! conda run -n iconocracy python --version &>/dev/null; then
        log "FAIL: conda env 'iconocracy' not available"
        ok=false
    else
        log "OK: Python environment"
    fi

    # Repo state
    if [[ ! -f "$REPO_ROOT/corpus/corpus-data.json" ]]; then
        log "FAIL: corpus-data.json not found"
        ok=false
    else
        local count
        count=$(python3 -c "import json; print(len(json.load(open('$REPO_ROOT/corpus/corpus-data.json'))['items']))" 2>/dev/null || echo "?")
        log "OK: corpus-data.json ($count items)"
    fi

    # SSD check (for download command)
    if [[ "$COMMAND" == "download" || "$COMMAND" == "full" ]]; then
        if [[ -d /Volumes/ICONOCRACIA/corpus/imagens ]]; then
            log "OK: SSD mounted"
        else
            log "WARN: SSD not mounted — images will go to vault/assets/"
        fi
    fi

    # Claude CLI
    if ! command -v "$CLAUDE_BIN" &>/dev/null; then
        log "FAIL: claude CLI not found (set CLAUDE_BIN if non-standard path)"
        ok=false
    else
        log "OK: claude CLI"
    fi

    if [[ "$ok" == false ]]; then
        log "Preflight failed — aborting"
        exit 1
    fi
    log "=== Preflight passed ==="
}

# Run a claude headless prompt and log output
run_claude() {
    local task_name="$1"
    local prompt="$2"
    local task_log="$LOGS_DIR/${COMMAND}_${task_name}_${TIMESTAMP}.log"

    log "Starting: $task_name"
    if [[ "$DRY_RUN" == true ]]; then
        log "[dry-run] Would run: claude -p '${prompt:0:80}...'"
        return 0
    fi

    "$CLAUDE_BIN" -p "$prompt" \
        --allowedTools "Edit,Read,Bash,Grep,Glob,Write,Agent" \
        --output-format text \
        2>&1 | tee -a "$task_log"

    local exit_code=${PIPESTATUS[0]}
    if [[ $exit_code -eq 0 ]]; then
        log "Completed: $task_name"
        save_checkpoint "$task_name"
    else
        log "FAILED: $task_name (exit $exit_code) — see $task_log"
        return $exit_code
    fi
}

# ── Task: Schema validation + gap analysis ──────────────────────────
task_validate() {
    run_claude "validate" "
cd $REPO_ROOT && conda run -n iconocracy python tools/scripts/validate_schemas.py
Then run: conda run -n iconocracy python tools/scripts/lacunas.py
Report: total items, validation errors, gaps found. Be concise.
"
}

# ── Task: Download missing images ───────────────────────────────────
task_download() {
    local country_flag=""
    [[ -n "$COUNTRY" ]] && country_flag="--only items matching prefix $COUNTRY"

    run_claude "download" "
cd $REPO_ROOT
Run the image download script for corpus items that are missing images:
  conda run -n iconocracy python tools/scripts/download_corpus_images.py $country_flag

If any downloads fail due to IIIF issues, try Playwright browser bypass as fallback.
After downloads complete, report: downloaded count, failed count, total corpus coverage.
"
}

# ── Task: Batch IconoCode analysis ──────────────────────────────────
task_iconocode() {
    local country_filter=""
    [[ -n "$COUNTRY" ]] && country_filter="Filter to items with ID prefix '$COUNTRY'."

    run_claude "iconocode" "
cd $REPO_ROOT
Read corpus/corpus-data.json. Find all items where iconocode analysis is missing or incomplete
(no 'endurecimento' score, no 'panofsky' field, or status is 'pending').
$country_filter

Process them in batches of $BATCH_SIZE using parallel Agent sub-agents with subagent_type='iconocode-analyze'.
After each batch:
1. Validate the updated corpus-data.json schema
2. Save progress (the file is the checkpoint)
3. Report batch N/total complete

Use Python atomic updates for corpus-data.json writes.
If an item's image is unavailable, do metadata-based analysis and flag it.
"
}

# ── Task: Corpus scouting ───────────────────────────────────────────
task_scout() {
    local country_filter=""
    [[ -n "$COUNTRY" ]] && country_filter="Focus on country: $COUNTRY."

    run_claude "scout" "
cd $REPO_ROOT
Read vault/sessoes/ for recent session notes to understand what's been searched.
Read corpus/corpus-data.json to understand current coverage.
Run tools/scripts/lacunas.py to identify gaps.
$country_filter

Then run a scouting campaign targeting the top gaps:
- Search Europeana, Gallica, and other digital archives
- For each candidate found, create an Obsidian note in vault/candidatos/
- Use the SCOUT-[ID] naming convention
- After every $BATCH_SIZE candidates, save a session note to vault/sessoes/

If Europeana or Gallica APIs fail after 2 attempts, switch to alternate archives.
Report: candidates found, notes created, remaining gaps.
"
}

# ── Command dispatch ────────────────────────────────────────────────
preflight

case "$COMMAND" in
    validate)  task_validate ;;
    download)  task_download ;;
    iconocode) task_iconocode ;;
    scout)     task_scout ;;
    full)
        log "=== Full pipeline: validate → download → iconocode → scout ==="
        task_validate
        task_download
        task_iconocode
        task_scout
        log "=== Full pipeline complete ==="
        ;;
esac

log "Log saved to: $LOG_FILE"
log "Done."
