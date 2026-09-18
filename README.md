<img width="2400" height="1200" alt="iconocracy_01_corpus_banner" src="https://github.com/user-attachments/assets/bca33fa4-0de9-4f3b-aa2e-31fa07be3c06" />

# Iconocracia · Female Allegory in Legal Iconography

**Alegoria Feminina na História da Cultura Jurídica (Séculos XIX-XX)**

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20dataset-warholana%2Ficonocracy--corpus-yellow.svg)](https://hf.co/datasets/warholana/iconocracy-corpus)
[![Site](https://img.shields.io/badge/site-iconocracia.com-black.svg)](https://iconocracia.com)
[![Dashboard](https://img.shields.io/badge/dashboard-live-2A7A5A.svg)](https://dashboard.iconocracia.com)

Research monorepo for a doctoral thesis in progress (PPGD/UFSC, Ana Vanzin). The thesis studies how female allegorical figures such as Justice, the Republic, Marianne, Britannia and Columbia come to organize reality and distribute state and legal authority.

The repository brings together (1) a searchable, **open and growing** corpus of female allegories on coins, stamps, monuments, courthouses, prints and banknotes; (2) a dual-agent pipeline that discovers and describes each item; (3) iconometric analysis, with *endurecimento* as its axis of fixity; and (4) the thesis manuscript itself.

> **The corpus is exploratory, not frozen.** It keeps growing until the defense. The counts below are a **working snapshot (September 2026, commit `e86cb37`)**: a state-of-progress reading, not a fixed *N*.

---

## Table of Contents

- [Where the research lives](#where-the-research-lives)
- [The corpus at a glance](#the-corpus-at-a-glance)
- [Method: iconometria and *endurecimento*](#method-iconometria-and-endurecimento)
- [The dual-agent pipeline](#the-dual-agent-pipeline)
- [Quickstart](#quickstart)
- [Repository layout](#repository-layout)
- [Thesis architecture](#thesis-architecture)
- [Data model & traceability](#data-model--traceability)
- [Known issues and honest numbers](#known-issues-and-honest-numbers)
- [Related resources](#related-resources)
- [Citation](#citation)
- [License](#license)

---

## Where the research lives

The research is a constellation: this repository is the canonical core, and the public surfaces are derived from it.

| Surface | Role | Where |
| --- | --- | --- |
| **Local** | Thesis writing, corpus expansion, visual coding, Obsidian vault | Working copy of this repo |
| **iconocracy-corpus** | Canonical history, schema validation (CI), publication backbone | This repo |
| **Research** | Meta-workspace: workflow specs and research automation | [anavvanzin/Research](https://github.com/anavvanzin/Research) |
| **Mnemosyne Viva** | Public editorial home of the archive | [iconocracia.com](https://iconocracia.com) · [anavvanzin/imagens](https://github.com/anavvanzin/imagens) |
| **Analytical dashboard** | `corpus/DASHBOARD_CORPUS.html` on Cloudflare Pages, first published 2026-08-14 | [dashboard.iconocracia.com](https://dashboard.iconocracia.com) |
| **Hugging Face** | Frozen dataset snapshots and a read-only explorer | [warholana/iconocracy-corpus](https://hf.co/datasets/warholana/iconocracy-corpus) |

**Mnemosyne Viva** is a static editorial site. Its repository validates the *acervo* against JSON Schema, reruns that validation every week, and checks image performance every month.

The browsable surfaces in this repo are self-contained HTML, so they open straight in a browser:

- **`corpus/index.html`**: full-text searchable corpus interface
- **`corpus/DASHBOARD_CORPUS.html`**: interactive dashboard with gallery and table views, filters, Chart.js charts, copy-ready citations, and a *Modo Foco* writing panel (the same file serves dashboard.iconocracia.com)
- **`corpus/atlas-iconometrico.html`**: visual atlas of the corpus
- **[`deploy/iconocracia-cv/`](deploy/iconocracia-cv/)**: course site and reproducible computer-vision dataset audit

---

## The corpus at a glance

*Working snapshot, September 2026 (commit `e86cb37`). Numbers grow between commits.*

- **335** records in the operational ledger (`data/processed/records.jsonl`)
- **335** items in the public projection (`corpus/corpus-data.json`)
- **286** coding observations in `data/processed/purification.jsonl` (77 are all-zero observations: 76 inherited placeholders and one genuine manual coding; see [Known issues](#known-issues-and-honest-numbers))
- **410** catalog cards in the Obsidian vault (`vault/candidatos/`), plus 38 rejected cards in `_rejeitados/`

**By country** (top of a non-exhaustive, transnational corpus):

| FR | BR | US | DE | UK | IT | PT | BE | NL | ES | + AT, CL, DK, MX, AR, CH, UY |
|----|----|----|----|----|----|----|----|----|----|----|
| 101 | 72 | 32 | 27 | 23 | 20 | 11 | 11 | 10 | 10 | |

**By iconocratic regime** (public projection):

| Regime | Count | Character |
|--------|-------|-----------|
| **Fundacional** | 163 | Sacrificial, body alive |
| **Normativo** | 103 | Domesticated, bureaucratic |
| **Militar** | 54 | Hardened, imperial |
| **Contra-alegoria** | 15 | Subversive, contested |

**Supports:** coin · stamp · monument/sculpture · courthouse architecture · print/engraving · frontispiece · banknote · poster

**Period:** 1800-2000 inclusion window, with priority on 1880-1920. Some items fall outside the window; see [Known issues](#known-issues-and-honest-numbers).

**Inclusion criteria** (all four required): a female allegorical figure · with an explicit juridical-political function · datable 1800-2000 · on an accepted support. Country is an *analytical variable*, **not** a gate (decision 2026-06-22), because the "universal" allegory is transnational by design.

**Sources:** Brasiliana Fotográfica · Hemeroteca Digital Brasileira · Gallica (BnF) · Europeana · Biblioteca Nacional Digital (Portugal) · Library of Congress · Bildindex der Kunst und Architektur · British Museum · Rijksmuseum.

---

## Method: iconometria and *endurecimento*

**Iconometria** is the umbrella methodological framework (decision 2026-07-11): the measurement and analysis of iconographic patterns in the corpus. *Endurecimento* (always in Portuguese) is its axis of fixity and the empirical operationalization of *Purificação Clássica*. Every coded item is described on **10 ordinal indicators (0-3)**:

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

The indicators are no longer summed. Since 2026-07-28 the composite index is retired as evidence and frozen as a historical artifact, and new coding records a verbal inventory of attributes instead ([decision](docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md)). The `endurecimento_score` field in the public projection carries only those frozen legacy values.

Regimes place each figure along the trajectory **Fundacional → Normativo → Militar**, with **Contra-alegoria** as the subversive counter-movement. Items are read at Panofsky's three levels together with Warburg's apparatus (*Pathosformel*, *Nachleben*, *Zwischenraum*, always in German).

Four original conceptual contributions of the thesis (Vanzin 2026): **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual**, and **Purificação Clássica**. They are the author's own concepts and are not attributable to Pateman or Mondzain.

---

## The dual-agent pipeline

```
WebScout  ──────────────▶  IconoCode  ──────────────▶  master records
(archive discovery)        (visual analysis)            records.jsonl → corpus-data.json
```

- **WebScout** queries digital archives (Europeana, Gallica, LOC, BnF, Numista, Colnect) for candidate figures and contextual metadata.
- **IconoCode** performs a 3-level Panofsky analysis plus the 10 *endurecimento* indicators.
- Output flows into `data/processed/records.jsonl` and `data/processed/purification.jsonl`, and is projected to `corpus/corpus-data.json` for the public surfaces.

A separate **ARGOS** workflow orchestrates acquisition (manifest → dispatch groups → report).

---

## Quickstart

```bash
# 1. Environment (conda, Python 3.11)
conda env create -f environment.yml
conda activate iconocracy

# 2. Browse the corpus: no build needed; open the file in any browser
#    corpus/DASHBOARD_CORPUS.html   (or corpus/index.html)

# 3. Validate the data
python tools/scripts/validate_schemas.py

# 4. Preview the records → public projection diff
python tools/scripts/records_to_corpus.py --diff

# 5. Check endurecimento coding progress
python tools/scripts/code_purification.py --status

# 6. Run the tests
pytest tests/
```

Every Python tool is run **from the repo root**: `python tools/scripts/<script>.py`.

**Release gate.** Run these steps in order before any public dataset or site release (see [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md)):

1. Validate `records.jsonl`.
2. Validate `purification.jsonl`.
3. Check authoritative export-field idempotence.
4. Generate and review the evidence traceability report. High-severity issues block the release.
5. Review `code_purification.py --status`.
6. Review `vault_sync.py status` or `diff`.
7. Build a Hugging Face snapshot if the public dataset changes.

`build_hf_release.py` runs steps 1 to 4 itself and refuses count or semantic export drift. Steps 5 and 6 remain explicit scholarly review gates.

---

## Repository layout

```
iconocracy-corpus/
├── corpus/            # Searchable corpus + self-contained HTML dashboards
│   ├── index.html            # Browser search interface
│   ├── corpus-data.json      # Public projection (regenerated, never hand-edited)
│   ├── DASHBOARD_CORPUS.html # Interactive analytical dashboard (Chart.js)
│   └── atlas-iconometrico.html
├── data/
│   ├── raw/                  # Manifests & Drive links ONLY, never binaries (ADR-001)
│   ├── interim/              # Data in transformation
│   └── processed/            # records.jsonl + purification.jsonl (canonical ledgers)
├── tools/
│   ├── scripts/              # ~115 Python automation scripts
│   ├── schemas/              # 9 JSON schemas (master-record, purification-record, IconoCode, WebScout, ...)
│   └── sql/                  # DB migrations for the dual-agent corpus
├── tese/                # Doctoral manuscript, revisions, research notes
│   ├── manuscrito/           # Chapters (Markdown → Pandoc)
│   └── revisoes/             # ABNT + terminological audits
├── notebooks/           # Analysis 01-08 (exploratory → Kruskal-Wallis → regression
│                        #   → correspondence → temporal → clustering → dimensionality
│                        #   → multidimensional scoring)
├── vault/               # Obsidian vault (candidatos/ catalog cards, templates, tese/ build)
├── atlas/               # Navigable knowledge graph over the monorepo
├── iconocracy-ingest/   # Ingestion pipeline for scanned archival material (BND, Câmara, Senado, Internet Archive)
├── docs/                # Specs, ADRs, decisions, operating model, workflows
├── deploy/              # Companion app, CV course site, studio, HF Space, Docker, mockups
├── tests/               # pytest suite (~40 test files)
├── wiki/ · concepts/ · entities/ · sources/ · biblio/ · archive/   # Research notes and historical material
├── environment.yml · requirements.txt · CITATION.cff · LICENSE
```

---

## Thesis architecture

The working architecture is **Arquitetura C**, chosen on 2026-09-08. Like everything in the thesis, it is provisional. The thesis is a theoretical proposition, demonstrated through a documentary series, with the image corpus in a declared auxiliary role.

- **Proposition.** Feminine abstraction organizes reality and distributes authority. Drawing on Olivecrona, feminist theory and historical iconology, the thesis argues that this capacity does not depend on reference: the allegory works through vacuity rather than fidelity, and it becomes restrictive when the abstraction turns into a prescriptive model of recognition.
- **Documentary series.** Acts in which the attribute appears as a reason for decision: statutes, legal opinions, rulings and explanatory memoranda.
- **Role of the image corpus.** It shows the availability and circulation of the figure, describes the French and Brazilian strata, and dates the iconographic series.
- **Scope.** France and Brazil, 1850-1929. The corpus itself stays transnational.

The earlier four-case plan (Brasil-República, Brasil-Tribunais, França-Marianne, UK-Britannia) in [`docs/PLANO-TESE-ICONOCRACIA.md`](docs/PLANO-TESE-ICONOCRACIA.md) predates this decision. The current continuity briefing is [`docs/BRIEFING-GPT-Astra6-espinha-tese.md`](docs/BRIEFING-GPT-Astra6-espinha-tese.md).

---

## Data model & traceability

Authority is assigned by field family rather than by a linear ranking ([ADR-006](docs/adr/006-canonical-field-ownership-and-projections.md)):

| Field family | Authority |
|---|---|
| Item identity, source evidence, descriptive metadata, IconoCode claims | `data/processed/records.jsonl` |
| *Endurecimento* observations, coder, round, instrument version, adjudication | `data/processed/purification.jsonl` |
| Raw binary identity and external storage location | `data/raw/drive-manifest.json` + Google Drive |
| Catalogue notes and research navigation | `vault/candidatos/` (auxiliary mirror) |

`corpus-data.json`, SQLite, CSV, dashboards and Hugging Face bundles are **disposable projections**. They must be rebuildable from the ledgers, so **never hand-edit `corpus-data.json`**; edit the source and regenerate with `records_to_corpus.py`.

Public-projection fields are `id`, `title`, `date`, `country`, `motif`, `regime`, `support`, `description`, `url`, `indicadores`, `endurecimento_score` (legacy), `citation_abnt`, `coded_at`, `coded_by` and `audit_flags`. Qualitative coding fields (`subtipo`, `familia_alegorica`, `vetor_colonial`, `hipotese_racial`, …) remain available in the public, CC BY 4.0-licensed canonical artifact `data/processed/records.jsonl`, nested under `purificacao`; they are intentionally omitted from the streamlined `corpus/corpus-data.json` interface projection.

**Traceability rule.** Every item exists in three places: Google Drive (+ `data/raw/drive-manifest.json`) · a vault card in `vault/candidatos/` · a master record in `records.jsonl`. Per **ADR-001**, `data/raw/` stays metadata-only in git; binaries live on Google Drive.

**CI.** The `Validate Schemas` workflow (`.github/workflows/validate.yml`) validates both ledgers against their schemas, checks record and projection counts, checks export idempotence, validates the traceability report, shows coding status, rejects binaries in `data/raw/`, and runs the test suite.

**Versioning.** Any analysis cited in academic text must reference an immutable commit or an existing release tag. No `v0.2` tag has been published; `v1.0` remains reserved for the qualification version. See [`CHANGELOG.md`](CHANGELOG.md).

---

## Known issues and honest numbers

The project audits itself. These findings come from a recount at commit `e86cb37`.

- **Coding coverage needs provenance-aware interpretation.** `code_purification.py --status` reports 286 of 335 items coded (85%). Of the 77 all-zero observations, 76 are inherited placeholders—57 from `vault-import` and 19 from `migration`—where zero means "pending" under [ADR-006](docs/adr/006-canonical-field-ownership-and-projections.md). The remaining row, `SCOUT-571`, is a genuine manual observation by `ana`, with timestamp and notes, and is not import debt.
- **Regime counts differ between ledgers.** The records ledger gives 163 / 103 / 54 / 15 across 335 items; `purification.jsonl` gives 149 / 99 / 28 / 10 across 286 observations. The two have not been reconciled.
- **Some ids do not join.** Ten coding ids do not resolve to a record through the id crosswalk, and two (`FR-007`, `US-011`) are not in the public projection.
- **The period window is not a hard gate in the data.** Dated items span 1239 to 2021; 227 of the 294 items with a year fall inside 1800-2000.
- **URLs.** Six records still carry placeholder URLs (`FR-036`, `FR-038`, `FR-039`, `FR-040`, `FR-047`, `FR-048`), and four URLs are shared by nine records as dedup candidates.
- **Legacy composite.** The exported `endurecimento_score` copies the retired composite, and notebooks 01-05 and 08 still read it.
- **Stale copies.** `corpus/companion-data.json` is frozen at an older 165-item snapshot (May 2026).
- **Country labels are mixed.** The `country` field combines full names, an ISO code (`CL`) and compound labels such as "France (held in Austria)".
- **Iconclass caution.** `48C51` is an internal project label. On iconclass.org it means painting; the official codes for the juridical cut are **44** (*state; law; political life*) and **11M44** (*Justitia*).
- Historical artifacts that cite N=145 or N=165 are **analysis snapshots, not errors**.

---

## Related resources

- 🤗 **Hugging Face dataset:** [warholana/iconocracy-corpus](https://hf.co/datasets/warholana/iconocracy-corpus)
- 🌐 **Project site (Mnemosyne Viva):** [iconocracia.com](https://iconocracia.com)
- 📊 **Analytical dashboard:** [dashboard.iconocracia.com](https://dashboard.iconocracia.com)
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

Code and tools: **MIT** ([`LICENSE`](LICENSE)). Corpus metadata: **CC BY 4.0** ([`LICENSE-DATA`](LICENSE-DATA)). Individual images are subject to the rights indicated in each entry.
