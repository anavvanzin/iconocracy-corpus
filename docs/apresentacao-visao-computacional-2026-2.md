# ICONOCRACIA × Visão Computacional — Apresentação e proposta de grupo

**Disciplina:** INE410159 / TRV410001 — Visão Computacional (2026.2, Profs. Aldo von Wangenheim e Antonio Sobieranski)
**Contexto de uso:** (1) apresentação mútua da primeira semana ("Interesses, Razões para Estarem na Disciplina, Projetos de Pesquisa"); (2) pitch para formação de equipe multidisciplinar; (3) texto de referência para o professor.

---

## 1. Quem eu sou

Ana Vanzin, doutoranda do Programa de Pós-Graduação em Direito da UFSC. Minha área não é Computação — é teoria e história do Direito, com foco na relação entre **Direito e imagem**. Trago para a disciplina um problema real da minha tese, na lógica que a própria disciplina propõe: a especialista de domínio que entende o problema e quer aprender a instrumentalizá-lo tecnicamente.

## 2. A tese: como a Justiça se tornou visível

**ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)** parte de uma observação simples: o Direito não é feito só de textos. Ao longo de séculos, a Justiça construiu uma **gramática visual própria** — a figura alegórica feminina com venda, balança e espada; frontispícios de códigos; iluminuras; gravuras; fachadas de tribunais; selos e moedas.

Essas imagens não são decoração: são **tecnologias de legitimação**. Elas ensinam visualmente o que a Justiça é, quem ela serve e o que ela promete. A pergunta central da tese é *o que essas imagens fazem* — como a autoridade jurídica se constrói visualmente, e o que muda quando essa iconografia se repete, endurece ou se transforma ao longo do tempo (a tese trabalha com o eixo de **endurecimento/fixidez iconográfica**, medido por 10 indicadores em escala 0–3).

## 3. O corpus

Para responder isso, construí um **corpus iconográfico aberto e em crescimento (~335 registros)** de alegorias femininas da cultura jurídica, adquirido de arquivos digitais (Europeana, Gallica, BnF, Library of Congress, Numista, Colnect) por um pipeline automatizado (WebScout → IconoCode).

Cada imagem é codificada segundo um **codebook próprio**, inspirado nos três níveis de Panofsky e em sistemas como o Iconclass: presença e forma de atributos (balança, espada, venda, livro, serpente…), postura, composição, suporte, contexto. A codificação é feita por instrumentos baseados em LLMs, com **auditoria de confiabilidade inter-instrumento (IRR)** — ou seja, o corpus já tem uma camada de anotação sistemática com controle de qualidade.

O corpus é versionado no GitHub, com validação de schemas em CI: é um dataset real, limpo e documentado — não uma pasta de JPEGs.

## 4. Por que isso é um problema de Visão Computacional

Hoje a codificação depende de LLMs que "olham" a imagem e respondem o codebook. Funciona, mas não me dá **medidas**. Traduzindo as perguntas da tese para a linguagem da disciplina:

| Pergunta da tese (Direito) | Tarefa de Visão Computacional |
|---|---|
| Quais atributos estão presentes, e em que forma? | Classificação / detecção de atributos |
| Quais imagens são composicionalmente semelhantes? | Extração de características + similaridade (CBIR) |
| Existem "famílias" iconográficas que meu codebook não antecipou? | Clustering sobre embeddings visuais |
| Como um atributo muda de forma ao longo do tempo? | Distância no espaço de características × análise temporal (endurecimento) |
| Onde está a figura alegórica dentro de uma página de manuscrito? | Segmentação figura–fundo |

E há uma ponte teórica que considero o coração do projeto: Panofsky dividiu a leitura de imagens em três níveis — (1) formas e cores, (2) figuras e símbolos reconhecidos, (3) sentido cultural interpretado. Isso é quase exatamente a arquitetura de um sistema de visão: **características de baixo nível → reconhecimento de padrões → semântica**. A fronteira entre o que o computador mede e o que o historiador interpreta — o *semantic gap* — não é um obstáculo para mim: **é o próprio objeto da tese**.

