<!-- Generated: 2026-06-22 | Files scanned: 79 scripts + 8 notebooks + 7 schemas | Token estimate: ~750 -->
# Architecture — ICONOCRACIA (doctoral-thesis monorepo)

**Type:** research monorepo (Python pipeline + corpus data + Obsidian vault + thesis manuscript). NOT a web app — `webiconocracy` retired; only public surface is a Cloudflare Worker companion + HF Space.

## Dual-agent pipeline (acquisition → coding → ledger)
```
WebScout/SCOUT          IconoCode                  Master records
(archive discovery) ──► (Panofsky 3-level +    ──► data/processed/records.jsonl
Gallica/LoC/Europeana   10 purification 0–3          (canonical ledger)
/Numista/Colnect)       indicators + regime)             │
        │                                                ▼
        ▼                                    corpus/corpus-data.json (public export)
   vault/candidatos/  (Obsidian XX-NNN notes, auxiliary mirror)
```

## Corpus lifecycle (source-of-truth order)
1. `data/processed/records.jsonl` — operational canonical ledger (master-record schema)
2. `corpus/corpus-data.json` — public export (browsers/dashboards/HF), derived via `records_to_corpus.py`
3. `data/processed/purification.jsonl` — endurecimento coding ledger
4. `vault/candidatos/` — Obsidian cataloguing mirror (XX-NNN Title.md)

## Subsystems (top-level)
- `tools/scripts/` (79) — automation pipeline; `tools/schemas/` (7 JSON schemas)
- `notebooks/` (01–08) — quantitative analysis (exploratory → kruskal_wallis → regression → correspondence → temporal → clustering → dimensionality → multidim_scoring)
- `tese/manuscrito/` — thesis chapters (Markdown → Pandoc → DOCX/PDF); `tese/{drafts,revisoes,artigos,council}`
- `corpus/` — corpus-data.json + HTML dashboards + candidatos/
- `data/{raw,processed}/` — raw metadata-only (ADR-001: binaries → Drive/SSD); processed ledgers + figures (fig_01..fig_13)
- `deploy/` — companion (Cloudflare Worker), HF corpus-explorer-space, docker/, tropical-atlas
- `vault/` — Obsidian (candidatos, sessoes, meta, tese); `wiki/` — second vault

## Methodology axes
- **3 iconocratic regimes:** FUNDACIONAL → NORMATIVO → MILITAR → CONTRA-ALEGORIA
- **10 purification indicators** (ordinal 0–3) — see `data.md`
- **N-stratification** (analytic-N debate): by `coded_by` instrument × validity stratum — see `data.md` + `docs/decisions/DIALETICA-N165-vs-265.md`

## See also
- `pipeline.md` — the 79 scripts by function
- `data.md` — stores, schemas, strata
- `dependencies.md` — env, MCPs, archives, CI, deploy
- Repo `CLAUDE.md` (authoritative), `docs/decisions/*` (ADRs/dialectics)
