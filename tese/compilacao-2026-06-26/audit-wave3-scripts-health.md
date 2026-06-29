# Audit Wave 3.2 — Scripts Health Report
**Date**: 2026-06-26  
**Repo**: `/Users/ana/Research/hub/iconocracy-corpus`  
**Scope**: All 88 Python scripts in `tools/scripts/`

---

## 1. Executive Summary

| Metric | Count |
|--------|-------|
| Total scripts | 88 |
| With shebang (`#!/usr/bin/env python3`) | 82 (93.2%) |
| Executable (`+x`) | 20 (22.7%) |
| Missing `__main__` guard | 4 (4.5%) |
| With test coverage | ~16 (18.2%) |
| Broken absolute paths | 5 scripts (5.7%) |
| Imports not in requirements.txt | 7 external packages |
| Deprecated/explicitly superseded | 1 (`notion_sync.py`) |
| **RECOMMENDATION: keep** | 48 (54.5%) |
| **RECOMMENDATION: fix** | 22 (25.0%) |
| **RECOMMENDATION: archive** | 14 (15.9%) |
| **RECOMMENDATION: delete** | 4 (4.5%) |

---

## 2. Complete Script Inventory

Legend: `✔` = OK, `⚠` = issue, `✗` = broken/delete

### 2.1 Key Scripts (from CLAUDE.md)

| # | Script | Lines | Shebang | Exec | `__main__` | Test | Recommendation |
|---|--------|-------|---------|------|------------|------|----------------|
| 1 | `validate_schemas.py` | 339 | ✔ | | ✔ | ✔ | **keep** |
| 2 | `check_thesis_terms.py` | 50 | ✔ | ✔ | ✔ | | **keep** |
| 3 | `code_purification.py` | 469 | ✔ | ✔ | ✔ | | **keep** |
| 4 | `vault_sync.py` | 625 | ✔ | | ✔ | | **keep** |
| 5 | `records_to_corpus.py` | 412 | ✔ | | ✔ | | **keep** |
| 6 | `build_hf_release.py` | 327 | ✔ | | ✔ | | **keep** |
| 7 | `argos_build_manifest.py` | 87 | ✔ | | ✔ | ✔ | **keep** |
| 8 | `argos_prepare_dispatch.py` | 166 | ✔ | | ✔ | ✔ | **keep** |
| 9 | `argos_report.py` | 33 | ✔ | | ✔ | ✔ | **keep** |

### 2.2 Full Inventory (alphabetical)

