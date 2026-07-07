import json
import random
import sys
from pathlib import Path
from datetime import datetime
import yaml

def pair_quote_with_record(corpus_path: Path, quotes_path: Path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    with open(quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    
    return random.choice(corpus), random.choice(quotes["posts"])

def update_cache(record_id: str, quote_position: int):
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
    else:
        state = {}
        
    if "jobs" not in state:
        state["jobs"] = {}
        
    state["jobs"]["zwischenraum-generator"] = {
        "last_run": datetime.now().isoformat(),
        "last_item_id": record_id,
        "last_quote_position": quote_position,
        "last_status": "ok"
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    corpus_path = repo_root / "corpus" / "corpus-data.json"
    quotes_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
    
    if not corpus_path.exists():
        print(f"Error: Corpus export not found at {corpus_path}", file=sys.stderr)
        return
    if not quotes_path.exists():
        print("Error: Quotes database forum-data.json not found.", file=sys.stderr)
        return
        
    record, quote = pair_quote_with_record(corpus_path, quotes_path)
    update_cache(record.get("id"), quote.get("position", 0))
    
    print(f"## Mnemosyne Associative Prompt (Zwischenraum)\n")
    print(f"Today's creative tension pairing unites corpus record **{record.get('id')}** (*{record.get('title', 'Untitled')}*) with this literary fragment:\n")
    print(f"> {quote.get('bodyText', 'No text')}\n")
    print(f"*How does the visual representation of state power in {record.get('id')} resonate with the silence or passion in this fragment? Reflect on the fends and gaps in the visual contract.*")

if __name__ == "__main__":
    main()
