# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monorepo for the doctoral research project **"Iconocracy: Female Allegory in the History of Legal Culture (19th–20th c.)"** at PPGD/UFSC (Ana Vanzin, 2026). Combines a searchable iconographic corpus, data processing tools, statistical analysis notebooks, and web applications.

## Key Commands

```bash
# Python environment
conda activate iconocracy                     # or: pip install -r requirements.txt
python tools/scripts/validate_schemas.py      # validate JSON against dual-agent schemas
python tools/scripts/validate_schemas.py examples/batch_001/master_record_*.json  # validate specific files

# Purification coding CLI
python tools/scripts/code_purification.py                  # code next uncoded item
python tools/scripts/code_purification.py --status         # show coding progress
python tools/scripts/code_purification.py --export-csv     # export corpus_dataset.csv

# Notion sync (requires NOTION_API_KEY + NOTION_CORPUS_DB_ID env vars)
python tools/scripts/notion_sync.py pull      # Notion → JSONL
python tools/scripts/notion_sync.py push      # JSONL → Notion
python tools/scripts/notion_sync.py sync      # bidirectional

# Iconclass data processing
python tools/scripts/extract_feminist_network.py   # extract 48C51 subnetwork
python tools/scripts/make_sqlite.py                # build SQLite from Iconclass textbase

# webiconocracy (React + Vite + Firebase app)
cd webiconocracy && npm install && npm run dev     # dev server on port 3000
cd webiconocracy && npm run build                  # production build
cd webiconocracy && npm run lint                   # TypeScript type check (tsc --noEmit)

# Gallica MCP server
cd indexing/gallica-mcp-server && npm install && npm run dev   # dev with tsx watch
cd indexing/gallica-mcp-server && npm run build                # compile TS → dist/

# Website deployment (automatic on push to main)
# Deploys website/ directory to GitHub Pages via .github/workflows/deploy.yml
```

## Architecture

### Dual-Agent Corpus Builder Pipeline

The core data architecture (`docs/dual-agent-corpus-builder.md`) uses two AI agents in sequence:

1. **WebScout** — contextual researcher that searches archives (Europeana, Gallica, Brasiliana Fotográfica, etc.) using 3-layer search packs (vocabularies → image databases → legal/history collections)
2. **IconoCode** — visual coder that performs 4-stage analysis: pre-iconographic description → Iconclass code assignment → interpretation → validation with claim-evidence ledger

Pipeline flow: batch manifest → WebScout workers → IconoCode workers → master record assembly → export (JSONL, CSV, ABNT citations). Schemas in `tools/schemas/` define the data contracts (JSON Schema 2020-12).

### Data Flow & Storage (ADRs in `docs/adr/`)

- **Raw data** lives on Google Drive, never in Git (ADR-001). `data/raw/` holds manifests and Drive links only.
- **Notion** is the collaborative index (ADR-002). Sync via `notion_sync.py`.
- **JSONL** (`data/processed/records.jsonl`) is the canonical format (ADR-003).
- The CI workflow rejects binary files in `data/raw/` — use Drive instead.

### Corpus Dataset

`corpus/corpus-data.json` — 66 catalogued items of feminist legal iconography. Fields: id, title, date, period, creator, institution, source_archive, country, medium, motif, description, url, thumbnail_url, rights, citations, tags.

`corpus/DASHBOARD_CORPUS.html` — self-contained interactive dashboard (Chart.js). Open directly in browser.

### Statistical Analysis Notebooks (`notebooks/`)

Sequential analysis pipeline: `01_exploratory` → `02_kruskal_wallis` → `03_regression` → `04_correspondence`. Requires conda environment (numpy, matplotlib, jupyter).

### Web Applications

- **webiconocracy/** — React 19 + TypeScript + Vite + Tailwind CSS 4 + Firebase/Firestore. Interactive corpus explorer with Gemini AI integration (`@google/genai`). Run with `npm run dev`.
- **website/** — Static HTML site for Ius Gentium research group. Auto-deployed to GitHub Pages on push to main.
- **indexing/gallica-mcp-server/** — MCP server (Node.js + TypeScript) for querying Gallica/BnF APIs. Uses `@modelcontextprotocol/sdk`.
- **atlas-iconometrico.html** — Standalone interactive atlas page (root level).

### Thesis Materials (`tese/`)

- `manuscrito/` — Chapters under revision (see `LEIAME.md` for supervisor-facing guide)
- `revisoes/` — Review documents (ABNT audit, source-claim alignment, terminological corrections)
- `pesquisa/` — NotebookLM research reports

### Vault (`vault/`)

Obsidian vault for research notes. Workspace/plugin files are gitignored. Output from `vault/tese/output/` is also gitignored.

## CI/CD

- **GitHub Pages deploy** (`deploy.yml`) — deploys `website/` on push to main
- **Schema validation** (`validate.yml`) — runs `validate_schemas.py` on changes to `data/processed/` or `tools/schemas/`; rejects binaries in `data/raw/`
- **CodeQL** (`codeql.yml`) — code quality analysis
- **Datadog Synthetics** (`datadog-synthetics.yml`) — monitoring
- **Google Cloud Run** (`google-cloudrun-docker.yml`) — Docker deployment pipeline

## Session Hook

`.claude/hooks/session-start.sh` runs on remote Claude Code sessions only (`CLAUDE_CODE_REMOTE=true`). It installs Python deps, verifies 13+ required directories, validates key data files (corpus JSON integrity, 66 items), and checks external tool availability.

## Important Conventions

- All Python scripts run from repo root: `python tools/scripts/<script>.py`
- Citations follow ABNT NBR 6023:2025 standard (Brazilian academic norm)
- Iconclass notation system is used throughout — `48C51` is the key code for feminist iconography
- The `iconocracy-corpus/` subdirectory is a nested copy of the same repo (for GitHub Pages structure) — avoid editing files there directly
- Research documents (`.md` files at root level like `Iconocracia_Sintese_de_Pesquisa.md`, `ICONOCRACIA_PROJETO.md`) are Portuguese-language research notes
