# Arquitetura de atributos — LPAI v3

Documento de decisão para a ICONOCRACIA (PPGD/UFSC). Responde a duas perguntas:
quais atributos entram no esquema de codificação, e se essa é de fato a decisão
de maior consequência.

Ana Vitória Vanzin Mendes · 29 de julho de 2026
Base empírica: 328 registros de `data/processed/records.jsonl`
Base bibliográfica: `pesquisa-arquitetura-atributos.md` (revisão de estado da arte)

---

## 1. Resposta direta

**Não. A seleção de atributos não é o fator mais importante — e no seu corpus é
possível demonstrar isso com números.**

A literatura de análise de conteúdo posiciona a lista de categorias em quarto
lugar numa hierarquia de consequência. Krippendorff é explícito: erros na
definição da unidade de análise e da amostragem se propagam de modo
irrecuperável, enquanto erros na lista de categorias, embora custosos, são
corrigíveis por recodificação iterativa ([Krippendorff, *Content Analysis*](https://www.metodos.work/wp-content/uploads/2020/05/content_analysis-kippendorf-book.pdf)).
Neuendorf converge ao situar o *unitizing* como etapa anterior à própria redação
do livro de códigos ([Neuendorf, *The Content Analysis Guidebook*](https://www.gbv.de/dms/ilmenau/toc/844049530.PDF)).
A literatura de *unit-of-analysis error* acrescenta o caso específico que
interessa aqui: coletar no nível do objeto e generalizar no nível do regime, sem
ponderar o desenho amostral, produz inferência estruturalmente inválida que
nenhum refinamento do esquema de atributos repara ([ISPOR](https://www.ispor.org/docs/default-source/publications/value-outcomes-spotlight/may-june-2016/vos-unit-of-analysis-error.pdf)).

A revisão de estado da arte concluiu que, no seu caso, três dessas decisões já
estariam tomadas — unidade de análise (o registro iconográfico individual),
população (os 328 casos) e nível de mensuração (corrigido pela aposentadoria do
índice) —, restando a arquitetura de atributos como único ponto de risco em
aberto. **O diagnóstico empírico mostra que essa premissa é falsa.** A população
não está fixada e o nível de mensuração não está resolvido, porque o corpus
contém uma política de ausência implícita que nunca foi decidida: 106 dos 328
registros carregam zeros que não são medições. Enquanto isso valer, mexer na
lista de atributos é otimizar a terceira casa decimal de um número cuja primeira
casa está errada.

---

## 2. A prova no seu corpus

### 2.1 Um terço do corpus não está codificado — está preenchido com zeros

| Situação | Registros | % |
|---|---|---|
| Todos os 10 indicadores em zero | 106 | 32,3% |
| Com ao menos um indicador marcado | 222 | 67,7% |

A origem desses 106 não deixa dúvida sobre a natureza do fenômeno: 86 vêm de
`vault-import`, 19 de `migration`, 1 de `ana`. São zeros de importação, não
juízos de codificação. O único registro de autoria humana no bloco pode ser uma
codificação genuína de ausência total — e precisa ser inspecionado à parte,
justamente porque é indistinguível dos outros 105 na estrutura atual.

Isso reinterpreta um número que você já conhecia: dos 148 registros da fila de
baixa confiança (origens `vault-import`, `hermes-auto`, `migration`,
`batch-tentative`), **105 são zeros de importação, ou 71%**. A fila de baixa
confiança não é majoritariamente um problema de qualidade de codificação. É um
problema de cobertura vestido de codificação.

### 2.2 O falso zero fabricou unidimensionalidade

Decomposi a matriz de correlação dos dez indicadores duas vezes: com os 328
registros e apenas com os 222 efetivamente codificados.

| | Componente 1 | Autovalores > 1 | Leitura |
|---|---|---|---|
| Com os 106 falsos zeros (n=328) | 69,2% | **1** | esquema unidimensional |
| Só codificados (n=222) | 46,5% | **3** | três dimensões (4,65 / 1,25 / 1,04) |

O alfa de Cronbach no subcorpus codificado é 0,846 — alto, mas longe do patamar
que os 328 registros sugeriam. Em outras palavras: **a aparência de que os dez
indicadores mediam uma coisa só era artefato dos zeros de importação.** Um bloco
de 106 linhas idênticas em todas as variáveis correlaciona tudo com tudo.

O efeito aparece nos pares. Com os falsos zeros, sete pares passavam de r=0,70,
e `dessexualizacao × uniformizacao_facial` chegava a 0,88. No subcorpus
codificado, sobra **um único par** acima de 0,70 (o mesmo, em 0,73). O esquema
não é redundante como parecia.

Isso tem uma consequência desconfortável e produtiva: parte da justificativa
estatística que se poderia dar à aposentadoria do índice — "os indicadores são
tão colineares que a média não perde informação" — era falsa. A aposentadoria
segue correta, mas pelas razões epistêmicas que você deu (validade,
auditabilidade, honestidade), não por redundância métrica.

### 2.3 O falso zero inverteu o sinal de uma afirmação da tese

Aqui está o achado mais grave. Médias por indicador, por regime:

| Indicador | Com falsos zeros: militar | Só codificados: militar | Direção |
|---|---|---|---|
| serialidade | 0,93 | **2,27** (o mais alto de todos os regimes) | inverte |
| inscricao_estatal | 0,89 | **2,18** | inverte |
| dessexualizacao | 0,78 (o mais baixo) | **1,91** (o mais alto) | inverte |
| heraldizacao | 0,76 | **1,86** | inverte |
| monocromatizacao | 0,56 (o mais baixo) | 1,36 | atenua |

Com os falsos zeros, o regime militar parecia o menos endurecido do corpus — o
que sustentava a leitura de "inflexão militar" como quebra ou perda de atributos.
Sem eles, o regime militar é o **mais** marcado em serialidade, inscrição
estatal, dessexualização e heraldização. A razão é aritmética e brutal: **59,3%
dos registros militares são zeros de importação.**

| Regime | Não codificados | Total | % |
|---|---|---|---|
| militar | 32 | 54 | **59,3%** |
| contra-alegoria | 6 | 14 | 42,9% |
| normativo | 35 | 102 | 34,3% |
| fundacional | 33 | 158 | 20,9% |

A inflexão militar que os scripts de fios detectavam — e que eu, ontem, migrei
diligentemente de "queda de escore" para "perda de atributos" — é, com alta
probabilidade, um artefato de cobertura. Migrei a métrica errada para uma
linguagem melhor. Isso não é conserto; é maquiagem mais honesta sobre o mesmo
buraco.

### 2.4 O viés de cobertura é também geográfico

| País | Não codificados | Total | % |
|---|---|---|---|
| Itália | 10 | 20 | 50,0% |
| Brasil | 29 | 68 | **42,6%** |
| Bélgica | 4 | 10 | 40,0% |
| Portugal | 4 | 11 | 36,4% |
| Espanha | 2 | 7 | 28,6% |
| França | 22 | 90 | 24,4% |
| Reino Unido / Alemanha | 5 | 23 cada | 21,7% |
| Estados Unidos | 6 | 32 | 18,8% |
| Países Baixos | 0 | 10 | 0% |

O Brasil — o caso central da tese — tem quase o dobro da taxa de não codificação
da França. Qualquer comparação Brasil–França feita hoje sobre a tabela completa
compara um corpus codificado com um corpus semicodificado. E o volume Brasil–Itália
sobre fontes de história jurídica das mulheres se apoiaria, do lado italiano, num
subcorpus com metade dos registros vazios.

### 2.5 O limiar de "atributo presente" move mais que a lista de atributos

| Limiar | Atributos por item (média) | Itens sem atributo | Assinaturas distintas |
|---|---|---|---|
| ≥ 1 | 5,6 | 106 (32%) | 65 |
| ≥ 2 (atual) | 3,0 | 116 (35%) | 94 |
| ≥ 3 | 0,8 | 230 (70%) | 45 |

Passar de ≥2 para ≥3 esvazia 70% do corpus. Passar para ≥1 quase dobra o
inventário médio. Nenhuma decisão sobre *quais* atributos entram produz variação
dessa magnitude. O limiar é um parâmetro de arquitetura que hoje está implícito
no código — eu o escrevi como `ATTRIBUTE_THRESHOLD = 2` sem que fosse uma decisão
sua registrada.

### 2.6 Um efeito de teto do lado da máquina

Dez registros têm todos os dez indicadores em nível ≥2. Todos vêm de lotes
`iconocode-opus` (7) e `iconocode-opus-4.6-metadata-refined` (3); nove estão no
regime normativo. Codificador que marca tudo alto não está lendo a imagem, está
confirmando a hipótese. Isso é o espelho simétrico do falso zero: na ponta baixa,
importação sem leitura; na ponta alta, leitura sem discriminação.

---

## 3. Onde a literatura ajuda e onde ela para

A revisão confirma o desenho de estratificação e devolve três resultados úteis.

Primeiro, **nenhuma fonte nomeia o problema de heterogeneidade ontológica como
você o formulou.** É lacuna real da literatura metodológica. O que existe é a
solução por design: AAT/Getty separa facetas, CIDOC-CRM separa classes, Iconclass
separa hierarquias — e nenhum deles jamais soma níveis distintos ([Iconclass](https://iconclass.org/help/basics);
[AAT](https://msi.dublincore.org/standards/aat/); [CIDOC-CRM](https://en.wikipedia.org/wiki/CIDOC_Conceptual_Reference_Model)).
O vocabulário mais próximo é a distinção de Krippendorff e Neuendorf entre
conteúdo manifesto e latente. Sua formulação é mais precisa que a da literatura,
e isso é material de tese, não fragilidade.

Segundo, **esses sistemas foram feitos para indexação e recuperação, não para
comparação entre casos.** Iconclass te diz como estruturar sem misturar; não te
diz como comparar 222 registros. A transposição exige adaptação autoral.

Terceiro, **toda alternativa à agregação reintroduz discricionariedade** —
calibração na QCA, escolha de eixos ativos na MCA, limiares na análise de
conceitos formais. As duas tradições que assumem isso abertamente são a
classificação politética de [Needham](https://www.semanticscholar.org/paper/Polythetic-Classfication:-Convergence-and-Needham/ffed29215328c97b9ccaa93c3389be983c0e6c5e)
e a montagem warburguiana — que é o que você já faz. Não há técnica que remova a
decisão autoral; há técnicas que a escondem melhor.

Um ponto de convergência forte com o seu objeto: [Agulhon](https://www.persee.fr/doc/hom_0439-4216_1990_num_30_115_369293)
codifica atributos por regime ao longo de *Marianne au pouvoir* e nunca os agrega
num índice. O precedente metodológico mais próximo da sua tese já opera na
arquitetura que você adotou.

---

## 4. A estrutura empírica coincide com a estratificação ontológica

Aqui os dois lados se encontram de um modo que não era previsível. Agrupei os dez
indicadores por correlação no subcorpus codificado (ligação média, corte em
r=0,55) e o resultado reproduz, sem que eu tenha imposto, a distinção de níveis
que você deduziu por argumento teórico:

| Cluster | Atributos | Coesão | Natureza |
|---|---|---|---|
| A — corpo | rigidez_postural, dessexualizacao, uniformizacao_facial | 0,77 | juízo iconográfico sobre o corpo |
| B — insígnia | heraldizacao, inscricao_estatal | 0,81 | marca institucional |
| C — isolados | desincorporacao, enquadramento_arquitetonico, apagamento_narrativo, serialidade | — | dimensões próprias |
| D — órfão | **monocromatizacao** | — | propriedade técnica do suporte |

`monocromatizacao` correlaciona-se com todo o resto entre 0,07 e 0,27, e com
`inscricao_estatal` em **−0,04**. Ela é ortogonal ao esquema. O argumento de
validade que você deu contra a média — que monocromatização é propriedade
técnica do suporte e não juízo iconográfico — aparece na matriz de correlação sem
que ninguém tenha dito à matriz o que procurar. É a melhor confirmação possível
da decisão de aposentar o índice, e vem dos próprios dados.

`serialidade` comporta-se de modo ambíguo, como a revisão bibliográfica previu:
correlaciona 0,50 com inscrição estatal e 0,44 com heraldização, mas 0,05 com
enquadramento arquitetônico. É o sintoma de um atributo que designa duas coisas —
tiragem técnica e repetição de tipo figural — sob um nome.

E `desincorporacao`, o conceito teoricamente mais central da tese, é o segundo
**pior** discriminador entre regimes (amplitude 0,61). Isso não o invalida: pode
significar que a desincorporação é condição geral do corpus, não variável entre
regimes. Mas exige que a tese pare de tratá-lo como eixo de variação e passe a
tratá-lo como fundo comum.

---

## 5. Arquitetura proposta: LPAI v3

Mantenha os dez indicadores. Estratifique-os. Cada estrato ganha escala,
protocolo de evidência e estatuto argumentativo próprios — e nenhum estrato se
soma a outro, nunca.

### Estrato I — Propriedade material do suporte

**Atributos:** `monocromatizacao`, `serialidade_tecnica` (desdobramento).

Escala binária ou categórica, não ordinal 0–3: uma tiragem é serial ou não é.
Verificação por exame do objeto ou de reprodução fiel; a fonte de desacordo entre
codificadores é erro de observação, não divergência de juízo, e portanto se espera
concordância próxima de 1. **Estatuto argumentativo: metadado descritivo do
corpus, não achado da tese.** Monocromatização entra na caracterização do suporte;
não entra como evidência de endurecimento simbólico. A ortogonalidade medida em
§4 é a justificativa empírica dessa realocação.

### Estrato II — Fato institucional documentável

**Atributos:** `inscricao_estatal`, o regime de emissão (quando tratado como fato
de contexto de produção) e a tipologia de recusas quando há ato documentado — um
decreto de substituição de efígie, uma ata de encomenda, uma norma de circulação.

Escala categórica com campo obrigatório de fonte. **Exigência de triangulação:
nenhuma codificação positiva sem ao menos uma fonte documental externa à imagem.**
Ausência de documentação codifica-se como `não verificado`, jamais como ausência
do fato. Esse é o ponto em que o framework de estudos de omissão é operacionalizável
([Jovanović, *Rethinking History*](https://www.tandfonline.com/doi/full/10.1080/13507486.2026.2654438)).

### Estrato III — Juízo iconográfico interpretativo

**Atributos:** `desincorporacao`, `rigidez_postural`, `dessexualizacao`,
`uniformizacao_facial`, `heraldizacao`, `enquadramento_arquitetonico`,
`apagamento_narrativo`, `serialidade_figural` (desdobramento).

Escala ordinal 0–3 preservada, **com frase justificativa obrigatória por atributo
marcado**. Sem a frase, o atributo não existe — é a tradução operacional da
lacuna que a auditoria francesa apontou. Dupla codificação em amostra
estratificada, com relato qualitativo dos desacordos, e não apenas coeficiente:
atributo cuja definição não permite concordância razoável deve ser redefinido
antes da aplicação em escala, não depois ([Krippendorff, "Reliability in content analysis"](https://pure.uva.nl/ws/files/9702768/Reliability_in_content_analysis.pdf)).

### Desdobramentos recomendados

`dessexualizacao` é hoje um juízo único e contestável carregando muito peso — é o
par mais correlacionado do subcorpus (0,73 com uniformização facial), o que sugere
que os dois estão medindo a mesma leitura. Desdobre em três observáveis próximos
da superfície da imagem, todos ancorados em vocabulário já validado pela
literatura especializada:

- nudez ou seminudez classicizante (presença/ausência);
- adereço de cabeça diagnóstico do tipo de autoridade — coroa mural, gorro
  frígio, diadema, elmo — categoria emprestada da tradição vexilológica e
  numismática;
- objeto empunhado diagnóstico — balança, espada, ramo, bandeira, livro —
  categoria emprestada de [Resnik & Curtis, *Representing Justice*](https://openyls.law.yale.edu/server/api/core/bitstreams/ae7aaca5-a423-4062-8021-c8ec2bdb8280/content).

`serialidade` desdobra-se em `serialidade_tecnica` (Estrato I) e
`serialidade_figural` (Estrato III), conforme diagnosticado em §4.

Isso não é acúmulo arbitrário: cada subatributo corresponde a unidade de
codificação já validada por conteúdo na literatura consagrada, o que satisfaz o
critério de validade de conteúdo. E o desdobramento tende a **aumentar** a
confiabilidade, porque move o juízo para mais perto da observação.

---

## 6. A política de ausência é o núcleo da arquitetura

Esta seção é a que responde à sua pergunta. Não é sobre quais atributos entram.

### Três estados, não dois

O esquema atual tem dois estados possíveis para um indicador: um número de 0 a 3,
ou nada. Isso força o zero a fazer dois trabalhos incompatíveis — "o codificador
olhou e o atributo não está lá" e "ninguém olhou". Os 106 registros de §2.1 são o
custo dessa economia.

O LPAI v3 exige três estados explícitos:

| Estado | Significado | Como se codifica |
|---|---|---|
| `0–3` | o codificador leu e atribuiu grau | valor ordinal + frase justificativa |
| `NC:<causa>` | leu e não pôde decidir | causa tipada: `evidencia_insuficiente`, `resolucao_inadequada`, `fora_de_escopo`, `ambiguidade_tipologica` |
| `NÃO_CODIFICADO` | ninguém leu | estado de proveniência, nunca de juízo |

Zero passa a significar exclusivamente ausência observada — e ausência observada
é dado positivo, o material das Recusas.

### A migração dos 106

Não recodifique por inferência e não apague. Converta os 106 zeros de importação
em `NÃO_CODIFICADO`, preservando `coded_by` e a data original. Isso é uma
operação de honestidade retroativa: o corpus passa a declarar o que não sabe. O
efeito imediato é que o denominador de toda estatística cai de 328 para 222, e é
o denominador certo. O registro codificado por `ana` no bloco sai da conversão e
vai para inspeção manual.

### Ausência substantiva versus ausência de coleta

Para as Recusas, a distinção precisa ser estrutural, não editorial. Uma célula
vazia na matriz país × período × suporte pode ser uma recusa histórica — o Estado
não produziu aquele corpo alegórico — ou uma falha de prospecção. Confundi-las
produz afirmação falsa sobre o Estado. A regra operacional: **ausência só é
substantiva com triangulação documental externa** — série completa de emissões,
catálogo de acervo, norma que institui o padrão. Sem isso, é `lacuna_de_coleta`, e
a coluna belga do corpus é o exemplo vivo.

### O limiar deixa de ser constante de código

`ATTRIBUTE_THRESHOLD = 2` é hoje uma linha em `lpai_indicators.py` que eu escrevi.
Deve ser decisão registrada, com justificativa, e reportada em toda tabela da
tese — porque, como §2.5 mostra, ela move mais o resultado do que a lista de
atributos.

---

## 7. Como comparar sem agregar

Quatro caminhos, em ordem de proximidade com o que a tese já faz.

**Assinaturas politéticas.** A unidade de comparação passa a ser o conjunto
nomeado de atributos — a assinatura. Hoje há 94 assinaturas distintas no corpus
completo; sobre os 222 codificados o número cai e ganha sentido. A comparação
pergunta quais assinaturas recorrem, quais são únicas, quais atravessam países.
Needham dá o fundamento: classes politéticas não exigem que todos os membros
compartilhem todos os atributos, o que é exatamente a situação de Justitia,
Marianne e Germania. Custo: nenhum. É formalização do que você já escreve.

**Montagem warburguiana.** A justaposição como forma de prova. Custo: exige que
cada painel exiba os atributos que sustentam a rima, e não apenas afirme a rima.
Ganho: é a única tradição que trata a decisão autoral de arranjo como método
declarado, não como viés a esconder.

**Análise de coocorrência e redes de atributos.** Os clusters de §4 são um
primeiro resultado disso. Serve para descobrir estrutura e para detectar
redundância. Custo baixo, ganho diagnóstico alto. **Estatuto: exploratório.**
Não vira evidência de tese.

**MCA, FCA e QCA.** Tecnicamente aplicáveis, e nenhuma resolve o problema de
fundo: todas reintroduzem uma escolha discricionária — eixos ativos, limiares de
conceito, calibração de conjuntos — tão autoral quanto pesos de índice, mas com
aparência de objetividade. A revisão não encontrou precedente de aplicação a
iconografia jurídico-política, o que significa que usá-las exigiria justificar o
método antes de usar o resultado. Recomendo mantê-las fora da tese e, no máximo,
como apêndice metodológico exploratório.

---

## 8. Consequências para a tese

**O painel ENDURECIMENTO precisa mudar de afirmação, não de linguagem.** Ontem
reescrevi a tese do painel de "medida que cresce monotonicamente" para "acúmulo
de atributos demonstrado por montagem". Depois de §2.3, isso é insuficiente: a
sequência que ele exibe pode estar ordenada por cobertura, não por endurecimento.
O painel precisa ser reconstruído sobre os 222, com a taxa de codificação
declarada em cada célula.

**A inflexão militar deve ser suspensa como achado.** Com 59,3% de não
codificação, o regime militar não sustenta afirmação comparativa. Ou se codifica
os 32 registros faltantes, ou a tese declara que a leitura do regime militar é
provisória. As duas saídas são honestas; a terceira, que é continuar afirmando, não é.

**A comparação Brasil–França precisa ser reponderada.** 42,6% contra 24,4% de não
codificação. E o volume Brasil–Itália herda um lado italiano com 50% de vazio.

**Um ganho argumentativo inesperado.** A ortogonalidade de monocromatização
(§4) é evidência empírica, produzida no seu próprio corpus, de que atributos de
níveis ontológicos distintos não pertencem à mesma escala. Isso transforma a
aposentadoria do índice de decisão prudencial em resultado demonstrado — e vale
uma seção do apêndice metodológico, porque a literatura, como a revisão mostrou,
não nomeia esse problema. Você tem uma contribuição metodológica aqui, não só uma
correção interna.

---

## 9. Ordem de execução

A ordem importa mais que os itens, porque cada passo muda o denominador do
seguinte.

1. **Converter os 106 falsos zeros em `NÃO_CODIFICADO`.** Sem isso, toda
   estatística subsequente é sobre um corpus que não existe. Inspecionar à parte
   o registro de autoria `ana`.
2. **Registrar a política de ausência de três estados** no codebook, como decisão
   (v2.3.0 ou v3.0.0), com o limiar de atributo explicitado e justificado.
3. **Recodificar o regime militar** — 32 registros — antes de qualquer afirmação
   comparativa sobre ele. É o maior retorno por unidade de esforço no corpus hoje.
4. **Estratificar os dez indicadores** nos três estratos, com escalas e protocolos
   próprios, e mover monocromatização para metadado descritivo.
5. **Desdobrar `dessexualizacao` e `serialidade`**, e recodificar a amostra
   afetada.
6. **Reconstruir o painel ENDURECIMENTO** sobre os 222, com taxa de codificação
   declarada por célula.
7. **Rodar o teste de confiabilidade por estrato**, com dupla codificação e relato
   qualitativo dos desacordos — separadamente para Estrato II e III, porque suas
   fontes de desacordo são de naturezas diferentes.

Os passos 1 a 3 são reparo; 4 a 7 são arquitetura. Fazer 4 antes de 1 seria
redesenhar o instrumento medindo com a régua quebrada.

---

## 10. Tensões que permanecem e o que é decisão sua

**Não sei se os 106 são todos falsos zeros.** A inferência vem da origem
(`vault-import`, `migration`) e do padrão idêntico em dez variáveis, o que é forte
mas não conclusivo. Se algum deles for codificação humana genuína de ausência
total, a conversão o destrói. Mitigação: converter preservando o valor original
num campo de proveniência, e revisar manualmente a amostra.

**A literatura não decide a granularidade do desdobramento.** Não há critério
objetivo para saber se `dessexualizacao` deve virar três atributos ou sete. Isso é
decisão autoral, e a única disciplina disponível é: desdobre até o ponto em que a
concordância entre codificadores para de melhorar.

**A contagem de atributos que eu instituí no código é, ela mesma, uma agregação.**
`attribute_count` soma coisas de estratos diferentes. Ela é menos falsa que a
média — cardinalidade não converte incomensuráveis numa grandeza comum — mas não
é inocente. Sob o LPAI v3, a contagem deve ser calculada **por estrato**, nunca
global. Preciso corrigir isso no módulo.

**Existe uma tensão entre parcimônia e fidelidade que nenhuma métrica resolve.**
Três dimensões efetivas em dez indicadores é um convite à redução; a fidelidade
iconográfica é um argumento contra. A revisão bibliográfica não resolve, e eu
também não. Minha inclinação: mantenha os dez, porque cada um corresponde a
atributo efetivamente discutido pela literatura especializada, e porque a
redundância medida (um par acima de 0,70) é pequena depois que os falsos zeros
saem.

**Onde eu poderia estar errada.** Toda a §2 depende de tratar o bloco de zeros
como não codificação. Se você me disser que `vault-import` era um fluxo em que a
ausência de atributo era codificada deliberadamente como zero, a inversão do
regime militar deixa de ser artefato e passa a ser achado — e a arquitetura muda
de forma. Essa é a única pergunta que eu não consigo responder a partir dos dados.

---

## 11. Fontes

**Metodologia de mensuração e análise de conteúdo**
- [Krippendorff, *Content Analysis: An Introduction to Its Methodology*](https://www.metodos.work/wp-content/uploads/2020/05/content_analysis-kippendorf-book.pdf)
- [Krippendorff, "Reliability in content analysis"](https://pure.uva.nl/ws/files/9702768/Reliability_in_content_analysis.pdf)
- [Neuendorf, *The Content Analysis Guidebook*](https://www.gbv.de/dms/ilmenau/toc/844049530.PDF)
- [ISPOR, "An Introduction to Unit-of-Analysis Error"](https://www.ispor.org/docs/default-source/publications/value-outcomes-spotlight/may-june-2016/vos-unit-of-analysis-error.pdf)
- [OECD/JRC, *Handbook on Constructing Composite Indicators*](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html)

**Sistemas de classificação e ontologias**
- [Iconclass basics](https://iconclass.org/help/basics)
- [Getty AAT](https://www.getty.edu/research/tools/vocabularies/aat/) · [ficha de padrão](https://msi.dublincore.org/standards/aat/)
- [CIDOC-CRM](https://en.wikipedia.org/wiki/CIDOC_Conceptual_Reference_Model) · [definição v6.2.8](https://cidoc-crm.org/sites/default/files/CIDOC%20CRM_v6.2.8%20Definition.pdf)
- [Duits, "The Warburg Institute Iconographic Database", *Visual Resources*](https://www.tandfonline.com/doi/full/10.1080/01973762.2014.936104)

**Alternativas à agregação**
- [Needham, "Polythetic Classification", *Man* (1975)](https://www.semanticscholar.org/paper/Polythetic-Classfication:-Convergence-and-Needham/ffed29215328c97b9ccaa93c3389be983c0e6c5e)
- [Ganter & Wille, *A First Course in Formal Concept Analysis*](https://bpb-us-e1.wpmucdn.com/sites.tufts.edu/dist/b/4296/files/2018/06/a-first-course-in-formal-concept-analysis.pdf)
- [Le Roux & Rouanet, "Multiple Correspondence Analysis"](https://muse.jhu.edu/pub/166/oa_edited_volume/chapter/3772666)
- [Arnold & Tilton, "Distant viewing", *DSH*](https://academic.oup.com/dsh/article/34/Supplement_1/i3/5694340)

**Ausência como evidência**
- [Jovanović, "Toward an omission studies framework in historical research", *Rethinking History*](https://www.tandfonline.com/doi/full/10.1080/13507486.2026.2654438)
- [*Absence in the Archives*, Cambridge Elements](https://www.cambridge.org/core/elements/absence-in-the-archives/587846C3687A675DE72B137014C4ACC2)

**Alegoria feminina, Estado e iconografia jurídica**
- [Warner, *Monuments and Maidens*](https://archive.org/details/monumentsmaidens00warn)
- [Agulhon, *Marianne au pouvoir*](https://www.persee.fr/doc/hom_0439-4216_1990_num_30_115_369293)
- [Resnik & Curtis, *Representing Justice*](https://openyls.law.yale.edu/server/api/core/bitstreams/ae7aaca5-a423-4062-8021-c8ec2bdb8280/content)
- [Effer, "L'iconografia della giustizia secondo Beccaria", *Etica & Politica*](https://sites.units.it/etica/2020_2/EFFER.pdf)
- [Douzinas, "The Legality of the Image", *Modern Law Review*](https://www.scribd.com/document/521499317/The-Modern-Law-Review-Volume-63-issue-6-2000-doi-10-1111-1468-2230-00296-Costas-Douzinas-The-Legality-of-the-Image-1)
- [Goodrich, *Legal Emblems and the Art of Law*](https://www.cambridge.org/core/books/abs/legal-emblems-and-the-art-of-law/preface/DC52F7ABE2CC00C3516F98B0AFD43788)

**Base empírica interna**
Análises reprodutíveis em `analise_indicadores.py`, `analise_dimensional.py` e
`analise_lacunas.py`, sobre `data/processed/records.jsonl` (328 registros,
codebook v2.2.1). Revisão de estado da arte completa em
`pesquisa-arquitetura-atributos.md`.
