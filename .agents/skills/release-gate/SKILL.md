---
name: release-gate
description: >
  Run the full public-release gate in safe sequence before any Hugging Face
  dataset snapshot, public corpus-data.json export, or site release. Use when
  the user says "release", "gate", "liberar", "publicar dataset", "snapshot HF",
  "antes de publicar". Stops at the first failure.
user-invocable: true
---

Run the ICONOCRACIA release gate in the sequence fixed by `docs/OPERATING_MODEL.md` §Release gate. Every step is read-only by default; only the final snapshot writes, and it writes under `output/huggingface/` without uploading unless the user explicitly asks.

## Pipeline

| # | Script | Mode | Purpose |
|---|--------|------|---------|
| 1 | `validate_schemas.py` | check | Validate `records.jsonl` + `corpus-data.json` against JSON schemas |
| 2 | `code_purification.py --status` | report | endurecimento coverage across corpus |
| 3 | `vault_sync.py status` | report | Vault ↔ records divergence |
| 4 | `records_to_corpus.py --diff` | report | Preview changes `records.jsonl` → `corpus-data.json` |
| 5 | `build_hf_release.py --release-tag <date>` | write (local) | Generate HF snapshot under `output/huggingface/<tag>/` |

## Execution

```bash
set -e
REPO="$CLAUDE_PROJECT_DIR"
PY="conda run -n iconocracy python"
TAG="${1:-$(date -u +%Y-%m-%d)}"

echo "=== Release Gate ICONOCRACIA — tag $TAG ==="

echo "[1/5] Validando schemas..."
$PY "$REPO/tools/scripts/validate_schemas.py"

echo "[2/5] Status de purificação (endurecimento)..."
$PY "$REPO/tools/scripts/code_purification.py" --status

echo "[3/5] Status do vault..."
$PY "$REPO/tools/scripts/vault_sync.py" status

echo "[4/5] Diff records → corpus-data.json..."
$PY "$REPO/tools/scripts/records_to_corpus.py" --diff

echo "[5/5] Gerando snapshot HF em output/huggingface/$TAG/ ..."
$PY "$REPO/tools/scripts/build_hf_release.py" --release-tag "$TAG"
```

## Rules

- **Stop at first non-zero exit.** Report which step failed + full stderr. Do not continue.
- Step 5 **never uploads** from this skill. To push: the user must run `build_hf_release.py --release-tag <tag> --push` manually after reviewing the snapshot.
- If step 4 shows unexpected deletions or score regressions, pause and ask the user before continuing to step 5.
- Tag defaults to today's UTC date (`YYYY-MM-DD`); user may pass `/release-gate 2026-04-13-rc1`.

## Report format

After running, present:

| # | Step | Status | Signal |
|---|------|--------|--------|
| 1 | validate_schemas | OK/FAIL | N records / error |
| 2 | purification status | OK/FAIL | coverage %, mean score |
| 3 | vault_sync status | OK/FAIL | N in sync / N drift |
| 4 | records→corpus diff | OK/FAIL | N added / N changed / N removed |
| 5 | hf snapshot | OK/FAIL | `output/huggingface/<tag>/` size |

If any step flags regressions (step 2 coverage drops, step 4 deletions, step 3 drift >0), end the report with a **Gate decision** line: `RELEASE BLOCKED — reason` or `RELEASE READY — review snapshot then run --push manually`.

## When to run

- Before any Hugging Face dataset publish
- Before tagging a public site/corpus release on GitHub
- After a SCOUT campaign that modified `records.jsonl` in bulk
- Weekly, as a drift check even without a release
