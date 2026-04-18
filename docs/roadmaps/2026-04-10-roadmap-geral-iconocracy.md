# Roadmap Geral — ICONOCRACY (home + monorepo)

Data: 2026-04-10
Status: proposta operacional de médio prazo
Escopo:
- infraestrutura geral em `/Users/ana`
- implementação específica em `/Users/ana/Research/hub/iconocracy-corpus`

---

## 1. Objetivo deste roadmap

Este roadmap reorganiza o projeto em duas camadas complementares:

1. **Camada home (`/Users/ana`)**
   Ambiente amplo de ferramentas, skills, MCPs, experimentos, superfícies auxiliares e laboratórios de IA.

2. **Camada monorepo (`/Users/ana/Research/hub/iconocracy-corpus`)**
   Superfície canônica da tese, do corpus e do pipeline WebScout → IconoCode → export/release.

Princípio central:
- `/Users/ana` = laboratório e infraestrutura de apoio
- `/Users/ana/Research/hub/iconocracy-corpus` = sistema de produção intelectual e documental da tese

---

## 2. Estado atual sintetizado

### 2.1. Home `/Users/ana`

Sinais atuais relevantes:
- `~/iconocracy-corpus` permanece como symlink de compatibilidade para o hub em `Research/`
- `~/Tools/` já concentra utilitários persistentes (ex.: `lm-eval-harness`, `remote-kernel`)
- `~/.hermes/skills/research/iconocracy-agent` já foi expandido com integração conceitual de CLIP e protótipo técnico
- há repositórios auxiliares em `~/Projects/`, inclusive:
  - `iurisvision`
  - `mcp/`
  - `skills/`
  - superfícies Ius Gentium separadas do núcleo ICONOCRACY
- existe `~/iconocracia-space`, sugerindo uma superfície pública/experimental paralela

### 2.2. Monorepo `/Users/ana/Research/hub/iconocracy-corpus`

Pontos estáveis observados:
- contrato canônico já definido:
  - `data/processed/records.jsonl`
  - `corpus/corpus-data.json`
  - `data/processed/purification.jsonl`
  - `vault/candidatos/` como espelho
- scripts canônicos já existem em `tools/scripts/`
- fluxo de release para Hugging Face já está documentado
- ingest/OCR já existem em `iconocracy-ingest/`
- o repositório já opera por superfícies Local / GitHub / Hugging Face

Sinais de expansão recente no working tree:
- dashboards e páginas auxiliares novos
- scripts novos para discovery, logging, MCP e refresh
- novos itens SCOUT no vault
- novos rascunhos e materiais de tese

Isso indica que o projeto entrou numa fase de **diversificação rápida** e precisa de um roadmap que recoloque ordem entre:
- infraestrutura
- corpus
- análise visual
- escrita
- publicação

---

## 3. Norte estratégico

### Meta principal

Transformar o ecossistema ICONOCRACY em um sistema integrado com cinco capacidades maduras:

1. **Descobrir** candidatos de corpus com rastreabilidade
2. **Analisar** imagens e séries visuais com rigor metodológico
3. **Organizar** notas, painéis e evidências no vault
4. **Escrever** tese e artigos a partir de material já estruturado
5. **Publicar** snapshots confiáveis em GitHub/Hugging Face sem contaminar o fluxo local

### Fórmula institucional do projeto

- `home` fornece ferramentas e inteligência auxiliar
- `iconocracy-corpus` conserva a verdade canônica
- `vault` organiza a inteligência de trabalho
- `HF/GitHub` publicam resultados congelados e auditáveis

---

## 4. Arquitetura-alvo em duas camadas

## A. Camada HOME (`/Users/ana`)

### A.1. Papel

Servir como infraestrutura transversal do ecossistema ICONOCRACY, sem competir com o monorepo canônico.

### A.2. O que deve viver no home

1. **Skills Hermes / Claude**
   - `~/.hermes/skills/`
   - `~/.claude/skills/`
   - skills de pesquisa, escrita, CLIP, auditoria, etc.

