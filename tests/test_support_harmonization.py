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
