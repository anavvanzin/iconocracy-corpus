#!/usr/bin/env bash
# preflight.sh — Environment health check for the Iconocracy research workflow
#
# Run at the start of any session to catch auth, env, and connectivity issues
# before they waste an hour.
#
# Usage:
#   ./tools/preflight.sh          # full check with color dashboard
#   ./tools/preflight.sh --quick  # skip connectivity tests
#   ./tools/preflight.sh --fix    # auto-fix safe issues (stale env vars, etc.)
#   ./tools/preflight.sh --log    # save results to vault/sessoes/

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
QUICK=false
FIX=false
LOG=false

for arg in "$@"; do
    case "$arg" in
        --quick) QUICK=true ;;
        --fix)   FIX=true ;;
        --log)   LOG=true ;;
        -h|--help) sed -n '2,/^$/p' "$0" | sed 's/^# \?//'; exit 0 ;;
    esac
done

# ── Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0
FIXES=()
REPORT=""

pass()  { ((PASS++)); REPORT+="  ${GREEN}PASS${NC}  $1\n"; }
warn()  { ((WARN++)); REPORT+="  ${YELLOW}WARN${NC}  $1\n"; }
fail()  { ((FAIL++)); REPORT+="  ${RED}FAIL${NC}  $1\n"; }
header(){ REPORT+="\n${BOLD}${BLUE}[$1]${NC}\n"; }

# ── 1. Shell Profile — conflicting env vars ─────────────────────────
header "Shell Profile"

# Check for ANTHROPIC_API_KEY override (the known 429 culprit)
if grep -q 'ANTHROPIC_API_KEY' ~/.zshrc ~/.bash_profile ~/.zprofile 2>/dev/null; then
    fail "ANTHROPIC_API_KEY set in shell profile — can override OAuth and cause 429 loops"
    FIXES+=("Remove or comment out ANTHROPIC_API_KEY from shell profile")
else
    pass "No ANTHROPIC_API_KEY in shell profiles"
fi

# Check for GOOGLE_APPLICATION_CREDENTIALS (Vertex override)
if grep -q 'GOOGLE_APPLICATION_CREDENTIALS' ~/.zshrc ~/.bash_profile ~/.zprofile 2>/dev/null; then
    fail "GOOGLE_APPLICATION_CREDENTIALS in shell profile — overrides Claude OAuth with Vertex"
    FIXES+=("Remove GOOGLE_APPLICATION_CREDENTIALS from shell profile")
elif [[ -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]]; then
    warn "GOOGLE_APPLICATION_CREDENTIALS is set in current env: $GOOGLE_APPLICATION_CREDENTIALS"
    FIXES+=("unset GOOGLE_APPLICATION_CREDENTIALS")
else
    pass "No Vertex credential override"
fi

# Check for sourced anthropic env files
if grep -qE '^\s*source.*anthropic' ~/.zshrc ~/.bash_profile ~/.zprofile 2>/dev/null; then
    warn "Active 'source' of anthropic env file in shell profile (check if commented out)"
else
    pass "No anthropic env sourcing"
fi

# Check for exposed API keys (bare keys in profile)
exposed_keys=$(grep -cE '(export\s+\w*API_KEY\w*=|export\s+\w*SECRET\w*=|export\s+\w*TOKEN\w*=)' ~/.zshrc 2>/dev/null || echo 0)
if [[ "$exposed_keys" -gt 0 ]]; then
    warn "$exposed_keys API key(s) exported directly in .zshrc — consider using a secrets manager"
else
    pass "No bare API keys in .zshrc"
fi

# ── 2. Python Environment ───────────────────────────────────────────
header "Python Environment"

if command -v conda &>/dev/null; then
    pass "conda available"
else
    fail "conda not found"
fi