2. **Ferramentas reutilizáveis**
   - `~/Tools/lm-eval-harness`
   - kernels, utilitários, ambientes de benchmark
   - scripts independentes de avaliação ou prototipagem

3. **MCPs e bridges**
   - `~/Projects/mcp/`
   - integrações com Gallica, memória, NotebookLM, Zotero etc.

4. **Laboratórios e superfícies experimentais**
   - `~/iconocracia-space`
   - protótipos públicos/semipúblicos
   - demos independentes do corpus canônico

5. **Projetos paralelos que inspiram o núcleo, mas não o redefinem**
   - `~/Projects/iurisvision`
   - repositórios visuais, embeddings, exploração front-end

### A.3. O que NÃO deve viver no home como fonte da tese

- versão canônica do corpus
- ledger principal de ENDURECIMENTO
- export oficial do corpus
- snapshots públicos definitivos
- edição “solta” da tese fora do monorepo/vault

### A.4. Roadmap da camada home

#### Fase H1 — Consolidar infraestrutura transversal

1. Padronizar `~/Tools/` como casa oficial de ferramentas persistentes
   - benchmark/eval
   - kernels
   - futuros utilitários visuais

2. Consolidar `~/.hermes/skills/research/iconocracy-agent` como interface principal de orquestração
   - SCOUT
   - ICONOCODE
   - ZWISCHENRAUM
   - REDIGIR/REVISAR
   - CLIP auxiliar

3. Organizar MCPs por função
   - acervos
   - memória
   - bibliografia
   - anotação

#### Fase H2 — Montar laboratório visual externo ao monorepo

1. Prototipar ferramentas que ainda não devem entrar no core:
   - embeddings em lote
   - clustering visual
   - recuperação por similaridade
   - painéis experimentais

2. Testar integrações candidatas antes de canonizar
   - CLIP
   - OCR visual especializado
   - protótipos de comparação multimodal

#### Fase H3 — Criar superfície de pesquisa assistida

1. Tornar o home um hub operacional para:
   - discovery em acervos
   - benchmark de ferramentas
   - testes de modelos
   - prototipação UI/UX

2. Só depois promover artefatos maduros ao monorepo

---

## B. Camada MONOREPO (`/Users/ana/Research/hub/iconocracy-corpus`)

### B.1. Papel

Ser a superfície canônica da tese e do corpus.

### B.2. Princípios fixos

1. Ordem de verdade não muda:
   - `data/processed/records.jsonl`
   - `corpus/corpus-data.json`
   - `data/processed/purification.jsonl`
   - `vault/candidatos/`

2. `data/raw/` continua metadata-only
3. release gate continua obrigatório
4. vault continua espelho estruturado de trabalho, não fonte soberana
5. CLIP e quaisquer modelos de visão continuam auxiliares, não autoridade interpretativa

---

## 5. Roadmap geral do monorepo

### Fase R1 — Estabilização e limpeza do núcleo operacional
Prioridade: máxima
Horizonte: imediato

Objetivo:
reduzir dispersão e deixar claro o que já é canônico, experimental ou transitório.

Entregas:
1. Auditar scripts novos em `tools/scripts/`
   - `gallica_discovery.py`
   - `log_agent_run.py`
   - `mcp_integration.py`
   - `refresh_dashboard.py`
   - decidir: canonizar, mover para experimental, ou remover

2. Organizar artefatos recentes do working tree
   - dashboards novos
   - páginas auxiliares em `deploy/`
   - notebooks exploratórios
   - scripts temporários em `tmp/`

3. Criar convenção explícita para estados de artefato:
   - canônico
   - experimental
   - derivado de sessão
   - release-only

4. Revisar documentação para refletir o estado real do repo
   - `README.md`
   - `docs/scripts.md`
   - `AGENTS.md`
   - `docs/OPERATING_MODEL.md`

