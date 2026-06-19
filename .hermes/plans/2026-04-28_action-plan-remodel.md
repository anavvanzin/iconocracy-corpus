# Action Plan — ICONOCRACY Remodel + Pipeline Catch-up

**Date:** 2026-04-28
**Branch:** iconocracy-research-materials-clean
**Repo state:** clean working tree, origin → SSD mirror

## Completed (remodel)

| # | Item | Commit |
|---|------|--------|
| 1 | GitHub surfaces removed (.github/, workflows, templates) | 2c1687f |
| 2 | Legacy drafts moved to archive/ + audit docs preserved | f1cb284 |
| 3 | AGENTS.md + CLAUDE.md updated (Local-SSD-HF surfaces) | 1ec3ee5 |
| 4 | Backup script tools/scripts/backup_iconocracy.sh | ee2dff8 |
| 5 | vault/tese/artigos/ (Mute Granite) + wiki/ gitignored | d8eed16 |

**SSD Mirror:** `/Volumes/ICONOCRACIA/git-mirrors/iconocracy-corpus.git`
**Backup cmd:** `cd ~/Research/hub/iconocracy-corpus && bash tools/scripts/backup_iconocracy.sh`

---

## Pending (Etapa 2–5 from original review)

### Etapa 2 — Fechar auditoria Abr 25
- [ ] `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`
- [ ] `python tools/scripts/vault_sync.py status`
- [ ] `python tools/scripts/records_to_corpus.py --diff`
- [ ] Decidir: `build_hf_release.py` agora?

### Etapa 3 — IMES v3.0 Fases 2–6
Reference: `docs/2026-04-26-ultraplan.md`
- [ ] Fase 2: Reescrever Cap. 2 com diagrama IMES
- [ ] Fase 3: Bump schema JSON (bloco `imes`)
- [ ] Fase 4: Mapear 4–6 Regimes Visuais com notas `imes-rv`
- [ ] Fase 5: Preregister 10 pranchas piloto
- [ ] Fase 6: Reescrever Cap. 1, 5, Intro, Conclusão + adversarial

### Etapa 4 — Notebook reprodutibilidade
- [ ] Verificar collisão fig_06–fig_10 entre notebooks 01–04 e 05–08
- [ ] Adicionar random_state
- [ ] Corrigir environment.yml (pandas, scipy, seaborn, sklearn, prince, scikit-posthocs)

### Etapa 5 — Batch 3 itens pendentes
- [ ] SCOUT-415 → designar lane contra-alegoria
- [ ] SCOUT-423 → verificar fonte arquivística
- [ ] SCOUT-206 → verificar URL/catálogo

---

## New untracked question (Hermes install)

User asked about installing Hermes from source (`git clone https://github.com/NousResearch/hermes-agent`) and starting gateway on :8642.

Hermes appears to be already installed and running on the user's Mac (session active). Verify current installation before giving install instructions.
