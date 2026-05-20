/*
 * ICONOCRACY Atlas Lab v1 demonstrative UI seed data.
 *
 * This file is intentionally small and front-end oriented.
 * It is not canonical corpus storage and must not be treated as a repository source of truth.
 * Canonical data remains in:
 * - data/processed/records.jsonl
 * - corpus/corpus-data.json
 *
 * Contract for Task 3 shell work:
 * - each entry may expose canonicalSource to indicate how it should later hydrate
 *   against canonical corpus data
 * - comparison pairs and panel role maps are demonstrative front-end helpers only
 */

export const ICONOCRACY_DEMO_ENTRIES = [
  {
    id: 'BR-001',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'BR-001' },
    title: 'Alegoria da Agricultura (RS)',
    date: '1908',
    country: 'BR',
    medium: 'Fotografia P&B',
    archive: 'Brasiliana Fotográfica',
    regime: '1',
    img: 'https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/11778/0000001.JPG.jpg',
    panelIds: ['P1', 'P5'],
    note:
      'Useful learning-oriented seed for discussing domesticity, agrarian allegory, and diffuse iconocratic recurrence.',
    indicators: { FEI: 1, CII: 2, PRI: 2, SMI: 0, SMS: 1, AMCP: 0, MVI: 2, WI: 0, RI: 1, AI: 2 },
  },
  {
    id: 'BR-002',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'BR-002' },
    title: 'Monumento à República (Belém)',
    date: '1940',
    country: 'BR',
    medium: 'Monumento',
    archive: 'Brasiliana Fotográfica',
    regime: '1',
    img: 'https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/13609/GV%20dvft%20004.JPG.jpg',
    panelIds: ['P1', 'P4'],
    note:
      'Useful for monumentality, republican myth, and the transition from founding allegory toward public stone authority.',
    indicators: { FEI: 0, CII: 3, PRI: 3, SMI: 3, SMS: 2, AMCP: 1, MVI: 1, WI: 1, RI: 1, AI: 3 },
  },
  {
    id: 'BR-005',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'BR-005' },
    title: 'A República (Matriz Positivista)',
    date: '1889',
    country: 'BR',
    medium: 'Pintura',
    archive: 'Museu Histórico Nacional',
    regime: '2',
    img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg/800px-D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg',
    panelIds: ['P2', 'P5'],
    note:
      'Useful for comparing state pedagogy, juridical idealisation, and a domesticated republican female figure.',
    indicators: { FEI: 2, CII: 3, PRI: 2, SMI: 1, SMS: 2, AMCP: 0, MVI: 2, WI: 1, RI: 1, AI: 3 },
  },
  {
    id: 'BR-006',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'BR-006' },
    title: 'A Justiça (Ceschiatti — STF)',
    date: '1961',
    country: 'BR',
    medium: 'Escultura',
    archive: 'Arquivo STF',
    regime: '2',
    img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/A_Justi%C3%A7a_STF.jpg/800px-A_Justi%C3%A7a_STF.jpg',
    panelIds: ['P2', 'P4'],
    note:
      'Core demonstrative case for juridical rigidity, statuary authority, and normative public femininity.',
    indicators: { FEI: 1, CII: 3, PRI: 3, SMI: 3, SMS: 1, AMCP: 0, MVI: 0, WI: 0, RI: 1, AI: 3 },
  },
  {
    id: 'FR-001',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'FR-001' },
    title: 'Marianne (Emprunt 1917)',
    date: '1917',
    country: 'FR',
    medium: 'Cartaz',
    archive: 'Gallica / Europeana',
    regime: '3',
    img: 'https://gallica.bnf.fr/iiif/ark:/12148/btv1b10051217v/f1/full/full/0/native.jpg',
    panelIds: ['P3'],
    note:
      'Useful research seed for militant mobilisation, wartime iconography, and the politicised female body.',
    indicators: { FEI: 1, CII: 2, PRI: 2, SMI: 0, SMS: 3, AMCP: 2, MVI: 0, WI: 2, RI: 1, AI: 2 },
  },
  {
    id: 'FR-003',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'FR-003' },
    title: 'La Liberté guidant le peuple',
    date: '1830',
    country: 'FR',
    medium: 'Pintura',
    archive: 'Louvre',
    regime: '1',
    img: 'https://upload.wikimedia.org/wikipedia/commons/5/5d/Eug%C3%A8ne_Delacroix_-_Le_28_Juillet._La_Libert%C3%A9_guidant_le_peuple.jpg',
    panelIds: ['P1'],
    note:
      'Useful demonstrative anchor for sacrificial founding rhetoric and insurgent allegorical leadership.',
    indicators: { FEI: 3, CII: 1, PRI: 2, SMI: 0, SMS: 3, AMCP: 2, MVI: 1, WI: 3, RI: 2, AI: 2 },
  },
  {
    id: 'UK-003',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'UK-003' },
    title: 'Lady Justice (Old Bailey)',
    date: '1907',
    country: 'UK',
    medium: 'Escultura',
    archive: 'Central Criminal Court',
    regime: '2',
    img: 'https://upload.wikimedia.org/wikipedia/commons/f/f4/Old_Bailey_Lady_Justice.jpg',
    panelIds: ['P2'],
    note:
      'Useful comparison point for the calcified transnational language of juridical femininity.',
    indicators: { FEI: 0, CII: 3, PRI: 3, SMI: 3, SMS: 1, AMCP: 0, MVI: 0, WI: 2, RI: 1, AI: 3 },
  },
  {
    id: 'US-001',
    canonicalSource: { type: 'demo-seed-from-public-atlas', key: 'US-001' },
    title: 'Statue of Liberty',
    date: '1886',
    country: 'US',
    medium: 'Monumento',
    archive: 'NPS',
    regime: '1',
    img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty_7.jpg/800px-Statue_of_Liberty_7.jpg',
    panelIds: ['P1', 'P3'],
    note:
      'Useful for comparing liberatory rhetoric, monumentality, and latent militarisation in republican form.',
    indicators: { FEI: 0, CII: 3, PRI: 3, SMI: 3, SMS: 2, AMCP: 2, MVI: 0, WI: 2, RI: 1, AI: 3 },
  },
];

