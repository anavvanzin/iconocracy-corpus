---
title: "Do Poder-Dever ao Dever-Poder: o Conselho de Contestação Algorítmica como Arquitetura de Devido Processo Legal na Administração Pública 4.0"
author: |
  Ana Vitória Vanzin  
  Programa de Pós-Graduação em Direito, Universidade Federal de Santa Catarina (PPGD/UFSC)
date: julho 2026
abstract: |
  Este artigo sustenta que, no contexto da Administração Pública algorítmica, o devido processo legal — garantido pelo artigo 5º, LV, da Constituição Federal e densificado pela Lei nº 9.784/1999 — exige a integração de quatro eixos: contraditório prévio, motivação jurídica qualificada (que pressupõe, mas não se reduz a, explicabilidade técnica), governança institucional com transparência qualificada e proteção de dados pessoais. A ausência de qualquer um desses eixos vicia a decisão automatizada. O diagnóstico estrutural que fundamenta essa tese é o de que o Estado brasileiro ocupa simultaneamente a posição de regulador do uso de algoritmos e de maior usuário desses mesmos algoritmos — uma dupla posição que este artigo denomina “Do Poder-Dever ao Dever-Poder” e que gera incentivos estruturais à subaplicação das normas que o próprio Estado edita. A partir da análise de quatro estudos especializados em direito digital, o artigo ilustra a tese da integração por meio do GovLens/DueProcess.AI, protótipo acadêmico cujo núcleo é o Conselho de Contestação Algorítmica, sistema de quatro personas jurídico-técnicas que emitem pareceres cruzados e produzem síntese fundamentada. O caso-âncora é o indeferimento de aposentadoria rural pelo INSS, contrastado analogicamente com o precedente do Sistema de Risco Indicativo de Fraude (SyRI) da Corte Distrital de Haia (2020). O artigo propõe duas contribuições normativas autorais: a literacia algorítmica como condição material de eficácia do contraditório e o princípio da notícia humana para decisões adversas dirigidas a pessoas vulneráveis.
keywords:
  - Administração Pública digital
  - contestabilidade algorítmica
  - devido processo legal
  - explicabilidade
  - LGPD
  - inteligência artificial no setor público
lang: pt-BR
citation_style: ABNT NBR 6023:2025
---

\noindent\textbf{Palavras-chave:} Administração Pública digital; contestabilidade algorítmica; devido processo legal; explicabilidade; LGPD; inteligência artificial no setor público.

## 1 Introdução

O Estado brasileiro edita a Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018), cria a Autoridade Nacional de Proteção de Dados, regulamenta o acesso à informação (Lei nº 12.527/2011) e estrutura o Governo Digital (Lei nº 14.129/2021). Ao mesmo tempo, é o maior coletor de dados pessoais do país, o maior usuário de sistemas algorítmicos na tomada de decisão administrativa e o ator com maior incentivo estrutural a subaplicar as normas que ele mesmo edita — pois a aplicação plena reduziria sua eficiência operacional. Essa ambiguidade não é acidental; ela constitui a posição estrutural que este artigo denomina "Do Poder-Dever ao Dever-Poder": o Estado que deveria regular o uso de algoritmos para proteger o cidadão é o mesmo que os emprega para decidir sobre ele, frequentemente sem lhe oferecer os mecanismos de compreensão e contestação que a Constituição Federal exige.

A literatura jurídica brasileira tem avançado na identificação desses riscos. Tavares, Bitencourt e Cristóvam (2024) formulam o conceito de contraditório algorítmico prévio como condição de validade da decisão automatizada no setor público. Saito e Salgado (2020) ampliam a compreensão do direito fundamental à proteção de dados para além da privacidade, alcançando a autodeterminação informativa. Sarlet e Molinaro (2019) exploram as tensões éticas e normativas do big data na saúde, revelando como a coleta massiva pode comprometer a dignidade. Cristóvam e Hahn (2020) articulam governo aberto, dados orientados e infraestrutura nacional de dados abertos como dimensões complementares da Administração Pública digital. Schiefler, Cristóvam e Sousa (2020) demonstram que a digitalização pode aprofundar exclusões se o acesso à tecnologia não for tratado como condição democrática da cidadania administrativa.

Esses artigos oferecem os pilares dogmáticos necessários, mas nenhum deles materializa, em artefato concreto, a integração dos quatro eixos num instrumento acessível ao cidadão afetado — nem, sobretudo, formula a integração como exigência de validade do ato administrativo automatizado. Este artigo propõe ambas as coisas: a tese normativa da integração como condição de validade (Seção 2) e sua ilustração por meio do GovLens/DueProcess.AI, um protótipo acadêmico cujo núcleo — o Conselho de Contestação Algorítmica — traduz cada eixo dogmático em uma persona jurídico-técnica que emite parecer, avalia os pareceres das demais e produz, por meio de um Relator, uma síntese fundamentada.

O texto avança em nove seções: formula a tese normativa e o diagnóstico estrutural que a fundamenta (Seção 2), percorre o marco teórico (Seção 3), diagnostica a lacuna institucional brasileira (Seção 4), apresenta o Conselho de Contestação Algorítmica como ilustração concreta da tese (Seção 5), desenvolve o caso-âncora do INSS (Seção 6), propõe duas contribuições normativas autorais (Seção 7), e encerra com os limites e a conclusão (Seções 8 e 9).

Metodologicamente, o artigo combina método dogmático-jurídico (reconstrução dos eixos normativos), análise documental de plataformas governamentais (diagnóstico da lacuna), *design science research* (materialização do Conselho como prova de conceito) e raciocínio analógico (caso SyRI). As limitações de cada abordagem são explicitadas na Seção 8.

## 2 Devido processo legal algorítmico: fundamento dogmático e tese normativa

### 2.1 As garantias constitucionais do processo administrativo

A Constituição Federal de 1988 inscreve a Administração Pública sob os princípios da legalidade, da impessoalidade, da moralidade, da publicidade e da eficiência (art. 37, *caput*). O artigo 5º, inciso LV, garante aos litigantes, em processo judicial ou administrativo, e aos acusados em geral, o contraditório e a ampla defesa, com os meios e recursos a ela inerentes. A Lei nº 9.784/1999, que regula o processo administrativo federal, densifica essas garantias ao exigir motivação explícita, clara e congruente para atos que afetem direitos ou interesses (art. 50), ao assegurar ao administrado a ciência da tramitação e a formulação de alegações antes da decisão (art. 3º, II e III), e ao prever o direito de interpor recurso administrativo independentemente de caução (art. 56).

