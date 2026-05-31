# Session: 2026-05-25 (Hermes on Mac)

**Started:** Evening
**Machine:** MacBook (now — Hermes session)
**Topic:** Config review + two-machine reconciliation Linux-side prep

---

## What was done

### MCP Config Review & Fixes
- **MCP inventory** — 13 servers found via mcporter; 9 healthy, 2 auth-required, 2 broken
- **Proxyman duplicate** — removed from `~/.claude.json` project-level `mcpServers` (top-level entry was canonical)
- **VS Code `mcp.json`** — fixed trailing comma after perplexity entry + rebuilt object structure; now valid JSON with 7 servers + 4 inputs
- **scite** — diagnosed: HTTP 502 → direct curl confirmed OAuth token expired (`401 Invalid user token`). Needs `npx mcporter auth scite` from a browser-capable terminal.
- **n8n-mcp** — diagnosed: entire n8n cloud instance `anavvvvv.app.n8n.cloud` returns 404 on every path (root, health, MCP). Not just a broken MCP endpoint — the workspace appears gone/deleted. Configured in both `~/.claude.json` (empty stub) and `~/.hermes/config.yaml` (with Bearer token).

### Repo State (Mac)
- Mac `HEAD = origin/main = cc094f4` — zero divergence, fully in sync
- No unpushed commits or dirty tree (4 untracked dirs: `docs/superpowers/status/`, `tese/council/`, `.pages file`, `vault/tese/metodologia/`)
- Phase 1 (Mac reconciliation) is **already done** — no action needed

### protobufjs Fix (applied, not pushed)
- `shared/package.json` overrides: `protobufjs ^7.5.6`, `@protobufjs/utf8 ^1.1.1`
- `npm install` refreshed lockfile: protobufjs 7.5.5 → 7.6.1, 6 subdeps bumped
- 7 Dependabot alerts fixed (protobufjs family)
- Not committed/pushed yet — needs Ana's go-ahead on push method

---

## What's still pending

| Item | Machine | Action |
|------|---------|--------|
| **scite re-auth** | Mac | Run `npx mcporter auth scite` (needs browser) |
| **protobufjs commit+push** | Mac | Commit + push to main (gated — needs Ana OK) |
| **Submodule edit** | Linux | `vault/2026-Q2-Seminario-AD/algoritmo-em-disputa` — commit or discard? |
| **stow install** | Linux | `sudo apt install stow` |
| **Dotfiles scaffold** | Linux | Create `~/dotfiles`, seed `linux/`, create private GitHub repo |
| **Dotfiles Mac side** | Mac | After repo exists: clone, seed `common/` + `macos/`, push |
| **n8n** | n8n dashboard | Redeploy or check if workspace still exists |

---

## Environment notes
- This session used deepseek-v4-flash-free (via OpenCode Zen)
- Design doc at `docs/superpowers/specs/2026-05-25-two-machine-reconciliation-design.md`
- Session handoff from earlier Linux session: `docs/superpowers/sessions/2026-05-25-two-machine-sync-session.md`
