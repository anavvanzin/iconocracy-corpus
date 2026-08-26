# ARGOS + ICONOCRACY SFT integration plan

> For Hermes: use subagent-driven-development if this plan moves into execution.

Goal: integrate ARGOS into the ICONOCRACY training/data workflow so acquisition-state knowledge and newly recovered assets can improve corpus preparation, dataset generation, and later model evaluation without breaking current corpus truth-order.

Architecture: keep ARGOS as the acquisition/orchestration layer and keep `records.jsonl` / `purification.jsonl` as canonical processed surfaces. The merge should happen through narrow interfaces: ARGOS emits structured acquisition outcomes; downstream scripts consume those outcomes to enrich corpus-ready records, generate training examples about provenance/traceability, and surface acquisition-aware QA/eval tasks.

Tech stack: Python 3.12, conda `iconocracy`, JSON/JSONL, existing `tools/argos/*` pipeline, existing SFT scripts in `tools/scripts/*`.

---

## 1. Recommended interpretation of “merge with ARGOS”

Do not collapse ARGOS and SFT into one monolithic script.

Recommended meaning of the merge:
1. ARGOS becomes the acquisition front-end for pending corpus items.
2. ARGOS outputs become inspectable structured inputs for downstream corpus and training utilities.
3. The SFT dataset expands to teach the assistant:
   - corpus traceability
   - acquisition provenance
   - source-quality caution
   - difference between recovered asset, landing page, screenshot, and unresolved/manual item
4. Evaluation prompts start checking whether the model respects acquisition uncertainty and provenance metadata.

This preserves the project’s order of truth:
- source/archive
- Drive / manifests / acquisition traces
- processed records (`records.jsonl`)
- derived training/eval datasets

---

## 2. Repo facts that matter for the merge

Current ARGOS surfaces:
- `tools/argos/`
- `tools/scripts/argos_build_manifest.py`
- `tools/scripts/argos_acquire_item.py`
- `tools/scripts/argos_prepare_dispatch.py`
- `tools/scripts/argos_report.py`
- `data/raw/argos/manifest.json`
- `data/raw/argos/report.md`

Current SFT surfaces:
- `tools/scripts/build_iconocracy_sft_dataset.py`
- `tools/scripts/split_iconocracy_sft_dataset.py`
- `tools/scripts/train_iconocracy_sft.py`
- `data/training/iconocracy_sft_v1_1.jsonl`
- `data/training/iconocracy_sft_v1_1_train.jsonl`
- `data/training/iconocracy_sft_v1_1_val.jsonl`
- `data/training/iconocracy_eval_prompts_v1_1.jsonl`

Important current behavior:
- `argos_acquire_item.py` already writes attempts/provenance-oriented result data back into the ARGOS manifest.
- `build_iconocracy_sft_dataset.py` currently trains only from `records.jsonl` and `purification.jsonl` plus fixed project guardrails/planning examples.
- The SFT builder does not yet consume ARGOS outcomes.
- The current dataset already emphasizes analytical and purification tasks, but has very little explicit supervision about acquisition/provenance discipline.

---

## 3. What should and should not be merged

### Merge these concerns
- acquisition provenance into downstream training data
- recovery status into corpus QA surfaces
- unresolved/manual states into guardrail examples
- asset-recovery metadata into later evaluation prompts
- ARGOS run summaries into operator-facing reports for corpus expansion planning

### Do not merge these concerns
- do not make ARGOS directly edit `records.jsonl`
- do not treat ARGOS manifest as canonical corpus truth
- do not train directly from raw landing-page HTML, screenshots, or unstable scrape artifacts
- do not let browser fallbacks or restricted-domain exceptions silently become “evidence” in the SFT dataset

---

## 4. End-state target

After the merge, the project should support this flow:

1. `argos_build_manifest.py` identifies pending items.
2. `argos_acquire_item.py` attempts recovery and writes structured provenance/attempt metadata.
3. a new export/bridge step converts eligible ARGOS outcomes into normalized acquisition summaries.
4. downstream corpus maintainers use those summaries to decide what is fit to promote into canonical records.
5. the SFT builder optionally ingests the normalized acquisition summaries to create new task families such as:
   - `traceability_explainer`
   - `acquisition_guardrails`
   - `provenance_interpreter`
   - `argos_run_diagnosis`
6. eval prompts test whether the model preserves uncertainty and provenance discipline.

---

## 5. Recommended new integration surfaces

### A. New normalized bridge artifact

Create a small bridge export instead of reading the raw manifest everywhere.

