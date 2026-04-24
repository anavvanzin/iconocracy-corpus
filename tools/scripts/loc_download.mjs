#!/usr/bin/env node
/**
 * Download images from Library of Congress JSON API for ICONOCRACY corpus.
 *
 * Launches real Google Chrome with remote debugging, connects via CDP.
 * Real Chrome passes Cloudflare Turnstile. Uses page.goto() for both
 * JSON and image downloads (not fetch()) to avoid CORS issues.
 *
 * Usage: node tools/scripts/loc_download.mjs
 */

import { chromium } from 'playwright';
import { writeFileSync, copyFileSync, existsSync, mkdirSync, statSync } from 'fs';
import { join } from 'path';
import { execSync, spawn } from 'child_process';

const BASE_DIR = '/Users/ana/Research/hub/iconocracy-corpus/data/raw';
const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const DEBUG_PORT = 9234;
const TEMP_PROFILE = '/tmp/chrome-loc-download';

const COUNTRY_MAP = {
  AT: 'DE', DE: 'DE', IT: 'FR', MX: 'BR', US: 'US',
};

const ITEMS = [
  ['AT-001',          'https://www.loc.gov/item/2004666193/'],
  ['DE-014',          'https://www.loc.gov/item/2004665855/'],
  ['IT-005',          'https://www.loc.gov/item/2004666216/'],
  ['MX-001',          'https://www.loc.gov/item/2003656173/'],
  ['US-001',          'https://www.loc.gov/item/2004673327/'],
  ['US-002',          'https://www.loc.gov/item/2009631377/'],
  ['US-003',          'https://www.loc.gov/item/2007675578/'],
  ['US-004',          'https://www.loc.gov/item/99613542/'],
  ['US-005',          'https://www.loc.gov/item/2004676797/'],
  ['US-006',          'https://www.loc.gov/item/2004673370/'],
  ['US-007',          'https://www.loc.gov/item/2018697020/'],
  ['US-008',          'https://www.loc.gov/item/97510759/'],
  ['US-009',          'https://www.loc.gov/item/2018664118/'],
  ['US-010',          'https://www.loc.gov/item/2008661765/'],
  ['US-011',          'https://www.loc.gov/item/91726511/'],
  ['US-012',          'https://www.loc.gov/item/95506508/'],
  ['US-016',          'https://www.loc.gov/item/91726511/'],
  ['US-017',          'https://www.loc.gov/item/95506508/'],
  ['US-018',          'https://www.loc.gov/item/2002708939/'],
  ['US-019',          'https://www.loc.gov/item/2004679037/'],
  ['US-BANNER-1861',  'https://www.loc.gov/item/91721286/'],
  ['US-NAST-1864',    'https://www.loc.gov/item/2022631575/'],
];

function getFolder(itemId) {
  const prefix = itemId.split('-')[0];
  return COUNTRY_MAP[prefix] || 'US';
}

function normalizeUrl(url) {
  if (url.startsWith('//')) return 'https:' + url;
  if (!url.startsWith('http')) return 'https://www.loc.gov' + url;
  return url;
}

/**
 * Upgrade a 150px thumbnail URL to the largest available version.
 * LOC pattern: ...3g11952_150px.jpg -> ...3g11952r.jpg (full resolution)
 * Also strips the hash fragment.
 */
function upgradeImageUrl(url) {
  // Strip hash fragment
  url = url.split('#')[0];
  // Replace _150px suffix with r (reproduction) suffix for full-size
  url = url.replace(/_150px\.jpg$/i, 'r.jpg');
  return url;
}

function findImageUrl(data) {
  // Strategy 1: item.image_url -- look for full-size URLs
  try {
    const urls = data?.item?.image_url || [];
    // Prefer URLs that don't have _150px (full size)
    for (const u of urls) {
      if (typeof u === 'string' && !u.includes('_150px') && (u.includes('jpg') || u.includes('tif'))) {
        return u;
      }
    }
    // Fall back to any image URL (will be upgraded later)
    for (const u of urls) {
      if (typeof u === 'string' && (u.toLowerCase().includes('jpg') || u.toLowerCase().includes('tif'))) {
        return u;
      }
    }
    if (urls.length > 0 && typeof urls[0] === 'string') return urls[0];
  } catch {}

  // Strategy 2: resources[0].files -- pick largest resolution
  try {
    const resources = data?.resources || [];
    if (resources.length > 0) {
      const allFiles = resources[0]?.files || [];
      // allFiles is array of arrays: [[{url, mimetype, size, width, height}, ...], ...]
      for (const pageFiles of allFiles) {
        if (!Array.isArray(pageFiles)) continue;
        let best = null, bestSize = 0;
        for (const f of pageFiles) {
          if (f && f.url && f.mimetype && f.mimetype.includes('image')) {
            const sz = (f.width || 0) * (f.height || 0) || f.size || 0;
            if (sz > bestSize) { best = f.url; bestSize = sz; }
          }
        }
        if (best) return best;
        // Fallback: first image file
        const first = pageFiles.find(f => f?.url && f?.mimetype?.includes('image'));
        if (first) return first.url;
      }
    }
  } catch {}

  // Strategy 3: resources[0].image
  try {
    const img = data?.resources?.[0]?.image;
    if (img) return img;
  } catch {}

  return null;
}

