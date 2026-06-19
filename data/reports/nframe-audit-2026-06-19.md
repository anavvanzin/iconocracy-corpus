# Corpus N-Frame Audit — Scope & Validity Revalidation

_2026-06-19 · análise read-only · **dado canônico revertido ao HEAD commitado nesta sessão** (corpus-data.json=264, records.jsonl=265 intactos)._

> Alinhado a `docs/decisions/DIALETICA-N165-vs-265.md` (Aufhebung v2, pós-santa-loop). Eixo de decisão = **estrato de validade × proveniência de instrumento**, NÃO data.

## 1. Decisão (Ana, 2026-06-19): quarentena de dois filtros
Dois filtros **ortogonais e disjuntos**, ambos documentados no dataset card do Cap.2:
- **Filtro 1 — critério de inclusão** (`fora-do-escopo`): 27 itens fora dos 6 países / período 1800–2000 (ES, PT, NL, MX, UY, EU pan-europeu, Justitias pré-1800). **Todos codificados** (iconocode-opus) — exclusão por escopo, não por validade.
- **Filtro 2 — validade de codificação** (Estrato 0): 41 itens **não-codificados** (sem `coded_by`, regime PENDENTE). Excluídos de análise quantitativa por definição (DIALETICA v2).
- Sobreposição = **0**. União removida = 68.

## 2. Mapa de fonte-da-verdade
| Store | N | Modelo | Chave | Papel |
|---|---|---|---|---|
| `data/processed/records.jsonl` | 265 | master-record v1.0 (rico) | UUID `item_id` | **canônico operacional**; schema-valid 265/265 |
| `corpus/corpus-data.json` | 264 | export plano (web/dashboards) | `id` semântico | **derivado** de records.jsonl via `records_to_corpus.py` |
| `Other/corpus-data.json` | 165 | snapshot congelado v1.0 (2026-04-25) | `id` semântico | **Corpus v1.0 primário Cap.3** (NÃO apagar — protegido) |
| `companion-data.json` | 165 | metadados gerados | — | stale; regenerável via `sync_companion.py` |

## 3. Estratos canônicos por `coded_by` (sobre os 264)
| coded_by | n | estrato |
|---|---|---|
| iconocode-opus | 100 | E1 (núcleo) |
| vault-import | 58 | E2 (auditar) |
| **(ausente)** | **41** | **E0 — quarentena F2** |
| iconocode-opus-4.6-metadata-refined | 29 | E1 |
| migration | 19 | E2 |
| iconocode-opus-4.6-image | 16 | E1 |
| manual-entry | 1 | E2 |

`endurecimento_score=0` é **score válido** (corpo vivo/baixa purificação), não ausência.

## 4. N analíticos resultantes
- **265** = ledger canônico (master). Nunca foi N analítico válido (inclui 41 não-codificados).
- **264** = export atual.
- **196** = após AMBOS os filtros (264 − 27 escopo − 41 não-cod).
  - **Estrato 1 (IconoCode) = 118** (opus 74 + opus-4.6-refined 28 + opus-4.6-image 16) — núcleo rigoroso, **pende confiabilidade inter-instrumento** (opus vs opus-4.6).
  - **Estrato 2 (import/migration/manual) = 78** — pende auditoria de proveniência.
- Mapeamento ao doc: N≈145 (IconoCode, pré-filtro-escopo) → **118 pós-escopo**; N≈223 (todos codificados) → **196 pós-escopo**.

## 5. Conjuntos exatos (preservados, não mutam o canônico)
- `corpus/quarantine/fora-do-escopo-2026-06-19.json` — 27 registros (Filtro 1).
- `corpus/quarantine/nao-codificado-2026-06-19.json` — 41 registros (Filtro 2).

## 6. ⚠️ Achado de implementação (por que a quarentena ainda NÃO é durável)
`corpus-data.json` é **export derivado** de `records.jsonl` via `records_to_corpus.py`. Editar o export diretamente é **efêmero** — foi regenerado de volta a 265 durante esta sessão.
- Quarentena durável exige mudança no **pipeline** (filtro em `records_to_corpus.py` por `fora-do-escopo` / `coded_by` vazio) **+ atualização do check de paridade do CI** (`validate.yml` valida master↔export 1:1; filtrar quebra isso) **+ `tests/test_corpus_export_idempotent.py`**.
- **NÃO usar `records_to_corpus.py --replace`** — descobri que ele gera export quebrado: **remove os campos `id`, `country`, `support`** de todos os registros. O export original vem de lógica diferente/mais nova.

## 7. Próximos passos (durável — sessão dedicada, com Ana)
1. Desenhar mecanismo de exclusão no pipeline (campo `quarantine`/`escopo` no master, ou filtro no export) que sobreviva à regeneração.
2. Atualizar check de paridade do CI para refletir corpus-quarentenado vs ledger-completo.
3. Confiabilidade inter-instrumento (opus vs opus-4.6) nos 10 indicadores → fixa Estrato 1.
4. Auditar Estrato 2 (import/migration) → decide inclusão → fixa N≈118 ou N≈196.
5. Dataset card no Cap.2: substituir "N=165" por estrutura de versões + proveniência por instrumento.
