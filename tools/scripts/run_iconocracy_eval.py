#!/usr/bin/env python3
"""
run_iconocracy_eval.py

Run the ICONOCRACY evaluation prompt set against a base model or a LoRA adapter.

Examples:
    python tools/scripts/run_iconocracy_eval.py \
      --model Qwen/Qwen2.5-3B-Instruct \
      --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
      --output data/training/eval_base_qwen3b.jsonl

    python tools/scripts/run_iconocracy_eval.py \
      --model Qwen/Qwen2.5-3B-Instruct \
      --adapter ~/Models/iconocracy-qwen25-3b-sft-pilot-lora \
      --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
      --output data/training/eval_ft_qwen3b.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

SYSTEM_PROMPT = (
    "Você é um assistente de pesquisa e redação da tese ICONOCRACIA. "
    "Use voz jurídico-histórica rigorosa, preserve a terminologia mandatória do projeto "
    "e não invente fatos ausentes da evidência fornecida. Nunca traduza ENDURECIMENTO, "
    "nunca atribua Feminilidade de Estado a Mondzain e não trate claims do pipeline "
    "como prova conclusiva sem qualificação."
)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_messages(prompt_text: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ICONOCRACY eval prompts against a base model or LoRA adapter")
    parser.add_argument("--model", required=True, help="Base model name or path")
    parser.add_argument("--adapter", help="Optional PEFT adapter path")
    parser.add_argument("--prompts", type=Path, required=True, help="Eval prompt JSONL")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL with generations")
    parser.add_argument("--max-new-tokens", type=int, default=220)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.95)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )
    if args.adapter:
        model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()

    prompts = load_jsonl(args.prompts)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as f:
        for row in prompts:
            messages = build_messages(row["prompt"])
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(text, return_tensors="pt").to(model.device)
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=args.max_new_tokens,
                    do_sample=args.temperature > 0,
                    temperature=args.temperature,
                    top_p=args.top_p,
                    pad_token_id=tokenizer.eos_token_id,
                )
            generated = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
            result = {
                "id": row["id"],
                "category": row.get("category"),
                "prompt": row["prompt"],
                "expectations": row.get("expectations", []),
                "model": args.model,
                "adapter": args.adapter,
                "response": generated,
            }
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(json.dumps({
        "status": "ok",
        "prompts": len(prompts),
        "output": str(args.output),
        "model": args.model,
        "adapter": args.adapter,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
