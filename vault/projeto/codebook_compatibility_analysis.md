# Análise de Compatibilidade do Codebook v0 e Schema Canonical (records.jsonl)

Esta análise mapeia o **Protocolo de Codificação Qualitativa (Codebook v0)**, estruturado em blocos para codificadores humanos, com o formato de dados canonizado em **`records.jsonl` (Codebook v2 / IMES v3)** do repositório Iconocracia.

---

## Mapeamento Geral de Blocos

### Bloco A — Identificação
Mapeia os metadados de procedência e arquivamento do item.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **ID** (`[PAÍS]-[SUPORTE]-[NÚMERO]`) | `item_id` | UUID canonical de 36 caracteres. O ID legível (`SCOUT-` ou `BR-`) é mapeado no index. |
| **País** | `input.place_hint` (entrada) / `region` (export) | Nome legível ou código regional. |
| **Suporte** | `purificacao.funcao_juridica` / `support` / `medium_norm` | Mapeado para enums padronizados (ex: `moeda_cedula` $\rightarrow$ `moeda`, `arquitetura_forense` $\rightarrow$ `arquitetura`). |
| **Título / denominação** | `input.title_hint` / `title` | Texto livre identificador do item. |
| **Data** | `input.date_hint` / `date` | Ano isolado ou intervalo textual. |
| **Instituição emissora** | `webscout.search_results[x].abnt_citation` | Extraído da citação bibliográfica formatada (ABNT). |
| **Fonte / localização** | `webscout.search_results[x].notes` | Descrito no campo de notas da evidência. |
| **URL / referência** | `input.input_url` / `webscout.search_results[x].url` | URL fonte da imagem ou paratexto. |
| **Dentro do escopo core?** | Filtrado via scripts de amostragem | Não exportado; garantido na fase de ingestão. |

---

### Bloco B — Figura Alegórica
Captura a iconografia básica e atributos formais.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **Tipo de alegoria** | `purificacao.familia_alegorica` | Enum: `["Virtudes", "Continentes", "Oceanos/Rios", "Nacional", "Outra"]`. |
| **Nome da figura** | `purificacao.subtipo` | Texto livre (ex: "Justiça", "Marianne", "Britânia"). |
| **Identificação certa?** | `purificacao.confidence_score` / `iconocode.confidence` | Escala contínua $[0.0, 1.0]$. |
| **Atributos visuais** | `purificacao.atributos_iconograficos` | Array de strings (ex: `["venda", "balança", "espada"]`). |
| **Postura / gesto** | `imes.pathosformel` | Conceito warburguiano (ex: "Justiça vendada sentada", "Corpo estático em trono"). |
| **Relação com texto** | `webscout.search_results[x].notes` | Descrito qualitativamente nas notas da evidência. |

---

### Bloco C — Marcadores de Gênero, Raça e Corpo
Mapeia a dimensão somática e visual da personificação.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **Gênero da figura** | `purificacao.genero_atribuido` | Enum: `["feminino", "masculino", "neutro", "hibrido", "ausente"]`. |
| **Codificação racial** | `purificacao.hipotese_racial` | Descrição qualitativa e categorização em texto livre. |
| **Tipo corporal** | `purificacao.notes` | Descrito nas observações textuais de purificação. |
| **Vestimenta** | `purificacao.atributos_iconograficos` / `purificacao.notes` | Ex: `toga`, `armadura` ou `nudez parcial` inseridos em atributos ou notas. |
| **Cabelo / cobertura** | `purificacao.atributos_iconograficos` | Elementos como `coroa mural`, `barrete frígio`, `capacete`. |
| **Seios expostos?** | Refletido em `purificacao.dessexualizacao` | O indicador de dessexualização varia de 0 (seios totalmente expostos / erotização clássica) a 3 (dessexualização estatal completa / armadura / toga rígida). |
| **Notas de gênero/raça** | `purificacao.notes` | Espaço para detalhamento das tensões corporais. |

---

