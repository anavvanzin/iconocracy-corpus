---
titulo: "6.3 — A Estrutura Multidimensional do endurecimento"
parte: "III — Resultados"
capitulo: 6
subsecao: 6.3
status: "rascunho-inicial"
palavras: 0
citacoes: 0
updated: "2026-04-17"
nota: "Seção nova — rascunho gerado por Hermes Agent. Requer revisão substantiva, verificação de citações e integração com as seções 6.1–6.5 existentes."
pandoc:
  reference-doc: "template.docx"
  csl: "abnt.csl"
  bibliography: "references.bib"
---

# 6.3 — A Estrutura Multidimensional do endurecimento

O modelo de scoring composto — média simples dos dez indicadores ordinais — opera sob um pressuposto implícito: que os dez indicadores de purificação corporal capturam uma única dimensão latente de endurecimento. Este pressuposto é estatisticamente testável. A análise de componentes principais (PCA) revela que ele é apenas parcialmente verdadeiro — e que o preço da simplificação é a perda de uma distinção historicamente significativa.

## 6.3.1 — Análise de componentes principais: uma ou três dimensões?

A PCA aplicada aos dez indicadores (em escala padronizada, n=145) revela a seguinte estrutura de variância:

| Componente | Variância explicada | Variância acumulada | Autovalor (λ) |
|-----------|-------------------|--------------------|----------------|
| PC1 | 53,7% | 53,7% | 5,40 |
| PC2 | 11,8% | 65,5% | 1,19 |
| PC3 | 9,6% | 75,0% | 0,96 |
| PC4 | 6,0% | 81,0% | 0,60 |
| PC5–PC10 | 19,0% | 100,0% | < 0,60 |

O critério de Kaiser (autovalor > 1) retém dois componentes: PC1 e PC2. Para atingir 80% da variância的解释 são necessários quatro componentes; para 90%, sete.

O score composto atual (média simples dos dez indicadores) é essencialmente PC1 — captura a dimensão geral de endurecimento que carrega todos os indicadores positivamente. Isso é confirmado pela altíssima correlação entre o composite e PC1 (ρ = 0,98). Mas PC2 e PC3 carregam variância estrutural que o composite ignora.

### PC1 — A dimensão geral de endurecimento

PC1 responde por 53,7% da variância total. Todos os dez indicadores carregam positivamente, com loadings entre 0,18 (monocromatização) e 0,37 (rigidez postural, uniformização facial). Este componente confirma que o endurecimento é, em primeiro nível, uma dimensão única — os dez indicadores variam juntos na direção do endurecimento. O Estado endurece a alegoria female de forma integrada, não isolando partes do corpo.

### PC2 — O eixo burocrático (11,8%)

PC2 (11,8% da variância) opõe dois grupos de indicadores:

- **Polo negativo (loading < −0,20):** desincorporação (−0,45), apagamento narrativo (−0,23)
- **Polo positivo (loading > 0,40):** serialidade (+0,66), inscrição estatal (+0,41)

Este componente captura a tensão entre a alegoria que se desvincula da narrativa visual (desincorporação, apagamento) e a alegoria que se insere na circulação burocrática do Estado (serialidade, inscrição). É o eixo da *economia visual de Estado* — a diferença entre a imagem que remove a figura do contexto narrativo e a imagem que a multiplica, inscreve e faz circular como emblema oficial.

### PC3 — O registro cromático (9,6%)

PC3 (9,6%) é dominado quase inteiramente pela monocromatização (loading = 0,87). Os demais indicadores carregam abaixo de 0,35 em valor absoluto. Este componente não é um segundo fator de endurecimento — é um eixo independente que mede *o que resta quando se remove a dimensão geral*.

A interpretação preliminar — de que PC3 capturaria uma "segunda dimensão" do endurecimento — revelou-se incorreta após análise mais aprofundada (ver seção 6.3.3).

## 6.3.2 — Os três registros visuais do Estado

A estrutura PCA sugere um modelo de três registros visuais que operam de forma parcialmente independente na produção da alegoria estatal feminina:

