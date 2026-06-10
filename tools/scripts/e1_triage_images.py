#!/usr/bin/env python3
# tools/scripts/e1_triage_images.py
"""E1 triage — resolve the best image source per record.

Cascade: local file (sigla-named) -> vault-note thumbnail URL -> excluded.
Outputs e1_worklist.json (codeable) and e1_excluded.json (#no-image).

Usage:
    python tools/scripts/e1_triage_images.py \
        --binaries-root /Users/ana/Research/hub/iconocracy-corpus/binaries/Images-reacquired-2026-06-09 \
        [--skip-head-check] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
VAULT_DIR = REPO / "vault" / "candidatos"
WORKLIST_PATH = REPO / "data" / "processed" / "e1_worklist.json"
EXCLUDED_PATH = REPO / "data" / "processed" / "e1_excluded.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
HEAD_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (iconocracy-corpus E1 triage; academic research)"


def load_records(path: Path = RECORDS_PATH) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def load_corpus_url_map(path: Path = CORPUS_PATH) -> dict[str, dict]:
    items = json.loads(path.read_text(encoding="utf-8"))
    return {it["url"]: it for it in items if it.get("url")}


def find_sigla(record: dict, url_map: dict[str, dict]) -> str:
    url = record.get("input", {}).get("input_url", "")
    item = url_map.get(url)
    if item and item.get("id"):
        return item["id"]
    # fallback: SCOUT id from webscout notes
    for sr in record.get("webscout", {}).get("search_results", []):
        m = re.search(r"((?:SCOUT|[A-Z]{2})-\d+)", sr.get("notes", ""))
        if m:
            return m.group(1)
    return record["item_id"][:12]


def find_local_image(sigla: str, roots: list[Path]) -> Path | None:
    for root in roots:
        for ext in IMAGE_EXTS:
            p = root / f"{sigla}{ext}"
            if p.is_file():
                return p
    return None


def extract_vault_thumb(sigla: str, vault_dir: Path = VAULT_DIR) -> str | None:
    for f in vault_dir.glob(f"{sigla}*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"\[imagem\]\((https?://[^)]+)\)", text)
        if m:
            return m.group(1)
        m = re.search(r"thumbnail[^:]*:\s*(https?://\S+)", text, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(")").rstrip(">")
    return None


def head_is_image(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=HEAD_TIMEOUT) as resp:
            ctype = resp.headers.get("Content-Type", "")
            return ctype.startswith("image/")
    except Exception:
        return False


def build_worklist(records: list[dict], url_map: dict[str, dict],
                   binaries_roots: list[Path], vault_dir: Path,
                   head_check: bool = True) -> tuple[list[dict], list[dict]]:
    now = datetime.now(timezone.utc).isoformat()
    worklist: list[dict] = []
    excluded: list[dict] = []
    for rec in records:
        sigla = find_sigla(rec, url_map)
        inp = rec.get("input", {})
        base = {
            "item_id": rec["item_id"],
            "sigla_id": sigla,
            "title": inp.get("title_hint", ""),
            "place": inp.get("place_hint", ""),
            "date": inp.get("date_hint", ""),
            "url": inp.get("input_url", ""),
        }
        local = find_local_image(sigla, binaries_roots)
        if local:
            worklist.append({**base, "image_source": "local",
                             "path_or_url": str(local), "status": "pending"})
            continue
        thumb = extract_vault_thumb(sigla, vault_dir)
        if thumb:
            if head_check and not head_is_image(thumb):
                excluded.append({**base, "reason": "not_an_image",
                                 "candidate_url": thumb, "checked_at": now})
                continue
            worklist.append({**base, "image_source": "url",
                             "path_or_url": thumb, "status": "pending"})
            continue
        excluded.append({**base, "reason": "no_image_source", "checked_at": now})
    return worklist, excluded


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--binaries-root", action="append", type=Path, default=[],
                    help="dir with sigla-named images (repeatable)")
    ap.add_argument("--skip-head-check", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    records = load_records()
    if args.limit:
        records = records[: args.limit]
    url_map = load_corpus_url_map()
    worklist, excluded = build_worklist(
        records, url_map, args.binaries_root, VAULT_DIR,
        head_check=not args.skip_head_check)

    WORKLIST_PATH.write_text(
        json.dumps(worklist, ensure_ascii=False, indent=1), encoding="utf-8")
    EXCLUDED_PATH.write_text(
        json.dumps(excluded, ensure_ascii=False, indent=1), encoding="utf-8")
    n_local = sum(1 for w in worklist if w["image_source"] == "local")
    print(f"worklist: {len(worklist)} (local={n_local}, "
          f"url={len(worklist) - n_local}) | excluded: {len(excluded)}")
    for reason in ("no_image_source", "not_an_image", "image_unreachable"):
        n = sum(1 for e in excluded if e["reason"] == reason)
        if n:
            print(f"  excluded/{reason}: {n}")


if __name__ == "__main__":
    main()