A doutrina administrativista brasileira é pacífica quanto ao conteúdo mínimo do devido processo legal administrativo: notificação adequada do interessado, oportunidade real de apresentar defesa e produzir provas, decisão proferida por autoridade competente com motivação suficiente e possibilidade de impugnação recursal (Mello, 2021; Di Pietro, 2022; Justen Filho, 2023). A motivação não é mera formalidade: ela é o instrumento que permite ao administrado compreender as razões da decisão, ao superior hierárquico revisá-la e ao Judiciário controlá-la. Sem motivação adequada, o ato administrativo é inválido — e essa consequência é consolidada na jurisprudência dos tribunais superiores brasileiros.

Nesse sentido, a transposição dessas garantias para a atividade administrativa digital sob suporte tecnológico exige que se compreenda a eficiência administrativa (art. 37, *caput*) não como um valor absoluto ou puramente econômico-burocrático, mas sim subordinado ao paradigma da Administração Pública democrática. Conforme sustenta Cristóvam (2015), o interesse público não se confunde com o mero interesse do aparato estatal em acelerar processos ou reduzir custos de transação; o interesse público primário reside na realização dos direitos fundamentais dos administrados e na legitimidade democrática de sua participação. Portanto, a supremacia do interesse público só se legitima quando reconfigurada democraticamente, o que obsta que a eficiência instrumental (corporificada na celeridade dos sistemas algorítmicos de decisão em massa) atropele as garantias mínimas do devido processo legal.

### 2.2 A reconfiguração das garantias pela automação decisória

Quando a Administração Pública automatiza decisões, essas garantias não desaparecem — elas se reconfiguram. A presente seção sustenta que a automação impõe três reconfigurações dogmáticas, cada uma correspondendo a uma das garantias clássicas do processo administrativo.

A primeira reconfiguração atinge a motivação. Na decisão humana, a motivação se exaure na fundamentação do agente público — o iter lógico que conduz dos fatos e do direito à conclusão. Na decisão automatizada, esse iter não é percorrido por um agente identificável, mas por um sistema cujos critérios podem ser opacos até para a própria Administração. É crucial, aqui, distinguir dois registros que a literatura sobre inteligência artificial frequentemente confunde e que o direito administrativo não pode confundir. A explicabilidade técnica (XAI — *explainable artificial intelligence*) revela quais variáveis pesaram na decisão e em que proporção; responde à pergunta *como* o algoritmo chegou ao resultado. A motivação jurídica é de natureza normativa: responde à pergunta *por que* a decisão é juridicamente correta à luz dos fatos, das normas e dos princípios aplicáveis. Um sistema pode ser tecnicamente explicável sem ser juridicamente motivado, porque a explicabilidade técnica não contém o raciocínio normativo que o artigo 50 da Lei nº 9.784/1999 exige. Esta distinção é central para a tese deste artigo: a legitimidade da decisão automatizada não se satisfaz com explicabilidade técnica; ela exige motivação jurídica.

A segunda reconfiguração atinge o contraditório. Na decisão tradicional, o contraditório se exerce após a ciência do ato: o administrado toma conhecimento da decisão e, se discordar, recorre. No contexto algorítmico, essa sequência pode ser ineficaz, porque a opacidade do sistema impede que o administrado sequer saiba o que contestar. Tavares, Bitencourt e Cristóvam (2024) formulam, por isso, o conceito de contraditório algorítmico prévio: a exigência de que a decisão automatizada seja acompanhada de explicação compreensível *antes* de produzir efeitos jurídicos. A tese deste artigo endossa esse conceito, mas acrescenta que o contraditório prévio é condição necessária, porém não suficiente: sem literacia algorítmica — a capacidade de o cidadão compreender que a decisão foi automatizada e o que isso significa —, o contraditório prévio é juridicamente reconhecido mas materialmente inacessível. A literacia é, portanto, degrau anterior à contestação (Seção 7.1).

A terceira reconfiguração atinge a publicidade e a governança. A publicidade do ato administrativo tradicional se satisfaz com a divulgação oficial. No contexto algorítmico, a publicidade precisa ser qualificada: não basta divulgar que uma decisão foi tomada; é preciso divulgar os dados que a alimentaram, os critérios que a produziram e os mecanismos pelos quais o cidadão pode contestá-la. Cristóvam e Hahn (2020) articulam essa exigência sob o paradigma do governo aberto orientado por dados. A Lei nº 14.129/2021 (Lei do Governo Digital) estrutura uma arquitetura normativa que combina transparência, dados abertos e canais de interação, mas sua incidência sobre municípios depende de adesão voluntária (art. 2º, III, e §2º), criando um federalismo assimétrico que fragiliza a uniformidade da garantia.

### 2.3 A tese normativa: integração como condição de validade

As três reconfigurações descritas acima convergem para uma tese central. Este artigo sustenta que, no contexto da Administração Pública algorítmica, o devido processo legal — tal como garantido pelo artigo 5º, LV, da Constituição e densificado pela Lei nº 9.784/1999 — exige a integração de quatro eixos: (i) contraditório prévio, (ii) motivação jurídica qualificada (que pressupõe, mas não se reduz a, explicabilidade técnica), (iii) governança institucional com transparência qualificada e (iv) proteção de dados pessoais como condição de autodeterminação informativa. Nenhum desses eixos, isoladamente, satisfaz o devido processo legal algorítmico; a ausência de qualquer um deles vicia a decisão automatizada por insuficiência de motivação, por cerceamento de defesa ou por violação da dignidade do administrado.

A afirmação de que a integração é condição de validade — e não mera recomendação de boa prática administrativa — é a contribuição dogmática central deste artigo. Ela se fundamenta em três premissas. A primeira é que o dever de motivar (art. 50, Lei nº 9.784/1999) não é satisfeito pela mera indicação do resultado do algoritmo; ele exige a exposição dos critérios, dos dados e do raciocínio que conduziram à decisão, em linguagem acessível ao destinatário — o que pressupõe explicabilidade e proteção de dados. A segunda é que o direito ao contraditório (art. 5º, LV, CF) não é satisfeito pela mera abertura de prazo recursal após decisão automatizada; ele exige que o administrado compreenda o que está sendo decidido, por quais critérios e com quais dados — o que pressupõe literacia algorítmica e governança transparente. A terceira é que a dignidade da pessoa humana (art. 1º, III, CF) impõe que a comunicação de decisões adversas a pessoas vulneráveis não seja feita por notificação automatizada fria — o que este artigo formula como o princípio da notícia humana (Seção 7.2).

### 2.4 O Estado como Regulador e Regulado: um diagnóstico estrutural, não uma tese

