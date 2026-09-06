# ADR-006: Canonical field ownership and disposable projections

**Status:** Accepted
**Date:** 2026-08-12

## Context

ADR-003 established `records.jsonl` as the canonical corpus ledger. Later
workflows introduced a separate coding ledger, SQLite, dashboards, and release
bundles. A linear source-of-truth ranking no longer explains which file owns
each scientific field, and derived outputs can accidentally preserve facts not
present in either ledger.

Vault imports also used ten zero values to represent pending coding. Zero is an
observed value on the 0–3 scale, so that representation collapses two different
states: not coded and coded as absent.

## Decision

Canonical authority is assigned by field family:

| Field family | Authority |
|---|---|
| Item identity, source evidence, descriptive metadata, IconoCode claims | `data/processed/records.jsonl` |
| Endurecimento observations, coder, round, instrument version, adjudication | `data/processed/purification.jsonl` |
| Raw binary identity and external storage location | `data/raw/drive-manifest.json` + Google Drive |
| Catalogue notes and research navigation | `vault/candidatos/` as auxiliary mirror |

`corpus-data.json`, SQLite, CSV, dashboards, notebooks inputs, and Hugging Face
bundles are disposable projections. They must be rebuildable without treating
their previous output as scientific evidence.

A qualitative regime imported from a vault note remains a tentative claim. It
does not create indicator values. A genuine all-zero coding remains valid only
when it is an explicit observation carrying coder and date provenance.

Evidence identifiers are scoped to their item. Relational projections therefore
use `(item_id, evidence_id)`, not `evidence_id` alone.

Coding observations are one-to-many per item. Projections preserve coder,
timestamp, round, prompt version, and adjudication status rather than overwriting
one row per item.

## Consequences

- Import and sync tools may propose records but cannot manufacture observations.
- SQLite reads both canonical ledgers directly and remains read-only/disposable.
- Release builds validate schemas and export idempotence, generate the evidence
  report, and block high-severity traceability failures. Existing medium-severity
  claim-linkage debt remains reported rather than silently waived.
- Existing `vault-import` zero vectors require a separate, evidence-controlled
  adjudication; this ADR does not delete them automatically.
- Legacy merge fallback in `records_to_corpus.py` remains temporarily for public
  fields not yet modeled canonically. It must not be expanded; later work should
  replace it with an explicit, versioned public-overlay ledger.

## Alternatives rejected

- **SQLite as canonical store:** efficient for querying but weaker for Git review
  and long-term human-readable provenance.
- **One mutable coding row per item:** cannot represent instrument comparison,
  recoding, or an apparatus of variants.
- **Runtime agent writes directly to canonical data:** obscures authorship and
  bypasses reviewable promotion from proposal to accepted observation.
