# IRR Re-Run Artifacts

This directory holds artifacts from the 2026-06-23 IRR re-run experiment.

## Contents

| File | Description | Use |
|---|---|---|
| `rater2_synthetic_baseline.jsonl` | 30-item synthetic Rater-2 (regime-typical means + bounded random noise, seed=42) | **NOT a real second coder.** For pipeline demo only. All alpha values from running `compute_irr.py --rater2` against this file came back `null` due to insufficient coder variance. |

## What this is NOT

- This is NOT the authoritative IRR report. The authoritative IRR is at
  `../irr_report.json` (April 2026 pilot baseline, _overall=0.7483,
  N=30, iconocode-opus vs opencode-pilot, 9 disagreements).
- This is NOT ready for use as evidence in the thesis or in any external
  communication. The synthetic data has too-low variance for
  Krippendorff's alpha to be mathematically defined.

## How this was produced

1. `purification.jsonl` was filtered to retain only the 30 sample items
   that appear in `../irr_sample.json`.
2. For each item, a synthetic Rater-2 coding was generated based on
   the item's `regime_iconocratico` (militar / normativo / fundacional
   / contra-alegoria) using regime-typical mean values per indicator,
   plus bounded random noise in {-1, 0, 0, 0, +1} clipped to [0, 4].
3. The synthetic records were written with `item_id` (not `id`) and
   `coded_by: "rater2-synthetic-baseline-2026-06-23"`.
4. `python tools/scripts/compute_irr.py --rater2 rater2_synthetic_baseline.jsonl --export-json`
   was run; all 10 alphas came back `null` ("insufficient data") because
   the regime-typical means did not produce enough spread between
   Rater-1 (iconocode-opus*) and the synthetic Rater-2.

## Why the synthetic data fails

Krippendorff's alpha (ordinal metric) is mathematically undefined when
the variance between coders is zero or near-zero. The regime-typical
means compress the synthetic Rater-2 toward the modal value of each
indicator per regime, so for most items the synthetic Rater-2
converges to the same value as the iconocode-opus coder.

A real Rater-2 (manual coding by Ana under a fresh session, ~1-2h of
work) would produce genuine variance. See
`docs/decisions/ICONOCRACY-LPAI-CODEBOOK-DECISIONS-2026-06-23.md`
section 7.4 for the recommended procedure.

## Companion artefact

The synthetic IRR report (output of `compute_irr.py --rater2`) is at
`../irr_reports/irr_report_synthetic-baseline_2026-06-23.json`. It has
`_metadata.kind: "synthetic-baseline"` and `_metadata.use_for: "Do not
use as IRR evidence"` to prevent mis-picking.