Add:
- `tools/scripts/export_argos_training_inputs.py`
- output path: `data/training/argos_training_inputs_v1.jsonl`

Each exported row should represent one ARGOS item with fields such as:
- `item_id`
- `title`
- `source_url`
- `source_domain`
- `protocol`
- `status`
- `failure_class`
- `attempt_count`
- `selected_method`
- `retrieved_from`
- `local_path`
- `asset_kind` if inferable
- `browser_capture_mode` if present
- `iiif_manifest_url` if present
- `notes`
- `has_real_asset`
- `is_manual_only`
- `is_restricted_domain`
- `traceability_summary`

Why this bridge matters:
- avoids coupling the SFT builder to raw ARGOS manifest internals
- keeps the training layer stable even if ARGOS evolves
- lets us filter low-quality acquisition outcomes before they affect training

### B. New SFT task families

Extend `build_iconocracy_sft_dataset.py` with optional ARGOS-derived examples.

Add task families:
- `traceability_explainer`
  - explain the difference between source URL, retrieved asset, manifest, and canonical record
- `acquisition_guardrails`
  - teach what counts as evidence vs hypothesis vs screenshot fallback
- `provenance_interpreter`
  - interpret acquisition outcomes cautiously
- `argos_run_diagnosis`
  - summarize why a batch/domain is failing and what next step is appropriate

These tasks should remain minority families in the mix, likely 5–15% total at first.

### C. New eval prompts

Extend `data/training/iconocracy_eval_prompts_v1_1.jsonl` or create `...v1_2.jsonl` with prompts that test:
- distinction between screenshot and real captured asset
- refusal to overclaim from unresolved/manual ARGOS items
- correct explanation of why ARGOS manifest is not the final canonical corpus
- appropriate recommendation when a domain is restricted or HTML-only

---

## 6. Bite-sized implementation plan

### Task 1: Document the integration contract

Objective: define exactly which ARGOS fields are safe to expose downstream.

Files:
- Create: `docs/plans/2026-04-14-argos-sft-integration-plan.md`
- Modify later if needed: `docs/ARGOS_RUNBOOK.md`

Step 1: confirm the downstream contract fields from current ARGOS manifest/provenance structure.
Step 2: list fields that are allowed for training use.
Step 3: explicitly exclude unstable fields and raw HTML blobs.

Verification:
- read the plan and confirm it preserves `records.jsonl` as canonical.

### Task 2: Add a bridge exporter from ARGOS manifest to training-ready JSONL

Objective: produce a narrow, stable JSONL file for downstream consumers.

Files:
- Create: `tools/scripts/export_argos_training_inputs.py`
- Test: `tests/argos/test_export_argos_training_inputs.py`

Implementation notes:
- read `data/raw/argos/manifest.json`
- export one normalized row per item
- compute booleans like `has_real_asset`, `is_manual_only`, `is_restricted_domain`
- derive a short `traceability_summary` string from status/provenance/attempts
- do not emit raw HTML or page dumps

Verification commands:
- `python -m unittest tests.argos.test_export_argos_training_inputs -v`
- `python tools/scripts/export_argos_training_inputs.py --manifest data/raw/argos/manifest.json --output data/training/argos_training_inputs_v1.jsonl`

### Task 3: Add optional ARGOS ingestion to the SFT builder

Objective: let the training dataset grow acquisition/provenance supervision without forcing it.

Files:
- Modify: `tools/scripts/build_iconocracy_sft_dataset.py`
- Test: add focused builder tests if a test surface already exists, or create `tests/training/test_build_iconocracy_sft_dataset.py`

Implementation notes:
- add optional CLI arg such as `--argos-input data/training/argos_training_inputs_v1.jsonl`
- keep the current dataset behavior unchanged when ARGOS input is absent
- create small deterministic example builders for each new task family
- attach metadata like `argos_status`, `argos_protocol`, `source_domain`, `item_id`

Verification commands:
- `python -m py_compile tools/scripts/build_iconocracy_sft_dataset.py`
- smoke run with a tiny ARGOS input sample
- inspect emitted rows manually

### Task 4: Add new eval prompts for provenance discipline

Objective: test whether the future fine-tuned model understands acquisition uncertainty.

Files:
- Modify or create: `data/training/iconocracy_eval_prompts_v1_2.jsonl`
- Modify or create: `docs/superpowers/specs/2026-04-14-iconocracy-sft-eval-guide-v1-2.md`

Implementation notes:
- include prompts about restricted domains, screenshots, IIIF manifests, unresolved HTML landing pages, and manual-only status
- score for prudence, traceability correctness, and refusal to overclaim

