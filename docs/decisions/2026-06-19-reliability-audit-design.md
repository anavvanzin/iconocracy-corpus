---
tags: [meta, methodology, reliability, data, design-spec, decision]
date: 2026-06-19
status: draft-for-review
sub_project: 2 (validade analítica dentro do release)
see_also:
  - docs/decisions/2026-06-19-ssot-apparatus-critico-design.md
  - docs/decisions/DIALETICA-N165-vs-265.md
---

# Design Spec — Auditoria de Confiabilidade do IconoCode
## (Validar a fusão opus + opus-4.6 → N analítico ≈ 145)

## 1. Problema
A análise quantitativa da tese (distribuições de endurecimento, Kruskal-Wallis) precisa de um **N analítico válido**. O corpus foi codificado por instrumentos distintos (`coded_by`): `iconocode-opus` (100 itens) e `iconocode-opus-4.6-*` (45: 29 metadata-refined + 16 image), em **conjuntos disjuntos** (0 itens codificados pelos dois). Fundi-los num N≈145 é hoje **invalidado**: não há dado pareado que mostre que (a) a codificação-IA é *válida* (concorda com a especialista) nem que (b) opus e 4.6 são *consistentes entre si*.

## 2. Decisão (brainstorming aprovado 2026-06-19)
Estabelecer **duas camadas** de confiabilidade a partir de **uma amostra unificada (n≈50)**, e decidir a fusão por regra explícita.
- **Camada 1 — Validade (humano×IA):** Ana codifica cega; é o *gold standard*. Concordância humano×opus e humano×4.6.
- **Camada 2 — Consistência inter-instrumento (opus×4.6):** justifica fundir as duas versões.
- **Regra de decisão:** se α ≥ 0,667 (mínimo aceitável) em ambas as camadas → **funde, reporta N≈145**; senão → **recua para opus-only N≈100**, documentado no dataset card.

## 3. Amostra unificada (n≈50)
- 50 itens sorteados dos **100 `iconocode-opus`** (assim o baseline opus já existe; só se adiciona humano + 4.6).
- **Estratificada por regime × faixa de `endurecimento_score`** (cobrir 0–3, não só os scores comuns) — concordância tem que ser testada onde é difícil.
- Um só conjunto rende as **três comparações**: humano×opus, humano×4.6, opus×4.6.

## 4. Métricas & limiar
- **Krippendorff's α (ordinal)** por indicador (10×) **e** pooled.
- **ICC** no `endurecimento_score` composto.
- **Cohen's κ** no rótulo de regime (nominal).
- Limiar: **α ≥ 0,80 bom · ≥ 0,667 mínimo aceitável** (convenção de content analysis).

## 5. Protocolo cego (controla confundimentos)
- Ana codifica **só pela imagem**, sem ver score-IA; ordem dos itens randomizada.
- O 4.6 re-roda **pela mesma modalidade (imagem)** que o opus usou → isola *versão-de-modelo* de *modalidade-de-input* (não comparar opus-imagem com 4.6-metadata-refined).
- 4.6 re-roda sem score prévio no contexto (cego por construção do LLM).

## 6. Captura out-of-band (NÃO sobrescreve o ledger)
Arquivo **novo** `data/reliability/paired-codings-2026-06-19.jsonl` — uma linha por (item × indicador):
```json
{"item_id":"...", "semantic_id":"BR-007", "regime":"militar",
 "indicador":"rigidez_postural", "valor_humano":2, "valor_opus":3, "valor_4_6":2,
 "modalidade_4_6":"image", "coded_at":"..."}
```
Schema validado (novo `tools/schemas/paired-coding.schema.json`). O ledger `records.jsonl` permanece intocado.

## 7. Saídas
- `data/reliability/reliability-report-2026-06-19.md` — αs por indicador + pooled, ICC, κ, e o **veredito** (funde N≈145 ou recua N≈100).
- Os números entram no **dataset card** do release (já previsto no aparato crítico) e viram material do **capítulo de metodologia** (sub-projeto 4).

## 8. Dependências (pré-requisitos de execução)
1. **Corpus canônico** (origin/main=309, pós-**Phase 0** do SSOT) para sortear a amostra.
2. **Acesso às imagens** (Google Drive / `data/raw` manifest) para Ana e o 4.6 codificarem.
3. Re-execução do instrumento `iconocode-opus-4.6` (image) nos 50 itens.

## 9. Não-objetivos / riscos
- **NÃO** sobrescrever codings existentes; a amostra é aditiva.
- **NÃO** validar import/migration (Estrato 2) — fora deste sub-projeto (seria o caminho N≈223).
- Risco: se a concordância falhar, o N cai p/ ~100 — aceito pela regra de decisão (a tese ainda roda com N=100, single-instrument, mais limpo).

## 10. Critérios de sucesso
- [ ] n≈50 pareado, estratificado, com as 3 comparações computadas.
- [ ] α/ICC/κ reportados com CI; veredito explícito de fusão.
- [ ] Codings pareados num arquivo out-of-band schema-válido; ledger intocado.
- [ ] Dataset card declara o N analítico final e a evidência de confiabilidade.