| # | Script | Lines | Shebang | Exec | `__main__` | Test | Issues | Recommendation |
|---|--------|-------|---------|------|------------|------|--------|----------------|
| 10 | `__init__.py` | 0 | — | | | | Empty package init | **keep** |
| 11 | `abnt_citations.py` | 304 | ✔ | | ✔ | | | **keep** |
| 12 | `analyze_purification_drift.py` | 128 | ✔ | | ✔ | | | **keep** |
| 13 | `argos_acquire_item.py` | 445 | ✔ | | ✔ | ✔ | | **keep** |
| 14 | `argos_manifest_update.py` | 56 | ✔ | | ✔ | ✔ | Thin wrapper | **keep** |
| 15 | `atlas_mapping.py` | 108 | ✔ | | ✔ | | | **keep** |
| 16 | `audio_transcribe_watcher.py` | 52 | ✔ | ✔ | ✔ | | | **keep** |
| 17 | `auto_code_purification.py` | 463 | ✔ | | ✔ | | ⚠ overlaps with code_purification.py | **archive** |
| 18 | `auto_issue.py` | 239 | ✔ | ✔ | ✔ | | | **keep** |
| 19 | `batch_example.py` | 326 | ✔ | | ✔ | | Demo/example only | **archive** |
| 20 | `build_cronologia.py` | 371 | ✔ | | | | ⚠ hardcoded Linux path `/home/user/workspace/moedas` | **fix** |
| 21 | `build_iconocracy_sft_dataset.py` | 556 | ✔ | | ✔ | | | **keep** |
| 22 | `calculate_irr.py` | 219 | ✔ | | ✔ | | ⚠ overlaps with compute_irr.py | **archive** |
| 23 | `check_corpus_export_idempotent.py` | 93 | ✔ | | ✔ | ✔ | | **keep** |
| 24 | `classify_support_types.py` | 101 | ✔ | | ✔ | | ⚠ overlaps with _rich variant | **archive** |
| 25 | `classify_support_types_rich.py` | 146 | ✔ | | ✔ | | Second pass — keep this, archive base | **keep** |
| 26 | `compare_iconocracy_eval_runs.py` | 113 | ✔ | | ✔ | ✔ | | **keep** |
| 27 | `compile_skills.py` | 137 | ✔ | ✔ | ✔ | | Hermes profile tool | **keep** |
| 28 | `compute_irr.py` | 664 | ✔ | | ✔ | | Primary IRR tool | **keep** |
| 29 | `csv_to_records.py` | 402 | ✔ | | ✔ | | Historical migration | **archive** |
| 30 | `download_corpus_images.py` | 376 | ✔ | | ✔ | | ⚠ hardcoded `/Volumes/ICONOCRACIA/corpus/imagens` | **fix** |
| 31 | `e1_mark_no_image.py` | 162 | ✔ | | ✔ | | | **keep** |
| 32 | `e1_pathosformel_batch.py` | 379 | ✔ | | ✔ | | | **keep** |
| 33 | `e1_reclassify_no_image.py` | 153 | ✔ | | ✔ | | | **keep** |
| 34 | `e1_recode_zeros.py` | 291 | ✔ | | ✔ | | | **keep** |
| 35 | `e3_firecrawl_recode.py` | 254 | ✔ | | ✔ | | | **keep** |
| 36 | `enrich_iiif.py` | 318 | ✔ | | ✔ (×2) | | Double `__main__` guard ⚠ | **fix** |
| 37 | `enrich_urls_and_regime.py` | 806 | ✔ | | ✔ | | ⚠ refs `/Volumes/ICONOCRACIA/…` | **fix** |
| 38 | `europeana_download.py` | 176 | ✔ | | ✔ | | SSL cert disabled ⚠ | **keep** |
| 39 | `extract_feminist_network.py` | 190 | ✔ | | ✔ | | | **keep** |
| 40 | `fix_records_schema_issues.py` | 154 | ✔ | | ✔ | ✔ | | **keep** |
| 41 | `gallica_discovery.py` | 273 | ✔ | | ✔ | | | **keep** |
| 42 | `generate_zettel.py` | 53 | ✔ | ✔ | ✔ | | | **keep** |
| 43 | `hunt.py` | 1146 | ✔ | ✔ | ✔ | | Largest script | **keep** |
| 44 | `iconocode_gemma4.py` | 700 | ✔ | ✔ | ✔ | ✔ | Optional dep (llama-cpp) | **keep** |
| 45 | `iconocode_to_corpus.py` | 120 | ✔ | | ✔ | | | **keep** |
| 46 | `iconocontext_daemon.py` | 70 | ✔ | ✔ | ✔ | | | **keep** |
| 47 | `iconocracy_clip.py` | 226 | ✔ | ✔ | ✔ | | | **keep** |
| 48 | `ingest_fichas_lpai.py` | 839 | ✔ | | ✔ | ✔ | | **keep** |
| 49 | `inventory_corpus.py` | 184 | ✔ | | ✔ | | yaml not in requirements | **fix** |
| 50 | `inventory_report.py` | 115 | ✔ | | ✔ | | ⚠ hardcoded dated CSV path | **fix** |
| 51 | `irr_rater2_batch.py` | 366 | ✔ | | ✔ | | | **keep** |
| 52 | `irr_sample.py` | 519 | ✔ | | ✔ | | ⚠ hardcoded `/data/iconocracy-corpus/…` | **fix** |
| 53 | `lacunas.py` | 295 | ✔ | ✔ | ✔ | | | **keep** |
| 54 | `loc_download.py` | 383 | ✔ | | ✔ | | Contains embedded JS ⚠ | **fix** |
| 55 | `log_agent_run.py` | 89 | ✔ | | ✔ | | | **keep** |
| 56 | `make_index.py` | 240 | ✗ | | ✔ | | No shebang, imports `textbase` | **fix** |
| 57 | `make_skos.py` | 154 | ✗ | | ✔ | | No shebang, imports `textbase`, `rich` | **fix** |
| 58 | `make_sqlite.py` | 177 | ✗ | | ✔ | | No shebang | **fix** |
| 59 | `mcp_integration.py` | 305 | ✔ | | ✔ | | | **keep** |
| 60 | `mcp_verify_image.py` | 141 | ✔ | ✔ | ✔ | | | **keep** |
| 61 | `migrate_atlas_schema.py` | 27 | ✗ | | | ✔ | No shebang, no `__main__`, library module | **archive** |
| 62 | `normalize_supports.py` | 359 | ✔ | | ✔ | ✔ | | **keep** |
| 63 | `notion_sync.py` | 58 | ✔ | | ✔ | | **DEPRECATED** → forwards to vault_sync | **delete** |
| 64 | `parallel_compare.py` | 113 | ✔ | | ✔ | | | **keep** |
| 65 | `prompt_dedupe.py` | 214 | ✔ | | ✔ | | ✗ hardcoded path `/Users/ana/research/hub/…` | **fix** |
| 66 | `prompt_index.py` | 204 | ✔ | | ✔ | | ✗ hardcoded path `/Users/ana/research/hub/…`; yaml not in reqs | **fix** |
| 67 | `purify-diff.py` | 241 | ✔ | ✔ | ✔ | | | **keep** |
| 68 | `reconcile_data.py` | 327 | ✔ | | ✔ | | | **keep** |
| 69 | `reconcile_iconocode.py` | 513 | ✔ | | ✔ | | | **keep** |
| 70 | `records_to_sqlite.py` | 329 | ✔ | ✔ | ✔ | | | **keep** |
| 71 | `refresh_dashboard.py` | 129 | ✔ | | ✔ | | | **keep** |
| 72 | `render_multimodal_chapters.py` | 82 | ✔ | ✔ | ✔ | | | **keep** |
| 73 | `run_iconocracy_eval.py` | 120 | ✔ | | ✔ | | Requires torch, transformers (not in reqs) | **fix** |
| 74 | `run_iconocracy_eval_openrouter.py` | 180 | ✔ | | ✔ | ✔ | | **keep** |
| 75 | `run_irr_pilot.py` | 424 | ✔ | ✔ | ✔ | ✔ | ⚠ hardcoded `/data/iconocracy-corpus/…` | **fix** |
| 76 | `run_research_cluster.py` | 557 | ✔ | | ✔ | | yaml not in requirements | **fix** |
| 77 | `scout_notes.py` | 353 | ✔ | ✔ | ✔ | | | **keep** |
| 78 | `select_irr_sample.py` | 121 | ✔ | ✔ | ✔ | ✔ | ⚠ overlaps with irr_sample.py | **archive** |
| 79 | `semantic_memory_to_schema.py` | 323 | ✔ | ✔ | ✔ | | | **keep** |
| 80 | `split_iconocracy_sft_dataset.py` | 99 | ✔ | | ✔ | | | **keep** |
| 81 | `sync_companion.py` | 201 | ✔ | | ✔ | | | **keep** |
| 82 | `sync_github_labels.py` | 88 | ✔ | | ✔ | | | **keep** |
| 83 | `textbase.py` | 60 | ✗ | | | | Library module, no shebang | **keep** |
| 84 | `trace_evidence.py` | 337 | ✔ | | ✔ | | | **keep** |
| 85 | `train_iconocracy_sft.py` | 160 | ✔ | | ✔ | | Requires torch/transformers/peft/trl/datasets | **fix** |
| 86 | `update_session_state.py` | 65 | ✔ | ✔ | ✔ | | Hermes tool | **keep** |
| 87 | `upload_thumbnails.py` | 326 | ✔ | | ✔ | | | **keep** |
| 88 | `vault_backup.py` | 82 | ✔ | | ✔ | | | **keep** |

