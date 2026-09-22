# Output — Prompt 1: Tese "A Monarca como Alegoria Forçada"
**Data:** 20 de Julho de 2026  
**Status:** Concluído (scout + parágrafo + cards provisórios)  
**Próximo:** Aguarda Prompt 2 (antítese) para síntese.

---

## Parágrafo Argumentativo (~500 palavras)

Quando o Estado coloca uma mulher real e soberana na face de uma moeda, ele não está apenas "representando a nação por uma mulher" — está realizando uma **alegorização forçada**. A operação exige que a figura feminina seja um *signo vazio* (Marianne, Justiça, Liberdade) para receber a projeção da soberania. A monarca real, porém, *enche* o signo com biografia, carne, envelhecimento, política partidária. Para que ela funcione como moeda, o Estado precisa submetê-la a um **endurecimento corporal radical**: pose fixa, perfil numismático imutável, apagamento da expressão, congelamento da idade. A mulher real vira *estátua* para poder funcionar como *moeda*.

Os casos scoutados confirmam essa lógica. A **Rainha Vitória** no retrato "Old Head" (3ª efígie, 1895–1901) aparece aos 76 anos, com véu longo, diadema imperial, expressão congelada e perfil rigidamente esquerdo. A efígie foi adaptada de um modelo de Joseph Edgar Boehm para o Jubileu de Ouro (1887) e manteve-se inalterada nos últimos seis anos de seu reinado — a imagem da rainha idosa foi *fixada* no metal enquanto a mulher continuava envelhecendo. Os indicadores de endurecimento atribuídos são: rigidez_postural=3, uniformizacao_facial=3, dessexualizacao=3, monocromatizacao=3, apagamento_narrativo=2. **Score provisório: 2.8/3.**

**Maria I** nas moedas de 6400 Réis (ouro, 1789–1805) e 10 Réis (cobre, 1791–1799) aparece com véu de viúva e coroa, busto voltado à direita, legendas em latim ("MARIA I D G PORT ET ALG REGINA"). O véu funciona como *marcador de luto* que neutraliza a maternidade e a sexualidade da rainha, reduzindo-a a função de "Rainha pela Graça de Deus". Score provisório: 2.0/3.

**Elizabeth II** na 5ª efígie definitiva (Jody Clark, 2015) usa o Royal Diamond Diadem, perfil direito, expressão contida, sem sorriso. Apesar de ser a efígie mais "realista" das cinco, o processo de seleção pelo Royal Mint Advisory Committee (RMAC) exigiu que o retrato fosse "respeitoso" e "não excessivamente idealizado" — ou seja, a idade da rainha (89 anos) teve de ser *reconhecida* mas não *mostrada*. Score provisório: 1.7/3.

A comparação com o baseline do corpus (N=15 alegorias abstratas, score médio 2.1) revela o paradoxo: a **Purificação Clássica atinge endurecimento comparável em corpos reais e fictícios**. A República *fabrica* o corpo endurecido (Marianne); a Monarquia *esvazia* o corpo real até atingir a mesma dureza. O *Contrato Sexual Visual* não distingue entre alegoria e pessoa — ele exige, em ambos os regimes, que a mulher no suporte estatal deixe de ser *mulher* para ser *moeda*.

---

## Cards de Caso (provisórios)

### Caso 1 — Vitória "Old Head" (1895–1901)
| Campo | Valor |
|-------|-------|
| **ID corpus** | `PENDING` (scout externo, sem entrada em `records.jsonl`) |
| **Tipo** | Moeda padrão (1 Penny, bronze) |
| **Material** | Bronze |
| **Data de emissão** | 1895–1901 |
| **Regime iconográfico** | `monarquico` (proposto) |
| **Endurecimento score** | **2.8/3** (provisório) |
| **Indicadores atribuídos** | rigidez_postural=3, uniformizacao_facial=3, dessexualizacao=3, monocromatizacao=3, apagamento_narrativo=2 |
| **URL imagem** | https://en.numista.com/670 |
| **Nota de atribuição** | Retrato baseado em modelo de Boehm (1887), mantido inalterado por 6 anos. Véu longo + diadema + perfil congelado = endurecimento corporal extremo. |

### Caso 2 — Maria I (6400 Réis, 1789–1805)
| Campo | Valor |
|-------|-------|
| **ID corpus** | `PENDING` (scout externo) |
| **Tipo** | Moeda padrão (ouro) |
| **Material** | Ouro (.917) |
| **Data de emissão** | 1789–1805 |
| **Regime iconográfico** | `monarquico` (proposto) |
| **Endurecimento score** | **2.0/3** (provisório) |
| **Indicadores atribuídos** | rigidez_postural=3, heraldizacao=2, inscricao_estatal=1, dessexualizacao=2 |
| **URL imagem** | https://en.numista.com/36273 |
| **Nota de atribuição** | Véu de viúva como marcador de luto que apaga maternidade/sexualidade. Legendas em latim reforçam inscrição estatal. |

### Caso 3 — Elizabeth II (5ª efígie, Clark, 2015)
| Campo | Valor |
|-------|-------|
| **ID corpus** | `PENDING` (scout externo) |
| **Tipo** | Moeda padrão (definitiva) |
| **Material** | Diversos (bronze, cuproníquel) |
| **Data de emissão** | 2015–2022 |
| **Regime iconográfico** | `monarquico` (proposto) |
| **Endurecimento score** | **1.7/3** (provisório) |
| **Indicadores atribuídos** | rigidez_postural=2, uniformizacao_facial=2, serialidade=1, dessexualizacao=2 |
| **URL imagem** | https://www.royalmint.com/stories/collect/the-coinage-portraits-of-her-late-majesty-queen-elizabeth-ii--the-artists-stories/ |
| **Nota de atribuição** | Processo do RMAC exigiu retrato "respeitoso" mas não idealizado. Diadema + perfil direito = continuidade da tradição. |

---

## Baseline do Corpus (alegorias abstratas)

| Estatística | Valor |
|-------------|-------|
| **N** | 15 |
| **Score médio** | 2.1 |
| **Score mínimo** | 0.5 |
| **Score máximo** | 3.0 |
| **Regimes** | normativo (13), contra-alegoria (1), fundacional (1) |

---

## Próximos Passos

1. **Aguardar Prompt 2** (antítese Kantorowicz) — subagente `deleg_1ed80148` em execução.
2. **Quando Prompt 2 chegar:** avaliar qualidade do contra-argumento. Se genérico, adicionar bridge paragraph conectando Kantorowicz ao meio numismático.
3. **Despachar Prompt 3** (síntese) com contexto completo de ambos os outputs.
4. **Coding oficial:** submeter os 3 casos a `code_purification.py` para scores canônicos (não provisórios).
