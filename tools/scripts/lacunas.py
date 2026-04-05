#!/usr/bin/env python3
"""
lacunas.py — Gap analysis for the Iconocracy corpus.

Crosses the existing corpus against the theoretical matrix
(6 countries x 3 regimes x 8 supports) to identify gaps.

Usage:
    python lacunas.py                  # full matrix report
    python lacunas.py --country FR     # gaps for France only
    python lacunas.py --hunt           # suggest hunt.py commands to fill gaps
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

CORPUS_PATH = Path(__file__).resolve().parents[2] / "corpus" / "corpus-data.json"
VAULT_PATH = Path(__file__).resolve().parents[2] / "vault" / "candidatos"

# ─── Theoretical matrix ──────────────────────────────────────────────────

SCOPE_COUNTRIES = ["FR", "UK", "DE", "US", "BE", "BR"]

COUNTRY_NAMES = {
    "FR": "France", "UK": "United Kingdom", "DE": "Germany",
    "US": "United States", "BE": "Belgium", "BR": "Brazil",
}

REGIMES = ["fundacional", "normativo", "militar"]

CORE_SUPPORTS = ["moeda", "selo", "monumento", "estampa",
                  "frontispicio", "papel-moeda", "cartaz", "medalha"]

# Minimum expected items per cell for a "complete" corpus
MIN_PER_CELL = 1

# Priority cells (from the thesis's analytical framework)
PRIORITY_CELLS = {
    ("FR", "fundacional", "estampa"),     # Révolution imagery
    ("FR", "normativo", "moeda"),          # Semeuse, Marianne-Coq
    ("FR", "normativo", "selo"),           # Semeuse stamps
    ("FR", "militar", "cartaz"),           # WWI propaganda
    ("UK", "normativo", "moeda"),          # Britannia pennies
    ("UK", "militar", "moeda"),            # Trade dollars
    ("DE", "normativo", "selo"),           # Germania stamps
    ("DE", "militar", "papel-moeda"),      # Notgeld, Reichsbanknoten
    ("US", "fundacional", "moeda"),        # Seated/Standing Liberty
    ("US", "normativo", "monumento"),      # Statues of Freedom/Republic
    ("BR", "fundacional", "moeda"),        # Efígie da República
    ("BR", "normativo", "selo"),           # Republic stamps
    ("BE", "normativo", "moeda"),          # Leopold francs
    ("BE", "militar", "papel-moeda"),      # Congo banknotes
}


# ─── Helpers ──────────────────────────────────────────────────────────────

def normalize_country(country_str):
    """Map country name to 2-letter code."""
    mapping = {
        "France": "FR", "United Kingdom": "UK", "Germany": "DE",
        "United States": "US", "Belgium": "BE", "Brazil": "BR",
    }
    return mapping.get(country_str)


def load_corpus():
    """Load corpus and return items within scope (6 countries)."""
    with open(CORPUS_PATH, encoding="utf-8") as f:
        items = json.load(f)
    scoped = []
    for item in items:
        cc = normalize_country(item.get("country", ""))
        if cc and cc in SCOPE_COUNTRIES:
            item["_cc"] = cc
            scoped.append(item)
    return scoped


def count_vault_notes():
    """Count SCOUT notes in vault by scanning filenames."""
    count = 0
    if VAULT_PATH.exists():
        for f in VAULT_PATH.iterdir():
            if f.suffix == ".md":
                count += 1
    return count


def build_matrix(items):
    """Build a 3D count matrix: country x regime x support."""
    matrix = defaultdict(int)
    items_by_cell = defaultdict(list)

    for item in items:
        cc = item.get("_cc", "")
        regime = item.get("regime", "")
        support = item.get("support", "")

        if not cc or not regime:
            continue

        # Count in matrix even if support is unusual
        key = (cc, regime, support or "outro")
        matrix[key] += 1
        items_by_cell[key].append(item.get("id", "?"))

    return matrix, items_by_cell


def find_gaps(matrix):
    """Identify cells with 0 items (absolute gaps)."""
    gaps = []
    for cc in SCOPE_COUNTRIES:
        for regime in REGIMES:
            for support in CORE_SUPPORTS:
                key = (cc, regime, support)
                count = matrix.get(key, 0)
                if count < MIN_PER_CELL:
                    is_priority = key in PRIORITY_CELLS
                    gaps.append({
                        "country": cc,
                        "regime": regime,
                        "support": support,
                        "count": count,
                        "priority": is_priority,
                    })
    return gaps


def print_matrix_table(matrix, countries=None):
    """Print the matrix as a readable table."""
    if countries is None:
        countries = SCOPE_COUNTRIES

    print(f"\n{'MATRIZ DO CORPUS':=^78}")
    print(f"{'':14s}", end="")
    for regime in REGIMES:
        print(f"  {regime.upper():^20s}", end="")
    print()

    for cc in countries:
        name = COUNTRY_NAMES.get(cc, cc)
        print(f"\n  {name} ({cc})")

        for support in CORE_SUPPORTS:
            print(f"    {support:16s}", end="")
            for regime in REGIMES:
                key = (cc, regime, support)
                count = matrix.get(key, 0)
                is_priority = key in PRIORITY_CELLS
                marker = "*" if is_priority else " "
                if count == 0:
                    cell = f"  ---{marker}"
                else:
                    cell = f"  {count:3d}{marker}"
                print(f"  {cell:>10s}", end="")
            print()

    print(f"\n{'* = célula prioritária para a tese':>78s}")


def print_gap_report(gaps, matrix, items):
    """Print the gap analysis report."""
    total_cells = len(SCOPE_COUNTRIES) * len(REGIMES) * len(CORE_SUPPORTS)
    filled = total_cells - len(gaps)
    coverage = filled / total_cells * 100

    print(f"\n{'RELATÓRIO DE LACUNAS':=^78}")
    print(f"  Itens no corpus (6 países): {len(items)}")
    print(f"  Notas no vault: {count_vault_notes()}")
    print(f"  Células da matriz: {total_cells}")
    print(f"  Preenchidas (>= {MIN_PER_CELL}): {filled} ({coverage:.0f}%)")
    print(f"  Lacunas: {len(gaps)}")

    priority_gaps = [g for g in gaps if g["priority"]]
    print(f"  Lacunas prioritárias: {len(priority_gaps)}")

    if priority_gaps:
        print(f"\n{'LACUNAS PRIORITÁRIAS':=^78}")
        for g in priority_gaps:
            name = COUNTRY_NAMES.get(g["country"], g["country"])
            print(f"  [{g['country']}] {name} / {g['regime'].upper()} / {g['support']}")

    # Group remaining gaps by country
    other_gaps = [g for g in gaps if not g["priority"]]
    if other_gaps:
        print(f"\n{'DEMAIS LACUNAS':=^78}")
        by_country = defaultdict(list)
        for g in other_gaps:
            by_country[g["country"]].append(g)

        for cc in SCOPE_COUNTRIES:
            if cc not in by_country:
                continue
            name = COUNTRY_NAMES.get(cc, cc)
            country_gaps = by_country[cc]
            print(f"\n  {name} ({cc}) — {len(country_gaps)} lacunas:")
            for g in country_gaps:
                print(f"    {g['regime']:14s} / {g['support']}")


def print_hunt_suggestions(gaps):
    """Generate hunt.py commands to fill priority gaps."""
    print(f"\n{'SUGESTÕES DE BUSCA (hunt.py)':=^78}")

    priority_gaps = [g for g in gaps if g["priority"]]
    if not priority_gaps:
        priority_gaps = gaps[:10]

    for g in priority_gaps:
        cmd = f"python3 tools/scripts/hunt.py --country {g['country']} --support {g['support']}"
        if g["regime"] == "fundacional":
            cmd += " --period 1789-1870"
        elif g["regime"] == "militar":
            cmd += " --period 1914-1945"
        elif g["regime"] == "normativo":
            cmd += " --period 1880-1920"
        cmd += " --limit 20"
        name = COUNTRY_NAMES.get(g["country"], g["country"])
        print(f"\n  # {name} / {g['regime'].upper()} / {g['support']}")
        print(f"  {cmd}")


def print_country_summary(matrix, items, countries=None):
    """Print per-country summary stats."""
    if countries is None:
        countries = SCOPE_COUNTRIES

    print(f"\n{'RESUMO POR PAÍS':=^78}")
    for cc in countries:
        name = COUNTRY_NAMES.get(cc, cc)
        cc_items = [i for i in items if i.get("_cc") == cc]

        regimes_count = defaultdict(int)
        supports_count = defaultdict(int)
        for item in cc_items:
            r = item.get("regime", "?")
            regimes_count[r] += 1
            s = item.get("support", "?")
            supports_count[s] += 1

        total_cells = len(REGIMES) * len(CORE_SUPPORTS)
        filled = sum(1 for r in REGIMES for s in CORE_SUPPORTS
                     if matrix.get((cc, r, s), 0) >= MIN_PER_CELL)
        coverage = filled / total_cells * 100

        print(f"\n  {name} ({cc}): {len(cc_items)} itens, {coverage:.0f}% cobertura")
        print(f"    Regimes: {dict(regimes_count)}")
        print(f"    Suportes: {dict(supports_count)}")


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Analyse gaps in the Iconocracy corpus"
    )
    parser.add_argument("--country", type=str, default=None,
                        help="Filter by country code (FR,UK,DE,US,BE,BR)")
    parser.add_argument("--hunt", action="store_true",
                        help="Print hunt.py commands to fill gaps")
    parser.add_argument("--json", action="store_true",
                        help="Output gaps as JSON")

    args = parser.parse_args()

    items = load_corpus()
    matrix, items_by_cell = build_matrix(items)

    countries = None
    if args.country:
        countries = [c.strip().upper() for c in args.country.split(",")]

    gaps = find_gaps(matrix)
    if countries:
        gaps = [g for g in gaps if g["country"] in countries]

    if args.json:
        print(json.dumps(gaps, ensure_ascii=False, indent=2))
        return

    # Print full report
    print_matrix_table(matrix, countries)
    print_country_summary(matrix, items, countries)
    print_gap_report(gaps, matrix, items)

    if args.hunt:
        print_hunt_suggestions(gaps)


if __name__ == "__main__":
    main()
