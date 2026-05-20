# Tropical Atlas — Iconocracia Corpus Explorer

Public atlas for the ICONOCRACY doctoral research corpus (PPGD/UFSC).
Deployed as a **Cloudflare Pages** static site with a **Pages Function** (Hono) backend
reading from the shared **D1** database and **R2** image bucket.

## Architecture

```
deploy/tropical-atlas/
├── public/              ← Static frontend (index.html — no build step)
│   └── index.html       ← Atlas + Admin SPA
├── functions/
│   └── api/[[route]].ts ← Hono API (Cloudflare Pages Function)
├── migrations/
│   └── 0001_atlas_entries.sql  ← D1 schema
├── wrangler.toml        ← Bindings: CORPUS_DB (D1), CORPUS_IMAGES (R2)
└── package.json
```

## Features

- **Image cards** with regime badge, LPAI score, motif label
- **5 filters**: country, medium, LPAI regime, period, free-text search
- **Citation popover**: full entry detail, all LPAI scores, ABNT NBR 6023:2025 reference, copy button
- **Admin panel**: drag-and-drop CSV import (preview + commit), export, corpus stats, regime chart
- **Dark mode** (system preference + toggle)
- **Grid / list** view toggle

## CSV Import

The import flow accepts the exact `corpus_dataset.csv` column headers from
`data/processed/`. No transformation needed — upload and commit.

Import modes:
- **Acrescentar** (append): adds rows, updates existing by `id` (UPSERT)  
- **Substituir tudo** (replace): clears all entries before importing

## Bindings (wrangler.toml)

Reuses existing resources from `iconocracia-companion`:

| Binding        | Resource                                |
|----------------|-----------------------------------------|
| `CORPUS_DB`    | D1 `iconocracy-corpus` (database_id: `77c09df7-…`) |
| `CORPUS_IMAGES`| R2 `iconocracia-images`                 |

## Deploy

```bash
cd deploy/tropical-atlas
npm install
# Apply D1 migration (once):
npx wrangler d1 execute iconocracy-corpus --file=migrations/0001_atlas_entries.sql
# Deploy Pages:
npx wrangler pages deploy public --project-name=tropical-atlas
```

## Local dev

```bash
npx wrangler pages dev public --compatibility-date=2026-04-01 --port=8788
```

Note: Pages Functions (`functions/`) are automatically picked up by Wrangler in dev mode.
