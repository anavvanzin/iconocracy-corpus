# Design Spec: IRR Calculation and Discrepancy Reporting

**Date:** 2026-05-24  
**Author:** Antigravity (AI assistant)  
**Status:** Under Review  

---

## 1. Objectives

This design details the implementation of the Inter-Rater Reliability (IRR) calculation and discrepancy reporting script (`tools/scripts/calculate_irr.py`).
The script will compare ratings of two observers:
1.  **Human Coder (Ana Vanzin):** Canonical ratings stored in `data/processed/records.jsonl` under `purificacao` key.
2.  **Synthetic Coder (Gemini 1.5 Pro):** Ratings stored in `data/processed/irr_pilot_synthetic_results.jsonl` (or mock file `data/processed/irr_pilot_synthetic_results_mock.jsonl` when the `--mock` flag is set).

And calculate:
-   Krippendorff's Alpha ($\alpha$) using the ordinal metric for each of the 10 purification indicators.
-   Overall/global Krippendorff's Alpha ($\alpha$) across all ratings.
-   Identify critical discrepancies where the absolute difference between ratings is $\ge 2$ and write detailed logs to `logs/irr_discrepancies.log`.

---

## 2. Requirements & Data Structure

### 2.1 Indicators
The 10 indicators are:
1.  `desincorporacao`
2.  `rigidez_postural`
3.  `dessexualizacao`
4.  `uniformizacao_facial`
5.  `heraldizacao`
6.  `enquadramento_arquitetonico`
7.  `apagamento_narrativo`
8.  `monocromatizacao`
9.  `serialidade`
10. `inscricao_estatal`

### 2.2 Input Mapping
-   **Human ratings:** Read from `data/processed/records.jsonl`.
    -   Key path: `record["purificacao"][indicator]`
    -   Key identifier: `record["item_id"]`
-   **Synthetic ratings:** Read from `data/processed/irr_pilot_synthetic_results.jsonl` (or mock file).
    -   Key path: `record["indicadores"][indicator]["score"]`
    -   Key identifier: `record["item_id"]`

### 2.3 Krippendorff's Alpha Calculation
We will use the standard `krippendorff` library to perform calculations.
Since both coders code all selected items:
-   For a single indicator: We build a $2 \times N$ matrix (where rows are coders, columns are items).
-   For the overall pooled alpha: We build a $2 \times (10 \times N)$ matrix containing all ratings for all 10 indicators.
-   In both cases, we call `krippendorff.alpha(reliability_data=matrix, level_of_measurement='ordinal')`.
-   We will also compute and display the average of the 10 individual indicator alphas.

---

## 3. Discrepancy Identification & Logging

A critical discrepancy is defined as:
$$\text{Discrepancy} = |\text{Score}_{\text{human}} - \text{Score}_{\text{synthetic}}| \ge 2$$

When a discrepancy is found, we log it to `logs/irr_discrepancies.log` with the format:
```
================================================================================
Timestamp: YYYY-MM-DD HH:MM:SS
Item ID: <item_id>
Indicator: <indicator_name>
Human Score: <score>
Synthetic Score: <score>
Difference: <diff>
Synthetic Justification:
<justification text from the synthetic results jsonl>
================================================================================
```

The script will overwrite/create the log file at the start of each run and write all critical discrepancies.

---

## 4. Script Interface

Command Line Options:
-   `--mock`: Uses `data/processed/irr_pilot_synthetic_results_mock.jsonl` instead of `irr_pilot_synthetic_results.jsonl`.
-   `--verbose` / `-v`: Print additional information (such as matching counts and details of identified discrepancies).

---

## 5. Verification Plan

1.  Run the script with the `--mock` flag:
    `python tools/scripts/calculate_irr.py --mock`
2.  Verify stdout output includes:
    -   Overall global alpha (pooled and averaged).
    -   Alphas per indicator.
    -   Number of records successfully matched.
    -   Number of discrepancies detected.
3.  Check `logs/irr_discrepancies.log` and confirm all critical discrepancies are logged with their correct fields, including the LLM justification.
