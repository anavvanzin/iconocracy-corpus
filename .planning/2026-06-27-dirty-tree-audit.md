# Dirty tree audit - 2026-06-27

## Scope

- Base repo: `/Users/ana/Research/hub/iconocracy-corpus`
- Branch opened for this pass: `codex/audit-pipeline-workflow-2026-06-27`
- Upstream state checked with `git -c core.fsmonitor=false fetch origin`; `main...origin/main` was aligned before the branch was created.
- Goal: classify WIP, keep source-of-truth changes separate from scratch output, improve the DIR410346/article workflow, and prepare a thematic commit plan after gates.

## Keep

These files are candidates for a thematic commit if gates pass:

| Path | Reason | Commit bucket |
| --- | --- | --- |
| `data/processed/records.jsonl` | Ledger expanded from 299 to 328 records via vault import batch. Validated 328/328. | `data(corpus)` |
| `corpus/corpus-data.json` | Regenerated from `records.jsonl` with `tools/scripts/records_to_corpus.py`; now 328 items and synchronized by URL. | `data(corpus)` |
| `corpus/DASHBOARD_CORPUS.html` | Regenerated with `tools/scripts/refresh_dashboard.py --corpus`; now embeds 328 items. | `data(corpus)` |
| `tests/test_validate_schemas.py` | Baseline test follows the new 328-record ledger. | `data(corpus)` |
| `vault/candidatos/BR-051 A Justica (Ceschiatti, 1975) - Escultura interna vandalizada no STF.md` | New candidate note corresponding to the corpus expansion. | `data(corpus)` |
| `vault/candidatos/FR-100 Marianne Mutilada no Arco do Triunfo (Rude, 2018).md` | New candidate note corresponding to the corpus expansion. | `data(corpus)` |
| `vault/candidatos/FR-101 Deborah de Robertis - Performance La Joconde de l Histoire (2018).md` | New candidate note corresponding to the corpus expansion. | `data(corpus)` |
| `docs/decisions/CONTRA-ALEGORIAS-INTEGRATION-2026-06-26.md` | Decision memo records the operational status of the contra-alegorias integration. | `docs(decision)` |
| `tese/manuscrito/sumario_iconocracia.md` | Terminology correction already aligned with thesis vocabulary. | `docs(thesis)` |
| `vault/tese/drafts/sumario-iconocracia.md` | Mirrors the thesis summary terminology correction. | `docs(thesis)` |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/artigo_v0_consolidado.md` | Existing tracked article draft with anti-anachronism corrections. | `docs(article)` |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/progress.md` | Tracks article workflow status. | `docs(article)` |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/task_plan.md` | Tracks article workflow plan. | `docs(article)` |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/artigo_v1_consolidado.md` | Source draft for the article v1; keep as Markdown source after citation cleanup. | `docs(article)` |
| `vault/obsidian-dir410346/Planejamento_Artigo_Duvidam_Punem.md` | Course-facing article plan; align with current anti-anachronism vocabulary. | `docs(dir410346)` |

## Fold Into Docs

These contain useful evidence or reasoning, but should not be committed wholesale as operational scratch:

| Path | Fold target | Note |
| --- | --- | --- |
| `.agents/victory_auditor/victory_audit_report.md` | This audit file and final handoff. | Useful as secondary evidence, but gates must be rerun directly before relying on it. |
| `.agents/orchestrator/handoff.md` and `.agents/orchestrator/plan.md` | Planning/progress docs if still useful. | Review before copying; do not commit the agent workspace as-is. |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/expansao_secoes_1_2.md` | Article planning folder. | Can remain as supporting draft if Ana wants a fuller article dossier. |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/rascunhos/` | Article planning folder. | Drafts are useful but should be staged only if the article dossier intentionally includes them. |
| `genealogia-alegoria-feminina.md` | Future thesis/article memo. | Potentially valuable, but outside this commit's current workflow. |
| `vault/random notes/` | Future codebook/thesis documentation. | Contains Elicit/codebook notes; review individually before moving into canonical docs. |

## Later

These are legitimate artifacts or generated outputs, but not part of the next clean commit unless explicitly chosen:

