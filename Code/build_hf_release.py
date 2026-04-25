#!/usr/bin/env python3
"""Build a Hugging Face dataset release snapshot from the local thesis repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CORPUS = REPO / "corpus" / "corpus-data.json"
RECORDS = REPO / "data" / "processed" / "records.jsonl"
PURIFICATION = REPO / "data" / "processed" / "purification.jsonl"
DEFAULT_OUTPUT_ROOT = REPO / "output" / "huggingface"
DEFAULT_DATASET_REPO = "warholana/iconocracy-corpus"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a release snapshot for the Hugging Face dataset.")
    parser.add_argument(
        "--dataset-repo",
        default=DEFAULT_DATASET_REPO,
        help=f"Target dataset repo id (default: {DEFAULT_DATASET_REPO})",
    )
    parser.add_argument(
        "--release-tag",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Release tag and output folder name (default: today's UTC date).",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Root directory for generated snapshots (default: {DEFAULT_OUTPUT_ROOT})",
    )
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Release note line to include in CHANGELOG and README. Repeat as needed.",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Upload the generated snapshot using `hf upload` after building it.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing snapshot directory for the same release tag.",
    )
    return parser.parse_args()


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compact_counter(counter: Counter, limit: int = 8) -> dict[str, int]:
    return dict(counter.most_common(limit))


def compute_stats(corpus: list[dict], records: list[dict], purification: list[dict]) -> dict:
    countries = Counter((item.get("country") or "Unknown") for item in corpus)
    regimes = Counter((item.get("regime") or "unknown") for item in corpus)
    supports = Counter(
        (
            item.get("support")
            or item.get("medium_norm")
            or item.get("medium")
            or "unknown"
        )
        for item in corpus
    )
    scores = [
        float(item["endurecimento_score"])
        for item in corpus
        if isinstance(item.get("endurecimento_score"), (int, float))
    ]
    coded_ids = sorted({row.get("id") for row in purification if row.get("id")})
    schema_versions = sorted({row.get("master_record_version", "unknown") for row in records})

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "corpus_items": len(corpus),
        "records_items": len(records),
        "purification_rows": len(purification),
        "coded_items": len(coded_ids),
        "country_count": len(countries),
        "schema_versions": schema_versions,
        "regime_counts": dict(regimes),
        "top_countries": compact_counter(countries),
        "top_supports": compact_counter(supports),
        "mean_endurecimento": round(sum(scores) / len(scores), 3) if scores else None,
        "corpus_records_delta": len(corpus) - len(records),
    }


def render_changelog(notes: list[str], stats: dict) -> str:
    lines = notes[:] if notes else []
    if not lines:
        lines.append("Generated from the local release pipeline.")
    lines.append(
        f"Snapshot counts: corpus={stats['corpus_items']}, records={stats['records_items']}, coded={stats['coded_items']}."
    )
    return "\n".join(f"- {line}" for line in lines) + "\n"


def render_readme(dataset_repo: str, release_tag: str, stats: dict, changelog: str) -> str:
    schema_versions = ", ".join(stats["schema_versions"]) if stats["schema_versions"] else "unknown"
    mean_score = "n/a" if stats["mean_endurecimento"] is None else str(stats["mean_endurecimento"])
    delta = stats["corpus_records_delta"]
    drift_line = "No corpus/records drift detected." if delta == 0 else (
        f"Corpus/records drift detected: corpus-data.json has {abs(delta)} "
        f"{'more' if delta > 0 else 'fewer'} item(s) than records.jsonl."
    )

    return f"""---
license: cc-by-4.0
language:
- pt
- en
- fr
- de
pretty_name: ICONOCRACY Corpus
size_categories:
- n<1K
tags:
- iconography
- legal-iconography
- legal-history
- female-allegory
- digital-humanities
- cultural-heritage
- political-iconography
- feminist-iconography
- abnt
- metadata
---

# ICONOCRACY Corpus

Release snapshot for `{dataset_repo}` built from the local `iconocracy-corpus` repository.

## Current release

- Release tag: `{release_tag}`
- Generated at: `{stats['generated_at']}`
- Corpus items: **{stats['corpus_items']}**
- Canonical records: **{stats['records_items']}**
- Coded items: **{stats['coded_items']}**
- Countries represented: **{stats['country_count']}**
- Mean endurecimento score: **{mean_score}**
- Master-record schema versions: `{schema_versions}`

## Contract

This dataset is a **release artifact**, not a live working mirror.

Source-of-truth hierarchy:

1. `data/processed/records.jsonl`
2. `corpus/corpus-data.json`
3. `data/processed/purification.jsonl`

