# Reconcile `/data` and `~/Documents` Working Copies Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not execute a later phase until the previous phase output has been reviewed and approved.

**Goal:** Reconcile the two divergent local clones of `anavvanzin/iconocracy-corpus` without losing committed or uncommitted work, then leave one canonical working copy plus a synchronized local backup copy.

**Architecture:** Treat this as a local Git rescue and data-integrity operation, not as a normal pull/merge. First preserve every reachable and uncommitted state, then bring all commit objects into one integration repository, then merge by evidence with record-key-aware corpus checks. After reconciliation, keep `/data` and `~/Documents` aligned by a deliberate backup/sync workflow rather than by allowing two independent active histories.

**Tech Stack:** Git, GitHub remote branches, `git bundle`, shell, repo-local Python/pytest checks.

---

## Current Known State

As of 2026-05-24, before refreshing remotes:

| Copy | Path | Branch | Cached `origin/main` | Local HEAD | Ahead/behind cached origin | Dirty state |
|------|------|--------|----------------------|------------|----------------------------|-------------|
| Documents | `~/Documents/projetos/research/hub/iconocracy-corpus` | `main` | `79ebfc6` | `e7d3cda` | ahead 15, behind 4 | modified files, untracked files, and one nested/submodule-like dirty path |
| data | `/data/projetos/research/hub/iconocracy-corpus` | `main` | `79ebfc6` | `4c4e97d` | ahead 29, behind 4 | mostly untracked files, including `.maintainer_backup/` |

Important constraints:

- The two clones do not currently know each other's local-only commits.
- Do not interpret "no merge-base visible" as "no common history"; it means the relevant objects are not yet present in one object database.
- `~/Documents` contains the highest-risk state because it has uncommitted edits to corpus and code files.
- `/data` contains the larger committed local series and appears to include the scout-DE Germania corpus expansion.
- The user wants local redundancy because this is a first Linux setup and `/data` acts as protection against losing work after a bad reboot or host problem. The fix is not "delete the backup"; the fix is "no unsupervised divergence between backup and working copy."
- No destructive operation is allowed before Phase 10.
- **Third diverging head — PR #59 (web session).** Open draft PR #59 ("Review + ingest the 2026-05-19 research run and Drive bundle"), base `main`, head `claude/review-thesis-research-oEuyV` (Claude Code on the web), is appending **7 KEEP candidates** to `data/processed/records.jsonl` (Phase 1 retuned 2026-05-24 from 19 → 7; verdict in `corpus/candidatos/review-2026-05-19.md` on that branch). Target: `records.jsonl` 274 → **281**, `corpus-data.json` parity 281. This branch is **not** present in either local clone. When this PR merges to `origin/main`, it becomes a *fourth* set of changes the eventual `/data` ↔ `~/Documents` reconcile must integrate — neither local copy will have those 7 records until it pulls. Pull/merge `origin/main` (incl. #59) **before** finalizing the reconcile so the merged corpus count reconciles against `max(local) + #59 additions`, not just `max(274, 265)`. The 7 KEEP ids are listed in the Phase 1 retune block (US: baker-godwin-lincoln-005, inger-liberty-004, kimmel-outbreak-007, traubel-triumph-006; FR: gusman-justice-vengeance-003 [country fixed UK→FR]; BR: alegoria-lei-aurea-villares-004, republica-manoel-lopes-rodrigues-003).

---

## Phase 0: Freeze and Inventory

**Intent:** Capture the exact state of both clones before any network update or cleanup.

**Approval needed before phase:** yes.

**Read-only commands:**

- [ ] In `/data/projetos/research/hub/iconocracy-corpus`, record:

```bash
git status --short
git branch -vv
git rev-parse --short HEAD
git rev-parse --short origin/main
git rev-list --left-right --count HEAD...origin/main
git log --oneline --decorate --max-count=20
```

- [ ] In `~/Documents/projetos/research/hub/iconocracy-corpus`, record:

```bash
git status --short
git branch -vv
git rev-parse --short HEAD
git rev-parse --short origin/main
git rev-list --left-right --count HEAD...origin/main
git log --oneline --decorate --max-count=20
```

