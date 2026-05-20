import type { CorpusItem, Regime } from '../types/corpus.js';

let _cache: CorpusItem[] | null = null;

/**
 * Load corpus data. In browser context, fetches from the JSON file.
 * Pass the data directly if already loaded (e.g. from a Vite import).
 */
export function loadCorpus(data: CorpusItem[]): CorpusItem[] {
  _cache = data;
  return _cache;
}

export function getCorpus(): CorpusItem[] {
  if (!_cache) throw new Error('Corpus not loaded. Call loadCorpus() first.');
  return _cache;
}

// ── Filters ─────────────────────────────────────────────────────────
export function filterByCountry(items: CorpusItem[], country: string): CorpusItem[] {
  return items.filter((i) => i.country_pt === country || i.country === country);
}

export function filterByRegime(items: CorpusItem[], regime: Regime): CorpusItem[] {
  return items.filter((i) => i.regime === regime);
}

export function filterByDateRange(items: CorpusItem[], start: number, end: number): CorpusItem[] {
  return items.filter((i) => i.year >= start && i.year <= end);
}

export function filterByIconclass(items: CorpusItem[], code: string): CorpusItem[] {
  return items.filter((i) =>
    i.panofsky?.iconographic?.iconclass?.includes(code)
  );
}

export function filterInScope(items: CorpusItem[]): CorpusItem[] {
  return items.filter((i) => i.in_scope);
}

// ── Stats ───────────────────────────────────────────────────────────
export function countByField<K extends keyof CorpusItem>(
  items: CorpusItem[],
  field: K
): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const item of items) {
    const val = String(item[field]);
    counts[val] = (counts[val] || 0) + 1;
  }
  return counts;
}

export function averageEndurecimento(items: CorpusItem[]): number {
  if (!items.length) return 0;
  return items.reduce((sum, i) => sum + (i.endurecimento_score || 0), 0) / items.length;
}
