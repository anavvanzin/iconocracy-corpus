#!/usr/bin/env python3
"""Download images from Library of Congress JSON API for ICONOCRACY corpus.

Uses a subprocess call to a Node.js/Playwright helper that passes Cloudflare,
fetches JSON metadata, and returns image URLs. Then downloads images via the
same browser context.

Falls back to direct urllib if Cloudflare is not active.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

BASE_DIR = "/Users/ana/Research/hub/iconocracy-corpus/data/raw"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "ICONOCRACY-Corpus/1.0 (PPGD/UFSC)"

COUNTRY_MAP = {
    "AT": "DE",
    "DE": "DE",
    "IT": "FR",
    "MX": "BR",
    "US": "US",
}

ITEMS = [
    ("AT-001", "https://www.loc.gov/item/2004666193/"),
    ("DE-014", "https://www.loc.gov/item/2004665855/"),
    ("IT-005", "https://www.loc.gov/item/2004666216/"),
    ("MX-001", "https://www.loc.gov/item/2003656173/"),
    ("US-001", "https://www.loc.gov/item/2004673327/"),
    ("US-002", "https://www.loc.gov/item/2009631377/"),
    ("US-003", "https://www.loc.gov/item/2007675578/"),
    ("US-004", "https://www.loc.gov/item/99613542/"),
    ("US-005", "https://www.loc.gov/item/2004676797/"),
    ("US-006", "https://www.loc.gov/item/2004673370/"),
    ("US-007", "https://www.loc.gov/item/2018697020/"),
    ("US-008", "https://www.loc.gov/item/97510759/"),
    ("US-009", "https://www.loc.gov/item/2018664118/"),
    ("US-010", "https://www.loc.gov/item/2008661765/"),
    ("US-011", "https://www.loc.gov/item/91726511/"),
    ("US-012", "https://www.loc.gov/item/95506508/"),
    ("US-016", "https://www.loc.gov/item/91726511/"),
    ("US-017", "https://www.loc.gov/item/95506508/"),
    ("US-018", "https://www.loc.gov/item/2002708939/"),
    ("US-019", "https://www.loc.gov/item/2004679037/"),
    ("US-BANNER-1861", "https://www.loc.gov/item/91721286/"),
    ("US-NAST-1864", "https://www.loc.gov/item/2022631575/"),
]

downloaded_cache = {}


def get_folder(item_id):
    prefix = item_id.split("-")[0]
    return COUNTRY_MAP.get(prefix, "US")


def find_image_url(data):
    """Extract best image URL from LOC JSON response."""
    # Strategy 1: item.image_url
    try:
        image_urls = data.get("item", {}).get("image_url", [])
        if image_urls:
            for url in image_urls:
                if isinstance(url, str) and ("jpg" in url.lower() or "tif" in url.lower()):
                    return url
            return image_urls[0]
    except (KeyError, IndexError, TypeError):
        pass

    # Strategy 2: resources[0].image
    try:
        resources = data.get("resources", [])
        if resources:
            img = resources[0].get("image", "")
            if img:
                return img
    except (KeyError, IndexError, TypeError):
        pass

    # Strategy 3: resources[0].files -- pick largest
    try:
        resources = data.get("resources", [])
        if resources:
            files = resources[0].get("files", [])
            if files and files[0]:
                file_list = files[0]
                if isinstance(file_list, list) and file_list:
                    best = None
                    best_size = 0
                    for f in file_list:
                        if isinstance(f, dict):
                            url = f.get("url", "")
                            size = f.get("size", 0) or f.get("width", 0) or 0
                            if url and size > best_size:
                                best = url
                                best_size = size
                    if best:
                        return best
                    for f in file_list:
                        if isinstance(f, dict) and f.get("url"):
                            return f["url"]
    except (KeyError, IndexError, TypeError):
        pass

    return None


def normalize_url(url):
    if url.startswith("//"):
        return "https:" + url
    if not url.startswith("http"):
        return "https://www.loc.gov" + url
    return url


def write_node_helper(items_file, output_dir):
    """Write a Node.js script that uses Playwright to fetch JSON + download images."""
    node_script = os.path.join(SCRIPT_DIR, "_loc_pw_helper.mjs")
    content = r"""
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const itemsFile = process.argv[2];
const outputDir = process.argv[3];
const items = JSON.parse(readFileSync(itemsFile, 'utf-8'));

