# P02 — Gemini vision validation for purification coding

Date: 13 July 2026
Model: `gemini-2.5-pro`
Status: completed pilot; no canonical scores changed

## Research question

Can a vision-language model improve the audit of the 99 records coded by `hermes-auto` from metadata alone?

## Method

The pilot used the ten IconoCode purification indicators on their 0–3 ordinal scale. Gemini received each image plus only its ID, title, country, support, and the coding rubric. It did not receive the existing scores. Temperature was 0, JSON output was schema-constrained, and the composite was recomputed deterministically as the mean of the ten indicators.

Two tests were run:

1. Calibration against 12 records previously coded from images by `iconocode-opus-4.6-image`, balanced across FUNDACIONAL, NORMATIVO, MILITAR, and CONTRA-ALEGORIA.
2. Visual audit of 10 `hermes-auto` records selected across five countries and three regimes. Their images were independently retrieved and verified before scoring.

The calibration reference is prior model-assisted image coding, not independent human ground truth. Results therefore measure consistency with the existing protocol, not definitive correctness.

## Calibration result (N = 12)

- Composite MAE: **0.342** on the 0–3 scale.
- Composite Spearman correlation: **ρ = 0.822**, p = 0.001.
- Quadratic weighted kappa across 120 indicator ratings: **0.635**.
- Exact indicator agreement: **45.0%**.
- Agreement within one ordinal point: **88.3%**.
- Regime agreement: **8/12 (66.7%)**.

Gemini reproduced the relative ordering of low- and high-purification images reasonably well, but it is not reliable enough to replace adjudication. Its weakest calibration indicators were `apagamento_narrativo` (MAE 1.08), `inscricao_estatal` (0.83), `desincorporacao` (0.75), and `serialidade` (0.75). Its strongest was `dessexualizacao` (MAE 0.33; weighted κ 0.86).

## Visual audit of `hermes-auto` records (N = 10)

| ID | Metadata | Vision | Delta | Metadata regime | Vision regime | Review |
|---|---:|---:|---:|---|---|---|
| FR-076 | 1.2 | 2.0 | +0.8 | fundacional | normativo | yes |
| BR-022 | 1.3 | 1.8 | +0.5 | fundacional | fundacional | yes |
| UK-012 | 1.4 | 1.6 | +0.2 | fundacional | fundacional | no |
| DE-017 | 2.6 | 2.6 | 0.0 | normativo | normativo | no |
| BE-004 | 1.7 | 1.6 | −0.1 | fundacional | fundacional | no |
| BR-024 | 2.5 | 1.9 | −0.6 | normativo | fundacional | yes |
| BR-025 | 2.5 | 2.4 | −0.1 | normativo | fundacional | yes |
| DE-021 | 2.5 | 2.6 | +0.1 | normativo | militar | yes |
| FR-077 | 2.5 | 2.3 | −0.2 | normativo | normativo | no |
| FR-051 | 1.4 | 0.7 | −0.7 | militar | militar | yes |

Summary:

- Metadata–vision composite MAE: **0.33**.
- Aggregate bias: **−0.01**; disagreement was substantial but not uniformly directional.
- Four records had an absolute composite delta of at least 0.5.
- Regimes matched in **6/10** cases.
- The union of large composite deltas and regime mismatches flags **6/10 records** for adjudication.

## Substantive findings

The metadata coder systematically missed visual morphology even when the composite happened to remain similar:

- `desincorporacao`: vision minus metadata mean = **−1.00**.
- `dessexualizacao`: **−0.80**.
- `apagamento_narrativo`: **−0.80**.
- `inscricao_estatal`: **+1.50**.
- `heraldizacao`: **+0.90**.

The clearest case is BR-024. Metadata treated the stamp as a strongly purified NORMATIVO object (2.5). The image shows a dynamic abolition narrative: the female allegory breaks the chains of an enslaved man. Vision reduced the score to 1.9 and classified it as FUNDACIONAL. The support is serial, bordered, and state-inscribed, but its internal morphology remains embodied and narrative.

FR-051 shows the converse problem. Metadata assigned 1.4 from its support and institutional function. The image is a highly dynamic, polychrome wartime narrative with Justice rising from the sea as a ship sinks. Vision retained MILITAR but reduced purification to 0.7.

FR-076 moved upward from 1.2 to 2.0 because the photograph shows a seated, hieratic sculptural model with an idealized face and reduced narrative context. Vision classified it as NORMATIVO rather than FUNDACIONAL.

These disagreements confirm the methodological claim already developed in Chapter 2: metadata is more dependable for material indicators than for morphology, and records sharing a support or institutional function can remain visually very different.

## Image acquisition and data quality

At the start of the pilot, none of the 99 `hermes-auto` records had an ID-matched local image binary. Their source distribution was:

- 90 external catalog URLs.
- 9 unresolved internal URLs of the form `https://iconocracy.corpus/vault/<UUID>`.

The pilot acquired and visually verified ten JPEGs in:

`/home/ana/Documents/iconocracy-corpus/binaries/Images/`

IDs: BE-004, BR-022, BR-024, BR-025, DE-017, DE-021, FR-051, FR-076, FR-077, UK-012.

BE-004 required extracting page 9 from an 88-page, 190 MB source PDF; the catalog thumbnail was only a site asset and was rejected during visual verification.

After acquisition, the binary folder contains 188 files with a `.jpg` extension: 109 genuine JPEGs and 79 files that are actually HTML, PDF, or another non-JPEG format. Extension alone must not be treated as proof that an image is available.

## Decision

Use Gemini vision as a **second-pass audit and prioritization layer**, not as an automatic replacement coder.

Recommended workflow for the remaining records:

1. Acquire and verify the source image; reject catalog thumbnails, logos, blank pages, and HTML/PDF files mislabeled as JPEG.
2. Run schema-constrained visual coding without exposing the existing scores.
3. Store the result in a separate audit ledger; never overwrite `purification.jsonl` automatically.
4. Flag records when `|vision − metadata| ≥ 0.5`, the regime differs, or any morphological indicator differs by at least 2 points.
5. Human-adjudicate only the flagged subset, inspecting the image, metadata, and both coding rationales together.
6. Recalibrate the prompt specifically for `apagamento_narrativo`, `desincorporacao`, and `inscricao_estatal` before a full 99-record pass.

## Artifacts

Raw outputs, source image URLs, calibration metrics, item-level deltas, and acquisition paths:

`Other/gemini-vision-validation-2026-07-13.json`

No API key is stored in the artifact. No canonical corpus score was modified.
