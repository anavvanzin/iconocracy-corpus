# Revisão de Branches — 2026-06-11

Auditoria de status de **todos os branches remotos** dos 4 repositórios do ecossistema ICONOCRACIA, com recomendação por branch. O corpo do relatório (até o checklist de ações) foi produzido em modo **report-only**: levantamento e recomendações, sem executar nada. Em seguida, **com autorização explícita de Ana na mesma sessão**, parte das ações foi executada — ver a seção **"Status de execução — 2026-06-11"** ao final, que registra exatamente o que foi merged/resgatado e o que permanece pendente ou bloqueado.

**Metodologia:** fetch completo de refs; por branch: último commit, ahead/behind vs `main`, diffstat vs merge-base, teste de ancestralidade (`merge-base --is-ancestor`), sonda de conflito (`git merge-tree --write-tree`); mapeamento contra PRs abertos/fechados/merged via API GitHub; CI via check-runs do head de cada PR aberto.

---

## Sumário executivo

**31 branches** (27 além dos 4 `main`) · **14 PRs abertos** (10 corpus, 3 research, 1 iuris-visio).

| Achado | Branches |
|---|---|
| 🔴 **Trabalho vivo não-mergeado em branch "já merged"** (risco de perda em limpeza ingênua) | `data/reacquire-images-batch2-iiif-20260609` (+2.238 linhas, 06-10), `reconcile/ssd-scripts-2026-06-04` (+2.169, 06-08), `Research:copilot/fix-research-commit-issues` (+2.075, 04-15) |
| 🔀 **Merge-ready** (CI verde, sem conflito) | corpus #74, #70, #67, #60 · research #9, #10 |
| 🛠 **Precisam rebase** (conflitos com main) | corpus #63, #64 · research #4 |
| ⚠️ **Não mergear ainda** | iuris-visio #1 (vitest 2→4 **major** + check `lint` **falhando**) |
| ✅ **Deleção segura** (conteúdo 100% em main) | corpus: `copilot/review-session-history`, `dialectic-cycle-1`, `iconocracy-research-materials-2026-04-25` · iuris-visio: `claude/thesis-articles-planning-J6YD6` |
| 🗃 **Obsoletos / salvage-audit antes de apagar** | corpus: `copilot/fix-irregularities-in-data`, `infra/hub-consistency-refactor`, `copilot/create-implementation-plan`, `reconcile/ssd-scripts-clean`, `iconocracy-research-materials-clean` · PR #23 (Hono) |
| 🧊 **Decisão de Ana** | corpus #13 (`claude/sad-roentgen`, **sem merge-base com main**), #52, #30 (`research/workspace-map`, 255 arquivos) |
| 📄 **Abrir PR** | `docs/prp-plans-2026-06` (trabalho recente sem PR) |

Branch de sessão `claude/blissful-keller-6tfahg` existe nos 4 clones (== main; carrega este relatório) — excluído da auditoria.

---

## 1. iconocracy-corpus (22 branches, 10 PRs abertos)

### 1.1 PRs abertos

