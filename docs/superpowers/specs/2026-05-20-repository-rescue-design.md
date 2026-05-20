# Design Spec: Repository Rescue, Submodule Cleanup, and Script Execution Audit

- **Date**: 2026-05-20
- **Author**: Antigravity (AI Coding Assistant)
- **Status**: Draft (Awaiting User Review)

---

## 1. Goal & Context

During a previous deduplication attempt in the `/home/ana/Documents/projetos/research/iconocracy-corpus` repository, a clean-up script matching files across the parent repository and an accidental circular nested clone/submodule directory (`iconocracy-corpus/`) deleted approximately 1,740 critical files from the parent repository (including `records.jsonl`, all schemas, and the wiki).

Additionally, all automation scripts located in `Code/` suffer from a path resolution bug (using `.parent.parent.parent` instead of `.parent.parent`), resolving paths to the repository's parent directory rather than the repository root.

This spec outlines the design to:
1. Revert the destructive commit (`d16b6ef`) to restore all files.
2. Remove the redundant nested submodule `iconocracy-corpus/`.
3. Correct all python path resolutions in `Code/`.
4. Prioritize running python tests and executing the notebook pipeline sequentially (01-08) to audit and verify notebook execution order and correctness.

---

## 2. Proposed System Design

### Section 1: Git Restore & Submodule Removal
- **Action**: Restore the git index and working tree to its state prior to commit `d16b6ef`.
- **Steps**:
  1. Revert the commit `d16b6ef` with `--no-edit`.
  2. Remove tracking of the circular submodule: `git rm -f iconocracy-corpus`.
  3. Recursively remove the physical submodule directory from disk.
- **Safety**: Preserve the 434MB `.maintainer_backup/` directory as a backup until all scripts and notebooks are verified.

### Section 2: Path Resolution Correction
- **Action**: Fix script path resolution so it correctly points to the root of the repository from the `Code/` folder.
- **Changes**:
  - Replace `Path(__file__).resolve().parent.parent.parent` with `Path(__file__).resolve().parent.parent` in python scripts.
  - In `Code/validate_schemas.py`, change `SCHEMA_DIR` to point to `Path(__file__).parent.parent / "tools" / "schemas"`.
  - In `Code/corpus_bridge.py`, change `REPO_ROOT` and `DEFAULT_CSV` references to correctly resolve.

---

## 3. Verification & Execution Plan

### Step 1: Execute Git Rescue
1. Run `git revert --no-edit d16b6ef`.
2. Run `git rm -f iconocracy-corpus` and `rm -rf iconocracy-corpus/`.
3. Verify directory contents of `data/processed/`, `tools/schemas/`, and `wiki/`.

### Step 2: Apply Path Fixes
1. Modify the 18 python files identified in the script audit.
2. Verify path correction changes using git diff.

### Step 3: Run Python Tests
1. Execute python test suite: `pytest Code/` or execute test files directly.
2. Identify and resolve any path-related test failures.

### Step 4: Execute & Audit Notebooks (01-08)
1. Restore all notebooks in `notebooks/` folder.
2. Audit notebook execution order. Check inputs/outputs of:
   - `01_exploratory.ipynb`
   - `02_kruskal_wallis.ipynb`
   - `03_regression.ipynb`
   - `04_correspondence.ipynb`
   - `05_temporal.ipynb`
   - `06_clustering.ipynb`
   - `07_dimensionality.ipynb`
   - `08_multidimensional_scoring.ipynb`
3. Sequentially run all notebooks using a headless execution script or papermill to confirm correctness and verify execution order.
4. Report any sequencing errors or output discrepancies found in the notebooks.
