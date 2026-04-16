# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Monorepo for the doctoral thesis **"ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"** (PPGD/UFSC, Ana Vanzin, defense 2026). Integrates a searchable corpus of 145+ female allegorical figures, research automation, statistical analysis, Obsidian vault, and the thesis manuscript.

---

## Quick Commands

```bash
# Environment
conda activate iconocracy                          # Python 3.10+ environment

# Validation & corpus
python tools/scripts/validate_schemas.py           # validate all JSON schemas
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/code_purification.py --status  # ENDURECIMENTO coding progress
python tools/scripts/code_purification.py --export-csv  # regenerate corpus_dataset.csv

# Corpus sync pipeline
python tools/scripts/vault_sync.py status          # vault ↔ records.jsonl state
python tools/scripts/vault_sync.py sync            # bidirectional sync
python tools/scripts/records_to_corpus.py --diff   # preview records → corpus-data.json changes

# ARGOS acquisition workflow
python tools/scripts/argos_build_manifest.py       # build pending acquisition manifest
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json  # derive dispatch groups
python tools/scripts/argos_report.py               # render markdown acquisition report

# Thesis compilation (Pandoc)
make -C vault/tese/ docx                           # full thesis → DOCX
make -C vault/tese/ pdf                            # full thesis → PDF (requires LaTeX)

# Web apps
cd webiconocracy && npm run dev                    # React corpus explorer (port 3000)
```

---

## Architecture

### Dual-Agent Pipeline

```
WebScout (archive discovery) → IconoCode (visual analysis) → master records
```

- **WebScout** queries digital archives (Europeana, Gallica, LOC, BnF, Numista, Colnect)
- **IconoCode** performs 3-level Panofsky analysis + 10 ENDURECIMENTO indicators (0–3 scale)
- Output: `data/processed/records.jsonl` (canonical) → `corpus/corpus-data.json` (public export)

### Canonical Data Hierarchy (source-of-truth order)

1. `data/processed/records.jsonl` — operational canonical ledger
2. `corpus/corpus-data.json` — public-facing export (browsers, dashboards, HF releases)
3. `data/processed/purification.jsonl` — ENDURECIMENTO coding ledger
4. `vault/candidatos/` — auxiliary cataloguing mirror only

### Key Directories

```
corpus/             → corpus-data.json + HTML dashboards (index.html, DASHBOARD_CORPUS.html)
data/raw/           → metadata-only in git (binaries → Google Drive / SSD, per ADR-001)
data/processed/     → records.jsonl, purification.jsonl (canonical ledgers)
vault/candidatos/   → Obsidian SCOUT notes (XX-NNN pattern, e.g. FR-013 Déclaration des droits.md)
vault/sessoes/      → session summary notes (SCOUT-SESSION-YYYY-MM-DD.md)
tese/manuscrito/    → thesis chapters (Markdown, compiled via Pandoc)
tools/scripts/      → Python automation scripts (50+; see tools/scripts/ for full list)
tools/schemas/      → JSON schemas (master-record, iconocode-output, webscout-input/output)
notebooks/          → sequential analysis (01_exploratory → 02_kruskal_wallis → 03_regression → 04_correspondence)
webiconocracy/      → React+Vite+Firebase corpus explorer
indexing/           → Gallica MCP server, corpus-scout-agent
deploy/             → Cloudflare Workers companion, HF Space
```

### CI/CD (`.github/workflows/validate.yml`)

Validates `records.jsonl` against `tools/schemas/master-record.schema.json`, checks consistency with `corpus-data.json`, and **rejects binary files in `data/raw/`** (ADR-001).

---

## Hooks (`.claude/settings.json`)

Active automation:
- **SessionStart**: checks SSD mount (`/Volumes/ICONOCRACIA`), reports corpus item count
- **PreToolUse**: blocks edits to `tese/manuscrito/*_original` files; enforces vault note naming (`XX-NNN Title.md`)
- **PostToolUse**: auto-stages vault notes to git; validates `corpus-data.json` schema on edit; regenerates CSV; counts thesis chapter words; checks Python syntax
- **PreCompact**: preserves corpus IDs, Iconclass codes, ENDURECIMENTO scores, and ongoing campaigns

---

## Mandatory Terminology

| Term | Rule |
|------|------|
| **ENDURECIMENTO** | Always in Portuguese. NEVER "hardening" or "embrutecimento" |
| **Contrato Sexual Visual** | Original thesis concept — do NOT attribute to Pateman |
| **Feminilidade de Estado** | Original thesis concept — do NOT attribute to Mondzain |
| **Pathosformel**, **Zwischenraum**, **Nachleben** | Warburg — always in German |
| **Mondzain** | Always 2002 edition |
| **ABNT NBR 6023:2025** | Citation standard for all references |
| **Iconclass 48C51** | Key code for feminist iconography |

---

## Corpus Parameters

**Countries:** FR (Marianne, La République, La Justice, La Liberté) · UK (Britannia, Justice, Hibernia, Scotia) · DE (Germania, Justitia, Minerva) · US (Columbia, Lady Justice, Liberty, America) · BE (La Belgique) · BR (A República, A Justiça)

**Supports:** moeda · selo · monumento/escultura · arquitetura forense · estampa/gravura · frontispício · papel-moeda · cartaz

**Period:** 1800–2000 (priority: 1880–1920)

