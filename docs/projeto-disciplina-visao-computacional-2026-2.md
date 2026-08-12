---
title: "ICONOCRACIA-CV — projeto para Visão Computacional"
disciplina: "INE410159 / TRV410001 — Visão Computacional"
semestre: "2026.2"
status: "proposta para validação com os professores e a equipe"
dataset_freeze: "ICONOCRACIA-CV-2026-08-12"
source_commit: "0f80b6b11e95a32312a2697344f27255dbf7ef78"
autora: "Ana Vitória Vanzin Mendes"
---

# ICONOCRACIA-CV — projeto para Visão Computacional

> Protocolo técnico do projeto de semestre e data card preliminar do
> experimento. Este documento complementa o
> [pitch de apresentação](apresentacao-visao-computacional-2026-2.md): o pitch
> explica o problema; este arquivo delimita o que será implementado, com quais
> dados e como será avaliado.

## Decisão executiva

O dataset proposto à disciplina será o **freeze do corpus ICONOCRACIA em 12 de
agosto de 2026**, com 335 registros canônicos. O corpus de pesquisa pode
continuar crescendo; o freeze do semestre permanece imutável para que todos os
experimentos sejam reproduzíveis.

O projeto construirá um **sistema de recuperação de imagens por similaridade**
(*content-based image retrieval*, CBIR) para o corpus ICONOCRACIA. Dada uma
alegoria como consulta, o sistema devolverá as imagens visualmente mais
próximas e permitirá comparar três formas de representar a imagem:

1. características clássicas definidas manualmente;
2. características aprendidas por uma CNN pré-treinada;
3. características de um transformador visual, como extensão.

O resultado principal será um **atlas computacional de vizinhanças visuais**,
acompanhado de avaliação técnica e histórico-iconográfica. A pergunta não é se
a máquina descobre o significado verdadeiro de uma alegoria, mas quais
proximidades cada representação privilegia e quais delas são úteis para a
comparação especializada.

O projeto não tem como objetivo treinar uma grande rede neural do zero. **O
dataset já foi construído pela pesquisadora.** O trabalho da disciplina
congelará essa contribuição original e construirá o pipeline experimental, as
visões operacionais por tarefa, o protocolo de avaliação e a análise dos erros.
Uma CNN pequena, iniciada com pesos aleatórios, poderá entrar apenas como
controle pedagógico opcional.

## 1. Encaixe na disciplina

A página da disciplina, capturada no Moodle em 12 de agosto de 2026, define
como objetivo prático a implementação de uma solução para um problema de mundo
real de Visão Computacional. O projeto atende a esse objetivo porque parte de
um problema aberto de pesquisa, possui imagens e metadados reais e exige uma
pipeline completa, não uma demonstração sobre um dataset didático pronto.

A progressão do projeto acompanha os dois módulos do curso:

- **Módulo 1:** pixels, histogramas, distâncias, convolução, bordas,
  segmentação e descritores como HOG, SIFT e ORB;
- **Módulo 2:** redes neurais artificiais, CNNs, aprendizado por transferência,
  detecção, segmentação semântica e transformadores visuais.

O material da disciplina oferece práticas com ResNet, EfficientNet, YOLO,
Detectron2, U-Net, DINOv2, CLIP e outros modelos. Portanto, usar uma arquitetura
pré-treinada e adaptá-la ao corpus é uma aplicação prevista pelo próprio curso;
não é um atalho externo à proposta pedagógica.

### Entregas finais informadas no Moodle

Para 2 de dezembro de 2026, a página lista:

- relatório em PDF descrevendo a solução;
- código em ZIP com link para checkpoints da rede neural;
- slides em PPTX ou ODP, com link para Google Slides;
- vídeo em MP4/H.265, com link para o YouTube;
- poster em PDF.

O PDF fornecido não contém pesos de avaliação, rubrica, tamanho máximo da
equipe, prazo de registro do projeto nem requisitos mínimos do dataset. Esses
pontos precisam ser confirmados com os professores.

## 2. Problema computacional

### Entrada

Uma imagem histórica de alegoria feminina vinculada à cultura jurídica ou
estatal.

