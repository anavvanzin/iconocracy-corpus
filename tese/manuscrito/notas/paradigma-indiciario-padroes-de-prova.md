# Paradigma Indiciário e Padrões de Prova: Posição Metodológica da Tese

> **Documento teórico autônomo — Estágio C (precede revisão ampla do Cap. 2/metodologia)**
>
> Elaborado em agosto/2026 a partir da síntese do Consensus ("Iconografia Jurídica Feminista: Paradigma Indiciário e Evidência Metodológica", jul/2026) e da sessão Kimi (2026-07-31). Fecha issue #168. Bloqueia Estágio B (revisão do capítulo).

---

## Introdução: duas validações, não uma

O capítulo de metodologia desta tese — Capítulo 2, "Iconometria Jurídica: Método, Corpus e Codificação" — demonstra com cuidado que o protocolo IconoCode produz resultados *operacionalmente* robustos: os deltas entre metadados e análise de imagem são mensuráveis e auditáveis (§2.5); os indicadores de purificação discriminam regimes iconocráticos com significância estatística (p < 0,05 em oito dos dez indicadores no teste de Kruskal-Wallis); os casos paradigmáticos emergem de maneira consistente com as hipóteses teóricas.

O que o capítulo ainda não faz — e que este documento se propõe a construir — é legitimar *epistemologicamente* o padrão de prova subjacente. A questão não é "os números estão corretos?" (resposta: sim, verificável) mas sim "qual tipo de conhecimento esses números produzem, e por que esse tipo de conhecimento é suficiente para as afirmações que a tese faz?". Essa é uma pergunta filosófica antes de ser uma pergunta técnica, e responde-la exige confrontar três objeções que qualquer banca informada levantará:

1. **A objeção do empiricismo frustrado** (Roele, "dodging empiricism"): a tese usa linguagem quantitativa mas não satisfaz os critérios do empiricismo científico — não há amostras probabilísticas, não há condições controladas, os codificadores são modelos de IA.
2. **A objeção da concordância intercodificadores**: se os 10 indicadores foram codificados por um modelo de linguagem multimodal ("iconocode-opus-4.6-image"), que garantia há de que a codificação é válida?
3. **A objeção do silêncio arquivístico**: a tese já usa `#ausencia-alegorica` e analisa a contra-alegoria por ausência (US-020, §2.4), mas não ancora essa intuição em teoria — o que significa "ausência como dado" epistemologicamente?

Estas três objeções são respondidas pelos três fios que estruturam este documento.

---

## Fio 1 — Posição estratificada por nível panofskiano: o problema da concordância intercodificadores

### 1.1 Por que a concordância intercodificadores não é uniforme nos três níveis de Panofsky

A pergunta "o quanto dois codificadores concordam?" pressupõe que "codificador" e "codificação" são categorias unitárias. A primeira contribuição deste fio é desfazer essa suposição à luz da estrutura tripartida de Panofsky.

No **Nível 1** (pré-iconográfico), a codificação descreve propriedades observáveis: a figura está de pé ou sentada, segura espada ou balança, o fundo é arquitetônico ou não. Essas são afirmações sobre fenômenos verificáveis intersubjetivamente. A concordância entre codificadores é, em princípio, *alta e mensurável* por estatísticas como o percentual de concordância simples (PA = acordos / total). Kappa de Cohen seria calculável aqui, mas seu valor seria modesto: kappa corrige o acordo pela probabilidade aleatória, o que faz sentido quando as categorias são exaustivas, predeterminadas e *mutuamente exclusivas*. Para variáveis como "presença de espada" (sim/não), kappa é adequado. Para variáveis compostas como "postura" (dinâmica/estática/ambígua), a adequação depende do grau em que as categorias foram operacionalizadas antes da codificação.

No **Nível 2** (iconográfico), a situação muda. Identificar "qual alegoria é representada" exige conhecimento de convenções — saber que a mulher com barrete frígio é Marianne e não simplesmente "mulher com chapéu cônico". Esse conhecimento não é observable no sentido estrito; é *culturalmente mediado*. A concordância tende a ser mais alta entre especialistas (que compartilham o repertório) e mais baixa entre leigos. Mais importante: as unidades de análise não são pré-determinadas de forma independente da interpretação — decidir que a imagem contém "uma Pathosformel de luto" já é uma decisão interpretativa que não pode ser separada da observação.