A observação que abre este artigo — o Estado como regulador e maior usuário de algoritmos, "Do Poder-Dever ao Dever-Poder" — não é a tese, mas o diagnóstico estrutural que a fundamenta. Essa dupla posição gera um incentivo estrutural à subaplicação das normas que o próprio Estado edita, porque a aplicação plena (explicabilidade, contraditório prévio, proteção de dados, inclusão digital) reduziria a eficiência operacional que a Administração Pública 4.0 promete.

Esse incentivo decorre de ao menos três fontes. A primeira é a pressão por eficiência operacional: o INSS processa milhões de requerimentos anuais, e a inclusão de etapas de explicabilidade e contraditório em cada decisão automatizada pode ser percebida pelo gestor como obstáculo à celeridade. A segunda é a dependência de fornecedores privados de software, cujos algoritmos são frequentemente opacos para a própria Administração contratante, criando uma zona de irresponsabilidade: o órgão público alega que não pode explicar o que não conhece, e o fornecedor alega segredo comercial. A terceira é a ausência de sanções efetivas por insuficiência de explicabilidade: diferentemente da omissão de motivação em atos tradicionais — cujas consequências estão bem estabelecidas na jurisprudência (nulidade do ato, responsabilidade do agente, dever de indenizar) —, a opacidade algorítmica ainda não gerou corpo consolidado de responsabilização administrativa ou judicial no Brasil. A Lei nº 14.129/2021 menciona transparência e controle social como princípios (art. 3º), mas não comina sanção específica; a LGPD prevê sanções administrativas (art. 52), mas a ANPD ainda não consolidou entendimento sobre sua aplicação a decisões automatizadas do poder público.

O diagnóstico estrutural serve para evidenciar que a integração dos quatro eixos não é uma opção de política pública entre outras — é uma exigência constitucional que o Estado, por sua posição dual, tem incentivos estruturais para descumprir. As seções que seguem desenvolvem cada eixo a partir do marco teórico, diagnosticam a lacuna institucional brasileira e apresentam o Conselho de Contestação Algorítmica como ilustração concreta de como a integração pode ser materializada.

## 3 Marco teórico: a convergência dos eixos

O fundamento dogmático deste artigo articula quatro eixos extraídos de estudos especializados em direito digital. O primeiro é o contraditório algorítmico prévio, que exige que a decisão automatizada seja acompanhada de explicação compreensível *antes* de produzir efeitos, evitando que a revisão *a posteriori* torne-se mera formalidade (Tavares; Bitencourt; Cristóvam, 2024). O segundo eixo foca na autodeterminação informativa, lendo a proteção de dados não apenas como privacidade, mas como instrumento ativo de controle do titular sobre o ciclo de vida de seus dados, sob pena de violação da dignidade humana (Saito; Salgado, 2020; Sarlet; Molinaro, 2019).

O terceiro eixo concerne à governança e transparência qualificada, integrando governo aberto, infraestrutura de dados abertos e o uso orientado de evidências para viabilizar a *accountability* (Cristóvam; Hahn, 2020). A Lei nº 14.129/2021 (Governo Digital) estrutura essa arquitetura, embora sua aplicação municipal sofra com um federalismo de adesão que fragmenta a garantia (Tavares; Bitencourt; Cristóvam, 2021).

Esses três eixos convergem na explicabilidade algorítmica, dimensão transversal sem a qual o contraditório é vazio, a proteção de dados é ineficaz e a governança é formal. Essa estrutura 3:1+1 reflete a tese central: a legitimidade da decisão automatizada é sempre resultado de uma integração, nunca de uma perspectiva isolada. Cada eixo mapeia-se em personas do Conselho de Contestação Algorítmica: a Defensoria (processo), o Cidadão (dados), o Administrador (governança) e o Cientista de Dados (explicabilidade).

## 4 Da transparência à contestabilidade: o gap normativo e institucional

O cenário brasileiro de contestação de decisões administrativas digitais é marcado por uma fragmentação que impede o cidadão de exercer, de forma integrada e compreensível, o direito de compreender, contestar e reverter decisões automatizadas que afetam seus direitos.

O Fala.BR, plataforma integrada de ouvidoria e acesso à informação gerida pela Controladoria-Geral da União, alcança mais de 310 órgãos do Executivo Federal e permite a manifestação de cidadãos por meio de pedidos de acesso à informação, denúncias, sugestões e reclamações. Sua relevância institucional é inegável, mas sua função é a de canal de comunicação, não a de ferramenta de análise jurídica. O Fala.BR não gera minutas, não explica critérios algorítmicos, não mapeia dados utilizados em decisões automatizadas e não oferece orientação jurídica personalizada ao cidadão afetado (Brasil, [s.d.]a).

O "Conteste Aqui", funcionalidade do Cadastro Único lançada em 2025, permite que cidadãos e gestores municipais contestem divergências em dados integrados automaticamente. A ferramenta é relevante para o universo específico do Programa Bolsa Família, mas seu alcance é limitado a esse contexto: não abrange decisões algorítmicas amplas, não oferece explicabilidade sobre os critérios de decisão e não gera recursos jurídicos (Brasil, 2025). O módulo de contestação do Auxílio Emergencial, disponibilizado pela Dataprev em 2020, era restrito a um benefício temporalmente delimitado e não oferecia análise jurídica ou explicabilidade algorítmica (Brasil, 2020). O ecossistema Gov.br reconhece o direito de solicitar revisão de decisões automatizadas com fundamento no artigo 20 da LGPD, mas o instrumento permanece um canal de comunicação — sem apoio para formular a solicitação, sem tradução dos critérios algorítmicos e sem geração de estratégia jurídica (Brasil, [s.d.]b).

A análise dessas plataformas — que não pretende ser exaustiva, mas baseada em plataformas governamentais publicamente documentadas nos portais da CGU, Dataprev, DPU e Gov.br — revela uma lacuna estrutural: nenhuma integra explicabilidade algorítmica, mapeamento de dados, geração de peças jurídicas e simulação de exclusão digital num único fluxo acessível ao cidadão.

A Tabela 1 sistematiza essa fragmentação, comparando as funcionalidades oferecidas por cada plataforma com aquelas que o GovLens/DueProcess.AI integra num único fluxo.

Tabela 1 — Comparativo de funcionalidades: plataformas existentes × GovLens

| Funcionalidade | Fala.BR | Conteste Aqui | Dataprev (Auxílio) | Gov.br (LGPD) | GovLens |
|---|---|---|---|---|---|
| Canal de manifestação | Sim | Sim | Sim | Sim | — |
| Explicabilidade algorítmica | Não | Não | Não | Não | Sim |
| Mapeamento de dados utilizados | Não | Não | Não | Não | Sim |
| Geração de minutas jurídicas | Não | Não | Não | Não | Sim |
| Auditoria de viés algorítmico | Não | Não | Não | Não | Sim |
| Simulação de exclusão digital | Não | Não | Não | Não | Sim |
| Avaliação cruzada multiperspectiva | Não | Não | Não | Não | Sim |

