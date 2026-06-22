#!/usr/bin/env python3
"""
irr_sample.py — Stratified sampling for IRR re-run.

Selects 30 items from the eligible population (real images only), stratified by
iconocratic regime, and exports corresponding images to data/processed/irr_re_run/sample/.

Usage:
    python tools/scripts/irr_sample.py --size 30 --seed 20260611
    python tools/scripts/irr_sample.py --size 25 --seed 20260611 --dry-run
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PURIFICATION_PATH = REPO_ROOT / "data" / "processed" / "purification.jsonl"
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
ID_MAPPING_PATH = REPO_ROOT / "data" / "processed" / "id-mapping.json"
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
DRIVE_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "drive-manifest.json"

SAMPLE_METADATA_OUT = REPO_ROOT / "data" / "processed" / "irr_re_run" / "sample_metadata.jsonl"
SAMPLE_IMAGES_DIR = REPO_ROOT / "data" / "processed" / "irr_re_run" / "sample"

# Known manual fallbacks for items without direct mappings
MANUAL_IMAGE_FALLBACKS = {
    "787ce58d-f363-5bdb-bfbe-6a6a531624bd": "FR-PIAST-1885.jpg"  # Numista Piastre mapping
}

INDICATORS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]

REGIMES = ["fundacional", "normativo", "militar", "contra-alegoria"]

REGIME_LABEL_MAP = {
    "FUNDACIONAL": "fundacional",
    "NORMATIVO": "normativo",
    "MILITAR": "militar",
    "CONTRA-ALEGORIA": "contra-alegoria",
    "fundacional": "fundacional",
    "normativo": "normativo",
    "militar": "militar",
    "contra-alegoria": "contra-alegoria",
}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_real_image(record: dict) -> bool:
    """
    Determine if a records.jsonl item has a real image (not textual/placeholder).
    """
    ws = record.get("webscout", {})
    search_results = ws.get("search_results", [])
    exports = record.get("exports", {})
    audit_flags = exports.get("audit_flags", [])

    # Explicit textual marker
    for res in search_results:
        notes = res.get("notes", "").lower()
        if "textual" in notes and "no image" in notes:
            return False
        if "ausencia alegorica" in notes.lower() or "ausência alegórica" in notes.lower():
            return False

    # Placeholder URL
    input_url = record.get("input", {}).get("input_url", "")
    if "iconocracy.corpus/placeholder" in input_url:
        return False

    # Summary too short (likely textual-only coding)
    summary = ws.get("summary_evidence", "")
    if len(summary.strip()) < 100:
        return False

    # Has at least one primary_image result with real content
    has_primary = any(res.get("source_type") == "primary_image" for res in search_results)
    if not has_primary:
        return False

    # sem-thumbnail flag means no thumbnail was generated, but full image may exist
    # Don't filter on this - check actual image paths instead
    return True


def debug_image_detection(records: list[dict], purif_ids: set, max_debug: int = 10):
    """Debug helper to understand why items are filtered out."""
    print(f"  DEBUG: Called with {len(records)} records, {len(purif_ids)} purif_ids")
    rec_ids = [r["item_id"] for r in records[:5]]
    purif_list = list(purif_ids)[:5]
    print(f"  First 5 record IDs: {rec_ids}")
    print(f"  First 5 purif IDs:  {purif_list}")

    debug_count = 0
    for r in records:
        if r["item_id"] not in purif_ids:
            continue
        if debug_count >= max_debug:
            break
        debug_count += 1

        ws = r.get("webscout", {})
        search_results = ws.get("search_results", [])
        exports = r.get("exports", {})
        audit_flags = exports.get("audit_flags", [])
        summary = ws.get("summary_evidence", "")
        url = r.get("input", {}).get("input_url", "")

        reasons = []
        for res in search_results:
            notes = res.get("notes", "").lower()
            if "textual" in notes and "no image" in notes:
                reasons.append("textual-no-image")
            if "ausencia alegorica" in notes.lower() or "ausência alegórica" in notes.lower():
                reasons.append("ausencia-alegorica")
        if "iconocracy.corpus/placeholder" in url:
            reasons.append("placeholder-url")
        if len(summary.strip()) < 100:
            reasons.append(f"short-summary({len(summary)})")
        has_primary = any(res.get("source_type") == "primary_image" for res in search_results)
        if not has_primary:
            reasons.append("no-primary-image")

        is_real = len(reasons) == 0
        print(f"  {r['item_id'][:12]}: real={is_real} reasons={reasons} url={url[:60]}")


def get_gallica_iiif_url(url: str) -> str | None:
    """Extract Gallica ARK identifier and build IIIF direct image link."""
    match = re.search(r"(ark:/12148/[a-z0-9]+)", url)
    if match:
        ark = match.group(1)
        return f"https://gallica.bnf.fr/iiif/{ark}/f1/full/full/0/native.jpg"
    return None


def download_image(url: str, dest_path: Path) -> bool:
    """Download an image file from a URL to dest_path."""
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        headers = {
            "User-Agent": "iconocracy-irr-sample/1.0 (+https://github.com/anavvanzin/iconocracy-corpus)"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            dest_path.write_bytes(content)
        return True
    except Exception as e:
        print(f"  [Downloader] Error downloading from {url}: {e}", file=sys.stderr)
        return False


def get_image_paths(item_id: str, corpus_id: str, record: dict) -> list[Path]:
    """
    Find candidate image paths on disk or download if URL available.
    Returns list of existing Path objects (empty if none found).
    """
    search_dirs = [
        Path("/media/ana/SSD_DATA/images"),
        Path("/media/ana/SSD_DATA"),
        REPO_ROOT / "images",
        REPO_ROOT / "Images",
        REPO_ROOT / "Images" / "Images",
        Path("/data/iconocracy-corpus/binaries/Images"),
        REPO_ROOT / ".cache" / "iconocode-images",
    ]

    candidates = []

    # Filenames to try
    filenames = set()
    if corpus_id:
        filenames.update([
            f"{corpus_id}.jpg", f"{corpus_id}.jpeg", f"{corpus_id}.png",
            f"{corpus_id.lower()}.jpg", f"{corpus_id.lower()}.jpeg", f"{corpus_id.lower()}.png",
            f"{corpus_id.upper()}.jpg", f"{corpus_id.upper()}.jpeg", f"{corpus_id.upper()}.png",
        ])
    if item_id:
        base = item_id.replace("-", "")
        filenames.update([
            f"{base}.jpg", f"{base}.jpeg", f"{base}.png",
            f"{item_id}.jpg", f"{item_id}.jpeg", f"{item_id}.png",
            f"{item_id.lower()}.jpg", f"{item_id.lower()}.jpeg", f"{item_id.lower()}.png",
        ])

    # Exact match search
    for sdir in search_dirs:
        if not sdir.exists():
            continue
        for fname in filenames:
            p = sdir / fname
            if p.exists() and p.is_file():
                candidates.append(p)

    # Case-insensitive stem search
    for sdir in search_dirs:
        if not sdir.exists():
            continue
        try:
            for fpath in sdir.iterdir():
                if not fpath.is_file():
                    continue
                stem = fpath.stem.lower()
                if corpus_id and stem == corpus_id.lower():
                    candidates.append(fpath)
                if item_id and stem == item_id.lower().replace("-", ""):
                    candidates.append(fpath)
        except Exception:
            pass

    # Deduplicate
    seen = set()
    uniq = []
    for c in candidates:
        rp = c.resolve()
        if rp not in seen:
            seen.add(rp)
            uniq.append(c)

    if uniq:
        return uniq

    # Try download from URLs if no local file found
    urls_to_try = []

    # 1. Check record URLs
    input_url = record.get("input", {}).get("input_url", "")
    if input_url:
        urls_to_try.append(input_url)

    # 2. Check webscout search results
    ws = record.get("webscout", {})
    for res in ws.get("search_results", []):
        if res.get("url"):
            urls_to_try.append(res["url"])

    # Download from first working URL (Gallica IIIF only for now)
    for url in urls_to_try:
        if "gallica.bnf.fr" in url:
            iiif_url = get_gallica_iiif_url(url)
            if iiif_url:
                dest = REPO_ROOT / ".cache" / "iconocode-images" / f"{item_id}.jpg"
                print(f"  [Downloader] Found Gallica URL for {item_id[:12]}. Fetching IIIF image...")
                if download_image(iiif_url, dest):
                    return [dest]

    return uniq


def main():
    parser = argparse.ArgumentParser(description="Stratified IRR sample with image export")
    parser.add_argument("--size", type=int, default=30, choices=[25, 30], help="Sample size (25 or 30)")
    parser.add_argument("--seed", type=int, default=20260611, help="Random seed for reproducibility")
    parser.add_argument("--dry-run", action="store_true", help="Show selection without copying images")
    parser.add_argument("--force", action="store_true", help="Overwrite existing sample directory")
    args = parser.parse_args()

    print("=== IRR Re-run Sample Selection ===\n")

    # Load data
    print("Loading data...")
    purifications = load_jsonl(PURIFICATION_PATH)
    records = load_jsonl(RECORDS_PATH)
    id_mapping = load_json(ID_MAPPING_PATH)
    corpus_data = load_json(CORPUS_PATH)
    drive_manifest = load_json(DRIVE_MANIFEST_PATH)

    # Build lookups
    records_by_id = {r["item_id"]: r for r in records}
    item_to_corpus = {m["item_id"]: m["corpus_id"] for m in id_mapping.get("mapping", [])}
    corpus_by_id = {c["id"]: c for c in corpus_data}
    drive_by_id = {item["id"]: item for item in drive_manifest.get("items", [])} if drive_manifest else {}

    # Index purifications by corpus_id (sigla), then map to item_id
    purif_by_corpus = {}
    for p in purifications:
        corpus_id = p.get("id")
        if corpus_id:
            purif_by_corpus[corpus_id] = p

    # Build purif_by_item via mapping
    purif_by_item = {}
    mapped = 0
    for item_id, corpus_id in item_to_corpus.items():
        if corpus_id in purif_by_corpus:
            purif_by_item[item_id] = purif_by_corpus[corpus_id]
            mapped += 1

    print(f"  Purifications (by corpus_id): {len(purif_by_corpus)}")
    print(f"  Mapped to item_ids: {mapped}")
    print(f"  Records: {len(records_by_id)} items")
    print(f"  Corpus: {len(corpus_by_id)} items")

    purif_ids = set(purif_by_item.keys())
    print(f"\n--- Image detection debug (first 15 of {len(purif_ids)} mapped items) ---")
    debug_image_detection(records, purif_ids, max_debug=15)

    # Build eligible population: items with purification + real image
    eligible = []
    for item_id, purif in purif_by_item.items():
        record = records_by_id.get(item_id)
        if not record:
            continue
        if not is_real_image(record):
            continue

        corpus_id = item_to_corpus.get(item_id, "")
        corpus_item = corpus_by_id.get(corpus_id, {})
        drive_item = drive_by_id.get(corpus_id, {})

        # Regime from purification (authoritative)
        regime_raw = purif.get("regime_iconocratico", "").strip().lower()
        regime = REGIME_LABEL_MAP.get(regime_raw, "fundacional")

        # Support from corpus or drive
        support = (corpus_item.get("support") or drive_item.get("support") or "monumento").strip().lower()

        # Image paths (skip download in dry-run, just check local)
        if args.dry_run:
            # Fast path: just check local, don't attempt downloads
            img_paths = []
            search_dirs = [
                Path("/media/ana/SSD_DATA/images"),
                Path("/media/ana/SSD_DATA"),
                REPO_ROOT / "images",
                REPO_ROOT / "Images",
                REPO_ROOT / "Images" / "Images",
                Path("/data/iconocracy-corpus/binaries/Images"),
                REPO_ROOT / ".cache" / "iconocode-images",
            ]
            # Quick check for any matching files
            for sdir in search_dirs:
                if sdir.exists():
                    for f in sdir.iterdir():
                        if f.is_file() and (corpus_id and corpus_id.lower() in f.stem.lower() or item_id.replace("-", "").lower() in f.stem.lower()):
                            img_paths.append(f)
                            break
                if img_paths:
                    break
            # Also check drive manifest
            if not img_paths and drive_item.get("local_path"):
                lp = Path(drive_item["local_path"])
                if lp.exists():
                    img_paths = [lp]
        else:
            img_paths = get_image_paths(item_id, corpus_id, record)
            if not img_paths:
                # Check drive manifest for local_path
                if drive_item.get("local_path"):
                    lp = Path(drive_item["local_path"])
                    if lp.exists():
                        img_paths = [lp]

        if not img_paths:
            continue

        eligible.append({
            "item_id": item_id,
            "corpus_id": corpus_id,
            "regime": regime,
            "support": support,
            "image_paths": img_paths,
            "record": record,
        })

    print(f"\nEligible population (real images): {len(eligible)} items")

    # Stratify by regime
    strata = defaultdict(list)
    for e in eligible:
        strata[e["regime"]].append(e)

    print("\nStratum counts:")
    for r in REGIMES:
        print(f"  {r:<15} {len(strata[r]):>3}")

    # Proportional allocation
    total_eligible = sum(len(strata[r]) for r in REGIMES)
    target = args.size

    allocation = {}
    for r in REGIMES:
        prop = len(strata[r]) / total_eligible if total_eligible > 0 else 0
        alloc = round(prop * target)
        allocation[r] = max(1, alloc) if len(strata[r]) > 0 else 0

    # Adjust to exact target
    diff = target - sum(allocation.values())
    for r in sorted(REGIMES, key=lambda x: len(strata[x]), reverse=True):
        if diff == 0:
            break
        if allocation[r] < len(strata[r]):
            allocation[r] += 1
            diff -= 1

    print(f"\nTarget sample size: {target}")
    print("Allocation:")
    for r in REGIMES:
        if allocation[r] > 0:
            print(f"  {r:<15} {allocation[r]:>2} / {len(strata[r])}")

    # Sample with fixed seed
    rng = random.Random(args.seed)
    selected = []
    for r in REGIMES:
        k = allocation[r]
        if k <= 0:
            continue
        pool = strata[r]
        chosen = rng.sample(pool, min(k, len(pool)))
        selected.extend(chosen)

    print(f"\nSelected {len(selected)} items.")

    if args.dry_run:
        print("\n--- DRY RUN: Selected items ---")
        for s in selected:
            print(f"  {s['item_id'][:12]}  regime={s['regime']:<15} support={s['support']:<15} corpus={s['corpus_id']}")
        return 0

    # Prepare output directory
    if SAMPLE_IMAGES_DIR.exists():
        if args.force:
            shutil.rmtree(SAMPLE_IMAGES_DIR)
        else:
            print(f"\nError: {SAMPLE_IMAGES_DIR} exists. Use --force to overwrite.")
            return 1
    SAMPLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_METADATA_OUT.parent.mkdir(parents=True, exist_ok=True)

    # Copy images and write metadata
    metadata_lines = []
    for idx, s in enumerate(selected, 1):
        src_img = s["image_paths"][0]  # Use first match
        ext = src_img.suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            ext = ".jpg"
        dst_name = f"{idx:02d}_{s['item_id'][:8]}{ext}"
        dst_path = SAMPLE_IMAGES_DIR / dst_name

        try:
            shutil.copy2(src_img, dst_path)
        except Exception as e:
            print(f"  Warning: Failed to copy {src_img} → {dst_path}: {e}")
            # Try next available
            for alt in s["image_paths"][1:]:
                try:
                    shutil.copy2(alt, dst_path)
                    break
                except Exception:
                    continue
            else:
                print(f"  ERROR: No usable image for {s['item_id']}")
                continue

        meta = {
            "item_id": s["item_id"],
            "corpus_id": s["corpus_id"],
            "regime": s["regime"],
            "support": s["support"],
            "image_file": dst_name,
            "image_path": str(dst_path.relative_to(REPO_ROOT)),
            "sample_index": idx,
        }
        metadata_lines.append(json.dumps(meta, ensure_ascii=False))

    # Write metadata JSONL
    with open(SAMPLE_METADATA_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(metadata_lines) + "\n")

    print(f"\n✅ Sample ready:")
    print(f"   Images:    {SAMPLE_IMAGES_DIR}")
    print(f"   Metadata:  {SAMPLE_METADATA_OUT}")
    print(f"   Items:     {len(selected)} ({args.size} target)")

    # Regime distribution in final sample
    final_regimes = defaultdict(int)
    for s in selected:
        final_regimes[s["regime"]] += 1
    print("   Distribution:", dict(final_regimes))

    return 0


if __name__ == "__main__":
    sys.exit(main())