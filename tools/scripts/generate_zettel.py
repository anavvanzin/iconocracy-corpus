#!/usr/bin/env python3
import argparse
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ZETTEL_DIR = REPO_ROOT / "vault" / "zettel"

def get_next_zettel_id():
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = ord('a')
    while True:
        z_id = f"{date_str}{chr(seq)}"
        target = ZETTEL_DIR / f"{z_id}.md"
        if not target.exists():
            return z_id
        seq += 1

def create_zettel(title, content, tags, links):
    ZETTEL_DIR.mkdir(parents=True, exist_ok=True)
    z_id = get_next_zettel_id()
    filepath = ZETTEL_DIR / f"{z_id}.md"
    
    tags_formatted = "\n".join([f"  - {t}" for t in tags])
    links_formatted = "\n".join([f"- [[{l}]]" for l in links]) if links else "*No connections.*"
    
    yaml_header = f"""---
id: {z_id}
title: "{title}"
date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
tags:
{tags_formatted}
---

# {z_id}: {title}

{content}

## Connections
{links_formatted}
"""
    filepath.write_text(yaml_header, encoding="utf-8")
    print(f"Zettelkasten card {z_id} created at: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Zettelkasten note.")
    parser.add_argument("--title", required=True, help="Note title")
    parser.add_argument("--content", required=True, help="Atomic idea content")
    parser.add_argument("--tags", nargs="*", default=["zettel"], help="Tags")
    parser.add_argument("--links", nargs="*", default=[], help="Wiki-links to existing notes")
    args = parser.parse_args()
    
    create_zettel(args.title, args.content, args.tags, args.links)