### Saída

Uma lista ordenada das `k` imagens mais próximas, contendo:

- identificador do item;
- miniatura e metadados essenciais;
- distância ou similaridade calculada;
- método que produziu o ranking;
- indicação de que a proximidade requer interpretação humana.

### Usuária e decisão apoiada

A usuária primária é a pesquisadora do domínio. O sistema apoia a escolha de
comparanda para análise iconográfica, painéis do atlas e investigação de
recorrências formais. Ele não atribui automaticamente regime iconocrático nem
encerra a interpretação iconológica.

### Pergunta de pesquisa

> Qual representação computacional produz vizinhanças visualmente coerentes e
> historicamente úteis no corpus ICONOCRACIA: descritores clássicos, embeddings
> de CNNs ou embeddings de transformadores visuais?

### Hipóteses testáveis

- **H1 — baseline clássico:** histogramas e HOG recuperarão semelhanças de cor,
  contorno e composição, mas serão sensíveis ao suporte, ao fundo e à qualidade
  da digitalização.
- **H2 — CNN:** embeddings de uma CNN pré-treinada produzirão rankings com maior
  relevância formal média que pixels e descritores clássicos, mesmo sem treinar
  a rede inteira no corpus.
- **H3 — transformador visual:** DINOv2 ou CLIP poderá aproximar imagens por
  relações mais globais ou semânticas, mas também poderá importar vieses de seu
  treinamento e confundir semelhança iconográfica com convenções genéricas de
  fotografia, texto ou suporte.
- **H4 — semantic gap:** nenhum método computacional coincidirá integralmente
  com a utilidade histórico-iconográfica atribuída pela especialista; a forma e
  a localização das divergências constituirão parte do resultado.

## 3. O produto mínimo viável

O produto mínimo deverá conter:

1. um freeze local do corpus, com versão, commit e hashes;
2. um manifesto derivado das imagens efetivamente utilizáveis;
3. um pipeline reproduzível de aquisição, validação e pré-processamento;
4. um baseline de pixels/histogramas;
5. um baseline clássico com HOG e, se útil, ORB ou SIFT;
6. um extrator de embeddings baseado em CNN pré-treinada;
7. busca `top-k` com os mesmos itens e consultas para todos os métodos;
8. avaliação cega das vizinhanças e análise dos erros;
9. geração de pranchas comparativas para relatório e poster.

Um notebook interativo é suficiente como interface do semestre. Uma aplicação
web, uma API de produção ou integração imediata ao site da ICONOCRACIA ficam
fora do escopo obrigatório.

## 4. Dataset: freeze do corpus ICONOCRACIA

### 4.1 O freeze é o dataset; cada tarefa produz uma coorte derivada

O dataset da disciplina será o snapshot integral
`ICONOCRACIA-CV-2026-08-12`. Trata-se de um corpus multimodal documentado, com
registros catalográficos, proveniência, anotações iconográficas e referências
às imagens. Sua unidade de análise é o item do corpus, não apenas o arquivo de
pixels.

> **Formulação para a proposta:** “Proponho trabalhar com um freeze do meu
> corpus de doutorado como dataset da disciplina: 335 registros de alegorias
> femininas da cultura jurídica, com metadados, proveniência e anotações
> especializadas. A partir desse freeze, construiremos a coorte visual adequada
> a cada experimento.”

O freeze não encerra o corpus da tese. Ele fixa apenas a versão observada pelo
projeto de semestre: itens adicionados ou corrigidos depois de 12 de agosto não
entram silenciosamente nos resultados. Uma atualização exigiria novo
identificador de release e nova execução completa.

O freeze integral e a coorte visual usada pelos modelos são, portanto, níveis do
mesmo dataset:

| Camada em 2026-08-12 | N | Função no projeto |
|---|---:|---|
| `data/processed/records.jsonl` | 335 | Universo catalográfico canônico; 335 `item_id` e hashes únicos |
| `data/processed/purification.jsonl` | 286 | Ledger separado de codificação; não cobre os 335 registros |
| `data/raw/drive-manifest.json` | 172 | Manifesto parcial; suas URLs de Drive ainda contêm `PLACEHOLDER_FOLDER_ID` |
| `data/processed/thumbnail_registry.jsonl` | 165 | Registro de recuperação de miniaturas; 122 têm URL de imagem |
| `gallery/` | 16 | Imagens locais curadas já presentes no repositório |
| Pool preliminar de auditoria | 92 | Candidatos não textuais, com URL e codificação fora dos quatro grupos de baixa confiança |
| Núcleo estável e dentro do escopo | 70 | Candidatos `verified_direct` ou `existing_pre_v01`, depois do filtro de escopo |
| Núcleo diretamente verificado | 31 | Itens `verified_direct` e dentro do escopo |

O N declarado do dataset é **335 registros**. O N de cada tarefa será relatado
separadamente: 335 para análises catalográficas; até 92 candidatos para
aquisição visual; aproximadamente 70 no núcleo visual estável atual; e um N
possivelmente menor para tarefas supervisionadas. Isso é seleção por contrato
de tarefa e disponibilidade, não substituição do dataset.

### 4.2 Identidade técnica do freeze proposto

| Elemento | Valor em 2026-08-12 |
|---|---|
| Identificador | `ICONOCRACIA-CV-2026-08-12` |
| Commit-fonte | `0f80b6b11e95a32312a2697344f27255dbf7ef78` |
| `records.jsonl` | 335 linhas; SHA-256 `93bce22629da9655cb1f61ba192d86ae837cf9a6544ce4e2f7c77bd72c87a558` |
| `corpus-data.json` | 335 itens; SHA-256 `e822c5c5d20d332228384638fafcc41e80e6d3cb1030858a4e855e8c772aa7a4` |
| `purification.jsonl` | 286 linhas; SHA-256 `2ceac28e974b31a59c33415f5225744aff2ea779d09e2be4882e16f8fe2b58d2` |

Esses valores identificam a proposta de freeze, mas o pacote local ainda deverá
ser materializado pelo fluxo de release do repositório depois dos gates. Criar
um freeze local não autoriza publicação automática no Hugging Face.

### 4.3 Estado de validação do freeze

Os gates foram executados em 12 de agosto de 2026:

| Gate | Resultado | Interpretação |
|---|---|---|
| Schema dos master records | `335/335 records valid` | integridade estrutural aprovada |
| Sincronização do export | `335 records / 335 exportados` | sincronizado por URL |
| Cobertura do ledger separado | `286/335` (85%) | 49 registros sem linha em `purification.jsonl` |

A terceira linha não invalida o dataset. Ela define uma dimensão de
*missingness* que precisa acompanhar o freeze e restringe quais registros podem
ser usados como referência supervisionada.

A interseção de 92 itens é apenas um **pool de auditoria**, não o N final. Ela
contém 31 URLs `verified_direct`, 47 `existing_pre_v01` e 14
`hotlink_protected`; oito desses itens estão sinalizados como fora de escopo.
Cada arquivo ainda precisa ser baixado, identificado por MIME real, aberto e
inspecionado. O projeto já encontrou, em piloto anterior, arquivos com extensão
`.jpg` cujo conteúdo era HTML, PDF ou outro formato.

Não há hoje um dataset visual completo no checkout. A cache contém apenas um
pequeno lote de imagens e os caminhos de binários registrados em exportações
legadas apontam para outro volume, não montado nesta sessão. URLs e caminhos
anteriores são receitas de aquisição, não prova de que o byte está disponível.

O snapshot histórico `v0.2`, de julho de 2026, registra 97 itens verdes segundo
critérios então vigentes. A diferença entre esse número e a interseção atual
decorre de snapshots e filtros distintos; nenhum deles deve ser copiado como N
experimental sem uma nova auditoria.

### 4.4 Confiança das anotações

Todos os 335 registros possuem os dez campos ordinais dentro do bloco
`purificacao` de `records.jsonl`, mas a presença de um número não garante
análise visual confiável. O snapshot contém 159 registros associados a quatro
proveniências em auditoria:

