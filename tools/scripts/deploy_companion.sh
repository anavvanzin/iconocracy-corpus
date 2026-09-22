#!/usr/bin/env bash
# deploy_companion.sh — Deploy ICONOCRACY companion app data
#
# Gera scout-data.json do corpus e faz deploy no Cloudflare Workers.
# O companion app está em ~/Documents/GitHub/iconocracy-corpus/deploy/iconocracia-companion/
# e o deploy usa wrangler.
#
# Uso:
#   ./tools/scripts/deploy_companion.sh              # sync + deploy completo
#   ./tools/scripts/deploy_companion.sh --sync-only   # só gerar dados
#   ./tools/scripts/deploy_companion.sh --dry-run     # preview

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY=/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python
COMPANION_REPO="$HOME/Documents/GitHub/iconocracy-corpus"
COMPANION_DEPLOY="$COMPANION_REPO/deploy/iconocracia-companion"
SYNC_ONLY=false
DRY_RUN=false

cd "$REPO_ROOT"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sync-only) SYNC_ONLY=true; shift ;;
    --dry-run)   DRY_RUN=true; shift ;;
    -h|--help)
      head -20 "$0" | grep '^#' | sed 's/^# \\?//'
      exit 0 ;;
    *) echo "Argumento desconhecido: $1"; exit 1 ;;
  esac
done

echo "═══ COMPANION DEPLOY — $(date '+%Y-%m-%d %H:%M') ═══"

# 1. Gera scout-data.json
echo "── Gerando scout-data.json ──"
if $DRY_RUN; then
  $PY tools/scripts/sync_companion.py 2>&1 | tail -5
  echo "[DRY-RUN] scout-data.json seria salvo em data/companion/scout-data.json"
else
  mkdir -p data/companion
  $PY tools/scripts/sync_companion.py --output data/companion/scout-data.json 2>&1
  echo "✓ scout-data.json ($(wc -c < data/companion/scout-data.json) bytes)"
fi

$SYNC_ONLY && { echo "═══ Sync-only: deploy pulado ═══"; exit 0; }

# 2. Copia para o repositório do companion app
echo "── Copiando para companion repo ──"
if [ ! -d "$COMPANION_DEPLOY" ]; then
  echo "⚠ Companion repo não encontrado em $COMPANION_DEPLOY"
  echo "  Copie manualmente: cp data/companion/scout-data.json <destino>/public/scout-data.json"
  exit 1
fi

if $DRY_RUN; then
  echo "[DRY-RUN] cp data/companion/scout-data.json $COMPANION_DEPLOY/public/scout-data.json"
else
  cp data/companion/scout-data.json "$COMPANION_DEPLOY/public/scout-data.json"
  echo "✓ Copiado para $COMPANION_DEPLOY/public/scout-data.json"
fi

# 3. Deploy via wrangler
echo "── Deploy Cloudflare ──"
if $DRY_RUN; then
  echo "[DRY-RUN] cd $COMPANION_DEPLOY && npx wrangler pages deploy"
elif $SYNC_ONLY; then
  echo "  (pulado: --sync-only)"
else
  cd "$COMPANION_DEPLOY"
  npx wrangler pages deploy . --project-name=iconocracia-atlas 2>&1 || echo "⚠ Deploy falhou (wrangler config?)"
  cd "$REPO_ROOT"
  echo "✓ Deploy concluído"
fi

echo "═══ COMPANION DEPLOY CONCLUÍDO ═══"
