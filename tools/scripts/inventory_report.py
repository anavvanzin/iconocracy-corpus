#!/usr/bin/env python3
"""Inventory report: pivot tables for corpus analysis.

Usage: python tools/scripts/inventory_report.py
"""

import csv
from collections import Counter, defaultdict

CSV_PATH = "docs/superpowers/inventory/2026-04-29-corpus-inventory.csv"

def load_csv():
    rows = []
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_counts(label, counter, top=8):
    print(f"\n  {label}:")
    for item, count in counter.most_common(top):
        bar = "█" * count
        print(f"    {item:20s} {count:3d}  {bar}")

def main():
    rows = load_csv()
    regular = [r for r in rows if "zwischenraum" not in r["type"].lower()]
    zw = [r for r in rows if "zwischenraum" in r["type"].lower()]

    print_section("OVERVIEW")
    print(f"  Total files:         {len(rows)}")
    print(f"  Regular candidates:  {len(regular)}")
    print(f"  Zwischenraum panels: {len(zw)}")
    print(f"  Already promoted:    {sum(1 for r in rows if r['promoted'])}")

    print_section("BY CENTURY")
    century_counts = Counter()
    for r in regular:
        c = r["century"].strip()
        if c:
            century_counts[c] += 1
        else:
            century_counts["UNKNOWN"] += 1
    print_counts("Century", century_counts)

    print_section("BY COUNTRY")
    country_counts = Counter()
    for r in regular:
        countries = r["country"].split(", ")
        for c in countries:
            c = c.strip()
            if c:
                country_counts[c] += 1
    print_counts("Country", country_counts)

    print_section("BY MEDIUM")
    medium_counts = Counter()
    for r in regular:
        m = r["medium"].strip()
        if m:
            medium_counts[m] += 1
        else:
            medium_counts["UNKNOWN"] += 1
    print_counts("Medium", medium_counts)

    print_section("BY FIGURE TYPE")
    figure_counts = Counter()
    for r in regular:
        f = r["figure_type"].strip()
        if f:
            figure_counts[f] += 1
        else:
            figure_counts["UNKNOWN"] += 1
    print_counts("Figure type", figure_counts, top=12)

    print_section("MISSING FRONTMATTER")
    missing = [r for r in rows if r["notes"] == "NO FRONTMATTER"]
    for m in missing:
        print(f"  {m['scout_id']}")

    print_section("NO CENTURY (needs review)")
    no_century = [r for r in regular if not r["century"].strip()]
    print(f"  {len(no_century)} items")
    for r in no_century[:15]:
        print(f"    {r['scout_id']:15s} {r['title'][:60]}")

    print_section("UNPROMOTED BY COUNTRY (gaps)")
    unpromoted = [r for r in regular if not r["promoted"]]
    country_gaps = Counter()
    for r in unpromoted:
        countries = r["country"].split(", ")
        for c in countries:
            c = c.strip()
            if c:
                country_gaps[c] += 1
    print_counts("Unpromoted by country", country_gaps)

    print_section("UNPROMOTED BY FIGURE TYPE")
    fig_gaps = Counter()
    for r in unpromoted:
        f = r["figure_type"].strip()
        if f:
            fig_gaps[f] += 1
        else:
            fig_gaps["UNKNOWN"] += 1
    print_counts("Unpromoted by figure type", fig_gaps, top=10)

if __name__ == "__main__":
    main()
