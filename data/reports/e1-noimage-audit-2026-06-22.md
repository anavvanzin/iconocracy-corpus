# Auditoria E1 — `#no-image` é placeholder, não "sem imagem"

**Data:** 2026-06-22 · **Branch:** `e1-opus48-batch-2026-06-22` · **Resolve:** o sinal amarelo levantado na revisão de sessão — 216/265 itens marcados `#no-image` no `pathosformel_index.jsonl`, contra os 79 não-imagens esperados pelo `plans/2026-06-05-june-plan.md`.

## Pergunta

Os 216 `#no-image` são genuinamente sem imagem (irrecuperáveis) ou backlog não-codificado nesta passagem? A distinção muda o que se pode afirmar em Cap.6 e o tamanho do backlog de julho.

## Método

Cruzamento de `data/processed/pathosformel_index.jsonl` (entradas `coded_by=="e1-no-image"`, N=216) com `corpus/corpus-data.json` (264 itens) pela chave `sigla_id` ↔ `id`. Para cada entrada `#no-image`, classifica-se conforme a `url` do item no corpus canônico:

| Categoria | Critério | N |
|---|---|---|
| Backlog — URL externa viva | `url` começa por `http` e host ≠ `iconocracy.corpus` | **201** |
| Backlog — local esperado | `url` é `iconocracy.corpus/vault/<uuid>` | **9** |
| Genuinamente sem imagem | `url` vazia e `thumbnail_url` vazia | **6** |
| | subtotal backlog (→ `e1-uncoded`) | **210** |
| | subtotal irrecuperável (→ `e1-no-image`) | **6** |

Classificação executada por `tools/scripts/e1_reclassify_no_image.py` (idempotente, reproduzível).

## Achado central

**O `#no-image` é uma convenção de bookkeeping, não uma alegação empírica.** O gerador `tools/scripts/e1_mark_no_image.py` é explícito na sua docstring:

> *"Marca itens sem imagem acessível como #no-image no pathosformel_index.jsonl, completando o DoD E1 (265 linhas). Identifica itens que ainda não estão no pathosformel_index, e acrescenta entradas #no-image com indicadores nulos."*

Ou seja: o script varre `records.jsonl`, pega tudo o que não foi codificado nesta passagem, e marca `#no-image` + indicadores nulos — para fechar o DoD em 265 linhas. **`motivo_exclusao` ficou `null` nos 216** — nenhum regista o motivo. Isto viola o princípio Tier 2 (audit trail) estabelecido pela dialética `docs/decisions/dialectic-corpus-2026-06-19/`: o recode marcou `#no-image` sem deixar rasto do motivo.

## Hosts das 210 URLs vivas (top)

| Host | N | Nota |
|---|---|---|
| `gallica.bnf.fr` | 40 | IIIF manifest — fetch dedicado |
| `loc.gov` | 28 | API de imagens |
| `europeana.eu` | 23 | agregador, IIIF |
| `en.numista.com` | 22 | numismática (subset numismático) |
| `kk.haum-bs.de` | 12 | |
| `commons.wikimedia.org` | 10 | directo |
| `iconocracy.corpus/vault/*` | 9 | local esperado, ficheiro não encontrado |
| `rijksmuseum.nl` | 8 | |
| `collections.vam.ac.uk` | 7 | |
| `colnect.com` | 5 | numismática (selos) |
| `memoria.bn.br` | 5 | |
| `brasilianafotografica.bn.gov.br` | 4 | |

Os 6 genuinamente sem imagem: `FR-036`, `FR-038`, `FR-039`, `FR-040`, `FR-047`, `FR-048` (`url=∅`, `thumbnail_url=∅`).

## Reclassificação aplicada

Para alinhar o artefato com o princípio de auditabilidade da dialética, o `pathosformel_index.jsonl` foi reclassificado em três estados, povoando `motivo_exclusao`:

| `coded_by` | `coded_from` | N | `motivo_exclusao` |
|---|---|---|---|
| `fable-5` | `image` / `image_direct` | 44 | (codificação real, in-scope) |
| `fable-5` | (fora_escopo) | 5 | (motivo já documentado) |
| `e1-uncoded` | `backlog` | **210** | `Backlog — URL viva/local esperado, não codificado nesta passagem (re-aquisição julho/2026)` |
| `e1-no-image` | `no_image` | **6** | `Sem URL/fonte de imagem — irrecuperável` |

Total: 44 + 5 + 210 + 6 = **265** ✓

`★ Nota de design` — mantém-se `e1-no-image` apenas para os 6 irrecuperáveis reais (sem URL). O backlog (219) passa a `e1-uncoded`, distinguindo "não codificado" de "sem imagem". Isto torna o index honesto para a banca e torna o backlog de julho visível.

## Impacto no que se pode afirmar

- **Tier 1 (estatístico, single-instrument):** N=44 fable-5. Defensável, mas magro. A estatística de headline (regime/composto) reporta-se sobre 44, qualificada como "subconjunto com imagem codificada (n=44 do corpus de 265)."
- **O "265/265 processado" do DoD é real mas enganador:** 210 são placeholder `e1-uncoded`, não processamento. A meta de junho foi cumprida por convenção (DoD = 265 linhas), não por codificação.
- **Backlog de julho = 210 (não 79):** o june-plan estimava 79 não-imagens; na verdade são 210 itens com fonte recuperável (201 externa + 9 local) + 6 irrecuperáveis. O subset numismático (numista 22 + colnect 5 = 27) é parte do backlog.

## Segurança da mudança (consumidores)

`grep -rn "e1-no-image"` em `*.py/*.html/*.js` (fora de `archive/`): apenas o gerador `e1_mark_no_image.py:91` produz o literal. Nenhum consumidor (`refresh_dashboard.py`, `analyze_purification_drift.py`, `records_to_sqlite.py`, `compute_irr.py`) filtra pelo valor `e1-no-image` — todos usam `coded_by` como campo, não como token de filtro. Renomear para `e1-uncoded` é seguro.

## Próximos passos

1. **Julho — re-aquisição do backlog (210):** priorizar por host. Gallica/loc.gov/europeana têm APIs/IIIF dedicados (W1 do `Specs/WORKFLOW-iconocracy-corpus-acquisition.md`). Numismática (27) é subset separado.
2. **Krippendorff α** sobre os 44 single-instrument — número para a banca (`compute_irr.py`).
3. **Popular `motivo_exclusao` em código novo:** qualquer futuro `#no-image`/`#uncoded` deve trazer o motivo. Considerar adicionar check no `validate_schemas.py` ou num hook que rejeite `motivo_exclusao==null` quando `coded_by` ∈ {`e1-no-image`,`e1-uncoded`}.