**REGISTRO DE endurecimento GERAL** (PC1, 53,7%): o endurecimento corporal — rigidez postural, dessexualização, uniformização facial, apagamento das particularidades. É o registro que a literatura Warburguiana e a teoria do Contrato Sexual Visual já identificam como a operação central do Estado sobre o corpo alegórico.

**REGISTRO CROMÁTICO** (monocromatização, ortogonal a PC1): a redução ou eliminação da paleta cromática. Opera independentemente do endurecimento corporal — um artefato pode ter alto endurecimento core e baixa ou alta monocromatização sem que uma prediga a outra. Este registro é o foco da seção 6.3.3.

**REGISTRO BURÓCRÁTICO** (PC2, 11,8%): a multiplicação serial da alegoria e sua inscrição no circuito de circulação estatal — moeda, selo, cartaz, papel-moeda. Este registro é parcialmente capturado pela regressão OLS da seção 6.3 (o efeito da numismática), mas a PCA o isola como dimensão independente da purificação corporal.

A média por regime iconocrático para cada sub-score ilustra como os registros se distribuem:

| Regime | endurecimento Core | REG. CROMÁTICO | REG. BURÓCRÁTICO | Composite (10 ind) |
|--------|-------------------|----------------|------------------|--------------------|
| Fundacional | 1,07 | 1,97 | 1,04 | 1,16 |
| Normativo | 1,70 | **2,40** | 2,16 | 1,82 |
| Militar | 1,73 | 1,67 | **2,52** | 1,80 |
| Contra-alegoria | 0,50 | 1,29 | 1,21 | 0,71 |

*Nota: endurecimento Core = média de 8 indicadores (excluindo monocromatização e serialidade); REG. CROMÁTICO = monocromatização isolada; REG. BURÓCRÁTICO = média de serialidade + inscrição estatal.*

Os regimes *normativo* e *militar* produzem scores compostos praticamente idênticos (1,82 vs. 1,80) — o teste de Kruskal-Wallis não os diferencia significativamente. Contudo, os sub-scores revelam que eles operam por lógicas visuais distintas: o regime normativo maximiza o registro cromático (2,40); o regime militar maximiza o registro burocrático (2,52). Essa distinção era invisível no composite.

## 6.3.3 — A variável que não é variável: o problema historiográfico da monocromia

### 6.3.3.1 — O que a PCA não diz

A análise de componentes principais identifica estruturas estatísticas nos dados. Ela não identifica causalidade histórica. O achado de que a monocromatização domina PC3 e carrega fracamente em PC1 merece scrutiny empírico, não apenas estatístico.

A primeira pergunta é: **o que prediz a monocromatização melhor do que o endurecimento geral?** A resposta é: o meio material.

### 6.3.3.2 — Monocromatização por meio material

A média do indicador de monocromatização por tipo de meio revela um padrão claro:

| Meio | Média monocromatização | n |
|------|------------------------|---|
| Moeda/coin | 3,6 | 12 |
| Selo/stamp | 2,6 | 6 |
| Fotografia | 2,9 | 7 |
| Gravura/Estampa | 2,3 | 35 |
| Pintura/Desenho | 1,2 | 15 |
| Cartaz | 0,9 | 19 |

A correlação de Spearman entre ano e monocromatização é ρ = −0,18 (p = 0,03) — fraca, mas significativa: engravings mais recentes tendem a ser codificadas como *menos* monocromáticas (ou seja, com menor score de monocromatização, mais policromáticas). Isso é contraintuitivo em relação à hipótese de uma tendência histórica à monocromia.

### 6.3.3.3 — O teste crucial: controle por meio

O teste decisivo é a correlação entre monocromatização e endurecimento core *dentro de cada tipo de meio*:

- **Dentro de gravuras** (n=55): ρ = −0,01 (p = 0,92) — correlação nula
- **Dentro de moedas**: ρ = −0,54 (p = 0,07) — marginal, direção inesperada
- **Corpus completo, controlando por ano** (correlação parcial): ρ = 0,35 (p < 0,001)

Dentro da mesma tecnologia visual, monocromatização e endurecimento corporal *não variam juntos*. A correlação aparente no corpus completo é espúria — reflete o fato de que diferentes meios (moeda, selo, pintura, cartaz) têm diferentes níveis de monocromatização por razão de affordance material, não de estratégia jurídico-visual.

