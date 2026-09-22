# Protocolo de Confiabilidade Inter-Instrumento (opus vs opus-4.6)

**Status:** rascunho · **Criado:** 2026-06-10
**Referências:** `IRR-RE-RUN-DESIGN-2026-06-09.md` · `IRR-PILOTO-2026-05-30.md` · `DIALETICA-N165-vs-265.md` · `audit-coded-by-2026-06-10.md`
**Pré-requisitos:** estratificação (`audit-coded-by-2026-06-10.md`) e limpeza do store de imagens (`nao-imagens-store-2026-05-30.json`).

---

## 1. Objetivo

Estabelecer a **confiabilidade inter-instrumento** entre as duas versões de modelo que codificaram o Estrato 1 (IconoCode): `iconocode-opus` (100 itens) vs. o cohort `iconocode-opus-4.6-*` (45: 29 `metadata-refined` + 16 `image`). Pergunta empírica estreita: **as duas versões pontuam os 10 indicadores ordinais consistentemente o bastante para serem agrupadas num único estrato analítico (N≈145)** antes do Kruskal-Wallis regime × morfologia (Cap. 6.2)?

Conforme `DIALETICA-N165-vs-265.md:55-57`, este diagnóstico **decide qual versão do corpus é primária** — converte a decisão de N de preferência em teste empírico.

## 2. Relação com IRR-RE-RUN-DESIGN (complementar, não duplicado)

| Eixo | IRR-RE-RUN (inter-AVALIADOR) | Este (inter-INSTRUMENTO) |
|---|---|---|
| Pergunta | O instrumento é replicável por avaliador novo? | As duas versões já usadas concordam? |
| Variável manipulada | Avaliador (rater-2 cego, modelo qualquer) | Versão do modelo (opus ↔ opus-4.6) |
| População | Itens elegíveis pós-E1 | Os 145 já codificados do Estrato 1 |
| Valida | Validade do instrumento | Legitimidade de fundir 145 num estrato |
| Consequência | Liberar/segurar E2 | Fixar o N analítico (≈145 pooled vs split) |

**Ordem recomendada: rodar ESTE antes do IRR-RE-RUN** — se as versões internas não concordam, o estrato a submeter ao rater-2 cego está mal definido. Ambos reusam `tools/scripts/compute_irr.py` (α ordinal, α por indicador, adjudicação) e o ledger multi-coder `data/processed/purification.jsonl` (schema já comporta 2+ codificações/item).

## 3. Diagnóstico de rubrica (mesma régua?)

**Conclusão: rubrica formalmente idêntica, mas com dois confundidores reais a controlar.**

A favor de "mesma régua": mesmas 10 chaves de indicador (escala 0–3) nos três instrumentos; codebook (`data/docs/codebook.md`) e schema (`tools/schemas/purification-record.schema.json`, `min 0 max 3`) estáveis no git durante a codificação; janela temporal curta (`coded_at` ≈ 31/03–07/04/2026, ~1 semana — **não** há a "deriva de ~1 ano" temida na dialética).

Confundidores a isolar:
1. **Re-escala 0–4 → 0–3** (`audit_flag = pre_canon_rescale_2026-04-19`): atinge ~5 itens opus + ~6 opus-4.6-image. Parte do corpus foi pontuada em 0–4 e re-escalada post hoc → analisar à parte.
2. **Modalidade dentro do "opus-4.6"**: `opus-4.6-image` (16) codificou da IMAGEM; `opus-4.6-metadata-refined` (29) codificou de METADADO/TEXTO sem ver a imagem (alguns constam na worklist de não-imagens). A comparação ingênua "opus vs opus-4.6" **confunde versão-de-modelo com modalidade-de-input**.

**Implicação:** três contrastes, não um — (a) opus-image ↔ opus4.6-image (versão pura); (b) opus-image ↔ opus4.6-metadata-refined (versão+modalidade, esperada pior); (c) sensibilidade sem os ~11 itens `pre_canon_rescale`.

## 4. Amostragem — re-codificação cruzada bidirecional

| Direção | Re-codificador | Alvo | n |
|---|---|---|---|
| A | opus-4.6-image | amostra estratificada por regime dos 100 opus | **35** |
| B | opus | censo dos 45 opus-4.6 (16 image + 29 metadata) | **45** |

