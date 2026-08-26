# Sprint 1 — Plano de Execução Concreto

Data: 2026-04-10
Baseado em: `docs/roadmaps/2026-04-10-roadmap-geral-iconocracy.md`
Objetivo da sprint: pôr ordem no ecossistema imediato do monorepo antes de ampliar capacidades.

---

## 1. Resultado esperado da sprint

Ao final desta sprint, o repositório deve ter:

1. uma separação clara entre artefatos canônicos, experimentais, derivados de sessão e superfícies públicas
2. uma leitura consistente do working tree atual
3. documentação operacional atualizada para refletir o estado real do projeto
4. um critério explícito para decidir o destino de novos scripts, dashboards, notas e páginas auxiliares
5. uma base limpa para começar a Sprint 2 (expansão do ledger central)

---

## 2. Critério de classificação de artefatos

Toda decisão nesta sprint deve usar estes quatro estados:

### A. Canônico

Entra no fluxo operacional principal do projeto.

Critérios:
- altera ou sustenta o pipeline central do corpus
- participa da ordem de verdade (`records.jsonl`, `corpus-data.json`, `purification.jsonl`, `vault`)
- tem uso recorrente e regra clara de manutenção
- pode ser documentado em `docs/scripts.md`, `AGENTS.md` ou `README.md`

Exemplos típicos:
- `tools/scripts/validate_schemas.py`
- `tools/scripts/vault_sync.py`
- `tools/scripts/records_to_corpus.py`

### B. Experimental

É promissor, mas ainda não deve ser tratado como parte do núcleo.

Critérios:
- ainda está em prova de conceito
- tem escopo incerto ou depende de validação metodológica
- pode mudar rapidamente
- ainda não deve alterar superfícies públicas sem curadoria

Destino preferencial:
- pasta explícita de experimento, ou documentação como protótipo

### C. Derivado de sessão

É produto de uma sessão de trabalho, não componente estrutural do sistema.

Critérios:
- notas temporais
- rascunhos operacionais
- relatórios datados
- saídas intermediárias de agente
- material que preserva histórico intelectual, mas não deve governar o pipeline

Destino preferencial:
- `vault/sessoes/`
- `vault/tese/ideias/`
- `docs/notes/` ou área equivalente, se necessário
- nunca misturar com contrato canônico por acidente

### D. Release-only / superfície pública

Existe para consumo público, visualização ou publicação.

Critérios:
- explorer
- dashboard
- companion pages
- superfícies estáticas de apresentação
- artefatos que dependem do corpus já congelado ou exportado

Regra:
- não podem se tornar fonte da verdade
- devem depender do pipeline canônico, não substituí-lo

---

## 3. Escopo concreto da Sprint 1

### 3.1 Diretórios e superfícies a auditar

#### Núcleo operacional
- `tools/scripts/`
- `data/processed/`
- `corpus/`
- `iconocracy-ingest/`
- `vault/`
- `docs/`
- `deploy/iconocracia-companion/`

#### Working tree atual que precisa de decisão
- `analyze_corpus.py`
- `corpus/DASHBOARD_AGENTS.html`
- `corpus/agent-runs.json`
- `data/processed/parallel_results.json`
- `deploy/iconocracia-companion/public/agents.html`
- `deploy/iconocracia-companion/public/analytics.html`
- `notebooks/01_exploratory/`
- `tmp/endurecimento_summary.py`
- `tools/scripts/gallica_discovery.py`
- `tools/scripts/log_agent_run.py`
- `tools/scripts/mcp_integration.py`
- `tools/scripts/refresh_dashboard.py`
- novos arquivos em `vault/candidatos/`
- novos arquivos em `vault/sessoes/`
- novos arquivos em `vault/tese/ideias/`
- novos arquivos em `vault/corpus/`

---

## 4. Decisões-alvo por área

## A. `tools/scripts/`

### Objetivo
Separar scripts canônicos de scripts em incubação.

### Arquivos que exigem decisão imediata
- `gallica_discovery.py`
- `log_agent_run.py`
- `mcp_integration.py`
- `refresh_dashboard.py`

### Perguntas de decisão
Para cada script, responder:
1. ele altera o pipeline central do corpus?
2. ele é reexecutável e previsível?
3. tem input/output bem definidos?
4. merece documentação em `docs/scripts.md`?
5. depende de infraestrutura ainda instável?

