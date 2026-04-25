# Autonomous agent training decision matrix for ICONOCRACY

> For Hermes: use this document to decide whether the next investment should be orchestration, fine-tuning, or a staged hybrid.

## Goal

Choose the best near-term path for building an autonomous ICONOCRACY agent that can:
- reason over corpus and thesis conventions
- respect provenance and traceability
- operate tools and workflows with discipline
- improve over base-model behavior in a measurable way

## Current repo facts

Confirmed in the repo right now:
- SFT builder exists: `tools/scripts/build_iconocracy_sft_dataset.py`
- stratified split script exists: `tools/scripts/split_iconocracy_sft_dataset.py`
- training script exists: `tools/scripts/train_iconocracy_sft.py`
- eval runner exists: `tools/scripts/run_iconocracy_eval.py`
- pilot shell exists: `tools/scripts/run_iconocracy_3b_pilot.sh`
- 3B pilot config exists: `tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json`
- 7B config exists separately in the training configs
- current SFT dataset already exists and has train/val files
- ARGOS exists as an acquisition/provenance subsystem
- there is no current DSPy-specific implementation surface in the repo

Implication:
- SFT-first has the lowest activation energy
- DSPy-first is strategically attractive but would require new scaffolding
- hybrid is feasible if staged carefully

---

## The three realistic paths

### Path A — DSPy / orchestration-first

Meaning:
- keep the base model mostly unchanged
- improve the agent by programming the workflow better
- focus on modular routing, retrieval, traceability, tool choice, self-checking, and evaluation

What this would look like here:
- add a small `tools/` or `experiments/` surface for DSPy modules
- define signatures for tasks like:
  - corpus note generation
  - provenance explanation
  - ARGOS run diagnosis
  - chapter-planning support
- build modules for retrieval, reasoning, and output validation
- compare outputs before any fine-tuning

Best when:
- the main problems are workflow and reliability
- data quality is still evolving
- you want fast iteration without GPU dependence
- autonomy depends more on decomposition than on memorized domain style

Main upside:
- highest controllability
- least risk of baking bad data into weights
- easiest to change as ARGOS and corpus evolve

Main downside:
- may not improve domain voice/terminology enough by itself
- still depends heavily on base model behavior
- requires fresh architecture work

### Path B — SFT-first

Meaning:
- use the current ICONOCRACY SFT pipeline as the main investment path
- improve the model’s domain behavior through fine-tuning first
- keep agent architecture relatively simple for now

What this would look like here:
- continue improving `build_iconocracy_sft_dataset.py`
- integrate optional ARGOS-derived supervision through a bridge JSONL
- run the 3B pilot, evaluate base vs fine-tuned, then decide on 7B

Best when:
- the main problems are terminology, tone, domain priors, and corpus-specific analytic style
- you already have enough stable examples to teach desired behavior
- you want the model itself to become more thesis-native

Main upside:
- directly improves the model’s default behavior
- strongest path for domain voice and project-specific guardrails
- repo already has working infrastructure for it

Main downside:
- easiest path to overfit templated data
- weak orchestration will still stay weak after fine-tuning
- more expensive to iterate than pure orchestration changes

### Path C — staged hybrid

Meaning:
- do a small amount of orchestration work first
- run a cheap SFT pilot second
- decide later whether the bigger win came from architecture or weights

What this would look like here:
1. add narrow ARGOS/SFT bridge
2. add provenance-aware task families and eval prompts
3. run 3B SFT pilot
4. in parallel, prototype one small orchestration layer for self-checking / provenance discipline
5. compare

Best when:
- you suspect both workflow and domain behavior matter
- you want evidence before committing to large training runs
- the repo is already halfway prepared for SFT but not yet mature enough to justify 7B immediately

Main upside:
- best balance of practical speed and epistemic caution
- reduces risk of choosing the wrong bottleneck
- fits the project’s current maturity level

Main downside:
- more moving parts
- requires discipline to keep the scope small

---

## Decision matrix

Scoring scale: 1 = weak, 5 = strong

