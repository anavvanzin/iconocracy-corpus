#!/usr/bin/env python3
"""
compute_irr.py — Inter-Rater Reliability for endurecimento purification coding.

Computes Krippendorff's Alpha (ordinal metric) across multiple coders for the
10 purification indicators. Supports adjudication of disagreements and rater-2
blind coding comparison.

Usage:
    python tools/scripts/compute_irr.py                              # full IRR report
    python tools/scripts/compute_irr.py --export-json                # machine-readable output
    python tools/scripts/compute_irr.py --adjudicate                 # interactive adjudication
    python tools/scripts/compute_irr.py --rater2 data/processed/irr_re_run/rater2_results.jsonl
        # compare rater-2 blind coding with existing purifications
    python tools/scripts/compute_irr.py --rater2 ... --output-raw    # save raw pairs
    python tools/scripts/compute_irr.py --rater2 ... --indicator-report
        # bootstrap CI per indicator
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def load_all_codings() -> dict[str, list[dict]]:
    """Load raw codings grouped by item ID (excludes adjudicated records)."""
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


def load_rater2_results(rater2_path: Path) -> dict[str, dict]:
    """Load rater-2 blind coding results from JSONL."""
    by_item = {}
    if not rater2_path.exists():
        return by_item
    with open(rater2_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                item_id = rec.get("item_id")
                if item_id:
                    by_item[item_id] = rec
    return by_item


def get_rater1_purification(item_id: str, all_codings: dict[str, list[dict]]) -> dict | None:
    """Get the rater-1 purification coding for an item (most recent non-migration)."""
    codings = all_codings.get(item_id, [])
    if not codings:
        return None
    # Prefer iconocode-opus or hermes-auto over migration
    priority_order = {"iconocode-opus": 3, "iconocode-opus-4.6-image": 3, "iconocode-opus-4.6-metadata-refined": 3,
                      "hermes-auto": 2, "e1-gemma4/gemma4": 2, "e1-gemma4/gemma4-fcrecode": 2,
                      "fable-5": 1, "migration": 0, "manual-entry": 4, "batch-tentative-2026-04-25": 1}
    best = None
    best_priority = -1
    for c in codings:
        coder = c.get("coded_by", "")
        priority = 0
        for key, val in priority_order.items():
            if key in coder:
                priority = val
                break
        if priority > best_priority:
            best_priority = priority
            best = c
    return best


def build_rater_pairs(rater1_codings: dict[str, list[dict]], rater2_results: dict[str, dict]) -> dict[str, list[dict]]:
    """
    Build paired codings for items that have both rater-1 and rater-2.
    Returns dict: item_id -> list of 2 coding dicts with standardized structure.
    """
    # Load id mapping: UUID item_id -> corpus_id (sigla)
    id_mapping_path = REPO_ROOT / "data" / "processed" / "id-mapping.json"
    item_to_corpus = {}
    if id_mapping_path.exists():
        mapping_data = json.load(id_mapping_path.open(encoding="utf-8"))
        for m in mapping_data.get("mapping", []):
            item_to_corpus[m["item_id"]] = m["corpus_id"]

    paired = {}
    for item_id, rater2_rec in rater2_results.items():
        # Map UUID item_id to corpus_id for rater-1 lookup
        corpus_id = item_to_corpus.get(item_id, item_id)
        rater1_rec = get_rater1_purification(corpus_id, rater1_codings)
        if not rater1_rec:
            continue

        # Standardize rater-1 format
        r1 = {"coded_by": rater1_rec.get("coded_by", "rater1")}
        for ind in INDICATORS:
            r1[ind] = rater1_rec.get(ind)
        r1["purificacao_composto"] = rater1_rec.get("purificacao_composto")
        r1["regime_iconocratico"] = rater1_rec.get("regime_iconocratico")

        # Standardize rater-2 format
        r2 = {"coded_by": rater2_rec.get("coded_by", "rater2")}
        indicadores = rater2_rec.get("indicadores", {})
        for ind in INDICATORS:
            ind_data = indicadores.get(ind, {})
            r2[ind] = ind_data.get("score") if isinstance(ind_data, dict) else ind_data
        r2["purificacao_composto"] = rater2_rec.get("purificacao_composto")
        r2["regime_iconocratico"] = rater2_rec.get("regime_iconocratico")
        r2["image_condition"] = rater2_rec.get("image_condition")

        paired[item_id] = [r1, r2]

    return paired


def compute_alpha(paired_codings: dict[str, list[dict]], indicator: str) -> float | None:
    """Compute Krippendorff's Alpha for one indicator across paired codings."""
    if len(paired_codings) < 2:
        return None

    all_coders = set()
    for codings in paired_codings.values():
        for c in codings:
            all_coders.add(c["coded_by"])
    coder_list = sorted(all_coders)

    items = sorted(paired_codings.keys())
    matrix = np.full((len(coder_list), len(items)), np.nan)

    for j, item_id in enumerate(items):
        for coding in paired_codings[item_id]:
            i = coder_list.index(coding["coded_by"])
            matrix[i, j] = coding.get(indicator, np.nan)

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