| Path | Reason |
| --- | --- |
| `corpus/infografico_corpus.pdf` | Binary generated artifact; decide release/storage policy first. |
| `corpus/infografico_gemini.pdf` | Binary generated artifact; decide release/storage policy first. |
| `tools/audit/diagrams/*.pdf` | Generated diagram outputs; stage only with their source/recipe or after release decision. |
| `.planning/2026-06-23-artigo-penal-malleus-cajada/artigo_v1.docx` | Generated from Markdown; keep as delivery artifact, not source-of-truth. |
| `vault/obsidian-dir410346/aulas/assets-apresentacao-malleus/processos_inquisitoriais_bahia_brasil.pdf` | Course asset; keep if intentionally added, but it is separate from article/source cleanup. |
| `wiki/DIR410346-Historia-Direito-Penal/aulas/assets-apresentacao-malleus/processos_inquisitoriais_bahia_brasil.pdf` | Mirrored course asset; decide whether wiki mirrors belong in git. |
| `wiki/relatorios/2026-04-21_relatorio.pdf` | Old report artifact; unrelated to current workflow. |

## Ignore Or Quarantine

Do not stage in a thematic commit without a separate cleanup decision:

| Path pattern | Reason |
| --- | --- |
| `.agents/auditor_1/`, `.agents/explorer_*`, `.agents/self_worker_1/`, `.agents/sentinel/`, `.agents/sourcing_worker/`, `.agents/teamwork_preview_*`, `.agents/worker_*` | Agent scratch/output directories. Preserve for now, but do not commit raw. |
| `.agents/ORIGINAL_REQUEST.md` and nested `ORIGINAL_REQUEST.md` files | Session metadata, not project source. |
| `vault/obsidian-dir410346/{aulas,leituras,memoriais,templates,assets}/...` | Literal brace-expansion paths; likely command artifact. Do not delete without Ana's confirmation, but do not stage. |
| `vault/obsidian-dir410346/aulas/{aulas,leituras,memoriais,templates,assets}/...` | Same brace-expansion artifact under `aulas/`. |
| `wiki/DIR410346-Historia-Direito-Penal/{aulas,leituras,memoriais,templates,assets}/...` | Same brace-expansion artifact in wiki mirror. |
| `wiki/DIR410346-Historia-Direito-Penal/aulas/{aulas,leituras,memoriais,templates,assets}/...` | Same brace-expansion artifact in wiki mirror. |

## Current Risks

1. Remaining untracked PDF and wiki mirror files may be valid deliverables, but they would make a noisy commit if mixed with corpus/article changes.
2. The `.agents/*` directories and literal brace-expansion paths should be quarantined or ignored only after Ana confirms cleanup policy.
3. `code_purification.py --status` still reports 299 total items in `purification.jsonl`; this is not a schema failure, but it means the 29 imported records are not yet coded in the endurecimento ledger.

## Gate Plan

Run before staging:

```bash
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/validate_schemas.py
/Users/ana/.venvs/iconocracy/bin/python3.12 -m pytest tests/test_validate_schemas.py
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/check_thesis_terms.py
git -c core.fsmonitor=false diff --check
rg -n "Cães de Guarda|narrativaç|embrutecimento|hardening|construção atlântica do tipo penal|tipo penal de bruxaria|práticas indígenas.*candomblé|quimbanda|jurema preta|curandeira de terreiro" \
  .planning/2026-06-23-artigo-penal-malleus-cajada/artigo_v0_consolidado.md \
  .planning/2026-06-23-artigo-penal-malleus-cajada/artigo_v1_consolidado.md \
  .planning/2026-06-23-artigo-penal-malleus-cajada/secao4_circulacao_atlantica.md \
  vault/obsidian-dir410346/Planejamento_Artigo_Duvidam_Punem.md
```

Optional read-only release checks:

```bash
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/records_to_corpus.py --diff
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/code_purification.py --status
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/vault_sync.py status
```

## Gate Results - 2026-06-27

```text
validate_schemas.py: 328/328 records valid
validate_records() warnings: 0
pytest tests/test_validate_schemas.py: 5 passed
records_to_corpus.py --diff: records.jsonl 328, corpus-data.json 328, synchronized by URL
json.tool corpus/corpus-data.json: ok
refresh_dashboard.py --corpus: 328 items
check_thesis_terms.py: thesis terms ok
git diff --check: ok
targeted article term scan: no hits
code_purification.py --status: 236/299 coded, 63 remaining, new imported records still outside purification ledger
vault_sync.py status: records 328, vault notes 360
markdownlint: not run, `markdownlint` and `markdownlint-cli` absent from PATH
```

## Commit Strategy

Recommended split:

1. `data(corpus): sync vault import to 328 records`
   - Stage ledger, corpus export, dashboard, validator test, candidate notes, and decision memo.
2. `docs(article): advance Malleus-Cajada workflow`
   - Stage article v0/v1, modular Section 4, progress, task plan, DIR410346 planning, thesis-summary terminology updates, and this audit.
3. Later cleanup commit only after confirmation:
   - Quarantine or ignore `.agents/*`, brace-expansion paths, generated PDFs, and wiki mirror artifacts.
