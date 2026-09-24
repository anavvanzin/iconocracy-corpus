import pytest

from tools.scripts.support_harmonization import (
    SupportHarmonizationError,
    frequency_counts,
    harmonize_candidates,
    harmonize_support,
)


def test_normalizes_and_preserves_raw_value():
    result = harmonize_support("  CÉDULA  ", "corpus/corpus-data.json")
    assert result["support_raw"] == "  CÉDULA  "
    assert result["support_stratum"] == "papel_moeda"
    assert result["support_family"] == "circulacao_monetaria"
    assert result["support_harmonization_version"] == "1.0.0"


@pytest.mark.parametrize("raw", ["?", None, "estampa/gravura", "moeda e selo", "cerâmica"])
def test_rejects_values_that_require_manual_adjudication(raw):
    with pytest.raises(SupportHarmonizationError):
        harmonize_support(raw, "corpus/corpus-data.json")


def test_batch_fails_before_sampling_if_any_candidate_is_rejected():
    candidates = [
        {"item_id": "OK", "support": "moeda", "support_source": "corpus/corpus-data.json"},
        {"item_id": "REVIEW", "support": "?", "support_source": "corpus/corpus-data.json"},
    ]
    with pytest.raises(SupportHarmonizationError, match="REVIEW"):
        harmonize_candidates(candidates)


def test_frequency_report_includes_zero_categories():
    candidates = harmonize_candidates([
        {"item_id": "A", "support": "moeda", "support_source": "corpus/corpus-data.json"},
        {"item_id": "B", "support": "coin", "support_source": "corpus/corpus-data.json"},
    ])
    report = frequency_counts(candidates)
    assert report["support_stratum"]["moeda"] == 2
    assert report["support_stratum"]["selo"] == 0


@pytest.mark.parametrize(
    ("raw", "stratum"),
    [("moeda", "moeda"), ("selo", "selo"), ("escultura", "escultura"), ("papel-moeda", "papel_moeda")],
)
def test_accepts_real_corpus_values_that_contain_the_letter_e(raw, stratum):
    """Regressão do gate rejeitando 291 de 336 itens do corpus.

    O marcador de composição " e " perdia os espaços na normalização e virava a letra
    "e"; todo suporte que a contivesse era rejeitado como composto — moeda (85 itens),
    selo, escultura. Os fixtures anteriores não pegavam isso: o único caso positivo era
    CÉDULA, sem "e" simples.
    """
    result = harmonize_support(raw, "corpus/corpus-data.json")
    assert result["support_stratum"] == stratum


@pytest.mark.parametrize(
    "raw",
    ["estampa/gravura", "monumento/escultura", "Moedas e cédulas", "selo and coin", "e moeda", "moeda e"],
)
def test_still_rejects_genuinely_composite_values(raw):
    """Os bloqueios legítimos ficam: barra, ' e ' e ' and ' entre palavras, nas pontas inclusive."""
    with pytest.raises(SupportHarmonizationError, match="composite"):
        harmonize_support(raw, "corpus/corpus-data.json")