def bootstrap_ci(paired_codings: dict[str, list[dict]], indicator: str, n_bootstrap: int = 1000, ci: float = 0.95) -> tuple[float, float] | None:
    """Compute bootstrap confidence interval for Krippendorff's alpha."""
    if len(paired_codings) < 3:
        return None

    items = list(paired_codings.keys())
    n_items = len(items)
    alphas = []

    rng = np.random.default_rng(42)
    for _ in range(n_bootstrap):
        # Sample with replacement
        sample_idx = rng.choice(n_items, size=n_items, replace=True)
        sample_items = [items[i] for i in sample_idx]
        sample_codings = {item_id: paired_codings[item_id] for item_id in sample_items}

        alpha = compute_alpha(sample_codings, indicator)
        if alpha is not None:
            alphas.append(alpha)

    if not alphas:
        return None

    lower = np.percentile(alphas, (1 - ci) / 2 * 100)
    upper = np.percentile(alphas, (1 + ci) / 2 * 100)
    return (round(lower, 4), round(upper, 4))


def find_disagreements(paired_codings: dict[str, list[dict]], threshold: int = 2) -> list[dict]:
    """Find items where coders disagree by >= threshold levels on any indicator."""
    disagreements = []
    for item_id, codings in paired_codings.items():
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


def regime_agreement(paired_codings: dict[str, list[dict]]) -> float | None:
    """Compute Cohen's kappa for regime agreement (simplified exact match for 2 raters)."""
    if len(paired_codings) < 2:
        return None

    matches = 0
    total = 0
    for item_id, codings in paired_codings.items():
        if len(codings) == 2:
            r1_reg = codings[0].get("regime_iconocratico")
            r2_reg = codings[1].get("regime_iconocratico")
            if r1_reg is not None and r2_reg is not None:
                total += 1
                if r1_reg == r2_reg:
                    matches += 1

    if total == 0:
        return None
    return round(matches / total, 4)


def report_paired(paired_codings: dict[str, list[dict]], bootstrap_ci_flag: bool = False) -> dict[str, Any]:
    """Generate IRR report for paired codings (rater-1 vs rater-2)."""
    print(f"\n{'=' * 60}")
    print("  Inter-Rater Reliability Report (Rater-1 vs Rater-2)")
    print(f"{'=' * 60}")
    print(f"  Paired items:       {len(paired_codings)}")

    if not paired_codings:
        print("\n  ⚠ No paired items found.")
        return {}

    coders = sorted(set(c["coded_by"] for c in next(iter(paired_codings.values()))))
    print(f"  Coders:             {', '.join(coders)}")
    print()

    results = {}
    # Compute alpha per indicator
    print(f"  {'Indicator':<30s} {'Alpha':>8s}  {'95% CI':<15s}  {'Interpretation'}")
    print(f"  {'─' * 75}")
    for indicator in INDICATORS:
        alpha = compute_alpha(paired_codings, indicator)
        ci_str = ""
        if bootstrap_ci_flag and alpha is not None:
            ci_result = bootstrap_ci(paired_codings, indicator)
            if ci_result:
                ci_str = f"[{ci_result[0]:.3f}, {ci_result[1]:.3f}]"

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

        results[indicator] = {"alpha": alpha, "ci": ci_result if bootstrap_ci_flag else None}
        alpha_str = f"{alpha:.3f}" if alpha is not None else "  N/A"
        print(f"  {indicator:<30s} {alpha_str:>8s}  {ci_str:<15s}  {symbol} {interp}")

    # Overall alpha (all indicators pooled)
    overall = compute_alpha_overall(paired_codings)
    results["_overall"] = overall
    if overall is not None:
        print(f"\n  {'OVERALL (pooled)':<30s} {overall:>8.3f}")

    # Regime agreement
    regime_kappa = regime_agreement(paired_codings)
    if regime_kappa is not None:
        print(f"\n  {'Regime agreement (exact)':<30s} {regime_kappa:>8.3f}")

    # Exact match rate per indicator
    print(f"\n  {'Indicator':<30s} {'Exact%':>8s}  {'Within-1%':>10s}")
    print(f"  {'─' * 55}")
    for indicator in INDICATORS:
        exact = 0
        within1 = 0
        total = 0
        for codings in paired_codings.values():
            if len(codings) == 2:
                v1 = codings[0].get(indicator)
                v2 = codings[1].get(indicator)
                if v1 is not None and v2 is not None:
                    total += 1
                    if v1 == v2:
                        exact += 1
                    if abs(v1 - v2) <= 1:
                        within1 += 1
        if total > 0:
            exact_pct = exact / total * 100
            within1_pct = within1 / total * 100
            print(f"  {indicator:<30s} {exact_pct:>7.1f}%  {within1_pct:>9.1f}%")
            results[f"{indicator}_exact_pct"] = round(exact_pct, 1)
            results[f"{indicator}_within1_pct"] = round(within1_pct, 1)

    # Composite score differences
    composite_diffs = []
    for codings in paired_codings.values():
        c1 = codings[0].get("purificacao_composto")
        c2 = codings[1].get("purificacao_composto")
        if c1 is not None and c2 is not None:
            composite_diffs.append(abs(c1 - c2))

    if composite_diffs:
        print(f"\n  Composite score (purificacao_composto):")
        print(f"    Mean absolute difference: {np.mean(composite_diffs):.3f}")
        print(f"    Max  absolute difference: {max(composite_diffs):.3f}")

    # Disagreements
    disagreements = find_disagreements(paired_codings)
    if disagreements:
        print(f"\n  ⚠ Disagreements (>= 2 levels apart): {len(disagreements)}")
        for d in disagreements[:10]:
            vals = ", ".join(f"{k}: {v}" for k, v in d["values"].items())
            print(f"    {d['item_id']:15s} {d['indicator']:<30s} [{vals}] (Δ={d['spread']})")

    print()
    return results


