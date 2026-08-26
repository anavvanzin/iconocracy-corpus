# OpenRouter-assisted model evaluation plan for ICONOCRACY

> For Hermes: use subagent-driven-development if this moves into implementation.

**Goal:** add an OpenRouter-based comparison lane to the existing ICONOCRACY evaluation workflow so we can compare candidate base models against the current local SFT path before committing to heavier training.

**Architecture:** keep the current local `run_iconocracy_eval.py` path for Hugging Face + LoRA adapters, and add a parallel OpenRouter evaluation script for remote API models. The OpenRouter lane should produce the same JSONL-shaped outputs as the local eval lane so results can be compared directly.

**Tech Stack:** Python 3.12, existing ICONOCRACY eval prompts JSONL, `requests` or OpenAI-compatible client for OpenRouter, current eval JSONL format, optional local comparison against Qwen 3B base and LoRA adapter.

---

## Why do this now

Current repo facts:
- `tools/scripts/run_iconocracy_eval.py` already exists
- it evaluates local/HuggingFace-style models and optional PEFT adapters
- `tools/scripts/run_iconocracy_3b_pilot.sh` already exists
- `data/training/iconocracy_eval_prompts_v1_1.jsonl` already exists

What is missing:
- a cheap model-selection lane before or alongside training
- a way to answer: is a better base model + stronger prompting enough?
- a way to compare OpenRouter-served models to local base/adapter results using the same prompts

So OpenRouter should be used as a decision tool, not as the core training system.

---

## Decision question this plan answers

Before spending more effort on dataset expansion or larger SFT runs, determine whether:
1. a stronger remote base model already solves much of the problem
2. the current Qwen path still deserves project-specific fine-tuning
3. the real bottleneck is model choice versus training versus orchestration

---

## Recommended candidate models to compare

Start with a small set of 4 models only.

### Group A — baseline open-weight path
1. `Qwen/Qwen2.5-3B-Instruct`
   - reason: matches the existing cheap pilot path conceptually

### Group B — stronger open-weight instruct family
2. `Qwen/Qwen2.5-7B-Instruct` or nearest OpenRouter-available equivalent
   - reason: tests whether a stronger non-fine-tuned Qwen already narrows the gap

### Group C — high-quality API baseline
3. one strong general-purpose model available via OpenRouter
   - likely candidate: a Gemini-, Claude-, or DeepSeek-class model available in your pricing/routing comfort zone
   - reason: establishes an upper baseline for “just use a better model”

### Group D — low-cost reasoning/value model
4. one cheaper OpenRouter model
   - reason: tests whether acceptable domain behavior can be achieved cheaply without training

Important rule:
- keep the comparison set small at first
- 4 models is enough for the first decision round

---

## What to compare

Use the exact existing prompt set first:
- `data/training/iconocracy_eval_prompts_v1_1.jsonl`

Primary comparison axes:
1. terminology discipline
2. method correctness
3. chapter-planning adherence
4. corpus-analysis usefulness
5. provenance / traceability caution

Once the ARGOS integration slice lands, add provenance-aware prompts too.

---

## Output contract

The OpenRouter eval lane should emit JSONL with the same core fields currently used by `run_iconocracy_eval.py`:

```json
{
  "id": "prompt-001",
  "category": "guardrails",
  "prompt": "...",
  "expectations": ["..."],
  "model": "openrouter:model-id",
  "adapter": null,
  "response": "..."
}
```

Optional additive fields are fine:
- `provider`: `openrouter`
- `latency_ms`
- `cost_estimate`
- `raw_model_id`

But do not break the shared comparison shape.

---

## Recommended implementation slice

### Task 1: Add a dedicated OpenRouter eval runner

**Objective:** create a script that runs the current ICONOCRACY eval prompts against OpenRouter models and writes compatible JSONL outputs.

**Files:**
- Create: `tools/scripts/run_iconocracy_eval_openrouter.py`
- Test: `tests/training/test_run_iconocracy_eval_openrouter.py`

**Step 1: Write failing test**

Test behaviors:
- loads prompt JSONL
- builds request payload with the existing system prompt
- writes one JSONL row per prompt
- preserves output fields `id`, `category`, `prompt`, `expectations`, `model`, `adapter`, `response`

Use request mocking rather than live API calls in unit tests.

**Step 2: Run test to verify failure**

Run:
`python -m unittest tests.training.test_run_iconocracy_eval_openrouter -v`

Expected:
- fail because script/module does not yet exist

**Step 3: Write minimal implementation**

Implementation requirements:
- read `OPENROUTER_API_KEY` from environment
- accept:
  - `--model`
  - `--prompts`
  - `--output`
  - `--max-tokens`
  - `--temperature`
- use the same system prompt currently embedded in `run_iconocracy_eval.py`
- write JSONL rows in the shared shape

**Step 4: Run test to verify pass**

Run:
`python -m unittest tests.training.test_run_iconocracy_eval_openrouter -v`

Expected:
- PASS

**Step 5: Commit**

```bash
git add tools/scripts/run_iconocracy_eval_openrouter.py tests/training/test_run_iconocracy_eval_openrouter.py
git commit -m "feat: add openrouter eval runner for iconocracy prompts"
```

---

### Task 2: Add a tiny comparison utility

**Objective:** make side-by-side comparison easier without requiring manual diffing of JSONL files.

**Files:**
- Create: `tools/scripts/compare_iconocracy_eval_runs.py`
- Test: `tests/training/test_compare_iconocracy_eval_runs.py`

**Step 1: Write failing test**

Test behaviors:
- loads two or more eval JSONL files
- groups rows by prompt `id`
- prints a markdown or text summary with prompt id, category, compared models, and truncated responses