| `coded_by` | N | Risco documentado |
|---|---:|---|
| `vault-import` | 86 | vetor zerado herdado da importação |
| `hermes-auto` | 43 | concentração em valor de fallback |
| `migration` | 19 | valores herdados de schema anterior |
| `batch-tentative-*` | 11 | codificação provisória |

Esses itens podem integrar análises não supervisionadas depois que a imagem for
validada, mas seus rótulos não entrarão no treino ou na avaliação supervisionada
até adjudicação. O codebook será tratado como **referência anotada por
especialista**, não como *ground truth* infalível.

Há ainda uma divergência estrutural: o bloco `purificacao` aparece aninhado nos
335 master records, enquanto `purification.jsonl` possui somente 286 linhas.
Dos 49 registros sem linha no ledger separado, 29 são `vault-import` com os dez
valores zerados. O manifesto da coorte visual deverá registrar de qual ledger veio
cada rótulo e rejeitar zeros de preenchimento como exemplos negativos.

Mesmo entre os 92 candidatos menos problemáticos, somente dez estão marcados
explicitamente como codificados por imagem; 23 são `metadata-refined` e 59
`iconocode-opus`. Logo, disponibilidade da imagem e confiabilidade do rótulo
serão verificadas separadamente.

Os dez indicadores permanecem separados. O campo composto legado não será
usado como alvo de predição nem como prova de uma trajetória histórica.

### 4.5 Perfil preliminar do pool de 92 itens

O pool já revela desbalanceamentos que precisam aparecer no relatório:

- regimes: 39 fundacionais, 27 normativos, 19 militares e 7 contra-alegorias;
- países: França 32, Estados Unidos 16, Alemanha 14, Brasil 7, Itália 7 e
  demais países 16;
- a taxonomia de suporte ainda precisa ser normalizada: uma leitura do campo
  canônico encontrou 22 casos sem suporte resolvido, além de concentrações em
  gravuras, cartazes, monumentos e moedas.

Essas distribuições impedem usar acurácia global ou divisão aleatória ingênua.
Também mostram por que **classificar o regime iconocrático não deve ser a tarefa
central**: além de interpretativo, o rótulo está desbalanceado e correlacionado
com país, suporte e período.

### 4.6 Critérios de inclusão

Um item entra na coorte visual experimental somente quando:

1. representa uma imagem, e não um registro exclusivamente textual;
2. o binário abre, possui MIME de imagem e corresponde ao objeto catalogado;
3. o menor lado tem pelo menos 224 pixels, salvo exceção documentada;
4. a fonte, a custódia e o status de licença estão registrados;
5. `SHA-256`, dimensões, formato e modo de cor foram calculados;
6. duplicatas e variantes pertencem a um mesmo `split_group`;
7. qualquer rótulo usado em avaliação possui proveniência verificável.

### 4.7 Critérios de exclusão

Serão excluídos da coorte visual do semestre:

- HTML, PDF, logos, páginas vazias ou erros salvos como imagem;
- imagem que não corresponda ao item catalogado;
- arquivo corrompido ou pequeno demais para o modelo;
- registro exclusivamente textual;
- duplicata exata, preservando-se uma ocorrência canônica;
- item sem situação de uso acadêmico documentável;
- item sem rótulo confiável, apenas para tarefas supervisionadas.

Uma imagem com rótulo incerto ainda pode permanecer na galeria de recuperação
não supervisionada, desde que essa incerteza esteja explícita.

### 4.8 Manifesto da coorte visual a ser criado

Depois do freeze integral, o primeiro artefato técnico do experimento deverá
ser um JSONL versionado com uma linha por imagem. Ele é uma visão derivada do
dataset, não um corpus concorrente:

| Campo | Conteúdo |
|---|---|
| `freeze_id` | `ICONOCRACIA-CV-2026-08-12` |
| `sample_id` | identificador estável da amostra visual |
| `item_id` | UUID do master record canônico |
| `legacy_handle` | identificador legível, quando existir |
| `image_sha256` | hash do binário efetivamente processado |
| `local_path` | caminho relativo no cache não versionado |
| `source_url` / `image_url` | proveniência catalográfica e imagem recuperada |
| `source_domain` | domínio para análise de viés e agrupamento |
| `license_status` | situação de uso e redistribuição |
| `width` / `height` / `mime_type` | contrato técnico do arquivo |
| `year` / `country` / `support` | metadados para estratificação |
| `series_id` | série, objeto ou matriz visual comum |
| `label_provenance` | origem e confiança das anotações |
| `split_group` | grupo indivisível entre treino, validação e teste |
| `eligible` / `exclusion_reason` | decisão auditável de entrada |
| `snapshot_date` | data ISO `YYYY-MM-DD` do congelamento |

Os binários continuarão fora do Git, conforme a política do repositório. O Git
versionará o manifesto, os hashes, as configurações e os resultados derivados.

### 4.9 Prevenção de vazamento

Uma divisão aleatória por arquivo seria inválida: frente e verso de uma moeda,
recortes da mesma obra, diferentes resoluções ou objetos da mesma série podem
cair em conjuntos distintos e inflar artificialmente o desempenho.

Antes do split, serão calculados hash exato e hash perceptual, seguidos de
inspeção das vizinhanças suspeitas. Todas as variantes do mesmo objeto ou série
receberão o mesmo `split_group` e permanecerão juntas.

Se houver tarefa supervisionada, será usada `StratifiedGroupKFold`: três folds
para um núcleo próximo de 70 itens e cinco apenas se a aquisição ampliar o N e
preservar ambas as classes em todos os folds. Um holdout separado só será
congelado se o número e a composição dos grupos permitirem. O projeto reduzirá
a ambição do classificador antes de relaxar a prevenção de vazamento.

## 5. Pipeline experimental

### Etapa 0 — aquisição e auditoria

- resolver `item_id` e identificadores legados;
- baixar ou localizar os binários autorizados;
- verificar MIME, dimensões, integridade e correspondência visual;
- calcular hashes e grupos de duplicatas;
- congelar o manifesto e gerar uma contact sheet da coorte.

O projeto deverá reaproveitar primeiro
`tools/scripts/harvest_corpus_images.py`, que já prevê cache, manifesto, hash e
dimensões, corrigindo ou estendendo o contrato apenas quando necessário.

### Etapa 1 — baseline mínimo

- redimensionamento com preservação da proporção;
- normalização de cor sem apagar deliberadamente a materialidade do suporte;
- vetor de pixels reduzido e histograma HSV;
- distância Euclidiana ou cosseno;
- busca por vizinhos mais próximos.

Esse baseline deve ser simples. Sua função é mostrar quanto se obtém antes de
adicionar descritores e redes.

### Etapa 2 — visão clássica

- HOG para contorno, postura e estrutura global;
- histograma de cor combinado ao HOG;
- ORB ou SIFT como ablação para pontos locais;
- `k`-NN sobre vetores normalizados;
- teste de pré-processamento com e sem bordas/segmentação, em subconjunto.

Mahalanobis só será usada se a dimensão e o número de amostras permitirem
estimar a covariância de forma estável.

### Etapa 3 — CNN com aprendizado por transferência

Modelo principal proposto: **EfficientNet-B0** ou **ResNet50** pré-treinada no
ImageNet. A primeira rodada congelará os pesos e extrairá o vetor da penúltima
camada. Isso permite comparar uma representação aprendida com HOG sem fingir
que 92 imagens bastam para treinar uma rede profunda inteira.

Como tarefa supervisionada auxiliar, poderá ser treinada uma cabeça linear ou o
último bloco da CNN para um atributo visual binarizado. Os candidatos iniciais
são `enquadramento_arquitetonico >= 2` e `inscricao_estatal >= 2`, que aparecem
em proporções preliminares próximas de 39/53 e 53/39 no pool de 92. Essas
proporções mudarão com o recorte estável de aproximadamente 70 itens. O alvo só
será confirmado depois da auditoria dos rótulos e da checagem dos grupos.

O checkpoint entregue deverá registrar:

- arquitetura e identificador dos pesos-base;
- pesos ajustados, se houver;
- transformação de entrada;
- classes e limiar;
- seed, identificador do freeze, versão da coorte e commit do código;
- métricas e limitações conhecidas.

