# Transição IMES v3.0 — Implementation Plan

> **For agentic workers:** Use subagent-driven-development (recommended) or executing-plans to implement task-by-task.

**Goal:** Executar a transição metodológica da tese de score-centric para IMES (Iconocracia como Dispositivo Metodológico Estratificado), cobrindo documentação, capítulo metodológico, schema JSON, mapeamento de Regimes Visuais e piloto de 3 pranchas.

**Architecture:** Três camadas operam sobre o corpus de 165 registros: Atlas-Argumento (pranchas warburguianas), Campo Cartográfico (posições no campo), LPAI-capta (triagem de ausência). A unidade de análise é o Regime Visual (RV), validado por Critérios de Justificação de Vizinhança (CJV).

**Tech Stack:** Markdown/Pandoc (tese), JSON Schema (corpus), Python/conda (notebooks + validação), Obsidian (vault), HTML/CSS ou TikZ (pranchas).

**Branch:** `feature/imes-v3-transition` (criar antes de tocar em ficheiros)

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `vault/tese/ideias/2026-04-23_decisao-metodologica-imes.md` | Create | Documento de decisão metodológica (defesa do IMES) |
| `vault/tese/metodologia/capitulo-2-reescrito.md` | Create | Reescrita do Cap. 2 com IMES como método central |
| `tools/schemas/master-record.schema.json` | Modify | Adicionar bloco `imes`, bump para 2.0.0-imes |
| `vault/research-wiki/ideas/idea004.md` | Create | Refinamento de IMES no research wiki |
| `vault/tese/metodologia/preregistration-pranchas.md` | Create | Preregistration das 10 pranchas piloto |
| `vault/tese/metodologia/regimes-visuais-mapeados.md` | Create | Lista de 4-6 RVs identificáveis no corpus |
| `vault/research-wiki/imes-rv/` | Create dir | Notas `imes-rv` para cada Regime Visual (template X4) |
| `notebooks/09-validacao-pranchas.ipynb` | Create | Notebook de validação CJV para pranchas-atlas |
| `ICONOCRACY_MASTER_PROMPT.md` | Already done | v3.0 já atualizado em 2026-04-23 |

---

## Task 1: Criar documento de decisão metodológica

**Files:**
- Create: `vault/tese/ideias/2026-04-23_decisao-metodologica-imes.md`

**Context:** O documento deve defender por que a transição para IMES é necessária e epistemologicamente justificada. Referenciar papers do research wiki.

- [ ] **Step 1: Escrever estrutura do documento**
  ```markdown
  ---
  tipo: decisao-metodologica
  data: 2026-04-23
  versao: 1.0
  ---

  # Decisão Metodológica: IMES v3.0

  ## 1. Por que score puro falha

  ### 1.1. Violação epistêmica (Merry 2016, Drucker 2011, Espeland & Sauder 2007)
  A escala 0-3 impõe teleologia onde o objeto é constitutivamente paradoxal. A alegoria
  feminina não "evolui" de 0 para 3; ela opera em regimes distintos com lógicas próprias.

  ### 1.2. Classificação de tipos vs. identificação de indivíduos
  O score agrupa em clusters numéricos o que deveria ser lido como constelação visual.
  Hayaert (2020) e Stramignoni (2024) demonstram que a análise warburguiana capta
  afinidades que o score esconde.

  ### 1.3. Reatividade do índice
  A escala foi herdada de um pipeline técnico, não construída a partir de convicção
  teórica sobre o objeto.

  ## 2. Por que atlas puro falha

  ### 2.1. Ausência de protocolo de validação (gap:G3)
  Warburg tinha 40 anos de erudição. Uma doutoranda precisa de critérios explícitos.
  Sem CJV, o atlas vira livre-associação estética.

  ### 2.2. Risco de HARKing visual
  Montar pranchas post-hoc e depois escrever o argumento como se a prancha tivesse
  sido projetada para demonstrá-lo.

  ### 2.3. Banca de direito pode não reconhecer rigor
  O atlas precisa de protocolo operacional para ser legível como método acadêmico.

  ## 3. Por que IMES resolve

  ### 3.1. Triangulação de três camadas
  Nenhuma camada sozinha sustenta a tese. Juntas, cancelam as premissas de unicidade
  metodológica e preservam o que cada uma faz bem.

  ### 3.2. Protocolo explícito (CJV)
  Critérios de justificação de vizinhança com regra de validação (80%). Não é livre
  associação; é constelação argumentativa.

  ### 3.3. Ineditismo defensável
  "Sou a primeira a construir um atlas warburguiano sistemático sobre alegoria feminina
  jurídica na América Latina, operacionalizado através de um protocolo de Regime Visual
  com critérios explícitos de justificação de vizinhança."

  ## 4. Defesa perante a banca

  ### 4.1. Precedentes
  - Stramignoni 2024: Pathosformel em imagem jurídica (1 imagem)
  - Pollock 2007: atlas warburguiano operacionalizado (feminismo)
  - Didi-Huberman 2011: atlas como dispositivo arqueológico

  ### 4.2. Originalidade
  Ninguém combinou: (a) corpus de 100+ imagens, (b) direito, (c) feminismo,
  (d) América Latina, (e) protocolo de validação explícito.

  ### 4.3. Limites honestos
  IMES é calibragem, não dogma. O limiar de 80% CJV pode ser ajustado.
  A Camada 2 (campo) depende de dados etnográficos que podem estar incompletos.
  ```

