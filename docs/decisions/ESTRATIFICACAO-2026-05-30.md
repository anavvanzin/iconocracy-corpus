# Estratificação do corpus + quarentena — 2026-05-30

Passo 1 da ação reformulada (ver `DIALETICA-N165-vs-265.md`). Read-only sobre o corpus;
manifesto-máquina em `quarantine-uncoded-2026-05-30.json`.

## Estratos por proveniência de instrumento (`coded_by`)

| Estrato | n | composição | uso analítico |
|---|---|---|---|
| **S0 — não-codificado** | **41** | sem `coded_by` E sem `regime` (conjunto idêntico) | **QUARENTENA — excluir de notebooks 01–08** |
| **S1 — IconoCode** | 145 | opus 100 · opus-4.6-metadata 29 · opus-4.6-image 16 | núcleo rigoroso (carece confiabilidade inter-versão) |
| **S2 — import/migration** | 78 | vault-import 58 · migration 19 · manual 1 | incluir só após auditoria de confiabilidade |
| **Total export** | 264 | | |

## Quarentena (41 itens) — caracterização
- Critério: **sem `coded_by` E sem `regime`** (conjuntos idênticos, confirmado).
- **Todos os 41 têm `endurecimento_score == 0`** → é **placeholder**, não codificação genuína (score 0
  legítimo exigiria regime + codificador). Não entram em nenhuma estatística até passarem pelo IconoCode.
- Distribuição por país: **FR 25** · UK 7 · BR 6 · US 3. (NÃO é BR-pesado — corrige a premissa dos monks.)
- IDs: `BR-021,023,027,041,044,045` · `FR-049,050,054–067,072,076,078–080,083,086,088,096` ·
  `UK-011–017` · `US-022,023,024`. Lista canônica completa no manifesto JSON.

## Achado de arquitetura (novo, fora do escopo da decisão de N)
`records.jsonl` (canônico, 265) usa IDs **UUID**; `corpus-data.json` (export, 264) usa IDs
**semânticos por país** (`FR-049`). Os campos óbvios `item_id`/`id` **não casam** → join export↔canônico
por id falha (interseção 0). Consequências:
- `coded_by`/`coded_at` (proveniência) **só existem no export**, não no ledger canônico.
- A chave de ligação records↔corpus precisa ser confirmada (`records_to_corpus.py` deve documentá-la).
- Até resolver, a estratificação por instrumento **só é possível sobre o export** — o que é aceitável p/
  decisão analítica, mas a proveniência deveria descer ao canônico.

## Próximos passos (do sequenciamento revisado)
- [x] **1. Estratificar** por `coded_by`.
- [x] **2. Quarentenar os 41** (manifesto gerado).
- [ ] 3. Confiabilidade inter-instrumento: re-codificar amostra cega com opus-4.6 vs opus; concordância nos 10 indicadores.
- [ ] 4. Auditar S2 (import/migration, 78): score é codificação real ou herdada?
- [ ] 5. Definir N analítico por validade (≈145 só-IconoCode vs ≈223 com S2 auditado) + dataset card no Cap.2.
- [ ] 6. (Pré-requisito de arquitetura) resolver a chave de join records↔export e descer proveniência ao canônico.