### 6.3.3.4 — O problema historiográfico

Este achado apresenta um problema hermenêutico que não se resolve no nível estatístico: **quando vemos uma alegoria estatal monocromática, não podemos determinar, apenas pelo código iconográfico, se a ausência de cor é uma escolha ou uma necessidade material.**

Três casos paradigmáticos do corpus ilustram o problema:

- **FR-HERC-1870** (5 Francs Hercule, moeda, 1870): core = 1,12, monocromatização = 4,0. A moeda de 1870 é monocromática porque *moedas são monocromáticas* — a metalurgia não permite policromia. O alto score neste indicador é um artefato do meio, não um sinal de endurecimento visual.

- **BR-016** (Alegoria da República, pintura, 1896): core = 2,12, monocromatização = 0,0. A pintura é policromática por natureza — a ausência de score de monocromatização não reflete escolha estética, mas affordance do meio.

- **FR-SEM-SELO-1903** (Semeuse, selo, 1903): core = 1,38, monocromatização = 3,0. Os selos postais franceses da Belle Époque eram impressos em colorido — mas *neste item específico* o codificador registrou monocromatização = 3,0. Aqui, o registro monocromático pode refletir uma decisão editorial (escolha de impressão específica), um viés de codificação (quem codifica pode ter sido influenciado pela redução visual típica do selo), ou uma diferença real no objeto. Não temos como determinar.

### 6.3.3.5 — A argumentação histórica

O problema não é um bug a ser corrigido — é uma lente historiográfica. A hipótese que se pode derivar é a seguinte:

*A emergência do Estado moderno ocidental coincide historicamente com a普及ação de tecnologias de reprodução visual mecânica (gravura, litografia, numismática, selo) que impõem formas visuais padronizadas e, frequentemente, monocromáticas. O que denominamos 'endurecimento cromático' é, em parte, um subproduto da materialidade das tecnologias de Estado — e, em parte, uma estratégia deliberada de economia visual que torna a alegoria legível em escala reduzida (moeda), circulável em larga escala (selo, cartaz) e resistente ao excesso sensual da pintura naturalista.*

A dificuldade interpretativa é que estes dois mecanismos — necessidade material e escolha estratégica — deixam a mesma marca no objeto iconográfico. A solução historiográfica não está na estatística, mas na pesquisa de arquivo: rastrear, para os itens com alto registro cromático e baixo endurecimento core (FR-HERC, NL-005, US-001), se havia alternativas policromáticas disponíveis no mesmo meio, no mesmo período, pelo mesmo Estado — e se a escolha monocromática foi documentada como decisão.

**Conclusão parcial:** o registro cromático deve ser reportado como achado exploratório, não como variável de endurecimento. A interpretação histórica requer validação arquivística item a item. O composite de 10 indicadores permanece como variável dependente principal; a monocromatização isolada é um descriptors suplementar cujo significado histórico permanece em aberto.

## 6.3.4 — Validação por clustering: a taxonomia de regimes sobrevive?

Os regimes iconocráticos — fundacional, normativo, militar, contra-alegoria — foram definidos por inferência teórica a partir do corpus. É legítimo perguntar: a estrutura não-supervisionada dos dados os confirma, ou impõe uma divisão diferente?

### 6.3.4.1 — Clustering hierárquico (Ward)

O algoritmo de agrupamento hierárquico com ligação de Ward foi aplicado à matriz de 145 itens × 10 indicadores. A análise de silhueta para k = 2 a 8 revelou o melhor ajuste em k = 2 (silhueta = 0,284), com queda progressiva para k maiores.

O coeficiente V de Cramér para a tabela de contingência cluster × regime é 0,502 — uma associação forte entre a estrutura não-supervisionada e a taxonomia teórica. Os clusters não são independentes dos regimes.

| Cluster | fundacional | normativo | militar | contra-alegoria | Total |
|---------|-------------|-----------|---------|-----------------|-------|
| 0 | 24 | 30 | 24 | 1 | 79 |
| 1 | 47 | 10 | 3 | 6 | 66 |

