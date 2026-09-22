# Wave 1.2 — Symlink Integrity Audit

**Date:** 2026-06-26  
**Scope:** `.hermes/skills/` and `.claude/skills/`  
**Repo:** `/Users/ana/Research/hub/iconocracy-corpus`

---

## Summary

| Metric | Count |
|--------|-------|
| **Total symlinks** (both dirs) | **63** |
| **Healthy** (target exists) | **6 + 6 = 12** (but 6 are duplicates) |
| **Broken** (target missing) | **51** |
| **Duplicates** (same target in both dirs) | **6** |
| **Fixable** (target exists elsewhere) | **1** |

---

## 1. `.hermes/skills/` — Full Listing (57 symlinks)

All symlinks point to `../../.agents/skills/<name>`. Target base resolves to `.agents/skills/` in repo root (10 dirs present).

### ✅ Healthy (6 of 57)

| # | Symlink | Target | Action |
|---|---------|--------|--------|
| 1 | `data-visualization` | `../../.agents/skills/data-visualization` | ⚠️ **keep** (duplicate; see §3) |
| 2 | `json-canvas` | `../../.agents/skills/json-canvas` | ⚠️ **keep** (duplicate; see §3) |
| 3 | `obsidian-markdown` | `../../.agents/skills/obsidian-markdown` | ⚠️ **keep** (duplicate; see §3) |
| 4 | `pandoc-docx` | `../../.agents/skills/pandoc-docx` | ⚠️ **keep** (duplicate; see §3) |
| 5 | `pandoc-pdf-generation` | `../../.agents/skills/pandoc-pdf-generation` | ⚠️ **keep** (duplicate; see §3) |
| 6 | `sqlite-database-expert` | `../../.agents/skills/sqlite-database-expert` | ⚠️ **keep** (duplicate; see §3) |

### ❌ Broken (51 of 57)

All point to `../../.agents/skills/<name>` — targets DO NOT exist in `.agents/skills/`.

#### 🗑️ Delete — no alternative exists anywhere (50)

| # | Symlink | Target |
|---|---------|--------|
| 1 | `api-expert` | `../../.agents/skills/api-expert` |
| 2 | `applescript` | `../../.agents/skills/applescript` |
| 3 | `appsec-expert` | `../../.agents/skills/appsec-expert` |
| 4 | `async-expert` | `../../.agents/skills/async-expert` |
| 5 | `async-programming` | `../../.agents/skills/async-programming` |
| 6 | `auto-update-systems-expert` | `../../.agents/skills/auto-update-systems-expert` |
| 7 | `celery-expert` | `../../.agents/skills/celery-expert` |
| 8 | `ci-cd-pipeline-security-expert` | `../../.agents/skills/ci-cd-pipeline-security-expert` |
| 9 | `cicd-expert` | `../../.agents/skills/cicd-expert` |
| 10 | `cilium-expert` | `../../.agents/skills/cilium-expert` |
| 11 | `cloud-api-integration` | `../../.agents/skills/cloud-api-integration` |
| 12 | `cross-platform-build-expert` | `../../.agents/skills/cross-platform-build-expert` |
| 13 | `database-design-expert` | `../../.agents/skills/database-design-expert` |
| 14 | `dbus` | `../../.agents/skills/dbus` |
| 15 | `devsecops-expert` | `../../.agents/skills/devsecops-expert` |
| 16 | `fastapi` | `../../.agents/skills/fastapi` |
| 17 | `fastapi-expert` | `../../.agents/skills/fastapi-expert` |
| 18 | `glsl` | `../../.agents/skills/glsl` |
| 19 | `graph-database-expert` | `../../.agents/skills/graph-database-expert` |
| 20 | `graphql-expert` | `../../.agents/skills/graphql-expert` |
| 21 | `gsap` | `../../.agents/skills/gsap` |
| 22 | `harbor-expert` | `../../.agents/skills/harbor-expert` |
| 23 | `javascript-expert` | `../../.agents/skills/javascript-expert` |
| 24 | `kanidm-expert` | `../../.agents/skills/kanidm-expert` |
| 25 | `linux-at-spi2` | `../../.agents/skills/linux-at-spi2` |
| 26 | `llm-integration` | `../../.agents/skills/llm-integration` |
| 27 | `macos-accessibility` | `../../.agents/skills/macos-accessibility` |
| 28 | `model-quantization` | `../../.agents/skills/model-quantization` |
| 29 | `pinia` | `../../.agents/skills/pinia` |
| 30 | `prompt-engineering` | `../../.agents/skills/prompt-engineering` |
| 31 | `python` | `../../.agents/skills/python` |
| 32 | `rabbitmq-expert` | `../../.agents/skills/rabbitmq-expert` |
| 33 | `rust` | `../../.agents/skills/rust` |
| 34 | `speech-to-text` | `../../.agents/skills/speech-to-text` |
| 35 | `sqlcipher-encrypted-database-expert` | `../../.agents/skills/sqlcipher-encrypted-database-expert` |
| 36 | `surrealdb-expert` | `../../.agents/skills/surrealdb-expert` |
| 37 | `tailwindcss` | `../../.agents/skills/tailwindcss` |
| 38 | `talos-os-expert` | `../../.agents/skills/talos-os-expert` |
| 39 | `tauri` | `../../.agents/skills/tauri` |
| 40 | `text-to-speech` | `../../.agents/skills/text-to-speech` |
| 41 | `threejs-tresjs` | `../../.agents/skills/threejs-tresjs` |
| 42 | `typescript` | `../../.agents/skills/typescript` |
| 43 | `typescript-expert` | `../../.agents/skills/typescript-expert` |
| 44 | `ui-ux-expert` | `../../.agents/skills/ui-ux-expert` |
| 45 | `vue-nuxt` | `../../.agents/skills/vue-nuxt` |
| 46 | `wake-word-detection` | `../../.agents/skills/wake-word-detection` |
| 47 | `web-audio-api` | `../../.agents/skills/web-audio-api` |
| 48 | `webgl` | `../../.agents/skills/webgl` |
| 49 | `websocket` | `../../.agents/skills/websocket` |
| 50 | `windows-ui-automation` | `../../.agents/skills/windows-ui-automation` |

