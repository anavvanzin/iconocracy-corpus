# Audit Toolkit — ICONOCRACIA

> Conjunto consolidado de scripts, dados, relatórios, taxonomia, diagramas e templates produzidos entre 25 mar. — 19 jun. 2026 para o pipeline de codificação iconográfica da tese **"Iconocracia: Alegoria Feminina na História da Cultura Jurídica (séculos XIX–XX)"** (PPGD/UFSC).
>
> Cada artefato abaixo é linkável diretamente nos cards do site de visualização da trajetória (`trajetoria-visualizada`).

**Base URL para uso em links:**

```
https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/
```

Para download bruto (PDF/XLSX/JSON), substitua `/blob/main/` por `/raw/main/`.

---

## Estrutura

```
tools/audit/
├── scripts/      → Python (analisadores de fios e taxonomia)
├── data/         → JSONs gerados pela análise
├── heatmaps/     → XLSX da auditoria Panofsky
├── reports/      → Relatórios markdown (auditorias, revisões)
├── taxonomy/     → Schema e guia de mapeamento da taxonomia
├── thread-analyzer/ → Toolkit standalone do analisador v1
├── mnemosyne/    → Templates e protocolo das 80 fios
└── diagrams/     → Diagramas visuais (PDF + SVG editáveis)
```

---

## 1. Scripts Python (`scripts/`)

| Arquivo | Versão | Descrição | Link |
| --- | --- | --- | --- |
| `analyze_threads.py` | v0.1 | Classificador inicial. Aceita fios binários (origem → destino), atribui ao tipo da taxonomia v0.1 (5 famílias × 15 tipos) via árvore de decisão. Gera relatório markdown + JSON estruturado + SVG de rede. | [scripts/analyze_threads.py](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/scripts/analyze_threads.py) |
| `analyze_threads_v2.py` | v0.2 | Classificador completo. Suporta **CHAIN ternário** (≥ 3 itens), **multi-tipo** como norma (até 3 relações ordenadas por fio), os **9 sub-tipos novos** (Genealogia canônica/tensional/ascendente, Translatio republicana/imperial/fundacional, Inversão sincrônica/diacrônica, Contradição intra/transnacional/colonial), os **5 flags** (institutional_transmission, colonial_register, diachronic, internal_to_country, cross_regime) e a regra de **inflexão militar** (cadeias monótonas até regime militar podem cair sem invalidar). | [scripts/analyze_threads_v2.py](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/scripts/analyze_threads_v2.py) |

---

## 2. Auditorias e Heatmaps (`heatmaps/`)

