#!/usr/bin/env python3
"""
Batch 2 re-acquisition script: 33 items from bildindex.de, britishmuseum.org,
bndigital.bnportugal.gov.pt, memoria.bn.br (BR-007 PDF), and misc domains.
"""
import urllib.request
import urllib.error
import json
import re
import time
import os
import sys

OUTPUT_DIR = "/home/user/iconocracy-corpus/binaries/Images-reacquired-2026-06-08"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

BATCH2_ITEMS = [
    ("BE-001", "https://collections.heritage.brussels/fr/objects/36822"),
    ("BE-002", "https://be-monumen.be/patrimoine-belge/poelaert-joseph/"),
    ("BR-005", "https://archive.nyu.edu/handle/2451/61396"),
    ("BR-006", "https://brasiliana.museus.gov.br/acervos/alegoria-da-republica/"),
    ("BR-007", "http://memoria.bn.br/pdf/702390/per702390_1827_00060.pdf"),
    ("BR-009", "https://acervos.ims.com.br/index.php/Detail/objects/18758"),
    ("BR-010", "https://eliseuvisconti.com.br/obra/d702/"),
    ("DE-001", "https://www.bildindex.de/document/que20183316"),
    ("DE-002", "https://www.bildindex.de/document/obj08148970"),
    ("DE-003", "https://www.bildindex.de/document/obj30110594"),
    ("DE-004", "https://www.bildindex.de/document/obj20553978"),
    ("DE-005", "https://www.bildindex.de/document/obj20672587"),
    ("DE-006", "https://www.bildindex.de/document/obj08158050"),
    ("DE-007", "https://www.bildindex.de/document/obj08108743"),
    ("DE-008", "https://www.bildindex.de/document/obj20608421"),
    ("DE-009", "https://www.bildindex.de/document/obj20459153"),
    ("DE-010", "https://www.bildindex.de/document/obj20677105"),
    ("DE-011", "https://www.bildindex.de/document/obj30143134"),
    ("DE-012", "https://lucascranach.org/en/PRIVATE_NONE-P457/"),
    ("DE-013", "https://www.dhm.de/lemo/bestand/objekt/gemaelde-friedrich-august-von-kaulbach-germania-1914"),
    ("DE-GERM-1900", "https://en.wikipedia.org/wiki/Germania_(stamp)"),
    ("DE-GERM-BELG-1914", "https://colnect.com/en/stamps/stamp/320475-overprint_on_Germania-Belgium-Belgium_German_Occupation_i"),
    ("ES-001", "https://bdh.bne.es/bnesearch/detalle/76944"),
    ("ES-002", "https://hemerotecadigital.bne.es/hd/es/card?sid=3971781"),
    ("PT-001", "https://bndigital.bnportugal.gov.pt/records/item/17148-justica-popular"),
    ("PT-002", "https://bndigital.bnportugal.gov.pt/records/item/39213-alegoria-a-historia"),
    ("PT-003", "https://bndigital.bnportugal.gov.pt/records/item/37491-alegoria-a-morte"),
    ("PT-004", "https://bndigital.bnportugal.gov.pt/records/item/37507-alegoria-ao-tempo"),
    ("UK-001", "https://www.britishmuseum.org/collection/object/P_1870-0625-185"),
    ("UK-002", "https://www.britishmuseum.org/collection/object/P_1862-0712-304"),
    ("UK-003", "https://www.britishmuseum.org/collection/object/P_1862-0712-305"),
    ("UK-004", "http://www.speel.me.uk/sculptlondon/oldbaileyjustice.htm"),
    ("UY-001", "https://www.museos.gub.uy/index.php/component/k2/item/1550-juan-manuel-blanes-1830-1901"),
]

