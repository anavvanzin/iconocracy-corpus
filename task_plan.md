# Task Plan — E1 fechamento + preparação do IRR

**Goal:** Fechar o N do E1 (corrigir os 7 motivos-núcleo com imagem ruim, decidir N analítico) e deixar o corpus pronto para o IRR re-run (rater-2). Resolver o `corpus-data.json` alheio antes de qualquer merge do branch.

**Worktree:** `.claude/worktrees/e1-fable5-recode` · branch `worktree-e1-fable5-recode` · base origin/main
**Plano-irmão (origem):** `docs/superpowers/plans/2026-06-09-e1-fable5-recode.md` (6/6 tasks ✅)
**Status E1:** `docs/decisions/E1-FABLE5-STATUS-2026-06.md`

---

## Estado atual (E1 COMPLETO)
- Índice `data/processed/pathosformel_index.jsonl`: 43 itens, todos `fable-5`, N=38 em escopo + 5 fora_escopo, all-zero=0.
- HEAD `155fb17`. 29 testes verdes. Nada pushado.
- 7 itens em `e1_excluded.json` (`bad_image_reacquire`) aguardando imagem nova.

## Fases

### Phase 0 — Decisões da Ana (GATE) — Status: COMPLETE
- [x] **#1** Reaquirir os 7 motivos-núcleo? → **SIM** (2026-06-15).
- [x] **#2** N=38 vs expandir? → **EXPANDIR** via reaquisição dos 258 sem-imagem antes de fechar o N (2026-06-15).
- [x] **#3** `corpus/corpus-data.json` alheio → RESOLVIDO 2026-06-15: era regressão (264 ⊆ HEAD 314, faltavam os 43 candidatos de 08/06). Descartado via `git checkout`, restaurado HEAD 314.
> As fases abaixo dependem destas respostas. Não executar antes.

### Phase 1 — Resolver corpus-data.json (independente) — Status: COMPLETE
- [x] Diagnóstico: working-tree=264 ⊆ HEAD=314; HEAD alinha melhor com records (296 vs 254). Veredito: regressão/lixo.
- [x] `git checkout corpus/corpus-data.json` → restaurado 314 itens. Working tree limpo.

### Phase 2 — Stage A: reaquirir + recodificar os 7 (PILOTO do loop) — Status: COMPLETE (6/7)
- [x] Re-fetch via firecrawl scrape/search + **verificação visual item a item**. 6/7 OK: DE-013, UK-FLORIN-1902, BR-006, UY-001, UK-010, DE-008. Salvos em `binaries/Images-reacquired-2026-06-15/`.
- [x] Recodificados via Workflow iconocode (wf_121f3a05), append validado → **N 38 → 44** (índice 49 linhas). Removidos do excluded.json; worklist marcada done.
- [x] **BE-002 resolvido (parcial):** Ana = "arquitetura forense sempre no escopo" ([[feedback-forensic-architecture-scope]]) + método = só codificar se achar alegoria feminina DO conjunto. Palais de Bruxelles = legisladores masculinos (Demóstenes) + edifício monumental; **nenhuma alegoria feminina do Palais achada** (2 buscas) → fica `pending_female_allegory` em excluded.json. Revisitar com input especializado.

### Phase 3 — Stage B: campanha de reaquisição dos 258 sem-imagem (#2=expandir) — Status: pending
- [ ] **B1 diagnóstico:** breakdown de domínios das 258 URLs; classificar (catálogo c/ og:image | IIIF | PDF | morto). Decidir estratégia de extração por classe (firecrawl_scrape/extract, archive-fallback, IIIF manifest).
- [ ] **B2 piloto:** extrair ~10-15 imagens reais de catálogos, verificar visualmente, medir taxa de sucesso por domínio.
- [ ] **B3 escala:** extrair o resto em lotes; triar; rotear falhas (morto/sem-imagem) p/ exclusão definitiva.
- [ ] **B4 codificar:** novos itens com imagem → Workflow iconocode (CUSTO: ~30k tokens/item). Append. Atualizar status doc.

### Phase 4 — Desenho do IRR re-run (depende do N expandido) — Status: pending
- [ ] Revisar `docs/decisions/IRR-RE-RUN-DESIGN-2026-06-09.md` p/ o N final.
- [ ] `select_irr_sample.py` (seed fixa); rater-2 sobre a amostra; `compute_irr.py`.

### Phase 5 — Fechamento — Status: pending
- [ ] Commit dos planning files + decisões; decidir merge do branch (PR) ou manter worktree. `release-gate` só se for exportar.

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (nenhum nesta fase ainda) | — | — |
