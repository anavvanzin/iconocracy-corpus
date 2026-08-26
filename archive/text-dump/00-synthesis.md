# Audit Synthesis — Research Workspace 360° — Wave 3
Data: 2026-04-19
Escopo: /Users/ana/Research/ (meta-workspace)
Lentes: 6 subagentes, 3 waves

## Resumo executivo

A auditoria de 3 waves identificou **24 findings** (7 CRITICAL, 11 MAJOR, 6 MINOR) e **8 pontos fortes**. O T5 já executou e resolveu C-01 (11 registros com valores 4). As prioridades remanescentes são: (1) correção do build_hf_release.py para bloquear release com purification.jsonl vazio, (2) sync do companion-data.json (145→165), (3)一刀切的 TypeScript `as any` no iurisvision, (4) padronização de citações Goodrich/Mondzain nos drafts. O pipeline canonical está funcional (165/165 válidos, 188 testes passando) mas carece de监控 CI para dados derivados e testes para o ETL core.

---

## Top-10 Achados Cross-Domain

| # | Severity | Finding | Domínio | Remediation |
|---|---|---|---|---|
| 1 | **CRITICAL** | build_hf_release.py não valida purification.jsonl vazio — HF snapshot construído com dado faltante | Data Engineer | Adicionar guard clause: `if len(purification) == 0: raise SystemExit` |
| 2 | **CRITICAL** | companion-data.json stale (145 vs 165) — CI sem cobertura | Data Engineer | Executar sync_companion.py + adicionar ao CI |
| 3 | **CRITICAL** | `window as any` em ThesisDashboard.tsx:566 — Runtime TypeError silencioso | Code Review | Verificar `if ('aistudio' in window)` antes do acesso |
| 4 | **CRITICAL** | visual-essay hardcoded 145 itens (stale, corpus→165) | Frontend/Visual | Atualizar contador para 165 |
| 5 | **CRITICAL** | Goodrich citado como 2013/2014/2017 — inconsistência bibliográfica | Academic Content | Padronizar para 2017 (*Legal Emblems*) |
| 6 | **CRITICAL** | Mondzain citada como 2002 E 2005 — ABNT viola padronização | Academic Content | Padronizar para 2002 (edição original francesa) |
| 7 | **MAJOR** | `as any` em iurisvision (12×) — Firebase Proxy + Firestore casts eliminam type safety | Code Review | Interfaces tipadas para FirestoreDoc, UserProfile |
| 8 | **MAJOR** | 3 parsers independentes de corpus-data.json — risco de divergência de schema | Architecture | Extrair `shared/corpus-parser.ts` canônico |
| 9 | **MAJOR** | purification.jsonl vazio (0 registros) — dual source sem reconciliação | Data Engineer | code_purification.py deve atualizar records.jsonl in-place |
| 10 | **MAJOR** | CI só em 2/7 repos — validate.yml não roda pytest (21 arquivos de teste nunca executados) | Architecture | Adicionar pytest step ao CI ou criar tests.yml |

---

## Matriz de Dependência (Fix X → Unlocks Y)

```
[C-01 T5] Scale fix       → [C-02] sync companion data
                       → [M-05] T3 coding (30 items queue)
                       → [M-04] visual-essay stale counter

[C-02] sync companion     → [C-03] window as any (independent)
                       → [M-01] as any iurisvision (independent)

[C-02] build_hf guard     → [M-06] HF release safety (unblocks release)

[M-03] corpus parser      → [M-02] 3 independent parsers converge
                       → [C-03] window as any (independent)

[M-05] citation fix       → [C-04] Mondzain standardization (independent)

[M-09] CI pytest          → [M-10] ETL tests (unblocks M-01 fix confidence)
```

---

## Roadmap em 3 Sprints

### Sprint 1 (esta semana) — Data Pipeline Fixes

| Task | Owner | Effort | Exit Criteria |
|---|---|---|---|
| T5 executar (scale fix) | **Eu** | 2h | ✓ Done — 165/165, commit 1d9e6f6 |
| build_hf_release.py guard clause | Eu ou subagente | 1h | `python build_hf_release.py` exits 1 se purification.jsonl vazio |
| sync_companion.py executar + commit | Eu | 30min | companion-data.json mostra 165, coded counts corretos por país |
| companion-data.json no CI trigger | subagente | 1h | validate.yml cobre companion-data.json |

### Sprint 2 (próxima semana) — Type Safety + CI Coverage

| Task | Owner | Effort | Exit Criteria |
|---|---|---|---|
| Fix `window as any` em ThesisDashboard.tsx | subagente (iurisvision) | 1h | `npx tsc --noEmit` clean |
| Refatorar `as any` Firebase casts → interfaces | subagente (iurisvision) | 4h | FirestoreDoc, UserProfile interfaces definidas e usadas |
| Extrair shared/corpus-parser.ts | subagente | 3h | 3 consumers (hub, scout-agent, companion) usam mesmo parser |
| Adicionar pytest ao validate.yml | subagente | 1h | CI executa 188 testes no gate |
| Notebook dependency fix (prince, statsmodels) | Eu | 2h | environment.yml inclui todas as deps ausentes |

### Sprint 3 (2-3 semanas) — Academic Content + Visual Surfaces

| Task | Owner | Effort | Exit Criteria |
|---|---|---|---|
| Padronizar citações Goodrich/Mondzain | Você (human) | 3h | `abnt_citations.py` reporta 0 inconsistências |
| Corrigir English draft terminology | Você (human) | 2h | desexualization-threshold-draft-v1.md usa PT originals |
| Atualizar visual-essay hardcoded counter (145→165) | Eu | 30min | visual-essay mostra 165 |
| Completar revisão manuscrito (2→9 capítulos _rev) | Você + subagente | ongoing | pipeline tracking atual, capítulo 3+ revisados |
| Notebooks 01-04: limpar outputs stored (anti-pattern) | Eu | 2h | Outputs não commitados, repo mais leve |

---

## Métricas de Sucesso da Auditoria

| Métrica | Valor |
|---|---|
| Total findings identificados | 24 (7 CRITICAL, 11 MAJOR, 6 MINOR) |
| T5 resolvido (scale fix) | ✓ 165/165, commit 1d9e6f6 |
| Wave 1 completa | ✓ 3/3 relatórios |
| Wave 2 completa | ✓ 3/3 relatórios |
| Wave 3 síntese | ✓ Este documento |
| Wall-clock total | ~30 min (subagentes) + T5 |

---

## Out of Scope (deferred)

- Repo topology decision (T1-T4 subtree/submodule/mirror)
- IAA pilot + scored codebook with anchors
- Second multimodal model via reconcile_iconocode.py
- mnemosyne-scout/ideas/ verificação/atualização
- ARGOS continuation (campaigns 11-16)

---

## Próximo Passo

Aprovado este synthesis → disparar remediation-plan para Sprint 1.
Execution: eu ou delegation para subagentes conforme esforço estimado.