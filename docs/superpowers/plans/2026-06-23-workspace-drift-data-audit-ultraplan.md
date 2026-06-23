# Workspace Drift + Data Pipeline Audit — Ultraplan

Data: 2026-06-23
Escopo: `/Users/ana/Research` + `/Users/ana/Research/hub/iconocracy-corpus`
Estratégia: auditoria em ondas para separar topologia/drift, contratos de dados, pipeline IMES e planos acadêmicos sem sobreposição.
Lentes: architecture/drift, data-pipeline, academic-planning
Produto final: dossiê de auditoria com achados priorizados, matriz de dependências e plano posterior de remediação.
Modo: planejamento apenas — nenhuma mutação em código, schemas, corpus ou manuscrito durante a auditoria.

## Ground Truth (reconhecimento realizado 2026-06-23)

### Raiz e paths resolvidos

```text
DATE: 2026-06-23
ROOT: /Users/ana/Research -> /Users/ana/Research
ICON: /Users/ana/Research/hub/iconocracy-corpus -> /Users/ana/Research/hub/iconocracy-corpus
```

### Tamanhos por bucket principal

```text
2.0G  /Users/ana/Research/hub
1.5G  /Users/ana/Research/GitHub
1.4G  /Users/ana/Research/apps
1.2G  /Users/ana/Research/scitex-python
1.1G  /Users/ana/Research/hermes-workspace
1.1G  /Users/ana/Research/Tools
873M  /Users/ana/Research/archive
439M  /Users/ana/Research/ml-intern
394M  /Users/ana/Research/labs
266M  /Users/ana/Research/shared
216M  /Users/ana/Research/hermes-agent
148K  /Users/ana/Research/plans
```

### Repos independentes encontrados (amostra relevante)

```text
/Users/ana/Research
/Users/ana/Research/apps/atlaslab
/Users/ana/Research/apps/iconocracia-companion
/Users/ana/Research/apps/iconocracia-research
/Users/ana/Research/apps/iconocracia-space
/Users/ana/Research/apps/pat.archive
/Users/ana/Research/hermes-agent
/Users/ana/Research/hermes-workspace
/Users/ana/Research/hub/iconocracy-corpus
/Users/ana/Research/hub/iconocracy-corpus-pr85-fix
/Users/ana/Research/labs/browser-harness
/Users/ana/Research/labs/iurisvision
/Users/ana/Research/shared/iconclass-data
/Users/ana/Research/shared/iconclass-data-avmadrj
/Users/ana/Research/vida-os
```

### Symlinks / topologia especial

```text
/Users/ana/Research/iconocracy-corpus -> /Volumes/data/projetos/research/hub/iconocracy-corpus
/Users/ana/Research/iconocracia-companion -> /users/ana/Research/apps/iconocracia-companion
/Users/ana/Research/hub/iconocracy-corpus/ROADMAP.md -> docs/ROADMAP-2026-04-29.md
/Users/ana/Research/labs/iuris-visio-roadmap/iuris-visio-roadmap -> /Users/ana/Research/labs/iuris-visio-roadmap
/Users/ana/Research/apps/iconocracia-space/iconocracia-space -> /Users/ana/Research/apps/iconocracia-space
/Users/ana/Research/shared/iconclass-data/iconclass-data -> /Users/ana/Research/shared/iconclass-data
/Users/ana/Research/shared/iconclass-data-avmadrj/iconclass-data-avmadrj -> /Users/ana/Research/shared/iconclass-data-avmadrj
```

### Estado git do sub-repo ICONOCRACY

```text
branch: feat/codebook-master-v2.2.0
head: 86e4cce feat(schema): consolidate LPAI codebook master v2.2.0

worktrees:
/Users/ana/Research/hub/iconocracy-corpus                                      [feat/codebook-master-v2.2.0]
/Users/ana/.codex/worktrees/34b4/iconocracy-corpus                             detached HEAD
/Users/ana/.codex/worktrees/7bca/iconocracy-corpus                             detached HEAD
/Users/ana/.codex/worktrees/e9db/iconocracy-corpus                             [claude/setup-thesis-corpus-e346H]
/Users/ana/copilot-worktrees/iconocracy-corpus/anavvanzin-miniature-eureka     [anavvanzin-release-gate-remediation]
/Users/ana/copilot-worktrees/iconocracy-corpus/anavvanzin-refactored-memory    [anavvanzin-orchestration-setup]
/Users/ana/copilot-worktrees/iconocracy-corpus/research-workspace-map          [research/workspace-map]
/Users/ana/Research/hub/iconocracy-corpus-pr85-fix                             detached HEAD
/Users/ana/Research/hub/iconocracy-corpus/.claude/worktrees/e1-fable5-recode   [worktree-e1-fable5-recode]
/Users/ana/Research/hub/iconocracy-corpus/.claude/worktrees/research-permanent [research/permanent]

status short:
?? .planning/config.json
?? ROADMAP.md
```

