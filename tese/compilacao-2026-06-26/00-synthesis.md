# 00-Synthesis — Auditoria 360° ICONOCRACY

**Data:** 2026-06-26
**Ondas:** 3 (7 subagentes)
**Escopo:** `/Users/ana/Research/hub/iconocracy-corpus`
**Relatórios:** 7 audit reports na `compilacao-2026-06-26/`

---

## Top-10 Achados (consolidado cross-domain)

### CRITICAL (6)

| # | ID | Domínio | Achado | Impacto |
|---|-----|---------|--------|---------|
| C1 | GIT-TOP-C1 | Branches | 3 worktrees em detached HEAD — 1 órfão total (commit `41516a9`) sem branch associada | **Perda de trabalho** se worktree for removido |
| C2 | GIT-TOP-C2 | Branches | 11 branches remotos órfãos em `origin` — 8 deletáveis, 3 com PRs abertos | Poluição do remote, risco de confusão |
| C3 | SYM-C1 | Symlinks | 51 symlinks quebrados em `.hermes/skills/` → `../../.agents/skills/*` (inexistente) | `hermes` não encontra skills listadas; 63% de falha silenciosa |
| C4 | GI-C1 | Gitignore | `wiki/.obsidian/plugins/` NÃO está no .gitignore — 297 arquivos de plugin (~50MB JS) tracked em git | Tamanho do repo inchado; builds de plugin não deveriam ser versionados |
| C5 | DI-C1 | Dados | Traceability Rule violada: Drive manifest cobre apenas 55% (165/299) | 134 itens sem backup confirmado no Google Drive (ADR-001) |
| C6 | DI-C2 | Dados | Vault coverage via id-mapping = ~15% (45/299). Pipeline vault↔records não automatizado | Rastreabilidade tripla quebrada para maioria dos itens |

### MAJOR (4)

| # | ID | Domínio | Achado | Impacto |
|---|-----|---------|--------|---------|
| M1 | GIT-TOP-M1 | Branches | 19 branches locais sem push remoto — sem backup | Perda permanente se falha de disco |
| M2 | GI-M1 | Gitignore | 34 PDFs + 186 binários totais tracked em git (incluindo PDFs de 22MB e 17MB) | Tamanho do clone cresce; git não é ideal para binários grandes |
| M3 | SCH-M1 | Schemas | Phantom field `justificativa_genero` detectado como drift de schema — campo existe em records mas não no schema | Inconsistência schema↔dados; futura validação pode quebrar |
| M4 | SCR-M1 | Scripts | 5 scripts com paths absolutos quebrados (`/Users/ana/research/...`, `/data/iconocracy-corpus/...`, `/home/user/workspace/moedas`) | Scripts não executáveis sem conserto manual |

### MINOR notáveis

- **DI-m1:** ID mapping com 3 duplicatas + 3 órfãos
- **SCH-m1:** `RefResolver` deprecated no validate_schemas.py
- **DOC-m1:** CLAUDE.md (278) vs AGENTS.md (280) vs realidade (299) — 3 contagens diferentes do corpus
- **SCR-m1:** 6 pacotes externos não listados em requirements.txt (yaml, torch, transformers, peft, trl, datasets)
- **SCR-m2:** Cobertura de testes: apenas 18.2% (16/88 scripts testados)

---

## Matriz de Dependências

| Se fixar... | Desbloqueia... |
|-------------|----------------|
| C3 (51 symlinks quebrados) | M1 (19 branches sem backup — symlinks são o maior "ruído" ao listar skills) |
| C5 (Drive manifest) | Rastreabilidade completa para CI/release gate |
| C2 (8 branches remotos órfãos) | Limpeza do origin, CI mais rápido |
| M3 (Phantom field schema) | Validação futura de schema não quebra |
| M4 (Scripts com paths quebrados) | Pipeline de scripts executável |

---

## Roadmap de Remediação

### Sprint 1 — Quick Wins (hoje/amanhã, ~30 min)

1. **🗑️ Deletar 9 branches merged** — `git branch -d` em lote
2. **🗑️ Deletar 6 branches Claude Code stale** — `claude/sad-roentgen`, `claude/setup-thesis-corpus-e346H`, etc.
3. **🗑️ Deletar 50 symlinks quebrados** — `find .hermes/skills -xtype l -delete`
4. **🔧 Resgatar worktree órfão** — `git branch rescue/detached-34b4 41516a9`
5. **📝 Atualizar contagens em CLAUDE.md/AGENTS.md** — 299 unificado
6. **📝 Adicionar `wiki/.obsidian/plugins/` ao .gitignore**

**Commits estimados:** 3

### Sprint 2 — Estrutural (esta semana, ~2h)

7. **🔄 Sincronizar Drive manifest** — rodar `vault_sync.py` e atualizar `drive-manifest.json` para ≥95% coverage
8. **🔄 Consertar 5 scripts com paths quebrados** — substituir paths absolutos por relativos
9. **📝 Adicionar 6 pacotes ao requirements.txt** — yaml, torch, transformers, peft, trl, datasets
10. **🗑️ Remover 8 branches remotos órfãos** (os sem PR aberto)
11. **📝 Resolver phantom field `justificativa_genero`** — adicionar ao schema ou remover dos records

**Commits estimados:** 5

### Sprint 3 — Polish (próxima semana, ~3h)

12. **🧹 Remover PDFs/binários grandes do git tracking** — `git rm --cached` + atualizar .gitignore
13. **🧪 Subir cobertura de testes** — adicionar testes para scripts sem cobertura (meta: 40%)
14. **📝 Migrar `RefResolver` → `referencing` no validate_schemas.py**
15. **🔄 Resolver 3 PRs abertos** em branches órfãos remotos (#82, #108, #79)
16. **📝 Unificar CLAUDE.md e AGENTS.md** — single source of truth ou divisão clara de responsabilidades

**Commits estimados:** 6

---

## Pontos Fortes (o que NÃO mexer)

- ✅ **Schema validation: 299/299 records, 236/236 purification — impecável**
- ✅ **Draft 2020-12 em todos os 5 schemas — consistente**
- ✅ **records.jsonl ↔ corpus-data.json sincronizados (299=299) — sem drift**
- ✅ **Nenhum secret/credential encontrado — limpo**
- ✅ **.gitignore cobre bem Python/Node/Obsidian (base sólida)**
- ✅ **CI com 12 workflows ativos no main**
- ✅ **CLAUDE.md bem estruturado e abrangente (17KB)**

---

## Métricas da Auditoria

| Métrica | Valor |
|---------|-------|
| Total achados | **23** (6 CRITICAL + 4 MAJOR + ~13 MINOR) |
| Wall-clock total | ~18 min (3 ondas) |
| Subagentes executados | 7/7 (100% sucesso) |
| Relatórios entregues | 7/7 |
| Schema adherence | Alta (variação entre formatos, mas todos completos) |
| Índice de integridade do corpus | 89% (core sólido, periferia frágil) |

---

## Decisões pendentes para Ana

1. **Worktrees:** Posso deletar os 3 worktrees detached HEAD? (após resgatar o órfão C1)
2. **Branches merged:** Deletar as 9 agora? (seguro, já estão em main)
3. **Branches remotos órfãos:** Deletar os 8 sem PR? (precisa de `git push origin --delete`)
4. **wiki/.obsidian/plugins/:** Gitignorar e `git rm --cached`? (297 arquivos, ~50MB)
5. **PDFs/binários tracked:** Remover do tracking? (34 PDFs, 186 binários)
