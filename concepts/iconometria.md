---
title: Iconometria
created: 2024-05-15
updated: 2026-07-11
type: concept
tags: [methodology, quantitative-analysis, iconography, data-analysis]
sources: [raw/articles/iconocracia-companion-web.md]
decision: docs/decisions/ICONOMETRIA-TRANSITION-2026-07-11.md
---

# Iconometria

**Iconometria** é o framework metodológico guarda-chuva da tese ICONOCRACIA: a
**medição e análise de padrões iconográficos** num corpus de alegorias femininas
da cultura jurídica (séc. XIX–XX). É uma abordagem quantitativa da imagem —
contagem e análise sistemática de elementos iconográficos para identificar
tendências, agrupamentos e significância estatística —, articulada à leitura
qualitativa (Panofsky, Warburg) e à genealogia jurídica.

## Relação com endurecimento

A iconometria **contém** o endurecimento como **um de seus eixos**, não o
substitui:

> **iconometria ⊇ endurecimento.** A iconometria é o *método de medição*; o
> endurecimento é *o que se mede no eixo da fixidez alegórica*.

- **Endurecimento** — eixo de **fixidez/purificação**: operacionalização empírica
  da **Purificação Clássica** (conceito autoral #4) por meio de **10 indicadores
  ordinais (0–3)**: desincorporação · rigidez_postural · dessexualização ·
  uniformização_facial · heraldicização · enquadramento_arquitetônico ·
  apagamento_narrativo · monocromatização · serialidade · inscrição_estatal.
- A iconometria abre espaço para outros vetores mensuráveis sob o mesmo aparato
  (p.ex. seriação, vetor colonial, densidade narrativa), sem que cada um colapse
  no escore único de fixidez.

> [!note] Estabilidade de dados
> O campo canônico permanece **`endurecimento_score`** (`records.jsonl`,
> `purification.jsonl`, `corpus-data.json`, CSV, schemas). A promoção de
> "iconometria" a guarda-chuva é conceitual; **não** renomeia a chave de dados.
> Ver plano faseado em [`docs/decisions/ICONOMETRIA-TRANSITION-2026-07-11.md`](../docs/decisions/ICONOMETRIA-TRANSITION-2026-07-11.md).

## Conceitos relacionados

- [[Iconocracia]]
- [[Purificação Clássica]] — matriz teórica do eixo endurecimento
- [[Methodology]]
- [[Quantitative Analysis]]
- [[Corpus]]
