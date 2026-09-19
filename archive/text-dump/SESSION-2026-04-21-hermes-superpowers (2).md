---
tipo: sessao-de-configuracao
data: 2026-04-21
fase: setup-hermes
status: concluida
tags:
  - hermes
  - superpowers
  - plugin
  - skills
---

# Sessão 2026-04-21 — Superpowers Plugin para Hermes

## O que foi feito

Instalou-se o plugin **superpowers** (obra/superpowers v5.0.7) no Hermes Agent. O repo ja estava cached em `~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/`. Copiaram-se os 14 skills para `~/.hermes/skills/superpowers/`.

## Skills instalados

Categoria `superpowers` com 14 skills:

| Skill | Descrição | Conflito de nome? |
|-------|-----------|-------------------|
| `brainstorming` | Sessão estruturada de ideação | nao |
| `dispatching-parallel-agents` | Orquestrar múltiplos subagentes | nao |
| `executing-plans` | Executar planos implementados | nao |
| `finishing-a-development-branch` | Fechar branch com verificações | nao |
| `receiving-code-review` | Receber feedback de code review | nao |
| `requesting-code-review` | Solicitar code review externo | nao |
| `subagent-driven-development` | Delegar para subagentes | SIM — `software-development/subagent-driven-development` |
| `systematic-debugging` | Workflow rigoroso de debugging | SIM — `software-development/systematic-debugging` |
| `test-driven-development` | Workflow TDD | SIM — `software-development/test-driven-development` |
| `using-git-worktrees` | Usar worktrees git para isolamento | nao |
| `using-superpowers` | Visão geral / como usar skills | nao |
| `verification-before-completion` | Verificação antes de declarar pronto | nao |
| `writing-plans` | Escrever planos de implementação | SIM — `software-development/writing-plans` |
| `writing-skills` | Criar e testar skills | nao |

## Como invocar skills com nome conflitante

Para usar a versao superpowers em vez da versao Hermes nativa:

```
skill_view(name="superpowers:subagent-driven-development")
skill_view(name="superpowers:writing-plans")
skill_view(name="superpowers:test-driven-development")
skill_view(name="superpowers:systematic-debugging")
```

## Caminho do repo source

```
~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/
```

## Para atualizar

```bash
# Remover e recopy se necessario
rm -rf ~/.hermes/skills/superpowers
cp -r ~/.cache/opencode/packages/superpowers@git+https:/github.com/obra/superpowers.git/node_modules/superpowers/skills/* ~/.hermes/skills/superpowers/
```

## Continuação desta sessão

Sessão anterior: `SESSION-2026-04-21-ultraplan-peer-review.md` — peer review do ultraplan de reposicionamento de originalidade com roadmap de 10 itens (3 REQUIRED, 4 STRONGLY RECOMMENDED, 3 SUGESTED).

Próximo passo recomendado: retomar o peer review e produzir o primeiro artefato pendente — **protocolo de validação inter-observador** (REQUIRED #2, a lacuna metodológica mais grave identificada por R3).
