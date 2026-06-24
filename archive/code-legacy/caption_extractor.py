"""
Extract captions and figure mentions from OCR text.

Targets common patterns in Portuguese, Spanish, French, and Italian
legal/institutional documents:
  - "Figura 1 — ...", "Fig. 2:", "Figure 3."
  - "Ilustração", "Gravura", "Estampa", "Imagem"
  - "Fotografia", "Prancha", "Lâmina"
  - "Illustration", "Planche", "Tavola", "Lámina"
  - Captions in parentheses after figure references
"""

import re
from dataclasses import dataclass


@dataclass
class CaptionMatch:
    """A single extracted caption or figure mention."""
    page_number: int
    match_type: str       # "figure_ref" | "caption" | "image_credit"
    label: str            # e.g. "Figura 3", "Fig. 2"
    text: str             # the full caption text
    start_pos: int        # character position in page text


# ── Patterns ─────────────────────────────────────────────────────────────────

# Figure/illustration labels across PT, ES, FR, IT, EN
_FIGURE_LABELS = (
    r"(?:Fig(?:ura)?|Figure|Illustration|Ilustra[cç][aã]o|Gravura|Estampa|"
    r"Imagem|Fotografia|Prancha|L[aâ]mina|Planche|Tavola|"
    r"L[áa]mina|Grabado|Quadro|Tabela|Table|Tableau)"
)

# Main pattern: Label + number + separator + caption text (up to end of sentence)
_FIGURE_PATTERN = re.compile(
    rf"({_FIGURE_LABELS})"                # group 1: label word
    r"\.?\s*"                              # optional period + space
    r"((?:n[°ºo.]?\s*)?\d+[a-zA-Z]?)"     # group 2: number (e.g. "3", "nº 4", "2a")
    r"\s*[:\.\-–—]\s*"                     # separator
    r"(.+?)(?:\.|$)",                      # group 3: caption text until period or EOL
    re.IGNORECASE | re.MULTILINE,
)

# Broader pattern: just detect figure references even without full caption
_FIGURE_REF_PATTERN = re.compile(
    rf"({_FIGURE_LABELS})"
    r"\.?\s*"
    r"((?:n[°ºo.]?\s*)?\d+[a-zA-Z]?)",
    re.IGNORECASE,
)

# Image credits: "Fonte:", "Source:", "Acervo:", "Crédito:", etc.
_CREDIT_PATTERN = re.compile(
    r"(Fonte|Source|Fuente|Acervo|Cr[eé]dito|Collection|Coll\.|"
    r"Arquivo|Archive|Archiv[eo])\s*:\s*(.+?)(?:\.|$)",
    re.IGNORECASE | re.MULTILINE,
)

# Parenthetical descriptions that often accompany figures
_PAREN_CAPTION = re.compile(
    r"\("
    r"((?:óleo|aquarela|gravura|litografia|fotografia|detalhe|"
    r"oil|watercolor|engraving|lithograph|photograph|detail|"
    r"huile|gravure|lithographie|photographie|détail|"
    r"olio|incisione|litografia|fotografia|dettaglio)"
    r".+?)"
    r"\)",
    re.IGNORECASE,
)


def extract_captions(text: str, page_number: int = 1) -> list[CaptionMatch]:
    """
    Extract all caption/figure mentions from a page's OCR text.
    Returns list of CaptionMatch objects.
    """
    matches = []
    seen_positions: set[int] = set()  # avoid duplicates

    # 1. Full captions (label + number + text)
    for m in _FIGURE_PATTERN.finditer(text):
        if m.start() not in seen_positions:
            seen_positions.add(m.start())
            matches.append(CaptionMatch(
                page_number=page_number,
                match_type="caption",
                label=f"{m.group(1)} {m.group(2)}".strip(),
                text=m.group(3).strip(),
                start_pos=m.start(),
            ))

    # 2. Figure references without full caption
    for m in _FIGURE_REF_PATTERN.finditer(text):
        if m.start() not in seen_positions:
            seen_positions.add(m.start())
            matches.append(CaptionMatch(
                page_number=page_number,
                match_type="figure_ref",
                label=f"{m.group(1)} {m.group(2)}".strip(),
                text="",
                start_pos=m.start(),
            ))

    # 3. Image credits
    for m in _CREDIT_PATTERN.finditer(text):
        if m.start() not in seen_positions:
            seen_positions.add(m.start())
            matches.append(CaptionMatch(
                page_number=page_number,
                match_type="image_credit",
                label=m.group(1).strip(),
                text=m.group(2).strip(),
                start_pos=m.start(),
            ))

    # 4. Parenthetical technique/medium descriptions
    for m in _PAREN_CAPTION.finditer(text):
        if m.start() not in seen_positions:
            seen_positions.add(m.start())
            matches.append(CaptionMatch(
                page_number=page_number,
                match_type="caption",
                label="(medium/technique)",
                text=m.group(1).strip(),
                start_pos=m.start(),
            ))

    return sorted(matches, key=lambda c: c.start_pos)


def extract_captions_from_pages(
    pages: list[tuple[int, str]],
) -> list[CaptionMatch]:
    """
    Extract captions from multiple pages.
    pages: list of (page_number, text) tuples.
    """
    all_captions = []
    for page_num, text in pages:
        all_captions.extend(extract_captions(text, page_number=page_num))
    return all_captions


def captions_to_text(captions: list[CaptionMatch]) -> str:
    """Format extracted captions as readable text for saving."""
    if not captions:
        return "No captions or figure references found.\n"

    lines = []
    for c in captions:
        prefix = f"[p.{c.page_number}] [{c.match_type}]"
        if c.text:
            lines.append(f"{prefix} {c.label}: {c.text}")
        else:
            lines.append(f"{prefix} {c.label}")
    return "\n".join(lines) + "\n"
