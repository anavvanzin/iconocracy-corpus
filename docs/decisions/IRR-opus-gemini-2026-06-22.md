# IRR opus-4.8 × Gemini-3.5-Flash (cross-instrumento direto) — 2026-06-22 — PRELIMINAR

Audit DIRETO do lote opus-4.8: rater-1 = opus-4.8 (14 itens coded do cohort principal), rater-2 = Gemini-3.5-Flash (High) via `agy`, **codificação cega** (só imagem, mesmos 10 indicadores 0–3). Krippendorff α ordinal.

## Resultado (N=14)
- **α global = −0.02** · composto MAD **1.17** · regime exato **0.50**.
- Todos os 10 indicadores α < 0.3 (a maioria negativo). Pior: desincorporacao −0.33, monocromatizacao −0.31. "Melhor": heraldicizacao 0.25.
- **Offset sistemático:** composto médio Gemini **1.85** vs opus-4.8 **0.84** (Gemini ancora ~+1 ponto em quase tudo).

## Leitura
O sinal dominante é **offset de calibração** (Gemini pontua sistematicamente mais alto), não ruído aleatório. α negativo = "os modelos usam a escala 0–3 de forma diferente", **não** "opus-4.8 inválido". Reforça: indicadores **não transferem entre instrumentos** sem calibração → análise estratificada por instrumento; nunca poolar indicador cru. opus×fable (0.601) era otimista porque opus/fable são classes próximas; Gemini (independente) revela mais divergência.

## ⚠️ CONFOUNDS — resultado PRELIMINAR, não definitivo
1. **Tier:** Gemini **3.5 Flash** (não Pro) — parte do desacordo pode ser ruído do Flash.
2. **Prompt desigual:** opus teve brief rico com ancoragem 0=X/3=Y; Gemini teve prompt condensado sem exemplos de calibração → ancorou alto.
3. **N=14** pequeno.
→ Para limpar: re-rodar com **Gemini 3.1 Pro (High)** + **mesmo brief rico**. Só então o número é citável.

## Comparação
| par | α global | composto MAD | regime exato | N |
|---|---|---|---|---|
| opus-legado × fable-5 | 0.601 | 0.31 | 0.61 | 28 |
| opus-4.8 × Gemini-3.5-Flash | −0.02 | 1.17 | 0.50 | 14 |

Ferramenta: `agy` (antigravity CLI, Gemini headless via `-p` + `@imagem`). Artefato: `IRR-opus-gemini-2026-06-22.json`.
