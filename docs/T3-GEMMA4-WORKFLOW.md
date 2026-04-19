# T3 — Gemma-4 IconoCode Workflow

Automated IconoCode coding for the 19 uncoded corpus items (queue:
`docs/T3-coding-queue.md`) using `google/gemma-4-E4B-it` (image-text-to-text,
apache-2.0, ~8B params). **Every output goes to a STAGING file and requires
per-item human review before it touches `corpus-data.json`.**

## What this is

`tools/scripts/iconocode_gemma4.py` loads Gemma-4, fetches the item image,
builds a Panofsky + 10-indicator prompt in Portuguese, and asks for strict
JSON back. Output is appended to
`data/staging/iconocode-gemma4-runs.jsonl` — one line per item per run.

## Install the extra dependencies

```
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/pip install \
    -r requirements-iconocode-gemma4.txt
```

The repo's main `requirements.txt` is left unchanged.

## How to run

Dry-run on a single item (loads the model, codes one, prints JSON, nothing
written):

```
conda activate iconocracy
python tools/scripts/iconocode_gemma4.py \
    --items BE-5F-LEOPOLD-1832 --dry-run
```

Full batch (all 19 uncoded items, writes to staging):

```
bash tools/scripts/iconocode_gemma4_batch.sh
```

Subset only:

```
python tools/scripts/iconocode_gemma4.py --items UK-PENNY-1912,DE-100M-1908
```

## Where output goes

- **`data/staging/iconocode-gemma4-runs.jsonl`** — append-only. Each line is
  one run of one item, tagged with `run_id` (UUID) + `coded_at` (ISO-8601 UTC).
- Re-runs accumulate; they do NOT overwrite. Use
  `tools/scripts/reconcile_iconocode.py` to arbitrate across multiple runs /
  agents.

The JSONL uses English keys (`indicators`, `regime`) to match the existing
`reconcile_iconocode.py` validator. The thesis corpus field is
`indicadores`; renaming happens only when a human approves and copies the
coding into a vault note.

## Human review workflow

1. **Open** `data/staging/iconocode-gemma4-runs.jsonl` in VS Code (one line
   per run).
2. **Inspect** each record. Red flags:
   - `confidence: "low"` — usually parse failure or missing image.
   - `parse_failed: true` — the model didn't produce valid JSON even after
     the repair pass. Look at `raw_model_output`.
   - `regime: null` — the model picked a non-canonical value. Re-read the
     reasoning and decide manually.
   - Indicator scores that don't match the image you remember from SCOUT.
3. **Drop or edit** rows you disagree with. The staging file is a scratchpad,
   not canon.
4. **Port approved codings** into the matching vault note under a
   `## IconoCode Analysis` section (format expected by
   `iconocode_to_corpus.py`). Keep the `endurecimento_score` line and each
   indicator as `<name>: <0-4>`.
5. **Merge** to `corpus-data.json`:
   ```
   python tools/scripts/iconocode_to_corpus.py            # dry run
   python tools/scripts/iconocode_to_corpus.py --write    # commit
   ```
6. **Verify** the uncoded counter drops from 19 to 0:
   ```
   python -c "import json;d=json.load(open('corpus/corpus-data.json'));print(sum(1 for i in d if not i.get('indicadores')))"
   ```

## Re-run behavior

The staging file is append-only. If you run the batch twice, you get two rows
per item — that's intentional for multi-run reliability checks. When you want
a canonical reconciled view, pipe the staging file through
`tools/scripts/reconcile_iconocode.py` (which already handles multi-agent
arbitration on the same schema).

## Troubleshooting

- **RAM pressure on MPS**: Gemma-4 E4B weights are ~16 GB in bfloat16. On a
  32 GB Mac, run with nothing else open. If the OS starts swapping, lower
  `max_new_tokens` in `iconocode_gemma4.py`, or fall back to `--device cpu`
  (very slow — minutes per item).
- **`transformers` version**: requires `>= 4.50` for the `AutoModelForImageTextToText`
  class with gemma-4. The repo env already has `5.5.3`.
- **Image fetch fails**: Numista / Wikipedia pages return HTML, not images.
  The script sniffs `Content-Type` and refuses HTML — the item is recorded
  with `confidence: low` and `image_hash: null`. Fix by adding a direct image
  URL to `thumbnail_url` in `corpus-data.json` (or drop an image in
  `.cache/iconocode-images/<item_id>.jpg` by hand and re-run).
- **Parse failure**: the repair prompt re-asks for JSON. If both attempts
  fail, the raw text is kept in `raw_model_output` for debugging.

## Critic's gate

**Never merge staging output directly into `corpus-data.json` without
per-item human review.** The staging file is a _suggestion_ from an 8B
multimodal model; the thesis banca will scrutinize every coding. Treat
Gemma-4 as a research assistant, not as a coder of record.
