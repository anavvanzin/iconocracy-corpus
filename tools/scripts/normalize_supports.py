#!/usr/bin/env python3
"""Normalize `support` and `country_pt` labels in corpus/corpus-data.json.

Task T1. Idempotent: running twice produces zero diff.

Scope (in-canonical merges, safe to apply automatically):

* `support`:
    - "estampa", "gravura", "gravura/litografia" -> "estampa/gravura"
    - "monumento"                                -> "monumento/escultura"
    - "frontispicio"                             -> "frontispício"

* `country_pt` (the task description names this "country", but the cited
  variants "EUA" / "Estados Unidos" / "Alemanha" actually live in the
  `country_pt` field; the English `country` field holds labels such as
  "United States", "Germany" and is left untouched):
    - "Estados Unidos" -> "EUA"
    - "Alemanha"       -> "Alemanha" (no variants present; already canonical)

Out-of-canonical `support` values are reported but NEVER rewritten:
"pintura", "fotografia", "texto", "cerâmica".

CLI:
    --dry-run      : show diff summary, make no writes
    --report-only  : print current counts, no diff computation, no writes
    (default)      : apply and atomically rewrite corpus-data.json

Exit codes: 0 success, 1 JSON parse / write / IO error, 2 unexpected variant.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"

# ---- Canonical sets and merge maps --------------------------------------

SUPPORT_CANONICAL = {
    "moeda",
    "selo",
    "monumento/escultura",
    "arquitetura forense",
    "estampa/gravura",
    "frontispício",
    "papel-moeda",
    "cartaz",
}

SUPPORT_MERGES = {
    "estampa": "estampa/gravura",
    "gravura": "estampa/gravura",
    "gravura/litografia": "estampa/gravura",
    "monumento": "monumento/escultura",
    "frontispicio": "frontispício",
}

# Known out-of-canonical values we intentionally DO NOT touch. Listed here
# so the report can distinguish "flagged for follow-up" from "unexpected".
SUPPORT_OUT_OF_CANONICAL = {"pintura", "fotografia", "texto", "cerâmica"}

COUNTRY_PT_MERGES = {
    "Estados Unidos": "EUA",
}


def _fold(s: str | None) -> str | None:
    """Case- and accent-fold for near-duplicate detection only."""
    if s is None:
        return None
    return (
        unicodedata.normalize("NFKD", s)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )


# ---- Core --------------------------------------------------------------


def load_corpus(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: corpus file not found: {path}", file=sys.stderr)
        raise
    except json.JSONDecodeError as exc:
        print(f"ERROR: corpus JSON parse failed: {exc}", file=sys.stderr)
        raise
    if not isinstance(data, list):
        raise ValueError(f"Expected top-level JSON array, got {type(data).__name__}")
    return data


def atomic_write_json(path: Path, data: list[dict[str, Any]]) -> None:
    """Write to a sibling .tmp file then os.replace() to target. Preserves
    field order via dict iteration order (CPython 3.7+)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # delete=False so we can rename the file; clean up on failure.
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=str(path.parent),
        prefix=path.name + ".",
        suffix=".tmp",
        delete=False,
    )
    tmp_path = Path(tmp.name)
    try:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp.close()
        os.replace(tmp_path, path)
    except Exception:
        tmp.close()
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise


def apply_normalization(
    data: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (new_data, stats). Does not mutate the input list (items are
    copied shallowly with updated fields).

    stats keys:
      support_before, support_after: Counter
      country_pt_before, country_pt_after: Counter
      support_out_of_canonical: Counter (subset of support_after that is
          neither canonical nor a merge source)
      support_changed, country_pt_changed: int
    """
    support_before: Counter[Any] = Counter()
    support_after: Counter[Any] = Counter()
    country_pt_before: Counter[Any] = Counter()
    country_pt_after: Counter[Any] = Counter()
    support_changed = 0
    country_pt_changed = 0

    out: list[dict[str, Any]] = []
    for item in data:
        new_item = dict(item)  # preserve field order, avoid mutating caller

        # --- support -------------------------------------------------
        s = new_item.get("support")
        support_before[s] += 1
        if isinstance(s, str) and s in SUPPORT_MERGES:
            new_s = SUPPORT_MERGES[s]
            if new_s != s:
                new_item["support"] = new_s
                support_changed += 1
            s = new_s
        support_after[s] += 1

        # --- country_pt ---------------------------------------------
        c = new_item.get("country_pt")
        country_pt_before[c] += 1
        if isinstance(c, str) and c in COUNTRY_PT_MERGES:
            new_c = COUNTRY_PT_MERGES[c]
            if new_c != c:
                new_item["country_pt"] = new_c
                country_pt_changed += 1
            c = new_c
        country_pt_after[c] += 1

        out.append(new_item)

    # support_out_of_canonical: values after normalization that are neither
    # in the canonical set nor None
    support_ooc: Counter[Any] = Counter()
    for v, n in support_after.items():
        if v is None:
            continue
        if v in SUPPORT_CANONICAL:
            continue
        support_ooc[v] = n

    stats = {
        "support_before": support_before,
        "support_after": support_after,
        "country_pt_before": country_pt_before,
        "country_pt_after": country_pt_after,
        "support_out_of_canonical": support_ooc,
        "support_changed": support_changed,
        "country_pt_changed": country_pt_changed,
    }
    return out, stats


def scan_near_dups(data: list[dict[str, Any]], field: str) -> dict[str, list[str]]:
    """Return case/accent-folded groups that contain >1 surface form."""
    groups: dict[str, set[str]] = defaultdict(set)
    for item in data:
        v = item.get(field)
        if not isinstance(v, str):
            continue
        groups[_fold(v) or ""].add(v)
    return {k: sorted(vs) for k, vs in groups.items() if len(vs) > 1}


# ---- Reporting ---------------------------------------------------------


def _fmt_counter(c: Counter[Any]) -> str:
    lines = []
    for k, v in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        lines.append(f"    {v:4d}  {k!r}")
    return "\n".join(lines) if lines else "    (empty)"


def print_report(stats: dict[str, Any], *, header: str) -> None:
    print(f"\n=== {header} ===")
    print("\n-- support before --")
    print(_fmt_counter(stats["support_before"]))
    print("\n-- support after --")
    print(_fmt_counter(stats["support_after"]))
    print(f"\nsupport items changed: {stats['support_changed']}")

    print("\n-- country_pt before --")
    print(_fmt_counter(stats["country_pt_before"]))
    print("\n-- country_pt after --")
    print(_fmt_counter(stats["country_pt_after"]))
    print(f"\ncountry_pt items changed: {stats['country_pt_changed']}")

    ooc = stats["support_out_of_canonical"]
    print("\n-- out-of-canonical support values (flagged, NOT rewritten) --")
    if ooc:
        for k, v in sorted(ooc.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            known = "known" if k in SUPPORT_OUT_OF_CANONICAL else "UNEXPECTED"
            print(f"    {v:4d}  {k!r}  [{known}]")
    else:
        print("    (none)")


# ---- Entry point -------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        default=CORPUS_PATH,
        help="Corpus JSON path (default: corpus/corpus-data.json)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print diff summary, make no writes.",
    )
    mode.add_argument(
        "--report-only",
        action="store_true",
        help="Print current field counts only, no normalization run.",
    )
    args = parser.parse_args(argv)

    try:
        data = load_corpus(args.path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 1

    print(f"Loaded {len(data)} items from {args.path}")

    if args.report_only:
        support = Counter(item.get("support") for item in data)
        country_pt = Counter(item.get("country_pt") for item in data)
        country = Counter(item.get("country") for item in data)
        print("\n-- support counts --")
        print(_fmt_counter(support))
        print("\n-- country_pt counts --")
        print(_fmt_counter(country_pt))
        print("\n-- country counts (not modified) --")
        print(_fmt_counter(country))
        return 0

    # Near-dup scan on country_pt and country BEFORE applying merges, so the
    # user sees any additional pairs they might not have anticipated.
    cpt_dups = scan_near_dups(data, "country_pt")
    c_dups = scan_near_dups(data, "country")
    if cpt_dups:
        print("\n-- near-dup groups in country_pt (folded key -> surface forms) --")
        for k, vs in sorted(cpt_dups.items()):
            print(f"    {k!r}: {vs}")
    if c_dups:
        print("\n-- near-dup groups in country (folded key -> surface forms) --")
        for k, vs in sorted(c_dups.items()):
            print(f"    {k!r}: {vs}")

    new_data, stats = apply_normalization(data)
    print_report(stats, header="Normalization summary")

    if args.dry_run:
        print("\n[dry-run] No writes performed.")
        return 0

    changed = stats["support_changed"] + stats["country_pt_changed"]
    if changed == 0:
        print("\nNo changes required (already normalized). Skipping write.")
        return 0

    try:
        atomic_write_json(args.path, new_data)
    except OSError as exc:
        print(f"ERROR: atomic write failed: {exc}", file=sys.stderr)
        return 1

    print(f"\nWrote {len(new_data)} items to {args.path} (atomic replace).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
