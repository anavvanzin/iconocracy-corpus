---
date: {{date:YYYY-MM-DD}}
routine: R4
type: writing
duration_min: 60
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
critical_path: true
tags: [rotina/R4, diario, escrita]
---

# R4 — Escrita 500 palavras · {{date:YYYY-MM-DD}}

> 60 min. Meta minima: 500 palavras liquidas em UM `cap-N/§M`. Caminho critico por padrao.
> Voz juridico-penal. ABNT NBR 6023:2025. Terminologia mandatoria (ver hub CLAUDE.md).

## Alvo

- Capitulo/§: `cap-N/§M`
- Arquivo: `vault/tese/capitulo-N.md` heading `§M ...`
- Argumento do bloco (1 frase):
- Conecta com hipotese: `H-0X`

## Rascunho

<!-- escreva livre; ao final, mover para o arquivo do capitulo -->

## Controle

- Palavras antes:
- Palavras depois:
- **Delta**: ___ (preencher em `emits.writing_words`)

## Proxima acao

- [ ] Mover prosa para `vault/tese/capitulo-N.md`
- [ ] Preencher `advances: [cap-N/§M]` + `emits.writing_words: <delta>`
- [ ] Se bloqueou -> criar `Q-NNN` em `vault/meta/perguntas-abertas.md` e registrar em `emits.questions`
- [ ] Se decidiu algo metodologico -> `vault/meta/decisoes/` + `emits.decisions`

## Bloqueios do dia
