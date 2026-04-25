"""Tests for corpus_bridge module."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.corpus_bridge import (
    csv_row_to_corpus_item,
    get_existing_ids,
    get_existing_hashes,
    humanize_filename,
    next_id_for_country,
)


def test_humanize_filename_standard():
    assert humanize_filename("BND_1891_0001_constituicao-federal.pdf") == "Constituicao Federal"


def test_humanize_filename_short():
    assert humanize_filename("doc.pdf") == "Doc"


def test_next_id_for_country_empty():
    assert next_id_for_country("BR", set()) == "BR-001"


def test_next_id_for_country_continues():
    existing = {"BR-001", "BR-002", "BR-005", "FR-001"}
    assert next_id_for_country("BR", existing) == "BR-006"
    assert next_id_for_country("FR", existing) == "FR-002"


def test_next_id_for_country_new():
    existing = {"BR-001", "FR-010"}
    assert next_id_for_country("DE", existing) == "DE-001"


def test_get_existing_ids():
    corpus = [{"id": "BR-001"}, {"id": "FR-001"}]
    assert get_existing_ids(corpus) == {"BR-001", "FR-001"}


def test_get_existing_hashes():
    corpus = [
        {"id": "BR-001", "ingest_metadata": {"file_id": "abc123"}},
        {"id": "FR-001"},  # no ingest_metadata
    ]
    assert get_existing_hashes(corpus) == {"abc123"}


def test_csv_row_to_corpus_item_basic():
    row = {
        "file_id": "deadbeef",
        "original_filename": "test.pdf",
        "renamed_filename": "BND_1891_0001_constituicao.pdf",
        "source_institution": "BND",
        "detected_language": "pt",
        "ocr_language_used": "por",
        "total_pages": "10",
        "mean_confidence": "75.3",
        "min_confidence": "42.1",
        "low_conf_pages": "3,7",
        "caption_count": "2",
        "has_figures": "True",
        "year_detected": "1891",
        "ingestion_timestamp": "2026-04-03T12:00:00Z",
        "input_folder": "/batch/bnd",
        "notes": "",
    }
    item = csv_row_to_corpus_item(row, "BR-012", "BR")

    assert item["id"] == "BR-012"
    assert item["year"] == 1891
    assert item["country"] == "Brazil"
    assert item["country_pt"] == "Brasil"
    assert item["institution"] == "Biblioteca Nacional Digital"
    assert item["in_scope"] is True
    assert item["indicadores"]["desincorporacao"] == 0
    assert item["panofsky"]["iconographic"]["iconclass"] == []

    meta = item["ingest_metadata"]
    assert meta["file_id"] == "deadbeef"
    assert meta["mean_confidence"] == 75.3
    assert meta["has_figures"] is True
    assert meta["total_pages"] == 10


def test_csv_row_to_corpus_item_no_year():
    row = {
        "file_id": "abc",
        "original_filename": "mystery.tiff",
        "renamed_filename": "UNKNOWN_0000_0001_mystery.tiff",
        "source_institution": "UNKNOWN",
        "detected_language": "und",
        "ocr_language_used": "por+eng",
        "total_pages": "1",
        "mean_confidence": "30.0",
        "min_confidence": "30.0",
        "low_conf_pages": "1",
        "caption_count": "0",
        "has_figures": "False",
        "year_detected": "",
        "ingestion_timestamp": "2026-04-03T12:00:00Z",
        "input_folder": "/batch/unknown",
        "notes": "low quality scan",
    }
    item = csv_row_to_corpus_item(row, "EU-001", "EU")

    assert item["year"] is None
    assert item["date"] == ""
    assert item["country"] == "Europe"
    assert item["ingest_metadata"]["has_figures"] is False
    assert item["ingest_metadata"]["notes"] == "low quality scan"


def test_corpus_item_has_all_required_fields():
    """Ensure skeleton items have all fields present in existing corpus items."""
    row = {
        "file_id": "x",
        "original_filename": "f.pdf",
        "renamed_filename": "BND_1900_0001_f.pdf",
        "source_institution": "BND",
        "detected_language": "pt",
        "ocr_language_used": "por",
        "total_pages": "1",
        "mean_confidence": "80",
        "min_confidence": "80",
        "low_conf_pages": "",
        "caption_count": "0",
        "has_figures": "False",
        "year_detected": "1900",
        "ingestion_timestamp": "2026-01-01T00:00:00Z",
        "input_folder": "/x",
        "notes": "",
    }
    item = csv_row_to_corpus_item(row, "BR-099", "BR")

    required_fields = [
        "id", "title", "date", "period", "creator", "institution",
        "source_archive", "country", "medium", "motif", "description",
        "url", "thumbnail_url", "rights", "citation_abnt", "citation_chicago",
        "tags", "year", "medium_norm", "country_pt", "period_norm",
        "motif_str", "tags_str", "regime", "endurecimento_score",
        "indicadores", "coded_by", "coded_at", "support", "in_scope",
        "scope_note", "panofsky",
    ]
    for field in required_fields:
        assert field in item, f"Missing field: {field}"