| Criterion | DSPy-first | SFT-first | Hybrid |
|---|---:|---:|---:|
| Uses current repo with minimal new scaffolding | 2 | 5 | 4 |
| Improves domain terminology and thesis voice | 2 | 5 | 4 |
| Improves provenance / tool discipline | 5 | 3 | 5 |
| Safe while data is still evolving | 5 | 3 | 4 |
| Cheap to iterate | 5 | 3 | 4 |
| Helps build truly autonomous behavior | 5 | 2 | 5 |
| Reduces risk of overtraining on templates | 5 | 2 | 4 |
| Time-to-first-measurable-result | 3 | 5 | 4 |
| Fit with ARGOS integration work | 4 | 4 | 5 |
| Strategic fit for ICONOCRACY right now | 4 | 4 | 5 |

Interpretation:
- DSPy-first wins on autonomy, controllability, and safety
- SFT-first wins on immediate leverage from what is already built
- Hybrid is the best overall fit because the repo already supports SFT, but the actual agent problem is not only a weights problem

---

## My recommendation

## Recommended path: staged hybrid

Not because it is diplomatically in the middle, but because it matches the actual repo and project state.

Why hybrid is best here:
1. You already have unusually strong SFT scaffolding in place.
2. ARGOS is introducing a provenance/acquisition layer that is more about reasoning discipline than style alone.
3. An autonomous ICONOCRACY agent will fail if either of these is weak:
   - domain behavior in the model
   - orchestration / provenance logic in the runtime
4. The current dataset is good enough for a pilot, but not obviously mature enough to justify betting everything on larger training immediately.

So the best path is:
- small architecture gain first
- cheap SFT pilot second
- evidence-based comparison third

---

## Recommended execution order

### Phase 1 — narrow integration and evaluation hardening

Do first:
1. implement the ARGOS → training bridge
2. add two new SFT task families only:
   - `acquisition_guardrails`
   - `traceability_explainer`
3. expand eval prompts to check provenance discipline

Why:
- this strengthens the dataset exactly where autonomy will matter
- small enough not to destabilize the current pipeline

### Phase 2 — cheap model pilot

Then:
1. rebuild dataset with ARGOS-derived examples
2. regenerate train/val split
3. run the 3B pilot with `tools/scripts/run_iconocracy_3b_pilot.sh`
4. compare base vs FT with the existing eval runner

Decision checkpoint:
- if improvement is mainly terminology/style: training is helping, but architecture still needs work
- if improvement includes provenance discipline and planning quality: fine-tuning is genuinely valuable
- if gains are marginal: do not scale to 7B yet

### Phase 3 — minimal orchestration prototype

In parallel or immediately after the pilot, prototype a small orchestration layer for one high-value loop only:
- provenance-aware corpus-note generation
or
- ARGOS failure diagnosis and next-step recommendation

Do not build a giant agent framework yet.

The goal is to test:
- does workflow decomposition beat fine-tuning for this task family?

### Phase 4 — choose the heavier investment

After Phase 2 + 3, choose one:
- scale to 7B if the fine-tuned model is clearly better
- invest in DSPy/orchestration if the main gains came from better decomposition and validation
- continue hybrid if both added distinct value

---

## What not to do

Do not do these next:
- do not jump straight to 7B main training
- do not try GRPO/RL before the SFT/eval baseline is stable
- do not train directly on raw ARGOS artifacts or unstable HTML/browser output
- do not build a huge autonomous agent shell before testing one narrow orchestration loop

---

## Practical skill stack for this path

Use these skills in this order:
1. `argos-development`
   - for safe ARGOS-side integration and provenance discipline
2. `iconocracy-sft-scaffold`
   - for data/task-family decisions
3. `iconocracy-trl-sft-pilot`
   - for the cheap pilot and eval workflow
4. `dspy`
   - for the orchestration-first comparison path
5. `hermes-agent`
   - for runtime/autonomy architecture decisions
6. `writing-plans`
   - for each implementation slice

---

## Concrete next step

Best next step from here:
- implement phase 1 only

Meaning:
1. create `tools/scripts/export_argos_training_inputs.py`
2. patch `build_iconocracy_sft_dataset.py` to accept `--argos-input`
3. add `acquisition_guardrails` and `traceability_explainer`
4. add provenance-aware eval prompts

This is the smallest move that improves both the training path and the future autonomous-agent path.

---

## Definition of success for the next step

The next step is successful if:
- ARGOS outputs can be exported into a stable training-ready JSONL
- dataset build still succeeds with and without ARGOS input
- new task families appear in train/val outputs
- eval prompts now test provenance/traceability behavior
- no canonical corpus surfaces are overwritten or blurred
