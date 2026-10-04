<p align="center">
  <img src="docs/brand/banner.svg" alt="ICONOCRACIA: female allegory, legal culture, sources and images" width="100%">
</p>

# ICONOCRACIA

**Alegoria Feminina como Operador Epistêmico da Legitimidade Jurídica**

*Feminine Allegory as an Epistemic Operator of Juridical Legitimacy*

Doctoral research in legal history and legal iconography by **Ana Vanzin**, PPGD/UFSC (Federal University of Santa Catarina).

This repository brings together images, source records, historical-legal research, comparative panels and the thesis manuscript. The research examines how female allegories participate in the recognition of legal and political authority, and how that visual authority relates to the legal position of concrete women.

[Research environment: iconocracia.com](https://iconocracia.com) · [Corpus dashboard](https://dashboard.iconocracia.com) · [Dataset snapshots](https://hf.co/datasets/warholana/iconocracy-corpus)

<p align="center"><img src="docs/brand/rule.svg" alt="" width="100%"></p>

## Contents

- [Research question and working scope](#research-question-and-working-scope)
- [Images, objects and sources](#images-objects-and-sources)
- [Method and interpretive limits](#method-and-interpretive-limits)
- [Corpus snapshot](#corpus-snapshot)
- [Where to work and consult](#where-to-work-and-consult)
- [Data authority and traceability](#data-authority-and-traceability)
- [Research assistance](#research-assistance)
- [Local setup and checks](#local-setup-and-checks)
- [Citation and reuse](#citation-and-reuse)

## Research question and working scope

**Working question:** how does a female allegorical figure become a condition for recognizing juridical authority, and how does that process bear on the women whose legal autonomy is at stake?

The current working direction is a genealogy centred on **Brazil, 1822–1922**, with European material used for historical comparison. The thesis title and direction are recorded in [CLAUDE.md](CLAUDE.md); the manuscript and case selection remain in development.

The **corpus is open and transnational**. Its chronology extends beyond the thesis focus, allowing earlier and later objects to serve as comparanda. Inclusion in the research catalogue does not establish that an item belongs in the thesis's documentary demonstration.

Images and their source records help document the availability, circulation and transformation of a figure. Claims about legal prescription, exclusion or reception require historical evidence appropriate to each claim: legislation, institutional records, production and commission documents, contemporary texts and other sources read alongside the object.

## Images, objects and sources

The catalogue includes **coins, stamps, monuments and sculpture, courthouse architecture, prints, frontispieces, banknotes and posters**. Justice, the Republic, Marianne, Britannia, Columbia and related figures are read through their specific objects, uses and documentary contexts.

Sources include Gallica/BnF, Europeana, the Library of Congress, Brasiliana Fotográfica, the Hemeroteca Digital Brasileira, Biblioteca Nacional Digital (Portugal) and other institutional collections.

For each object, research connects the image to its catalogue record and available documentation: attribution, date, support, inscription, place of production or use, collection identifier, source URL and rights information. Uncertain metadata and interpretive claims retain their verification status.

The site is a research environment for finding, comparing and revisiting these materials. GitHub and Hugging Face support provenance, collaboration and access to dated derivatives.

## Method and interpretive limits

Analysis combines **Panofsky's three levels** of description, iconographic identification and iconological interpretation with **Warburgian comparison and montage**: *Pathosformel*, *Nachleben* and *Zwischenraum*. The historical-legal argument depends on source criticism and documented relations between objects.

**Iconometria** provides a descriptive framework for organizing iconographic observations. **Endurecimento** is its axis of fixity, documented through a verbal inventory of attributes and ten ordinal indicators:

| Indicator | English gloss |
|---|---|
| desincorporação | disembodiment |
| rigidez_postural | postural rigidity |
| dessexualização | desexualization |
| uniformização_facial | facial uniformization |
| heraldicização | heraldic abstraction |
| enquadramento_arquitetônico | architectural framing |
| apagamento_narrativo | narrative erasure |
| monocromatização | monochromatization |
| serialidade | seriality |
| inscrição_estatal | state inscription |

The indicators retain their **0–3 ordinal scale** and require contextual interpretation. Comparisons use regime labels such as **FUNDACIONAL**, **NORMATIVO**, **MILITAR** and **CONTRA-ALEGORIA**, whose applicability must be justified for each object.

The [2026-07-28 decision](docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md) retired the composite index as a probatory claim. The [2026-09-24 decision, updated on 2026-09-29](docs/decisions/2026-09-24-remocao-definitiva-do-campo.md) removed `endurecimento_score` and composite fields from the active ledgers and exports. Historical sources retain their dated status.

Current coding requires a **verbal attribute inventory** alongside the separate ordinal observations. Inventory coverage remains partial, so undocumented qualitative claims remain pending. Sums, means, attribute counts and density do not substitute for the retired composite or rank the atlas.

The [methodological decision of 2026-07-31](docs/decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md) defines the corpus as a documented catalogue and the indicators as interpretive *capta*. The [2026-09-22 audit](docs/decisions/2026-09-22-auditoria-camada-inferencial.md) maintains descriptive iconometria and freezes **notebooks 02–08** as exploratory artifacts for internal diagnosis. **Notebook 01** remains the descriptive notebook.

The thesis develops four authorial concepts: **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual** and **Purificação Clássica**.

## Corpus snapshot

**File count, 2026-10-04, source commit [`33132b3`](https://github.com/anavvanzin/iconocracy-corpus/commit/33132b3485629183d7378c674c67cd8136d53ce1).** These figures describe that repository version, rather than a frozen dataset release.

| File | Entries |
|---|---:|
| [`records.jsonl`](data/processed/records.jsonl): item records | 337 |
| [`purification.jsonl`](data/processed/purification.jsonl): coding observations | 286 |
| [`corpus-data.json`](corpus/corpus-data.json): public projection | 337 |

A coding observation is not interchangeable with an item: the model allows multiple observations per item, and historical imports require their own evidence review. These counts do not establish complete coding coverage or verified image availability. The [field-ownership decision](docs/adr/006-canonical-field-ownership-and-projections.md) documents the distinction between observed zeros and pending coding.

Any quantitative description used in academic writing should identify its dated source files and version. Historical counts elsewhere in the repository belong to their respective snapshots.

## Where to work and consult

| Resource | Research use |
|---|---|
| [`tese/manuscrito/`](tese/manuscrito/) | Thesis chapters and working text |
| [`vault/candidatos/`](vault/candidatos/) | Catalogue notes and object dossiers |
| [`atlas/`](atlas/) | Relations between objects and research notes |
| [`data/processed/`](data/processed/) | Canonical item and coding ledgers |
| [`corpus/`](corpus/) | Derived interfaces and exports |
| [`docs/decisions/`](docs/decisions/) | Dated methodological decisions |
| [`tools/scripts/`](tools/scripts/) | Validation, acquisition and export tools |
| [`notebooks/`](notebooks/) | Descriptive work and archived exploratory analyses |

For local consultation, open [`corpus/index.html`](corpus/index.html), [`corpus/DASHBOARD_CORPUS.html`](corpus/DASHBOARD_CORPUS.html) or [`corpus/atlas-iconometrico.html`](corpus/atlas-iconometrico.html). Their embedded data and analytical displays should be read with their snapshot and methodological status in mind.

Related research environments:

- [iconocracia.com](https://iconocracia.com): editorial and visual consultation.
- [dashboard.iconocracia.com](https://dashboard.iconocracia.com): corpus dashboard.
- [Hugging Face dataset](https://hf.co/datasets/warholana/iconocracy-corpus): dated public derivatives.
- [`deploy/iconocracia-cv/`](deploy/iconocracia-cv/): computer-vision course materials and dataset audit.
- [Research meta-workspace](https://github.com/anavvanzin/Research): coordination and workflow documentation.

## Data authority and traceability

Authority is assigned **by field family**, as specified in [ADR-006](docs/adr/006-canonical-field-ownership-and-projections.md):

| Field family | Authority |
|---|---|
| Item identity, source evidence, descriptive metadata and IconoCode claims | `data/processed/records.jsonl` |
| Endurecimento observations, coder, round, instrument version and adjudication | `data/processed/purification.jsonl` |
| Raw binary identity and storage location | `data/raw/drive-manifest.json` + Google Drive |
| Catalogue notes and research navigation | `vault/candidatos/`, an auxiliary mirror |

`corpus-data.json`, SQLite, CSV, dashboards, notebook inputs and Hugging Face bundles are **derived projections**. Rebuild them from their authoritative sources; changes to the public export go through `records_to_corpus.py`.

Qualitative fields such as `subtipo`, `familia_alegorica`, `vetor_colonial` and `hipotese_racial` remain publicly available under `purificacao` in the canonical `records.jsonl` artifact. They are intentionally omitted from the streamlined `corpus-data.json` interface projection.

The traceability contract connects each item to its image and storage manifest, catalogue note and master record. Raw image files are held outside Git; `data/raw/` contains metadata and manifests. This contract is a requirement to verify, rather than a claim that every existing item has completed acquisition and documentation.

## Research assistance

```text
WebScout → candidate and source evidence
IconoCode → visual description and interpretive coding
Research review → canonical ledgers → derived interfaces
```

**WebScout** assists archive discovery and metadata collection. **IconoCode** assists visual description and coding. Candidate records and agent-generated interpretations require research review and supporting evidence before being treated as validated claims.

**ARGOS** supports image acquisition through manifests, dispatch groups and acquisition reports. These tools serve the investigation of objects and sources.

## Local setup and checks

The environment specification is [`environment.yml`](environment.yml). Run the following from the repository root:

```bash
conda env create -f environment.yml
conda activate iconocracy

python tools/scripts/validate_schemas.py
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
```

The HTML corpus interfaces can be consulted directly. The [operating model](docs/OPERATING_MODEL.md) describes the validation, export-consistency and evidence-traceability gates for a public release.

For manuscript compilation, use the Makefile in [`vault/tese/`](vault/tese/):

```bash
make -C vault/tese/ docx
```

Project guidance: [AGENTS.md](AGENTS.md) · [CLAUDE.md](CLAUDE.md) · [Workflow](docs/WORKFLOW.md).

## Citation and reuse

Use [`CITATION.cff`](CITATION.cff) for the dataset's citation metadata, identifying the version or snapshot used. A citation of the corpus does not establish a completed or defended thesis.

Code and tools: **MIT**, under [`LICENSE`](LICENSE). Corpus metadata and datasets: **CC BY 4.0**, under [`LICENSE-DATA`](LICENSE-DATA). Images retain the rights recorded for each source item.

References follow **ABNT NBR 6023:2025** in Portuguese and Chicago in English.

<p align="center"><img src="docs/brand/rule.svg" alt="" width="100%"></p>

<p align="center">
  <sub><strong>ICONOCRACIA</strong> · Ana Vanzin · PPGD/UFSC</sub>
</p>