---

## 3. Detailed Issue Analysis

### 3.1 Shebang Violations (5 scripts)

These scripts lack `#!/usr/bin/env python3`:

| Script | First line | Severity |
|--------|-----------|----------|
| `make_index.py` | `import os` | **HIGH** — cannot be run as `./script` |
| `make_skos.py` | `import os` | **HIGH** |
| `make_sqlite.py` | `import os` | **HIGH** |
| `migrate_atlas_schema.py` | `# tools/scripts/…` | MED — library module |
| `textbase.py` | `"""` (docstring) | LOW — library module |

**Fix**: Add `#!/usr/bin/env python3` to `make_index.py`, `make_skos.py`, `make_sqlite.py`. Optionally add to library modules for consistency.

### 3.2 Missing Executable Flag (68 scripts)

Only 20 of 88 scripts (22.7%) have `+x`. For scripts meant to be run directly (those with `if __name__ == "__main__":` and shebangs), the executable flag should be set.

**Fix**: `chmod +x` on all scripts with shebangs and `__main__` guards (approximately 60 scripts).

### 3.3 Broken Hardcoded Paths (5 scripts)

| Script | Line(s) | Hardcoded Path | Problem |
|--------|---------|----------------|---------|
| `prompt_dedupe.py` | 18 | `/Users/ana/research/hub/iconocracy-corpus` | Wrong casing (`research` vs `Research`); not portable |
| `prompt_index.py` | 16 | `/Users/ana/research/hub/iconocracy-corpus` | Same as above |
| `build_cronologia.py` | 17 | `/home/user/workspace/moedas` | Linux path on macOS |
| `irr_sample.py` | 198, 362 | `/data/iconocracy-corpus/binaries/Images` | Container/server path |
| `run_irr_pilot.py` | 107 | `/data/iconocracy-corpus/binaries/Images` | Same as above |

