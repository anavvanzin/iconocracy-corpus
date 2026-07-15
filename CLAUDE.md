# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Quick-reference companion:** [`AGENTS.md`](AGENTS.md) — essential commands, counts, and guardrails in a compact card for any agent.

## Project

Monorepo for the doctoral thesis **"ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"** (PPGD/UFSC, Ana Vanzin, defense 2026). Integrates a searchable, **open and growing** corpus of female allegorical figures (recent working snapshot ~328 records in `records.jsonl`; **N is intentionally non-fixed** — exploratory posture, see *Known Data Issues* §3), research automation, statistical analysis, Obsidian vault, and the thesis manuscript.

> **Master plan**: `docs/PLANO-TESE-ICONOCRACIA.md` — comprehensive thesis architecture, methodology, case rankings, risk matrix, 24-month work plan, and 10 immediate decisions.

**Parent CLAUDE.md context** (do not duplicate; read on demand):
- `~/Documents/CLAUDE.md` — host layout, stale `/data/` → `~/Documents/` migration, location of binary drop zone `iconocracy-corpus/binaries/` (separate from this repo).
- `~/Documents/projetos/research/CLAUDE.md` — meta-workspace conventions (sub-repo containment, where new pipelines/labs/apps go).
- `~/.claude/CLAUDE.md` — user profile, conda env, citation defaults, skill catalogue.

---

## Quick Commands

```bash
# Environment
conda activate iconocracy                          # Python 3.11 env (see environment.yml)

# Validation & corpus
python tools/scripts/validate_schemas.py           # validate all JSON schemas
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/check_thesis_terms.py          # forbidden terms + misattributions
python tools/scripts/code_purification.py --status  # endurecimento coding progress
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
make -C vault/tese/ capitulo-1.docx                # single chapter

# Tests (pytest, no config file — runs from repo root)
pytest tests/                                       # full suite (argos/, tools/, training/ + top-level)
pytest tests/test_corpus_export_idempotent.py -v    # single file
pytest tests/argos/ -k acquisition                  # filter by keyword

# NOTE: webiconocracy React explorer and indexing/gallica-mcp-server were retired
# (directories no longer present in repo; were Mac-era symlinks).
```

---

## Architecture

### Dual-Agent Pipeline

```
WebScout (archive discovery) → IconoCode (visual analysis) → master records
```

- **WebScout** queries digital archives (Europeana, Gallica, LOC, BnF, Numista, Colnect)
- **IconoCode** performs 3-level Panofsky analysis + iconometria measurement (endurecimento = fixity axis, 10 indicators 0–3 scale)
- Output: `data/processed/records.jsonl` (canonical) → `corpus/corpus-data.json` (public export)

### Canonical Data Hierarchy (source-of-truth order)

1. `data/processed/records.jsonl` — operational canonical ledger
2. `corpus/corpus-data.json` — public-facing export (browsers, dashboards, HF releases)
3. `data/processed/purification.jsonl` — endurecimento coding ledger
4. `vault/candidatos/` — auxiliary cataloguing mirror only

### Key Directories

```
corpus/             → corpus-data.json + HTML dashboards (index.html, DASHBOARD_CORPUS.html)
data/raw/           → metadata-only in git (binaries → Google Drive / SSD, per ADR-001)
data/processed/     → records.jsonl, purification.jsonl (canonical ledgers)
vault/candidatos/   → Obsidian SCOUT notes (XX-NNN pattern, e.g. FR-013 Déclaration des droits.md)
vault/sessoes/      → session summary notes (SCOUT-SESSION-YYYY-MM-DD.md)
tese/manuscrito/    → thesis chapters (Markdown, compiled via Pandoc)
tools/scripts/      → Python automation scripts (69; see tools/scripts/ for full list)
tools/schemas/      → JSON schemas (master-record, iconocode-output, webscout-input/output)
notebooks/          → sequential analysis 01–08 (exploratory → kruskal_wallis → regression → correspondence → temporal → clustering → dimensionality → multidimensional_scoring)
deploy/             → Cloudflare Workers companion, HF Space
```

### CI/CD (`.github/workflows/validate.yml`)

