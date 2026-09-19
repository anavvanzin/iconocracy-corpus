# ICONOCRACY Workflow Scripts

- `watchdog-corpus-validation.sh` — nightly corpus validation watchdog
- `watch-compile.py` — compile-on-change watcher
- `pick.py` — prompt launcher from `vault/prompts/INDEX.md`
- `env-check.py` — credential hygiene without exposing secrets
- `.pick-prompt-staging.bak` — retired previous pick variant

Usage:
- watchdog: run via cron or manual bash call
- watch-compile: `python scripts/watch-compile.py`
- pick: `python scripts/pick.py`, `pick -d escrita`, `pick -n 3`
- env-check: `python scripts/env-check.py`

All new workflow scripts are versioned with the rest of the monorepo.
