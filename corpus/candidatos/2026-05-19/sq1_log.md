# ICONOCRACIA SQ1 — Log de execução

**Data:** 2026-05-23 | **Executor:** subagent (research-assistant) | **Resultado:** 8 candidatos

## Resumo

Tarefa: localizar 8–10 novos candidatos de alegorias femininas da Justiça (século XIX longo), excluindo Gallica e URLs já no dedup_urls.txt (368 entradas).

## Fontes consultadas

| Arquivo | Status | Resultado |
|---|---|---|
| Albertina Wien (sammlungenonline) | Acessível | 1 candidato confirmado (DG2017/1/6542) |
| Rijksmuseum Amsterdam | Acessível | 1 candidato confirmado (RP-P-1970-232) |
| British Museum Londres | Acessível | 1 candidato confirmado (1878,0713.2311) |
| Library of Congress P&P | Acessível (páginas de item) | 4 candidatos confirmados (pga-03861, ppmsca-19254, pga-02893, pga-01777) |
| Museo Nacional del Prado | Acessível | 1 candidato confirmado (Goya, Desastres 79) |
| ONB Austria (digital.onb.ac.at) | disallow_by_robots | 0 |
| HathiTrust | disallow_by_robots | 0 |
| KBR Bélgica | Acessível, mas somente itens anteriores ao século XIX | 0 |
| MetMuseum API | uncrawlable_url | 0 usáveis |
| Princeton Art Museum | Acessível | Rethel Todtentanz identificado; descartado (Justiça como figura de fundo) |

## Candidatos selecionados (8 de 8)

1. **Schwind/Langer — Justitia 1848** | Albertina Wien | sq1-2026-05-19-schwind-justitia-001 | alta confiança
2. **De La Serrie/Prud'hon — Justitia protege Inocência 1806** | Rijksmuseum | sq1-2026-05-19-prud-hon-innocence-002 | alta confiança
3. **Gusman/Prud'hon — Justice et Vengeance Divine c1840–78** | British Museum | sq1-2026-05-19-gusman-justice-vengeance-003 | alta confiança
4. **Inger — Liberty (Justice e Peace) 1863** | Library of Congress | sq1-2026-05-19-inger-liberty-004 | alta confiança
5. **Baker & Godwin — Abraham Lincoln (Justice à esquerda) c1860** | Library of Congress | sq1-2026-05-19-baker-godwin-lincoln-005 | alta confiança
6. **Traubel — Triumph (Justice à direita de Freedom) c1861** | Library of Congress | sq1-2026-05-19-traubel-triumph-006 | alta confiança
7. **Kimmel & Forster — Outbreak of Rebellion (Justice sem venda) c1865** | Library of Congress | sq1-2026-05-19-kimmel-outbreak-007 | alta confiança
8. **Goya — La verdad ha muerto / Truth has died (Justice em luto) 1814–15** | Museo del Prado | sq1-2026-05-19-goya-truth-died-008 | confiança média (Justiça secundária)

## Cobertura IIIF

- Rijksmuseum (candidato 2): IIIF manifest disponível via API Rijksmuseum
- Restantes: sem manifesto IIIF confirmado; LoC oferece handles HDL, não manifesto Presentation API completo

## Dedup checks

Todos os 8 URLs canônicos verificados contra dedup_urls.txt (368 entradas). Nenhum duplicado encontrado. Os itens selecionados (2003689287, 2003689297, 2004665350, 2004665366) NÃO constam na lista.

## Limitações

- Candidato 8 (Goya): Justiça é figura secundária; incluído por qualidade iconográfica e raridade no corpus.
- ONB, HathiTrust e BNP: robots.txt bloqueou fetches diretos.
- MetMuseum: API não crawlável via fetch_url; busca web retornou somente itens anteriores ao período.
