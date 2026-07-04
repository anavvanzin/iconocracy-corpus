"""Tests for the derived SQL data-model strata."""

from __future__ import annotations

from tools.scripts.records_to_sqlite import (
    INDICATOR_COLUMNS,
    classify_record_stratum,
)


def _record(
    *,
    coded_by: str | None = "iconocode-opus",
    regime: str | None = "normativo",
    analytic_eligible: bool | None = None,
    period_extended: bool | None = None,
    audit_flags: list[str] | None = None,
):
    purificacao = {name: 1 for name in INDICATOR_COLUMNS}
    if coded_by is not None:
        purificacao["coded_by"] = coded_by
    if regime is not None:
        purificacao["regime_iconocratico"] = regime
    if analytic_eligible is not None:
        purificacao["analytic_eligible"] = analytic_eligible
    if period_extended is not None:
        purificacao["period_extended"] = period_extended
    return {
        "purificacao": purificacao,
        "exports": {"audit_flags": audit_flags or []},
    }


def test_uncoded_missing_provenance_is_excluded():
    record = _record(coded_by=None, regime=None)

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "uncoded"
    assert stratum["validity_stratum"] == "S0_UNCODED"
    assert stratum["quantitative_status"] == "excluded_uncoded"
    assert stratum["has_coded_by"] == 0
    assert stratum["has_regime"] == 0


def test_direct_iconocode_is_core_candidate():
    record = _record(coded_by="iconocode-opus-4.6-image")

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "iconocode_direct"
    assert stratum["validity_stratum"] == "S1_ICONOCODE_DIRECT"
    assert stratum["quantitative_status"] == "core_candidate"
    assert stratum["scope_status"] == "core_1800_2000"


def test_legacy_import_requires_audit():
    record = _record(coded_by="vault-import")

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "legacy_or_imported"
    assert stratum["validity_stratum"] == "S3_LEGACY_OR_IMPORTED"
    assert stratum["quantitative_status"] == "audit_required"


def test_curatorial_record_is_separate_from_direct_iconocode():
    record = _record(coded_by="ana")

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "curatorial"
    assert stratum["validity_stratum"] == "S2_CURATORIAL"
    assert stratum["quantitative_status"] == "audit_required"


def test_tentative_batch_requires_audit():
    record = _record(coded_by="batch-tentative-2026-04-25")

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "tentative"
    assert stratum["validity_stratum"] == "S4_TENTATIVE"
    assert stratum["quantitative_status"] == "audit_required"


def test_opus48_is_separate_pending_stratum():
    record = _record(coded_by="opus-4.8")

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "opus48_pending"
    assert stratum["validity_stratum"] == "S5_OPUS48_PENDING"
    assert stratum["quantitative_status"] == "audit_required"
    assert stratum["scope_status"] == "core_1800_2000"


def test_scope_extension_excludes_even_when_direct_iconocode():
    record = _record(
        coded_by="iconocode-opus",
        analytic_eligible=False,
        period_extended=True,
        audit_flags=["fora-do-escopo"],
    )

    stratum = classify_record_stratum(record)

    assert stratum["instrument_family"] == "iconocode_direct"
    assert stratum["validity_stratum"] == "S1_ICONOCODE_DIRECT"
    assert stratum["quantitative_status"] == "excluded_scope"
    assert stratum["scope_status"] == "extended_or_out_of_scope"
    assert stratum["analytic_eligible"] == 0
    assert stratum["period_extended"] == 1


def test_scope_extension_overrides_opus48_pending_status():
    record = _record(coded_by="opus-4.8", period_extended=True)

    stratum = classify_record_stratum(record)

    assert stratum["validity_stratum"] == "S5_OPUS48_PENDING"
    assert stratum["quantitative_status"] == "excluded_scope"
    assert stratum["scope_status"] == "extended_or_out_of_scope"


def test_incomplete_indicators_force_uncoded_stratum():
    record = _record(coded_by="iconocode-opus")
    del record["purificacao"][INDICATOR_COLUMNS[0]]

    stratum = classify_record_stratum(record)

    assert stratum["validity_stratum"] == "S0_UNCODED"
    assert stratum["quantitative_status"] == "excluded_uncoded"
    assert stratum["has_complete_indicators"] == 0
