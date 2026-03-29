---
id: URL-VERIFICATION-2026-03-29
tipo: verificacao
data: 2026-03-29
fonte: scout-session-2026-03-28
tags:
  - protocolo
  - verificar
related:
  - "[[SCOUT-SESSION-2026-03-28-F]]"
---

# Relatorio de Verificacao de URLs — Scout Session 2026-03-28

**Data da verificacao:** 2026-03-29
**Fonte:** `vault/corpus/scout-session-2026-03-28/`
**Criterio:** todas as URLs com flag `#verificar` (tag YAML ou flag em secao Flags)
**Metodo:** navegacao direta via browser, leitura do titulo da pagina carregada

---

## Resultados

| SCOUT ID | URL | Status | Notes |
|---|---|---|---|
| SCOUT-029a | https://en.numista.com/274388 | accessible (200) | Titulo confirmado: "500 Mark (Stadtsparkasse) - City of Bielefeld (notgeld) -- Numista". Conteudo compativel com Notgeld Bielefeld 500 Mark. |
| SCOUT-032 | https://karlgoetz.com/ImageDetail.aspx?idImage=223 | inaccessible (site em manutencao) | Pagina redireciona para "Coming Soon -- Karl Goetz" com heading "ARRIVING SOON! Catalogue Raisonne". O site karlgoetz.com esta em redesign; a URL especifica do K-299 nao exibe o conteudo esperado. Necessita URL alternativa. |
| SCOUT-034 | https://artgallery.yale.edu/collections/objects/165690 | accessible (200) | Titulo confirmado: "Medal of Die Schwarze Schmach Yale University Art Gallery". Conteudo compativel com medalha Goetz Die Schwarze Schmach. |
| SCOUT-035 | https://en.numista.com/catalogue/pieces27258.html | accessible (200, redirect) | Redirect de `/catalogue/pieces27258.html` para `/27258`. Titulo confirmado: "5 Francs (50 Years of Belgium) - Belgium -- Numista". Conteudo compativel com moeda comemorativa belga 1880. |

---

## Resumo

- **3/4 URLs acessiveis** e com conteudo confirmado
- **1/4 URL inacessivel** (SCOUT-032 — karlgoetz.com em manutencao)

## Acoes recomendadas

1. **SCOUT-032:** Buscar URL alternativa para K-299 "Die Wacht an der Ruhr". Opcoes:
   - US Naval History and Heritage Command (acervo secundario listado na nota)
   - Kienast catalog digital (se disponivel)
   - Numista (buscar medalha Goetz K-299)
   - Wikimedia Commons (possivel imagem em dominio publico)
2. **SCOUT-035:** Atualizar URL canonica para `https://en.numista.com/27258` (formato curto, pos-redirect)
3. Marcar `#verificar` como `[x]` nas notas SCOUT-029a, SCOUT-034 e SCOUT-035
