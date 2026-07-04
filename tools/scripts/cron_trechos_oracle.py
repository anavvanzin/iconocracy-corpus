#!/usr/bin/env python3
"""
Creative Suite - Job 1: The "Trechos" Oracle
Selects a random curated literary quote from Ana's forum database,
registers it in the cache, and prints it for the LLM to process and deliver.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

# Paths
QUOTES_DB = Path("/Users/ana/.copilot/repos/anavvanzin.github.io/quotes/forum-data.json")
CACHE_PATH = Path("/Users/ana/.hermes/cron-cache/iconocracy-jobs.yaml")

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

def clean_quote(text: str) -> str:
    """Clean up quotes, stray markdown characters, or HTML fragments."""
    if not text:
        return ""
    text = text.strip()
    # Replace common HTML line breaks
    text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    # Clean up double quotes
    if text.startswith("“") and text.endswith("”"):
        text = text[1:-1].strip()
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text

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
        "job_id": "trechos-oracle",
        "status": "ok",
        "quote": "",
        "author": "Unknown",
        "position": 0,
        "last_run": datetime.now().isoformat(),
        "errors": []
    }

    if not QUOTES_DB.exists():
        result["status"] = "error"
        result["errors"].append(f"Quotes database not found at: {QUOTES_DB}")
        print(json.dumps(result))
        return

    try:
        # 1. Load and parse the database
        with open(QUOTES_DB, "r", encoding="utf-8") as f:
            data = json.load(f)

        posts = data.get("posts", [])
        # Filter out noise (empty, "-", placeholders)
        valid_posts = []
        for p in posts:
            body = p.get("bodyText", "").strip()
            if body and body != "-" and len(body) > 5:
                valid_posts.append(p)

        if not valid_posts:
            result["status"] = "error"
            result["errors"].append("No valid quotes found in the database.")
            print(json.dumps(result))
            return

        # 2. Pick a random quote
        selected_post = random.choice(valid_posts)
        body_text = clean_quote(selected_post["bodyText"])
        position = selected_post.get("position", 0)

        # Separate author if listed (often formatted as "Quote — Author" or "Quote - Author")
        author = "Unknown"
        if "—" in body_text:
            parts = body_text.rsplit("—", 1)
            body_text = parts[0].strip()
            author = parts[1].strip()
        elif "–" in body_text:  # en-dash
            parts = body_text.rsplit("–", 1)
            body_text = parts[0].strip()
            author = parts[1].strip()

        result["quote"] = body_text
        result["author"] = author
        result["position"] = position

        # 3. Update Cache
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        oracle_cache = jobs_cache.setdefault("trechos-oracle", {})

        oracle_cache["last_run"] = result["last_run"]
        oracle_cache["last_status"] = "ok"
        oracle_cache["last_quote_position"] = position
        save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["errors"].append(f"Exception raised in Trechos Oracle: {str(e)}")
        result["traceback"] = traceback.format_exc()

    print(json.dumps(result))

if __name__ == "__main__":
    main()