async function waitForCfClear(page, maxWaitMs = 45000) {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    const title = await page.title();
    if (title && !title.toLowerCase().includes('just a moment') && !title.toLowerCase().includes('attention') && !title.toLowerCase().includes('checking')) {
      return true;
    }
    await page.waitForTimeout(2000);
  }
  return false;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  const results = { ok: [], fail: [], copy: [] };

  // Deduplicate
  const seenUrls = {};
  const uniqueItems = [];
  const dupItems = [];

  for (const [itemId, locUrl] of ITEMS) {
    if (seenUrls[locUrl]) {
      dupItems.push({ itemId, srcItemId: seenUrls[locUrl], locUrl });
    } else {
      seenUrls[locUrl] = itemId;
      uniqueItems.push([itemId, locUrl]);
    }
  }

  console.log(`Items: ${ITEMS.length} total, ${uniqueItems.length} unique, ${dupItems.length} duplicates`);
  console.log(`Duplicates: ${dupItems.map(d => `${d.itemId} (= ${d.srcItemId})`).join(', ')}\n`);

  // Kill any leftover Chrome on our debug port
  try { execSync(`pkill -f "remote-debugging-port=${DEBUG_PORT}" 2>/dev/null`); } catch {}
  await sleep(1000);

  // Launch real Chrome
  console.log('Launching Google Chrome with remote debugging...');
  mkdirSync(TEMP_PROFILE, { recursive: true });

  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${DEBUG_PORT}`,
    `--user-data-dir=${TEMP_PROFILE}`,
    '--no-first-run',
    '--no-default-browser-check',
    'about:blank',
  ], { detached: true, stdio: 'ignore' });
  chromeProc.unref();

  // Wait for Chrome
  let wsEndpoint = null;
  for (let i = 0; i < 20; i++) {
    await sleep(1000);
    try {
      const resp = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
      const data = await resp.json();
      wsEndpoint = data.webSocketDebuggerUrl;
      if (wsEndpoint) break;
    } catch {}
  }

  if (!wsEndpoint) {
    console.error('ERROR: Could not connect to Chrome.');
    process.exit(1);
  }
  console.log(`Connected via CDP.\n`);

  const browser = await chromium.connectOverCDP(wsEndpoint);
  const context = browser.contexts()[0] || await browser.newContext();
  const page = context.pages()[0] || await context.newPage();

  // Solve Cloudflare on loc.gov
  console.log('Step 0: Solving Cloudflare on loc.gov...');
  await page.goto('https://www.loc.gov/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  const cleared = await waitForCfClear(page, 45000);
  console.log(`  Title: "${await page.title()}" (cleared: ${cleared})`);

  if (!cleared) {
    console.log('  Waiting 15 more seconds for manual solve...');
    await page.waitForTimeout(15000);
  }

  // Also warm up tile.loc.gov (separate CF domain)
  console.log('  Warming up tile.loc.gov...');
  await page.goto('https://tile.loc.gov/', { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
  await waitForCfClear(page, 20000);
  console.log(`  tile.loc.gov title: "${await page.title()}"\n`);

  // Now process each item using page.goto() for navigation
  for (const [itemId, locUrl] of uniqueItems) {
    const folder = getFolder(itemId);
    const destDir = join(BASE_DIR, folder);
    mkdirSync(destDir, { recursive: true });
    const destPath = join(destDir, `${itemId}.jpg`);

    console.log('='.repeat(60));
    console.log(`[${itemId}] ${locUrl}`);

    // Step 1: Fetch JSON via page navigation
    const apiUrl = locUrl.replace(/\/$/, '') + '/?fo=json';
    let jsonData = null;

    try {
      console.log(`  Fetching JSON...`);
      const resp = await page.goto(apiUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
      if (resp && resp.status() === 200) {
        const bodyText = await resp.text();
        try {
          jsonData = JSON.parse(bodyText);
        } catch {
          // Page might have rendered JSON inside HTML
          const text = await page.innerText('body');
          jsonData = JSON.parse(text);
        }
      } else {
        const status = resp ? resp.status() : 'no response';
        // Might be CF challenge page
        if (status === 403) {
          console.log(`  Got 403, waiting for CF to clear...`);
          await waitForCfClear(page, 20000);
          // Retry
          const resp2 = await page.goto(apiUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
          if (resp2 && resp2.status() === 200) {
            jsonData = JSON.parse(await resp2.text());
          } else {
            results.fail.push([itemId, `HTTP ${resp2?.status() || 'none'}`]);
            continue;
          }
        } else {
          results.fail.push([itemId, `HTTP ${status}`]);
          continue;
        }
      }
    } catch (e) {
      console.log(`  JSON ERROR: ${e.message}`);
      results.fail.push([itemId, `JSON: ${e.message}`]);
      continue;
    }

    // Step 2: Find and upgrade image URL
    let imageUrl = findImageUrl(jsonData);
    if (!imageUrl) {
      console.log(`  NO IMAGE URL.`);
      results.fail.push([itemId, 'no image URL']);
      continue;
    }

    imageUrl = normalizeUrl(imageUrl);
    imageUrl = upgradeImageUrl(imageUrl);
    console.log(`  Image: ${imageUrl.slice(0, 120)}`);

    // Step 3: Download image via page.goto()
    try {
      const imgResp = await page.goto(imageUrl, { waitUntil: 'load', timeout: 60000 });
      if (imgResp && imgResp.status() === 200) {
        const imgBytes = await imgResp.body();
        // Verify it's actually image data (not HTML challenge page)
        if (imgBytes.length > 5000 && imgBytes[0] !== 0x3C) { // Not starting with '<' (HTML)
          writeFileSync(destPath, imgBytes);
          const sizeKB = (imgBytes.length / 1024).toFixed(1);
          console.log(`  OK -> ${destPath} (${sizeKB} KB)`);
          results.ok.push(itemId);
        } else if (imgBytes.length > 1000) {
          // Might be CF challenge, wait and retry
          console.log(`  Got HTML instead of image, waiting for CF...`);
          await waitForCfClear(page, 15000);
          const retry = await page.goto(imageUrl, { waitUntil: 'load', timeout: 60000 });
          if (retry && retry.status() === 200) {
            const retryBytes = await retry.body();
            if (retryBytes.length > 5000 && retryBytes[0] !== 0x3C) {
              writeFileSync(destPath, retryBytes);
              const sizeKB = (retryBytes.length / 1024).toFixed(1);
              console.log(`  OK (retry) -> ${destPath} (${sizeKB} KB)`);
              results.ok.push(itemId);
            } else {
              console.log(`  Still got HTML after retry`);
              results.fail.push([itemId, 'CF challenge on image']);
            }
          } else {
            results.fail.push([itemId, `image retry HTTP ${retry?.status()}`]);
          }
        } else {
          console.log(`  Image too small (${imgBytes.length} bytes)`);
          results.fail.push([itemId, 'image too small']);
        }
      } else {
        const status = imgResp ? imgResp.status() : 'no response';
        console.log(`  IMAGE HTTP ${status}`);
        // Try CF clear and retry if 403
        if (status === 403) {
          await waitForCfClear(page, 15000);
          const retry = await page.goto(imageUrl, { waitUntil: 'load', timeout: 60000 });
          if (retry && retry.status() === 200) {
            const retryBytes = await retry.body();
            writeFileSync(destPath, retryBytes);
            const sizeKB = (retryBytes.length / 1024).toFixed(1);
            console.log(`  OK (retry) -> ${destPath} (${sizeKB} KB)`);
            results.ok.push(itemId);
          } else {
            results.fail.push([itemId, `image HTTP ${status}`]);
          }
        } else {
          results.fail.push([itemId, `image HTTP ${status}`]);
        }
      }
    } catch (e) {
      console.log(`  IMAGE ERROR: ${e.message}`);
      results.fail.push([itemId, `image: ${e.message}`]);
    }

    await page.waitForTimeout(1500);
  }

  // Disconnect
  browser.close();
  try { process.kill(chromeProc.pid); } catch {}
  try { execSync(`pkill -f "remote-debugging-port=${DEBUG_PORT}"`); } catch {}

  // Duplicate copies
  console.log('\n' + '='.repeat(60));
  console.log('DUPLICATE COPIES');
  for (const { itemId, srcItemId } of dupItems) {
    const srcFolder = getFolder(srcItemId);
    const srcPath = join(BASE_DIR, srcFolder, `${srcItemId}.jpg`);
    const dstFolder = getFolder(itemId);
    const dstDir = join(BASE_DIR, dstFolder);
    mkdirSync(dstDir, { recursive: true });
    const dstPath = join(dstDir, `${itemId}.jpg`);

    if (existsSync(srcPath) && statSync(srcPath).size > 1000) {
      copyFileSync(srcPath, dstPath);
      const sizeKB = (statSync(dstPath).size / 1024).toFixed(1);
      console.log(`  ${srcItemId} -> ${itemId} (${sizeKB} KB)`);
      results.copy.push(itemId);
    } else {
      console.log(`  Cannot copy ${srcItemId} -> ${itemId}: source missing`);
      results.fail.push([itemId, `source ${srcItemId} missing`]);
    }
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('SUMMARY');
  console.log('='.repeat(60));
  console.log(`  Downloaded: ${results.ok.length}`);
  console.log(`  Copied (dups): ${results.copy.length}`);
  console.log(`  Failed: ${results.fail.length}`);
  if (results.ok.length) console.log(`\n  OK: ${results.ok.join(', ')}`);
  if (results.copy.length) console.log(`  Copies: ${results.copy.join(', ')}`);
  if (results.fail.length) {
    console.log(`\n  FAILURES:`);
    for (const [id, reason] of results.fail) console.log(`    ${id}: ${reason}`);
  }

  process.exit(results.fail.length > 0 ? 1 : 0);
})();