### Regras de destino
- se “sim” para uso recorrente + previsibilidade -> canônico
- se ainda for prova de conceito -> experimental
- se for utilitário de sessão pontual -> derivado / mover para `tmp/` ou área de notes

### Entrega da área
- tabela final “script -> estado -> destino -> owner lógico -> documentação exigida”

---

## B. `corpus/` e dashboards

### Objetivo
Separar export canônico de superfícies de visualização.

### Arquivos a rever
- `corpus/DASHBOARD_CORPUS.html`
- `corpus/DASHBOARD_AGENTS.html`
- `corpus/index.html`
- `corpus/atlas-iconometrico.html`
- `corpus/agent-runs.json`

### Decisão esperada
- `corpus-data.json` continua sendo o export canônico público
- dashboards devem ser classificados como superfícies derivadas ou release-only
- `DASHBOARD_AGENTS.html` e `agent-runs.json` precisam de contrato explícito

### Perguntas de decisão
1. este dashboard é interno, público, ou ambos?
2. sua fonte de dados é canônica ou transitória?
3. ele pertence a `corpus/` ou a `deploy/`?
4. ele precisa existir no repositório principal ou pode ser gerado?

### Entrega da área
- matriz “artefato visual -> interno / público / derivado / release-only”

---

## C. `deploy/iconocracia-companion/`

### Objetivo
Definir o papel dessa superfície em relação a `corpus/` e Hugging Face.

### Arquivos a rever
- `deploy/iconocracia-companion/public/index.html`
- `deploy/iconocracia-companion/public/agents.html`
- `deploy/iconocracia-companion/public/analytics.html`

### Decisão esperada
- companion = superfície pública derivada, nunca fonte
- páginas novas precisam de contrato de uso
- distinguir claramente explorer público de dashboard interno

### Entrega da área
- definição documental do papel do companion
- origem dos dados de cada página

---

## D. `vault/`

### Objetivo
Separar espelho canônico, sessão, narrativa, ideia e escrita.

### Áreas que exigem revisão
- `vault/candidatos/`
- `vault/sessoes/`
- `vault/corpus/`
- `vault/tese/ideias/`
- `vault/tese/rascunhos-artigos/`
- `vault/_templates/`

### Decisão esperada
1. `vault/candidatos/` continua espelho operacional de catalogação
2. `vault/sessoes/` guarda histórico datado de trabalho
3. `vault/tese/ideias/` guarda sínteses e sublações conceituais, não registros canônicos do corpus
4. `vault/corpus/` precisa de papel mais explícito: planejamento/coordenação ou camada narrativa
5. templates novos devem ser classificados como canônicos ou experimentais

### Regra crítica
Nenhuma nota do vault deve virar fonte soberana por acidente.
Se um conteúdo precisa entrar no pipeline, deve ser puxado/sincronizado por script explícito.

### Entrega da área
- mapa de função de cada subdiretório do vault
- convenção curta de nomes e papéis

---

## E. `docs/`

### Objetivo
Atualizar a documentação para espelhar o estado real do sistema.

### Arquivos obrigatórios da sprint
- `README.md`
- `docs/scripts.md`
- `AGENTS.md`
- `docs/OPERATING_MODEL.md`

### Atualizações esperadas
#### `README.md`
- refletir superfícies atuais e novos componentes reais
- explicitar melhor a diferença entre corpus/export/dashboard/companion/vault

#### `docs/scripts.md`
- incluir apenas scripts canonizados
- marcar scripts experimentais como tal ou excluí-los da lista principal

#### `AGENTS.md`
- alinhar atalhos com o estado real do repositório
- registrar melhor os guardrails sobre artefatos derivados

#### `docs/OPERATING_MODEL.md`
- adicionar a taxonomia de estados de artefato
- reforçar relação entre home/laboratório e monorepo/canônico, se for conveniente por remissão

### Entrega da área
- documentação mínima consistente com o estado do repo pós-auditoria

---

## 5. Sequência de execução recomendada

### Etapa 1 — Inventário e classificação

Objetivo:
produzir uma lista fechada dos artefatos novos/recentes e classificá-los.

Ações:
1. gerar inventário do working tree atual
2. listar scripts novos e arquivos novos por diretório
3. atribuir um rótulo provisório a cada item:
   - canônico
   - experimental
   - derivado de sessão
   - release-only

Saída esperada:
- tabela mestra de triagem

### Etapa 2 — Decidir destino físico

Objetivo:
transformar classificação em topologia real.

