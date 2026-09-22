#!/usr/bin/env python3
"""
C1: Corpus Validation Cron Script
Computes the SHA-256 hash of records.jsonl, runs the validate_schemas.py script,
updates the state cache, and outputs a JSON summary for the LLM to process.
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Absolute Paths
REPO_ROOT = Path("/Users/ana/Research/hub/iconocracy-corpus")
RECORDS_FILE = REPO_ROOT / "data/processed/records.jsonl"
VALIDATE_SCRIPT = REPO_ROOT / "tools/scripts/validate_schemas.py"
CACHE_PATH = Path("/Users/ana/.hermes/cron-cache/iconocracy-jobs.yaml")
PYTHON_EXEC = "/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python"

def compute_sha256(path: Path) -> str:
    """Compute the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def count_records(path: Path) -> int:
    """Count non-empty lines in a jsonl file."""
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return count

def load_cache() -> dict:
    """Load the state cache using PyYAML."""
    import yaml
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}", file=sys.stderr)
    return {}

def save_cache(cache_data: dict):
    """Save the state cache atomically."""
    import yaml
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CACHE_PATH.with_suffix(".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(cache_data, f, default_flow_style=False)
        temp_path.replace(CACHE_PATH)
    except Exception as e:
        print(f"Error: Failed to save cache atomically: {e}", file=sys.stderr)
        if temp_path.exists():
            temp_path.unlink()

def main():
    try:
        import yaml
    except ImportError:
        print(json.dumps({
            "status": "error",
            "error": "PyYAML library is missing from the environment.",
            "last_run": datetime.now().isoformat()
        }))
        return

    result = {
        "job_id": "corpus-validation",
        "status": "ok",
        "changed": False,
        "item_count": 0,
        "records_hash": "",
        "errors": [],
        "last_run": datetime.now().isoformat()
    }

    if not RECORDS_FILE.exists():
        result["status"] = "error"
        result["errors"].append(f"records.jsonl file not found at: {RECORDS_FILE}")
        print(json.dumps(result))
        return

    try:
        # 1. Compute Hash and Count
        current_hash = compute_sha256(RECORDS_FILE)
        current_count = count_records(RECORDS_FILE)
        result["records_hash"] = current_hash
        result["item_count"] = current_count

        # 2. Check Cache
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        c1_cache = jobs_cache.setdefault("corpus-validation", {})

        previous_hash = c1_cache.get("records_hash")
        if previous_hash != current_hash:
            result["changed"] = True

        # 3. Run Validation Script
        if VALIDATE_SCRIPT.exists():
            # Run using the canonical python environment to preserve dependency lookup
            proc = subprocess.run(
                [PYTHON_EXEC, str(VALIDATE_SCRIPT)],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            if proc.returncode != 0:
                result["status"] = "error"
                # Strip out long tracebacks or format errors nicely
                result["errors"].append(proc.stderr.strip() or proc.stdout.strip() or "validate_schemas.py failed.")
        else:
            result["status"] = "error"
            result["errors"].append(f"Validation script not found at: {VALIDATE_SCRIPT}")

        # 4. Save Cache if successful
        if result["status"] == "ok":
            c1_cache["last_run"] = result["last_run"]
            c1_cache["last_status"] = "ok"
            c1_cache["records_hash"] = current_hash
            c1_cache["item_count"] = current_count
            save_cache(cache)
        else:
            c1_cache["last_run"] = result["last_run"]
            c1_cache["last_status"] = "error"
            save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["errors"].append(f"Exception raised: {str(e)}")
        result["traceback"] = traceback.format_exc()

    print(json.dumps(result))

if __name__ == "__main__":
    main()
