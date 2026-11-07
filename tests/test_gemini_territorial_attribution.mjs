import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import test from 'node:test';
import vm from 'node:vm';

// Execute the actual TypeScript module with an in-memory SDK. No package install,
// API credential, model request or network access is required.
const source = readFileSync(new URL('../shared/services/gemini.ts', import.meta.url), 'utf8');

async function loadService({ key, responses = [] } = {}) {
  const requests = [];
  let clientCount = 0;
  const context = vm.createContext({ process: { env: key ? { GEMINI_API_KEY: key } : {} } });
  class MockGoogleGenAI {
    constructor() {
      clientCount += 1;
      this.models = {
        generateContent: async (request) => {
          requests.push(request);
          assert.ok(responses.length, 'Unexpected model request');
          return responses.shift();
        },
      };
    }
  }
  const sdk = new vm.SyntheticModule(
    ['GoogleGenAI', 'Type', 'ThinkingLevel'],
    function () {
      this.setExport('GoogleGenAI', MockGoogleGenAI);
      this.setExport('Type', { OBJECT: 'object', ARRAY: 'array', STRING: 'string', NUMBER: 'number' });
      this.setExport('ThinkingLevel', { HIGH: 'high' });
    },
    { context },
  );
  const service = new vm.SourceTextModule(stripTypeScriptTypes(source), { context });
  await service.link((specifier) => {
    assert.equal(specifier, '@google/genai');
    return sdk;
  });
  await service.evaluate();
  return { api: service.namespace, requests, clients: () => clientCount };
}

test('catalogue hints return a documented gap without a key or model call', async () => {
  const service = await loadService();
  for (const title of ['Justitia em Paris', 'A República brasileira', 'Artista estrangeiro']) {
    const pending = service.api.generateCorpusInference(title, '1900', '44B03');
    assert.equal(typeof pending.then, 'function', 'Public async signature remains usable');
    const result = await pending;
    assert.equal(typeof result, 'string');
    assert.ok(result.includes(title), 'Catalogue hint remains identifiable');
    assert.match(result, /Lacuna documental \(gap\)/);
    assert.match(result, /consulte fontes/);
    assert.match(result, /permite manter o item no catálogo/);
    assert.match(result, /demais afirmações que tenham evidência própria/);
  }
  assert.equal(service.clients(), 0);
  assert.equal(service.requests.length, 0);
});

test('evidence pipeline preserves response shapes and sends qualified attribution instructions', async () => {
  const webScout = {
    search_results: [{ evidence_id: 'E1', url: 'https://example.org/catalogue/1', score: 0.8, institution: 'Acervo' }],
    gaps: ['Circulação desconhecida; fonte de encomenda não localizada.'],
  };
  const masterRecord = {
    iconclass_codes: ['44B03'],
    semiotic_analysis: '[tentative] Atribuição do catálogo; supports: E1; gaps: encomenda.',
    abnt_citation: '[gap] Metadados bibliográficos incompletos.',
  };
  const service = await loadService({ key: 'offline-test', responses: [
    { text: JSON.stringify(webScout) },
    { text: JSON.stringify(masterRecord) },
  ] });
  const result = await service.api.mineEvidences('Obra francesa no Brasil', undefined, { location: 'Brasil' });
  assert.deepEqual(JSON.parse(JSON.stringify(result)), { webScout, masterRecord });
  assert.equal(service.requests.length, 2);
  for (const request of service.requests) {
    const instruction = request.config.systemInstruction;
    for (const relation of ['autoria', 'produção', 'localização atual', 'assunto representado', 'encomenda/patrocínio', 'jurisdição na data', 'circulação', 'recepção']) {
      assert.ok(instruction.includes(relation), `Missing relation: ${relation}`);
    }
    assert.match(instruction, /não é necessário preencher todas/i);
    assert.match(instruction, /não exclui relação documentada com o Brasil/);
    assert.match(instruction, /Busca sem resultado não prova inexistência/);
  }
  const iconoCodeRequest = service.requests[1];
  assert.deepEqual(Array.from(iconoCodeRequest.config.responseSchema.required), [
    'iconclass_codes', 'semiotic_analysis', 'abnt_citation',
  ]);
  assert.match(iconoCodeRequest.config.systemInstruction, /supported, tentative ou gap/);
  assert.match(iconoCodeRequest.config.systemInstruction, /registro documental, filologia conceitual e hipótese iconológica/);
  assert.doesNotMatch(iconoCodeRequest.config.systemInstruction, /foque na tensão entre a tradição europeia e a apropriação brasileira/);
  assert.ok(service.requests[0].contents.parts.some((part) => part.text?.includes('não substituem as fontes primárias')));
});
