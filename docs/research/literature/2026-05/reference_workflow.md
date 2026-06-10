# Reference Workflow (Week 2)

> Process doc do bundle dialético — workflow de rastreabilidade claim→fonte→confiança.

## Goal

Create a traceable pipeline where every claim in your writing maps to:

- one row in the evidence matrix
- one registered source record
- a clear confidence score

## Files To Use

- `reference_register_template.csv`: source-level metadata (one row per source).
- `evidence_matrix_template.csv`: claim-level evidence (one row per claim).

## Step-By-Step Workflow

1. **Register source first.** Add a new `source_id` (SRC-0001, ...); fill `source_type`, `country_focus`, `period_focus`, `support_focus`; mark `primary_secondary` and `state_sanction_evidence`.
2. **Extract claims second.** One row per substantive claim (CLM-0001, ...); link to `source_id`; keep claim atomic.
3. **Assign core fields consistently.** `source_type`, `support`, `country` from controlled values below; `period` as YYYY or YYYY-YYYY; `confidence` per 1–5 rubric.
4. **Save verification details.** `page_or_locator`; `evidence_excerpt` (factual, no interpretation); `status` ∈ {draft, verified, rejected}.
5. **Run weekly QA.** Check missing `source_id`, empty period, confidence without locator; resolve duplicates; promote only verified rows to drafting.

## Controlled Values

- **source_type:** journal_article · book · book_chapter · legal_document · archival_record · catalog_record · government_report · thesis · conference_paper · press_piece
- **support:** coin · banknote · stamp · monument · court_interior · court_exterior · poster · coat_of_arms · mixed
- **country:** Brazil · UK · France · Germany · Spain · USA · Comparative

## Confidence Rubric (1–5)

- **5:** Direct primary evidence, explicit claim, precise locator, minimal ambiguity.
- **4:** Strong evidence with clear locator, minor interpretation needed.
- **3:** Plausible but indirect evidence; some uncertainty remains.
- **2:** Weak or partial support; wording/context not fully aligned.
- **1:** Speculative; insufficient support for thesis use.

## Weekly Output Rule

At the end of each week, produce: updated source register; updated evidence matrix; short log (total claims, verified, rejected, unresolved).

## Minimum Completion Criteria For Week 2

- ≥ 40 registered sources · ≥ 120 claim rows extracted · ≥ 60 verified · zero verified rows missing `source_id`, period, or `page_or_locator`.
