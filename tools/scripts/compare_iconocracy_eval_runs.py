#!/usr/bin/env python3
"""
compare_iconocracy_eval_runs.py

Create a side-by-side markdown comparison across two or more ICONOCRACY eval JSONL runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def truncate(text: str, limit: int = 400) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def collect_rows(paths: Iterable[Path]) -> Dict[str, Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"prompt": None, "category": None, "expectations": [], "runs": []})
    for path in paths:
        for row in load_jsonl(path):
            prompt_id = row["id"]
            entry = grouped[prompt_id]
            entry["prompt"] = row.get("prompt")
            entry["category"] = row.get("category")
            entry["expectations"] = row.get("expectations", [])
            entry["runs"].append(
                {
                    "model": row.get("model"),
                    "adapter": row.get("adapter"),
                    "provider": row.get("provider"),
                    "response": row.get("response", ""),
                    "source_file": str(path),
                }
            )
    return dict(sorted(grouped.items(), key=lambda item: item[0]))


def render_markdown(grouped: Dict[str, Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# ICONOCRACY eval run comparison")
    lines.append("")
    lines.append(f"Compared prompts: {len(grouped)}")
    lines.append("")
    for prompt_id, entry in grouped.items():
        lines.append(f"## {prompt_id}")
        lines.append("")
        if entry.get("category"):
            lines.append(f"- Category: `{entry['category']}`")
        if entry.get("expectations"):
            lines.append("- Expectations:")
            for expectation in entry["expectations"]:
                lines.append(f"  - {expectation}")
        lines.append("")
        lines.append("### Prompt")
        lines.append("")
        lines.append(entry.get("prompt") or "")
        lines.append("")
        lines.append("### Responses")
        lines.append("")
        for run in entry.get("runs", []):
            label = run.get("model") or "unknown-model"
            if run.get("adapter"):
                label += f" + adapter={run['adapter']}"
            lines.append(f"#### {label}")
            lines.append("")
            if run.get("provider"):
                lines.append(f"- Provider: `{run['provider']}`")
            lines.append(f"- Source: `{run['source_file']}`")
            lines.append("")
            lines.append(truncate(run.get("response", "")))
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two or more ICONOCRACY eval JSONL runs")
    parser.add_argument("--inputs", nargs="+", type=Path, required=True, help="Eval JSONL files to compare")
    parser.add_argument("--output", type=Path, help="Optional markdown output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    grouped = collect_rows(args.inputs)
    markdown = render_markdown(grouped)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(json.dumps({"status": "ok", "output": str(args.output), "prompts": len(grouped)}, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
