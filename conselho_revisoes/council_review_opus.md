# Council Review — IconoCode Recodification Pilot (n=15)

## 1. Verdict
**DO NOT SCALE YET.** The method conflates two incompatible constructs — *degree of hardening* and *regime type* — and its treatment of absent bodies actively poisons the ENDURECIMENTO scale. Fix the scoring model before touching the remaining 144.

## 2. Score / Rubric (0–10)
- **(a) Construct validity:** 4 — Ten indicators are plausible but overlapping (serialidade/monocromatizacao/inscricao_estatal co-move mechanically for all coins/stamps, inflating scores for the medium rather than the phenomenon). Regime and score measure different things but are reasoned about as one.
- **(b) Indicator consistency across the 15:** 3 — Anchors are not operationalized. `uniformizacao_facial=3` on BR-041 is explicitly scored for a sketch's *diluted execution*, not iconographic hardening; low resolution (NORMATIVO 2.7, BR-041) contaminates several fine-attribute indicators.
- **(c) Regime-assignment logic:** 3 — US-BANNER-1861 is MILITAR yet scores 1.3; DE-GERM-1900 is NORMATIVO yet ties for the highest score (3.0). Regime is assigned by inferred *function/intent* ("dedicated to a general," "latent militarism") rather than visual evidence, making it unfalsifiable.
- **(d) Missing/absent data:** 5 — Genuinely absent images are honestly nulled (good), but the assignat absence is scored 3.0 (bad), so the category is handled inconsistently.
- **(e) Reproducibility at scale:** 3 — No codebook anchors, no dual-coding, no inter-rater check. Narrative-inference calls (US-BANNER, DE-GERM) will not replicate across coders or across 144 records.

## 3. Top 3 flaws most likely to corrupt the scale-up
1. **Medium-driven score inflation.** serialidade, monocromatizacao, and inscricao_estatal are near-automatic 3–4 for any circulating coin/stamp, so ENDURECIMENTO will cluster high regardless of the female body. This biases the entire distribution toward "hardening."
2. **Intent-based regime coding.** Assigning MILITAR/NORMATIVO from dedications and "latent" tendencies, not pixels, is subjective and non-reproducible — the single largest inter-rater risk.
3. **Confidence not gated to score.** Low-res/diluted images (2.7, BR-041) still produce full 10-indicator scores that enter the dataset with the same weight as high-confidence reads.

## 4. The absence problem
Scoring the assignat **3.0 is invalid.** desincorporacao=4 and dessexualizacao=4 on a body that does not exist are not measurements of hardening — they are category errors that manufacture a high-hardening data point from *nothing*. Including it will right-shift the ENDURECIMENTO mean and falsely support the thesis. **Correct treatment:** CONTRA-ALEGORIA / structural absence must receive a **null ENDURECIMENTO score** and be reported as a separate categorical count, never as a numeric point on the 0–4 continuum. Absence is a different phenomenon, not maximal hardening.

## 5. Concrete improvements before scaling
- **Anchored codebook:** one written visual exemplar per indicator per level (0–4); score only what is *depicted*.
- **Separate regime from score:** assign regime from visual attributes via an explicit decision tree; forbid intent/dedication as evidence.
- **Dual-code + IRR:** two coders on ~20% overlap; report Krippendorff's α (target ≥0.67) before scaling.
- **Confidence gating:** exclude or flag-only any record below a resolution/verification threshold; never emit full scores from diluted images.
- **Formal absence rule:** null score + categorical tag; audit medium-effect indicators (consider down-weighting serialidade/monocromatizacao or normalizing within support type).
