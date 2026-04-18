# Corpus Restoration Log

Data: 2026-04-17
Branch: `infra/hub-consistency-refactor`
Worktree: `/Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency`

## Problema investigado

O gate canônico falhava porque `data/processed/records.jsonl` tinha apenas 2 registros experimentais e ambos estavam fora do schema atual. Isso produzia:
- falha em `validate_schemas.py`
- divergência massiva em `records_to_corpus.py --diff`
- ruptura prática do contrato `records.jsonl -> corpus-data.json`

## Evidência de causa-raiz

1. `corpus/corpus-data.json` continuava com 165 itens
2. `data/processed/corpus_dataset.csv` existia e continha a base de indicadores
3. o script `tools/scripts/csv_to_records.py` existe explicitamente para reconstruir `records.jsonl` a partir dessas superfícies
4. o dry-run do script gerou 165 registros, confirmando que a base de reconstrução estava presente
5. a primeira reconstrução ainda falhou no schema por incompatibilidade entre o script e o schema atual:
   - `coded_by` / `coded_at` vazios ou `null`
   - alguns indicadores ainda em escala legada 0–4
   - alguns compostos acima de 3

## Correções aplicadas

### `tools/scripts/csv_to_records.py`
- normalizei `coded_by` com fallback textual seguro
- normalizei `coded_at` para `date-time` válido, inclusive convertendo datas simples para `T00:00:00Z`
- limitei indicadores legados à escala atual 0–3
- limitei `purificacao_composto` ao intervalo 0–3

### `tools/scripts/records_to_corpus.py`
- tratei placeholders `https://iconocracy.corpus/placeholder/<ID>` como ausência de URL para matching e diff
- corrigi o matching entre `records.jsonl` e `corpus-data.json` para itens sem URL real
- preservei o comportamento de não exportar placeholders como URLs públicas no corpus

### `tools/scripts/vault_sync.py`
- alinhei `push` e `_record_to_vault_note()` para preferir a URL primária de `webscout.search_results[0].url` antes de `input_url`
- isso evita gerar notas novas com URL de handle/landing page quando o registro já carrega a URL primária da evidência

### Dados escritos
- regenerei `data/processed/records.jsonl` com 165 registros válidos
- executei `vault_sync.py push`, que criou 113 notas novas para cobrir itens do corpus ainda sem espelho no vault

## Verificações executadas

### Schema
```bash
conda run -n iconocracy python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
```
Resultado:
- `165/165 records valid`

### Diff records -> corpus
```bash
conda run -n iconocracy python tools/scripts/records_to_corpus.py --diff
```
Resultado:
- `Em sincronização (por URL).`

### Purificação
```bash
conda run -n iconocracy python tools/scripts/code_purification.py --status
```
Resultado:
- 165 itens
- 0 codificados
- 165 restantes

### Vault status
```bash
conda run -n iconocracy python tools/scripts/vault_sync.py status
```
Resultado após push:
- `records.jsonl`: 165 registros
- `vault/candidatos/`: 306 notas
- 255 notas SCOUT e 26 notas com corpus ID

## Estado final

### Restaurado
- `records.jsonl` voltou a ser schema-válido
- `records_to_corpus.py --diff` voltou a sincronizar com `corpus-data.json`
- o contrato central `records.jsonl -> corpus-data.json` foi restaurado

### Ainda pendente
- `purification.jsonl` continua vazio em termos substantivos de codificação
- o vault continua contendo muitas notas SCOUT extras que não pertencem ao ledger canônico; isso é backlog de curadoria, não ruptura do schema

## Próximo passo recomendado

Abrir uma frente separada para decidir o status das notas SCOUT extras do vault:
1. candidatas a promoção para ledger canônico
2. candidatas a arquivamento
3. candidatas a exclusão/contra-alegoria/fora de escopo
