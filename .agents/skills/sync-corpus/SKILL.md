---
name: sync-corpus
description: >
  Run the full corpus sync pipeline in safe sequence. Use when the user says
  "sync", "sincronizar", "pipeline sync", "atualizar corpus", or after adding
  new candidates to corpus-data.json. Includes optional ingest bridge step.
user-invocable: true
---

Run the ICONOCRACIA corpus sync pipeline in sequence. Stop immediately if any step fails.

## Pipeline

| Step | Script | What it does |
|------|--------|--------------|
| 0 | `corpus_bridge.py` | *(optional)* Bridges ingest CSV to corpus-data.json |
| 1 | `validate_schemas.py` | Validates corpus-data.json against JSON schemas |
| 2 | `sync_companion.py` | Rebuilds companion-data.json from corpus |
| 3 | `make_index.py` | Rebuilds index.html and search index |
| 4 | `code_purification.py --status` | Reports ENDURECIMENTO scores across corpus |

## Execution

```bash
set -e
REPO="$CLAUDE_PROJECT_DIR"
PYTHON="conda run -n iconocracy python"
INGEST="$REPO/iconocracy-ingest"

echo "=== Sync Corpus ICONOCRACIA ==="

# Step 0: Bridge ingest CSV (only if master CSV exists)
MASTER_CSV="$INGEST/output/iconocracy_master.csv"
if [ -f "$MASTER_CSV" ]; then
  echo "[0/4] Bridge: checking ingest CSV for new items..."
  cd "$INGEST" && python3 -m modules.corpus_bridge --csv "$MASTER_CSV"
  # Agent should ask user before running with --write
else
  echo "[0/4] Bridge: skipped (no ingest CSV found)"
fi

echo "[1/4] Validando schemas..."
$PYTHON "$REPO/tools/scripts/validate_schemas.py"

echo "[2/4] Sincronizando companion data..."
$PYTHON "$REPO/tools/scripts/sync_companion.py"

echo "[3/4] Reconstruindo indice..."
$PYTHON "$REPO/tools/scripts/make_index.py"

echo "[4/4] Status de purificacao..."
$PYTHON "$REPO/tools/scripts/code_purification.py" --status
```

**Bridge step behavior:**

- Step 0 runs the bridge in **dry-run mode** first, showing new items
- If new items are found, **ask the user** before running with `--write`
- To write directly: `cd $INGEST && python3 -m modules.corpus_bridge --write`
- To force a country: `--country FR`

## Report format

After running, present a table:

| Passo | Status | Detalhes |
|-------|--------|----------|
| bridge (ingest) | OK/SKIP/FAIL | N novos itens / skipped / erro |
| validate_schemas | OK/FAIL | N itens validos / erro |
| sync_companion | OK/FAIL | companion-data.json atualizado |
| make_index | OK/FAIL | index.html reconstruido |
| code_purification | OK/FAIL | Score medio de ENDURECIMENTO: X.X |

If any step fails, show the full error and stop. Do not run subsequent steps.

## When to run

- After adding new items to `corpus/corpus-data.json`
- After running `ingest.py` on a new batch of scans
- Before committing changes to the corpus
- After running Scout campaigns that modify corpus data