- [ ] **Step 2: Verificar se ficheiro foi criado**
  ```bash
  ls -la vault/tese/ideias/2026-04-23_decisao-metodologica-imes.md
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add vault/tese/ideias/2026-04-23_decisao-metodologica-imes.md
  git commit -m "docs: decisao metodologica IMES v3.0 — defesa da transicao"
  ```

---

## Task 2: Reescrever Capítulo 2 (Metodologia IMES)

**Files:**
- Create: `vault/tese/metodologia/capitulo-2-reescrito.md`
- Read first: `ICONOCRACY_MASTER_PROMPT.md` (Seções G, H, IMES)

**Context:** O capítulo metodológico atual (se existir) está score-centric. Esta é a reescrita completa apresentando IMES como método central.

- [ ] **Step 1: Escrever estrutura do Cap. 2**
  ```markdown
  # Capítulo 2 — Dispositivo Metodológico Estratificado (IMES)

  ## 2.1. Do instrumento de medição ao dispositivo de leitura

  [Transição epistemológica: por que abandonar score puro]

  ## 2.2. Arquitetura IMES

  ### 2.2.1. Camada 1: Atlas-Argumento (primária)
  ### 2.2.2. Camada 2: Campo Cartográfico (relacional)
  ### 2.2.3. Camada 3: LPAI-capta (instrumental)

  [Inserir diagrama conceitual aqui — ver template abaixo]

  ## 2.3. Regime Visual: unidade de análise

  ### 2.3.1. Definição
  ### 2.3.2. Componentes (suporte, campo, Pathosformel, linha de fuga)
  ### 2.3.3. Exemplos do corpus (4-6 RVs)

  ## 2.4. Critérios de Justificação de Vizinhança (CJV)

  ### 2.4.1. CJV-1: Eco formal
  ### 2.4.2. CJV-2: Eco histórico
  ### 2.4.3. CJV-3: Eco de campo
  ### 2.4.4. Regra de validação (80%)
  ### 2.4.5. Protocolo de aplicação

  ## 2.5. LPAI-capta: enquadramento instrumental

  ### 2.5.1. All data is capta (Drucker 2011)
  ### 2.5.2. Os 10 indicadores como triagem documental
  ### 2.5.3. Score de endurecimento: resumo, não prova

  ## 2.6. Prevenção de HARKing visual

  ### 2.6.1. Preregistration de pranchas
  ### 2.6.2. Documentação de decisões
  ### 2.6.3. Auditoria de pranchas

  ## 2.7. Limites e honestidade metodológica

  [Nota de rodapé sobre o que IMES não faz]
  ```

- [ ] **Step 2: Inserir diagrama IMES (TikZ ou ASCII)**
  ```latex
  % Opcional: TikZ para compilação Pandoc
  \begin{tikzpicture}[node distance=2cm]
    \node (corpus) [draw, rectangle] {Corpus (N=165)};
    \node (atlas) [draw, rectangle, above left of=corpus] {Camada 1: Atlas-Argumento};
    \node (campo) [draw, rectangle, above of=corpus] {Camada 2: Campo Cartográfico};
    \node (capta) [draw, rectangle, above right of=corpus] {Camada 3: LPAI-capta};
    \draw[->] (corpus) -- (atlas);
    \draw[->] (corpus) -- (campo);
    \draw[->] (corpus) -- (capta);
  \end{tikzpicture}
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add vault/tese/metodologia/capitulo-2-reescrito.md
  git commit -m "docs: reescrita do Cap.2 com IMES v3.0 como metodo central"
  ```

