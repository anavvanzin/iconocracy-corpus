# Two-Machine Reconciliation & Ongoing Sync

**Date:** 2026-05-25
**Status:** Approved design + runbook
**Machines:** MacBook (macOS — rich pre-repair config, possibly un-pushed repo work) ↔ Linux VAIO (Debian 13 — fresh, currently the active driver)

---

## 1. Goal

The MacBook returned from repair; the Linux VAIO was bought while it was gone and has been the active machine since. Both will now coexist. Set up an ongoing workflow where the two machines stay reconciled **without** repeating the 2026-05-24 divergence (disjoint local histories across copies).

Scope: the `iconocracy-corpus` repo + dotfiles/shell config. Nothing else.

## 2. Invariants (the rules that prevent divergence)

1. **Machines never sync to each other directly.** Every sync goes through a git hub: GitHub `origin` for the repo, a new private `dotfiles` repo for shell config.
2. **Pull `--ff-only` at the start of work, push at the end.** No silent local-only history accumulation.
3. **Before any machine pulls onto a tree that might hold local work, that work is committed to a safety branch and pushed first.** Nothing irreversible until the work exists on `origin`.
4. **Cross-OS-incompatible state is never synced** (see §5).

## 3. Track 1 — `iconocracy-corpus` repo (hub = GitHub `origin`)

Current state (verified 2026-05-25):
- `origin/main` = `a5526d4` (source of truth).
- Linux VAIO = `a5526d4`, in sync. Only local change: one edited submodule `vault/2026-Q2-Seminario-AD/algoritmo-em-disputa` (handled separately — see §6 Phase 1b).
- MacBook = unknown; sitting on its pre-repair state.

### 3a. One-time Mac reconciliation — **RUN ON THE MAC**

```bash
cd <path-to>/iconocracy-corpus
git fetch origin
git status                              # note any dirty/uncommitted files
git log --oneline origin/main..HEAD     # any commits the Mac has that origin lacks?
```

**If the Mac has un-pushed commits OR a dirty tree**, preserve everything on a safety branch first:

```bash
git switch -c mac-prerepair-2026-05-25
git add -A && git commit -m "snapshot: Mac pre-repair working state 2026-05-25"   # only if dirty
git push -u origin mac-prerepair-2026-05-25     # everything is now safe on origin
git switch main
```

Then bring `main` up to origin:

```bash
git pull --ff-only origin main          # fast-forwards to a5526d4 if main had no local commits
```

If `--ff-only` is **rejected** (main had local commits), the work is already safe on `mac-prerepair-2026-05-25`, so realign main to origin:

```bash
git reset --hard origin/main            # safe: nothing lost — it lives on the branch + origin
```

Afterward, review `mac-prerepair-2026-05-25` and cherry-pick / merge anything still wanted, or delete it.

> macOS-era absolute symlinks (`/Users/ana/Research/…`) are broken on Linux — ignore them and use in-tree paths on both machines.

### 3b. Going forward (both machines)

- Start of a work session: `git pull --ff-only`
- End of a work session: `git add -A && git commit && git push`
- Never edit the same repo on both machines simultaneously without pushing/pulling between.

## 4. Track 2 — dotfiles via GNU stow (hub = new private `dotfiles` repo)

`stow` is apt-official on Debian (`2.4.1-2`) and available via `brew` on macOS — fits the install-source policy.

### 4a. Repo layout

```
dotfiles/
  common/   # shared across both OSes (.gitconfig, shared .zshrc fragment, ~/.claude/settings.json, keybindings.json)
  linux/    # Debian-only (apt paths, Linux oh-my-zsh bits)
  macos/    # macOS-only (brew paths, mac aliases)
```

Each package mirrors `$HOME`. Stow per machine from `~/dotfiles`:

```bash
stow common          # always
stow linux           # on the VAIO
stow macos           # on the MacBook
```

`.zshrc` lives in `common/` and sources an OS-conditional fragment:

```bash
case "$OSTYPE" in
  darwin*) [ -f ~/.zshrc.macos ] && source ~/.zshrc.macos ;;
  linux*)  [ -f ~/.zshrc.linux ] && source ~/.zshrc.linux ;;
esac
```

### 4b. Content sourcing

- **MacBook is the rich source** → seeds `common/` + `macos/` (years of accumulated config).
- **Linux VAIO is fresh** → seeds `linux/` from current config (zsh + oh-my-zsh, git, Claude settings).

### 4c. Stow gotcha (handle during implementation)

`~/.claude` is an existing real directory with lots of content. Do **not** let stow fold/symlink the whole `.claude` dir — stow only the specific files we want (`settings.json`, `keybindings.json`) so the rest of `~/.claude` stays a normal directory.

## 5. Deliberately NOT synced

- **conda envs** — not portable across OS; recreate per machine from `environment.yml`.
- **`~/.claude/projects/` history** — machine-specific; would bloat and conflict.
- **SSH private keys, tokens, secrets** — never in the dotfiles repo.
- **The `/data` SSD mirror** — Ana chose 2026-05-25 to leave it frozen.
- **Binary drop-zone** (`Images/`, `PDFs/`, `Other/`) — excluded per ADR-001.

## 6. Order of operations

**Phase 0 — Linux, now (Claude):** write this runbook (done), `sudo apt install stow`.

**Phase 1 — Mac, Ana:** repo reconciliation (§3a). Independent of dotfiles.
**Phase 1b — Linux, Claude:** resolve the dangling submodule edit (`vault/…/algoritmo-em-disputa`) — commit or discard per Ana's call.

**Phase 2 — dotfiles bootstrap:**
1. Linux (Claude): create `~/dotfiles` with the layout, seed `linux/` from current VAIO config, create the private GitHub `dotfiles` repo, push.
2. Mac (Ana): clone `dotfiles`, add `common/` + `macos/` from Mac config, push.
3. Linux (Claude): pull, then `stow common && stow linux`.
4. Mac (Ana): `stow common && stow macos`.

**Phase 3 — verification (§7) on both machines.**

## 7. Verification checklist

- [ ] Mac: `git log --oneline -1` shows `a5526d4` (or a clean descendant) on `main`; any pre-repair work preserved on a branch or merged.
- [ ] Linux: repo still in sync at `a5526d4`; submodule edit resolved.
- [ ] `dotfiles` repo exists on GitHub (private) with `common/ linux/ macos/`.
- [ ] Both machines: `stow` applied cleanly, no broken/over-folded symlinks; `~/.claude/projects/` untouched.
- [ ] Both machines: new shell session loads config without errors; `git config user.email` correct.
- [ ] No secrets committed to `dotfiles` (`git log -p` spot-check).