Resultado esperado:
uma topologia nítida do que é core vs experimento.

### Fase R2 — Fortalecer o pipeline canônico do corpus
Prioridade: máxima
Horizonte: curto prazo

Objetivo:
fazer `records.jsonl` virar o centro realmente operacional de tudo.

Entregas:
1. Expandir o schema operacional do registro com camadas auxiliares bem separadas
   - `clip_assist`
   - `ocr_extract`
   - `audit_flags`
   - `nearest_neighbors`
   - `evidence_status`

2. Integrar melhor:
   - ingest
   - sync com vault
   - export para corpus público
   - coding de ENDURECIMENTO

3. Garantir que qualquer nova camada auxiliar preserve a separação:
   - observação visual
   - auxílio computacional
   - interpretação iconológica
   - evidência documental

Resultado esperado:
um registro mestre mais rico sem perda de rigor.

### Fase R3 — CLIP operacional no fluxo SCOUT / ZWISCHENRAUM
Prioridade: alta
Horizonte: curto prazo

Objetivo:
promover CLIP de protótipo conceitual a ferramenta auxiliar real.

Entregas:
1. Pipeline para salvar embeddings por item
2. geração de `clip_assist` por imagem ou lote
3. busca por vizinhos visuais
4. uso em ranking de candidatos SCOUT
5. uso em sugestão de comparanda para painéis Zwischenraum

Regras metodológicas:
- CLIP nunca atribui regime final
- CLIP nunca fecha score final de ENDURECIMENTO
- CLIP sempre entra com `review_required: true`

Resultado esperado:
atlas visual navegável sem colapso interpretativo.

### Fase R4 — OCR, inscrições e contexto material
Prioridade: alta
Horizonte: curto/médio prazo

Objetivo:
integrar texto materialmente inscrito ao pipeline visual.

Entregas:
1. ligar `iconocracy-ingest/modules/ocr_engine.py` ao fluxo canônico
2. padronizar campos para:
   - texto inscrito
   - legenda
   - confiabilidade do OCR
   - origem do recorte/texto
3. anexar OCR a SCOUT e ICONOCODE
4. reforçar análise de inscrição estatal e contexto institucional

Resultado esperado:
articulação mais forte entre imagem, linguagem estatal e interpretação.

### Fase R5 — Vault como cockpit intelectual
Prioridade: alta
Horizonte: médio prazo

Objetivo:
fazer do vault a superfície viva da tese, ligada ao corpus canônico.

Entregas:
1. atualizar templates de notas
   - candidato
   - sessão
   - Zwischenraum
   - artigo/capítulo

2. integrar campos canônicos às notas
   - indicadores
   - `clip_assist`
   - OCR/inscrição
   - evidência
   - links para comparanda

3. criar estruturas para navegação
   - Bases do corpus
   - Bases de painéis
   - Base de lacunas
   - Canvas/JSON Canvas para painéis warburguianos

Resultado esperado:
pensamento, catalogação e escrita funcionando no mesmo circuito.

### Fase R6 — Escrita assistida a partir do corpus estruturado
Prioridade: alta
Horizonte: médio prazo

Objetivo:
ligar corpus e tese sem retrabalho manual excessivo.

Entregas:
1. gerar dossiês por item/painel
2. ligar itens do corpus a seções da tese
3. produzir notas de síntese por tema:
   - República
   - Justiça
   - moeda
   - selo
   - tribunal
   - monumentalização
   - ENDURECIMENTO

4. permitir passagem mais fluida:
   - SCOUT -> ICONOCODE -> ZWISCHENRAUM -> REDIGIR

Resultado esperado:
o corpus passa a ser infraestrutura de escrita, não apenas arquivo.

### Fase R7 — Publicação e superfícies externas
Prioridade: média
Horizonte: médio prazo

Objetivo:
estabilizar as superfícies públicas sem misturá-las ao fluxo de pesquisa.

