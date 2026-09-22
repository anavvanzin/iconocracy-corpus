#!/usr/bin/env python3
"""
Reproduz as tabelas estatísticas do Appendix A do Working Paper
"Dessexualization Threshold".

Uso:
    python3 tese/artigos/scripts/appendix-a-stats.py

Roda a partir da raiz de ~/Research/hub/iconocracy-corpus/.

Cada função imprime uma das tabelas do apêndice em markdown; basta
copiar-colar a saída no .md se precisar regerar.

Estado-atual ancorado em 5/jun/2026, N=314.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter
from typing import Any

CORPUS_PATH = pathlib.Path("corpus/corpus-data.json")


def load_corpus() -> list[dict[str, Any]]:
    if not CORPUS_PATH.exists():
        sys.exit(
            f"corpus não encontrado em {CORPUS_PATH}\n"
            "Execute a partir da raiz de iconocracy-corpus/."
        )
    with CORPUS_PATH.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        sys.exit("Esperado JSON-array no topo de corpus-data.json")
    return data


def table_country(data: list[dict[str, Any]]) -> None:
    print("\n## A.1.1 Country distribution\n")
    counter = Counter(item.get("country") or "(unspecified)" for item in data)
    total = sum(counter.values())
    print("| Country | N | % of corpus |")
    print("|---|---:|---:|")
    main = counter.most_common(10)
    listed = sum(c for _, c in main)
    for name, n in main:
        print(f"| {name} | {n} | {n*100/total:.1f} |")
    other = total - listed
    if other:
        print(f"| Other / multiple | {other} | {other*100/total:.1f} |")
    print(f"| **Total** | **{total}** | **100.0** |")


def table_regime(data: list[dict[str, Any]]) -> None:
    print("\n## A.1.2 Regime distribution\n")
    counter = Counter(
        (item.get("regime") or "").strip().lower() or "(uncoded)" for item in data
    )
    coded = sum(c for k, c in counter.items() if k != "(uncoded)")
    order = ["fundacional", "normativo", "militar", "contra-alegoria"]
    print("| Regime | N | % of coded |")
    print("|---|---:|---:|")
    for key in order:
        n = counter.get(key, 0)
        pct = n * 100 / coded if coded else 0
        label = {
            "fundacional": "fundacional (foundational)",
            "normativo": "normativo (normative)",
            "militar": "militar (military)",
            "contra-alegoria": "contra-alegoria",
        }[key]
        print(f"| {label} | {n} | {pct:.1f} |")
    uncoded = counter.get("(uncoded)", 0)
    print(f"| **Coded subtotal** | **{coded}** | **100.0** |")
    print(f"| (regime not yet assigned) | {uncoded} | — |")
    print(f"| **Total** | **{coded + uncoded}** | — |")


def table_country_x_regime(data: list[dict[str, Any]]) -> None:
    print("\n## A.1.3 Country × Regime cross-tabulation\n")
    top = [c for c, _ in Counter(
        item.get("country") for item in data if item.get("country")
    ).most_common(10)]
    print("| Country | found. | norm. | milit. | contra. | (uncoded) | total |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for ct in top:
        items = [i for i in data if i.get("country") == ct]
        r = Counter((i.get("regime") or "").strip().lower() for i in items)
        row = [
            ct,
            r.get("fundacional", 0),
            r.get("normativo", 0),
            r.get("militar", 0),
            r.get("contra-alegoria", 0),
            r.get("", 0),
            len(items),
        ]
        print("| " + " | ".join(str(x) for x in row) + " |")


def table_scores(data: list[dict[str, Any]]) -> None:
    print("\n## A.2.2 Score distribution\n")
    scores = [
        item["endurecimento_score"]
        for item in data
        if isinstance(item.get("endurecimento_score"), (int, float))
    ]
    n = len(scores)
    bins = [
        (0.0, 1.0, "LOW", "0.00 ≤ s < 1.00"),
        (1.0, 2.0, "MED-LOW", "1.00 ≤ s < 2.00"),
        (2.0, 2.5, "MEDIUM", "2.00 ≤ s < 2.50"),
        (2.5, 3.0, "MED-HIGH", "2.50 ≤ s < 3.00"),
        (3.0, 5.0, "HIGH", "s ≥ 3.00"),
    ]
    print("| Range | Label | N | % |")
    print("|---|---|---:|---:|")
    for lo, hi, label, rng in bins:
        c = sum(1 for s in scores if lo <= s < hi)
        print(f"| {rng} | {label} | {c} | {c*100/n:.1f} |")
    print(f"| **Total scored** | | **{n}** | **100.0** |")
    print(f"\nMean = {sum(scores)/n:.2f} | min = {min(scores):.2f} | "
          f"max = {max(scores):.2f}")


def table_high_score(data: list[dict[str, Any]]) -> None:
    print("\n## A.2.3 Items with score ≥ 2.50\n")
    high = sorted(
        (i for i in data if isinstance(i.get("endurecimento_score"), (int, float))
         and i["endurecimento_score"] >= 2.5),
        key=lambda x: -x["endurecimento_score"],
    )
    print("| Score | Country | Regime | Item |")
    print("|---:|---|---|---|")
    for it in high:
        title = (it.get("title") or "").strip()
        if len(title) > 60:
            title = title[:57] + "…"
        print(f"| {it['endurecimento_score']:.2f} | {it.get('country','-')} | "
              f"{it.get('regime','-')} | {title} |")


def table_temporal(data: list[dict[str, Any]]) -> None:
    print("\n## A.3 Temporal distribution (decadal)\n")
    years: list[int] = []
    for item in data:
        raw = item.get("year") or item.get("date_iso") or ""
        try:
            if isinstance(raw, str) and len(raw) >= 4 and raw[:4].isdigit():
                years.append(int(raw[:4]))
            elif isinstance(raw, int):
                years.append(raw)
        except ValueError:
            continue
    if not years:
        print("(nenhum item com data válida)")
        return
    decades = Counter((y // 10) * 10 for y in years)
    print(f"N com ano = {len(years)} / {len(data)}\n")
    print("| Decade | N |")
    print("|---|---:|")
    for d in sorted(decades):
        print(f"| {d}s | {decades[d]} |")


def main() -> None:
    data = load_corpus()
    print(f"# Appendix A statistics — reproduced from corpus-data.json")
    print(f"\nN = {len(data)}")
    table_country(data)
    table_regime(data)
    table_country_x_regime(data)
    table_scores(data)
    table_high_score(data)
    table_temporal(data)


if __name__ == "__main__":
    main()