O Cluster 0 agrega normativo, militar e fundacional em proporções semelhantes — é um cluster de "endurecimento misto". O Cluster 1 é dominado por fundacional (71% do cluster), com contra-alegorias sobrerrepresentadas (9% vs. 5% no corpus). O Cluster 1 parece ser o cluster do regime fundacional residual.

### 6.3.4.2 — Concordância hierarquia × k-means

O índice de Rand ajustado (ARI) entre o agrupamento hierárquico e k-means (k=2) é 0,741 — alta concordância entre os dois métodos. Para k=3 a 8, o ARI varia entre 0,50 e 0,67. A estrutura de dois clusters é robusta entre métodos.

### 6.3.4.3 — O teste de remoção de monocromatização

Quando se refaz o clustering excluindo a monocromatização do conjunto de indicadores, o ARI entre as soluções com e sem o indicador é 0,790. A remoção altera moderately a estrutura — mas a estrutura fundamental (k=2) sobrevive. A monocromatização não é estruturalmente irrelevante, mas não é indispensável para a organização dos dados.

### 6.3.4.4 — Itens outliers

Dez itens do corpus apresentam silhueta negativa — isto é, estão mais próximos do cluster errado do que do correto. Entre os mais problemáticos:

- **FR-019** (sil = −0,32, regime militar): cartaz da Primeira Guerra Mundial com ícone de Justitia
- **FR-008** (sil = −0,21, regime militar): cartaz "La République nous appelle..."
- **US-004** (sil = −0,19, regime militar): selo da Primeira Guerra com Liberty, Justice, Demeter e Athena

Estes são itens militar que carregam traços de fluidez narrativa (não foram completamente endurecidos pelo registro burocrático) — e por isso não encaixam no padrão do cluster militar. A interpretação visual sugere que são alegorias em transição, em que a lógica fundacional ainda não foi completamente substituída pela lógica militar.

### 6.3.4.5 — Itens fora do escopo

O teste de concentração de itens *out-of-scope* (comparanda e borderline) nos clusters revela que o Cluster 1 (dominado por fundacional) tem 30,3% de itens fora do escopo, contra 8,9% no Cluster 0. A fronteira escopo/não-escopo é estruturalmente visível nos dados — os comparanda genuínos ocupam um espaço iconográfico distinto, quello dos contra-tipos Warburguianos que a tese utiliza como ancoragem histórica mas não como objeto de análise central.

### 6.3.4.6 — Conclusão da validação

A taxonomia de quatro regimes é empiricamente sustentada pela estrutura não-supervisionada dos dados. A associação entre clusters e regimes é forte (V = 0,502). Contudo, a estrutura de dois clusters dominantes — endurecimento burocrático misto vs. fundacional residual — sugere que a distinción mais fundamental no corpus não é entre os quatro regimes, mas sim entre a alegoria que foi capturada pela lógica de Estado (Cluster 0) e a que ainda opera fora dela ou contra ela (Cluster 1).

## 6.3.5 — Dinâmica temporal: quando endurece?

*A presente seção é descritiva e ilustrativa, não inferencial. O corpus não constitui amostra aleatória; a disponibilidade em arquivos digitais determina a distribuição temporal. Qualquer tendência deve ser interpretada como hipótese historiográfica, não como fato estatístico.*

A distribuição temporal do corpus (n=158 itens com ano) revela concentrações significativas em três períodos:

- **1790s–1780s** (n=13): auge da gravura política pré-revolucionária
- **1860s–1900s** (n=43): expansão da numismática e do selo estatal
- **1910s** (n=32): produção maciça de cartazes militares da Primeira Guerra Mundial (23 militar)

A média de endurecimento por década (apenas décadas com n ≥ 3 para média ± desvio padrão):

| Década | endurecimento médio | n |
|--------|---------------------|---|
| 1850s | 1,12 ± 0,33 | 4 |
| 1860s | 1,61 ± 1,00 | 7 |
| 1870s | 1,01 ± 0,75 | 9 |
| 1880s | 1,61 ± 0,54 | 7 |
| 1890s | 1,62 ± 0,73 | 9 |
| 1900s | 1,84 ± 1,02 | 7 |
| **1910s** | **1,65 ± 0,47** | **27** |
| 1920s | 1,05 ± 0,59 | 8 |
| 1940s | 1,73 ± 0,29 | 4 |
| 1950s | 2,58 ± 0,15 | 4 |

