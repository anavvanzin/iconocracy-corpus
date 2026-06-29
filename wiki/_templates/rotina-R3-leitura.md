---
date: {{date:YYYY-MM-DD}}
routine: R3
type: reading
duration_min: 45
budget_min: 90
advances: []
entities_touched:
  corpus: []
  readings: []
  iconclass: []
emits:
  decisions: []
  questions: []
  writing_words: 0
critical_path: false
tags: [rotina/R3, diario, leitura]
---

# R3 — Leitura + fichamento · {{date:YYYY-MM-DD}}

> 45 min. 1 texto, 1 capitulo-destino. Extrair: tese, evidencia, citacao literal ABNT, contra-ponto.

## Leitura

- Ref (ABNT NBR 6023:2025):
- Paginas lidas:
- Capitulo-destino: `cap-N/§M`
- `reading_id` (autor-ano-slug):

## Tese do autor (1 paragrafo)

## Evidencia / exemplo forte

## Citacao literal (com pagina)

> "..."
> (AUTOR, ano, p. XX)

## Como entra na tese

- Posicao: corrobora / tensiona / contradiz
- Hipotese tocada: `H-01` / `H-02` / `H-03`
- Bloco de redacao alvo: [[capitulo-N#§M]]

## Contra-ponto

## Proxima acao

- [ ] Preencher `advances: [cap-N/§M]` + `entities_touched.readings: [autor-ano-slug]`
- [ ] Se citacao entra em R4 amanha -> marcar em `emits.decisions`
