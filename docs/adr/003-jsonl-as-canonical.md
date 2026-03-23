# ADR-003: JSONL como formato canônico de registros

**Status:** Aceito
**Data:** 2026-03-22

## Decisão

O arquivo `data/processed/records.jsonl` é a fonte canônica do corpus.
Cada linha é um JSON válido conforme `tools/schemas/master-record.schema.json`.
Todas as outras representações (Notion, CSV, SQLite, HTML) são derivadas deste arquivo.

## Motivação

- JSONL é append-friendly e git-diff-friendly (uma linha por registro)
- Validação automática via JSON Schema no CI
- Portável: qualquer linguagem lê JSONL sem dependências
- Compatível com ferramentas de streaming (jq, pandas, duckdb)

## Consequências

- Todo pipeline de ingestão deve produzir JSONL como saída final
- `corpus_dataset.csv` é gerado a partir de `records.jsonl` (nunca editado manualmente)
- O CI (`validate.yml`) valida cada registro contra o schema a cada push
- Migrações de schema devem ser versionadas em `tools/sql/migrations/`
