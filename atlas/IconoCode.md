---
title: IconoCode
aliases:
  - Icono Code
  - ICONOCODE
type: kg/pipeline
tags:
  - kg
  - projeto/iconocracia
  - pipeline
  - metodo/quantitativo
related:
  - "[[Pipeline Dual-Agente — MOC]]"
  - "[[WebScout]]"
  - "[[Endurecimento]]"
  - "[[Regimes Iconocráticos]]"
  - "[[Esquemas JSON]]"
sources:
  - ../CLAUDE.md
  - ../tools/schemas/iconocode-output.schema.json
  - ../tools/schemas/purification-record.schema.json
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# IconoCode

Segundo agente do [[Pipeline Dual-Agente — MOC|pipeline]]: **análise visual** dos
candidatos vindos do [[WebScout]].

## O que produz

1. **Análise de Panofsky em 3 níveis** — pré-iconográfico → iconográfico →
   iconológico.
2. **10 indicadores de [[Endurecimento]]** (escala ordinal 0–3) → posiciona a
   imagem num [[Regimes Iconocráticos|regime]].

## Contrato de dados

- **Saída:** [`iconocode-output.schema.json`](../tools/schemas/iconocode-output.schema.json)
- **Codificação de purificação:** [`purification-record.schema.json`](../tools/schemas/purification-record.schema.json)
- O bloco `iconocode` é um dos campos obrigatórios do **master record** — ver
  [[Esquemas JSON]] e [[Hierarquia de Dados — MOC]].

## Modo ICONOCODE (agente)

Triggers: `codificar`, `iconocode`, `analisar imagem`, ou ao receber uma imagem.
Codificação de lote/status via:

```bash
python tools/scripts/code_purification.py --status
```

> [!question] Confiabilidade inter-instrumento
> O corpus foi codificado por **6 instrumentos** (`coded_by`); a auditoria de
> confiabilidade entre `iconocode-opus` e `opus-4.6` está pendente e condiciona o
> N analítico. Ver [[ADRs e Decisões — MOC]] e
> [IRR-PILOTO](../docs/decisions/IRR-PILOTO-2026-05-30.md).
