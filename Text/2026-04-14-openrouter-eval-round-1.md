# OpenRouter eval round 1 for ICONOCRACY

Goal: compare a small set of OpenRouter-served base models against the existing local ICONOCRACY evaluation lane before committing to more training work.

## Existing comparison lanes

Local lanes already available:
1. local base `Qwen/Qwen2.5-3B-Instruct`
2. local fine-tuned 3B adapter, when the pilot run exists

New lanes for round 1:
3. one stronger OpenRouter-served Qwen-family model
4. one strong general-purpose OpenRouter model
5. one cheaper OpenRouter model

Keep round 1 small. Maximum 4 OpenRouter models.

## Prompt set

Use the current shared prompt file:
- `data/training/iconocracy_eval_prompts_v1_1.jsonl`

Do not change the prompt set during round 1. The point is to compare model behavior on the same tasks.

## What to score qualitatively

For each model, review:
1. Terminology
   - preserves `endurecimento`
   - does not misattribute `Feminilidade de Estado`
2. Method
   - explains QUAN→QUAL→síntese correctly
   - distinguishes records and purification surfaces
3. Thesis planning
   - answers with adherence to project plans
   - avoids generic academic filler
4. Corpus reasoning
   - produces useful, cautious analytical notes
   - distinguishes observation from inference
5. Traceability discipline
   - respects canonical truth-order
   - does not overclaim from derived or uncertain material

## Suggested initial candidate set

Use a compact set like this, adjusting only if a model is unavailable or too expensive:

1. Local baseline
- `Qwen/Qwen2.5-3B-Instruct`

2. OpenRouter stronger Qwen-family baseline
- nearest available stronger Qwen instruct model

3. OpenRouter strong API baseline
- one high-quality general-purpose model

4. OpenRouter cheaper value baseline
- one lower-cost but competent model

## Stop/go rules

### Continue toward more SFT investment if:
- the local fine-tuned 3B adapter clearly beats the remote base models on terminology, planning, and corpus-note usefulness
- or the OpenRouter models still miss project-specific guardrails that the fine-tuned model captures reliably

### Delay larger SFT investment if:
- a strong OpenRouter base model already performs very well across most prompt categories
- and the fine-tuned local model adds little beyond small style differences

### Prioritize orchestration/data work if:
- all models remain weak on provenance discipline or traceability
- or all models produce plausible but epistemically sloppy answers
- or gains are inconsistent across categories

## Expected outputs

Round 1 should produce:
- local eval JSONL outputs under `data/training/`
- OpenRouter eval JSONL outputs under `data/training/`
- one comparison markdown file
- one conclusion memo

## Conclusion questions

The round is complete only when we can answer:
1. Is a better base model enough for now?
2. Does the local SFT path still look strategically justified?
3. Which failures are really architecture/data failures rather than model-choice failures?