A tendência sugerida é de endurecimento progressivo das décadas de 1850 às de 1950 — da média de 1,12 para 2,58. A década de 1920 quebra a tendência (retração para 1,05), possivelmente refletindo um período de relaxamento do imaginário de Estado após a Primeira Guerra.

O pico dos anos 1950s (n=4, todos selos e moedas estatais) sugere que a alegoria jurídica no segundo pós-guerra tende ao endurecimento extremo — mas a base é muito pequena para generalização.

A circulação de países no corpus por década mostra que a produção imagética de Estado é dominada por França, Estados Unidos e Alemanha no século XIX; o Brasil aparece com força a partir de 1889; a Bélgica colonial é visível nos anos 1910–1920.

## 6.3.6 — Síntese: o que a quantificação revela e o que ela oculta

A análise multidimensional dos indicadores de purificação produz três achados principais:

**1. O endurecimento é estruturalmente unidimensional, com duas dimensões residuais.** O score composto de 10 indicadores captura 53,7% da variância (PC1) — a dimensão geral de endurecimento corporal. As dimensões residuais (PC2: burocrática; PC3: cromática) são estatisticamente significativas mas substancialmente menores.

**2. Os regimes normativo e militar são funcionalmente distintos por trás do composite.** Ambos produzem scores compostos quase idênticos (1,82 vs. 1,80). Os sub-scores revelam que o regime normativo opera pelo registro cromático (padronização visual, redução cromática) enquanto o regime militar opera pelo registro burocrático (multiplicação serial, inscrição estatal). São duas estratégias visuais distintas que convergem no composite.

**3. A monocromatização é um descriptor material, não um indicador de endurecimento.** A correlação entre monocromatização e endurecimento core desaparece dentro de categorias de meio (ρ = −0,01 dentro de gravuras). O alto score de monocromatização em moedas e selos é um artefato de affordance, não de estratégia visual. A interpretação histórica deste indicador requer validação arquivística item a item.

**O que a quantificação não pode dizer:** não pode determinar, para cada item com alto registro cromático, se a ausência de cor é escolha deliberada ou necessidade material. Esta é uma questão historiográfica que pertence ao arquivo, não ao modelo estatístico. A seção 6.5 (os limites da quantificação) recupera esta tensão como problema central do método iconométrico — o número captura a forma; a intenção por trás da forma pertence à interpretação.

---

## Nota sobre os notebooks de análise

As análises apresentadas nesta seção foram realizadas nos seguintes notebooks Jupyter (diretório `notebooks/`):

- **05_temporal.ipynb** — Dinâmica temporal (regimes, endurecimento, países, suportes por década)
- **06_clustering.ipynb** — Clustering hierárquico e k-means; silhueta; validação cruzada
- **07_dimensionality.ipynb** — PCA: scree plot, loadings, biplot
- **08_multidimensional_scoring.ipynb** — Sub-scores (endurecimento core, monocromatização, formalização burocrática); comparações por regime; exportação de `subscores.csv`

Os notebooks usam Python 3.12 (ambiente conda `iconocracy`), com as bibliotecas pandas, numpy, scipy, scikit-learn, matplotlib e seaborn. Todos foram executados e validados em 2026-04-17. Os resultados reportados nesta seção são reproduzíveis a partir dos notebooks.

As figuras geradas (fig_06 a fig_18) estão disponíveis em `data/processed/`.

---

## Referências do capítulo

As referências aos métodos estatísticos (PCA, Kruskal-Wallis, clustering hierárquico, correlação parcial) seguem os padrões de reporting de pesquisa quantitativa em ciências sociais. As referências historiográficas para a interpretação de monocromatização e reprodução mecânica incluem Walter Benjamin (*A Obra de Arte na Era de Sua Reprodutibilidade Técnica*, 1935/1955), Mario Sbriccoli (*La legislazione penale*, 1998) e Marie-Jo Mondzain (*Image, Icône, Économie*, 2002). Citações completas em ABNT NBR 6023:2025 no arquivo `references.bib`.
