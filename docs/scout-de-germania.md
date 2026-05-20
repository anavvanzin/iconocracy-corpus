# Campanha SCOUT-DE — A Curva Diacrônica de Germania (1848–1925)

*Relatório de Análise Iconométrica e Metodológica para a Tese de Doutorado de Ana Vanzin*

---

## 1. Contexto e Problema de Pesquisa

A alegoria de **Germania** constitui o caso mais nítido de variação diacrônica no *iconocracy-corpus*. Enquanto a *Marianne* francesa experimentou múltiplos abrandamentos e oscilações ao longo de suas repúblicas, Germania apresenta uma trajetória linear e contínua em direção ao **endurecimento máximo**, culminando em sua **extinção visual abrupta** após a queda do Império em 1918.

Esta campanha (**SCOUT-DE**) foi executada para mapear e medir a curva do Índice de Endurecimento (IE) — ou Score de Purificação Composto ($I_{pc}$) — ao longo de um arco temporal de 77 anos, do nascimento da alegoria na Paulskirche de Frankfurt (1848) à sua eliminação burocrática pela República de Weimar (1925).

---

## 2. A Série Diacrônica de Germania no Corpus

Adicionamos e revisamos a codificação dos seguintes itens no banco de dados para calibrar toda a trajetória:

| Item ID | Ano | Título do Suporte | Regime Iconocrático | Score $I_{pc}$ |
|---|---|---|---|---|
| `72c21b13-55b2...` | 1848 | Germania (Philipp Veit, Pintura Paulskirche) | **FUNDACIONAL** | **0.4** |
| `f4a4e50f-0c41...` | c. 1871 | Germania — Guter Rat ist teuer (Cartoon Kladderadatsch) | **CONTRA-ALEGORIA** | **0.8** |
| `f96693a2-99a6...` | 1900 | Selo Definitivo Germania 10 Pfennig (Kaiserreich) | **MILITAR** | **2.8** |
| `7dea14ce-d3b8...` | 1900 | Selo Definitivo Germania 5 Pfennig (Kaiserreich) | **MILITAR** | **2.8** |
| `be91e95b-9083...` | 1908 | 100 Mark Reichsbanknote (Germania Sentada) | **NORMATIVO** | **2.0** |
| `dd0e6773-94a5...` | 1908 | Moeda de 5 Mark Wilhelm II (Kaiserreich) | **MILITAR** | **2.8** |
| `e3479a03-4866...` | 1910 | 1000 Mark Reichsbanknote (Alegorias) | **NORMATIVO** | **2.0** |
| `f78e3dff-d7b9...` | 1914 | Germania (Pintura de F. A. von Kaulbach) | **NORMATIVO** | **1.5** |
| `99a7c9ba-d743...` | WWI | Germania "Belgien" Overprint (Selo de Ocupação) | **MILITAR** | **2.8** |
| `f049b319-a096...` | 1919 | 50 Mark Reichsbanknote (Young Girl / Weimar) | **NORMATIVO** | **2.2** |
| `3f7d2171-8dbb...` | 1920 | Selo Germania Weimar Mi.141 (Weimar) | **NORMATIVO** | **2.7** |
| `c9d3a591-3572...` | 1925 | Moeda 1 Reichsmark (Águia de Weimar - Controle) | **NORMATIVO** (Ausência) | **0.0** |

---

## 3. Análise da Trajetória Iconométrica

A variação de $I_{pc}$ (composta por 10 sub-indicadores que medem desde a monocromatização e rigidez postural até a dessexualização e apagamento narrativo) descreve três momentos cruciais:

```
Score I_pc
  ^
3.0|         [Selo 1900 / Moeda 1908] (I_pc=2.8) -------- [WWI Belgien] (I_pc=2.8)
   |                /                                  \
2.0|               /    [Banknotes 1908/1910] (I_pc=2.0) \-------- [Weimar Stamp 1920] (I_pc=2.7)
   |              /                                       \
1.0| [Satírico 1871] (I_pc=0.8)                             \
   |      /                                                  \
0.0| [Veit 1848] (I_pc=0.4)                                    \--> [Weimar Eagle 1925] (I_pc=0.0)
   +------------------------------------------------------------------------------------> Tempo
```