- [ ] Classify every dirty path in both clones into exactly one bucket:
  - `real`: must be preserved and reviewed in the merge.
  - `junk`: generated, temporary, or safe to ignore, but still preserved before destructive cleanup.
  - `external`: submodule, nested repository, symlink target, worktree, or path whose state is not represented by the parent Git repo.
  - `unknown`: do not commit or delete until manually inspected.

**Known paths requiring explicit classification in Documents:**

```text
corpus/corpus-data.json
data/processed/purification.jsonl
deploy/tropical-atlas/functions/api/[[route]].ts
deploy/tropical-atlas/public/index.html
environment.yml
requirements.txt
tools/scripts/code_purification.py
tools/scripts/upload_thumbnails.py
vault/2026-Q2-Seminario-AD/algoritmo-em-disputa
.coverage
.session-state.md
.superpowers/
data/processed/stats.txt
docs/superpowers/plans/2026-05-19-housekeeping-pass.md
docs/superpowers/plans/2026-05-24-irr-pilot.md
docs/superpowers/specs/2026-05-24-irr-pilot-synthetic-coder.md
findings.md
task_plan.md
tools/scripts/analyze_purification_drift.py
tools/scripts/auto_code_purification.py
tools/scripts/classify_support_types.py
tools/scripts/classify_support_types_rich.py
```

**Known paths requiring explicit classification in `/data`:**

```text
.maintainer_backup/
docs/superpowers/plans/2026-05-24-reconcile-data-documents.md
modules
test_data.json
test_file_2.txt
tools/maintainer/data.json
vault/Untitled.base
```

**Stop condition:** produce an inventory table with path, clone, status, bucket, and proposed preservation method.

---

## Phase 1: Make Every State Recoverable

**Intent:** Create recovery points before committing, fetching, merging, cleaning, resetting, or deleting anything.

**Approval needed before phase:** yes.

**Safety artifacts:**

- [ ] Create an artifact directory outside both Git worktrees:

```bash
mkdir -p /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24
```

- [ ] Create local safety tags for current committed heads:

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus tag reconcile-start-documents-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus tag reconcile-start-data-2026-05-24
```

- [ ] Create Git bundles containing each clone's current committed history:

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus bundle create /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24.bundle --all
git -C /data/projetos/research/hub/iconocracy-corpus bundle create /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24.bundle --all
```

- [ ] Save uncommitted diffs from both clones:

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus diff > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24.diff
git -C ~/Documents/projetos/research/hub/iconocracy-corpus diff --cached > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24-cached.diff
git -C /data/projetos/research/hub/iconocracy-corpus diff > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24.diff
git -C /data/projetos/research/hub/iconocracy-corpus diff --cached > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24-cached.diff
```

- [ ] Preserve untracked files from both clones as archives, excluding `.git`:

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus ls-files --others --exclude-standard -z > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24-untracked.zlist
git -C /data/projetos/research/hub/iconocracy-corpus ls-files --others --exclude-standard -z > /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24-untracked.zlist
tar -C ~/Documents/projetos/research/hub/iconocracy-corpus --null -T /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24-untracked.zlist -czf /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-documents-2026-05-24-untracked.tar.gz
tar -C /data/projetos/research/hub/iconocracy-corpus --null -T /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24-untracked.zlist -czf /data/projetos/research/hub/iconocracy-corpus-reconcile-2026-05-24/reconcile-data-2026-05-24-untracked.tar.gz
```

**Stop condition:** verify that both bundles exist, both diff files exist, both untracked manifests and archives exist, and every dirty path from Phase 0 appears either in a commit plan or in a preservation artifact.

---

## Phase 2: Commit Real Uncommitted Work

**Intent:** Convert real working tree edits into normal Git objects before pushing backup branches.

**Approval needed before phase:** yes.

**Documents clone:**

- [ ] Commit `real` paths together only if they form one coherent change.
- [ ] Split unrelated edits into separate WIP commits if they represent different concerns:
  - corpus/coding edits.
  - deployment/atlas edits.
  - dependency/environment edits.
  - analysis script additions.
  - docs/plans/specs.
- [ ] Do not commit paths bucketed as `junk`.
- [ ] Do not commit paths bucketed as `external` until their repository/submodule status is understood.
- [ ] Do not commit paths bucketed as `unknown`.

Suggested commit message format:

```text
wip(reconcile): preserve documents corpus and tooling edits
wip(reconcile): preserve documents atlas deployment edits
wip(reconcile): preserve documents analysis scripts
```

**`/data` clone:**

- [ ] Commit this revised plan if the plan itself should become part of the repository history.
- [ ] Do not commit `.maintainer_backup/`, test scratch files, or `vault/Untitled.base` unless Phase 0 classifies them as `real`.
- [ ] Leave junk untracked after confirming it is preserved by Phase 1 artifacts.

**Stop condition:** both clones have clean working trees except deliberately retained `junk`, `external`, or `unknown` paths that are preserved and documented.

---

## Phase 3: Refresh Remote Reality

**Intent:** Update cached remote refs without merging or rebasing either clone.

**Approval needed before phase:** yes, because this touches the network.

**Commands:**

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus fetch origin
git -C /data/projetos/research/hub/iconocracy-corpus fetch origin
```

Then re-measure:

```bash
git rev-list --left-right --count HEAD...origin/main
git log --oneline HEAD..origin/main
git log --oneline origin/main..HEAD
```

Run the re-measure commands in both clones.

**Stop condition:** report the refreshed remote-only, Documents-only, and `/data`-only commit counts and commit summaries.

---

## Phase 4: Publish Recovery Branches

**Intent:** Put all committed local work on GitHub under explicit temporary refs before integration.

**Approval needed before phase:** yes, because this writes to the remote.

**Commands:**

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus push origin HEAD:refs/heads/reconcile/documents-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus push origin HEAD:refs/heads/reconcile/data-2026-05-24
```

Optional but recommended if policy allows remote tags:

```bash
git -C ~/Documents/projetos/research/hub/iconocracy-corpus push origin reconcile-start-documents-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus push origin reconcile-start-data-2026-05-24
```

**Stop condition:** confirm both remote branches exist:

```bash
git ls-remote --heads origin 'refs/heads/reconcile/*'
```

Expected refs:

```text
refs/heads/reconcile/documents-2026-05-24
refs/heads/reconcile/data-2026-05-24
```

---

## Phase 5: Build Integration Branch

**Intent:** Bring both local histories and current `origin/main` into a single repository without touching `main`.

**Approval needed before phase:** yes.

**Preferred integration repo:** `/data/projetos/research/hub/iconocracy-corpus`, unless Phase 0 reveals a better reason to use `~/Documents`.

**Commands:**

```bash
git -C /data/projetos/research/hub/iconocracy-corpus fetch origin
git -C /data/projetos/research/hub/iconocracy-corpus switch -c reconcile/integration-2026-05-24 origin/main
```

Inspect graph:

```bash
git log --graph --oneline --decorate --boundary origin/main origin/reconcile/documents-2026-05-24 origin/reconcile/data-2026-05-24
git merge-base origin/reconcile/documents-2026-05-24 origin/reconcile/data-2026-05-24
git merge-base origin/main origin/reconcile/documents-2026-05-24
git merge-base origin/main origin/reconcile/data-2026-05-24
```

**Stop condition:** report the graph shape and merge bases. Do not merge yet.

---

## Phase 6: Decide Merge Strategy from Diffs

**Intent:** Decide whether the corpus files can be merged mechanically or require manual record-level reconciliation.

**Approval needed before phase:** yes.

**Diff commands:**

```bash
git diff --stat origin/main..origin/reconcile/documents-2026-05-24
git diff --stat origin/main..origin/reconcile/data-2026-05-24
git diff --name-status origin/reconcile/documents-2026-05-24..origin/reconcile/data-2026-05-24
```

**Corpus-specific checks:**

- [ ] Extract changed records from each branch for:
  - `data/processed/records.jsonl`
  - `data/processed/purification.jsonl`
  - `corpus/corpus-data.json`
- [ ] Compare by stable key, not by line number:
  - prefer `item_id` where present.
  - use `item_hash` where `item_id` is absent.
  - for `corpus-data.json`, use the established export schema keys.
- [ ] Classify each changed record:
  - `documents-only`
  - `data-only`
  - `same-key-identical`
  - `same-key-conflict`

**Strategy rules:**

