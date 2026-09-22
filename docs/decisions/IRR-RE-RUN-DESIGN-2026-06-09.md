# IRR Re-run Design — ICONOCRACY E2 stepping stone

**Status:** rascunho
**Criado:** 2026-06-09
**Referência:** `IRR-PILOTO-2026-05-30.md` (docs/decisions/)
**Pré-requisito:** `pathosformel_index.jsonl` com 265 itens codificados (E1 completo)

---

## 1. Objetivo

Estabelecer a confiabilidade inter-avaliador (inter-rater reliability) do protocolo IconoCode
antes de prosseguir para E2 (cluster por regime visual). O piloto (n=4, α=0.52) foi
subdimensionado e contaminado por não-imagens. O re-run deve produzir α estável **por
indicador** (não apenas pooled) com poder estatístico adequado.

## 2. Requisitos do piloto anterior

| Requisito | Piloto (30/05) | Re-run |
|-----------|----------------|--------|
| Amostra | 4 itens (todos BR) | 25-30 itens |
| Imagens reais | 4/12 da amostra eram reais | **100% reais** |
| Rater-2 cego | Sim | Sim |
| α por indicador | n=4 instável | n≥25-30 estável |
| α pooled | 0,52 (não aceitável) | Target ≥0,667 |
| Regime | 1/4 concordância | Target ≥0,667 |
| Script | `compute_irr.py` | Mesmo script + melhorias |

## 3. Design amostral

### 3.1 População elegível

Itens do `pathosformel_index.jsonl` com **imagem real** confirmada no store.
Excluídos:
- 79 não-imagens (HTML/PDF) da worklist `nao-imagens-store-2026-05-30.json`
- Itens marcados como `#no-image`
- Itens cujo rater-1 score veio de descrição textual (summary <100ch) — *opcional*

Após E1 completo + quarentena, população esperada: ~186-200 itens reais.

### 3.2 Amostragem

Estratificada proporcional por regime iconocrático (para evitar viés de classe):

| Estrato | Pop. estimada | Amostra 30 | Amostra 25 |
|---------|--------------|------------|------------|
| Fundacional | ~100 | 15 | 12 |
| Normativo | ~60 | 9 | 8 |
| Militar | ~20 | 4 | 3 |
| Contra-alegoria | ~8 | 2 | 2 |
| **Total** | **~188** | **30** | **25** |

**Critério de seleção dentro do estrato:** amostra aleatória simples (SRS) via seed fixa
(ex.: `irr_seed = 20260611`) para reprodutibilidade.

**Requisito mínimo por indicador:** n≥25 → α de Krippendorff com 2 raters + 10 indicadores
= 250-300 pares ordinais, poder adequado para detectar α≥0,667 a β=0,80.

### 3.3 Pré-requisito de imagem

**Cada item sorteado deve ter imagem real** verificada antes da ida ao rater-2.
Workflow:
1. Sortear item
2. Verificar se `data/raw/drive-manifest.json` ou `exports.local_path` aponta para JPEG/PNG real
3. Se não-imagem, sortear substituto do mesmo estrato
4. Exportar imagem para pasta `data/processed/irr_re_run/sample/` para rater-2

## 4. Protocolo de codificação cega (rater-2)

### 4.1 Ferramenta

Reutilizar `compute_irr.py` do repo (já usa `krippendorff` alpha). Extensão necessária:
- `--rater2` flag para modo cego (não exibe scores de rater-1)
- `--output-raw` para salvar pares (rater-1, rater-2) em JSONL
- `--indicator-report` para α por indicador com IC de 95% (bootstrap)

### 4.2 Apresentação

Para cada item, mostrar:
1. Imagem (da pasta `irr_re_run/sample/`)
2. Título, país, data, suporte (contexto mínimo — igual ao E1)
3. Prompt de codificação idêntico ao E1 (10 indicadores + regime)

Rater-2 **não vê**:
- Scores do rater-1
- Sigla completa (para evitar viés de identificação)
- Regime atribuído por rater-1