### Estado de planos no repo meta `Research`

```text
?? plans/2026-07-01-july-plan.md
?? plans/2026-07-06-biweekly-imes-pranchas.md
```

### Contagens de dados atuais no branch ativo

```text
corpus/corpus-data.json: 278 items
data/processed/pathosformel_index.jsonl: 265 items
data/processed/regimes_visuais.yaml: exists
corpus/records.jsonl: MISSING
```

Diagnóstico estrutural de contagem:

```text
corpus type: list
corpus len: 278
pathos len: 265
id overlap by naive id/url key: 0
corpus_only: 278
pathos_only: 265
```

Interpretação preliminar: a comparação ingênua por `id`/`url` não funciona porque `pathosformel_index.jsonl` usa outro contrato de identificação ou outro campo-chave. A auditoria deve descobrir o join correto antes de concluir “13 gaps”.

### Histograma de extensões em `/Users/ana/Research` (pruned)

```text
files_scanned: 56203
.md: 19271
.json: 11907
.py: 6245
.log: 2374
.png: 2046
.ts: 2042
.js: 1000
.tsx: 877
.yaml: 661
.pdf: 510
.csv: 368
.yml: 262
.sh: 260
.docx: 193
.jsonl: 144
```

### Governança carregada

- `/Users/ana/Research/AGENTS.md`: meta-workspace, sub-repos isolados; não rodar build/test/lint na raiz; planos thesis devem viver em `~/Research/plans/`; sub-repos têm `.git` próprio.
- `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md`: fonte autoritativa do sub-repo; canonical data hierarchy: `data/processed/records.jsonl` > `corpus/corpus-data.json` > `data/processed/purification.jsonl`; Known Data Issues já documenta 278/278 e análise antiga N=165.
- `/Users/ana/Research/hub/iconocracy-corpus/AGENTS.md`: quick brief está defasado, ainda registra counts 2026-05-24 (265/264/264/314). Deve ser tratado como drift documentado, não como verdade operacional.

## Premissas

1. A auditoria é read-only, exceto pelos relatórios markdown que serão gravados em `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/` se Ana aprovar execução.
2. Nenhum subagente deve editar corpus, schemas, scripts, capítulos, planos ou arquivos de config.
3. O branch ativo do sub-repo é `feat/codebook-master-v2.2.0`; qualquer achado deve registrar branch e path exato.
4. `CLAUDE.md` do sub-repo vence `AGENTS.md` quando houver divergência de contagens, pois `AGENTS.md` está explicitamente mais antigo.
5. A comparação entre `corpus-data.json` e `pathosformel_index.jsonl` exige descobrir o contrato real de join; a ausência de overlap ingênuo é achado, não prova de ausência de pathosformel.
6. Os planos em `~/Research/plans/` estão atualmente untracked no repo meta; isso deve ser auditado antes de commit/push.
7. Caches e worktrees devem ser mapeados, mas não varridos como se fossem fontes canônicas.
8. Diretórios excluídos da varredura profunda: `.git`, `node_modules`, `.venv`, `dist`, `build`, `.next`, `.opencode`, `.claude/worktrees` salvo quando explicitamente analisados como worktrees.

## Riscos conhecidos e mitigações

| Risco | Mitigação |
|---|---|
| Subagentes duplicarem achados de drift | Escopos por path sem sobreposição; cada agente recebe lista fechada de paths. |
| Confundir worktree com fonte canônica | Todo relatório deve declarar branch/path; worktrees só entram na lente de topologia. |
| Concluir “gaps” por join errado | Agente de dados deve primeiro mapear campos-chave e provar join correto. |
| Reintroduzir contagens obsoletas nos planos | Agente de planos deve comparar `CLAUDE.md`, planos e dados vivos; default: dado vivo vence plano. |
| Escrever relatórios em sessão isolada e o pai não ver | Cada subagente deve retornar o markdown completo no resumo e salvar em path explícito. |
| Glob lento ou varredura enorme | Subagentes recebem paths explícitos; proibido varrer `/Users/ana/Research` inteiro salvo agente de topologia. |
| Alterar corpus acidentalmente | Contexto de cada subagente declara: read-only, não usar patch/write exceto relatório. |
| Git status já contém arquivos untracked | Não stagear nada durante auditoria; síntese deve listar estado preexistente. |
| `AGENTS.md` stale induzir conclusão errada | Relatório deve marcar `AGENTS.md` como artefato auditado com data e conflito, não fonte final. |

