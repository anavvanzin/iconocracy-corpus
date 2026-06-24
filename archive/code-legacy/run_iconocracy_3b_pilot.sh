#!/usr/bin/env bash
set -euo pipefail

# End-to-end ICONOCRACY 3B pilot:
# 1. train LoRA adapter
# 2. run eval on base model
# 3. run eval on fine-tuned adapter
# 4. print output locations

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

CONFIG="tools/configs/training/iconocracy_qwen25_3b_qlora_pilot.json"
PROMPTS="data/training/iconocracy_eval_prompts_v1_1.jsonl"
BASE_MODEL="Qwen/Qwen2.5-3B-Instruct"
ADAPTER_DIR_DEFAULT="$HOME/Models/iconocracy-qwen25-3b-sft-pilot-lora"
BASE_EVAL_OUT="data/training/eval_base_qwen3b.jsonl"
FT_EVAL_OUT="data/training/eval_ft_qwen3b.jsonl"

if [[ ! -f "$CONFIG" ]]; then
  echo "Missing config: $CONFIG" >&2
  exit 1
fi

if [[ ! -f "$PROMPTS" ]]; then
  echo "Missing eval prompts: $PROMPTS" >&2
  exit 1
fi

echo "[1/3] Training 3B pilot adapter..."
python tools/scripts/train_iconocracy_sft.py --config "$CONFIG"

ADAPTER_DIR="${ADAPTER_DIR:-$ADAPTER_DIR_DEFAULT}"
if [[ ! -d "$ADAPTER_DIR" ]]; then
  echo "Adapter directory not found after training: $ADAPTER_DIR" >&2
  echo "Set ADAPTER_DIR=/path/to/adapter if your remote environment saved elsewhere." >&2
  exit 1
fi

echo "[2/3] Running eval on base model..."
python tools/scripts/run_iconocracy_eval.py \
  --model "$BASE_MODEL" \
  --prompts "$PROMPTS" \
  --output "$BASE_EVAL_OUT"

echo "[3/3] Running eval on fine-tuned adapter..."
python tools/scripts/run_iconocracy_eval.py \
  --model "$BASE_MODEL" \
  --adapter "$ADAPTER_DIR" \
  --prompts "$PROMPTS" \
  --output "$FT_EVAL_OUT"

echo
echo "Pilot complete. Outputs:"
echo "  Adapter:   $ADAPTER_DIR"
echo "  Base eval: $BASE_EVAL_OUT"
echo "  FT eval:   $FT_EVAL_OUT"