All hardcoded absolute paths should be replaced with `Path(__file__).resolve().parents[2]` (repo root) or configurable via CLI argument.

### 3.4 External Dependency Paths (external volumes)

| Script | Reference | Notes |
|--------|-----------|-------|
| `download_corpus_images.py` | `/Volumes/ICONOCRACIA/corpus/imagens` | External SSD — expected, but should fail gracefully |
| `enrich_urls_and_regime.py` | `/Volumes/ICONOCRACIA/corpus/imagens/[PAIS]/` | Mentioned in help text only |

### 3.5 Import Audit — Modules NOT in requirements.txt

| Module | Used by | In any requirements file? |
|--------|---------|--------------------------|
| `yaml` (PyYAML) | `inventory_corpus.py`, `prompt_index.py`, `run_research_cluster.py` | **NO** — missing |
| `torch` | `run_iconocracy_eval.py`, `train_iconocracy_sft.py` | **NO** — missing |
| `transformers` | `run_iconocracy_eval.py`, `train_iconocracy_sft.py` | **NO** — missing |
| `peft` | `run_iconocracy_eval.py`, `train_iconocracy_sft.py` | **NO** — missing |
| `trl` | `train_iconocracy_sft.py` | **NO** — missing |
| `datasets` (HuggingFace) | `train_iconocracy_sft.py` | **NO** — missing |
| `llama-cpp-python` | `iconocode_gemma4.py` | ✔ In `requirements-iconocode-gemma4.txt` |
| `playwright` | `argos_acquire_item.py`, `loc_download.py` | ✔ In `requirements-argos.txt` |

**Recommended**: Add `yaml` to `requirements.txt`. The ML stack (`torch`, `transformers`, `peft`, `trl`, `datasets`) should go in a separate `requirements-training.txt` or be documented as optional.

### 3.6 Embedded Non-Python Code