Fonte: elaboração própria com base na análise documental das plataformas (2026).

As plataformas existentes não são deficientes — cumprem as funções para as quais foram desenhadas. A lacuna está na ausência de um instrumento que as complemente com as funções que nenhuma delas se propõe a exercer. O GovLens não concorre com essas plataformas — ele as pressupõe e as complementa.

A lacuna não é apenas funcional — é democrática. Schiefler, Cristóvam e Sousa (2020) alertavam que a Administração Pública digital pode aprofundar exclusões se o acesso à tecnologia não for tratado como condição democrática da cidadania administrativa. A TIC Domicílios 2024, pesquisa do Comitê Gestor da Internet no Brasil e do Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação, registrou que apenas 22% da população brasileira com dez anos ou mais possuía conectividade significativa — definida como acesso regular a Internet banda larga em dispositivos pessoais. Na classe A, o índice chegava a 73%; nas classes DE, caía para 3% (CGI.br; Cetic.br, 2024). Um serviço público "100% digital" pode ser formalmente disponível e materialmente inacessível para a maioria da população.

Dessa forma, a cidadania administrativa, conceituada como o direito de o cidadão participar ativamente da formação das decisões públicas que o afetam, é esvaziada quando convertida em um dever de autoatendimento digital sem suporte estatal. A exclusão digital deixa de ser um mero problema de infraestrutura e passa a ser compreendida como um óbice constitucional intransponível à própria cidadania administrativa. Como apontam Schiefler, Cristóvam e Sousa (2020), o avanço para a Administração Pública digital deve ser acompanhado de políticas de fomento ao acesso e à literacia tecnológica, sob pena de a digitalização atuar como um filtro censitário que aparta os cidadãos mais vulneráveis da fruição de seus direitos fundamentais perante o Estado.

A transparência, portanto, não é sinônimo de contestabilidade. Um portal pode ser transparente sem ser compreensível. Uma decisão pode ser pública sem ser contestável. A distância entre a transparência formal e a contestabilidade efetiva é o espaço onde a Administração Pública 4.0 produz decisões que o cidadão não compreende, não contesta e não reverte — mesmo quando a Constituição exige que possa fazê-lo.

## 5 O Conselho de Contestação Algorítmica: concepção e funcionamento

O GovLens/DueProcess.AI é um protótipo acadêmico desenvolvido para ilustrar, em artefato concreto, como a integração dos quatro eixos dogmáticos pode ser materializada. Não é uma ouvidoria digital, tampouco um produto comercial — e não pretende substituir a atuação de defensores, advogados ou controladores. Sua função é heurística: demonstrar que a tese da integração como condição de validade pode ser operacionalizada em software. Trata-se de uma prova de conceito (*proof of concept*), não de uma validação empírica: o artefato é tecnicamente viável e opera conforme projetado, mas seus efeitos no mundo — aumento da compreensão do cidadão, efetividade do contraditório — são objeto de pesquisa futura (Seção 8). Seu conceito-chave é contestabilidade: uma decisão administrativa deve poder ser compreendida, questionada, auditada e, quando inadequada, revertida por meios administrativos.

O núcleo do protótipo é o Conselho de Contestação Algorítmica. Sua premissa é que nenhuma perspectiva isolada — nem a jurídico-processual, nem a técnico-explicativa, nem a de governança, nem a do titular dos dados — é suficiente para avaliar a legitimidade de uma decisão automatizada. A avaliação precisa ser múltipla, cruzada e sintética.

O Conselho opera em três fases. Na Fase 1, cada uma das quatro personas emite um parecer independente sobre a decisão submetida, fundamentado com referência a dispositivos legais, princípios constitucionais e literatura especializada. Na Fase 2, os pareceres são submetidos a avaliação cruzada anônima: cada persona recebe os pareceres das demais — sem identificação de autoria — e emite uma avaliação crítica, identificando concordâncias, divergências, lacunas e contradições. A anonimidade visa reduzir o viés de autoridade e forçar o enfrentamento argumentativo. Na Fase 3, o Relator — uma quinta instância do sistema — lê os quatro pareceres originais e as doze avaliações cruzadas e produz uma síntese fundamentada, integrando as perspectivas, resolvendo contradições quando possível e sinalizando quando a contradição é substantiva e irresolvível.

### 5.1 Mapeamento entre persona, artigo e eixo jurídico

Três artigos oferecem perspectivas distintas e complementares; um quarto eixo — explicabilidade — atravessa todos. A Defensoria Pública carrega a voz processual: contraditório e ampla defesa (art. 5º, LV, CF), motivação do ato (art. 50, Lei nº 9.784/1999), meios efetivos de impugnação — é o eixo de Tavares, Bitencourt e Cristóvam (2024). O Cientista de Dados não se filia a um único artigo; opera transversalmente sobre explicabilidade e viés algorítmico: os critérios e pesos do sistema são compreensíveis para um não-especialista? Há *proxies* de raça, gênero ou território? O Administrador Público representa a governança — Cristóvam e Hahn (2020) — e pergunta se a decisão é compatível com a Lei do Governo Digital, se os dados vêm de bases abertas e se a implementação respeita o desenho federativo. O Cidadão/Direitos Digitais fala pelo titular: autodeterminação informativa, base legal do tratamento, minimização de dados, exercício real do direito de revisão do artigo 20 da LGPD — eixo de Saito e Salgado (2020) e Sarlet e Molinaro (2019).

### 5.2 O que o Conselho evidencia que a dogmática isoladamente não evidencia

Encarnar a dogmática em software produz efeitos que o texto acadêmico, sozinho, não produz — embora a afirmação deva ser lida como hipótese de design, não como resultado de validação empírica. Cada persona é forçada a emitir parecer fundamentado com referência a dispositivos legais e princípios específicos; a vagueza tolerável no artigo é rejeitada pelo sistema. A avaliação cruzada expõe contradições que a exposição sequencial dos eixos oculta: quando a Defensoria defende o contraditório prévio como absoluto e o Administrador Público insiste na celeridade, a tensão materializa-se nos pareceres e precisa ser enfrentada pelo Relator.

