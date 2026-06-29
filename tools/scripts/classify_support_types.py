#!/usr/bin/env python3
"""
Classify support type (medium_norm/support) for corpus items missing it.

Reads corpus-data.json, classifies items missing 'support' field using
title/description keyword heuristics, and writes the result back.

Usage:
    conda activate iconocracy
    python tools/scripts/classify_support_types.py
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"

# Keyword rules ordered by specificity (first match wins)
SUPPORT_RULES = [
    # High-specificity matches (look for bracketed hints like "[estampe]")
    (r"\[estampa\]|\[estampe\]|\[gravura\]|\[print\]|\.gravura|litografia", "estampa/gravura"),
    (r"\[fotografia\]|\[photographie\]|\[photograph\]|\.foto\",|fotografia[^a]", "fotografia"),
    (r"\[medalh[ae]\]|medalha", "medalha"),
    (r"\[moeda\]|coin[^a-z]|penny[^a-z]|moeda|piastre[^a-z]|franc[^a-z]|réis|pfennig", "moeda"),
    (r"\[selo\]|postage[^a-z]|selo[^a-z]", "selo"),
    (r"\[cartaz\]|poster|affiche|cartaz[^a-z]", "cartaz"),
    (r"\[monumento\]|monument|statue|escultura|sculptur|busto", "monumento/escultura"),
    (r"\[papel-moeda\]|banknote|paper.money|cédula|notgeld|reichsmark|mil.réis|milreis", "papel-moeda"),
    (r"frontispício|frontispice|frontispiece", "frontispício"),
    (r"pintura[^a-z]|painting|óleo.sobre|oleo|oil.on.canvas|\.pintura", "pintura"),
    (r"cerâmica|porcelana|faiança", "cerâmica"),
    (r"textual|literary|prosopopeia|dialogue|periodical|artigo|jornal", "texto"),
    (r"cartaz|propaganda|affiche", "cartaz"),
    (r"estamp|gravur|print|etching|lithograph|litografia", "estampa/gravura"),
    (r"fotograf[ia]|photograph", "fotografia"),
]


def classify_support(item):
    """Infer support type from a corpus item's title and description."""
    text = f"{item.get('title', '')} {item.get('description', '')}"
    text_lower = text.lower()

    for pattern, support_type in SUPPORT_RULES:
        if re.search(pattern, text_lower):
            return support_type

    # Last resort: if description contains both artist and technique keywords
    # or item id hints at type
    item_id = item.get("id", "")
    # Numista items are usually coins
    url = item.get("url", "")
    if "numista" in url:
        return "moeda"
    if "gallica" in url and "estamp" in text_lower:
        return "estampa/gravura"
    if "gallica" in url:
        return "estampa/gravura"

    return "?"  # truly unclassifiable


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    missing = [x for x in corpus if not x.get("support")]
    print(f"Total corpus items: {len(corpus)}")
    print(f"Items missing support: {len(missing)}")

    if not missing:
        print("Nothing to classify.")
        return

    # Track classification results
    classified = {}
    unclassified = []

    for item in missing:
        support = classify_support(item)
        item["support"] = support
        classified[support] = classified.get(support, 0) + 1
        if support == "?":
            unclassified.append(item["id"])

    # Write back
    with open(CORPUS_PATH, "w") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print("\nClassification results:")
    for st, count in sorted(classified.items(), key=lambda x: -x[1]):
        print(f"  {st:25s} {count:3d} items")
    print(f"\nUnclassified: {len(unclassified)}")
    for uid in unclassified[:10]:
        print(f"  {uid}")
    print(f"\nWritten to {CORPUS_PATH}")


if __name__ == "__main__":
    main()
