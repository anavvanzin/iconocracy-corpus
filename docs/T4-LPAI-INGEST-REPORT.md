# T4 — LPAI v2 Ingest Report (staging phase)

**Run date:** 2026-04-19  
**Source DOCX:** `/Users/ana/Downloads/Documents/Fichas_LPAI_v2_Campanha_SCOUT_BR_FR.docx`  
**Parser:** `tools/scripts/ingest_fichas_lpai.py`  
**Batch ID:** `00000000-0000-4000-8000-lpaiv2scout0001`

> This report documents the **staging** phase only. Nothing in
> `corpus/corpus-data.json`, `data/processed/records.jsonl`,
> `data/processed/purification.jsonl`, or `vault/candidatos/` was touched.

## 1. Parse outcome

- **Fichas detected:** 15/15 (expected 15).
- **Distribution:** BR = 7 (`BR-SCOUT-001..007`), FR = 8 (`FR-SCOUT-001..008`).
- **Schema validation:** 15/15 pass `tools/schemas/master-record.schema.json`
  via `tools/scripts/validate_schemas.py`. Every record carries an
  `audit_flags: ["lpai_v2_ingest"]` tag so downstream tooling can
  distinguish ingested-but-uncoded items from fully-coded corpus members.
- **Inline images in DOCX:** 0 (confirmed via `zipfile` inspection of
  `word/media/`). The `_images/` directory is created empty for
  consistency; image attachment happens through the existing ARGOS
  pipeline, not here.

## 2. Per-ficha table

