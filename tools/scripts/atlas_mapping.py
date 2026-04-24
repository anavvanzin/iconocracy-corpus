#!/usr/bin/env python3
"""
atlas_mapping.py — Map Zwischenraum panels to thesis Atlas panels.

The thesis defines 8 Atlas panels (from the companion app).
The vault contains N Zwischenraum panels (SCOUT-ZW-*).
This script maps each ZW panel to one or more Atlas panels
and generates a mapping file for the companion.

Usage:
    python tools/scripts/atlas_mapping.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
VAULT = REPO / "vault" / "candidatos"

# The 8 thesis Atlas panels (from iconocracia-companion)
ATLAS_PANELS = {
    1: {"name": "Gênese", "desc": "A primeira vez que o Estado vestiu um corpo feminino",
        "keywords": ["fundacional", "1789", "constitution", "founding", "genesis", "primeiro"]},
    2: {"name": "Justitia", "desc": "Balança, espada, venda — a fórmula que sobrevive",
        "keywords": ["justitia", "justice", "balança", "espada", "tribunal"]},
    3: {"name": "Domesticação", "desc": "Como o corpo alegórico foi purificado",
        "keywords": ["normativo", "purificação", "domesticação", "semeuse", "definitivo"]},
    4: {"name": "endurecimento", "desc": "O corpo que endurece quando o Estado faz guerra",
        "keywords": ["militar", "guerra", "endurecimento", "colonial", "trade dollar", "piastre"]},
    5: {"name": "Pedra e Bronze", "desc": "Quando a alegoria se torna monumento",
        "keywords": ["monumento", "escultura", "pedra", "bronze", "cariátide", "edifício"]},
    6: {"name": "Balança e Império", "desc": "A justiça como arma geopolítica",
        "keywords": ["colonial", "império", "imperial", "indochina", "congo", "trade"]},
    7: {"name": "Branquitude", "desc": "O contrato racial da imagem soberana",
        "keywords": ["racial", "branquitude", "colonial", "contrato-racial", "expulsão"]},
    8: {"name": "Fissuras", "desc": "Contra-alegorias e rupturas",
        "keywords": ["contra-alegoria", "ruptura", "fissura", "ausência", "negativo"]},
}


def score_panel_match(zw_text: str, atlas_keywords: list[str]) -> int:
    """Score how well a ZW panel matches an Atlas panel."""
    text_lower = zw_text.lower()
    return sum(1 for kw in atlas_keywords if kw.lower() in text_lower)


def map_zw_to_atlas():
    """Map each ZW panel to its best Atlas panel(s)."""
    mappings = []

    for zw_path in sorted(VAULT.glob("SCOUT-ZW-*.md")):
        text = zw_path.read_text()

        # Extract ZW metadata
        id_match = re.search(r"id:\s*(SCOUT-ZW-\d+)", text)
        title_match = re.search(r'titulo:\s*"(.+?)"', text)
        zw_id = id_match.group(1) if id_match else zw_path.stem
        zw_title = title_match.group(1) if title_match else zw_path.stem

        # Score against each Atlas panel
        scores = {}
        for panel_n, panel in ATLAS_PANELS.items():
            score = score_panel_match(text, panel["keywords"])
            if score > 0:
                scores[panel_n] = score

        # Best matches (top 2 if tied, otherwise top 1)
        if scores:
            max_score = max(scores.values())
            best = [n for n, s in scores.items() if s >= max_score - 1]
        else:
            best = []

        mappings.append({
            "zw_id": zw_id,
            "zw_title": zw_title,
            "atlas_panels": best,
            "atlas_names": [ATLAS_PANELS[n]["name"] for n in best],
            "scores": scores,
            "file": zw_path.name,
        })

    return mappings


def main():
    mappings = map_zw_to_atlas()

    print("# Atlas Panel Mapping\n")
    print(f"| ZW Panel | Atlas Panel(s) | Score |")
    print(f"|----------|---------------|-------|")

    for m in mappings:
        names = ", ".join(f"{n}: {ATLAS_PANELS[n]['name']}" for n in m["atlas_panels"])
        top_score = max(m["scores"].values()) if m["scores"] else 0
        print(f"| {m['zw_id']} | {names} | {top_score} |")

    # Write JSON mapping
    output = REPO / "corpus" / "atlas-mapping.json"
    output.write_text(json.dumps(mappings, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWritten to {output}")


if __name__ == "__main__":
    main()
