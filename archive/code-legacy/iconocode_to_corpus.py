#!/usr/bin/env python3
"""
iconocode_to_corpus.py — Merge IconoCode analysis scores into corpus-data.json.

Reads vault/candidatos/ notes that have an ## IconoCode Analysis section,
extracts the 10 purification indicators, and merges them into the matching
item in corpus/corpus-data.json.

Usage:
    python tools/scripts/iconocode_to_corpus.py           # dry run
    python tools/scripts/iconocode_to_corpus.py --write    # write changes
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
VAULT = REPO / "vault" / "candidatos"

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]


def extract_iconocode_from_note(path: Path) -> dict | None:
    """Extract IconoCode scores from a vault note if present."""
    text = path.read_text()

    if "## IconoCode Analysis" not in text and '"indicadores"' not in text:
        return None

    # Try JSON block first
    json_match = re.search(r'"indicadores"\s*:\s*\{([^}]+)\}', text)
    if json_match:
        try:
            raw = "{" + json_match.group(1) + "}"
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

    # Try line-by-line extraction (e.g., "desincorporacao: 3")
    scores = {}
    for ind in INDICATORS:
        match = re.search(rf"{ind}\s*[:=]\s*(\d)", text)
        if match:
            scores[ind] = int(match.group(1))

    return scores if scores else None


def extract_scout_id(path: Path) -> str | None:
    """Extract the SCOUT-NNN id from frontmatter."""
    text = path.read_text()
    match = re.search(r"id:\s*(SCOUT-\d+)", text)
    return match.group(1) if match else None


def find_corpus_match(corpus: list, scout_id: str, note_path: Path) -> dict | None:
    """Try to match a vault note to a corpus-data.json item."""
    # Read the vault note for title/url
    text = note_path.read_text()
    url_match = re.search(r'url:\s*"(https?://[^"]+)"', text)
    title_match = re.search(r'titulo:\s*"(.+?)"', text)

    url = url_match.group(1) if url_match else None
    title = title_match.group(1) if title_match else None

    for item in corpus:
        if url and item.get("url") == url:
            return item
        if title and title.lower() in item.get("title", "").lower():
            return item

    return None


def main():
    write_mode = "--write" in sys.argv

    corpus = json.loads(CORPUS.read_text())
    updated = 0
    found = 0

    for note_path in sorted(VAULT.glob("SCOUT-[0-9]*.md")):
        scores = extract_iconocode_from_note(note_path)
        if not scores:
            continue

        found += 1
        scout_id = extract_scout_id(note_path) or note_path.stem
        match = find_corpus_match(corpus, scout_id, note_path)

        if match:
            endurecimento = round(sum(scores.values()) / len(scores), 2) if scores else 0
            match["iconocode_indicators"] = scores
            match["endurecimento_score"] = endurecimento
            updated += 1
            print(f"  MERGE: {scout_id} → {match['id']} (score: {endurecimento})")
        else:
            print(f"  SKIP: {scout_id} — no match in corpus-data.json")

    print(f"\nFound {found} coded notes, merged {updated} into corpus.")

    if write_mode and updated > 0:
        CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n")
        print(f"Written to {CORPUS}")
    elif updated > 0:
        print("Dry run — use --write to save changes.")


if __name__ == "__main__":
    main()
