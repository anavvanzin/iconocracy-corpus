import os
from pathlib import Path
import yaml

def main():
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if not cache_path.exists():
        initial_data = {
            "jobs": {
                "trechos-oracle": {"last_run": None, "last_quote_position": 0},
                "zwischenraum-generator": {"last_run": None, "last_item_id": None},
                "thesis-progress-coach": {"last_run": None, "baseline_words": 0}
            }
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(initial_data, f, default_flow_style=False, allow_unicode=True)
        print(f"Initialized cache state at: {cache_path}")
    else:
        print("Cache state already exists.")

if __name__ == "__main__":
    main()
