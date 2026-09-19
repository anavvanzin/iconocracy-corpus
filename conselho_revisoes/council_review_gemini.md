### 1. Verdict
**DO NOT SCALE YET**
The protocol conflates the *absence* of a body with the *hardening* of a body, corrupting the ENDURECIMENTO construct and making regime assignment highly subjective.

### 2. Score/rubric
**(a) Construct validity: 4/10** — The index measures "hardening of the allegorical female body" but breaks when applied to objects lacking a female body (e.g., assignat, architecture).
**(b) Consistency: 5/10** — Scoring logic is erratic. For FR-ASSIGNAT-1792, absence yields maximum scores (4), but for BE-CONGO-MON-1921, monumental architecture yields contextual scores.
**(c) Regime-assignment logic: 3/10** — Regime boundaries are highly subjective and frequently override explicit indicators. US-BANNER-1861 is explicitly labeled MILITAR despite acknowledging a dynamic, living body (FUNDACIONAL), merely because of text dedications.
**(d) Handling missing data: 2/10** — Terrible. Scoring an absent body as "maximum hardening" (4s) artificially inflates the mean score to 3.0 (the highest in the pilot), destroying the metric's validity.
**(e) Reproducibility at scale: 3/10** — High variance in resolving borderline cases (e.g., transitional regimes, missing bodies, latent vs. explicit traits) guarantees low inter-rater reliability.

### 3. Top 3 concrete flaws
1. **The Absence Conflation**: Scoring structurally absent bodies (e.g., FR-ASSIGNAT-1792) as maximum values (4) for bodily variables (desincorporacao, dessexualizacao) creates artificial peaks in ENDURECIMENTO, mathematically equating "no body" with "maximum state rigidity."
2. **Regime vs. Form Decoupling**: Regimes are being assigned based on external historical context (dedications, general usage) rather than visual form. If a dynamic Columbia is scored 1.3 but classed MILITAR (US-BANNER-1861), the protocol measures historical intent, not iconographic form.
3. **Indicator Contradictions in Transitions**: The protocol cannot handle transitional cases systematically. DE-GERM-1900 is classed NORMATIVO but scored high (3.0) for "latent" militarism, while others are classed MILITAR but scored low (US-BANNER-1861). This makes regime assignment arbitrary.

### 4. The absence problem
Scoring an absent body is entirely invalid and fatally contaminates the ENDURECIMENTO distribution. Treating "no body" as "maximum desexualization" (4) or "maximum disincorporation" (4) implies an infinite progression of hardening that mathematically breaks the ordinal scale.
**Recommendation**: The construct requires an allegorical female body to exist. Records with no female body must be strictly excluded from the ENDURECIMENTO calculation (Null/NA, not 0 or 4) and tagged with a distinct binary flag (e.g., `corpo_ausente=True`). They belong in a separate qualitative category, not on the quantitative continuum.

### 5. Concrete improvements
- **Gating Question**: Add a hard gate: "Is there a female allegorical body?" (Yes/No). If No, skip all 10 indicators, set ENDURECIMENTO to NULL, and assign to CONTRA-ALEGORIA or a new "ANICÔNICO" regime.
- **Visual-Only Anchoring**: Regime assignment must be strictly anchored to the visual indicators, not external metadata. If the score is < 1.5, it cannot be MILITAR, regardless of who it is dedicated to. Establish strict numerical thresholds for regimes.
- **Inter-Rater Reliability (IRR)**: Before scaling, two independent raters must score 30 items blind. Proceed only if Cohen’s Kappa is > 0.70.
- **Standardized Rubric**: Define exact visual anchors for 0, 1, 2, 3, and 4 for every indicator (e.g., for `rigidez_postural`: 0=running/flying, 2=standing still, 4=frozen bust).