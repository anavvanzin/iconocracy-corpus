# Two-Machine Atomic Sync Workflow

## Scope

Canonical repo: `/Users/ana/Research/hub/iconocracy-corpus`

Remote alias already present: `ssd-mirror` mapped to `/Volumes/ICONOCRACIA/git-mirrors/iconocracy-corpus`

Machines:
- **Mac** (`192.168.100.22`) — primary
- **Debian** (`192.168.100.12`) — secondary, currently password-only SSH

## Golden Rule

Never edit `main` directly on either machine. All changes flow through feature branches, then into `sync/mac` or `sync/debian` via explicit merge, then main is updated by designated machine only.

## Branch Contract

```
main
 ├── sync/mac        ← Mac pushes here after local validation
 ├── sync/debian     ← Debian pushes here after local validation
 ├── feat/<slug>     ← short-lived feature work
 └── safety/<date>   ← emergency rollback snapshots
```

Rules:
- Each side merges its own `sync/*` branch into `main` only after:
  - `./scripts/watchdog-corpus-validation.sh` passed on latest `sync/*`
  - no merge conflicts on `data/processed/*.jsonl*`, `corpus/corpus-data.json`, `vault/tese/*`
- Mac is authoritative for corpus data, schema, and scripts
- Debian is authoritative for computation/experiments
- If both sides changed corpus files, do NOT auto-merge. Request manual adjudication.

## Daily Sync Loop (Mac)

1. `git checkout main && git pull ssd-mirror main`
2. `git checkout sync/mac && git merge main --ff-only`
3. Work; commit often to `feat/*` branches
4. Open PR: `feat/* -> sync/mac` (or directly merge if trivial)
5. `git checkout sync/mac && git log --oneline origin/main..HEAD` — confirm diff is intentional
6. `./scripts/watchdog-corpus-validation.sh`
7. If OK, `git checkout main && git merge --ff-only sync/mac`
8. Push: `git push ssd-mirror main` and `git push origin main` when available
9. `git push origin sync/mac`

## Daily Sync Loop (Debian)

1. `git checkout main && git pull ssd-mirror main`
2. `git checkout sync/debian && git merge main --ff-only`
3. Work; commit to `feat/*` branches
4. PR to `sync/debian`
5. `git checkout sync/debian && git log --oneline origin/main..HEAD`
6. Run local validation (same checksum/outputs as Mac checker)
7. If OK, fast-forward merge `sync/debian -> main`
8. `git push ssd-mirror main` only if Mac didn’t push in the same window

## Merge Conflict Protocol

For these paths, conflicts require human adjudication:
- `data/processed/records.jsonl`
- `data/processed/purification.jsonl`
- `corpus/corpus-data.json`
- `vault/tese/*`
- `docs/plans/*`

For everything else:
- prefer upstream `main` changes
- if both sides are needed, collapse to one coherent version before commit

## Rollback

If a bad sync corrupts data:
1. `git checkout safety/$(date +%Y%m%d) || git checkout -b safety/$(date +%Y%m%d)`
2. `git revert <bad-commit>`
3. `git push ssd-mirror safety/<date> main`
4. Re-run `watchdog-corpus-validation.sh`
5. Notify on Telegram: schema discrepancies and rollback rationale

## Reconcile Pending Dirty Tree

First-action checklist for Mac:
```bash
cd /Users/ana/Research/hub/iconocracy-corpus
git checkout main
git pull ssd-mirror main --ff-only
git checkout -b safety/20260531-tree-clean
git status --short | head -50
git stash push -m pre-audit-$(date +%Y%m%d)
git restore .
./scripts/watchdog-corpus-validation.sh
```

If stash contains real work, cherry-pick or replay selectively.

## Debian Open Items

- [ ] Enable SSH key auth (password-only blocks full integration)
- [ ] Confirm conda env parity: `iconocracy` on Python 3.12
- [ ] Install `bash`, `python3`, `conda`, `git`, `make`, `entr` or `fswatch`

## Notes

- `git push` to `main` requires explicit approval. Do not set up any force-push or auto-merge to main.
- `git push --force` and `git reset --hard` are blocked by harness permissions for corpus directories.
