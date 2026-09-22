**Verdict: DO NOT SCALE YET.** The pilot shows serious visual engagement, but the scoring rules are not stable enough to apply to 144 more records without contaminating the distribution.

**Score/rubric**
- Construct validity of method: **6/10**. The indicators broadly match “hardening,” but the construct mixes morphology, medium, political function, and circulation in one mean.
- Consistency of indicator scoring across the 15: **5/10**. Some scores are well reasoned, but “latent” militarism, low-resolution images, and absence are handled ad hoc.
- Regime-assignment logic: **5/10**. Regime sometimes follows iconography, sometimes historical function, sometimes medium; US-BANNER-1861 and DE-GERM-1900 expose this instability.
- Honest handling of missing/absent data: **6/10**. Non-recodable items are mostly excluded properly, but FR-ASSIGNAT-1792 violates the same principle by scoring what is absent.
- Reproducibility at scale: **4/10**. Without anchors, coder rules, and adjudication, the next 144 records will amplify subjective exceptions.

**Top 3 concrete flaws**
1. **Regime and score are not separated cleanly.** A low-hardening dynamic Columbia is labelled MILITAR because of wartime dedication, while a high-hardening Germania remains NORMATIVO because it is a civil definitive stamp. That may be defensible, but only if regime is explicitly a historical-political category and ENDURECIMENTO a separate visual-morphological metric.
2. **Ordinal anchors are underspecified.** Values like desincorporacao=1 vs 3, apagamento_narrativo=2 vs 3, and uniformizacao_facial=3 in blurred imagery depend on interpretive discretion. The arithmetic mean gives false precision to uneven judgments.
3. **Confidence is not operationalized.** Medium/low confidence flags do not consistently gate scoring, inclusion, or downstream analysis. Low-resolution or alternate-source images should not enter the same quantitative distribution as directly verified high-resolution records.

**The absence problem**
Scoring an absent female body as ENDURECIMENTO=3.0 is not valid. It converts non-presence into maximum purification, but “hardening of the allegorical female body” presupposes a body or at least a female allegorical residue. FR-ASSIGNAT-1792 should be coded as **CONTRA-ALEGORIA / ABSENCE**, with ENDURECIMENTO = **NA**, not 3.0. It can be analyzed in a separate absence/refusal variable, but including it in the mean contaminates rank order and artificially ties it with DE-GERM-1900.

**Concrete improvements**
- Create a 0–4 anchor sheet for each indicator with visual examples and exclusion rules.
- Separate fields: visual ENDURECIMENTO score, regime, medium, political context, and absence/refusal type.
- Add confidence gating: only high-confidence directly viewed images enter quantitative ENDURECIMENTO; medium cases require review; low/unverified cases are NA.
- Dual-code at least 20–30 records before scale-up; report weighted kappa or Krippendorff’s alpha per indicator.
- Require a short evidence note for every score ≥3 and every regime/score mismatch.
- Treat missing, wrong URL, non-female allegory, and absent allegory as distinct NA categories, not numeric scores.
