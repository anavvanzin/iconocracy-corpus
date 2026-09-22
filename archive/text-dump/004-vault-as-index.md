# ADR-004 — Vault Obsidian como Espelho Catalográfico (substitui Notion)

**Data**: 2026-04-04  
**Status**: Aceito  
**Substitui**: ADR-002 (Notion como index)

---

## Contexto

O ADR-002 designava o Notion como espelho catalográfico do corpus. Na prática,
a integração Notion exigia credenciais externas (`NOTION_API_KEY`), tornava o
sync dependente de serviço de terceiros, e não era utilizada no fluxo diário
de pesquisa. O vault Obsidian (`vault/candidatos/`) já era o ponto de trabalho
real da pesquisadora.

## Decisão

O **vault Obsidian** (`vault/candidatos/`) substitui o Notion como espelho
catalográfico. O `data/processed/records.jsonl` permanece a fonte canônica.

### Fluxo canônico

```
corpus/corpus-data.json      ← fonte de enriquecimento (panofsky, instituição)
        +
data/processed/corpus_dataset.csv  ← purificação (10 indicadores)
        ↓
  csv_to_records.py
        ↓
data/processed/records.jsonl  ← FONTE CANÔNICA (master-record schema)
        ↕
  vault_sync.py (pull/push)
        ↕
vault/candidatos/             ← ESPELHO CATALOGRÁFICO (Obsidian)
        ↓
  records_to_corpus.py
        ↓
corpus/corpus-data.json       ← SITE / COMPANION APP
```

### Scripts afetados

| Script | Mudança |
|--------|---------|
| `vault_sync.py` | **NOVO** — substitui `notion_sync.py` |
| `notion_sync.py` | **DESCONTINUADO** — redireciona para `vault_sync.py` |
| `csv_to_records.py` | **NOVO** — migração corpus-data.json → records.jsonl |
| `records_to_corpus.py` | **NOVO** — export records.jsonl → corpus-data.json |
| `validate_schemas.py` | **ATUALIZADO** — modo sem args valida records.jsonl por padrão |
| `.github/workflows/validate.yml` | **ATUALIZADO** — verifica existência e valida records.jsonl |

## Consequências

**Positivo:**
- Sem credenciais externas — funciona offline
- Vault é o ambiente de trabalho real da pesquisadora
- Sincronização bidirecional via `vault_sync.py status/diff/pull/push/sync`
- CI valida `records.jsonl` a cada push (schema master-record)

**Negativo:**
- Perda da interface visual do Notion (banco de dados com filtros)
- Formatação das notas Obsidian é mais heterogênea que campos estruturados do Notion

## Regras operacionais

1. `records.jsonl` é sempre a fonte canônica — nunca editar `corpus-data.json` diretamente
2. Novas notas SCOUT → `vault_sync.py push` gera registros preliminares em `records.jsonl`
3. `records_to_corpus.py` regenera `corpus-data.json` para o site
4. `validate_schemas.py` (sem args) valida `records.jsonl` — deve passar antes de qualquer commit em `data/`
