# Iconocracy

**Alegoria Feminina na Iconografia Jurídica · Female Allegory in Legal Iconography**

Monorepo for the doctoral research project *"Iconocracy: Female Allegory in the History of Legal Culture (19th–20th c.)"* at PPGD/UFSC, integrating the searchable corpus, data processing tools, Iconclass classification data, and the Ius Gentium research group website.

---

## Structure

```
iconocracy/
├── corpus/              # Searchable iconographic corpus (HTML + JSON)
│   ├── index.html       # Browser-based search interface
│   └── corpus-data.json # Full corpus dataset
├── tools/               # Research automation scripts
│   ├── scripts/         # Python tools (ABNT citations, feminist network extraction, etc.)
│   ├── schemas/         # JSON schemas (IconoCode, WebScout, master records)
│   ├── sql/             # Database migrations for dual-agent corpus
│   └── email-workflow/  # Email notification workflow
├── data/                # Extracted datasets and networks
├── docs/                # Technical specifications
├── examples/            # Example pipeline outputs (batch_001)
├── website/             # Ius Gentium research group site (grupoiusgentium.com.br)
├── CITATION.cff         # Citation metadata
├── environment.yml      # Conda environment
└── LICENSE
```

## Components

### Corpus (`corpus/`)

A searchable database of feminist legal iconography across European and Brazilian archives, documenting how female allegorical figures — Justice, the Republic, Marianne, Justitia — have shaped the visual vocabulary of law and state power.

- Full-text search across all metadata fields
- Multi-dimensional filtering (country, period, archive, motif)
- Citation export (ABNT and Chicago formats)

**Sources:** Brasiliana Fotográfica, Hemeroteca Digital Brasileira, Gallica (BnF), Europeana, Biblioteca Nacional Digital (Portugal).

### Tools (`tools/`)

Research automation pipeline built on the [Iconclass](https://iconclass.org/) classification system:

| Script | Purpose |
|---|---|
| `abnt_citations.py` | Generate ABNT NBR 6023:2025 citations |
| `extract_feminist_network.py` | Extract feminist iconography subnetwork from Iconclass |
| `batch_example.py` | Batch processing pipeline demo |
| `trace_evidence.py` | Evidence chain tracer for corpus entries |
| `validate_schemas.py` | JSON schema validation for pipeline outputs |
| `make_sqlite.py` | Build SQLite database from Iconclass data |
| `make_index.py` / `make_skos.py` | Index and SKOS generation utilities |

**Schemas** define the dual-agent corpus builder pipeline (IconoCode visual coder + WebScout contextual researcher).

### Website (`website/`)

Static site for the [Ius Gentium](https://www.grupoiusgentium.com.br/) research group at PPGD/UFSC. Deployed via GitHub Pages.

### Data (`data/`)

Pre-extracted datasets:
- `feminist_network_48C51_pt.json` — Feminist iconography subnetwork (Iconclass 48C51) in Portuguese

## Related Resources

- **Iconclass Python library:** [iconclass/code](https://github.com/iconclass/code) — Software libraries for the Iconclass Classification System
- **Iconclass website:** [iconclass.org](https://iconclass.org/)
- **Research HQ:** [ICONOCRACY HQ on Notion](https://www.notion.so/322158101a0581568e58cfc997b7b727)

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