`vault/candidatos/` remains an auxiliary mirror only.

## Release notes

{changelog}
## Validation notes

- `{drift_line}`
- Raw binaries remain outside the repository and live in Google Drive.
- Notion is out of scope for the active workflow.

## Files

- `corpus-data.json`
- `records.jsonl`
- `purification.jsonl`
- `release.json`
- `CHANGELOG.md`

## License

Metadata: CC BY 4.0. Original images remain subject to their source institution rights.
"""


def ensure_hf_auth() -> None:
    if shutil.which("hf") is None:
        raise SystemExit("hf CLI not found on PATH; cannot publish.")
    result = subprocess.run(["hf", "auth", "whoami"], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit("hf CLI is not authenticated. Run `hf auth login` first.")


def validate_local_contract() -> None:
    """Fail closed if local dataset artifacts are invalid or drifted."""
    validate_script = REPO / "tools" / "scripts" / "validate_schemas.py"
    subprocess.run(
        [sys.executable, str(validate_script), str(RECORDS), "--schema", "master-record", "--verbose"],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(validate_script), str(PURIFICATION), "--schema", "purification-record", "--verbose"],
        check=True,
    )

    corpus = load_json(CORPUS)
    records = load_jsonl(RECORDS)
    purification = load_jsonl(PURIFICATION)
    stats = compute_stats(corpus, records, purification)
    delta = stats["corpus_records_delta"]
    if delta != 0:
        raise SystemExit(
            "Refusing to build HF snapshot: corpus/records drift detected "
            f"(corpus={stats['corpus_items']}, records={stats['records_items']}, delta={delta})."
        )


def write_sha256sums(snapshot_dir: Path) -> None:
    lines: list[str] = []
    for name in ["corpus-data.json", "records.jsonl", "purification.jsonl", "release.json", "CHANGELOG.md", "README.md"]:
        path = snapshot_dir / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {name}")
    (snapshot_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def publish_snapshot(dataset_repo: str, snapshot_dir: Path, release_tag: str, notes: list[str]) -> None:
    ensure_hf_auth()
    commit_message = f"release: dataset snapshot {release_tag}"
    description = "\n".join(notes) if notes else "Automated release snapshot upload."
    subprocess.run(
        [
            "hf",
            "upload",
            dataset_repo,
            str(snapshot_dir),
            ".",
            "--repo-type",
            "dataset",
            "--commit-message",
            commit_message,
            "--commit-description",
            description,
        ],
        check=True,
    )


def main() -> None:
    args = parse_args()
    validate_local_contract()
    corpus = load_json(CORPUS)
    records = load_jsonl(RECORDS)
    purification = load_jsonl(PURIFICATION)
    stats = compute_stats(corpus, records, purification)

    snapshot_dir = args.output_root / args.release_tag
    if snapshot_dir.exists() and not args.force:
        raise SystemExit(
            f"Snapshot directory already exists: {snapshot_dir}. Re-run with --force to overwrite."
        )
    snapshot_dir.mkdir(parents=True, exist_ok=True)

# Guard: refuse to build HF release with empty purification.jsonl
    purif_path = Path('data/processed/purification.jsonl')
    if purif_path.exists() and purif_path.stat().st_size < 100:
        print('ERROR: purification.jsonl is empty — code items before releasing to HF')
        raise SystemExit(1)

    shutil.copy2(CORPUS, snapshot_dir / 'corpus-data.json')
    shutil.copy2(RECORDS, snapshot_dir / 'records.jsonl')
    shutil.copy2(PURIFICATION, snapshot_dir / 'purification.jsonl')

    changelog = render_changelog(args.note, stats)
    (snapshot_dir / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    release_manifest = {
        "dataset_repo": args.dataset_repo,
        "release_tag": args.release_tag,
        "stats": stats,
        "notes": args.note,
    }
    (snapshot_dir / "release.json").write_text(
        json.dumps(release_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (snapshot_dir / "README.md").write_text(
        render_readme(args.dataset_repo, args.release_tag, stats, changelog),
        encoding="utf-8",
    )
    write_sha256sums(snapshot_dir)

    print(f"Release snapshot written to: {snapshot_dir}")
    print(
        "Counts: corpus={corpus_items}, records={records_items}, coded={coded_items}".format(
            **stats
        )
    )

    if args.publish:
        publish_snapshot(args.dataset_repo, snapshot_dir, args.release_tag, args.note)
        print(f"Published snapshot to {args.dataset_repo}")


if __name__ == "__main__":
    main()
