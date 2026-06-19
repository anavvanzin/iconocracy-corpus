# Progress Log — SSOT / abordagem de dados

## Sessão 2026-06-19
- ✅ Brainstorming (superpowers): escopo → fonte única da verdade; raiz → multi-ferramenta/consolidar.
- ✅ Dialética (hegelian-dialectic, 1 rodada, 2 monks): tensão dataset vs hermenêutica → síntese aprovada (aparato crítico git-versionado; DB = índice derivado). Virou a escolha inicial (SQLite event-sourced).
- ✅ Design spec: `docs/decisions/2026-06-19-ssot-apparatus-critico-design.md`.
- ✅ Guia de consulta DuckDB: `docs/apparatus/GUIA-consulta-corpus.md` (validado ao vivo).
- ✅ Planning files: task_plan.md, findings.md, progress.md.
- ⏳ PRÓXIMO: Phase 0 (reconciliar fork ↔ origin/main=309) — precisa do aval da Ana na estratégia. NÃO bulldoze.

### Notas
- Esta entrega foi publicada via branch `docs/ssot-methodology-2026-06-19` (a partir de origin/main, base 309), pois o main local divergente não pode dar fast-forward push.
- Artefatos superseded (nframe-audit, corpus/quarantine reinventada, analytic_corpus.py) NÃO foram commitados — o origin já tem o mecanismo real de quarentena.
- ATENÇÃO operacional: há automação (crons/worktrees) que apaga arquivos untracked no working tree do main local. Trabalhar via branch/worktree isolado.
