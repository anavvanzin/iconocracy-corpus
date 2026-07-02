# SQ4 ICONOCRACIA — Log de consolidação

**Data:** 2026-05-19 | **Agente:** SQ4 consolidate subagent | **Fragmentos de entrada:** 27 arquivos sq4_*.json | **Saída:** sq4_candidates.json (11 candidatos; 1 — Ripa 1603 Heidelberg — rejeitado depois por dedup contra o corpus enriquecido, restando 10 consolidados)

## 1. Candidatos produzidos

| # | ID | Obra | Ano | País | IIIF | Conf |
|---|---|---|---|---|---|---|
| 1 | sq4-2026-05-19-ripa1603-mdz-001 | Ripa *Iconologia* 1603 (MDZ/Augsburg) | 1603 | Italy | v2 | high |
| 2 | sq4-2026-05-19-ripa1603-heidel-002 | Ripa *Iconologia* 1603 (Heidelberg) — **rejeitado (dedup)** | 1603 | Italy | v2+v3 | high |
| 3 | sq4-2026-05-19-ripa1613-siena-003 | Ripa *Iconologia* 1613 Siena | 1613 | Italy | v2+v3 | high |
| 4 | sq4-2026-05-19-ripa1645-veneza-004 | Ripa *Iconologia* 1645 Veneza | 1645 | Italy | v2+v3 | high |
| 5 | sq4-2026-05-19-ripa1669-frankfurt-005 | Ripa *Erneuerte Iconologia* 1669 Frankfurt | 1669 | Germany | v2+v3 | high |
| 6 | sq4-2026-05-19-alciato1531-augsburg-006 | Alciato *Emblematum liber* 1531 Augsburg | 1531 | Germany | — | high |
| 7 | sq4-2026-05-19-alciato1550-lyon-007 | Alciato *Emblemata* 1550 Lyon (Rovilius) | 1550 | France | v2 | high |
| 8 | sq4-2026-05-19-alciato1577-antwerp-008 | Alciato *Omnia Emblemata* 1577 Antuérpia (Plantin) | 1577 | Belgium | v2 | high |
| 9 | sq4-2026-05-19-camerarius-cent3-009 | Camerarius *Symbolorum cent. III* 1596 Nuremberg | 1596 | Germany | v2 | high |
| 10 | sq4-2026-05-19-saavedra1643-empresas-010 | Saavedra Fajardo *Empresas Políticas* 1643 | 1643 | Spain | — | high |
| 11 | sq4-2026-05-19-loscher1536-iustitia-011 | Loscher *Allegorie der Gerechtigkeit* 1536 Augsburg | 1536 | Germany | — | medium |

**Total bruto:** 11 | **Consolidado:** 10 (após dedup) | **Com IIIF:** 8/11 (73%)

## 2. Cobertura de obras

- **Ripa (Iconologia):** 5 — edições 1603 (2 instâncias), 1613, 1645, 1669
- **Alciato (Emblemata):** 3 — 1531, 1550, 1577
- **Camerarius:** 1 — centuria III (aves/insetos), 1596
- **Saavedra Fajardo:** 1 — *Empresas Políticas* 1643
- **Fonte jurídica alemã (escultura):** 1 — Loscher 1536

## 3. Manifestos IIIF confirmados (padrões)

- **Heidelberg:** `https://digi.ub.uni-heidelberg.de/diglit-data/iiif/{slug}/manifest.json`
- **MDZ:** `https://api.digitale-sammlungen.de/iiif/presentation/v2/{id}/manifest`

## 4. Notas iconográficas relevantes

- **Ripa — Giustizia:** *Giustizia Divina* (olhos claros, balança, espada, pomba); *Giustizia Terrena* (vendada — "exercitada no Tribunal de juízes seculares"); *Giustizia* segundo Aulus Gellius (olhos penetrantes). Venda como imparcialidade (não cegueira) emerge a partir de 1611.
- **Alciato:** emblema IUSTITIA (balança/espada, sem venda na maioria); IURIS PRUDENTIA (olhos abertos). Tradição Alciato insiste na clarividência vs. Ripa admite a venda.
- **Camerarius:** CUSTOS IUSTITIAE (grua com pedra = vigilância); IUSTA ULTIO (cegonha = retribuição justa).
- **Saavedra Fajardo:** 101 empresas; Iustitia como virtude régia ("os príncipes decretam a justiça em nome de Deus").
- **Loscher (1536):** dualidade irdisch/göttlich; Iustitia volta-se de balança/espada para Deus Pai; colunas como força jurídica.

## 5. Verificação de dedup

Todos os 11 URLs canônicos verificados contra dedup_urls.txt (368 URLs): nenhum duplicado na lista; Ripa 1603 Heidelberg rejeitado por já estar no corpus enriquecido (corpus-data-enriched.json).
