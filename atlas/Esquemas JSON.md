---
title: Esquemas JSON
aliases:
  - Schemas
  - Esquemas
type: kg/esquema
tags:
  - kg
  - projeto/iconocracia
  - dados
  - validacao
related:
  - "[[Hierarquia de Dados — MOC]]"
  - "[[WebScout]]"
  - "[[IconoCode]]"
  - "[[Endurecimento]]"
sources:
  - ../tools/schemas/master-record.schema.json
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# Esquemas JSON

Os **7 esquemas** (JSON Schema 2020-12) em [`../tools/schemas/`](../tools/schemas/)
que validam todo o fluxo. Validador: `python tools/scripts/validate_schemas.py`.

| Esquema | Valida | Etapa |
| --- | --- | --- |
| [`master-record`](../tools/schemas/master-record.schema.json) | o registro canônico completo | saída do pipeline |
| [`webscout-input`](../tools/schemas/webscout-input.schema.json) | consulta de descoberta | [[WebScout]] |
| [`webscout-output`](../tools/schemas/webscout-output.schema.json) | candidatos descobertos | [[WebScout]] |
| [`iconocode-output`](../tools/schemas/iconocode-output.schema.json) | análise Panofsky + indicadores | [[IconoCode]] |
| [`purification-record`](../tools/schemas/purification-record.schema.json) | 1 registro de codificação 0–3 | [[Endurecimento]] |
| [`argos-manifest`](../tools/schemas/argos-manifest.schema.json) | manifesto de aquisição | ARGOS |
| [`research-cluster`](../tools/schemas/research-cluster.schema.json) | clusters temáticos (tópico × prompts × extração) | pesquisa |

## Anatomia do `master-record`

Campos **obrigatórios** (top-level):

```
master_record_version · batch_id · item_id · item_hash ·
input · webscout · iconocode · exports · timestamps
```

Campo opcional: `purificacao` (bloco de [[Endurecimento]]).

> [!note] O `master-record` é o nó-cola
> Ele embute a saída do [[WebScout]] (`webscout`), a do [[IconoCode]]
> (`iconocode`) e a codificação de [[Endurecimento]] (`purificacao`) — por isso é
> o topo da [[Hierarquia de Dados — MOC]].

## CI/CD

`.github/workflows/validate.yml` valida `records.jsonl` contra `master-record`,
checa consistência com `corpus-data.json` e **rejeita binários em `data/raw/`**
([ADR-001](../docs/adr/001-drive-as-raw-store.md)).
