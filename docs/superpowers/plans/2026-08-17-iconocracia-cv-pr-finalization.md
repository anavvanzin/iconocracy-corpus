# ICONOCRACIA-CV PR Finalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the completed ICONOCRACIA-CV site and academic dossier through an auditable Pull Request, update `main`, and create the independent image-layer branch.

**Architecture:** Preserve the current branch as the complete source of the course-facing delivery, validate that exact tree, and merge it into `main` with a merge commit after mandatory checks pass. Create the image-layer branch only from the resulting `origin/main`, so visual-data work has no stacked-branch dependency.

**Tech Stack:** Git, GitHub CLI, Python 3.12/pytest, Node.js, OpenAI Sites Worker build, Hugging Face Datasets Server APIs.

## Global Constraints

- Current source branch: `codex/consolidate-iconocracia-cv`.
- Pull Request base: `main`.
- Future visual branch: `anavvanzin/feat/build-corpus-image-layer`.
- Do not force-push.
- Do not publish a new Hugging Face snapshot; local and remote data hashes already match.
- Do not add image bytes, provisional image URLs, or a visual manifest to the current PR.
- Preserve the current worktree while the PR is under review.
- Merge only when every mandatory check is green.
- Use a merge commit, not a squash, to preserve commit-level provenance.

---

### Task 1: Version the execution plan and validate the exact PR tree

**Files:**
- Create: `docs/superpowers/plans/2026-08-17-iconocracia-cv-pr-finalization.md`
- Reference: `docs/superpowers/specs/2026-08-17-iconocracia-cv-pr-finalization-design.md`
- Test: `tests/`
- Build: `deploy/iconocracia-cv/`

**Interfaces:**
- Consumes: the approved finalization specification and the clean feature branch.
- Produces: a committed, fully validated branch head suitable for pushing.

- [ ] **Step 1: Commit this plan**

```bash
git add docs/superpowers/plans/2026-08-17-iconocracia-cv-pr-finalization.md
git commit -m "docs(cv): plan auditable PR finalization"
```

Expected: one documentation commit and a clean worktree.

- [ ] **Step 2: Run the complete Python suite on the final tree**

```bash
/Users/ana/.venvs/iconocracy/bin/python3.12 -m pytest tests/
```

Expected: `279 passed`; the eight unregistered `pytest.mark.unit` warnings may remain documented but must not become errors.

- [ ] **Step 3: Build the site Worker**

```bash
cd deploy/iconocracia-cv
npm run build
cd ../..
```

Expected: `Built ICONOCRACIA-CV Sites Worker with 11 routes.`

- [ ] **Step 4: Confirm repository integrity and scope**

```bash
git diff --check origin/main...HEAD
git status --short
git diff --stat origin/main...HEAD
```

Expected: no whitespace errors, no uncommitted files, and a diff limited to the ICONOCRACIA-CV site, dossier, design documents, generator, figure, specification, and this plan.

### Task 2: Push the branch and open the academic Pull Request

**Files:**
- Reference: `docs/superpowers/specs/2026-08-17-iconocracia-cv-pr-finalization-design.md`
- Reference: `docs/superpowers/plans/2026-08-17-iconocracia-cv-pr-finalization.md`

**Interfaces:**
- Consumes: the validated branch head from Task 1.
- Produces: a GitHub Pull Request from `codex/consolidate-iconocracia-cv` to `main`.

- [ ] **Step 1: Push without rewriting history**

```bash
git push -u origin codex/consolidate-iconocracia-cv
```

Expected: the remote branch advances by fast-forward to the validated local head.

- [ ] **Step 2: Create the Pull Request with the complete academic report**

Use this title:

```text
Finalize ICONOCRACIA-CV course surface and academic dossier
```

Use this body:

```markdown
## Summary

- integrates the published ICONOCRACIA-CV course surface into the corpus monorepo history
- versions the bilingual system-design documents, integrated dossier, pipeline figure, and reproducible generator
- records the course layer as a derivation of the integral corpus, not an autonomous corpus

## Validation

- Python suite: 279 passed
- site build: 11 Worker routes
- schemas: 335/335 canonical records valid
- export: 335 records in both canonical and public strata; URL delta zero
- purification: 286/335 coded, with 49 remaining
- Hugging Face: corpus=335, records=335, purification=286
- remote preview, viewer, search, filter, and statistics: valid
- SHA-256: local and public corpus-data.json, records.jsonl, and purification.jsonl match

## Academic traceability

The ICONOCRACIA-CV material is a course-facing visual-computing layer derived from the integral ICONOCRACIA corpus. This PR does not claim that the corpus is complete or directly trainable as an image dataset.

Known limitations remain explicit: 49 uncoded items, vault divergence, 3.3% structured evidence traceability, unknown support labels, no image bytes or Image feature, and 172 placeholder Drive-manifest entries.

## Scope boundary

This PR does not publish another Hugging Face snapshot and does not add corpus image bytes. The visual dataset layer will proceed independently from updated main on `anavvanzin/feat/build-corpus-image-layer`, joined to metadata only through canonical item_id values.

## Public surfaces

- https://iconocracia-cv.pages.dev/
- https://iconocracia-cv.iconocracia-5216.chatgpt.site/
- https://huggingface.co/datasets/warholana/iconocracy-corpus
```