| PR | Branch | Estado | Idade | CI | Conflito? | Recomendação |
|---|---|---|---|---|---|---|
| #74 | `copilot/health-check-semanal-2026-06-08` | draft | 06-08 | ✅ verde | limpo | 🔀 Revisar (toca ledgers → rodar `validate_schemas.py` local), un-draft e **merge** |
| #70 | `copilot/track-purification-backlog-…` | draft | 06-08 | ✅ verde | limpo | 🔀 **Merge prioritário** — manifesto do backlog dos itens sem codificação de endurecimento; pré-requisito operacional da decisão pendente do N analítico (`docs/decisions/DIALETICA-N165-vs-265.md`) |
| #67 | `dependabot/npm_and_yarn/deploy/iconocracia-companion/…` | ready | 06-08 | ✅ verde | limpo | 🔀 **Merge** (deps do companion) |
| #64 | `fix/export-contract-56` | ready | 05-31 | — | **conflita** | 🛠 **Rebase e merge** — restaura `id/country/support/year` no contrato de export (#56); alto valor, 1 commit |
| #63 | `fix/protobufjs-7.5.6` | ready | 05-31 | — | **conflita** | 🛠 Segurança. `/shared` já foi corrigido (#50/#51); este cobre o companion. **Rebase e merge** (ou fechar se Socket já não acusa nada in main) |
| #60 | `docs/archive-reconcile-plan-2026-05-24` | ready | 05-24 | ✅ verde | limpo | 🔀 **Merge** (1 doc, +526) |
| #52 | `claude/decide-next-steps-v2mE3` | draft | 05-17 | — | **conflita** | 🧊 Consolidação editorial + higiene de notebooks; 49 atrás. **Decidir:** rebase e concluir, ou extrair só a higiene de `PENDING_REVIEW` e fechar |
| #30 | `research/workspace-map` | draft | 04-14 (ativo até 06-08) | — | **conflita** | 🧊 **Decisão.** 68 commits / 255 arquivos misturando fixes de aquisição (04-25, possivelmente supersedidos pelo ARGOS em main) + docs. ⚠️ contém `deploy/iconocracia-companion/.wrangler/cache/wrangler-account.json` commitado (higiene). Sobrepõe `docs/prp-plans-2026-06` (workspace-map reescrito lá). Sugestão: dividir — docs reconciliados com prp-plans; fixes de pipeline auditados contra main; depois fechar |
| #23 | `copilot/migrate-worker-routing-to-hono` | ready | 04-10 | — | **conflita** | 🗃 **Fechar** — superseded arquiteturalmente: o Hono/API agora é responsabilidade do repo `iuris-visio-roadmap` (ver tabela de responsabilidades no CLAUDE.md de lá); 124 atrás |
| #13 | `claude/sad-roentgen` | ready | 04-03 | — | **sem merge-base** | 🧊 **Histórico não relacionado ao main atual** (157 commits desde o corpus inicial de 33 itens; 34 arquivos / 21k linhas em corpus+data). Tentativa de merge já falhou (#17, fechado). Curadoria parcial já feita via #59 (7 KEEP / 7 HOLD / 5 REJECT) e há PRP de reingest em `docs/prp-plans-2026-06`. **Congelar como arquivo até o reingest concluir; então fechar #13** (apagar branch só depois de auditar os 43 itens contra `records.jsonl`) |

### 1.2 Branches "merged" com trabalho vivo pós-merge — ⚠️ NÃO APAGAR

| Branch | Situação | Conteúdo novo (não está em main) | Recomendação |
|---|---|---|---|
| `data/reacquire-images-batch2-iiif-20260609` | PR #76 squash-merged 06-10; branch foi **rebasado e estendido depois** | 3 commits (06-09/06-10, +2.238 linhas): `e1_pathosformel_batch.py`, `e1_recode_zeros.py`, `e3_firecrawl_recode.py`, scaffold Cap. 1 (`tese/compilacao-2026-06-09/`), edições `capitulo-6`, e 3 decision docs: `audit-coded-by-2026-06-10.md`, `IRR-INTER-INSTRUMENTO-2026-06-10.md`, `IRR-RE-RUN-DESIGN-2026-06-09.md` | 🔴 **Trabalho mais recente do repo.** Cherry-pick dos 3 commits finais para novo branch → PR próprio → só então apagar. Os decision docs alimentam diretamente a decisão pendente do N analítico |
| `reconcile/ssd-scripts-2026-06-04` | PR #66 squash-merged 06-05; **7 commits depois** (06-07/06-08) | +2.169/-487 em 18 arquivos: pipeline v2.0 (`release.sh`, `deploy_companion.sh`), `fix_drive_import_records.py` (normaliza os 43 registros drive-import!), fixes `vault_sync`/`records_to_corpus`, expansão `capitulo-7`, docker fixes. ⚠️ toca `records.jsonl`/`corpus-data.json` e usa caminhos antigos `vault/tese/` (pré-reorg 06-04) | 🔴 Salvage por cherry-pick seletivo em novo PR (scripts primeiro; dados regenerados via pipeline, não via blob; capítulo-7 portado para `tese/manuscrito/drafts/`). Depois apagar |

### 1.3 Branches sem PR

