# tests/tools/test_e1_append_batch.py
"""Tests for e1_append_batch.py — worklist-enriched validated atomic append.

Identity/metadata come from the worklist (source of truth); results provide only
coding + fora_escopo. The append self-corrects hallucinated item_ids via sigla.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools" / "scripts"))

from e1_append_batch import (
    INDICATORS,
    build_row,
    resolve_worklist_entry,
    validate_item,
    append_batch,
)


def _result(sigla_id="FR-013", item_id="uuid-1", fora_escopo=False, **over):
    base = {
        "item_id": item_id, "sigla_id": sigla_id,
        "coded_by": "fable-5", "coded_at": "2026-06-09T20:00:00Z",
        "coded_from": "image", "image_source": "local",
        "regime_iconocratico": "normativo",
        "fora_escopo": fora_escopo, "motivo_exclusao": None,
    }
    base.update({ind: 2 for ind in INDICATORS})
    base.update(over)
    return base


def _wl_entry(item_id="uuid-1", sigla_id="FR-013"):
    return {
        "item_id": item_id, "sigla_id": sigla_id, "title": "Marianne",
        "place": "France", "date": "1880", "url": "https://ex.org/1",
        "image_source": "local", "status": "pending",
    }


def _row(**over):
    return build_row(_result(**over), _wl_entry())


# ---- resolve_worklist_entry -------------------------------------------------

def test_resolve_by_item_id():
    by_item = {"uuid-1": _wl_entry()}
    assert resolve_worklist_entry(_result(), by_item, {})["item_id"] == "uuid-1"


def test_resolve_falls_back_to_sigla_when_item_id_hallucinated():
    by_item = {"uuid-1": _wl_entry()}
    by_sigla = {"FR-013": _wl_entry()}
    # result carries a wrong (hallucinated) item_id but the right sigla
    res = _result(item_id="HALLUCINATED-999")
    entry = resolve_worklist_entry(res, by_item, by_sigla)
    assert entry is not None and entry["item_id"] == "uuid-1"


def test_resolve_returns_none_when_no_match():
    assert resolve_worklist_entry(_result(item_id="x", sigla_id="y"), {}, {}) is None


# ---- build_row --------------------------------------------------------------

def test_build_row_pulls_metadata_from_worklist():
    # result lacks title/place/date/url; worklist supplies them
    row = build_row(_result(), _wl_entry())
    assert row["title"] == "Marianne" and row["url"] == "https://ex.org/1"


def test_build_row_uses_worklist_item_id_not_result():
    row = build_row(_result(item_id="HALLUCINATED"), _wl_entry(item_id="real-id"))
    assert row["item_id"] == "real-id"


def test_build_row_fora_escopo_nulls_indicators_and_regime():
    row = build_row(
        _result(fora_escopo=True, motivo_exclusao="Efigie masculina"), _wl_entry())
    assert row["fora_escopo"] is True
    assert all(row[ind] is None for ind in INDICATORS)
    assert row["regime_iconocratico"] is None
    assert row["purificacao_composto"] is None
    assert row["motivo_exclusao"] == "Efigie masculina"


# ---- validate_item ----------------------------------------------------------

def test_validate_in_scope_row_ok():
    assert validate_item(_row(), known_ids={"uuid-1"}, indexed_ids=set()) == []


def test_validate_rejects_out_of_range():
    errs = validate_item(_row(desincorporacao=4),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("desincorporacao" in e for e in errs)


def test_validate_rejects_bool_indicator():
    errs = validate_item(_row(serialidade=True),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("serialidade" in e for e in errs)


def test_validate_rejects_bad_regime():
    errs = validate_item(_row(regime_iconocratico="imperial"),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("regime" in e for e in errs)


def test_validate_rejects_unknown_item():
    errs = validate_item(_row(), known_ids={"other"}, indexed_ids=set())
    assert any("records.jsonl" in e for e in errs)


def test_validate_rejects_duplicate():
    errs = validate_item(_row(), known_ids={"uuid-1"}, indexed_ids={"uuid-1"})
    assert any("duplicado" in e for e in errs)


def test_validate_fora_escopo_ok_with_motivo():
    row = build_row(
        _result(fora_escopo=True, motivo_exclusao="Figura masculina"), _wl_entry())
    assert validate_item(row, known_ids={"uuid-1"}, indexed_ids=set()) == []


def test_validate_fora_escopo_requires_motivo():
    row = build_row(_result(fora_escopo=True), _wl_entry())  # motivo None
    errs = validate_item(row, known_ids={"uuid-1"}, indexed_ids=set())
    assert any("motivo_exclusao" in e for e in errs)


# ---- append_batch -----------------------------------------------------------

def test_append_enriches_metadata_and_computes_composto(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps([_wl_entry()]))
    ok, errors = append_batch([_result()], index, worklist, known_ids={"uuid-1"})
    assert ok == 1 and not errors
    row = json.loads(index.read_text().strip())
    assert row["purificacao_composto"] == 2.0
    assert row["title"] == "Marianne"          # pulled from worklist
    assert json.loads(worklist.read_text())[0]["status"] == "done"


def test_append_self_corrects_item_id_via_sigla(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps([_wl_entry(item_id="real-id")]))
    # result has a hallucinated item_id but the correct sigla
    res = _result(item_id="HALLUCINATED-999")
    ok, errors = append_batch([res], index, worklist, known_ids={"real-id"})
    assert ok == 1 and not errors
    assert json.loads(index.read_text().strip())["item_id"] == "real-id"


def test_append_writes_fora_escopo_row(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps([_wl_entry()]))
    res = _result(fora_escopo=True, motivo_exclusao="Efigie masculina (Leopold I)")
    ok, errors = append_batch([res], index, worklist, known_ids={"uuid-1"})
    assert ok == 1 and not errors
    row = json.loads(index.read_text().strip())
    assert row["fora_escopo"] is True and row["purificacao_composto"] is None
    assert row["desincorporacao"] is None


def test_append_rejects_unmatched_result(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps([_wl_entry()]))
    res = _result(item_id="ghost", sigla_id="ZZ-999")
    ok, errors = append_batch([res], index, worklist, known_ids={"uuid-1"})
    assert ok == 0 and errors
    assert not index.exists() or index.read_text() == ""


def test_append_rejects_whole_invalid_item(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps([_wl_entry()]))
    ok, errors = append_batch([_result(serialidade=-1)], index, worklist,
                              known_ids={"uuid-1"})
    assert ok == 0 and errors
    assert not index.exists() or index.read_text() == ""
    assert json.loads(worklist.read_text())[0]["status"] == "pending"
