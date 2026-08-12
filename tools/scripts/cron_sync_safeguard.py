#!/usr/bin/env python3
"""
C3: Sync Safeguard Cron Script
Checks the git status of Research root and iconocracy-corpus repo.
Checks if SSD mirror is mounted and synced, and identifies uncommitted files.
Updates the state cache, and outputs a JSON summary for the LLM.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Absolute Paths
RESEARCH_ROOT = Path("/Users/ana/Research")
CORPUS_REPO = Path("/Users/ana/Research/hub/iconocracy-corpus")
SSD_MIRROR_DIR = Path("/Volumes/ICONOCRACIA/git-mirrors")
CACHE_PATH = Path("/Users/ana/.hermes/cron-cache/iconocracy-jobs.yaml")

def get_git_status(repo_path: Path) -> dict:
    """Check git status of a repository."""
    status = {
        "exists": False,
        "is_dirty": False,
        "uncommitted_files": [],
        "branch": "",
        "last_commit_time": "",
        "days_since_commit": 0.0
    }
    
    if not repo_path.exists() or not (repo_path / ".git").exists():
        return status
        
    status["exists"] = True
    
    try:
        # Get active branch
        branch_proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(repo_path)
        )
        status["branch"] = branch_proc.stdout.strip()
        
        # Get dirty status (porcelain)
        status_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(repo_path)
        )
        lines = [line.strip() for line in status_proc.stdout.splitlines() if line.strip()]
        if lines:
            status["is_dirty"] = True
            # Limit the file list to avoid token bloating
            status["uncommitted_files"] = lines[:15]
            if len(lines) > 15:
                status["uncommitted_files"].append(f"... and {len(lines) - 15} more files")
                
        # Get last commit timestamp
        commit_proc = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            capture_output=True, text=True, cwd=str(repo_path)
        )
        if commit_proc.returncode == 0 and commit_proc.stdout.strip():
            commit_timestamp = int(commit_proc.stdout.strip())
            last_commit = datetime.fromtimestamp(commit_timestamp, tz=timezone.utc)
            status["last_commit_time"] = last_commit.isoformat()
            
            # Calculate days since last commit
            delta = datetime.now(timezone.utc) - last_commit
            status["days_since_commit"] = round(delta.total_seconds() / 86400, 2)
            
    except Exception as e:
        print(f"Warning: Failed to parse git status for {repo_path}: {e}", file=sys.stderr)
        
    return status

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
        "job_id": "sync-safeguard",
        "status": "ok",
        "changed": False,
        "research_root": {},
        "corpus_repo": {},
        "ssd_mounted": False,
        "warnings": [],
        "last_run": datetime.now().isoformat()
    }

    try:
        # 1. Audit Git Status
        result["research_root"] = get_git_status(RESEARCH_ROOT)
        result["corpus_repo"] = get_git_status(CORPUS_REPO)

        # 2. Audit SSD Mirror Presence
        ssd_mounted = SSD_MIRROR_DIR.exists()
        result["ssd_mounted"] = ssd_mounted

        # 3. Formulate Warnings & Detect "Changed" State (to decide on [SILENT])
        is_dirty = result["research_root"].get("is_dirty", False) or result["corpus_repo"].get("is_dirty", False)
        
        # Warning trigger: uncommitted changes or long time since commit
        if is_dirty:
            result["warnings"].append("Uncommitted local changes exist in your workspace.")
            # If the last commit is older than 24 hours, raise precedence
            if result["research_root"].get("days_since_commit", 0) > 1.0 or result["corpus_repo"].get("days_since_commit", 0) > 1.0:
                result["warnings"].append("No local commits made in the last 24 hours despite active changes.")

        if not ssd_mounted:
            # We don't always spam the user with SSD warnings unless they are dirty
            if is_dirty:
                result["warnings"].append("SSD Backup drive /Volumes/ICONOCRACIA/ is not mounted. Sync deferred.")

        # 4. Check Cache to determine if result "changed"
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        c3_cache = jobs_cache.setdefault("sync-safeguard", {})

        prev_dirty = c3_cache.get("is_mac_dirty", False)
        prev_mounted = c3_cache.get("ssd_mounted", False)

        # We consider state "changed" if dirty status changes, ssd mount state changes, or warnings increase
        if prev_dirty != is_dirty or prev_mounted != ssd_mounted or len(result["warnings"]) > 0:
            result["changed"] = True

        # Always trigger "changed" if we're dirty and it's been more than a day (continuous nudge)
        if is_dirty and (result["research_root"].get("days_since_commit", 0) > 1.0 or result["corpus_repo"].get("days_since_commit", 0) > 1.0):
            result["changed"] = True

        # Save back to cache
        c3_cache["last_run"] = result["last_run"]
        c3_cache["last_status"] = "ok"
        c3_cache["is_mac_dirty"] = is_dirty
        c3_cache["ssd_mounted"] = ssd_mounted
        save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["warnings"].append(f"Exception raised during sync safeguard: {str(e)}")
        result["traceback"] = traceback.format_exc()
        result["changed"] = True

    print(json.dumps(result))

if __name__ == "__main__":
    main()
