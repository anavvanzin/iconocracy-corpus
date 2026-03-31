#!/usr/bin/env python3
"""
notion_sync.py — Sincroniza corpus-data.json ↔ Notion database (DB1).

Uses the Notion MCP tools when available (via Claude Code), or falls back
to direct Notion API calls.

Uso:
    python tools/scripts/notion_sync.py pull   # Notion → corpus-data.json
    python tools/scripts/notion_sync.py push   # corpus-data.json → Notion
    python tools/scripts/notion_sync.py diff   # Show differences without writing
    python tools/scripts/notion_sync.py status # Count items in both

Variáveis de ambiente requeridas:
    NOTION_API_KEY          Token de integração Notion
    NOTION_CORPUS_DB_ID     ID da database principal (DB1)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
RECORDS = REPO / "data" / "processed" / "records.jsonl"

NOTION_VERSION = "2022-06-28"


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"ERRO: variável de ambiente {name} não definida.", file=sys.stderr)
        print(f"  export {name}=<valor>", file=sys.stderr)
        sys.exit(1)
    return val


def _notion_headers() -> dict:
    return {
        "Authorization": f"Bearer {_require_env('NOTION_API_KEY')}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _query_notion_db(db_id: str) -> list[dict]:
    """Query all pages from a Notion database."""
    if not HAS_REQUESTS:
        print("ERRO: 'requests' não instalado. pip install requests", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = _notion_headers()
    pages = []
    payload: dict = {}

    while True:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        pages.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]

    return pages


def _extract_notion_item(page: dict) -> dict:
    """Extract corpus fields from a Notion page."""
    props = page.get("properties", {})

    def _text(prop_name: str) -> str:
        p = props.get(prop_name, {})
        if p.get("type") == "title":
            return "".join(t.get("plain_text", "") for t in p.get("title", []))
        if p.get("type") == "rich_text":
            return "".join(t.get("plain_text", "") for t in p.get("rich_text", []))
        if p.get("type") == "url":
            return p.get("url") or ""
        if p.get("type") == "select":
            sel = p.get("select")
            return sel.get("name", "") if sel else ""
        return ""

    return {
        "notion_id": page["id"],
        "id": _text("ID") or _text("id"),
        "title": _text("Title") or _text("Titulo") or _text("title"),
        "country": _text("Country") or _text("Pais") or _text("country"),
        "date": _text("Date") or _text("Data") or _text("date"),
        "url": _text("URL") or _text("url"),
        "medium": _text("Medium") or _text("Suporte") or _text("medium"),
        "regime": _text("Regime") or _text("regime"),
        "last_edited": page.get("last_edited_time", ""),
    }


def _load_corpus() -> list[dict]:
    return json.loads(CORPUS.read_text())


def status():
    """Show item counts in both systems."""
    corpus = _load_corpus()
    print(f"Local corpus-data.json: {len(corpus)} items")

    try:
        db_id = _require_env("NOTION_CORPUS_DB_ID")
        pages = _query_notion_db(db_id)
        print(f"Notion DB1: {len(pages)} pages")

        # Find items in corpus but not Notion (by title match)
        notion_titles = {_extract_notion_item(p)["title"].lower() for p in pages}
        corpus_titles = {item.get("title", "").lower() for item in corpus}
        only_local = corpus_titles - notion_titles
        only_notion = notion_titles - corpus_titles

        if only_local:
            print(f"\nOnly in local ({len(only_local)}):")
            for t in sorted(only_local)[:10]:
                print(f"  + {t[:80]}")
        if only_notion:
            print(f"\nOnly in Notion ({len(only_notion)}):")
            for t in sorted(only_notion)[:10]:
                print(f"  - {t[:80]}")
        if not only_local and not only_notion:
            print("\nIn sync (by title match).")
    except SystemExit:
        print("Notion credentials not set — showing local only.")


def diff():
    """Show differences between local and Notion."""
    status()  # For now, diff = status. Full field-level diff is TODO.


def pull():
    """Pull from Notion → update corpus-data.json with new items."""
    db_id = _require_env("NOTION_CORPUS_DB_ID")
    pages = _query_notion_db(db_id)
    corpus = _load_corpus()

    corpus_urls = {item.get("url", ""): item for item in corpus if item.get("url")}
    corpus_titles = {item.get("title", "").lower(): item for item in corpus}

    added = 0
    for page in pages:
        notion_item = _extract_notion_item(page)
        # Check if already in corpus
        if notion_item["url"] in corpus_urls:
            continue
        if notion_item["title"].lower() in corpus_titles:
            continue

        # New item from Notion
        new_item = {
            "id": notion_item["id"] or f"NOTION-{added+1:03d}",
            "title": notion_item["title"],
            "date": notion_item["date"],
            "country": notion_item["country"],
            "medium": notion_item["medium"],
            "url": notion_item["url"],
            "source_archive": "Notion DB1",
            "notion_id": notion_item["notion_id"],
        }
        corpus.append(new_item)
        added += 1
        print(f"  PULL: {new_item['id']} — {new_item['title'][:60]}")

    if added:
        CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n")
        print(f"\nAdded {added} items from Notion. Total: {len(corpus)}")
    else:
        print("No new items in Notion.")


def push():
    """Push corpus-data.json → create pages in Notion for items not yet there."""
    db_id = _require_env("NOTION_CORPUS_DB_ID")
    corpus = _load_corpus()
    pages = _query_notion_db(db_id)

    notion_titles = {_extract_notion_item(p)["title"].lower() for p in pages}

    pushed = 0
    for item in corpus:
        title = item.get("title", "")
        if title.lower() in notion_titles:
            continue

        # Create Notion page
        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "Title": {"title": [{"text": {"content": title}}]},
                "ID": {"rich_text": [{"text": {"content": item.get("id", "")}}]},
                "Country": {"rich_text": [{"text": {"content": item.get("country", "")}}]},
                "Date": {"rich_text": [{"text": {"content": item.get("date", "")}}]},
                "URL": {"url": item.get("url") or None},
                "Medium": {"rich_text": [{"text": {"content": item.get("medium", "")}}]},
            },
        }

        resp = requests.post(
            "https://api.notion.com/v1/pages",
            headers=_notion_headers(),
            json=payload,
        )
        if resp.status_code == 200:
            pushed += 1
            print(f"  PUSH: {item.get('id', '?')} — {title[:60]}")
        else:
            print(f"  FAIL: {item.get('id', '?')} — {resp.status_code}: {resp.text[:100]}")

    print(f"\nPushed {pushed} items to Notion.")


def main():
    parser = argparse.ArgumentParser(description="Sincroniza corpus-data.json ↔ Notion")
    parser.add_argument("command", choices=["pull", "push", "diff", "status"])
    args = parser.parse_args()

    {"pull": pull, "push": push, "diff": diff, "status": status}[args.command]()


if __name__ == "__main__":
    main()