| Proposed ID | Title (truncated) | Country | Support (truncated) | URL | Dedup |
|---|---|---|---|---|---|
| BR-SCOUT-001 | Alegoria da República Brasileira — Revista Illustrada | BR | Litografia em periódico (Revista Il… | commons.wikimedia.org/wiki/File:Repub… | NEW |
| BR-SCOUT-002 | Alegoria à República — Capa da Revista Illustrada n. 566 | BR | Litografia em periódico (capa, Revi… | commons.wikimedia.org/wiki/File:Capa_… | NEW |
| BR-SCOUT-003 | Alegoria da República — Manoel Lopes Rodrigues (óleo s.t.) | BR | Óleo sobre tela, 230 × 120 cm | artsandculture.google.com/story/cole… | NEW |
| BR-SCOUT-004 | Alegoria à Lei de 13 de Maio de 1888 (estudo) | BR | Pintura a óleo sobre tela (estudo) | mhn.museus.gov.br/estudo-de-decio-vil… | NEW |
| BR-SCOUT-005 | A Justiça (escultura monumental) — STF, Brasília | BR | Granito monolítico de Petrópolis, 3… | commons.wikimedia.org/wiki/Category:J… | NEW |
| BR-SCOUT-006 | Suffragistas — Fon-Fon, 16 de maio de 1914 | BR | Litografia/caricatura em periódico… | bndigital.bn.gov.br/exposicoes/brasil… | NEW |
| BR-SCOUT-007 | O Feminismo Triumphante — Revista da Semana, 20 maio 1933 | BR | Fotografia/ilustração em periódico | bndigital.bn.gov.br/exposicoes/brasil… | NEW |
| FR-SCOUT-001 | La République aimable | FR | Estampa (gravura, eau-forte) | gallica.bnf.fr/ark:/12148/btv1b531842… | **PARTIAL → FR-005** |
| FR-SCOUT-002 | La République nous appelle... (État avec remarque) | FR | Litografia (état avec remarque, édi… | gallica.bnf.fr/ark:/12148/btv1b105106… | NEW |
| FR-SCOUT-003 | République de Clésinger (fotografia de demonstração) | FR | Fotografia (tirage de démonstration… | gallica.bnf.fr/ark:/12148/btv1b531241… | NEW |
| FR-SCOUT-004 | Unité indivisibilité de la République (j'ai rompu mes c…) | FR | Estampa (gravura em relevo/entalhe) | gallica.bnf.fr/ark:/12148/btv1b695038… | NEW |
| FR-SCOUT-005 | Buste de la République (série de 4 fotografias) | FR | Fotografia de imprensa (busto escul…) | gallica.bnf.fr/ark:/12148/btv1b695287… | NEW |
| FR-SCOUT-006 | Liberté (Moitte/Janinet) | FR | Estampa (gravura colorida — Janinet…) | gallica.bnf.fr/ark:/12148/btv1b100269… | NEW |
| FR-SCOUT-007 | La République (en hauteur) — Exposição Internacional 1889 | FR | Fotografia (escultura monumental da…) | gallica.bnf.fr/ark:/12148/btv1b116003… | NEW |
| FR-SCOUT-008 | Étude pour le 1er mai? (Steinlen) | FR | Desenho (dessin original) | gallica.bnf.fr/ark:/12148/btv1b531888… | NEW |

## 3. Dedup deep-dive (PARTIAL matches)

### FR-SCOUT-001 ↔ existing FR-005

- **New (LPAI v2):** La République aimable — no creator in title.
- **Existing corpus item FR-005:** `La République aimable (Félicien Rops)` —
  attributed to Rops, dated 1871, regime `contra-alegoria`.
- **Shared signals:** identical `url`
  (`https://gallica.bnf.fr/ark:/12148/btv1b531842166`) **and**
  normalized-title substring match.
- **Diagnosis:** almost certainly the same object; the LPAI v2 ficha drops
  the parenthetical attribution. The dedup classifier flagged this as
  PARTIAL (not MATCHES) because only the URL hit registered as an exact
  signal — the LPAI title is a strict prefix of the canonical title.

**Recommended resolution:** *do not create a new corpus entry*. Promote the
staging record as an **enrichment** of `FR-005` — merge LPAI v2 fields
(`lpai_v2_code`, `classe`, `atributos`, `nota_analitica`, updated
`citation_abnt`) into the existing record rather than appending a new
row. The staged JSON line and draft vault note for FR-SCOUT-001 should be
archived but not promoted.

## 4. Validation summary

- **Schema-ready to merge:** 15/15 (all records satisfy
  `master-record.schema.json`, including the `webscout` and `iconocode`
  stubs with `audit_flags: ["lpai_v2_ingest"]`).
- **Iconocode stubs are placeholders.** They carry only the Iconclass
  tokens extracted from the LPAI ficha and a single `tentative`
  interpretation claim. Full Panofsky + Iconclass coding is the T3 queue
  (see action 5.b below).
- **Purificação (`purificacao`) is absent on every ingested record.**
  Valid — the schema marks that block optional. It will be populated by
  IconoCode after promotion.

## 5. Required human actions before merge

### a. Disambiguate FR-SCOUT-001

Decide: merge into `FR-005` (recommended) or assert this is a distinct
printing/state that deserves its own record. If merging: drop the line
for FR-SCOUT-001 from the staged JSONL before appending to
`records.jsonl`, and copy the LPAI-specific fields into `FR-005`
manually.

### b. Queue the 15 new records for IconoCode coding

After merge, the T3 coding queue grows by **14** items (15 ingested,
minus 1 de-duplicated):

```bash
# once promoted
python tools/scripts/code_purification.py --status
python tools/scripts/code_purification.py --item BR-SCOUT-001
# ... (repeat per item, or use iconocode-batch skill)
```

### c. Review draft vault notes

Fifteen Markdown drafts are in
`data/staging/vault-drafts-lpai-v2/`. Each has
`status: staging-lpai-v2` in the frontmatter. Review each for:

- Title spelling / accent normalization (check BR-SCOUT-003, BR-SCOUT-004
  for tela-support items — make sure ARGOS manifest will be able to pull
  the image).
- Any Iconclass code that looks over- or under-specified.
- Whether `aliases: []` should be populated (e.g., FR-SCOUT-004 has a
  long title with multiple legends).

### d. Image attachment

The DOCX itself carries no inline media. For each staged item:

- If URL download is hosted on Wikimedia Commons / BNDigital: the image
  can be fetched directly. See `tools/scripts/download_corpus_images.py`.
- If URL is on Gallica (8 FR items + 1 BR): prior runs hit
  robots-blocked status. Plan to route through the Playwright bypass or
  the Gallica MCP server in `indexing/gallica-mcp-server/`.

## 6. Promotion commands (run after review)

**DO NOT run these until actions 5.a–5.c above are satisfied.** This is
the skeleton merge pipeline; see `docs/OPERATING_MODEL.md` §release-gate
for policy.

```bash
# 1. Promote (approved) vault drafts to vault/candidatos/
#    Review each file, then:
cp data/staging/vault-drafts-lpai-v2/BR-SCOUT-001*.md vault/candidatos/
# ... repeat for each approved ficha ...
# (or use a for-loop once you've inspected all 14/15)

# 2. Append ingested JSONL to the canonical ledger
cat data/staging/fichas-lpai-v2-parsed.jsonl >> data/processed/records.jsonl

# 3. Re-validate the canonical ledger
python tools/scripts/validate_schemas.py

# 4. Regenerate the public corpus-data.json from records.jsonl
python tools/scripts/records_to_corpus.py --diff   # preview
python tools/scripts/records_to_corpus.py          # apply

# 5. Run coherence regression test
python -m pytest tests/tools/test_reconcile_coherence.py -v

# 6. Queue coding for the new items (T3)
python tools/scripts/code_purification.py --status
```

## 7. Artifacts

- `data/staging/fichas-lpai-v2-parsed.jsonl` — 15 master-record-shaped
  stubs.
- `data/staging/vault-drafts-lpai-v2/*.md` — 15 draft vault notes.
- `data/staging/vault-drafts-lpai-v2/_images/` — empty (no inline media
  in DOCX).

All three paths are `.gitignore`-excluded to keep staging artifacts out
of the canonical tree.