**Step 2: Run test to verify failure**

Run:
`python -m unittest tests.training.test_compare_iconocracy_eval_runs -v`

Expected:
- FAIL because script does not yet exist

**Step 3: Write minimal implementation**

Implementation requirements:
- inputs:
  - `--inputs file1.jsonl file2.jsonl ...`
  - `--output optional_path`
- output:
  - readable markdown or plain text summary
- do not add scoring logic yet; keep v1 focused on aligned comparison output

**Step 4: Run test to verify pass**

Run:
`python -m unittest tests.training.test_compare_iconocracy_eval_runs -v`

Expected:
- PASS

**Step 5: Commit**

```bash
git add tools/scripts/compare_iconocracy_eval_runs.py tests/training/test_compare_iconocracy_eval_runs.py
git commit -m "feat: add iconocracy eval comparison utility"
```

---

### Task 3: Add an execution doc for the first comparison round

**Objective:** define exactly which models to compare and in what order.

**Files:**
- Create: `docs/superpowers/specs/2026-04-14-openrouter-eval-round-1.md`

**Step 1: Write the comparison matrix**

Document these lanes:
1. local base `Qwen/Qwen2.5-3B-Instruct`
2. local fine-tuned 3B adapter when available
3. OpenRouter strong model
4. OpenRouter cheaper model
5. optionally OpenRouter stronger Qwen-family model

**Step 2: Define evaluation questions**

For each model, review:
- Endurecimento preservation
- Mondzain / Feminilidade de Estado guardrail
- QUAN→QUAL→síntese explanation
- corpus traceability correctness
- thesis-planning usefulness

**Step 3: Define stop/go conditions**

Write rules such as:
- if a strong OpenRouter base model already solves most prompt categories, delay larger SFT investment
- if fine-tuned Qwen clearly beats remote base models on terminology + planning + corpus notes, continue SFT path
- if neither is clearly strong, prioritize orchestration and dataset quality before larger training

**Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-04-14-openrouter-eval-round-1.md
git commit -m "docs: add openrouter evaluation round 1 plan"
```

---

### Task 4: Add one shell wrapper for the first eval round

**Objective:** reduce operator friction for the first OpenRouter comparison batch.

**Files:**
- Create: `tools/scripts/run_iconocracy_openrouter_eval_round_1.sh`

**Step 1: Check prerequisites in script**

Must verify:
- `OPENROUTER_API_KEY` is set
- prompts file exists
- output directory exists or can be created

**Step 2: Run 2–4 model evaluations**

The script should call:
- `python tools/scripts/run_iconocracy_eval_openrouter.py ...`
for each selected OpenRouter model

Use clearly named outputs like:
- `data/training/eval_openrouter_model_a.jsonl`
- `data/training/eval_openrouter_model_b.jsonl`

**Step 3: Optionally run the comparison utility**

If local base/fine-tuned outputs already exist, include them in the comparison summary too.

**Step 4: Verify shell syntax**

Run:
`bash -n tools/scripts/run_iconocracy_openrouter_eval_round_1.sh`

Expected:
- no syntax errors

**Step 5: Commit**

```bash
git add tools/scripts/run_iconocracy_openrouter_eval_round_1.sh
git commit -m "feat: add openrouter eval round 1 wrapper"
```

---

### Task 5: Run the first decision round

**Objective:** collect evidence before committing to a bigger training step.

**Files:**
- Outputs under: `data/training/`
- Summary under: `docs/superpowers/specs/` or `docs/plans/`

**Step 1: Run local baseline if needed**

Run existing local eval lane:
```bash
python tools/scripts/run_iconocracy_eval.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
  --output data/training/eval_base_qwen3b.jsonl
```

**Step 2: Run OpenRouter round 1 wrapper**

Run:
```bash
bash tools/scripts/run_iconocracy_openrouter_eval_round_1.sh
```

**Step 3: Generate side-by-side comparison output**

Run:
```bash
python tools/scripts/compare_iconocracy_eval_runs.py \
  --inputs data/training/eval_base_qwen3b.jsonl data/training/eval_openrouter_*.jsonl \
  --output docs/plans/2026-04-14-openrouter-round-1-comparison.md
```

**Step 4: Review manually with the existing eval guide**

Use:
- `docs/superpowers/specs/2026-04-11-iconocracy-sft-eval-guide.md`

**Step 5: Write conclusion memo**

Create:
- `docs/plans/2026-04-14-openrouter-round-1-conclusion.md`

Conclusion must answer:
- is better base model selection enough for now?
- does local fine-tuning still look strategically necessary?
- which prompt categories remain weak regardless of model?

---

## Candidate model policy

Round 1 should not optimize forever.

Rules:
- maximum 4 OpenRouter models
- prefer one model per role:
  - cheap
  - strong
  - Qwen-family stronger base
  - optional reasoning-oriented candidate
- stop after the first round if one path is obviously better

---

## What counts as a successful decision round

Success does not mean “find the perfect model.”

It means you can answer these 3 questions with evidence:
1. Is the current local SFT path still justified?
2. Would a stronger OpenRouter-served base model delay or replace the need for near-term fine-tuning?
3. Which deficits are actually architecture/data problems rather than model-choice problems?

---

## Recommended immediate next move

If implementing now, do only Tasks 1–3 first:
1. `run_iconocracy_eval_openrouter.py`
2. `compare_iconocracy_eval_runs.py`
3. `2026-04-14-openrouter-eval-round-1.md`

Why:
- smallest useful slice
- enough to make OpenRouter genuinely decision-relevant
- avoids premature scripting around still-unstable model choices
