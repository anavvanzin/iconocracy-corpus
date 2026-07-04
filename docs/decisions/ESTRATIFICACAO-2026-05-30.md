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

## Atualização 2026-07-04 — contrato de modelo de dados

Estado verificado no `origin/main` de 2026-07-04:

| Camada | n | papel |
|---|---:|---|
| `data/processed/records.jsonl` | 328 | ledger canônico, com `purificacao.coded_by` e `purificacao.regime_iconocratico` |
| `corpus/corpus-data.json` | 328 | export público achatado, sincronizado por URL via `records_to_corpus.py --diff` |
| `data/processed/purification.jsonl` | 238 | ledger de codificações de endurecimento formalizadas |
| `vault/candidatos/` | 399 | espelho catalográfico auxiliar |

Decisão: o conserto do JSON é um **contrato de projeções**, não a troca da fonte
canônica por SQL.

1. `records.jsonl` continua sendo o aparato canônico versionado.
2. `corpus-data.json` continua sendo export público derivado; não deve ser editado manualmente.
3. SQLite/DuckDB/D1 são camadas **derivadas** de consulta e publicação.
4. O N analítico é uma consulta por estrato, não o tamanho bruto de nenhum arquivo.

### Projeção SQL derivada

`tools/scripts/records_to_sqlite.py` materializa a tabela `corpus_strata`, uma linha por
`item_id`, com:

| Campo | Função |
|---|---|
| `coded_by` | proveniência bruta do instrumento |
| `instrument_family` | família estável: `uncoded`, `iconocode_direct`, `curatorial`, `legacy_or_imported`, `tentative`, `opus48_pending`, `other` |
| `validity_stratum` | estrato metodológico: `S0_UNCODED`, `S1_ICONOCODE_DIRECT`, `S2_CURATORIAL`, `S3_LEGACY_OR_IMPORTED`, `S4_TENTATIVE`, `S5_OPUS48_PENDING`, `S9_OTHER_CODED` |
| `quantitative_status` | uso: `excluded_uncoded`, `excluded_scope`, `core_candidate`, `audit_required` |
| `scope_status` | `core_1800_2000` ou `extended_or_out_of_scope` |
| `has_complete_indicators` / `has_regime` / `has_coded_by` | flags 0/1 para auditoria |
| `analytic_eligible`, `period_extended`, `cohort` | metadados de escopo quando presentes |

Regra interpretativa: `core_candidate` não significa “já definitivo para a tese”; significa
“candidato quantitativo sem pendência técnica de codificação no modelo atual”. Estratos
`audit_required` só entram em análise quantitativa após auditoria metodológica explícita.

`opus-4.8` recebe estrato próprio (`S5_OPUS48_PENDING`, `audit_required`) em vez de ser
fundido ao `S1_ICONOCODE_DIRECT`: é instrumento metodologicamente separado até haver
confiabilidade inter-instrumento (IRR) contra os codificadores IconoCode ou decisão
explícita de pooling. Itens `opus-4.8` fora de escopo (`period_extended`/`analytic_eligible=false`/
`fora-do-escopo`) tornam-se `excluded_scope`, preservando o estrato de origem.

Snapshot local 2026-07-04 (`records_to_sqlite.py --output` sobre 328 registros):
S0 41 `excluded_uncoded` · S1 134 (107 `core_candidate` / 27 `excluded_scope`) ·
S2 15 `audit_required` · S3 108 `audit_required` · S4 11 `audit_required` ·
S5 19 (14 `audit_required` / 5 `excluded_scope`).

## Quarentena (41 itens) — caracterização
- Critério: **sem `coded_by` E sem `regime`** (conjuntos idênticos, confirmado).
- **Todos os 41 têm `endurecimento_score == 0`** → é **placeholder**, não codificação genuína (score 0
  legítimo exigiria regime + codificador). Não entram em nenhuma estatística até passarem pelo IconoCode.
- Distribuição por país: **FR 25** · UK 7 · BR 6 · US 3. (NÃO é BR-pesado — corrige a premissa dos monks.)
- IDs: `BR-021,023,027,041,044,045` · `FR-049,050,054–067,072,076,078–080,083,086,088,096` ·
  `UK-011–017` · `US-022,023,024`. Lista canônica completa no manifesto JSON.

## Achado de arquitetura (histórico, parcialmente resolvido em 2026-07-04)
`records.jsonl` (canônico, 265) usa IDs **UUID**; `corpus-data.json` (export, 264) usa IDs
**semânticos por país** (`FR-049`). Os campos óbvios `item_id`/`id` **não casam** → join export↔canônico
por id falha (interseção 0). Consequências:
- Em 2026-05-30, `coded_by`/`coded_at` (proveniência) eram tratados como superfície do export.
- Em 2026-07-04, `purificacao.coded_by` e `purificacao.coded_at` já estão no ledger canônico para os
  registros codificados; a projeção SQL usa `records.jsonl` como fonte e só enriquece metadados via export.
- A chave de ligação records↔corpus é materializada por `data/processed/id-mapping.json` e pelo UUID5
  determinístico usado por `records_to_corpus.py`/`records_to_sqlite.py`.

## Próximos passos (do sequenciamento revisado)
- [x] **1. Estratificar** por `coded_by`.
- [x] **2. Quarentenar os 41** (manifesto gerado).
- [ ] 3. Confiabilidade inter-instrumento: re-codificar amostra cega com opus-4.6 vs opus; concordância nos 10 indicadores.
- [ ] 4. Auditar S2 (import/migration, 78): score é codificação real ou herdada?
- [ ] 5. Definir N analítico por validade (≈145 só-IconoCode vs ≈223 com S2 auditado) + dataset card no Cap.2.
- [x] 6. (Arquitetura) materializar chave records↔export e proveniência em projeção derivada (`corpus_strata`);
  manter `records.jsonl` como fonte canônica.
