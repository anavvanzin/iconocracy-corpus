# IRR piloto inter-instrumento + achado de integridade — 2026-05-30

Passo 3 do sequenciamento (ver `DIALETICA-N165-vs-265.md`). Search-first → adotou
`compute_irr.py`/`krippendorff` (já no repo). Rater-1 = `iconocode-opus` (do `purification.jsonl`);
rater-2 = agente `iconocode` **cego** (não viu rater-1). **NÃO escrito no ledger canônico** — α
computado direto, dado rater-2 preservado aqui.

## ⚠️ Achado principal (maior que o α): integridade do store de imagens
Numa amostra de 12 itens opus-codificados, **8 "imagens" não eram imagens**:

| ID | arquivo real |
|---|---|
| BE-001, BE-002, BR-005, BR-006, BR-009, BR-010 | **HTML** (página web salva como `.jpg`) |
| BR-007 | **PDF** (6 páginas) como `.jpg` |
| BR-008 | JPEG real (agente errou em nullar) |
| BR-001–004 | JPEG real ✅ |

**Implicação grave:** o rater-1 (`iconocode-opus`) atribuiu scores 0–3 a esses não-imagens
(HTML/PDF). Essas codificações são **inválidas** — baseadas em metadado/alucinação, não na imagem
(coerente com os coders `*-metadata-refined`). A validade da codificação está comprometida **upstream
da decisão de N** — qualquer estatística (a 165 ou 265) inclui itens cuja "imagem" é uma página web.
- Extensão no store inteiro (`binaries/Images`): **79 não-imagens de 206 arquivos = 38%** (127 imagens
  reais · 78 HTML/text · 1 PDF). Mais de um terço da base visual é página web/PDF mascarada de `.jpg`.
  Lista por id em `nao-imagens-store-2026-05-30.json` (worklist de re-aquisição).
  **Padrão diagnóstico:** a maioria são numismáticos (moedas/cédulas — `DE-1000M-1910`, `UK-PENNY-1860`,
  `FR-CERES-5F-1849`, `US-SEATED-1840`…). O pipeline de aquisição de fontes numismáticas (Numista/Colnect)
  salvou a **página de catálogo HTML** em vez da imagem → bug de pipeline localizado. Re-aquisição é
  direcionada (re-resolver URLs numismáticas), não 79 casos avulsos.

## IRR piloto (só os 4 JPEGs reais — BR-001..004)
**Subdimensionado (n=4): indicativo, NÃO resultado.** Per-indicador a n=4 é estatisticamente fraco.

| Métrica | Valor | Limiar |
|---|---|---|
| **Krippendorff α pooled** (40 pares ordinais) | **+0.52** | <0.667 = não-aceitável |
| Concordância exata | 50% | |
| Within-1 ponto | 92% | erros quase sempre ≤1 |
| Diferença média absoluta | 0.57 | |
| **Concordância de REGIME** | **1/4** | instrumentos discordam do regime em 3 de 4 |

Per-indicador (n=4, indicativo): α=1.00 monocromatização, heraldização · α≈0 desincorporação,
rigidez_postural, dessexualização, serialidade · intermediários: apagamento 0.58, enquadramento 0.41.

## Leitura
- Sinal preliminar: **a codificação NÃO é robusta entre versões de modelo** (α pooled 0.52, regime 1/4).
  Vindica a reformulação da dialética: o eixo real é validade de instrumento, não 165-vs-265.
- MAS o piloto é underpowered E contaminado pelo problema de store. **Não tomar decisão de N sobre isto.**

## Próximos passos (revisados pelo achado)
1. **PRÉ-REQUISITO NOVO — limpar o store de imagens:** identificar todos os `.jpg/.png` que são
   HTML/PDF/outros; re-baixar as imagens reais ou marcar itens como sem-imagem. Bloqueia qualquer
   coding visual confiável.
2. **Invalidar codificações sobre não-imagens:** os itens cujo arquivo é HTML/PDF têm endurecimento
   inválido → quarentena adicional (além dos 41 já sem regime).
3. **Refazer o IRR** com n≥25–30 imagens REAIS, após (1)+(2), p/ α estável por indicador.
4. Só então a decisão de N analítico (≈145 vs ≈223) faz sentido.

## Dados rater-2 (cego) — para reprodutibilidade
```
BR-001 norm: 1,3,3,2,1,3,2,3,1,2   (r1 fund: 1,1,2,1,1,1,2,3,1,1)
BR-002 fund: 0,1,0,1,1,1,1,3,0,1   (r1 norm: 1,2,2,2,1,1,2,3,1,2)
BR-003 norm: 1,2,2,2,2,3,2,3,1,2   (r1 norm: 2,2,2,2,2,2,3,3,1,2)
BR-004 norm: 1,1,2,1,0,1,0,2,1,1   (r1 fund: 0,1,1,1,0,0,1,2,1,0)
ordem: desincorporacao,rigidez_postural,dessexualizacao,uniformizacao_facial,heraldizacao,enquadramento_arquitetonico,apagamento_narrativo,monocromatizacao,serialidade,inscricao_estatal
```
