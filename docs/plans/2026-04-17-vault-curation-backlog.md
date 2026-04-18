# Vault Curation Backlog — pós-restauração do ledger

Data: 2026-04-17
Branch: `infra/hub-consistency-refactor`
Worktree: `/Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency`

## Objetivo

Após restaurar `records.jsonl`, o próximo problema deixou de ser estrutural e passou a ser curatorial:
- o ledger canônico está válido
- `records_to_corpus.py --diff` está sincronizado
- o vault ainda contém um backlog grande de notas SCOUT e notas legadas fora do ledger canônico

Este documento organiza o backlog para a próxima frente de trabalho.

## Estado atual

- `records.jsonl`: 165 registros válidos
- `vault/candidatos/`: 314 notas
- `records.jsonl` agora tem espelho para todos os seus itens no vault
- ainda restam muitas notas no vault que não pertencem ao ledger canônico atual

## Diagnóstico consolidado

### 1. Divergência residual do vault não é mais quebra de sync do ledger
O problema remanescente é:
- excesso de notas no vault (`vault-only`)
- mistura de:
  - notas legadas sem `url:` padronizada
  - notas SCOUT especulativas
  - duplicatas por URL normalizada
  - candidatas reais ainda não promovidas ao ledger

### 2. Causas principais já identificadas

#### A. Notas legadas com frontmatter incompleto
Muitas notas antigas têm `id` e título, mas não têm `url:` em frontmatter.
Isso distorce diagnósticos puramente baseados em URL.

#### B. Diferenças de título e URL normalizada
Há casos em que o item já existe no vault, mas com:
- título diferente
- mirror de URL diferente
- `http` vs `https`
- Gallica com ou sem `.item`

#### C. Backlog SCOUT genuíno
Há um conjunto substantivo de notas que parecem candidatas reais à promoção, mas ainda não foram integradas ao ledger canônico.

#### D. SCOUTs fora de escopo ou de baixa prioridade
Outro conjunto parece ser:
- false positive de busca
- duplicata de item já representado
- variante de denominação já abstraída no corpus
- nota metodológica / controle negativo

## Buckets operacionais

## Bucket 1 — Duplicatas / normalização (não promover)

Duplicatas claras ou muito prováveis:
- `SCOUT-106`
- `SCOUT-341`
- `SCOUT-344`

Ação recomendada:
- marcar explicitamente como duplicata consolidada
- manter fora de `records.jsonl`
- opcionalmente mover para subgrupo/arquivo de duplicatas curadas

## Bucket 2 — Candidatas fortes para promoção futura

Prioridade alta sugerida:
- `SCOUT-406`
- `SCOUT-204`
- `SCOUT-205`
- `SCOUT-206`
- `SCOUT-423`
- `SCOUT-415`
- `SCOUT-321`

Conjunto mais amplo de promoção provável:
- `BR-017`
- `SCOUT-090`
- `SCOUT-091`
- `SCOUT-092`
- `SCOUT-095`
- `SCOUT-098`
- `SCOUT-102`
- `SCOUT-204`
- `SCOUT-205`
- `SCOUT-206`
- `SCOUT-320`
- `SCOUT-321`
- `SCOUT-406`
- `SCOUT-407`
- `SCOUT-408`
- `SCOUT-409`
- `SCOUT-410`
- `SCOUT-411`
- `SCOUT-412`
- `SCOUT-413`
- `SCOUT-414`
- `SCOUT-415`
- `SCOUT-416`
- `SCOUT-417`
- `SCOUT-418`
- `SCOUT-419`
- `SCOUT-420`
- `SCOUT-421`
- `SCOUT-422`
- `SCOUT-423`
- `SCOUT-424`

Observação crítica:
- alguns casos ainda dependem de limpeza de URL antes da promoção
- principalmente notas com URL genérica de Hemeroteca / `memoria.bn.br`

## Bucket 3 — Backlog SCOUT legado / baixa prioridade

Principalmente notas auto-geradas ou pouco validadas, por exemplo:
- `SCOUT-323` a `SCOUT-360` (com exceções já identificadas)
- `SCOUT-361`
- `SCOUT-362`
- `SCOUT-365`
- `SCOUT-366`
- `SCOUT-367`
- variantes de série/denominação como `SCOUT-104`, `SCOUT-107`, `SCOUT-120`, `SCOUT-121`, `SCOUT-126`, `SCOUT-127`

Ação recomendada:
- não promover automaticamente
- manter como backlog de triagem iconográfica
- só promover após revisão manual com critério de corpus

## Bucket 4 — Controles negativos / material metodológico

Exemplos:
- `SCOUT-NC-01`
- `SCOUT-NC-03`

Ação recomendada:
- manter fora do ledger positivo
- considerar uma superfície separada de controle negativo / contra-alegoria

## Próxima sequência recomendada

### Fase 1 — Limpeza semântica do vault
1. criar marcação consistente para duplicatas
2. criar marcação consistente para backlog não promovido
3. separar controles negativos do fluxo de candidatos positivos

### Fase 2 — Promoção curada em lotes pequenos
Promover em lotes de 5–10 notas, começando pelo grupo de prioridade alta:
- `SCOUT-406`
- `SCOUT-204`
- `SCOUT-205`
- `SCOUT-206`
- `SCOUT-423`
- `SCOUT-415`
- `SCOUT-321`

### Fase 3 — Normalização de URLs legadas
Antes da promoção de certos SCOUTs, corrigir URLs genéricas ou instáveis.

## Critério para promoção ao ledger

Promover somente se:
1. a nota estiver claramente em escopo do corpus
2. houver URL rastreável suficiente
3. não for duplicata substantiva de item já canônico
4. a nota tiver descrição iconográfica minimamente utilizável
5. a promoção não quebrar a distinção entre candidato e item canônico

## Resultado desta etapa

Nesta etapa não houve promoção automática de backlog SCOUT ao ledger canônico.
O que foi feito foi:
- restaurar o sync do ledger
- completar o espelho do ledger atual no vault
- registrar uma triagem explícita do backlog remanescente para a próxima passada
