---
titulo: "Análise Quantitativa: Padrões Iconométricos"
parte: "III - Resultados"
capitulo: 6
status: "rascunho"
palavras: 1200
citacoes: 0
updated: "2026-04-15"
pandoc:
  reference-doc: "template.docx"
  csl: "abnt.csl"
  bibliography: "references.bib"
---

# Capítulo 6 - Análise Quantitativa: Padrões Iconométricos

Este capítulo tem como objetivo apresentar os resultados da aplicação do protocolo *IconoCode* ao corpus da pesquisa, traduzindo as categorias iconográficas desenvolvidas nos capítulos anteriores em variáveis mensuráveis. Longe de pretender uma exatidão matemática sobre objetos visuais historicamente contingentes, a iconometria aqui proposta funciona como uma ferramenta heurística: ela permite visualizar padrões de longa duração e continuidades transatlânticas que escapariam à análise qualitativa de imagens isoladas.

## 6.1 - Panorama descritivo do corpus e do grau de purificação

O corpus analisado é composto por 145 artefatos visuais codificados integralmente, englobando suportes que transitam desde a grande estatuária oficial até a numismática e o meio impresso. O recorte geográfico reflete o circuito hegemônico de produção da cultura jurídica ocidental moderna, com predominância da França (42 itens) e dos Estados Unidos (20 itens), seguidos por Alemanha (18), Brasil (12), Reino Unido (10) e Itália (8).

A métrica central desta análise é o *score* composto de endurecimento (variando teoricamente de 0 a 3), que agrega os dez indicadores ordinais de purificação corporal. No conjunto global do corpus, a média de endurecimento situa-se em 1.44 (com dispersão de 0.10 a 3.10). Contudo, esse valor médio oculta variações cruciais quando os artefatos são agrupados por regime iconocrático.

O corpus distribui-se de maneira desigual entre os quatro regimes identificados: o regime *fundacional* é o mais populoso (71 itens), refletindo a proliferação de imagens no calor das rupturas constitucionais ou revolucionárias; segue-se o regime *normativo* (40 itens), característico da consolidação e rotinização do poder estatal; o regime *militar* ou imperial (27 itens); e, marginalmente, as *contra-alegorias* (7 itens), que funcionam como o reverso subversivo da iconografia oficial.

A análise das correlações internas ($\rho$ de Spearman) entre os dez indicadores revela que o processo de "purificação" estatal não opera de forma isolada sobre partes do corpo, mas como um "pacote" integrado de disciplinamento. As correlações mais fortes ocorrem entre a *rigidez postural* e a *uniformização facial* ($\rho = 0.750$), bem como entre a *dessexualização* e a *uniformização facial* ($\rho = 0.738$). Isso demonstra que a captura do corpo feminino pela linguagem do Estado exige, simultaneamente, o congelamento da espinha dorsal e o apagamento das particularidades do rosto e do sexo. A carne que se faz lei perde, antes de tudo, sua mobilidade e seu desejo.

## 6.2 - Regimes iconocráticos e morfologia corporal: Análise de variância (Kruskal-Wallis)

Para testar estatisticamente a hipótese de que diferentes momentos da cultura jurídica produzem diferentes morfologias corporais, aplicou-se o teste não-paramétrico de Kruskal-Wallis. Os resultados são contundentes: para 9 dos 10 indicadores de purificação, a hipótese nula de igualdade entre as distribuições foi rejeitada com altíssima significância estatística ($p < 0.05$). A única exceção foi o indicador de *enquadramento arquitetônico* ($H = 4.48, p = 0.106$), sugerindo que o uso de nichos, pedestais ou molduras não discrimina adequadamente o regime político, consistindo em uma técnica transversal da gramática arquitetônica oficial.

Os testes *post-hoc* de Dunn (com correção de Bonferroni) revelaram o exato ponto de fratura na iconocracia. Há uma cisão clara: os regimes *militar* e *normativo* operam em um patamar de endurecimento corporal severamente superior ao do regime *fundacional*.

No momento fundacional da lei (como as imagens da primeira República francesa ou os esboços da República brasileira), o corpo alegórico retém traços de fluidez, movimento e corporalidade - o caos originário ainda pulsa na imagem. No entanto, quando a ordem jurídica se consolida (regime normativo, média de endurecimento = 1.82) ou se impõe pela força armada (regime militar, média = 1.80), o corpo sofre uma mineralização. Os testes confirmam que a diferença entre o regime normativo e o fundacional é estatisticamente significativa para indicadores vitais como a dessexualização ($p = 0.0004$) e o apagamento narrativo ($p = 0.0003$). A lei estabilizada exige, visualmente, um corpo inerte.

## 6.3 - Preditores do endurecimento: Regressão e o papel do suporte material

A fim de isolar o efeito do regime iconocrático em relação a outros fatores, construiu-se um modelo de regressão (Ordinary Least Squares - OLS) tendo o *score* composto de endurecimento como variável dependente ($R^2$ ajustado = 0.451).

