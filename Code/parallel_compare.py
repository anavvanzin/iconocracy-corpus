#!/usr/bin/env python3
"""Compare Parallel AI FindAll results with existing corpus to identify gaps.

Usage:
    python tools/scripts/parallel_compare.py results.json
    python tools/scripts/parallel_compare.py results.json --save-gaps
"""

import json
import sys
from pathlib import Path

CORPUS_PATH = Path(__file__).parent.parent.parent / "corpus" / "corpus-data.json"

# Countries in our thesis scope
SCOPE_COUNTRIES = {"France", "Germany", "United Kingdom", "United States", "Belgium", "Brazil",
                   "Argentina", "Italy", "Spain", "Portugal", "Netherlands", "Switzerland",
                   "Mexico", "Uruguay", "Austria"}


def normalize(s: str) -> str:
    return s.lower().strip().replace("–", "-").replace("—", "-")


def load_corpus():
    with open(CORPUS_PATH) as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("items", data.get("data", []))
    titles = {normalize(it.get("title", ""))[:60] for it in items}
    return items, titles


def load_parallel(path: str):
    with open(path) as f:
        data = json.load(f)
    candidates = data.get("candidates", data.get("matches", data.get("results", [])))
    return candidates


def main():
    if len(sys.argv) < 2:
        print("Usage: python parallel_compare.py <results.json> [--save-gaps]")
        sys.exit(1)

    results_path = sys.argv[1]
    save_gaps = "--save-gaps" in sys.argv

    corpus_items, corpus_titles = load_corpus()
    candidates = load_parallel(results_path)

    matched = [c for c in candidates if c.get("match_status") == "matched"]
    print(f"Parallel FindAll: {len(candidates)} candidates, {len(matched)} matched")
    print(f"Existing corpus:  {len(corpus_items)} items")
    print()

    new_allegories = []
    known = []

    for c in matched:
        name = c.get("name", "")
        enrichments = c.get("enrichments", [{}])
        output = enrichments[0].get("output", {}) if enrichments else {}
        allegory_name = output.get("allegory_name", name)
        country = output.get("country_of_use", "?")
        earliest = output.get("earliest_use_date", "?")
        latest = output.get("latest_use_date", "?")
        desc = output.get("symbolism_description", "")

        # fuzzy match against corpus titles
        name_norm = normalize(allegory_name)
        found = any(name_norm[:20] in t or t[:20] in name_norm for t in corpus_titles if len(t) > 5)

        entry = {
            "name": allegory_name,
            "country": country,
            "earliest": earliest,
            "latest": latest,
            "description": desc[:120],
            "in_corpus": found,
        }

        if found:
            known.append(entry)
        else:
            new_allegories.append(entry)

    print(f"── Already in corpus: {len(known)}")
    print(f"── NEW (not in corpus): {len(new_allegories)}")
    print()

    if new_allegories:
        # separate in-scope vs out-of-scope
        in_scope = [a for a in new_allegories if a["country"] in SCOPE_COUNTRIES]
        out_scope = [a for a in new_allegories if a["country"] not in SCOPE_COUNTRIES]

        print(f"  In scope ({len(in_scope)}):")
        for a in sorted(in_scope, key=lambda x: x["country"]):
            print(f"    {a['name']:40s} {a['country']:20s} [{a['earliest']} → {a['latest']}]")

        if out_scope:
            print(f"\n  Out of scope ({len(out_scope)}):")
            for a in sorted(out_scope, key=lambda x: x["country"]):
                print(f"    {a['name']:40s} {a['country']:20s} [{a['earliest']} → {a['latest']}]")

    if save_gaps and new_allegories:
        gaps_path = Path(results_path).with_suffix(".gaps.json")
        with open(gaps_path, "w") as f:
            json.dump(new_allegories, f, indent=2, ensure_ascii=False)
        print(f"\nGaps saved to: {gaps_path}")


if __name__ == "__main__":
    main()