Aqui entra a demonstração de Rau e Shih (2021) aplicada por analogia ao problema desta tese. Rau e Shih mostraram matematicamente que kappa pressupõe **unidades de análise predeterminadas, fixas e independentes do conteúdo**: no contexto de análise de gênero textual, eles demonstraram que aplicar kappa a categorias como "tom irônico" ou "argumento implícito" produz valores artificialmente baixos não por falta de concordância real, mas porque as categorias não satisfazem os pressupostos formais da estatística. O passo analógico para a codificação iconográfica deve ser construído explicitamente, não apenas invocado:

> **Analogia estrutural (Nível 2):** Assim como a identificação de "tom irônico" em um texto exige que o codificador *já tenha construído* a unidade de análise ("este segmento textual exprime ironia") antes de pontuá-la, a identificação de uma Pathosformel ativa numa imagem exige que o codificador *já tenha decidido* o que conta como "unidade Pathosformel" — e essa decisão é ela mesma interpretativa, não observacional. Kappa, aplicado ao Nível 2, mediria não concordância sobre o conteúdo mas concordância sobre a *unidade de análise*, colapsando duas etapas que são logicamente distintas.

No **Nível 3** (iconológico), a interpretação é francamente hermenêutica. Afirmar que "esta imagem manifesta o Contrato Sexual Visual" é uma proposição teórica que não pode ser confirmada ou refutada por contagem. Nenhuma estatística de concordância é adequada aqui — e nem precisa ser. A validade do Nível 3 é argumentativa: depende da coerência interna do argumento, da ancoragem nos Níveis 1 e 2, e da interlocução com a literatura.

### 1.2 A forma peculiar do problema quando os codificadores são modelos de IA

O protocolo IconoCode foi aplicado por um modelo de linguagem multimodal ("iconocode-opus-4.6-image"). Isso não é um segredo metodológico que a tese esconde; é uma decisão que precisa ser tematizada diretamente, porque a banca levantará a questão.

A objeção padrão à codificação por IA é: "como sabemos que o modelo não está alucinando?" Essa objeção pressupõe que o padrão de validade é a correspondência entre a saída do modelo e algum "gabarito humano" externo. Mas para os Níveis 2 e 3 da codificação panofskiana — que é o núcleo teórico desta tese —, não existe gabarito humano neutro. A interpretação iconológica é disputada entre historiadores da arte; a atribuição de um regime icoNocrático é uma proposição da própria tese, não um fato a confirmar.

O que a tese pode e deve oferecer é diferente:

1. **Auditabilidade do Nível 1**: para os indicadores pré-iconográficos (presença de atributos, postura, escala da figura), a codificação do modelo é verificável por qualquer observador com acesso à imagem. Os 335 itens do corpus são publicamente acessíveis nos arquivos de origem (Europeana, Gallica, LOC). A verificação independente é estruturalmente possível — o que equivale à replicabilidade em sentido forte.

2. **Consistência interna documentada**: a variação dos scores de endurecimento ao longo do corpus é *teoricamente coerente*: o regime FUNDACIONAL tem média mais baixa que o NORMATIVO, que tem média mais baixa que o MILITAR nos indicadores materiais; os outliers (Steinlen vs. Lelong) são explicáveis por propriedades identificáveis das imagens. Consistência interna não prova validade, mas torna a hipótese de codificação aleatória implausível.

3. **Declaração de limites**: para os indicadores do Nível 2 e 3, a tese não afirma que o modelo produziu "a interpretação correta"; afirma que produziu "uma interpretação teoricamente informada, coerente com o aparato conceitual da tese, e verificável pela cadeia de raciocínio documentada em cada relatório de codificação". Isso é epistêmico, não estatístico.

### 1.3 Resposta à objeção de Roele e o argumento de Moran e Braman

