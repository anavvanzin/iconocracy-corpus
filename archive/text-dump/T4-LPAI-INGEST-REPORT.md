# T4 — LPAI v2 Ingest Report (staging phase)

**Run date:** 2026-04-19 (parser), updated 2026-04-19 (T4 review follow-up)
**Source DOCX:** `/Users/ana/Downloads/Documents/Fichas_LPAI_v2_Campanha_SCOUT_BR_FR.docx`
**Parser:** `tools/scripts/ingest_fichas_lpai.py`
**Batch ID:** `00000000-0000-4000-8000-lpaiv2scout0001`

> This report documents the **staging** phase only. Nothing in
> `corpus/corpus-data.json`, `data/processed/records.jsonl`,
> `data/processed/purification.jsonl`, or `vault/candidatos/` was touched.
>
> **Updated after T4 review:** intra-batch dedup, URL canonicalization,
> title-substring dedup, and a `placeholder_url_BLOCK_PROMOTE` audit flag
> have been added to the parser. The per-ficha table and §3 reflect the
> post-fix classifier.

## 1. Parse outcome

- **Fichas detected:** 15/15 (expected 15).
- **Distribution:** BR = 7 (`BR-SCOUT-001..007`), FR = 8 (`FR-SCOUT-001..008`).
- **Schema validation:** 15/15 pass `tools/schemas/master-record.schema.json`
  via `tools/scripts/validate_schemas.py`. Every record carries an
  `audit_flags: ["lpai_v2_ingest"]` tag so downstream tooling can
  distinguish ingested-but-uncoded items from fully-coded corpus members.
- **Intra-batch duplicates:** 0 (no copy-paste duplicates inside the 15
  ficha tables). The parser tracks `(ficha_id, canonicalized_url)` seen
  during the parse loop and appends an `intra_batch_duplicate` audit
  flag on any second-or-later occurrence; the DOCX has none.
- **Inline images in DOCX:** 0 (confirmed via `zipfile` inspection of
  `word/media/`). The `_images/` directory is created empty for
  consistency; image attachment happens through the existing ARGOS
  pipeline, not here.

## 2. Per-ficha table

Post-fix (T4 follow-up) dedup signals. Columns: `url` (exact after
canonicalization), `title_exact` (normalized equality, parentheticals
stripped), `title_substring` (weaker containment ≥ 8 chars). Two or more
signals → `MATCHES`; one → `PARTIAL`; none → `NEW`. `INTRA-BATCH` would
appear here if the parser flagged a record as a within-batch duplicate;
this run has none.