Ações:
1. confirmar o que permanece onde está
2. mover o que estiver em local errado
3. criar, se necessário, uma área explícita para experimentos ou notas operacionais
4. remover ambiguidade entre `corpus/` e `deploy/`

Saída esperada:
- diretórios com função mais nítida

### Etapa 3 — Canonizar o que for core

Objetivo:
incorporar ao sistema apenas o que já tem contrato estável.

Ações:
1. documentar scripts aprovados
2. documentar superfícies aprovadas
3. registrar inputs/outputs e dependências dos novos componentes canonizados

Saída esperada:
- `docs/scripts.md` e docs correlatas atualizadas

### Etapa 4 — Encapsular o que ainda é laboratório

Objetivo:
evitar mistura entre protótipo e núcleo.

Ações:
1. marcar protótipos como experimentais
2. documentar condições para futura promoção ao core
3. garantir que não interfiram na ordem de verdade

Saída esperada:
- experimentos claramente isolados e sem ambiguidade epistemológica

### Etapa 5 — Revisão documental final

Objetivo:
fechar a sprint com o repositório legível para humanos e agentes.

Ações:
1. revisar `README.md`
2. revisar `AGENTS.md`
3. revisar `docs/OPERATING_MODEL.md`
4. revisar `docs/scripts.md`
5. adicionar uma nota curta de decisão em `docs/roadmaps/` ou ADR, se necessário

Saída esperada:
- repositório navegável e inteligível

---

## 6. Tabela inicial de triagem sugerida

Esta tabela é proposição inicial, não decisão final.

| Artefato | Classificação inicial sugerida | Ação inicial sugerida |
|---|---|---|
| `tools/scripts/gallica_discovery.py` | experimental -> candidato a canônico | auditar interface e decidir se entra no fluxo SCOUT |
| `tools/scripts/log_agent_run.py` | experimental/derivado | definir se é telemetria canônica ou log auxiliar |
| `tools/scripts/mcp_integration.py` | experimental | manter fora do core até contrato claro |
| `tools/scripts/refresh_dashboard.py` | candidato a canônico | auditar se vira parte oficial do pipeline visual |
| `corpus/DASHBOARD_AGENTS.html` | derivado/release-only | decidir se é dashboard interno ou público |
| `corpus/agent-runs.json` | derivado | não tratar como dado canônico do corpus |
| `deploy/iconocracia-companion/public/agents.html` | release-only | manter como superfície pública derivada |
| `deploy/iconocracia-companion/public/analytics.html` | release-only | manter como superfície pública derivada |
| `notebooks/01_exploratory/` | experimental | manter como análise exploratória, sem papel canônico |
| `tmp/endurecimento_summary.py` | derivado/temporário | mover, promover ou remover |
| `vault/candidatos/SCOUT-*` novos | canônico-vault-espelho | sincronizar com cuidado e validar papel |
| `vault/sessoes/SCOUT-SESSION-*` | derivado de sessão | manter como histórico, não fonte |
| `vault/tese/ideias/*` | derivado intelectual | manter fora do ledger do corpus |
| `vault/corpus/*` | ambíguo | definir papel documental exato |

---

## 7. Critérios de pronto da Sprint 1

A sprint só termina quando:

1. cada artefato novo relevante tiver classificação e destino explícitos
2. scripts canônicos estiverem distinguidos de scripts experimentais
3. superfícies públicas estiverem distinguidas de superfícies internas
4. o vault estiver com papéis internos mais claros
5. a documentação central estiver coerente com o estado real do repo
6. ficar preparado o terreno para a Sprint 2 sem ambiguidade estrutural

---

## 8. Próximo passo após esta sprint

Depois da Sprint 1, iniciar imediatamente a Sprint 2:

**Fortalecer o ledger central (`records.jsonl`)** com novos blocos auxiliares bem separados, incluindo:
- `clip_assist`
- `ocr_extract`
- `audit_flags`
- `nearest_neighbors`
- `evidence_status`

Mas isso só deve começar quando a topologia do repositório estiver realmente estabilizada.

---

## 9. Proposta de execução prática imediata

Se a Sprint 1 for executada agora, a ordem ideal é:

1. auditar `tools/scripts/`
2. auditar `corpus/` + `deploy/`
3. auditar `vault/`
4. revisar `docs/`
5. consolidar decisões em um documento curto de fechamento da sprint

Essa sequência minimiza retrabalho, porque primeiro define infraestrutura, depois superfícies, depois documentação.