A síntese evidencia que os eixos são complementares, não concorrentes — e que a legitimidade da Administração Pública 4.0 depende da integração de todos. Mas a integração não é mera justaposição de perspectivas. O Conselho revela que certas tensões são constitutivas, não acidentais: a eficiência administrativa e o contraditório prévio estão em tensão permanente, e nenhum arranjo institucional elimina essa tensão — apenas a administra. O Relator, ao sintetizar os pareceres, não resolve a tensão entre celeridade e devido processo; ele a expõe como dado estrutural da Administração Pública algorítmica, e recomenda que, no caso concreto, um dos polos deva prevalecer — fundamentadamente.

Esse é o ganho analítico de materializar a dogmática em software: as contradições que o texto acadêmico pode contornar com parágrafos de transição, o código precisa enfrentar como regra de decisão.

### 5.3 Implementação

O GovLens/DueProcess.AI é um protótipo *full-stack* com código aberto, implementado em Python (FastAPI) no backend e React (Vite) no frontend, com comunicação com os modelos de linguagem intermediada pelo OpenRouter. O código-fonte está disponível publicamente no repositório `github.com/anavvanzin/algoritmo-em-disputa`. O detalhamento da arquitetura foge ao escopo jurídico deste artigo; o que importa reter é que o Conselho é um sistema funcional que, alimentado com um caso, produz pareceres fundamentados, avaliações cruzadas e minutas jurídicas.

## 6 Caso-âncora: o INSS e a negativa automática de aposentadoria rural

O cenário que ancora a proposta é o indeferimento de aposentadoria rural pelo Instituto Nacional do Seguro Social — situação reconhecível por profissionais da Defensoria Pública e da advocacia previdenciária. O segurado rural, frequentemente em situação de vulnerabilidade socioeconômica e digital, solicita o benefício; o sistema do INSS cruza dados do Cadastro Nacional de Informações Sociais e de outras bases; e o indeferimento é emitido com motivação padronizada que, segundo relatos de defensores públicos, pode não identificar quais dados foram utilizados, quais critérios foram aplicados ou como contestar. A descrição baseia-se em padrões documentados na literatura previdenciária e em relatos de órgãos de defesa, embora o artigo não disponha de levantamento empírico próprio sobre a frequência de indeferimentos automatizados.

O caso do segurado rural exemplifica com precisão o que Tavares, Bitencourt e Cristóvam (2024) denominam como o "problema da redução da realidade a dados". A atividade do trabalhador rural é marcada pela informalidade, sazonalidade e, frequentemente, pela escassez de registros digitais formais. Sua vida de trabalho, vivida de forma corpórea no campo, é uma realidade complexa e multifacetada que não se deixa apreender de modo integral por cadastros de dados padronizados. Ao realizar o cruzamento automático de bases de dados administrativas (como o CNIS e o CPF), o sistema operacionaliza uma redução ontológica: o trabalhador real é substituído por sua representação cadastral incompleta. Se um dado inexiste no cadastro, para o algoritmo, o fato simplesmente inexiste na realidade. Essa redução funciona como uma barreira invisível e intransponível para o cidadão vulnerável, cuja subsistência depende justamente de elementos fáticos (prova testemunhal, início de prova material precária, verificação de condições de vida locais) que a frieza dos cruzamentos automatizados descarta em nome da padronização e da eficiência administrativa.

A situação agrava-se quando o indeferimento é emitido em desconformidade com a Instrução Normativa nº 128/2022 do INSS, que regula a concessão de benefícios previdenciários e estabelece critérios específicos para a comprovação de atividade rural — incluindo a admissão de início de prova material e de prova testemunhal complementar. Se um sistema automatizado ignorasse ou subaplicasse esses critérios, produzindo indeferimentos que a instrução normativa não autoriza, a decisão violaria simultaneamente o princípio da legalidade (art. 5º, II, CF), o contraditório e a ampla defesa (art. 5º, LV, CF) e a motivação obrigatória de atos administrativos (art. 50, Lei nº 9.784/1999).

O precedente internacional que ilumina o caso por analogia é o do Sistema de Risco Indicativo de Fraude (SyRI), utilizado pelo governo dos Países Baixos para detectar fraudes em benefícios sociais. Em 5 de fevereiro de 2020, a Corte Distrital de Haia (*Rechtbank Den Haag*, ECLI:NL:RBDHA:2020:1878) declarou que o sistema violava o artigo 8º da Convenção Europeia de Direitos Humanos por insuficiência de salvaguardas legais e operacionais. A Corte considerou que a opacidade do algoritmo, a ausência de supervisão humana efetiva e o impacto desproporcional sobre populações vulneráveis tornavam o sistema incompatível com os direitos fundamentais. O precedente é frequentemente citado na literatura brasileira sobre governança algorítmica, e a sua *ratio decidendi* é transponível ao contexto nacional por analogia, ainda que a Convenção Europeia não se aplique ao ordenamento jurídico brasileiro.

A transposição exige, porém, cautela. A Corte Distrital de Haia decidiu com base no artigo 8º da Convenção Europeia de Direitos Humanos, que protege o direito ao respeito à vida privada e familiar — um registro normativo distinto do artigo 5º, LV, da Constituição Federal, que garante o contraditório e a ampla defesa. No Brasil, a ausência de precedente judicial equivalente sobre automação decisória administrativa significa que a *ratio decidendi* do SyRI precisa ser reconstruída sobre fundamentos constitucionais próprios — o que este artigo esboça, mas não esgota. O SyRI é, portanto, ilustração comparada, não precedente direto.

O cenário do INSS apresenta, hipoteticamente, elementos análogos àqueles que a Corte Distrital de Haia condenou: opacidade algorítmica, impacto sobre população vulnerável, ausência de contraditório prévio e motivação insuficiente.

Quando alimentado com o caso INSS, o Conselho produziria um parecer no qual a Defensoria Pública identifica a ausência de contraditório prévio e a motivação insuficiente; o Cientista de Dados sinaliza o risco de viés territorial (segurados rurais em municípios com menor cobertura digital podem ter dados cadastrais menos atualizados); o Administrador Público avalia a compatibilidade com a Lei do Governo Digital e a IN 128/2022; e o Cidadão/Direitos Digitais examina se o segurado foi informado da automação e se pode exercer o direito de revisão do artigo 20 da LGPD. O Relator sintetiza os pareceres e recomenda: pedido de acesso à informação; requerimento de revisão com fundamento no artigo 20 da LGPD; recurso administrativo (arts. 56 e seguintes da Lei nº 9.784/1999); e comunicação à Defensoria Pública da União.

A demonstração com o caso INSS permite três observações de design — hipóteses a validar, não resultados empíricos. Primeiro, as personas convergiram na identificação da violação de direitos, mas divergiram na ênfase: a Defensoria priorizou o vício processual, o Cientista de Dados o viés sistêmico, o Administrador Público a desconformidade normativa e o Cidadão a violação da autodeterminação informativa. Essa divergência não é fraqueza — é o que a avaliação cruzada se propõe a expor: a mesma decisão parece diferente conforme o eixo de análise, e a tarefa do Relator é integrar essas diferenças sem apagá-las.

