# data/processed/

Datasets validados e prontos para análise.

## Arquivos

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `records.jsonl` | JSONL | Master records canônicos (1 registro/linha) — ver [ADR-003](../../docs/adr/003-jsonl-as-canonical.md) |
| `corpus_dataset.csv` | CSV | Tabela plana para análise estatística (gerada de `records.jsonl`) |
| `feminist_network_48C51_pt.json` | JSON | Sub-rede feminista Iconclass 48C51 |

## Validação

Cada registro em `records.jsonl` é validado contra
[`master-record.schema.json`](../../tools/schemas/master-record.schema.json)
no CI via `.github/workflows/validate.yml`.

## Regras

- **Nunca editar manualmente** `corpus_dataset.csv` — ele é derivado de `records.jsonl`.
- Para corrigir um registro, edite em `records.jsonl` (ou via Notion + sync).
