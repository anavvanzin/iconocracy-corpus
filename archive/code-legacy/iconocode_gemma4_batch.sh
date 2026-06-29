#!/usr/bin/env bash
# iconocode_gemma4_batch.sh — Run the Gemma-4 IconoCode analyzer on all 19
# uncoded corpus items, then print next-step instructions.
#
# NOTE: this is intentionally a thin wrapper. It loads the ICONOCRACIA conda
# env, runs the analyzer, and prints the human-review workflow. It does NOT
# merge anything into corpus-data.json — that step stays manual, by design.

set -u  # -e omitted on purpose: exit code 2 from the script is a SIGNAL, not
        # a fatal error — the caller must see it.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

CONDA_BASE="/opt/homebrew/Caskroom/miniforge/base"
# shellcheck disable=SC1091
if [[ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]]; then
  source "$CONDA_BASE/etc/profile.d/conda.sh"
  conda activate iconocracy
else
  echo "AVISO: conda.sh não encontrado em $CONDA_BASE — tentando python direto." >&2
fi

PY="${PY:-/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12}"

echo "=== iconocode_gemma4 — batch de 19 itens ===" >&2
echo "Python: $PY" >&2
echo "Repo:   $REPO_ROOT" >&2
echo >&2

"$PY" tools/scripts/iconocode_gemma4.py --all-uncoded "$@"
STATUS=$?

echo >&2
echo "=== Próximos passos ===" >&2
cat <<'EOF' >&2
1. Abra data/staging/iconocode-gemma4-runs.jsonl e revise CADA registro.
   - Descarte / reedite linhas com confidence=low ou regime incoerente.
   - Itens marcados parse_failed=true precisam de intervenção humana (ou
     nova geração com imagem melhor).

2. Transfira as codificações aprovadas para as notas do vault em
   vault/candidatos/SCOUT-NNN ...md, na seção "## IconoCode Analysis"
   (formato esperado pelo script iconocode_to_corpus.py).

3. Com as notas do vault atualizadas, rode:
       python tools/scripts/iconocode_to_corpus.py           # dry run
       python tools/scripts/iconocode_to_corpus.py --write   # grava

4. Verifique que 'indicadores' caiu de 19 para 0 itens faltantes:
       python -c "import json;d=json.load(open('corpus/corpus-data.json'));\
       print(sum(1 for i in d if not i.get('indicadores')))"

5. NUNCA mergear staging direto em corpus-data.json sem revisão humana
   item-a-item. O staging é gate, não destino.
EOF

exit "$STATUS"
