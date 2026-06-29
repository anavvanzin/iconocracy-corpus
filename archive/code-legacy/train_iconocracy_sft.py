#!/usr/bin/env python3
"""
train_iconocracy_sft.py

TRL SFT training script for ICONOCRACY.

Supports two dataset modes:
1. Explicit split files via train_dataset_path + val_dataset_path
2. Single dataset file via dataset_path + validation_split fallback

Assumes:
- CUDA environment (not local macOS)
- recent versions of: torch, transformers, datasets, peft, trl, bitsandbytes
- chat-format JSONL with a `messages` field on each line

Usage:
    python tools/scripts/train_iconocracy_sft.py \
      --config tools/configs/training/iconocracy_qwen25_7b_qlora.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple

import torch
from datasets import Dataset, load_dataset
from peft import LoraConfig, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer


def load_config(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def apply_chat_template(example: Dict[str, Any], tokenizer: AutoTokenizer) -> Dict[str, str]:
    text = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": text}


def load_train_eval_datasets(cfg: Dict[str, Any], tokenizer: AutoTokenizer) -> Tuple[Dataset, Dataset]:
    train_path = cfg.get("train_dataset_path")
    val_path = cfg.get("val_dataset_path")

    if train_path and val_path:
        train_path = str(Path(train_path).expanduser())
        val_path = str(Path(val_path).expanduser())
        train_dataset = load_dataset("json", data_files=train_path, split="train")
        eval_dataset = load_dataset("json", data_files=val_path, split="train")
    else:
        dataset_path = str(Path(cfg["dataset_path"]).expanduser())
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        validation_split = float(cfg.get("validation_split", 0.05))
        split = dataset.train_test_split(test_size=validation_split, seed=cfg.get("seed", 42))
        train_dataset = split["train"]
        eval_dataset = split["test"]

    train_dataset = train_dataset.map(lambda ex: apply_chat_template(ex, tokenizer), desc="Applying chat template to train")
    eval_dataset = eval_dataset.map(lambda ex: apply_chat_template(ex, tokenizer), desc="Applying chat template to eval")
    return train_dataset, eval_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Train ICONOCRACY SFT model with TRL + QLoRA")
    parser.add_argument("--config", type=Path, required=True, help="Path to JSON config")
    args = parser.parse_args()

    cfg = load_config(args.config)
    output_dir = str(Path(cfg["output_dir"]).expanduser())

    tokenizer = AutoTokenizer.from_pretrained(cfg["base_model"], use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = BitsAndBytesConfig(
        load_in_4bit=cfg.get("load_in_4bit", True),
        bnb_4bit_quant_type=cfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_use_double_quant=cfg.get("bnb_4bit_use_double_quant", True),
        bnb_4bit_compute_dtype=torch.bfloat16 if cfg.get("bf16", True) else torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        cfg["base_model"],
        quantization_config=quant_config,
        device_map="auto",
        attn_implementation=cfg.get("attn_implementation", "sdpa"),
    )
    model.config.use_cache = False
    if cfg.get("gradient_checkpointing", True):
        model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=cfg.get("lora_r", 16),
        lora_alpha=cfg.get("lora_alpha", 32),
        lora_dropout=cfg.get("lora_dropout", 0.05),
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=cfg.get("target_modules"),
    )

    train_dataset, eval_dataset = load_train_eval_datasets(cfg, tokenizer)

    training_args = SFTConfig(
        output_dir=output_dir,
        learning_rate=cfg.get("learning_rate", 2e-5),
        num_train_epochs=cfg.get("num_train_epochs", 2),
        per_device_train_batch_size=cfg.get("per_device_train_batch_size", 2),
        per_device_eval_batch_size=cfg.get("per_device_eval_batch_size", 2),
        gradient_accumulation_steps=cfg.get("gradient_accumulation_steps", 8),
        warmup_ratio=cfg.get("warmup_ratio", 0.03),
        logging_steps=cfg.get("logging_steps", 10),
        save_steps=cfg.get("save_steps", 100),
        eval_steps=cfg.get("eval_steps", 100),
        bf16=cfg.get("bf16", True),
        gradient_checkpointing=cfg.get("gradient_checkpointing", True),
        save_strategy="steps",
        eval_strategy="steps",
        logging_strategy="steps",
        seed=cfg.get("seed", 42),
        max_length=cfg.get("max_seq_length", 2048),
        dataset_text_field="text",
        report_to=[],
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        peft_config=lora_config,
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(json.dumps({
        "status": "ok",
        "output_dir": output_dir,
        "train_examples": len(train_dataset),
        "eval_examples": len(eval_dataset),
        "base_model": cfg["base_model"],
        "train_dataset_path": cfg.get("train_dataset_path"),
        "val_dataset_path": cfg.get("val_dataset_path"),
        "dataset_path": cfg.get("dataset_path"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
