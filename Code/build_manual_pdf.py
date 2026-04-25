#!/usr/bin/env python3
"""Generate a readable PDF manual from the Markdown source using ReportLab."""

import re
import textwrap
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable


# ── Colours ──────────────────────────────────────────────────────────────────
WINE       = HexColor("#722F37")
DARK_WINE  = HexColor("#4A1A20")
CREAM      = HexColor("#FDF8F0")
LIGHT_GREY = HexColor("#F5F0E8")
MID_GREY   = HexColor("#E8E0D4")
TEXT_DARK  = HexColor("#2C2218")
TEXT_MED   = HexColor("#5C4F3D")
CODE_BG    = HexColor("#F0EBE1")
CODE_BORDER= HexColor("#D4C9B8")
TABLE_HEAD = HexColor("#722F37")
TABLE_ALT  = HexColor("#FAF5ED")
LINK_COLOR = HexColor("#8B4049")


# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    ss = getSampleStyleSheet()

    body = ParagraphStyle(
        "Body", parent=ss["Normal"],
        fontName="Helvetica", fontSize=10, leading=14.5,
        textColor=TEXT_DARK, alignment=TA_JUSTIFY,
        spaceAfter=6, spaceBefore=2,
    )
    h1 = ParagraphStyle(
        "H1", parent=body,
        fontName="Helvetica-Bold", fontSize=18, leading=22,
        textColor=WINE, spaceBefore=28, spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "H2", parent=body,
        fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=DARK_WINE, spaceBefore=20, spaceAfter=8,
    )
    h3 = ParagraphStyle(
        "H3", parent=body,
        fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=TEXT_DARK, spaceBefore=14, spaceAfter=6,
    )
    bullet = ParagraphStyle(
        "Bullet", parent=body,
        bulletFontName="Helvetica", bulletFontSize=10,
        leftIndent=18, bulletIndent=6,
        spaceBefore=2, spaceAfter=2,
    )
    code_inline = ParagraphStyle(
        "CodeInline", parent=body,
        fontName="Courier", fontSize=9, leading=12,
        textColor=TEXT_DARK,
    )
    code_block = ParagraphStyle(
        "CodeBlock", parent=body,
        fontName="Courier", fontSize=8.5, leading=12,
        textColor=TEXT_DARK, alignment=TA_LEFT,
        leftIndent=12, rightIndent=12,
        spaceBefore=6, spaceAfter=6,
        backColor=CODE_BG,
    )
    title_style = ParagraphStyle(
        "TitleStyle", parent=body,
        fontName="Helvetica-Bold", fontSize=26, leading=32,
        textColor=WINE, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=4,
    )
    subtitle = ParagraphStyle(
        "Subtitle", parent=body,
        fontName="Helvetica", fontSize=12, leading=16,
        textColor=TEXT_MED, alignment=TA_CENTER,
        spaceBefore=4, spaceAfter=4,
    )
    footer_style = ParagraphStyle(
        "Footer", parent=body,
        fontName="Helvetica", fontSize=8, leading=10,
        textColor=TEXT_MED, alignment=TA_CENTER,
    )
    toc_entry = ParagraphStyle(
        "TOCEntry", parent=body,
        fontName="Helvetica", fontSize=10.5, leading=16,
        textColor=TEXT_DARK, leftIndent=0, spaceAfter=1, spaceBefore=1,
    )
    toc_sub = ParagraphStyle(
        "TOCSub", parent=toc_entry,
        fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=TEXT_MED, leftIndent=16,
    )

    return dict(
        body=body, h1=h1, h2=h2, h3=h3, bullet=bullet,
        code_inline=code_inline, code_block=code_block,
        title=title_style, subtitle=subtitle, footer=footer_style,
        toc_entry=toc_entry, toc_sub=toc_sub,
    )