Segundo, a Fase 2 capturou uma imprecisão relevante: o Cientista de Dados mencionou "algoritmo de *machine learning*" como hipótese, mas a Defensoria observou, na avaliação cruzada, que o sistema do INSS pode operar com regras determinísticas — e que a distinção entre sistema opaco por complexidade e sistema opaco por falta de transparência é juridicamente relevante. O Relator incorporou a correção na síntese.

Terceiro, o Conselho gerou minutas operacionais — pedido de acesso à informação, requerimento de revisão e recurso administrativo — que, embora não substituam defensor ou advogado, oferecem ao cidadão um ponto de partida concreto, com campos a preencher e estrutura jurídica preservada.

## 7 Contribuições normativas: literacia algorítmica e notícia humana

Além do mapeamento entre persona e artigo, o GovLens/DueProcess.AI incorpora duas contribuições normativas que ultrapassam a dogmática apresentada nos artigos do seminário e que constituem a camada autoral diferenciadora da proposta.

### 7.1 Literacia algorítmica como condição de eficácia do contraditório

O contraditório algorítmico, tal como formulado por Tavares, Bitencourt e Cristóvam (2024), pressupõe que o cidadão saiba que a decisão que o afetou foi automatizada e compreenda, em termos básicos, o que isso significa. A experiência empírica demonstra que essa premissa frequentemente não se sustenta. Muitos cidadãos não distinguem uma decisão administrativa tomada por um servidor daquela produzida por um sistema algorítmico; recebem a negativa do INSS como se fosse uma decisão humana e não sabem que o contraditório prévio foi suprimido por automação.

A literacia algorítmica — isto é, a capacidade de compreender que decisões são tomadas por algoritmos, de identificar os dados que as alimentam e de saber que o direito de contestar existe — constitui um degrau anterior à contestação. Distingue-se da transparência: um portal pode ser transparente (disponibilizando dados e critérios) sem ser compreensível (se o cidadão não dispõe de ferramentas cognitivas para processar a informação). A inteligibilidade é a propriedade de a informação ser processável por seu destinatário; a transparência é a propriedade de a informação estar disponível.

O protótipo materializa essa contribuição por meio de uma camada propedêutica — denominada "Você sabe que foi uma máquina?" — que precede o acesso às telas de análise e contestação. Antes de permitir a contestação, a plataforma apresenta, em linguagem cidadã, uma explicação sobre o que é uma decisão algorítmica, por que ela pode ser diferente de uma decisão humana e qual é o direito do cidadão mesmo quando a decisão parece automática e definitiva. Essa camada não é uma formalidade; é uma condição de eficácia do contraditório. Sem ela, o contraditório é juridicamente reconhecido, mas materialmente inacessível.

A distinção entre acesso formal e acesso material ao contraditório algorítmico é análoga à distinção que a literatura constitucional brasileira estabelece entre igualdade formal e igualdade material: a previsão normativa do direito não basta se o titular não dispõe das condições fáticas para exercê-lo. A literacia algorítmica é, nesse sentido, uma condição material do contraditório — assim como a assistência jurídica gratuita é condição material do acesso à justiça (art. 5º, LXXIV, CF). O Estado que automatiza decisões sem garantir que o cidadão compreenda o que é uma decisão automatizada não está apenas sendo ineficiente na comunicação — está produzindo uma desigualdade material no exercício do direito de defesa.

### 7.2 Notícia humana para decisões adversas dirigidas a vulneráveis

A segunda contribuição normativa decorre de uma observação que a bibliografia do seminário não desenvolve explicitamente: a distinção entre o *momento da decisão* e o *momento da comunicação*. A dogmática do contraditório algorítmico concentra-se na decisão — seus critérios, seus dados, sua explicabilidade. Mas a comunicação da decisão adversa a uma pessoa em situação de vulnerabilidade é, ela mesma, um ato administrativo que pode ferir a dignidade.

Quando o INSS nega automaticamente a aposentadoria rural de um trabalhador analfabeto de setenta anos, a negativa não chega como resultado de uma interlocução humana — chega como uma notificação padronizada, frequentemente incompreensível, sem orientação sobre como contestar. O cidadão vulnerável não apenas perde o benefício; perde a possibilidade de compreender por que perdeu e o que pode fazer. A dignidade do administrado está também em como ele é avisado.

A tese normativa que este artigo propõe é a seguinte: decisões administrativas automatizadas podem ser legítimas quando os critérios são explicáveis e o contraditório é assegurado, mas a comunicação de uma decisão adversa a uma pessoa em situação de vulnerabilidade deveria ser feita por um ser humano — ou, no mínimo, por um sistema que simule a mediação humana de forma significativa — e não por uma notificação automática fria. O humano no circuito não apenas na decisão, mas no cuidado da comunicação.

O protótipo materializa essa contribuição por meio de um flag de "notícia humana": casos sinalizados como vulneráveis (idoso, analfabeto, rural, sem conectividade significativa) que envolvam decisão adversa (negativa de benefício, corte de auxílio) disparam uma recomendação de comunicação assistida, não notificação automática. A recomendação não é vinculante — o protótipo é acadêmico — mas sinaliza que a arquitetura de uma Administração Pública 4.0 democraticamente legítima deve considerar não apenas o que decide, mas como comunica a decisão aos mais vulneráveis.

É preciso antecipar duas objeções. A primeira é a da escala: notificação humana para decisões adversas em massa parece economicamente inviável. A resposta é que o princípio da notícia humana não exige notificação individualizada em todos os casos — exige que a arquitetura do sistema não trate a comunicação como etapa irrelevante, delegando-a a uma notificação automática fria por *default*. O *default* deve ser a mediação humana; a automação deve ser exceção justificada. A segunda objeção é a do paternalismo: tratar vulneráveis como se precisassem de proteção especial pode ser forma de exclusão. A resposta é que a notícia humana não se funda na suposta incapacidade do vulnerável, mas na assimetria de poder entre Estado e administrado: quando o Estado decide sobre o benefício de um trabalhador rural analfabeto, a mera formalidade da notificação automática perpetua essa assimetria. A mediação humana é, aqui, medida de igualdade substantiva.

## 8 Limites e direções de pesquisa

O protótipo não foi validado com usuários reais. A demonstração usa cenário hipotético e personas simuladas por LLMs; se o cidadão de fato compreende a análise, se as minutas são juridicamente adequadas, se a experiência reduz a impotência — são questões empíricas que só testes com defensorias, clínicas jurídicas e cidadãos afetados podem responder. A validação empírica é a direção prioritária de pesquisa futura.