### 4.3 Modelo rater-2

**Opção A — mesmo modelo que o rater-1 (Gemma-4):** mais comparável, mede
estabilidade intra-modelo. Vantagem: controla variável de modelo. Desvantagem:
não testa viés de arquitetura.

**Opção B — modelo diferente (Grok, Claude Sonnet, GPT):** mais conservador,
mede robustez cross-modelo.

**Recomendação:** Opção B (cross-modelo) para o re-run. Se α ≥ 0,667, a
codificação é robusta independentemente do modelo. Se falhar, refazer com
Opção A para diagnóstico (instabilidade é do modelo ou do instrumento?).

### 4.4 Prompt rater-2

Idêntico ao E1 (mesma escala, mesmos indicadores), com a adição de:
- Campo `image_condition: str` — "visivel" | "parcialmente_visivel" | "ilegivel" |
  "nao_carregou"
- Se `nao_carregou`, o item é registrado como falha técnica e substituído

## 5. Métricas e limiares

| Métrica | Alvo | Interpretação |
|---------|------|---------------|
| Krippendorff α pooled (10 indicadores × n itens) | ≥0,667 | Aceitável para pesquisa exploratória |
| Krippendorff α por indicador | ≥0,667 (individ.) ou ≥0,500 (discutível) | Indicadores problemáticos viram nota de rodapé no Cap.6 |
| Concordância exata | ≥60% | Benchmark |
| Within-1 (erro ≤1 ponto) | ≥90% | Manter benchmark do piloto |
| Concordância de regime (κ de Cohen) | ≥0,667 | Regime é constructo central |
| α por estrato (fundacional / normativo / militar) | reportar | Diagnóstico de viés de regime |

## 6. Plano de execução

```
Passo 1 — [QUI 11/06]   Amostrar 30 itens estratificados da população elegível
Passo 2 — [QUI 11/06]   Verificar imagens e exportar para data/processed/irr_re_run/sample/
Passo 3 — [SEX 12/06]   Rodar rater-2 (batch via script, modelo alternativo)
Passo 4 — [SEX 12/06]   Rodar compute_irr.py --indicator-report
Passo 5 — [SEG 15/06]   Revisar resultados e decidir:
                         • α≥0,667 pooled → liberar E2 (cluster)
                         • 0,500≤α<0,667 → reportar indicadores fracos, seguir E2 com cautela
                         • α<0,500 → revisar instrumento (rever prompts/indicadores)
```

## 7. Scripts e artefatos

| Artefato | Local | Status |
|----------|-------|--------|
| `compute_irr.py` | `tools/scripts/compute_irr.py` | Existe (usar) |
| Extensão cross-modelo | `tools/scripts/irr_rater2_batch.py` | **Criar** |
| Amostra estratificada | `tools/scripts/irr_sample.py` | **Criar** |
| Planilha de resultados | `data/processed/irr_re_run/results.json` | Será gerado |
| Visualização (heatmap) | `notebooks/09_irr_heatmap.ipynb` | Opcional |

## 8. Open questions

1. **Modelo rater-2:** Qual modelo usar? (→ decisão da pesquisadora)
2. **Rater humano:** A pesquisadora quer atuar como rater-2 humano em subamostra (n=10)?
   Isso permitiria validar não só o instrumento mas a codificação automática vs. humana.
3. **ITC (Intra-rater):** Vale a pena testar estabilidade intra-avaliador (rater-1 vs. rater-1
   duas semanas depois) em n=10? Detecta deriva nas respostas do modelo.

---

## Apêndice — Orçamento de tokens

- Prompt: ~600 tokens por item
- Output: ~200 tokens por item
- 30 itens × 800 tokens = 24K tokens por rater-2 rodada
- Modelo alternativo: estimar custo (gratuito via OpenRouter ou Nous Portal)
- Tempo estimado: 30 itens × ~60s = ~30 min
