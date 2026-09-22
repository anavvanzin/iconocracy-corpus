# 🔬 ICONOCRACY 360° — Wave 1.1: Git Topology Audit

**Data:** 2026-06-26
**Repo:** `anavvanzin/iconocracy-corpus` · Branch atual: `main` (826d8dd)
**Escopo:** Classificação de 35 branches locais + 24 remotos + 15 worktrees

---

## 📊 Resumo executivo

| Métrica | Valor |
|---|---|
| Branches locais totais | 35 |
| Branches remotos (origin) | 24 |
| Worktrees ativos | 15 (11 named + 3 detached + 1 main) |
| Branches merged em `main` | 9 |
| Branches unmerged | 25 (excluindo main) |
| PRs abertos no GitHub | 6 |
| Branches com PR aberto | 3 locais + 3 remote-only |
| Branches órfãos remotos | 11 (existem em origin, NÃO localmente) |
| Branches locais sem remote | 19 |

---

## 🚨 CRITICAL

### CRIT-1: 3 worktrees em detached HEAD — risco de perda de trabalho

Três worktrees estão em detached HEAD sem branch nomeada associada. Commits podem ser perdidos se o worktree for removido:

| Worktree Path | Commit | Alcancável por |
|---|---|---|
| `/Users/ana/.codex/worktrees/34b4/iconocracy-corpus` | `41516a9` | **NENHUMA branch** ⚠️ |
| `/Users/ana/.codex/worktrees/7bca/iconocracy-corpus` | `2487699` | `data/reacquire-images-batch2-iiif-20260609` |
| `/Users/ana/Research/hub/iconocracy-corpus-pr85-fix` | `5db68b7` | `claude/fervent-meitner-u7lvik` |

**Ação:** O worktree 34b4 (commit `41516a9`: "docs(tese): clarify analytical N by instrument stratum") é **órfão total** — não pertence a nenhuma branch. Resgatar com `git branch rescue/detached-34b4 41516a9` IMEDIATAMENTE.

### CRIT-2: 11 branches remotos órfãos — lixo acumulado no origin

Branches que existem em `origin` mas NÃO localmente. 3 deles têm PRs abertos (bloqueiam remoção):

| Branch remoto | PR | Estado |
|---|---|---|
| `claude/awesome-hawking-41owe1` | #82 | **ABERTO** |
| `claude/thesis-glossary-h8lno4` | #108 | **ABERTO** |
| `rescue/ssd-pipeline-v2-20260611` | #79 | **ABERTO** |
| `copilot/create-implementation-plan` | — | órfão |
| `copilot/fix-irregularities-in-data` | — | órfão |
| `copilot/review-session-history` | — | órfão |
| `dialectic-cycle-1` | — | órfão |
| `docs/prp-plans-2026-06` | — | órfão |
| `fix/protobufjs-7.5.6` | — | órfão |
| `iconocracy-research-materials-2026-04-25` | — | órfão |
| `iconocracy-research-materials-clean` | #44 | CLOSED |

**Ação:** 8 branches podem ser removidos do remote imediatamente. Os 3 com PR aberto exigem merge/fechamento primeiro.

---

## 🔴 MAJOR

### MAJ-1: 19 branches locais sem contraparte remota — risco de perda

Branches que existem apenas localmente (nunca fizeram push). Sem backup no GitHub, `git gc` ou falha de disco = perda permanente:

| Branch | Classificação | Ahead/Behind |
|---|---|---|
| `add-claude-github-actions-1775789759242` | 🗑️ safe-delete | +2/−594 |
| `anavvanzin-orchestration-setup` | 📦 worktree | 0/−99 |
| `anavvanzin-release-gate-remediation` | 📦 worktree | 0/−98 |
| `ci/fix-crda-permissions` | 🗑️ safe-delete | 0/−456 |
| `claude/decide-next-steps-v2mE3` | 🗑️ safe-delete | 0/−55 |
| `codex/local-work-pr107-followup` | 🔍 verify-first | +1/−2 |
| `consolidate/2026-06-19-audit-ssot` | 🔍 verify-first | +1/−105 |
| `copilot/add-csv-json-export-analytics-dashboard` | 🗑️ safe-delete | +2/−588 |
| `copilot/migrate-worker-routing-to-hono` | 🔍 verify-first | +3/−51 |
| `docs/reliability-audit-2026-06-19` | 🔍 verify-first | +1/−103 |
| `docs/ssot-methodology-2026-06-19` | 🔍 verify-first | +18/−123 |
| `e1-opus48-batch-2026-06-22` | 🚫 protected | +9/−99 |
| `e1-opus48-promote-2026-06-22` | 🚫 protected | +2/−91 |
| `feat/codebook-master-v2.2.0` | 🔍 verify-first | +1/−67 |
| `feature/imes-v3-transition` | 🔍 verify-first | +4/−463 |
| `pr-33-sync` | 🗑️ safe-delete | 0/−196 |
| `pr-research-materials-v2` | 🗑️ safe-delete | 0/−167 |
| `pr/76/data/reacquire-images-batch2-iiif-20260609` | 🚫 protected | +4/−105 |
| `worktree-e1-fable5-recode` | 📦 worktree | +22/−123 |

**Ação:** Fazer push dos branches protegidos e verify-first importantes. Os safe-delete não precisam de backup.

### MAJ-2: 6 PRs abertos bloqueiam limpeza — 3 em branches locais, 3 em remote-only

| PR | Branch | Status Local | Classificação |
|---|---|---|---|
| #13 | `claude/sad-roentgen` | presente | 🔍 verify-first |
| #64 | `fix/export-contract-56` | presente | 🔍 verify-first |
| #77 | `claude/blissful-keller-6tfahg` | presente | 🔍 verify-first |
| #79 | `rescue/ssd-pipeline-v2-20260611` | remote-only | órfão |
| #82 | `claude/awesome-hawking-41owe1` | remote-only | órfão |
| #108 | `claude/thesis-glossary-h8lno4` | remote-only | órfão |

**Ação:** PR #13 (2026-04-03) e PR #64 (2026-05-31) são antigos — decidir merge ou close. PR #77 é recente (2026-06-11). PRs #79, #82, #108 são recentes.

### MAJ-3: 15 worktrees ativos — fragmentação excessiva

Worktrees espalhados por 4 localizações no filesystem:

| Localização base | Worktrees |
|---|---|
| `~/.codex/worktrees/` | 3 (codex) |
| `~/.gemini/antigravity/worktrees/` | 1 (gemini) |
| `~/copilot-worktrees/` | 6 (copilot) |
| `~/Research/hub/iconocracy-corpus/.claude/worktrees/` | 2 (claude) |
| `~/Research/` | 3 (main + pr85-fix + editorial) |

**Ação:** Consolidar worktrees de agentes que não estão mais ativos. Worktrees do copilot e gemini podem ser removidos se as branches subjacentes não forem mais necessárias.

---

## 🟡 MINOR

### MIN-1: Branch `pr/76/data/reacquire-images-batch2-iiif-20260609` duplica `data/reacquire-images-batch2-iiif-20260609`

