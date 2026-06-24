# Task Plan: Complete pending methodological obligations for ICONOCRACIA thesis defense

## Goal

Fulfill all pending methodological requirements (IRR piloto, codebook congelamento, issues #37 and #38, inclusion of thesis/defense as corpus items, validation, backup) and prepare the manuscript for defense.

## Current Phase

Phase 1

## Phases

### Phase 1: IRR Pilot (Confiabilidade Inter‑observador)
- [ ] Select 30 random images from corpus
- [ ] Create simple evaluation form (Google Form or spreadsheet) with the six LPAi v2 dimensions
- [ ] Share with two additional evaluators (besides yourself)
- [ ] Collect responses and compute Krippendorff α using a Python script (install krippendorff if needed)
- [ ] Record α value in findings.md
- [ ] If α ≥ 0.70, consider pilot successful; otherwise refine criteria and repeat
- **Status:** in_progress

### Phase 2: Codebook Freezing
- [ ] Generate final version of codebook from LPAi v2 (e.g., docs/codebook_v2.md)
- [ ] Add version notes with date and SHA‑256 hash of the file
- [ ] Block any further changes: mention in README that after this date no recoding should alter criteria
- [ ] Update corpus documentation to point to frozen codebook
- **Status:** pending

### Phase 3: Issue #37 – Sul Epistêmico Integration
- [ ] Schedule focused reading session on authors: Glissant, Carneiro, Lugones, Fanon, Mbembe, etc.
- [ ] Extract passages dialoguing with each of the four contracts/alegorias of the thesis
- [ ] Create vault notes for each selected work using pattern CC-NNN Nome.md (starting from 166)
- [ ] Link notes to LPAi v2 dimensions via front‑matter properties
- [ ] Either add these items to records.jsonl (expanding corpus) or create a separate supplementary document (docs/sul_epistemico.md) and reference in chapter 5/6
- **Status:** pending

### Phase 4: Issue #38 – External Audit
- [ ] Identify 2‑3 external experts (history of law, iconography, gender studies)
- [ ] Send them current package: corpus manifest, frozen codebook, purification spreadsheet, preliminary results summary (chapter 6)
- [ ] Schedule 1h structured feedback meetings using a rubric based on the 6 felicidade conditions (α–ζ) and the 3 declared limits
- [ ] Record meeting minutes in vault/sessoes/ as AUDITORIA-YYYY-MM-DD.md
- [ ] Incorporate suggestions into chapter 7 (discussion) or an methodological annex (Anexo M.3)
- **Status:** pending

### Phase 5: Inclusion of Thesis and Defense as Corpus Items
- [ ] Codify the thesis itself and the upcoming defense as items 166‑169 (or follow the numbering after #37 items) using the same six LPAi v2 dimensions
- [ ] Add these entries to the end of data/processed/records.jsonl (or to a supplementary file if keeping corpus of 165 for pure empirical analysis)
- [ ] In chapter 7, reflect on how the academic production inserts itself into the repertoire of feminine state allegories, closing the reflexive loop required by condition ζ
- **Status:** pending

### Phase 6: Validation, Backup & Release Preparation
- [ ] Run schema validation: `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`
- [ ] Execute export diff check: `python tools/scripts/records_to_corpus.py --diff`
- [ ] If clean, build Hugging Face release: `python tools/scripts/build_hf_release.py`
- [ ] Perform vault and corpus backup: `python tools/scripts/vault_backup.py` storing to /data/ssd-backup/iconocracy/ (preserving existing Mac Research backup)
- [ ] Verify backup integrity
- **Status:** pending

### Phase 7: Manuscript Refinement & Defense Preparation
- [ ] Review chapter 6 results: highlight beta = 0.797 for numismatic support, discuss theoretical implications
- [ ] In chapter 5 methodology, add subsection on IRR protocol applied and codebook freezing, emphasizing transparency
- [ ] Ensure chapter 7 addresses recognized limits (arquivo vs repertório, northern epistemic last) and incorporates feedback from external audit and sul‑epistêmico integration
- [ ] Prepare defense slides (≈5 min): problem, method, main finding, limitations, contributions (sul epistêmico, auditoria externa, reflexividade)
- [ ] Rehearse defense talk and anticipate possible questions
- **Status:** pending

## Key Questions
1. What is the acceptable Krippendorff α threshold for this project?
2. How should the sul‑epistêmico materials be integrated—expanded corpus or separate annex?
3. Which external experts are best suited for the audit, and what is their availability?

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use LPAi v2 as situated capture, not positivist score | Resolved methodological tension via METHOD-atlas-vs-score-cartografia-warburguiana.md |
| Treat Atlas topocuratorial as argumentative structure | Same decision |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- Update phase status as you progress: pending → in_progress → complete
- Re‑read this plan before major decisions
- Log ALL errors – they help avoid repetition
- Never repeat a failed action – mutate your approach instead