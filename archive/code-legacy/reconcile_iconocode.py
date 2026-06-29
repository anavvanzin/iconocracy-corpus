#!/usr/bin/env python3.12
"""
reconcile_iconocode.py — Arbitrates multi-agent iconocode codings for corpus items.

When multiple iconocode agents code the same corpus item in parallel, their scores
may disagree. This script applies arbitration rules to produce a canonical reconciled
record per item, plus a flags file for items requiring human review.

Arbitration rules:
  - Numeric indicators (0–3 scale): if |max − min| ≤ 1 → mean score, confidence=high
                                     if |max − min| > 1  → NULL, confidence=low, flagged
  - Regime (categorical): majority vote if ≥ ⅔ agents agree → confidence=high
                           else → NULL, confidence=low, flagged
  - Panofsky text fields: concatenated verbatim, prefixed by agent_id — never auto-merged

Input schema (one JSON object per line):
    {
        "item_id": "FR-013",
        "agent_id": "iconocode-1",
        "indicators": {
            "desincorporacao": 2,
            "rigidez_postural": 3,
            ...  (10 total — see KNOWN_INDICATORS)
        },
        "regime": "normativo",
        "panofsky": {
            "pre_iconografico": "...",
            "iconografico": "...",
            "iconologico": "..."
        }
    }

NOTE: downstream ledger data/processed/purification.jsonl uses the field name
`regime_iconocratico`. This script currently expects `regime` on input; callers
producing per-agent records for reconciliation must emit `regime` (not
`regime_iconocratico`) or the field rename must be applied before piping in.

Output — reconciled (.reconciled.jsonl):
    {
        "item_id": "FR-013",
        "n_agents": 2,
        "indicators": {
            "desincorporacao": {"mean": 2.5, "min": 2, "max": 3, "n_agents": 2, "confidence": "high"},
            ...
        },
        "regime": {"value": "normativo", "votes": 2, "n_agents": 2, "confidence": "high"},
        "panofsky_raw": [
            {"agent": "iconocode-1", "pre_iconografico": "...", "iconografico": "...", "iconologico": "..."},
            ...
        ]
    }

Output — flags (.flags.jsonl):
    {
        "item_id": "FR-xxx",
        "flags": [
            {"indicator": "desincorporacao", "scores": [1, 4], "reason": "delta=3 > 1"},
            {"field": "regime", "votes": {"normativo": 1, "fundacional": 1}, "reason": "tie"}
        ]
    }

Usage:
    python tools/scripts/reconcile_iconocode.py --input records.jsonl
    python tools/scripts/reconcile_iconocode.py --input records.jsonl --output out.reconciled.jsonl --flags out.flags.jsonl

Exit codes:
    0 — success
    1 — validation errors in input
    2 — I/O error
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Canonical indicator keys per data/processed/purification.jsonl schema
# (ASCII snake_case, no accents). Endurecimento is the UMBRELLA concept
# per CLAUDE.md Mandatory Terminology — the 10 indicators below compose it.
# Reference list only; runtime collects indicator keys dynamically from
# each input record (see reconcile_indicators).
KNOWN_INDICATORS: list[str] = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]

PANOFSKY_FIELDS: list[str] = [
    "pre_iconografico",
    "iconografico",
    "iconologico",
]

SCORE_MIN = 0
SCORE_MAX = 3


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_input(path: Path) -> list[dict[str, Any]]:
    """Load JSONL records from *path*. Returns list of dicts."""
    records: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    records.append(json.loads(raw))
                except json.JSONDecodeError as exc:
                    print(
                        f"ERRO: linha {lineno} em {path}: JSON inválido — {exc}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
    except OSError as exc:
        print(f"ERRO de I/O ao ler {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write list of dicts to *path* as JSONL (one JSON object per line)."""
    try:
        with path.open("w", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"ERRO de I/O ao escrever {path}: {exc}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_record(rec: dict[str, Any], lineno: int) -> list[str]:
    """Return list of validation error messages for *rec*."""
    errors: list[str] = []
    prefix = f"linha {lineno} (item_id={rec.get('item_id', '?')})"

    if "item_id" not in rec:
        errors.append(f"{prefix}: campo 'item_id' ausente")
    if "agent_id" not in rec:
        errors.append(f"{prefix}: campo 'agent_id' ausente")

    indicators = rec.get("indicators")
    if not isinstance(indicators, dict):
        errors.append(f"{prefix}: 'indicators' deve ser um objeto")
    else:
        for key, val in indicators.items():
            if not isinstance(val, (int, float)):
                errors.append(f"{prefix}: indicador '{key}' = {val!r} não é numérico")
            elif not (SCORE_MIN <= val <= SCORE_MAX):
                errors.append(
                    f"{prefix}: indicador '{key}' = {val} fora do intervalo [{SCORE_MIN}, {SCORE_MAX}]"
                )

    if "regime" not in rec:
        errors.append(f"{prefix}: campo 'regime' ausente")

    panofsky = rec.get("panofsky")
    if panofsky is not None and not isinstance(panofsky, dict):
        errors.append(f"{prefix}: 'panofsky' deve ser um objeto ou null")

    return errors


# ---------------------------------------------------------------------------
# Group codings by item
# ---------------------------------------------------------------------------


def group_by_item(
    records: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Return {item_id: [coding, ...]} preserving insertion order."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        grouped[rec["item_id"]].append(rec)
    return dict(grouped)


# ---------------------------------------------------------------------------
# Arbitration logic
# ---------------------------------------------------------------------------


def reconcile_indicators(
    codings: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Arbitrate numeric indicator scores across multiple agent codings.

    Returns:
        (indicator_results, flag_entries)
        indicator_results — dict keyed by indicator name
        flag_entries      — list of flag dicts for divergent indicators
    """
    # Collect all indicator keys seen across all codings
    all_keys: set[str] = set()
    for coding in codings:
        all_keys.update(coding.get("indicators", {}).keys())

    results: dict[str, Any] = {}
    flags: list[dict[str, Any]] = []

    for key in sorted(all_keys):
        scores: list[float] = []
        for coding in codings:
            val = coding.get("indicators", {}).get(key)
            if val is not None:
                scores.append(float(val))

        if not scores:
            # No agent reported this indicator
            results[key] = {
                "mean": None,
                "min": None,
                "max": None,
                "n_agents": 0,
                "confidence": "low",
            }
            continue

        score_min = min(scores)
        score_max = max(scores)
        delta = score_max - score_min
        n = len(scores)

        if delta <= 1:
            mean_val = sum(scores) / n
            # Round to 2 decimal places for readability
            mean_val = round(mean_val, 2)
            results[key] = {
                "mean": mean_val,
                "min": score_min,
                "max": score_max,
                "n_agents": n,
                "confidence": "high",
            }
        else:
            results[key] = {
                "mean": None,
                "min": score_min,
                "max": score_max,
                "n_agents": n,
                "confidence": "low",
            }
            flags.append(
                {
                    "indicator": key,
                    "scores": scores,
                    "reason": f"delta={int(delta) if delta == int(delta) else delta} > 1",
                }
            )

    return results, flags


def reconcile_regime(
    codings: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Arbitrate regime (categorical) via majority vote (>= 2/3 threshold).

    Returns:
        (regime_result, flag_entries)
    """
    votes: list[str] = [
        c["regime"] for c in codings if isinstance(c.get("regime"), str)
    ]
    n = len(votes)
    flags: list[dict[str, Any]] = []

    if n == 0:
        return {"value": None, "votes": 0, "n_agents": 0, "confidence": "low"}, flags

    counts = Counter(votes)
    winner, winner_votes = counts.most_common(1)[0]

    # 2/3 threshold — ceiling division to avoid float issues
    threshold = math.ceil(n * 2 / 3)

    if winner_votes >= threshold:
        result = {
            "value": winner,
            "votes": winner_votes,
            "n_agents": n,
            "confidence": "high",
        }
    else:
        result = {
            "value": None,
            "votes": winner_votes,
            "n_agents": n,
            "confidence": "low",
        }
        flags.append(
            {
                "field": "regime",
                "votes": dict(counts),
                "reason": f"tie — nenhum regime atingiu 2/3 ({threshold}/{n} votos necessarios)",
            }
        )

    return result, flags


def collect_panofsky_raw(codings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Concatenate Panofsky text fields from all agents — never auto-merged."""
    raw: list[dict[str, Any]] = []
    for coding in codings:
        agent_id = coding.get("agent_id", "unknown")
        panofsky = coding.get("panofsky") or {}
        entry: dict[str, Any] = {"agent": agent_id}
        for field in PANOFSKY_FIELDS:
            entry[field] = panofsky.get(field, "")
        raw.append(entry)
    return raw


def reconcile_item(
    item_id: str, codings: list[dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Produce reconciled record and optional flags entry for one item.

    Returns:
        (reconciled_record, flags_record_or_None)
    """
    indicator_results, indicator_flags = reconcile_indicators(codings)
    regime_result, regime_flags = reconcile_regime(codings)
    panofsky_raw = collect_panofsky_raw(codings)

    reconciled: dict[str, Any] = {
        "item_id": item_id,
        "n_agents": len(codings),
        "indicators": indicator_results,
        "regime": regime_result,
        "panofsky_raw": panofsky_raw,
    }

    all_flags = indicator_flags + regime_flags
    flags_record: dict[str, Any] | None = None
    if all_flags:
        flags_record = {"item_id": item_id, "flags": all_flags}

    return reconciled, flags_record


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reconcile_iconocode.py",
        description=(
            "Arbitrates multi-agent iconocode codings.\n\n"
            "For each corpus item coded by multiple agents, applies:\n"
            "  - Numeric indicators: mean if |max-min| <= 1 (confidence=high), else NULL (confidence=low)\n"
            "  - Regime: majority vote >= 2/3 agents; else flagged\n"
            "  - Panofsky: all outputs concatenated verbatim, prefixed by agent ID\n\n"
            "Writes .reconciled.jsonl and .flags.jsonl alongside the input file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        required=True,
        metavar="JSONL",
        help="Path to input JSONL file containing one iconocode coding per line.",
    )
    parser.add_argument(
        "--output",
        metavar="JSONL",
        help=(
            "Path for reconciled output. Defaults to <input>.reconciled.jsonl "
            "in the same directory as the input file."
        ),
    )
    parser.add_argument(
        "--flags",
        metavar="JSONL",
        help=(
            "Path for flags output. Defaults to <input>.flags.jsonl "
            "in the same directory as the input file."
        ),
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip input record validation (faster, use when input is trusted).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-item summary to stderr.",
    )
    return parser


def resolve_output_paths(
    input_path: Path,
    output_arg: str | None,
    flags_arg: str | None,
) -> tuple[Path, Path]:
    """Resolve output and flags paths from CLI args or defaults."""
    stem = input_path.name
    # Strip known extensions to build clean suffix
    for ext in (".jsonl", ".json"):
        if stem.endswith(ext):
            stem = stem[: -len(ext)]
            break

    out_path = Path(output_arg) if output_arg else input_path.parent / f"{stem}.reconciled.jsonl"
    flags_path = Path(flags_arg) if flags_arg else input_path.parent / f"{stem}.flags.jsonl"
    return out_path, flags_path


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERRO: arquivo de entrada nao encontrado: {input_path}", file=sys.stderr)
        sys.exit(2)

    out_path, flags_path = resolve_output_paths(input_path, args.output, args.flags)

    # Load records
    records = load_input(input_path)
    if not records:
        print("AVISO: arquivo de entrada vazio — nada a reconciliar.", file=sys.stderr)
        sys.exit(0)

    # Validate
    if not args.skip_validation:
        all_errors: list[str] = []
        for i, rec in enumerate(records, 1):
            all_errors.extend(validate_record(rec, i))
        if all_errors:
            print(
                f"ERRO: {len(all_errors)} problema(s) de validacao no input:",
                file=sys.stderr,
            )
            for err in all_errors:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)

    # Group by item
    grouped = group_by_item(records)
    n_items = len(grouped)
    n_solo = sum(1 for codings in grouped.values() if len(codings) == 1)

    if args.verbose:
        print(
            f"INFO: {len(records)} codificacoes para {n_items} itens "
            f"({n_solo} com agente unico).",
            file=sys.stderr,
        )

    # Reconcile
    reconciled_records: list[dict[str, Any]] = []
    flag_records: list[dict[str, Any]] = []

    # Sort by item_id for deterministic output across re-runs (git-diff stability).
    for item_id, codings in sorted(grouped.items()):
        reconciled, flags_rec = reconcile_item(item_id, codings)
        reconciled_records.append(reconciled)
        if flags_rec:
            flag_records.append(flags_rec)
        if args.verbose:
            n_flags = len(flags_rec["flags"]) if flags_rec else 0
            status = f"{n_flags} flag(s)" if n_flags else "OK"
            print(
                f"  {item_id}: {len(codings)} agente(s) -> {status}",
                file=sys.stderr,
            )

    # Write outputs
    write_jsonl(out_path, reconciled_records)
    write_jsonl(flags_path, flag_records)

    print(
        f"Reconciliacao completa: {n_items} itens -> {out_path.name} "
        f"({len(flag_records)} flags -> {flags_path.name})"
    )


if __name__ == "__main__":
    main()
