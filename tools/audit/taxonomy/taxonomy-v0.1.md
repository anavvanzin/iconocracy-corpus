# Taxonomia provisória das relações iconocráticas

## Para a seção de metodologia visual da tese ICONOCRACIA

**Autora:** Ana Vanzin (PPGD/UFSC)
**Versão:** v0.1 (provisória, junho 2026)
**Função no projeto:** formalização do dispositivo Warburg como instrumento metodológico próprio, distinto dos painéis Mnemosyne originais, ancorado no corpus de 309 itens e nas três regiões iconocráticas (fundacional, normativo, militar) acrescidas da contra-alegoria.

---

## Nota preliminar

Esta taxonomia é construída em dois movimentos. Primeiro, **dedutivo**: parte das três funções iconocráticas já teorizadas (regime fundacional, regime normativo, regime militar) e da contra-alegoria como dispositivo crítico, perguntando que tipos de relação entre imagens essas funções tornam possíveis. Segundo, **indutivo**: a partir da estrutura do corpus existente (motivos recorrentes, pathosformeln já registradas nos campos `panofsky.iconographic.pathosformel`, distribuição de scores de endurecimento por regime), identifica que relações o material efetivamente sustenta como evidência.

A versão final da taxonomia deverá ser refinada contra os fios desenhados pela pesquisadora no Atlas Warburg da companion — esta é a sua função metodológica essencial: o ato de desenhar o fio é, ao mesmo tempo, um ato de leitura iconológica e um ato de calibração da taxonomia.

---

## I. Princípios da taxonomia

Quatro princípios estruturam o sistema:

**1. Toda relação iconocrática é orientada.** Mesmo quando o fio aparece visualmente como linha simétrica entre duas imagens, o pensamento iconológico que o produz é vetorial: A precede B, A descende para B, A inverte B, A serializa-se em B. A taxonomia registra a direção quando ela é interpretativamente relevante.

**2. Relações iconocráticas operam em três escalas simultâneas.** Há relações de superfície (motivos visuais compartilhados — barrete frígio, balança, espada), relações de função (papel performativo no aparelho de poder — fundar, regular, mobilizar), e relações de tempo (sobrevivência, transmissão, anacronismo). Um único fio pode pertencer a múltiplas escalas ao mesmo tempo. A taxonomia atribui uma **relação primária** e relações **secundárias**.

**3. A força de uma relação é mensurável, mas a mensuração é interpretativa.** Para cada categoria, há indicadores empíricos que podem ser checados no corpus (delta temporal, sobreposição de motivos, distância de score de endurecimento, identidade de país). Esses indicadores produzem uma escala 0–1 que sugere — não decide — a classificação.

**4. A taxonomia não substitui a interpretação iconológica panofskyana; ela a operacionaliza.** Cada categoria nomeia um movimento iconológico já articulável em prosa; a tipificação serve para tornar acessível à análise quantitativa o que de outro modo permanece num registro puramente descritivo.

---

## II. Tipos primários de relação iconocrática

### A. Relações genealógicas (eixo do tempo)

#### **1. Nachleben** (sobrevivência, no sentido warburguiano)
A imagem B reativa uma fórmula visual já presente em A, separada por longos intervalos temporais (tipicamente > 50 anos) e frequentemente por descontinuidades institucionais. O barrete frígio republicano (presente nas estampas de 1789, FR-013/014) reaparece na Semeuse de Roty (1898, FR-SEM-1898) e na Marianne de Steinlen (1915, FR-008) sem cadeia direta de transmissão entre os artistas: é o motivo que sobrevive ao seu contexto de produção e ressurge.

- **Indicadores empíricos:** Δ temporal > 50 anos; motivos compartilhados ≥ 1; ausência de relação institucional direta.
- **Operacionalização no analisador:** campo `pathosformel` no JSON com palavras-chave comuns nos dois extremos.
- **No corpus:** 57 itens têm o campo `pathosformel` registrado. Sobrevivências documentadas incluem: "Nachleben of Nike/Victory" (BR-001, FR-001), "Nachleben of Marianne tradition" (US-SLQ-1916), "Ripa via revolutionary sculpture" (FR-038).

#### **2. Mimesis** (imitação direta)
B copia ou parafraseia A num intervalo curto, com ou sem mediação institucional. Distingue-se do Nachleben pela proximidade temporal e pela cadeia documentável de transmissão. A Britannia das colônias britânicas (UK-TRADE-1895) imita explicitamente o desenho doméstico da Britannia (UK-PENNY-1860).

- **Indicadores:** Δ temporal ≤ 50 anos; motivos quase idênticos; mesmo país ou cadeia colonial.

