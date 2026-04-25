# Hugging Face Release Flow

This repository treats Hugging Face as a **public release surface**:

- Dataset: frozen release snapshots
- Space: read-only corpus explorer

The local repo remains the working surface. Publish only after the local
release gate is clean.

## Dataset repo

- Default owner: `warholana`
- Default dataset repo: `warholana/iconocracy-corpus`

## Build a local release snapshot

Generate a snapshot directory with release metadata and an updated dataset card:

```bash
python tools/scripts/build_hf_release.py \
  --note "Aligned public dataset with local thesis snapshot." \
  --note "Counts reflect current corpus, coding, and records ledgers."
```

By default this writes to `output/huggingface/<release-tag>/`.

Snapshot contents:

- `corpus-data.json`
- `records.jsonl`
- `purification.jsonl`
- `release.json`
- `CHANGELOG.md`
- `README.md`

## Publish the dataset

Prerequisite: authenticate the local CLI first.

```bash
hf auth login
```

Then build and publish:

```bash
python tools/scripts/build_hf_release.py \
  --publish \
  --note "Release note 1" \
  --note "Release note 2"
```

The publish step uses:

- `hf upload <dataset-repo> <snapshot-dir> . --repo-type dataset`

> Note: `huggingface-cli` is deprecated. Use `hf` (installed via `pip install huggingface-hub>=0.20`).

## Space scaffold

The first Space lives in:

- `deploy/huggingface/corpus-explorer-space/`

It is intentionally:

- static
- read-only
- dataset-backed
- free of LLM or writeback behavior

Recommended repo target:

- `warholana/iconocracy-corpus-explorer`

Create or update it with:

```bash
hf repos create warholana/iconocracy-corpus-explorer \
  --repo-type space \
  --space-sdk static \
  --exist-ok

hf upload warholana/iconocracy-corpus-explorer \
  deploy/huggingface/corpus-explorer-space \
  . \
  --repo-type space
```

## Space behavior contract

The Space may:

- browse the frozen dataset
- filter by country, regime, and support
- inspect item metadata
- copy ABNT and Chicago citations
- display a few thesis metrics

The Space must not:

- edit the dataset
- write back to the repository
- perform cataloguing or coding
- depend on Gemini or LLM inference to function
