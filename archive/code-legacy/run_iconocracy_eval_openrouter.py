#!/usr/bin/env python3
"""
run_iconocracy_eval_openrouter.py

Run the ICONOCRACY evaluation prompt set against an OpenRouter-served model.

Example:
    OPENROUTER_API_KEY=... python tools/scripts/run_iconocracy_eval_openrouter.py \
      --model openai/gpt-4.1-mini \
      --prompts data/training/iconocracy_eval_prompts_v1_1.jsonl \
      --output data/training/eval_openrouter_gpt41mini.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests

SYSTEM_PROMPT = (
    "Você é um assistente de pesquisa e redação da tese ICONOCRACIA. "
    "Use voz jurídico-histórica rigorosa, preserve a terminologia mandatória do projeto "
    "e não invente fatos ausentes da evidência fornecida. Nunca traduza endurecimento, "
    "nunca atribua Feminilidade de Estado a Mondzain e não trate claims do pipeline "
    "como prova conclusiva sem qualificação."
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


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


def parse_response(payload: Dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        raise ValueError("OpenRouter response missing choices")
    message = choices[0].get("message") or {}
    content = message.get("content", "")
    if isinstance(content, list):
        chunks: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                chunks.append(str(item.get("text", "")))
            else:
                chunks.append(str(item))
        return "".join(chunks).strip()
    return str(content).strip()


def run_prompt(
    *,
    model: str,
    prompt_text: str,
    api_key: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    timeout: int,
    site_url: str | None = None,
    site_name: str | None = None,
) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_name:
        headers["X-Title"] = site_name

    body = {
        "model": model,
        "messages": build_messages(prompt_text),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
    }

    started = time.time()
    response = requests.post(OPENROUTER_URL, headers=headers, json=body, timeout=timeout)
    response.raise_for_status()
    latency_ms = int((time.time() - started) * 1000)
    payload = response.json()

    return {
        "response": parse_response(payload),
        "latency_ms": latency_ms,
        "usage": payload.get("usage"),
        "raw_model_id": payload.get("model", model),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ICONOCRACY eval prompts against an OpenRouter model")
    parser.add_argument("--model", required=True, help="OpenRouter model id")
    parser.add_argument("--prompts", type=Path, required=True, help="Eval prompt JSONL")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL with generations")
    parser.add_argument("--max-tokens", type=int, default=220)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--site-url", default="https://github.com/anavvanzin/iconocracy-corpus")
    parser.add_argument("--site-name", default="ICONOCRACY Eval")
    parser.add_argument("--api-key", help="Optional OpenRouter API key; defaults to OPENROUTER_API_KEY env var")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("Missing OpenRouter API key. Set OPENROUTER_API_KEY or pass --api-key.")

    prompts = load_jsonl(args.prompts)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as f:
        for row in prompts:
            result = run_prompt(
                model=args.model,
                prompt_text=row["prompt"],
                api_key=api_key,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                top_p=args.top_p,
                timeout=args.timeout,
                site_url=args.site_url,
                site_name=args.site_name,
            )
            output_row = {
                "id": row["id"],
                "category": row.get("category"),
                "prompt": row["prompt"],
                "expectations": row.get("expectations", []),
                "model": f"openrouter:{args.model}",
                "adapter": None,
                "provider": "openrouter",
                "latency_ms": result["latency_ms"],
                "raw_model_id": result.get("raw_model_id"),
                "usage": result.get("usage"),
                "response": result["response"],
            }
            f.write(json.dumps(output_row, ensure_ascii=False) + "\n")

    print(json.dumps({
        "status": "ok",
        "prompts": len(prompts),
        "output": str(args.output),
        "model": f"openrouter:{args.model}",
        "provider": "openrouter",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"OpenRouter request failed: {exc}", file=sys.stderr)
        raise
