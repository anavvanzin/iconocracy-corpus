---
name: sync-corpus
description: Run the full corpus sync pipeline in safe sequence. Use when the user says "sync", "sincronizar", "pipeline sync", "atualizar corpus", or after adding new candidates to corpus-data.json.
user-invocable: true
---

Run the ICONOCRACIA corpus sync pipeline in sequence. Stop immediately if any step fails.

## Pipeline

| Step | Script | What it does |
|------|--------|--------------|
| 1 | `validate_schemas.py` | Validates corpus-data.json against JSON schemas |
| 2 | `sync_companion.py` | Rebuilds companion-data.json from corpus |
| 3 | `make_index.py` | Rebuilds index.html and search index |
| 4 | `code_purification.py --status` | Reports ENDURECIMENTO scores across corpus |

## Execution

```bash
set -e
REPO="$CLAUDE_PROJECT_DIR"
PYTHON="conda run -n iconocracy python"

echo "=== Sync Corpus ICONOCRACIA ==="

echo "[1/4] Validando schemas..."
$PYTHON "$REPO/tools/scripts/validate_schemas.py"

echo "[2/4] Sincronizando companion data..."
$PYTHON "$REPO/tools/scripts/sync_companion.py"

echo "[3/4] Reconstruindo índice..."
$PYTHON "$REPO/tools/scripts/make_index.py"

echo "[4/4] Status de purificação..."
$PYTHON "$REPO/tools/scripts/code_purification.py" --status
```

## Report format

After running, present a table:

| Passo | Status | Detalhes |
|-------|--------|----------|
| validate_schemas | ✅/❌ | N itens válidos / erro |
| sync_companion | ✅/❌ | companion-data.json atualizado |
| make_index | ✅/❌ | index.html reconstruído |
| code_purification | ✅/❌ | Score médio de ENDURECIMENTO: X.X |

If any step fails, show the full error and stop. Do not run subsequent steps.

## When to run

- After adding new items to `corpus/corpus-data.json`
- Before committing changes to the corpus
- After running Scout campaigns that modify corpus data
