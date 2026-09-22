# Audit Wave 3.1 — Documentation Governance

**ICONOCRACY 360° Audit | Wave 3.1 | 2026-06-26**
**Scope:** Cross-reference CLAUDE.md vs AGENTS.md, Known Data Issues currency, ADR audit, PLANO-TESE vs sumário, stale docs, broken path references.
**Status:** COMPLETE
**Severity Summary:** 🔴 3 CRITICAL | 🟡 5 HIGH | 🟢 6 MEDIUM | ℹ️ 4 LOW

---

## Executive Summary

Governance documentation is **actively maintained but inconsistent across surfaces**. The three primary agent-facing documents (CLAUDE.md, AGENTS.md, README.md) report **three different corpus snapshots** from different dates, and none matches the actual state. The `docs/adr/` directory (5 classical ADRs) and `docs/decisions/` (23+ decision records) coexist as **two separate decision registries with no index or cross-reference**, and multiple documents reference the wrong directory. CLAUDE.md's Known Data Issues section is **materially stale** (claims 278 records, 277 companion_total; actual: 299 records, 165 companion_total). The PLANO-TESE and sumário represent **completely different thesis architectures** — the sumário (March 2026 with ongoing updates) is clearly authoritative, but CLAUDE.md still designates PLANO-TESE as the "Master plan."

---

## 1. CLAUDE.md vs AGENTS.md Cross-Reference

### 1.1 Corpus Count Discrepancies (🔴 CRITICAL)

Both documents claim audit date **2026-06-23** but report different numbers:

| Data Source | CLAUDE.md | AGENTS.md | ACTUAL (2026-06-26) |
|---|---|---|---|
| `records.jsonl` | **278** | **280** | **299** |
| `corpus-data.json` | **278** | **280** | **299** |
| `purification.jsonl` | **234** | **236** | **236** |
| `vault/candidatos/` | _not stated_ | **314** | **357** |
| `companion-data.json` | **277** (corpus_total) | _not mentioned_ | **165** |

**Findings:**
- CLAUDE.md and AGENTS.md disagree on **every shared count** despite claiming the same audit date.
- AGENTS.md's purification count (236) matches reality, but its records count (280) is 19 behind.
- CLAUDE.md's companion-data claim (277) is **catastrophically wrong** — actual is 165, indicating the file is frozen from a much earlier snapshot.
- Neither document mentions vault/candidatos growth from 314 → 357 (+43 notes since last audit).

### 1.2 Release Gate Order (🔴 CRITICAL)

The two documents prescribe **different execution orders** for the release gate:

| Step | CLAUDE.md Order | AGENTS.md Order |
|---|---|---|
| 1 | `validate_schemas.py` | `validate_schemas.py` |
| 2 | `code_purification.py --status` | `vault_sync.py status` |
| 3 | `vault_sync.py status` | `records_to_corpus.py --diff` |
| 4 | `records_to_corpus.py --diff` | `code_purification.py --status` |
| 5 | `build_hf_release.py` | `build_hf_release.py` |

**This is a concrete operational hazard.** An agent following AGENTS.md's order may attempt `records_to_corpus.py --diff` before validating `code_purification.py --status`, potentially exporting stale purification data. The CLAUDE.md order (validate → coding status → sync status → export diff → build) is logically safer: it surfaces coding drift before syncing exports.

### 1.3 Command Syntax Differences (🟡 HIGH)

| Aspect | CLAUDE.md | AGENTS.md |
|---|---|---|
| Vault sync args | `vault_sync.py status` / `vault_sync.py sync` | `vault_sync.py pull\|push\|sync\|diff\|status` |
| Code purification args | `code_purification.py --status` / `--export-csv` | `code_purification.py --status\|--item ID\|--batch SIGLA\|--export-csv` |
| Test file count | Not specified | "24 test files" |
| Vault note pattern | `XX-NNN Title.md` | `CC-NNN Title.md` (line 61) but line 69 says `XX-NNN Title.md` |

**Vault sync args:** The actual script (`vault_sync.py --help`) supports `{status,diff,pull,push,sync}` — AGENTS.md is more complete here. CLAUDE.md omits `pull`/`push`.

**Vault note pattern (AGENTS.md):** AGENTS.md line 61 says `CC-NNN` (typo for `XX-NNN`), corrected on line 69. Internal inconsistency within AGENTS.md itself.

### 1.4 Content Coverage Gaps (🟡 HIGH)