## Schema de Relatório (TODO subagente retorna neste formato)

```markdown
# Audit Report — <domain> — <agent lens>
Escopo examinado: <paths>
Arquivos analisados: N
Data: 2026-06-23

## Resumo executivo (≤5 linhas)

## Achados — CRITICAL (bloqueante)
- [C-01] <título> · `<path>:<linha>` · <diagnóstico> · <remediação>

## Achados — MAJOR
- [M-01] ...

## Achados — MINOR
- [m-01] ...

## Pontos fortes (o que NÃO mexer)

## Métricas mensuradas
- métrica: valor

## Dependências inter-domínio
- <achado> depende de / conflita com <outro domínio>

## Recomendações priorizadas (top 5)
```

Instrução fixa para cada subagente:

> Return value must follow this schema verbatim. Save it to the requested path AND return the full markdown in your summary. Do not modify source files. Only write the report file if explicitly instructed; otherwise return report only.

## WAVE 1 — Reconhecimento especializado (4 agentes, executar em dois lotes por limite de concorrência)

### Agent 1.1 — Architecture / topology / drift

Escopo:
- `/Users/ana/Research/AGENTS.md`
- `/Users/ana/Research/CLAUDE.md`
- `/Users/ana/Research/README.md`
- `/Users/ana/Research/iconocracy-corpus` symlink
- `/Users/ana/Research/hub/iconocracy-corpus`
- `git worktree list` output do sub-repo
- paths de worktrees listados no Ground Truth, sem varredura profunda de conteúdo

Goal:
1. Mapear topologia real: raiz meta, sub-repo canônico, symlink externo, worktrees Claude/Codex/Copilot.
2. Identificar documentos de governança stale ou conflitantes (`AGENTS.md` vs `CLAUDE.md`).
3. Identificar riscos de path drift (`/Volumes/data/...`, `/users/ana/...`, self-symlinks).
4. Distinguir fonte canônica, clones/espelhos, worktrees e backups.
5. Propor mapa “fonte de verdade” para agentes futuros.

Toolsets: terminal, file, search.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/01-architecture-topology.md`

### Agent 1.2 — Data contracts / schemas / counts

Escopo:
- `/Users/ana/Research/hub/iconocracy-corpus/data/processed/`
- `/Users/ana/Research/hub/iconocracy-corpus/corpus/corpus-data.json`
- `/Users/ana/Research/hub/iconocracy-corpus/schema/`
- `/Users/ana/Research/hub/iconocracy-corpus/schemas/`
- `/Users/ana/Research/hub/iconocracy-corpus/tools/schemas/`
- `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/validate_schemas.py`
- `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/records_to_corpus.py`

Goal:
1. Medir contagens reais: records, corpus export, purification, pathosformel, regimes_visuais.
2. Descobrir o contrato de join correto entre `corpus-data.json` e `pathosformel_index.jsonl`.
3. Verificar se `regimes_visuais.yaml` existe, qual schema implícito usa e se é derivado ou canônico.
4. Identificar JSON/YAML consumidos por múltiplos scripts sem schema explícito.
5. Listar comandos de validação existentes e lacunas de CI.

Toolsets: terminal, file, search.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/02-data-contracts.md`

### Agent 1.3 — IMES / pipeline readiness

Escopo:
- `/Users/ana/Research/hub/iconocracy-corpus/data/processed/pathosformel_index.jsonl`
- `/Users/ana/Research/hub/iconocracy-corpus/data/processed/regimes_visuais.yaml`
- `/Users/ana/Research/hub/iconocracy-corpus/docs/decisions/`
- `/Users/ana/Research/hub/iconocracy-corpus/docs/pilots/`
- `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/`
- `/Users/ana/Research/hub/iconocracy-corpus/notebooks/`

Goal:
1. Verificar se E1, E2, E3 existem de fato e em que estado.
2. Confirmar se `cluster_rv.py` existe ou se E2 usa outro script/nome.
3. Identificar outputs derivados já presentes mas não refletidos nos planos.
4. Mapear dependências para produzir pranchas E3.
5. Separar “necessário para julho” de “melhoria técnica posterior”.

