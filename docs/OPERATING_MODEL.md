# Operating Model — ICONOCRACY

**Status:** active as of 2026-04-06

This document defines the day-to-day operating model for `iconocracy-corpus`.
It replaces the earlier tendency to treat the repository as both working
surface and backup log.

## Three durable surfaces

### 1. Local research surface

Use the local repository for the thesis itself:

- corpus expansion and evidence capture
- Endurecimento coding
- manuscript drafting
- vault note-taking and mirroring

This is the only place where unfinished research work should happen.

### 2. GitHub surface

GitHub is the **canonical collaboration and release backbone**, not an
automatic backup log.

- `main` is reserved for intentional, human-readable commits
- short-lived topic branches are the default working pattern
- issues stay lightweight and map to four streams only:
  - `corpus-expansion`
  - `purification-coding`
  - `thesis-writing`
  - `infra-publishing`
- labels are limited to:
  - `corpus`
  - `coding`
  - `writing`
  - `infra`
  - `blocked`
  - `release`

### 3. Hugging Face surface

Hugging Face is the public release layer:

- the dataset is a frozen release artifact, not a live working copy
- releases happen at meaningful milestones, not on every repo change
- the first Space is read-only and browses a frozen dataset snapshot

## Canonical data contract

Authority is assigned by field family rather than by a linear ranking:

- `data/processed/records.jsonl` owns item identity, source evidence,
  descriptive metadata, and IconoCode claims.
- `data/processed/purification.jsonl` owns endurecimento observations and their
  coder, round, instrument, and adjudication provenance.
- `data/raw/drive-manifest.json` plus Google Drive own raw-binary identity and
  external storage location.
- `vault/candidatos/` is an auxiliary cataloguing and navigation mirror.

`corpus-data.json`, SQLite, CSV, dashboards, and release bundles are disposable
projections. See `docs/adr/006-canonical-field-ownership-and-projections.md`.

Additional rules:

- Google Drive stores raw binaries and manifests only.
- `data/raw/` must remain metadata-only in git.
- Notion is historical context only and is out of the active workflow.

## Release gate

Before any public dataset or site release:

1. Validate `records.jsonl`.
2. Validate `purification.jsonl`.
3. Check authoritative export-field idempotence.
4. Generate and review the evidence traceability report; high-severity issues
   block release, while historical coverage debt remains visible in the report.
5. Review `code_purification.py --status`.
6. Review `vault_sync.py status` or `diff`.
7. Generate a release snapshot for Hugging Face if the public dataset changes.

`build_hf_release.py` runs steps 1–4 itself and refuses count or semantic export
drift. Steps 5–6 remain explicit scholarly review gates.

## Backup policy

Automatic vault backups must not land on `main`.

Supported alternatives:

- a dedicated backup branch outside the normal thesis history
- non-git timestamped archives via `tools/scripts/vault_backup.py`

The repository default is the second option.
