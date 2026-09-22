# Varredura de Recusas — Corpus ICONOCRACIA v2

**Data:** 24 de julho de 2026  
**Método:** recodificação score→inventário (328 registros) + varredura completa de recusas com verificação visual  
**Hipótese testada:** REMASCULINIZAÇÃO — quando o corpo feminino de Estado é recusado, o que entra no lugar é masculino ou masculino-animal.

## O que mudou no corpus

- **Campo `endurecimento_score` removido dos 328 registros.** Os artefatos 0,0 e 1,4 do pipeline hermes-auto deixaram de existir.
- **Os 10 indicadores viraram inventário qualitativo** (grau em palavras: ausente/mínimo/moderado/pronunciado/extremo). Nenhuma média, nenhuma soma.
- **Novo campo `recusa`** com inventário do substituto para cada caso verificado.

## O achado central: a remasculinização é parcial — e isso é a descoberta

Dos 26 candidatos triados, **13 confirmados como recusa genuína** (13 eram falsos positivos: corpo feminino presente, apenas satirizado — ou inacessível). Dos 13 confirmados:

- **7 confirmam a remasculinização** (substituto masculino/masculino-animal)
- **6 são contra-exemplos** — e definem os limites do padrão

A hipótese não vale como lei universal. Vale como **um de vários mecanismos de recusa** — e a tipologia que emerge é mais rica que a hipótese original:

| Mecanismo | O que entra no lugar do corpo | Casos |
|-----------|------------------------------|:-----:|
| **Remasculinização por substituição** | águia, perfil do rei, esqueleto-Morte, clero, mãos masculinas armadas | 6 |
| **Remasculinização por deslocamento** (limítrofe) | juízo moral transferido a homens humanos, sem emblema (US-020) | 1 |
| **Negação pura (vazio)** | nada — o corpo é destruído/removido e não substituído | 3 |
| **Feminino-esvaziado** | o feminino reciclado degradado (Anastasie) ou reivindicado | 2 |
| **Neutro-abstrato** | esfera celeste, constelação (brasão do Brasil) | 1 |

> Nota de codificação: **US-020** é um caso limítrofe — marcado \`remasculinizacao: true\` porque a autoridade moral passa a homens humanos, mas *sem* substituto heráldico. Você deve decidir se conta como remasculinização (deslocamento para corpos masculinos) ou como negação pura. É o tipo de fronteira que só a sua leitura resolve.

## Por que os contra-exemplos são o mais valioso

O modelo do score nunca poderia ter produzido isto — ele achataria tudo num número. A varredura revelou que **recusar não é uma coisa só**:

1. **Substituição vs. negação são processos distintos.** A águia de Weimar (DE-018) e o assignat (FR-ASSIGNAT) *substituem* o corpo por masculino-animal. Mas a Marianne mutilada do Arco do Triunfo (0970108c) e o busto vandalizado do STF (e0399402) *não substituem nada* — produzem um vazio. Destruição pura e remasculinização são gestos diferentes, com significados jurídico-políticos diferentes.

2. **Anastasie complica o gênero da recusa.** Quando a recusa precisa de rosto (FR-031), ela não masculiniza — recicla o feminino numa velha cega e degradada, a anti-Marianne. O feminino é usado *contra* si mesmo.

3. **A inversão mexicana (SCOUT-571).** No Paseo de la Reforma a lógica se inverte: é o corpo *masculino* colonial (Colombo) que é recusado, e uma alegoria *feminina* de justiça é instalada em seu lugar — com o cancelamento explícito de um projeto de substituição por figuras masculinas. A remasculinização tem, portanto, seu reverso histórico contemporâneo.

4. **O brasão brasileiro (SCOUT-562)** substitui o corpo por abstração celeste — nem masculino nem feminino. Um limite neutro do padrão.

## Tabela dos 13 confirmados

| ID | Caso | Espécie | Substituto | Remasc. |
|----|------|---------|-----------|:-------:|
| `0970108c-16` | Marianne / La Marseillaise (François Rud | recusa-iconoclástica | nenhum substituto figurativo — o corpo não é r | — |
| `BE-5F-LEOPO` | 5 Francs — Léopold I (founding coin of B | ausência | retrato/perfil do rei Leopoldo I | ✓ |
| `DE-018` | 1 Reichsmark — Weimar Republic (eagle re | substituição-heráldica | águia (Reichsadler) acima da data, sem coroa i | ✓ |
| `FR-031` | Madame Anastasie (avec les ciseaux de la | recusa-iconoclástica | Madame Anastasie — velha corcunda, cega/surda  | — |
| `FR-032` | La Paix — Idylle | recusa-iconoclástica | esqueleto da Morte (figura masculinizada/gende | ✓ |
| `FR-033` | L'Empire c'est la paix | recusa-iconoclástica | nenhum corpo — campo de ruínas, fumaça e cadáv | — |
| `FR-ASSIGNAT` | Assignat de 400 livres (21 nov. 1792, an | substituição-heráldica | águia republicana segurando fasces com barrete | ✓ |
| `SCOUT-562` | Brasão da República dos Estados Unidos d | substituição-heráldica | escudo circular azul-celeste com a constelação | — |
| `SCOUT-571` | Intervenção feminista no Paseo de la Ref | recusa-iconoclástica | escultura de madeira roxa de uma mulher com pu | — |
| `US-019` | Liberty Is Not Anarchy | recusa-iconoclástica | mãos desincorporadas empunhando espada com águ | ✓ |
| `US-020` | Looking Backward | ausência | nenhum — vazio; a cena é ocupada inteiramente  | ✓ |
| `ce773ab1-3b` | La verdad ha muerto (Truth has died) | recusa-iconoclástica | clero (bispo com mitra, monges, clérigos) — fi | ✓ |
| `e0399402-b5` | A Justiça (interior) — Escultura em bron | recusa-iconoclástica | nenhum — vazio; o painel de onde a escultura f | — |

## Correções de catalogação encontradas na varredura

- `DE-015`: a descrição do corpus dizia Alsácia/Lorena em trajes femininos; a imagem mostra **dois meninos** — Germania está presente e central. Não era recusa.
- `BR-019` (voto feminino): domínio `memoria.bn.br` inexistente (NXDOMAIN) — link morto, marcado inacessível.
- `SCOUT-567`: sem elemento hídrico figurativo; o azul é celeste, não aquático — hipótese sem base factual.
- `e0399402`: distinção confirmada entre a Justiça interior de bronze (1975, vandalizada em 8/1/2023) e a estátua externa de granito (1961).

## Consequência para a espinha da tese

O capítulo **Recusas** não deve defender a remasculinização como tese única, mas como **o mais forte de quatro mecanismos**. A estrutura ganha uma tipologia interna: substituição remasculinizante · negação pura · feminino-esvaziado · abstração neutra. Cada uma responde a uma pergunta jurídico-política distinta sobre o desconforto do Estado com o corpo que ele próprio escolheu como máscara.