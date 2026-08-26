---
tipo: "meta"
tags: [meta, adr]
---

# Decisões Arquiteturais (ADRs)

Registro das decisões técnicas do projeto. Fonte canônica: `docs/adr/`.

## ADR-001: Google Drive como armazenamento bruto

**Status:** Aceito | **Data:** 2026-03-22

Binários (imagens, PDFs) vivem no Drive; GitHub armazena apenas manifests JSON.
→ `docs/adr/001-drive-as-raw-store.md`

## ADR-002: Notion como índice catalográfico

**Status:** Aceito | **Data:** 2026-03-22

Notion serve como interface de catalogação; sincronizado via `notion_sync.py`.
→ `docs/adr/002-notion-as-index.md`

## ADR-003: JSONL como formato canônico

**Status:** Aceito | **Data:** 2026-03-22

`records.jsonl` é a fonte de verdade; CSV, Notion e SQLite são derivados.
→ `docs/adr/003-jsonl-as-canonical.md`

## ADR-004: Obsidian como vault de pesquisa

**Status:** Aceito | **Data:** 2026-03-23

Obsidian complementa Notion: escrita longa (capítulos via Pandoc), catalogação
com wiki-links, diário de pesquisa. O vault vive em `vault/` no repositório.
→ Este documento.

### Motivação
- Markdown nativo, versionável no git
- Wiki-links entre fichas, capítulos e notas
- Dataview para consultas sobre o corpus via frontmatter
- Pandoc pipeline para compilação acadêmica (ABNT, DOCX/PDF)
- Trabalho offline sem dependência de API

### Consequências
- Notion permanece para colaboração com orientador e equipe
- `notion_sync.py` sincroniza Notion ↔ JSONL (não Obsidian diretamente)
- Fichas no Obsidian são criadas manualmente ou importadas do JSONL
- `.obsidian/workspace.json` é gitignored (estado pessoal)