#### **3. Genealogia** (descendência tipológica)
A produz uma família de B, B', B''… onde cada descendente herda traços estruturais sem ser cópia. O Compromisso Constitucional de Figueiredo (BR-002, 1896) gera uma família de alegorias republicanas brasileiras que reaparece em selos, moedas, e monumentos pelas três décadas seguintes.

- **Indicadores:** A precede temporalmente uma série de B; A é citado em fontes secundárias como protótipo; B compartilha estrutura compositiva mas não o motivo único.

#### **4. Serialização** (multiplicação industrial)
A mesma imagem é reproduzida em escala industrial em múltiplos suportes: moeda → selo → papel-moeda → poster. A Semeuse de Roty (FR-SEM-1898, score 2.5) é serializada no selo de 1903 (FR-SEM-SELO-1903, score 1.7) sem alteração iconográfica significativa, apenas adequando-se à exigência do suporte. Esta é a forma mais pura de **endurecimento normativo**.

- **Indicadores:** mesmo motivo principal; mesmo país; suportes distintos (M.1, M.3, M.10); Δ temporal ≤ 20 anos; score de endurecimento ≥ 1.5.
- **No corpus:** 9 itens numismáticos + 6 selos + 3 papéis-moeda + cartazes de Emprunts (≥ 10 itens) constituem o cluster mais denso de serialização.

---

### B. Relações estruturais (eixo da função)

#### **5. Translatio** (tradução nacional)
A mesma função iconocrática é executada por figuras visualmente distintas em tradições nacionais diferentes. Marianne em França (FR-009), Britannia em Inglaterra (UK-PENNY-1860), Germania em Alemanha (DE-001), Columbia nos EUA (US-007), Efígie da República no Brasil (BR-2000R-1907). Esses cinco itens não compartilham forma — compartilham **função normativa**: cada um é a personificação feminina do Estado em seu suporte numismático mais difundido.

- **Indicadores:** mesmo regime (em geral normativo); países diferentes; motivo "personificação nacional"; suportes equivalentes.
- **Importância para a tese:** translatio é a relação que prova o caráter **transnacional** do contrato sexual visual. Se a função normativa é executável por Marianne, Britannia, Germania e Columbia indistintamente, então a estrutura é estrutural — não um acidente francês.

#### **6. Concretização**
A passagem de uma alegoria abstrata para uma figura nomeada e individuada. Liberty enquanto abstração revolucionária (FR-038) torna-se Marianne enquanto personagem com biografia política recorrente (FR-009). A operação inversa — abstração — também ocorre.

- **Indicadores:** A é alegoria abstrata sem nome próprio fixo; B é nomeada e individuada; mesmo país; sobreposição de atributos.

#### **7. Par genderizado**
A figura feminina alegórica aparece em par com uma figura masculina soberana, configurando o "contrato sexual visual" no nível do plano pictórico. Ernouf retratado dentro de moldura alegórica feminina (FR-018); A Liberty/Britannia que recebe a espada do general (US-007); Justitia que entrega o documento ao monarca (FR-005 ou FR-006).

- **Indicadores:** presença explícita de figura masculina ao lado da alegoria feminina; figura masculina em posição ativa (recebe, executa, comanda); figura feminina em posição produtiva (gera, fia, autoriza).
- **Importância para a tese:** este é o cluster relacional que sustenta a leitura via Pateman do *Contrato Sexual*. Cada fio que conecta itens nesta categoria é evidência direta da tese.

---

### C. Relações de tensão (eixo crítico)

#### **8. Inversão**
A iconografia é reativada com sinal trocado. O barrete frígio que em Le Barbier autoriza a Declaração (FR-013) torna-se, em Veber (FR-010), brinquedo infantil — a Republic-as-rattle. A inversão preserva os atributos, mas reverte o seu valor performativo.

- **Indicadores:** mesmo motivo principal entre A e B; B classificado como contra-alegoria; mesmo país; Δ temporal típico de 30–80 anos.

#### **9. Satirização**
O fio conecta uma alegoria solene (regime normativo ou fundacional) à sua paródia visual. Marianne canônica (FR-009) ↔ Marianne satírica de Rops (FR-005). A satirização é distinta da inversão pela tonalidade: a inversão é estrutural; a satirização é tópica, situada num evento histórico específico (crise boulangista para FR-006, decadência republicana para FR-005).

- **Indicadores:** B classificado como contra-alegoria; suporte M.6 (cartoon/print); pertence a periódico identificável; produzido em momento de crise política nomeada.

#### **10. Contradição dialética**
A e B não são parodicamente opostos, mas estão em **tensão produtiva**. A Justitia colonial belga (BE-CONGO-1912) e a Justitia constitucional belga (BE-IND-1880) executam, no mesmo país e quase no mesmo período, papéis dialéticos: uma legitima o sistema constitucional doméstico, a outra legitima o regime colonial congolês. A contradição não é resolvida internamente ao corpus; é a contradição que se torna **objeto de análise**.

