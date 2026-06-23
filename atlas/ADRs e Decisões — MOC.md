---
title: ADRs e Decisões — MOC
aliases:
  - MOC Decisões
  - ADRs
type: kg/decisao
tags:
  - kg
  - projeto/iconocracia
  - meta/moc
  - arquitetura
related:
  - "[[Iconocracia — Mapa Central]]"
  - "[[Hierarquia de Dados — MOC]]"
  - "[[Endurecimento]]"
sources:
  - ../docs/adr/003-jsonl-as-canonical.md
  - ../docs/decisions/DIALETICA-N165-vs-265.md
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# ADRs e Decisões — MOC

As decisões de arquitetura (ADRs) e as decisões **metodológicas** que governam o
corpus.

## Architecture Decision Records

| ADR | Decisão | Liga a |
| --- | --- | --- |
| [ADR-001](../docs/adr/001-drive-as-raw-store.md) | Google Drive como armazenamento de dados brutos | [[Hierarquia de Dados — MOC]] |
| [ADR-002](../docs/adr/002-notion-as-index.md) | Notion como índice catalográfico *(substituído)* | → ADR-004 |
| [ADR-003](../docs/adr/003-jsonl-as-canonical.md) | **JSONL como formato canônico** de registros | [[Hierarquia de Dados — MOC]] |
| [ADR-004](../docs/adr/004-vault-as-index.md) | Vault Obsidian como espelho catalográfico (substitui Notion) | [[WebScout]] |
| [ADR-005](../docs/adr/005-github-and-hf-release-surfaces.md) | GitHub como backbone canônico · Hugging Face como superfície pública | release |

> [!note] ADRs presentes
> O repositório traz **ADR-001 a 005**. A **política de cobertura parcial de
> purificação** vive no dossiê de decisões abaixo (não há ADR dedicado a ela).

## Decisão metodológica em aberto — o N analítico

> [!question] DECISÃO PENDENTE (Ana)
> Qual é o **N analítico válido**? O enquadramento "165 vs 265" foi **rejeitado**
> por revisão adversarial. O eixo real é **estrato de validade de codificação ×
> proveniência de instrumento**, não data.

- **Corpus bruto (todos os itens)** → NÃO é um N analítico válido: inclui itens sem `regime` (não codificados).
- **Estrato IconoCode** → apenas itens codificados pelo instrumento IconoCode.
- **Todos os codificados** → após auditoria de confiabilidade inter-instrumento.

> Os tamanhos de cada estrato variam a cada auditoria — ver [`../CLAUDE.md`](../CLAUDE.md) §*Known Data Issues*.

Dossiê de decisão:

- [DIALÉTICA N=165 vs 265](../docs/decisions/DIALETICA-N165-vs-265.md) — o framing rejeitado e o reenquadramento
- [Estratificação + quarentena (2026-05-30)](../docs/decisions/ESTRATIFICACAO-2026-05-30.md)
- [IRR piloto inter-instrumento (2026-05-30)](../docs/decisions/IRR-PILOTO-2026-05-30.md)
- [Status consolidado (2026-05-30)](../docs/decisions/STATUS-2026-05-30.md)

> [!warning] Fora de escopo deste grafo
> Resolver o N analítico é trabalho metodológico em andamento. Este nó **mapeia**
> a decisão; não a antecipa. Ver [[Manuscrito — MOC]] (Cap. 2 substituirá
> "N=165" por "N=[válido]").
