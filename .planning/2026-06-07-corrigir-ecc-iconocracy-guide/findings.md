# Findings — Auditoria do ecc-iconocracy-guide

## Evidência coletada (turno anterior)

### Host real
- `uname -a` → `Darwin 192.168.100.83 25.6.0 … arm64` → **macOS**.
- `/Volumes/` → `'Macintosh HD' -> /` e `com.apple.TimeMachine.localsnapshots`. Sem `/Volumes/SSD_DATA`, sem `/Volumes/data`.
- `/media/ana/SSD_DATA` → inexistente (Linux only).
- Memória global (`~/.claude/CLAUDE.md`): SSD é Linux Syncthing, `ufsd_ExtFS`, binários falham no macOS com `exec format error`.

### Plugin ECC
- `/Users/ana/.claude/plugins/marketplaces/everything-claude-code/.claude-plugin/plugin.json`:
  - `"name": "everything-claude-code"`
  - `"version": "1.10.0"`
- Guia afirma `ecc v2.0.0-rc.1` → divergente em nome e versão.
- `.claude/commands/` no projeto está vazio. Comandos vivem em `/Users/ana/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.10.0/commands/`.

### Slash-commands listados — existem?
| Comando | Resultado `find` |
|---|---|
| `/python-review` | ✓ commands/python-review.md |
| `/code-review` | ✓ commands/code-review.md |
| `/security-scan` | ✗ NOT FOUND |
| `/test-coverage` | ✓ |
| `/quality-gate` | ✓ |
| `/refactor-clean` | ✓ |
| `/build-fix` | ✓ |
| `/update-docs` | ✓ |
| `/update-codemaps` | ✓ |
| `/plan` | ✓ |
| `/feature-dev` | ✓ |
| `/model-route` | ✓ |
| `/find-skills` | ✗ NOT FOUND (existe a skill `find-skill`, não slash-command) |
| `/ecc-guide` | ✗ NOT FOUND |

### MCPs declarados
- `grep scite /Users/ana/.claude/settings*.json /Users/ana/.mcp.json` → **zero ocorrências**.
- Context7: disponível como `mcp__plugin_context7_context7__*` e `mcp__plugin_everything-claude-code_context7__*`.
- Exa: disponível como `mcp__plugin_everything-claude-code_exa__*`.
- **Firecrawl**: disponível como `mcp__firecrawl__*` (não mencionado no guia, mas é a busca web recomendada no CLAUDE.md global).

### Skills do projeto
26 entradas em `.claude/skills/` — todas as listadas no guia existem:
`compilar-tese`, `sync-corpus`, `scout-dedupe`, `ssd-health`, `abnt-precommit`, `zotero-cite`, `release-gate`, `archive-fallback`, `pandoc-fix` ✓

### Skill ssd-health
`SKILL.md` linha 14: "Linux (Debian). The SSD is partition `sdb1`… Mac-era paths são stale."
→ Skill explicitamente Linux-only; rodar no macOS atual não vai funcionar.

### Skill iconocracy-agent
- Existe em `/Users/ana/.claude/skills/iconocracy-agent/` (user-level, não projeto).
- CLAUDE.md do hub a cita como "default umbrella — orchestrates corpus research, coding, compile, progress".
- Guia atual não a menciona.

### Contagens do corpus (contexto, fora do escopo da correção do guia)
- `records.jsonl` → **308 linhas** (CLAUDE.md afirma 265).
- `corpus-data.json` → **315 itens** (CLAUDE.md afirma 264).
- Drift documentado mas não corrigido — tarefa separada.

## Resumo das mudanças propostas

| Sev | Item | Onde no guia |
|---|---|---|
| CRITICAL | Inverter host Mac↔Linux | L85–86 |
| CRITICAL | `ecc v2.0.0-rc.1` → `everything-claude-code v1.10.0`; comandos no cache global, não em `.claude/commands/` local | L17 |
| HIGH | Remover `/security-scan` | L60 |
| HIGH | Remover `/find-skills`, `/ecc-guide` | L78–79 |
| HIGH | Remover scite da tabela MCP | L72 |
| MEDIUM | Adicionar firecrawl (busca web primária) | L68–74 |
| MEDIUM | Adicionar nota "iconocracy-agent (user-level)" | L23 |
| MEDIUM | Avisar que ssd-health é Linux-only | L30 |
| MEDIUM | Remover "(~69 scripts em tools/scripts/)" — comandos ECC não são wrappers desses scripts | L53 |
| LOW | Renumerar (3 camadas → 4 seções) ou ajustar texto | L14, L76 |
| LOW | Glossário "Smart Citations" — torna-se irrelevante se scite sair | L72 |
| LOW | Adicionar dica de auditoria do próprio plugin (`cat .../plugin.json`) | nova seção |

## Decisões pendentes da usuária
- Q1: escopo (CRITICAL+HIGH apenas, ou incluir MEDIUM/LOW?)
- Q2: estrutura "3 camadas" → "4 seções"
- Q3: firecrawl substitui scite, ou linha separada de "busca web"
- Q4: iconocracy-agent como skill primária ou só nota
