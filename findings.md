# Findings — SSOT / abordagem de dados (2026-06-19)

## Estado do dado (CRÍTICO)
- **Local `main` é fork STALE:** corpus-data.json=264, records.jsonl=265.
- **`origin/main` é canônico e à frente:** corpus-data.json=**309**, records.jsonl=**308**, uncoded=78. PRs #67–#87 (corpus setup #86/#87, reconcile companion #84, purification #70, re-acquire #75/#76).
- **Git:** local 18-ahead / 17-behind origin/main. Reconciliação = Phase 0 (bloqueia tudo).
- **Mecanismo de quarentena JÁ EXISTE no origin** (2026-05-30): `tag_uncoded_purification.py`, `build_purification_manifest.py`, `purification-manifest.json`, `docs/decisions/quarantine-uncoded-2026-05-30.json` (mesmos 41 ids). flag `fora-do-escopo:27` também existe.

## Arquitetura de dados (descoberta empírica)
- `corpus-data.json` é EXPORT derivado de `records.jsonl` via `records_to_corpus.py` (modo merge default preserva campos curados id/country/support + campos extras; `--replace` os QUEBRA — não usar).
- Editar o export é efêmero (regenerado). Por isso a verdade tem que ser release congelado, não edição de arquivo.
- Git já serve como log de eventos (commit/tag/mensagem). DB seria redundante como mestre.

## Resultado da dialética (decisão de método)
- Verdade = **disciplina de aparato crítico** (releases git congelados + aparato de codificação + dataset card). DB invertido para índice derivado opcional.
- Cross-domain chave: **apparatus criticus** filológico = proveniência-de-juízo sem positivismo, 500 anos de humanidades.
- 2 atritos declarados (não resolvidos, a nomear): "reprodutibilidade" tem 2 sentidos opostos (estatística vs hermenêutica); custo de atenção é real (orçar).
- Arquivos: `docs/decisions/dialectic-ssot-2026-06-19/` (briefing, monks, negação, síntese).

## Ambiente
- jsonschema 4.26.0 instalado no conda env `iconocracy` (validate_schemas.py voltou a rodar; era o único blocker).
- Python canônico: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12`.

## Decisões da Ana nesta sessão
1. Foco = fonte única da verdade (vs validade/roadmap).
2. Raiz = multi-ferramenta → consolidar.
3. (revisada pela dialética) mestre = não mais SQLite event-sourced; agora aparato crítico git-versionado.
4. Proveniência = (era event-sourced total) → agora proveniência-de-juízo via aparato.
