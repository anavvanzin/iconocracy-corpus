# T3 — Gemma-4 IconoCode Workflow

Automated IconoCode coding for the 19 uncoded corpus items (queue:
`docs/T3-coding-queue.md`) using **`unsloth/gemma-4-E4B-it-GGUF` (Q4_K_M,
~4.6 GB) + `mmproj-F16`** via `llama-cpp-python` with Metal.
**Every output goes to a STAGING file and requires per-item human review
before it touches `corpus-data.json`.**

> **Why GGUF and not transformers fp16?** Gemma-4 E4B fp16 safetensors ≈ 15
> GB, which OOMs on a 16 GB unified-memory Mac (e.g. M4). Q4_K_M GGUF ≈ 4.6
> GB fits comfortably with headroom for activations, image buffers, and the
> OS. Quality delta vs. fp16 is measured at roughly 1–2 pp on Gemma-4 vision
> benchmarks — acceptable for a staging signal that a human vets anyway.

> ## ⚠️ Escala dos indicadores: 0–4 ou 0–3?
>
> O repo contém um conflito documental que precisa ser resolvido pela
> pesquisadora antes de qualquer coding em produção:
>
> - `tools/schemas/master-record.schema.json` — restringe cada indicador a
>   `integer, minimum: 0, maximum: 4`. É o schema que a CI valida contra
>   `data/processed/records.jsonl`.
> - `tools/schemas/purification-record.schema.json` — descreve a escala
>   como `0-3 ordinal scale`.
> - `CLAUDE.md` (repo) — descreve a escala como `(0–3)` em três lugares.
>
> Este script (`iconocode_gemma4.py`) segue o **master-record schema (0–4)**
> porque é o que a CI enforça operacionalmente. Se o codebook da tese é
> 0–3, é necessário ou (a) atualizar `master-record.schema.json` para 0–3 e
> ajustar `INDICATOR_SCALE_MAX` aqui, ou (b) manter 0–4 e atualizar
> `CLAUDE.md` + `purification-record.schema.json`. **Não faça coding em
> produção até que o conflito esteja resolvido** — qualquer staging gerado
> agora com escala errada precisará ser rejeitado no review humano.

## What this is

`tools/scripts/iconocode_gemma4.py` loads Gemma-4, fetches the item image,
builds a Panofsky + 10-indicator prompt in Portuguese, and asks for strict
JSON back. Output is appended to
`data/staging/iconocode-gemma4-runs.jsonl` — one line per item per run.

## Install the extra dependencies

```bash
# Install llama-cpp-python with Metal (one-time, compiles locally)
CMAKE_ARGS="-DLLAMA_METAL=on" \
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/pip install \
    -r requirements-iconocode-gemma4.txt
```

The repo's main `requirements.txt` is left unchanged.

## Download the model

```bash
# ~5.6 GB total: Q4_K_M (4.64 GB) + mmproj-F16 (945 MB)
hf download unsloth/gemma-4-E4B-it-GGUF \
    gemma-4-E4B-it-Q4_K_M.gguf mmproj-F16.gguf
```

Override the default filenames (e.g., to try Q5_K_M for higher quality) via
env vars read by the script:

```bash
export ICONOCODE_GGUF_MODEL=gemma-4-E4B-it-Q5_K_M.gguf
export ICONOCODE_GGUF_MMPROJ=mmproj-F16.gguf
```

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

- **RAM pressure on M4 16 GB**: Q4_K_M is ~4.6 GB resident; mmproj-F16 adds
  ~950 MB; Python + image processing + KV-cache adds ~2 GB. Expect ~7–8 GB
  total. If Activity Monitor shows memory pressure, close browsers before
  running, or switch to a smaller quant (Q4_0 is fractionally smaller; E2B
  is ~2 GB if you accept lower iconographic fidelity).
- **`llama-cpp-python` not importable**: rebuild with Metal:
  `CMAKE_ARGS="-DLLAMA_METAL=on" pip install --force-reinstall llama-cpp-python`.
- **GGUF not found**: the script looks under the HF hub cache.
  Run `hf download unsloth/gemma-4-E4B-it-GGUF gemma-4-E4B-it-Q4_K_M.gguf
  mmproj-F16.gguf` first (~5.6 GB).
- **Image fetch fails**: Numista / Wikipedia pages return HTML, not images.
  The script sniffs `Content-Type` and refuses HTML — the item is recorded
  with `confidence: low` and `image_hash: null`. Fix by adding a direct image
  URL to `thumbnail_url` in `corpus-data.json` (or drop an image in
  `.cache/iconocode-images/<item_id>.jpg` by hand and re-run).
- **Parse failure**: the repair prompt re-asks for JSON. If both attempts
  fail, the raw text is kept in `raw_model_output` for debugging.
- **Gemma4 chat handler not available**: the script uses `Gemma3ChatHandler`
  from `llama_cpp.llama_chat_format` because Gemma-4 reuses the Gemma-3 chat
  template family. If/when a `Gemma4ChatHandler` ships upstream, update
  `iconocode_gemma4.py`'s `load()` method to import it.

## Critic's gate

**Never merge staging output directly into `corpus-data.json` without
per-item human review.** The staging file is a _suggestion_ from an 8B
multimodal model; the thesis banca will scrutinize every coding. Treat
Gemma-4 as a research assistant, not as a coder of record.
