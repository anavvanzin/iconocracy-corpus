"""Tests for caption_extractor module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.caption_extractor import extract_captions, captions_to_text


def test_portuguese_figure_caption():
    text = "Figura 1 — Alegoria da República, óleo sobre tela."
    caps = extract_captions(text)
    assert len(caps) >= 1
    assert any(c.match_type == "caption" and "Figura 1" in c.label for c in caps)


def test_french_figure_caption():
    text = "Figure 3 : La Liberté guidant le peuple."
    caps = extract_captions(text)
    assert len(caps) >= 1
    assert any("Figure 3" in c.label for c in caps)


def test_abbreviated_fig():
    text = "Fig. 12 - Gravura representando a Justiça."
    caps = extract_captions(text)
    assert len(caps) >= 1
    assert any("Fig" in c.label and "12" in c.label for c in caps)


def test_estampa_label():
    text = "Estampa 5 — Medalha comemorativa da Constituição de 1891."
    caps = extract_captions(text)
    assert len(caps) >= 1


def test_planche_label():
    text = "Planche 2 : Allégorie de la Justice."
    caps = extract_captions(text)
    assert len(caps) >= 1


def test_image_credit():
    text = "Fonte: Acervo da Biblioteca Nacional Digital."
    caps = extract_captions(text)
    assert len(caps) >= 1
    assert any(c.match_type == "image_credit" for c in caps)


def test_source_credit_english():
    text = "Source: Library of Congress, Prints and Photographs Division."
    caps = extract_captions(text)
    assert any(c.match_type == "image_credit" for c in caps)


def test_parenthetical_technique():
    text = "Marianne (óleo sobre tela, 1848)"
    caps = extract_captions(text)
    assert any("medium/technique" in c.label for c in caps)


def test_no_captions_in_plain_text():
    text = "Este documento discute aspectos gerais da legislação brasileira."
    caps = extract_captions(text)
    assert len(caps) == 0


def test_captions_to_text_empty():
    assert "No captions" in captions_to_text([])


def test_captions_to_text_formats():
    text = "Figura 1 — A República. Fonte: BND."
    caps = extract_captions(text, page_number=3)
    result = captions_to_text(caps)
    assert "[p.3]" in result


def test_multiple_captions_on_same_page():
    text = (
        "Figura 1 — Alegoria da República.\n"
        "Figura 2 — Alegoria da Justiça.\n"
        "Fonte: Acervo Nacional."
    )
    caps = extract_captions(text)
    assert len(caps) >= 3