| Arquivo | Tipo | Descrição | Link |
| --- | --- | --- | --- |
| `panofsky-heatmap-309entries.xlsx` | XLSX (6 sheets) | Auditoria completa do corpus em 309 entradas. Sheets: (1) Visão geral, (2) Matriz país × regime × década, (3) Cobertura Panofsky por entrada, (4) Flags P1–P5 com priorização, (5) Lacunas regionais, (6) Lista de ações. Apenas 49,5% das entradas têm objeto Panofsky; só 2,6% estão integralmente codificadas; 141 entradas usam tag de uma palavra em `iconological.regime`. | [heatmaps/panofsky-heatmap-309entries.xlsx](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/heatmaps/panofsky-heatmap-309entries.xlsx) — [download direto](https://github.com/anavvanzin/iconocracy-corpus/raw/main/tools/audit/heatmaps/panofsky-heatmap-309entries.xlsx) |

---

## 3. Dados de saída (`data/`)

| Arquivo | Origem | Descrição | Link |
| --- | --- | --- | --- |
| `french-revolutionary-audit.json` | manual + análise | Auditoria das 34 entradas francesas do corpus revolucionário. 24 sem codificação Panofsky; FR-012/FR-021 identificadas como duplicata Delacroix. Estrutura `{ entry_id, gap_level, missing_fields, recommendation }`. | [data/french-revolutionary-audit.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/data/french-revolutionary-audit.json) |
| `iconocracy-flags-263actions.json` | derivado do heatmap | 263 ações de codificação priorizadas (P1 crítico → P5 nice-to-have) para fechar o débito técnico Panofsky. Cada item tem `entry_id`, `priority`, `action_type`, `expected_effort`. | [data/iconocracy-flags-263actions.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/data/iconocracy-flags-263actions.json) |
| `thread-analysis-v1-output.json` | `analyze_threads.py` | Saída estruturada do analisador v0.1 sobre conjunto demo. Para validação histórica. | [data/thread-analysis-v1-output.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/data/thread-analysis-v1-output.json) |
| `thread-analysis-v2-output.json` | `analyze_threads_v2.py` | Saída do analisador v0.2 sobre os mesmos fios após reestruturação. Inclui campo `chain` populado e `flags[]`. | [data/thread-analysis-v2-output.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/data/thread-analysis-v2-output.json) |

---

## 4. Relatórios (`reports/`)

| Arquivo | Tipo | Descrição | Link |
| --- | --- | --- | --- |
| `french-panofsky-audit.md` | Auditoria | Relatório das 24 entradas francesas sem codificação Panofsky completa. Diagnóstico do que falta em cada campo (pré-iconográfico, iconográfico, iconológico). Identifica FR-021 como duplicata canônica de FR-012. | [reports/french-panofsky-audit.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/french-panofsky-audit.md) |
| `mini-validation-3panels.md` | Validação | Stress-test da taxonomia v0.1 em 30 fios distribuídos entre 3 painéis de alto risco (ENDURECIMENTO, Balança e Império, Fissuras). Concordância manual ↔ analyzer: **50%**. Documenta 10 falhas estruturais que motivaram os 10 ajustes da v0.2. | [reports/mini-validation-3panels.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/mini-validation-3panels.md) |
| `systematic-review-conversation.md` | Revisão sistemática | Revisão PRISMA-adaptada da conversa de produção. Identifica os 22 artefatos produzidos e classifica em 3 níveis de débito técnico (A/B/C). Base para o plano de qualificação. | [reports/systematic-review-conversation.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/systematic-review-conversation.md) |
| `chain-analysis-v2.md` | Análise CHAIN | Discussão da nova relação ternária introduzida na v0.2. Critérios formais para reconhecer ENDURECIMENTO PROGRESSIVO, ENDURECIMENTO TRANSNACIONAL e CONSTELAÇÃO TEMPORAL. | [reports/chain-analysis-v2.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/chain-analysis-v2.md) |
| `thread-analysis-v1-report.md` | Relatório analyzer | Relatório legível produzido por `analyze_threads.py` sobre dataset demo. | [reports/thread-analysis-v1-report.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/thread-analysis-v1-report.md) |
| `thread-analysis-v2-report.md` | Relatório analyzer | Equivalente para v0.2. Mostra distribuição multi-tipo, flags ativados, CHAINs detectados. | [reports/thread-analysis-v2-report.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/reports/thread-analysis-v2-report.md) |

---

## 5. Taxonomia (`taxonomy/`)

| Arquivo | Versão | Descrição | Link |
| --- | --- | --- | --- |
| `taxonomy-v0.1.md` | v0.1 | Documento metodológico original: 5 famílias (Genealógicas, Estruturais, Tensionais, Transicionais, Sincrônicas) × 15 tipos. Árvore de decisão para classificação. Regimes esperados por tipo. 18 kb de prosa. | [taxonomy/taxonomy-v0.1.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/taxonomy/taxonomy-v0.1.md) |
| `taxonomy-v0.2-schema.json` | v0.2 | Schema autoritativo da versão atual: 5 famílias, 15 tipos base, 9 sub-tipos, 3 chains, 5 flags. JSON estruturado consumível por scripts e templates. | [taxonomy/taxonomy-v0.2-schema.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/taxonomy/taxonomy-v0.2-schema.json) |
| `data-mapping-guide-v0.2.md` | v0.2 | Guia operacional do mapeamento da taxonomia v0.2 sobre dados existentes. Explica como migrar fios v0.1 → v0.2, quando ativar flags, como reconhecer CHAINs. | [taxonomy/data-mapping-guide-v0.2.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/taxonomy/data-mapping-guide-v0.2.md) |

---

## 6. Thread Analyzer toolkit (`thread-analyzer/`)

| Arquivo | Descrição | Link |
| --- | --- | --- |
| `README.md` | Documentação do toolkit standalone — instalação, uso, formato de entrada. | [thread-analyzer/README.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/thread-analyzer/README.md) |
| `thread-graph.svg` | Visualização de rede produzida pelo analisador (demo). Pode ser editado no Inkscape. | [thread-analyzer/thread-graph.svg](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/thread-analyzer/thread-graph.svg) |

---

## 7. Mnemosyne — sessão de 80 fios (`mnemosyne/`)

| Arquivo | Descrição | Link |
| --- | --- | --- |
| `protocol.md` | Protocolo operacional da sessão de validação: 10 fios por painel × 8 painéis + ≥ 3 cadeias CHAIN. Critérios de seleção, ordem, tempo estimado. | [mnemosyne/protocol.md](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/mnemosyne/protocol.md) |
| `template-v0.1.xlsx` | Template original (XLSX, 10 sheets). Aceita só fios binários. | [mnemosyne/template-v0.1.xlsx](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/mnemosyne/template-v0.1.xlsx) — [download](https://github.com/anavvanzin/iconocracy-corpus/raw/main/tools/audit/mnemosyne/template-v0.1.xlsx) |
| `template-v0.2.xlsx` | Template revisado (XLSX, 11 sheets). Inclui sheet de CHAINs, colunas multi-tipo, flags. **Versão a ser usada na sessão completa.** | [mnemosyne/template-v0.2.xlsx](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/mnemosyne/template-v0.2.xlsx) — [download](https://github.com/anavvanzin/iconocracy-corpus/raw/main/tools/audit/mnemosyne/template-v0.2.xlsx) |
| `starter-8panels.json` | 8 painéis pré-semeados com 10 placements cada, prontos para importar no Warburg Atlas. | [mnemosyne/starter-8panels.json](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/mnemosyne/starter-8panels.json) |

---

## 8. Diagramas visuais (`diagrams/`)

| Arquivo | Formato | Uso | Link |
| --- | --- | --- | --- |
| `taxonomy-landscape-A3.pdf` / `.svg` | PDF + SVG | Diagrama paisagem A3 — 5 famílias × 15 tipos em 5 bandas horizontais. Para impressão e apresentação. | [PDF](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-landscape-A3.pdf) · [SVG](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-landscape-A3.svg) |
| `taxonomy-portrait-A4.pdf` / `.svg` | PDF + SVG | Versão retrato A4 — para inserir como figura na tese. | [PDF](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-portrait-A4.pdf) · [SVG](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-portrait-A4.svg) |
| `taxonomy-banca-poster.pdf` / `.svg` / `.png` | PDF + SVG + PNG | Pôster 16:9 otimizado para projeção 3 m da qualificação. Branding UFSC/PPGD/Ius Gentium. | [PDF](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-banca-poster.pdf) · [SVG](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/diagrams/taxonomy-banca-poster.svg) · [PNG hi-res](https://github.com/anavvanzin/iconocracy-corpus/raw/main/tools/audit/diagrams/taxonomy-banca-poster.png) |

---

## Tabela de mapeamento — cards do site → artefatos no repo

Esta tabela é o **ponto de entrada para linkar o site de visualização**. Cada linha corresponde a um card (`art-id`) na seção "22 artefatos produzidos" do site `trajetoria-visualizada`.

| Card | Título no site | Artefato no repo | URL |
| --- | --- | --- | --- |
| **B3** | Iconocracy flags JSON | `data/iconocracy-flags-263actions.json` | `tools/audit/data/iconocracy-flags-263actions.json` |
| **B4** | Mnemosyne starter JSON | `mnemosyne/starter-8panels.json` | `tools/audit/mnemosyne/starter-8panels.json` |
| **B5** | Taxonomy v0.2 schema | `taxonomy/taxonomy-v0.2-schema.json` | `tools/audit/taxonomy/taxonomy-v0.2-schema.json` |
| **C1** | French Panofsky audit | `reports/french-panofsky-audit.md` + `data/french-revolutionary-audit.json` | `tools/audit/reports/french-panofsky-audit.md` |
| **C2** | Heatmap completo XLSX | `heatmaps/panofsky-heatmap-309entries.xlsx` | `tools/audit/heatmaps/panofsky-heatmap-309entries.xlsx` |
| **C3** | Mini-validação 30 fios | `reports/mini-validation-3panels.md` | `tools/audit/reports/mini-validation-3panels.md` |
| **D1** | Taxonomia v0.1 (markdown) | `taxonomy/taxonomy-v0.1.md` | `tools/audit/taxonomy/taxonomy-v0.1.md` |
| **E1** | Taxonomia paisagem A3 | `diagrams/taxonomy-landscape-A3.{pdf,svg}` | `tools/audit/diagrams/taxonomy-landscape-A3.pdf` |
| **E2** | Taxonomia retrato A4 | `diagrams/taxonomy-portrait-A4.{pdf,svg}` | `tools/audit/diagrams/taxonomy-portrait-A4.pdf` |
| **E3** | Pôster banca 16:9 | `diagrams/taxonomy-banca-poster.{pdf,svg,png}` | `tools/audit/diagrams/taxonomy-banca-poster.pdf` |
| **E5** | Thread graph SVG | `thread-analyzer/thread-graph.svg` | `tools/audit/thread-analyzer/thread-graph.svg` |
| **F1** | analyze_threads.py (v1) | `scripts/analyze_threads.py` | `tools/audit/scripts/analyze_threads.py` |
| **F2** | analyze_threads_v2.py | `scripts/analyze_threads_v2.py` | `tools/audit/scripts/analyze_threads_v2.py` |
| **G4** | Mnemosyne template v0.2 | `mnemosyne/template-v0.2.xlsx` | `tools/audit/mnemosyne/template-v0.2.xlsx` |

---

## Convenção de URLs

Para uso direto no HTML do site:

```html
<!-- Para visualização no GitHub -->
<a href="https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/[caminho]">

<!-- Para download bruto (XLSX, PDF, JSON) -->
<a href="https://github.com/anavvanzin/iconocracy-corpus/raw/main/tools/audit/[caminho]">
```

---

## Próximas adições previstas

- `data/mnemosyne-session-2026-XX.json` — saída completa da sessão de 80 fios
- `reports/taxonomy-v1.0-finalization.md` — relatório da finalização da v1.0 após validação
- `heatmaps/panofsky-heatmap-post-recoding.xlsx` — segunda iteração da auditoria, após fechar débito Panofsky

---

**Mantenedora:** Ana Vanzin · PPGD/UFSC · `warholana@msn.com`
**Repositório principal:** [github.com/anavvanzin/iconocracy-corpus](https://github.com/anavvanzin/iconocracy-corpus)
**Site da trajetória:** ver `/computer/a/iconocracia-trajetoria` na sessão Perplexity
**Companion:** [iconocracia-companion.warholana.workers.dev](https://iconocracia-companion.warholana.workers.dev/)
**Atlas público:** [iconocracia-atlas](https://www.perplexity.ai/computer/a/iconocracia-atlas-7saKqNyZTLCkLkFNF.tbOw)

*Última atualização: 19 jun. 2026.*
