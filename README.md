<img width="2400" height="1200" alt="iconocracy_01_corpus_banner" src="https://github.com/user-attachments/assets/bca33fa4-0de9-4f3b-aa2e-31fa07be3c06" />

**Alegoria Feminina na Iconografia Jurídica · Female Allegory in Legal Iconography**

Monorepo for the doctoral research project *"Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"* at PPGD/UFSC, integrating the searchable corpus, data processing tools, Iconclass classification data, and the doctoral manuscript.

---

## Operating Model

This repository works through three explicit surfaces:

- **Local**: thesis work, corpus expansion, coding, manuscript, vault
- **GitHub**: canonical history, lightweight issues, validation, publication backbone
- **Hugging Face**: frozen dataset snapshots plus a read-only public explorer

Canonical data hierarchy (counts as of 2026-05-24):

1. `data/processed/records.jsonl` — operational ledger (**265** records, all schema-valid)
2. `corpus/corpus-data.json` — public-facing export (**264** items)
3. `data/processed/purification.jsonl` — endurecimento coding ledger (**264** records)
4. `vault/candidatos/` — auxiliary mirror (**314** catalog cards, SCOUT notes)

See [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md), [docs/WORKFLOW.md](docs/WORKFLOW.md), and [docs/huggingface-release.md](docs/huggingface-release.md).

Canonical workspace root: `/Users/ana/Research`.
Workspace topology and compatibility paths: [docs/workspace-map.md](docs/workspace-map.md).

---

## Structure

```
iconocracy/
├── corpus/                    # Searchable iconographic corpus
│   ├── index.html             # Browser-based search interface
│   ├── corpus-data.json       # Public corpus export (264 items)
│   ├── DASHBOARD_CORPUS.html  # Interactive analytical dashboard (Chart.js)
│   └── atlas-iconometrico.html # Visual atlas (React app)
├── tese/                      # Doctoral manuscript and research outputs
│   ├── manuscrito/            # Chapters under revision (Introdução, Cap.1–5)
│   ├── revisoes/              # Review documents (ABNT, terminological audit)
│   ├── pesquisa/              # Research notes and NotebookLM reports
│   ├── apresentacoes/         # Progress presentations (PPTX)
│   ├── Para_Orientador_Mar2026/ # Companion articles for advisor
│   ├── ATLAS_ICONOCRACIA.pdf  # Printed atlas: sumário + glossary + gallery
│   └── ATLAS_ICONOCRACIA.docx # Editable source for the atlas
├── tools/                     # Research automation suite (69 Python scripts)
│   ├── scripts/               # Python tools (see docs/scripts.md)
│   ├── schemas/               # JSON schemas (IconoCode, WebScout, master records)
│   ├── sql/                   # Database migrations for dual-agent corpus
│   └── atlas_lab/             # AtlasLab interactive viewer (JSX)
├── data/                      # Datasets (traceability: Drive → GitHub → vault)
│   ├── raw/                   # Manifests and Drive links only (never raw files)
│   ├── interim/               # Data in transformation
│   ├── processed/             # Datasets ready for analysis
│   └── docs/                  # Dataset documentation
├── docs/                      # Technical specifications and ADRs
├── notebooks/                 # Exploratory analysis and iconometrics
├── sources/                   # Saved research results and reference materials
├── examples/                  # Example pipeline outputs (batch_001)
├── vault/                     # Obsidian vault (cataloging cards, Pandoc templates)
├── tests/                     # Test suite (24 files, pytest)
├── archive/                   # Archived legacy files (dialectic essays, Code/ mirror)
├── CITATION.cff               # Citation metadata
├── environment.yml            # Conda environment
├── requirements.txt           # pip dependencies
└── LICENSE
```

## Thesis Architecture

Four studies of case across two centuries:

| Case | Period | Allegorical figure |
|------|--------|--------------------|
| **Brasil-República** | 1889–1930 | A República, A Justiça |
| **Brasil-Tribunais** | — | Justiça vendada no STF |
| **França-Marianne** | 1789–1946 | Marianne, La République, La Justice |
| **UK-Britannia** | 1800–1950 | Britannia, Justice, Hibernia |

Three argumentative versions: **historical**, **theoretical-conceptual**, **comparative-postcolonial**.

Four theoretical clusters: Legal History · Visual Culture · Feminist Theory · Post-colonial.

## Corpus (`corpus/`)

A searchable database of feminist legal iconography across European and Brazilian archives, documenting how female allegorical figures — Justice, the Republic, Marianne, Justitia — have shaped the visual vocabulary of law and state power.

**`corpus-data.json`** — public release export of the corpus (264 items). Fields include `id`, `title`, `date`, `period`, `creator`, `institution`, `source_archive`, `country`, `medium`, `motif`, `description`, `url`, `thumbnail_url`, `rights`, `citation_abnt`, `citation_chicago`, `tags`, `regime`, `endurecimento_score`, and `indicadores`.

**`DASHBOARD_CORPUS.html`** — Self-contained interactive dashboard. Open in any browser. Includes: Gallery + Table views, modal with full metadata and copy-ready citations, filters by country/period/medium/archive/motif, 6 Chart.js charts (country, medium, period, sources, top motifs, top tags), 6 KPI cards.

- Full-text search across all metadata fields
- Multi-dimensional filtering (country, period, archive, motif)
- Citation export in ABNT NBR 6023:2025 and Chicago formats