def compute_alpha_overall(paired_codings: dict[str, list[dict]]) -> float | None:
    """Compute pooled Krippendorff's Alpha across all 10 indicators."""
    all_coders = set()
    for codings in paired_codings.values():
        for c in codings:
            all_coders.add(c["coded_by"])
    coder_list = sorted(all_coders)

    items = sorted(paired_codings.keys())
    n_units = len(items) * len(INDICATORS)
    matrix = np.full((len(coder_list), n_units), np.nan)

    for j, item_id in enumerate(items):
        for ind_idx, indicator in enumerate(INDICATORS):
            col = j * len(INDICATORS) + ind_idx
            for coding in paired_codings[item_id]:
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


def report(all_codings: dict[str, list[dict]]) -> dict[str, Any] | None:
    """Generate full IRR report (legacy multi-coder mode)."""
    # ... (existing implementation) ...
    # Keep existing logic for multi-coder mode
    from collections import defaultdict
    import numpy as np

    # Get items with 2+ coders
    double_coded = {k: v for k, v in all_codings.items() if len(set(c["coded_by"] for c in v)) >= 2}

    if not double_coded:
        print("\n  ⚠ No double-coded items found.")
        return None

    coders = set()
    for codings in double_coded.values():
        for c in codings:
            coders.add(c["coded_by"])
    print(f"\n  {'=' * 60}")
    print("  Inter-Rater Reliability Report (Krippendorff's Alpha)")
    print(f"{'=' * 60}")
    print(f"  Double-coded items:   {len(double_coded)}")
    print(f"  Coders:               {', '.join(sorted(coders))}")
    print()

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

    overall = compute_alpha_overall(double_coded)
    results["_overall"] = overall
    if overall is not None:
        print(f"\n  {'OVERALL (pooled)':<30s} {overall:>8.3f}")

    # Composite agreement
    composite_diffs = []
    for codings in double_coded.values():
        composites = [c.get("purificacao_composto") for c in codings if c.get("purificacao_composto") is not None]
        if len(composites) >= 2:
            composite_diffs.append(max(composites) - min(composites))
    if composite_diffs:
        print("\n  Composite score (purificacao_composto):")
        print(f"    Mean absolute difference: {np.mean(composite_diffs):.3f}")
        print(f"    Max  absolute difference: {max(composite_diffs):.3f}")

    # Disagreements
    disagreements = find_disagreements(double_coded)
    if disagreements:
        print(f"\n  ⚠ Disagreements (>= 2 levels apart): {len(disagreements)}")
        for d in disagreements[:10]:
            vals = ", ".join(f"{k}: {v}" for k, v in d["values"].items())
            print(f"    {d['item_id']:15s} {d['indicator']:<30s} [{vals}] (Δ={d['spread']})")

    print()
    return results