- If files are disjoint: normal sequential merges are acceptable.
- If same files but disjoint record keys: merge files with a key-aware script or one-off checked procedure.
- If same record keys differ: manual reconciliation is required for those records.
- Do not use textual "union merge" for JSON or JSONL corpus files.

**Stop condition:** produce a merge decision table with file, conflict type, affected keys, and proposed resolution owner.

---

## Phase 7: Merge on Integration Branch

**Intent:** Produce one combined branch that contains remote `main`, Documents work, and `/data` work.

**Approval needed before phase:** yes.

**General sequence:**

```bash
git -C /data/projetos/research/hub/iconocracy-corpus switch reconcile/integration-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus merge --no-ff origin/reconcile/data-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus merge --no-ff origin/reconcile/documents-2026-05-24
```

The invariant is: integration starts at fresh `origin/main`, then merges both recovery branches exactly once. If the graph inspection in Phase 5 shows that this command sequence does not satisfy that invariant, stop and revise Phase 7 before running any merge.

**Conflict policy:**

- Resolve code/docs conflicts with normal Git conflict review.
- Resolve corpus data conflicts by key-aware manual review.
- For each same-key corpus conflict, record the chosen resolution in the phase report.
- Do not resolve data conflicts by accepting one side wholesale unless Phase 6 proves that side is authoritative for that key.

**Stop condition:** integration branch has no conflict markers, `git status --short` is clean, and `git log --graph` shows both recovery branches merged.

---

## Phase 8: Validate Integrated Corpus and App Contracts

**Intent:** Prove that the merged repository is structurally valid and that corpus counts are explained.

**Approval needed before phase:** no, if all commands are local and dependencies are already installed.

**Minimum validations:**

```bash
python -m json.tool corpus/corpus-data.json >/dev/null
python - <<'PY'
import json
from collections import Counter
from pathlib import Path

for path in [Path("data/processed/records.jsonl"), Path("data/processed/purification.jsonl")]:
    rows = []
    with path.open() as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: {exc}")
    ids = [r.get("item_id") for r in rows if r.get("item_id")]
    hashes = [r.get("item_hash") for r in rows if r.get("item_hash")]
    duplicate_ids = [k for k, n in Counter(ids).items() if n > 1]
    duplicate_hashes = [k for k, n in Counter(hashes).items() if n > 1]
    print(path, "rows", len(rows), "duplicate_item_id", len(duplicate_ids), "duplicate_item_hash", len(duplicate_hashes))
    if duplicate_ids or duplicate_hashes:
        raise SystemExit(1)
PY
```

Run repo-local checks that exist in this checkout:

```bash
pytest
```

If full `pytest` is too broad or fails for known unrelated reasons, run and report narrower checks relevant to:

- JSON/JSONL loading.
- duplicate `item_id` / `item_hash`.
- purification coding integrity.
- atlas/export contract.
- record-count and uncoded-count reporting.

**Count reconciliation:**

- [ ] Report final total record count.
- [ ] Report final coded count.
- [ ] Report final uncoded count.
- [ ] Explain any final total lower than `274`.
- [ ] Explain any final total higher than `274`.
- [ ] Confirm whether the previous `52` uncoded count remained stable or changed, and why.

**Stop condition:** validation output is recorded and any failures are either fixed or explicitly classified as unrelated pre-existing failures.

---

## Phase 9: Promote Integration to `main`

**Intent:** Move the reconciled history to `main` only after validation.

**Approval needed before phase:** yes. This is the first phase allowed to affect shared `main`.

**Commands after approval:**

```bash
git -C /data/projetos/research/hub/iconocracy-corpus switch main
git -C /data/projetos/research/hub/iconocracy-corpus merge --ff-only reconcile/integration-2026-05-24
git -C /data/projetos/research/hub/iconocracy-corpus push origin main
```

If `--ff-only` fails, stop. Do not force push. Re-inspect the graph and decide whether `main` moved during reconciliation.

**Stop condition:** GitHub `main` points to the validated integration commit.

---

## Phase 10: Re-sync Local Copies and Preserve Local Backup

**Intent:** End with one canonical active Git clone and one synchronized local backup path, so local redundancy remains without future Git-history divergence.

**Approval needed before phase:** yes. This phase can be destructive.

**Canonical-location decision:**