Verification:
- JSONL line validation
- manual read-through of prompts for terminology correctness

### Task 5: Add operator reporting for the merge

Objective: make ARGOS useful not just for acquisition, but for training/corpus planning.

Files:
- Modify: `tools/argos/report.py`
- Possibly modify: `tools/scripts/argos_report.py`

Implementation notes:
- add report sections summarizing:
  - exportable-for-training items
  - unresolved/manual items that should become guardrail examples
  - domains with high HTML-only or screenshot-only rates
- keep this reporting additive and non-breaking

Verification commands:
- existing ARGOS report generation command
- manual inspection of markdown report output

### Task 6: Validate the integrated flow in the target environment

Objective: verify the bridge + builder pipeline in conda `iconocracy`.

Files:
- no new business logic if everything passes

Verification commands:
- `conda run -n iconocracy python -m unittest discover -s tests/argos -p 'test_*.py'`
- `conda run -n iconocracy python tools/scripts/export_argos_training_inputs.py --manifest data/raw/argos/manifest.json --output data/training/argos_training_inputs_v1.jsonl`
- `conda run -n iconocracy python tools/scripts/build_iconocracy_sft_dataset.py --argos-input data/training/argos_training_inputs_v1.jsonl`
- `conda run -n iconocracy python tools/scripts/split_iconocracy_sft_dataset.py --input data/training/iconocracy_sft_v1_2.jsonl --train-output data/training/iconocracy_sft_v1_2_train.jsonl --val-output data/training/iconocracy_sft_v1_2_val.jsonl`

---

## 7. Minimal schema for `argos_training_inputs_v1.jsonl`

Proposed shape:

```json
{
  "item_id": "AT-001",
  "title": "Example item",
  "source_url": "https://example.org/item/1",
  "source_domain": "example.org",
  "protocol": "direct",
  "status": "acquired",
  "failure_class": "",
  "attempt_count": 2,
  "selected_method": "iiif",
  "retrieved_from": "https://example.org/iiif/full/full/0/default.jpg",
  "local_path": "/path/to/asset.jpg",
  "has_real_asset": true,
  "is_manual_only": false,
  "is_restricted_domain": false,
  "browser_capture_mode": "asset",
  "iiif_manifest_url": "https://example.org/iiif/manifest",
  "notes": ["html_landing_page", "resolved_via_iiif"],
  "traceability_summary": "Landing page resolved to IIIF image; real asset captured and stored locally."
}
```

---

## 8. Design rules

1. Keep ARGOS and SFT loosely coupled.
2. Never promote raw acquisition output straight into canonical corpus records.
3. Prefer a bridge exporter over direct manifest parsing in multiple places.
4. Treat screenshot-only outcomes as weaker evidence than real asset capture.
5. Use ARGOS failures as training material for caution/traceability, not only as engineering defects.
6. Keep all new behavior optional behind explicit CLI inputs.
7. Validate final integrated flow in conda `iconocracy`, not just ambient Python.

---

## 9. Risks and mitigations

Risk: ARGOS manifest internals keep changing.
Mitigation: use a dedicated exporter and stable v1 JSONL schema.

Risk: training data becomes polluted with scrape noise.
Mitigation: export only normalized summaries and exclude raw page content.

Risk: model learns to overtrust screenshots or browser captures.
Mitigation: add explicit guardrail/eval examples distinguishing screenshot from real asset.

Risk: canonical truth-order gets blurred.
Mitigation: repeat in docs, prompts, and metadata that ARGOS is acquisition/provenance support, not the canonical processed corpus.

Risk: merge scope expands too fast.
Mitigation: implement only bridge exporter + optional SFT ingestion first.

---

## 10. Recommended first slice

Best first slice:
1. create `export_argos_training_inputs.py`
2. emit `data/training/argos_training_inputs_v1.jsonl`
3. patch `build_iconocracy_sft_dataset.py` to accept `--argos-input`
4. add only two new task families initially:
   - `acquisition_guardrails`
   - `traceability_explainer`

Why this slice first:
- smallest useful integration
- low risk to canonical corpus surfaces
- immediately improves the assistant’s understanding of provenance discipline
- avoids premature coupling to richer ARGOS internals

---

## 11. Definition of done for phase 1

Phase 1 is done when:
- a stable ARGOS-to-training bridge JSONL exists
- SFT builder can optionally ingest it
- at least two ARGOS-derived task families are generated
- a small integrated dataset build passes
- the split step still works
- new eval prompts cover provenance/traceability behavior
- all relevant tests pass in the `iconocracy` conda env