| Branch | Último commit | Conteúdo | Recomendação |
|---|---|---|---|
| `docs/prp-plans-2026-06` | 06-08 | PRPs: codificar 52 uncoded (#57) + reingest 7 KEEP (#59); reescrita do workspace-map como contrato; alinhamento `OPERATING_MODEL`/`CLAUDE.md`. Conflita (churn de CLAUDE.md) | 📄 **Rebase e abrir PR** — trabalho recente e central ao backlog de purificação. Reconciliar com #30 antes |
| `copilot/create-implementation-plan` | 04-25 | `upload_thumbnails.py` (já em main via #46) + `tese/anchors/historian-1910-1920-br.md` (+305, **só aqui**) | 🗃 Cherry-pick do arquivo de anchors → apagar branch |
| `copilot/fix-irregularities-in-data` | 04-15 | 17 commits "kitchen-sink": Hono, script CLIP, pipeline SFT, infra IRR double-blind, planos de tese. 124 atrás, conflita | 🗃 Salvage-audit dirigido (infra IRR vs decision docs atuais; CLIP vs `iconocracy_clip.py` de main) → fechar/apagar. Baixa prioridade |
| `infra/hub-consistency-refactor` | 04-17 | 19 commits: taxonomia do hub, fixes vault_sync, BibTeX Cap. 3, promoção de scout batch, **5 commits de vault backup** (violariam a regra "backups não vão a main") | 🗃 Largamente superseded pela reorg 2026-06-04. Salvage-audit (BibTeX Cap. 3) → apagar |
| `reconcile/ssd-scripts-clean` | 06-04 | Regenera `corpus-data.json` 264→265 (+SCOUT-414) — **exatamente o drift de 1 item documentado em Known Data Issues** — + CSV N=265 + port do matching difflib. Conflita (JSON churned) | 🛠 **Não mergear o blob JSON.** Rebase dos scripts e **re-rodar o pipeline em main** (`records_to_corpus.py`) para fechar o drift; depois apagar |
| `iconocracy-research-materials-clean` | 04-25 | PR #44 fechado sem merge; diff líquido: 2 arquivos, **-1 linha** | ✅ Apagar |
| `copilot/review-session-history` | 06-05 | ancestral de main (0 à frente) | ✅ Apagar |
| `dialectic-cycle-1` | 04-25 | PR #41 merged; ancestral de main | ✅ Apagar |
| `iconocracy-research-materials-2026-04-25` | 04-25 | ancestral de main | ✅ Apagar |

---

## 2. Research (5 branches, 3 PRs abertos)

| Branch | PR | Estado | Recomendação |
|---|---|---|---|
| `dependabot/npm_and_yarn/cowork/ws-8.20.1` | #10 | CI ✅, limpo | 🔀 **Merge** — patch de segurança do `ws` (vazamento de memória não inicializada em `close()`) |
| `claude/debian-research-setup-FXiPM` | #9 (draft) | CI ✅, limpo, +1.979 (docs onboarding Debian 12) | 🔀 Un-draft e **merge** quando Ana validar o pacote (é só documentação/scripts novos; merge limpo) |
| `claude/wire-self-improving-agent` | #4 (draft, 04-23) | CI ✅, **conflita** (arquivos do agente evoluíram in main) | 🛠 Rebase + verificar se o wiring (`.claude/settings.json` hooks) ainda é desejado; senão fechar |
| `copilot/fix-research-commit-issues` | #1 **merged** 04-15, mas **10 commits pós-merge** | +2.075 linhas; código do agente superseded (main tem versões mais novas), mas **só aqui**: `docs/imported/` (7 docs + README), `self-improving-agent-summary.md`, `.learnings/*`, `blank.yml` | 🔴 Salvage de `docs/imported/` + summary via cherry-pick/PR novo → apagar branch |

---

## 3. iuris-visio-roadmap (3 branches, 1 PR aberto)

| Branch | PR | Estado | Recomendação |
|---|---|---|---|
| `dependabot/npm_and_yarn/npm_and_yarn-4825ac1e2e` | #1 | merge limpo, **mas check `lint` FALHOU** e `test`/`deploy` skipped | ⚠️ **Não mergear.** vitest 2.1.9 → 4.1.8 é salto de 2 majors; investigar o lint, rodar `vitest` localmente contra `vitest.config.ts` antes de decidir |
| `claude/thesis-articles-planning-J6YD6` | — | ancestral de main; main **removeu deliberadamente** a infra thesis-articles depois (348dc84) | ✅ Apagar (histórico preservado no git) |

---

## 4. new.companion.thesis (1 branch)

Apenas `main` (último commit 06-10, `google-cloudrun-source.yml`). Nada a revisar. ✅

---

## Status de execução — 2026-06-11 (autorizado por Ana na mesma sessão)

**Fase 2 — merges (squash): ✅ EXECUTADA.** #74 → `3fafb0a` · #70 → `326a57f` · #60 → `6b00500` · #67 → `4edb641` · Research #10 → `7b3b3ac`. Verificação pós-merge: `validate_schemas.py` in main → **308/308 válidos** (antes do #74, main estava com 43 registros drive-import inválidos — 265/308). Research #9 segue aberto aguardando validação de Ana.

**Fase 3 — resgates: ✅ EXECUTADA (4 PRs draft abertos).**
| PR | Conteúdo |
|---|---|
| [#78](https://github.com/anavvanzin/iconocracy-corpus/pull/78) | E1/E3 pathosformel + 3 decision docs (coded_by/IRR) + scaffold Cap. 1 — cherry-picks limpos de `batch2-iiif` |
| [#79](https://github.com/anavvanzin/iconocracy-corpus/pull/79) | Pipeline v2.0 — só scripts de `reconcile/ssd-scripts-2026-06-04` (dados e `vault/tese/` excluídos) |
| [#80](https://github.com/anavvanzin/iconocracy-corpus/pull/80) | Âncora historiográfica BR 1910–1920 |
| [Research #12](https://github.com/anavvanzin/Research/pull/12) | `docs/imported/` + sumário do self-improving-agent |

**Fase 1 — deleções: ⛔ BLOQUEADA pelo ambiente remoto** (proxy git recusa `--delete` com HTTP 403; sem `gh` CLI nem tool de API para refs). As 5 deleções re-verificadas ficam para execução local de Ana (comandos na Fase 1 acima). Após mergear #78/#79/#80/#12, adicionar à lista: `data/reacquire-images-batch2-iiif-20260609`, `reconcile/ssd-scripts-2026-06-04`, `copilot/create-implementation-plan`, `Research:copilot/fix-research-commit-issues`.

**Itens 3.5/3.6 — NÃO executados, com achado novo:** o preview do export (`records_to_corpus.py --diff`, com o fix de itens sem URL do #79) revela **~38 registros sem URL** agora exportáveis **+ 7 itens existentes só em corpus-data.json** (`sq1/sq2-2026-05-19-*`, reingest #59) — deriva reversa contra a hierarquia canônica. A regeneração deixou de ser mecânica; tratar junto do PRP de reingest (`docs/prp-plans-2026-06`) e da decisão do N analítico.

**⚠️ Gate de consistência do CI está vermelho por deriva pré-existente em main:** o passo "records.jsonl / corpus-data.json consistency" de `validate.yml` falha com **308 vs 314** — estado herdado de main *antes* dos merges de hoje (verificado em `f614232`: corpus-data já tinha 314; #70 preservou a contagem). Consequência: **todo PR que toque os paths monitorados terá `validate` vermelho** (caso dos resgates #78/#79/#80) até a reconciliação 308↔314 — que é exatamente a decisão de deriva reversa acima. Os PRs de resgate estão corretos em conteúdo; o vermelho é herdado.

**Nota Socket (#78):** alerta "obfuscated code" em `as-table@1.0.55` (transitiva) apareceu no diff-scan após o update de base trazer os bumps do #67 para o branch — pacote já está in main via #67, não foi introduzido pelo resgate. Triagem no dashboard Socket fica a critério de Ana (não suprimi o alerta).

**Correções ao snapshot da auditoria:** `records.jsonl` está em **308** registros (não 265 — os 43 drive-import entraram via #75/#76); a seção *Known Data Issues* do `CLAUDE.md` (auditada em 05-24) está desatualizada nos números e merece revisão.

**Pendentes (Fases 4–5):** rebases de #64, #63 e Research #4 (exigem push nos branches originais — fora do alcance deste ambiente); decisões de #13, #52, #30, #23, iuris-visio #1 (lint do bump vitest), salvage-audits de `fix-irregularities-in-data` e `infra/hub-consistency-refactor`.

---

## Atualização — 2026-06-15 (decisões de Ana)

- **Research #12 → ✅ MERGED** (`d6470f8`, squash). `docs/imported/` + sumário do agente preservados em `Research:main`. Branch `rescue/imported-docs-20260611` fica elegível para deleção (junto da lista da Fase 1, ainda bloqueada pelo proxy).
- **Gate 308↔314 → decisão: NÃO mexer em dado canônico agora; dobrar na linha de reingest.** A deriva reversa (export `corpus-data.json` = 314 carrega ~6–7 itens *uncoded* — `coded_by=''` — sem registro canônico em `records.jsonl` = 308; vários são *fontes* iconográficas, p.ex. edições da *Iconologia* de Ripa, SMK, páginas de museus BR) será tratada como parte do PRP de reingest #59 / decisão do N analítico (`docs/prp-plans-2026-06`, `docs/decisions/DIALETICA-N165-vs-265.md`), **não** como conserto mecânico de CI. Consequência aceita: **#78 e #79 permanecem draft** com `validate` vermelho herdado até essa reconciliação; o vermelho é de contagem, não de conteúdo (ambos os resgates estão corretos).
- **Revisão Copilot em #77 → resolvida.** Contradição "report-only" na abertura corrigida; comentário do `labeler.yml` endurecido. Confirmado contra os READMEs oficiais do `actions/labeler`: o formato do `@v4` fixado é **lista de globs por rótulo** (config atual correta); a sugestão de migrar para `changed-files`/`any-glob-to-any-file` is sintaxe **v5** e quebraria o `@v4` — rebatida com evidência, threads resolvidas. (v5 também é `node20`; bump de major não resolve a depreciação do Node 20 — fica para PR próprio.)

### Fase 4 (rebases) — investigada 2026-06-15; resultado: nenhum rebase cego

Ana liberou force-push dos 3 branches. A investigação mostrou que **nenhum deles deve ser rebasado às cegas**:

- **#63 `fix/protobufjs-7.5.6` → ✅ FECHADO (superseded).** `main` já fixa `overrides: protobufjs ^7.5.6 / @protobufjs/utf8 ^1.1.1` (via #51) — rebase seria no-op. Fechado com comentário; reabrir se o Socket reacusar.
- **#64 `fix/export-contract-56` → manter aberto; re-portar na linha de reingest.** `main` reescreveu `records_to_corpus.py` independentemente e já implementa o `id` do #56 (via `_extract_id_from_record` + `id-mapping.json`), mas **ainda não emite `country/support/year`**. O valor restante do #64 (country via `COUNTRY_BY_PREFIX`/id-mapping + support + year) precisa ser **re-implementado sobre a função atual de `main`**, não resgatado por conflito — e como regenera o export, pertence ao mesmo bundle do gate 308↔314 (mesmo script). Rebase abortado. Folded na linha de reingest.
- **Research #4 `claude/wire-self-improving-agent` → decisão de Ana.** Rebase cego regrediria os 5 arquivos do agente (versões mais novas in `main`). Porém o **valor real** — `.claude/settings.json` que ativa os hooks — é **limpo e aditivo**: os 4 scripts referenciados já existem in `main` e `main` não tem `settings.json`. Salvável via cherry-pick **só do `settings.json`**. Pendente: ativar a automação (hooks em todo tool-call) é mudança de comportamento → requer consentimento.

---

*Auditoria: 2026-06-11 · fontes: GitHub API (branches, PRs #1–#76, check-runs) + git local (fetch completo dos 4 clones). Relatório gerado em sessão Claude Code; seção de execução adicionada após autorização explícita na mesma sessão.*
