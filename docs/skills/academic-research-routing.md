# Routing: `academic-research-skills` (13-agent suite) — ICONOCRACIA Decision

**Status:** Option A adopted (2026-04-14). Use `deep-research` sub-skill only. Skip writer sub-skills.

---

## Why this doc exists

The `academic-research-skills` plugin ships a 13-agent suite covering discovery → literature review → drafting → citation → style check. Default config targets:

- **Citation standards:** APA / IEEE / Chicago
- **Languages:** English + 繁體中文 (zh-TW)
- **Output style:** Anglo-Saxon monograph / scientific paper

ICONOCRACIA thesis requirements are orthogonal on every axis:

- **Citation standard:** ABNT NBR 6023:2025 (Brazilian, significantly different rules — `Disponível em:`, `Acesso em:`, author format, page-ref requirements on direct quotes)
- **Language:** Portuguese (PT-BR), with sections in DE / ES / FR / IT for primary sources
- **Output style:** tese de doutorado PPGD/UFSC (criminal law history register, not sciences style)

Wrapping or forking the writer sub-skills to cover ABNT+PT-BR would take longer than keeping the existing pipeline. The existing pipeline (`compilar-tese` skill, `chapter-integrity` agent, `abnt-checker` agent, `abnt-precommit` skill, Pandoc Makefile at `vault/tese/`) already handles writing, citation, and style gates correctly for this thesis.

---

## Routing Decision

| Sub-skill / agent in `academic-research-skills` | Action |
|--------------------------------------------------|--------|
| `deep-research` (discovery via exa MCP) | **USE** — wired via `docs/research/deep-research-runbook.md` |
| Literature review sub-skills | **SKIP** — `literature-bibliography-*` already tracked in `docs/` manually |
| Drafting / writer sub-skills | **SKIP** — ABNT+PT-BR mismatch; existing thesis pipeline handles it |
| Citation sub-skills (APA/IEEE/Chicago) | **SKIP** — `abnt-checker` agent + `abnt-precommit` skill own citations |
| Style check sub-skills (EN/zh-TW) | **SKIP** — `chapter-integrity` agent owns PT-BR style gates |

---

## Existing Pipeline (what handles the skipped halves)

| Writer/citation need | Where it lives |
|----------------------|----------------|
| Chapter drafting (Markdown → PDF) | `vault/tese/Makefile` + Pandoc, invoked via `compilar-tese` skill |
| ABNT NBR 6023:2025 verification | `.claude/agents/abnt-checker.md` agent + `abnt-precommit` skill |
| Chapter coherence / terminology | `.claude/agents/chapter-integrity.md` agent |
| Bibliography (BibTeX / Zotero) | `vault/tese/references.bib` + `zotero-cite` skill |
| Iconclass notation review | `.claude/agents/iconclass-reviewer.md` agent |
| Corpus data QA | `validate-corpus` skill + `tools/scripts/validate_schemas.py` |

---

## If requirements change

Revisit this doc if:

- Sub-paper is needed in English for international submission → may want writer sub-skill for that one-off, kept separate from thesis pipeline
- `academic-research-skills` adds ABNT/PT-BR locale support
- Committee requires an external literature review format

Until then: **deep-research is the only door in**.

---

## Updates / Changelog

- **2026-04-14** — Option A adopted; routing fixed. Origem: sessão docker-stack, skill #3.