Os modelos de linguagem podem alucinar fundamentação jurídica: citar artigos inexistentes, confundir dispositivos, produzir texto superficialmente convincente mas incorreto. Esse risco é particularmente agudo no direito administrativo brasileiro, onde a legislação é fragmentada, as instruções normativas são numerosas e a jurisprudência dos tribunais de contas e dos tribunais regionais federais nem sempre está indexada de forma acessível aos modelos. O protótipo mitiga parcialmente esse risco com instruções de sistema detalhadas e com a avaliação cruzada — no caso INSS, as referências legais citadas pelo Conselho foram verificadas manualmente e confirmadas como corretas, e a Fase 2 capturou imprecisões corrigidas pelo Relator. Mas um teste unitário não substitui verificação sistemática em maior escala. A mitigação mais robusta exigiria *retrieval-augmented generation* (RAG) com base em repositórios oficiais de legislação e jurisprudência atualizados, o que não está implementado na versão atual do protótipo.

Há também o limite de custo. Cada caso submetido ao Conselho dispara quatro chamadas na Fase 1, doze na Fase 2 e uma na Fase 3 — dezessete chamadas a APIs de modelos de linguagem, que, dependendo do modelo selecionado e da extensão dos pareceres, podem representar um custo significativo se o sistema fosse escalado para uso institucional. O protótipo não incorpora estimativa de custo por caso, e a viabilidade econômica de uma versão operacional do Conselho depende de otimizações como cache de pareceres similares, uso de modelos menores para a Fase 2 e redução do número de avaliações cruzadas sem perda de qualidade analítica.

O foco no âmbito federal (INSS, LGPD, LAI, Lei do Governo Digital) limita a generalização. Decisões municipais — licenças, alvarás, benefícios locais — exigem adaptação das personas, das bases de referência e das minutas; o federalismo de adesão da Lei nº 14.129/2021 torna isso necessariamente caso a caso.

O limite jurisprudencial da analogia com o SyRI já foi explicitado na Seção 6: a reconstrução da *ratio decidendi* sobre fundamentos constitucionais brasileiros é tarefa que este artigo esboça, mas que só um corpo de decisões nacionais poderá consolidar.

A infraestrutura digital é limite material. Para o cidadão sem conectividade significativa — 78% da população com dez anos ou mais, segundo a TIC Domicílios 2024 — o protótipo não existe. Canais não-digitais (USSD, SMS, atendimento presencial) estão fora do escopo.

As direções de pesquisa futura incluem: validação empírica com usuários reais; ampliação do corpus de casos-teste; avaliação comparativa com plataformas de contestação em outros ordenamentos jurídicos; e investigação sobre a responsabilização administrativa e judicial por insuficiência de explicabilidade em decisões automatizadas.

## 9 Conclusão

A tese normativa que este artigo sustenta — a integração dos quatro eixos como condição de validade do ato administrativo automatizado — ancora-se no devido processo legal constitucional (art. 5º, LV, CF) e na Lei nº 9.784/1999, e é fundamentada pelo diagnóstico estrutural do Estado como Regulador e Regulado. O Conselho de Contestação Algorítmica ilustra como essa integração pode ser materializada: cada persona traduz um eixo em parecer, a avaliação cruzada expõe tensões que a dogmática isolada oculta, e o Relator produz uma síntese que o cidadão pode usar. O caso INSS condensa o argumento; o SyRI o ilumina por analogia, mas a ancoragem da tese é constitucional brasileira, não convencional europeia.

Duas contribuições vão além da bibliografia do seminário: a literacia algorítmica como condição material de eficácia do contraditório e a notícia humana como exigência da dignidade da pessoa humana (art. 1º, III, CF) no momento da comunicação de decisões adversas a vulneráveis. O GovLens/DueProcess.AI não resolve o problema da legitimidade da Administração Pública algorítmica; sua função é heurística — demonstrar que a tese da integração pode ser operacionalizada, desde que a dogmática jurídica, e não a arquitetura de software, oriente o desenho institucional.

\begin{center}
\textbf{From Power-Duty to Duty-Power: the Algorithmic Contestation Council as an Architecture of Due Process in Public Administration 4.0}
\end{center}

\begin{center}
\textbf{Abstract}
\end{center}

\begin{singlespace}
\small
\noindent This article argues that, in the context of algorithmic Public Administration, due process of law — guaranteed by article 5, LV, of the Brazilian Federal Constitution and specified by Law No. 9,784/1999 — requires the integration of four axes: prior adversarial participation, qualified legal reasoning (which presupposes, but is not reducible to, technical explainability), institutional governance with qualified transparency, and personal data protection. The absence of any of these axes invalidates an automated decision. The structural diagnosis supporting this thesis is that the Brazilian State simultaneously occupies the position of regulator of algorithmic use and of the largest user of those same algorithms — a dual position that this article calls “From Power-Duty to Duty-Power” and that creates structural incentives for underenforcement of the rules enacted by the State itself. Based on the analysis of four articles published in specialized digital-law journals, the article illustrates the integration thesis through GovLens/DueProcess.AI, an academic prototype centered on the Algorithmic Contestation Council, a system of four legal-technical personas that issue cross-reviewed opinions and produce a reasoned synthesis. The anchor case is the denial of a rural retirement benefit by the Brazilian National Social Security Institute (INSS), analogically contrasted with the Dutch District Court of The Hague’s 2020 precedent on the System Risk Indication (SyRI). The article proposes two original normative contributions: algorithmic literacy as a material condition for effective adversarial participation and the principle of human notification for adverse decisions directed at vulnerable persons.
\end{singlespace}

\noindent\textbf{Keywords:} Digital Public Administration; algorithmic contestability; due process of law; explainability; personal data protection; artificial intelligence in the public sector.

\begin{center}
\textbf{Referências}
\end{center}

\begingroup
\singlespacing
\setlength{\parindent}{0pt}
\raggedright

## Referências


BRASIL. Constituição da República Federativa do Brasil de 1988. Brasília, DF: Presidência da República, 1988. Disponível em: <https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm>. Acesso em: 12 jul. 2026.

BRASIL. Controladoria-Geral da União. Fala.BR: visão geral. Brasília, DF: CGU, [s.d.]a. Disponível em: <https://www.gov.br/acessoainformacao/pt-br/falabr/visao-geral/falabr/>. Acesso em: 12 jul. 2026.