Validates `records.jsonl` against `tools/schemas/master-record.schema.json`, checks consistency with `corpus-data.json`, and **rejects binary files in `data/raw/`** (ADR-001).

---

## Hooks (`.claude/settings.json`)

Active automation:
- **SessionStart**: checks SSD mount (`/media/ana/SSD_DATA`), reports corpus item count
- **PreToolUse**: blocks edits to `tese/manuscrito/*_original` files; enforces vault note naming (`XX-NNN Title.md`)
- **PostToolUse**: auto-stages vault notes to git; validates `corpus-data.json` schema on edit; regenerates CSV; counts thesis chapter words; checks Python syntax
- **PreCompact**: preserves corpus IDs, Iconclass codes, endurecimento scores, and ongoing campaigns

---

## Terminology — Reference (NOT enforced during drafting)

> **Não é guardrail (decisão 2026-06-24).** Esta tabela é **referência para polimento perto da defesa**, não regra bloqueante durante a redação exploratória. Não flagrar/corrigir termos ou traduções no rascunho; rodar `check_thesis_terms.py` só quando Ana pedir. Única ressalva digna de nota (gentil, não-bloqueante, perto da defesa): não ceder a autoria dos 4 conceitos originais a Pateman/Mondzain. Ver `~/.claude/CLAUDE.md` §"Thesis Drafting".

| Term | Reference note |
|------|------|
| **Iconometria** | Framework metodológico **guarda-chuva** (decisão 2026-07-11): medição e análise de padrões iconográficos no corpus. **Contém** endurecimento como eixo de fixidez (`iconometria ⊇ endurecimento`). Ver `concepts/iconometria.md` + `docs/decisions/ICONOMETRIA-TRANSITION-2026-07-11.md` |
| **Endurecimento** | Always in Portuguese. NEVER "hardening" or "embrutecimento". **Eixo de fixidez dentro da iconometria** — operacionalização empírica da **Purificação Clássica** via 10 ordinal indicators (0–3). Campo de dados canônico permanece `endurecimento_score` (chave estável; não renomear sem migração coordenada) |
| **Contrato Sexual Visual** | Original thesis concept #1 — do NOT attribute to Pateman (Pateman is the source of the non-visual contract; the visual extension is autoral) |
| **Feminilidade de Estado** | Original thesis concept #2 — do NOT attribute to Mondzain. Genealogical roots: Legendre (juiz totêmico) + Carson (hystéra) |
| **Contrato Racial Visual** | Original thesis concept #3 — branquitude constitutiva da alegoria "universal"; transferência transatlântica de modelos neoclássicos. Cap. 3 |
| **Purificação Clássica** | Original thesis concept #4 — operação formal de extração do feminino histórico para fixá-lo no eterno alegórico. Matriz primária jurídica (Kantorowicz/Legendre/Hespanha); extensão ferramental (Latour 1991 / Haraway 1985 / Descola). Operacionalizada em endurecimento. Cap. 5.2. Use sempre "Purificação Clássica" no manuscrito final, não "purificação iconocrática" |
| **Pathosformel**, **Zwischenraum**, **Nachleben** | Warburg — always in German |
| **Mondzain** | Always 2002 edition |
| **ABNT NBR 6023:2025** | Citation standard for all references |
| **Iconclass 48C51** | Rótulo **interno do projeto** para a sub-rede de iconografia feminista (`extract_feminist_network.py` → `feminist_network_48C51_pt.json`). ⚠ **Não é o rótulo oficial.** No iconclass.org, `48C51` = *"painting (incl. book-illumination, miniature-painting)"*; os códigos oficiais do recorte jurídico são **44** (*state; law; political life*) e **11M44** (*Justitia*). No manuscrito, não afirmar "48C51 = iconografia feminista" como se fosse rótulo oficial do Iconclass — usar 44/11M44 para citações Iconclass. (verificado iconclass.org, 2026-06-26) |
| **"ciberfeminismo"** | NEVER use in thesis text. Reservado para paper derivado pós-defesa. Operadores Haraway/Latour/Descola entram como matriz ferramental de Purificação Clássica, não como filiação a tradição |

