#!/usr/bin/env python3
"""
compute_irr.py — Inter-Rater Reliability for endurecimento purification coding.

Computes Krippendorff's Alpha (ordinal metric) across multiple coders for the
10 purification indicators. Supports adjudication of disagreements.

Usage:
    python tools/scripts/compute_irr.py                  # full IRR report
    python tools/scripts/compute_irr.py --export-json    # machine-readable output
    python tools/scripts/compute_irr.py --adjudicate     # interactive adjudication
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    import krippendorff
except ImportError:
    print(
        "Error: krippendorff library required. Install with: pip install krippendorff",
        file=sys.stderr,
    )
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PURIFICATION_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"
IRR_REPORT_JSON = REPO_ROOT / "data" / "processed" / "irr_report.json"

INDICATORS = [
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


def load_all_codings():
    """Load raw codings grouped by item ID.

    Adjudicated consensus records stay in the ledger for downstream exports,
    but they must not count as independent coder passes in IRR calculations.
    """
    by_item = defaultdict(list)
    if PURIFICATION_JSONL.exists():
        with open(PURIFICATION_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    if rec.get("adjudication_status") == "adjudicated":
                        continue
                    by_item[rec["id"]].append(rec)
    return dict(by_item)


def get_double_coded(all_codings):
    """Return items with 2+ codings from different coders."""
    double = {}
    for item_id, codings in all_codings.items():
        coders = {c["coded_by"] for c in codings}
        if len(coders) >= 2:
            double[item_id] = codings
    return double


def compute_alpha(double_coded, indicator):
    """Compute Krippendorff's Alpha for one indicator across double-coded items.

    Returns alpha value or None if insufficient data.
    """
    if len(double_coded) < 2:
        return None

    # Collect all unique coders
    all_coders = set()
    for codings in double_coded.values():
        for c in codings:
            all_coders.add(c["coded_by"])
    coder_list = sorted(all_coders)

    # Build reliability matrix: rows = coders, cols = items
    items = sorted(double_coded.keys())
    matrix = np.full((len(coder_list), len(items)), np.nan)

    for j, item_id in enumerate(items):
        for coding in double_coded[item_id]:
            i = coder_list.index(coding["coded_by"])
            matrix[i, j] = coding.get(indicator, np.nan)

    # Need at least 2 non-NaN values per column for some items
    valid_cols = np.sum(~np.isnan(matrix), axis=0) >= 2
    if valid_cols.sum() < 2:
        return None

    try:
        alpha = krippendorff.alpha(
            reliability_data=matrix[:, valid_cols], level_of_measurement="ordinal"
        )
        return round(alpha, 4)
    except Exception:
        return None


def find_disagreements(double_coded, threshold=2):
    """Find items where coders disagree by >= threshold levels on any indicator."""
    disagreements = []
    for item_id, codings in double_coded.items():
        for indicator in INDICATORS:
            values = [c.get(indicator) for c in codings if c.get(indicator) is not None]
            if len(values) >= 2 and (max(values) - min(values)) >= threshold:
                disagreements.append(
                    {
                        "item_id": item_id,
                        "indicator": indicator,
                        "values": {c["coded_by"]: c.get(indicator) for c in codings},
                        "spread": max(values) - min(values),
                    }
                )
    return sorted(disagreements, key=lambda d: d["spread"], reverse=True)


def report(all_codings):
    """Generate full IRR report."""
    double_coded = get_double_coded(all_codings)

    print(f"\n{'=' * 60}")
    print(f"  Inter-Rater Reliability Report (Krippendorff's Alpha)")
    print(f"{'=' * 60}")
    print(
        f"  Total items in ledger:    {sum(len(v) for v in all_codings.values())} codings across {len(all_codings)} items"
    )
    print(f"  Double-coded items:       {len(double_coded)}")

    if not double_coded:
        print("\n  ⚠ No double-coded items found. Run double-coding first:")
        print("    python tools/scripts/code_purification.py --item XX-NNN --coder ana")
        print()
        return None

    # Collect coders
    coders = set()
    for codings in double_coded.values():
        for c in codings:
            coders.add(c["coded_by"])
    print(f"  Coders:                   {', '.join(sorted(coders))}")
    print()

    # Compute alpha per indicator
    results = {}
    print(f"  {'Indicator':<30s} {'Alpha':>8s}  {'Interpretation'}")
    print(f"  {'─' * 60}")
    for indicator in INDICATORS:
        alpha = compute_alpha(double_coded, indicator)
        if alpha is None:
            interp = "insufficient data"
            symbol = "  "
        elif alpha >= 0.800:
            interp = "good reliability"
            symbol = "✅"
        elif alpha >= 0.667:
            interp = "tentative"
            symbol = "🟡"
        else:
            interp = "low reliability"
            symbol = "❌"
        results[indicator] = alpha
        alpha_str = f"{alpha:.3f}" if alpha is not None else "  N/A"
        print(f"  {indicator:<30s} {alpha_str:>8s}  {symbol} {interp}")

    # Overall alpha (all indicators pooled)
    overall = compute_alpha_overall(double_coded)
    results["_overall"] = overall
    if overall is not None:
        print(f"\n  {'OVERALL (pooled)':<30s} {overall:>8.3f}")

    # Composite agreement
    composite_diffs = []
    for item_id, codings in double_coded.items():
        composites = [
            c.get("purificacao_composto")
            for c in codings
            if c.get("purificacao_composto") is not None
        ]
        if len(composites) >= 2:
            composite_diffs.append(max(composites) - min(composites))
    if composite_diffs:
        print(f"\n  Composite score (purificacao_composto):")
        print(f"    Mean absolute difference: {np.mean(composite_diffs):.3f}")
        print(f"    Max  absolute difference: {max(composite_diffs):.3f}")

    # Disagreements
    disagreements = find_disagreements(double_coded)
    if disagreements:
        print(f"\n  ⚠ Disagreements (>= 2 levels apart): {len(disagreements)}")
        for d in disagreements[:10]:
            vals = ", ".join(f"{k}: {v}" for k, v in d["values"].items())
            print(
                f"    {d['item_id']:15s} {d['indicator']:<30s} [{vals}] (Δ={d['spread']})"
            )

    print()
    return results


def compute_alpha_overall(double_coded):
    """Compute pooled Krippendorff's Alpha across all 10 indicators."""
    all_coders = set()
    for codings in double_coded.values():
        for c in codings:
            all_coders.add(c["coded_by"])
    coder_list = sorted(all_coders)

    items = sorted(double_coded.keys())
    n_units = len(items) * len(INDICATORS)
    matrix = np.full((len(coder_list), n_units), np.nan)

    for j, item_id in enumerate(items):
        for ind_idx, indicator in enumerate(INDICATORS):
            col = j * len(INDICATORS) + ind_idx
            for coding in double_coded[item_id]:
                i = coder_list.index(coding["coded_by"])
                matrix[i, col] = coding.get(indicator, np.nan)

    valid_cols = np.sum(~np.isnan(matrix), axis=0) >= 2
    if valid_cols.sum() < 2:
        return None

    try:
        alpha = krippendorff.alpha(
            reliability_data=matrix[:, valid_cols], level_of_measurement="ordinal"
        )
        return round(alpha, 4)
    except Exception:
        return None


