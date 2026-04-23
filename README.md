<img width="2400" height="1200" alt="iconocracy_01_corpus_banner" src="https://github.com/user-attachments/assets/bca33fa4-0de9-4f3b-aa2e-31fa07be3c06" />

**Alegoria Feminina na Iconografia Jurídica · Female Allegory in Legal Iconography**

Monorepo for the doctoral research project *"Iconocracy: Female Allegory in the History of Legal Culture (19th–20th c.)"* at PPGD/UFSC, integrating the searchable corpus, data processing tools, Iconclass classification data, and the doctoral manuscript.

---

## Operating Model

This repository now works through three explicit surfaces:

- local thesis work: corpus expansion, coding, manuscript, vault
- GitHub: canonical history, lightweight issues, validation, publication backbone
- Hugging Face: frozen dataset snapshots plus a read-only public explorer

Canonical data hierarchy:

1. `data/processed/records.jsonl` — operational ledger
2. `corpus/corpus-data.json` — public-facing export
3. `data/processed/purification.jsonl` — ENDURECIMENTO coding ledger
4. `vault/candidatos/` — auxiliary mirror only

See [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md) and [docs/huggingface-release.md](docs/huggingface-release.md).

---

## Structure

```
iconocracy/
├── corpus/                    # Searchable iconographic corpus
│   ├── index.html             # Browser-based search interface
│   ├── corpus-data.json       # Public corpus export (145 items in the current local snapshot)
│   ├── DASHBOARD_CORPUS.html  # Interactive analytical dashboard (Chart.js)
│   └── atlas-iconometrico.html # Visual atlas (React app)
├── tese/                      # Doctoral manuscript and research outputs
│   ├── manuscrito/            # Chapters under revision (Introdução, Cap.1)
│   ├── revisoes/              # Review documents (ABNT, terminological audit)
│   ├── pesquisa/              # Research notes and NotebookLM reports
│   ├── apresentacoes/         # Progress presentations (PPTX)
│   ├── Para_Orientador_Mar2026/ # Companion articles for advisor
│   ├── ATLAS_ICONOCRACIA.pdf  # Printed atlas: sumário + glossary + gallery
│   └── ATLAS_ICONOCRACIA.docx # Editable source for the atlas
├── tools/                     # Research automation scripts
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
├── website/                   # Ius Gentium research group site (grupoiusgentium.com.br)
├── CITATION.cff               # Citation metadata
├── environment.yml            # Conda environment
├── requirements.txt           # pip dependencies
└── LICENSE
```

## Components

### Corpus (`corpus/`)

A searchable database of feminist legal iconography across European and Brazilian archives, documenting how female allegorical figures — Justice, the Republic, Marianne, Justitia — have shaped the visual vocabulary of law and state power.

**`corpus-data.json`** — public release export of the corpus (145 items in the current local snapshot). Fields include `id`, `title`, `date`, `period`, `creator`, `institution`, `source_archive`, `country`, `medium`, `motif`, `description`, `url`, `thumbnail_url`, `rights`, `citation_abnt`, `citation_chicago`, `tags`, `regime`, `endurecimento_score`, and `indicadores`.

**`DASHBOARD_CORPUS.html`** — Self-contained interactive dashboard. Open in any browser. Includes: Gallery + Table views, modal with full metadata and copy-ready citations, filters by country/period/medium/archive/motif, 6 Chart.js charts (country, medium, period, sources, top motifs, top tags), 6 KPI cards.

- Full-text search across all metadata fields
- Multi-dimensional filtering (country, period, archive, motif)
- Citation export in ABNT NBR 6023:2025 and Chicago formats

**Sources:** Brasiliana Fotográfica, Hemeroteca Digital Brasileira, Gallica (BnF), Europeana, Biblioteca Nacional Digital (Portugal), Library of Congress, Bildindex der Kunst und Architektur.

### Tools (`tools/`)

Research automation pipeline built on the [Iconclass](https://iconclass.org/) classification system:

| Script | Purpose |
|---|---|
| `abnt_citations.py` | Generate ABNT NBR 6023:2025 citations |
| `build_hf_release.py` | Build a frozen Hugging Face dataset snapshot and dataset card |
| `extract_feminist_network.py` | Extract feminist iconography subnetwork from Iconclass |
| `sync_github_labels.py` | Apply the small GitHub label set once auth is available |
| `batch_example.py` | Batch processing pipeline demo |
| `trace_evidence.py` | Evidence chain tracer for corpus entries |
| `validate_schemas.py` | JSON schema validation for pipeline outputs |
| `vault_backup.py` | Create timestamped local vault backups outside `main` |
| `make_sqlite.py` | Build SQLite database from Iconclass data |
| `make_index.py` / `make_skos.py` | Index and SKOS generation utilities |

**Schemas** define the dual-agent corpus builder pipeline (IconoCode visual coder + WebScout contextual researcher).

### Data (`data/`)

Pre-extracted datasets in `data/processed/`:
- `feminist_network_48C51_pt.json` — Feminist iconography subnetwork (Iconclass 48C51) in Portuguese

See `data/docs/README.md` for full dataset documentation and traceability.

### Tese (`tese/`)

Doctoral manuscript materials for *"Iconocracy: Female Allegory in the History of Legal Culture (19th–20th c.)"* — PPGD/UFSC, Ana Vanzin, 2026.

**`ATLAS_ICONOCRACIA.pdf`** — 10-page A4 printed atlas (ReportLab). Three sections: structural summary (clean, without annotations), operational concepts glossary (10 entries: Contrato Sexual Visual, Feminilidade de Estado, Visiocracia, Iconocracia, Pathosformel, Zwischenraum, Regime Iconocrático, Purificação Clássica, ENDURECIMENTO, Colonialidade do Ver), and iconographic gallery (6 public domain images from Wikimedia Commons).

**`manuscrito/`** — Chapters in advanced revision state. See `LEIAME.md` for supervisor-facing guide.

**`revisoes/`** — Review documents: `CITACOES_FALTANTES.md` (all added citations with complete bibliographic data), `REVISAO_ICONOCRACY.md` (argumentative architecture + ABNT audit), `REVISAO_AWR.md` (source-claim alignment table + revised paragraphs).

**`pesquisa/`** — NotebookLM research reports (typology of political regimes, symbolic-architectural plan, Columbia/Hispania comparative analysis).

## Related Resources

- **Iconclass Python library:** [iconclass/code](https://github.com/iconclass/code) — Software libraries for the Iconclass Classification System
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
