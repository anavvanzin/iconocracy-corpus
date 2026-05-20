#!/usr/bin/env bash
# autopilot.sh — Autonomous corpus pipeline with self-healing
#
# End-to-end pipeline that runs preflight → gap analysis → scouting →
# image download → IconoCode analysis → validation, with per-item
# error recovery and structured session logs.
#
# Unlike run-corpus-batch.sh (which wraps individual tasks), autopilot
# chains everything with feedback loops: failures in one stage inform
# the next, and the pipeline adapts its strategy mid-run.
#
# Usage:
#   ./tools/autopilot.sh                          # full autonomous run
#   ./tools/autopilot.sh --stage iconocode        # start from a specific stage
#   ./tools/autopilot.sh --country FR             # filter to one country
#   ./tools/autopilot.sh --max-items 20           # cap total items processed
#   ./tools/autopilot.sh --dry-run                # preview plan without executing
#   ./tools/autopilot.sh --resume                 # resume from last checkpoint
#
# Stages (in order):
#   1. preflight    — environment health check (aborts on FAIL)
#   2. gaps         — identify corpus coverage gaps via lacunas.py
#   3. scout        — search archives for candidates to fill gaps
#   4. download     — fetch images (IIIF → direct URL → Playwright)
#   5. iconocode    — run IconoCode analysis on uncoded items
#   6. validate     — schema validation + final report
#   7. report       — session summary to vault/sessoes/

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGS_DIR="$REPO_ROOT/logs/autopilot"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOGS_DIR/autopilot_${TIMESTAMP}.log"
CHECKPOINT_FILE="$LOGS_DIR/.autopilot-checkpoint"
STATE_FILE="$LOGS_DIR/.autopilot-state.json"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

# Defaults
DRY_RUN=false
RESUME=false
COUNTRY=""
MAX_ITEMS=50
START_STAGE="preflight"
BATCH_SIZE=5

ALL_STAGES=(preflight gaps scout download iconocode validate report)

# ── Parse arguments ─────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --stage)      START_STAGE="$2"; shift ;;
        --country)    COUNTRY="$2"; shift ;;
        --max-items)  MAX_ITEMS="$2"; shift ;;
        --batch-size) BATCH_SIZE="$2"; shift ;;
        --dry-run)    DRY_RUN=true ;;
        --resume)     RESUME=true ;;
        -h|--help)    sed -n '2,/^$/p' "$0" | sed 's/^# \?//'; exit 0 ;;
        *)            echo "Unknown: $1"; exit 1 ;;
    esac
    shift
done

mkdir -p "$LOGS_DIR"

# ── Logging ─────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

log()  { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
stage_header() {
    echo "" | tee -a "$LOG_FILE"
    echo -e "${BOLD}${BLUE}━━━ Stage: $1 ━━━${NC}" | tee -a "$LOG_FILE"
}

# ── State management ────────────────────────────────────────────────
save_state() {
    # Save pipeline state as JSON for resume capability
    python3 -c "
import json, sys
state = {
    'timestamp': '$TIMESTAMP',
    'last_stage': '$1',
    'country': '$COUNTRY',
    'max_items': $MAX_ITEMS,
    'items_processed': ${2:-0},
    'items_failed': ${3:-0},
    'gaps_found': ${4:-0}
}
json.dump(state, open('$STATE_FILE', 'w'), indent=2)
"
    echo "$1" > "$CHECKPOINT_FILE"
}

load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        python3 -c "import json; s=json.load(open('$STATE_FILE')); print(f'Last run: {s[\"timestamp\"]}, stage: {s[\"last_stage\"]}, processed: {s[\"items_processed\"]}, failed: {s[\"items_failed\"]}')"
    fi
    if [[ -f "$CHECKPOINT_FILE" ]]; then
        cat "$CHECKPOINT_FILE"
    fi
}

# Determine starting stage
if [[ "$RESUME" == true ]]; then
    last=$(load_state)
    if [[ -n "$last" ]]; then
        log "Resuming from stage: $last"
        # Start from the stage AFTER the last completed one
        found=false
        for s in "${ALL_STAGES[@]}"; do
            if [[ "$found" == true ]]; then
                START_STAGE="$s"
                break
            fi
            [[ "$s" == "$last" ]] && found=true
        done
    fi
fi

should_run() {
    local stage="$1"
    local start_idx=-1 stage_idx=-1
    for i in "${!ALL_STAGES[@]}"; do
        [[ "${ALL_STAGES[$i]}" == "$START_STAGE" ]] && start_idx=$i
        [[ "${ALL_STAGES[$i]}" == "$stage" ]] && stage_idx=$i
    done
    [[ $stage_idx -ge $start_idx ]]
}

