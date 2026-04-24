"""Tests for corpus export idempotence gate."""

from __future__ import annotations

from tools.scripts.check_corpus_export_idempotent import diff_authoritative_fields


def test_no_diff_when_generated_and_existing_match():
    generated = {
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
    existing = dict(generated)
    assert diff_authoritative_fields(generated, existing) == []


def test_diff_reports_changed_authoritative_field():
    generated = {
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
    existing = dict(generated)
    existing["title"] = "Title B"
    diffs = diff_authoritative_fields(generated, existing)
    assert len(diffs) == 1
    assert "title" in diffs[0]


def test_diff_ignores_non_authoritative_extra_field():
    generated = {
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
    existing = dict(generated)
    existing["panofsky"] = {"pre_iconographic": "extra"}
    existing["extra_field"] = "should be ignored"
    assert diff_authoritative_fields(generated, existing) == []
