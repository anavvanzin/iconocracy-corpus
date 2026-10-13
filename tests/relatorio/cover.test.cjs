// Run: node --test tests/relatorio/cover.test.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');

test('Iustitia remains until authenticated scene readiness; returns on error and narrow layouts', () => {
  const events = {};
  const medal = { dataset: { state: 'loading' } };
  let display = 'block';
  let blindfolds = 0;
  const ctx = new Proxy({}, { get: (o, k) => o[k] || (k === 'createLinearGradient' ? () => ({addColorStop(){}}) : k === 'fillRect' ? () => { if (o.fillStyle === 'red') blindfolds++; } : () => {}), set: (o,k,v) => (o[k]=v,true) });
  const context = {
    document: {getElementById: () => ({}), querySelector: () => medal},
    getComputedStyle: () => ({display}), addEventListener: (k, fn) => events[k] = fn,
    requestAnimationFrame: fn => fn(0),
    U: {bindCanvas: () => ({fit: () => ({w:1100,h:900}),ctx}), PAL: {lacre:'red'}, REDUCE:true, TAU:Math.PI*2,clamp:(n,a,b)=>Math.max(a,Math.min(b,n))}
  };
  vm.runInNewContext(read('relatorio/js/cover.js'),context);
  assert.ok(blindfolds > 0);
  medal.dataset.state = 'ready'; blindfolds = 0; events.cover3dstate(); assert.equal(blindfolds,0);
  medal.dataset.state = 'error'; events.cover3dstate(); assert.ok(blindfolds > 0);
  medal.dataset.state = 'ready'; display='none'; blindfolds=0; events.resize(); assert.ok(blindfolds > 0);
});

test('each embed receives viewport/visibility state and ignores unrelated readiness messages', () => {
  const events={}; const messageListeners=[]; const docEvents={}; const observers=[]; const timers=[];
  const medal={dataset:{}}; const messages=[];
  const frames=[true,false].map(isMedal => ({contentWindow:{postMessage:m=>messages.push([isMedal,m.visible])},closest:()=>isMedal?medal:null,addEventListener:(k,fn)=>{ if(isMedal) events.load=fn; }}));
  const context={
    document:{hidden:false, querySelectorAll:()=>frames,addEventListener:(k,fn)=>docEvents[k]=fn},
    location:{origin:'https://example.test'},getComputedStyle:()=>({display:'block'}),
    addEventListener:(k,fn)=>{ if(k === "message") messageListeners.push(fn); else events[k]=fn; },
    dispatchEvent:()=>{},Event:class {},setTimeout:fn=>(timers.push(fn),timers.length),clearTimeout:()=>{},
    IntersectionObserver:class { constructor(fn){observers.push(fn);} observe(){} }
  };
  vm.runInNewContext(read('relatorio/js/embeds.js'),context);
  const notify=(source,origin,state)=>messageListeners.forEach(fn=>fn({source,origin,data:{type:'iconocracy:scene',state}}));
  notify({},context.location.origin,'ready'); assert.equal(medal.dataset.state,'loading');
  notify(frames[0].contentWindow,'https://evil.test','ready'); assert.equal(medal.dataset.state,'loading');
  notify(frames[1].contentWindow,context.location.origin,'ready'); assert.equal(medal.dataset.state,'loading');
  notify(frames[0].contentWindow,context.location.origin,'ready'); assert.equal(medal.dataset.state,'ready');
  events.load(); assert.equal(medal.dataset.state,'ready');
  observers[0]([{isIntersecting:true}]); assert.deepEqual(messages.at(-1),[true,true]);
  observers[0]([{isIntersecting:false}]); assert.deepEqual(messages.at(-1),[true,false]);
  observers[1]([{isIntersecting:true}]); assert.deepEqual(messages.at(-1),[false,true]);
  context.document.hidden=true; docEvents.visibilitychange(); assert.equal(messages.at(-1)[1],false);
  notify(frames[0].contentWindow,context.location.origin,'error'); assert.equal(medal.dataset.state,'error');
  timers[0](); assert.equal(medal.dataset.state,'error');
});
