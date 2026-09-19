# Deep Research Runbook — ICONOCRACIA

**Purpose:** systematic corpus expansion past the 145-item canonical set in `corpus/corpus-data.json`, using web search/fetch MCP to surface allegorical figures in legal iconography (19th–20th c.) that existing archive pipelines (Gallica, Europeana direct) miss.

**Scope:** candidate discovery only. Dedup, schema validation, and ingestion happen downstream.

---

## Pipeline

```
deep-research runbook (this file)
        │
        │  executes search+fetch with exa MCP
        ▼
corpus/candidatos/research-YYYY-MM-DD.md   ← Markdown report, one entry per candidate
        │
        │  corpus-scout skill triages + fills missing metadata
        ▼
corpus-dedup agent   ← rejects items already in corpus-data.json
        │
        ▼
corpus-scout → formal ingest (JSONL) → schema validate → corpus-data.json
```

---

## Tools (MCP)

| Tool | When |
|------|------|
| `mcp__plugin_everything-claude-code_exa__web_search_exa` | broad discovery; use semantic queries in PT/EN/FR/DE/IT |
| `mcp__plugin_everything-claude-code_exa__web_fetch_exa` | extract full text of promising hits; keep for ABNT metadata |

**No firecrawl.** Exa-only per `skill-comply` audit of deep-research SKILL.md.

---

## Sub-Questions (v1 — 2026-04-14)

Four research tracks, each runs as one session with cap ~15 candidates.

### SQ1 — Alegorias femininas da Justiça séc. XIX fora de Gallica

- Fontes alvo: Bibliothèque royale de Belgique (KBR), Österreichische Nationalbibliothek (ONB), Biblioteca Nacional de Portugal, Hathitrust, Internet Archive, Biblioteca Digital do Senado BR
- Iconclass seed: 44G, 48C51, 11MM31 (Iustitia)
- Excluir: itens já catalogados com `fonte: gallica` em `corpus-data.json`

### SQ2 — Iconografia jurídica latino-americana 1850–1950

- Fontes alvo: BN Argentina (Tesauro), BN México (Hemeroteca), Biblioteca Nacional de Chile, Hemeroteca Digital BR, IHGB, Museu Histórico Nacional (RJ)
- Foco: capas de códigos penais, frontispícios de tratados de direito criminal, alegorias em edições ilustradas de constituições
- Especial interesse: obras de Pedro Américo, Victor Meirelles, Candido Portinari (representações de Justiça)

### SQ3 — Iconclass 48C51 em museus europeus não-indexados pela Europeana

- Método: scrape museus com coleção online mas fora Europeana — Germanisches Nationalmuseum (Nürnberg), Bayerische Staatsbibliothek, KHM Wien, Statens Museum for Kunst (Copenhagen)
- Output: item + IIIF manifest URL se disponível (compatível com tooling existente `indexing/gallica-mcp-server` por analogia)

### SQ4 — Tratados de iconologia jurídica em alemão/italiano

- Fontes alvo: MDZ (Münchener Digitalisierungszentrum), Internet Culturale (Italia), SBB-IPK Berlin, Biblioteca Nazionale Centrale Roma
- Autores-semente: Giovanni Battista Valvassor, Cesare Ripa (edições tardias), Ernst von Moy de Sons, Rudolf von Ihering (alegorias no *Geist des römischen Rechts*)
- Output: obra + edição + páginas com iconografia específica

---

## Candidate Output Schema

Arquivo: `corpus/candidatos/research-YYYY-MM-DD.md` (onde `YYYY-MM-DD` = data execução, ISO 8601)

Cada candidato = bloco YAML frontmatter + prose notes:

~~~markdown
## [slug-kebab-case]

```yaml
id: sq1-2026-04-14-iustitia-kbr-001
title: Frontispício do Code pénal belga, edição 1867
fonte: KBR (Bibliothèque royale de Belgique)
url: https://uurl.kbr.be/1234567
iconclass_guess: 48C51, 11MM31
allegory_figure: Iustitia (venda, espada, balança)
date_object: 1867
support: gravura em talho-doce
author: anon. / gravador não identificado
notes: |
  Edição comemorativa do código; frontispício com Iustitia flanqueada
  por Themis. Busto de Rogier no pedestal. Possível diálogo com capa
  da edição francesa 1810.
abnt_ref: |
  BÉLGICA. Code pénal. Bruxelles: Bruylant, 1867. Disponível em:
  https://uurl.kbr.be/1234567. Acesso em: 14 abr. 2026.
confidence: medium
```
~~~

**Minimum fields** (corpus-scout will reject if missing): `id`, `title`, `fonte`, `url`, `allegory_figure`, `date_object`, `abnt_ref`.

**Optional but recommended:** `iconclass_guess`, `author`, `support`, `notes`, `confidence`.

---

## Execution Checklist (per session)

1. Pick one SQ (SQ1–SQ4).
2. Run 3–5 queries via `web_search_exa`. Capture raw results in memory.
3. Filter: drop already-indexed (grep por URL no `corpus/corpus-data.json`).
4. For survivors, `web_fetch_exa` to get full page text.
5. Extract candidate metadata → fill YAML schema above.
6. Write to `corpus/candidatos/research-YYYY-MM-DD.md`. Append entries se arquivo já existe.
7. Cap: 15 candidates/session (qualidade > volume).
8. Handoff: invocar `corpus-scout` skill para triagem → `corpus-dedup` agent → ingest.

---

## ABNT NBR 6023:2025 Notes

- Citação de recurso online: autor. Título. Local: editora, data. Disponível em: URL. Acesso em: data.
- Para gravuras/iconografia sem autor: usar `[s. n.]` como autor. Manter título descritivo em itálico.
- `abnt_ref` no YAML serve como **semente** — `abnt-checker` agent valida/ajusta antes do ingest final.

---

## Smoke Test Target (first run)

SQ1, query: `"justicia ciega" frontispicio código penal siglo XIX -gallica -site:gallica.bnf.fr`

Expected: 5–10 resultados, filtra por já-indexado, extrai 2–3 candidatos concretos. Se passar, pipeline validado end-to-end.

---

## Out of Scope

- Dedup próprio (é job do `corpus-dedup` agent).
- Schema JSON validation (é job do `validate-corpus` skill + `tools/scripts/validate_schemas.py`).
- Download de imagens raw (raw fica em Google Drive, não versionado, per CLAUDE.md).
- Correção ABNT final (é job do `abnt-checker` agent).

---

## Updates / Changelog

- **2026-04-14** — runbook criado; 4 sub-questões definidas; schema v1 fixado. Origem: sessão docker-stack, skill #2.
