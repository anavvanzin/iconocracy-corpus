#!/usr/bin/env python3
"""
Download corpus images in highest available quality to the SSD.

Priority: Gallica IIIF full-res > url_image_download > thumbnail_url
Saves to: /Volumes/ICONOCRACIA/corpus/imagens/{PAIS}/{ID}.jpg

Usage:
    python download_corpus_images.py [--dry-run] [--only ID1,ID2,...]
"""

import json
import os
import re
import ssl
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# SSL context for sites with cert issues
SSL_UNVERIFIED = ssl.create_default_context()
SSL_UNVERIFIED.check_hostname = False
SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE

CORPUS_PATH = Path(__file__).resolve().parents[2] / "corpus" / "corpus-data-enriched.json"
SSD_BASE = Path("/Volumes/ICONOCRACIA/corpus/imagens")
REPORT_PATH = Path(__file__).resolve().parents[2] / "corpus" / "download-report.md"

# Country prefix → folder mapping
COUNTRY_MAP = {
    "BR": "BR", "FR": "FR", "DE": "DE", "US": "US", "UK": "UK", "BE": "BE",
    "NL": "NL", "PT": "PT", "EU": "EU", "ES": "ES", "MX": "MX", "UY": "UY",
}


def get_country_folder(item_id):
    """Extract country code from item ID prefix."""
    # Handle special IDs like US-EDUC-1896-02, FR-SEM-1898, DE-NOTG-1921, DE-WR-*
    for prefix in sorted(COUNTRY_MAP.keys(), key=len, reverse=True):
        if item_id.startswith(prefix + "-"):
            return COUNTRY_MAP[prefix]
    return "OTHER"


def download_file(url, dest_path, timeout=60, retries=3):
    """Download a file with streaming + retry logic. Returns (success, file_size, error_msg)."""
    for attempt in range(retries):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ICONOCRACIA-corpus/1.0",
                "Accept": "image/jpeg,image/png,image/*,*/*",
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # Stream download in chunks to avoid IncompleteRead
                total_size = 0
                with open(dest_path, "wb") as f:
                    while True:
                        chunk = resp.read(65536)  # 64KB chunks
                        if not chunk:
                            break
                        f.write(chunk)
                        total_size += len(chunk)
                if total_size < 500:
                    os.remove(dest_path)
                    return False, 0, f"File too small ({total_size} bytes) — likely error page"
                return True, total_size, None
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                wait = (attempt + 1) * 5
                print(f"      Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if e.code == 403 and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            return False, 0, f"HTTP {e.code}: {e.reason}"
        except ssl.SSLCertVerificationError:
            # Retry with unverified SSL
            try:
                req2 = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req2, timeout=timeout, context=SSL_UNVERIFIED) as resp:
                    total_size = 0
                    with open(dest_path, "wb") as f:
                        while True:
                            chunk = resp.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                            total_size += len(chunk)
                    if total_size < 500:
                        os.remove(dest_path)
                        return False, 0, f"File too small ({total_size} bytes)"
                    return True, total_size, None
            except Exception as e2:
                return False, 0, f"SSL fallback failed: {e2}"
        except Exception as e:
            # For IncompleteRead, check if we got enough data via streaming
            if "IncompleteRead" in str(e) and os.path.exists(dest_path):
                size = os.path.getsize(dest_path)
                if size > 10000:  # >10KB is probably a valid partial image
                    return True, size, None
                os.remove(dest_path)
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            return False, 0, str(e)
    return False, 0, "Max retries exceeded"


def get_gallica_fullres_url(item):
    """Upgrade Gallica IIIF URL from 1000px to full resolution."""
    dl_url = item.get("url_image_download", "") or ""
    iiif_url = item.get("url_iiif", "") or ""

    # Extract ARK from IIIF manifest URL
    ark_match = re.search(r"(ark:/12148/[a-z0-9]+)", iiif_url or dl_url)
    if ark_match:
        ark = ark_match.group(1)
        # Full resolution IIIF request
        return f"https://gallica.bnf.fr/iiif/{ark}/f1/full/full/0/native.jpg"

    # If URL already has the pattern, just swap 1000, for full
    if "/full/1000,/" in dl_url:
        return dl_url.replace("/full/1000,/", "/full/full/")

    return dl_url


def get_best_url(item):
    """Determine best download URL for an item. Returns (url, source_type)."""
    iiif_source = item.get("iiif_source", "")
    dl_url = item.get("url_image_download", "") or ""
    iiif_url = item.get("url_iiif", "") or ""
    thumb_url = item.get("thumbnail_url", "") or ""

    # Priority 1: Gallica IIIF full resolution
    if iiif_source in ("gallica", "europeana_gallica") and iiif_url:
        fullres = get_gallica_fullres_url(item)
        if fullres:
            return fullres, "gallica_fullres"

    # Priority 2: LoC IIIF (already at pct:100, which is full res)
    if iiif_source in ("loc", "loc_api") and dl_url:
        return dl_url, "loc_direct"

    # Priority 3: Direct download URL (Europeana resolved, thumbnails, etc.)
    if dl_url:
        return dl_url, "direct"

    # Priority 4: Thumbnail fallback
    if thumb_url:
        return thumb_url, "thumbnail"

    return None, "none"


