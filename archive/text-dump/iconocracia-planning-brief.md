# ICONOCRACIA

*Regimes iconocráticos e a presidenta totêmica*

**Plano de pesquisa, cronograma e estratégia de financiamento**

Documento de trabalho — tese de doutorado em cotutela UFSC × UGent

---

**ANA V. VANZIN** · Doutoranda · PPGD/UFSC · OAB/SC 64.343
Abril de 2026 · Florianópolis

---

## Sumário executivo

A tese ICONOCRACIA investiga os regimes iconocráticos — sistemas estruturados de imagens, gestos e símbolos que instituem a autoridade jurídica antes que a norma a codifique. O caso central é a *presidenta totêmica*, leitura das três fases iconográficas de Dilma Rousseff (totem, tabu e restauração) a partir de uma adaptação do modelo de Hodson para uma chefia de Estado feminina no Brasil contemporâneo.

O projeto é uma tese de doutorado em cotutela entre o Programa de Pós-Graduação em Direito da UFSC (orientação do Prof. Dr. Arno Dal Ri Jr., grupo Ius Gentium) e o Instituut voor Rechtsgeschiedenis da Universidade de Gent (co-orientação do Prof. Dr. Georges Martyn, escola de Gent em iconologia jurídica). Desenvolve-se em cinco fases entre abril de 2026 e 2028, culminando com defesa conjunta UFSC–UGent. O cronograma articula avanço dos oito capítulos, aquisição de competências (neerlandês, métodos quantitativos em R, codificação Iconclass) e uma trilha pública de três artigos revisados por pares, três apresentações internacionais e uma proposta de livro.

Este documento organiza o projeto em formato apresentável a comissões acadêmicas, supervisores e órgãos de fomento — em particular à linha CAPES-PrInt, alvo prioritário de financiamento para a estadia em Gent em 2027.1.

---

## 1 · Projeto de pesquisa

### 1.1  Argumento central

Imagens não são ornamento do poder jurídico. São sua infraestrutura simbólica. Regimes políticos produzem regimes iconocráticos — sistemas estruturados de imagens, gestos, símbolos e rituais que instituem a autoridade antes mesmo que a norma a codifique, e que continuam operando em camadas de governamentalidade que o texto jurídico, sozinho, não alcança.

A tese articula duas teses subsidiárias. A primeira: que a iconografia do poder não é epifenômeno do direito, mas constitui uma camada própria do governo, com gramática, economia e temporalidade distintas. A segunda: que essa camada pode ser descrita com rigor metodológico — classificada, quantificada, comparada — e que fazê-lo permite ler regimes políticos por dentro de sua economia simbólica.

### 1.2  Arcabouço teórico

A fundamentação teórica articula quatro tradições que pensam a imagem como operação jurídica, e não como mera representação.

**Aby Warburg.** O método atlas (Mnemosyne) e o conceito de *Pathosformel* oferecem o instrumental para rastrear a sobrevivência (*Nachleben*) das fórmulas gestuais da Antiguidade clássica nas imagens do poder moderno. A iconografia jurídica herda uma gramática que não escolheu.

**Marie-José Mondzain.** A teorização do iconoclasmo bizantino como matriz estabelece que a imagem não representa — ela opera, medeia, institui. A economia icônica precede a economia jurídica e a constitui.

**Peter Goodrich.** A semiótica jurídica permite ler o direito como regime de signos visíveis. A lei lida com o invisível (intenção, soberania, obrigação) através de seu registro icônico — o regime iconocrático é o que torna o abstrato juridicamente eficaz.

**Loren Hodson — *The Totemic Judge*.** O conceito do juiz como totem — autoridade institucional ancorada em investimento simbólico coletivo — é a base sobre a qual a tese constrói sua formulação da *presidenta totêmica*, deslocando a figura de sua origem judicial (masculina, anglo-saxã) para uma chefia executiva feminina no Brasil contemporâneo.

### 1.3  Os três regimes iconocráticos

