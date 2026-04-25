#!/usr/bin/env python3
from __future__ import annotations
"""
upload_thumbnails.py — Generate and upload thumbnails for ICONOCRACY corpus items.

Reads from: Other/analytics.html (DATA hardcoded) or data/processed/records.jsonl
Generates: 300px-wide WebP thumbnails
Outputs: local thumbnails/ directory + updates thumbnail_url in analytics.html

Usage:
    python upload_thumbnails.py [--dry-run] [--limit N] [--item ID] [--r2]

R2 upload requires CLOUDFLARE_API_TOKEN + R2_ACCOUNT_ID env vars.
Without R2 credentials, thumbnails are saved locally only.
"""
import base64
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNING: Pillow not installed. Thumbnails will be downloaded but not resized.")

# ── Config ──────────────────────────────────────────────────────────────────
ANALYTICS_HTML = Path(__file__).resolve().parents[2] / "Other" / "analytics.html"
THUMBNAILS_DIR = Path(__file__).resolve().parents[2] / "thumbnails"
THUMBNAILS_DIR.mkdir(exist_ok=True)

TARGET_WIDTH = 300
THUMBNAIL_QUALITY = 82  # WebP quality
MAX_DIM = (TARGET_WIDTH, TARGET_WIDTH * 2)  # allow tall images

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

TIMEOUT = 15
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ICONOCRACIA-thumbnailer/1.0)"
}

# ── URL cleanup ──────────────────────────────────────────────────────────────
def clean_url(url: str) -> str:
    """Remove query params that cause 302 loops or size limits."""
    if not url:
        return ""
    url = url.split("?")[0]
    # Wikimedia Commons: prefer original upload URL
    url = url.replace("/thumb/", "/")
    # Numista: use the full image URL (strip thumb params)
    url = re.sub(r'thumbs/\d+_\d+', 'images', url)
    return url

