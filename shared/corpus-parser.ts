/**
 * Canonical parser for corpus-data.json
 * All consumers should use this to ensure schema consistency.
 */

export interface CorpusItem {
  id: string;
  title: string;
  support: string;
  country: string;
  url?: string;
  thumbnail_url?: string;
  indicadores: Record<string, number> | null;
  regime?: string;
  [key: string]: unknown;
}

export interface CorpusData {
  corpus: CorpusItem[];
  metadata: {
    total: number;
    generated_at: string;
    version: string;
  };
}

/**
 * Parse corpus-data.json from a file path or JSON string.
 * Returns null on parse failure.
 */
export function parseCorpusData(source: string | object): CorpusData | null {
  try {
    const data = typeof source === 'string' ? JSON.parse(source) : source;
    if (!Array.isArray(data)) return null;
    return {
      corpus: data as CorpusItem[],
      metadata: {
        total: data.length,
        generated_at: new Date().toISOString(),
        version: '1.0.0'
      }
    };
  } catch {
    return null;
  }
}

/**
 * Find a corpus item by ID.
 */
export function findCorpusItem(data: CorpusData, id: string): CorpusItem | undefined {
  return data.corpus.find(item => item.id === id);
}

/**
 * Get all uncoded item IDs (items without indicadores).
 */
export function getUncodedIds(data: CorpusData): string[] {
  return data.corpus.filter(item => !item.indicadores).map(item => item.id);
}