Roele ("dodging empiricism") argumenta que as humanidades digitais frequentemente adotam a forma do empiricismo (números, visualizações, estatísticas) sem seu conteúdo (amostragem, controle experimental, replicabilidade). A crítica é pertinente e esta tese não a evita.

A resposta adequada não é negar que a tese "desvia" do empiricismo stricto sensu — ela desvia, e desviar é uma decisão metodológica legítima num corpus de alegorias estatais do século XIX. A resposta é articular o padrão de prova alternativo que a tese adota e mostrar que esse padrão é defendido na literatura especializada.

Moran (2022), em sua análise da imagem como evidência jurídica, distingue entre **evidência proposicional** (a imagem como prova de um fato) e **evidência demonstrativa** (a imagem como ilustração de um argumento). A iconometria desta tese produz evidência *demonstrativa*: os scores de endurecimento não provam que o Estado "fez X"; demonstram que o corpus *exibe um padrão* compatível com a hipótese de que o Estado operou por purificação alegórica. A inferência da prática histórica a partir do padrão morfológico é indiciária — no sentido preciso de Ginzburg.

Braman (em Mnookin e Ristovska, 2023) vai mais longe: ao analisar estudos de prova visual em contexto jurídico, Braman argumenta que a objetividade da imagem como prova é sempre construída — não dada — e que os critérios de admissibilidade probatória mais rigorosos (*Daubert*, no direito norte-americano) exigem não replicabilidade cega mas *transparência do raciocínio inferencial*. Transposta para o contexto desta tese: o que valida a iconometria não é a possibilidade de reproduzir mecanicamente o mesmo score, mas a possibilidade de *reconstruir o raciocínio* que levou a cada score a partir dos relatórios de codificação disponíveis.

---

## Fio 2 — Legitimação indiciária: Ginzburg, Warburg/Didi-Huberman, Panofsky

### 2.1 Ginzburg: o paradigma indiciário como epistemologia alternativa

Em "Sinais: raízes de um paradigma indiciário" (GINZBURG, 1989, p. 143–179), Carlo Ginzburg identifica uma forma de conhecimento que ele denomina *paradigma indiciário* ou *sintomático*, distinto do paradigma galileano (baseado em leis gerais e experimentos reprodutíveis). O paradigma indiciário é definido por três características:

1. **Trabalha a partir de pistas, não de leis**: o médico que diagnostica uma doença a partir de sintomas, o detetive que infere o criminoso a partir de rastros, o historiador da arte que atribui uma obra a partir de detalhes minúsculos — todos eles reconstroem uma realidade singular a partir de traços que a revelam obliquamente.
2. **Opera por inferência ab singular**: ao contrário da lógica indutiva (do particular ao universal) e dedutiva (do universal ao particular), o paradigma indiciário infere *um* singular a partir de *outros* singulares, sem passar pelo universal como mediador necessário.
3. **Produz conhecimento probabilístico, não certo**: o diagnóstico é sempre "provavelmente X" com base nos sinais observados; a certeza absoluta é estruturalmente impossível (e, acrescenta Ginzburg, suspeita — pois geralmente indica simplificação).

Os três protótipos históricos que Ginzburg mobiliza — Giovanni Morelli (atribuição de pinturas por detalhes anatômicos menores), Sigmund Freud (psicanálise como leitura de sintomas) e Sherlock Holmes (dedução a partir de pistas) — convergem numa epistemologia que valida a inferência a partir do detalhe para o todo, sem que esse procedimento precise satisfazer os critérios de replicabilidade do experimento científico.

O paradigma indiciário legitima exatamente o movimento metodológico central desta tese: a inferência do *Contrato Sexual Visual* (o todo histórico-teórico) a partir dos scores de endurecimento e das análises iconológicas (os sinais particulares). Não é uma inferência estatística (do padrão à lei); é uma inferência indiciária (do vestígio à prática). A diferença é epistemologicamente crucial.