def fetch_url(url, extra_headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.geturl()

def detect_magic(data):
    if len(data) < 12:
        return None, "TOO_SHORT"
    if data[:3] == b'\xff\xd8\xff':
        return "jpg", "JPEG"
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return "png", "PNG"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return "webp", "WEBP"
    if data[:4] == b'%PDF':
        return "pdf", "PDF"
    sniff = data[:50].lower()
    if b'<html' in sniff or b'<!doc' in sniff:
        return None, "HTML"
    return None, "UNKNOWN"

def extract_og_image(html_bytes):
    try:
        html = html_bytes.decode('utf-8', errors='replace')
    except:
        return None
    # og:image
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # twitter:image
    m = re.search(r'<meta[^>]+(?:name|property)=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:name|property)=["\']twitter:image["\']', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None

def extract_first_large_img(html_bytes, base_url=""):
    try:
        html = html_bytes.decode('utf-8', errors='replace')
    except:
        return None
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html, re.IGNORECASE)
    for src in imgs:
        if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            if not src.startswith('http'):
                from urllib.parse import urljoin
                src = urljoin(base_url, src)
            return src
    return None

def fetch_image_from_url(img_url):
    data, _ = fetch_url(img_url)
    ext, magic_name = detect_magic(data)
    if ext:
        return data, ext, magic_name
    return None, None, magic_name

def handle_bildindex(item_id, url):
    html, final_url = fetch_url(url, extra_headers={"Accept": "text/html,application/xhtml+xml"})
    html_str = html.decode('utf-8', errors='replace')

    # Try og:image first
    img_url = extract_og_image(html)

    # Try bildanzeige img
    if not img_url:
        m = re.search(r'<img[^>]+id=["\']bildanzeige["\'][^>]+src=["\']([^"\']+)["\']', html_str, re.IGNORECASE)
        if m:
            img_url = m.group(1)

    # Try bildindex.de/bilder/ pattern
    if not img_url:
        m = re.search(r'(https://(?:www\.)?bildindex\.de/bilder/[^\s"\'<>]+)', html_str)
        if m:
            img_url = m.group(1)

    # Try data-src or large image patterns
    if not img_url:
        m = re.search(r'data-src=["\']([^"\']+(?:jpg|jpeg|png|webp)[^"\']*)["\']', html_str, re.IGNORECASE)
        if m:
            img_url = m.group(1)

    if not img_url:
        # Try any image with typical art pattern
        m = re.search(r'src=["\']([^"\']*(?:obj|que|bild)[^"\']*\.(?:jpg|jpeg|png|webp))["\']', html_str, re.IGNORECASE)
        if m:
            img_url = m.group(1)

    if not img_url:
        return None, None, "NO_OG_IMAGE", None

    if not img_url.startswith('http'):
        from urllib.parse import urljoin
        img_url = urljoin(final_url, img_url)

    data, final_img_url = fetch_url(img_url)
    ext, magic_name = detect_magic(data)
    if ext:
        return data, ext, magic_name, img_url
    return None, None, f"BAD_MAGIC:{magic_name}", img_url

def handle_britishmuseum(item_id, url):
    html, final_url = fetch_url(url, extra_headers={"Accept": "text/html,application/xhtml+xml"})
    img_url = extract_og_image(html)
    if not img_url:
        return None, None, "NO_OG_IMAGE", None
    if not img_url.startswith('http'):
        from urllib.parse import urljoin
        img_url = urljoin(final_url, img_url)
    data, final_img_url = fetch_url(img_url)
    ext, magic_name = detect_magic(data)
    if ext:
        return data, ext, magic_name, img_url
    return None, None, f"BAD_MAGIC:{magic_name}", img_url

def handle_bnportugal(item_id, url):
    html, final_url = fetch_url(url)
    html_str = html.decode('utf-8', errors='replace')
    img_url = extract_og_image(html)

    # Try IIIF manifest
    if not img_url:
        m = re.search(r'(https://[^\s"\'<>]+/manifest[^\s"\'<>]*)', html_str)
        if m:
            manifest_url = m.group(1)
            try:
                manifest_data, _ = fetch_url(manifest_url, extra_headers={"Accept": "application/json"})
                manifest = json.loads(manifest_data)
                # IIIF v3
                try:
                    img_url = manifest['items'][0]['items'][0]['items'][0]['body']['id']
                except (KeyError, IndexError, TypeError):
                    pass
                # IIIF v2
                if not img_url:
                    try:
                        img_url = manifest['sequences'][0]['canvases'][0]['images'][0]['resource']['@id']
                    except (KeyError, IndexError, TypeError):
                        pass
            except:
                pass

    if not img_url:
        # Look for IIIF image service URL pattern
        m = re.search(r'(https://[^\s"\'<>]+/iiif/[^\s"\'<>]+/full/[^\s"\'<>]+)', html_str)
        if m:
            img_url = m.group(1)

    if not img_url:
        img_url = extract_first_large_img(html, final_url)

    if not img_url:
        return None, None, "NO_OG_IMAGE", None

    if not img_url.startswith('http'):
        from urllib.parse import urljoin
        img_url = urljoin(final_url, img_url)

    data, _ = fetch_url(img_url)
    ext, magic_name = detect_magic(data)
    if ext:
        return data, ext, magic_name, img_url
    return None, None, f"BAD_MAGIC:{magic_name}", img_url

def handle_br007_pdf(item_id, url):
    # Download the PDF
    data, _ = fetch_url(url)
    ext, magic_name = detect_magic(data)
    if ext != "pdf":
        return None, None, f"BAD_MAGIC:{magic_name}", None

    pdf_path = os.path.join(OUTPUT_DIR, f"{item_id}.pdf")
    with open(pdf_path, 'wb') as f:
        f.write(data)

    # Try pdftoppm
    import subprocess
    out_prefix = os.path.join(OUTPUT_DIR, f"{item_id}_p060")
    try:
        result = subprocess.run(
            ["pdftoppm", "-f", "60", "-l", "60", "-jpeg", "-r", "200", pdf_path, out_prefix],
            capture_output=True, timeout=60
        )
        # pdftoppm creates {prefix}-060.ppm or {prefix}-060.jpg
        candidates = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(f"{item_id}_p060") and f.endswith('.jpg')]
        if candidates:
            img_path = os.path.join(OUTPUT_DIR, candidates[0])
            with open(img_path, 'rb') as f:
                img_data = f.read()
            ext2, magic2 = detect_magic(img_data)
            if ext2:
                return img_data, ext2, f"PDF+RENDER:{magic2}", url
        # Check ppm output
        candidates_ppm = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(f"{item_id}_p060")]
        if candidates_ppm:
            return None, None, f"PDF_SAVED+PPM_RENDER:check_{candidates_ppm[0]}", url
    except FileNotFoundError:
        # pdftoppm not installed — try apt-get
        try:
            subprocess.run(["apt-get", "install", "-y", "poppler-utils"], capture_output=True, timeout=120)
            result = subprocess.run(
                ["pdftoppm", "-f", "60", "-l", "60", "-jpeg", "-r", "200", pdf_path, out_prefix],
                capture_output=True, timeout=60
            )
            candidates = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(f"{item_id}_p060") and f.endswith('.jpg')]
            if candidates:
                img_path = os.path.join(OUTPUT_DIR, candidates[0])
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                ext2, magic2 = detect_magic(img_data)
                if ext2:
                    return img_data, ext2, f"PDF+RENDER:{magic2}", url
        except:
            pass
        return None, "pdf", "MANUAL_RENDER", url
    except Exception as e:
        return None, "pdf", f"MANUAL_RENDER:{e}", url

    return None, "pdf", "MANUAL_RENDER", url