Toolsets: terminal, file, search.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/03-imes-pipeline-readiness.md`

### Agent 1.4 — Academic plans / manuscript consistency

Escopo:
- `/Users/ana/Research/plans/2026-07-01-july-plan.md`
- `/Users/ana/Research/plans/2026-07-06-biweekly-imes-pranchas.md`
- `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/`
- `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/`
- `/Users/ana/Research/hub/iconocracy-corpus/docs/plans/`
- `/Users/ana/Research/hub/iconocracy-corpus/docs/research/elicit/`

Goal:
1. Verificar se planos atualizados refletem o estado real após Cap.1 consolidado.
2. Medir word counts dos capítulos relevantes com método consistente.
3. Identificar números obsoletos no manuscrito (N=145, 165, 265, 278, 280) e classificá-los por risco.
4. Verificar se Elicit/resultados e plano do dia foram incorporados sem colidir com plano mensal.
5. Propor correções de plano sem editar os arquivos.

Toolsets: terminal, file, search.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/04-academic-plans-manuscript.md`

## WAVE 2 — Verificação cruzada e lacunas (2 agentes)

Executar somente depois de ler os 4 relatórios Wave 1.

### Agent 2.1 — Count reconciliation / source-of-truth matrix

Escopo:
- Relatórios Wave 1.1, 1.2, 1.3, 1.4
- `CLAUDE.md`
- dados vivos contados na Wave 1

Goal:
1. Produzir matriz única de contagens: documento, arquivo, comando, resultado, data, status.
2. Identificar quais números podem aparecer em planos/manuscrito e quais devem ser proibidos.
3. Propor linguagem-padrão para “analytic N” vs “operational corpus N”.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/05-count-reconciliation.md`

### Agent 2.2 — Execution readiness / July feasibility

Escopo:
- Relatórios Wave 1
- Planos julho/biweekly
- Estado pipeline IMES

Goal:
1. Testar se o plano biweekly é executável com os arquivos existentes.
2. Marcar passos que dependem de scripts inexistentes, dados sem join ou imagens ausentes.
3. Propor versão “mínima executável” da primeira semana de julho.

Saída esperada:
- `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/06-july-readiness.md`

## WAVE 3 — Síntese (orquestrador, NÃO subagente)

O agente pai deve:

1. Ler todos os relatórios Wave 1 e Wave 2 em disco.
2. Verificar pelo menos 3 achados críticos diretamente com ferramentas (`read_file`, `terminal`, `search_files`).
3. Produzir `00-synthesis.md` com:
   - top 10 achados cross-domain;
   - matriz de dependências;
   - “não mexer” / pontos fortes;
   - roadmap de remediação em 2 sprints;
   - decisões que exigem Ana.
4. Produzir um segundo plano separado de remediação, somente se Ana pedir execução.

## Caminhos de arquivos que serão criados

```text
docs/superpowers/plans/
  2026-06-23-workspace-drift-data-audit-ultraplan.md

docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/
  00-synthesis.md
  01-architecture-topology.md
  02-data-contracts.md
  03-imes-pipeline-readiness.md
  04-academic-plans-manuscript.md
  05-count-reconciliation.md
  06-july-readiness.md
```

## Métricas de sucesso

- Reconhecimento e plano não alteram nenhum artefato além do ultraplan.
- Wave 1 completa em dois lotes de subagentes, sem overlap de paths.
- 100% dos relatórios seguem o schema de relatório.
- Nenhum achado “gap de dados” é aceito sem provar o campo de join.
- Síntese final distingue claramente:
  - corpus operacional;
  - analytic N;
  - export público;
  - outputs derivados;
  - planos.
- Roadmap de remediação não mistura auditoria com fix.

## Open questions / decisões do usuário

1. **Lente padrão escolhida por falta de resposta:** architecture/drift + data-pipeline. Default: seguir com essa lente, não full 360°.
2. **Relatórios em disco:** salvar em `docs/superpowers/audits/2026-06-23-workspace-drift-data-audit/`. Default: sim, se Ana aprovar execução.
3. **Incluir apps/frontend na auditoria?** Default: não nesta rodada; apps ficam fora salvo se afetarem corpus export.
4. **Tratar `AGENTS.md` stale como correção posterior?** Default: auditar e recomendar, não editar nesta fase.
5. **Executar Wave 1 agora?** Default: não; aguardar “executa” explícito.