---

## Corpus Parameters

**Countries** (variável analítica, **NÃO gate de inclusão** desde 2026-06-22; lista-núcleo não-exaustiva): FR (Marianne, La République, La Justice, La Liberté) · UK (Britannia, Justice, Hibernia, Scotia) · DE (Germania, Justitia, Minerva) · US (Columbia, Lady Justice, Liberty, America) · BE (La Belgique) · BR (A República, A Justiça) · + qualquer país que satisfaça os 4 critérios (AT, NL, DK, ES já no corpus)

**Supports:** moeda · selo · monumento/escultura · arquitetura forense · estampa/gravura · frontispício · papel-moeda · cartaz

**Period:** 1800–2000 (priority: 1880–1920)

**Three iconocratic regimes:** FUNDACIONAL (sacrificial, body alive) → NORMATIVO (domesticated, bureaucratic) → MILITAR (hardened, imperial) → CONTRA-ALEGORIA (subversive, contested)

**10 purification indicators** (ordinal 0–3): desincorporação · rigidez_postural · dessexualização · uniformização_facial · heraldicização · enquadramento_arquitetônico · apagamento_narrativo · monocromatização · serialidade · inscrição_estatal

**Inclusion criteria** (all 4 required): female allegorical figure + explicit juridical-political function + datable 1800–2000 + accepted support. *(País deixou de ser critério de inclusão em 2026-06-22 — a alegoria "universal" é transnacional, base do Contrato Racial Visual; país permanece variável analítica, não gate. Ver `docs/decisions/E1-OPUS48-BATCH-2026-06-22.md` e memória `feedback_no_country_inclusion_rule`.)*

---

## Mode Routing & Shortcut Commands

The agent dispatches by trigger keywords (archived legacy reference: `archive/root-stale/ICONOCRACY_MASTER_PROMPT.md`). Execute directly without confirmation:

| Trigger | Mode | Action |
|---------|------|--------|
| `scout [query]`, `campanha N`, `buscar`, `lacunas`, `auditoria` | SCOUT | Archive search, Obsidian note generation, gap analysis |
| `argos`, `acquisition`, `orquestrar aquisicao`, `orquestrar aquisição` | ARGOS | Build manifest, prepare dispatch groups, coordinate acquisition workflow |
| `codificar`, `iconocode`, `analisar imagem`, or image received | ICONOCODE | 3-level Panofsky + 10 indicators |
| `compilar`, `make tese`, `gerar PDF` | COMPILAR | Markdown → PDF via Pandoc |
| `validar [file]` | VALIDAR | JSON schema validation (`validate_schemas.py`) |
| `sync vault pull/push/sync/diff/status` | SYNC | Bidirectional vault ↔ records sync (`vault_sync.py`) |
| `purificacao status/item/lote/exportar` | PURIFICAÇÃO | endurecimento coding (`code_purification.py`) |
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
- All Codebook v2 allegory fields (e.g. `subtipo`, `familia_alegorica`, `vetor_colonial`, `hipotese_racial`) must be nested under the `"purificacao"` key in `data/processed/records.jsonl`. The export script `records_to_corpus.py` flattens these fields to the root of `corpus/corpus-data.json`. Direct manual edits to `corpus-data.json` will be overwritten.
- `data/raw/` must remain metadata-only in git (ADR-001: Google Drive stores binaries)
- Vault notes follow pattern `XX-NNN Title.md` where XX = country code, NNN = sequential number (e.g., `FR-013 Déclaration des droits.md`)
- All generic vault notes in `vault/**/*.md` should default to **Obsidian Flavored Markdown**: frontmatter properties, `[[wikilinks]]`, `![[embeds]]`, callouts, comments, highlights, and external URLs only as Markdown links
- Canonical vault guide: `vault/meta/Guia — Obsidian Flavored Markdown.md`; generic default template: `vault/_templates/nota-obsidian-padrao.md`
- Thesis original files (`*_original`) are protected — use `vault/tese/` for revised drafts
- SSD `/media/ana/SSD_DATA` stores raw images, Zotero PDFs, and backups
- Automatic vault backups must not land on `main` (use `vault_backup.py`)
- Academic voice: formal Portuguese with jurídico-penal framing (legal-criminal history, NOT anthropological/sociological)

