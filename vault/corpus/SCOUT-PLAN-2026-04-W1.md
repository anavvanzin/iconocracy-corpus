---
id: SCOUT-PLAN-2026-04-W1
tipo: plano-campanha
status: ativo
tags:
  - corpus/planejamento
  - campanha-1
  - brasil
  - fundacional
created: 2026-04-10
---

# Plano de Campanha — Semana 1 (08–14 abr. 2026)

## Objetivo

Localizar ao menos 3 itens brasileiros (1889–1910) que mostrem a transferência da Pathosformel republicana francesa para suportes oficiais brasileiros com alto acoplamento imagem-norma.

## Alvos prioritários

| Item | Acervo | URL base | Notas |
|------|--------|----------|-------|
| Litografia "Proclamação da República" | BNDigital (Hemeroteca) | https://bndigital.bn.gov.br | Pesquisar "Proclamação da República" + "litograph" + 1889 |
| Frontispício do Decreto 1 (1889) | Arquivo Nacional digital | https://docvirt.com/docreader/DocReader.aspx?bib=ACDigital | Verificar legibilidade/IIIF |
| Medalha comemorativa 1890 | Museu Histórico Nacional / portal Brasiliana Iconográfica | https://www.brasilianaiconografica.art.br | Consultar "medalha República" |

## Query book

### BNDigital SRU
```
https://bndigital.bn.gov.br/sru?version=1.2&operation=searchRetrieve&startRecord=1&maximumRecords=25&query=dc.creator%20all%20%22Visconti%22%20and%20dc.subject%20all%20%22Republica%22
```

### Brasiliana Fotográfica
- Tags: `República`, `alegoria`, `justiça`.
- Filtros: 1880–1910, suporte "gravura" ou "ilustração".

### Iconocartografia RJ
- Buscar "allegoria republicana" `site:iconocartografiarj.com.br`.

## Sequência operacional

1. Executar queries (segunda-feira) → salvar links/THUMB em `vault/corpus/assets/2026-04-XX/`.
2. Redigir notas SCOUT usando template (máx. 3 por campanha) e anexar dados ao `SCOUT-NARR-2026-04-W1C1`.
3. Rodar IconoCode para cada item → verificar indicadores (desincorporação, rigidez, acoplamento).
4. Atualizar `Storytelling - Campanhas Abril 2026` com resultados e painel alvo do Atlas.
5. Registrar sessão em `vault/sessoes/SCOUT-SESSION-2026-04-XX.md` com métricas.

## Checkpoints

- [ ] Garantir IIIF ou imagem HD para cada item.
- [x] Preencher campo `related` com `[[Capitulo 3]]`, `[[Capitulo 5]]`, `[[Atlas Painel I]]`.
- [x] Marcar flags `#verificar-data` ou `#sem-iiif` quando aplicável.

## Observações

- Priorizar itens com presença explícita de texto normativo (pergaminhos, decretos, inscrições legíveis).
- Coletar paletas cromáticas com `pip install colour-science` (rodar depois) para Atlas.
- Registrar insights para Artigo A (contraste ENDURECIMENTO fundacional x militar).
