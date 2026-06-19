# Findings — SSOT / abordagem de dados (2026-06-19)

## Estado do dado (CRÍTICO)
- **`origin/main` é canônico:** corpus-data.json=**309**, records.jsonl=**308**, uncoded=78.
- **Local `main` era fork STALE** (264/265; 18-ahead/17-behind). Atenção: SEMPRE `git fetch` + comparar com origin/main antes de tocar dado.
- **Mecanismo de quarentena JÁ EXISTE no origin** (2026-05-30): `tag_uncoded_purification.py`, `build_purification_manifest.py`, `purification-manifest.json`, `docs/decisions/quarantine-uncoded-2026-05-30.json` (mesmos 41 ids). flag `fora-do-escopo:27` também existe.

## Arquitetura de dados (descoberta empírica)
- `corpus-data.json` é EXPORT derivado de `records.jsonl` via `records_to_corpus.py` (modo merge default preserva campos curados id/country/support + extras; `--replace` os QUEBRA — não usar).
- Editar o export é efêmero (regenerado). A verdade tem que ser release congelado.
- Git já é o log de eventos. DB redundante como mestre.

## Resultado da dialética
- Verdade = disciplina de aparato crítico (releases git congelados + aparato + dataset card). DB = índice derivado opcional (DuckDB).
- Cross-domain: apparatus criticus filológico = proveniência-de-juízo sem positivismo.
- 2 atritos a declarar: "reprodutibilidade" tem 2 sentidos; custo de atenção.

## Demo DuckDB (validada ao vivo no corpus local 264)
- N por estrato: iconocode-opus 100, vault-import 58, uncoded 41, opus-4.6-refined 29, migration 19, opus-4.6-image 16, manual 1. N analítico (codificados) = 223.
- **Endurecimento por regime (gradiente monotônico):** contra-alegoria 0,63 < fundacional 0,83 < normativo 1,09 < militar 1,60.
- (Recomputar na verdade canônica 309 após reconciliar.)

## Ambiente
- jsonschema 4.26.0 + duckdb 1.5.4 instalados no conda env `iconocracy`.
- Python: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12`.
