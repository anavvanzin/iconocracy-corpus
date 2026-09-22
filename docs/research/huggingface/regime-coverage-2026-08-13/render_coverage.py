#!/usr/bin/env python3
"""Render the public Hugging Face regime-coverage snapshot as SVG."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "coverage.csv"
PENDING_INPUT = HERE / "tmp_coverage.csv"
OUTPUT = HERE / "coverage.svg"

WIDTH = 1440
HEIGHT = 900
BAR_X = 350
BAR_WIDTH = 900
BAR_HEIGHT = 54
MAX_TOTAL = 163

COLORS = {
    "background": "#FAF6EC",
    "ink": "#1C1C1C",
    "muted": "#6B6459",
    "coded": "#6B1E2E",
    "pending": "#E8D4D7",
    "gold": "#B8892B",
    "grid": "#D8CCB9",
}

LABELS = {
    "fundacional": "Fundacional",
    "normativo": "Normativo",
    "militar": "Militar",
    "contra-alegoria": "Contra-alegoria",
}


def load_rows(path: Path = INPUT) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "regime",
        "total_items",
        "coded_items",
        "pending_items",
        "coverage_pct",
    }
    if not rows or set(rows[0]) != required:
        raise SystemExit(f"Unexpected columns in {path.name}: {rows[0].keys() if rows else 'empty'}")
    if sum(int(row["total_items"]) for row in rows) != 335:
        raise SystemExit(f"Unexpected corpus total in {path.name}")
    if sum(int(row["coded_items"]) for row in rows) != 286:
        raise SystemExit(f"Unexpected purification total in {path.name}")
    if any(
        int(row["coded_items"]) + int(row["pending_items"]) != int(row["total_items"])
        for row in rows
    ):
        raise SystemExit(f"Inconsistent coverage arithmetic in {path.name}")
    return rows


def pct_pt(value: str) -> str:
    return value.replace(".", ",") + "%"


def render(rows: list[dict[str, str]]) -> str:
    svg: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
            'role="img" aria-labelledby="title desc">'
        ),
        '<title id="title">Cobertura de codificação por regime iconocrático</title>',
        (
            '<desc id="desc">Barras horizontais empilhadas mostram itens codificados e '
            'pendentes nos regimes fundacional, normativo, militar e contra-alegoria.</desc>'
        ),
        '<style>',
        '  .serif { font-family: Gentium, Georgia, serif; }',
        '  .sans { font-family: Inter, Helvetica, Arial, sans-serif; }',
        '  .mono { font-family: "DejaVu Sans Mono", Menlo, monospace; }',
        '</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS["background"]}"/>',
        (
            f'<text id="chart-title" x="80" y="78" class="serif" font-size="38" '
            f'font-weight="700" fill="{COLORS["ink"]}">Cobertura de codificação por regime</text>'
        ),
        (
            f'<text x="80" y="116" class="sans" font-size="19" fill="{COLORS["muted"]}">'
            'Corpus público: 335 itens · purification: 286 observações · 49 pendências</text>'
        ),
        f'<line x1="80" y1="140" x2="670" y2="140" stroke="{COLORS["gold"]}" stroke-width="2"/>',
        (
            f'<text x="1360" y="76" text-anchor="end" class="serif" font-size="32" '
            f'fill="{COLORS["coded"]}">❋</text>'
        ),
        (
            f'<text x="1360" y="108" text-anchor="end" class="mono" font-size="12" '
            f'fill="{COLORS["muted"]}">ICONOCRACIA · 2026-08-13</text>'
        ),
        (
            f'<rect x="870" y="157" width="20" height="20" rx="2" fill="{COLORS["coded"]}"/>'
            f'<text x="900" y="173" class="sans" font-size="14" fill="{COLORS["ink"]}">Codificado</text>'
        ),
        (
            f'<rect x="1025" y="157" width="20" height="20" rx="2" fill="{COLORS["pending"]}" '
            f'stroke="{COLORS["muted"]}" stroke-width="1"/>'
            f'<text x="1055" y="173" class="sans" font-size="14" fill="{COLORS["ink"]}">Pendente</text>'
        ),
    ]

    for tick in (0, 40, 80, 120, 160):
        x = BAR_X + (tick / MAX_TOTAL) * BAR_WIDTH
        svg.extend(
            [
                f'<line x1="{x:.1f}" y1="205" x2="{x:.1f}" y2="690" stroke="{COLORS["grid"]}" stroke-width="1"/>',
                (
                    f'<text x="{x:.1f}" y="716" text-anchor="middle" class="mono" '
                    f'font-size="12" fill="{COLORS["muted"]}">{tick}</text>'
                ),
            ]
        )

    start_y = 235
    gap = 112
    for index, row in enumerate(rows):
        y = start_y + index * gap
        total = int(row["total_items"])
        coded = int(row["coded_items"])
        pending = int(row["pending_items"])
        total_width = total / MAX_TOTAL * BAR_WIDTH
        coded_width = coded / MAX_TOTAL * BAR_WIDTH
        pending_width = pending / MAX_TOTAL * BAR_WIDTH
        label = escape(LABELS.get(row["regime"], row["regime"]))
        coverage = pct_pt(row["coverage_pct"])
        coded_label = str(coded) if coded_width < 140 else f"{coded} codificados"

        svg.extend(
            [
                (
                    f'<text x="320" y="{y + 34}" text-anchor="end" class="serif" '
                    f'font-size="22" fill="{COLORS["ink"]}">{label}</text>'
                ),
                (
                    f'<rect x="{BAR_X}" y="{y}" width="{total_width:.1f}" height="{BAR_HEIGHT}" '
                    f'rx="5" fill="{COLORS["pending"]}" stroke="{COLORS["muted"]}" stroke-width="1"/>'
                ),
                (
                    f'<path d="M {BAR_X + 5} {y} H {BAR_X + coded_width:.1f} '
                    f'V {y + BAR_HEIGHT} H {BAR_X + 5} Q {BAR_X} {y + BAR_HEIGHT} '
                    f'{BAR_X} {y + BAR_HEIGHT - 5} V {y + 5} Q {BAR_X} {y} {BAR_X + 5} {y} Z" '
                    f'fill="{COLORS["coded"]}"/>'
                ),
                (
                    f'<text x="{BAR_X + 14}" y="{y + 34}" class="mono" font-size="14" '
                    f'fill="#FFFFFF">{coded_label}</text>'
                ),
                (
                    f'<text x="{BAR_X + total_width + 18:.1f}" y="{y + 25}" class="mono" '
                    f'font-size="14" font-weight="700" fill="{COLORS["ink"]}">{coverage}</text>'
                ),
                (
                    f'<text x="{BAR_X + total_width + 18:.1f}" y="{y + 45}" class="sans" '
                    f'font-size="12" fill="{COLORS["muted"]}">{pending} pendentes · n={total}</text>'
                ),
            ]
        )

    svg.extend(
        [
            (
                f'<text x="{BAR_X + BAR_WIDTH / 2}" y="750" text-anchor="middle" class="sans" '
                f'font-size="14" fill="{COLORS["muted"]}">Itens históricos</text>'
            ),
            f'<line x1="80" y1="790" x2="1360" y2="790" stroke="{COLORS["gold"]}" stroke-width="1"/>',
            (
                f'<text x="80" y="822" class="sans" font-size="13" fill="{COLORS["ink"]}">'
                '<tspan font-weight="700">Leitura:</tspan> o regime militar concentra 26 das 49 pendências '
                'e tem a menor cobertura (51,9%).</text>'
            ),
            (
                f'<text x="80" y="850" class="sans" font-size="12" fill="{COLORS["muted"]}">'
                'Fonte: Hugging Face Dataset Viewer · warholana/iconocracy-corpus · configs corpus e purification. '
                'Comparação agregada por regime; sem join item a item.</text>'
            ),
            '</svg>',
        ]
    )
    return "\n".join(svg) + "\n"


def main() -> None:
    if PENDING_INPUT.exists():
        load_rows(PENDING_INPUT)
        PENDING_INPUT.replace(INPUT)
        print(f"Promoted {PENDING_INPUT.name} to {INPUT.name}")
    rows = load_rows()
    OUTPUT.write_text(render(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
