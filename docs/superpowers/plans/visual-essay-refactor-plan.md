# ICONOCRACY Hub Consistency Refactor Plan

> For agentic workers: use subagent-driven-development or executing-plans when moving from this document into execution.

Goal: refactor `/Users/ana/Research/hub/iconocracy-corpus` for structural consistency without breaking the canonical data contract, symlink topology, thesis workflow, or release gate.

Architecture: treat the hub as the canonical thesis repo inside the larger `/Users/ana/Research` workspace. The refactor should separate four concerns cleanly: canonical tracked surfaces, derived/generated artifacts, compatibility symlinks, and legacy/archive material. Do the work in waves so documentation, topology, and filesystem changes converge together instead of drifting again.

Tech stack: Git, Python 3.12 in conda `iconocracy`, Markdown docs, JSON/JSONL contracts, symlinked workspace paths under `/Users/ana/Research`.

---

## 0. Ground truth gathered before planning

Working tree state observed from repo root:

- current branch: `main`
- tracked dirty files:
  - `vault/.makemd/fileCache.mdc`
  - `vault/.makemd/superstate.mdc`
- untracked generated/research files:
  - `data/processed/fig_06_regime_timeline.png`
  - `data/processed/fig_07_endurecimento_trend.png`
  - `data/processed/fig_08_country_timeline.png`
  - `data/processed/fig_09_medium_timeline.png`
  - `data/processed/fig_10_indicator_correlation.png`
  - `data/processed/fig_11_dendrogram.png`
  - `data/processed/fig_12_cluster_profiles.png`
  - `data/processed/fig_13_scree.png`
  - `data/processed/fig_14_loadings.png`
  - `data/processed/fig_15_pca_biplot.png`
  - `data/processed/fig_16_subscore_by_regime.png`
  - `data/processed/fig_17_subscore_scatter.png`
  - `data/processed/fig_18_composite_vs_core.png`
  - `data/processed/subscores.csv`
  - `notebooks/05_temporal.ipynb`
  - `notebooks/06_clustering.ipynb`
  - `notebooks/07_dimensionality.ipynb`
  - `notebooks/08_multidimensional_scoring.ipynb`
  - `tools/schemas/ICONOCRACIA — O que os números escondem.pdf`
  - `vault/tese/capitulo-6-sessao-2026-04-17.md`

Top-level observations from the current hub:

- actual symlinks at repo root:
  - `Atlas -> /Users/ana/Research/pipelines/Atlas`
  - `indexing -> /Users/ana/Research/pipelines/indexing`
  - `iurisvision -> /Users/ana/Research/labs/iurisvision`
  - `js-genai -> /Users/ana/Research/archive/js-genai`
- tracked internal directories still physically inside the hub:
  - `iconocracy-ingest/`
  - `vault/`
  - `tese/`
- documentation drift already visible:
  - `docs/superpowers/plans/` does not exist
  - `docs/plans/` does exist
  - `README.md` still describes `website/` and `webiconocracy/`, but neither path currently exists in the hub
- potentially inconsistent top-level folders present in the hub root:
  - `New Folder/`
  - `Notas e Textos/`
  - `random outputs/`
  - `PHD/`
  - `Bibliografia - Uso simbólico/`
  - `misc/`
  - `output/`
  - `archive/`
- large non-core directories at root that should be explicitly classified:
  - `.uv-cache/`
  - `.venv-pdf/`
  - `deploy/`
  - `data/`
  - `vault/`
  - `tese/`

Repository documents already asserting the intended model:

- `AGENTS.md`
- `CLAUDE.md`
- `docs/workspace-map.md`
- `docs/WORKFLOW.md`
- `docs/OPERATING_MODEL.md`
- `README.md`

Canonical contract that must not change during refactor:

1. `data/processed/records.jsonl`
2. `corpus/corpus-data.json`
3. `data/processed/purification.jsonl`
4. `vault/candidatos/` as mirror only

---

## 1. Recommended interpretation of “refactor the whole folder for consistency”

Do not start by moving files ad hoc.

Recommended meaning of the refactor:

1. define the intended taxonomy of the hub root
2. classify every top-level path as canonical, derived, compatibility, experimental, cache, or archive
3. reconcile the docs so `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/workspace-map.md`, and `docs/WORKFLOW.md` all describe the same topology
4. isolate generated outputs and local caches from canonical tracked surfaces
5. only then move, rename, ignore, archive, or re-home paths
6. finish with validation of data contracts, symlink expectations, and release-gate commands

This is a consistency refactor, not a content rewrite of the thesis and not a blind cleanup of every untracked file.

---

## 2. Scope boundaries

### In scope

