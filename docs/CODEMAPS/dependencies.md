<!-- Generated: 2026-06-22 | Files scanned: deploy/, .github/workflows/, env | Token estimate: ~700 -->
# Dependencies — env, services, integrations, deploy, CI

## Runtime
- **conda env `iconocracy`** (Python **3.11** per `environment.yml`; rebuilt 3.12→3.11 2026-06-22). Use version-agnostic `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python` — NOT a pinned `python3.12`/`python3.11`. NEVER system Python; NEVER the SSD env (Linux build → exec format error on macOS).
- Node/npm present (`node_modules/`) for deploy tooling.

## External archives (acquisition sources)
Gallica (BnF) · Library of Congress · Europeana · Numista · Colnect · Rijksmuseum · museum/IIIF endpoints (Heidelberg, Munich, SMK, V&A, Met, bildindex, DHM). IIIF via `enrich_iiif.py` (Gallica/Europeana/LoC strategies); image-extraction fallback via firecrawl scrape/search.

## MCP servers (session-connected)
- `corpus-vault` (filesystem → `vault/`) · `iconclass-db` (sqlite → `shared/iconclass-data/iconclass_index.sqlite`)
- `firecrawl` (web scrape/search/research) · `context7` (library docs) · `github` · `playwright` · `firebase` · `proxyman` · GitKraken
- (Cloudflare, HuggingFace = "needs authentication"; gemini CLI present but needs browser auth)

## Deploy targets (`deploy/`)
- `iconocracia-companion/` — **Cloudflare Worker** (public corpus companion; `sync_companion.py` feeds `companion-data.json`)
- `huggingface/corpus-explorer-space/` — HF Space (built via `build_hf_release.py`)
- `docker/` — `mcp.Dockerfile`, `thesis.Dockerfile`, `tools.Dockerfile`, `web.Dockerfile`
- `tropical-atlas/`

## CI (`.github/workflows/`)
- `validate.yml` — records.jsonl schema + records↔corpus consistency + **reject binaries in data/raw** (ADR-001)
- `claude.yml`, `claude-code-review.yml` — Claude automation
- `codeql.yml`, `crda.yml`, `jscrambler-code-integrity.yml`, `datadog-synthetics.yml` — security/QA
- `deploy.yml`

## Issue tracker
GitHub Issues @ `anavnzin/iconocracy-corpus` via `gh` CLI (labels: needs-triage, ready-for-agent, …).

## Key conventions (see CLAUDE.md)
- `data/raw/` metadata-only (ADR-001: binaries → Google Drive / SSD `/media/ana/SSD_DATA`)
- Citations: ABNT NBR 6023:2025 · Iconclass 48C51 = feminist iconography
- Mandatory terminology: Endurecimento (PT) · Purificação Clássica · Contrato Sexual Visual · Feminilidade de Estado · Pathosformel/Zwischenraum/Nachleben (DE)