## 5. Os dois caminhos (ancorados no plano da disciplina)

**Caminho clássico (Módulo 1):**

- **Cap. 1.1 — Medidas de Similaridade e Distância** (Hamming, Euclidiana, kNN, Mahalanobis): a base formal da pergunta "quão parecidas são duas Justiças?". Aplicável já nas semanas 2–3 com histogramas de cor — a alegoria da Justiça tem convenções cromáticas fortes.
- **Cap. 1.2 — Convolução, Morfologia, Bordas, Segmentação**: isolar a figura alegórica do fundo (iluminuras e frontispícios têm margens, texto e ornamentos que contaminam qualquer descritor global).
- **Cap. 1.4 — HOG, SIFT, ORB, Hough, Gabor**: emparelhar atributos recorrentes (balança, espada) entre imagens de épocas e suportes diferentes.
- Vantagem metodológica para uma tese de Direito: um modelo clássico é **interpretável** — posso explicar à banca *por que* a máquina agrupou aquilo.

**Caminho de aprendizado profundo (Módulo 2):**

- **Cap. 2.3–2.4 — Detecção de objetos (YOLO) e segmentação semântica**: localizar atributos automaticamente dentro das imagens.
- **Cap. 2.7 — Transformadores Visuais (SAM, DINOv2, DETR, CLIP)**: o caminho mais promissor para corpus pequeno — **embeddings de modelos pré-treinados (CLIP/DINOv2) para similaridade e clustering sem treinar nada do zero**, e SAM para segmentação figura–fundo sem anotação manual.
- Desafios que me interessam discutir: N pequeno (~335), classes desbalanceadas (quase toda Justiça tem balança; poucas têm serpente), e imagens históricas fora da distribuição dos datasets de treino (iluminuras medievais não são fotos do ImageNet).

## 6. Proposta de projeto de semestre (o pitch para o grupo)

**Título de trabalho:** *Um atlas de similaridade das alegorias femininas da Justiça: medindo o endurecimento iconográfico com visão clássica e embeddings profundos.*

**Pipeline em três etapas:**
1. **Pré-processamento e visão clássica** — normalização das imagens, segmentação figura–fundo, extração de histogramas de cor e descritores (HOG/SIFT), similaridade por kNN.
2. **Embeddings profundos** — CLIP/DINOv2 sobre o corpus, clustering, busca por similaridade (CBIR).
3. **Avaliação contra o codebook** — os agrupamentos encontrados pela máquina convergem ou divergem das famílias iconográficas codificadas? A divergência é achado de pesquisa, não falha: indica padrões formais que a tradição iconográfica não nomeou.

**O que o grupo ganha:**
- **Dados prontos**: 335 imagens curadas, versionadas, com metadados e documentação metodológica.
- **Ground truth de graça**: o codebook auditado funciona como gabarito anotado — raríssimo em projetos de semestre.
- **Poster visualmente imbatível**: alegorias de cinco séculos lado a lado, mapas de similaridade, clusters visuais.
- **Potencial de publicação interdisciplinar** (Direito × Computação, humanidades digitais).

**O que eu trago:** o corpus, o codebook, o domínio (sei dizer *por que* separar a Justiça com serpente da Justiça sem serpente importa historicamente), um pipeline Python/Jupyter já existente e infraestrutura de versionamento com CI.

**O que procuro:** 1–2 colegas com mais experiência em implementação de ML/CV — alguém que queira aplicar o conteúdo da disciplina num problema onde os dados e a pergunta de pesquisa já existem.

## 7. Encaixe no cronograma 2026.2

- **Semanas 1–4 (Módulo 1 início):** histogramas + medidas de distância (Cap. 1.1) — primeiro resultado concreto cedo.
- **Meio do semestre (apresentações de andamento):** segmentação + descritores clássicos vs. primeiros embeddings.
- **02/12/2026 (sessão síncrona de trabalhos) / poster session final:** atlas de similaridade + comparação clássico × profundo × codebook.
