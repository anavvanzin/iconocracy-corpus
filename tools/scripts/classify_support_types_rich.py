#!/usr/bin/env python3
"""
Second pass: classify remaining unclassified items using records.jsonl metadata.

Bypasses the heuristic classifier and reads records.jsonl for richer fields:
input.title_hint, webscout search results (URLs, titles), iconclass codes, notes.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"


def load_records(path):
    records = {}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            item_id = r.get("item_id", "")
            # Also find the corresponding corpus id
            exports = r.get("exports", {})
            records[item_id] = r
    return records


def find_corpus_id(record):
    """Try to match a record to a corpus item by looking at various ID fields."""
    return record.get("item_id", "")


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    records = load_records(RECORDS_PATH)

    # Build a lookup by ID (corpus items have 'id' field like "FR-049")
    corpus_by_id = {item["id"]: item for item in corpus}

    # Build a reverse lookup: records item_id -> corpus id
    # We can match by looking at the purification ledger or by matching embedded IDs
    # Let's use a simpler approach: search records by title hint match
    record_by_titlehint = {}
    for rid, rec in records.items():
        title_hint = rec.get("input", {}).get("title_hint", "")
        if title_hint:
            # Normalize for matching
            key = title_hint.lower().strip()
            record_by_titlehint[key] = rec

    # Also build URL-based lookup
    record_by_url = {}
    for rid, rec in records.items():
        url = rec.get("input", {}).get("input_url", "")
        if url:
            record_by_url[url] = rec

    unclassified = [x for x in corpus if x.get("support") == "?"]
    print(f"Still unclassified: {len(unclassified)}")
    print()

    newly_classified = 0
    for item in unclassified:
        item_id = item["id"]
        url = item.get("url", "")
        title = (item.get("title") or "").lower()

        # Strategy 1: match by URL
        rec = record_by_url.get(url)

        # Strategy 2: match by title substring in records
        if not rec:
            for hint, r in record_by_titlehint.items():
                if title and (title in hint or hint in title):
                    rec = r
                    break

        if not rec:
            continue

        # We have a matching record — extract support info
        all_text = ""
        all_text += f" {rec.get('input', {}).get('title_hint', '')}"
        all_text += f" {rec.get('input', {}).get('place_hint', '')}"
        for sr in rec.get("webscout", {}).get("search_results", []):
            all_text += f" {sr.get('title', '')}"
            all_text += f" {sr.get('url', '')}"
            all_text += f" {sr.get('notes', '')}"
            for ic in sr.get("iconclass_candidates", []):
                all_text += f" {ic}"
        for ic in rec.get("iconocode", {}).get("codes", []):
            all_text += f" {ic.get('notation', '')}"
        all_text += f" {rec.get('webscout', {}).get('summary_evidence', '')}"
        notes = rec.get("purificacao", {}).get("notes", "") if "purificacao" in rec else ""
        all_text += f" {notes}"
        all_text_lower = all_text.lower()

        # Classify from richer text
        support = None
        patterns = [
            (r"estamp|gravur|etching|lithograph|litografia", "estampa/gravura"),
            (r"moeda|coin|franc|pfennig|penny|réis|piastre|numista", "moeda"),
            (r"selo|stamp|postage|timbre", "selo"),
            (r"cédula|banknote|paper.money|notgeld|reichsmark|milreis|mil.réis", "papel-moeda"),
            (r"cartaz|poster|affiche|propaganda", "cartaz"),
            (r"monument|statue|escultur|sculptur|busto", "monumento/escultura"),
            (r"frontispício|frontispice|frontispiece", "frontispício"),
            (r"fotograf[ia]|photograph", "fotografia"),
            (r"pintura|painting|óleo|oleo|oil.on", "pintura"),
            (r"medal[ha]|medaille|médaille", "medalha"),
            (r"cerâmica|porcelana|porcelain", "cerâmica"),
            (r"textual|literary|prosopopeia|dialogue|periodical", "texto"),
        ]

        for pattern, st in patterns:
            if re.search(pattern, all_text_lower):
                support = st
                break

        if support:
            item["support"] = support
            newly_classified += 1
            print(f"  {item_id:15} -> {support:20s} (from: {all_text[:60]})")
        else:
            # Debug: show what we have
            print(f"  {item_id:15} -> still ?  (hint: {all_text[:70]})")

    if newly_classified > 0:
        with open(CORPUS_PATH, "w") as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
        print(f"\nNewly classified: {newly_classified}")

    remaining = [x for x in corpus if x.get("support") == "?"]
    print(f"\nStill unclassified after second pass: {len(remaining)}")

    if remaining:
        print("\nManual review needed for:")
        for item in remaining:
            print(f"  {item['id']:15} {item.get('title','')[:70]}")


if __name__ == "__main__":
    main()