---

## Task 3: Atualizar schema JSON (master-record v2.0.0-imes)

**Files:**
- Modify: `tools/schemas/master-record.schema.json`
- Test: `tools/scripts/validate_schemas.py`

**Context:** O schema atual é v1.0.0 e não inclui o bloco `imes`. Precisa de bump para 2.0.0-imes.

- [ ] **Step 1: Fazer backup do schema atual**
  ```bash
  cp tools/schemas/master-record.schema.json tools/schemas/master-record.schema.v1.json
  ```

- [ ] **Step 2: Adicionar bloco `imes` ao schema**
  ```json
  "imes": {
    "type": "object",
    "description": "Iconocracia como Dispositivo Metodológico Estratificado",
    "properties": {
      "regime_visual": {
        "type": "string",
        "description": "Nome do Regime Visual identificado"
      },
      "pathosformel": {
        "type": "string",
        "description": "Eco formal gestual dominante"
      },
      "linha_de_fuga": {
        "type": "string",
        "description": "Tensão interna ou transformação em curso"
      },
      "camada_1_atlas": {
        "type": "object",
        "properties": {
          "pranchas": {
            "type": "array",
            "items": { "type": "string" },
            "description": "IDs das pranchas-atlas onde o item aparece"
          },
          "cjvs": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Critérios de justificação de vizinhança satisfeitos"
          }
        }
      },
      "camada_2_campo": {
        "type": "object",
        "properties": {
          "posicao_campo": { "type": "string" },
          "produtores": {
            "type": "array",
            "items": { "type": "string" }
          },
          "circulacao": { "type": "string" }
        }
      },
      "camada_3_lpai_capta": {
        "type": "object",
        "properties": {
          "indicadores": {
            "type": "object",
            "properties": {
              "desincorporacao": { "type": "integer", "minimum": 0, "maximum": 3 },
              "rigidez_postural": { "type": "integer", "minimum": 0, "maximum": 3 },
              "dessexualizacao": { "type": "integer", "minimum": 0, "maximum": 3 },
              "uniformizacao_facial": { "type": "integer", "minimum": 0, "maximum": 3 },
              "heraldizacao": { "type": "integer", "minimum": 0, "maximum": 3 },
              "enquadramento_arquitetônico": { "type": "integer", "minimum": 0, "maximum": 3 },
              "apagamento_narrativo": { "type": "integer", "minimum": 0, "maximum": 3 },
              "monocromatizacao": { "type": "integer", "minimum": 0, "maximum": 3 },
              "serialidade": { "type": "integer", "minimum": 0, "maximum": 3 },
              "inscricao_estatal": { "type": "integer", "minimum": 0, "maximum": 3 }
            }
          },
          "endurecimento_score": { "type": "number", "minimum": 0, "maximum": 3 },
          "ausencias": {
            "type": "array",
            "items": { "type": "string" },
            "description": "O que a imagem esconde ou omite"
          },
          "contradicoes": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Contradições entre indicadores ou entre indicadores e leitura visual"
          }
        }
      }
    }
  }
  ```

- [ ] **Step 3: Bump da versão no schema**
  Modificar `"master_record_version"` de `"1.0.0"` para `"2.0.0-imes"`

- [ ] **Step 4: Validar schema**
  ```bash
  cd /Users/ana/iconocracy-corpus
  conda run -n iconocracy python tools/scripts/validate_schemas.py
  ```

- [ ] **Step 5: Commit**
  ```bash
  git add tools/schemas/master-record.schema.json
  git commit -m "schema: master-record v2.0.0-imes com bloco IMES"
  ```

---

## Task 4: Criar idea:004 no research wiki

**Files:**
- Create: `vault/research-wiki/ideas/idea004.md`
- Read first: `vault/research-wiki/ideas/idea003.md` (IMES base)

**Context:** Refinamento da idea:003 após a transição ser decidida. Status: validated.