**Ancoragem explícita para o capítulo de metodologia**: Ginzburg (1989) deve aparecer como a espinha epistemológica da seção que justifica a combinação de análise quantitativa (detecção de padrões/sinais) com análise qualitativa aprofundada (inferência dos casos paradigmáticos). A sequência "quantitativo identifica casos anômalos → qualitativo interpreta as anomalias" *é* o paradigma indiciário em operação.

### 2.2 Warburg via Didi-Huberman: a inferência visual como epistemologia

Aby Warburg não formulou uma teoria explícita do conhecimento iconográfico, mas seu método — desenvolvido no Atlas Mnemosyne e nas preleções sobre Pathosformeln — pressupõe uma epistemologia que Didi-Huberman tornou filosóficamente explícita em *Devant le temps* (2000) e *L'image survivante* (2002).

O núcleo da epistemologia warburguiana, na reconstrução de Didi-Huberman, é a ideia de que as imagens *sobrevivem* — que os Pathosformeln da Antiguidade reaparecem em contextos historicamente distantes não por imitação consciente mas por *Nachleben* (sobrevivência ativa). Isso tem uma consequência metodológica que Didi-Huberman torna explícita: a análise das imagens não pode ser linear nem cumulativa (no sentido positivista); ela é *anacrónica*, montando justaposições entre imagens de períodos distintos para tornar visíveis as continuidades formais que a história linear apaga.

O método do Atlas Mnemosyne — a montagem de imagens em painéis sem hierarquia explícita — não é falta de argumento; é um argumento de outra forma. A justaposição *demonstra* a persistência do Pathosformel sem precisar enunciá-la em proposições verificáveis. Didi-Huberman chama isso de *saber por montagem* — um saber que é visual antes de ser discursivo.

Para esta tese, a implicação é direta: o Atlas Iconocrático (Capítulo 9) não precisa satisfazer os critérios do argumento proposicional para ser *válido epistemologicamente*. Sua validade é a da montagem warburguiana: a evidência está na justaposição, não na prova.

Mais ainda: Panofsky *direto* (1939, *Studies in Iconology*; 1955, *Meaning in the Visual Arts*) antecipou o problema epistemológico da iconologia ao distinguir entre "síntese intuitiva" (reconhecimento do tema iconográfico) e "intuição sintética" (compreensão do sentido último). Para Panofsky, o Nível 3 (iconológico) exige *"uma familiaridade com as tendências essenciais do espírito humano"* — o que é deliberadamente circular: só se reconhece o sentido iconológico de uma imagem se já se está inserido na tradição cultural que o produz. A circularidade não invalida o método; é sua condição. Isso é o que os epistemólogos depois chamariam de círculo hermenêutico.

### 2.3 Síntese: a cadeia epistemológica da tese

A posição epistemológica desta tese pode agora ser articulada como uma cadeia coerente:

1. **Panofsky** fornece a estrutura tripartida (pré-iconográfico → iconográfico → iconológico) que estratifica os tipos de afirmação em correspondência com os tipos de evidência admissíveis.
2. **Ginzburg** fornece a legitimação da inferência indiciária: o movimento do sinal particular à hipótese sobre a prática histórica não precisa passar pelo experimento controlado para ser epistemologicamente respeitável.
3. **Warburg/Didi-Huberman** fornece a legitimação da montagem visual como argumento: a justaposição de imagens no Atlas Iconocrático não é ornamento — é evidência na forma que lhe é própria.
4. **Moran e Braman** fornecem ancoragem jurídica: no próprio direito, a imagem como prova opera por inferência demonstrativa (não proposicional), e o critério de validade é a transparência do raciocínio, não a replicabilidade mecânica.

---

## Fio 3 — Silêncio arquivístico visual: Hartman, Fuentes e a ausência como dado

### 3.1 Hartman: a fabulação crítica como método para o irrepresentável

Em "Venus in Two Acts" (HARTMAN, 2008), Saidiya Hartman desenvolve o conceito de **fabulação crítica** (*critical fabulation*): um método que responde ao silêncio dos arquivos coloniais — em que as vidas das pessoas escravizadas aparecem apenas como notas marginais, inventários, registros de punição — imaginando o que poderia ter sido a partir dos fragmentos que sobreviveram, mantendo explícito o caráter especulativo dessa imaginação.

