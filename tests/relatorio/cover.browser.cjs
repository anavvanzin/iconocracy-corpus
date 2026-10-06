// Serve the repo, then run with Playwright installed:
// REPORT_URL=http://127.0.0.1:8765/relatorio/ node --test tests/relatorio/cover.browser.cjs
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const url = process.env.REPORT_URL || 'http://127.0.0.1:8765/relatorio/';
const launch = async () => {
  const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--no-zygote', '--in-process-gpu', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
});
  if (process.env.THREE_CACHE) {
    const original = browser.newPage.bind(browser);
    browser.newPage = async options => {
      const page = await original(options);
      await page.route('https://unpkg.com/three@0.184.0/**', route => route.fulfill({
        path: require('node:path').join(process.env.THREE_CACHE, new URL(route.request().url()).pathname.replace('/three@0.184.0/', '')),
        contentType: 'text/javascript', headers: {'access-control-allow-origin':'*'}
      }));
      return page;
    };
  }
  return browser;
};
const ready = page => page.waitForFunction(() => document.querySelector('.cover-3d').dataset.state === 'ready',null,{timeout:60000});
const scene = page => page.frames().find(f => f.url().includes('medalhao=1'));
async function counter(page) {
  await page.addInitScript(() => {
    window.drawCalls = 0;
    for (const type of [window.WebGLRenderingContext,window.WebGL2RenderingContext]) {
      if (!type) continue;
      for (const name of ['clear']) {
        const original = type.prototype[name];
        type.prototype[name] = function(...args) { window.drawCalls++; return original.apply(this,args); };
      }
    }
  });
}

test('desktop/tablet/mobile: scene has its own space, copy is legible, no overflow',async () => {
  const browser=await launch();
  try {
    const page=await browser.newPage({viewport:{width:1920,height:900},reducedMotion:'reduce'});
    const errors=[];page.on('pageerror', e=>errors.push(e.message));
    await page.goto(url,{waitUntil:'domcontentloaded'}); await ready(page);
    assert.match(await page.title(),/gramática alegórica/);
    assert.ok(await page.locator('h1').innerText());
    for (const width of [1920,1600,1510,1440,1280,1180,1100,1050,1024,800,768,390]) {
      await page.setViewportSize({width,height:900});
      const layout=await page.evaluate(() => {
        const medal=document.querySelector('.cover-3d'),copy=document.querySelector('.cover-inner');
        const a=medal.getBoundingClientRect(),b=copy.getBoundingClientRect();
        return {visible:getComputedStyle(medal).display!=='none',left:a.left,right:b.right,overflow:b.right>document.querySelector("#cover").getBoundingClientRect().right + 1};
      });
      assert.equal(layout.overflow,false,`overflow at ${width}`);
      if(layout.visible) assert.ok(layout.left-layout.right>=40,`overlap at ${width}`);
      if(width===1280 || width===800 || width===390) assert.equal(layout.visible,false);
      if(process.env.QA_SCREENSHOTS && [1920,1280,800,390].includes(width)) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/cover-${width}.png`});
    }
    assert.deepEqual(errors,[]);
  } finally {await browser.close();}
});

test('loading keeps fallback; WebGL, GLB, module failures and context loss restore it',async () => {
  const browser=await launch();
  try {
    for(const failure of ['webgl','glb','module','context']) {
      const page=await browser.newPage({viewport:{width:1920,height:900}});
      if(failure==='webgl') await page.addInitScript(() => {
        const original=HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext=function(type,...args) {
          return /webgl/.test(type) ? null : original.call(this,type,...args);
        };
      });
      if(failure==='glb') await page.route('**/metamorfose-alegorias.glb',route=>route.abort());
      if(failure==='module') await page.route('https://unpkg.com/**',route=>route.abort());
      await page.goto(url,{waitUntil:'domcontentloaded'});
      if(failure==='context') {
        await ready(page);
        await scene(page).evaluate(() => document.querySelector('canvas').dispatchEvent(new Event('webglcontextlost',{cancelable:true})));
      }
      await page.waitForFunction(()=>document.querySelector('.cover-3d').dataset.state==='error',null,{timeout:60000});
      assert.equal(await page.locator('.cover-3d').evaluate(el=>getComputedStyle(el).visibility),'hidden');
      assert.ok(await page.locator('#cover-canvas').evaluate(el=>el.width>0 && el.height>0));
      if(process.env.QA_SCREENSHOTS && failure==='webgl') await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/cover-webgl-failure.png`});
      await page.close();
    }
    // Hold model load: a wrapper/working WebGL context cannot count as readiness.
    const page=await browser.newPage({viewport:{width:1920,height:900}});
    let release; const gate=new Promise(resolve=>release=resolve);
    await page.route('**/metamorfose-alegorias.glb',async route=>{await gate;await route.continue();});
    await page.goto(url,{waitUntil:'domcontentloaded'});
    assert.equal(await page.locator('.cover-3d').evaluate(el=>getComputedStyle(el).visibility),'hidden');
    release();await ready(page);assert.equal(await page.locator('.cover-3d').evaluate(el=>getComputedStyle(el).visibility),'visible');
  } finally {await browser.close();}
});

test('cover GPU draws stop offscreen, resume on return; interlude is independent',async () => {
  const browser=await launch();
  try {
    const page=await browser.newPage({viewport:{width:1920,height:900}});await counter(page);
    await page.goto(url,{waitUntil:'domcontentloaded'});await ready(page);const cover=scene(page);
    await page.waitForTimeout(350);const active=await cover.evaluate(()=>drawCalls);
    await cover.waitForFunction(n=>drawCalls>n,active,{timeout:15000});
    await page.locator('.vitrine-frame').scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);const paused=await cover.evaluate(()=>drawCalls);
    await page.waitForTimeout(500);assert.equal(await cover.evaluate(()=>drawCalls),paused);
    const interlude=page.frames().find(f=>f.url().endsWith('/metamorfose/embed.html'));
    await interlude.waitForFunction(()=>drawCalls>0,null,{timeout:60000});
    const n=await interlude.evaluate(()=>drawCalls);await interlude.waitForFunction(n=>drawCalls>n,n,{timeout:15000});
    await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(1500);
    assert.ok(await cover.evaluate(()=>drawCalls)>paused);
    const other=await interlude.evaluate(()=>drawCalls);await page.waitForTimeout(500);assert.equal(await interlude.evaluate(()=>drawCalls),other);
    await page.setViewportSize({width:800,height:900});await page.waitForTimeout(500);
    const hidden=await cover.evaluate(()=>drawCalls);await page.waitForTimeout(350);assert.equal(await cover.evaluate(()=>drawCalls),hidden);
  } finally {await browser.close();}
});
