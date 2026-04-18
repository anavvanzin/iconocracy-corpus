# Handoff

## State
- Shipped `e29e941` on main: protobufjs override ^7.5.5 in `shared/package.json` (CVE-2026-41242). Dependabot alert #1 resolved. 0 vulns.
- Santa-method review of `bbae856` + `4df06d8` + reconciliation plan → both FAILED. Fixes not yet applied.
- Root cause of rogue "vault backup:" commits identified: `vault/.obsidian/plugins/obsidian-git/data.json` (autoSaveInterval=10, autoCommitOnlyStaged=false, disablePush=false). NOT cron/Claude.

## Next
1. Apply 5 Santa fixes: (a) widen ruff regex in `.claude/settings.json` to include `tools|tests|corpus|deploy` + root; (b) fix `legendre1994` title → add "chrétienne"; (c) fix `haraway1985` title hyphen "Socialist-Feminism"; (d) `.gitignore corpus/DASHBOARD_CORPUS.html` + `git rm --cached` + patch obsidian-git `autoCommitOnlyStaged=true`; (e) close Dependabot PR `origin/dependabot/npm_and_yarn/shared/npm_and_yarn-91b74eecbb`.
2. Verify `descola2023` translator (Mariana Nogueira vs Marcela Vieira) from printed Ubu edition.
3. Deferred: `carson2023` editora/tradutor/cidade (needs user); then session plan continues (Devil's Advocate cap-5 §5.2.1 OR intro §I.4–I.6).

## Context
- cwd `/Users/ana/Research`; main work in `hub/iconocracy-corpus`. Caveman mode on. Portuguese for thesis, English for code.
- Uncommitted pre-existing: `vault/.makemd/fileCache.mdc`, `vault/.makemd/superstate.mdc`; untracked `vault/Tags/`.
- Santa agent IDs preserved for SendMessage: `a365f0e3620ef6dac`, `acc44585b20370ddd`, `a57678138b2b3b8fa`, `a00d5213cbab13397`, `aee81aaadd3472e47`, `a748d495a128ad127`.
