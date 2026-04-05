/** 10-dimension purification indicator vector */
export interface Indicadores {
  desincorporacao: number;
  rigidez_postural: number;
  dessexualizacao: number;
  uniformizacao_facial: number;
  heraldizacao: number;
  enquadramento_arquitetonico: number;
  apagamento_narrativo: number;
  monocromatizacao: number;
  serialidade: number;
  inscricao_estatal: number;
}

export interface PanofskyIconographic {
  motivo_alegorico: string;
  iconclass: string[];
  tradicao: string;
  pathosformel: string;
}

export interface PanofskyIconological {
  regime: string;
  funcao: string;
  contrato_sexual_visual: string;
  colonialidade_do_ver: string;
}

export interface Panofsky {
  pre_iconographic: string;
  iconographic: PanofskyIconographic;
  iconological: PanofskyIconological;
  analyst_notes?: string;
}

export type Regime = 'fundacional' | 'normativo' | 'militar';

export interface CorpusItem {
  id: string;
  title: string;
  date: string;
  period: string;
  creator: string;
  institution: string;
  source_archive: string;
  country: string;
  medium: string;
  motif: string[];
  description: string;
  url: string;
  thumbnail_url: string;
  rights: string;
  citation_abnt: string;
  citation_chicago: string;
  tags: string[];
  year: number;
  medium_norm: string;
  country_pt: string;
  period_norm: string;
  motif_str: string;
  tags_str: string;
  regime: Regime;
  endurecimento_score: number;
  indicadores: Indicadores;
  coded_by: string;
  coded_at: string;
  support: string;
  in_scope: boolean;
  scope_note: string | null;
  panofsky: Panofsky;
}