Materialize the reviewed body block above verbatim at
`/tmp/iconocracy-cv-pr-body-2026-08-17.md` using `apply_patch`, then create the
PR with:

```bash
gh pr create \
  --base main \
  --head codex/consolidate-iconocracia-cv \
  --title "Finalize ICONOCRACIA-CV course surface and academic dossier" \
  --body-file /tmp/iconocracy-cv-pr-body-2026-08-17.md
```

Expected: a new open PR URL targeting `main`. The reviewed body must be supplied verbatim from the block above through a temporary file; the temporary file is not committed.

### Task 3: Review the PR and enforce the merge gate

**Files:**
- Review: the GitHub PR diff and check suite.

**Interfaces:**
- Consumes: the open PR from Task 2.
- Produces: a reviewed PR with all mandatory checks green.

- [ ] **Step 1: Confirm PR identity and mergeability**

```bash
gh pr view --json number,url,state,baseRefName,headRefName,mergeable,mergeStateStatus
```

Expected: `state=OPEN`, `baseRefName=main`, `headRefName=codex/consolidate-iconocracia-cv`, and no merge conflict.

- [ ] **Step 2: Inspect the complete changed-file list**

```bash
gh pr diff --name-only
```

Expected: no corpus ledgers, image binaries from the research corpus, thesis originals, secrets, or unrelated configuration files.

- [ ] **Step 3: Wait for checks**

```bash
gh pr checks --watch --interval 10
```

Expected: every required check passes. Any failure stops the merge and is diagnosed on the preserved branch.

### Task 4: Merge the reviewed PR and verify the canonical result

**Files:**
- No source files are edited in this task.

**Interfaces:**
- Consumes: the open, reviewed, green PR from Task 3.
- Produces: a merge commit on `origin/main` containing the complete delivery.

- [ ] **Step 1: Merge without deleting the feature branch**

```bash
gh pr merge --merge --delete-branch=false
```

Expected: PR state becomes `MERGED`; GitHub reports the merge commit SHA.

- [ ] **Step 2: Refresh and verify `origin/main`**

```bash
git fetch origin --prune
git merge-base --is-ancestor HEAD origin/main
gh pr view --json state,mergedAt,mergeCommit,url
```

Expected: the feature head is an ancestor of `origin/main`, and the PR state is `MERGED`.

- [ ] **Step 3: Re-run the focused post-merge gates from the canonical commit**

```bash
git show "origin/main:deploy/iconocracia-cv/site/index.html" >/dev/null
git show "origin/main:docs/superpowers/specs/2026-08-17-iconocracia-cv-pr-finalization-design.md" >/dev/null
git show "origin/main:docs/superpowers/plans/2026-08-17-iconocracia-cv-pr-finalization.md" >/dev/null
```

Expected: all three canonical delivery files exist on `origin/main`.

### Task 5: Create the independent image-layer branch from updated main

**Files:**
- No source files are edited during branch creation.

**Interfaces:**
- Consumes: updated `origin/main` containing the merged ICONOCRACIA-CV delivery.
- Produces: local branch `anavvanzin/feat/build-corpus-image-layer` at the canonical merge result.

- [ ] **Step 1: Confirm the approved branch name is unused**

```bash
git show-ref --verify --quiet refs/heads/anavvanzin/feat/build-corpus-image-layer
git ls-remote --exit-code --heads origin anavvanzin/feat/build-corpus-image-layer
```

Expected: both commands report that the branch does not exist. An existing branch stops creation and requires a naming decision.

- [ ] **Step 2: Create the branch directly from updated `origin/main`**

```bash
git switch -c anavvanzin/feat/build-corpus-image-layer origin/main
```

Expected: the current branch is `anavvanzin/feat/build-corpus-image-layer`, its HEAD equals `origin/main`, and the worktree is clean.

- [ ] **Step 3: Verify the new branch provenance**

```bash
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git status --short
```

Expected: branch name matches exactly, both SHAs are identical, and status is empty.
