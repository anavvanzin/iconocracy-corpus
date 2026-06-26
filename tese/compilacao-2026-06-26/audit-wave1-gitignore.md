# Wave 1.3 — `.gitignore` Audit Report

**Project:** ICONOCRACY Corpus  
**Date:** 2026-06-26  
**Auditor:** Hermes Agent (nousresearch)  
**Scope:** `.gitignore` patterns, tracked large files, secrets scan, `.git/info/exclude`

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| `.gitignore` lines | 163 |
| Total tracked files | 3,909 |
| Total tracked size | ~351 MB |
| Secrets found | **0** (clean) |
| CRITICAL issues | 2 |
| HIGH issues | 2 |
| MEDIUM issues | 4 |
| LOW issues | 3 |
| Redundant patterns | 1 confirmed |

**Bottom line:** The `.gitignore` is well-structured for Python/Node/Obsidian but has **two critical gaps**: (1) `wiki/.obsidian/plugins/` is not ignored, causing 297 plugin files (~50+ MB of JS bundles) to be tracked, and (2) large PDFs/binaries (34 PDFs, 186 total binary files) are tracked in git, including 22 MB and 17 MB PDFs in `vault/`. Secrets scan is clean.

---

## 2. Large Directory Tracking Status

| Directory | Disk Size | Tracked? | Files Tracked | Status |
|-----------|-----------|----------|---------------|--------|
| `shared/` | 181 MB | Partially | 11 files (~70 KB) | ✅ OK — 181M is `node_modules/` (gitignored) |
| `vault/` | 158 MB | Yes | 845 files | ⚠️ REVIEW — contains large PDFs (see §3) |
| `wiki/` | 104 MB | **YES** | 1,048 files | 🔴 **CRITICAL** — Obsidian plugins + PDFs |
| `postman/` | 53 MB | No | 0 | ✅ OK — gitignored at line 104 |
| `archive/` | 7.7 MB | Partially | some | ✅ OK |
| `.claude/` | 396 MB | Partially | 52 files | ✅ OK — most blocked by lines 148–163 |
| `.uv-cache/` | 66 MB | No | 0 | ✅ OK — local `.gitignore` blocks it |
| `.venv-pdf/` | 58 MB | No | 0 | ✅ OK — local `.gitignore` blocks it |

### 2.1 `shared/` — NOT CRITICAL
The 181 MB is entirely `shared/node_modules/` which is correctly gitignored (line 61). Only 11 small TypeScript source files (~70 KB) are tracked: `corpus-parser.ts`, `index.ts`, `package.json`, `package-lock.json`, and service/type definitions. **No action needed.**

