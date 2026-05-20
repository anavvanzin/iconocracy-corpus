---
name: zotero-cite
description: >
  Resolve a thesis citation via Zotero MCP, insert into vault/tese/references.bib
  if missing, and return the Pandoc @cite-key ready to paste into a chapter.
  Use when the user says "citar", "cite", "cita", "insere citação", "zotero",
  or references an author/title while drafting tese/manuscrito/*.md.
user-invocable: true
---

Bridge Zotero → `references.bib` → ABNT-validated `@cite-key`. Never silently overwrite existing entries.

## Inputs

One of:

- **Author + year**: `/zotero-cite "Mondzain 2002"` or `/zotero-cite Pateman 1988`
- **Zotero item key**: `/zotero-cite ABCD1234`
- **Free query**: `/zotero-cite "contrato sexual visual alegoria feminina"`

## Pipeline

### Step 1 — Locate in Zotero

Use `mcp__zotero-mcp__zotero_search_items` with the query. If multiple hits, show top 5 with `{key, title, authors, year}` and ask the user to pick. If zero hits, **stop** and suggest the user add the item to Zotero first.

### Step 2 — Derive cite-key

Read `vault/tese/references.bib` and check if a BibTeX entry already exists for the chosen item. Match by DOI, ISBN, or `title + year + first author`.

- **Exists** → reuse its cite-key. Skip to Step 4.
- **Missing** → proceed to Step 3.

Cite-key convention for this repo: `SURNAME_YEAR_KEYWORD` in lowercase, ASCII-only (e.g., `mondzain_2002_image`, `pateman_1988_contract`).

### Step 3 — Fetch metadata and append to `references.bib`

```
mcp__zotero-mcp__zotero_item_metadata(item_key=<key>)
```

Map to BibTeX:

| Zotero field | BibTeX field |
|--------------|--------------|
| itemType=book | `@book` |
| itemType=journalArticle | `@article` |
| itemType=bookSection | `@incollection` |
| itemType=thesis | `@phdthesis` / `@mastersthesis` |
| creators (authors) | `author = {SURNAME, Given and ...}` |
| date / issued | `year` (YYYY) |
| title | `title` |
| publisher | `publisher` |
| place | `address` |
| DOI | `doi` |
| URL | `url` + `urldate` (YYYY-MM-DD, today UTC) |

Append the new entry to `vault/tese/references.bib` via Edit. **Preserve alphabetical order by cite-key.** Do not touch existing entries.

### Step 4 — Validate ABNT

Dispatch the `abnt-checker` subagent with the newly written BibTeX block **and** the Pandoc-rendered form (run a dry-render snippet through `pandoc --citeproc --csl=vault/tese/abnt.csl` if available). Collect any warnings.

### Step 5 — Return

Emit:

```
ZOTERO-CITE
  source:   Zotero key <X> → "<Title>" (<Author> <Year>)
  bib:      <cite-key>     [new | reused]
  abnt:     OK | N warning(s) — <summary>
  ready:    @<cite-key>
```

If `abnt` status is not `OK`, show each warning verbatim; do not silently accept.

## Rules

- **Never overwrite** an existing BibTeX entry. If conflict detected, ask the user which to keep.
- If Zotero returns no DOI/URL but the item is online-only, prompt for a URL before writing.
- Always set `urldate` to today UTC (`YYYY-MM-DD`) for online sources.
- Titles go inside `{...}` to preserve capitalization: `title = {{ICONOCRACIA: Alegoria Feminina...}}`.
- Do not insert the `@cite-key` into chapter text automatically — the user pastes it where the citation belongs. Return it, don't write it.

## When to run

- While drafting any `tese/manuscrito/*.md` chapter and a new source is mentioned
- After a literature review batch to ingest several items at once (pass a list)
- When `chapter-integrity` agent flags a missing cite-key
