# Task Plan — Versão Canônica de Referência via Aparato Crítico (SSOT sub-projeto 1)

**Goal:** Estabelecer UMA versão canônica de referência do corpus Iconocracia — datada, legível, com proveniência de juízo — ao menor custo de atenção até nov/2027. Metodologia: disciplina de aparato crítico (releases git congelados + aparato de codificação + dataset card). DB = índice derivado opcional.

**Spec:** `docs/decisions/2026-06-19-ssot-apparatus-critico-design.md`
**Dialética:** `docs/decisions/dialectic-ssot-2026-06-19/round_1_synthesis.md`

**Princípios:** git é o log de eventos (de graça); exports são projeções; proveniência-de-JUÍZO (não de medição); aparato ACRESCE por alegação, não upfront.

---

## Phase 0 — Reconciliar a divergência (PRÉ-REQUISITO, bloqueia tudo) — Status: pending
Sem um estado conhecível não há o que congelar. Local `main` está 18-ahead/17-behind `origin/main` (309 reg, onde o trabalho canônico evoluiu).
- [ ] 0.1 Auditar os 18 commits locais: têm trabalho ÚNICO não presente no origin? (`git log origin/main..main`, inspecionar cada).
- [ ] 0.2 Auditar os 17 commits do origin que faltam local (já mapeados: #67–#87; corpus setup, reconcile companion #84, purification #70, re-acquire #75/#76).
- [ ] 0.3 Decidir estratégia COM Ana: (a) reset local→origin/main salvando o único; (b) rebase seletivo dos 18; (c) cherry-pick pontual. NÃO bulldoze.
- [ ] 0.4 Executar a estratégia escolhida; confirmar local == origin/main (309/308).
- [ ] 0.5 Reaplicar os artefatos desta sessão (spec, dialética, planning) sobre o estado reconciliado.
- **Aceitação:** `git rev-list --left-right --count origin/main...HEAD` = 0/0 (ou só commits intencionais); corpus contável = 309; nada único perdido.

## Phase 1 — Congelar corpus-v1.0 (primeiro release) — Status: pending
- [ ] 1.1 Escrever `tools/scripts/freeze_release.py`: dado git main, cria tag `corpus-v1.0`, gera snapshot legível + valida schema/paridade. Idempotente.
- [ ] 1.2 Rodar; produzir o snapshot + tag.
- [ ] 1.3 Stub do dataset card `docs/apparatus/corpus-v1.0-card.md` (N, estratos por coded_by, países).
- **Aceitação:** existe tag `corpus-v1.0`; snapshot reconstruível; contagem única e datada.

## Phase 2 — Aparato + dataset card completo — Status: pending
- [ ] 2.1 `docs/apparatus/TEMPLATE.md`: campos por coding contestado/revisado (id, dimensão, valor, racional-prosa, revisões/variantes, motivo de quarentena).
- [ ] 2.2 Dataset card completo: significado das 10 dimensões; **declarar os 2 sentidos de "reprodutibilidade"** (estatística vs hermenêutica) e qual a tese reivindica.
- [ ] 2.3 Popular o aparato SÓ para codings já usados em alegações existentes (não os 309).
- **Aceitação:** todo coding citado num capítulo tem racional recuperável; card declara as 2 reprodutibilidades.

## Phase 3 — Disciplina de escritor único — Status: pending
- [ ] 3.1 Doc `docs/WORKFLOW-single-writer.md`: entre releases, git main é canônico; ferramentas (CC, Antigravity, crons) propõem via commit/PR, nunca escrita direta espalhada.
- [ ] 3.2 Aposentar/redirecionar escritores concorrentes identificados (crons que escrevem em JSON solto).
- **Aceitação:** nenhuma ferramenta escreve fora do fluxo git; documentado.

## Phase 4 — (DIFERIDO/opcional) índice SQLite derivado — Status: deferred
- [ ] 4.1 Só se consulta/dashboard exigir: `tools/scripts/build_index.py` reconstrói SQLite do release. Nunca mestre.
- **Aceitação:** índice descartável e reconstruível; verdade permanece no release git.

---

## Decisions Log
| Data | Decisão | Por quê |
|------|---------|---------|
| 2026-06-19 | SSOT = aparato crítico git-versionado, não SQLite event-sourced mestre | Dialética: ambos os monks convergiam em snapshot congelado; proveniência-de-juízo tem tecnologia humanista nativa; git = log grátis |
| 2026-06-19 | DB invertido para índice derivado opcional | Custo de manter mestre vivo > benefício; releases git bastam p/ verdade |
| 2026-06-19 | Reconciliação (Phase 0) bloqueia tudo | Sem estado conhecível não há o que congelar |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (none yet) | | |