- Default candidate: `/data/projetos/research/hub/iconocracy-corpus`, because it already contains the larger committed local series and this plan lives there.
- Override only if Phase 0-8 evidence shows `~/Documents` is operationally safer.

**Allowed outcomes:**

- [ ] Keep `/data/projetos/research/hub/iconocracy-corpus` as the canonical active Git clone and make `~/Documents/projetos/research/hub/iconocracy-corpus` a read-only or clearly marked backup mirror refreshed from canonical.
- [ ] Keep `~/Documents/projetos/research/hub/iconocracy-corpus` as the canonical active Git clone and make `/data/projetos/research/hub/iconocracy-corpus` a read-only or clearly marked backup mirror refreshed from canonical.
- [ ] Keep one canonical active clone and replace the other path with a symlink only if the user accepts losing a physically separate copy at that path.
- [ ] Keep one canonical active clone and recreate the other path as a Git worktree only if the user accepts that a worktree shares the same repository object store and is not a full independent backup.
- [ ] Keep both as full clones only if there is an explicit sync rule: after each work session, push/pull through `origin/main` or run a one-direction backup refresh from canonical to backup. Do not edit both independently.

**Preferred outcome for this user's stated risk model:**

- [ ] Use one canonical active clone for all edits.
- [ ] Keep the second location as a backup mirror.
- [ ] Refresh the backup only from the canonical reconciled state.
- [ ] Before any backup refresh that overwrites files, create a dated backup artifact or confirm the backup clone has no unique work.

**Forbidden without separate explicit confirmation:**

```bash
git reset --hard
rm -rf
git clean -fdx
```

**Stop condition:** both filesystem paths contain the same reconciled project state, and exactly one is documented as the active editing clone. The other remains available as local redundancy but is documented as backup-only unless it is first synchronized.

---

## Phase 11: Cleanup and Prevention

**Intent:** Remove temporary rescue infrastructure only after it is no longer needed and document the backup discipline that prevents recurrence.

**Approval needed before phase:** yes for remote branch deletion; no for documentation updates.

**Cleanup candidates:**

```text
origin/reconcile/documents-2026-05-24
origin/reconcile/data-2026-05-24
reconcile-start-documents-2026-05-24
reconcile-start-data-2026-05-24
reconcile-documents-2026-05-24.bundle
reconcile-data-2026-05-24.bundle
reconcile-documents-2026-05-24.diff
reconcile-documents-2026-05-24-cached.diff
reconcile-data-2026-05-24.diff
reconcile-data-2026-05-24-cached.diff
reconcile-documents-2026-05-24-untracked.zlist
reconcile-data-2026-05-24-untracked.zlist
reconcile-documents-2026-05-24-untracked.tar.gz
reconcile-data-2026-05-24-untracked.tar.gz
```

Do not delete bundles, diffs, or manifests until:

- [ ] `origin/main` contains the integration commit.
- [ ] the canonical local clone is clean.
- [ ] the non-canonical path has been converted into a synchronized backup mirror, symlinked, worktree-linked, recloned, reset, or otherwise handled by explicit approval.
- [ ] record counts and validation outputs have been saved in the reconciliation report.

Prevention tasks:

- [ ] Document the canonical clone location.
- [ ] Document the backup clone location.
- [ ] Add a "backup-only unless synchronized" note to the backup path, for example a local untracked `README-BACKUP-COPY.txt`.
- [ ] Update memory notes `project-iconocracia` and `reference-ssd-data` with the resolved location.
- [ ] Add a short repo note explaining that parallel full clones may exist for local redundancy, but should not both be used for active work without a push/pull or one-direction sync checkpoint.

**Stop condition:** no active divergent clone remains, the local backup policy is documented, and temporary remote branches are deleted only if their content is reachable from `main`.

---

## Execution Log

- _2026-05-24_: initial plan identified divergence but overstated recoverability and under-specified dirty-path triage.
- _2026-05-24_: revised plan adds full inventory, bundle/diff/untracked preservation, key-aware corpus merge rules, exact remote ref names, validation gates, and explicit destructive-operation boundaries.
- _2026-05-24_: user clarified that `/data` is an intentional local safety backup for first Linux setup. Plan updated to preserve local redundancy while preventing independent active histories.