BRASIL. Governo Federal. Governo habilita novo canal para contestação do auxílio. Brasília, DF, 4 ago. 2020. Disponível em: <https://www.gov.br/pt-br/noticias/assistencia-social/2020/08/governo-habilita-novo-canal-para-contestacao-do-auxilio>. Acesso em: 12 jul. 2026.

BRASIL. Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome. Informe nº 69: a funcionalidade Conteste Aqui já está disponível no Portal do Cadastro Único. Brasília, DF, 23 maio 2025. Disponível em: <https://www.gov.br/mds/pt-br/acoes-e-programas/cadastro-unico/informes/2025/informe_cadastro_unico_n_69>. Acesso em: 12 jul. 2026.

BRASIL. Secretaria-Geral da Presidência da República. Termo de uso e política de privacidade. Brasília, DF, [s.d.]b. Disponível em: <https://www.gov.br/secretariageral/pt-br/termo-de-uso-e-politica-de-privacidade/termo-de-uso/termo-de-uso/>. Acesso em: 12 jul. 2026.

BRASIL. Lei nº 9.784, de 29 de janeiro de 1999. Regula o processo administrativo no âmbito da Administração Pública Federal. Brasília, DF: Presidência da República, 1999. Disponível em: <https://www.planalto.gov.br/ccivil_03/leis/l9784.htm>. Acesso em: 12 jul. 2026.

BRASIL. Lei nº 12.527, de 18 de novembro de 2011. Regula o acesso a informações. Brasília, DF: Presidência da República, 2011. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm>. Acesso em: 12 jul. 2026.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais. Brasília, DF: Presidência da República, 2018. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>. Acesso em: 12 jul. 2026.

BRASIL. Lei nº 14.129, de 29 de março de 2021. Dispõe sobre princípios, regras e instrumentos para o Governo Digital e para o aumento da eficiência pública. Brasília, DF: Presidência da República, 2021. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14129.htm>. Acesso em: 12 jul. 2026.

BRASIL. Instituto Nacional do Seguro Social. Instrução Normativa PRES/INSS nº 128, de 28 de março de 2022. Disciplina as regras, procedimentos e rotinas necessárias à efetiva aplicação das normas de direito previdenciário. Brasília, DF: INSS, 2022. Disponível em: <https://www.gov.br/inss/pt-br/centrais-de-conteudo/legislacao/instrucao-normativa/2022>. Acesso em: 12 jul. 2026.

COMITÊ GESTOR DA INTERNET NO BRASIL; CENTRO REGIONAL DE ESTUDOS PARA O DESENVOLVIMENTO DA SOCIEDADE DA INFORMAÇÃO. **TIC Domicílios 2024**. São Paulo: CGI.br/Cetic.br, 2024.

CRISTÓVAM, José Sérgio da Silva. **Administração Pública democrática e supremacia do interesse público**: novo regime jurídico-administrativo e seus princípios constitucionais estruturantes. Curitiba: Juruá, 2015.

CRISTÓVAM, José Sérgio da Silva; HAHN, Tatiana Meinhart. Administração Pública orientada por dados: governo aberto e infraestrutura nacional de dados abertos. **Revista de Direito Administrativo e Gestão Pública**, Florianópolis, v. 6, n. 1, p. 1-24, jan./jun. 2020. DOI: https://doi.org/10.26668/IndexLawJournals/2526-0073/2020.v6i1.6388. Disponível em: https://www.indexlaw.org/index.php/rdagp/article/view/6388. Acesso em: 11 jul. 2026.

DI PIETRO, Maria Sylvia Zanella. **Direito administrativo**. 36. ed. Rio de Janeiro: Forense, 2022.

JUSTEN FILHO, Marçal. **Curso de direito administrativo**. 14. ed. São Paulo: Revista dos Tribunais, 2023.

MELLO, Celso Antônio Bandeira de. **Curso de direito administrativo**. 35. ed. São Paulo: Malheiros, 2021.

RECHTBANK DEN HAAG. **ECLI:NL:RBDHA:2020:1878**. Corte Distrital de Haia, 5 fev. 2020. Disponível em: <https://deeplink.rechtspraak.nl/uitspraak?id=ECLI:NL:RBDHA:2020:1878>. Acesso em: 10 jul. 2026.

SAITO, Vitória Hiromi; SALGADO, Eneida Desiree. Privacidade e proteção de dados: por uma compreensão ampla do direito fundamental em face da sua multifuncionalidade. **International Journal of Digital Law**, Belo Horizonte, v. 1, n. 3, p. 117-137, set./dez. 2020. DOI: https://doi.org/10.47975/IJDL/3hiromi. Disponível em: https://journal.nuped.com.br/index.php/revista/article/view/saito2020. Acesso em: 11 jul. 2026.

SARLET, Gabrielle Bezerra Sales; MOLINARO, Carlos Alberto. Questões tecnológicas, éticas e normativas da proteção de dados pessoais na área da saúde em um contexto de big data. **Revista Brasileira de Direitos Fundamentais & Justiça**, Belo Horizonte, ano 13, n. 41, p. 183-212, jul./dez. 2019. DOI: https://doi.org/10.30899/dfj.v13i41.811. Acesso em: 12 jul. 2026.

SCHIEFLER, Eduardo André Carvalho; CRISTÓVAM, José Sérgio da Silva; SOUSA, Thanderson Pereira de. Administração Pública digital e a problemática da desigualdade no acesso à tecnologia. **International Journal of Digital Law**, Belo Horizonte, v. 1, n. 2, p. 97-116, maio/ago. 2020. DOI: https://doi.org/10.47975/IJDL/1schiefler. Disponível em: https://journal.nuped.com.br/index.php/revista/article/view/schiefler2020. Acesso em: 11 jul. 2026.

TAVARES, André Afonso; BITENCOURT, Caroline Müller; CRISTÓVAM, José Sérgio da Silva. Explicabilidade e contraditório algorítimico nas decisões automatizadas no setor público: as decisões em processos apoiados em algoritmos e o problema da redução da realidade a dados. **Diké – Revista Jurídica**, Vitória da Conquista, v. 23, n. 27, p. 2-32, set./dez. 2024. DOI: https://doi.org/10.36113/dike.27.2024.4556. Acesso em: 12 jul. 2026.

TAVARES, André Afonso; BITENCOURT, Caroline Müller; CRISTÓVAM, José Sérgio da Silva. A Lei do Governo Digital no Brasil: análise das contribuições à transparência pública e à concretização do exercício do controle social. **Novos Estudos Jurídicos**, Itajaí, v. 26, n. 3, p. 788-813, set./dez. 2021. DOI: https://doi.org/10.14210/nej.v26n3.p788-814. Disponível em: <https://periodicos.univali.br/index.php/nej/article/view/18326>. Acesso em: 12 jul. 2026.