#### 🔗 Fixable — target exists elsewhere (1)

| # | Symlink | Target | Alternative Source |
|---|---------|--------|-------------------|
| 1 | `browser-automation` | `../../.agents/skills/browser-automation` | `~/.agents/skills/browser-automation` |

> **Recommendation:** Can be relinked or copied from `~/.agents/skills/browser-automation` if the skill is needed.

---

## 2. `.claude/skills/` — Symlinks Only (6 of 28 entries)

`.claude/skills/` has 28 total entries: 6 symlinks + 22 real directories.  
**All 6 symlinks are healthy** and point to the same targets as the healthy `.hermes/skills/` ones.

| # | Symlink | Target | Status | Action |
|---|---------|--------|--------|--------|
| 1 | `data-visualization` | `../../.agents/skills/data-visualization` | EXISTS | ⚠️ **keep** (duplicate; see §3) |
| 2 | `json-canvas` | `../../.agents/skills/json-canvas` | EXISTS | ⚠️ **keep** (duplicate; see §3) |
| 3 | `obsidian-markdown` | `../../.agents/skills/obsidian-markdown` | EXISTS | ⚠️ **keep** (duplicate; see §3) |
| 4 | `pandoc-docx` | `../../.agents/skills/pandoc-docx` | EXISTS | ⚠️ **keep** (duplicate; see §3) |
| 5 | `pandoc-pdf-generation` | `../../.agents/skills/pandoc-pdf-generation` | EXISTS | ⚠️ **keep** (duplicate; see §3) |
| 6 | `sqlite-database-expert` | `../../.agents/skills/sqlite-database-expert` | EXISTS | ⚠️ **keep** (duplicate; see §3) |

---

## 3. Duplicate Analysis

6 symlinks exist identically in **both** `.hermes/skills/` and `.claude/skills/`:

| Skill | Target |
|-------|--------|
| `data-visualization` | `../../.agents/skills/data-visualization` |
| `json-canvas` | `../../.agents/skills/json-canvas` |
| `obsidian-markdown` | `../../.agents/skills/obsidian-markdown` |
| `pandoc-docx` | `../../.agents/skills/pandoc-docx` |
| `pandoc-pdf-generation` | `../../.agents/skills/pandoc-pdf-generation` |
| `sqlite-database-expert` | `../../.agents/skills/sqlite-database-expert` |

**Recommendation:** ⚠️ **Keep all 12** (6 in each dir). These are intentional duplicates — Claude Code and Hermes Agent each need their own skill resolution path. Both point to the same canonical source in `.agents/skills/`, so they remain in sync automatically. No action needed.

---

## 4. `.agents/skills/` — Target Base (ground truth)

Only **10 directories** exist in `.agents/skills/`:

| Directory | Referenced by |
|-----------|--------------|
| `compilar-tese` | (real dir in `.claude/skills/`) |
| `data-visualization` | .hermes + .claude symlinks |
| `dir410346` | (unreferenced) |
| `json-canvas` | .hermes + .claude symlinks |
| `obsidian-markdown` | .hermes + .claude symlinks |
| `pandoc-docx` | .hermes + .claude symlinks |
| `pandoc-pdf-generation` | .hermes + .claude symlinks |
| `sqlite-database-expert` | .hermes + .claude symlinks |
| `sync-corpus` | (real dir in `.claude/skills/`) |
| `validate-corpus` | (unreferenced) |

> Note: `compilar-tese` and `sync-corpus` exist as real directories in `.claude/skills/`, not symlinks. `dir410346` and `validate-corpus` are unreferenced.

---

## 5. Recommended Actions

### Batch 1: Delete 50 broken symlinks (no alternative)

```bash
cd /Users/ana/Research/hub/iconocracy-corpus

rm .hermes/skills/api-expert
rm .hermes/skills/applescript
rm .hermes/skills/appsec-expert
rm .hermes/skills/async-expert
rm .hermes/skills/async-programming
rm .hermes/skills/auto-update-systems-expert
rm .hermes/skills/celery-expert
rm .hermes/skills/ci-cd-pipeline-security-expert
rm .hermes/skills/cicd-expert
rm .hermes/skills/cilium-expert
rm .hermes/skills/cloud-api-integration
rm .hermes/skills/cross-platform-build-expert
rm .hermes/skills/database-design-expert
rm .hermes/skills/dbus
rm .hermes/skills/devsecops-expert
rm .hermes/skills/fastapi
rm .hermes/skills/fastapi-expert
rm .hermes/skills/glsl
rm .hermes/skills/graph-database-expert
rm .hermes/skills/graphql-expert
rm .hermes/skills/gsap
rm .hermes/skills/harbor-expert
rm .hermes/skills/javascript-expert
rm .hermes/skills/kanidm-expert
rm .hermes/skills/linux-at-spi2
rm .hermes/skills/llm-integration
rm .hermes/skills/macos-accessibility
rm .hermes/skills/model-quantization
rm .hermes/skills/pinia
rm .hermes/skills/prompt-engineering
rm .hermes/skills/python
rm .hermes/skills/rabbitmq-expert
rm .hermes/skills/rust
rm .hermes/skills/speech-to-text
rm .hermes/skills/sqlcipher-encrypted-database-expert
rm .hermes/skills/surrealdb-expert
rm .hermes/skills/tailwindcss
rm .hermes/skills/talos-os-expert
rm .hermes/skills/tauri
rm .hermes/skills/text-to-speech
rm .hermes/skills/threejs-tresjs
rm .hermes/skills/typescript
rm .hermes/skills/typescript-expert
rm .hermes/skills/ui-ux-expert
rm .hermes/skills/vue-nuxt
rm .hermes/skills/wake-word-detection
rm .hermes/skills/web-audio-api
rm .hermes/skills/webgl
rm .hermes/skills/websocket
rm .hermes/skills/windows-ui-automation
```

### Batch 2: Fix 1 broken symlink (target exists elsewhere)

```bash
# Option A: Repoint symlink to ~/.agents/skills/browser-automation
rm .hermes/skills/browser-automation
ln -s ~/.agents/skills/browser-automation .hermes/skills/browser-automation

# Option B: Copy the skill content into .agents/skills/ and keep symlink as-is
cp -r ~/.agents/skills/browser-automation .agents/skills/browser-automation
# (symlink already points to correct relative path)
```

### Batch 3: No action needed (12 symlinks — 6 in each dir)

Keep all 6 healthy symlinks in both `.hermes/skills/` and `.claude/skills/`. They are intentional cross-agent duplicates pointing to a single canonical source.

---

## 6. Post-Audit State (after recommended deletions)

| Directory | Before | After | Healthy | Broken |
|-----------|--------|-------|---------|--------|
| `.hermes/skills/` | 57 symlinks | 7 symlinks | 6 (kept) + 1 (fixed) | 0 |
| `.claude/skills/` | 6 symlinks | 6 symlinks | 6 | 0 |
| **Total** | **63** | **13** | **13** | **0** |

---

## Legend

| Icon | Meaning |
|------|---------|
| 🗑️ | Delete — broken, no alternative found |
| 🔗 | Fix — broken but target exists elsewhere |
| ⚠️ | Keep — duplicate but intentional (dual-agent) |
| ✅ | Keep — healthy, unique |

---

*Generated by Hermes Agent during ICONOCRACY 360° Audit — Wave 1.2*