# ── Utilities ────────────────────────────────────────────────────────────────
def esc(text):
    """Escape XML entities for ReportLab Paragraph."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def md_inline(text):
    """Convert inline Markdown (bold, italic, code, links) to ReportLab XML."""
    # Protect code spans: replace with placeholders before bold/italic
    code_spans = []
    def _save_code(m):
        idx = len(code_spans)
        code_spans.append(f'<font name="Courier" size="9" color="#5C4F3D">{m.group(1)}</font>')
        return f'\x00CODE{idx}\x00'
    text = re.sub(r'`([^`]+)`', _save_code, text)
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Links [text](url) → just text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Restore code spans
    for idx, span in enumerate(code_spans):
        text = text.replace(f'\x00CODE{idx}\x00', span)
    return text


class WineRule(Flowable):
    """A thin decorative rule in wine colour."""
    def __init__(self, width, thickness=0.75):
        super().__init__()
        self.width = width
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(WINE)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

    def wrap(self, aW, aH):
        self.width = min(self.width, aW)
        return (self.width, self.thickness + 2)


# ── Page template callbacks ──────────────────────────────────────────────────
def on_first_page(canvas, doc):
    canvas.saveState()
    # Thin wine stripe at top
    canvas.setFillColor(WINE)
    canvas.rect(0, A4[1] - 6*mm, A4[0], 6*mm, fill=1, stroke=0)
    canvas.restoreState()


def on_later_pages(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header line
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, h - 14*mm, w - 20*mm, h - 14*mm)
    # Header text
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(TEXT_MED)
    canvas.drawString(20*mm, h - 12.5*mm, "Manual de Instruções — Iconocracia")
    canvas.drawRightString(w - 20*mm, h - 12.5*mm, "PPGD/UFSC · 2026")
    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(TEXT_MED)
    canvas.drawCentredString(w / 2, 12*mm, f"— {doc.page} —")
    canvas.restoreState()


# ── Parse and build ──────────────────────────────────────────────────────────
def parse_md_to_flowables(md_text, styles):
    """Convert Markdown text to a list of ReportLab flowables."""
    lines = md_text.split("\n")
    flowables = []
    i = 0
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    page_width = A4[0] - 40*mm  # available text width

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            in_table = False
            return
        # Build table
        ncols = len(table_rows[0])
        col_width = page_width / ncols
        col_widths = [col_width] * ncols

        # Convert to Paragraphs
        data = []
        for ri, row in enumerate(table_rows):
            pstyle = ParagraphStyle(
                "TC", parent=styles["body"],
                fontSize=8.5, leading=11.5,
                textColor=white if ri == 0 else TEXT_DARK,
                fontName="Helvetica-Bold" if ri == 0 else "Helvetica",
                alignment=TA_LEFT,
            )
            data.append([Paragraph(md_inline(esc(cell.strip())), pstyle) for cell in row])

        t = Table(data, colWidths=col_widths, repeatRows=1)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.4, MID_GREY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, TABLE_ALT]),
        ]
        t.setStyle(TableStyle(style_cmds))
        flowables.append(Spacer(1, 4))
        flowables.append(t)
        flowables.append(Spacer(1, 6))
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

        # ── Code blocks ──
        if line.strip().startswith("```"):
            if in_code_block:
                # End code block
                code_text = "\n".join(code_lines)
                if code_text.strip():
                    flowables.append(Spacer(1, 4))
                    pre = Preformatted(code_text, styles["code_block"])
                    flowables.append(pre)
                    flowables.append(Spacer(1, 4))
                code_lines = []
                in_code_block = False
            else:
                if in_table:
                    flush_table()
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(esc(line))
            i += 1
            continue

        stripped = line.strip()

        # ── Blank line ──
        if not stripped:
            if in_table:
                flush_table()
            i += 1
            continue

        # ── Horizontal rule ──
        if stripped in ("---", "***", "___"):
            if in_table:
                flush_table()
            flowables.append(Spacer(1, 6))
            flowables.append(WineRule(page_width))
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # ── Table rows ──
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Skip separator rows (|---|---|)
            if all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue
            if not in_table:
                in_table = True
            table_rows.append(cells)
            i += 1
            continue

        if in_table:
            flush_table()

        # ── Headings ──
        m = re.match(r'^(#{1,3})\s+(.+)$', stripped)
        if m:
            level = len(m.group(1))
            text = md_inline(esc(m.group(2)))
            style_key = {1: "h1", 2: "h2", 3: "h3"}[level]
            flowables.append(Paragraph(text, styles[style_key]))
            i += 1
            continue

        # ── Bullet/list ──
        m = re.match(r'^[-*]\s+(.+)$', stripped)
        if m:
            text = md_inline(esc(m.group(1)))
            flowables.append(
                Paragraph(f'<bullet>&bull;</bullet>{text}', styles["bullet"])
            )
            i += 1
            continue

        # ── Numbered list ──
        m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m:
            num = m.group(1)
            text = md_inline(esc(m.group(2)))
            flowables.append(
                Paragraph(f'<bullet>{num}.</bullet>{text}', styles["bullet"])
            )
            i += 1
            continue

        # ── Blockquote ──
        if stripped.startswith(">"):
            text = md_inline(esc(stripped.lstrip("> ")))
            bq_style = ParagraphStyle(
                "BQ", parent=styles["body"],
                leftIndent=20, textColor=TEXT_MED,
                fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
            )
            flowables.append(Paragraph(text, bq_style))
            i += 1
            continue

        # ── Normal paragraph ──
        # Gather continuation lines
        para_lines = [stripped]
        while i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if (not next_line or next_line.startswith("#") or
                next_line.startswith("```") or next_line.startswith("|") or
                next_line.startswith("- ") or next_line.startswith("* ") or
                re.match(r'^\d+\.\s', next_line) or
                next_line in ("---", "***", "___")):
                break
            para_lines.append(next_line)
            i += 1

        text = md_inline(esc(" ".join(para_lines)))
        flowables.append(Paragraph(text, styles["body"]))
        i += 1

    if in_table:
        flush_table()

    return flowables


def build_cover(styles):
    """Build cover page flowables."""
    elements = []
    elements.append(Spacer(1, 60*mm))
    elements.append(Paragraph("ICONOCRACIA", styles["title"]))
    elements.append(Spacer(1, 4))
    elements.append(WineRule(120*mm))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        "Manual de Instruções do Repositório",
        styles["subtitle"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Alegoria Feminina na História da Cultura Jurídica (Séc. XIX–XX)",
        ParagraphStyle("SubSub", parent=styles["subtitle"],
                       fontSize=10, leading=14, textColor=TEXT_MED)
    ))
    elements.append(Spacer(1, 30*mm))
    elements.append(WineRule(60*mm))
    elements.append(Spacer(1, 8))

    info_style = ParagraphStyle("Info", parent=styles["body"],
                                alignment=TA_CENTER, fontSize=10,
                                textColor=TEXT_MED, leading=15)
    elements.append(Paragraph("Ana Vanzin", info_style))
    elements.append(Paragraph("PPGD/UFSC", info_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Versão 1.0 — Março 2026", info_style))

    elements.append(PageBreak())
    return elements


def build_toc(styles):
    """Build a simple table of contents page."""
    elements = []
    elements.append(Paragraph("Sumário", styles["h1"]))
    elements.append(Spacer(1, 8))

    toc_items = [
        ("1.", "Visão geral do projeto", False),
        ("2.", "Pré-requisitos e instalação", False),
        ("3.", "Mapa do repositório", False),
        ("4.", "Fluxos de trabalho diários", False),
        ("", "4.1  Catalogar uma imagem no corpus", True),
        ("", "4.2  Codificar indicadores de purificação", True),
        ("", "4.3  Escrever um capítulo da tese", True),
        ("", "4.4  Compilar capítulos para DOCX/PDF", True),
        ("", "4.5  Explorar o corpus pelo dashboard", True),
        ("", "4.6  Criar nota de pesquisa", True),
        ("5.", "Pipeline de dados", False),
        ("6.", "Scripts disponíveis", False),
        ("7.", "Esquemas e validação", False),
        ("8.", "Notebooks de análise", False),
        ("9.", "Convenções e boas práticas", False),
        ("10.", "Decisões arquiteturais (ADRs)", False),
        ("11.", "Resolução de problemas", False),
    ]

    for num, title, is_sub in toc_items:
        s = styles["toc_sub"] if is_sub else styles["toc_entry"]
        prefix = f"<b>{num}</b>  " if num else ""
        elements.append(Paragraph(f"{prefix}{title}", s))

    elements.append(PageBreak())
    return elements


def main():
    repo = Path("/home/user/iconocracy-corpus")
    md_path = repo / "docs" / "MANUAL.md"
    out_path = repo / "docs" / "MANUAL_Iconocracia.pdf"

    md_text = md_path.read_text(encoding="utf-8")

    # Remove the markdown TOC section (we build our own)
    md_text = re.sub(
        r'## Sumário\n.*?(?=\n---|\n## )', '', md_text, flags=re.DOTALL
    )
    # Remove the first title line and version/author lines (cover handles it)
    md_text = re.sub(r'^# Manual de Instruções.*\n', '', md_text)
    md_text = re.sub(r'^\*\*Versão:\*\*.*\n', '', md_text)
    md_text = re.sub(r'^\*\*Autora:\*\*.*\n', '', md_text)

    styles = make_styles()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        topMargin=20*mm,
        bottomMargin=20*mm,
        leftMargin=20*mm,
        rightMargin=20*mm,
        title="Manual de Instruções — Iconocracia",
        author="Ana Vanzin — PPGD/UFSC",
        subject="Repositório de pesquisa doutoral",
    )

    elements = []
    elements.extend(build_cover(styles))
    elements.extend(build_toc(styles))
    elements.extend(parse_md_to_flowables(md_text, styles))

    # Final page: colophon
    elements.append(Spacer(1, 20*mm))
    elements.append(WineRule(A4[0] - 40*mm))
    elements.append(Spacer(1, 6))
    colophon = ParagraphStyle("Colophon", parent=styles["body"],
                              alignment=TA_CENTER, fontSize=8.5,
                              textColor=TEXT_MED, leading=12)
    elements.append(Paragraph(
        "Manual gerado em 23 de março de 2026.", colophon
    ))
    elements.append(Paragraph(
        "Iconocracia — github.com/anavvanzin/iconocracy-corpus", colophon
    ))

    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF gerado: {out_path}")
    print(f"Páginas: abra o arquivo para conferir.")


if __name__ == "__main__":
    main()