# ── Claude runner with retry ────────────────────────────────────────
run_claude_with_retry() {
    local task_name="$1"
    local prompt="$2"
    local max_retries="${3:-2}"
    local attempt=0
    local task_log="$LOGS_DIR/${task_name}_${TIMESTAMP}.log"

    while [[ $attempt -lt $max_retries ]]; do
        ((attempt++))
        log "[$task_name] Attempt $attempt/$max_retries"

        if [[ "$DRY_RUN" == true ]]; then
            log "[dry-run] Would run claude -p for: $task_name"
            return 0
        fi

        "$CLAUDE_BIN" -p "$prompt" \
            --allowedTools "Edit,Read,Bash,Grep,Glob,Write,Agent" \
            --output-format text \
            2>&1 | tee -a "$task_log"

        local exit_code=${PIPESTATUS[0]}
        if [[ $exit_code -eq 0 ]]; then
            log "[$task_name] Completed"
            return 0
        fi

        log "[$task_name] Failed (exit $exit_code)"
        if [[ $attempt -lt $max_retries ]]; then
            log "[$task_name] Retrying in 10s..."
            sleep 10
        fi
    done

    log "[$task_name] All $max_retries attempts failed — see $task_log"
    return 1
}

# ── Country filter clause for prompts ───────────────────────────────
country_clause() {
    if [[ -n "$COUNTRY" ]]; then
        echo "Filter to items with country prefix '$COUNTRY' only."
    fi
}

# ══════════════════════════════════════════════════════════════════════
# STAGES
# ══════════════════════════════════════════════════════════════════════

# ── 1. Preflight ────────────────────────────────────────────────────
stage_preflight() {
    stage_header "preflight"
    "$REPO_ROOT/tools/preflight.sh" --quick 2>&1 | tee -a "$LOG_FILE"
    local exit_code=${PIPESTATUS[0]}
    if [[ $exit_code -ne 0 ]]; then
        log "Preflight found failures. Attempting auto-fix..."
        "$REPO_ROOT/tools/preflight.sh" --quick --fix 2>&1 | tee -a "$LOG_FILE"
        # Re-check
        "$REPO_ROOT/tools/preflight.sh" --quick 2>&1 | tee -a "$LOG_FILE"
        if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
            log "Preflight still failing — manual intervention needed. Aborting."
            exit 1
        fi
    fi
    save_state "preflight"
}

# ── 2. Gap analysis ────────────────────────────────────────────────
stage_gaps() {
    stage_header "gaps"
    local country_flag=""
    [[ -n "$COUNTRY" ]] && country_flag="--country $COUNTRY"

    log "Running lacunas.py..."
    local gaps_output
    gaps_output=$(conda run -n iconocracy python "$REPO_ROOT/tools/scripts/lacunas.py" $country_flag 2>&1) || true
    echo "$gaps_output" | tee -a "$LOG_FILE"

    # Extract gap count for state
    local gap_count
    gap_count=$(echo "$gaps_output" | grep -c "GAP\|gap\|missing" || echo "0")
    save_state "gaps" 0 0 "$gap_count"
    log "Gaps identified: $gap_count"
}

# ── 3. Scout ────────────────────────────────────────────────────────
stage_scout() {
    stage_header "scout"
    run_claude_with_retry "scout" "
cd $REPO_ROOT

You are the Corpus Scout for the ICONOCRACY thesis. Read SKILL.md for your full role.

TASK: Fill corpus coverage gaps by searching digital archives.

CONTEXT:
- Read vault/sessoes/ for recent session notes (avoid re-searching)
- Read corpus/corpus-data.json for current coverage
- Run: conda run -n iconocracy python tools/scripts/lacunas.py $([ -n "$COUNTRY" ] && echo "--country $COUNTRY")
$(country_clause)

STRATEGY (with fallbacks):
1. Search Europeana API first
2. If Europeana fails or rate-limits after 2 attempts → switch to Gallica SRU
3. If Gallica also fails → search via web_search for specific archive catalogs
4. Never spend more than 3 attempts on any single API

For each candidate found:
- Create an Obsidian note in vault/candidatos/ using SCOUT-[ID] format
- Follow the exact template from SKILL.md
- Include all required metadata fields

LIMITS:
- Process at most $MAX_ITEMS candidates
- After every $BATCH_SIZE candidates, save a session note to vault/sessoes/
- Stop and save progress if you encounter 3 consecutive API failures

Report: candidates found, notes created, APIs used, any issues.
"
    save_state "scout"
}

# ── 4. Download ─────────────────────────────────────────────────────
stage_download() {
    stage_header "download"
    run_claude_with_retry "download" "
cd $REPO_ROOT

TASK: Download missing corpus images using the fallback chain.

FALLBACK CHAIN (try in order, move to next after 2 failures):
1. IIIF manifest → full resolution image
2. url_image_download field (direct URL)
3. thumbnail_url (last resort for metadata-only analysis)
4. If all fail → flag item with #sem-imagem for Playwright bypass later

Run: conda run -n iconocracy python tools/scripts/download_corpus_images.py $([ -n "$COUNTRY" ] && echo "--only $COUNTRY")

$(country_clause)

After the script completes:
- Check download-report.md for failures
- For any items that failed with 403/429, attempt Playwright browser bypass:
  Use Bash to run a headless Playwright script that navigates to the source URL and saves the image
- If SSD is not mounted, save to vault/assets/ and tag with #mover-para-ssd

Report: total downloaded, failed count, coverage percentage.
"
    save_state "download"
}

