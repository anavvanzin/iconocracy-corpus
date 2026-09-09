# Architecture Hardening Plan — Canonical Data and Projections

**Date:** 2026-08-12
**Status:** implemented
**Base:** `main` at `7e95a8e`
**Branch:** `codex/architecture-hardening`

## Objective

Make scientific state explicit and make every database or public artifact a
rebuildable projection. Preserve the accepted JSONL-first architecture while
removing silent authority from imports and derived outputs.

## Invariants

1. `pending` is not encoded as ten observed zero values.
2. Evidence identity is local to a corpus item unless explicitly global.
3. Multiple coding observations for one item remain representable.
4. SQLite, dashboards, and release bundles are disposable projections.
5. Release validation checks semantic projection and evidence traceability,
   not only record counts.
6. Existing public file formats remain readable during this hardening phase.

## Step 1 — Prevent placeholder coding during vault import

Refactor `vault_sync.py` so a vault note with a qualitative regime but no ten
observed indicators does not acquire a `purificacao` block. Preserve the regime
as a tentative interpretation and add regression tests for pending and genuinely
coded zero states.

**Acceptance:** new vault imports contain no synthetic indicator vector;
genuine zero-valued coding remains valid; focused tests pass.

**Out of scope:** retrospective deletion or adjudication of the 86 existing
`vault-import` zero vectors.

## Step 2 — Rebuild SQLite from canonical ledgers

Refactor `records_to_sqlite.py` to read `records.jsonl` and
`purification.jsonl` directly. Use `(item_id, evidence_id)` for evidence and a
stable coding-observation identity that permits multiple coders and rounds.
Remove dependence on `corpus-data.json` for canonical research fields.

**Acceptance:** all 339 current evidence relations survive projection; all
coding rows survive projection; foreign-key checks pass; rebuild is deterministic.

**Out of scope:** making SQLite a writable or canonical database.

## Step 3 — Strengthen projection and release gates

Remove the silent Brazil fallback from `records_to_corpus.py`. Make the Hugging
Face builder run schema validation, export idempotence, and evidence traceability
through one fail-closed contract before generating a snapshot.

**Acceptance:** missing country remains unknown rather than fabricated; direct
release builds reject semantic export drift; focused release tests pass.

**Out of scope:** removing all legacy merge fallbacks before an explicit public
overlay ledger exists.

## Step 4 — Document authority boundaries and verify end to end

Record the canonical-field ownership model and projection contract in an ADR,
update operating documentation, run focused and full tests, run schema checks,
and execute the repository drift detector before delivery.

**Acceptance:** documentation names one authority per field family; validators
and tests pass in the `iconocracy` environment; changed files are reviewable as
one coherent diff.

**Out of scope:** corpus-wide recoding, manuscript revision, dashboard redesign,
deployment, merge, or publication.

## Rollback

Each implementation step is isolated by tests and can be reverted independently.
No canonical corpus row is modified by this plan. Generated SQLite files and
release snapshots remain untracked, disposable artifacts.