- top-level root taxonomy of the hub
- naming and placement consistency for docs, plans, notebooks, outputs, and legacy folders
- compatibility symlink policy
- generated artifact policy
- docs reconciliation across root and `docs/`
- `.gitignore` and local-tooling hygiene if needed
- validation workflow after structural changes

### Out of scope for the first pass

- changing corpus semantics or schema fields
- editing `records.jsonl`, `corpus-data.json`, or `purification.jsonl` except for path fixes caused by the refactor
- public release generation
- thesis prose rewriting beyond path/reference updates
- restructuring external sibling repos under `/Users/ana/Research/apps`, `/pipelines`, `/labs`, `/vaults`, or `/shared`

---

## 3. Success criteria

The refactor is complete only when all of the following are true:

1. every root-level path has an explicit category and rationale
2. no ambiguous scratch directories remain at repo root
3. all path references in `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/workspace-map.md`, and `docs/WORKFLOW.md` agree
4. plan documents live in one documented location only
5. generated notebook outputs have a documented home and are either tracked deliberately or ignored deliberately
6. symlinked paths are documented as compatibility surfaces, not mistaken for native tracked directories
7. the validation gate still passes:
   - `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`
   - `python tools/scripts/records_to_corpus.py --diff`
   - `python tools/scripts/code_purification.py --status`
   - `python tools/scripts/vault_sync.py status`
8. `git status --short` becomes legible and policy-aligned

---

## 4. File map likely to change

### Canonical docs likely to modify

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/workspace-map.md`
- `docs/WORKFLOW.md`
- `docs/OPERATING_MODEL.md`
- `docs/scripts.md`
- `.gitignore`

### Plan/docs paths likely to create or normalize

- `docs/plans/` or `docs/superpowers/plans/` (choose one canonical location and migrate references)
- `docs/adr/006-hub-root-taxonomy.md` or equivalent ADR documenting the new organization
- `docs/root-inventory.md` or equivalent inventory table generated during audit
- `docs/generated-artifacts-policy.md` if the policy becomes large enough to deserve its own page

### Paths likely to move, archive, or re-home after audit

- `New Folder/`
- `Notas e Textos/`
- `random outputs/`
- `output/`
- `PHD/`
- `Bibliografia - Uso simbólico/`
- loose PDFs and one-off root files that do not belong in the canonical root

### Paths requiring explicit keep-as-is decisions

- `iconocracy-ingest/`
- `vault/`
- `tese/`
- `Atlas`
- `indexing`
- `iurisvision`
- `js-genai`
- `deploy/`
- `archive/`
- `data/`
- `tools/`

---

## 5. Risks and mitigations

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Breaking canonical data flow | `records.jsonl -> corpus-data.json -> purification/vault` is the hub’s contract | Do not move canonical data surfaces in phase 1 |
| Breaking symlink expectations | `Atlas`, `indexing`, `iurisvision`, `js-genai` are compatibility surfaces into other workspace buckets | Audit each symlink target before any rename; update docs first |
| Mixing generated artifacts with canonical data | current untracked figures and notebooks suggest analysis outputs are drifting into tracked zones | Define one generated-artifact policy before moving anything |
| Cleaning too aggressively | root contains research material that may look like junk but may have real use | Inventory first, classify second, move third |
| Docs continue drifting after cleanup | multiple authoritative docs already diverge | Use one docs-reconciliation task and one acceptance checklist across all docs |
| Local tool caches keep reappearing | `.makemd`, `.uv-cache`, `.venv-pdf`, logs can pollute status | classify as tracked support vs ignored local state explicitly |
| Plan-path inconsistency | current request referenced `docs/superpowers/plans`, but repo currently uses `docs/plans` | choose one canonical plan location and update all references in the same commit |

---

## 6. Execution strategy

Use four sequential phases. Do not collapse them into one giant diff.

### Phase A — Inventory and classification

Objective: build a complete inventory of root-level paths and assign each one a category.

Deliverables:
- root inventory table
- category taxonomy
- keep / move / archive / ignore / document decision for each path

Category vocabulary to use consistently:
- canonical
- derived
- compatibility-symlink
- generated-local
- experimental
- archive
- cache-tooling
- unknown-needs-review

### Phase B — Documentation convergence

Objective: update all authoritative docs to describe the same topology and policy.

Deliverables:
- reconciled root map
- one canonical location for plans
- one canonical explanation of the `/Users/ana/Research` migration
- corrected references to `website/`, `webiconocracy/`, and any retired paths

### Phase C — Filesystem refactor

Objective: move or archive ambiguous material and normalize the root.

Deliverables:
- cleaned root
- explicit homes for scratch, generated, and bibliographic material
- `.gitignore` updates if needed
- no accidental changes to canonical ledgers

### Phase D — Validation and release-safety check

Objective: prove the refactor did not damage operational workflows.

Deliverables:
- validation command log
- symlink verification log
- final `git status --short`
- short migration note for future agents

---

## 7. Bite-sized implementation plan

## Task 1: Freeze the current state before touching structure

Files:
- Create: `docs/root-inventory.md`
- Modify: none yet
- Verify: repo root only

- [ ] Step 1: capture current working tree state
  Command:
  ```bash
  cd /Users/ana/Research/hub/iconocracy-corpus
  git status --short
  git diff --stat
  ```

- [ ] Step 2: capture root path inventory with symlink status
  Command:
  ```bash
  python - <<'PY'
  from pathlib import Path
  root = Path('/Users/ana/Research/hub/iconocracy-corpus')
  for p in sorted(root.iterdir(), key=lambda x: x.name.lower()):
      print(f"{p.name}\t{'symlink' if p.is_symlink() else 'dir' if p.is_dir() else 'file'}")
  PY
  ```

- [ ] Step 3: write `docs/root-inventory.md` with columns
  Required columns:
  - `path`
  - `kind`
  - `category`
  - `owner-surface`
  - `status`
  - `action`
  - `notes`

- [ ] Step 4: mark every root path with one of the allowed categories

- [ ] Step 5: commit only the inventory snapshot
  Commands:
  ```bash
  git checkout -b infra/hub-consistency-refactor
  git add docs/root-inventory.md
  git commit -m "docs: inventory hub root for consistency refactor"
  ```

## Task 2: Decide the canonical plan/docs topology

Files:
- Modify: `README.md`
- Modify: `docs/WORKFLOW.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Create or modify: `docs/adr/006-hub-root-taxonomy.md`
- Migrate if chosen: `docs/plans/*` or `docs/superpowers/plans/*`

