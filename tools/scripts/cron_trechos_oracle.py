import json
import random
from pathlib import Path
import yaml
from datetime import datetime

def select_random_quote(db_path: Path) -> dict:
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    posts = data.get("posts", [])
    if not posts:
        raise ValueError("No quotes found in database.")
    return random.choice(posts)

def main():
    db_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()

    if not db_path.exists():
        print("Error: Quotes database forum-data.json not found.")
        return

    try:
        quote = select_random_quote(db_path)
    except Exception as e:
        print(f"Error selecting quote: {e}")
        return

    # Print the quote in beautiful markdown format
    print(f"## Trechos Oracle\n\n> {quote.get('bodyText', '').strip()}\n")

    # Update state cache
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                state = yaml.safe_load(f) or {}
            
            if "jobs" not in state:
                state["jobs"] = {}
            if "trechos-oracle" not in state["jobs"]:
                state["jobs"]["trechos-oracle"] = {}

            state["jobs"]["trechos-oracle"]["last_run"] = datetime.now().isoformat()
            state["jobs"]["trechos-oracle"]["last_quote_position"] = quote.get("position", 0)
            state["jobs"]["trechos-oracle"]["last_status"] = "ok"

            with open(cache_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Warning: Failed to update cache: {e}")

if __name__ == "__main__":
    main()
