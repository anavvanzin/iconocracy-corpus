# ADR 007 — Partial Purification Coverage Policy

**Status:** Accepted  
**Date:** 2026-06-08  
**Related:** Issue #57, ADR 005, `tools/scripts/build_purification_manifest.py`, `data/processed/purification-manifest.json`

## Context

`corpus/corpus-data.json` is the canonical corpus used by `code_purification.py`.
It currently contains more entries than `data/processed/purification.jsonl` covers,
leaving a number of records without endurecimento coding. The exact gap is tracked in
`data/processed/purification-manifest.json`.

These uncoded records are valid corpus items — they passed schema validation — but they
cannot participate in quantitative analysis until coded. Coding requires manual
iconographic judgment per item and is unrealistic to complete all at once on the current
thesis timeline.

## Decision

The uncoded records remain in the public corpus (`corpus/corpus-data.json`) tagged with
`audit_flags: ["uncoded-purification"]`. The authoritative work queue lives at
`data/processed/purification-manifest.json`. Health reporting uses **the total corpus
count as the canonical denominator** and reports the coded/queued split explicitly.

This is the "defer with documented queue" option (Issue #57). The "batch-code all
uncoded now" and "exclude from release-facing views" alternatives were rejected.

## Consequences

- `code_purification.py --status` displays a **Backlog** section citing Issue #57 and
  this ADR, showing the queued count and pointing at the manifest file.
- Analytical chapters (Cap. 6) **MUST** filter for
  `audit_flags ∌ "uncoded-purification"` and disclose the filter in the methodology
  section.
- The HF dataset card and release summaries **MUST** cite both the total catalog count
  and the coded count explicitly, e.g. *"265 catalog / 165 coded"*.
- Notebook headers must verify coverage before claiming full-corpus statistics.
- New corpus entries that lack purification coding receive the flag automatically after
  running `tag_uncoded_purification.py`; the manifest regenerator
  (`build_purification_manifest.py`) is idempotent.

## How to clear an item from the queue

1. Code the record via `python tools/scripts/code_purification.py --item <corpus_id>`.
2. Re-run `python tools/scripts/build_purification_manifest.py` to refresh the manifest.
3. Re-run `python tools/scripts/tag_uncoded_purification.py` to remove the audit flag
   from the newly coded entry and confirm zero drift.

## Alternatives considered

- **Batch-code all uncoded entries now:** blocks thesis timeline; the IRR pilot
  (Cap. 4) and other chapters are more urgent.
- **Exclude uncoded entries from `corpus-data.json`:** misrepresents the catalog state;
  downstream tools that count items would show an understated total and obscure the
  backlog.