def adjudicate(all_codings):
    """Interactive adjudication of disagreements."""
    double_coded = get_double_coded(all_codings)
    if not double_coded:
        print("  ⚠ No double-coded items to adjudicate.")
        return

    disagreements = find_disagreements(double_coded, threshold=1)
    items_to_adjudicate = sorted(set(d["item_id"] for d in disagreements))

    print(f"\n  Adjudication mode: {len(items_to_adjudicate)} items with disagreements")
    print(
        f"  For each indicator, enter the consensus value (0-3) or Enter to keep first coder's value.\n"
    )

    adjudicated = 0
    for item_id in items_to_adjudicate:
        codings = double_coded[item_id]
        print(f"\n  {'=' * 50}")
        print(f"  Item: {item_id}")

        # Show all codings side by side
        coder_names = [c["coded_by"] for c in codings]
        header = f"  {'Indicator':<30s}" + "".join(
            f" {name:>15s}" for name in coder_names
        )
        print(header)
        print(f"  {'─' * (30 + 16 * len(coder_names))}")

        consensus_scores = {}
        for indicator in INDICATORS:
            values = [c.get(indicator, "?") for c in codings]
            vals_str = "".join(f" {str(v):>15s}" for v in values)
            differs = len(set(v for v in values if v != "?")) > 1
            marker = " ⚡" if differs else ""
            print(f"  {indicator:<30s}{vals_str}{marker}")

            if differs:
                while True:
                    default = values[0] if values[0] != "?" else values[1]
                    inp = input(
                        f"    → Consensus for {indicator} [{default}]: "
                    ).strip()
                    if inp == "":
                        consensus_scores[indicator] = default
                        break
                    if inp == "q":
                        print(f"\n  Adjudicated {adjudicated} items this session.")
                        return
                    if inp in ("0", "1", "2", "3"):
                        consensus_scores[indicator] = int(inp)
                        break
                    print("      Enter 0-3 or Enter for default")
            else:
                consensus_scores[indicator] = values[0]

        composite = round(sum(consensus_scores.values()) / len(consensus_scores), 2)

        # Regime — take majority or ask
        regimes = [c.get("regime_iconocratico") for c in codings]
        if len(set(regimes)) == 1:
            regime = regimes[0]
        else:
            print(f"\n  Regimes differ: {regimes}")
            regime = (
                input(f"    → Consensus regime [{regimes[0]}]: ").strip() or regimes[0]
            )

        record = {
            "id": item_id,
            **consensus_scores,
            "purificacao_composto": composite,
            "regime_iconocratico": regime,
            "coded_by": "consensus-ana",
            "coded_at": datetime.now(timezone.utc).isoformat(),
            "adjudication_status": "adjudicated",
            "coding_round": max(c.get("coding_round", 1) for c in codings) + 1,
        }

        # Append to ledger
        with open(PURIFICATION_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"  ✅ {item_id} adjudicated: composite={composite:.2f}, regime={regime}")
        adjudicated += 1

    print(f"\n  Session complete: {adjudicated} items adjudicated")


def export_json(results, all_codings):
    """Export IRR results as JSON for notebook consumption."""
    double_coded = get_double_coded(all_codings)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_items": len(all_codings),
        "double_coded_items": len(double_coded),
        "alphas": results if results else {},
        "disagreements": find_disagreements(double_coded) if double_coded else [],
        "thresholds": {
            "good": 0.800,
            "tentative": 0.667,
            "method": "Krippendorff's Alpha (ordinal metric)",
        },
    }

    with open(IRR_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  ✅ IRR report saved to {IRR_REPORT_JSON}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute inter-rater reliability (Krippendorff's Alpha) for endurecimento coding"
    )
    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Export results as JSON for notebook consumption",
    )
    parser.add_argument(
        "--adjudicate",
        action="store_true",
        help="Interactive adjudication of disagreements",
    )
    args = parser.parse_args()

    all_codings = load_all_codings()

    if args.adjudicate:
        adjudicate(all_codings)
        return

    results = report(all_codings)

    if args.export_json and results:
        export_json(results, all_codings)


if __name__ == "__main__":
    main()