### 1. Emergência e Instabilidade (1848–1871)
No quadro de Philipp Veit (`DE-VEIT-1848`), a alegoria é carregada de expressividade humana (cabelos ao vento, olhar emotivo, seios proeminentes em trajes românticos, movimento dinâmico). O score $I_{pc} = 0.4$ define o polo revolucionário da escala: a imagem serve à convocação cívica e à utopia da unificação nacional. A sátira de 1871 (`f4a4e50f-0c41...`) opera com $I_{pc} = 0.8$ como uma contra-alegoria, resistindo ao aprisionamento estrito da imagem solene.

### 2. A Blindagem do Kaiserreich (1900–1914)
Após a unificação bismarckiana, o corpo revolucionário de Germania é capturado pelo aparato de Estado e endurecido. Paul Waldraff desenha a efígie de Germania (`f96693a2-99a6...`) vestindo armadura metálica pesada, coroa imperial otoniana e empunhando espada. O score dispara para **2.8** nos selos e nas moedas imperiais. O corpo feminino é metalizado e dessexualizado — sua presença cívica serve à purificação de estado máxima. As cédulas de papel-moeda de 1908 e 1910 mantêm scores estáveis em **2.0**, refletindo a inércia do regime burocrático e normativo.

### 3. A Fissura e Extinção em Weimar (1919–1925)
Com a derrota em 1918 e a instauração da República de Weimar, ocorre um fenômeno paradoxal:
* O selo postal de Weimar (`3f7d2171-8dbb...`) mantém a efígie de Germania com score **2.7** por pura inércia material e infraestrutural. A hiperinflação obrigou o reaproveitamento das chapas de impressão antigas, demonstrando o **determinismo do suporte postal**.
* A moeda de Weimar de 1924–1925 (`c9d3a591-3572...`) realiza a ruptura definitiva: **o corpo de Germania é inteiramente abolido** e substituído pela águia de Weimar (*Reichsadler*), zerando o score de purificação composto ($I_{pc} = 0.0$).

---

## 4. Discussão Teórica: A Hipótese do Endurecimento Autorruinoso

O estudo detalhado da série de Germania permite testar empiricamente uma nova formulação para a tese: **a hipótese do endurecimento autorruinoso**.

Sob regimes liberais com fraco acoplamento normativo, o corpo feminino alegórico retém alguma flexibilidade expressiva, o que paradoxalmente garante sua resiliência histórica (como a Semeuse francesa que transita suavemente entre repúblicas e moedas). No entanto, sob o regime imperial prussiano de centralização máxima, o processo de purificação iconográfica de Germania seguiu a curva de um *sistema sob estresse*:
1. **Metalização Total**: O corpo da mulher foi transformado em armadura e heráldica.
2. **Perda de Subjetividade**: As feições foram idealizadas e endurecidas ao ponto de máscara pura.
3. **Equivalência Semiótica Absoluta**: A alegoria tornou-se idêntica ao próprio Estado Imperial.

Quando o Império ruiu em 1918, a equivalência visual absoluta revelou o seu limite estrutural: **o corpo de Germania estava tão fundido ao militarismo estatal que se tornou impossível utilizá-lo como suporte da nova República de Weimar**. Weimar não pôde abrandar Germania de volta a 1848, porque seu repertório iconográfico fora permanentemente monopolizado pelo Kaiserreich. 

A única solução semiótica para Weimar foi a **desincorporação total** (a ausência alegórica), substituindo o corpo feminino pelo signo geométrico e heráldico da águia. O endurecimento máximo da Feminilidade de Estado levou, portanto, à sua própria autodestruição visual e obsolescência material.

---

*Este relatório de pesquisa consolida a campanha SCOUT-DE e está conectado aos dados compilados em `corpus/corpus-data.json`.*
