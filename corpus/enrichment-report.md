# Relatório de regeneração — corpus-data-enriched.json

**Data**: 2026-09-19
**Fonte autoritativa**: `corpus/corpus-data.json` (336 itens)
**Enriched anterior**: 335 itens (335 overlays legados preservados)
**Saída**: `corpus/corpus-data-enriched.json` (336 itens, ordenados por país + id)

## Órfãos do enriched anterior (revisão necessária)

Presentes no enriched antigo, **ausentes do ledger** — excluídos da regeneração:


## Distribuição por regime

| Regime | Itens |
|--------|-------|
| FUNDACIONAL | 164 |
| NORMATIVO | 103 |
| MILITAR | 54 |
| CONTRA-ALEGORIA | 15 |

## Distribuição por país

| País (ledger) | Itens |
|---------------|-------|
| France | 102 |
| Brazil | 72 |
| United States | 32 |
| Germany | 27 |
| United Kingdom | 23 |
| Italy | 20 |
| Belgium | 11 |
| Portugal | 11 |
| Netherlands | 10 |
| Spain | 10 |
| Austria | 4 |
| CL | 3 |
| Denmark | 3 |
| Mexico | 3 |
| Argentina | 1 |
| France (held in Austria) | 1 |
| Germany (Netherlands origin) | 1 |
| Switzerland | 1 |
| Uruguay | 1 |

## Qualidade e lacunas

- Itens com `regime_incerto` (classificador diverge do ledger): **1**
- Itens sem `date` no ledger (emitidos com `date: ""`): **22**
- Itens sem `support` útil (None/'?'): **83**
- Itens legados cujo regime mudou em relação ao enriched antigo (ledger vence, justificativa regenerada): **0**
- Valores de `support` em texto livre sem mapeamento canônico: **0**

### Cobertura de campos

| Campo | Itens preenchidos |
|-------|-------------------|
| creator | 91/336 |
| institution | 91/336 |
| source_archive | 91/336 |
| medium | 286/336 |
| medium_norm | 281/336 |
| period | 312/336 |
| rights | 86/336 |
| thumbnail_url | 38/336 |
| url_iiif | 42/336 |
| url_image_download | 81/336 |
| iiif_source | 91/336 |
| iiif_note | 74/336 |
| local_image_path | 78/336 |
| citation_chicago | 86/336 |
| citation_abnt | 336/336 |
| year | 295/336 |

## Anomalias do ledger

- **161 itens com `endurecimento_score` > 1.0** (máx. 3.0). A escala real parece ser 0–3 (média dos 10 indicadores, cada um 0–3), não 0–1. O schema externo exige máximo 1 — esses itens falham na validação de intervalo (classe conhecida). Recomendado: normalizar dividindo por 3 ou revisar o schema.
- 22 itens sem `date` (ano derivado null).
- `country` usa variantes com parênteses ('Germany (Netherlands origin)', 'France (held in Austria)') e o código 'CL' em vez de 'Chile' — `country_pt` foi derivado do país-base.

## Lacunas conhecidas dos 244 itens novos

Nulos até uma futura passada de rede/IIIF: `iiif_source`, `iiif_note`, `url_iiif`, `url_image_download`, `thumbnail_url`, `rights`, `creator`, `institution`, `source_archive`, `citation_chicago`. `period_norm` também é null para itens novos (ver docstring de `derive_period` no script). `local_image_path` é null para todos: `corpus/imagens/` não existe nesta máquina.

## Follow-up

- **Não sincronizado**: `/Users/ana/Research/imagens/site/data/corpus-data-enriched.json` (cópia do site) — atualizar em passo separado, fora deste repositório.
- Decidir o destino dos 4 órfãos (reimportar ao ledger ou aposentar).
- Revisar itens com `regime_incerto` listados abaixo.

### Itens com regime_incerto (ledger ≠ classificador)

- 324a90b6-403b-5b36-9bcf-d4c4db9efdc1: ledger=FUNDACIONAL, classificador=NORMATIVO
