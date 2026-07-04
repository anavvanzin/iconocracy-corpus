#!/usr/bin/env python3
"""
Creative Suite - Job 2: The "Mnemosyne" Associative Engine (Zwischenraum Generator)
Selects a random literary quote and a random visual corpus item,
pairs them to spark a Warburgian associative prompt, and prints JSON for the LLM.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

# Paths
QUOTES_DB = Path("/Users/ana/.copilot/repos/anavvanzin.github.io/quotes/forum-data.json")
CORPUS_DATA = Path("/Users/ana/Research/hub/iconocracy-corpus/corpus/corpus-data.json")
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
    text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
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
        "job_id": "zwischenraum-generator",
        "status": "ok",
        "quote": "",
        "quote_author": "Unknown",
        "corpus_item": {},
        "last_run": datetime.now().isoformat(),
        "errors": []
    }

    if not QUOTES_DB.exists():
        result["status"] = "error"
        result["errors"].append(f"Quotes database not found at: {QUOTES_DB}")
        print(json.dumps(result))
        return

    if not CORPUS_DATA.exists():
        result["status"] = "error"
        result["errors"].append(f"Corpus data not found at: {CORPUS_DATA}")
        print(json.dumps(result))
        return

    try:
        # 1. Load random quote
        with open(QUOTES_DB, "r", encoding="utf-8") as f:
            quotes_data = json.load(f)

        posts = quotes_data.get("posts", [])
        valid_posts = [p for p in posts if p.get("bodyText") and p["bodyText"].strip() != "-" and len(p["bodyText"].strip()) > 5]
        
        if not valid_posts:
            result["status"] = "error"
            result["errors"].append("No valid quotes found.")
            print(json.dumps(result))
            return

        selected_post = random.choice(valid_posts)
        body_text = clean_quote(selected_post["bodyText"])
        
        quote_author = "Unknown"
        if "—" in body_text:
            parts = body_text.rsplit("—", 1)
            body_text = parts[0].strip()
            quote_author = parts[1].strip()
        elif "–" in body_text:
            parts = body_text.rsplit("–", 1)
            body_text = parts[0].strip()
            quote_author = parts[1].strip()

        result["quote"] = body_text
        result["quote_author"] = quote_author

        # 2. Load random corpus item
        with open(CORPUS_DATA, "r", encoding="utf-8") as f:
            corpus_json = json.load(f)

        # corpus-data.json could be a list or a dict containing "items"
        items = corpus_json if isinstance(corpus_json, list) else corpus_json.get("items", [])
        valid_items = [item for item in items if item.get("id") or item.get("item_id")]

        if not valid_items:
            result["status"] = "error"
            result["errors"].append("No valid corpus items found.")
            print(json.dumps(result))
            return

        selected_item = random.choice(valid_items)
        
        # Pull key descriptors
        item_id = selected_item.get("id") or selected_item.get("item_id", "Unknown")
        title = selected_item.get("title") or selected_item.get("input", {}).get("title_hint", "Untitled")
        place = selected_item.get("place") or selected_item.get("input", {}).get("place_hint", "Unknown")
        date = selected_item.get("date") or selected_item.get("input", {}).get("date_hint", "Unknown")
        url = selected_item.get("url") or selected_item.get("input", {}).get("input_url", "")
        
        # Get motifs or keywords
        motifs = []
        if "iconocode" in selected_item:
            motifs = [m.get("motif", "") for m in selected_item["iconocode"].get("pre_iconographic", []) if m.get("motif")]

        result["corpus_item"] = {
            "id": item_id,
            "title": title,
            "place": place,
            "date": date,
            "url": url,
            "motifs": motifs[:10]  # limit count
        }

        # 3. Update Cache
        cache = load_cache()
        jobs_cache = cache.setdefault("jobs", {})
        generator_cache = jobs_cache.setdefault("zwischenraum-generator", {})

        generator_cache["last_run"] = result["last_run"]
        generator_cache["last_status"] = "ok"
        generator_cache["last_item_id"] = item_id
        save_cache(cache)

    except Exception as e:
        import traceback
        result["status"] = "error"
        result["errors"].append(f"Exception raised in Zwischenraum Generator: {str(e)}")
        result["traceback"] = traceback.format_exc()

    print(json.dumps(result))

if __name__ == "__main__":
    main()
