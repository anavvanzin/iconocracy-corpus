#!/usr/bin/env bash
# release.sh — Release gate consolidado para ICONOCRACY
#
# Executa a sequência completa de validação, publicação e tagging.
# Uso:
#   ./tools/scripts/release.sh                    # validação completa (pré-release)
#   ./tools/scripts/release.sh --publish          # valida + publica HF + companion
#   ./tools/scripts/release.sh --dry-run          # preview sem escrever
#   ./tools/scripts/release.sh --note "..."       # release note personalizada
#
# Release gate (pré-requisito):
#   validate_schemas → vault_sync status → records→corpus diff → purification status

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY=/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python
TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
DRY_RUN=false
PUBLISH=false
NOTES=()
TAG="release-$(date +%Y%m%d)"

cd "$REPO_ROOT"

# ─── Parse args ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --publish)   PUBLISH=true; shift ;;
    --dry-run)   DRY_RUN=true; shift ;;
    --note)      NOTES+=("$2"); shift 2 ;;
    -h|--help)
      head -20 "$0" | grep '^#' | sed 's/^# \\?//'
      exit 0 ;;
    *) echo "Argumento desconhecido: $1"; exit 1 ;;
  esac
done

echo "═══════════════════════════════════════════════════════════════"
echo "  ICONOCRACY RELEASE GATE — $(date '+%Y-%m-%d %H:%M')"
echo "  Tag: $TAG"
echo "  Publish: $PUBLISH"
echo "═══════════════════════════════════════════════════════════════"

PASS=0
FAIL=0

_run() {
  local label=$1; shift
  echo ""
  echo "── $label ──"
  if $DRY_RUN; then
    echo "  [DRY-RUN] $*"
    PASS=$((PASS + 1))
  elif "$@" 2>&1; then
    echo "  ✓ $label"
    PASS=$((PASS + 1))
  else
    echo "  ✗ $label — FALHOU"
    FAIL=$((FAIL + 1))
  fi
}

# ─── Pre-release validation ────────────────────────────────────────────
_run "validate_schemas" $PY tools/scripts/validate_schemas.py
_run "vault_sync status" $PY tools/scripts/vault_sync.py status
_run "records_to_corpus diff" $PY tools/scripts/records_to_corpus.py --diff
_run "purification status" $PY tools/scripts/code_purification.py --status
_run "thesis terms check" $PY tools/scripts/check_thesis_terms.py
_run "idempotence check" $PY tools/scripts/check_corpus_export_idempotent.py

# ─── Abort on pre-release failures ─────────────────────────────────────
if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════"
  echo "  ✗ $FAIL validação(ões) falharam — abortando release"
  echo "  Corrija os erros antes de publicar."
  echo "═══════════════════════════════════════════════════════════════"
  exit 1
fi

# ─── Publish (opcional, só com --publish) ──────────────────────────────
if $PUBLISH; then
  echo ""
  echo "═══ PUBLICANDO RELEASE ═══"

  # Gerar nota de release
  NOTE_TEXT="${NOTES[*]:-release automático $TIMESTAMP}"

  # 1. Build HF release snapshot
  _run "build_hf_release" $PY tools/scripts/build_hf_release.py \
    --release-tag "$TAG" \
    --note "Pipeline release $TIMESTAMP: $NOTE_TEXT"

  # 2. Push dataset to HuggingFace
  _run "publish HF" $PY tools/scripts/build_hf_release.py \
    --release-tag "$TAG" \
    --publish \
    --note "$NOTE_TEXT"

  # 3. Sync companion app data
  _run "sync companion" $PY tools/scripts/sync_companion.py \
    --output data/companion/scout-data.json

  # Opcional: push para o companion app live
  # (descomentar quando endpoint estiver configurado)
  # _run "deploy companion" $PY tools/scripts/sync_companion.py \
  #   --push "https://iconocracia-companion.warholana.workers.dev"

  # 4. Git tag
  if ! $DRY_RUN; then
    git tag "$TAG" -m "Release $TAG: $NOTE_TEXT"
    echo "  ✓ Tagged: $TAG"
    echo "  Para fazer push: git push origin $TAG"
  fi

  echo ""
  echo "═══ RELEASE PUBLICADO ═══"
fi

# ─── Resumo ────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Release gate: $PASS ok / $FAIL falha"
if $PUBLISH; then
  echo "  Tag: $TAG"
  echo "  Para finalizar: git push origin $TAG"
fi
echo "═══════════════════════════════════════════════════════════════"

[[ $FAIL -eq 0 ]] || exit 1