Estratificação dir. A (proporcional à distribuição opus: fundacional 58 / normativo 29 / militar 13 / contra-alegoria 0): **fundacional 20, normativo 10, militar 5**. Seleção via `tools/scripts/select_irr_sample.py` com seed fixa. Restringir a itens com imagem real (cruzar `nao-imagens-store-2026-05-30.json`; substituir não-imagens dentro do mesmo estrato).

**Poder:** n=35 (A) + 45 (B) ⟹ ~80 pares ordinais por indicador (~800 no pooled), acima do piso de 250–300 que o IRR-RE-RUN estima para α≥0,667 com β≈0,80. Corrige o piloto n=4 (α por indicador instável: monocromatização α=1,00 vs desincorporação α≈0 por acaso amostral).

## 5. Métrica e limiar

**Primária por indicador: Krippendorff's α (nível ordinal)** — os indicadores são genuinamente ordinais 0–3; α ordinal penaliza discordâncias proporcionalmente, generaliza p/ >2 instrumentos, tolera faltantes, e já está implementado em `compute_irr.py` (`level_of_measurement="ordinal"`). **Não** κ ponderado de Cohen (restrito a 2 avaliadores/categorias). **Não** Spearman como primária (mede associação, não concordância — entra só como diagnóstico de viés sistemático vs ruído).

| Métrica | Alvo |
|---|---|
| α por indicador | ≥0,80 bom · 0,667–0,80 tentativo · <0,667 fraco (vira nota de rodapé no Cap. 6) |
| α pooled | ≥0,667 (piso para fundir) |
| Within-1 ponto | ≥90% (benchmark do piloto) |
| κ de regime (Cohen) | ≥0,667 |

## 6. Procedimento

1. Congelar codificação original como `coding_round=1` em `purification.jsonl`.
2. Amostrar (dir. A via `select_irr_sample.py` + seed); dir. B = censo dos 45.
3. Verificar imagem real; exportar p/ `data/processed/inter_instrumento/sample/`.
4. **Re-codificação cega:** modelo recebe só imagem + contexto mínimo (título/país/data/suporte) + prompt do codebook. **Não** recebe codificação original, regime, nem nome do outro instrumento (anti-leakage).
5. Gravar como `coding_round=2`; `compute_irr.py` detecta itens com ≥2 coders.
6. Computar **sempre** α por indicador **e** pooled (nunca decidir só pelo composto).
7. Três relatórios de contraste (§3).
8. Adjudicar discordâncias ≥2 níveis via `compute_irr.py --adjudicate`.

## 7. Custo estimado

~800 tok/item (600 prompt + 200 saída): dir. A ≈28K + dir. B ≈36K = **~64K tok** texto; com input multimodal (imagem), pior caso **~150–250K tok**. Execução ~80 itens × ~60s ≈ **~80 min** em batch. Zero re-aquisição se o store já estiver limpo.

## 8. Regra de decisão sobre N (contraste (a) decide)

| Resultado (a) opus-image↔opus4.6-image | Decisão de N | Sub-cohorts |
|---|---|---|
| α pooled ≥0,80 **e** κ regime ≥0,667 | **Pool total → N≈145 primário** | versões fundidas; metadata só se (b) ≥0,667 |
| 0,667 ≤ α < 0,80 | **N≈145 com ressalvas** (indicadores <0,667 = limitação) | metadata como sensibilidade se (b) fraco |
| α < 0,667 | **NÃO fundir → N=100 (só opus) primário** | opus-4.6 vira sensibilidade em apêndice (estrutura v1.0/v2.0) |
| (b) fraco mas (a) bom | pool das versões-imagem | metadata-refined quarentenado como Estrato 1b (modalidade textual) |

Resultado alimenta o **dataset card do Cap. 2** substituindo "N=165": "Estrato 1 (IconoCode) = N≈145 após auditoria inter-instrumento (α=[valor]); ondas opus / opus-4.6 [fundidas | separadas]".

## 9. Artefatos (reuso — search-first)

| Artefato | Local | Status |
|---|---|---|
| Amostrador estratificado | `tools/scripts/select_irr_sample.py` | reusar |
| α ordinal + por indicador + adjudicação | `tools/scripts/compute_irr.py` | reusar |
| Ledger multi-coder | `data/processed/purification.jsonl` | reusar (schema OK) |
| Codebook (régua) | `data/docs/codebook.md` | estável no período |
| Batch de re-codificação cega cross-versão | (a criar — compartilhar com IRR-RE-RUN) | **criar** |
| Amostra/resultados | `data/processed/inter_instrumento/` | a gerar |
