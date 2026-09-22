# Progress Log

## Session 2026-06-13/14 — E1 codificação completa
- Retomei do índice vazio (dry-run de 10/06 não gravado).
- Reescrevi `e1_append_batch.py` p/ Estratégia B (fora_escopo + enriquecimento da worklist + auto-correção de item_id via sigla) + corrigi 2 testes obsoletos da triagem. → 29 testes verdes. Commit 5f69510.
- Gravei os 5 do dry-run (062aca4).
- Codifiquei os 45 restantes via Workflow (45 agentes iconocode, schema validado, 1.35M tokens). 2 falsos starts: args-como-string e schema sem coded_by → corrigidos.
- Separei 7 imagens-ruins (reaquisição) de 3 fora_escopo genuínos; gravei 38. Commit 13c963d.
- Status doc + handoff. Commit 155fb17. **6/6 tasks do plano-irmão fechadas.**
- Resultado: índice 43 itens, N=38, all-zero=0.

### Test results
- `pytest tests/tools/test_e1_append_batch.py tests/tools/test_e1_triage_images.py` → 29 passed.

### Pendências p/ próxima sessão
- 3 decisões da Ana (Phase 0 do task_plan.md): reaquirir os 7? / N=38 vs expandir / corpus-data.json alheio.
- Próximo passo provável: Phase 1 (diagnosticar corpus-data.json via sync-corpus) — é independente e destrava merge.

## Session 2026-06-15 — Stage A (reaquisição dos 7) + setup do /insights
- Phase 1: corpus-data.json alheio era regressão (264⊆314) → git checkout, restaurado 314.
- Setup (/insights): hook global secret-scan (validado), skill /reconcile, MCP corpus-vault (filesystem) + iconclass-db (sqlite) — ambos Connected. CLAUDE.md global: +Diagnosis-before-action, +State-Persistence (#1/#2 já existiam).
- Stage A: 6/7 motivos-núcleo reaquiridos (firecrawl + verificação visual), recodificados via Workflow (wf_121f3a05). N 38→44 (índice 49). BE-002 deferido (arquitetura).
- Regimes N=44: normativo 21, fundacional 13, militar 8, contra-alegoria 2.
