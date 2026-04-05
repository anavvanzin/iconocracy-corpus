export interface SearchResult {
  evidence_id: string;
  url: string;
  score: number;
  institution: string;
}

export interface GroundingChunk {
  uri: string;
  title: string;
}

export interface WebScoutOutput {
  search_results: SearchResult[];
  gaps: string[];
  grounding_chunks?: GroundingChunk[];
}

export interface MasterRecord {
  iconclass_codes: string[];
  semiotic_analysis: string;
  abnt_citation: string;
}

export interface PipelineOutput {
  webScout: WebScoutOutput;
  masterRecord: MasterRecord;
}

export interface AdvancedParams {
  dateRange?: string;
  location?: string;
  iconclassCodes?: string;
}
