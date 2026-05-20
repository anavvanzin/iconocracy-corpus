# Repository Rescue and Notebook Execution Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the deleted repository files, clean up circular nested git submodules, correct path resolutions in `Code/` files, and execute python tests and jupyter notebooks to verify the repository state.

**Architecture:** We will revert the destructive commit `d16b6ef` to bring back all files, remove the `iconocracy-corpus/` directory, update path resolution from `.parent.parent.parent` to `.parent.parent` in python scripts, and run pytest/jupyter executions sequentially to verify.

**Tech Stack:** Python 3, Git, Pytest, Jupyter/nbconvert/papermill.

---

## Tasks

### Task 1: Restore Files and Cleanup Submodule

**Files:**
- Modify: `.git/config`
- Delete: `iconocracy-corpus/` (nested submodule)

- [x] **Step 1: Revert the destructive commit**
  Run: `git revert --no-edit d16b6ef`
  Expected: All deleted files (wiki, schemas, jsonl) are restored to the working directory.

- [x] **Step 2: Untrack the nested submodule**
  Run: `git rm -f iconocracy-corpus`
  Expected: The gitlink/submodule reference is removed from git tracking.

- [x] **Step 3: Delete the nested submodule folder from disk**
  Run: `rm -rf iconocracy-corpus/`
  Expected: The nested folder is completely deleted.

---

### Task 2: Correct Path Resolution in Python Scripts

**Files:**
- Modify: `Code/atlas_mapping.py:20`
- Modify: `Code/build_iconocracy_sft_dataset.py:20`
- Modify: `Code/code_purification.py:26`
- Modify: `Code/compute_irr.py:32`
- Modify: `Code/csv_to_records.py:28`
- Modify: `Code/gallica_discovery.py:15-16`
- Modify: `Code/iconocode_gemma4.py:47`
- Modify: `Code/iconocode_to_corpus.py:21`
- Modify: `Code/ingest_fichas_lpai.py:37`
- Modify: `Code/mcp_integration.py:23`
- Modify: `Code/normalize_supports.py:44`
- Modify: `Code/parallel_compare.py:13`
- Modify: `Code/records_to_corpus.py:26`
- Modify: `Code/sync_companion.py:22`
- Modify: `Code/test_ingest_fichas_lpai.py:14`
- Modify: `Code/validate_schemas.py:22,208`
- Modify: `Code/vault_sync.py:30`
- Modify: `Code/corpus_bridge.py:36-39`

- [x] **Step 1: Update simple REPO/REPO_ROOT definitions**
  Replace `Path(__file__).resolve().parent.parent.parent` with `Path(__file__).resolve().parent.parent` in the following files:
  - `Code/atlas_mapping.py:20`
  - `Code/build_iconocracy_sft_dataset.py:20`
  - `Code/code_purification.py:26`
  - `Code/compute_irr.py:32`
  - `Code/csv_to_records.py:28`
  - `Code/iconocode_gemma4.py:47`
  - `Code/iconocode_to_corpus.py:21`
  - `Code/ingest_fichas_lpai.py:37`
  - `Code/normalize_supports.py:44`
  - `Code/records_to_corpus.py:26`
  - `Code/sync_companion.py:22`
  - `Code/test_ingest_fichas_lpai.py:14`
  - `Code/vault_sync.py:30`

- [x] **Step 2: Update specific server and output paths in gallica_discovery.py**
  In `Code/gallica_discovery.py:15-16`, replace:
  ```python
  self.gallica_server_path = Path(__file__).parent.parent.parent / "indexing" / "gallica-mcp-server"
  self.output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
  ```
  with:
  ```python
  self.gallica_server_path = Path(__file__).parent.parent / "indexing" / "gallica-mcp-server"
  self.output_dir = Path(__file__).parent.parent / "data" / "raw"
  ```

