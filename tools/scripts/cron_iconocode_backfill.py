#!/usr/bin/env python3
"""
C4: Iconocode Backfill Cron Script
Compares candidate notes in vault/candidatos/ against the id_crosswalk.jsonl
to identify any unmapped or unanalyzed items that require backfill.
Updates the state cache, and outputs a JSON summary for the LLM.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Absolute Paths
REPO_ROOT = Path("/Users/ana/Research/hub/iconocracy-corpus")
CANDIDATOS_DIR = REPO_ROOT / "vault/candidatos"
CROSSWALK_FILE = REPO_ROOT / "data/processed/id_crosswalk.jsonl"
CACHE_PATH = Path("/Users/ana/.hermes/cron-cache/iconocracy-jobs.yaml")

def get_candidate_handle(filename: str) -> str:
    """Extract candidate handle from file name (e.g., 'FR-094' or 'SCOUT-436')."""
    # Grab the first token before a space or hyphen-as-separator
    # File name structure: "PREFIX-NUMBER Description" or similar
    name_no_ext = Path(filename).stem
    match = re.match(r"^([A-Z0-9a-z_-]+)", name_no_ext)
    if match:
        return match.group(1).strip()
    return name_no_ext.split()[0].strip()

def load_mapped_handles() -> set:
    """Load all mapped handles from id_crosswalk.jsonl."""
    handles = set()
    if CROSSWALK_FILE.exists():
        with open(CROSSWALK_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        if "handle" in record:
                            handles.add(record["handle"].strip())
                    except json.JSONDecodeError:
                        continue
    return handles

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
        "job_id": "iconocode-backfill",
        "status": "ok",
        "changed": False,
        "total_candidate_files": 0,
        "total_mapped_handles": 0,
        "unmapped_candidates": [],
        "last_run": datetime.now().isoformat(),
        "errors": []
    }

    if not CANDIDATOS_DIR.exists():
        result["status"] = "error"
        result["errors"].append(f"Candidatos folder not found at: {CANDIDATOS_DIR}")
        print(json.dumps(result))
        return

    try:
        # 1. Load mapped handles from crosswalk
        mapped_handles = load_mapped_handles()
        result["total_mapped_handles"] = len(mapped_handles)

        # 2. Scan candidates folder
        unmapped = []
        candidate_files = sorted(CANDIDATOS_DIR.glob("*.md"))
        result["total_candidate_files"] = len(candidate_files)

        for filepath in candidate_files:
            filename = filepath.name
            # Skip hidden files, readmes, subfolders, or templates
            if filename.startswith("_") or filename.lower() == "readme.md":
                continue
                
            handle = get_candidate_handle(filename)
            # Skip empty or helper files
            if not handle or handle == "SCOUT-SESSION" or handle == "SCOUT-NC":
                continue
                
            if handle not in mapped_handles:
                unmapped.append({
                    "handle": handle,
                    "filename": filename
                })

        result["unmapped_candidates"] = unmapped[:15]
        result["total_unmapped_count"] = len(unmapped)

        # 3. Determine if the unmapped list changed from last run
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        c4_cache = jobs_cache.setdefault("iconocode-backfill", {})

        prev_unmapped_count = c4_cache.get("unmapped_count", 0)
        current_unmapped_count = len(unmapped)

        if prev_unmapped_count != current_unmapped_count or current_unmapped_count > 0:
            result["changed"] = True

        # Save back to cache
        c4_cache["last_run"] = result["last_run"]
        c4_cache["last_status"] = "ok"
        c4_cache["unmapped_count"] = current_unmapped_count
        save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["errors"].append(f"Exception raised during iconocode backfill: {str(e)}")
        result["traceback"] = traceback.format_exc()
        result["changed"] = True

    print(json.dumps(result))

if __name__ == "__main__":
    main()
