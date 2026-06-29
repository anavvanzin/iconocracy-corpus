#!/usr/bin/env python3
"""Download 11 images from Europeana Record API with Gallica IIIF fallback.

Usage:
    python tools/scripts/europeana_download.py
"""

import json
import os
import ssl
import sys
import time
import urllib.request
import urllib.error

# SSL context for servers with cert issues (e.g. Albertina)
SSL_UNVERIFIED = ssl.create_default_context()
SSL_UNVERIFIED.check_hostname = False
SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE

BASE_DIR = "/Users/ana/Research/hub/iconocracy-corpus/data/raw"
API_BASE = "https://api.europeana.eu/record/v2"
WSKEY = "api2demo"
USER_AGENT = "ICONOCRACY-Corpus/1.0 (PPGD/UFSC)"
RATE_LIMIT = 1  # seconds between requests

# (item_id, europeana_record_id, country_folder, gallica_ark_or_None)
ITEMS = [
    ("EU-002", "/2048001/AP_10342206",                        "FR", None),
    ("EU-003", "/89/item_ZCR4KC47OMJN7DRRDFTIWRQS33M7PBN2",  "FR", None),
    ("EU-004", "/446/RML0348941",                             "FR", None),
    ("EU-005", "/15502/KK_6068",                              "FR", None),
    ("EU-006", "/89/item_MH6IXNHWTECBQCNPU7IIMCFP2BDFAV76", "FR", None),
    ("EU-007", "/2048001/AP_10133590",                        "FR", None),
    ("EU-008", "/15508/30435",                                "FR", None),
    ("EU-009", "/15508/DG1918_7",                             "FR", None),
    ("FR-008", "/9200518/ark__12148_btv1b10510623s",          "FR", "ark:/12148/btv1b10510623s"),
    ("FR-009", "/9200518/ark__12148_btv1b6952880n",           "FR", "ark:/12148/btv1b6952880n"),
    ("FR-010", "/9200518/ark__12148_btv1b8577646g",           "FR", "ark:/12148/btv1b8577646g"),
]


def make_request(url: str, is_json: bool = False):
    """HTTP GET with User-Agent. Returns bytes or parsed dict, or None on error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if is_json:
                return json.loads(data)
            return data
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
            print(f"  [WARN] SSL error, retrying without verification ...")
            req2 = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(req2, timeout=30, context=SSL_UNVERIFIED) as resp:
                    data = resp.read()
                    if is_json:
                        return json.loads(data)
                    return data
            except Exception as e2:
                print(f"  [ERROR] SSL fallback also failed: {e2}")
                return None
        print(f"  [ERROR] {url[:100]}  =>  {e}")
        return None


def get_europeana_image_url(record_id: str):
    """Query Europeana Record API and return best image URL or None."""
    api_url = f"{API_BASE}{record_id}.json?wskey={WSKEY}"
    print(f"  API: {api_url}")
    data = make_request(api_url, is_json=True)
    if not data or "object" not in data:
        print("  [WARN] No 'object' in response")
        return None

    obj = data["object"]

    # Try edmIsShownBy (full resolution)
    aggs = obj.get("aggregations", [])
    if aggs:
        url = aggs[0].get("edmIsShownBy")
        if url:
            print(f"  edmIsShownBy: {url[:120]}")
            return url

    # Fallback: edmPreview (thumbnail)
    euro_agg = obj.get("europeanaAggregation", {})
    url = euro_agg.get("edmPreview")
    if url:
        print(f"  edmPreview (fallback): {url[:120]}")
        return url

    print("  [WARN] No image URL in record")
    return None


def gallica_iiif_url(ark: str) -> str:
    """Gallica IIIF URL from ark identifier."""
    return f"https://gallica.bnf.fr/iiif/{ark}/f1/full/1024,/0/default.jpg"


def download_image(url: str, dest: str) -> bool:
    """Download image bytes to dest. Returns True on success."""
    print(f"  GET {url[:120]}")
    data = make_request(url)
    if data and len(data) > 500:
        with open(dest, "wb") as f:
            f.write(data)
        kb = len(data) / 1024
        print(f"  => {dest}  ({kb:.1f} KB)")
        return True
    if data:
        print(f"  [WARN] Only {len(data)} bytes -- probably an error page")
    return False


def main():
    ok_list = []
    fail_list = []

    for idx, (item_id, record_id, country, ark) in enumerate(ITEMS):
        print(f"\n[{idx + 1}/{len(ITEMS)}] {item_id}")

        country_dir = os.path.join(BASE_DIR, country)
        os.makedirs(country_dir, exist_ok=True)
        dest = os.path.join(country_dir, f"{item_id}.jpg")

        if os.path.exists(dest) and os.path.getsize(dest) > 500:
            kb = os.path.getsize(dest) / 1024
            print(f"  Already exists ({kb:.1f} KB) -- skipping")
            ok_list.append(item_id)
            if idx < len(ITEMS) - 1:
                time.sleep(RATE_LIMIT)
            continue

        success = False

        # Strategy 1: Europeana Record API
        img_url = get_europeana_image_url(record_id)
        if img_url:
            time.sleep(RATE_LIMIT)
            success = download_image(img_url, dest)

        # Strategy 2: Gallica IIIF fallback
        if not success and ark:
            print("  Trying Gallica IIIF fallback ...")
            g_url = gallica_iiif_url(ark)
            time.sleep(RATE_LIMIT)
            success = download_image(g_url, dest)

        if success:
            ok_list.append(item_id)
        else:
            fail_list.append(item_id)

        if idx < len(ITEMS) - 1:
            time.sleep(RATE_LIMIT)

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {len(ok_list)}/{len(ITEMS)} downloaded")
    if ok_list:
        print(f"  OK:     {', '.join(ok_list)}")
    if fail_list:
        print(f"  FAILED: {', '.join(fail_list)}")
    print("=" * 60)
    return len(fail_list)


if __name__ == "__main__":
    sys.exit(main())