- [x] **Step 3: Update base_path in mcp_integration.py**
  In `Code/mcp_integration.py:23`, replace:
  ```python
  self.base_path = Path(__file__).parent.parent.parent
  ```
  with:
  ```python
  self.base_path = Path(__file__).parent.parent
  ```

- [x] **Step 4: Update CORPUS_PATH in parallel_compare.py**
  In `Code/parallel_compare.py:13`, replace:
  ```python
  CORPUS_PATH = Path(__file__).parent.parent.parent / "corpus" / "corpus-data.json"
  ```
  with:
  ```python
  CORPUS_PATH = Path(__file__).parent.parent / "corpus" / "corpus-data.json"
  ```

- [x] **Step 5: Update schema directories and root in validate_schemas.py**
  In `Code/validate_schemas.py:22`, replace:
  ```python
  SCHEMA_DIR = Path(__file__).parent.parent / "schemas"
  ```
  with:
  ```python
  SCHEMA_DIR = Path(__file__).parent.parent / "tools" / "schemas"
  ```
  In `Code/validate_schemas.py:208`, replace:
  ```python
  repo_root = Path(__file__).resolve().parent.parent.parent
  ```
  with:
  ```python
  repo_root = Path(__file__).resolve().parent.parent
  ```

- [x] **Step 6: Update INGEST_DIR and REPO_ROOT in corpus_bridge.py**
  In `Code/corpus_bridge.py:36-39`, replace:
  ```python
  INGEST_DIR = Path(__file__).resolve().parent.parent
  REPO_ROOT = INGEST_DIR.parent
  CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
  DEFAULT_CSV = INGEST_DIR / "output" / "iconocracy_master.csv"
  ```
  with:
  ```python
  REPO_ROOT = Path(__file__).resolve().parent.parent
  CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
  DEFAULT_CSV = REPO_ROOT / "output" / "iconocracy_master.csv"
  ```

---

### Task 3: Run Python Tests and Verify schemas

**Files:**
- Test: `Code/` (run tests)

- [x] **Step 1: Execute schema validation script**
  Run: `python Code/validate_schemas.py`
  Expected: Successfully loads and validates all JSON schemas.

- [x] **Step 2: Run python unit tests**
  Run: `pytest Code/` or execute individual test scripts (e.g., `python Code/test_file_utils.py`, `python Code/test_storage.py`)
  Expected: Tests execute and pass. Fix any path resolution issues encountered.

---

### Task 4: Execute and Audit Jupyter Notebooks (01-08)

**Files:**
- Audit: `notebooks/`

- [x] **Step 1: Check notebook execution order**
  Create and execute a scratch python script `docs/superpowers/scratch/run_notebooks.py` to run notebooks `01_exploratory.ipynb` through `08_multidimensional_scoring.ipynb` sequentially using `nbconvert` and catch execution errors.
  ```python
  import subprocess
  from pathlib import Path

  notebooks_dir = Path("/home/ana/Documents/projetos/research/iconocracy-corpus/notebooks")
  order = [
      "01_exploratory.ipynb",
      "02_kruskal_wallis.ipynb",
      "03_regression.ipynb",
      "04_correspondence.ipynb",
      "05_temporal.ipynb",
      "06_clustering.ipynb",
      "07_dimensionality.ipynb",
      "08_multidimensional_scoring.ipynb"
  ]

  for nb in order:
      nb_path = notebooks_dir / nb
      if not nb_path.exists():
          print(f"Notebook {nb} does not exist!")
          continue
      print(f"Executing {nb}...")
      res = subprocess.run([
          "jupyter", "nbconvert", "--to", "notebook", "--execute",
          "--inplace", str(nb_path)
      ], capture_output=True, text=True)
      if res.returncode != 0:
          print(f"Error in {nb}: {res.stderr}")
          break
      else:
          print(f"Finished {nb} successfully.")
  ```
  Run: `python docs/superpowers/scratch/run_notebooks.py`
  Expected: Sequentially runs the notebooks and prints results/errors. Fix any execution errors found.
