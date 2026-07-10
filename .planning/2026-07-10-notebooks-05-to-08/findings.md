# Notebooks 05-08 Re-run Findings

## 1. Data Integrity Issues Resolved
- **The Fake Zero Contamination:** The raw `corpus_dataset.csv` contains 328 rows, but 76 of them had exactly `0` for all 10 indicators. These were artifacts injected by `vault-import` and `migration` scripts, creating a false cluster of "zero endurance" items.
- All notebooks (05 through 08) were patched to apply a strict mask `~is_fake_zero`, ensuring the statistical baseline is the **N=161** truly coded items.
- **The Schema Evolution Gap:** The `medium` and `medium_norm` properties no longer exist in the export artifacts (`corpus-data.json` or `corpus_dataset.csv`). In 05_temporal, the timeline of mediums was disabled and documented as a schema loss.

## 2. Updated Analytics (N=161)
- **Composite Score:** The true composite mean of the corpus is **1.46** (on a scale of 0 to 3), reflecting a solid baseline of endurance across the dataset.
- **Top Indicators:** `monocromatizacao` remains the highest scoring factor (mean ~1.81), followed closely by `inscricao_estatal` and `serialidade`.

## 3. Dimensionality & Clustering
- **PCA (NB07):** A methodological note was inserted acknowledging that running standard PCA on ordinal (0-3) data is an exploratory approximation and that Polychoric PCA or Multiple Correspondence Analysis (MCA) would be the rigorous standard.
- **Clustering (NB06):** Unsupervised clustering now reflects the real structural separation of the corpus, unpolluted by the 76 false zeros that were previously pulling algorithms toward an artificial "low endurance" center of gravity.

## 4. Sub-scores (NB08)
- Subscores for `endurecimento_core` (8 indicators), `monocromatizacao_score` (1), and `formalizacao_bur` (2) were regenerated and exported to `data/processed/subscores.csv`.

**Status:** All four notebooks executed successfully from top to bottom. New figures generated in `data/processed/fig_*.png` are now accurate to the actual coded dataset.