| Proposed ID | Title (truncated) | Country | URL (host) | Dedup |
|---|---|---|---|---|
| BR-SCOUT-001 | Alegoria da República Brasileira — Revista Illustrada | BR | commons.wikimedia.org | **PARTIAL → BR-005** (title_substring) |
| BR-SCOUT-002 | Alegoria à República — Capa da Revista Illustrada n. 566 | BR | commons.wikimedia.org | NEW |
| BR-SCOUT-003 | Alegoria da República — Manoel Lopes Rodrigues (óleo s.t.) | BR | artsandculture.google.com | **PARTIAL → BR-005** (title_substring) |
| BR-SCOUT-004 | Alegoria à Lei de 13 de Maio de 1888 (estudo) | BR | mhn.museus.gov.br | NEW |
| BR-SCOUT-005 | A Justiça (escultura monumental) — STF, Brasília | BR | commons.wikimedia.org | **PARTIAL → BR-009** (title_substring) |
| BR-SCOUT-006 | Suffragistas — Fon-Fon, 16 de maio de 1914 | BR | bndigital.bn.gov.br | NEW |
| BR-SCOUT-007 | O Feminismo Triumphante — Revista da Semana, 20 maio 1933 | BR | bndigital.bn.gov.br | NEW |
| FR-SCOUT-001 | La République aimable | FR | gallica.bnf.fr | **MATCHES → FR-005** (url + title_exact) |
| FR-SCOUT-002 | La République nous appelle... (État avec remarque) | FR | gallica.bnf.fr | **PARTIAL → FR-008** (title_exact) |
| FR-SCOUT-003 | République de Clésinger (fotografia de demonstração) | FR | gallica.bnf.fr | NEW |
| FR-SCOUT-004 | Unité indivisibilité de la République (j'ai rompu mes c…) | FR | gallica.bnf.fr | NEW |
| FR-SCOUT-005 | Buste de la République (série de 4 fotografias) | FR | gallica.bnf.fr | **PARTIAL → FR-009** (title_exact) |
| FR-SCOUT-006 | Liberté (Moitte/Janinet) | FR | gallica.bnf.fr | **PARTIAL → FR-038** (title_exact) |
| FR-SCOUT-007 | La République (en hauteur) — Exposição Internacional 1889 | FR | gallica.bnf.fr | NEW |
| FR-SCOUT-008 | Étude pour le 1er mai? (Steinlen) | FR | gallica.bnf.fr | NEW |

Post-fix distribution: `MATCHES` = 1, `PARTIAL` = 6, `NEW` = 8,
`INTRA-BATCH` = 0.

## 3. Dedup deep-dive

### 3.1 How the classifier works (post-fix)

`DedupIndex.classify` now produces a **signal list** rather than a single
winner. Three signal families:

1. **`url`** — exact equality after `_canonicalize_url` (lowercase host,
   strip `www.`, drop trailing `/`, force `https` on known archive hosts:
   `gallica.bnf.fr`, `europeana.eu`, `loc.gov`, `numista.com`,
   `bildindex.de`, `rijksmuseum.nl`, `bn.gov.br`,
   `bndigital.bnportugal.gov.pt`). Applied at both index-build and query
   time, so http/https and www./non-www variants collide.
2. **`title_exact`** — normalized-title dict equality. Normalization
   lowercases, strips diacritics, removes punctuation, **and strips
   parenthetical content** (so `"La République aimable (Félicien Rops)"`
   reduces to `"la republique aimable"`).
3. **`title_substring`** — second-pass containment check over the title
   index (≥ 8 chars on each side, iterates the full index). Promotes
   weaker prefix/substring matches that exact equality would miss.

Classification: zero signals → `NEW`; exactly one signal → `PARTIAL`; two
or more orthogonal signals → `MATCHES`.

**Correction of the pre-fix report.** An earlier revision of §3
incorrectly claimed the original (pre-fix) classifier matched
FR-SCOUT-001 ↔ FR-005 via URL **and** a "normalized-title substring
match". That was false: the original `DedupIndex.classify` did only
exact-equality dict lookup on normalized titles, and the authorial
parenthetical `(Félicien Rops)` broke that exact match, so only the URL
signal registered — which is why the status was `PARTIAL`, not `MATCHES`.
The T4 review follow-up (I1) added the explicit substring pass and (also
I1) made `_normalize_title` strip parentheticals, which is what now
drives the `title_exact` match for this pair.

### 3.2 FR-SCOUT-001 ↔ existing FR-005 (MATCHES, post-fix)

- **New (LPAI v2):** `La République aimable` — no creator in title.
- **Existing corpus item FR-005:** `La République aimable (Félicien Rops)`,
  dated 1871, regime `contra-alegoria`.
- **Shared signals after the fix:**
  - `url`: `https://gallica.bnf.fr/ark:/12148/btv1b531842166` (identical
    on both sides; canonicalization has no effect here because both are
    already `https`, no `www`, no trailing slash — but would equally
    absorb a legacy `http://www.gallica.bnf.fr/...` link if one appeared).
  - `title_exact`: after stripping the `(Félicien Rops)` parenthetical,
    the two titles normalize to the same string `"la republique aimable"`.
- **Classification:** two orthogonal signals → **MATCHES** (was `PARTIAL`
  in the original T4 run because the pre-fix classifier used
  exact-equality on normalized titles without stripping parentheticals;
  URL alone gave the single PARTIAL hit).

**Resolution unchanged:** treat as an enrichment of `FR-005`, not a new
corpus entry. The staged JSON line and draft vault note for FR-SCOUT-001
should be archived but not promoted. Merge LPAI-specific fields into
`FR-005` (`lpai_v2_code`, `classe`, `atributos`, `nota_analitica`,
updated ABNT) manually or via `records_to_corpus.py` after editing the
canonical record.

### 3.3 Other PARTIAL matches — need human adjudication

The I1 title-substring pass plus the parenthetical-stripping normalization
surfaced five additional PARTIAL overlaps that the pre-fix classifier
could not see. Every one needs a human call before promotion.

| Candidate | Existing | Signal | Notes |
|---|---|---|---|
| BR-SCOUT-001 | BR-005 `Alegoria da República (Décio Villares)` | `title_substring` | Different object (Agostini litho in Revista Illustrada vs. Villares oil). Both carry the stem "alegoria da republica" — substring match is noise here. Promote as new. |
| BR-SCOUT-003 | BR-005 `Alegoria da República (Décio Villares)` | `title_substring` | Different object (Lopes Rodrigues oil vs. Villares oil). Same substring noise as BR-SCOUT-001. Promote as new. |
| BR-SCOUT-005 | BR-009 `A Justiça (Alfredo Ceschiatti, STF Brasília)` | `title_substring` | **Same object.** LPAI ficha title omits the Ceschiatti attribution. Enrich BR-009, do not promote as new. |
| FR-SCOUT-002 | FR-008 `La République nous appelle... (Steinlen)` | `title_exact` | Same object, different edition/state (état avec remarque). Promote as a sibling variant record cross-linked to FR-008, or merge as enrichment — Ana decides. |
| FR-SCOUT-005 | FR-009 `Buste de la République (Agence Rol)` | `title_exact` | Same object family (Buste de la République series). Enrich FR-009 with the "série de 4 fotografias" grouping, or promote as a sibling. |
| FR-SCOUT-006 | FR-038 `Liberté (d'après Moitte)` | `title_exact` | Same object. Canonical FR-038 has no URL; LPAI ficha supplies the Gallica URL. Enrich FR-038 with the URL instead of creating a duplicate. |

`title_substring` matches are weaker than `title_exact` and frequently
false-positive on corpus-wide stems like "alegoria da república". Treat
them as review triggers, not verdicts. `title_exact` matches (where
parenthetical stripping produced the equality) are much stronger signals
— assume same-or-sibling object and adjudicate accordingly.

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
- **Placeholder-URL guard (C3).** The parser no longer silently slots
  `https://example.org/lpai-placeholder` into records with empty URLs.
  The placeholder is still written (master-record + webscout-output both
  require `format: uri`), but the record now also carries an all-caps
  `placeholder_url_BLOCK_PROMOTE` audit flag. A downstream promote step
  can `grep` for this marker and refuse to merge those records into the
  canonical ledger until a real URL lands. This run produced zero
  placeholder records — all 15 fichas have URLs.

## 5. Required human actions before merge

### a. Disambiguate FR-SCOUT-001 and the five other PARTIAL matches

**COMPLETED 2026-04-22** via Council & Santa method adjudication.

FR-SCOUT-001 is a MATCHES result — merge into FR-005 (do not promote as a
new row). The six PARTIAL results were adjudicated as follows:

| Candidate | Existing | Decision | Method | Rationale |
|---|---|---|---|---|
| BR-SCOUT-001 | BR-005 | **NEW** | Santa | title_substring noise; different creators (Agostini lithograph vs Villares oil) |
| BR-SCOUT-003 | BR-005 | **NEW** | Santa | title_substring noise; different creators (Lopes Rodrigues 1896 vs Villares 1888) |
| BR-SCOUT-005 | BR-009 | **ENRICH** | Council | Same object (Ceschiatti sculpture); LPAI title omits attribution |
| FR-SCOUT-002 | FR-008 | **ENRICH** | Council | Same object, different state (etat avec remarque); atlas does not need separate panel |
| FR-SCOUT-005 | FR-009 | **ENRICH** | Council | Same object family; photographic series enriches the bust record |
| FR-SCOUT-006 | FR-038 | **ENRICH** | Santa | Same object; LPAI supplies missing Gallica URL and Janinet attribution |

Log: `data/staging/t4-adjudication-log.json`.
Four existing records enriched with LPAI evidence; two staged records
approved for promotion.

### b. Queue the new records for IconoCode coding

After merge, the T3 coding queue grows by the number of items that land
as fresh entries (between 8 and 14, depending on the §3.3 adjudications).

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

**DO NOT run these until actions 5.a–5.c above are satisfied, and in
particular until you have `grep`-checked the staged JSONL for
`placeholder_url_BLOCK_PROMOTE` and `intra_batch_duplicate` flags.** This
is the skeleton merge pipeline; see `docs/OPERATING_MODEL.md`
§release-gate for policy.

```bash
# 0. Gate: refuse to promote records with placeholder URLs or intra-batch duplicates
grep -l "placeholder_url_BLOCK_PROMOTE\|intra_batch_duplicate" \
  data/staging/fichas-lpai-v2-parsed.jsonl \
  && echo "STOP — clean up flagged records first" && exit 1

# 1. Promote (approved) vault drafts to vault/candidatos/
#    Review each file, then:
cp data/staging/vault-drafts-lpai-v2/BR-SCOUT-001*.md vault/candidatos/
# ... repeat for each approved ficha ...

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
