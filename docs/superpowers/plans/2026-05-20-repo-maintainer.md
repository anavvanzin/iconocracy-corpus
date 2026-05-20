# Repo Maintainer (Interactive Auditor) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a "Repo Maintainer" script that identifies structural redundancies and data drift in `iconocracy-corpus` and provides a visual interface for resolution.

**Architecture:** A Python-based backend that scans the filesystem and clusters conflicts into "Action Sets." A JSON-over-HTTP (or static JSON file) bridge connects the scanner to a browser-based Visual Dashboard for user decisions.

**Tech Stack:** Python 3.11+, `pathlib`, `hashlib`, `gitpython` (optional, or shell git), HTML5/JS for the dashboard.

---

### Task 1: Scanner & Identity Resolver

**Files:**
- Create: `tools/maintainer/scanner.py`
- Test: `tests/maintainer/test_scanner.py`

- [ ] **Step 1: Write tests for identity resolution**
```python
import pytest
from tools.maintainer.scanner import calculate_checksum

def test_checksum_identity(tmp_path):
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.txt"
    f1.write_text("content")
    f2.write_text("content")
    assert calculate_checksum(f1) == calculate_checksum(f2)
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/maintainer/test_scanner.py -v`
Expected: `ImportError` or `AttributeError`

- [ ] **Step 3: Implement checksum logic**
```python
import hashlib
from pathlib import Path

def calculate_checksum(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

- [ ] **Step 4: Run tests to verify they pass**
Run: `pytest tests/maintainer/test_scanner.py -v`
Expected: PASS

- [ ] **Step 5: Implement Fuzzy Path Scanner**
Add to `tools/maintainer/scanner.py`:
```python
def find_potential_duplicates(root_dir: Path):
    all_files = {}
    for path in root_dir.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            checksum = calculate_checksum(path)
            if checksum not in all_files:
                all_files[checksum] = []
            all_files[checksum].append(str(path))
    
    duplicates = {k: v for k, v in all_files.items() if len(v) > 1}
    return duplicates
```

- [ ] **Step 6: Commit**
```bash
git add tools/maintainer/scanner.py tests/maintainer/test_scanner.py
git commit -m "feat(maintainer): add identity-based scanner"
```

---

### Task 2: Action Set Clustering

**Files:**
- Create: `tools/maintainer/clustering.py`
- Test: `tests/maintainer/test_clustering.py`

- [ ] **Step 1: Write test for clustering duplicates**
```python
from tools.maintainer.clustering import cluster_duplicates

def test_basic_clustering():
    duplicates = {
        "hash1": ["Text/report.md", "docs/report.md"],
        "hash2": ["Code/script.py", "tools/scripts/script.py"]
    }
    clusters = cluster_duplicates(duplicates)
    assert len(clusters) == 2
    assert clusters[0]["concern"] == "Conflict: Multiple paths for same content"
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/maintainer/test_clustering.py -v`

- [ ] **Step 3: Implement basic clustering**
```python
def cluster_duplicates(duplicates: dict):
    clusters = []
    for checksum, paths in duplicates.items():
        clusters.append({
            "id": f"set_{checksum[:8]}",
            "concern": "Conflict: Multiple paths for same content",
            "files": paths,
            "type": "structural_redundancy"
        })
    return clusters
```

- [ ] **Step 4: Run test to verify it passes**
Run: `pytest tests/maintainer/test_clustering.py -v`

- [ ] **Step 5: Commit**
```bash
git add tools/maintainer/clustering.py tests/maintainer/test_clustering.py
git commit -m "feat(maintainer): add action set clustering"
```

---

### Task 3: Visual Data Bridge

**Files:**
- Create: `tools/maintainer/ui_adapter.py`
- Create: `tools/maintainer/dashboard.html`

- [ ] **Step 1: Implement JSON exporter**
In `tools/maintainer/ui_adapter.py`:
```python
import json
from pathlib import Path

def export_action_sets(clusters, output_path: Path):
    with open(output_path, "w") as f:
        json.dump({"action_sets": clusters}, f, indent=2)
```

- [ ] **Step 2: Create basic Dashboard HTML**
Create `tools/maintainer/dashboard.html` with a simple JS table to display the `action_sets`.

- [ ] **Step 3: Commit**
```bash
git add tools/maintainer/ui_adapter.py tools/maintainer/dashboard.html
git commit -m "feat(maintainer): add visual dashboard and data bridge"
```

---

### Task 4: Executor (Safe Delete & Git)

**Files:**
- Create: `tools/maintainer/executor.py`
- Test: `tests/maintainer/test_executor.py`

- [ ] **Step 1: Write test for safe deletion**
```python
import os
from tools.maintainer.executor import resolve_set

def test_resolve_keep_one(tmp_path):
    f1 = tmp_path / "keep.txt"
    f2 = tmp_path / "delete.txt"
    f1.write_text("data")
    f2.write_text("data")
    
    resolve_set(strategy="keep_first", paths=[str(f1), str(f2)])
    assert f1.exists()
    assert not f2.exists()
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Implement execution logic**
```python
import os
import subprocess

def resolve_set(strategy, paths):
    if strategy == "keep_first":
        to_delete = paths[1:]
        for p in to_delete:
            os.remove(p)
            # Optional: git rm
            subprocess.run(["git", "rm", p], capture_output=True)
```

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**
```bash
git add tools/maintainer/executor.py tests/maintainer/test_executor.py
git commit -m "feat(maintainer): add execution engine with git support"
```

---

### Task 5: Main CLI Entry Point

**Files:**
- Create: `tools/maintainer/main.py`

- [ ] **Step 1: Implement main loop**
```python
import argparse
from pathlib import Path
from tools.maintainer.scanner import find_potential_duplicates
from tools.maintainer.clustering import cluster_duplicates
from tools.maintainer.ui_adapter import export_action_sets

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    
    if args.scan:
        dupes = find_potential_duplicates(Path("."))
        clusters = cluster_duplicates(dupes)
        export_action_sets(clusters, Path("tools/maintainer/data.json"))
        print("Scan complete. Open tools/maintainer/dashboard.html to resolve.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit and verify**
```bash
git add tools/maintainer/main.py
git commit -m "feat(maintainer): add main entry point"
```