O modelo confirmou as intuições visuais: a materialidade do suporte exerce um poder ditatorial sobre a forma do corpo jurídico. A mídia da numismática (moedas e medalhas) atua como um fortíssimo preditor do endurecimento corporal (coeficiente $\beta = 0.797, p < 0.001$). A moeda não apenas miniaturiza a alegoria; sua ontologia circulante e metálica exige um grau extremo de dessexualização e heraldicização para garantir a legitimação serial do valor do Estado. Em contrapartida, as mídias da pintura e do desenho predizem um *relaxamento* dos indicadores de purificação ($\beta = -0.529, p < 0.01$). O óleo sobre tela abriga a carne; a numismática exige o brasão.

Ainda controlando pelo suporte material, a regressão demonstra que o tipo de regime permanece como um preditor altamente significativo. Em comparação com as contra-alegorias (usadas como *baseline*), a passagem para o regime normativo impulsiona drasticamente o congelamento do corpo ($\beta = 0.818, p < 0.001$).

Quando se analisa qual indicador possui maior peso preditivo para o *score* composto geral, a *uniformização facial* ($\rho = 0.855$) e a *rigidez postural* ($\rho = 0.820$) emergem como os vetores primários. O Estado moderno, ao converter corpos femininos em avatares da Justiça e da República, realiza sua operação ideológica mais violenta não apenas ao cobrir a figura, mas ao petrificar seu rosto em uma simetria inexpressiva e alinhar sua coluna a um eixo estritamente ortogonal.

## 6.4 - Circulação transatlântica e o espaço das correspondências

A Análise de Correspondência Múltipla (MCA) permitiu mapear as distâncias multivariadas entre os itens do corpus, integrando período histórico, país, suporte, regime e nível de endurecimento. A inércia explicada pelas primeiras dimensões, embora limitada matematicamente (típico de MCA com variáveis densas), desenha uma topologia clara do imaginário jurídico transatlântico.

No espaço Euclidiano projetado pelo algoritmo, itens periféricos ou de expansão ultramarina muitas vezes adotam um grau superlativo de endurecimento para compensar sua posição subordinada ou justificar a dominação. Entre os artefatos com maior distância da origem no mapa de correspondências, encontra-se a alegoria colonial belga (BE-CONGO-1912), perfeitamente alinhada ao quadrante militar de alto endurecimento, assim como a *Britannia* da expansão imperial comercial britânica do final do século XIX (UK-TRADE-1895). Ao mesmo tempo, no extremo oposto do gráfico, agrupam-se as caricaturas e contra-alegorias francesas (como FR-031 e FR-032), que subvertem a gramática visual desincorporando a alegoria de seu pedestal estatal ou devolvendo-lhe as paixões narrativas.

## 6.5 — Limites da quantificação: o que os números não dizem

A iconometria, embora desvele padrões morfológicos ocultos sob a poeira dos arquivos, esbarra em um limite epistemológico essencial. O número captura a rigidez postural, mas não captura a raça; ele quantifica o enquadramento arquitetônico, mas não a branquitude como pré-requisito da universalidade. A estatística revela que o Estado dessexualiza a alegoria para torná-la lei, mas a operação excludente que converte *apenas* corpos caucasianos e classicizados em metáforas válidas da jurisdição opera muitas vezes abaixo do radar da abstração quantitativa.

Para essa dimensão do contrato visual, a contagem deve necessariamente ceder espaço à crítica teórica: é a *colonialidade do ver* (objeto do Capítulo 3) que ilumina por que o endurecimento afeta de maneira diferencial os corpos que podem — ou não — ascender ao Panteão normativo do Estado moderno.

## 6.6 — Materializações brasileiras: cinco direções para o caso sul-global

O argumento desenvolvido neste capítulo opera primordialmente sobre o corpus transatlântico clássico (França, EUA, Alemanha, Reino Unido, Itália). A extensão para o Sul Global — especificamente para o caso brasileiro — não deve ser tratada como mera "aplicação" do modelo, mas como possibilidade de contribuição original, dado que as cinco dimensões do contrato visual (sexual, racial, linguístico, fenomenológico, econômico) se articulam de forma específica no contexto brasileiro.

Cinco direções foram mapeadas para essa extensão:

1. **Abordagem monetária e comemorativa** — a economia visual das moedas e cédulas imperiais e republicanas como extensão do contrato para o bolso do cidadão
2. **Monumentos neoclássicos seriados** — análise da reprodução mecânica da fórmula canônica nos monumentos públicos brasileiros do século XIX e XX
3. **Conexão italiana** — escultores e oficinas italianas como tecnologia importada de construção da alegoria estatal brasileira
4. **Arquitetura judiciária** — programas visuais interiores dos tribunais brasileiros como espaço de produção de subjetividade judicial
5. **Dimensão racial** — a interseção entre contrato sexual e contrato racial na alegoria brasileira (corpo branco como pré-requisito da universalidade)

> 📎 Ver completo em: [[brazilian-visual-economy-proposals]]  
> 📊 Matriz comparativa: [[brazilian-case-decision-matrix]]

O bloco "Contrato Racial Visual" (Bloco 3 da Matriz de Hipóteses) não deve ser reduzido a uma sub-seção do caso brasileiro — requer desenvolvimento próprio, demonstrado *através* do caso mas não limitado a ele.