**Sources:** Brasiliana Fotográfica, Hemeroteca Digital Brasileira, Gallica (BnF), Europeana, Biblioteca Nacional Digital (Portugal), Library of Congress, Bildindex der Kunst und Architektur.

**10 purification indicators** (ordinal 0–3, measuring the *endurecimento* of female allegorical figures across iconocratic regimes):

| # | Indicator (PT) | English gloss |
|---|----------------|---------------|
| 0 | desincorporação | disembodiment |
| 1 | rigidez_postural | postural rigidity |
| 2 | dessexualização | de-sexualization |
| 3 | uniformização_facial | facial uniformization |
| 4 | heraldização | heraldic abstraction |
| 5 | enquadramento_arquitetônico | architectural framing |
| 6 | apagamento_narrativo | narrative erasure |
| 7 | monocromatização | monochromatization |
| 8 | serialidade | seriality / mass reproduction |
| 9 | inscrição_estatal | state inscription |

Three iconocratic regimes: FUNDACIONAL (sacrificial, body alive) → NORMATIVO (domesticated, bureaucratic) → MILITAR (hardened, imperial) → CONTRA-ALEGORIA (subversive, contested).

## Tools (`tools/`)

Research automation suite (69 Python scripts in `tools/scripts/`) built on the [Iconclass](https://iconclass.org/) classification system. Key functional groups:

| Category | Scripts |
|----------|---------|
| **Corpus pipeline** | `validate_schemas.py`, `records_to_corpus.py`, `vault_sync.py`, `trace_evidence.py` |
| **ARGOS acquisition** | `argos_build_manifest.py`, `argos_prepare_dispatch.py`, `argos_report.py`, `argos_acquire_item.py` |
| **IconoCode coding** | `code_purification.py`, `iconocode_gemma4.py`, `iconocode_to_corpus.py` |
| **Data exports** | `build_hf_release.py`, `abnt_citations.py`, `csv_to_records.py`, `endurecimento_summary.py` |
| **Image processing** | `download_corpus_images.py`, `europeana_download.py`, `loc_download.py`, `iiif.py` |
| **KB / indexing** | `make_index.py`, `make_sqlite.py`, `make_skos.py`, `extract_feminist_network.py` |
| **Analysis** | `notebooks/` 01–08 (exploratory → Kruskal-Wallis → regression → clustering → multidimensional scoring) |
| **Evaluation** | `compute_irr.py`, `run_iconocracy_eval.py`, `compare_iconocracy_eval_runs.py` |
| **Ingestion** | `ingest_fichas_lpai.py`, `t4_adjudicate.py`, `sync_companion.py` |

**Schemas** define the dual-agent corpus builder pipeline (IconoCode visual coder + WebScout contextual researcher).

| Schema | File | Version |
|--------|------|---------|
| **Codebook LPAI** | `schemas/codebook-v2.1.0.schema.json` | v2.1.0 |
| Master Record | `tools/schemas/master-record.schema.json` | v1 |
| WebScout | `tools/schemas/webscout.schema.json` | v1 |

See `schemas/codebook-v2.1.0.schema.json` for the expanded codebook schema with: capta declaration, split attribute lists (objetos_regalia / marcas_corporais / marcadores_cena), conditional justifications (gênero, incerteza), power_at_stake, programa_id for individual figures in iconographic programs, intercoder adjudication log, and 10 purification indicators.

## Data (`data/`)

Pre-extracted datasets in `data/processed/`:
- `feminist_network_48C51_pt.json` — Feminist iconography subnetwork (Iconclass 48C51) in Portuguese

See `data/docs/README.md` for full dataset documentation and traceability.

## Tese (`tese/`)

Doctoral manuscript materials for *"Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"* — PPGD/UFSC, Ana Vanzin, 2026.

**`ATLAS_ICONOCRACIA.pdf`** — 10-page A4 printed atlas (ReportLab). Three sections: structural summary, operational concepts glossary (10 entries: Contrato Sexual Visual, Feminilidade de Estado, Visiocracia, Iconocracia, Pathosformel, Zwischenraum, Regime Iconocrático, Purificação Clássica, endurecimento militar, Colonialidade do Ver), and iconographic gallery (6 public domain images).

**`manuscrito/`** — Chapters in advanced revision state. See `LEIAME.md` for supervisor-facing guide.

**`revisoes/`** — Review documents: `CITACOES_FALTANTES.md` (all added citations with complete bibliographic data), `REVISAO_ICONOCRACY.md` (argumentative architecture + ABNT audit), `REVISAO_AWR.md` (source-claim alignment table + revised paragraphs).

**`pesquisa/`** — NotebookLM research reports (typology of political regimes, symbolic-architectural plan, Columbia/Hispania comparative analysis, legal iconography extended analysis).

## Related Resources

- **Iconclass Python library:** [iconclass/code](https://github.com/iconclass/code)
- **Iconclass website:** [iconclass.org](https://iconclass.org/)
- **Hugging Face dataset:** [warholana/iconocracy-corpus](https://hf.co/datasets/warholana/iconocracy-corpus)
- **Operating model:** [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md)

## Citation

If you use this corpus or tools in your research, please cite:

```bibtex
@misc{vanzin2026iconocracy,
  author    = {Vanzin, Ana},
  title     = {Iconocracy: Female Allegory in the History of Legal Culture},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/anavvanzin/iconocracy-corpus}
}
```

## License

Code and tools: MIT License. Corpus metadata: CC BY 4.0. Individual images are subject to the rights indicated in each entry.