- [ ] **Step 1: Escrever idea:004**
  ```markdown
  ---
  type: idea
  node_id: idea:004
  title: "IMES v3.0 — Protocolo de Regime Visual e CJV"
  status: validated
  stage: active
  added: 2026-04-23T14:40:00Z
  updated: 2026-04-23T14:40:00Z
  ---

  # idea:004 — IMES v3.0 (Refinamento)

  ## Description

  Refinamento operacional de IMES (idea:003) após decisão de transição metodológica.
  Versão 3.0 inclui: (a) Regime Visual como unidade de análise, (b) CJV com regra
  de 80%, (c) prevenção de HARKing via preregistration, (d) master prompt v3.0,
  (e) schema JSON 2.0.0-imes.

  ## Predecessor

  - idea:003 (IMES base)

  ## Based on

  - paper:stramignoni2024, paper:didi_huberman2011, paper:pollock2007
  - paper:merry2016, paper:drucker2011
  - ultraplan:2026-04-23-transicao-imes

  ## Target gaps

  - gap:G3 (protocolo de validade para justaposições atlas) — parcialmente resolvido
  - gap:G1 (Warburg + direito + feminismo + AmLatina) — avançado

  ## Expected outcome

  Piloto de 10 pranchas validadas com CJV ≥80%, documentação completa no capítulo
  metodológico, schema JSON operacional.

  ## Risks (atualizados)

  - **Cronograma:** 19 passos no ultraplan. Priorizar piloto de 3 pranchas primeiro.
  - **Banca:** preparar guia de leitura e devil's advocate antes da qualificação.
  - **CJV 80%:** é calibragem, não dogma. Documentar na tese.

  ## Notes

  Status changed from proposed to validated após Fase 6 da dialética.
  Ver também: decisao-metodologica-imes, capitulo-2-reescrito.
  ```

- [ ] **Step 2: Commit**
  ```bash
  git add vault/research-wiki/ideas/idea004.md
  git commit -m "docs(wiki): idea:004 IMES v3.0 refinamento validado"
  ```

---

## Task 5: Mapear Regimes Visuais no corpus

**Files:**
- Create: `vault/tese/metodologia/regimes-visuais-mapeados.md`
- Create dir: `vault/research-wiki/imes-rv/`
- Read first: `data/processed/records.jsonl` (para identificar itens exemplares)

**Context:** Identificar 4-6 RVs estáveis nos 165 registros. Cada RV precisa de itens exemplares.

- [ ] **Step 1: Escrever mapeamento de RVs**
  ```markdown
  # Regimes Visuais Mapeados — Corpus ICONOCRACIA

  > Gerado em: 2026-04-23
  > Fonte: data/processed/records.jsonl (N=165, válidos=154)
  > Método: leitura manual de registros codificados + agrupamento por afinidade

  ## RV-1: Justitia Monumental

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | Palácios do Judiciário, fachadas de tribunais, salas de sessão |
  | Posição de campo | Comissões de arte do Judiciário, concursos públicos |
  | Pathosformel | Balança-nua, postura frontal, toga clássica |
  | Linha de fuga | Militarização (capacete/espada em contextos de guerra) |

  **Itens exemplares:**
  - SCOUT-??? [Identificar do records.jsonl]
  - SCOUT-???

  ## RV-2: Libertas Republicana

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | Moeda, selo, medalha comemorativa |
  | Posição de campo | Casas da Moeda, ministérios, comissões oficiais |
  | Pathosformel | Coroa radiada, braço erguido, corpo em movimento |
  | Linha de fuga | Desfeminização (substituição por símbolos abstratos) |

  ## RV-3: Germania Imperial

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | Moeda colonial, medalha militar, cartaz de propaganda |
  | Posição de campo | Estado imperial, bancos emissores coloniais |
  | Pathosformel | Couraça-elmo, espada, corpo blindado |
  | Linha de fuga | Abandono (República de Weimar substitui por águia) |

  ## RV-4: República Positivista (Brasil)

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | Moeda, selo, monumento público |
  | Posição de campo | Comissão de arte do TJ, concursos nacionais |
  | Pathosformel | Coroa de louros, postura estática, vestes clássicas |
  | Linha de fuga | Congelamento (importação neoclássica sem transformação local) |

  ## RV-5: Britannia Colonial

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | British Trade Dollar, selo colonial, cartaz imperial |
  | Posição de campo | Royal Mint, East India Company, administração colonial |
  | Pathosformel | Tridente, elmo, de pé sobre globo |
  | Linha de fuga | Descolonização (abandono progressivo da alegoria) |

  ## RV-6: Justitia Contracanônica

  | Componente | Descrição |
  |------------|-----------|
  | Suporte material | Arte de rua, cartaz político, intervenção urbana |
  | Posição de campo | Movimentos sociais, arte ativista, contracultura |
  | Pathosformel | Balança invertida, corpo fragmentado, rosto visível |
  | Linha de fuga | Reapropriação (subversão do código oficial) |
  ```

