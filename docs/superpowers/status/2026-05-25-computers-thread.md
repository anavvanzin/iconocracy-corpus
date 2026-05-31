# Status — "Computers" Thread (Mac ↔ Linux reconcile)

**Date:** 2026-05-25
**Author:** Claude Code (resume of 2026-05-24/25 sessions)
**Purpose:** Durable state-of-play so this work stops being re-diagnosed from scratch every session. Read this first on resume.

---

## TL;DR

There is no single "the computers" task — there are **four parallel threads**. Most prior work already persisted on GitHub (PR #60 = reconcile plan, PR #59 = research ingest, Issues #57/#61). The two real-world blockers are physical: the `origin` mirror drive is unmounted, and the Linux↔Linux reconcile can only run on the Linux box.

---

## Machine / copy topology

| Copy | Path | Notes |
|------|------|-------|
| **Mac (here)** | `~/Research/hub/iconocracy-corpus` | Active working copy. Dirty: ~8 modified + ~15 untracked. Mostly DIR410346 coursework + a `.pages` file + `metodologia/`. |
| Linux "Documents" | `~/Documents/projetos/research/hub/iconocracy-corpus` | Highest-risk: uncommitted corpus/code edits. (per PR #60) |
| Linux "data" | `/data/projetos/research/hub/iconocracy-corpus` | Pull-only backup mirror on the Debian box. (per PR #60) |
| `github` remote | `github.com/anavvanzin/iconocracy-corpus` | Canonical source of truth. |
| `origin` remote | `/Volumes/ICONOCRACIA/git-mirrors/...` | **DRIVE NOT MOUNTED → remote dead until plugged in.** |

> Note: PR #60's plan is written for the **Linux box's two clones** (`/data` + `~/Documents`). It **cannot be executed from this Mac** — paths don't exist here.

---

## Thread 1 — Mac dirty working copy  *(actionable from this Mac)*

- **State:** ~8 modified (AGENTS.md, CLAUDE.md, DASHBOARD_CORPUS.html, 4 DIR410346 notes), 1 deleted (`Capitulo2_metodologia.md`), ~15 untracked (9 DIR410346 leituras/memoriais, a `.pages` file under `vault/projeto/`, `tese/council/`, `vault/tese/metodologia/`, `.worktrees/`).
- **Risk:** The `.pages` file and `metodologia/` may be qualifying-thesis material — **do not delete/discard without explicit say-so.**
- **Blocker:** none technical. Just needs triage decisions (commit / ignore / stash per path).
- **Next action:** classify the 15 untracked paths into commit vs gitignore, then a clean commit of the coursework set.

## Thread 2 — Linux ↔ Linux reconcile  *(NOT actionable from this Mac)*

- **State:** Plan written and archived → **PR #60** (`docs/archive-reconcile-plan-2026-05-24`, file `docs/superpowers/plans/2026-05-24-reconcile-data-documents.md`). 11-phase git-rescue plan; `/data` ahead 29 / behind 4, `~/Documents` ahead 15 / behind 4 vs cached `origin/main`. No destructive op before Phase 10.
- **Blocker:** must run **on the Debian box**; also `rsync` missing on Debian; also must pull `origin/main` incl. PR #59's 7 records before finalizing.
- **Next action (on Linux):** `sudo apt install rsync`, then execute PR #60 Phase 0 (read-only inventory).

## Thread 3 — GitHub PRs / Issues  *(actionable from anywhere)*

- **PR #60** — archive reconcile plan (doc-only). Safe to merge.
- **PR #59** — ingest 2026-05-19 research run, +7 KEEP records (→ records.jsonl 281). Needs review.
- **PR #23 / Issue #21** — migrate companion Worker to Hono. **Note: webiconocracy retired** — confirm this PR isn't reviving dead app before any action.
- **PR #13** — 43 gallery items, corpus-data.json conflict (was 116→165).
- **PR #52 (draft)**, **PR #30** — editorial/topology docs.
- **Issue #61** — weekly Health Check (auto, 2026-05-25). Was RED: 99 null rows in `data/processed/purification.jsonl` rows 166–264.
- **Issue #57** — tracks the 100 uncoded canonical records (= the purification nulls). **This is where the null-coding backlog belongs.**
- **Issue #56** — export contract regression in `records_to_corpus.py`.

## Thread 4 — Local housekeeping  *(done / minor leftover)*

- Docker: 6 dangling CLI symlinks relinked (`/Volumes/Ana` → `/Applications/Docker.app`); daemon + mcp-gateway verified. ✅
- Stale plugins `sagemaker-ai`, `goodmem` in `settings.json` — **manual removal still pending** (automode blocked it).
- n8n-mcp added to `~/.claude.json` (user scope) — **JWT leak flagged, rotate before use.**

---

## The recurring failure (fix this)

Sessions 2026-05-24 and 2026-05-25 both re-diagnosed the same divergence because state lived only in chat + ephemeral `.remember/` buffers. **This doc is the durable handoff.** Update it at session end instead of re-discovering. Commit it so every machine's `git pull` carries it.