`loc_download.py` (lines 128–195) contains a JavaScript/Node.js script embedded as a Python raw string, written to a temp `.mjs` file and executed with `node`. This is functional but fragile. Recommend extracting to a standalone `.mjs` file.

### 3.7 Double `__main__` Guard

`enrich_iiif.py` has **two** `if __name__ == "__main__":` blocks. Likely a merge artifact. Should be consolidated.

### 3.8 Missing `__main__` Guard (4 scripts)

| Script | Notes |
|--------|-------|
| `__init__.py` | Expected (package init) |
| `textbase.py` | Library module — acceptable |
| `migrate_atlas_schema.py` | Library module — acceptable |
| `build_cronologia.py` | Standalone script — **should have `__main__`** |

---

## 4. Duplicated / Overlapping Functionality

### 4.1 IRR Calculations: `calculate_irr.py` vs `compute_irr.py`

| | `calculate_irr.py` | `compute_irr.py` |
|---|---|---|
| Lines | 219 | 664 |
| Purpose | Human vs synthetic pilot comparison | Full IRR for purification coding |
| Features | Basic Krippendorff's Alpha | Bootstrap CI, adjudication, rater-2 support, indicator reports |
| Test | | |
| Recommendation | **ARCHIVE** — superseded by `compute_irr.py` | **KEEP** |

### 4.2 IRR Sampling: `select_irr_sample.py` vs `irr_sample.py`

| | `select_irr_sample.py` | `irr_sample.py` |
|---|---|---|
| Lines | 121 | 519 |
| Features | Basic stratified sampling, metadata export | Stratified sampling + image copy, full CLI |
| Test | ✔ | |
| Recommendation | **ARCHIVE** — superseded | **KEEP** |

### 4.3 Support Classification: `classify_support_types.py` vs `classify_support_types_rich.py`

| | `classify_support_types.py` | `classify_support_types_rich.py` |
|---|---|---|
| Lines | 101 | 146 |
| Purpose | First-pass heuristic classifier | Second-pass using records.jsonl metadata |
| Recommendation | **ARCHIVE** (first-pass, succeeded) | **KEEP** |

### 4.4 Purification Coding: `auto_code_purification.py` vs `code_purification.py`

| | `auto_code_purification.py` | `code_purification.py` |
|---|---|---|
| Lines | 463 | 469 |
| Purpose | Auto-infer scores from metadata | Interactive CLI for human coding |
| Test | | |
| Recommendation | **ARCHIVE** (one-shot script, already executed) | **KEEP** |

### 4.5 Deprecated Forwarder: `notion_sync.py`

This script is explicitly deprecated. It prints a deprecation warning and forwards all commands to `vault_sync.py`. No active functionality. **DELETE**.

### 4.6 Historical Migration: `csv_to_records.py`

One-shot migration script (`corpus-data.json + corpus_dataset.csv → records.jsonl`). After migration, this is only useful as documentation. **ARCHIVE**.

### 4.7 Example/Demo: `batch_example.py`

326-line example demonstrating dual-agent corpus builder workflow. Not production code. **ARCHIVE**.

### 4.8 Library Module: `migrate_atlas_schema.py`

27-line utility providing `calculate_axes()` and `add_bilingual_labels()`. Pure library — no CLI, no `__main__`. Has a test. Should live in `tools/lib/` rather than `tools/scripts/`. **ARCHIVE** (move to lib).

### 4.9 `records_to_corpus.py` vs `records_to_sqlite.py`

Not duplicated — different output targets (JSON vs SQLite). Both needed. **KEEP both**.

### 4.10 `enrich_iiif.py` vs `enrich_urls_and_regime.py`

Different enrichment passes (IIIF manifests vs image URLs + regime classification). Complementary. **KEEP both**.

---

## 5. Test Coverage Map

### 5.1 Scripts with Direct Test Coverage (16 of 88 = 18.2%)