A tese propõe uma tipologia operativa — não meramente descritiva — para classificar regimes políticos pela economia simbólica que os sustenta. Três tipos-ideais emergem da análise comparativa do corpus.

**Regime fundacional.** Regimes que produzem suas próprias imagens originárias — constituintes, revolucionários, refundadores. Operam com alta densidade ritual; a iconografia é instituinte. Exemplos: proclamações, cartas fundamentais, atos de instauração.

**Regime normativo.** Regimes que operam pela estabilização do símbolo — democracias consolidadas, ordens jurídicas rotinizadas. A saliência iconográfica é baixa porque o símbolo está internalizado. Exemplos: cerimônias eleitorais, rituais parlamentares, iconografia judicial ordinária.

**Regime militar.** Regimes que substituem o símbolo pela força — ditaduras, estados de exceção, ocupações. A imagem é arma ou alvo: iconoclasmos, desfiles, apropriações violentas do espaço público. A violência simbólica se sobrepõe à norma.

Um mesmo Estado pode atravessar os três regimes em sequência ou operar em sobreposição. A tipologia é ferramenta analítica, não caixa classificatória rígida.

### 1.4  Caso central: a presidenta totêmica

Dilma Rousseff como caso-limite. A tese faz uma leitura em três fases iconográficas, cada uma correspondendo a uma operação simbólica distinta sobre a figura presidencial.

**Fase I · Totem (2010–2013).** Ascensão e consagração. A imagem da presidenta condensa os afetos do projeto desenvolvimentista-petista. Iconografia de força — fotografia oficial composta, gestos presidenciais codificados, entrada no panteão simbólico da chefia executiva brasileira.

**Fase II · Tabu (2014–2016).** Contaminação simbólica. A figura se torna objeto de interdição: ódio público, ridicularização midiática, desdobramento viral em memes. A iconografia é de avaria — adesivos em carros, capas de revista, a repetição da imagem para erodi-la. O impeachment é também um iconoclasmo.

**Fase III · Restauração (2016–presente).** Reinscrição tardia. A imagem retorna como memória política — museificação, biopic, rememoração institucional. Iconografia de luto e de retorno; a figura é reconstruída simbolicamente após o episódio de avaria, incorporada à narrativa nacional em nova posição.

---

## 2 · Método

*Um pipeline em três camadas conecta a coleta iconográfica, a codificação controlada e a análise quantitativa reproduzível. A infraestrutura está parcialmente implementada — ver `iconocracia-companion.warholana.workers.dev`.*

### 2.1  Coleta (IconoCode × Scout)

O corpus é composto de quatro tipos de suportes: (i) capas de jornal e revista do período estudado; (ii) imagem digital e memética, incluindo artefatos virais; (iii) fotografia oficial e vernacular, capturando o gesto presidencial em registros distintos; (iv) peça museológica e cerimonial, alcançando os rituais de Estado. A pipeline Scout automatiza a descoberta inicial; a seleção final é feita por critérios iconográficos explícitos.

### 2.2  Codificação (Iconclass controlado)

