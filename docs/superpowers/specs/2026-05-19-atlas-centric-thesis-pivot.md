# Spec: Atlas-Centric Thesis Pivot

**Date:** 2026-05-19
**Project:** ICONOCRACIA
**Status:** Draft
**Topic:** Reorienting the doctoral thesis structure and research infrastructure around a Hybrid Atlas (Comparative Plates + Empirical Index).

## 1. Problem Statement
The current thesis structure treats the iconographic corpus as a data appendix. With 265 records already validated, there is an opportunity to pivot toward an **Atlas-Centric** model where the visual evidence drives the legal-historical narrative. This requires a unified conceptual framework and a robust workflow to sync local data with both the printed manuscript and the digital web companion.

## 2. Goals
*   **Elevate the Atlas:** Transform the corpus from a list of records into a structured visual volume.
*   **Unified Conceptual Framework:** Replace "purificação clássica" and "endurecimento" with the bilingual axes: **Formalization / Formalização**, **Statization / Estatização**, and **Idealization / Idealização**.
*   **Hybrid Architecture:** Combine Warburgian "Comparative Plates" (narrative) with a "Data-Driven Index" (empirical proof).
*   **Digital/Print Parity:** Ensure the `iconocracia-companion` web app and the printed Atlas volume reflect the same curated data.

## 3. Proposed Design

### 3.1. Theoretical Axes (Bilingual)
All analysis and metadata will be organized around three primary axes (0–3 scale):
1.  **Formalization / Formalização:** Measures visual rigidity, posture, and the removal of organic/human traits.
2.  **Statization / Estatização:** Measures institutional presence (heraldry, state symbols, bureaucratic framing).
3.  **Idealization / Idealização:** Measures the abstraction of the figure into an eternal allegorical form (erasures of race, age, and historical narrative).

### 3.2. Hybrid Atlas Structure
*   **Volume A: The Narrative Plates:**
    *   8 thematic "Plates" (Warburgian panels).
    *   Clusters of 4–9 images per plate.
    *   Focus on the *Zwischenraum* (relationships between images).
*   **Volume B: The Analytical Index:**
    *   Exhaustive list of all 265 items.
    *   Miniature images + Metadata + Axis Scores.
    *   Sorted by AXIS or COUNTRY for easy reference.

### 3.3. Digital Companion Update
The `iconocracia-companion` Cloudflare Worker will be updated to:
*   Support bilingual English/Portuguese labels.
*   Group candidates by the 8 Atlas Plate categories.
*   Provide dynamic sorting by the three new analytical axes.

## 4. Implementation Workflow

### Stage 1: Data Migration & Standardization
*   **Script:** `tools/scripts/migrate_atlas_schema.py`
*   **Action:** Update `records.jsonl` to map existing indicators to the 3 new axes.
*   **Metadata:** Add `label_en` and `label_pt` fields to the canonical records.

### Stage 2: Atlas Generation Tooling
*   **Script:** `tools/scripts/build_atlas.py`
*   **Function:**
    *   Generate Markdown/HTML snippets for the thesis manuscript.
    *   Compile `atlas-data.json` for the digital companion.
    *   Verify image availability in `CORPUS_IMAGES` R2 bucket.

### Stage 3: Visual Curation (Obsidian)
*   **Location:** `vault/atlas/`
*   **Action:** Create 8 plate-specific notes (`PLATE-01.md`, etc.).
*   **Workflow:** Link corpus records (`[[FR-013]]`) into these notes to define plate clusters.

### Stage 4: Deployment
*   **Command:** `npm run deploy-atlas` (within `deploy/iconocracia-companion/`)
*   **Action:** Push updated data and site code to Cloudflare.

## 5. Success Criteria
1.  All 265 records mapped to the new axes.
2.  8 Comparative Plates curated and rendered in the digital companion.
3.  A generated Empirical Index included in the thesis compilation pipeline.
4.  Bilingual consistency across all Atlas interfaces.

## 6. Self-Review
*   **Placeholder scan:** No "TBD" or "TODO". Workflow scripts are named and defined.
*   **Consistency:** The three axes are applied consistently across print and digital designs.
*   **Scope:** The migration of 265 records is focused and manageable through automation.
*   **Ambiguity:** Bilingual requirements are clearly defined as English primary / Portuguese secondary.
