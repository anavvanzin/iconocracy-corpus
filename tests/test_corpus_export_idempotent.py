"""Tests for corpus export idempotence gate."""

from __future__ import annotations

from tools.scripts.check_corpus_export_idempotent import (
    AUTHORITATIVE_FIELDS,
    diff_authoritative_fields,
)


def _full_generated():
    return {
        "url": "https://example.org/a",
        "title": "Title A",
        "description": "Desc A",
        "motif": ["Liberty"],
        "regime": "normativo",
        "endurecimento_score": 2.1,
        "coded_by": "test",
        "coded_at": "2026-04-07T00:00:00Z",
        "indicadores": {"desincorporacao": 1},
        "citation_abnt": "Citation A",
        "audit_flags": ["flag1"],
    }


def test_no_diff_when_generated_and_existing_match():
    generated = _full_generated()
    existing = dict(generated)
    assert diff_authoritative_fields(generated, existing) == []


def test_diff_reports_changed_authoritative_field():
    generated = _full_generated()
    existing = dict(generated)
    existing["title"] = "Title B"
    diffs = diff_authoritative_fields(generated, existing)
    assert len(diffs) == 1
    assert "title" in diffs[0]


def test_diff_ignores_non_authoritative_extra_field():
    generated = _full_generated()
    existing = dict(generated)
    existing["panofsky"] = {"pre_iconographic": "extra"}
    existing["extra_field"] = "should be ignored"
    assert diff_authoritative_fields(generated, existing) == []


def test_float_tolerance_endurecimento_score():
    generated = _full_generated()
    existing = dict(generated)
    existing["endurecimento_score"] = 1.2000000001
    generated["endurecimento_score"] = 1.2
    assert diff_authoritative_fields(generated, existing) == []


def test_new_id_in_generated_reports_all_fields():
    generated = _full_generated()
    existing = {}
    diffs = diff_authoritative_fields(generated, existing)
    assert len(diffs) == len(AUTHORITATIVE_FIELDS)
    for field, diff_line in zip(AUTHORITATIVE_FIELDS, diffs):
        assert field in diff_line


def test_deleted_id_in_existing_reports_all_fields():
    generated = {}
    existing = _full_generated()
    diffs = diff_authoritative_fields(generated, existing)
    assert len(diffs) == len(AUTHORITATIVE_FIELDS)
    for field, diff_line in zip(AUTHORITATIVE_FIELDS, diffs):
        assert field in diff_line


def test_field_absence_vs_none_distinction():
    generated = _full_generated()
    generated["title"] = None
    del generated["description"]

    existing = _full_generated()
    del existing["title"]
    existing["description"] = None

    diffs = diff_authoritative_fields(generated, existing)
    assert not any("title" in d for d in diffs)
    assert not any("description" in d for d in diffs)