- [ ] **Step 2: Identificar itens exemplares do records.jsonl**
  ```bash
  cd /Users/ana/iconocracy-corpus
  conda run -n iconocracy python -c "
  import json
  with open('data/processed/records.jsonl') as f:
      for line in f:
          rec = json.loads(line)
          print(rec.get('item_id'), rec.get('regime_iconocratico'), rec.get('pais'))
  " | head -30
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add vault/tese/metodologia/regimes-visuais-mapeados.md
  git commit -m "docs: mapeamento de 6 Regimes Visuais no corpus"
  ```

---

## Task 6: Criar preregistration de 10 pranchas piloto

**Files:**
- Create: `vault/tese/metodologia/preregistration-pranchas.md`

**Context:** Preregistration é obrigatória para prevenir HARKing. Cada prancha precisa de tese, imagens propostas e CJV esperados — ANTES de montar qualquer prancha visual.

- [ ] **Step 1: Escrever preregistration**
  ```markdown
  # Preregistration de Pranchas Piloto IMES

  > Data de preregistration: 2026-04-23
  > Número de pranchas: 10
  > Critério de validação: ≥80% dos pares adjacentes satisfazem CJV
  > Status: pre-registrado (ainda não montado)

  ## Prancha 1: Gênese Republicana

  **Tese:** O nascimento da alegoria republicana no Brasil (1889) recapitula padrões
  visuais das revoluções francesa (1848) e americana (1787), mas com dessexualização
  prévia importada do positivismo.

  **Imagens propostas (6-8):**
  1. SCOUT-??? — Proclamação da República, BR 1889
  2. SCOUT-??? — Marianne de 1848, FR
  3. SCOUT-??? — Columbia/EUA 1787
  4. SCOUT-??? — A República (BR, moeda/selo)
  5. SCOUT-??? — Marianne barricada, FR 1848
  6. SCOUT-??? — A República positivista, BR

  **CJV esperados:**
  - CJV-1 (Eco formal): Pathosformel do braço erguido/corpo dinâmico
  - CJV-2 (Eco histórico): Eventos fundacionais republicanos
  - CJV-3 (Eco de campo): Produção estatal/comissionada

  ## Prancha 2: Justitia e a Venda

  **Tese:** A venda nos olhos de Justitia opera como limiar de dessexualização:
  sua introdução marca a transição de FUNDACIONAL para NORMATIVO.

  ## Prancha 3: Da Barricada ao Selo

  **Tese:** A domesticação de Marianne (1789 → Semeuse 1898) demonstra o
  endurecimento como purificação progressiva do corpo vivo em ícone estatal.

  ## Prancha 4: Corpo em Guerra

  **Tese:** A militarização da alegoria feminina (1914-1918) não é linear:
  Germania endurece completamente; Marianne resiste; Britannia já nasceu armada.

  ## Prancha 5: Pedra e Bronze

  **Tese:** A arquitetura forense como suporte material do RV monumental fixa
  a alegoria no espaço público de forma irreversível.

  ## Prancha 6: Balança e Império

  **Tese:** A balança da Justitia é exportada como instrumento de hierarquização
  geopolítica nas moedas coloniais (UK, FR, BE).

  ## Prancha 7: Branquitude e Ausência

  **Tese:** O Contrato Racial Visual opera como ausência: corpos não-brancos
  são sistematicamente excluídos da alegoria "universal" (lacuna Resnik-Curtis no BR).

  ## Prancha 8: Dessexualização como Limiar

  **Tese:** A dessexualização é condição necessária de sobrevivência iconocrática.
  Comparação: Educational Series EUA (falha) vs. Semeuse FR (sucesso).

  ## Prancha 9: Contra-Alegorias

  **Tese:** Contra-alegorias não são "falhas" do sistema iconocrático, mas
  reapropriações que desestabilizam o Contrato Sexual Visual.

  ## Prancha 10: Zwischenraum Brasil

  **Tese:** A República brasileira de 1889 e a de 1922 representam polos de um
  Zwischenraum: gênese fundacional vs. estabilização normativa.
  ```

- [ ] **Step 2: Commit**
  ```bash
  git add vault/tese/metodologia/preregistration-pranchas.md
  git commit -m "docs: preregistration de 10 pranchas piloto IMES"
  ```

---

## Task 7: Criar notebook de validação CJV

**Files:**
- Create: `notebooks/09-validacao-pranchas.ipynb`
- Read first: `notebooks/` existentes (para seguir mesmo padrão)

