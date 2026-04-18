# Vault Curation — Batch 2 (promoção curada)

Data: 2026-04-17
Worktree: `/Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency`

## Objetivo

Promover ao ledger canônico o primeiro sublote de candidatos considerados seguros no batch 1.

## Itens promovidos

1. `SCOUT-205` — Frontispício do Decreto n.º 1 — Governo Provisório (1889)
2. `SCOUT-204` — Proclamação da República — litografia de Angelo Agostini
3. `SCOUT-321` — Statue of the Republic -- World's Columbian Exposition, Chicago
4. `SCOUT-406` — Alegorias do Palácio do Catete — esculturas Val d'Osne (República, Justiça, Agricultura)

## Método aplicado

- leitura das notas fonte em `vault/candidatos/`
- conversão para registros por reutilização da lógica de `vault_sync._vault_note_to_record(...)`
- inserção dos 4 registros no ledger `data/processed/records.jsonl`
- reexport de `corpus/corpus-data.json` a partir de `records_to_corpus.py`
- validação do schema e conferência do sync com o vault

## Novos item_ids gerados

- `SCOUT-204` -> `de7d8e5b-feee-588a-b9e7-69dc588b3a0c`
- `SCOUT-205` -> `c02356de-a24e-52bc-9ee8-15d6cec55a4b`
- `SCOUT-321` -> `7e321b60-8b81-5311-895f-9cc9197d18e6`
- `SCOUT-406` -> `0982e2d1-9591-5fce-9146-143f183fc95a`

## Resultado do batch

### Ledger
- `records.jsonl`: de 165 -> 169 registros
- os 4 novos registros passaram no schema atual

### Export público
- `corpus/corpus-data.json`: reexportado com 169 itens
- os 4 novos itens passaram a integrar a superfície derivada pública local

### Vault
- os 4 itens já estavam presentes como notas no vault
- após a promoção, `vault_sync.py diff` continuou indicando:
  - 0 itens de `records.jsonl` sem nota no vault

## Verificações executadas

### Schema
```bash
conda run -n iconocracy python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
```
Resultado:
- `169/169 records valid`

### Diff antes do reexport
```bash
conda run -n iconocracy python tools/scripts/records_to_corpus.py --diff
```
Resultado:
- 4 itens apareciam como `Only in records.jsonl`
- correspondentes exatamente aos 4 promovidos neste batch

### Reexport
```bash
conda run -n iconocracy python tools/scripts/records_to_corpus.py
```
Resultado:
- `OK: 169 itens escritos em corpus/corpus-data.json`

### Vault sync
```bash
conda run -n iconocracy python tools/scripts/vault_sync.py diff
```
Resultado:
- `Sem itens exclusivos em records.jsonl (por URL).`
- `Itens em records.jsonl sem nota vault (por título): 0`

## Itens mantidos fora deste batch

Continuam fora da promoção automática neste momento:
- `SCOUT-423` — depende de fonte mais sólida
- `SCOUT-206` — URL/catalogação ainda frágil
- `SCOUT-415` — melhor tratado em lane de contra-alegoria / resistência visual

## Próximo passo recomendado

Abrir batch 3 com os casos que dependem de reforço de rastreabilidade:
- `SCOUT-423`
- `SCOUT-206`

E, em paralelo, decidir a arquitetura de ingestão para:
- contra-alegoria
- controles negativos
- backlog SCOUT histórico não promovido
