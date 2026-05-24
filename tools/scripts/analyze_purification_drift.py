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
import sys
from collections import Counter, defaultdict
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

    o_comp = sum(x["purificacao_composto"] for x in original) / len(original)
    a_comp = sum(x["purificacao_composto"] for x in auto) / len(auto)
    print(f"{'purificacao_composto':<32} {o_comp:>6.2f} {a_comp:>6.2f} {a_comp-o_comp:>+7.2f}")
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
        o_mean = sum(x["purificacao_composto"] for x in o_r) / len(o_r) if o_r else 0
        a_mean = sum(x["purificacao_composto"] for x in a_r) / len(a_r) if a_r else 0
        print(f"    items: {len(o_r)} orig, {len(a_r)} auto")
        print(f"    composite: {o_mean:.2f} -> {a_mean:.2f} (drift {a_mean-o_mean:+.2f})")
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
        o_mean = sum(x["purificacao_composto"] for x in o_c) / len(o_c) if o_c else 0
        a_mean = sum(x["purificacao_composto"] for x in a_c) / len(a_c) if a_c else 0
        flag = " **" if abs(a_mean - o_mean) > 0.5 else ""
        print(f"  {country}: {len(o_c)} orig ({o_mean:.2f}), {len(a_c)} auto ({a_mean:.2f}), drift {a_mean-o_mean:+.2f}{flag}")

    # --- Top outliers ---
    print(f"\n{'='*60}")
    print("TOP AUTO-CODED OUTLIERS (vs regime/country peers)")
    print("=" * 60)
    for idx, item in enumerate(auto):
        c = get_country(item["id"])
        regime = item.get("regime_iconocratico", "unknown")
        peers = [x for x in original if get_country(x["id"]) == c and x.get("regime_iconocratico") == regime]
        if peers:
            peer_mean = sum(x["purificacao_composto"] for x in peers) / len(peers)
            outlier_score = item["purificacao_composto"] - peer_mean
        else:
            outlier_score = 0
        item["_country"] = c
        item["_outlier_score"] = outlier_score

    # Sort by abs(outlier)
    sorted_items = sorted(auto, key=lambda x: abs(x["_outlier_score"]), reverse=True)
    for item in sorted_items[:15]:
        print(f"  {item['id']:20} comp={item['purificacao_composto']:.1f}  "
              f"{item['_country']}/{item.get('regime_iconocratico','?')}  "
              f"outlier_vs_peers={item['_outlier_score']:+.2f}  "
              f"auto-mean={a_comp:.2f}")


if __name__ == "__main__":
    main()
