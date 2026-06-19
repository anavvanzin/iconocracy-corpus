# Plano: Ação Pós-Revisão de Sessões
**Data:** 2026-04-28
**Escopo:** ~/iconocracy-corpus

---

## Contexto

Revisão de todas as sessões desde Abr 2026 identificou:

- **T5 canonicalization + CONTRA-ALEGORIA**: propagado em todos os skills, mas **commit/push pode não ter ido** (sessão foi truncada)
- **IMES v3.0**: decisão metodológica feita (três camadas irredutíveis), Fase 1 concluída, **Fases 2-6 pendentes**
- **Auditoria 360° Abr 25**: executada (3 waves), `00-synthesis.md` produzida com 10 achados + roadmap P1-P3, mas **audit wave 2+3 não foi fechada** (validate-corpus pendente)
- **Notebooks**: fig_06–fig_10 collision, environment.yml broken, no random_state — reprodutibilidade ~2/5
- **Batch 3**: SCOUT-415 pendente (precisa lane contra-alegoria), SCOUT-423/SCOUT-206 pendentes
- **Git state**: dirty com 10 arquivos de drafts deletados + `.gitignore` modificado + 6 dirs untracked
- **Vault gap**: 194 candidatos vs 165 corpus items — diferença não mapeada

---

## Meta

Definir a fila de prioridade e iniciar a execução controlada.

---

## Etapa 1 — Verificar estado real do repo

**Executar (terminal):**
```bash
cd ~/iconocracy-corpus
git log --oneline -5          # ver últimos commits
git status --short            # ver estado atual
```

**Se o último commit não incluir T5/cONTRA-ALEGORIA:**
- `git stash` do estado atual
- verificar o que está pendente de commit
- confirmar com a usuária antes de commitar

**Decisão:** Commitar `.gitignore` agora (já aprovado) ou esperar?

---

## Etapa 2 — Fechar auditoria Abr 25

`00-synthesis.md` existe e tem 3 ações propostas:
1. Limpeza dos drafts em `vault/rascunhos-artigos/` ← já feito (arquivos movidos para `archive/notas-legacy/`)
2. Integração teórica Auerburg/Warburg nos Cap 7/8 ← **P2, pendente**
3. build_hf_release.py ← **validar primeiro**

**Executar:**
```bash
conda run -n iconocracy python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose 2>&1 | tail -20
python tools/scripts/vault_sync.py status
python tools/scripts/records_to_corpus.py --diff 2>&1 | tail -10
```

**Se validação passa →** confirmar com usuária se quer build HF release agora.

---

## Etapa 3 — IMES v3.0 Fases 2-6 (thread principal)

Arquivo de referência: `vault/tese/ideias/2026-04-23_ultraplan-transicao-imes.md`

**Fase 1 ✅** (já feito: MASTER_PROMPT v3.0, documento de decisão, SKILL sync)
**Fases pendentes:**
- **Fase 2**: Reescrever Cap. 2 com diagrama IMES
- **Fase 3**: Bump do schema JSON (bloco `imes`)
- **Fase 4**: Mapear 4–6 Regimes Visuais com notas `imes-rv`
- **Fase 5**: Preregistrar 10 pranchas piloto
- **Fase 6**: Reescrever Cap. 1, Cap. 5, Intro, Conclusão + validação adversarial

**Pergunta para a usuária:** Qual fase quer atacar primeiro?

---

## Etapa 4 — Notebook reprodutibilidade

**Problemas críticos:**
1. `fig_06`–`fig_10` collisão entre notebooks 01–04 e 05–08
2. `environment.yml` sem deps (pandas, scipy, seaborn, sklearn, prince, scikit-posthocs)
3. Sem `random_state` em todos os notebooks

**Ação mínima (sem rewrite):**
```bash
cd ~/iconocracy-corpus/notebooks
# Verificar se existe environment.yml
cat environment.yml
# Verificar quais notebooks têm fig_06
grep -l "fig_06" *.ipynb
```

**Resultado:** Relatório do estado atual. Decidir se refaz todos os notebooks ou só renomeia figuras.

---

## Etapa 5 — Batch 3 pendente

**Itens em standby:**
- `SCOUT-415` → designar lane **contra-alegoria** (não promover ao ledger positivo)
- `SCOUT-423` → precisa fonte arquivística mais forte
- `SCOUT-206` → URL/catálogo frágil

**Ação:** Verificar status atual dos 3 items no staging.

---

## Etapa 6 — Wiki ZK garden (`wiki/`)

O novo `wiki/` (Obsidian, 34 entries) é o ZK garden real.
`vault/` tem 194 candidatos — muitos são obsoletos ou duplicados.

**Ação:** `wiki/` precisa de `.gitignore` próprio ou integração no fluxo da tese?
Perguntar à usuária.

---

## Validação Final

Ao final de qualquer sessão de trabalho:
```bash
git status --short
conda run -n iconocracy python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record
```

---

## Riscos e Tradeoffs

| Risco | Mitigação |
|---|---|
| Commits parciais durante trabalho | Sempre verificar `git status` antes de sair |
| Schema quebrado após mudanças | Rodar validate_schemas.py antes de qualquer commit |
| Perda de drafts deletados | Backup já em `archive/notas-legacy/` — não mexer |
| Vault drift (194 vs 165) | `vault_sync.py diff` antes de qualquer escrita no vault |

## Perguntas Abertas

1. Commitar `.gitignore` agora ou esperar?
2. IMES v3.0 — qual fase atacar primeiro?
3. Wikis — integrar `wiki/` no fluxo ou deixar isolado?
4. HF release — quer fazer uma agora que a auditoria passou?