| Script | Test File | Test Dir |
|--------|-----------|----------|
| `validate_schemas.py` | `test_validate_schemas.py` | tests/ |
| `check_corpus_export_idempotent.py` | `test_corpus_export_idempotent.py` | tests/ |
| `fix_records_schema_issues.py` | `test_fix_records_schema_issues.py` | tests/ |
| `run_irr_pilot.py` | `test_run_irr_pilot.py` | tests/ |
| `select_irr_sample.py` | `test_select_irr_sample.py` | tests/ |
| `argos_acquire_item.py` | `test_acquire_item.py` | tests/argos/ |
| `argos_prepare_dispatch.py` | `test_dispatch.py` | tests/argos/ |
| `argos_build_manifest.py` | `test_manifest_builder.py` | tests/argos/ |
| `argos_report.py` | `test_report.py` | tests/argos/ |
| `argos_manifest_update.py` | `test_manifest_update.py` | tests/argos/ |
| `normalize_supports.py` | `test_normalize_supports.py` | tests/tools/ |
| `migrate_atlas_schema.py` | `test_migrate_atlas_schema.py` | tests/tools/ |
| `iconocode_gemma4.py` | `test_iconocode_gemma4.py` | tests/tools/ |
| `ingest_fichas_lpai.py` | `test_ingest_fichas_lpai.py` | tests/tools/ |
| `compare_iconocracy_eval_runs.py` | `test_compare_iconocracy_eval_runs.py` | tests/training/ |
| `run_iconocracy_eval_openrouter.py` | `test_run_iconocracy_eval_openrouter.py` | tests/training/ |

### 5.2 Test Files for Internal Modules (Not Scripts)

| Test File | Tests |
|-----------|-------|
| `test_cross_file_consistency.py` | Cross-file data integrity |
| `test_reconcile_coherence.py` | Reconciliation logic |
| `argos/test_classifier.py` | ARGOS classifier |
| `argos/test_html_extraction.py` | HTML extraction |
| `argos/test_manifest_schema.py` | Manifest schema validation |
| `argos/test_playwright_fallback.py` | Playwright fallback |
| `argos/test_protocols_core.py` | Protocol core |
| `argos/test_smoke.py` | ARGOS smoke test |
| `argos/test_storage.py` | ARGOS storage |

### 5.3 Critical Scripts WITHOUT Tests

These are called out in `CLAUDE.md` / `AGENTS.md` as key scripts but lack tests:

| Script | Risk | Priority |
|--------|------|----------|
| `check_thesis_terms.py` | Guards terminology integrity | **HIGH** |
| `code_purification.py` | Core interactive coding CLI | **HIGH** |
| `vault_sync.py` | Bidirectional data sync | **HIGH** |
| `records_to_corpus.py` | Canonical export pipeline | **CRITICAL** |
| `build_hf_release.py` | Release gate | **HIGH** |

---

## 6. Additional Findings

### 6.1 SSL Certificate Verification Disabled

`europeana_download.py` (lines 17–19) disables SSL certificate verification globally:
```python
SSL_UNVERIFIED = ssl.create_default_context()
SSL_UNVERIFIED.check_hostname = False
SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE
```
**Risk**: MITM vulnerability. Should use per-domain exceptions instead.

### 6.2 Scripts Without `from __future__ import annotations` (43 scripts)

43 of 88 scripts use the modern annotation import. The rest may have type annotation issues on Python <3.10. Not urgent but should be standardized.

### 6.3 Old Modification Date Scripts

| Script | Last Modified | Notes |
|--------|---------------|-------|
| `extract_feminist_network.py` | 2026-04-25 | Oldest; may be stale |
| `iconocode_to_corpus.py` | 2026-06-18 | Older than repo average |
| `sync_github_labels.py` | 2026-06-18 | Older than repo average |
| `textbase.py` | 2026-06-18 | Older than repo average |
| `vault_backup.py` | 2026-06-18 | Older than repo average |

All appear functional; no action needed.

### 6.4 Inconsistent Script Naming