### Etapa 4 — transformador visual

Como extensão, será testado **DINOv2** ou **CLIP** como extrator congelado. Um
modelo é suficiente. DINOv2 oferece uma comparação visual sem depender de
prompts; CLIP permite explorar linguagem e imagem, mas exige controle adicional
dos termos usados.

O repositório já contém um wrapper experimental para CLIP em
`tools/scripts/iconocracy_clip.py`, mas seu runtime externo não está completo no
ambiente atual. Ele será tratado como protótipo anterior, não como entrega já
pronta do grupo.

### Controle opcional — CNN iniciada do zero

Se os professores considerarem pedagogicamente útil, será treinada uma CNN
pequena, com duas ou três etapas convolucionais, exclusivamente como controle.
Espera-se que ela apresente alta variância ou sobreajuste. O interesse do teste
é demonstrar empiricamente por que o aprendizado por transferência é apropriado
a um corpus pequeno, não competir com arquiteturas de grande escala.

### Fora do núcleo

Detecção com YOLO exige caixas delimitadoras; segmentação semântica exige
máscaras por pixel. Como o corpus ainda não possui essas anotações, nenhuma das
duas tarefas será promessa central. Um piloto de segmentação assistida em poucas
imagens poderá entrar como ablação de fundo, depois que o sistema de recuperação
estiver funcionando.

## 6. Protocolo de avaliação

### 6.1 Avaliação principal da recuperação

Será selecionado um conjunto de aproximadamente 15 consultas, estratificado por
suporte, país, período e regime, sem variantes próximas entre as consultas.
Cada método retornará `top-10`. Os resultados serão reunidos, deduplicados e
avaliados sem revelar qual modelo produziu cada vizinho.

A especialista atribuirá duas notas independentes:

| Dimensão | 0 | 1 | 2 |
|---|---|---|---|
| Similaridade formal | sem relação visual relevante | compartilha um traço formal | forte proximidade morfológica/composicional |
| Utilidade iconográfica | não serve como comparandum | comparação possível | comparandum historicamente produtivo |

Métrica primária: **nDCG@10 para similaridade formal**. Métricas secundárias:

- nDCG@10 para utilidade iconográfica;
- Precision@5 considerando relevante a nota maior ou igual a 1;
- tempo de inferência e memória;
- análise qualitativa dos melhores e piores vizinhos.

### 6.2 Diagnósticos automáticos

Serão relatados como diagnósticos, não como verdade de referência:

- proporção de vizinhos do mesmo suporte;
- diferença média entre os dez indicadores separados;
- concentração por país, arquivo de origem e período;
- estabilidade dos vizinhos sob pequenas mudanças de pré-processamento;
- presença de texto, bordas, moldura ou fundo como possível atalho do modelo.

Clustering e projeções UMAP podem ilustrar o espaço de embeddings, mas não
substituem a avaliação da recuperação. Um cluster visualmente compacto pode
estar agrupando apenas papel envelhecido, molduras ou marcas do acervo.

### 6.3 Avaliação da tarefa supervisionada auxiliar

Se a cabeça classificadora for viável, serão usados:

- macro-F1;
- balanced accuracy;
- matriz de confusão;
- média e variação entre folds agrupados;
- erros separados por suporte, país e fonte.

Acurácia isolada não será aceita, e o conjunto de teste não será usado para
escolher arquitetura, limiar ou transformação.

### 6.4 Critério de sucesso

O sucesso científico não depende de a CNN “vencer”. O projeto é bem-sucedido se:

1. o freeze e a coorte visual são auditáveis e reproduzíveis;
2. não há vazamento conhecido entre grupos;
3. todos os métodos usam as mesmas consultas e galeria;
4. a avaliação é cega e as métricas são calculadas corretamente;
5. os erros e vieses são explicitados;
6. a conclusão respeita o alcance real dos dados.

## 7. Cronograma alinhado ao curso

