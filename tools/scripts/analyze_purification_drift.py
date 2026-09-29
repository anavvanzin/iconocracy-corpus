#!/usr/bin/env python3
"""
Analyze score drift between original and auto-coded endurecimento entries.

Reads purification.jsonl, splits by coded_by, and reports per-indicator,
per-country, and per-regime comparisons. Flags indicators with drift > 0.5
for potential recalibration.

Usage:
    python tools/scripts/analyze_purification_drift.py
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PURIFICATION = REPO_ROOT / "data" / "processed" / "purification.jsonl"

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]


def load_items(path):
    with open(path) as f:
        return [json.loads(line) for line in f]


def get_country(item_id):
    parts = item_id.split("-")
    return parts[0] if len(parts) >= 2 else "??"


def mean_indicator(items, ind):
    """Mean of one ordinal indicator across a group (0 for empty group)."""
    return sum(x[ind] for x in items) / len(items) if items else 0


def mean_abs_indicator_drift(group_a, group_b):
    """Drift = média do delta absoluto por indicador ordinal entre dois grupos.

    Substitui o antigo drift de purificacao_composto (campo removido —
    decisão 2026-09-24): o composto não é mais emitido nem lido.
    """
    if not group_a or not group_b:
        return 0
    return sum(
        abs(mean_indicator(group_a, ind) - mean_indicator(group_b, ind))
        for ind in INDICATORS
    ) / len(INDICATORS)


def main():
    items = load_items(PURIFICATION)
    original = [x for x in items if x["coded_by"] != "hermes-auto"]
    auto = [x for x in items if x["coded_by"] == "hermes-auto"]

    # --- Overall drift ---
    print("=" * 60)
    print("PHASE 1 — SCORE DRIFT ANALYSIS")
    print(f"Original-coded: {len(original)}  |  Auto-coded: {len(auto)}")
    print("=" * 60)

    print(f"\n{'Indicator':<32} {'Orig':>6} {'Auto':>6} {'Diff':>7}  {'Flag':>6}")
    print("-" * 60)
    flagged = []
    for ind in INDICATORS:
        o_mean = sum(x[ind] for x in original) / len(original)
        a_mean = sum(x[ind] for x in auto) / len(auto)
        diff = a_mean - o_mean
        flag = "**" if abs(diff) > 0.5 else ""
        if abs(diff) > 0.5:
            flagged.append((ind, diff))
        print(f"{ind:<32} {o_mean:>6.2f} {a_mean:>6.2f} {diff:>+7.2f}  {flag:>6}")

    o_lvl = sum(mean_indicator(original, ind) for ind in INDICATORS) / len(INDICATORS)
    a_lvl = sum(mean_indicator(auto, ind) for ind in INDICATORS) / len(INDICATORS)
    print(f"{'media_indicadores':<32} {o_lvl:>6.2f} {a_lvl:>6.2f} {a_lvl-o_lvl:>+7.2f}")
    global_drift = mean_abs_indicator_drift(original, auto)
    print(f"  drift médio |Δ| por indicador: {global_drift:.2f}")
    print(f"\nFlagged indicators (|diff| > 0.5): {len(flagged)}")
    for ind, diff in flagged:
        print(f"  {ind}: {diff:+.2f}")

    # --- By regime ---
    print(f"\n{'='*60}")
    print("BY REGIME")
    for regime in ["fundacional", "normativo", "militar", "contra-alegoria"]:
        o_r = [x for x in original if x.get("regime_iconocratico") == regime]
        a_r = [x for x in auto if x.get("regime_iconocratico") == regime]
        if not o_r and not a_r:
            continue
        print(f"\n  {regime}:")
        drift = mean_abs_indicator_drift(o_r, a_r)
        print(f"    items: {len(o_r)} orig, {len(a_r)} auto")
        print(f"    drift |Δ| médio por indicador: {drift:.2f}")
        for ind in INDICATORS:
            o_m = sum(x[ind] for x in o_r) / len(o_r) if o_r else 0
            a_m = sum(x[ind] for x in a_r) / len(a_r) if a_r else 0
            d = a_m - o_m
            if abs(d) > 0.5:
                print(f"      {ind}: {o_m:.2f} -> {a_m:.2f} ({d:+.2f})")

    # --- By country ---
    print(f"\n{'='*60}")
    print("BY COUNTRY")
    countries = set()
    for item in items:
        countries.add(get_country(item["id"]))
    for country in sorted(countries):
        o_c = [x for x in original if get_country(x["id"]) == country]
        a_c = [x for x in auto if get_country(x["id"]) == country]
        if not o_c and not a_c:
            continue
        drift = mean_abs_indicator_drift(o_c, a_c)
        flag = " **" if drift > 0.5 else ""
        print(f"  {country}: {len(o_c)} orig, {len(a_c)} auto, drift {drift:.2f}{flag}")

    # --- Top outliers ---
    print(f"\n{'='*60}")
    print("TOP AUTO-CODED OUTLIERS (vs regime/country peers)")
    print("=" * 60)
    for idx, item in enumerate(auto):
        c = get_country(item["id"])
        regime = item.get("regime_iconocratico", "unknown")
        peers = [x for x in original if get_country(x["id"]) == c and x.get("regime_iconocratico") == regime]
        if peers:
            outlier_score = sum(
                abs(item[ind] - mean_indicator(peers, ind)) for ind in INDICATORS
            ) / len(INDICATORS)
        else:
            outlier_score = 0
        item["_country"] = c
        item["_outlier_score"] = outlier_score

    # Sort by abs(outlier)
    sorted_items = sorted(auto, key=lambda x: abs(x["_outlier_score"]), reverse=True)
    for item in sorted_items[:15]:
        print(f"  {item['id']:20} "
              f"{item['_country']}/{item.get('regime_iconocratico','?')}  "
              f"outlier_vs_peers={item['_outlier_score']:+.2f}  "
              f"drift_global={global_drift:.2f}")


if __name__ == "__main__":
    main()