export const ICONOCRACY_DEMO_COMPARISON_PAIRS = [
  {
    id: 'foundational-vs-juridical',
    label: 'Foundational allegory vs juridical rigidity',
    leftEntryId: 'FR-003',
    rightEntryId: 'BR-006',
    panelIds: ['P1', 'P2'],
    modeIds: ['learning', 'research'],
    guidingQuestion:
      'How does insurgent allegorical movement become stabilized as judicial authority?',
  },
  {
    id: 'monument-vs-militant',
    label: 'Monumental republic vs militant mobilisation',
    leftEntryId: 'BR-002',
    rightEntryId: 'FR-001',
    panelIds: ['P3', 'P4'],
    modeIds: ['research'],
    guidingQuestion:
      'What changes when the female figure shifts from stone permanence to wartime mobilisation?',
  },
  {
    id: 'domestic-recurrence-vs-state-ideal',
    label: 'Diffuse recurrence vs state idealisation',
    leftEntryId: 'BR-001',
    rightEntryId: 'BR-005',
    panelIds: ['P5', 'P2'],
    modeIds: ['learning'],
    guidingQuestion:
      'How do intimate or everyday surfaces reinforce broader state iconographic scripts?',
  },
];

export const ICONOCRACY_PANEL_ROLE_MAP = {
  P1: {
    heroEntryId: 'FR-003',
    comparisonEntryIds: ['US-001', 'BR-002'],
    teachingUse: 'Introduce foundational-sacrificial rhetoric through high-recognition images.',
  },
  P2: {
    heroEntryId: 'BR-006',
    comparisonEntryIds: ['UK-003', 'BR-005'],
    teachingUse: 'Show juridical authority through rigid posture, statuary form, and legal symbolism.',
  },
  P3: {
    heroEntryId: 'FR-001',
    comparisonEntryIds: ['US-001'],
    teachingUse: 'Expose militarisation and mobilisation as a differentiated visual regime.',
  },
  P4: {
    heroEntryId: 'BR-002',
    comparisonEntryIds: ['BR-006'],
    teachingUse: 'Discuss monumentality, whitened authority, and public normativity.',
  },
  P5: {
    heroEntryId: 'BR-001',
    comparisonEntryIds: ['BR-005'],
    teachingUse: 'Surface recurring allegorical scripts outside exclusively monumental settings.',
  },
};

export const ICONOCRACY_DEMO_DATASET = {
  datasetId: 'atlas-lab-iconocracy-demo-v1',
  type: 'demonstrative-ui-seed',
  entryCount: ICONOCRACY_DEMO_ENTRIES.length,
  entries: ICONOCRACY_DEMO_ENTRIES,
  comparisonPairs: ICONOCRACY_DEMO_COMPARISON_PAIRS,
  panelRoleMap: ICONOCRACY_PANEL_ROLE_MAP,
};

export default ICONOCRACY_DEMO_DATASET;
