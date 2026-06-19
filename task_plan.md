# Task Plan — Versão Canônica de Referência via Aparato Crítico (SSOT sub-projeto 1)

**Goal:** Estabelecer UMA versão canônica de referência do corpus Iconocracia — datada, legível, com proveniência de juízo — ao menor custo de atenção até nov/2027. Metodologia: disciplina de aparato crítico (releases git congelados + aparato de codificação + dataset card). DB = índice derivado opcional (DuckDB).

**Spec:** `docs/decisions/2026-06-19-ssot-apparatus-critico-design.md`
**Dialética:** `docs/decisions/dialectic-ssot-2026-06-19/round_1_synthesis.md`
**Guia de consulta:** `docs/apparatus/GUIA-consulta-corpus.md`

---

## Phase 0 — Reconciliar a divergência (PRÉ-REQUISITO, bloqueia tudo) — Status: pending
Local `main` está 18-ahead/17-behind `origin/main` (309 reg, canônico).
- [ ] 0.1 Auditar os 18 commits locais: têm trabalho ÚNICO? (`git log origin/main..main`).
- [ ] 0.2 Auditar os 17 commits do origin que faltam local (#67–#87).
- [ ] 0.3 Decidir estratégia COM Ana: reset / rebase seletivo / cherry-pick. NÃO bulldoze.
- [ ] 0.4 Executar; confirmar local == origin/main (309/308).
- **Aceitação:** `git rev-list --left-right --count origin/main...HEAD` = 0/0; corpus = 309; nada único perdido.

## Phase 1 — Congelar corpus-v1.0 — Status: pending
- [ ] 1.1 `tools/scripts/freeze_release.py` (tag + snapshot legível + valida). Idempotente.
- [ ] 1.2 Rodar; produzir snapshot + tag.
- [ ] 1.3 Stub dataset card `docs/apparatus/corpus-v1.0-card.md`.

## Phase 2 — Aparato + dataset card — Status: pending
- [ ] 2.1 `docs/apparatus/TEMPLATE.md` (campos por coding contestado).
- [ ] 2.2 Card: 10 dimensões + 2 sentidos de "reprodutibilidade".
- [ ] 2.3 Popular o aparato só para codings usados em alegações.

## Phase 3 — Disciplina de escritor único — Status: pending
- [ ] 3.1 `docs/WORKFLOW-single-writer.md`.
- [ ] 3.2 Redirecionar escritores concorrentes (crons em JSON solto).

## Phase 4 — (DIFERIDO) índice DuckDB derivado — Status: deferred
- [ ] 4.1 `tools/scripts/build_index.py` reconstrói índice do release. Nunca mestre. (DuckDB lê os releases no lugar — ver guia.)

---

## Decisions Log
| Data | Decisão | Por quê |
|------|---------|---------|
| 2026-06-19 | SSOT = aparato crítico git-versionado | Dialética: convergência em snapshot congelado; proveniência-de-juízo nativa; git = log grátis |
| 2026-06-19 | DB invertido para índice derivado (DuckDB) | Custo de mestre vivo > benefício |
| 2026-06-19 | Reconciliação (Phase 0) bloqueia tudo | Sem estado conhecível não há o que congelar |
