#!/usr/bin/env python3
"""
split_iconocracy_sft_dataset.py

Create deterministic train/validation splits for ICONOCRACY SFT chat JSONL datasets.

This splitter is stratified by metadata.task_type so the validation file keeps
coverage across task families whenever possible.

Usage:
    python tools/scripts/split_iconocracy_sft_dataset.py \
      --input data/training/iconocracy_sft_v1_1.jsonl \
      --train-output data/training/iconocracy_sft_v1_1_train.jsonl \
      --val-output data/training/iconocracy_sft_v1_1_val.jsonl
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split ICONOCRACY SFT dataset into stratified train/val JSONL files.")
    parser.add_argument("--input", type=Path, required=True, help="Input JSONL dataset")
    parser.add_argument("--train-output", type=Path, required=True, help="Train JSONL output path")
    parser.add_argument("--val-output", type=Path, required=True, help="Validation JSONL output path")
    parser.add_argument("--val-ratio", type=float, default=0.05, help="Validation ratio (default: 0.05)")
    parser.add_argument("--seed", type=int, default=42, help="Shuffle seed")
    args = parser.parse_args()

    rows = load_jsonl(args.input)
    rng = random.Random(args.seed)

    by_task: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        task = row.get("metadata", {}).get("task_type", "unknown")
        by_task[task].append(row)

    train_rows: List[Dict[str, Any]] = []
    val_rows: List[Dict[str, Any]] = []

    for task, task_rows in by_task.items():
        rng.shuffle(task_rows)
        if len(task_rows) == 1:
            # Keep singleton tasks in train; they are too small for meaningful eval.
            train_rows.extend(task_rows)
            continue
        val_count = max(1, int(round(len(task_rows) * args.val_ratio)))
        if val_count >= len(task_rows):
            val_count = len(task_rows) - 1
        val_rows.extend(task_rows[:val_count])
        train_rows.extend(task_rows[val_count:])

    rng.shuffle(train_rows)
    rng.shuffle(val_rows)

    write_jsonl(args.train_output, train_rows)
    write_jsonl(args.val_output, val_rows)

    train_counts = Counter(r.get("metadata", {}).get("task_type", "unknown") for r in train_rows)
    val_counts = Counter(r.get("metadata", {}).get("task_type", "unknown") for r in val_rows)

    print(json.dumps({
        "input": str(args.input),
        "train_output": str(args.train_output),
        "val_output": str(args.val_output),
        "total": len(rows),
        "train": len(train_rows),
        "validation": len(val_rows),
        "val_ratio": args.val_ratio,
        "train_task_types": dict(train_counts),
        "val_task_types": dict(val_counts),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