A fabulação crítica não é licença para inventar; é uma *disciplina do limite*: o pesquisador reconhece o que o arquivo não permite saber, articula o que o arquivo revela obliquamente, e declara explicitamente a fronteira entre evidência e inferência. Para Hartman, a declaração de limites não é confissão de fraqueza metodológica — é rigor epistêmico numa situação em que o silêncio do arquivo *é ele mesmo* um dado sobre a estrutura de poder que produziu o arquivo.

### 3.2 Fuentes: a violência epistêmica da ausência

Marisa Fuentes, em *Dispossessed Lives* (2016), analisa arquivos coloniais das Barbados para argumentar que a ausência de mulheres negras escravizadas como sujeitos nos documentos históricos não é um acidente — é uma consequência estrutural da violência epistêmica que organizava quem merecia ser registrado como agente histórico. A metodologia de Fuentes é arqueológica no sentido foucaultiano: ela escava os documentos à procura dos rastros deixados *ao redor* das ausências.

A transferência desse método para o corpus visual desta tese exige atenção ao que muda: o corpus iconocrático não é um arquivo colonial stricto sensu, mas compartilha uma estrutura homóloga. A **ausência de representação feminina historicamente específica** nas alegorias estatais — as mulheres *reais* apagadas para que a Mulher *alegórica* possa ocupar o lugar — é uma violência epistêmica de estrutura análoga. Não se registra quem é a mulher concreta cuja fisionomia foi usada como modelo de Marianne nos 36.000 bustos; não há arquivo que documente se ela consentiu com essa apropriação.

### 3.3 A ausência como dado no corpus desta tese

O corpus já operacionaliza essa intuição em dois lugares:

1. **Tag `#ausencia-alegorica`**: itens em que a ausência da alegoria feminina onde ela seria esperada pelas convenções é o dado analiticamente relevante.
2. **US-020 (Keppler, 1893)**: analisado no §2.4 como "subversão por ausência" — a contra-alegoria que funciona pela não-aparição de Columbia/Liberty numa cena de imigração.

O que falta é a ancoragem teórica explícita. Com Hartman e Fuentes, essa ancoragem pode ser formulada assim:

> **Proposição metodológica**: A ausência de representação alegórica feminina num corpus iconocrático não é lacuna documental a ser preenchida — é dado constitutivo que exige interpretação. A declaração explícita dessa ausência (tag `#ausencia-alegorica`) e a análise de sua função (US-020) são formas de validação epistêmica: a tese reconhece o que não está, articula por que não está, e declara os limites do que pode ser inferido a partir da não-presença.

Isso responde a uma pergunta que a banca certamente fará: "você não está apenas interpretando silêncios?" A resposta é: sim, e isso é um método, não uma fuga — com Hartman e Fuentes como ancestrais teóricos e com o corpus visual como o campo específico onde o método é aplicado.

### 3.4 Limites interpretativos como forma de validação

A ideia de que declarar limites é uma forma de rigor — e não sua ausência — está implícita em Hartman e Fuentes, mas pode ser articulada mais explicitamente à luz da discussão de validação em humanidades digitais.

Nos chamados *paradata* — os dados sobre como os dados foram produzidos — a declaração de incerteza é considerada boa prática de pesquisa digital (DALLAS et al., 2017). O mesmo princípio estrutura a arqueologia interpretativa (HODDER, 1999): o registro das "decisões metodológicas e suas incertezas" é parte do argumento, não margem que pode ser cortada.

Para esta tese, isso se traduz em três práticas que já estão em vigor mas precisam ser nomeadas como metodológicas:

1. **Relatórios de codificação auditáveis**: cada item do corpus tem um relatório IconoCode que documenta a cadeia de raciocínio em todos os três níveis panofskianos.
2. **Scores diferenciados por nível**: o score de endurecimento agrega os 10 indicadores, mas estes são estratificados em morfológicos (Níveis 1–2) e materiais (Nível 3), e as análises estatísticas controlam por suporte para não confundir determinação material com escolha ideológica.
3. **Declaração de casos-limite**: os itens com `#verificar` e `#possivel-duplicata` são documentados explicitamente no corpus, não silenciados.

