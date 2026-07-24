"""Regression tests for canonical record-to-corpus field propagation."""

from __future__ import annotations

from tools.scripts.records_to_corpus import _corpus_entry_from_record


def _record(*, medium: object = None) -> dict:
    purificacao: dict = {}
    if medium is not None:
        purificacao["record_metadata"] = {"medium": medium}
    return {
        "item_id": "record-1",
        "input": {"title_hint": "Item de teste", "place_hint": "Brazil"},
        "purificacao": purificacao,
    }


def test_support_is_propagated_from_canonical_record_metadata() -> None:
    entry = _corpus_entry_from_record(
        _record(medium="  Escultura em bronze  "),
        existing={"id": "BR-TEST", "support": "valor legado"},
    )

    assert entry["support"] == "Escultura em bronze"


def test_support_is_not_preserved_without_canonical_source() -> None:
    entry = _corpus_entry_from_record(
        _record(),
        existing={"id": "BR-TEST", "support": "valor apenas no export"},
    )

    assert "support" not in entry


def test_blank_or_non_string_medium_is_not_a_canonical_source() -> None:
    for medium in ("   ", [], {"type": "escultura"}):
        entry = _corpus_entry_from_record(
            _record(medium=medium),
            existing={"id": "BR-TEST", "support": "valor apenas no export"},
        )

        assert "support" not in entry
