# Session: 2026-05-25

**Started:** ~afternoon (Ana "just got my computer back")
**Last Updated:** 14:39
**Project:** iconocracy-corpus (ICONOCRACIA thesis monorepo) + home/dotfiles setup
**Topic:** Reconciling two coexisting computers (MacBook ↔ Linux VAIO) + memory corrections + Dependabot triage

---

## What We Are Building

Ana's MacBook (macOS, her original machine with all pre-repair data) came back from the repair shop. While it was gone she bought a Linux VAIO (Debian 13) and has been working on it since — it's now the active driver and `origin/main` reflects its work. The goal: set up an **ongoing workflow so both machines coexist and stay reconciled** without repeating the 2026-05-24 divergence (disjoint local histories).

Scope settled to two tracks:
1. **`iconocracy-corpus` repo** — sync cross-OS via GitHub `origin` (the only sane path). Mac needs a one-time safe reconciliation.
2. **dotfiles/shell config** — kept consistent macOS↔Linux via **GNU stow** (apt-official, fits Ana's no-third-party-repo policy). Mac is the rich source, Linux is fresh.

A design+runbook was written and committed to the repo so it travels to the Mac on pull. Separately, two stale memory facts were corrected, and the repo's 7 Dependabot alerts were triaged (fix proposed, not yet applied).

---

## What WORKED (with evidence)

- **Repo state diagnosis** — confirmed by: `git rev-list --left-right --count` and `git fetch`. `~/Documents` copy in sync at `a5526d4` (now `64867f8`); `/data` backup frozen at `9be98bb`, 5 behind, with 5 staged files; GitHub SSH auth works (`ssh -T git@github.com` → "Hi anavvanzin").
- **Runbook written + committed + pushed** — confirmed by: `git push origin main` succeeded (`a5526d4..64867f8`), `git rev-list` shows `0 0` (in sync). File: `docs/superpowers/specs/2026-05-25-two-machine-reconciliation-design.md`.
- **Memory corrections written** — confirmed by: Edit tool success on `reference_ssd_data.md`, `project_iconocracia.md`, and `MEMORY.md` index lines.
- **Dependabot triage** — confirmed by: `gh api .../dependabot/alerts` returned 7 open alerts, all `protobufjs`/`@protobufjs/utf8` in `shared/package-lock.json`, all patched by 7.5.6 / 1.1.1. Root cause = `overrides.protobufjs: "^7.5.5"` in `shared/package.json` (verified still unchanged).

---

## What Did NOT Work (and why)

- **Combined commit+push in one Bash call** — failed because: the auto-mode classifier denied it ("pushing to main bypasses PR review; user authorized writing the runbook, not pushing"). Resolved by splitting: commit locally first, then ask Ana → she approved "push to main" → push succeeded. **Lesson for next session: don't chain a `main` push with other git ops; pushing to `main` is gated and needs explicit per-action OK.**
- **chezmoi for dotfiles** — rejected because: NOT in Debian apt (`apt-cache policy chezmoi` empty), would need official install script or third-party repo — off Ana's install-source policy. Chose GNU stow instead (`stow` is in apt, `2.4.1-2`).

---

## What Has NOT Been Tried Yet

- **Mac-side repo reconciliation (Phase 1)** — Ana runs on the MacBook: `git fetch`, `git log --oneline origin/main..HEAD` to detect unpushed pre-repair commits, then safety-branch (`mac-prerepair-2026-05-25`) + push + `git pull --ff-only` (or `reset --hard origin/main` if ff rejected). She'll paste the `git log origin/main..HEAD` output for the exact next command.
- **Phase 0 / 2.1 (Linux side, mine)** — `sudo apt install stow`; scaffold `~/dotfiles` (`common/ linux/ macos/`); seed `linux/` from current VAIO config; create private GitHub `dotfiles` repo + push. NOT started — waiting on Ana's go.
- **protobufjs fix** — bump `overrides` to `protobufjs: "^7.5.6"` + add `@protobufjs/utf8: "^1.1.1"` in `shared/package.json`, then `cd shared && npm install` to refresh lockfile. Proposed, awaiting Ana's go + push method.
- **Dangling submodule edit** — `vault/2026-Q2-Seminario-AD/algoritmo-em-disputa` is modified/uncommitted on Linux. Not yet inspected or resolved (Phase 1b).
- **7 Dependabot alerts triage→fix** — fix identified but not applied.

---

## Current State of Files

| File | Status | Notes |
| ---- | ------ | ----- |
| `docs/superpowers/specs/2026-05-25-two-machine-reconciliation-design.md` | Complete + pushed | Design + cross-machine runbook; commit `64867f8` on origin/main |
| `~/.claude/projects/-home-ana/memory/reference_ssd_data.md` | Complete | Corrected: device node `/dev/sda1`→`/dev/sdb1`, rely on `/data` mountpoint |
| `~/.claude/projects/-home-ana/memory/project_iconocracia.md` | Complete | Added verified-2026-05-25 working-copy state; old reconcile narrative marked `[historical]` |
| `~/.claude/projects/-home-ana/memory/MEMORY.md` | Complete | Index lines updated for both above |
| `shared/package.json` | Not changed yet | protobufjs override still `^7.5.5` (vulnerable); fix proposed |
| `shared/package-lock.json` | Not changed yet | Needs `npm install` after override bump |
| `vault/2026-Q2-Seminario-AD/algoritmo-em-disputa` (submodule) | Modified, uncommitted | Pending decision (commit or discard) |

---

## Decisions Made

- **Git-through-origin as the only cross-OS sync path** — reason: two physical clones editing independently caused the 2026-05-24 divergence; machines must never sync directly, only through `origin/main`. Invariant: pull `--ff-only` at start, push at end; safety-branch any local work before pulling.
- **GNU stow over chezmoi/bare-repo for dotfiles** — reason: apt-official (fits no-third-party-repo policy), git-backed, `common/ + per-OS` layout handles macOS/Linux split for Ana's scope (zsh, git, Claude settings.json/keybindings).
- **Leave `/data` mirror frozen** — Ana's explicit choice 2026-05-25; do not fast-forward/discard its staged drift without asking again.
- **Runbook lives in the repo** (`docs/superpowers/specs/`) — reason: follows existing convention AND rides along to the Mac on pull.
- **Exclude from any sync:** conda envs (recreate per-OS from `environment.yml`), `~/.claude/projects/` history, SSH keys/tokens, the macOS `/Users/ana/Research/…` symlinks.

---

## Blockers & Open Questions

- **Mac's repo state unknown** — does the MacBook hold un-pushed pre-repair commits or uncommitted edits? Must be checked on the Mac before it pulls (the safety-branch step protects against loss either way).
- **Push-to-main is gated** — each direct push to `main` needs Ana's explicit OK (or a Bash permission rule in settings).
- **Pending go-aheads from Ana:** (a) start Linux-side stow/dotfiles work? (b) apply the protobufjs fix? (c) resolve the submodule edit?

---

## Exact Next Step

Ana was asked whether to apply the protobufjs fix (last open question). When resuming: confirm which of the three pending go-aheads she wants — most likely **apply the protobufjs fix** (edit `shared/package.json` overrides → `protobufjs: "^7.5.6"` + `@protobufjs/utf8: "^1.1.1"`, run `cd shared && npm install`, show diff, then commit + ask push method). In parallel, she may run the **Mac Phase-1 reconciliation** and paste `git log --oneline origin/main..HEAD` for the exact safe command.

---

## Environment & Setup Notes

- Repo: `~/Documents/projetos/research/hub/iconocracy-corpus` (origin `git@github.com:anavvanzin/iconocracy-corpus.git`). conda env `iconocracy`.
- `/data` SSD now enumerates as `/dev/sdb1` (was `/dev/sda1`); mounts via automount at `/data`.
- `shared/` is a private npm package (`@iconocracy/shared`), devDeps firebase + @google/genai; needs `npm` for the protobufjs lockfile refresh.
- stow available via `apt install stow` (Linux) / `brew install stow` (Mac).