- [ ] Step 1: choose one canonical plan directory
  Default recommendation: `docs/plans/`
  Reason: it already exists, while `docs/superpowers/plans/` does not.

- [ ] Step 2: update all references to the chosen plan directory in root docs

- [ ] Step 3: add an ADR that defines:
  - what belongs at repo root
  - what belongs under `docs/`
  - what belongs under `archive/`
  - what is a compatibility symlink
  - what is generated-local only

- [ ] Step 4: remove stale claims from `README.md`
  Specifically verify and correct:
  - references to `website/`
  - references to `webiconocracy/`
  - any root layout examples that no longer match reality

- [ ] Step 5: commit the docs convergence separately
  Commands:
  ```bash
  git add README.md AGENTS.md CLAUDE.md docs/WORKFLOW.md docs/workspace-map.md docs/OPERATING_MODEL.md docs/adr/006-hub-root-taxonomy.md
  git commit -m "docs: reconcile hub topology and consistency rules"
  ```

## Task 3: Normalize generated artifacts and local caches

Files:
- Modify: `.gitignore`
- Modify: `docs/WORKFLOW.md`
- Modify: `docs/scripts.md`
- Possibly create: `docs/generated-artifacts-policy.md`

- [ ] Step 1: classify each currently untracked notebook and figure
  Decision per item:
  - keep tracked in canonical location
  - move to a generated outputs location
  - ignore locally
  - archive elsewhere

- [ ] Step 2: define one output home for exploratory notebook artifacts
  Default recommendation:
  - notebooks remain in `notebooks/`
  - exported figures move to `output/figures/` or `data/processed/derived/` only if they are truly part of a reproducible analytic surface

- [ ] Step 3: define a policy for local caches and editor state
  Candidates to classify explicitly:
  - `vault/.makemd/*`
  - `.uv-cache/`
  - `.venv-pdf/`
  - `firebase-debug.log`
  - `logs/`
  - `tmp/`

- [ ] Step 4: update `.gitignore` to match the chosen policy

- [ ] Step 5: commit cache/output normalization without mixing path moves from other phases
  Commands:
  ```bash
  git add .gitignore docs/WORKFLOW.md docs/scripts.md docs/generated-artifacts-policy.md
  git commit -m "infra: define generated artifact and local cache policy"
  ```

## Task 4: Clean the hub root taxonomy

Files:
- Move or archive only the paths approved in `docs/root-inventory.md`
- Modify: `README.md` if displayed structure changes
- Modify: `docs/workspace-map.md` if compatibility notes change

- [ ] Step 1: move obviously ambiguous scratch folders out of root into an approved home
  Candidate targets:
  - `archive/legacy-root/`
  - `docs/research-notes/`
  - `output/`
  - `sources/`
  Use the inventory decisions, not improvisation.