---

## Known Data Issues (last audit: 2026-07-13)

These documented problems affect corpus operations:

1. **Minor drift across exports** — current counts (audit: 2026-07-13, sync with main):
   - `data/processed/records.jsonl` → **328 records, all schema-valid** (`validate_schemas.py` → 328/328 ✓)
   - `corpus/corpus-data.json` → **328 items** (`records_to_corpus.py --diff` → synchronized by URL)
   - `data/processed/purification.jsonl` → **279 records, all schema-valid** (`validate_schemas.py data/processed/purification.jsonl --schema purification-record` → 279/279 ✓; endurecimento coding now **279/328 = 85%**, 49 remaining, up from 236 on 2026-07-02)
   - `companion-data.json` → **277 declared corpus_total**, **9 country groups**, **21 `zwischenraum_panels`**; derived UI surface, not canonical authority.
2. **Placeholder-`input_url` drift between ledger and export** — `records.jsonl` now carries **6** placeholder `input_url`s (all `https://iconocracy.corpus/placeholder/FR-0XX`), down from 8, but `corpus/corpus-data.json` still surfaces **8** placeholder-bearing items. Note this is *not* caught by `records_to_corpus.py --diff`: that check keys on `webscout.search_results[0].url` (normalized to corpus_id), **not** `input_url`, so the "synchronized by URL" green light does not cover the `input_url` field — which is exactly why this drift can persist unnoticed. Re-run `records_to_corpus.py` and verify the 6 remaining against `data/raw/drive-manifest.json`.
   - Minor dedup watch: **4 duplicate `input_url`s** in `records.jsonl` — 3× `https://iconocracy-corpus.local/piloto/` (pilot rows, distinct from the placeholder set above) + 3 real-source pairs — candidates for `corpus-dedup`, not confirmed duplicates.
3. **Corpus N is intentionally NOT fixed — exploratory posture (decided 2026-06-24).** The corpus is open and growing until the defense (>1yr out). Do **not** treat any N as frozen, "pinned", or a blocking "pending decision"; there is no "decide N first" gate. Acquiring and coding new allegories is normal exploratory research — never block it.
   - In prose, describe the corpus **provisionally** ("em expansão", "amostra analisada", "instantâneo de trabalho") and fix concrete numbers only near the defense. When precision is needed, distinguish *ledger operacional* (grows; recent audits ~278–328) from *amostra analítica congelada* (a snapshot used for Cap. 6 reproducibility, re-runnable on the final corpus).
   - Older artifacts that reference 145/165 (notebooks `01/05/06/07`; manuscript `Capitulo2_metodologia.md`, `Introducao_rev.md`, etc.; the frozen `Other/corpus-data.json`) are **historical analysis snapshots, not errors** — each records the sample a given run used. Update them lazily near the defense, not as blocking debt. `Other/` also holds a duplicate of `notebooks/01–08` (stale copy, not a second source of truth).
   - `endurecimento_score=0` is a valid score (low purification), not "uncoded". Background on the stratification dialectic: memory `corpus-n-20260605` + `docs/decisions/DIALETICA-N165-vs-265.md` — **informative, not a gate.**

**Resolved issues:** the "11 records with out-of-range indicator values (>3)" and the records/export count drift are resolved in the current operational snapshot — `validate_schemas.py` reports 328/328 records valid, `purification.jsonl` reports 279/279 valid, and `records_to_corpus.py --diff` reports synchronization by URL.

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

---

## Agent skills

Per-repo config consumed by Matt Pocock's engineering skills (`triage`, `to-issues`, `to-prd`, `diagnose`, `tdd`, `improve-codebase-architecture`, etc.).

### Issue tracker

GitHub Issues at `anavvanzin/iconocracy-corpus` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical defaults (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at repo root (created lazily by `/grill-with-docs`) + 5 ADRs in `docs/adr/`. See `docs/agents/domain.md`.
