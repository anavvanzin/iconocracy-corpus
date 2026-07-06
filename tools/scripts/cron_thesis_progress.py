#!/usr/bin/env python3
"""
C2: Thesis Progress Cron Script
Counts the words in the active manuscript draft, calculates weekly velocity,
updates the state cache, and outputs a JSON summary for the LLM to process.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Absolute Paths
REPO_ROOT = Path("/Users/ana/Research/hub/iconocracy-corpus")
MANUSCRITO_DIR = REPO_ROOT / "tese/manuscrito"
CACHE_PATH = Path("/Users/ana/.hermes/cron-cache/iconocracy-jobs.yaml")

def count_words_in_file(path: Path) -> int:
    """Count words in a markdown file, ignoring frontmatter if present."""
    try:
        content = path.read_text(encoding="utf-8")
        # Strip simple YAML frontmatter if present
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]
        # Count words (sequences of alphanumeric/characters)
        words = re.findall(r"\w+", content)
        return len(words)
    except Exception as e:
        print(f"Warning: Failed to count words in {path}: {e}", file=sys.stderr)
        return 0

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
        "job_id": "thesis-progress",
        "status": "ok",
        "current_words": 0,
        "baseline_words": 0,
        "weekly_velocity": 0,
        "target_weekly": 1000,
        "chapters_counted": [],
        "last_run": datetime.now().isoformat(),
        "errors": []
    }

    if not MANUSCRITO_DIR.exists():
        result["status"] = "error"
        result["errors"].append(f"Manuscript directory not found at: {MANUSCRITO_DIR}")
        print(json.dumps(result))
        return

    try:
        # 1. Identify active manuscript files and count words
        # Active chapters are those in 'tese/manuscrito/*.md', skipping LEIAME, original versions, and backup directories
        total_words = 0
        md_files = sorted(MANUSCRITO_DIR.glob("*.md"))
        
        for md_file in md_files:
            filename = md_file.name
            # Skip readme and summary files
            if filename.lower() in ("leiame.md", "sumario_iconocracia.md") or "original" in filename.lower() or "notas" in filename.lower():
                continue
            
            words = count_words_in_file(md_file)
            if words > 0:
                total_words += words
                result["chapters_counted"].append({
                    "name": filename,
                    "words": words
                })
        
        result["current_words"] = total_words

        # 2. Check and Update Cache
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        c2_cache = jobs_cache.setdefault("thesis-progress", {})

        # Load previous words as baseline
        prev_words = c2_cache.get("current_words")
        if prev_words is not None:
            # Baseline is what we had on the last run
            result["baseline_words"] = prev_words
            result["weekly_velocity"] = total_words - prev_words
        else:
            # Fallback for first run
            result["baseline_words"] = total_words
            result["weekly_velocity"] = 0

        # Preserve manual or custom baseline_words from cache if any
        custom_baseline = c2_cache.get("baseline_words")
        if custom_baseline is not None:
            result["baseline_words"] = custom_baseline
            result["weekly_velocity"] = total_words - custom_baseline

        # Save back to cache
        c2_cache["last_run"] = result["last_run"]
        c2_cache["last_status"] = "ok"
        c2_cache["baseline_words"] = result["baseline_words"]
        c2_cache["current_words"] = total_words
        c2_cache["weekly_velocity"] = result["weekly_velocity"]
        c2_cache["target_weekly"] = result["target_weekly"]
        save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["errors"].append(f"Exception raised during word count: {str(e)}")
        result["traceback"] = traceback.format_exc()

    print(json.dumps(result))

if __name__ == "__main__":
    main()