def run_downloads(items, dry_run=False, only_ids=None):
    """Download all corpus images."""
    results = []
    total = 0
    success = 0
    failed = 0
    skipped = 0
    thumbnail_count = 0
    total_bytes = 0

    for item in items:
        item_id = item.get("id", "?")

        if only_ids and item_id not in only_ids:
            continue

        total += 1
        country = get_country_folder(item_id)
        dest_dir = SSD_BASE / country
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Determine file extension from URL
        url, source_type = get_best_url(item)

        if not url:
            print(f"  [{item_id}] ⏭️  No URL available")
            skipped += 1
            results.append({"id": item_id, "status": "skipped", "reason": "no URL"})
            continue

        # Determine extension
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".tif" in url.lower():
            ext = ".tif"

        dest_path = dest_dir / f"{item_id}{ext}"

        # Skip if already downloaded
        if dest_path.exists() and dest_path.stat().st_size > 500:
            size = dest_path.stat().st_size
            print(f"  [{item_id}] ✅ Already exists ({size:,} bytes)")
            success += 1
            total_bytes += size
            results.append({
                "id": item_id, "status": "exists", "size": size,
                "path": str(dest_path), "source": source_type
            })
            item["local_image_path"] = f"corpus/imagens/{country}/{item_id}{ext}"
            continue

        is_thumbnail = source_type == "thumbnail"
        quality_tag = "🖼️ full-res" if source_type == "gallica_fullres" else (
            "📷 direct" if source_type in ("direct", "loc_direct") else "🔍 thumbnail"
        )

        print(f"  [{item_id}] ⬇️  {quality_tag} from {source_type}...", end=" ", flush=True)

        if dry_run:
            print(f"(dry run) → {dest_path}")
            results.append({"id": item_id, "status": "dry_run", "url": url[:80]})
            continue

        ok, size, err = download_file(url, str(dest_path))

        if ok:
            success += 1
            total_bytes += size
            print(f"✅ {size:,} bytes")
            item["local_image_path"] = f"corpus/imagens/{country}/{item_id}{ext}"
            if is_thumbnail:
                thumbnail_count += 1
                # Add tag
                tags = item.get("tags", [])
                if isinstance(tags, list) and "#baixa-resolucao" not in tags:
                    tags.append("#baixa-resolucao")
                    item["tags"] = tags
            results.append({
                "id": item_id, "status": "downloaded", "size": size,
                "path": str(dest_path), "source": source_type
            })
        else:
            failed += 1
            print(f"❌ {err}")
            results.append({
                "id": item_id, "status": "failed", "error": err,
                "url": url[:100], "source": source_type
            })

        # Polite delay between requests
        time.sleep(0.8)

    return {
        "total": total,
        "success": success,
        "failed": failed,
        "skipped": skipped,
        "thumbnails": thumbnail_count,
        "total_bytes": total_bytes,
        "details": results,
    }


def generate_report(stats, items):
    """Generate download report."""
    lines = [
        "# Download Report — ICONOCRACIA Corpus Images",
        "",
        f"**Date**: 2026-04-01",
        f"**Total items**: {stats['total']}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Downloaded | {stats['success']} |",
        f"| Failed | {stats['failed']} |",
        f"| Skipped (no URL) | {stats['skipped']} |",
        f"| Thumbnails (low-res) | {stats['thumbnails']} |",
        f"| Total size | {stats['total_bytes'] / 1024 / 1024:.1f} MB |",
        "",
    ]

    # Group by source type
    from collections import Counter
    sources = Counter(d["source"] for d in stats["details"] if d["status"] in ("downloaded", "exists"))
    if sources:
        lines.extend([
            "## By source type",
            "",
            "| Source | Count |",
            "|--------|-------|",
        ])
        for src, count in sorted(sources.items(), key=lambda x: -x[1]):
            lines.append(f"| {src} | {count} |")
        lines.append("")

    # Failed items
    failures = [d for d in stats["details"] if d["status"] == "failed"]
    if failures:
        lines.extend([
            "## Failed downloads",
            "",
        ])
        for f in failures:
            lines.append(f"- **{f['id']}**: {f.get('error', '?')} — {f.get('url', '')[:80]}")
        lines.append("")

    # Skipped items
    skips = [d for d in stats["details"] if d["status"] == "skipped"]
    if skips:
        lines.extend([
            "## Skipped (no URL available)",
            "",
        ])
        for s in skips:
            lines.append(f"- **{s['id']}**: {s.get('reason', '?')}")
        lines.append("")

    lines.extend([
        "## Storage location",
        "",
        "`/Volumes/ICONOCRACIA/corpus/imagens/{PAIS}/{ID}.jpg`",
        "",
        "Accessible via symlinks at `data/raw/{PAIS}/` in the repository.",
    ])

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report saved to {REPORT_PATH}")


def main():
    dry_run = "--dry-run" in sys.argv
    only_ids = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only_ids = set(sys.argv[idx + 1].split(","))

    # Check SSD
    if not SSD_BASE.exists():
        print("ERROR: SSD not mounted at /Volumes/ICONOCRACIA")
        sys.exit(1)

    print(f"Loading corpus from {CORPUS_PATH}")
    with open(CORPUS_PATH, encoding="utf-8") as f:
        items = json.load(f)

    print(f"Loaded {len(items)} items")
    print(f"SSD base: {SSD_BASE}")
    if dry_run:
        print("DRY RUN — no files will be downloaded")
    print()

    stats = run_downloads(items, dry_run=dry_run, only_ids=only_ids)

    print(f"\n{'='*50}")
    print(f"  Total:      {stats['total']}")
    print(f"  Downloaded: {stats['success']}")
    print(f"  Failed:     {stats['failed']}")
    print(f"  Skipped:    {stats['skipped']}")
    print(f"  Size:       {stats['total_bytes'] / 1024 / 1024:.1f} MB")
    print(f"{'='*50}")

    if not dry_run:
        # Save updated corpus with local_image_path
        with open(CORPUS_PATH, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"\n  Updated {CORPUS_PATH} with local_image_path field")

        # Generate report
        generate_report(stats, items)


if __name__ == "__main__":
    main()
