# Handoff

## State
I ran Sprint 0 (backup all repos) + full security/architecture cleanup on `iconocracy-corpus`. 122 files removed from git (-9,904 lines), history scrubbed with `git filter-repo` and force-pushed. All 157 downloadable corpus images recovered to `data/raw/{BR,FR,UK,DE,US,BE}` (real dirs, no longer SSD symlinks). SSD was reformatted for Time Machine — no other backup of original images exists. 8 items still missing (BR-016, DE-NOTG-1921, FR-036/38/39/40/47/48 — no source URLs).

## Next
1. SCOUT campaigns for the 8 missing items (manually-ingested orphans with no URLs)
2. 52 untracked files remain in hub — individual triage (vault aula notes, tools scripts, test data)
3. Rotate Anna's Archive API key + regenerate GitHub recovery codes + check Firebase Security Rules

## Context
- `gh` CLI has TLS cert issue on macOS 26 — `gh api` fails, but `curl` with `gh auth token` works. Repo creation done via curl + GitHub API.
- LOC downloads require real Chrome via CDP (`tools/scripts/loc_download.mjs`) — Cloudflare Turnstile blocks urllib and headless Playwright.
- `data/raw/` dirs are now real folders (not symlinks to `/Volumes/ICONOCRACIA`). `.gitignore` still excludes them per ADR-001.
- `tools/scripts/node_modules/` was created by LOC agent — consider cleaning up or gitignoring.