- [ ] Step 2: normalize naming conventions for surviving root folders
  Rule set:
  - no generic names like `New Folder`
  - no mixed Portuguese/English scratch labels at root unless they are canonical research surfaces
  - no space-heavy ad hoc folder names at root unless historically justified and documented

- [ ] Step 3: verify symlink surfaces still resolve after cleanup
  Command:
  ```bash
  python - <<'PY'
  from pathlib import Path
  root = Path('/Users/ana/Research/hub/iconocracy-corpus')
  for name in ['Atlas','indexing','iurisvision','js-genai']:
      p = root / name
      print(name, p.exists(), p.is_symlink(), p.resolve() if p.exists() else None)
  PY
  ```

- [ ] Step 4: commit only root-taxonomy moves and related doc updates
  Commands:
  ```bash
  git add -A
  git commit -m "refactor: normalize hub root taxonomy"
  ```

## Task 5: Reconcile thesis/vault split and compatibility language

Files:
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `docs/workspace-map.md`
- Modify: `docs/WORKFLOW.md`

- [ ] Step 1: make the `vault/` and `tese/` relationship explicit everywhere
  Required wording:
  - `vault/` is the working mirror and Obsidian surface
  - canonical data truth still begins at `data/processed/records.jsonl`
  - `vault/` is never the primary source of truth for corpus data

- [ ] Step 2: make the `iconocracy-ingest/` exception explicit everywhere
  Required wording:
  - it remains physically inside the hub for git-safe reasons
  - the canonical workspace entrypoint is the `Research/pipelines/...` path

- [ ] Step 3: remove any remaining contradiction between `README.md` and `docs/workspace-map.md`

- [ ] Step 4: commit compatibility-language cleanup
  Commands:
  ```bash
  git add README.md AGENTS.md CLAUDE.md docs/workspace-map.md docs/WORKFLOW.md
  git commit -m "docs: clarify hub compatibility and source-of-truth language"
  ```

## Task 6: Validate the refactor end-to-end

Files:
- Modify: `docs/WORKFLOW.md` if any validation wording is still outdated
- Optionally create: `docs/plans/2026-04-17-hub-consistency-validation-log.md`

- [ ] Step 1: run the structural validation checks
  Commands:
  ```bash
  cd /Users/ana/Research/hub/iconocracy-corpus
  find /Users/ana/Research/hub/iconocracy-corpus -mindepth 2 -maxdepth 4 -name .git
  python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
  python tools/scripts/records_to_corpus.py --diff
  python tools/scripts/code_purification.py --status
  python tools/scripts/vault_sync.py status
  ```

- [ ] Step 2: review final repository shape
  Commands:
  ```bash
  git status --short
  git diff --stat origin/main...HEAD
  ```

- [ ] Step 3: verify no forbidden binary/raw drift was introduced under `data/raw/`

- [ ] Step 4: write a short validation log summarizing:
  - what moved
  - what stayed
  - what was ignored
  - what still needs human review

- [ ] Step 5: only then request code review or merge review

---

## 8. Recommended default decisions

Use these defaults unless a later audit proves they are wrong:

1. canonical plan location should be `docs/plans/`, not `docs/superpowers/plans/`
2. `README.md` should describe the current hub, not historical structures
3. root-level scratch names should be eliminated or re-homed
4. compatibility symlinks should remain at root but be labeled clearly in docs
5. notebook outputs should not accumulate directly in `data/processed/` unless they are part of a documented reproducible export surface
6. local editor cache under `vault/.makemd/` should not remain a recurring tracked-noise source

---

## 9. Open questions for execution

1. Should exploratory figures generated from notebooks become tracked research outputs or ignored local exports?
   Default: keep notebooks tracked, move generated figures to a dedicated derived-output location only if referenced by thesis/docs.

2. Should `docs/plans/` absorb all planning docs, including current `docs/superpowers/specs/` material?
   Default: no; keep `docs/plans/` for implementation/refactor plans and leave `docs/superpowers/specs/` for specs/guides.

3. Should ambiguous bibliographic and note folders be archived inside the repo or moved outside the hub entirely?
   Default: archive inside the repo first, then prune later.

4. Should the refactor happen in one branch or in separate stacked branches?
   Default: one branch with four clean commits aligned to the phases above.

5. Should we execute this as a straight-line local refactor or as a multi-agent audit first?
   Default: start with one focused inventory pass locally, then delegate only if the inventory shows 3+ truly independent cleanup domains.

---

## 10. Handoff recommendation

Best next move: execute Task 1 and Task 2 first, not filesystem moves. The repo already shows documentation drift and root-taxonomy ambiguity; fixing the map before moving material will make the rest of the refactor much safer.