| Data | Conteúdo da disciplina | Entrega interna do projeto |
|---|---|---|
| 12/08 | Paradigmas; clássico × deep learning | pitch, problema e formação da equipe |
| 19/08 | Thresholding e histogramas | auditoria inicial das imagens e histograma baseline |
| 26/08 | Distâncias, NN e kNN | primeira busca por similaridade |
| 02/09 | Convolução e morfologia | pipeline de pré-processamento versionado |
| 09/09 | Bordas e Canny | ablação de bordas e inspeção de contornos |
| 16/09 | Segmentação clássica | teste de contaminação por fundo em subconjunto |
| 23/09 | HOG, SIFT, SURF e ORB | descritor clássico e comparação com baseline |
| 30/09 | Hough, Gabor e pipeline clássico | congelamento do baseline clássico |
| 07/10 | ANNs e backpropagation | split agrupado e harness de treino/evaluação |
| 14/10 | CNNs, ResNet, EfficientNet, transfer learning | embeddings CNN e primeiro checkpoint |
| 21/10 | YOLO e Detectron2 | análise de atributos/localização; extensão opcional |
| 04/11 | U-Net e segmentação semântica | ablação assistida de figura–fundo, se necessária |
| 11/11 | Estudos de caso com deep learning | integração, análise de erros e decisão de escopo final |
| 18/11 | ViTs, SAM, DINOv2, DETR e CLIP | extensão com um transformador visual |
| 25/11 | andamento das equipes faltantes | resultados congelados, relatório e poster em revisão |
| 02/12 | Poster Session e sessão síncrona | cinco artefatos finais do Moodle |

A página fornecida não mostra atividade em 28 de outubro e só identifica 25 de
novembro como apresentação das equipes faltantes. O cronograma será atualizado
se o Plano de Ensino ou a agenda da turma trouxer outras datas.

## 8. Artefatos e reprodutibilidade

O freeze integral poderá ser materializado localmente com
`tools/scripts/build_hf_release.py`, que reúne os três ledgers, metadados de
release e `SHA256SUMS.txt`. A publicação externa é uma operação separada e não
faz parte automática deste projeto.

Cada execução deverá registrar:

- identificador e hashes do freeze integral;
- versão e hash do manifesto da coorte visual;
- commit do código;
- modelo e versão dos pesos pré-treinados;
- configuração completa de pré-processamento;
- seed e dispositivo de execução;
- consultas, galeria e `split_group`;
- métricas, rankings e julgamentos humanos;
- duração, memória e erros;
- ambiente Python reproduzível.

O desenvolvimento poderá usar Jupyter, OpenCV e PyTorch/fast.ai, coerentemente
com os materiais da disciplina. No computador da pesquisadora, os scripts do
repositório devem usar o ambiente `iconocracy`; para Colab ou VLAB@UFSC, as
versões de dependências deverão ser congeladas separadamente.

### Correspondência com as entregas finais

| Entrega Moodle | Conteúdo do projeto |
|---|---|
| Relatório PDF | problema, data card, métodos, métricas, erros e limites |
| Código ZIP | pipeline reproduzível, notebooks limpos, configs e testes essenciais |
| Checkpoint | cabeça ajustada ou modelo pequeno, mais referência verificável aos pesos-base |
| Slides | pergunta, comparação dos métodos e três achados centrais |
| Vídeo | demonstração da consulta e explicação de um sucesso e um erro |
| Poster PDF | atlas visual, diagrama da pipeline, métricas e limites |

As imagens com restrição de redistribuição não irão dentro do ZIP. O manifesto
permitirá reconstruir o dataset a partir das fontes, dentro das condições de uso
de cada acervo.

## 9. Divisão de responsabilidades

### Especialista de domínio

- definir elegibilidade e recorte historiográfico;
- adjudicar rótulos e duplicatas conceituais;
- selecionar consultas;
- avaliar formalidade e utilidade iconográfica;
- interpretar erros e redigir os limites epistemológicos.

### Implementação de ML/CV

- automatizar aquisição e validação técnica;
- implementar descritores, indexação e busca;
- configurar CNN, checkpoints e métricas;
- garantir split agrupado e reprodutibilidade;
- gerar visualizações comparáveis.

### Responsabilidade compartilhada