if conda env list 2>/dev/null | grep -q 'iconocracy'; then
    pass "conda env 'iconocracy' exists"

    py_version=$(conda run -n iconocracy python --version 2>/dev/null | awk '{print $2}')
    if [[ "$py_version" == 3.12* ]]; then
        pass "Python $py_version (3.12.x)"
    elif [[ -n "$py_version" ]]; then
        warn "Python $py_version — expected 3.12.x"
    else
        fail "Could not determine Python version in iconocracy env"
    fi

    # Check required packages
    for pkg in jsonschema rich; do
        if conda run -n iconocracy python -c "import $pkg" 2>/dev/null; then
            pass "Package: $pkg"
        else
            fail "Package missing: $pkg"
            FIXES+=("conda run -n iconocracy pip install $pkg")
        fi
    done
else
    fail "conda env 'iconocracy' not found"
    FIXES+=("conda create -n iconocracy python=3.12 && conda run -n iconocracy pip install -r $REPO_ROOT/requirements.txt")
fi

# ── 3. Git & Auth ───────────────────────────────────────────────────
header "Git & Auth"

# gh CLI
if command -v gh &>/dev/null; then
    if gh auth token &>/dev/null 2>&1; then
        pass "gh CLI authenticated ($(gh auth status 2>&1 | grep -o 'Logged in to [^ ]*' || echo 'token valid'))"
    else
        warn "gh CLI not authenticated — needed for push/PR, not for local corpus work"
        FIXES+=("gh auth login --web")
    fi
else
    warn "gh CLI not installed — needed for push/PR, not for local corpus work"
fi

