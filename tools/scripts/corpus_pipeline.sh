#!/usr/bin/env bash
# corpus_pipeline.sh — Pipeline sequencial para manutenção diária do corpus
#
# Executa os passos canônicos de validação, sync e exportação em ordem.
# Cada passo é independente e falhas interrompem o pipeline (set -e).
#
# Uso:
#   ./tools/scripts/corpus_pipeline.sh              # pipeline completo
#   ./tools/scripts/corpus_pipeline.sh --dry-run     # preview sem escrita
#   ./tools/scripts/corpus_pipeline.sh --step N      # executa só o passo N
#   ./tools/scripts/corpus_pipeline.sh --from N      # executa a partir do passo N
#
# Passos:
#   1. Validar schemas JSON
#   2. Sync vault ↔ records.jsonl
#   3. Exportar records → corpus-data.json
#   4. Regenerar CSV (purification export)
#   5. Atualizar dashboards HTML
#   6. Análise de lacunas
#   7. Relatório de status final

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONDA_ENV="iconocracy"
TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
LOG_DIR="${REPO_ROOT}/logs"
LOG_FILE="${LOG_DIR}/pipeline_${TIMESTAMP}.log"
DRY_RUN=false
STEP_ONLY=0
STEP_FROM=1

# ─── Parse args ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --step)    STEP_ONLY="$2"; shift 2 ;;
    --from)    STEP_FROM="$2"; shift 2 ;;
    -h|--help)
      head -20 "$0" | grep '^#' | sed 's/^# \?//'
      exit 0 ;;
    *) echo "Argumento desconhecido: $1"; exit 1 ;;
  esac
done

# ─── Helpers ────────────────────────────────────────────────────────────
mkdir -p "$LOG_DIR"

_py() {
  conda run -n "$CONDA_ENV" python "$@" 2>&1
}

_run_step() {
  # Run a command, log output, return its exit code
  local output
  output=$("$@" 2>&1) || { echo "$output" | tee -a "$LOG_FILE"; return 1; }
  echo "$output" | tee -a "$LOG_FILE"
  return 0
}

_step_enabled() {
  local n=$1
  if [[ $STEP_ONLY -gt 0 ]]; then
    [[ $STEP_ONLY -eq $n ]]
  else
    [[ $n -ge $STEP_FROM ]]
  fi
}

_header() {
  local n=$1; shift
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  PASSO $n: $*"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

PASS=0
FAIL=0
SKIP=0

_record() {
  local status=$1
  case "$status" in
    pass) PASS=$((PASS + 1)) ;;
    fail) FAIL=$((FAIL + 1)) ;;
    skip) SKIP=$((SKIP + 1)) ;;
  esac
}

# ─── Pipeline ───────────────────────────────────────────────────────────
cd "$REPO_ROOT"

echo "CORPUS PIPELINE — $(date '+%Y-%m-%d %H:%M')"
echo "Repo: $REPO_ROOT"
echo "Dry-run: $DRY_RUN"
echo "" | tee -a "$LOG_FILE"

# --- Passo 1: Validar schemas -------------------------------------------
if _step_enabled 1; then
  _header 1 "Validar schemas JSON"
  if _run_step _py tools/scripts/validate_schemas.py; then
    echo "  [OK] Schemas válidos"
    _record pass
  else
    echo "  [ERRO] Falha na validação de schemas"
    _record fail
    exit 1
  fi
else
  _record skip
fi

# --- Passo 2: Sync vault ↔ records --------------------------------------
if _step_enabled 2; then
  _header 2 "Sync vault <-> records.jsonl"
  if $DRY_RUN; then
    if _run_step _py tools/scripts/vault_sync.py diff; then
      echo "  [DRY-RUN] diff exibido, nada escrito"
    else
      echo "  [DRY-RUN] diff exibido (com diferenças)"
    fi
    _record pass
  else
    if _run_step _py tools/scripts/vault_sync.py sync; then
      echo "  [OK] Sync concluído"
      _record pass
    else
      echo "  [ERRO] Falha no sync vault <-> records"
      _record fail
    fi
  fi
else
  _record skip
fi

# --- Passo 3: Exportar records → corpus-data.json -----------------------
if _step_enabled 3; then
  _header 3 "Exportar records -> corpus-data.json"
  if $DRY_RUN; then
    if _run_step _py tools/scripts/records_to_corpus.py --diff; then
      echo "  [DRY-RUN] diff exibido, nada escrito"
    else
      echo "  [DRY-RUN] diff exibido (com diferenças)"
    fi
    _record pass
  else
    if _run_step _py tools/scripts/records_to_corpus.py; then
      echo "  [OK] Exportação concluída"
      _record pass
    else
      echo "  [ERRO] Falha na exportação records -> corpus"
      _record fail
    fi
  fi
else
  _record skip
fi

# --- Passo 4: Regenerar CSV (purification export) -----------------------
if _step_enabled 4; then
  _header 4 "Regenerar corpus_dataset.csv"
  if $DRY_RUN; then
    echo "  [DRY-RUN] Pulando regeneração CSV"
  else
    if _run_step _py tools/scripts/code_purification.py --export-csv; then
      echo "  [OK] CSV atualizado"
      _record pass
    else
      echo "  [ERRO] Falha na regeneração CSV"
      _record fail
    fi
  fi
else
  _record skip
fi

# --- Passo 5: Atualizar dashboards HTML ---------------------------------
if _step_enabled 5; then
  _header 5 "Atualizar dashboards HTML"
  if $DRY_RUN; then
    echo "  [DRY-RUN] Pulando refresh de dashboards"
  else
    if _run_step _py tools/scripts/refresh_dashboard.py; then
      echo "  [OK] Dashboards atualizados"
      _record pass
    else
      echo "  [ERRO] Falha ao atualizar dashboards"
      _record fail
    fi
  fi
else
  _record skip
fi

# --- Passo 6: Análise de lacunas ----------------------------------------
if _step_enabled 6; then
  _header 6 "Análise de lacunas"
  if _run_step _py tools/scripts/lacunas.py; then
    echo "  [OK] Lacunas mapeadas"
    _record pass
  else
    echo "  [ERRO] Falha na análise de lacunas"
    _record fail
  fi
else
  _record skip
fi

# --- Passo 7: Relatório de status final ---------------------------------
if _step_enabled 7; then
  _header 7 "Relatório de status"
  echo ""
  echo "── records.jsonl ──"
  _run_step _py tools/scripts/vault_sync.py status || true
  echo ""
  echo "── ENDURECIMENTO ──"
  _run_step _py tools/scripts/code_purification.py --status || true
  echo ""
  _record pass
else
  _record skip
fi

# ─── Resumo ─────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESUMO: $PASS ok / $FAIL falha / $SKIP pulados"
echo "  Log: $LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ $FAIL -eq 0 ]] || exit 1