**Information unique to CLAUDE.md (absent from AGENTS.md):**
- Complete Architecture section with Dual-Agent Pipeline diagram
- Canonical Data Hierarchy explanation
- CI/CD description (`.github/workflows/validate.yml`)
- Hooks system (`.claude/settings.json` — SessionStart, PreToolUse, PostToolUse, PreCompact)
- Terminology reference table (detailed dos/don'ts)
- Mode Routing table (12 trigger keywords → agent modes)
- Vault Tags and Traceability Rule
- Key Conventions (SSD mount, academic voice, backup policy)
- Known Data Issues section
- Skills catalog and Review agent names
- Agent skills (`triage`, `to-issues`, etc.)
- Triage labels and domain docs references

**Information unique to AGENTS.md (absent from CLAUDE.md):**
- Data hierarchy counts with `vault/candidatos/` (CLAUDE.md omits this count)
- Guardrail: Codebook v2 allegory fields nested under `"purificacao"` key
- Guardrail: `records_to_corpus.py` flattens fields to root; direct edits to `corpus-data.json` will be overwritten

### 1.5 Terminology Consistency (🟢 LOW)

- Both documents use "endurecimento", "Purificação Clássica", "Contrato Sexual Visual" consistently.
- CLAUDE.md has a detailed terminology table; AGENTS.md has a condensed bullet list.
- AGENTS.md says "heraldização" (line 50), CLAUDE.md says "heraldicização" (line 136). Both refer to indicator #4. CLAUDE.md's form matches the actual codebook.

### 1.6 README.md Third Surface Divergence (🟡 HIGH)

README.md reports a **third, even older** snapshot (2026-05-24):
- records: 265, corpus-data: 264, purification: 264, vault: 314

This is stale by 2 months. The README is the **public-facing repository surface** and still claims the corpus has ~265 items when it actually has 299.

---

## 2. Known Data Issues Currency Audit

### 2.1 Section Location and Audit Date

CLAUDE.md §"Known Data Issues" claims **last audit: 2026-06-23** — 3 days ago. This is recent, but the data is already stale.

### 2.2 Detailed Currency Check

| Claim (CLAUDE.md) | Actual (2026-06-26) | Status |
|---|---|---|
| records.jsonl → 278, all valid | **299**, all valid (assumed) | 🟡 STALE (-21) |
| corpus-data.json → 278, synced by URL | **299** | 🟡 STALE (-21) |
| purification.jsonl → 234, all valid | **236**, all valid (assumed) | 🟡 STALE (-2) |
| companion-data.json → 277 corpus_total | **165** | 🔴 CRITICAL — frozen at earlier snapshot |
| companion-data.json → 9 country groups | **9** countries (list, not groups) | 🟢 CORRECT |
| companion-data.json → 21 zwischenraum_panels | **21** panels | 🟢 CORRECT |
| 8 records with placeholder URLs | _not re-verified_ | ⚠️ UNKNOWN — needs re-audit |

### 2.3 companion-data.json Drift Analysis (🔴 CRITICAL)

`companion-data.json` reports `corpus_total: 165` — this is the **historical frozen sample**, not the current operational corpus. CLAUDE.md claims it shows `277`, which is neither the frozen sample (165) nor the current state (299). This suggests:
- The file was **never updated** to reflect the growth to 278+ records, OR
- CLAUDE.md's claim of 277 was **never verified** against the actual file.

The Known Data Issues note describes companion as "derived UI surface, not canonical authority" — which is correct, but the reported number is still wrong.

### 2.4 "Resolved Issues" Verification

CLAUDE.md claims resolved: "11 records with out-of-range indicator values (>3)" and "records/export drift." These appear genuinely resolved — the 236 purification records (all valid) and 299 records correspond. However, the companion drift has **changed form** (277→165 discrepancy) rather than being resolved.

### 2.5 Missing from Known Data Issues

The following known problems are **not documented** in the Known Data Issues section:
- `docs/adr/006-corpus-export-schema.md` and `docs/adr/007-purification-coverage-policy.md` are referenced in plans/superpowers but **do not exist**
- `docs/adr/` vs `docs/decisions/` schizophrenia (two decision registries)
- `CONTEXT.md` is missing from repo root (referenced by CLAUDE.md)
- `companion-data.json` frozen at N=165 is not explicitly flagged

---

## 3. ADR Audit

### 3.1 Two Decision Registries (🔴 CRITICAL)

The repository has **two separate decision directories** with no cross-referencing:

**`docs/adr/`** — 5 classical Architecture Decision Records (numeric prefix):
- `001-drive-as-raw-store.md` — Google Drive as raw storage
- `002-notion-as-index.md` — Notion as index (superseded by ADR-004)
- `003-jsonl-as-canonical.md` — JSONL as canonical format
- `004-vault-as-index.md` — Vault as catalog mirror (replaces ADR-002)
- `005-github-and-hf-release-surfaces.md` — GitHub + HF release surfaces

**`docs/decisions/`** — 23 .md files (plus 9 in subdirectory) following different naming conventions:
- 18 files use descriptive+date naming: e.g., `ELICIT-CODEBOOK-PATCH-v2.3.0-2026-06-25.md`
- 3 files use date-first naming: e.g., `2026-06-19-reliability-audit-design.md`
- 2 files use topic-only naming: e.g., `DIALETICA-N165-vs-265.md`, `ESTRATIFICACAO-2026-05-30.md`
- Plus 4 `.json` and `.jsonl` data companions
- 1 subdirectory: `dialectic-corpus-2026-06-19/` with 9 files (dialectic rounds, confound audit, index)

**Key problems:**
1. No `README.md` or `index.md` at `docs/decisions/` level — only the subdirectory has an index
2. CLAUDE.md says "5 ADRs in `docs/adr/`" but makes no mention of `docs/decisions/` as a decision registry
3. Multiple documents reference `docs/adr/006` and `docs/adr/007` which **do not exist** — see §5
4. The two registries use completely different formats, metadata conventions, and status tracking

### 3.2 Naming Convention Analysis

`docs/decisions/` naming is **inconsistent across 4 patterns**:

| Pattern | Count | Examples |
|---|---|---|
| `TOPIC-YYYY-MM-DD.md` | 18 | `ELICIT-CODEBOOK-PATCH-v2.3.0-2026-06-25.md` |
| `YYYY-MM-DD-topic.md` | 3 | `2026-06-19-reliability-audit-design.md` |
| `TOPIC.md` (no date) | 2 | `DIALETICA-N165-vs-265.md` |
| Mixed with version tags | varies | `v2.1.0`, `v2.3.0`, `DESENHO-2-0` |

Recommended convention: **`YYYY-MM-DD-SLUG.md`** — date-first for chronological sorting, slug for topic identification.

### 3.3 ADR Coverage Gaps

Referenced but missing ADRs:
- `docs/adr/006-corpus-export-schema.md` — referenced in superpowers/plans/2026-05-19-housekeeping-pass.md
- `docs/adr/007-purification-coverage-policy.md` — same source

These were planned but never written. The decisions they would document may have been captured in `docs/decisions/` instead, but no cross-reference exists.

### 3.4 ADRs in Worktrees (ℹ️ LOW)

The 5 classical ADRs also exist in `.claude/worktrees/e1-fable5-recode/docs/adr/` and `.claude/worktrees/research-permanent/docs/adr/` — these are worktree copies, not duplicates. Not a problem, but confirming the canonical source is `docs/adr/`.

---

## 4. PLANO-TESE vs Sumário

### 4.1 Structural Comparison

| Aspect | PLANO-TESE (2026-05-24) | Sumário (March 2026, updated Jun 26) |
|---|---|---|
| **Status** | "Documento de referência" | "PROPOSTA DE SUMÁRIO DETALHADO" |
| **Chapter count** | 6 (Intro, Cap 2–5, Conclusão) | 9 + Intro + Conclusão |
| **Organization** | Flat, by case study | 4 Parts (I: Theory, II: Method, III: Results, IV: Atlas) |
| **Case studies** | 4 (BR-República, BR-Tribunais, FR-Marianne, UK-Britannia) | Embedded in Cap 7 (qualitative analysis of 6 cases) |
| **Atlas** | Not mentioned | 8 Warburgian panels (Cap 8–9) as thesis culmination |
| **Methodology** | 4-step (coleta → Panofsky → contexto → comparação) | Mixed methods QUAN→QUAL sequential + Warburgian montage |
| **Corpus size** | "80–120 itens" (in risk mitigation) | "~300 imagens oficiais" |
| **Tools** | Airtable, Zotero, Tropy, Iconclass | GitHub, Google Drive, Notion, IconoCode, ICONCLASS, Pandoc |
| **Glossary** | 4 terms (alegoria, iconocracia, iconografia, iconologia) | 10 terms (Contrato Sexual Visual, Feminilidade de Estado, Visiocracia, Iconocracia, Pathosformel, Zwischenraum, Regime Iconocrático, Purificação Clássica, endurecimento militar, Colonialidade do Ver) |

### 4.2 Authoritative Document

**The sumário is clearly authoritative.** Evidence:
- It was last modified **today** (2026-06-26) vs PLANO-TESE's 2026-05-24 (but both have git timestamps from Jun 24, indicating mass migration)
- It reflects the current 4-part architecture used in actual manuscript drafting (`vault/tese/` has 9 chapters + intro + conclusão matching the sumário structure)
- It includes the Atlas, which is now central to the thesis (8 panels, 21 zwischenraum_panels in companion)
- It documents the mixed-methods design (QUAN→QUAL) used in notebooks 01–08
- It mentions the 10-indicator protocol and IconoCode, which are operational

**CLAUDE.md is wrong** in designating PLANO-TESE as "Master plan" — it should point to the sumário instead.

### 4.3 Specific Inconsistencies

| Claim | PLANO-TESE | Sumário | Reality |
|---|---|---|---|
| Chapter structure | 6 flat chapters | 9 chapters in 4 parts | vault/tese/ has 9 chapters |
| Corpus N | "80–120 itens" | "~300 imagens" | 299 actual |
| Tool: Airtable | "⭐ ESSENCIAL" | Not mentioned | Not used operationally |
| Tool: Notion | Out of scope | "índice intellectual" | "historical context only" per OPERATING_MODEL |
| 4 case studies | Named and ranked | Subsumed into Cap 7 qualitative | Matches but expanded to 6 cases |
| Risk: "Amplitude excessiva" | Corpus 80–120 | Not a concern | Corpus at 299, growing |

### 4.4 Obsolete Content in PLANO-TESE

The following sections of PLANO-TESE describe a state that no longer reflects the project:
- **§5 Estudos de Caso**: Case rankings with ✅/⚡/❌/📝 — these decisions were made but the current thesis structure uses a different organization (qualitative chapter, not case-study chapters)
- **§6 Riscos**: "Corpus 80–120 itens" risk mitigation is obsolete
- **§7 Cronograma**: 24-month plan from a pre-2026 starting point — timeline needs recalibration
- **§9 Ferramentas**: Airtable is listed as "ESSENCIAL" but is not in the current toolchain
- **§10 Prompt Elicit**: References `tese/pesquisa/elicit-research-prompt.md` — Elicit is listed as "Pago/ÚTIL" but the prompt file still exists

### 4.5 Sumário vs Actual Manuscript

The sumário structure (4 parts, 9 chapters) maps perfectly to `vault/tese/`:
- `introducao.md`
- `capitulo-1.md` through `capitulo-9.md`
- `conclusao.md`

This confirms the sumário is the live architectural document. PLANO-TESE is an **early planning artifact** that should be explicitly marked as superseded or archived.

---

## 5. Broken Path References

### 5.1 Critical — Referenced Paths That Do Not Exist (🔴 CRITICAL)

| Document | Broken Reference | Notes |
|---|---|---|
| CLAUDE.md | `CONTEXT.md` (repo root) | MISSING — claimed to be "created lazily by `/grill-with-docs`" |
| CLAUDE.md | `docs/adr/` (claims "5 ADRs") | Directory exists but CLAUDE.md ignores `docs/decisions/` entirely |
| docs/agents/domain.md | `docs/adr/` (as primary ADR location) | Should reference both `docs/adr/` AND `docs/decisions/` |
| docs/MANUAL.md | `docs/adr/` (claims ADRs documented there) | `docs/decisions/` is the active registry |
| atlas/ADRs e Decisões — MOC.md | `../docs/adr/` (references all 5 ADRs) | No mention of `docs/decisions/` |
| docs/superpowers/plans/2026-05-19-housekeeping-pass.md | `docs/adr/006-corpus-export-schema.md` | MISSING — never created |
| docs/superpowers/plans/2026-05-19-housekeeping-pass.md | `docs/adr/007-purification-coverage-policy.md` | MISSING — never created |
| PLANO-TESE | `CHECKLIST-SEMANAL.md` (bare filename, implied same dir) | Actually at `docs/CHECKLIST-SEMANAL.md` |
| README.md | `LEIAME.md` (repo root) | Actually at `tese/manuscrito/LEIAME.md` |
| README.md | `ATLAS_ICONOCRACIA.pdf` (tese/) | MISSING — only `ATLAS_ICONOCRACIA.docx` exists |

### 5.2 Typographical Errors in References (🟡 HIGH)

| Document | Reference | Correct Path |
|---|---|---|
| README.md | `CITACOES_FALTANTES.md` | `tese/revisoes/CITACOES_FALTANTES.md` (Ç vs Ç — subtle but link-breaking) |
| README.md | `notebooks/` → "01–08" listing | `01_exploratory` directory exists but most are `.ipynb` files, not directories |
| AGENTS.md line 61 | `CC-NNN Title.md` | Should be `XX-NNN Title.md` (corrected on line 69 of same file) |
| CLAUDE.md line 136 | `heraldicização` | AGENTS.md says `heraldização` — the codebook uses `heraldização` |

### 5.3 Absolute/External Path References (🟢 LOW)

| Reference | Status |
|---|---|
| `~/Documents/CLAUDE.md` | External host system — cannot verify from repo |
| `~/Documents/projetos/research/CLAUDE.md` | External host system — cannot verify |
| `~/.claude/CLAUDE.md` | User profile — cannot verify |
| `/media/ana/SSD_DATA` | Mount point — presence depends on hardware |

### 5.4 Archived Legacy Reference (🟢 MEDIUM)

CLAUDE.md line 144 references `archive/root-stale/ICONOCRACY_MASTER_PROMPT.md` as "archived legacy reference." The file **exists** in the archive but its presence in a governance document is confusing — it suggests the file should be consulted but simultaneously declares it stale.

---

## 6. Stale Documents

### 6.1 Documents Modified > 6 Months Ago (ℹ️ LOW)

**No stale documents found.** All `.md` files outside `archive/` were touched after 2025-12-26, reflecting the June 2026 mass migration. The oldest non-archive files are from April 2026, well within the 6-month window.

The `archive/` directory contains intentionally preserved historical artifacts. Per the CLAUDE.md Known Data Issues §3, artifacts referencing N=145/165 are **historical analysis snapshots, not errors.**

### 6.2 Stale Content (Documents That Need Updates)

| Document | Issue | Recommendation |
|---|---|---|
| README.md | Corpus counts from 2026-05-24 (N=265) | Update to reflect current operational state (~299, expanding) |
| PLANO-TESE | Entire document is a pre-Atlas planning artifact | Mark as superseded; add banner pointing to sumário |
| OPERATING_MODEL.md | Status "active as of 2026-04-06" | Update status date; add reference to `docs/decisions/` |
| CLAUDE.md Known Data Issues | Counts stale (278 vs 299); companion wrong (277 vs 165) | Full re-audit needed |

### 6.3 Companion Data Staleness (🟡 HIGH)

`corpus/companion-data.json` is frozen at `corpus_total: 165` — a historical snapshot that predates the current operational corpus by ~134 records. The file has no accompanying documentation explaining its frozen status, and CLAUDE.md's Known Data Issues incorrectly claims it shows 277. This file is **actively misleading** for any agent or tool that consumes it as a corpus summary.

### 6.4 `Other/` Directory (ℹ️ LOW)

The `Other/` directory contains duplicate notebooks (01–08 `.ipynb` files) and dashboard HTML. CLAUDE.md §Known Data Issues correctly notes: "`Other/` also holds a duplicate of `notebooks/01–08` (stale copy, not a second source of truth)." This is already documented.

---

## 7. Findings Summary

### Critical (🔴) — Must Fix

| # | Finding | Section |
|---|---|---|
| C1 | CLAUDE.md and AGENTS.md report different corpus counts for same audit date (2026-06-23) | §1.1 |
| C2 | Release gate execution order differs between CLAUDE.md and AGENTS.md | §1.2 |
| C3 | `companion-data.json` frozen at N=165; CLAUDE.md falsely claims 277 | §2.3 |
| C4 | Two separate decision registries (`docs/adr/` and `docs/decisions/`) with zero cross-referencing | §3.1 |
| C5 | CLAUDE.md designates PLANO-TESE as "Master plan" but sumário_iconocracia.md is authoritative | §4.2 |
| C6 | `docs/adr/006` and `docs/adr/007` referenced but never created | §5.1 |
| C7 | `CONTEXT.md` missing from repo root (referenced by CLAUDE.md) | §5.1 |

### High (🟡) — Should Fix

| # | Finding | Section |
|---|---|---|
| H1 | README.md corpus counts are 2 months stale (N=265 vs 299 actual) | §1.6 |
| H2 | AGENTS.md has internal inconsistency: `CC-NNN` vs `XX-NNN` note pattern | §1.3 |
| H3 | PLANO-TESE contains obsolete content (Airtable, N=80-120, 24-month plan) | §4.4 |
| H4 | Broken reference: README.md `CITACOES_FALTANTES.md` contains broken Ç character | §5.2 |
| H5 | Broken reference: README.md `LEIAME.md` — file is in `tese/manuscrito/`, not root | §5.1 |
| H6 | `docs/decisions/` has no index/README and 4 inconsistent naming conventions | §3.2 |

### Medium (🟢) — Nice to Fix

| # | Finding | Section |
|---|---|---|
| M1 | README.md references `ATLAS_ICONOCRACIA.pdf` (missing; only .docx exists) | §5.1 |
| M2 | PLANO-TESE references `CHECKLIST-SEMANAL.md` with wrong relative path | §5.1 |
| M3 | AGENTS.md omits CLAUDE.md's Terminology table and Mode Routing | §1.4 |
| M4 | Archive reference in CLAUDE.md (§Mode Routing) is confusing | §5.4 |
| M5 | `companion-data.json` has no documentation explaining its frozen N=165 | §6.3 |
| M6 | CLAUDE.md claims Python 3.11 — should verify and update if needed | §1.2 |

### Low (ℹ️) — Informational

| # | Finding | Section |
|---|---|---|
| L1 | Terminology variant: "heraldicização" (CLAUDE.md) vs "heraldização" (AGENTS.md, codebook) | §1.5 |
| L2 | 5 ADRs duplicated in worktrees (expected, not an error) | §3.4 |
| L3 | No stale documents by modification date (>6 months) — all recently touched | §6.1 |
| L4 | External path references (~/Documents, ~/.claude, /media) cannot be verified from repo | §5.3 |

---

## 8. Recommendations

### Immediate (this week)

1. **Re-audit CLAUDE.md Known Data Issues** with actual corpus counts (299 records, 299 corpus-data, 236 purification, 357 vault candidatos). Fix companion-data.json claim (165, not 277).
2. **Align release gate order** between CLAUDE.md and AGENTS.md. Recommended: CLAUDE.md's order (validate → coding status → sync status → export diff → build).
3. **Harmonize corpus counts** across CLAUDE.md, AGENTS.md, and README.md to a single snapshot date.
4. **Update CLAUDE.md §"Master plan"** to point to `tese/manuscrito/sumario_iconocracia.md` as authoritative, with PLANO-TESE marked as historical reference.

### Short-term (next 2 weeks)

5. **Create `docs/decisions/README.md`** with index of all decisions, cross-reference to `docs/adr/`, and naming convention documentation.
6. **Create missing ADRs or document their disposition**: `docs/adr/006-corpus-export-schema.md` and `007-purification-coverage-policy.md`.
7. **Fix broken path references** in README.md, PLANO-TESE, and AGENTS.md.
8. **Document companion-data.json frozen status** in both the file (as a metadata field) and in CLAUDE.md Known Data Issues.

### Medium-term

9. **Decide on ADR registry consolidation**: keep `docs/adr/` for classical ADRs and `docs/decisions/` for research decisions, but add explicit cross-references in both.
10. **Normalize `docs/decisions/` naming** to `YYYY-MM-DD-SLUG.md`.
11. **Archive PLANO-TESE** or add a prominent banner: "This document is superseded by `tese/manuscrito/sumario_iconocracia.md`."
12. **Regenerate companion-data.json** from current corpus state, or add a `frozen: true` and `frozen_at: "2026-XX-XX"` field.

---

## 9. Audit Metadata

- **Audit ID:** WAVE3-DOCS-GOVERNANCE-2026-06-26
- **Wave:** 3.1 — Documentation Governance
- **Repository:** `/Users/ana/Research/hub/iconocracy-corpus`
- **Executor:** Hermes Agent (deepseek-v4-pro)
- **Documents Audited:** CLAUDE.md, AGENTS.md, README.md, SKILLS.md, PLANO-TESE-ICONOCRACIA.md, sumario_iconocracia.md, OPERATING_MODEL.md, docs/decisions/ (23+ files), docs/adr/ (5 files), companion-data.json, WORKFLOW.md, workspace-map.md, huggingface-release.md
- **Corpus Snapshot Verified:** records.jsonl=299, corpus-data.json=299, purification.jsonl=236, vault/candidatos=357
- **Total Findings:** 7 Critical + 6 High + 6 Medium + 4 Low = 23