- **Indicadores:** mesmo país; mesmo período; regimes ou funções incompatíveis; mesmo aparelho institucional.
- **Importância para a tese:** este cluster sustenta o capítulo sobre **colonialidade do ver**.

---

### D. Relações de transição (eixo dos regimes)

Estas relações descrevem a passagem entre regimes iconocráticos — o movimento que sua hipótese central do ENDURECIMENTO requer demonstrar.

#### **11. Martialização**
Uma alegoria fundacional ou normativa é redeployada em registro militar. A Marianne civil da Declaração (FR-013, score 1.8, fundacional) reaparece como Marianne convocadora da Steinlen em 1915 (FR-008, militar). A operação adiciona armadura, gesto de comando, contexto de guerra; preserva a figura.

- **Indicadores:** A é fundacional ou normativo; B é militar; A precede B; mesmo motivo principal.
- **Score esperado:** Δ score positivo em direção a B (a versão militar costuma estar entre 0.8 e 1.8).
- **No corpus:** este é o cluster mais frágil estatisticamente (apenas 34 itens militares no corpus, sendo que apenas 4 são franceses). A taxonomia depende crucialmente do preenchimento desta lacuna.

#### **12. Desmilitarização**
O movimento inverso: a alegoria militar (pôster de guerra, medalha, monumento equestre) é integrada ao patrimônio civil em tempo de paz, perdendo função mobilizadora e ganhando função comemorativa. Os Emprunts da Défense Nationale de 1916–1920 documentam o início desta passagem: produzidos como mobilização militar, são reincorporados no século XXI como objeto histórico-civil.

- **Indicadores:** A é militar; B é normativo; A precede B; mesma figura ou motivo central.

#### **13. Endurecimento progressivo**
Cadeia ordenada de três ou mais itens onde o score de endurecimento cresce monotonicamente no tempo. Necker 1781 (1.3) → Le Barbier 1789 (1.8) → Semeuse 1898 (2.5) → busto cívico c. 1950 (2.4) constitui a cadeia paradigmática do caso francês. Esta não é uma relação binária — é uma **trajetória** que só se revela quando três ou mais fios são desenhados sequencialmente.

- **Indicadores:** três ou mais itens ligados em sequência temporal; scores monotonicamente crescentes; mesmo país e tradição alegórica; suportes compatíveis com serialização (M.1, M.3, M.4, M.9, M.10).
- **Operacionalização:** o analisador detecta esta relação quando identifica caminhos de comprimento ≥ 3 no grafo com score monotonicamente crescente.

---

### E. Relações de co-presença (eixo sincrônico)

#### **14. Co-presença política**
A e B não têm relação genealógica, mas pertencem ao mesmo momento histórico-político. O Compromisso Constitucional de Figueiredo (BR-002, 1896) e a Caricatura *La République aimable* de Rops (FR-005, 1871) não estão geneticamente conectados, mas ambos pertencem ao período pós-1870 da consolidação republicana europeia/americana — e a leitura dos dois lado a lado revela o que cada nacionalismo legitima e o que cada um nega.

- **Indicadores:** Δ temporal ≤ 25 anos; países diferentes; ausência de motivo compartilhado direto; pertencem a uma conjuntura política comum identificável.
- **Função analítica:** este é o tipo de fio que organiza painéis temáticos. Não pretende provar genealogia; pretende construir **constelação**.

#### **15. Co-presença institucional**
A e B pertencem ao mesmo aparelho institucional (mesmo tribunal, mesmo parlamento, mesmo museu). Justitia do STF (BR-009) e A República escultórica brasileira (BR-002) co-existem no mesmo aparelho de Estado, e a sua justaposição revela a composição interna do imaginário institucional.

- **Indicadores:** mesma instituição custodial; suportes compatíveis (escultura, pintura, fresco); produzidos como programa unitário.

---

## III. Padrões esperados por regime

A hipótese teórica produz previsões testáveis sobre quais tipos de relação devem predominar em cada regime.

### Regime fundacional

| Relação esperada | Por quê |
|---|---|
| **Co-presença política** | O regime fundacional opera em **constelação revolucionária** — múltiplas alegorias produzidas simultaneamente para autorizar o evento fundador |
| **Par genderizado** | A operação fundacional requer a sanção feminina sobre o ato masculino legislador |
| **Concretização** | Abstrações filosóficas (Liberté, Égalité) ganham corpo nomeado (Marianne) no momento fundacional |
| **Inversão (com contra-alegoria)** | Toda fundação produz seu satirista; Veber e Rops são contemporâneos do triunfo republicano |

