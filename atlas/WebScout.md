---
title: WebScout
aliases:
  - Web Scout
  - SCOUT
type: kg/pipeline
tags:
  - kg
  - projeto/iconocracia
  - pipeline
  - "#corpus"
related:
  - "[[Pipeline Dual-Agente — MOC]]"
  - "[[IconoCode]]"
  - "[[Esquemas JSON]]"
  - "[[Parâmetros do Corpus]]"
sources:
  - ../CLAUDE.md
  - ../tools/schemas/webscout-input.schema.json
  - ../tools/schemas/webscout-output.schema.json
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# WebScout

Primeiro agente do [[Pipeline Dual-Agente — MOC|pipeline dual-agente]]:
**descoberta** de imagens candidatas em arquivos digitais.

## Arquivos consultados

Europeana · Gallica · LOC · BnF · Numista · Colnect.

## Contrato de dados

- **Entrada:** [`webscout-input.schema.json`](../tools/schemas/webscout-input.schema.json)
- **Saída:** [`webscout-output.schema.json`](../tools/schemas/webscout-output.schema.json)
- Ver [[Esquemas JSON]] para o conjunto completo.

## Modo SCOUT (agente)

Triggers: `scout [query]`, `campanha N`, `buscar`, `lacunas`, `auditoria`.
Gera notas Obsidian em `vault/candidatos/` (padrão `XX-NNN Título.md`) e roda
análise de lacunas. Filtra pelos [[Parâmetros do Corpus|critérios de inclusão]].

> [!note] Resiliência de arquivo
> Falhas de arquivo (ex.: Gallica 429, Europeana timeout) acionam a rotina de
> *fallback* (IIIF → retries → Playwright → registro metadata-only com
> `#imagem-pendente`).

## Próxima etapa

→ [[IconoCode]] (análise visual dos candidatos descobertos).
