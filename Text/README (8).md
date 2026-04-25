---
license: cc-by-4.0
language:
- pt
- en
- fr
- de
pretty_name: ICONOCRACY Corpus
size_categories:
- n<1K
tags:
- iconography
- legal-iconography
- legal-history
- female-allegory
- digital-humanities
- cultural-heritage
- political-iconography
- feminist-iconography
- abnt
- metadata
---

# ICONOCRACY Corpus

Release snapshot for `warholana/iconocracy-corpus` built from the local `iconocracy-corpus` repository.

## Current release

- Release tag: `2026-04-23`
- Generated at: `2026-04-23T13:58:44Z`
- Corpus items: **165**
- Canonical records: **165**
- Coded items: **154**
- Countries represented: **17**
- Mean endurecimento score: **1.416**
- Master-record schema versions: `1.0`

## Contract

This dataset is a **release artifact**, not a live working mirror.

Source-of-truth hierarchy:

1. `data/processed/records.jsonl`
2. `corpus/corpus-data.json`
3. `data/processed/purification.jsonl`

`vault/candidatos/` remains an auxiliary mirror only.

## Release notes

- Aligned public dataset with local thesis snapshot: 165 corpus records.
- Regenerated purification.jsonl from canonical records purificacao blocks: 154/165 coded; 11 remain uncoded.
- Removed stale image and legacy analysis artifacts from the Hugging Face dataset surface.
- Snapshot counts: corpus=165, records=165, coded=154.

## Validation notes

- `No corpus/records drift detected.`
- Raw binaries remain outside the repository and live in Google Drive.
- Notion is out of scope for the active workflow.

## Files

- `corpus-data.json`
- `records.jsonl`
- `purification.jsonl`
- `release.json`
- `CHANGELOG.md`

## License

Metadata: CC BY 4.0. Original images remain subject to their source institution rights.