- formular hipóteses;
- revisar erros caso a caso;
- decidir extensões;
- produzir relatório, apresentação, vídeo e poster.

## 10. Riscos e respostas

| Risco | Resposta prevista |
|---|---|
| Confundir o N catalográfico com o N de uma tarefa visual | declarar o freeze N=335 e o N de cada visão derivada |
| N pequeno | usar transferência de aprendizado e avaliação de recuperação |
| Rótulos frágeis | excluir proveniências em auditoria das tarefas supervisionadas |
| Classes desbalanceadas | macro-F1, balanced accuracy, amostragem e slices explícitos |
| Duplicatas e séries | hash, hash perceptual e `split_group` |
| Modelo aprender suporte ou acervo | análise de erros por suporte, fonte, país e fundo |
| Imagens históricas fora do ImageNet | comparar métodos e não presumir generalização |
| Resolução e digitalização heterogêneas | contrato de imagem e ablações de pré-processamento |
| Direitos autorais heterogêneos | licença por item; binários restritos fora da entrega |
| Escopo excessivo | retrieval primeiro; classificação e segmentação só depois |
| Proximidade visual virar afirmação causal | separar medida computacional de interpretação histórica |

## 11. Guardrails epistemológicos

O projeto não afirmará que:

- uma rede neural compreendeu o terceiro nível de Panofsky;
- distância entre embeddings demonstra filiação histórica;
- os dez indicadores formam uma escala psicométrica única;
- o codebook é uma verdade objetiva;
- uma classificação visual prova um regime iconocrático;
- o corpus é uma amostra probabilística de toda a cultura jurídica;
- o resultado generaliza para qualquer alegoria ou qualquer acervo.

Formulação permitida:

> O modelo identificou proximidades em um espaço de características visuais.
> Essas proximidades foram avaliadas como formalmente semelhantes ou
> iconograficamente úteis segundo um protocolo explícito.

## 12. Decisões a validar com os professores

1. Recuperação por similaridade é aceita como tarefa principal do trabalho?
2. A entrega exige necessariamente pesos ajustados ou um extrator pré-treinado
   com cabeça linear e checkpoint próprio é suficiente?
3. Há número mínimo ou máximo de integrantes por equipe?
4. Qual é o prazo para registrar grupo e projeto?
5. Existe rubrica ou modelo obrigatório para relatório, vídeo e poster?
6. O VLAB@UFSC estará disponível para toda a equipe e com qual hardware?
7. O ZIP pode omitir imagens restritas e reconstruí-las por manifesto?
8. Há apresentação de andamento antes de 25 de novembro?

## 13. Primeiro sprint e regra de redução de escopo

### Sprint 0 — dados antes de modelos

1. materializar o freeze `ICONOCRACIA-CV-2026-08-12` e seu checksum;
2. gerar do freeze a lista dos 92 candidatos visuais;
3. recuperar e validar os binários;
4. calcular hashes, dimensões e MIME;
5. agrupar duplicatas e variantes;
6. produzir contact sheet para revisão;
7. congelar a visão derivada `cv-view-v0.1`;
8. somente então executar o baseline de histogramas e kNN.

### Regra de redução

- **80 ou mais imagens válidas:** pipeline completo, CNN congelada e tarefa
  supervisionada auxiliar;
- **50–79 imagens válidas:** recuperação com descritores e modelos congelados,
  sem fine-tuning como resultado central;
- **menos de 50 imagens válidas:** estudo piloto curado, sem alegação de
  desempenho geral e sem CNN profunda treinada do zero.

Essa regra impede que a pressão por mostrar uma rede neural transforme dados
insuficientes em resultados artificialmente seguros.

## Referências internas

- [Descrição canônica do dataset](../data/docs/dataset-description.md)
- [Snapshot de thumbnails v0.2](../data/processed/v0.2/README.md)
- [Piloto de validação visual](pilots/P02-gemini-vision-validation.md)
- [Decisão metodológica 2.0](decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md)
- [Conceito de iconometria](../concepts/iconometria.md)
- [Roadmap geral da ICONOCRACIA](roadmaps/2026-04-10-roadmap-geral-iconocracy.md)
