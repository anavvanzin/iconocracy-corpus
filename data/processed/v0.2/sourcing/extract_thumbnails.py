#!/usr/bin/env python3
"""Thumbnail sourcing for amber-recoverable v0.2 items."""
import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

SCRIPT_DIR = Path(__file__).resolve().parent
SNAPSHOT_DIR = SCRIPT_DIR.parent
DEFAULT_INPUT = SNAPSHOT_DIR / "amber_recoverable_full.json"
DEFAULT_OUTPUT = SCRIPT_DIR / "round1_candidates.json"

UA = "Mozilla/5.0 (compatible; iconocracy-corpus-research/1.0; +https://github.com/anavvanzin/iconocracy-corpus)"


def first_scalar(value):
    """Return a stable scalar string from LOC list/string/dict metadata."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        for item in value:
            text = first_scalar(item)
            if text:
                return text
        return ""
    if isinstance(value, dict):
        if len(value) == 1:
            return str(next(iter(value.keys())))
        return ", ".join(str(k) for k in value)
    return str(value)

def fetch(url, timeout=15, extra_headers=None):
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,pt-BR;q=0.9,fr;q=0.8",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
        try:
            return body.decode("utf-8", errors="ignore"), dict(r.headers), r.geturl()
        except Exception:
            return body, dict(r.headers), r.geturl()

def extract_og(html):
    """Extract og:image and og:image:secure_url."""
    for pat in [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
    ]:
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1)
    return None

def h_loc(url, item):
    """Library of Congress: use JSON API."""
    sep = "&" if "?" in url else "?"
    resp, _, _ = fetch(url + sep + "fo=json")
    data = json.loads(resp)
    res = (data.get("resources") or [{}])[0]
    img = res.get("image") or ""
    # LOC provides multiple sizes via files
    largest = None
    for f_group in res.get("files", []):
        for f in f_group:
            if f.get("mimetype", "").startswith("image/") and f.get("mimetype") != "image/tiff":
                if not largest or (f.get("width") or 0) > (largest.get("width") or 0):
                    largest = f
    if largest and largest.get("url"):
        img = largest["url"]
    it = data.get("item", {})
    rights = first_scalar(it.get("rights_advisory"))
    date_on_page = first_scalar(it.get("dates"))
    return {
        "image_url": img,
        "license": rights or "",
        "license_source": "Library of Congress rights_advisory",
        "title_on_page": it.get("title", ""),
        "date_on_page": date_on_page,
        "notes": "",
    }

def h_wikipedia(url, item):
    """Wikipedia: use REST API for the article to get the lead image."""
    m = re.search(r"wikipedia\.org/wiki/([^?#]+)", url)
    if not m:
        return None
    title = urllib.parse.unquote(m.group(1))
    lang = re.search(r"//([a-z]+)\.wikipedia", url).group(1)
    api = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    resp, _, _ = fetch(api)
    data = json.loads(resp)
    img = (data.get("originalimage") or data.get("thumbnail") or {}).get("source", "")
    return {
        "image_url": img,
        "license": "See Wikimedia Commons file page for per-image license",
        "license_source": f"Wikipedia {lang} article",
        "title_on_page": data.get("title", ""),
        "date_on_page": None,
        "notes": data.get("description", ""),
    }

def h_gallica(url, item):
    """Gallica: use IIIF thumbnail service. Extract ARK id."""
    m = re.search(r"gallica\.bnf\.fr/(?:ark:/12148/([^/?#]+)|.*ark:/12148/([^/?#]+))", url)
    ark = None
    if m:
        ark = m.group(1) or m.group(2)
    if not ark:
        # try og:image fallback
        html, _, _ = fetch(url)
        og = extract_og(html)
        return {"image_url": og or "", "license": "Domaine public (Gallica)", "license_source": "Gallica BnF", "title_on_page": "", "date_on_page": None, "notes": ""}
    iiif = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f1/full/1200,/0/native.jpg"
    return {
        "image_url": iiif,
        "license": "Domaine public (Gallica) or per-item — verify on source page",
        "license_source": "Gallica BnF IIIF",
        "title_on_page": "",
        "date_on_page": None,
        "notes": f"ARK: {ark}",
    }

def h_europeana(url, item):
    """Europeana: extract record ID and use API."""
    # /portal/en/record/{dataset}/{id}
    m = re.search(r"europeana\.eu/(?:portal/[a-z]+/)?record/([^/]+)/([^?#/]+)", url)
    if not m:
        html, _, _ = fetch(url)
        og = extract_og(html)
        return {"image_url": og or "", "license": "See Europeana page", "license_source": "Europeana", "title_on_page": "", "date_on_page": None, "notes": ""}
    dataset, rid = m.group(1), m.group(2)
    # Europeana public API needs a key, but they also expose IIIF/edmIsShownBy in JSON-LD on the page
    html, _, _ = fetch(url)
    og = extract_og(html)
    # find edmIsShownBy in JSON-LD
    ld = re.search(r'"edmIsShownBy":\s*"([^"]+)"', html)
    img = og or (ld.group(1) if ld else "")
    rights = re.search(r'"webResourceEdmRights"[^"]*"([^"]+)"', html) or re.search(r'"rights":\s*"([^"]+)"', html)
    return {
        "image_url": img,
        "license": rights.group(1) if rights else "See Europeana record",
        "license_source": "Europeana",
        "title_on_page": "",
        "date_on_page": None,
        "notes": f"Record: {dataset}/{rid}",
    }

def h_met(url, item):
    """Met Museum: use collection API. Extract object ID."""
    m = re.search(r"metmuseum\.org/art/collection/search/(\d+)", url)
    if not m:
        return None
    oid = m.group(1)
    api = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}"
    resp, _, _ = fetch(api)
    data = json.loads(resp)
    return {
        "image_url": data.get("primaryImage") or data.get("primaryImageSmall") or "",
        "license": ("Public domain — CC0" if data.get("isPublicDomain") else "Restricted — see Met page"),
        "license_source": "Met Museum API",
        "title_on_page": data.get("title", ""),
        "date_on_page": data.get("objectDate"),
        "notes": data.get("creditLine", ""),
    }

def h_smithsonian(url, item):
    """Smithsonian NMAH: use og:image."""
    html, _, _ = fetch(url)
    og = extract_og(html)
    return {
        "image_url": og or "",
        "license": "See Smithsonian record",
        "license_source": "Smithsonian NMAH",
        "title_on_page": "",
        "date_on_page": None,
        "notes": "",
    }

def h_generic(url, item):
    """Generic: try og:image with a browser-like UA."""
    try:
        html, headers, final_url = fetch(url)
        if isinstance(html, bytes):
            return None
        og = extract_og(html)
        return {
            "image_url": og or "",
            "license": "See source page",
            "license_source": urllib.parse.urlparse(final_url).netloc,
            "title_on_page": "",
            "date_on_page": None,
            "notes": "",
        }
    except (HTTPError, URLError) as e:
        return {"image_url": "", "license": "", "license_source": "", "title_on_page": "", "date_on_page": None, "notes": f"BLOCKED: {e}"}

HANDLERS = [
    ("loc.gov", h_loc),
    ("wikipedia.org", h_wikipedia),
    ("gallica.bnf.fr", h_gallica),
    ("europeana.eu", h_europeana),
    ("metmuseum.org", h_met),
    ("americanhistory.si.edu", h_smithsonian),
]

def route(url, item):
    for host_frag, handler in HANDLERS:
        if host_frag in url:
            try:
                return handler(url, item)
            except Exception as e:
                return {"image_url": "", "license": "", "license_source": "", "title_on_page": "", "date_on_page": None, "notes": f"HANDLER_ERROR: {e}"}
    return h_generic(url, item)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Input amber recoverable JSON")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output round1 candidates JSON")
    parser.add_argument("--delay", type=float, default=0.4, help="Delay between requests in seconds")
    args = parser.parse_args()

    input_path = args.input.expanduser().resolve()
    output_path = args.output.expanduser().resolve()

    with open(input_path, encoding="utf-8") as f:
        items = json.load(f)
    results = []
    for i, it in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {it['id']:30s} {urllib.parse.urlparse(it['source_url']).netloc}", flush=True)
        r = route(it['source_url'], it)
        r = r or {}
        r['id'] = it['id']
        r['source_url'] = it['source_url']
        r['expected_title'] = it['title']
        r['year'] = it['year']
        r['country'] = it['country']
        r['support'] = it['support']
        results.append(r)
        time.sleep(args.delay)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    # summary
    hit = sum(1 for r in results if r.get('image_url'))
    print(f"\nHITS: {hit}/{len(results)}")
    # by host
    from collections import Counter
    by_host_hit = Counter()
    by_host_total = Counter()
    for it, r in zip(items, results):
        host = urllib.parse.urlparse(it['source_url']).netloc
        by_host_total[host] += 1
        if r.get('image_url'):
            by_host_hit[host] += 1
    print("\nBy host (hits/total):")
    for h, tot in sorted(by_host_total.items(), key=lambda x: -x[1]):
        print(f"  {by_host_hit[h]:3d}/{tot:3d}  {h}")

if __name__ == "__main__":
    main()
