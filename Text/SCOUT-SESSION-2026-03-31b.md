---
tipo: sessao-scout
data: "2026-03-31"
sessao: "2026-03-31b"
total_candidatos: 4
total_controles_negativos: 1
total_zwischenraum: 2
tags:
  - corpus/sessao-scout
---

# SCOUT Session — 2026-03-31b

## Sumário

Sessão focada em preencher lacunas críticas: **moedas, papel-moeda, e o caso Weimar**.

### Candidatos adicionados

| ID | Título | País | Suporte | Regime |
|---|---|---|---|---|
| SCOUT-114 | $2 Educational Series: Science Presenting Steam and Electricity | US | papel-moeda | normativo |
| SCOUT-115 | $5 Educational Series: Electricity Presenting Light to the World | US | papel-moeda | normativo |
| SCOUT-116 | Semeuse 1 Franc — Oscar Roty silver coin | FR | moeda | normativo |
| SCOUT-117 | Notgeld Bielefeld — Jungbrunnen silk note | DE | papel-moeda | fundacional |

### Controles negativos

| ID | Título | País | Significado |
|---|---|---|---|
| SCOUT-NC-03 | Weimar Republic 1 Reichsmark | DE | Germania desaparece — substituída por águia heráldica |

### Zwischenraum panels

| ID | Título | Polos | Argumento |
|---|---|---|---|
| SCOUT-ZW-10 | Electricity vs Semeuse | US $5 × FR 1F | Limiar do corpo tolerável — dessexualização como variável decisiva |
| SCOUT-ZW-11 | Semeuse vs Reichsmark | FR 1F × DE 1RM | Presença x Ausência — iconocracia como fenômeno contingente, não universal |

## Descobertas-chave

### 1. O limiar da dessexualização (ZW-10)
A $5 Educational (score endurecimento 1.9) e a Semeuse (score 2.5) diferem em apenas 0.6 pontos — mas a primeira foi banida em 3 anos e a segunda sobrevive há 120+. A variável decisiva é a dessexualização (0 vs 3).

### 2. A iconocracia não é universal (ZW-11)
A República de Weimar elimina TODA alegoria feminina da moeda oficial — substituindo por águia heráldica. A iconocracia (uso do corpo feminino como imagem soberana) é um fenômeno **francês** por excelência, não uma necessidade republicana.

### 3. Os Notgeld como válvula (SCOUT-117)
Quando o Estado central abandona a alegoria feminina, os municípios a recuperam nos Notgeld — com corpos MENOS endurecidos (score 0.4 vs 2.5 da Semeuse). O endurecimento se inverte na descentralização.

### 4. O corpus agora tem moedas e papel-moeda
Antes desta sessão: 0 moedas, 0 papel-moeda no corpus. Agora: 1 moeda (Semeuse), 3 papel-moeda (Educational $2, $5, Notgeld). Suportes massificados fundamentais para o argumento da serialidade.

## Estado do corpus

| Métrica | Valor |
|---|---|
| Total corpus-data.json | 93 items |
| Vault candidatos | ~50 |
| Vault ZW panels | 16 |
| Controles negativos | 3 |
| Países cobertos | 9 |

## Integração técnica realizada

- Fixed Python 3.9 compat (added `from __future__ import annotations`) in scripts
- Fixed Worker PUT bug in companion `/api/corpus` endpoint
- Wired companion HTML to fetch live data from `/api/corpus` and `/api/atlas`
- Added `--push` option to sync_companion.py
- Generated companion-data.json and atlas-mapping.json
- Fixed hook commands (removed emojis + `#`-prefixed text causing permission errors)
- Ran atlas_mapping.py: 14 ZW panels mapped to 8 thesis panels

## Lacunas identificadas

1. **SCOUT-117 #verificar-imagem** — Notgeld Bielefeld precisa de URL verificável
2. **FR Semeuse 50c e 2F** — Temos o 1F, faltam as outras denominações
3. **FR Semeuse vs Semeuse selo** — Comparação moeda/selo do mesmo design (potencial ZW panel)
4. **US $1 Educational** — Already in corpus? Verificar se o trio está completo
5. **DE Weimar selos** — O que acontece com a alegoria feminina nos selos de Weimar?
6. **UK moedas** — Britannia em moedas (penny, crown) — não temos nenhuma moeda UK

## Próximos passos

1. UK coins — Britannia on the penny, florin, crown
2. BR moedas — Efígie da República em cruzeiros
3. Semeuse selo × moeda Zwischenraum
4. Verificar Notgeld com URL confiável
5. Run `iconocode_to_corpus.py --write` quando análises existirem
