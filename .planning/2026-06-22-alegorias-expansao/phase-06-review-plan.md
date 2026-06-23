---
phase: "06-revisao-subagentes"
plan: "06-01"
type: "review"
wave: 1
depends_on: ["05-wiki-pages"]
files_modified: [
  "docs/decisions/ALE-GORIAS-VIRTUDES-CONTINENTES-OCEANOS-2026-06-22.md",
  "docs/methodology/codebook-v2-alegorias.md",
  "data/processed/records.jsonl"
]
autonomous: true
must_haves:
  truths: [
    "Krippendorff's alpha >= 0.67 para codificação intercodificadores",
    "Nenhum registro duplicado em relação aos 265 originais"
  ]
  artifacts: [
    "docs/reviews/PHASE-06-ACADEMIC-REVIEW.md",
    "docs/reviews/PHASE-06-ANTHROPOLOGICAL-AUDIT.md",
    "docs/reviews/PHASE-06-DEDUP-REPORT.md",
    "docs/reviews/PHASE-06-ADJUSTMENTS-LOG.md"
  ]
---

# Phase 6: Revisão e Auditoria de Ingestão por Subagentes

Este plano operacionaliza a auditoria de qualidade, consistência conceitual e verificação de redundâncias para a expansão do corpus (Virtudes, Continentes, Oceanos) realizada nas fases anteriores.

---

## Plan

### Task 1: Auditoria de Rigor Metodológico e Normas ABNT (Academic Reviewer)

**Files:**
- Create: `docs/reviews/PHASE-06-ACADEMIC-REVIEW.md`
- Read: `docs/decisions/ALE-GORIAS-VIRTUDES-CONTINENTES-OCEANOS-2026-06-22.md`
- Read: `docs/methodology/codebook-v2-alegorias.md`

- [ ] **Step 1: Instanciar subagente academic-peer-reviewer**
  Avaliar se a nota metodológica cumpre os requisitos de consistência epistemológica (Drucker/Warner/Ihering) e se as citações estão aderentes à ABNT NBR 6023:2025 (incluindo edições e DOIs das fontes referenciadas).
  
- [ ] **Step 2: Gerar o relatório de revisão**
  Salvar a avaliação e pontuar inconsistências de nomenclatura conceitual (ex: flutuações de tradução ou desvios de "endurecimento").

---

### Task 2: Auditoria de Sensibilidade Pós-Colonial e Alinhamento Antropológico

**Files:**
- Create: `docs/reviews/PHASE-06-ANTHROPOLOGICAL-AUDIT.md`
- Read: `wiki/concepts/alegoria-continentes.md`
- Read: `docs/methodology/codebook-v2-alegorias.md`

- [ ] **Step 1: Instanciar subagente Anthropologist**
  Revisar a conceituação e codificação da família "Continentes" sob a ótica pós-colonial (contrato racial visual). Garantir que a pílula de codificação `subaltern_caution` e os vetores de subalternização estejam descritos de forma analítica e não meramente etnográfica ou essencialista.
  
- [ ] **Step 2: Consolidar recomendações**
  Documentar salvaguardas para o capítulo do manuscrito da tese, garantindo o rigor nas seções de iconologia pós-colonial.

---

### Task 3: Verificação de Redundância e Deduplicação do Corpus (DEDUP)

**Files:**
- Create: `docs/reviews/PHASE-06-DEDUP-REPORT.md`
- Modify: `data/processed/records.jsonl`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Scan for duplicate records**
  Comparar estruturalmente os 12/15 novos itens piloto incluídos na expansão com os 265 itens canônicos originais. Analisar metadados (Título, Autor, Data, Suporte, Instituição) e assinaturas visuais para garantir sobreposição zero.
  
- [ ] **Step 2: Emitir relatório de deduplicação**
  Confirmar que a integridade matemática do corpus consolidado (N=280) está mantida e sem registros duplicados ou fantasmas.

---

### Task 3.4: Compilação de Ajustes e Adjudicação

**Files:**
- Create: `docs/reviews/PHASE-06-ADJUSTMENTS-LOG.md`
- Modify: `docs/reviews/PHASE-06-ADJUSTMENTS-LOG.md`

- [ ] **Step 1: Agregar findings dos subagentes**
  Reunir os logs de revisão gerados nas Tarefas 1, 2 e 3 em uma lista unificada de itens de ação, classificados sob a taxonomia de:
  - **Obrigatórios (Critical/Blocking)**: quebras de validação de schema, inconsistências metodológicas estruturais.
  - **Recomendações (Optional)**: sugestões de refinamento de prosa no wiki ou expansão bibliográfica.
