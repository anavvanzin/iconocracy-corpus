<!-- Generated: 2026-06-22 | Files scanned: 79 tools/scripts/*.py | Token estimate: ~900 -->
# Pipeline — tools/scripts/ by function (79 scripts)

> Run from repo root: `python tools/scripts/<script>.py`. Conda env `iconocracy` (Py 3.12).
> (Replaces "backend/frontend" — this is a data pipeline, not an app server.)

## 1. Acquisition / SCOUT / ARGOS  (archives → vault → ledger)
`gallica_discovery` · `argos_build_manifest` · `argos_prepare_dispatch` · `argos_acquire_item` · `argos_manifest_update` · `argos_report` · `europeana_download` · `loc_download` · `download_corpus_images` · `enrich_iiif` · `enrich_urls_and_regime` · `upload_thumbnails` · `scout_notes` · `lacunas` · `hunt` · `ingest_fichas_lpai` · `csv_to_records` · `classify_support_types[_rich]` · `normalize_supports`

## 2. Coding / IconoCode / Purification  (Panofsky + 10 indicators)
`iconocode_gemma4` · `iconocode_to_corpus` · `code_purification` · `auto_code_purification` · `reconcile_iconocode` · `analyze_purification_drift` · `purify-diff` · `mcp_verify_image` · `atlas_mapping` · `migrate_atlas_schema`
> E1 Fable-5 recode pipeline lives in the `worktree-e1-fable5-recode` branch: `e1_triage_images.py`, `e1_append_batch.py` (+ tests).

## 3. Reliability / IRR  (inter-instrument audit — the analytic-N resolver)
`compute_irr` · `calculate_irr` · `run_irr_pilot` · `select_irr_sample` · `run_iconocracy_eval[_openrouter]` · `compare_iconocracy_eval_runs` · `parallel_compare`

## 4. Sync / canonical data flow
`records_to_corpus` (records→export, **canonical**) · `vault_sync` (vault↔records) · `sync_companion` · `reconcile_data` · `reconcile_iconocode` · `inventory_corpus` · `inventory_report` · `fix_records_schema_issues` · `analytic_corpus` (N-strata, 2026-06-19)

## 5. Validation
`validate_schemas` (all JSON schemas) · `check_corpus_export_idempotent` · `check_thesis_terms` (forbidden terms / misattributions)

## 6. Export / release / dashboards / compile
`build_hf_release` · `refresh_dashboard` · `make_index` · `make_skos` · `make_sqlite` · `abnt_citations` · `render_multimodal_chapters` · `upload_thumbnails`
> Thesis compile is separate: `make -C tese/manuscrito/ {docx,pdf}` (Pandoc).

## 7. ML / dataset / network
`build_iconocracy_sft_dataset` · `split_iconocracy_sft_dataset` · `train_iconocracy_sft` · `extract_feminist_network` (Iconclass 48C51) · `iconocracy_clip` · `semantic_memory_to_schema`

## 8. Infra / automation / misc
`notion_sync` · `sync_github_labels` · `auto_issue` · `log_agent_run` · `update_session_state` · `generate_zettel` · `textbase` · `trace_evidence` · `vault_backup` · `compile_skills` · `prompt_{dedupe,index}` · `mcp_integration` · `iconocontext_daemon` · `audio_transcribe_watcher` · `batch_example`

## Tests
`tests/` (pytest, no config) — `tests/{argos,tools,training}/` + top-level (`test_corpus_export_idempotent`, `test_cross_file_consistency`, `test_run_irr_pilot`, `test_select_irr_sample`, …). E1 tests in worktree: `test_e1_{append_batch,triage_images}` (29 passing).
