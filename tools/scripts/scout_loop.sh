#!/usr/bin/env bash
# scout_loop.sh — Loop autônomo de campanha SCOUT via claude -p
#
# Executa N iterações de pesquisa iconográfica em arquivos digitais,
# usando Claude Code para descobrir, catalogar e validar novos itens.
# Cada iteração é um ciclo: gap analysis → hunt → vault note → validate.
#
# Usa SHARED_TASK_NOTES.md para persistir contexto entre iterações.
#
# Uso:
#   ./tools/scripts/scout_loop.sh                                    # 3 iterações, todos os países
#   ./tools/scripts/scout_loop.sh --max-runs 5 --country FR          # 5 iterações, só França
#   ./tools/scripts/scout_loop.sh --max-runs 10 --regime fundacional # focar regime
#   ./tools/scripts/scout_loop.sh --dry-run                          # preview sem executar
#
# Padrão: Sequential Pipeline + De-Sloppify (autonomous-loops skill)
# Cada iteração:
#   1. Ler lacunas e notas compartilhadas
#   2. Pesquisar em arquivos digitais (hunt)
#   3. Criar nota vault para cada descoberta
#   4. Validar schemas e sync
#   5. Atualizar notas compartilhadas com progresso

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONDA_ENV="iconocracy"
TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
LOG_DIR="${REPO_ROOT}/logs"
NOTES_FILE="${REPO_ROOT}/SHARED_TASK_NOTES.md"

# Defaults
MAX_RUNS=3
COUNTRY=""
REGIME=""
SUPPORT=""
DRY_RUN=false
COMPLETION_COUNT=0
COMPLETION_THRESHOLD=2

# ─── Parse args ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-runs)  MAX_RUNS="$2"; shift 2 ;;
    --country)   COUNTRY="$2"; shift 2 ;;
    --regime)    REGIME="$2"; shift 2 ;;
    --support)   SUPPORT="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=true; shift ;;
    -h|--help)
      head -25 "$0" | grep '^#' | sed 's/^# \?//'
      exit 0 ;;
    *) echo "Argumento desconhecido: $1"; exit 1 ;;
  esac
done

mkdir -p "$LOG_DIR"

# ─── Helpers ────────────────────────────────────────────────────────────
_py() {
  conda run -n "$CONDA_ENV" python "$@" 2>&1
}

_claude() {
  if $DRY_RUN; then
    echo "[DRY-RUN] claude -p: $1" | head -c 200
    echo ""
    return 0
  fi
  claude -p "$1" 2>&1
}

# ─── Init shared notes ─────────────────────────────────────────────────
if [[ ! -f "$NOTES_FILE" ]]; then
  cat > "$NOTES_FILE" << 'NOTES'
# SCOUT Campaign — Shared Task Notes

## Filtros ativos
- País: (todos)
- Regime: (todos)
- Suporte: (todos)

## Progresso
(nenhuma iteração completada)

## Itens descobertos
(nenhum ainda)

## Lacunas prioritárias
(executar lacunas.py para preencher)

## Notas
- Priorizar lacunas com 0 itens no regime fundacional
- Evitar duplicatas — verificar corpus-data.json antes de criar nota
NOTES
fi

# Build filter context for prompts
FILTER_CTX=""
[[ -n "$COUNTRY" ]] && FILTER_CTX="${FILTER_CTX} Focar APENAS no país: $COUNTRY."
[[ -n "$REGIME" ]]  && FILTER_CTX="${FILTER_CTX} Focar APENAS no regime: $REGIME."
[[ -n "$SUPPORT" ]] && FILTER_CTX="${FILTER_CTX} Focar APENAS no suporte: $SUPPORT."

# ─── Main loop ──────────────────────────────────────────────────────────
echo "SCOUT LOOP — $(date '+%Y-%m-%d %H:%M')"
echo "Max runs: $MAX_RUNS | País: ${COUNTRY:-todos} | Regime: ${REGIME:-todos}"
echo "Dry-run: $DRY_RUN"
echo ""

cd "$REPO_ROOT"

