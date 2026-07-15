# Task Plan: Clean SFT Datasets from Fake Zeros

**Goal:** Clean the language model training data (SFT files) that were generated on June 30th containing the "fake zero" contaminated records (the 76 items from vault-import/migration). This ensures any downstream model trained on Iconocracia data learns from the N=161 truly coded items, avoiding bias toward artificially low endurecimento scores.

## Context
We discovered that `Downloads/data/training/` held SFT files (`iconocracy_sft_v1_1.jsonl`, etc.) which included the contaminated dataset. Since we purged that backup, we need to regenerate or clean the canonical training sets wherever they reside (likely inside the `hub/iconocracy-corpus/data/` structure) so future fine-tuning is methodologically sound.

## Phases

### Phase 1: Locate Canonical SFT Files
- **Status:** complete

### Phase 2: Filter Contamination
- **Status:** complete

### Phase 3: Final Verification
- **Status:** complete

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| | | |

## Verification
- [ ] No `vault-import` or `migration` items remain in the training datasets.
