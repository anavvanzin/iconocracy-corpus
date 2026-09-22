# Auditoria 360° — iconocracy-corpus / Ultraplan
Data: 2026-06-26
Escopo: `/Users/ana/Research/hub/iconocracy-corpus`
Estratégia: 3 ondas concorrentes — branches/skills → dados/schemas → docs/scripts
Lentes: git-topology, symlink-integrity, data-integrity, code-quality, doc-governance
Produto final: 7 relatórios + 1 síntese com top-10 achados + roadmap de remediação
Modo: planejamento apenas — nenhuma mutação até aprovação da síntese

## Ground Truth (reconhecimento 2026-06-26)

- **Repo único**, 35 branches locais (9 merged, 25 unmerged), 25 remotas, 11 worktrees
- **Dados**: 299 records.jsonl | 299 corpus-data.json | 236 purification.jsonl — estável
- **Scripts**: 88 Python em tools/scripts/
- **Arquivos**: 5.427 .md | 1.427 .py | 447 .json | 297 .gz | 245 .pdf
- **Symlinks quebrados**: 49 em `.hermes/skills/` → `../../.agents/skills/*` (inexistente)
- **CI**: 12 workflows no main, duplicados em 2 worktrees
- **Diretórios grandes**: shared/ 181M | vault/ 158M | wiki/ 104M | postman/ 53M

## Premissas

1. `e1-opus48-batch` NÃO deletar (staging até defesa, per memory)
2. `main` é canônico
3. `.gitignore` bloqueia `tese/compilacao-*/` (force-add necessário)
4. Symlinks quebrados podem ser deletados em lote
5. Worktrees precisam de `git worktree` para gerenciar
6. Nenhum arquivo de corpus canônico (records.jsonl, purification.jsonl, corpus-data.json) será mutado sem OK explícito

## Riscos conhecidos e mitigações

| Risco | Mitigação |
|-------|-----------|
| Worktree com trabalho ativo é deletado | Listar worktrees primeiro, confirmar com usuário |
| Branch staging (e1-opus48) deletado por engano | Excluir da lista de deleção, marcar como protegido |
| Symlink quebrado que ainda é referenciado | Verificar se há imports/requires antes de deletar |
| Subagentes timeout em diretórios grandes | Escopos com paths exatos, não glob de raiz |
| Duplicação de achados entre agentes | Partição de paths sem overlap |

## Schema de Relatório (todos os subagentes)

```markdown
# Audit Report — <domínio> — <lente>
Escopo examinado: <paths>
Arquivos analisados: N
Data: 2026-06-26

## Resumo executivo (≤5 linhas)

## Achados — CRITICAL (bloqueante)
- [C-01] ...

## Achados — MAJOR
- [M-01] ...

## Achados — MINOR
- [m-01] ...

## Pontos fortes (o que NÃO mexer)

## Métricas mensuradas

## Recomendações priorizadas (top 5)
```

## WAVE 1 — Infraestrutura (3 agentes concorrentes)

### Agent 1.1 — Git Topology (branches + worktrees + remotes)
Escopo: `git branch`, `git worktree list`, `git remote`
Goal:
a) Listar todas as branches com status (merged/unmerged/stale/worktree)
b) Classificar em 4 buckets: 🗑️ safe-delete, 🔍 verify-first, 🚫 protected, 📦 worktree
c) Verificar worktrees: quais têm trabalho não commitado?
d) Checar branches remotas órfãs (sem local)
e) Identificar branches com PRs abertos no GitHub
Toolsets: terminal, file, search
Saída esperada: `audit-wave1-git-topology.md` com tabela de classificação

### Agent 1.2 — Symlink Integrity
Escopo: `.hermes/skills/`, `.claude/skills/`
Goal:
a) Listar todos os symlinks quebrados (49 em .hermes/skills/)
b) Verificar se os targets originais existem em outro path
c) Identificar quais skills são duplicadas em .claude/ vs .hermes/
d) Recomendar: deletar, consertar, ou ignorar cada um
Toolsets: terminal, file, search
Saída esperada: `audit-wave1-symlinks.md` com tabela link→target→ação

