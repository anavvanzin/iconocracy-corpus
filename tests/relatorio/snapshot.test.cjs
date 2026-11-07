// Run: node --test tests/relatorio/snapshot.test.cjs
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const read = p => fs.readFileSync(path.join(__dirname, '../..', p), 'utf8');
const historical = 'eae4c3a0a524eca6f1c4863c2d6fc21959f9435b';

test('report retains its historical count and exposes its date before drilling', () => {
  const context = {window: {}};
  vm.runInNewContext(read('relatorio/js/data.js'), context);
  const item = context.window.RPT.stats[0];
  assert.equal(item.num, 336);
  assert.match(item.lbl, /28\/09\/2026/);
  assert.match(item.drill.value, /histórico/);
  assert.match(item.drill.sub, /15\/09\/2026/);
  assert.match(item.drill.source, /K29/);
  const html = read('relatorio/index.html');
  const countReferences = html.match(/(?:<meta[^>]+>|<p\b[^>]*>[\s\S]*?<\/p>)/g).filter(s => /336/.test(s));
  assert.ok(countReferences.length >= 4);
  for (const reference of countReferences) {
    assert.match(reference, /histórico/);
    assert.match(reference, /28\/09\/2026/);
  }
  const note = html.match(/<p id="corpus-snapshot">[\s\S]*?<\/p>/)[0];
  assert.match(note, /337 registros/);
  assert.match(note, /04\/10\/2026/);
  assert.match(note, /33132b3485629183d7378c674c67cd8136d53ce1\/data\/processed\/records.jsonl/);
  assert.match(note, /já tinha 337 entradas em 27\/09/);
  assert.match(note, /BUILD_LOG.md#reconciliacao-2026-10-13/);
});

test('K29 points to a recoverable historical version and discloses the consultation uncertainty', () => {
  const context = {window: {}, document: {getElementById: () => null}};
  vm.runInNewContext(read('relatorio/js/sources.js'), context);
  const source = context.window.SRCS.find(s => s.k === 'K29');
  assert.equal(source.url, `https://github.com/anavvanzin/imagens/blob/${historical}/site/data/corpus-data-enriched.json`);
  assert.match(source.date, /2026-09-15/);
  assert.match(source.date, /2026-09-28/);
  assert.match(source.note, /336 itens/);
  assert.match(source.note, /não comprova a versão exata/);
  assert.match(source.note, /337 em 27\/09/);
});