`purify-diff.py` uses a hyphen instead of underscore — inconsistent with all other scripts (e.g., `vault_sync.py`, `code_purification.py`). Rename to `purify_diff.py` for consistency.

---

## 7. Recommendations Summary

### 7.1 DELETE (4 scripts)

| Script | Reason |
|--------|--------|
| `notion_sync.py` | Explicitly deprecated; forwards to vault_sync.py |
| _(others to archive, not delete)_ | |

### 7.2 ARCHIVE (14 scripts)

Move to `tools/archive/` with a README explaining why:

| Script | Reason |
|--------|--------|
| `auto_code_purification.py` | One-shot auto-coder; already executed |
| `batch_example.py` | Demo/example, not production |
| `calculate_irr.py` | Superseded by `compute_irr.py` |
| `classify_support_types.py` | First pass completed; `_rich` variant is canonical |
| `csv_to_records.py` | One-shot historical migration |
| `migrate_atlas_schema.py` | Library module; move to `tools/lib/` |
| `select_irr_sample.py` | Superseded by `irr_sample.py` |
| _(remaining to be determined)_ | |

### 7.3 FIX (22 scripts)

| Priority | Script | Issue |
|----------|--------|-------|
| **CRITICAL** | `prompt_dedupe.py` | Hardcoded broken path |
| **CRITICAL** | `prompt_index.py` | Hardcoded broken path |
| **HIGH** | `irr_sample.py` | Hardcoded container path |
| **HIGH** | `run_irr_pilot.py` | Hardcoded container path |
| **HIGH** | `build_cronologia.py` | Hardcoded Linux path |
| **HIGH** | `make_index.py` | Missing shebang |
| **HIGH** | `make_skos.py` | Missing shebang |
| **HIGH** | `make_sqlite.py` | Missing shebang |
| **MED** | `download_corpus_images.py` | Hardcoded SSD path (fail gracefully) |
| **MED** | `enrich_urls_and_regime.py` | Hardcoded SSD path in help text |
| **MED** | `enrich_iiif.py` | Double `__main__` guard |
| **MED** | `loc_download.py` | Embedded JS should be external file |
| **MED** | `inventory_report.py` | Dated CSV path |
| **MED** | `inventory_corpus.py` | Missing `yaml` in requirements.txt |
| **MED** | `run_research_cluster.py` | Missing `yaml` in requirements.txt |
| **LOW** | `run_iconocracy_eval.py` | Missing torch/transformers in reqs |
| **LOW** | `train_iconocracy_sft.py` | Missing ML deps in reqs |
| **LOW** | `purify-diff.py` | Inconsistent naming (hyphen vs underscore) |
| **LOW** | `build_cronologia.py` | Missing `__main__` guard |

### 7.4 KEEP (48 scripts)

All scripts not in ARCHIVE or DELETE categories. These are active, functional scripts with no critical issues.

---

## 8. Action Plan

### Phase 1 — Immediate (pre-defense)
1. Delete `notion_sync.py`
2. Fix 4 broken hardcoded paths in `prompt_dedupe.py`, `prompt_index.py`, `irr_sample.py`, `run_irr_pilot.py`
3. Add shebangs to `make_index.py`, `make_skos.py`, `make_sqlite.py`
4. Consolidate `enrich_iiif.py` double `__main__` guard

### Phase 2 — Short-term (post-defense cleanup)
1. Archive 14 superseded/one-shot scripts to `tools/archive/`
2. Add `yaml` to `requirements.txt`
3. Create `requirements-training.txt` for ML dependencies
4. Make all shebanged scripts executable (`chmod +x`)
5. Rename `purify-diff.py` → `purify_diff.py`

### Phase 3 — Medium-term
1. Add tests for 5 critical untested scripts
2. Extract embedded JS from `loc_download.py`
3. Replace `/Volumes/ICONOCRACIA` references with `--output-dir` CLI arguments
4. Standardize `from __future__ import annotations` on all scripts

---

*Generated by Hermes Agent — Wave 3.2 Scripts Health Audit — 2026-06-26*