# ── Image fetch ───────────────────────────────────────────────────────────────
def fetch_image_bytes(url: str, timeout: int = TIMEOUT) -> bytes | None:
    """Download image bytes from URL. Returns None on failure."""
    if not url or not url.startswith(("http://", "https://")):
        return None
    req = urllib.request.Request(clean_url(url), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
            ct = r.headers.get("Content-Type", "")
            if "image" not in ct and "html" not in ct:
                return r.read()
            elif "image" in ct:
                return r.read()
    except Exception as e:
        print(f"  fetch error {url[:60]}: {e}")
    return None

def make_thumbnail(img_bytes: bytes, max_w: int = TARGET_WIDTH) -> bytes | None:
    """Resize image to max_w, convert to WebP, return bytes."""
    if not HAS_PIL:
        return img_bytes
    try:
        img = Image.open(BytesIO(img_bytes))
        # Convert palette/RGBA
        if img.mode in ("P", "RGBA", "LA"):
            img = img.convert("RGB")
        elif img.mode == "1":
            img = img.convert("L").convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        w, h = img.size
        if w > max_w:
            ratio = max_w / w
            new_h = int(h * ratio)
            img = img.resize((max_w, new_h), Image.LANCZOS)

        buf = BytesIO()
        img.save(buf, format="WEBP", quality=THUMBNAIL_QUALITY, method=6)
        return buf.getvalue()
    except Exception as e:
        print(f"  thumbnail error: {e}")
    return img_bytes if HAS_PIL else None

# ── R2 upload ────────────────────────────────────────────────────────────────
def upload_to_r2(image_bytes: bytes, key: str) -> str | None:
    """Upload thumbnail bytes to Cloudflare R2, return public URL or None."""
    account_id = os.getenv("R2_ACCOUNT_ID")
    bucket = os.getenv("R2_BUCKET", "iconocracia-images")
    token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not all([account_id, token]):
        return None

    url = f"https://{account_id}.r2.cloudflarestorage.com/{bucket}/{key}"
    req = urllib.request.Request(
        url,
        data=image_bytes,
        method="PUT",
        headers={
            "Content-Type": "image/webp",
            "Authorization": f"Bearer {token}",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status in (200, 201):
                return f"/images/{key}"
    except Exception as e:
        print(f"  R2 upload error: {e}")
    return None

# ── Item ID → key ─────────────────────────────────────────────────────────────
def item_key(item_id: str) -> str:
    """Normalize item ID to safe R2 key."""
    return f"{item_id}-thumb.webp"

# ── Parse analytics.html DATA ─────────────────────────────────────────────────
def parse_analytics_data(html_path: Path) -> list[dict]:
    """Extract DATA array from analytics.html using incremental JSON parsing.

    The DATA array contains 165 items spanning exactly 247604 characters
    starting after 'const DATA = [' in the original file.

    The naive json.loads() fails on Python 3.9 because the file contains
    a FR-024 item URL with 'item.]' near position ~505383 — the closing
    ']' of CORES array — which would cause the decoder to stop early.
    We use json.JSONDecoder().raw_decode() in a loop, skipping comma
    separators, to consume exactly the 165 objects in order.
    """
    content = html_path.read_text(encoding="utf-8")
    d_pos = content.find("const DATA = [")
    if d_pos < 0:
        raise ValueError("Could not find 'const DATA = [' in analytics.html")
    json_start = d_pos + len("const DATA = [")

    DATA_ARRAY_LEN = 247604
    s = content[json_start:json_start + DATA_ARRAY_LEN]

    decoder = json.JSONDecoder()
    pos = 0
    items = []

    while pos < DATA_ARRAY_LEN:
        s_rem = s[pos:]
        if not s_rem.strip():
            break
        # Stop if we've reached the closing ] of the DATA array
        if s_rem.startswith("]"):
            break
        try:
            obj, end = decoder.raw_decode(s_rem)
            items.append(obj)
            pos += end
            # Skip optional comma / whitespace separator between objects
            while pos < DATA_ARRAY_LEN and s[pos:pos + 1] in (" ", "\t", "\n", "\r", ","):
                pos += 1
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse DATA array at pos {pos}: {e}"
            ) from e

    return items


def write_analytics_data(html_path: Path, data: list[dict]):
    """Rewrite DATA array in analytics.html, preserving everything else.

    Replacement strategy:
    - Find the DATA array start ('const DATA = [')
    - Find the CORES JavaScript start ('const CORES = [')
    - Replace everything between them with the new JSON + '];'
    """
    content = html_path.read_text(encoding="utf-8")

    d_pos = content.find("const DATA = [")
    cores_pos = content.find("const CORES = [")

    if d_pos < 0:
        raise ValueError("Could not find 'const DATA = [' in analytics.html")
    if cores_pos < 0:
        raise ValueError("Could not find 'const CORES = [' in analytics.html")

    # Build new DATA array JSON — single-line per object (matching original style)
    new_items = []
    for item in data:
        new_items.append(json.dumps(item, ensure_ascii=False))
    new_json = "[\n" + ",\n".join(new_items) + "\n];\n\n"

    # Preserve everything before 'const DATA = [' and after 'const CORES = ['
    before = content[:d_pos]
    after = content[cores_pos:]

    new_content = before + new_json + after
    html_path.write_text(new_content, encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    dry_run = "--dry-run" in sys.argv
    limit = 50
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])
    target_item = None
    if "--item" in sys.argv:
        idx = sys.argv.index("--item")
        target_item = sys.argv[idx + 1]

    use_r2 = "--r2" in sys.argv and os.getenv("CLOUDFLARE_API_TOKEN")

    print(f"Reading {ANALYTICS_HTML}...")
    data = parse_analytics_data(ANALYTICS_HTML)
    print(f"  {len(data)} items loaded")

    needs_thumb = [
        d for d in data
        if not d.get("thumbnail_url") or d.get("thumbnail_url") == ""
    ]
    print(f"  {len(needs_thumb)} need thumbnails")

    if target_item:
        needs_thumb = [d for d in needs_thumb if d["id"] == target_item]

    processed = 0
    updated = 0

    for item in needs_thumb[:limit]:
        item_id = item["id"]
        src_url = item.get("url") or item.get("source_archive_url") or ""
        thumb_path = THUMBNAILS_DIR / item_key(item_id)

        # Skip if already exists locally
        if thumb_path.exists() and not dry_run:
            local_url = f"thumbnails/{item_key(item_id)}"
            if item.get("thumbnail_url") != local_url:
                item["thumbnail_url"] = local_url
                updated += 1
            print(f"  [{item_id}] already local: {local_url}")
            continue

        print(f"  [{item_id}] src: {src_url[:80]}", end="", flush=True)

        if dry_run:
            print(" [DRY RUN]")
            processed += 1
            continue

        img_bytes = fetch_image_bytes(src_url)
        if not img_bytes:
            print(" [FAILED - no image]")
            processed += 1
            continue

        thumb_bytes = make_thumbnail(img_bytes)
        if not thumb_bytes:
            print(" [FAILED - thumbnail]")
            processed += 1
            continue

        # Save locally
        thumb_path.write_bytes(thumb_bytes)
        print(f" -> {thumb_path.stat().st_size:,} bytes")

        # R2 upload
        if use_r2:
            r2_url = upload_to_r2(thumb_bytes, item_key(item_id))
            if r2_url:
                item["thumbnail_url"] = r2_url
            else:
                item["thumbnail_url"] = f"thumbnails/{item_key(item_id)}"
        else:
            item["thumbnail_url"] = f"thumbnails/{item_key(item_id)}"

        updated += 1
        processed += 1
        time.sleep(0.5)  # polite rate limiting

    print(f"\nDone: {processed} items processed, {updated} thumbnail_url updated")

    if updated > 0 and not dry_run:
        # Copy to deploy location
        deploy_analytics = Path(__file__).resolve().parents[2] / "deploy" / "iconocracia-companion" / "public" / "analytics.html"
        if deploy_analytics.exists():
            import shutil
            src = ANALYTICS_HTML
            shutil.copy2(src, deploy_analytics)
            print(f"Copied to {deploy_analytics}")
        write_analytics_data(ANALYTICS_HTML, data)
        print(f"Updated {ANALYTICS_HTML} with new thumbnail_url values")


if __name__ == "__main__":
    main()