### Agent 1.3 — .gitignore Audit
Escopo: `.gitignore`, `.git/info/exclude`
Goal:
a) Verificar se o gitignore atual cobre todos os padrões necessários
b) Identificar arquivos grandes/desnecessários tracked no git (shared/ 181M, wiki/ 104M, postman/ 53M)
c) Checar se `tese/compilacao-*/` é a regra correta ou deve ser refinada
d) Verificar se há secrets/credentials tracked
Toolsets: terminal, file, search
Saída esperada: `audit-wave1-gitignore.md` com recomendações

## WAVE 2 — Dados & Schemas (2 agentes concorrentes)

### Agent 2.1 — Data Integrity
Escopo: `data/processed/`, `corpus/`, `data/raw/`
Goal:
a) Validar records.jsonl vs corpus-data.json (contagem, consistência)
b) Verificar purification.jsonl — itens órfãos ou duplicados
c) Checar data/raw/drive-manifest.json vs records.jsonl (traceability rule)
d) Identificar records com URLs placeholder (8 conhecidos)
e) Verificar se há drift entre exports
Toolsets: terminal, file, search
Saída esperada: `audit-wave2-data-integrity.md`

### Agent 2.2 — Schema Audit
Escopo: `tools/schemas/`, `tools/scripts/validate_schemas.py`
Goal:
a) Verificar todos os schemas JSON (versão draft, validação)
b) Checar se master-record.schema.json cobre todos os campos em uso
c) Identificar campos no records.jsonl que NÃO estão no schema
d) Verificar consistência entre os 3 schemas (master-record, iconocode-output, webscout-input/output)
e) Rodar validate_schemas.py e reportar resultado
Toolsets: terminal, file
Saída esperada: `audit-wave2-schemas.md`

## WAVE 3 — Docs & Scripts (2 agentes concorrentes)

### Agent 3.1 — Documentation Governance
Escopo: `CLAUDE.md`, `AGENTS.md`, `README.md`, `SKILLS.md`, `docs/`
Goal:
a) Verificar consistência entre CLAUDE.md e AGENTS.md (contagens, paths, comandos)
b) Checar docs/decisions/ — quantos ADRs, estão indexados?
c) Verificar docs/PLANO-TESE-ICONOCRACIA.md vs sumário atual
d) Identificar docs stale/desatualizados
e) Checar referências a paths que não existem mais
Toolsets: terminal, file, search
Saída esperada: `audit-wave3-docs-governance.md`

### Agent 3.2 — Scripts Health
Escopo: `tools/scripts/` (88 scripts)
Goal:
a) Identificar scripts sem shebang ou não-executáveis
b) Verificar imports quebrados (módulos não instalados)
c) Checar scripts que referenciam paths inexistentes
d) Identificar duplicação funcional entre scripts
e) Recomendar: quais manter, quais arquivar, quais consertar
Toolsets: terminal, file, search
Saída esperada: `audit-wave3-scripts-health.md`

## WAVE 4 — Síntese (parent agent, NÃO subagente)

Após todos os 7 relatórios:
1. Ler cada arquivo do disco
2. Produzir `00-synthesis.md` com:
   - Top-10 achados cross-domain (CRITICAL + MAJOR)
   - Matriz de dependências (fix X → unlock Y)
   - Roadmap em 3 sprints (1: quick wins, 2: structural, 3: polish)
3. Spawnar plano de remediação separado

## Caminhos de arquivos que serão criados

```
tese/compilacao-2026-06-26/
  audit-wave1-git-topology.md
  audit-wave1-symlinks.md
  audit-wave1-gitignore.md
  audit-wave2-data-integrity.md
  audit-wave2-schemas.md
  audit-wave3-docs-governance.md
  audit-wave3-scripts-health.md
  00-synthesis.md
```

## Métricas de sucesso

- Wall-clock ≤ 45 min
- ≥ 20 achados CRITICAL+MAJOR
- Zero duplicação entre agentes
- Todos os relatórios no schema

## Decisões do usuário (antes de executar)

1. `e1-opus48-batch` e `e1-opus48-promote` — protegidos, NÃO deletar ✅ (já confirmado)
2. Worktrees: posso listar e recomendar, mas NÃO deletar sem OK?
3. Symlinks quebrados: deletar em lote ou confirmar um a um?
4. Branches merged: deletar as 9 agora ou esperar a auditoria completa?
5. `postman/` (53M) e `wiki/` (104M) — investigar se são lixo ou necessários?
