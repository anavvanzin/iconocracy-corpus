# Reconciliação — 2026-06-19

## Estado final
- `records.jsonl`: 265 linhas
- `corpus-data.json`: 265 itens (264 canônicos originais + BR-047)
- `purification.jsonl`: 264 linhas (1 registro órfão não tinha entrada em purification.jsonl)

## Origem do item extra
O item `8d89996e-c2aa-5a2e-a462-26b91f5308e4` (“A República nos braços de Floriano”, BR, 1891) estava em `records.jsonl` mas ausente de `corpus-data.json`.
Decisão: promover para `BR-047` em `corpus-data.json` com regime `PENDENTE`, pois o registro tem fonte vault-import válida e metadados mínimos.

## Mapa de IDs
Arquivo gerado: `data/processed/record_id_map.json` (264/265 mapeados por título; órfão mapeado manualmente para BR-047).
