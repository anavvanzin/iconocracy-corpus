---
name: sync-corpus
description: >
  Run the full corpus sync pipeline in safe sequence. Use when the user says
  "sync", "sincronizar", "pipeline sync", "atualizar corpus", or after adding
  new candidates to corpus-data.json.
user-invocable: true
---

Run the ICONOCRACIA corpus sync pipeline in sequence. Stop immediately if any step fails.

## Pipeline

| Step | Script | What it does |
|------|--------|--------------|
| 1 | `validate_schemas.py` | Validates records.jsonl against master-record schema |
| 2 | `vault_sync.py status` | Reports vault ↔ records.jsonl drift |
| 3 | `records_to_corpus.py --diff` | Reports records.jsonl ↔ corpus-data.json drift |
| 4 | `sync_companion.py` | Rebuilds companion-data.json from corpus |
| 5 | `refresh_dashboard.py` | Re-embeds data into HTML dashboards |
| 6 | `code_purification.py --status` | Reports ENDURECIMENTO scores across corpus |

## Execution

```bash
set -e
REPO="$CLAUDE_PROJECT_DIR"
PYTHON="conda run -n iconocracy python"

echo "=== Sync Corpus ICONOCRACIA ==="

echo "[1/6] Validando schemas..."
$PYTHON "$REPO/tools/scripts/validate_schemas.py"

echo "[2/6] Vault drift..."
$PYTHON "$REPO/tools/scripts/vault_sync.py" status

echo "[3/6] Records ↔ corpus drift..."
$PYTHON "$REPO/tools/scripts/records_to_corpus.py" --diff

echo "[4/6] Sincronizando companion data..."
$PYTHON "$REPO/tools/scripts/sync_companion.py" > /dev/null

echo "[5/6] Atualizando dashboards..."
$PYTHON "$REPO/tools/scripts/refresh_dashboard.py"

echo "[6/6] Status de purificacao..."
$PYTHON "$REPO/tools/scripts/code_purification.py" --status
```

## Report format

After running, present a table:

| Passo | Status | Detalhes |
|-------|--------|----------|
| validate_schemas | OK/FAIL | N itens válidos / erro |
| vault_sync | OK/DRIFT | N notas, X SCOUT pendentes |
| records_to_corpus | OK/DRIFT | N itens só em records / M só em corpus |
| sync_companion | OK/FAIL | companion-data.json atualizado |
| refresh_dashboard | OK/FAIL | corpus + agents dashboards |
| code_purification | OK/FAIL | Score médio ENDURECIMENTO: X.X |

If any step fails, show the full error and stop. Do not run subsequent steps.
Log the run via `tools/scripts/log_agent_run.py --agent sync --status success/error`.

## When to run

- After adding new items to `corpus/corpus-data.json`
- After running `ingest.py` on a new batch of scans
- Before committing changes to the corpus
- After running Scout campaigns that modify corpus data

## Notes

- Bridge step (`corpus_bridge.py`) removed — module deleted, ingest pipeline
  refactor in progress (2026-04).
- `make_index.py` is the Iconclass index builder (takes `<lang> <cmd>`),
  not a corpus tool — excluded.
