# Docker — iconocracy-corpus

Reproducible local dev: web app + MCP server + Python tools (conda) + thesis compile (pandoc/latex). No host install needed beyond Docker Desktop.

## Services

| Service | Image base                | Purpose                                      | Profile     |
|---------|---------------------------|----------------------------------------------|-------------|
| web     | node:22-alpine            | Vite dev for `webiconocracy/` on :3000       | (default)   |
| mcp     | node:22-alpine            | `gallica-mcp-server` (tsx watch)             | (default)   |
| tools   | mambaorg/micromamba:1.5   | Conda env `iconocracy` (Py 3.11 + scripts)   | `tools`     |
| thesis  | pandoc/latex:3.5          | `vault/tese/Makefile` compile (DOCX/PDF)     | `thesis`    |

Default `docker compose up` runs **web + mcp** only. `tools` and `thesis` are on-demand.

## Quickstart

```bash
cd ~/iconocracy-corpus

# Long-running dev services
docker compose up                              # web :3000, mcp foreground

# Run schema validator (one-shot)
docker compose run --rm tools \
    python tools/scripts/validate_schemas.py

# Coding progress
docker compose run --rm tools \
    python tools/scripts/code_purification.py --status

# Compile thesis to DOCX
docker compose run --rm thesis make docx

# Compile thesis to PDF (see Font Caveat below)
docker compose run --rm thesis make pdf

# Shell into conda env interactively
docker compose run --rm tools bash
```

## Volumes

- **bind mount** `webiconocracy/` and `indexing/gallica-mcp-server/` for hot reload.
- **named volumes** `web_node_modules` / `mcp_node_modules` shield container deps from host overlay.
- `tools` mounts entire repo at `/workspace` for read/write of `corpus/`, `data/`, scripts.
- `thesis` mounts only `vault/tese/` at `/thesis`.

## Apple Silicon Note

`pandoc/latex` is amd64-only. The `thesis` service is pinned to `platform: linux/amd64` and runs via Rosetta on M1/M2/M3 Macs. Slower (~2-3x) but works. The other 3 services are multi-arch.

## Font Caveat (PDF target)

`vault/tese/Makefile` requests `Times New Roman`. Not in Alpine. Either:

- Substitute in Makefile: `-V mainfont="TeX Gyre Termes"` (free Times-equivalent), or
- Mount host fonts via the `thesis` service in `docker-compose.yml`:
  ```yaml
  volumes:
    - ./vault/tese:/thesis
    - /System/Library/Fonts/Supplemental:/usr/share/fonts/truetype/macos:ro
  ```
  (macOS path; Linux/Windows differ.) Then `fc-cache -f` once.

## Production / Cloud Run

These Dockerfiles are **dev-only** (multi-stage `dev` target, hot reload, no production hardening). For Cloud Run / production, add a `production` stage in `web.Dockerfile`:

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY webiconocracy/ ./
RUN npm run build

FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

## Troubleshooting

```bash
docker compose ps                      # what's running
docker compose logs -f web             # follow logs
docker compose exec web sh             # shell in
docker compose down -v                 # nuke volumes (DESTRUCTIVE — re-installs node_modules)

# Rebuild after env.yml or package.json change
docker compose build --no-cache tools
docker compose build web mcp
```

## What's NOT containerized

- Firebase emulator (use `firebase emulators:start` on host until needed)
- Jupyter notebooks (run from `tools` shell: `docker compose run --rm -p 8888:8888 tools jupyter lab --ip=0.0.0.0 --no-browser --allow-root`)
- Cloud Run deploy (still uses `gcloud run deploy` from host)
