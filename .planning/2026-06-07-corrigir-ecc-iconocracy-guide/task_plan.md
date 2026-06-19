# Task Plan: Corrigir ecc-iconocracy-guide

## Goal

Corrigir contradições verificadas no `.claude/skills/ecc-iconocracy-guide/SKILL.md` para que o guia descreva o ambiente macOS atual e só liste skills/comandos/MCPs que **existem de fato neste host**, mantendo a estrutura "3 camadas + descoberta" intacta.

## Current Phase

DONE

## Phases

### Phase 1: Confirmar escopo com a usuária
- [x] Apresentar o conjunto mínimo (CRITICAL + HIGH) e pedir aprovação
- [x] Decidir sobre MEDIUM (firecrawl, iconocracy-agent, ssd-health Linux-only, parêntese "~69 scripts")
- [x] Decidir sobre LOW (renumeração, glossário scite, dica de auditoria do plugin)
- **Status:** complete
- **Resultado:** escopo=TUDO; scite=manter com nota "em setup" + adicionar firecrawl como linha ativa; iconocracy-agent=nota de rodapé na seção 1

### Phase 2: Aplicar correções aprovadas
- [x] Editar `SKILL.md` (uma substituição por bloco)
  - [x] Host macOS primário + Linux secundário (decisão da usuária)
  - [x] Plugin corrigido para `everything-claude-code v1.10.0` + caminho real do cache + dica de auditoria
  - [x] **Mantido** `/security-scan` (descoberta: skill existe em `~/.claude/plugins/cache/.../skills/security-scan/`); refraseado para refletir o que faz (config Claude, não código Python)
  - [x] **Mantido** `/find-skill` (typo: `/find-skills` plural não existia; singular existe)
  - [x] Removido `/ecc-guide` (não existe)
  - [x] scite mantido com nota "**em setup** — falta configurar MCP" + firecrawl adicionado como ativo
  - [x] Nota de rodapé `iconocracy-agent` na seção 1
  - [x] Aviso `(Linux-only)` em ssd-health
  - [x] Removido "(~69 scripts em tools/scripts/)" e esclarecido que comandos ECC NÃO são wrappers desses scripts
  - [x] Renumerado "três camadas" → "três camadas + duas seções transversais"
  - [x] Adicionada dica `cat .claude-plugin/plugin.json` + `ls .../commands/` na seção descoberta
- [x] `description:` permanece (escopo da skill não mudou)
- **Status:** complete

### Phase 3: Verificação
- [x] Re-ler `SKILL.md` editado e checar coerência (numeração, links, tabelas) → OK
- [x] Reexecutar verificações: plugin v1.10.0 ✓, 11 slash-commands ✓, security-scan skill ✓, find-skill skill ✓, conda macOS ✓
- [x] `description:` permanece — escopo declarado ainda bate
- **Status:** complete

### Phase 4: Entrega
- [x] Diff resumido (antes/depois) — 41 linhas alteradas, 21 add / 20 del
- [x] Commit `7844d13` e push do branch
- [x] PR #68 contra main: https://github.com/anavvanzin/iconocracy-corpus/pull/68
- [x] `progress.md` atualizado
- **Status:** complete

## Key Questions

1. Aplicar **só** CRITICAL+HIGH ou incluir MEDIUM/LOW?
2. Manter a estrutura "3 camadas" ou renumerar para "4 seções" (LOW #11)?
3. Adicionar firecrawl como **substituto** de scite na seção MCP, ou em linha separada de "busca web" (MEDIUM #7)?
4. Mencionar `iconocracy-agent` (user-level) como skill primária acima das skills de projeto, ou só em nota (MEDIUM #8)?

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Usar `.planning/<slug>/` em vez de `task_plan.md` na raiz | Trabalho paralelo em curso no branch `reconcile/ssd-scripts-2026-06-04`; isola contextos |
| Entrar em worktree (`fix-ecc-iconocracy-guide`) | Hook bg-isolation exigiu; previne pisar no checkout principal |
| Pedir confirmação antes de editar (Phase 1 separada) | CLAUDE.md exige scope-check antes de ação não-trivial; o guia é referência viva |
| Não tocar `CLAUDE.md` (counts 265 vs reais 308/315) nesta tarefa | Fora de escopo — drift já listado em "Known Data Issues", merece tarefa própria |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| `CLAUDE_PLUGIN_ROOT` vazio ao chamar session-catchup.py | 1 | Resolvi caminho absoluto `/Users/ana/.claude/skills/planning-with-files/` |
| `bg session hasn't isolated` ao tentar Write em `.planning/` | 1 | Chamei EnterWorktree e re-iniciei o plano dentro do worktree |

## Notes

- Auditoria com evidência (`ls`, `find`, `uname -a`, `grep`) já feita no turno anterior — todas as mudanças propostas são verificáveis.
- Guia em `.claude/skills/ecc-iconocracy-guide/SKILL.md` (87 linhas).
- Sem teste automatizado para skill descriptions; verificação é leitura + re-grep dos recursos citados.
- Worktree: `/Users/ana/Research/hub/iconocracy-corpus/.claude/worktrees/fix-ecc-iconocracy-guide/`