Cada item do corpus recebe quatro camadas de codificação: (i) classificação iconográfica formal segundo o sistema Iconclass (4ª edição); (ii) atribuição de regime iconocrático (fundacional, normativo, militar); (iii) mapeamento de *pathosformel* warburguianas identificadas; (iv) revisão por pares inter-coder sobre subamostra para calcular concordância (Cohen's κ alvo ≥ 0,70).

### 2.3  Análise (R · FactoMineR · OLR)

A análise quantitativa opera sobre o corpus codificado e articula três procedimentos complementares: (i) *Ordinal Logistic Regression* para modelar a relação entre variáveis iconográficas e a intensidade do regime; (ii) teste de Kruskal-Wallis para diferenças entre grupos não paramétricos; (iii) Análise de Correspondência Múltipla (MCA) via pacote FactoMineR para visualizar a estrutura de co-ocorrência. A análise quantitativa é integrada à síntese qualitativa em prosa — não a substitui.

---

## 3 · Arquitetura da tese

*A tese move-se da fundamentação teórica para o caso brasileiro, passando pela análise iconográfica belga como contraponto comparativo.*

| Capítulo | Descritor |
|----------|-----------|
| **1** | Introdução — apresentação do problema, do argumento, e do caso central. Mapa da tese. |
| **2** | Arcabouço teórico — articulação de Warburg, Mondzain, Goodrich e Hodson. Fundamentação da categoria iconocracia. |
| **3** | Iconografia jurídica brasileira — primeira camada do corpus. Imagens do poder judicial, legislativo e executivo no Brasil republicano. |
| **4** | Iconografia jurídica europeia (Bélgica) — contraponto comparativo. A escola de Gent em diálogo com o caso brasileiro. |
| **5** | Presidenta totêmica — fase totem. Análise iconográfica do primeiro período Dilma (2010–2013). |
| **6** | Presidenta totêmica — tabu e restauração. Análise das fases II e III (2014–presente). |
| **7** | Síntese — regimes iconocráticos. Tipologia operativa articulada com os resultados quantitativos do corpus. |
| **8** | Conclusão — teoria iconocrática. Síntese teórica; implicações para a história do direito e para a teoria constitucional. |

---

## 4 · Cronograma em cinco fases

*De 2026.1 à defesa prevista em 2028. Cada fase articula avanço de tese, aquisição de método e trajetória institucional.*

### Fase 1 · Fechar o semestre  ·  abr–jul 2026

Encerramento dos créditos remanescentes: DIR410346 (História do Direito Penal), DIR510212 (Métodos e Metodologias) e DIR410340 (Direito Administrativo Digital). Atuação como parecerista na Mostra de Pesquisa do Congresso de Direito da UFSC. Trava do acordo de cotutela com UGent — datas, créditos, composição da banca. Redação do Capítulo 1 (introdução). Início do neerlandês em nível A1 e treinamento aprofundado em Iconclass integrado à pipeline IconoCode.

### Fase 2 · Capítulos-núcleo + verba  ·  ago–dez 2026

Redação dos Capítulos 2 (arcabouço teórico) e 3 (iconografia jurídica brasileira). Encerramento do lote inicial de codificação do corpus segundo o protocolo. Submissão à CAPES-PrInt (ou via institucional) para apoio à estadia em Gent. Submissão de um artigo a periódico brasileiro, mobilizando material dos capítulos 2/3. Envio de abstracts para conferências 2027 (ESCLH e evento nacional). Neerlandês A2; Python para análise de imagem (OpenCV + pipeline Vertex AI).

### Fase 3 · Estágio Gent + qualificação  ·  jan–jul 2027

Estadia de pesquisa em Gent (alvo: 3 a 6 meses). Redação dos Capítulos 4 (iconografia jurídica belga) e 5 (presidenta totêmica — fase totem) em ambiente institucional da escola de Gent. Exame de qualificação no PPGD/UFSC. Peça co-autorada com Martyn ou Huygebaert, planejada durante a estadia. Apresentação na ESCLH 2027 (ou equivalente) e em seminário do Legal History Institute. Neerlandês B1 em imersão; métodos arquivísticos no Rijksarchief Gent e Algemeen Rijksarchief Brussel.

### Fase 4 · Síntese + tier-1  ·  ago–dez 2027

Redação dos Capítulos 6 (tabu e restauração) e 7 (síntese — regimes iconocráticos). Rodada quantitativa final sobre o corpus consolidado: OLR, Kruskal-Wallis, MCA. Submissão a periódico internacional tier-1 (*Law and Humanities* ou *Journal of Legal History*). Apresentação em conferência internacional (LSA ou painel de iconografia no ISHA). Início do mapeamento de trilhas pós-doutorado e concursos públicos.

### Fase 5 · Defesa + pós-doutorado  ·  2028

Redação do Capítulo 8 (conclusão — teoria iconocrática). Revisão integral da tese (versão completa em português e versão parcial em inglês/francês para a banca UGent). Defesa conjunta UFSC+UGent. Submissões a editais de pós-doutorado (Max Planck Frankfurt, EUI Florença, UGent, Humboldt, FAPESP-PD). Preparação de concursos públicos federais. Proposta de livro submetida a editora-alvo (Hart, Palgrave Law-Humanities, Routledge, ou coleção nacional).

---

## 5 · Estrutura de cotutela

*Dupla titulação articulando a historiografia jurídica brasileira (linha Ius Gentium) à escola de Gent em iconologia jurídica.*

### 5.1  UFSC · Brasil

**Programa de Pós-Graduação em Direito** — linha Teoria, História e Filosofia do Direito. Grupo Ius Gentium, cadastrado no CNPq, com tradição consolidada em história do direito internacional e historiografia jurídica humanista (Grossi, Hespanha, Van Caenegem).

**Orientador — Prof. Dr. Arno Dal Ri Jr.** Professor Titular, historiador do direito internacional, coordenador do Ius Commune (UFSC/CNPq). Principal elo institucional entre o PPGD/UFSC e a historiografia jurídica europeia (Gent, Florença, Milão, Paris I, Lille). Editor das coleções *Clássicos do Direito Internacional* e *Arqueologia Jurídica*.

### 5.2  UGent · Bélgica

**Instituut voor Rechtsgeschiedenis** — Legal History Institute, centro de referência da escola de Gent em iconologia jurídica contemporânea. Produziu o volume de referência *The Art of Law* (Lannoo 2016; Springer 2018) e a leitura panofskyana aplicada à imagem jurídica belga de 1795–1914.

**Co-orientador — Prof. Dr. Georges Martyn.** Editor do *The Art of Law*, referência em iconografia jurídica flamenga, articulador do diálogo entre a escola de Gent e a historiografia jurídica brasileira. Publicações conjuntas com grupos de pesquisa da UFSC desde *Métodos da historiografia do direito contemporânea* (2024).

### 5.3  Dupla titulação

O acordo de cotutela prevê (a) dupla diplomação UFSC–UGent ao final do doutoramento; (b) estadia mínima de 3 meses em Gent durante a fase 3 do cronograma (janeiro a julho de 2027); (c) banca de defesa composta conjuntamente por membros UFSC e UGent, com peso de co-decisão em ambos os programas; (d) tese redigida em português com resumo extenso e capítulos-chave traduzidos para inglês ou francês conforme exigência UGent.

---

## 6 · Estratégia de financiamento

### 6.1  CAPES-PrInt — prioritário

A linha CAPES-PrInt é o alvo prioritário de fomento para a estadia em Gent (fase 3). A UFSC possui chamada institucional CAPES-PrInt com linha de apoio a doutorados em cotutela. O enquadramento do projeto ICONOCRACIA na chamada se dá por três eixos: (i) internacionalização estruturante, via cotutela formalizada UFSC–UGent com orientador titular brasileiro e co-orientador belga, produzindo dupla titulação; (ii) tema com forte dimensão comparada — iconografia jurídica brasileira em contraponto à belga, dois casos nacionais da mesma família historiográfica; (iii) produtos concretos e mensuráveis — co-publicação com Martyn ou Huygebaert, apresentação em ESCLH, artigo tier-1 submetido em 2027.

Documentos necessários para a submissão (a reunir entre maio e agosto de 2026): carta de anuência assinada pelo orientador, carta de aceite formal UGent assinada pelo co-orientador, plano detalhado de atividades em Gent, cronograma de entregáveis, orçamento da estadia (mensalidade + deslocamento + moradia), resumo ampliado em inglês, currículo Lattes atualizado e currículo internacional em inglês.

### 6.2  CNPq · FAPESC

Bolsa de doutorado no Brasil via CNPq GD/GM (se não contemplada por edital interno da UFSC ou já em vigor). Auxílios pontuais via FAPESC para cobertura de deslocamentos a eventos nacionais e aquisição de materiais de pesquisa não cobertos por outras linhas.

### 6.3  Pós-defesa — Humboldt · Erasmus+ · FAPESP-PD

Mapeamento antecipado, com aplicação na fase 4, de linhas de pós-doutorado que permitam continuidade imediata após a defesa: Humboldt Foundation (Alemanha), Erasmus+ staff mobility para início de vínculos com centros europeus, FAPESP-PD se o vínculo for com USP ou UNICAMP, e editais do Max Planck Institute for Legal History (Frankfurt) e do European University Institute (Florença).

---

## 7 · Veículos-alvo e trajetória pública

### 7.1  Periódicos — shortlist comentado

Artigos previstos: três submissões revisadas por pares, distribuídas entre 2026.1 e 2027.2, escaladas em ambição.

- **Revista Brasileira de História do Direito (IBHD).** Veículo natural para o primeiro artigo (fase 1, refil do *Iconocracia Tropical* já auditado).
- **Sequência (UFSC) / Quaestio Iuris (UERJ).** Veículos nacionais tier-1, qualis A. Apropriados para material dos capítulos 2/3 (fase 2).
- **Rechtsgeschiedenis / Pro Memorie (Bélgica/Holanda).** Veículos da escola de Gent. Apropriados para peça co-autorada com Martyn ou Huygebaert (fase 3).
- **Law and Humanities (Routledge).** Alvo tier-1 anglófono, encaixe temático muito forte para iconografia jurídica. Submissão prevista fase 4.
- **Journal of Legal History (Taylor & Francis).** Alternativa tier-1, perfil mais tradicional. Segunda opção se *Law and Humanities* não couber no timing.
- **Quaderni Fiorentini / Rechtsgeschichte (Max Planck).** Veículos de destino para a versão europeizada de material do capítulo 4, em italiano ou alemão.

### 7.2  Conferências

- **ESCLH — European Society for Comparative Legal History.** Conferência bienal. Submissão de abstract na fase 2, apresentação na fase 3.
- **LSA — Law and Society Association.** Anual. Apresentação prevista para fase 4, após dados quantitativos consolidados.
- **ISHA — International Society for the History of Art.** Painéis de iconografia jurídica; encaixe direto com capítulos 3–4.
- **Encontros de História do Direito da UFSC · Congresso IBHD.** Circuito brasileiro; participação contínua, não programada como marco.

### 7.3  Livro

A tese é concebida desde a arquitetura para duplo destino — defesa acadêmica e publicação em livro. Editoras-alvo, por ordem de preferência: Hart Publishing (UK), Palgrave Law-Humanities (UK/US), Routledge Studies in Law and Humanities (UK), coleção internacional do Max Planck (Frankfurt), e, no Brasil, Editora Fundação Boiteux (UFSC) ou Editora Contracorrente. Proposta de livro será submetida na fase 5.

---

## 8 · Produtos esperados

| Entregável | Descrição |
|------------|-----------|
| **Tese** | Oito capítulos, ~300 páginas. Defesa conjunta UFSC+UGent em 2028. |
| **Artigos** | Três artigos revisados por pares: um em veículo brasileiro (fase 1), um intermediário (fase 2 ou 3), um tier-1 internacional (fase 4). |
| **Co-publicação** | Uma peça co-autorada com Martyn ou Huygebaert (fase 3). |
| **Apresentações** | Três apresentações internacionais: ESCLH, LSA ou ISHA, seminário UGent. |
| **Livro** | Proposta de livro submetida a editora tier-1 na fase 5. |
| **Corpus público** | Dashboard de pesquisa `iconocracia-companion.warholana.workers.dev` atualizado e documentado para uso por outros pesquisadores. |

---

## Contato

**ANA V. VANZIN**
Doutoranda · PPGD/UFSC · OAB/SC 64.343
Dashboard de pesquisa: `iconocracia-companion.warholana.workers.dev`
Grupo Ius Gentium: `grupoiusgentium.com.br`