def adjudicate(all_codings: dict[str, list[dict]]):
    """Interactive adjudication of disagreements."""
    double_coded = {k: v for k, v in all_codings.items() if len(set(c["coded_by"] for c in v)) >= 2}
    if not double_coded:
        print("  ⚠ No double-coded items to adjudicate.")
        return

    disagreements = find_disagreements(double_coded, threshold=1)
    items_to_adjudicate = sorted(set(d["item_id"] for d in disagreements))

    print(f"\n  Adjudication mode: {len(items_to_adjudicate)} items with disagreements")
    print("  For each indicator, enter the consensus value (0-3) or Enter to keep first coder's value.\n")

    adjudicated = 0
    for item_id in items_to_adjudicate:
        codings = double_coded[item_id]
        print(f"\n  {'=' * 50}")
        print(f"  Item: {item_id}")

        coder_names = [c["coded_by"] for c in codings]
        header = f"  {'Indicator':<30s}" + "".join(f" {name:>15s}" for name in coder_names)
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
                    inp = input(f"    → Consensus for {indicator} [{default}]: ").strip()
                    if inp == "":
                        consensus_scores[indicator] = default
                        break
                    if inp == "q":
                        print(f"\n  Adjudicated {adjudicated} items this session.")
                        return
                    if inp in ("0", "1", "2", "3", "4"):
                        consensus_scores[indicator] = int(inp)
                        break
                    print("      Enter 0-4 or Enter for default")
            else:
                consensus_scores[indicator] = values[0]

        composite = round(sum(consensus_scores.values()) / len(consensus_scores), 2)

        regimes = [c.get("regime_iconocratico") for c in codings]
        if len(set(regimes)) == 1:
            regime = regimes[0]
        else:
            print(f"\n  Regimes differ: {regimes}")
            regime = input(f"    → Consensus regime [{regimes[0]}]: ").strip() or regimes[0]

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

        with open(PURIFICATION_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"  ✅ {item_id} adjudicated: composite={composite:.2f}, regime={regime}")
        adjudicated += 1

    print(f"\n  Session complete: {adjudicated} items adjudicated")


def export_json(results: dict, all_codings: dict[str, list[dict]]):
    """Export IRR results as JSON for notebook consumption."""
    double_coded = {k: v for k, v in all_codings.items() if len(set(c["coded_by"] for c in v)) >= 2}

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


def export_raw_pairs(paired_codings: dict[str, list[dict]], output_path: Path):
    """Export raw rater pairs as JSONL for further analysis."""
    with open(output_path, "w", encoding="utf-8") as f:
        for item_id, codings in paired_codings.items():
            if len(codings) == 2:
                r1, r2 = codings[0], codings[1]
                row = {
                    "item_id": item_id,
                    "rater1": r1["coded_by"],
                    "rater2": r2["coded_by"],
                }
                for ind in INDICATORS:
                    row[f"r1_{ind}"] = r1.get(ind)
                    row[f"r2_{ind}"] = r2.get(ind)
                row["r1_composite"] = r1.get("purificacao_composto")
                row["r2_composite"] = r2.get("purificacao_composto")
                row["r1_regime"] = r1.get("regime_iconocratico")
                row["r2_regime"] = r2.get("regime_iconocratico")
                row["r2_image_condition"] = r2.get("image_condition")
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"  ✅ Raw pairs exported to {output_path}")


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
    parser.add_argument(
        "--rater2",
        type=Path,
        help="Path to rater-2 blind coding results JSONL for IRR re-run comparison",
    )
    parser.add_argument(
        "--output-raw",
        type=Path,
        help="Export raw rater-1 vs rater-2 pairs as JSONL",
    )
    parser.add_argument(
        "--indicator-report",
        action="store_true",
        help="Include bootstrap 95% CI per indicator (requires --rater2)",
    )
    args = parser.parse_args()

    # Load data
    all_codings = load_all_codings()

    if args.adjudicate:
        adjudicate(all_codings)
        return

    if args.rater2:
        # IRR re-run mode: compare rater-1 vs rater-2
        print("=== IRR Re-run: Rater-1 vs Rater-2 ===")
        rater2_results = load_rater2_results(args.rater2)
        print(f"  Rater-2 results loaded: {len(rater2_results)} items")

        paired = build_rater_pairs(all_codings, rater2_results)
        print(f"  Paired items (both raters): {len(paired)}")

        if args.output_raw:
            export_raw_pairs(paired, args.output_raw)

        results = report_paired(paired, bootstrap_ci_flag=args.indicator_report)

        if args.export_json and results:
            # Extend export for re-run
            output = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "mode": "rater1_vs_rater2",
                "paired_items": len(paired),
                "alphas": results,
                "thresholds": {
                    "good": 0.800,
                    "tentative": 0.667,
                    "method": "Krippendorff's Alpha (ordinal metric)",
                },
            }
            with open(IRR_REPORT_JSON, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"  ✅ IRR re-run report saved to {IRR_REPORT_JSON}")
        return

    # Legacy multi-coder mode
    results = report(all_codings)

    if args.export_json and results:
        export_json(results, all_codings)


if __name__ == "__main__":
    sys.exit(main())