import json
import random
from pathlib import Path
import yaml
from datetime import datetime

def pair_quote_with_record(corpus_path: Path, quotes_path: Path) -> tuple:
    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    with open(quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    
    posts = quotes.get("posts", [])
    if not corpus:
        raise ValueError("Corpus database is empty.")
    if not posts:
        raise ValueError("Quotes database is empty.")
        
    return random.choice(corpus), random.choice(posts)

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    corpus_path = repo_root / "corpus" / "corpus-data.json"
    quotes_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()

    if not corpus_path.exists():
        print("Error: Corpus database corpus-data.json not found.")
        return
    if not quotes_path.exists():
        print("Error: Quotes database forum-data.json not found.")
        return

    try:
        record, quote = pair_quote_with_record(corpus_path, quotes_path)
    except Exception as e:
        print(f"Error generating juxtaposition: {e}")
        return

    # Print a beautifully styled Mnemosyne Associative Prompt
    print(f"## Mnemosyne Associative Prompt (Zwischenraum)\n")
    print(f"Pairing visual/legal record **{record.get('id', 'N/A')}** with literary fragment:\n")
    print(f"> \"{quote.get('bodyText', '').strip()}\"\n")
    if 'author' in quote and quote['author']:
        print(f"— {quote['author']}\n")
    
    print(f"**Iconographic Concept:** {record.get('title', 'N/A')}\n")
    print(f"**Tension Prompt:** Construct an associative bridge between this female allegory's legal function and the internal landscape of the literary fragment.")

    # Update state cache
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                state = yaml.safe_load(f) or {}
            
            if "jobs" not in state:
                state["jobs"] = {}
            if "zwischenraum-generator" not in state["jobs"]:
                state["jobs"]["zwischenraum-generator"] = {}

            state["jobs"]["zwischenraum-generator"]["last_run"] = datetime.now().isoformat()
            state["jobs"]["zwischenraum-generator"]["last_item_id"] = record.get("id", "N/A")
            state["jobs"]["zwischenraum-generator"]["last_quote_position"] = quote.get("position", 0)
            state["jobs"]["zwischenraum-generator"]["last_status"] = "ok"

            with open(cache_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Warning: Failed to update cache: {e}")

if __name__ == "__main__":
    main()
