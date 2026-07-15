# Sincronização da pesquisa no Consensus

**Data da coleta:** 15 de julho de 2026  
**Escopo:** literatura para a tese e para o repositório `iconocracy-corpus`  
**Manifesto estruturado:** `data/research/consensus_sync_2026-07-15.json`

## Finalidade e limite probatório

Esta sincronização registra literatura científica recuperada no Consensus e a vincula às decisões metodológicas já documentadas no repositório. Ela não altera registros do corpus visual, nem converte artigos em prova de procedência de uma imagem. A origem, a datação, a licença e a custódia de cada peça continuam dependentes de sua fonte primária ou institucional.

As referências abaixo devem ser verificadas no texto integral e no catálogo da editora antes de integrarem a bibliografia final em ABNT. O registro do Consensus serve como trilha de descoberta, identificação e priorização.

## Resultados incorporados

| Chave | Integração proposta | Status |
|---|---|---|
| `Matthews2000Britannia` | Sustentar o estudo comparado de Britânia e John Bull no Capítulo 5, com atenção à genealogia clássica e vernacular das personificações nacionais. | Prioridade alta |
| `Baylis2014GenderFrame` | Usar como comparador metodológico para a relação entre performance de gênero, fotografia e formação da narrativa nacional. Não expande o corpus core. | Prioridade média |
| `Carvalho2013FormationSouls` | Reconciliação bibliográfica. A obra já é nuclear no projeto; o novo registro evita duplicação entre a edição em língua inglesa e a referência brasileira já adotada. | Já canônico |
| `Cusack2005TinyTransmitters` | Apoiar a categoria “selo” e os marcadores de nacionalismo colonial no codebook, sem projetar automaticamente as conclusões portuguesas sobre o Brasil. | Prioridade alta |
| `PrietoAndresEtAl2025ColonialPropaganda` | Examinar como precedente de análise quantitativa de selos coloniais para teste do codebook. | Provisório |

## Fichas de pesquisa

### Britânia e personificação nacional

MATTHEWS, Roy T. [Britannia and John Bull: From Birth to Maturity](https://consensus.app/papers/britannia-and-john-bull-from-birth-to-maturity-matthews/64a9d0ef74ab5588b16abb6b16aed3df/?utm_source=chatgpt). The Historian, v. 62, p. 799-820, 2000. 7 citações no Consensus em 15 jul. 2026.

A leitura é prioritária para o capítulo comparativo porque situa Britânia em relação a John Bull e distingue matrizes clássicas, cristãs e vernaculares de personificação. A contribuição esperada é descritiva e genealógica, não uma equivalência imediata entre alegoria feminina e representação de mulheres reais.

### Gênero, fotografia e narrativa nacional

BAYLIS, Gail. [Gender in the frame: photography and the performance of the nation narrative in early twentieth-century Ireland](https://consensus.app/papers/gender-in-the-frame-photography-and-the-performance-of-the-baylis/24e8ded74d965acc8618ead5c581d9e2/?utm_source=chatgpt). Irish Studies Review, v. 22, p. 184-206, 2014. 3 citações no Consensus em 15 jul. 2026.

A pesquisa oferece um controle metodológico útil: a repetição de performances de gênero pode naturalizar uma narrativa de nação, ao passo que os arquivos visuais podem conservar suas contradições. A entrada deve informar a discussão de análise contextual no Capítulo 4, mas a Irlanda permanece fora do recorte quantitativo.

### Imaginário da República brasileira

CARVALHO, José Murilo de; LANDERS, Clifford E.; CARVALHO, M. A. [The Formation of Souls: Imagery of the Republic in Brazil](https://consensus.app/papers/the-formation-of-souls-imagery-of-the-republic-in-brazil-carvalho-landers/e6caf7999e9854ad82ac5b428442f3be/?utm_source=chatgpt), 2013. 6 citações no Consensus em 15 jul. 2026.

O resultado confirma a adequação da obra de José Murilo de Carvalho ao núcleo brasileiro da tese, especialmente para a legitimidade republicana produzida por imagens, símbolos e figuras nacionais. Como o repositório já usa a edição brasileira de 1990, esta ficha não cria nova entrada na bibliografia final.

### Selos, colonialismo e nacionalismo

CUSACK, Igor. [Tiny transmitters of nationalist and colonial ideology: the postage stamps of Portugal and its Empire](https://consensus.app/papers/tiny-transmitters-of-nationalist-and-colonial-ideology-cusack/5ae8bc3172885b1bb6b4f8b821978bdd/?utm_source=chatgpt). Nations and Nationalism, v. 11, p. 591-612, 2005. 53 citações no Consensus em 15 jul. 2026.

Esta é a referência externa mais forte para tratar o selo como suporte estatal de circulação de iconografia nacional e colonial. Ela reforça a separação entre: (a) a identificação material do suporte; (b) a codificação de figura feminina, raça, território e regime; e (c) a interpretação histórica da circulação.

PRIETO-ANDRÉS, Antonio; FERNÁNDEZ-ROMERO, Cayetano; SIERRA, M. [Colonial Propaganda In The Belgian Congo Through Postage Stamps (1894–1960): A Quantitative Content Analysis](https://consensus.app/papers/colonial-propaganda-in-the-belgian-congo-through-postage-prieto-andrs-fernndez-romero/96f10d11ea1b5d9da34c70f662a13c2f/?utm_source=chatgpt). Journal of Intercultural Communication, 2025. 0 citações no Consensus em 15 jul. 2026.

O estudo deve ser lido como precedente metodológico, não como autoridade conclusiva. Antes de uso na tese, verificar o texto integral, a descrição da amostra e a estabilidade da referência editorial.

## Implicações operacionais para o repositório

1. Manter a literatura em um registro próprio, por chave de citação e URL canônica, separado de `corpus_dataset.csv`.
2. Para selos, preservar os campos de suporte, instituição emissora, jurisdição, intervalo temporal e fonte primária. A literatura funciona como interpretação e desenho de pesquisa, não como substituto de metadados.
3. Tratar os campos de gênero, colonialidade, raça e territorialização como códigos analíticos com definição explícita, exemplos positivos e casos limítrofes antes de qualquer teste de confiabilidade intercodificador.
4. Distinguir `corpus_core`, `comparador_principal`, `comparador_metodologico`, `apoio_metodologico` e `comparador_apendice` também no registro bibliográfico. Isso impede que leituras comparativas ampliem silenciosamente a amostra estatística.

## Próxima revisão

- Conferir DOI, editora, fascículo e paginação em catálogos primários.
- Ler integralmente Matthews, Baylis e Cusack antes de redigir o Capítulo 5.
- Fazer um pré-teste do codebook de selos com fontes brasileiras, sem transferir categorias coloniais europeias sem justificação histórica.
- Decidir se Prieto-Andrés, Fernández-Romero e Sierra deve entrar na bibliografia da tese após verificação editorial e metodológica.
