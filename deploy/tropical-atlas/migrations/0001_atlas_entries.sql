-- Atlas corpus entries table
-- Field names mirror corpus_dataset.csv exactly for zero-friction CSV import
CREATE TABLE IF NOT EXISTS atlas_entries (
  id TEXT PRIMARY KEY,                  -- e.g. AR-001, BR-005
  title TEXT NOT NULL,
  date TEXT,
  year INTEGER,
  period TEXT,
  period_norm TEXT,
  creator TEXT,
  country TEXT,
  country_pt TEXT,
  medium TEXT,
  medium_norm TEXT,
  support TEXT,
  source_archive TEXT,
  url TEXT,
  thumbnail_url TEXT,
  description TEXT,
  citation_abnt TEXT,
  motif_str TEXT,
  tags_str TEXT,
  in_scope INTEGER DEFAULT 1,
  scope_note TEXT,
  -- LPAI purification scores (stored as real, nullable)
  desincorporacao REAL,
  rigidez_postural REAL,
  dessexualizacao REAL,
  uniformizacao_facial REAL,
  heraldizacao REAL,
  enquadramento_arquitetonico REAL,
  apagamento_narrativo REAL,
  monocromatizacao REAL,
  serialidade REAL,
  inscricao_estatal REAL,
  purificacao_composto REAL,
  regime_iconocratico TEXT,
  coded_by TEXT,
  coded_at TEXT,
  notes TEXT,
  -- Admin metadata
  imported_at TEXT DEFAULT (datetime('now')),
  source_file TEXT
);

CREATE INDEX IF NOT EXISTS idx_country ON atlas_entries(country_pt);
CREATE INDEX IF NOT EXISTS idx_medium ON atlas_entries(medium_norm);
CREATE INDEX IF NOT EXISTS idx_regime ON atlas_entries(regime_iconocratico);
CREATE INDEX IF NOT EXISTS idx_year ON atlas_entries(year);
CREATE INDEX IF NOT EXISTS idx_scope ON atlas_entries(in_scope);