### 2.2 `wiki/` — CRITICAL
**1,048 tracked files totaling ~104 MB.** Breakdown:
- **723 content files** — Mostly `.md` Obsidian notes (legitimate to track, though worth reviewing if all belong in git)
- **325 `.obsidian/` files** — Includes 297 plugin files, ~146 of which are `.js` bundles (8.6 MB `excalidraw`, 5.7 MB `make-md`, 4.3 MB `quickadd`, 4.2 MB `remotely-save`, etc.)
- **6 PDFs tracked in wiki/** (duplicates of vault/ content)
- **`wiki/.obsidian/workspace.json`** — User-local workspace state, should NOT be tracked
- **`wiki/.obsidian/community-plugins.json`** — Plugin list (reasonable to track) but plugins themselves should not be

**Root cause:** The `.gitignore` has rules for `vault/.obsidian/plugins/` (line 31) and `vault/.obsidian/workspace.json` (line 29) but **no corresponding rules for `wiki/.obsidian/`**.

### 2.3 `vault/` — REVIEW NEEDED
845 files tracked including large PDFs (see §3). The `.obsidian/` rules (lines 29–33) correctly block plugins, workspace files, and hotkeys. However, large binaries in vault subdirectories are tracked.

### 2.4 `postman/` — CORRECTLY IGNORED
Gitignored at line 104 (`postman/`) and line 105 (`.postman/`). Zero tracked files. **No action needed.**

---

## 3. Large Tracked Binaries

### 3.1 Top 20 Largest Tracked Files

| Size | File |
|------|------|
| 22.3 MB | `vault/2026-Q2-Seminario-AD/01-Materials/.../Estado inteligente...Bethânia.pdf` |
| 17.1 MB | `vault/2026-Q2-Seminario-AD/01-Materials/.../Direito administrativo do medo..pdf` |
| 16.2 MB | `vault/2026-Q2-Seminario-AD/01-Materials/.../Administração Pública democrática...pdf` |
| 14.4 MB | `vault/obsidian-dir410346/materiais/...legislação penal brasileira.pd.pdf` |
| 10.0 MB | `vault/2026-Q2-Seminario-AD/01-Materials/.../princípios constitucionais estruturantes.pdf` |
| 8.6 MB | `wiki/.obsidian/plugins/obsidian-excalidraw-plugin/main.js` |
| 7.3 MB | `vault/projeto/...Report.pages` |
| 5.7 MB | `wiki/.obsidian/plugins/make-md/main.js` |
| 5.2 MB | `vault/obsidian-dir410346/.../Malleus Maleficarum...Bruxaria.pptx` |
| 4.3 MB | `wiki/.obsidian/plugins/quickadd/main.js` |
| 4.3 MB | `wiki/.obsidian/plugins/remotely-save/main.js` |
| 4.2 MB | `wiki/.obsidian/plugins/notebook-navigator/main.js` |
| 4.0 MB | `wiki/.obsidian/plugins/obsidian-markmind/main.js` |
| 4.0 MB | `wiki/.obsidian/plugins/obsidian-local-rest-api/main.js` |
| 3.8 MB | `tese/Entrega_Orientador_Mar2026_FINAL/sumario/sumario.pdf` |
| 3.8 MB | `tese/manuscrito/sumario.pdf` |
| 2.9 MB | `wiki/.obsidian/plugins/media-extended/main.js` |
| 2.6 MB | `wiki/.obsidian/plugins/obsidian-citation-plugin/main.js` |
| 2.4 MB | `wiki/.obsidian/plugins/terminal/main.js` |
| 1.8 MB | `wiki/.obsidian/plugins/obsidian-advanced-slides/.../tex-svg-full.js` |

### 3.2 Binary File Summary

| Type | Count | Risk |
|------|-------|------|
| `.pdf` | 34 | 🔴 Bloats repo; most belong on Google Drive per ADR-001 |
| `.js` (plugin bundles) | 146 | 🔴 Obsidian plugins should be installed locally, not committed |
| `.pptx` | 3 | 🟡 Presentation files; small enough but non-diffable |
| `.pages` | 1 | 🟡 Apple Pages format (7.3 MB); non-diffable |
| Other binaries | 2 | 🟡 `.dylib`/`.so` covered by lines 136–137 |

**Note:** `tese/Entrega_Orientador_Mar2026_FINAL/` contains thesis delivery artifacts (PDFs of articles, atlas, manuscript chapters) that are arguably version-worthy but consume significant space (~20+ MB).

---

## 4. Missing `.gitignore` Patterns

| Pattern | Severity | Rationale |
|---------|----------|-----------|
| `wiki/.obsidian/plugins/` | 🔴 CRITICAL | 297 plugin files tracked; mirrors existing `vault/.obsidian/plugins/` rule |
| `wiki/.obsidian/workspace.json` | 🔴 CRITICAL | User-local workspace state tracked; mirrors vault rule |
| `wiki/.obsidian/workspace-mobile.json` | 🟡 MEDIUM | Same as above for mobile |
| `wiki/.obsidian/hotkeys.json` | 🟡 MEDIUM | Per-user hotkeys; mirrors vault rule |
| `*.log` | 🔴 HIGH | 11 `.log` files tracked (`Text/*.log`, `logs/autopilot/*.log`, `vault/vault_operations.log`). Only `firebase-debug.log` is explicitly ignored; `logs/` (dir) is ignored but files already committed are not retroactively blocked |
| `.env.*` | 🟡 MEDIUM | Only `.env` is ignored (line 12), not `.env.local`, `.env.production`, `.env.staging`, etc. |
| `*.pptx` | 🟡 MEDIUM | PowerPoint files tracked (e.g., 5.2 MB `Bruxaria.pptx` in vault) |
| `*.pages` | 🟡 MEDIUM | Apple Pages format tracked (7.3 MB `Report.pages`) |
| `data/raw/*.pdf` | 🟡 LOW | 34 PDFs tracked; ADR-001 says `data/raw/` is metadata-only |
| `.python-version` | 🟢 LOW | Not currently tracked; minor hygiene |

### 4.1 Common Python Patterns — Already Present ✅

The `.gitignore` already covers the standard Python patterns well:
- `__pycache__/` ✅ (line 2)
- `*.py[cod]` ✅ (line 3) — covers `.pyc`, `.pyo`, `.pyd`
- `*$py.class` ✅ (line 4)
- `*.egg-info/` ✅ (line 5)
- `dist/`, `build/`, `.eggs/`, `*.egg` ✅ (lines 6–9)
- `.venv`, `env/`, `venv/`, `ENV/` ✅ (lines 13–16)
- `.DS_Store`, `Thumbs.db` ✅ (lines 25–26)
- `.vscode/`, `.idea/` ✅ (lines 19–20)
- `node_modules/` ✅ (line 61)

**Missing niche patterns (low priority):**
- `.venv*` — `.venv` is at line 13 but `.venv312`, `.venv-old`, etc. would not match. (`.venv-pdf` is handled by its own local `.gitignore`.)
- `pip-wheel-metadata/` — Not relevant; the project uses `uv` or `conda`.

---

## 5. Overbroad / Problematic Patterns

### 5.1 `tese/compilacao-*/` (line 95) — CORRECT, with caveat

**Rule:** `tese/compilacao-*/`

**Verification:**
- Oldest tracked compilation: `tese/compilacao-2026-04-19/` (5 files) — committed before rule existed
- Current working compilation: `tese/compilacao-2026-06-26/` (10 files) — files added via `git add -f`
- The rule correctly blocks `git add` for new compilations but does NOT retroactively untrack already-committed files

**Assessment:** The rule is functioning as designed. Files committed before the rule or force-added will remain tracked. This is standard git behavior, not a bug.

**Recommendation:** If the goal is to NEVER track compilations, use `git rm --cached` to un-track existing compilations, then the rule will prevent re-addition.

### 5.2 `review/` (line 58) — INTENTIONAL
Blocks the entire `review/` directory. Comment says "Review artifacts." This is deliberate — review artifacts are ephemeral. **No action needed.**

### 5.3 `output/`, `tmp/`, `logs/` (lines 77–79) — INTENTIONAL
These block local operational artifacts. However, `logs/autopilot/` has 1 tracked file (committed before the rule). See §4.

### 5.4 `Images/`, `PDFs/` (lines 133–134) — INTENTIONAL
Comment explains: "Binary assets (stored in /data/iconocracy-corpus/binaries/)." **No action needed.**

### 5.5 `.agents/` surgical rules (lines 107–116) — WELL-DESIGNED
The comment block (lines 107–111) explains this was deliberately changed from a blanket `.agents/` ignore to surgical paths. The `.agents/skills/` directory is intentionally tracked. **No action needed.**

---

## 6. Redundant Patterns

| Pattern | Location | Duplicate | Action |
|---------|----------|-----------|--------|
| `*.zip` | Line 52 | Line 135 | Remove one (keep line 52 with archives comment) |

**Line 120–121:** `*.bak*` (line 120) already covers `corpus/corpus-data.json.bak-dedupe` (line 121). Line 121 is redundant but harmless — it was likely added as an explicit reminder.

---

## 7. Secrets Scan

### 7.1 Methodology
Scanned all tracked text files (excluding binaries: `.pdf`, `.png`, `.jpg`, `.exe`, `.dll`, `.so`, `.dylib`, `.zip`, `.gz`, `.min.js`, Obsidian plugin JS, `node_modules/`) for patterns matching:
- `password`, `secret`, `token`, `api_key`, `credential` with assignment operators
- `-----BEGIN (RSA|EC|DSA)? PRIVATE KEY-----`
- `ghp_`, `gho_`, `github_pat_` (GitHub tokens)
- `sk-` (OpenAI/Anthropic API keys)
- `AIza` (Google API keys)
- `hf_` (HuggingFace tokens)

### 7.2 Results: CLEAN ✅

**Zero secrets found.** 

One false positive examined:
- `Other/iconocracy-local.environment.yaml` line 7: `key: diarySecret` — This is a **key name** in a YAML configuration schema, not a secret value. No actual secret is exposed.
- `docs/superpowers/sessions/2026-05-25-hermes-mac-config-review.md` — Contains diagnostic notes about an **expired** OAuth token for scite (HTTP 401). The token value is not present; only the error description is documented.

### 7.3 Recommendation
Continue good practices. Consider adding a `.gitignore` pattern for `.env.*` (currently only `.env` is blocked) and using a pre-commit hook like `detect-secrets` or `gitleaks` for automated scanning.

---

## 8. `.git/info/exclude` Review

**File:** `/Users/ana/Research/hub/iconocracy-corpus/.git/info/exclude`

Content (3 active rules):
```
vault/.obsidian/plugins/obsidian-git/obsidian_askpass.sh
wiki/.obsidian/plugins/obsidian-git/obsidian_askpass.sh
.playwright-mcp/
```

**Assessment:** No issues. These are local-only excludes for:
- `obsidian_askpass.sh` — Obsidian Git plugin's credential helper script (sensitive to local machine)
- `.playwright-mcp/` — Playwright test artifacts (local only)

**No action needed.**

---

## 9. Recommendations

### 9.1 CRITICAL — Address Immediately

| # | Action | Impact |
|---|--------|--------|
| R1 | Add `wiki/.obsidian/plugins/` to `.gitignore` (mirror line 31) | Blocks 297 plugin files (~50+ MB) |
| R2 | Add `wiki/.obsidian/workspace.json` and `wiki/.obsidian/workspace-mobile.json` to `.gitignore` (mirror lines 29–30) | Blocks user-local workspace state |
| R3 | Run `git rm --cached -r wiki/.obsidian/plugins/` to untrack existing plugin files | Repo size reduction |
| R4 | Add `*.log` catch-all to `.gitignore` | Blocks future log files |

### 9.2 HIGH — Address This Week

| # | Action | Impact |
|---|--------|--------|
| R5 | Add `*.pptx` and `*.pages` to `.gitignore` | Blocks non-diffable presentation files |
| R6 | Consider adding `vault/2026-Q2-Seminario-AD/01-Materials/*.pdf` to `.gitignore` — large seminar reading PDFs (22M + 17M + 16M + 14M + 10M) should live on Google Drive per ADR-001 | ~80 MB repo size reduction |
| R7 | Run `git rm --cached` on tracked `.log` files in `Text/` and `logs/` | Clean up 11 log files |

### 9.3 MEDIUM — Address This Sprint

| # | Action | Impact |
|---|--------|--------|
| R8 | Add `.env.*` pattern to `.gitignore` | Prevents accidental credential commits |
| R9 | Consider adding `wiki/.obsidian/hotkeys.json` (mirror line 32) | User-local hotkeys |
| R10 | Consider whether `tese/compilacao-*/` should also use `git rm --cached` for legacy tracked compilations | Consistency |

### 9.4 LOW — Housekeeping

| # | Action | Impact |
|---|--------|--------|
| R11 | Remove duplicate `*.zip` at line 135 (keep line 52) | Cleaner file |
| R12 | Consider adding `.python-version` to `.gitignore` | Minor hygiene |
| R13 | Consider adding `vault/obsidian-dir410346/materiais/*.pdf` to `.gitignore` | 14 MB reading PDF |

### 9.5 Suggested Additions to `.gitignore`

```gitignore
# Wiki Obsidian plugins (mirror vault rules at lines 29-33)
wiki/.obsidian/plugins/
wiki/.obsidian/workspace.json
wiki/.obsidian/workspace-mobile.json
wiki/.obsidian/hotkeys.json

# Log files (catch-all)
*.log

# Environment variants
.env.*

# Non-diffable binaries
*.pptx
*.pages

# Large seminar reading PDFs (per ADR-001: data/raw metadata-only)
vault/2026-Q2-Seminario-AD/01-Materials/*.pdf
vault/obsidian-dir410346/materiais/*.pdf
```

---

## 10. Appendix: Gitignore Pattern Coverage Matrix

| Category | Pattern | Present? | Line |
|----------|---------|----------|------|
| **Python cache** | `__pycache__/` | ✅ | 2 |
| **Python compiled** | `*.py[cod]` | ✅ | 3 |
| **Python class** | `*$py.class` | ✅ | 4 |
| **Python packages** | `*.egg-info/`, `dist/`, `build/` | ✅ | 5–9 |
| **Virtual envs** | `.venv`, `env/`, `venv/`, `ENV/` | ✅ | 13–16 |
| **IDE** | `.vscode/`, `.idea/` | ✅ | 19–20 |
| **Vim** | `*.swp`, `*.swo` | ✅ | 21–22 |
| **macOS** | `.DS_Store` | ✅ | 25 |
| **Windows** | `Thumbs.db` | ✅ | 26 |
| **Node** | `node_modules/` | ✅ | 61 |
| **Env files** | `.env` | ✅ | 12 |
| **Env variants** | `.env.*` | ❌ | — |
| **Log files** | `*.log` | ❌ | — |
| **Obsidian vault plugins** | `vault/.obsidian/plugins/` | ✅ | 31 |
| **Obsidian wiki plugins** | `wiki/.obsidian/plugins/` | ❌ | — |
| **Obsidian workspace** | `vault/.obsidian/workspace.json` | ✅ | 29 |
| **Obsidian wiki workspace** | `wiki/.obsidian/workspace.json` | ❌ | — |
| **PowerPoint** | `*.pptx` | ❌ | — |
| **Apple Pages** | `*.pages` | ❌ | — |
| **Databases** | `*.sqlite`, `*.db` | ✅ | 40–41 |
| **Archives** | `*.zip`, `*.gz` | ✅ | 39, 52 |
| **PDF (general)** | any pattern | ❌ | — |
| **Temp Word files** | `~$*` | ✅ | 55 |
| **Coverage** | `.coverage` | ✅ | 144 |
| **Cloudflare** | `.wrangler/` | ✅ | 98 |
| **Firebase** | `firebase-debug.log` | ✅ | 101 |
| **Postman** | `postman/`, `.postman/` | ✅ | 104–105 |
| **Claude Code** | `.claude/worktrees/`, `.claude/ecc/`, etc. | ✅ | 74, 148–163 |
| **Hermes** | `.hermes/` | ✅ | 117 |
| **Corpus data** | `data/raw/BR`, `data/raw/FR`, etc. | ✅ | 44–49 |

---

*End of Wave 1.3 audit. Next wave: Wave 1.4 (large file remediation) or Wave 2.1 (dependency audit).*
