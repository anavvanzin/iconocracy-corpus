#!/usr/bin/env python3
"""
reconcile_data.py — Reconcile corpus-data.json vs records.jsonl

Compares the two canonical data stores of the ICONOCRACY corpus:
  1. corpus/corpus-data.json  (145 items, IDs like AR-001)
  2. data/processed/records.jsonl (139 items, UUIDs)

Matching strategy: primary key is URL; fallback is normalized title+date.

Usage:
    python tools/scripts/reconcile_data.py              # full report
    python tools/scripts/reconcile_data.py --dry-run    # counts only
    python tools/scripts/reconcile_data.py --json       # JSON output
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict


REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"


def normalize_url(url: str) -> str:
    """Strip protocol, trailing slashes, and www. for fuzzy URL matching."""
    if not url:
        return ""
    url = url.strip().rstrip("/")
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url.lower()


def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation and extra whitespace."""
    if not title:
        return ""
    title = re.sub(r"[^\w\s]", "", title.lower())
    return " ".join(title.split())


def load_corpus(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_records(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def build_index(items: list[dict], url_key: str, title_key: str, date_key: str):
    """Build lookup dicts keyed by normalized URL and by title+date."""
    by_url = {}
    by_title = {}
    for item in items:
        url = normalize_url(item.get(url_key, "") if isinstance(item.get(url_key), str)
                            else item.get(url_key, {}).get("input_url", "") if isinstance(item.get(url_key), dict)
                            else "")
        if url:
            by_url[url] = item

        title = item.get(title_key, "") if isinstance(item.get(title_key), str) else ""
        date = str(item.get(date_key, ""))
        key = f"{normalize_title(title)}||{date}"
        if title:
            by_title[key] = item

    return by_url, by_title


def get_corpus_url(item: dict) -> str:
    return normalize_url(item.get("url", ""))


def get_record_url(item: dict) -> str:
    return normalize_url(item.get("input", {}).get("input_url", ""))


def get_corpus_title_key(item: dict) -> str:
    return f"{normalize_title(item.get('title', ''))}||{item.get('date', '')}"


def get_record_title_key(item: dict) -> str:
    inp = item.get("input", {})
    return f"{normalize_title(inp.get('title_hint', ''))}||{inp.get('date_hint', '')}"


def reconcile(corpus: list[dict], records: list[dict]) -> dict:
    """Main reconciliation logic. Returns a results dict."""

    # Build URL indexes
    corpus_by_url = {}
    for c in corpus:
        u = get_corpus_url(c)
        if u:
            corpus_by_url[u] = c

    records_by_url = {}
    for r in records:
        u = get_record_url(r)
        if u:
            records_by_url[u] = r

    # Phase 1: URL matching
    matched = []
    corpus_matched_ids = set()
    record_matched_ids = set()

    for url, c_item in corpus_by_url.items():
        if url in records_by_url:
            r_item = records_by_url[url]
            matched.append((c_item, r_item, "url"))
            corpus_matched_ids.add(c_item["id"])
            record_matched_ids.add(r_item["item_id"])

    # Phase 2: Title+date fallback for unmatched
    unmatched_corpus = [c for c in corpus if c["id"] not in corpus_matched_ids]
    unmatched_records = [r for r in records if r["item_id"] not in record_matched_ids]

    records_title_idx = {}
    for r in unmatched_records:
        k = get_record_title_key(r)
        if k and k != "||":
            records_title_idx[k] = r

    for c in list(unmatched_corpus):
        k = get_corpus_title_key(c)
        if k in records_title_idx:
            r_item = records_title_idx[k]
            matched.append((c, r_item, "title+date"))
            corpus_matched_ids.add(c["id"])
            record_matched_ids.add(r_item["item_id"])

    # Orphans
    orphans_corpus = [c for c in corpus if c["id"] not in corpus_matched_ids]
    orphans_records = [r for r in records if r["item_id"] not in record_matched_ids]

    # Divergences in matched pairs
    divergences = []
    for c_item, r_item, match_type in matched:
        diffs = []
        # Compare title
        c_title = c_item.get("title", "")
        r_title = r_item.get("input", {}).get("title_hint", "")
        if c_title and r_title and normalize_title(c_title) != normalize_title(r_title):
            diffs.append({"field": "title", "corpus": c_title, "records": r_title})

        # Compare date
        c_date = str(c_item.get("date", ""))
        r_date = str(r_item.get("input", {}).get("date_hint", ""))
        if c_date and r_date and c_date != r_date:
            diffs.append({"field": "date", "corpus": c_date, "records": r_date})

        # Compare URL
        c_url = c_item.get("url", "")
        r_url = r_item.get("input", {}).get("input_url", "")
        if c_url and r_url and normalize_url(c_url) != normalize_url(r_url):
            diffs.append({"field": "url", "corpus": c_url, "records": r_url})

        # Check if iconocode exists in records but not coded in corpus
        has_iconocode = bool(r_item.get("iconocode", {}).get("codes"))
        corpus_coded = bool(c_item.get("coded_by"))
        if has_iconocode and not corpus_coded:
            diffs.append({"field": "coding_sync", "corpus": "not coded", "records": "has iconocode"})

        if diffs:
            divergences.append({
                "corpus_id": c_item["id"],
                "record_id": r_item["item_id"],
                "match_type": match_type,
                "differences": diffs,
            })

    return {
        "summary": {
            "corpus_total": len(corpus),
            "records_total": len(records),
            "matched": len(matched),
            "matched_by_url": sum(1 for _, _, m in matched if m == "url"),
            "matched_by_title": sum(1 for _, _, m in matched if m == "title+date"),
            "orphans_corpus": len(orphans_corpus),
            "orphans_records": len(orphans_records),
            "divergent_pairs": len(divergences),
        },
        "orphans_corpus": [
            {"id": c["id"], "title": c.get("title", ""), "url": c.get("url", "")}
            for c in orphans_corpus
        ],
        "orphans_records": [
            {
                "item_id": r["item_id"],
                "title": r.get("input", {}).get("title_hint", ""),
                "url": r.get("input", {}).get("input_url", ""),
            }
            for r in orphans_records
        ],
        "divergences": divergences,
    }


def print_report(results: dict, dry_run: bool = False):
    s = results["summary"]

    print("=" * 70)
    print("  ICONOCRACY CORPUS RECONCILIATION REPORT")
    print("=" * 70)
    print()
    print(f"  corpus-data.json:  {s['corpus_total']:>4} items")
    print(f"  records.jsonl:     {s['records_total']:>4} items")
    print(f"  {'─' * 40}")
    print(f"  Matched:           {s['matched']:>4}  (URL: {s['matched_by_url']}, title: {s['matched_by_title']})")
    print(f"  Orphans (corpus):  {s['orphans_corpus']:>4}  (in corpus but not in records)")
    print(f"  Orphans (records): {s['orphans_records']:>4}  (in records but not in corpus)")
    print(f"  Divergent pairs:   {s['divergent_pairs']:>4}")
    print()

    if dry_run:
        print("  [--dry-run: detail omitted]")
        return

    if results["orphans_corpus"]:
        print("─" * 70)
        print("  ORPHANS: in corpus-data.json only")
        print("─" * 70)
        for o in results["orphans_corpus"]:
            print(f"  {o['id']:>8}  {o['title'][:55]}")
        print()

    if results["orphans_records"]:
        print("─" * 70)
        print("  ORPHANS: in records.jsonl only")
        print("─" * 70)
        for o in results["orphans_records"]:
            title = o["title"][:45] or "(no title)"
            print(f"  {o['item_id'][:12]}…  {title}")
        print()

    if results["divergences"]:
        print("─" * 70)
        print("  FIELD DIVERGENCES")
        print("─" * 70)
        for d in results["divergences"]:
            print(f"  {d['corpus_id']} ↔ {d['record_id'][:12]}… [{d['match_type']}]")
            for diff in d["differences"]:
                print(f"    {diff['field']:>15}: corpus={diff['corpus'][:30]}")
                print(f"    {'':>15}  records={diff['records'][:30]}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Reconcile corpus-data.json vs records.jsonl")
    parser.add_argument("--dry-run", action="store_true", help="Show counts only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--corpus", type=Path, default=CORPUS_PATH)
    parser.add_argument("--records", type=Path, default=RECORDS_PATH)
    args = parser.parse_args()

    if not args.corpus.exists():
        print(f"ERROR: {args.corpus} not found", file=sys.stderr)
        sys.exit(1)
    if not args.records.exists():
        print(f"ERROR: {args.records} not found", file=sys.stderr)
        sys.exit(1)

    corpus = load_corpus(args.corpus)
    records = load_records(args.records)
    results = reconcile(corpus, records)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_report(results, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
