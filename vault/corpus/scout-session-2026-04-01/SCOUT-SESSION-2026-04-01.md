---
id: SCOUT-SESSION-2026-04-01
tipo: sessao-scout
data: 2026-04-01
query_executada: "Campanha numismática: preencher lacunas em MILITAR (moedas, medalhas) e moeda/papel-moeda (todos os regimes) nos 6 países do corpus"
total_candidatos: 8
pais: [UK, FR, US, BE, BR]
periodo: "1860-1937"
tags:
  - corpus/sessao-scout
  - protocolo
  - suporte/moeda
  - suporte/papel-moeda
  - lacunas
related:
  - "[[DB1 Corpus Iconográfico]]"
  - "[[IconoCode -- Protocolo]]"
  - "[[ENDURECIMENTO]]"
---

## Resumo da sessão

**Query:** Campanha numismática para preencher lacunas em MILITAR e moeda/papel-moeda
**Acervos consultados:** Numista, WebSearch (Heritage Auctions, CoinWeek, Wikipedia, Museum Victoria, Smithsonian)
**Candidatos encontrados:** 8
**Nível de confiança predominante:** alto

## Candidatos

| ID | Título | País | Suporte | Regime | Confiança |
|----|--------|------|---------|--------|-----------|
| SCOUT-067 | British Trade Dollar — Britannia | UK | moeda | MILITAR | alto |
| SCOUT-068 | Piastre de Commerce — Marianne | FR | moeda | MILITAR | alto |
| SCOUT-069 | Standing Liberty Quarter — Liberty | US | moeda | MILITAR | alto |
| SCOUT-070 | 5 Francs Independence — La Belgique | BE | moeda | FUNDACIONAL | alto |
| SCOUT-071 | 2000 Réis — Efígie da República | BR | moeda | NORMATIVO | alto |
| SCOUT-072 | Penny — Britannia Seated | UK | moeda | NORMATIVO | alto |
| SCOUT-073 | 5 Francs Hercule — République et Justice | FR | moeda | FUNDACIONAL | alto |
| SCOUT-074 | 20 Francs Belgian Congo — Europe et Afrique | BE | papel-moeda | MILITAR | alto |

## Impacto no corpus

| Métrica | Antes | Depois (se aceitos) |
|---------|-------|---------------------|
| **Total items** | 95 | 103 |
| **Moeda** | 2 | 8 (+6) |
| **Papel-moeda** | 4 | 5 (+1) |
| **MILITAR** | 10 | 14 (+4) |
| **BE items** | 4 | 6 (+2) |
| **UK moeda** | 0 | 2 (+2) |
| **BR moeda** | 0 | 1 (+1) |

## Zwischenraum potenciais identificados

1. **ZW: Britannia sentada vs. Britannia de pé** — SCOUT-072 (Penny, NORMATIVO, metrópole) vs. SCOUT-067 (Trade Dollar, MILITAR, colônia). Mesma alegoria, mesmo atributo (tridente+escudo), transição postural sentada→de pé correlaciona com metrópole→colônia.

2. **ZW: Standing Liberty Type I vs. Type II** — SCOUT-069 internamente: seio nu (1916) vs. cota de malha (1917). ENDURECIMENTO documentável em tempo real, dessexualização forçada.

3. **ZW: La Belgique constitucional vs. La Belgique colonial** — SCOUT-070 (5 Francs 1880, FUNDACIONAL) vs. SCOUT-074 (Congo 20 Francs, MILITAR). Mesma alegoria nacional, da fundação à colonização.

4. **ZW: Moedas de comércio colonial** — SCOUT-067 (British Trade Dollar) vs. SCOUT-068 (Piastre de Commerce). Britannia de pé vs. Marianne sentada — duas estratégias imperiais de alegorização feminina para Ásia.

## Lacunas remanescentes

- **DE moeda:** Nenhuma moeda alemã com alegoria feminina encontrada — o Kaiserreich usa apenas a águia imperial nos Marks. A **ausência** de Germania nas moedas é em si significativa (`#ausencia-alegorica`).
- **MILITAR selo:** Nenhum selo postal militar no corpus.
- **UK selo:** Nenhum selo britânico no corpus (Britannia nos selos existe: Machin head é a rainha, mas existem Britannia definitives).
- **BR selo:** Selos brasileiros com alegorias republicanas (República com barrete frígio).
- **Medalhas comemorativas:** Nenhuma medalha no corpus — suporte rico para regimes FUNDACIONAL e MILITAR.

## Próximas buscas sugeridas

1. **Selos postais com alegorias femininas** — FR (Semeuse selo), UK (Britannia definitives), BR (selos República Velha), DE (Germania selo 1900-1922)
2. **Germania selo 1900-1922** — a Germania aparece nos SELOS do Kaiserreich (Reichspost), não nas moedas — lacuna importante
3. **Medalhas de guerra e fundação** — FR medalhas WWI com Marianne, US medalhas com Columbia, BE medalhas independência
4. **Moedas coloniais adicionais** — British West Africa, French West Africa (AOF), East Africa — alegorias projetadas sobre África

## Flags de atenção

- Numista bloqueia WebFetch (403) — todas as URLs precisam verificação manual
- Standing Liberty Quarter URL precisa confirmação (`#verificar`)
- Datas da nota do Congo Belga precisam refinamento (`#verificar`)
- **Ausência de Germania nas moedas alemãs** merece nota teórica dedicada