Entregas:
1. consolidar explorer/dashboards públicos
2. separar claramente:
   - dashboards internos
   - companion/public explorer
   - Hugging Face frozen snapshot
3. rever `deploy/iconocracia-companion/`
4. transformar páginas auxiliares novas em superfícies com contrato explícito

Resultado esperado:
publicação mais limpa e menos acoplada ao trabalho em progresso.

### Fase R8 — Auditoria epistemológica do ecossistema
Prioridade: média-alta
Horizonte: contínuo

Objetivo:
explicitar a diferença entre:
- dado
- hipótese
- auxílio de modelo
- interpretação
- evidência documental

Entregas:
1. ampliar `audit_flags`
2. criar relatórios automáticos de conflito
3. marcar itens por status:
   - supported
   - tentative
   - gap
   - conflicting
4. priorizar revisão humana dos casos mais frágeis

Resultado esperado:
um corpus mais forte para tese, artigos e apresentação pública.

---

## 6. Integrações prioritárias (lista curta)

Se fosse preciso escolher apenas 5 frentes para os próximos ciclos, eu priorizaria:

1. **Estabilização do repo e classificação dos artefatos novos**
2. **Expansão do `records.jsonl` como ledger central**
3. **CLIP operacional com embeddings + vizinhos visuais**
4. **OCR/inscrição como camada canônica auxiliar**
5. **Vault/Bases/Canvas como cockpit de trabalho intelectual**

Essas cinco frentes já criam uma nova geração do projeto.

---

## 7. Separação explícita de responsabilidades

### O que pertence ao home
- skills
- MCPs
- ferramentas reutilizáveis
- laboratórios de protótipos
- benchmarks e experimentos com modelos
- superfícies auxiliares ainda não canonizadas

### O que pertence ao monorepo
- dados canônicos
- scripts canônicos
- vault espelhado/canonicamente sincronizado
- tese e manuscrito
- release pipeline
- exports e superfícies públicas oficiais

### Regra prática
Se algo responde à pergunta “isto altera a verdade do corpus/tese?”, deve entrar no monorepo.
Se responde à pergunta “isto testa, apoia ou acelera o trabalho?”, pode nascer no home.

---

## 8. Sequência de execução recomendada

### Sprint 1 — pôr ordem
- auditar working tree atual
- classificar scripts/páginas novos
- criar pasta e política para artefatos experimentais
- atualizar documentação operacional

### Sprint 2 — fortalecer ledger central
- desenhar schema expandido
- adicionar `clip_assist`, `ocr_extract`, `audit_flags`
- revisar sync/export/validação para os novos campos

### Sprint 3 — tornar CLIP real
- gerar embeddings
- salvar vizinhos visuais
- ligar CLIP ao SCOUT e ao ZWISCHENRAUM

### Sprint 4 — integrar OCR
- conectar ingest/OCR ao registro mestre
- reforçar texto inscrito e inscrição estatal

### Sprint 5 — transformar vault em cockpit
- templates
- Bases
- Canvas
- notas de sessão e painéis mais estruturados

### Sprint 6 — ligar corpus e escrita
- dossiês por item
- sínteses por tema
- ponte direta para capítulos e artigos

---

## 9. Critérios de sucesso

Este roadmap estará funcionando quando:

1. o home estiver claramente organizado como infraestrutura e laboratório
2. o monorepo estiver claramente organizado como superfície canônica
3. toda nova automação visual entrar como camada auxiliar auditável
4. o vault estiver operando como cockpit real do projeto
5. o corpus estiver mais fácil de explorar, comparar, escrever e publicar

---

## 10. Próximo passo recomendado

Próximo passo ideal: executar a **Sprint 1 — pôr ordem**.

Razão:
antes de adicionar novas capacidades, o projeto precisa consolidar o que já surgiu recentemente no working tree e separar melhor:
- core
- experimental
- derivado
- publicável

Depois disso, a Sprint 2 (schema expandido do ledger central) vira o verdadeiro ponto de inflexão do ecossistema.
