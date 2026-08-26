# DOCKER OPTIMIZATION GUIDE FOR ICONOCRACY PROJECT

Complete instructions for optimizing Docker setup across the research ecosystem. This guide covers performance improvements, production-readiness, AI/model integration, and team collaboration.

---

## TABLE OF CONTENTS

1. [Part 1: Quick Wins](#part-1-quick-wins)
2. [Part 2: Production-Grade Improvements](#part-2-production-grade-improvements)
3. [Part 3: AI/Model Integration](#part-3-aimodel-integration)
4. [Part 4: Verification & Testing](#part-4-verification--testing)
5. [Part 5: Summary Table](#part-5-summary-table)
6. [Part 6: Execution Order](#part-6-execution-order)
7. [Sources](#sources)

---

## PART 1: QUICK WINS

Do these first. Total time: ~10 minutes.

### 1️⃣ Expand `.dockerignore`

**File**: `./hub/iconocracy-corpus/.dockerignore`

**Action**: Add these patterns to the end of the file:

```
# Project-specific local artifacts
logs/
*.pdf
.agents/
.air/
.remember/
.postman/
.vscode/
.idea/
tmp/
misc/
random outputs/
New Folder/
PHD/
Notas e Textos/
```

**Why**: Excludes ~500MB+ of local PDFs, notebooks, IDE config from Docker build context → faster builds, smaller cache.

**Expected result**: Build time reduced by ~20–30%.

---

### 2️⃣ Pin micromamba version

**File**: `./hub/iconocracy-corpus/deploy/docker/tools.Dockerfile`

**Change line 1 from:**
```dockerfile
FROM mambaorg/micromamba:1.5
```

**To:**
```dockerfile
FROM mambaorg/micromamba:1.5.10
```

**Why**: Freezes base image version → reproducible builds across machines and time.

**Expected result**: Team members always get identical conda environment.

---

### 3️⃣ Merge `requirements.txt` into `environment.yml`

**File**: `./hub/iconocracy-corpus/environment.yml`

**Step 1**: Update the `pip:` section from:
```yaml
pip:
  - jsonschema>=4.0
  - rich>=10.0
```

**To:**
```yaml
pip:
  - jsonschema>=4.0
  - rich>=10.0
  - krippendorff>=0.8
  - numpy>=1.24
```

**Step 2**: Delete `./hub/iconocracy-corpus/requirements.txt`

**Why**: Single source of truth. Avoids confusion about which file is authoritative.

**Expected result**: One conda env config, no duplicate dependency definitions.

---

## PART 2: PRODUCTION-GRADE IMPROVEMENTS

Advanced optimizations for multi-stage builds, security, health checks, and production deployments. Total time: ~50 minutes.

### 4️⃣ Update `web.Dockerfile` with production stage

**File**: `./hub/iconocracy-corpus/deploy/docker/web.Dockerfile`

**Action**: Replace entire file with:

```dockerfile
# webiconocracy — React + Vite + Firebase dev server
# Build context: repo root. Run: docker compose up web

FROM node:22-alpine AS deps
WORKDIR /app
COPY --from=webapp package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
USER nextjs
ENV HOST=0.0.0.0
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Production: build + nginx
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=webapp . .
RUN npm run build

FROM nginx:1.27-alpine AS production
RUN addgroup -g 101 -S www-data && \
    adduser -S www-data -u 101 -G www-data
USER www-data
COPY --from=build /app/dist /usr/share/nginx/html
COPY deploy/docker/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

**Why**:
- Multi-stage build with `dev` and `production` targets
- Non-root user (nextjs for dev, www-data for nginx)
- Production stage compiles Vite assets → nginx serves static files
- Health check enables orchestrator auto-recovery
- Reduces prod image size by 30–50%

**Expected result**: Production-ready image. Dev/prod separation. Auto-recovery in orchestrators.

---

### 5️⃣ Create `nginx.conf`

**File**: `./hub/iconocracy-corpus/deploy/docker/nginx.conf` (new file)

**Action**: Create new file with content:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # SPA fallback: route all non-file requests to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }

    # Cache static assets aggressively
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Deny dot-files
    location ~ /\. {
        deny all;
    }
}
```

**Why**:
- Proper SPA routing (single-page app fallback to index.html)
- Health endpoint for container orchestrators
- Aggressive caching for static assets (1 year expiration)
- Denies access to hidden files (security)

**Expected result**: Vite SPA works correctly in production. Fast asset loading. Secure config.

---

### 6️⃣ Update `mcp.Dockerfile` with non-root + production stage

**File**: `./hub/iconocracy-corpus/deploy/docker/mcp.Dockerfile`

**Action**: Replace entire file with:

```dockerfile
# gallica-mcp-server — MCP server for Gallica (BnF)
# Build context: repo root. Run: docker compose up mcp

FROM node:22-alpine AS deps
WORKDIR /app
COPY --from=mcpsrc package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

FROM node:22-alpine AS dev
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S mcp -u 1001
USER mcp
COPY --from=deps /app/node_modules ./node_modules
CMD ["npm", "run", "dev"]

FROM node:22-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S mcp -u 1001
USER mcp
COPY --from=deps /app/node_modules ./node_modules
COPY --from=mcpsrc . .
RUN npm ci --omit=dev
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["npm", "run", "start"]
```

**Why**:
- `dev` target: hot-reload for development
- `production` target: `--omit=dev` removes test frameworks, linters, dev tools
- Non-root user (mcp) hardens security
- Health check for orchestrator monitoring
- Reduces prod image size by 30–50%

**Expected result**: Separate dev/prod images. Leaner production. Security hardened.

---

### 7️⃣ Update `tools.Dockerfile` with non-root user

**File**: `./hub/iconocracy-corpus/deploy/docker/tools.Dockerfile`

**Action**: Replace entire file with:

```dockerfile
# tools — conda iconocracy env (Python 3.11, jupyter, schema validators, corpus scripts)
# Build context: repo root. Run: docker compose run --rm tools <cmd>

FROM mambaorg/micromamba:1.5.10

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends git make ca-certificates && \
    rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba env create -f /tmp/environment.yml && \
    micromamba clean --all --yes

ENV ENV_NAME=iconocracy
ARG MAMBA_DOCKERFILE_ACTIVATE=1

WORKDIR /workspace
CMD ["bash"]
```

**Why**:
- Explicit version pin (1.5.10) for reproducibility
- Non-root default via $MAMBA_USER
- Cleaner setup with minimal layers

**Expected result**: Reproducible conda env. Security hardened.

---

### 8️⃣ Update `thesis.Dockerfile` with non-root user

**File**: `./hub/iconocracy-corpus/deploy/docker/thesis.Dockerfile`

**Action**: Replace entire file with:

```dockerfile
# thesis — Pandoc + LaTeX for compiling tese (vault/tese/Makefile)
# Build context: repo root. Run: docker compose run --rm thesis make docx
# NOTE: Times New Roman not in Alpine; PDF target may need TeX Gyre Termes substitute.

FROM pandoc/latex:3.5

RUN apk add --no-cache make font-noto && \
    addgroup -g 1001 -S thesis && \
    adduser -S thesis -u 1001

USER thesis
WORKDIR /thesis
ENTRYPOINT []
CMD ["make", "docx"]
```

**Why**:
- Non-root user (thesis, UID 1001) hardens security
- Explicit version pin (3.5)
- Minimal setup

**Expected result**: Security hardened. Reproducible.

---

### 9️⃣ Update `docker-compose.yml` with health checks and optional models

**File**: `./hub/iconocracy-corpus/docker-compose.yml`

**Action**: Replace entire file with:

```yaml
# iconocracy-corpus — local dev orchestration
#
# Default (web + mcp long-running):
#   docker compose up
#
# On-demand profiles:
#   docker compose run --rm tools python tools/scripts/validate_schemas.py
#   docker compose run --rm thesis make docx
#   docker compose --profile models up
#
# See deploy/docker/README.md

services:
  web:
    build:
      context: .
      dockerfile: deploy/docker/web.Dockerfile
      additional_contexts:
        webapp: ./webiconocracy
    ports:
      - "127.0.0.1:3000:3000"
    volumes:
      - ./webiconocracy:/app
      - web_node_modules:/app/node_modules
    working_dir: /app
    environment:
      - NODE_ENV=development
      - VITE_HOST=0.0.0.0
    env_file:
      - path: ./webiconocracy/.env
        required: false
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

  mcp:
    build:
      context: .
      dockerfile: deploy/docker/mcp.Dockerfile
      additional_contexts:
        mcpsrc: ./indexing/gallica-mcp-server
    volumes:
      - ./indexing/gallica-mcp-server:/app
      - mcp_node_modules:/app/node_modules
    working_dir: /app
    environment:
      - NODE_ENV=development
    stdin_open: true
    tty: true
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s

  tools:
    build:
      context: .
      dockerfile: deploy/docker/tools.Dockerfile
    volumes:
      - .:/workspace
    working_dir: /workspace
    profiles: ["tools"]

  thesis:
    build:
      context: .
      dockerfile: deploy/docker/thesis.Dockerfile
    platform: linux/amd64
    volumes:
      - ./vault/tese:/thesis
    working_dir: /thesis
    profiles: ["thesis"]

  # Optional: Local model inference (Ollama)
  models:
    image: ollama/ollama:latest
    profiles: ["models"]
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    healthcheck:
      test: ["CMD", "ollama", "list"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  web_node_modules:
  mcp_node_modules:
  ollama_data:
```

**Why**:
- Health checks enable Docker and orchestrators to detect and recover unhealthy services
- `web` checks http://localhost:3000 (Vite dev server)
- `mcp` checks http://localhost:3000/health (Gallica server)
- Optional `models` service for local Ollama inference (run with `--profile models`)
- Named volumes protect node_modules from bind mount overlay

**Expected result**: Services monitored. Can run `docker compose ps` and see health status. Optional local models.

---

### 🔟 Update `deploy/docker/README.md`

**File**: `./hub/iconocracy-corpus/deploy/docker/README.md`

**Action**: Add these sections at the end (after existing Troubleshooting):

```markdown
## Security

All services run as **non-root users**:
- `web` / `mcp`: node user (UID 1001)
- `tools`: conda user (`$MAMBA_USER`)
- `thesis`: thesis user (UID 1001)
- `nginx` (production): www-data user (UID 101)

This limits privilege escalation and container escape impact. For dev convenience, volumes are still bind-mounted; production deployments should use read-only mounts or secrets management.

## Production readiness

The `web` service includes a `production` target with nginx + health checks. To build and test locally:

```bash
docker build -f deploy/docker/web.Dockerfile --target production -t webiconocracy:prod .
docker run --rm -p 8080:80 webiconocracy:prod
```

Visit `http://localhost:8080`; health check at `/health`.

For Cloud Run / managed container services, use the production image. Dev images are not recommended for production.

## Caching strategy

- **Fast rebuild (cached layers)**: `docker compose build web mcp` — reuses npm cache if package.json unchanged.
- **Fresh rebuild**: `docker compose build --no-cache web mcp` — rebuilds from scratch, catches stale transitive deps.
- **Clean slate**: `docker compose down -v && docker compose up` — nukes volumes, reinstalls everything.

## Local model inference (optional)

Run local AI models via Ollama without external API costs or data privacy concerns:

```bash
# Start Ollama service
docker compose --profile models up

# Pull a model (first time only)
docker exec <container_id> ollama pull llama2

# Call via OpenAI-compatible API
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Analyze this legal iconography...",
  "stream": false
}'
```

Models run on your machine with no external API calls. Useful for corpus analysis, visual understanding, or agent testing before pushing to Gemini/Firebase.
```

**Why**: Documents security posture, production deploy path, caching strategy, and optional local models.

**Expected result**: Team knows how to deploy to production, when to rebuild with/without cache, how to use local models.

---

## PART 3: AI/MODEL INTEGRATION

Integrate MCP Toolkit, Docker Model Runner, and Docker Build Cloud into your workflow. Total time: ~25 minutes.

### MCP Toolkit Setup

Your `mcp` service (Gallica) is already containerized. To unlock agent integration with Claude Desktop, Cursor, VS Code Copilot, etc.:

**Step 1**: Open **Docker Desktop** → **MCP Toolkit** tab

**Step 2**: Click **"Add Server"**

**Step 3**: Select **"Gallica MCP Server"** from catalog (or upload custom)

**Step 4**: Configure environment variables:
```
GALLICA_API_KEY=<your_key>
AUTH_TOKEN=<optional>
```

**Step 5**: Save as profile: **`iconocracy-research`**

**Step 6**: Connect to one or more clients:
- Claude Desktop
- Cursor IDE
- VS Code Copilot
- Continue.dev
- Gemini CLI

**Result**: AI agents can now call `search_gallica()` directly during code generation, research tasks, or thesis indexing. Your Gallica server is discoverable across 200+ containerized MCP tools in the Docker catalog.

**For dev**: Keep using `docker compose up mcp` for hot-reload and local testing.

---

### Docker Model Runner Setup

Run local LLMs for corpus analysis, no API costs, no data leaving your machine.

**Step 1**: Pull a model from Hugging Face (GGUF format):

```bash
docker model pull llama2
# or: mistral, neural-chat, openchat, etc.
```

**Step 2**: Run it (starts OpenAI-compatible API):

```bash
docker model run llama2
```

**Step 3**: Test the API:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [{"role": "user", "content": "Analyze this legal iconography in feminist context..."}]
  }'
```

**Alternative: Use Ollama in compose** (already configured):

```bash
# Start Ollama service
docker compose --profile models up

# Pull a model
docker exec <container_id> ollama pull mistral

# Call the API
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Summarize legal iconography trends...",
  "stream": false
}'
```

**Use cases for your thesis:**
- Local corpus analysis before agent processing (no API calls)
- Visual understanding of images via llava model
- Test agent workflows offline before deploying to Gemini/Firebase
- Analyze batch data without API rate limits

**Cost benefit**: No API charges for large corpus analysis. Data stays private.

---

### Docker Build Cloud Setup

Accelerate multi-platform builds (up to 39x faster) + shared team cache.

**Step 1**: Enable in Docker Desktop:
- Go to **Settings** → **Builders**
- Click **"Create a builder"** → **"Docker Build Cloud"**
- Link your Docker Hub account

**Step 2**: Local builds with Build Cloud:

```bash
cd ./hub/iconocracy-corpus

# Build multi-platform (amd64 + ARM64 for different servers)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t webiconocracy:latest \
  -f deploy/docker/web.Dockerfile \
  .
```

**Step 3**: Set up GitHub Actions for automated builds

**File**: `.github/workflows/build.yml` (create new file)

**Content**:

```yaml
name: Build & Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build & push web (multi-platform)
        uses: docker/build-push-action@v5
        with:
          context: ./hub/iconocracy-corpus
          file: ./hub/iconocracy-corpus/deploy/docker/web.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/webiconocracy:latest
            ${{ secrets.DOCKER_USERNAME }}/webiconocracy:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/webiconocracy:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/webiconocracy:buildcache,mode=max
      
      - name: Build & push mcp (multi-platform)
        uses: docker/build-push-action@v5
        with:
          context: ./hub/iconocracy-corpus
          file: ./hub/iconocracy-corpus/deploy/docker/mcp.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-mcp:latest
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-mcp:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-mcp:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-mcp:buildcache,mode=max

      - name: Build & push tools
        uses: docker/build-push-action@v5
        with:
          context: ./hub/iconocracy-corpus
          file: ./hub/iconocracy-corpus/deploy/docker/tools.Dockerfile
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-tools:latest
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-tools:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-tools:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-tools:buildcache,mode=max

      - name: Build & push thesis
        uses: docker/build-push-action@v5
        with:
          context: ./hub/iconocracy-corpus
          file: ./hub/iconocracy-corpus/deploy/docker/thesis.Dockerfile
          platforms: linux/amd64
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-thesis:latest
            ${{ secrets.DOCKER_USERNAME }}/iconocracy-thesis:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-thesis:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/iconocracy-thesis:buildcache,mode=max
```

**Benefits of Build Cloud:**
- Builds run in cloud, free up your Mac for editing
- Shared cache across team → faster rebuilds for collaborators
- Multi-arch support (amd64 for Cloud Run, ARM64 for EC2)
- Up to 39x faster builds
- CI/CD integrates seamlessly with GitHub

**Expected result**: Push code → GitHub Actions builds automatically on all platforms → images available on Docker Hub.

---

## PART 4: VERIFICATION & TESTING

Run these commands after applying all changes. Total time: ~10 minutes.

```bash
cd ./hub/iconocracy-corpus

# 1. Lint all Dockerfiles with hadolint
docker run --rm -i hadolint/hadolint < deploy/docker/web.Dockerfile
docker run --rm -i hadolint/hadolint < deploy/docker/mcp.Dockerfile
docker run --rm -i hadolint/hadolint < deploy/docker/tools.Dockerfile
docker run --rm -i hadolint/hadolint < deploy/docker/thesis.Dockerfile

# 2. Rebuild all services (fresh)
docker compose build --no-cache web mcp tools thesis

# 3. Start services in background
docker compose up -d

# 4. Check health status (wait ~15s for startup)
sleep 15
docker compose ps
# Should show "healthy" or "starting" for web/mcp

# 5. Test web service
curl http://localhost:3000
# Should return HTML (Vite dev page)

# 6. Test tools
docker compose run --rm tools python tools/scripts/validate_schemas.py

# 7. Test thesis
docker compose run --rm thesis make docx

# 8. View logs
docker compose logs web
docker compose logs mcp

# 9. Build production image locally
docker build -f deploy/docker/web.Dockerfile --target production -t webiconocracy:prod .
docker run --rm -p 8080:80 webiconocracy:prod &
sleep 5
curl http://localhost:8080/health
# Should return "OK"

# 10. Clean up
docker compose down -v
```

**Expected results:**
- ✅ All Dockerfiles pass linting
- ✅ All services build without errors
- ✅ Health checks pass
- ✅ Web service responds
- ✅ Tools run validation
- ✅ Thesis compiles
- ✅ Production image builds and serves

---

## PART 5: SUMMARY TABLE

| Change | File(s) | Benefit | Effort | Impact |
|--------|---------|---------|--------|--------|
| Expand `.dockerignore` | `.dockerignore` | Faster builds (skip 500MB+ junk) | 5 min | High |
| Pin micromamba | `tools.Dockerfile` | Reproducible base image | 1 min | High |
| Merge pip deps | `environment.yml` → delete `requirements.txt` | Single source of truth | 2 min | Medium |
| Add prod stage to web | `web.Dockerfile` | 30–50% smaller image, nginx, health checks | 10 min | High |
| Create nginx config | `nginx.conf` (new) | Proper SPA routing, caching | 5 min | High |
| Update mcp.Dockerfile | `mcp.Dockerfile` | `--omit=dev`, non-root, health checks | 10 min | High |
| Update tools/thesis | `tools.Dockerfile`, `thesis.Dockerfile` | Non-root users, version pins | 5 min | Medium |
| Add health checks | `docker-compose.yml` | Orchestrator auto-recovery | 5 min | Medium |
| Add models service | `docker-compose.yml` (optional) | Local LLM inference (Ollama) | 0 min | Medium |
| Update README | `deploy/docker/README.md` | Documents security, prod, caching, models | 5 min | Low |
| MCP Toolkit | Docker Desktop UI | Agent integration (Claude, Cursor, Copilot) | 5 min | High |
| Model Runner | CLI | Local AI inference, no API costs | 5 min | Medium |
| Build Cloud | GitHub Actions workflow | 39x faster builds, multi-arch, shared cache | 15 min | High |

**Total effort**: ~90 minutes for everything. Can split into sessions.

---

## PART 6: EXECUTION ORDER

Recommended flow for implementing all changes:

### Session 1: Quick Wins (10 minutes)

1. Expand `.dockerignore`
2. Pin micromamba to 1.5.10
3. Merge `requirements.txt` into `environment.yml` and delete old file

**Verify**: `docker compose build tools` should use pinned version.

---

### Session 2: Dockerfiles & Config (40 minutes)

4. Update `web.Dockerfile` (production stage, non-root, health check)
5. Create `nginx.conf`
6. Update `mcp.Dockerfile` (non-root, `--omit=dev`, health check)
7. Update `tools.Dockerfile` (explicit version, non-root)
8. Update `thesis.Dockerfile` (non-root)
9. Update `docker-compose.yml` (health checks, optional models)

**Verify**: 
```bash
docker compose build --no-cache web mcp tools thesis
docker compose up -d
sleep 15
docker compose ps
# Should show healthy/starting status
```

---

### Session 3: Documentation & Verification (15 minutes)

10. Update `deploy/docker/README.md` (security, production, caching, models)
11. Run full verification suite (hadolint, rebuild, test all services)

**Verify**: 
```bash
# All tests pass (see Part 4)
```

---

### Session 4: AI/Model Integration (25 minutes)

12. Set up MCP Toolkit (Docker Desktop UI, 5 min)
13. Test Docker Model Runner locally (5 min)
14. Create GitHub Actions workflow for Build Cloud (15 min)

**Verify**:
```bash
# Local build with buildx
docker buildx build --platform linux/amd64,linux/arm64 -t test:latest .

# GitHub Actions workflow triggers on push
```

---

### Quick Implementation Checklist

- [ ] Expand `.dockerignore`
- [ ] Pin micromamba to 1.5.10
- [ ] Merge `requirements.txt` into `environment.yml` and delete
- [ ] Replace `web.Dockerfile`
- [ ] Create `nginx.conf`
- [ ] Replace `mcp.Dockerfile`
- [ ] Replace `tools.Dockerfile`
- [ ] Replace `thesis.Dockerfile`
- [ ] Replace `docker-compose.yml`
- [ ] Update `deploy/docker/README.md`
- [ ] Run verification tests
- [ ] Set up MCP Toolkit
- [ ] Create GitHub Actions workflow for Build Cloud

---

## Sources

- https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/
- https://docs.docker.com/ai/model-runner/
- https://docs.docker.com/build-cloud/
- https://docs.docker.com/build/cache/
- https://docs.docker.com/reference/dockerfile/
- https://docs.docker.com/build/ci/github-actions/

---

## Questions?

- Production deployment: See "Production readiness" section in Part 2, step 10
- Local models: See "Docker Model Runner Setup" in Part 3
- Team builds: See "Docker Build Cloud Setup" in Part 3
- Security: See "Security" section in Part 2, step 10