A branch `pr/76/data/reacquire-images-batch2-iiif-20260609` (🚫 protected, pr/**) é essencialmente um espelho da branch `data/reacquire-images-batch2-iiif-20260609` (🔍 verify-first). PR #76 já foi MERGED.

**Ação:** Remover `pr/76/...` após verificar que não há trabalho não-pushado.

### MIN-2: Branches `pr-33-sync` e `pr-research-materials-v2` são tracking branches obsoletos

Ambos merged (ahead=0), ambos local-only, ambos com PRs originais já fechados/merged:
- `pr-33-sync` → PR #33 (MERGED)
- `pr-research-materials-v2` → PR #44 (CLOSED)

**Ação:** Delete imediato.

### MIN-3: Branch `infra/hub-consistency-refactor` está 507 commits atrás de main

Ahead=10, behind=507. O gap é grande demais para rebase trivial. Pode exigir merge strategy manual.

---

## ✅ Pontos fortes

1. **Branch `main` limpa e atualizada** — commit 826d8dd, sem divergências.
2. **Branches protegidas explícitas** — `e1-opus48-*` identificadas como NÃO DELETAR com justificativa documentada.
3. **PR #108 é recente** (2026-06-26) — mostra atividade ativa de documentação.
4. **Worktrees organizados por agente** — codex, copilot, gemini, claude separados, facilitando auditoria por ferramenta.
5. **Boa adoção de convenções** — branches usam prefixos `feat/`, `fix/`, `docs/`, `data/`, `editorial/`, `reconcile/`.

---

## 📈 Métricas

### Distribuição por bucket

| Bucket | Count | % |
|---|---|---|
| 🗑️ safe-delete | 6 | 17.1% |
| 🔍 verify-first | 13 | 37.1% |
| 🚫 protected | 5 | 14.3% |
| 📦 worktree (named) | 10 | 28.6% |
| ★ main | 1 | 2.9% |

### Distribuição por origem do agente

| Origem | Count | Branches |
|---|---|---|
| Claude Code | 7 | blissful, corpus-acq, decide, fervent, sad, setup, add-actions |
| Copilot | 2 | add-csv, migrate-worker |
| Codex | 1 | local-work-pr107 |
| Gemini | 1 | cosmic-ember |
| Manual/humano | 24 | demais |

### Idade dos PRs abertos

| PR | Branch | Criado | Idade |
|---|---|---|---|
| #13 | claude/sad-roentgen | 2026-04-03 | 84 dias |
| #64 | fix/export-contract-56 | 2026-05-31 | 26 dias |
| #77 | claude/blissful-keller-6tfahg | 2026-06-11 | 15 dias |
| #79 | rescue/ssd-pipeline-v2 | 2026-06-11 | 15 dias |
| #82 | claude/awesome-hawking | 2026-06-15 | 11 dias |
| #108 | claude/thesis-glossary | 2026-06-26 | <1 dia |

---

## 🗂️ Classificação completa

### 🗑️ safe-delete (6 branches — ação: `git branch -D`)

| # | Branch | Ahead/Behind | Remote? | PR? | Motivo |
|---|---|---|---|---|---|
| 1 | `add-claude-github-actions-1775789759242` | +2/−594 | ❌ local-only | — | stale Claude auto-name |
| 2 | `ci/fix-crda-permissions` | 0/−456 | ❌ local-only | — | merged |
| 3 | `claude/decide-next-steps-v2mE3` | 0/−55 | ❌ local-only | — | merged + stale Claude |
| 4 | `copilot/add-csv-json-export-analytics-dashboard` | +2/−588 | ❌ local-only | — | stale copilot/add-* |
| 5 | `pr-33-sync` | 0/−196 | ❌ local-only | PR #33 (MERGED) | merged tracking |
| 6 | `pr-research-materials-v2` | 0/−167 | ❌ local-only | PR #44 (CLOSED) | merged tracking |

### 🔍 verify-first (13 branches — ação: revisar antes de decidir)

| # | Branch | Ahead/Behind | Remote? | PR? | Nota |
|---|---|---|---|---|---|
| 1 | `claude/blissful-keller-6tfahg` | +15/−123 | ✅ origin | #77 ABERTO | PR aberto, NÃO deletar |
| 2 | `claude/sad-roentgen` | +2/−661 | ✅ origin | #13 ABERTO | PR aberto, NÃO deletar |
| 3 | `codex/local-work-pr107-followup` | +1/−2 | ❌ local-only | — | ahead=1, quase merged |
| 4 | `consolidate/2026-06-19-audit-ssot` | +1/−105 | ❌ local-only | — | recente, ahead=1 |
| 5 | `copilot/migrate-worker-routing-to-hono` | +3/−51 | ❌ local-only | — | ahead=3, pequeno gap |
| 6 | `data/reacquire-images-batch2-iiif-20260609` | +9/−105 | ✅ origin | PR #76 MERGED | data/**, verificar se fully merged |
| 7 | `docs/reliability-audit-2026-06-19` | +1/−103 | ❌ local-only | — | docs/**, verificar utilidade |
| 8 | `docs/ssot-methodology-2026-06-19` | +18/−123 | ❌ local-only | — | ahead=18, trabalho significativo |
| 9 | `feat/alegorias-piloto-v2` | +20/−70 | ✅ origin | PRs #96/#98 MERGED | feat/**, 20 commits ahead |
| 10 | `feat/codebook-master-v2.2.0` | +1/−67 | ❌ local-only | — | feat/**, verificar |
| 11 | `feature/imes-v3-transition` | +4/−463 | ❌ local-only | — | behind=463, gap grande |
| 12 | `fix/export-contract-56` | +1/−123 | ✅ origin | #64 ABERTO | PR aberto, NÃO deletar |
| 13 | `infra/hub-consistency-refactor` | +10/−507 | ✅ origin | — | behind=507, verificar relevância |

### 🚫 protected (5 branches — ação: NÃO DELETAR sem autorização explícita)

| # | Branch | Ahead/Behind | Remote? | Worktree? | Nota |
|---|---|---|---|---|---|
| 1 | `e1-opus48-batch-2026-06-22` | +9/−99 | ❌ local-only | ❌ | NÃO DELETAR |
| 2 | `e1-opus48-promote-2026-06-22` | +2/−91 | ❌ local-only | ❌ | NÃO DELETAR |
| 3 | `pr/76/data/reacquire-images-batch2-iiif-20260609` | +4/−105 | ❌ local-only | ✅ copilot | pr/**, duplica data/ branch |
| 4 | `reconcile/ssd-scripts-2026-06-04` | +37/−123 | ✅ origin | ❌ | reconcile/**, 37 commits ahead |
| 5 | `reconcile/ssd-scripts-clean` | +3/−123 | ✅ origin | ❌ | reconcile/**, versão limpa |

### 📦 worktree (10 named branches + main — branches com worktrees ativos)

| # | Branch | Worktree Path | Ahead/Behind | Agente |
|---|---|---|---|---|
| 1 | `main` ★ | `/Users/ana/Research/hub/iconocracy-corpus` | — | main |
| 2 | `anavvanzin-orchestration-setup` | `~/copilot-worktrees/.../anavvanzin-refactored-memory` | 0/−99 | copilot |
| 3 | `anavvanzin-release-gate-remediation` | `~/copilot-worktrees/.../anavvanzin-miniature-eureka` | 0/−98 | copilot |
| 4 | `claude/corpus-acquisition-orchestrator-qDOpX` | `~/copilot-worktrees/.../claude-corpus-acquisition-orchestrator-qDOpX` | +2/−459 | copilot |
| 5 | `claude/fervent-meitner-u7lvik` | `~/copilot-worktrees/.../claude-fervent-meitner-u7lvik` | +17/−123 | copilot |
| 6 | `claude/setup-thesis-corpus-e346H` | `~/.codex/worktrees/e9db/iconocracy-corpus` | +1/−804 | codex |
| 7 | `cosmic-ember-floats-17h23` | `~/.gemini/antigravity/worktrees/.../cosmic-ember-floats-17h23` | 0/−40 | gemini |
| 8 | `editorial/revisao-2026-06-24` | `~/Research/iconocracy-editorial-wt` | +1/−50 | manual |
| 9 | `research/permanent` | `~/.../iconocracy-corpus/.claude/worktrees/research-permanent` | 0/−507 | claude |
| 10 | `research/workspace-map` | `~/copilot-worktrees/.../research-workspace-map` | 0/−40 | copilot |
| 11 | `worktree-e1-fable5-recode` | `~/.../iconocracy-corpus/.claude/worktrees/e1-fable5-recode` | +22/−123 | claude |

### 🔗 Detached HEAD worktrees (3 — fora de branches nomeadas)

| # | Worktree Path | Commit | Commit Message | Reachable via |
|---|---|---|---|---|
| 1 | `~/.codex/worktrees/34b4/iconocracy-corpus` | `41516a9` | docs(tese): clarify analytical N by instrument stratum | **NONE** ⚠️ |
| 2 | `~/.codex/worktrees/7bca/iconocracy-corpus` | `2487699` | docs(decisions): auditoria de estratificação | `data/reacquire-images-batch2-iiif-20260609` |
| 3 | `~/Research/hub/iconocracy-corpus-pr85-fix` | `5db68b7` | chore(corpus): regenerate stale root companion-data.json | `claude/fervent-meitner-u7lvik` |

---

## 🔍 Remote orphan branches (existem em origin, NÃO localmente)

| # | Branch remoto | PR | Estado PR | Ação recomendada |
|---|---|---|---|---|
| 1 | `claude/awesome-hawking-41owe1` | #82 | ABERTO | Aguardar merge/close do PR |
| 2 | `claude/thesis-glossary-h8lno4` | #108 | ABERTO | Aguardar merge/close do PR |
| 3 | `rescue/ssd-pipeline-v2-20260611` | #79 | ABERTO | Aguardar merge/close do PR |
| 4 | `copilot/create-implementation-plan` | — | — | `git push origin --delete` |
| 5 | `copilot/fix-irregularities-in-data` | — | — | `git push origin --delete` |
| 6 | `copilot/review-session-history` | — | — | `git push origin --delete` |
| 7 | `dialectic-cycle-1` | — | — | `git push origin --delete` |
| 8 | `docs/prp-plans-2026-06` | — | — | `git push origin --delete` |
| 9 | `fix/protobufjs-7.5.6` | — | — | `git push origin --delete` |
| 10 | `iconocracy-research-materials-2026-04-25` | — | — | `git push origin --delete` |
| 11 | `iconocracy-research-materials-clean` | #44 | CLOSED | `git push origin --delete` |

---

## 📋 Recomendações top 5

### 1. 🆘 Resgatar commit órfão `41516a9` IMEDIATAMENTE
```bash
cd /Users/ana/Research/hub/iconocracy-corpus
git branch rescue/detached-codex-34b4 41516a9
git push origin rescue/detached-codex-34b4
```
O worktree `~/.codex/worktrees/34b4/` contém trabalho de documentação da tese ("clarify analytical N by instrument stratum") que não pertence a nenhuma branch. Se o worktree for removido, o commit se torna inalcançável e será garbage-collected.

### 2. 🗑️ Deletar 6 branches safe-delete
```bash
git branch -D add-claude-github-actions-1775789759242
git branch -D ci/fix-crda-permissions
git branch -D claude/decide-next-steps-v2mE3
git branch -D copilot/add-csv-json-export-analytics-dashboard
git branch -D pr-33-sync
git branch -D pr-research-materials-v2
```

### 3. 🧹 Limpar 8 branches órfãos do remote (sem PRs abertos)
```bash
git push origin --delete copilot/create-implementation-plan
git push origin --delete copilot/fix-irregularities-in-data
git push origin --delete copilot/review-session-history
git push origin --delete dialectic-cycle-1
git push origin --delete docs/prp-plans-2026-06
git push origin --delete fix/protobufjs-7.5.6
git push origin --delete iconocracy-research-materials-2026-04-25
git push origin --delete iconocracy-research-materials-clean
```

### 4. 🔍 Revisar e decidir destino dos 6 PRs abertos
- **PR #13** (84 dias, `claude/sad-roentgen`) — o mais antigo. Merge ou close com justificativa.
- **PR #64** (26 dias, `fix/export-contract-56`) — fix de contrato de exportação. Merge se aprovado.
- **PR #77** (15 dias, `claude/blissful-keller-6tfahg`) — auditoria de branches. Relevante para este audit.
- **PR #79** (15 dias, remote-only) — rescue pipeline. Fetch e revisar.
- **PR #82** (11 dias, remote-only) — apresentação grupo de estudos. Fetch e revisar.
- **PR #108** (<1 dia, remote-only) — desambiguação Iconclass. Muito recente.

### 5. 📦 Consolidar worktrees de agentes inativos
Verificar quais agentes ainda estão em uso ativo:
- **copilot** (6 worktrees): maior fragmentação. Se o agente não está mais ativo, remover worktrees e decidir destino das branches subjacentes.
- **gemini** (1 worktree): `cosmic-ember-floats-17h23` já foi merged (ahead=0). Remover worktree.
- **codex** (3 worktrees): 2 detached + 1 em `claude/setup-thesis-corpus-e346H`. Resgatar o detached #34b4 e consolidar.

---

## 📎 Apêndice: Comandos de auditoria executados

```bash
git branch -a                          # Lista completa de branches
git worktree list                      # Todos os worktrees com paths
git ls-remote --heads origin           # Branches remotos
git branch --merged main               # Branches merged
git rev-list --count main..<branch>    # Ahead count
git rev-list --count <branch>..main    # Behind count
gh pr list --state open                # PRs abertos
gh pr view <N> --json state,headRefName,title,url  # Detalhes de PRs
git branch --contains <commit>         # Alcancabilidade de commits detached
```

---

*Relatório gerado por Hermes Agent (Nous Research) em 2026-06-26 para o projeto ICONOCRACY 360° — Wave 1.1: Git Topology.*
