#!/usr/bin/env python3
"""Normalize schema-sensitive fields in records JSONL files."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

DATE_ONLY_LENGTH = 10


def _is_date_only(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != DATE_ONLY_LENGTH:
        return False
    year, first_dash, month, second_dash, day = value[:4], value[4], value[5:7], value[7], value[8:10]
    return first_dash == "-" and second_dash == "-" and year.isdigit() and month.isdigit() and day.isdigit()


def _percent_encode_url(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        return value

    encoded_path = quote(parsed.path, safe="/%:@!$&'()*+,;=")
    encoded_query = quote(parsed.query, safe="/%=&?+:@!$'()*+,;[]")
    encoded_fragment = quote(parsed.fragment, safe="/%=&?+:@!$'()*+,;[]")
    return urlunsplit((parsed.scheme, parsed.netloc, encoded_path, encoded_query, encoded_fragment))


def normalize_record(record: dict[str, Any]) -> list[str]:
    """Normalize one record in place and return changed field paths."""
    changed: list[str] = []

    timestamps = record.get("timestamps")
    if isinstance(timestamps, dict):
        created_at = timestamps.get("created_at")
        if _is_date_only(created_at):
            timestamps["created_at"] = f"{created_at}T00:00:00Z"
            changed.append("timestamps.created_at")

    input_data = record.get("input")
    if isinstance(input_data, dict) and "input_url" in input_data:
        original = input_data.get("input_url")
        normalized = _percent_encode_url(original)
        if normalized != original:
            input_data["input_url"] = normalized
            changed.append("input.input_url")

    webscout = record.get("webscout")
    if isinstance(webscout, dict):
        search_results = webscout.get("search_results")
        if isinstance(search_results, list):
            for index, result in enumerate(search_results):
                if not isinstance(result, dict) or "url" not in result:
                    continue
                original = result.get("url")
                normalized = _percent_encode_url(original)
                if normalized != original:
                    result["url"] = normalized
                    changed.append(f"webscout.search_results.{index}.url")

    return changed


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            data = json.loads(stripped)
            if not isinstance(data, dict):
                raise ValueError(f"Line {line_number}: expected JSON object")
            records.append(data)
    return records


def write_jsonl_atomic(path: Path, records: list[dict[str, Any]]) -> None:
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
        ) as handle:
            tmp_path = Path(handle.name)
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
        tmp_path = None
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    write_jsonl_atomic(path, records)


def normalize_file(path: Path, write: bool = False) -> tuple[int, Counter[str]]:
    records = load_jsonl(path)
    counts: Counter[str] = Counter()

    for record in records:
        counts.update(normalize_record(record))

    total_changes = sum(counts.values())
    print(f"records:{len(records)}")
    if counts:
        for field, count in counts.items():
            print(f"{field}:{count}")
    else:
        print("changes:0")

    if total_changes and write:
        write_jsonl_atomic(path, records)
        print(f"wrote:{path}")
    elif total_changes:
        print("dry-run: changes needed (rerun with --write)")

    return total_changes, counts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSONL records file to normalize")
    parser.add_argument("--write", action="store_true", help="rewrite the JSONL file with normalized records")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    total_changes, _counts = normalize_file(args.path, write=args.write)
    if total_changes and not args.write:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