**Three iconocratic regimes:** FUNDACIONAL (sacrificial, body alive) → NORMATIVO (domesticated, bureaucratic) → MILITAR (hardened, imperial)

**10 purification indicators** (ordinal 0–3): desincorporação · rigidez_postural · dessexualização · uniformização_facial · heraldicização · enquadramento_arquitetônico · apagamento_narrativo · monocromatização · serialidade · inscrição_estatal

**Inclusion criteria** (all 5 required): female allegorical figure + explicit juridical-political function + datable 1800–2000 + one of 6 countries + accepted support

---

## Mode Routing & Shortcut Commands

The agent dispatches by trigger keywords (full spec: `ICONOCRACY_MASTER_PROMPT.md` §C). Execute directly without confirmation:

| Trigger | Mode | Action |
|---------|------|--------|
| `scout [query]`, `campanha N`, `buscar`, `lacunas`, `auditoria` | SCOUT | Archive search, Obsidian note generation, gap analysis |
| `argos`, `acquisition`, `orquestrar aquisicao`, `orquestrar aquisição` | ARGOS | Build manifest, prepare dispatch groups, coordinate acquisition workflow |
| `codificar`, `iconocode`, `analisar imagem`, or image received | ICONOCODE | 3-level Panofsky + 10 indicators |
| `compilar`, `make tese`, `gerar PDF` | COMPILAR | Markdown → PDF via Pandoc |
| `validar [file]` | VALIDAR | JSON schema validation (`validate_schemas.py`) |
| `sync vault pull/push/sync/diff/status` | SYNC | Bidirectional vault ↔ records sync (`vault_sync.py`) |
| `purificacao status/item/lote/exportar` | PURIFICAÇÃO | ENDURECIMENTO coding (`code_purification.py`) |
| `pesquisar`, `lit review`, `revisão de literatura` | PESQUISAR | Deep academic research |
| `redigir`, `draft`, `escrever capítulo` | REDIGIR | Academic writing |
| `revisar`, `peer review` | REVISAR | Multi-perspective review |
| `zwischenraum`, `painel comparativo` | ZWISCHENRAUM | Warburg comparative panels |
| `salvar` | — | Save last note to `vault/candidatos/` |
| `sessão` | — | Save session summary to `vault/sessoes/` |

---

## Vault Tags

Namespaced prefixes: `corpus/`, `pais/` (BR, FR, UK, DE, US, BE), `suporte/` (moeda, selo, monumento, estampa, frontispicio, papel-moeda, cartaz), `regime/` (fundacional, normativo, militar), `motivo/` (marianne, republica, justitia, britannia, columbia, germania, belgique). Flags: `#verificar`, `#possivel-duplicata`, `#contra-alegoria`, `#ausencia-alegorica`, `#colonialidade-do-ver`, `#contrato-racial-visual`.

---

## Traceability Rule

Every corpus item must exist in three places:

| Location | Content |
|----------|---------|
| Google Drive + `data/raw/drive-manifest.json` | Raw image origin + item_id link |
| `vault/candidatos/` | Obsidian note with metadata and analysis |
| `data/processed/records.jsonl` | Canonical master record |

---

## Key Conventions

- All Python scripts run from repo root: `python tools/scripts/<script>.py`
- Never use `sed` or partial edits on JSON config files — rewrite entirely with `Write`
- For `corpus-data.json`, use Python scripts for atomic updates rather than direct Edit
- `data/raw/` must remain metadata-only in git (ADR-001: Google Drive stores binaries)
- Vault notes follow pattern `XX-NNN Title.md` where XX = country code, NNN = sequential number (e.g., `FR-013 Déclaration des droits.md`)
- All generic vault notes in `vault/**/*.md` should default to **Obsidian Flavored Markdown**: frontmatter properties, `[[wikilinks]]`, `![[embeds]]`, callouts, comments, highlights, and external URLs only as Markdown links
- Canonical vault guide: `vault/meta/Guia — Obsidian Flavored Markdown.md`; generic default template: `vault/_templates/nota-obsidian-padrao.md`
- Thesis original files (`*_original`) are protected — use `vault/tese/` for revised drafts
- SSD `/Volumes/ICONOCRACIA` stores raw images, Zotero PDFs, and backups
- Automatic vault backups must not land on `main` (use `vault_backup.py`)
- Academic voice: formal Portuguese with jurídico-penal framing (legal-criminal history, NOT anthropological/sociological)

---

## Release Gate

Before public release: `validate_schemas.py` → `code_purification.py --status` → `vault_sync.py status` → `records_to_corpus.py --diff` → `build_hf_release.py`. See `docs/OPERATING_MODEL.md` for full policy.

---

## Skills for this workspace

Curated skills Claude should prefer inside the thesis hub. Global + `find-skill` still apply.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `iconocracy-agent` | Default umbrella — orchestrates corpus research, coding, compile, progress |
| `compilar-tese` | Direct thesis compile (DOCX/PDF) when bypassing the agent |
| `validate-corpus` | Quick schema check after editing `corpus/corpus-data.json` |

### Branches (when bypassing the agent)
- `corpus-scout` · `iconocode-analyze` · `iconocode-batch` · `thesis-progress` · `citation-management` · `dir410346`

### Review agents (subagent dispatch)
- `abnt-checker` · `thesis-reviewer` · `chapter-integrity` · `iconclass-reviewer` · `iconocode` · `corpus-dedup`
