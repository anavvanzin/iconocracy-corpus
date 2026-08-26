---
id: SCOUT-SESSION-2026-04-10-B
tipo: sessao-scout
data: 2026-04-10
query_executada: "BR fundacional/cedula — cédulas brasileiras da Primeira República com alegorias femininas (1889-1930)"
total_candidatos: 2
pais: [BR]
periodo: "1890-1893"
tags:
  - corpus/sessao-scout
  - protocolo
  - pais/BR
  - suporte/cedula
related:
  - "[[DB1 Corpus Iconografico]]"
  - "[[IconoCode -- Protocolo]]"
  - "[[SCOUT-SESSION-2026-04-10]]"
---

## Resumo da sessao

**Query:** Busca de cédulas brasileiras da Primeira República (1889-1930) com alegorias femininas (Liberdade, Justiça, Governo, República). Lacuna identificada: BR fundacional/cédula.
**Acervos consultados:** Numista, World Banknotes & Coins, Wikipedia, atsnotes.com
**Candidatos encontrados:** 2 (+ 1 Zwischenraum)
**Nivel de confianca predominante:** alto (SCOUT-423), medio (SCOUT-424)

### Candidatos gerados

| ID | Titulo | Regime | Confianca |
|----|--------|--------|-----------|
| SCOUT-423 | 50 Mil Réis — Banco do Brazil (1890) | FUNDACIONAL | alto |
| SCOUT-424 | 20 Mil Réis — Banco da República (c. 1890) | FUNDACIONAL | medio |
| SCOUT-ZW-09 | Painel 9 — Cédulas Fundacionais BR | — | — |

### Contexto

Esta sessão complementa a campanha BR iniciada em sessões anteriores (SCOUT-413 a SCOUT-422, focada em moedas). O foco aqui foi **papel-moeda** (cédulas), que constitui uma lacuna significativa no corpus: nenhuma cédula brasileira estava representada.

As cédulas de 1890 são particularmente relevantes porque representam os primeiros instrumentos monetários visuais do regime republicano — a Proclamação foi em 15/11/1889, e as primeiras emissões republicanas começaram em 1890.

## Lacunas identificadas

1. **BR normativo/cédula (1930-1942)**: cédulas da Era Vargas com alegorias femininas
2. **BR normativo/selo**: selos postais brasileiros com efígie da República (série "Cabeça da Liberdade" de 1891 — já temos SCOUT-410)
3. **BR fundacional/medalha**: medalhas comemorativas da Proclamação da República (1889-1892)
4. **BR cédula/Cruzeiro**: verificar se as cédulas de Cruzeiro (1942+) mantêm alegorias femininas ou transitam para figuras históricas masculinas
5. **100 Mil Réis cédula**: referência encontrada com medalhão de Marianne + grupo de três mulheres (Ciência, Agricultura, Comércio) — não foi possível confirmar detalhes (Numista 403)

## Proximas buscas sugeridas

1. `BR selo "cabeça da liberdade" OR "efígie da República" 1891 1906` — completar lacuna selo
2. `BR medalha "proclamação da república" 1889 1890 alegoria feminina` — medalhas fundacionais
3. `BR cedula Cruzeiro alegoria feminina 1942 1967` — transição fundacional→normativo no papel-moeda
4. `BR cedula "100 Mil Réis" 1890 Marianne Ciência Agricultura Comércio` — confirmar candidato potencial

## Flags de atencao

- Numista retornando 403 para WebFetch — necessita acesso manual ou Playwright para contornar
- SCOUT-424 tem confiança média por falta de imagem de alta resolução — necessita verificação visual
- Normalização de país/suporte no corpus-data.json precisa de limpeza (múltiplas grafias)
