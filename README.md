<img width="2400" height="1200" alt="iconocracy_01_corpus_banner" src="https://github.com/user-attachments/assets/bca33fa4-0de9-4f3b-aa2e-31fa07be3c06" />

# Iconocracia · Female Allegory in Legal Iconography

**Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)**

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20dataset-warholana%2Ficonocracy--corpus-yellow.svg)](https://hf.co/datasets/warholana/iconocracy-corpus)
[![Site](https://img.shields.io/badge/site-iconocracia.com-black.svg)](https://iconocracia.com)

Research monorepo for a doctoral thesis (PPGD/UFSC, Ana Vanzin, defense 2026) that asks a single question: **how does the female allegorical figure — Justice, the Republic, Marianne, Britannia, Columbia — get *hardened* into an instrument of state and legal power?**

It brings together (1) a searchable, **open and growing** corpus of female allegories on coins, stamps, monuments, courthouses, prints and banknotes; (2) a dual-agent pipeline that discovers and codes each item; (3) statistical analysis of the "hardening" process; and (4) the thesis manuscript itself.

> **The corpus is exploratory, not frozen.** It keeps growing until the defense. The counts below are a **working snapshot (July 2026)** — treat them as a state-of-progress reading, not a fixed *N*.

---

## Table of Contents

- [What's inside](#whats-inside)
- [The corpus at a glance](#the-corpus-at-a-glance)
- [Core concept: *endurecimento*](#core-concept-endurecimento)
- [The dual-agent pipeline](#the-dual-agent-pipeline)
- [Quickstart](#quickstart)
- [Repository layout](#repository-layout)
- [Thesis architecture](#thesis-architecture)
- [Data model & traceability](#data-model--traceability)
- [Related resources](#related-resources)
- [Citation](#citation)
- [License](#license)

---

## What's inside

This repository operates across three surfaces:

| Surface | Role |
| --- | --- |
| **Local** | Thesis writing, corpus expansion, visual coding, Obsidian vault |
| **GitHub** (this repo) | Canonical history, schema validation (CI), the publication backbone |
| **Hugging Face** | Frozen dataset snapshots + a read-only public [explorer](https://hf.co/datasets/warholana/iconocracy-corpus) |

The public-facing browsable surfaces are all self-contained HTML — open them straight in a browser:

- **`corpus/index.html`** — full-text searchable corpus interface
- **`corpus/DASHBOARD_CORPUS.html`** — interactive dashboard (gallery + table, filters, Chart.js charts, copy-ready citations)
- **`corpus/atlas-iconometrico.html`** — visual atlas of the corpus

---

## The corpus at a glance

*Working snapshot — July 2026. Numbers grow between commits.*

- **~328** coded records in the operational ledger (`data/processed/records.jsonl`)
- **~328** items in the public export (`corpus/corpus-data.json`)
- **~279** items with full *endurecimento* coding (`data/processed/purification.jsonl`)
- **~363** catalog cards in the Obsidian vault (`vault/candidatos/`)

**By country** (top of a non-exhaustive, transnational corpus):

| FR | BR | US | DE | UK | IT | PT | BE | NL | ES | + AT, DK, MX, CL, AR… |
|----|----|----|----|----|----|----|----|----|----|----|
| 97 | 72 | 32 | 27 | 23 | 20 | 11 | 11 | 10 | 7 | |

**By iconocratic regime:**

| Regime | Count | Character |
|--------|-------|-----------|
| **Fundacional** | 158 | Sacrificial, body alive |
| **Normativo** | 102 | Domesticated, bureaucratic |
| **Militar** | 54 | Hardened, imperial |
| **Contra-alegoria** | 14 | Subversive, contested |

**Supports:** coin · stamp · monument/sculpture · courthouse architecture · print/engraving · frontispiece · banknote · poster
**Period:** 1800–2000 (priority 1880–1920)

**Inclusion criteria** (all four required): a female allegorical figure · with an explicit juridical-political function · datable 1800–2000 · on an accepted support. Country is an *analytical variable*, **not** a gate — the "universal" allegory is transnational by design.

**Sources:** Brasiliana Fotográfica · Hemeroteca Digital Brasileira · Gallica (BnF) · Europeana · Biblioteca Nacional Digital (Portugal) · Library of Congress · Bildindex der Kunst und Architektur.

---

## Core concept: *endurecimento*

The thesis measures how allegorical female figures are progressively **hardened** (*endurecimento*, always in Portuguese — the empirical operationalization of *Purificação Clássica*) into abstract instruments of the state. Every item is scored on **10 ordinal indicators (0–3)**:

| # | Indicator (PT) | English gloss |
|---|----------------|---------------|
| 1 | desincorporação | disembodiment |
| 2 | rigidez_postural | postural rigidity |
| 3 | dessexualização | de-sexualization |
| 4 | uniformização_facial | facial uniformization |
| 5 | heraldização | heraldic abstraction |
| 6 | enquadramento_arquitetônico | architectural framing |
| 7 | apagamento_narrativo | narrative erasure |
| 8 | monocromatização | monochromatization |
| 9 | serialidade | seriality / mass reproduction |
| 10 | inscrição_estatal | state inscription |

The sum feeds an `endurecimento_score` and places each figure along the regime trajectory: **Fundacional → Normativo → Militar**, with **Contra-alegoria** as the subversive counter-movement.

Four original conceptual contributions of the thesis (Vanzin 2026): **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual**, and **Purificação Clássica**.

---

## The dual-agent pipeline

```
WebScout  ──────────────▶  IconoCode  ──────────────▶  master records
(archive discovery)        (visual analysis)            records.jsonl → corpus-data.json
```

- **WebScout** queries digital archives (Europeana, Gallica, LOC, BnF, Numista, Colnect) for candidate figures and contextual metadata.
- **IconoCode** performs a 3-level Panofsky analysis plus the 10 *endurecimento* indicators.
- Output flows into `data/processed/records.jsonl` (canonical) and is exported to `corpus/corpus-data.json` (public).

A separate **ARGOS** workflow orchestrates acquisition (manifest → dispatch groups → report).

---

## Quickstart

```bash
# 1. Environment (conda, Python 3.11)
conda env create -f environment.yml
conda activate iconocracy

# 2. Browse the corpus — no build needed; open the file in any browser
#    corpus/DASHBOARD_CORPUS.html   (or corpus/index.html)

# 3. Validate the data
python tools/scripts/validate_schemas.py

# 4. Preview the records → public-export diff
python tools/scripts/records_to_corpus.py --diff

# 5. Check endurecimento coding progress
python tools/scripts/code_purification.py --status

# 6. Run the tests
pytest tests/
```

Every Python tool is run **from the repo root**: `python tools/scripts/<script>.py`.

**Release gate** (run in order before any public/HF snapshot):
`validate_schemas.py` → `code_purification.py --status` → `vault_sync.py status` → `records_to_corpus.py --diff` → `build_hf_release.py`. See [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md).

---

## Repository layout

```
iconocracy-corpus/
├── corpus/            # Searchable corpus + self-contained HTML dashboards
│   ├── index.html            # Browser search interface
│   ├── corpus-data.json      # Public export (the canonical public surface)
│   ├── DASHBOARD_CORPUS.html # Interactive analytical dashboard (Chart.js)
│   └── atlas-iconometrico.html
├── data/
│   ├── raw/                  # Manifests & Drive links ONLY — never binaries (ADR-001)
│   ├── interim/              # Data in transformation
│   └── processed/            # records.jsonl + purification.jsonl (canonical ledgers)
├── tools/
│   ├── scripts/              # ~100 Python automation scripts
│   ├── schemas/              # JSON schemas (master-record, IconoCode, WebScout)
│   └── sql/                  # DB migrations for the dual-agent corpus
├── tese/                # Doctoral manuscript, revisions, research notes, atlas
│   ├── manuscrito/           # Chapters (Markdown → Pandoc)
│   └── revisoes/             # ABNT + terminological audits
├── notebooks/           # Analysis 01–08 (exploratory → Kruskal-Wallis → regression
│                        #   → correspondence → temporal → clustering → dimensionality
│                        #   → multidimensional scoring)
├── vault/               # Obsidian vault (candidatos/ catalog cards, templates)
├── docs/                # Specs, ADRs, operating model, workflows
├── deploy/              # Cloudflare Workers companion, HF Space
├── tests/              # pytest suite (~32 files)
├── environment.yml · requirements.txt · CITATION.cff · LICENSE
```

---

## Thesis architecture

Four case studies across two centuries:

| Case | Period | Allegorical figures |
|------|--------|---------------------|
| **Brasil-República** | 1889–1930 | A República, A Justiça |
| **Brasil-Tribunais** | 20th c. | Justiça vendada no STF |
| **França-Marianne** | 1789–1946 | Marianne, La République, La Justice |
| **UK-Britannia** | 1800–1950 | Britannia, Justice, Hibernia |

Read three ways — **historical**, **theoretical-conceptual**, and **comparative-postcolonial** — across four theoretical clusters: Legal History · Visual Culture · Feminist Theory · Post-colonial studies.

> **Master plan:** [`docs/PLANO-TESE-ICONOCRACIA.md`](docs/PLANO-TESE-ICONOCRACIA.md) — full architecture, methodology, case rankings, risk matrix, and work plan.

---

## Data model & traceability

Canonical source-of-truth order:

1. **`data/processed/records.jsonl`** — operational canonical ledger
2. **`corpus/corpus-data.json`** — public-facing export (browsers, dashboards, HF)
3. **`data/processed/purification.jsonl`** — *endurecimento* coding ledger
4. **`vault/candidatos/`** — auxiliary cataloguing mirror

Public-export fields include `id`, `title`, `date`, `country`, `motif`, `regime`, `description`, `url`, `endurecimento_score`, `indicadores`, and `citation_abnt`. Coding fields (`subtipo`, `familia_alegorica`, `vetor_colonial`, `hipotese_racial`, …) live nested under `purificacao` in `records.jsonl` and are flattened into the export by `records_to_corpus.py` — so **never hand-edit `corpus-data.json`**; edit the source and regenerate.

**Traceability rule** — every item exists in three places: Google Drive (+ `data/raw/drive-manifest.json`) · a vault card in `vault/candidatos/` · a master record in `records.jsonl`. Per **ADR-001**, `data/raw/` stays metadata-only in git; binaries live on Google Drive.

CI (`.github/workflows/validate.yml`) validates the ledger against the schema, checks consistency with the export, and rejects binaries in `data/raw/`.

---

## Related resources

- 🤗 **Hugging Face dataset:** [warholana/iconocracy-corpus](https://hf.co/datasets/warholana/iconocracy-corpus)
- 🌐 **Project site:** [iconocracia.com](https://iconocracia.com)
- 📐 **Iconclass** classification system: [iconclass.org](https://iconclass.org/) · [iconclass/code](https://github.com/iconclass/code)
- 📄 **Operating model & workflows:** [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md) · [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
- 🃏 **Agent quick-reference:** [`AGENTS.md`](AGENTS.md) · [`CLAUDE.md`](CLAUDE.md)

---

## Citation

If you use this corpus or the tools in your research, please cite:

```bibtex
@misc{vanzin2026iconocracy,
  author    = {Vanzin, Ana},
  title     = {Iconocracy: Female Allegory in the History of Legal Culture},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/anavvanzin/iconocracy-corpus}
}
```

Machine-readable metadata: [`CITATION.cff`](CITATION.cff).

---

## License

Code and tools: **MIT**. Corpus metadata: **CC BY 4.0**. Individual images are subject to the rights indicated in each entry.