mkdirSync(outputDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });
  const page = await context.newPage();

  // Warm up: pass Cloudflare challenge
  console.log('Warming up: passing Cloudflare challenge on loc.gov...');
  await page.goto('https://www.loc.gov/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(5000);
  console.log('Page title:', await page.title());

  const results = [];

  for (const { item_id, loc_url, dest_path } of items) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`[${item_id}] ${loc_url}`);

    const apiUrl = loc_url.replace(/\/$/, '') + '/?fo=json';
    let jsonData = null;

    // Fetch JSON
    try {
      console.log(`  Fetching JSON: ${apiUrl}`);
      const resp = await page.goto(apiUrl, { waitUntil: 'networkidle', timeout: 30000 });
      if (resp && resp.status() === 200) {
        const bodyText = await resp.text();
        jsonData = JSON.parse(bodyText);
      } else {
        const status = resp ? resp.status() : 'no response';
        console.log(`  HTTP ${status}`);
        results.push({ item_id, status: 'fail', reason: `HTTP ${status}` });
        continue;
      }
    } catch (e) {
      console.log(`  JSON FETCH ERROR: ${e.message}`);
      results.push({ item_id, status: 'fail', reason: `JSON: ${e.message}` });
      await page.waitForTimeout(2000);
      continue;
    }

    // Write JSON to output dir for Python to parse image URLs
    const jsonPath = join(outputDir, `${item_id}.json`);
    writeFileSync(jsonPath, JSON.stringify(jsonData));

    // Find image URL
    let imageUrl = null;
    try {
      const imageUrls = jsonData?.item?.image_url || [];
      for (const u of imageUrls) {
        if (typeof u === 'string' && (u.toLowerCase().includes('jpg') || u.toLowerCase().includes('tif'))) {
          imageUrl = u;
          break;
        }
      }
      if (!imageUrl && imageUrls.length > 0) imageUrl = imageUrls[0];
    } catch {}

    if (!imageUrl) {
      try {
        const resources = jsonData?.resources || [];
        if (resources.length > 0) imageUrl = resources[0]?.image || null;
      } catch {}
    }

    if (!imageUrl) {
      try {
        const files = jsonData?.resources?.[0]?.files?.[0] || [];
        if (files.length > 0) {
          let best = null, bestSize = 0;
          for (const f of files) {
            const sz = f.size || f.width || 0;
            if (f.url && sz > bestSize) { best = f.url; bestSize = sz; }
          }
          imageUrl = best || files.find(f => f.url)?.url || null;
        }
      } catch {}
    }

    if (!imageUrl) {
      console.log(`  NO IMAGE URL found`);
      results.push({ item_id, status: 'fail', reason: 'no image URL' });
      continue;
    }

    // Normalize URL
    if (imageUrl.startsWith('//')) imageUrl = 'https:' + imageUrl;
    else if (!imageUrl.startsWith('http')) imageUrl = 'https://www.loc.gov' + imageUrl;

    console.log(`  Image URL: ${imageUrl.slice(0, 120)}...`);

    // Download image
    try {
      const imgResp = await page.goto(imageUrl, { waitUntil: 'load', timeout: 60000 });
      if (imgResp && imgResp.status() === 200) {
        const imgBytes = await imgResp.body();
        writeFileSync(dest_path, imgBytes);
        const sizeKB = (imgBytes.length / 1024).toFixed(1);
        console.log(`  OK -> ${dest_path} (${sizeKB} KB)`);
        results.push({ item_id, status: 'ok', size_kb: parseFloat(sizeKB) });
      } else {
        const status = imgResp ? imgResp.status() : 'no response';
        console.log(`  IMAGE HTTP ${status}`);
        results.push({ item_id, status: 'fail', reason: `image HTTP ${status}` });
      }
    } catch (e) {
      console.log(`  IMAGE ERROR: ${e.message}`);
      results.push({ item_id, status: 'fail', reason: `image: ${e.message}` });
    }

    await page.waitForTimeout(1500);
  }

  await browser.close();

  // Write results
  writeFileSync(join(outputDir, '_results.json'), JSON.stringify(results, null, 2));
  console.log(`\nDone. Results written to ${join(outputDir, '_results.json')}`);
})();
""".strip()

    with open(node_script, "w") as f:
        f.write(content)
    return node_script


def main():
    results = {"ok": [], "fail": [], "copy": []}

    # Prepare unique items (skip duplicates for download, copy later)
    unique_items = []
    dup_map = {}  # item_id -> source item_id (for copies)
    seen_urls = {}  # loc_url -> item_id

    for item_id, loc_url in ITEMS:
        if loc_url in seen_urls:
            dup_map[item_id] = (seen_urls[loc_url], loc_url)
        else:
            seen_urls[loc_url] = item_id
            unique_items.append((item_id, loc_url))

    # Prepare items file for the Node helper
    tmpdir = tempfile.mkdtemp(prefix="loc_dl_")
    pw_items = []
    for item_id, loc_url in unique_items:
        folder = get_folder(item_id)
        dest_dir = os.path.join(BASE_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, f"{item_id}.jpg")
        pw_items.append({
            "item_id": item_id,
            "loc_url": loc_url,
            "dest_path": dest_path,
        })

    items_file = os.path.join(tmpdir, "items.json")
    with open(items_file, "w") as f:
        json.dump(pw_items, f)

    # Write and run Node helper
    node_script = write_node_helper(items_file, tmpdir)
    print(f"Running Playwright via Node.js ({len(unique_items)} unique items)...")
    print(f"  Duplicates to copy later: {list(dup_map.keys())}\n")

    proc = subprocess.run(
        ["npx", "playwright", "test", "--config=/dev/null", node_script],
        capture_output=False,
        cwd=SCRIPT_DIR,
    )

    # If npx playwright test doesn't work for .mjs, fall back to node directly
    # But we need the playwright module path. Let's just use node directly.
    # Actually, let's run it as a plain node script since playwright is available via npx.

    # Try running with node directly using the npx-installed playwright
    proc = subprocess.run(
        ["node", node_script, items_file, tmpdir],
        capture_output=False,
        cwd=SCRIPT_DIR,
        timeout=600,
    )

    # Read results
    results_file = os.path.join(tmpdir, "_results.json")
    if os.path.exists(results_file):
        with open(results_file) as f:
            pw_results = json.load(f)
        for r in pw_results:
            if r["status"] == "ok":
                results["ok"].append(r["item_id"])
            else:
                results["fail"].append((r["item_id"], r.get("reason", "unknown")))
    else:
        print("WARNING: No results file found from Playwright helper")
        for item in pw_items:
            if os.path.exists(item["dest_path"]) and os.path.getsize(item["dest_path"]) > 1000:
                results["ok"].append(item["item_id"])
            else:
                results["fail"].append((item["item_id"], "no result"))

    # Handle duplicate copies
    for dup_id, (src_id, loc_url) in dup_map.items():
        src_folder = get_folder(src_id)
        src_path = os.path.join(BASE_DIR, src_folder, f"{src_id}.jpg")
        dup_folder = get_folder(dup_id)
        dup_dir = os.path.join(BASE_DIR, dup_folder)
        os.makedirs(dup_dir, exist_ok=True)
        dup_path = os.path.join(dup_dir, f"{dup_id}.jpg")

        if os.path.exists(src_path) and os.path.getsize(src_path) > 1000:
            shutil.copy2(src_path, dup_path)
            size_kb = os.path.getsize(dup_path) / 1024
            print(f"  COPIED {src_id} -> {dup_id} ({size_kb:.1f} KB)")
            results["copy"].append(dup_id)
        else:
            print(f"  Cannot copy {src_id} -> {dup_id}: source missing or empty")
            results["fail"].append((dup_id, f"source {src_id} missing"))

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Downloaded: {len(results['ok'])} items")
    print(f"  Copied (duplicates): {len(results['copy'])} items")
    print(f"  Failed: {len(results['fail'])} items")
    if results["ok"]:
        print(f"\n  OK: {', '.join(results['ok'])}")
    if results["copy"]:
        print(f"  Copies: {', '.join(results['copy'])}")
    if results["fail"]:
        print(f"\n  FAILURES:")
        for item_id, reason in results["fail"]:
            print(f"    {item_id}: {reason}")

    # Cleanup
    try:
        os.unlink(node_script)
    except OSError:
        pass

    return 0 if not results["fail"] else 1


if __name__ == "__main__":
    sys.exit(main())