# ── 5. IconoCode ────────────────────────────────────────────────────
stage_iconocode() {
    stage_header "iconocode"
    run_claude_with_retry "iconocode" "
cd $REPO_ROOT

TASK: Run IconoCode analysis on all uncoded corpus items.

1. Read corpus/corpus-data.json
2. Find items missing IconoCode analysis (no 'endurecimento' score, no 'panofsky' field, or status 'pending')
$(country_clause)

3. Process in batches of $BATCH_SIZE using parallel Agent sub-agents (subagent_type='iconocode-analyze')

FOR EACH ITEM:
- If image exists in data/raw/[PAIS]/ → full visual analysis (3-level Panofsky + 10 indicators)
- If image unavailable → metadata-based analysis using description, support type, period, and regime
  Flag as 'metadata-only' in the analysis notes

AFTER EACH BATCH:
- Use Python atomic update to write results to corpus-data.json
- Run: conda run -n iconocracy python tools/scripts/validate_schemas.py
- If validation fails → diagnose the error, fix the JSON, re-validate before continuing
- Log: 'Batch N/total: X coded, Y failed, Z metadata-only'

SELF-HEALING:
- If a sub-agent fails → retry that single item once, then skip and log
- If validation fails after fix attempt → rollback that batch (re-read corpus-data.json from git)
- Never proceed to next batch with invalid JSON

Cap at $MAX_ITEMS items total.
Report: total coded, metadata-only count, failures, final validation status.
" 3  # 3 retries for this heavy stage
    save_state "iconocode"
}

# ── 6. Validate ─────────────────────────────────────────────────────
stage_validate() {
    stage_header "validate"
    log "Running schema validation..."
    conda run -n iconocracy python "$REPO_ROOT/tools/scripts/validate_schemas.py" 2>&1 | tee -a "$LOG_FILE"

    log "Running gap analysis..."
    conda run -n iconocracy python "$REPO_ROOT/tools/scripts/lacunas.py" 2>&1 | tee -a "$LOG_FILE"

    log "Running coding progress check..."
    conda run -n iconocracy python "$REPO_ROOT/tools/scripts/code_purification.py" --status 2>&1 | tee -a "$LOG_FILE"

    save_state "validate"
}

# ── 7. Report ───────────────────────────────────────────────────────
stage_report() {
    stage_header "report"
    local report_date
    report_date=$(date +%Y-%m-%d)
    local report_file="$REPO_ROOT/vault/sessoes/AUTOPILOT-${report_date}.md"

    # Count corpus items
    local item_count
    item_count=$(python3 -c "
import json
d = json.load(open('$REPO_ROOT/corpus/corpus-data.json'))
items = d.get('items', d if isinstance(d, list) else [])
print(len(items))
" 2>/dev/null || echo "?")

    mkdir -p "$REPO_ROOT/vault/sessoes"
    cat > "$report_file" << EOF
---
type: autopilot-session
date: $report_date
corpus_items: $item_count
country_filter: ${COUNTRY:-all}
max_items: $MAX_ITEMS
start_stage: $START_STAGE
---

# Autopilot Session — $report_date

## Parameters
- **Country filter**: ${COUNTRY:-all countries}
- **Max items**: $MAX_ITEMS
- **Batch size**: $BATCH_SIZE
- **Start stage**: $START_STAGE

## Pipeline Log
\`\`\`
$(tail -50 "$LOG_FILE" 2>/dev/null || echo "No log available")
\`\`\`

## Corpus State
- **Total items**: $item_count

## Files
- Full log: \`$LOG_FILE\`

---
tags: corpus/sessao-scout, #autopilot
EOF

    log "Session report saved to: $report_file"
    save_state "report"
}

# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       ICONOCRACY — Autopilot Pipeline        ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""
log "Starting autopilot: stage=$START_STAGE country=${COUNTRY:-all} max=$MAX_ITEMS batch=$BATCH_SIZE"
[[ "$DRY_RUN" == true ]] && log "*** DRY RUN MODE ***"

should_run "preflight" && stage_preflight
should_run "gaps"      && stage_gaps
should_run "scout"     && stage_scout
should_run "download"  && stage_download
should_run "iconocode" && stage_iconocode
should_run "validate"  && stage_validate
should_run "report"    && stage_report

echo ""
echo -e "${BOLD}${GREEN}Autopilot complete.${NC}"
log "Full log: $LOG_FILE"
log "Done."
