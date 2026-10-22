// Serve the repo, then run: node --test tests/relatorio/mobile.browser.cjs
// Browser dependencies stay outside the report (see report-mobile.yml).
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const path = require('node:path');
const url = process.env.REPORT_URL || 'http://127.0.0.1:8765/relatorio/';
async function launch() {
  return chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--no-zygote', '--in-process-gpu', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
}
async function open(browser, width) {
  const page = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce', isMobile: width < 768, hasTouch: width < 768});
  // Exercise the real WebGL-unavailable fallback; #233's separate suite covers
  // rendered GLB readiness and GPU suspension. Avoid software GPU work obscuring
  // layout checks when scrolling through both full-page model embeds.
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, ...args) {
      return /webgl/.test(type) ? null : original.call(this, type, ...args);
    };
  });
  if (process.env.THREE_CACHE) await page.route('https://unpkg.com/three@0.184.0/**', route => route.fulfill({
    path: path.join(process.env.THREE_CACHE, new URL(route.request().url()).pathname.replace('/three@0.184.0/', '')),
    contentType: 'text/javascript', headers: {'access-control-allow-origin': '*'}
  }));
  await page.goto(url, {waitUntil: 'networkidle'});
  await page.evaluate(() => document.fonts.ready);
  await page.locator('#source-list .src-row').last().waitFor({state: 'attached'});
  return page;
}
async function pageFits(page, state) {
  const size = await page.evaluate(() => ({viewport: document.documentElement.clientWidth,
    document: document.documentElement.scrollWidth, body: document.body.scrollWidth}));
  assert.ok(size.document <= size.viewport + 1 && size.body <= size.viewport + 1, `${state}: ${JSON.stringify(size)}`);
}
async function boxFits(locator, page, state) {
  const box = await locator.boundingBox();
  assert.ok(box && box.x >= 0 && box.x + box.width <= page.viewportSize().width + 1, `${state}: ${JSON.stringify(box)}`);
}

test('complete report fits viewport before and after visiting every section', async () => {
  const browser = await launch();
  try {
    for (const width of [320,360,390,430,768,800,1024,1180,1280,1440,1920]) {
      const page = await open(browser, width);
      assert.match(await page.title(), /gramática alegórica/);
      assert.ok(await page.locator('main h2').first().innerText());
      await pageFits(page, `initial ${width}`);
      assert.match(await page.locator('.cover-anchor').innerText(), /histórico.*28\/09\/2026/);
      assert.match(await page.locator('#stat-row .stat').first().innerText(), /336.*28\/09\/2026/s);
      const snapshot = page.locator('#corpus-snapshot');
      await snapshot.scrollIntoViewIfNeeded();
      assert.match(await snapshot.innerText(), /337 registros/);
      await boxFits(snapshot, page, `snapshot note ${width}`);
      await page.locator('#stat-row .stat').first().click();
      const detail = page.locator('#drill-card');
      await detail.waitFor({state:'visible'});
      assert.match(await detail.locator('.d-sub').innerText(), /28\/09\/2026/);
      await boxFits(detail, page, `snapshot detail ${width}`);
      await page.keyboard.press('Escape');
      for (const section of await page.locator('main section, .colophon').all()) {
        await section.evaluate(el => el.scrollIntoView());
        await pageFits(page, `${width} ${await section.getAttribute('id') || 'footer'}`);
      }
      if (process.env.QA_SCREENSHOTS && [320,390,1440].includes(width)) {
        await page.locator('#sec-matrix').scrollIntoViewIfNeeded();
        await page.screenshot({path: `${process.env.QA_SCREENSHOTS}/matrix-${width}.png`});
      }
      await page.close();
    }
  } finally {await browser.close();}
});

test('mobile matrix remains fully reachable and detail card fits on open and resize', async () => {
  const browser = await launch();
  try {
    for (const width of [320,390]) {
      const page = await open(browser, width);
      const region = page.getByRole('region', {name: 'Matriz de distribuição de gênero'});
      await region.scrollIntoViewIfNeeded();
      await boxFits(region, page, `matrix region ${width}`);
      await region.focus();
      assert.equal(await region.evaluate(el => el === document.activeElement), true);
      await page.keyboard.press('ArrowRight');
      await page.waitForFunction(() => document.querySelector('.table-scroll').scrollLeft > 0);
      await pageFits(page, 'keyboard scroll stays local');
      // Scroll to the far edge and verify the last column can be read in full.
      const scroll = await region.evaluate(el => {
        el.scrollLeft = el.scrollWidth;
        return {left: el.scrollLeft, max: el.scrollWidth - el.clientWidth};
      });
      assert.ok(scroll.max > 0 && scroll.left >= scroll.max - 1);
      await boxFits(page.locator('.mtx tbody tr').last().locator('td').last(), page, 'last matrix cell');
      const cell = page.locator('.mtx .cell').last();
      await cell.focus();
      await page.keyboard.press('Enter');
      const drill = page.locator('#drill-card');
      await drill.waitFor({state: 'visible'});
      assert.ok(await drill.locator('.d-sub').innerText());
      await boxFits(drill, page, `drill ${width}`);
      await pageFits(page, `open drill ${width}`);
      await page.setViewportSize({width: width === 320 ? 390 : 320, height:900});
      await page.waitForFunction(() => {
        const r = document.querySelector('#drill-card').getBoundingClientRect();
        return r.left >= 0 && r.right <= document.documentElement.clientWidth + 1;
      });
      await boxFits(drill, page, 'resized open drill');
      await pageFits(page, 'resized open drill');
      // Rotation/short viewports also change height and text wrapping.
      await page.setViewportSize({width:320, height:180});
      await page.waitForFunction(() => {
        const r = document.querySelector('#drill-card').getBoundingClientRect();
        return r.top >= 8 && r.bottom <= innerHeight - 7;
      }, null, {timeout:3000});
      await drill.evaluate(el => { el.scrollTop = el.scrollHeight; });
      const source = await drill.locator('.d-src').boundingBox();
      assert.ok(source && source.y >= 8 && source.y + source.height <= 173,
        `detail source remains readable in short viewport: ${JSON.stringify(source)}`);
      await page.keyboard.press('Escape');
      await drill.waitFor({state:'hidden'});
      await page.close();
    }
  } finally {await browser.close();}
});

test('cover navigation reaches sources without horizontal scroll', async () => {
  const browser = await launch();
  try {
    const page = await open(browser, 390);
    await page.getByRole('button', {name:'Fontes', exact:true}).click();
    await page.waitForFunction(() => Math.abs(document.querySelector('#sec-sources').getBoundingClientRect().top) < 2);
    const link = page.locator('#source-list a').last();
    assert.match(await link.getAttribute('href'), /eae4c3a0a524eca6f1c4863c2d6fc21959f9435b/);
    await link.focus();
    assert.equal(await link.evaluate(el => el === document.activeElement), true);
    await boxFits(link, page, 'source link');
    await pageFits(page, 'sources navigation');
    await page.close();
  } finally {await browser.close();}
});
