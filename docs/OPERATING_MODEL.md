# Operating Model — ICONOCRACY

**Status:** active as of 2026-04-06

This document defines the day-to-day operating model for `iconocracy-corpus`.
It replaces the earlier tendency to treat the repository as both working
surface and backup log.

## Three durable surfaces

### 1. Local research surface

Use the local repository for the thesis itself:

- corpus expansion and evidence capture
- ENDURECIMENTO coding
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

The source-of-truth hierarchy is:

1. `data/processed/records.jsonl`
   Operational canonical ledger for traceable corpus records.
2. `corpus/corpus-data.json`
   Public-facing export for browsers, dashboards, and public releases.
3. `data/processed/purification.jsonl`
   Canonical ledger for ENDURECIMENTO coding.
4. `vault/candidatos/`
   Auxiliary cataloguing mirror only.

Additional rules:

- Google Drive stores raw binaries and manifests only.
- `data/raw/` must remain metadata-only in git.
- Notion is historical context only and is out of the active workflow.

## Release gate

Before any public dataset or site release:

1. Validate `records.jsonl`.
2. Review `code_purification.py --status`.
3. Review `vault_sync.py status` or `diff`.
4. Review `records_to_corpus.py --diff` if release data depends on `corpus-data.json`.
5. Generate a release snapshot for Hugging Face if the public dataset changes.

## Backup policy

Automatic vault backups must not land on `main`.

Supported alternatives:

- a dedicated backup branch outside the normal thesis history
- non-git timestamped archives via `tools/scripts/vault_backup.py`

The repository default is the second option.
