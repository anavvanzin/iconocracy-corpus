# Task Plan: Re-run Notebooks 05 to 08

**Goal:** Execute notebooks 05, 06, 07, and 08 using the cleaned corpus (N=161, filtering out the 76 false zeros from vault-import/migration) and correct data joins (date/country from `corpus-data.json`, 10 Codebook v2 indicators).

## Phases

### Phase 1: Clean and Run 05_temporal.ipynb
- **Status:** complete
- **Tasks:**
  - Update data loading to filter out items with exactly 0 in all 10 indicators.
  - Join `date` from `corpus-data.json` and parse it robustly.
  - Run temporal analysis (distribution, temporal drift of `purificacao_composto`).
  - Save updated notebook and figures.

### Phase 2: Clean and Run 06_clustering.ipynb
- **Status:** complete
- **Tasks:**
  - Load clean subset (N=161).
  - Use the correct 10 v2 indicators.
  - Perform unsupervised clustering (K-Means/Agglomerative) and validate silhouette scores.
  - Save updated notebook and figures.

### Phase 3: Clean and Run 07_dimensionality.ipynb
- **Status:** complete
- **Tasks:**
  - Load clean subset (N=161).
  - Acknowledge ordinal data (use MCA or polychoric PCA if available, otherwise document limitation).
  - Determine principal components and confirm if `monocromatizacao` remains isolated/dominant.
  - Check if "medium" test can be proxied (or omitted as discussed).
  - Save updated notebook and figures.

### Phase 4: Clean and Run 08_multidimensional_scoring.ipynb
- **Status:** complete
- **Tasks:**
  - Run any final ad-hoc scoring or composite generation.
  - Document the updated total variance explained based on N=161.
  - Save updated notebook and figures.

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| | | |

## Verification
- [ ] All notebooks execute top-to-bottom without errors.
- [ ] Outputs/figures reflect N=161 (or matching subset) rather than contaminated N=328/165.
- [ ] No `KeyError` referencing Codebook v1 indicators.