---

## Síntese: o padrão de prova desta tese

Este documento construiu, ao longo de três fios, a seguinte posição metodológica:

| Nível de análise | Tipo de afirmação | Padrão de validade | Referência | Estatística aplicável |
|---|---|---|---|---|
| Pré-iconográfico (N1) | Observacional | Concordância intersubjetiva verificável | Panofsky 1939; Rau & Shih 2021 | PA, kappa limitado |
| Iconográfico (N2) | Interpretativa-convencional | Coerência com repertório + auditabilidade | Panofsky 1955; Ginzburg 1989 | Não aplicável |
| Iconológico (N3) | Hermenêutica-teórica | Argumentação interna + ancoragem em N1–N2 | Didi-Huberman 2000; Ginzburg 1989 | Não aplicável |
| Ausência / silêncio | Arqueológica | Declaração explícita de limites | Hartman 2008; Fuentes 2016 | Não aplicável |
| Padrão de conjunto | Indiciária | Transparência do raciocínio inferencial | Moran 2022; Braman 2023 | Não aplicável |

A tese *não* "desvia" do empiricismo por negligência — ela adota um padrão de prova alternativo que é adequado ao seu objeto (imagens históricas de Estado), consistente com sua tradição disciplinar (história da cultura jurídica), e defendido na literatura metodológica relevante (Ginzburg, Panofsky, Didi-Huberman, Hartman, Fuentes, Moran, Braman).

Esse padrão pode ser enunciado numa frase: **a validade desta tese é indiciária, não experimental; hermenêutica, não estatística; e a declaração de limites é parte da prova, não sua ausência**.

---

## Referências

BRAMAN, Sandra. Visual evidence in law. In: MNOOKIN, Jennifer; RISTOVSKA, Lili (Org.). *Seeing Evidence*. Chicago: University of Chicago Press, 2023.

DIDI-HUBERMAN, Georges. *Devant le temps: histoire de l'art et anachronisme des images*. Paris: Les Éditions de Minuit, 2000.

DIDI-HUBERMAN, Georges. *L'image survivante: histoire de l'art et temps des fantômes selon Aby Warburg*. Paris: Les Éditions de Minuit, 2002.

FUENTES, Marisa J. *Dispossessed Lives: Enslaved Women, Violence, and the Archive*. Philadelphia: University of Pennsylvania Press, 2016.

GINZBURG, Carlo. Sinais: raízes de um paradigma indiciário. In: ______. *Mitos, emblemas, sinais: morfologia e história*. Tradução de Federico Carotti. São Paulo: Companhia das Letras, 1989. p. 143–179.

HARTMAN, Saidiya. Venus in Two Acts. *Small Axe*, n. 26, v. 12, n. 2, p. 1–14, jun. 2008.

MORAN, Leslie J. *Imagining Penology: On the Visual Cultures of Punishment*. London: Routledge, 2022.

PANOFSKY, Erwin. *Studies in Iconology: Humanistic Themes in the Art of the Renaissance*. New York: Oxford University Press, 1939.

PANOFSKY, Erwin. *Meaning in the Visual Arts: Papers in and on Art History*. New York: Doubleday Anchor Books, 1955.

RAU, Roland; SHIH, Yi-Kang. Adequacy of kappa statistics for inter-rater reliability in text genre categorization: a mathematical reconsideration. *Quality & Quantity*, v. 55, n. 2, p. 651–666, 2021.

ROELE, Isobel. Dodging empiricism: the legal humanities. *Journal of Law and Society*, v. 48, n. 1, p. 1–27, 2021.

---

*Localização*: `tese/manuscrito/notas/paradigma-indiciario-padroes-de-prova.md`
*Próximo passo*: Estágio B — revisão ampla do Capítulo 2 à luz deste documento (incorporar Fio 1 em §2.5, Fio 2 em §2.1–2.2, Fio 3 em §2.4).
