---
title: Manuscrito — MOC
aliases:
  - MOC Manuscrito
  - Capítulos
type: kg/manuscrito
tags:
  - kg
  - projeto/iconocracia
  - meta/moc
  - manuscrito
related:
  - "[[Iconocracia — Mapa Central]]"
  - "[[Conceitos — MOC]]"
  - "[[ADRs e Decisões — MOC]]"
sources:
  - ../tese/manuscrito/sumario_iconocracia.md
  - ../tese/manuscrito/LEIAME.md
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# Manuscrito — MOC

Os capítulos em [`../tese/manuscrito/`](../tese/manuscrito/) e onde cada
[[Conceitos — MOC|conceito]] é desenvolvido. Compilação via Pandoc:
`make -C tese/manuscrito/ docx`.

| Peça | Arquivo | Conceitos centrais |
| --- | --- | --- |
| Introdução | [`Introducao_rev.md`](../tese/manuscrito/Introducao_rev.md) | tese geral; N analítico |
| Cap. 1 | [`Capitulo1_rev.md`](../tese/manuscrito/Capitulo1_rev.md) | [[Contrato Sexual Visual]] · [[Feminilidade de Estado]] |
| Cap. 2 — Metodologia | [`Capitulo2_metodologia.md`](../tese/manuscrito/Capitulo2_metodologia.md) | [[Esquemas JSON]] · dataset card · N |
| Cap. 3 — Análise quantitativa | [`Capitulo3_analise_quantitativa.md`](../tese/manuscrito/Capitulo3_analise_quantitativa.md) | [[Endurecimento]] · [[Contrato Racial Visual]] |
| Conclusão | _(ainda não no manuscrito)_ | síntese |
| Sumário | [`sumario_iconocracia.md`](../tese/manuscrito/sumario_iconocracia.md) | — |

> [!warning] Arquivos protegidos
> Os `*_original` (ex.: `Capitulo1_original_v2.md`, `Introducao_original_v2.md`)
> são **protegidos** por hook PreToolUse. Revisar em `tese/manuscrito/drafts/`.

## Pendências de redação ligadas ao dado

> [!todo] N=165 ainda no texto
> Cap. 2 (`:66,161`) e Introdução (`:127,193`) afirmam **N=165**, enquanto o
> corpus cresceu além disso. A substituição por "N=[válido]" depende de
> [[ADRs e Decisões — MOC|resolver o N analítico]]. Contagens atuais e o item 3 em
> [`../CLAUDE.md`](../CLAUDE.md) §*Known Data Issues*.

## Antes de commitar capítulos

- ABNT NBR 6023:2025 — rodar verificação (`/abnt-checker`, `/chapter-integrity`).
- Terminologia obrigatória — ver [[Conceitos — MOC]] e
  `python tools/scripts/check_thesis_terms.py`.