for ((i=1; i<=MAX_RUNS; i++)); do
  ITER_LOG="${LOG_DIR}/scout_iter${i}_${TIMESTAMP}.log"

  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  ITERAÇÃO $i / $MAX_RUNS                           "
  echo "╚══════════════════════════════════════════════════╝"

  # ── Passo 1: Análise de lacunas + contexto ──────────────────────────
  echo "  [1/5] Analisando lacunas..."
  if [[ -n "$COUNTRY" ]]; then
    LACUNAS=$(_py tools/scripts/lacunas.py --country "$COUNTRY")
  else
    LACUNAS=$(_py tools/scripts/lacunas.py)
  fi
  CORPUS_COUNT=$(_py -c "import json; d=json.load(open('corpus/corpus-data.json')); print(len(d) if isinstance(d,list) else len(d.get('items',d)))")
  SHARED_NOTES=$(cat "$NOTES_FILE")

  # ── Passo 2: Pesquisa via Claude (SCOUT) ────────────────────────────
  echo "  [2/5] Pesquisando em arquivos digitais..."
  SCOUT_RESULT=$(_claude "
Você é o WebScout do projeto ICONOCRACIA. Sua tarefa é descobrir UM novo item para o corpus.

CONTEXTO DO CORPUS:
- Total atual: $CORPUS_COUNT itens em corpus-data.json
- Notas compartilhadas: $SHARED_NOTES

LACUNAS IDENTIFICADAS:
$LACUNAS

FILTROS:$FILTER_CTX

REGRAS:
1. Leia SHARED_TASK_NOTES.md para saber o que já foi tentado/descoberto
2. Escolha a lacuna mais prioritária (células com 0 itens têm prioridade)
3. Use hunt.py OU pesquise manualmente em fontes confiáveis (Gallica, LOC, Europeana, Numista, Colnect)
4. Verifique se o item NÃO é duplicata: leia corpus/corpus-data.json e compare
5. Se encontrar um item válido, crie a nota vault em vault/candidatos/ seguindo o padrão XX-NNN Título.md
6. Se NÃO encontrar nada novo, diga 'SCOUT_CAMPAIGN_COMPLETE' no final

CRITÉRIOS DE INCLUSÃO (todos 5 obrigatórios):
- Figura alegórica feminina
- Função jurídico-política explícita
- Datável 1800–2000
- Um dos 6 países (FR, UK, DE, US, BE, BR)
- Suporte aceito (moeda, selo, monumento, estampa, frontispício, papel-moeda, cartaz, medalha)

Após criar a nota, atualize SHARED_TASK_NOTES.md com:
- O que foi descoberto (id, título, fonte)
- Lacuna preenchida
- Próximas lacunas a priorizar
")

  echo "$SCOUT_RESULT" >> "$ITER_LOG"

  # Check for completion signal
  if echo "$SCOUT_RESULT" | grep -q "SCOUT_CAMPAIGN_COMPLETE"; then
    ((COMPLETION_COUNT++))
    echo "  [!] Sinal de conclusão ($COMPLETION_COUNT/$COMPLETION_THRESHOLD)"
    if [[ $COMPLETION_COUNT -ge $COMPLETION_THRESHOLD ]]; then
      echo "  [DONE] Campanha concluída — $COMPLETION_THRESHOLD sinais consecutivos"
      break
    fi
  else
    COMPLETION_COUNT=0
  fi

  # ── Passo 3: Validação (De-Sloppify) ────────────────────────────────
  echo "  [3/5] Validando notas criadas..."
  _claude "
Revise as mudanças feitas na iteração anterior do SCOUT loop.

1. Verifique se novas notas em vault/candidatos/ seguem o padrão de nomeação XX-NNN Título.md
2. Verifique se o frontmatter YAML está correto (id, title, date, country, support, regime, tags)
3. Verifique que NÃO há duplicatas em corpus-data.json
4. Se encontrar problemas, corrija-os
5. NÃO crie novos itens — apenas valide e corrija os existentes

Diga 'VALIDAÇÃO OK' se tudo está correto ou liste as correções feitas.
" >> "$ITER_LOG" 2>&1

  # ── Passo 4: Sync pipeline ──────────────────────────────────────────
  echo "  [4/5] Sync pipeline..."
  if ! $DRY_RUN; then
    _py tools/scripts/validate_schemas.py >> "$ITER_LOG" 2>&1 || true
    _py tools/scripts/vault_sync.py sync >> "$ITER_LOG" 2>&1 || true
  fi

  # ── Passo 5: Status ─────────────────────────────────────────────────
  echo "  [5/5] Status atualizado"
  _py tools/scripts/code_purification.py --status 2>&1 | tail -5

  echo "  Log: $ITER_LOG"
done

# ─── Cleanup & relatório final ──────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SCOUT LOOP CONCLUÍDO"
echo "  Iterações: $i / $MAX_RUNS"
echo "  Logs: $LOG_DIR/scout_iter*_${TIMESTAMP}.log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Show final shared notes
echo ""
echo "── Notas compartilhadas ──"
cat "$NOTES_FILE"
