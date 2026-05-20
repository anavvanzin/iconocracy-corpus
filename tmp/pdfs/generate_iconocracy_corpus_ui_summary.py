from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path("/Users/ana/iconocracy-corpus")
CORPUS_DIR = ROOT / "corpus"
OUTPUT_PDF = ROOT / "output" / "pdf" / "iconocracy-corpus-ui-summary.pdf"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def wrap_lines(text: str, font_name: str, font_size: float, width: float) -> list[str]:
    return simpleSplit(text, font_name, font_size, width)


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font_name: str,
    font_size: float,
    color=black,
    leading: float | None = None,
) -> float:
    leading = leading or (font_size * 1.3)
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    lines = wrap_lines(text, font_name, font_size, width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_bullets(
    c: canvas.Canvas,
    bullets: list[str],
    x: float,
    y: float,
    width: float,
    font_name: str = "Helvetica",
    font_size: float = 8.6,
    bullet_gap: float = 10,
    leading: float = 11.2,
) -> float:
    text_width = width - bullet_gap
    for bullet in bullets:
        lines = wrap_lines(bullet, font_name, font_size, text_width)
        if not lines:
            continue
        c.setFont(font_name, font_size)
        c.setFillColor(black)
        c.drawString(x, y, "-")
        c.drawString(x + bullet_gap, y, lines[0])
        y -= leading
        for line in lines[1:]:
            c.drawString(x + bullet_gap, y, line)
            y -= leading
        y -= 1.5
    return y


def draw_section(
    c: canvas.Canvas,
    title: str,
    body_lines: list[str],
    x: float,
    y: float,
    width: float,
    title_color,
    body_font_size: float = 8.6,
) -> float:
    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(title_color)
    c.drawString(x, y, title)
    y -= 14
    if body_lines:
        y = draw_bullets(
            c,
            body_lines,
            x,
            y,
            width,
            font_size=body_font_size,
        )
    return y - 4


def collect_evidence() -> dict[str, object]:
    corpus_index = read_text(CORPUS_DIR / "index.html")
    dashboard = read_text(CORPUS_DIR / "DASHBOARD_CORPUS.html")
    atlas = read_text(CORPUS_DIR / "atlas-iconometrico.html")
    corpus_readme = read_text(CORPUS_DIR / "README.md")
    manual = read_text(ROOT / "docs" / "MANUAL.md")
    records = json.loads(read_text(CORPUS_DIR / "corpus-data.json"))

    item_count = len(records)
    count_66_in_docs = (
        "66 items catalogados" in dashboard
        and "66 itens catalogados" in manual
        and "66 catalogued items" in ROOT.joinpath("README.md").read_text(encoding="utf-8")
    )
    count_89_in_repo = "89 catalogued items" in corpus_readme

    atlas_missing = [
        name for name in ("base.css", "style.css", "app.js") if not (CORPUS_DIR / name).exists()
    ]

    corpus_data_link_found = any(
        "corpus-data.json" in text for text in (corpus_index, dashboard, atlas)
    )

    return {
        "item_count": item_count,
        "count_66_in_docs": count_66_in_docs,
        "count_89_in_repo": count_89_in_repo,
        "atlas_missing": atlas_missing,
        "corpus_data_link_found": corpus_data_link_found,
        "uses_chartjs": "chart.js" in dashboard.lower(),
        "uses_react": "react.production.min.js" in atlas.lower(),
        "uses_recharts": "recharts" in atlas.lower(),
        "uses_babel": "@babel/standalone" in atlas.lower(),
        "remote_image_urls": ("thumbnail_url" in dashboard) and ("thumbnail_url" in corpus_index),
    }


def build_pdf() -> None:
    evidence = collect_evidence()
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = A4
    c = canvas.Canvas(str(OUTPUT_PDF), pagesize=A4)

    ink = HexColor("#1F2937")
    slate = HexColor("#475569")
    accent = HexColor("#8B3A1A")
    line = HexColor("#D6D3D1")
    paper = HexColor("#F8F5EF")
    alert = HexColor("#B42318")

    margin = 34
    content_width = page_width - (margin * 2)
    gap = 18
    col_width = (content_width - gap) / 2
    left_x = margin
    right_x = margin + col_width + gap

    header_h = 88
    intro_h = 66

    c.setFillColor(paper)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    c.setFillColor(ink)
    c.rect(0, page_height - header_h, page_width, header_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(margin, page_height - 30, "Iconocracy Corpus UI")
    c.setFont("Helvetica", 9.5)
    c.drawString(
        margin,
        page_height - 46,
        "One-page repo-based summary of the static corpus browser, dashboard, and atlas.",
    )
    draw_wrapped(
        c,
        "Scope: corpus/index.html, DASHBOARD_CORPUS.html, atlas-iconometrico.html",
        margin,
        page_height - 60,
        content_width,
        "Helvetica",
        8.1,
        white,
        9.2,
    )

    intro_top = page_height - header_h - 12
    c.setStrokeColor(line)
    c.setFillColor(white)
    c.roundRect(margin, intro_top - intro_h, content_width, intro_h, 8, fill=1, stroke=1)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 10.2)
    c.drawString(margin + 12, intro_top - 18, "What it is")
    c.setFillColor(ink)
    c.setFont("Helvetica", 8.8)
    intro_text = (
        "A static, browser-based research interface for browsing and analyzing the Iconocracy "
        "corpus of female legal and political allegories. The repo exposes three UI surfaces: "
        "a searchable corpus browser, an analytical dashboard, and an iconometric atlas."
    )
    draw_wrapped(
        c,
        intro_text,
        margin + 12,
        intro_top - 33,
        content_width - 24,
        "Helvetica",
        8.8,
        ink,
        11.4,
    )

    column_top = intro_top - intro_h - 16

    left_y = column_top
    left_y = draw_section(
        c,
        "Who it's for",
        [
            "Primary persona: a legal-history or digital-humanities researcher working with the Iconocracy corpus.",
            "Secondary fit: thesis collaborators reviewing corpus coverage, citations, and comparative visual patterns.",
        ],
        left_x,
        left_y,
        col_width,
        accent,
    )
    left_y -= 4
    left_y = draw_section(
        c,
        "What it does",
        [
            "Searches corpus records across title, description, creator, motifs, tags, institution, country, period, and medium.",
            "Lets users combine pill-based filters for country, period, archive, and motif in the corpus browser.",
            "Shows card-based browsing with thumbnails, placeholders, and detail modals for metadata and provenance.",
            "Copies or exports citations in ABNT and Chicago formats from the corpus UI and dashboard modal views.",
            "Presents dashboard KPIs, filter controls, gallery and table views, sorting, pagination, and six Chart.js charts.",
            "Offers an atlas view with regime filters, image cards, a detail panel, and radar charts for ten iconometric indicators.",
        ],
        left_x,
        left_y,
        col_width,
        accent,
    )

    right_y = column_top
    how_it_works = [
        "The UI is client-side static HTML, CSS, and inline JavaScript; no repo-backed app server is documented for the corpus browser or dashboard.",
        "The dashboard ships its dataset inline in DASHBOARD_CORPUS.html and renders charts with Chart.js loaded from a CDN.",
        "The atlas loads React, ReactDOM, Babel, and Recharts from CDNs, then renders an inline React app from a hard-coded CORPUS array.",
        "Images and thumbnails resolve to external archive or Wikimedia URLs, so network access affects how much media appears at runtime.",
        (
            "Runtime linkage to corpus-data.json: "
            + ("Found in repo." if evidence["corpus_data_link_found"] else "Not found in repo.")
        ),
    ]
    right_y = draw_section(
        c,
        "How it works",
        how_it_works,
        right_x,
        right_y,
        col_width,
        accent,
    )
    right_y -= 4
    right_y = draw_section(
        c,
        "How to run",
        [
            "Open corpus/index.html directly in a browser for the searchable corpus browser.",
            "Open corpus/DASHBOARD_CORPUS.html directly in a browser for the analytical dashboard; docs say no web server is required.",
            "Open corpus/atlas-iconometrico.html directly in a browser for the atlas view; internet is still needed for CDN scripts and remote images.",
        ],
        right_x,
        right_y,
        col_width,
        accent,
    )
    right_y -= 4
    right_y = draw_section(
        c,
        "Evidence gaps",
        [
            (
                "Item count: Inconsistent in repo. corpus/corpus-data.json has "
                f"{evidence['item_count']} items and corpus/README.md states 89, while dashboard and manual copy still state 66."
            ),
            (
                "Atlas support files: "
                + (
                    "Not found in repo: " + ", ".join(evidence["atlas_missing"]) + "."
                    if evidence["atlas_missing"]
                    else "Found in repo."
                )
            ),
        ],
        right_x,
        right_y,
        col_width,
        alert,
        body_font_size=8.4,
    )

    footer_y = 50
    c.setStrokeColor(line)
    c.line(margin, footer_y + 18, page_width - margin, footer_y + 18)
    c.setFillColor(slate)
    c.setFont("Helvetica", 7.6)
    footer = (
        "Evidence checked from corpus/index.html, corpus/DASHBOARD_CORPUS.html, "
        "corpus/atlas-iconometrico.html, corpus/README.md, docs/MANUAL.md, and corpus/corpus-data.json."
    )
    draw_wrapped(c, footer, margin, footer_y + 7, content_width, "Helvetica", 7.6, slate, 9.5)

    c.save()


if __name__ == "__main__":
    build_pdf()
