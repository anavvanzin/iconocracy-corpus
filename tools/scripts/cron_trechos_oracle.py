import json
import random
import sys
from pathlib import Path
from datetime import datetime
import yaml

def select_random_quote(db_path: Path) -> dict:
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return random.choice(data["posts"])

def update_cache(quote_position: int):
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
    else:
        state = {}
        
    if "jobs" not in state:
        state["jobs"] = {}
        
    state["jobs"]["trechos-oracle"] = {
        "last_run": datetime.now().isoformat(),
        "last_quote_position": quote_position,
        "last_status": "ok"
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)

def main():
    db_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
    if not db_path.exists():
        print("Error: Quotes database forum-data.json not found.", file=sys.stderr)
        return
        
    quote = select_random_quote(db_path)
    update_cache(quote.get("position", 0))
    
    print(f"## Trechos Oracle\n")
    print(f"> {quote.get('bodyText', 'No text')}\n")
    print(f"*— Sourced from your collection of {quote.get('position', 0)}/1608 trechos.*")

if __name__ == "__main__":
    main()