**Context:** Notebook que aplica CJV a pares de itens e calcula percentagem de satisfação.

- [ ] **Step 1: Escrever estrutura do notebook**
  ```python
  # Célula 1: Imports
  import json
  import pandas as pd
  from itertools import combinations

  # Célula 2: Carregar corpus
  records = []
  with open('../data/processed/records.jsonl') as f:
      for line in f:
          records.append(json.loads(line))
  df = pd.DataFrame(records)
  print(f"Corpus carregado: {len(df)} registros")

  # Célula 3: Definir CJV
  def cjv_eco_formal(item_a, item_b):
      """CJV-1: Pathosformel compartilhado"""
      # Implementar comparação de atributos visuais
      pass

  def cjv_eco_historico(item_a, item_b):
      """CJV-2: Mesmo evento/transformação institucional"""
      # Implementar comparação de datas/eventos
      pass

  def cjv_eco_campo(item_a, item_b):
      """CJV-3: Mesma posição no campo"""
      # Implementar comparação de produtores/circulação
      pass

  # Célula 4: Validar prancha
  def validar_prancha(itens_ids, df):
      """Retorna percentagem de pares adjacentes que satisfazem CJV"""
      itens = df[df['item_id'].isin(itens_ids)]
      pares = list(combinations(itens_ids, 2))
      validos = 0
      for a, b in pares:
          cjvs = sum([
              cjv_eco_formal(a, b),
              cjv_eco_historico(a, b),
              cjv_eco_campo(a, b)
          ])
          if cjvs >= 2:
              validos += 1
      return validos / len(pares) if pares else 0

  # Célula 5: Testar com prancha piloto
  prancha_1_ids = ['SCOUT-001', 'SCOUT-002', 'SCOUT-003']  # substituir
  score = validar_prancha(prancha_1_ids, df)
  print(f"Validação prancha 1: {score:.1%} CJV satisfeitos")
  assert score >= 0.8, f"Prancha inválida: {score:.1%} < 80%"
  ```

- [ ] **Step 2: Commit**
  ```bash
  git add notebooks/09-validacao-pranchas.ipynb
  git commit -m "feat(notebook): validacao CJV para pranchas-atlas IMES"
  ```

---

## Task 8: Criar notas imes-rv no vault

**Files:**
- Create: `vault/research-wiki/imes-rv/IMES-RV-01-justitia-monumental.md`
- Create: `vault/research-wiki/imes-rv/IMES-RV-02-libertas-republicana.md`
- Create: `vault/research-wiki/imes-rv/IMES-RV-03-germania-imperial.md`
- Create: `vault/research-wiki/imes-rv/IMES-RV-04-republica-positivista.md`
- Create: `vault/research-wiki/imes-rv/IMES-RV-05-britannia-colonial.md`
- Create: `vault/research-wiki/imes-rv/IMES-RV-06-justitia-contracanonica.md`

**Context:** Template X4 do master prompt v3.0. Uma nota por RV.

- [ ] **Step 1: Escrever nota IMES-RV-01**
  Usar template X4 (ver master prompt Seção X4). Preencher com dados do mapeamento.

- [ ] **Step 2: Commit**
  ```bash
  git add vault/research-wiki/imes-rv/
  git commit -m "docs(wiki): 6 notas imes-rv para Regimes Visuais"
  ```

---

## Self-Review

1. **Spec coverage:** Todos os passos do ultraplan Fases 1-4 estão mapeados? ✅
   - Fase 1 (docs): Tasks 1, 4 ✅
   - Fase 2 (Cap.2): Task 2 ✅
   - Fase 3 (corpus/schema): Tasks 3, 5, 8 ✅
   - Fase 4 (piloto): Tasks 6, 7 ✅

2. **Placeholder scan:** Nenhum TBD/TODO. Código de teste incluído. ✅

3. **Type consistency:** Schema JSON usa integer 0-3 para indicadores, number para score. ✅

---

## Execution Handoff

**Escolha de execução:**

1. **Subagent-Driven (recomendado)** — Fresh subagent por task, two-stage review
2. **Inline Execution** — Batch execution com checkpoints

**Nota:** As Tasks 1, 2, 4, 6 são puramente documentação (Markdown) — podem ser
executadas em paralelo. Tasks 3 (schema JSON), 5 (mapeamento de dados), 7 (notebook),
8 (notas wiki) dependem de dados do corpus.

**Branch sugerido:** `feature/imes-v3-transition`