### Regime normativo

| Relação esperada | Por quê |
|---|---|
| **Serialização** | O regime normativo opera por repetição industrial — moeda, selo, busto |
| **Mimesis** | Cópia controlada; o modelo é fixado e reproduzido sem desvio |
| **Translatio** | Esta é a fase em que cada nação consolida sua personificação canônica |
| **Genealogia** | Modelos de Roty e Ceschiatti geram famílias de obras |

### Regime militar

| Relação esperada | Por quê |
|---|---|
| **Martialização** | Quase por definição: o regime militar é a transição vinda do normativo |
| **Co-presença institucional** | Programas estatais coordenados (cartazes, medalhas, hinos) |
| **Inversão** (no momento de desmobilização) | A alegoria militar requer ser depois desautorizada quando a paz volta |

### Contra-alegoria

| Relação esperada | Por quê |
|---|---|
| **Satirização** | Definitória |
| **Inversão** | Categoria estrutural |
| **Nachleben crítico** | A contra-alegoria sobrevive como tradição própria (Veber → Henfil → Quino) |

---

## IV. Métricas de força da relação

Cada fio recebe três pontuações que, juntas, produzem uma **força de relação** entre 0 e 1:

- **Força semântica:** sobreposição de motivos (jaccard sobre o campo `motif`) — varia 0 a 1.
- **Força temporal:** distância no tempo modulada por expectativa do tipo de relação. Para Nachleben, Δ ≥ 50 anos aumenta a força. Para mimesis, Δ ≤ 20 anos aumenta a força.
- **Força regimental:** se o par de regimes corresponde ao esperado para o tipo declarado.

A força total é a média ponderada das três pontuações. Fios com força > 0.7 são reportados como **relações fortes** no relatório; fios com força < 0.3 são marcados para revisão.

---

## V. O que esta taxonomia *não* faz

Três limitações precisam estar inscritas na própria seção metodológica:

1. **Não substitui análise iconológica panofskyana de três níveis.** Cada categoria pressupõe que os itens já foram analisados nos três níveis. O fio é o quarto nível — a leitura comparativa.

2. **Não é simétrica entre regimes.** A taxonomia é mais rica para o regime normativo (onde há mais dados no corpus) e mais frágil para o militar. Esta assimetria reflete a lacuna do corpus, não uma escolha metodológica.

3. **Não é definitiva.** Esta é a v0.1. A versão v1.0, a ser fixada antes da qualificação, será produzida pelo confronto entre esta proposta dedutiva e o conjunto de fios efetivamente desenhados pela pesquisadora nas oito sessões de trabalho sobre os painéis Mnemosyne. Cada novo fio é, simultaneamente, um dado e uma testagem da taxonomia.

---

## VI. Operacionalização computacional

A taxonomia é executada pelo script `analyze_threads.py` que:

1. Lê o `corpus.json` com os 309 itens.
2. Lê os arquivos de painel exportados do Atlas Warburg (JSON, um por painel ou consolidado).
3. Para cada fio, calcula os indicadores empíricos descritos acima.
4. Atribui uma relação primária e secundárias.
5. Produz: um relatório markdown agrupando fios por painel e por tipo; um JSON estruturado para uso posterior em estatística; um SVG do grafo da rede (eixo X = ano, eixo Y = regime, cor = tipo de relação).

Output esperado nas seções da tese:

- **Capítulo 4 (Desenho Metodológico)** — apresenta a taxonomia completa como item 4.X.
- **Capítulo 9 (Os 8 Painéis do Atlas)** — para cada painel, lista os fios desenhados, sua classificação taxonômica e o argumento iconológico que os justifica.
- **Anexo metodológico** — o algoritmo de classificação como pseudocódigo, com tabela de transparência sobre falsos positivos e negativos identificados em rodadas de teste.

---

## VII. Próximo passo

Para sair da v0.1 e chegar à v1.0:

1. Desenhar pelo menos **10 fios por painel** no Atlas Warburg (= 80 fios). Cada fio deve registrar, no campo de ensaio do painel, a relação tipificada que a pesquisadora atribui a ele com base nesta taxonomia.
2. Exportar os 8 JSONs e rodar o analisador.
3. Comparar a classificação automática com a manual.
4. Onde houver discordância > 30%, **a taxonomia que precisa ajustar-se é a automática, não a manual** — a taxonomia é dispositivo descritivo da intuição iconológica da pesquisadora, não substituto dela.
5. Em janeiro/2027, fixar v1.0 como anexo do projeto de qualificação.

---

*Documento produzido para discussão com a banca de qualificação. Sujeito a revisão substantiva conforme o trabalho avance no Atlas Warburg.*