### Bloco D — Circulação e Uso Institucional
Mapeia a inserção do item nos circuitos jurídicos e estatais.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **Alcance de circulação** | `imes.camada_2_campo.circulacao` | Array de strings (ex: `["Nacional", "Imperial"]`). |
| **Função institucional primária** | `purificacao.funcao_juridica` | Enum padronizado de suportes e funções jurídicas. |
| **Contexto de emissão** | `webscout.summary_evidence` / `purificacao.notes` | Narrativa de fundo histórico-legal. |
| **Duração em uso** | `input.date_hint` | Intervalo de vigência jurídica do dispositivo. |
| **Substituída por quê?** | `imes.linha_de_fuga` | Linha de fuga do dispositivo alegórico (tensão/transformação). |

---

### Bloco E — Conflito de Imagens / Iconoclasmo
Registra disputas visuais e cancelamento simbólico.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **Houve iconoclasmo?** | `purificacao.houve_iconoclasmo` | Booleano / Categórico sob chave `"purificacao"`. |
| **Tipo de conflito** | `purificacao.notes` | Detalhado qualitativamente nas observações de purificação. |
| **Data do conflito** | `purificacao.notes` | Registrado nas notas de conflito. |
| **Agente do conflito** | `purificacao.notes` | Identificação do ator social ou estatal. |
| **Documentação** | `webscout.search_results` | Referência secundária de evidência de contestação visual. |

---

### Bloco F — Análise Iconológica (Nível Interpretativo)
Níveis clássicos da hermenêutica da imagem (Panofsky/Warburg) integrados na triagem LPAI e IMES.

| Campo Codebook v0 | Propriedade em `records.jsonl` | Tipo / Observações |
|---|---|---|
| **Nível pré-iconográfico** | `iconocode.pre_iconographic` / `imes.camada_3_lpai_capta.nivel_pre_iconografico` | Motivos factuais observados na superfície da imagem. |
| **Nível iconográfico** | `iconocode.codes` (Iconclass) / `imes.camada_3_lpai_capta.nivel_iconografico` | Identificação formal através do vocabulário controlado Iconclass. |
| **Nível iconológico** | `iconocode.interpretation` / `imes.camada_3_lpai_capta.nivel_iconologico` | Interpretação conceitual (dispositivo, regimes, hipóteses). |
| **Relação com hipótese central** | `purificacao.regime_iconocratico` / `imes.linha_de_fuga` | Enquadramento nos três regimes (Fundacional, Normativo, Militar) ou Contra-Alegoria. |

---

## Alinhamento Teórico dos Indicadores de Purificação (Codebook v2)

Os **10 Indicadores de Purificação (0 a 3)** do Codebook v2 fornecem uma métrica quantitativa estruturada que condensa e operacionaliza as observações qualitativas dos Blocos B, C e D do Codebook v0:

1. **`desincorporacao`**: Mede a transição da figura de uma corporificação realista e contingente para uma abstração semiótica pura (Bloco C: Vestimenta / Tipo corporal).
2. **`rigidez_postural`**: Opera o indicador qualitativo de "Postura / gesto" (Bloco B), quantificando a contenção motora em direção à imobilidade pétrea estatal.
3. **`dessexualizacao`**: Mede a ocultação de marcadores sexuais e a contenção do seio feminino exposto (Bloco C: Seios expostos?).
4. **`uniformizacao_facial`**: Avalia a supressão de traços fisionômicos individuais e expressivos em prol de uma efígie geométrica clássica (Bloco C: Notas de gênero).
5. **`heraldizacao`**: Quantifica a incorporação de escudos, brasões e insígnias oficiais que engolem a autonomia da figura (Bloco B: Atributos).
6. **`enquadramento_arquitetonico`**: Mede a submissão da figura a frontões, nichos e colunatas nos tribunais (Bloco D: Função institucional / Contexto arquitetônico).
7. **`apagamento_narrativo`**: Avalia a transição de cenas dinâmicas (narrativas) para símbolos autônomos e isolados (Bloco B: Postura).
8. **`monocromatizacao`**: Mede a perda de cor e realismo cromático em direção ao preto e branco, metal monetário ou mármore (Bloco A: Suporte).
9. **`serialidade`**: Avalia o grau de reprodução técnica em massa e circulação repetitiva (Bloco D: Alcance de circulação).
10. **`inscricao_estatal`**: Mede a presença e proximidade física de inscrições de poder estatal (decretos, chancelas, siglas de emissores) junto à imagem (Bloco B: Relação com texto).
