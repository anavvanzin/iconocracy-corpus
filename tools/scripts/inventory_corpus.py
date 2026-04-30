#!/usr/bin/env python3
"""Extract neutral metadata from all SCOUT candidate files into CSV.

Usage: python tools/scripts/inventory_corpus.py
Output: docs/superpowers/inventory/2026-04-29-corpus-inventory.csv
"""

import csv
import os
import re
import yaml
from datetime import datetime

CANDIDATOS_DIR = "vault/candidatos"
OUTPUT_DIR = "docs/superpowers/inventory"
RECORDS_PATH = "data/processed/records.jsonl"

def parse_frontmatter(filepath):
    """Extract YAML frontmatter from a markdown file."""
    with open(filepath, "r") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

def extract_century(data_str):
    """Extract century from data_estimada field (e.g. '1792', '1789-1791', 'c.1910')."""
    if not data_str:
        return ""
    years = re.findall(r"\b(\d{4})\b", str(data_str))
    if not years:
        return ""
    year = int(years[0])
    return str((year - 1) // 100 + 1) + "th"

def load_promoted_ids():
    """Load all records_item_id from records.jsonl for cross-reference."""
    if not os.path.exists(RECORDS_PATH):
        return set()
    promoted = set()
    with open(RECORDS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = yaml.safe_load(line)
                if rec and "item_id" in rec:
                    promoted.add(rec["item_id"])
            except yaml.YAMLError:
                pass
    return promoted

def figure_type_simplify(motivo):
    """Map motivo_alegorico to a simpler figure type."""
    if not motivo:
        return ""
    motivo_lower = motivo.lower()
    if "justi" in motivo_lower or "justitia" in motivo_lower:
        return "Justitia"
    if "república" in motivo_lower or "republique" in motivo_lower or "republica" in motivo_lower:
        return "Republic"
    if "liberdade" in motivo_lower or "liberte" in motivo_lower or "libert" in motivo_lower or "freedom" in motivo_lower:
        return "Liberty"
    if "marianne" in motivo_lower:
        return "Marianne"
    if "britannia" in motivo_lower:
        return "Britannia"
    if "germania" in motivo_lower or "germany" in motivo_lower:
        return "Germania"
    if "columbia" in motivo_lower or "colúmbia" in motivo_lower:
        return "Columbia"
    if "constitution" in motivo_lower or "constituição" in motivo_lower:
        return "Constitution"
    if "ceres" in motivo_lower:
        return "Ceres"
    if "hispania" in motivo_lower:
        return "Hispania"
    if "helvetia" in motivo_lower:
        return "Helvetia"
    if "athena" in motivo_lower or "minerva" in motivo_lower:
        return "Minerva/Athena"
    if "alegoria" in motivo_lower or "allegory" in motivo_lower or "allegori" in motivo_lower or "female figure" in motivo_lower:
        return "Generic allegory"
    if "vitória" in motivo_lower or "victory" in motivo_lower or "victoria" in motivo_lower or "victoire" in motivo_lower:
        return "Victory"
    if "paz" in motivo_lower or "peace" in motivo_lower or "paix" in motivo_lower:
        return "Peace"
    return motivo[:60]  # truncate long descriptions

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    promoted_ids = load_promoted_ids()

    rows = []
    scout_files = sorted(
        [f for f in os.listdir(CANDIDATOS_DIR) if f.startswith("SCOUT-") and f.endswith(".md")],
        key=lambda x: x.lower()
    )

    for fname in scout_files:
        fpath = os.path.join(CANDIDATOS_DIR, fname)
        fm = parse_frontmatter(fpath)
        if fm is None:
            rows.append({
                "scout_id": fname.replace(".md", ""),
                "title": "",
                "country": "",
                "century": "",
                "medium": "",
                "figure_type": "",
                "iconclass": "",
                "type": "corpus-candidato",
                "promoted": "",
                "notes": "NO FRONTMATTER"
            })
            continue

        scout_id = fm.get("id", fname.replace(".md", ""))
        item_id = fm.get("records_item_id", "")
        promoted = "YES" if item_id and item_id in promoted_ids else ""

        ctype = fm.get("tipo", "corpus-candidato")
        if isinstance(ctype, list):
            ctype = ctype[0] if ctype else "corpus-candidato"

        country = fm.get("pais", "")
        if isinstance(country, list):
            country = ", ".join(country)

        medium = fm.get("suporte", "")

        motivo = fm.get("motivo_alegorico", "")
        fig_type = figure_type_simplify(motivo)

        iconclass = ""
        if "iconclass" in fm:
            iconclass = str(fm["iconclass"])
        tags = fm.get("tags", [])
        if isinstance(tags, list):
            for t in tags:
                if "48C" in str(t):
                    iconclass = str(t)

        rows.append({
            "scout_id": scout_id,
            "title": fm.get("titulo", ""),
            "country": country,
            "century": extract_century(fm.get("data_estimada", "")),
            "medium": medium,
            "figure_type": fig_type,
            "iconclass": iconclass,
            "type": ctype,
            "promoted": promoted,
            "notes": ""
        })

    # Write CSV
    outpath = os.path.join(OUTPUT_DIR, "2026-04-29-corpus-inventory.csv")
    fieldnames = ["scout_id", "title", "country", "century", "medium", "figure_type", "iconclass", "type", "promoted", "notes"]
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    promoted_count = sum(1 for r in rows if r["promoted"])
    zw_count = sum(1 for r in rows if "zwischenraum" in r["type"].lower())
    no_fm = sum(1 for r in rows if r["notes"] == "NO FRONTMATTER")

    print(f"Written: {outpath}")
    print(f"Total candidates: {len(rows)}")
    print(f"  Regular: {len(rows) - zw_count}")
    print(f"  Zwischenraum (ZW): {zw_count}")
    print(f"  Already promoted: {promoted_count}")
    print(f"  Missing frontmatter: {no_fm}")

if __name__ == "__main__":
    main()