def handle_generic(item_id, url, extra_sleep=0):
    if extra_sleep:
        time.sleep(extra_sleep)
    html, final_url = fetch_url(url, extra_headers={"Accept": "text/html,application/xhtml+xml"})
    # Check if what we got is already an image
    ext, magic_name = detect_magic(html)
    if ext:
        return html, ext, magic_name, url

    img_url = extract_og_image(html)
    if not img_url:
        img_url = extract_first_large_img(html, final_url)
    if not img_url:
        return None, None, "NO_OG_IMAGE", None

    if not img_url.startswith('http'):
        from urllib.parse import urljoin
        img_url = urljoin(final_url, img_url)

    data, _ = fetch_url(img_url)
    ext, magic_name = detect_magic(data)
    if ext:
        return data, ext, magic_name, img_url
    return None, None, f"BAD_MAGIC:{magic_name}", img_url


def process_item(item_id, url):
    from urllib.parse import urlparse
    domain = urlparse(url).netloc

    print(f"  Processing {item_id} [{domain}] ...", end=" ", flush=True)

    try:
        if 'bildindex.de' in domain:
            data, ext, magic, img_url = handle_bildindex(item_id, url)
        elif 'britishmuseum.org' in domain:
            data, ext, magic, img_url = handle_britishmuseum(item_id, url)
            time.sleep(1.5)  # extra delay for BM
        elif 'bnportugal.gov.pt' in domain:
            data, ext, magic, img_url = handle_bnportugal(item_id, url)
        elif 'memoria.bn.br' in domain:
            data, ext, magic, img_url = handle_br007_pdf(item_id, url)
            if magic == "MANUAL_RENDER" or (magic and magic.startswith("PDF_SAVED")):
                size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f"{item_id}.pdf")) // 1024 if os.path.exists(os.path.join(OUTPUT_DIR, f"{item_id}.pdf")) else 0
                print(f"PDF_SAVED ({size_kb}KB) → {magic}")
                return {"id": item_id, "domain": domain, "status": "MANUAL_RENDER", "magic": "PDF", "size_kb": size_kb, "notes": f"PDF saved; {magic}"}
        else:
            data, ext, magic, img_url = handle_generic(item_id, url)

        if data and ext:
            out_path = os.path.join(OUTPUT_DIR, f"{item_id}.{ext}")
            with open(out_path, 'wb') as f:
                f.write(data)
            size_kb = len(data) // 1024
            print(f"OK {magic} ({size_kb}KB)")
            return {"id": item_id, "domain": domain, "status": "OK", "magic": magic, "size_kb": size_kb, "notes": img_url or url}
        else:
            # If BR-007 pdf was saved but no render
            if item_id == "BR-007" and os.path.exists(os.path.join(OUTPUT_DIR, f"{item_id}.pdf")):
                size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f"{item_id}.pdf")) // 1024
                print(f"PDF_ONLY ({size_kb}KB) → {magic}")
                return {"id": item_id, "domain": domain, "status": "MANUAL_RENDER", "magic": "PDF", "size_kb": size_kb, "notes": f"PDF saved; render failed: {magic}"}
            print(f"FAIL → {magic}")
            return {"id": item_id, "domain": domain, "status": "FAIL", "magic": magic or "UNKNOWN", "size_kb": 0, "notes": url}

    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        return {"id": item_id, "domain": domain, "status": f"HTTP_{e.code}", "magic": "-", "size_kb": 0, "notes": str(e)}
    except urllib.error.URLError as e:
        print(f"URL_ERR: {e.reason}")
        return {"id": item_id, "domain": domain, "status": "URL_ERROR", "magic": "-", "size_kb": 0, "notes": str(e.reason)}
    except Exception as e:
        print(f"ERR: {e}")
        return {"id": item_id, "domain": domain, "status": "ERROR", "magic": "-", "size_kb": 0, "notes": str(e)[:120]}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []

    for i, (item_id, url) in enumerate(BATCH2_ITEMS):
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        delay = 3.0 if 'britishmuseum' in domain else 1.5
        if i > 0:
            time.sleep(delay)
        result = process_item(item_id, url)
        results.append(result)

    return results


if __name__ == "__main__":
    print("=== Batch 2 Re-acquisition ===\n")
    results = main()

    ok = [r for r in results if r['status'] == 'OK']
    manual = [r for r in results if 'MANUAL' in r['status']]
    fail = [r for r in results if r['status'] not in ('OK',) and 'MANUAL' not in r['status']]

    print(f"\n=== Summary ===")
    print(f"OK:     {len(ok)}/33")
    print(f"Manual: {len(manual)}/33")
    print(f"Fail:   {len(fail)}/33")

    # Save JSON results for report generation
    with open(os.path.join(OUTPUT_DIR, "_batch2-results.json"), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {OUTPUT_DIR}/_batch2-results.json")