# HTTPS remote (not SSH)
if [[ -d "$REPO_ROOT/.git" ]]; then
    remote_url=$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || echo "")
    if [[ "$remote_url" == https://* ]]; then
        pass "Git remote uses HTTPS: $remote_url"
    elif [[ "$remote_url" == git@* ]]; then
        warn "Git remote uses SSH — HTTPS is more reliable for this setup"
        FIXES+=("git -C $REPO_ROOT remote set-url origin $(echo "$remote_url" | sed 's|git@github.com:|https://github.com/|')")
    elif [[ -z "$remote_url" ]]; then
        warn "No git remote 'origin' configured"
    fi

    # Check for dirty state
    dirty=$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$dirty" -gt 0 ]]; then
        warn "$dirty uncommitted change(s) in repo"
    else
        pass "Working tree clean"
    fi
else
    warn "Not a git repo: $REPO_ROOT"
fi

# ── 4. Corpus Data ──────────────────────────────────────────────────
header "Corpus Data"

corpus_file="$REPO_ROOT/corpus/corpus-data.json"
if [[ -f "$corpus_file" ]]; then
    item_count=$(python3 -c "import json; d=json.load(open('$corpus_file')); print(len(d.get('items', d if isinstance(d, list) else [])))" 2>/dev/null || echo "?")
    pass "corpus-data.json: $item_count items"

    # Schema validation
    if conda run -n iconocracy python "$REPO_ROOT/tools/scripts/validate_schemas.py" &>/dev/null 2>&1; then
        pass "Schema validation passed"
    else
        warn "Schema validation had errors — run: python tools/scripts/validate_schemas.py"
    fi
else
    fail "corpus-data.json not found"
fi

# SSD
if [[ -d /Volumes/ICONOCRACIA/corpus/imagens ]]; then
    ssd_size=$(du -sh /Volumes/ICONOCRACIA/corpus/imagens 2>/dev/null | awk '{print $1}')
    pass "SSD mounted — images: $ssd_size"
else
    warn "SSD (ICONOCRACIA) not mounted — image operations will use vault/assets/"
fi

# Symlinks
broken_links=0
for link in "$REPO_ROOT"/data/raw/*/; do
    if [[ -L "${link%/}" ]] && [[ ! -e "${link%/}" ]]; then
        ((broken_links++))
    fi
done
if [[ "$broken_links" -gt 0 ]]; then
    warn "$broken_links broken symlink(s) in data/raw/ (SSD probably not mounted)"
else
    pass "data/raw/ symlinks OK"
fi

# ── 5. External Services (skip with --quick) ────────────────────────
if [[ "$QUICK" == false ]]; then
    header "External Services"

    check_url() {
        local name="$1" url="$2"
        if curl -sf --max-time 5 -o /dev/null "$url" 2>/dev/null; then
            pass "$name"
        else
            warn "$name unreachable — may cause pipeline fallbacks"
        fi
    }

    check_url "Europeana API"       "https://api.europeana.eu/record/v2/search.json?query=test&rows=1"
    check_url "Gallica (BnF)"       "https://gallica.bnf.fr/SRU?operation=searchRetrieve&query=test&maximumRecords=1"
    check_url "GitHub API"          "https://api.github.com/rate_limit"
    check_url "HuggingFace Hub"     "https://huggingface.co/api/whoami-v2"
    check_url "Cloudflare Workers"  "https://iconocracia-companion.warholana.workers.dev"
fi

# ── 6. Claude Code & MCP ────────────────────────────────────────────
header "Claude Code"

if command -v claude &>/dev/null; then
    claude_version=$(claude --version 2>/dev/null || echo "unknown")
    pass "Claude CLI: $claude_version"
else
    fail "Claude CLI not found"
fi

# Check hooks config
claude_settings="$HOME/.claude/settings.json"
if [[ -f "$claude_settings" ]]; then
    if python3 -c "import json; json.load(open('$claude_settings'))" 2>/dev/null; then
        pass "settings.json: valid JSON"
    else
        fail "settings.json: invalid JSON"
        FIXES+=("Rewrite $claude_settings with valid JSON")
    fi
else
    warn "No Claude settings.json found"
fi

# ── Dashboard ───────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║     ICONOCRACY — Environment Health Check    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo -e "$REPORT"
echo -e "${BOLD}─────────────────────────────────────────────${NC}"
echo -e "  ${GREEN}$PASS passed${NC}  ${YELLOW}$WARN warnings${NC}  ${RED}$FAIL failures${NC}"
echo -e "${BOLD}─────────────────────────────────────────────${NC}"

# ── Fixes ────────────────────────────────────────────────────────────
if [[ ${#FIXES[@]} -gt 0 ]]; then
    echo ""
    echo -e "${BOLD}Suggested fixes:${NC}"
    for i in "${!FIXES[@]}"; do
        echo -e "  $((i+1)). ${FIXES[$i]}"
    done

    if [[ "$FIX" == true ]]; then
        echo ""
        echo -e "${YELLOW}Auto-fixing safe issues...${NC}"
        for fix in "${FIXES[@]}"; do
            # Only auto-fix env var unsets and pip installs
            if [[ "$fix" == unset* ]] || [[ "$fix" == *"pip install"* ]]; then
                echo -e "  Running: $fix"
                eval "$fix" 2>/dev/null && echo -e "  ${GREEN}Done${NC}" || echo -e "  ${RED}Failed${NC}"
            else
                echo -e "  ${YELLOW}Manual:${NC} $fix"
            fi
        done
    fi
fi

# ── Log to vault ─────────────────────────────────────────────────────
if [[ "$LOG" == true ]]; then
    log_date=$(date +%Y-%m-%d)
    log_file="$REPO_ROOT/vault/sessoes/PREFLIGHT-${log_date}.md"
    mkdir -p "$REPO_ROOT/vault/sessoes"
    {
        echo "---"
        echo "type: preflight"
        echo "date: $log_date"
        echo "pass: $PASS"
        echo "warn: $WARN"
        echo "fail: $FAIL"
        echo "---"
        echo ""
        echo "# Preflight Check — $log_date"
        echo ""
        # Strip ANSI codes for markdown
        echo -e "$REPORT" | sed 's/\x1b\[[0-9;]*m//g'
        echo ""
        if [[ ${#FIXES[@]} -gt 0 ]]; then
            echo "## Fixes needed"
            for fix in "${FIXES[@]}"; do
                echo "- \`$fix\`"
            done
        fi
    } > "$log_file"
    echo ""
    echo -e "Log saved to: ${BLUE}$log_file${NC}"
fi

# Exit code: 1 if any failures
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
