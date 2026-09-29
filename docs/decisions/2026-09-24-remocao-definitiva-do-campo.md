---
documento: decisao
id: DEC-2026-09-24-REMOCAO-CAMPO
data: "2026-09-24"
autor: Ana Vanzin
escopo: "remoção definitiva do campo endurecimento_score (exportador, dados, manuscrito, docs)"
completa: DEC-2026-07-28-COMPOSTO
status: vigente
licenca: CC-BY-4.0
---

# Remoção definitiva do campo `endurecimento_score`

## Decisão

A autora (Ana Vanzin) decidiu, em 2026-09-24, **remover completamente o campo
`endurecimento_score`** do exportador, dos dados canônicos, do manuscrito e da
documentação operacional. Esta decisão **completa** a aposentadoria
metodológica do índice composto registrada em
`docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md` e em
`corpus/docs/CHANGELOG-v2.md`: o conselho de três modelos recomendou a remoção
porque os valores (0,0 de importações vazias; 1,4 de fallback) eram artefatos
de pipeline, nunca medições. A remoção do campo de dados era o último passo
pendente — agora executado.

## Escopo executado

1. **Exportador** — `tools/scripts/records_to_corpus.py` não deriva nem emite
   mais `endurecimento_score` nem o bloco agregado `indicadores` na projeção
   pública (valores legados de um `corpus-data.json` pré-existente são
   descartados no merge). Tratamento equivalente nos demais geradores de
   exports públicos e consumidores: `iconocode_to_corpus.py`,
   `refresh_dashboard.py`, `regenerate_enriched.py`, `build_hf_release.py`,
   `ingest_research_candidates.py`, `purify-diff.py`,
   `corpus/infografico_corpus.py`, `iconocracy-ingest/modules/corpus_bridge.py`,
   `shared/types/corpus.ts`, `shared/services/corpus.ts`, `shared/index.ts`,
   `shared/corpus-parser.ts` — e nos testes correspondentes. O acessor legado
   `legacy_composite` de `tools/scripts/lpai_indicators.py` foi removido.
2. **Dados canônicos** — `tools/scripts/strip_endurecimento.py` (migração
   única) remove: `iconographic_metadata.endurecimento_score`;
   `endurecimento_score`/`indicadores`/`purificacao_composto` de nível
   superior; `purificacao.purificacao_composto` e
   `purificacao.record_metadata.endurecimento_score` em `records.jsonl`;
   `purificacao_composto` em `purification.jsonl`; e o parêntese mecânico
   `(endurecimento N.N)` em `claim_text`. Aplicado a
   `corpus/corpus-data.json`, `data/processed/records.jsonl` e
   `data/processed/purification.jsonl`.
3. **Manuscrito** — scaffolds de `tese/manuscrito/scaffolds/` que usavam o
   escore (`2026-09-22-cap6.md`, `2026-09-22-cap6-sec64.md`,
   `2026-09-24-cap6.md`) e o `Glossario.md`: cirurgia, não amputação. Os
   achados substantivos ("normativo supera fundacional", gradiente de
   suportes, variância colonial) foram preservados como observações a
   re-expressar, marcados com
   `[RECHECAGEM PENDENTE: re-expressar sobre indicadores ordinais]` onde o
   número era o argumento.
4. **Docs operacionais** — `AGENTS.md`, `CLAUDE.md`, `README.md`,
   `docs/CODEMAPS/data.md` e `concepts/iconometria.md` passam a declarar o
   campo como **removido** (apontando para esta decisão), em vez de "chave
   estável". Documentos históricos datados (`docs/decisions/**`,
   `corpus/docs/CHANGELOG-v2.md`, `archive/**`, `wiki/**`, `vault/**`,
   `notebooks/**`) permanecem como registro, no máximo com uma linha de
   atualização.

## O que permanece

- Os **10 indicadores ordinais (0–3)** e o **inventário verbal de atributos**
  (codificação vigente, qualitativa) em `purification.jsonl` e em
  `records.jsonl` (`purificacao.*`, exceto o composto removido).
- A palavra-conceito **"endurecimento"** na prosa interpretativa e teórica
  (eixo de fixidez da iconometria).
- O `regime_iconocratico` e demais campos qualitativos do codebook v2.3.0.

## O que esta decisão NÃO muda

- **Nada renomeia a iconometria**: o framework guarda-chuva segue intacto
  (`iconometria ⊇ endurecimento`, decisão 2026-07-11).
- A **lente qualitativa** segue: endurecimento continua sendo lido caso a
  caso, como inventário verbal — nunca somado.
- Nenhum documento histórico datado é reescrito.

## Execução técnica

Branch `chore/remove-endurecimento-score`. A migração de dados é reproduzível:
`python tools/scripts/strip_endurecimento.py` (idempotente: reexecutá-lo sobre
dados já limpos reporta 0 remoções e não altera nada).
