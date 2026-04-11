#!/usr/bin/env python3
"""Repo-level helper for the ICONOCRACY CLIP prototype.

Wraps the Hermes skill-local CLIP script so it can be invoked from the repo with
stable defaults and corpus-friendly path handling.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = Path.home() / ".hermes" / "skills" / "research" / "iconocracy-agent"
SKILL_VENV_PYTHON = SKILL_ROOT / ".venv" / "bin" / "python"
SKILL_SCRIPT = SKILL_ROOT / "scripts" / "clip_iconocracy_prototype.py"
DEFAULT_PROMPTS = SKILL_ROOT / "templates" / "clip-prompts-iconocracy.txt"
DEFAULT_GALLERY = REPO_ROOT / "gallery"


def existing_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.exists():
        raise argparse.ArgumentTypeError(f"path does not exist: {value}")
    return path


def ensure_runtime() -> None:
    missing = [
        path
        for path in [SKILL_VENV_PYTHON, SKILL_SCRIPT, DEFAULT_PROMPTS]
        if not path.exists()
    ]
    if missing:
        joined = "\n  - ".join(str(path) for path in missing)
        raise SystemExit(
            "ICONOCRACY CLIP runtime is incomplete. Missing:\n"
            f"  - {joined}\n"
            "Expected Hermes skill assets under ~/.hermes/skills/research/iconocracy-agent/."
        )


def iter_images(paths: Sequence[Path], recursive: bool, exts: set[str]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path.is_file() and path.suffix.lower() in exts:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                out.append(resolved)
            continue
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            for candidate in sorted(path.glob(pattern)):
                if candidate.is_file() and candidate.suffix.lower() in exts:
                    resolved = candidate.resolve()
                    if resolved not in seen:
                        seen.add(resolved)
                        out.append(resolved)
    return out


def run_skill(args: Sequence[str]) -> dict:
    proc = subprocess.run(
        [str(SKILL_VENV_PYTHON), str(SKILL_SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f"skill script failed with code {proc.returncode}")

    stdout = proc.stdout.strip()
    start = stdout.find("{")
    if start == -1:
        raise SystemExit(f"Could not find JSON output from skill script. Raw output:\n{stdout}")
    try:
        return json.loads(stdout[start:])
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse JSON output: {exc}\nRaw output:\n{stdout}") from exc


def cmd_rank(ns: argparse.Namespace) -> int:
    ensure_runtime()
    images = iter_images(ns.paths, recursive=ns.recursive, exts={".jpg", ".jpeg", ".png", ".webp"})
    if not images:
        raise SystemExit("No images found. Pass files or directories containing jpg/jpeg/png/webp files.")

    if ns.limit:
        images = images[: ns.limit]

    payload = run_skill(
        [
            "--model",
            ns.model,
            "rank",
            "--images",
            *[str(path) for path in images],
            "--prompts",
            str(ns.prompts),
            "--top-k",
            str(ns.top_k),
        ]
    )

    if ns.output:
        ns.output.parent.mkdir(parents=True, exist_ok=True)
        ns.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_pair(ns: argparse.Namespace) -> int:
    ensure_runtime()
    payload = run_skill(
        [
            "--model",
            ns.model,
            "pair",
            "--image-a",
            str(ns.image_a.resolve()),
            "--image-b",
            str(ns.image_b.resolve()),
        ]
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_embed(ns: argparse.Namespace) -> int:
    ensure_runtime()
    images = iter_images(ns.paths, recursive=ns.recursive, exts={".jpg", ".jpeg", ".png", ".webp"})
    if not images:
        raise SystemExit("No images found. Pass files or directories containing jpg/jpeg/png/webp files.")
    if ns.limit:
        images = images[: ns.limit]

    payload = run_skill(
        [
            "--model",
            ns.model,
            "embed",
            "--images",
            *[str(path) for path in images],
            "--output",
            str(ns.output),
        ]
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repo-level wrapper for the ICONOCRACY CLIP prototype"
    )
    parser.add_argument(
        "--model",
        default="openai/clip-vit-base-patch32",
        help="CLIP model name passed through to the skill script",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    rank = sub.add_parser("rank", help="rank one or more images against the ICONOCRACY prompt set")
    rank.add_argument(
        "paths",
        nargs="*",
        type=existing_path,
        default=[DEFAULT_GALLERY / "gallica"],
        help="image files or directories (default: gallery/gallica)",
    )
    rank.add_argument("--recursive", action="store_true", help="recurse into directories")
    rank.add_argument("--limit", type=int, help="limit number of images after collection")
    rank.add_argument("--top-k", type=int, default=5, help="matches to keep per image")
    rank.add_argument(
        "--prompts",
        type=existing_path,
        default=DEFAULT_PROMPTS,
        help="prompt file (default: skill template prompts)",
    )
    rank.add_argument(
        "--output",
        type=Path,
        help="optional path to save JSON output",
    )
    rank.set_defaults(func=cmd_rank)

    pair = sub.add_parser("pair", help="measure similarity between two images")
    pair.add_argument("image_a", type=existing_path)
    pair.add_argument("image_b", type=existing_path)
    pair.set_defaults(func=cmd_pair)

    embed = sub.add_parser("embed", help="generate JSONL embeddings for one or more images")
    embed.add_argument(
        "paths",
        nargs="*",
        type=existing_path,
        default=[DEFAULT_GALLERY / "gallica"],
        help="image files or directories (default: gallery/gallica)",
    )
    embed.add_argument("--recursive", action="store_true", help="recurse into directories")
    embed.add_argument("--limit", type=int, help="limit number of images after collection")
    embed.add_argument(
        "--output",
        type=Path,
        required=True,
        help="output JSONL file",
    )
    embed.set_defaults(func=cmd_embed)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return ns.func(ns)


if __name__ == "__main__":
    raise SystemExit(main())
