# tests/tools/test_e1_append_batch.py
"""Tests for e1_append_batch.py — validated atomic append to the index."""
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools" / "scripts"))

from e1_append_batch import validate_item, append_batch, INDICATORS


def _coded(item_id="uuid-1", **over):
    base = {
        "item_id": item_id, "sigla_id": "FR-013", "title": "Marianne",
        "place": "France", "date": "1880", "url": "https://ex.org/1",
        "coded_by": "fable-5", "coded_at": "2026-06-09T20:00:00Z",
        "coded_from": "image", "image_source": "local",
        "confidence": 0.9, "flags": [], "notes": "ok",
        "regime_iconocratico": "normativo",
    }
    base.update({ind: 2 for ind in INDICATORS})
    base.update(over)
    return base


def test_validate_ok():
    assert validate_item(_coded(), known_ids={"uuid-1"}, indexed_ids=set()) == []


def test_validate_rejects_out_of_range():
    errs = validate_item(_coded(desincorporacao=4),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("desincorporacao" in e for e in errs)


def test_validate_rejects_bad_regime():
    errs = validate_item(_coded(regime_iconocratico="imperial"),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("regime" in e for e in errs)


def test_validate_rejects_unknown_item():
    errs = validate_item(_coded(), known_ids={"other"}, indexed_ids=set())
    assert any("records.jsonl" in e for e in errs)


def test_validate_rejects_duplicate():
    errs = validate_item(_coded(), known_ids={"uuid-1"}, indexed_ids={"uuid-1"})
    assert any("duplicado" in e for e in errs)


def test_append_batch_writes_composto_and_marks_worklist(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps(
        [{"item_id": "uuid-1", "status": "pending"}]))
    ok, errors = append_batch([_coded()], index, worklist,
                              known_ids={"uuid-1"})
    assert ok == 1 and not errors
    row = json.loads(index.read_text().strip())
    assert row["purificacao_composto"] == 2.0
    wl = json.loads(worklist.read_text())
    assert wl[0]["status"] == "done"


def test_append_batch_rejects_whole_invalid_item(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps(
        [{"item_id": "uuid-1", "status": "pending"}]))
    ok, errors = append_batch([_coded(serialidade=-1)], index, worklist,
                              known_ids={"uuid-1"})
    assert ok == 0 and errors
    assert not index.exists() or index.read_text() == ""
    assert json.loads(worklist.read_text())[0]["status"] == "pending"
