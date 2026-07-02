"""Tests for --draft-file support in code_purification.py."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(script_name):
    path = REPO_ROOT / "tools" / "scripts" / f"{script_name}.py"
    spec = importlib.util.spec_from_file_location(script_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[script_name] = module
    spec.loader.exec_module(module)
    return module


cp = _load("code_purification")
xw = _load("id_crosswalk")


@pytest.mark.unit
def test_load_drafts_accepts_wrapped_and_plain(tmp_path):
    # Arrange
    wrapped = tmp_path / "wrapped.json"
    wrapped.write_text(json.dumps({"drafts": [{"id": "A"}, {"id": "B"}]}), encoding="utf-8")
    plain = tmp_path / "plain.json"
    plain.write_text(json.dumps([{"id": "C"}, {"no_id": True}]), encoding="utf-8")

    # Act / Assert
    assert [d["id"] for d in cp.load_drafts(wrapped)] == ["A", "B"]
    assert [d["id"] for d in cp.load_drafts(plain)] == ["C"]  # entries without id dropped


@pytest.mark.unit
def test_match_draft_exact_id():
    drafts = [{"id": "BR-001", "purificacao": {"desincorporacao": 2}}]
    item = {"id": "BR-001"}
    assert cp.match_draft(drafts, item) is drafts[0]


@pytest.mark.unit
def test_match_draft_via_crosswalk(tmp_path, monkeypatch):
    # Arrange: crosswalk maps handle SQ-XYZ (assigned) to the uuid derived from BR-009
    item = {"id": "BR-009"}
    item_uuid = xw.derive_uuid("BR-009")
    crosswalk = tmp_path / "id_crosswalk.jsonl"
    crosswalk.write_text(json.dumps(
        {"handle": "SQ-XYZ", "uuid": item_uuid, "class": "assigned"}) + "\n",
        encoding="utf-8")
    monkeypatch.setattr(xw, "CROSSWALK_JSONL", crosswalk)

    # Act: draft identified by the alias, item by its handle
    draft = {"id": "SQ-XYZ", "purificacao": {}}
    assert cp.match_draft([draft], item) is draft

    # Assert: unknown key does not match
    assert cp.match_draft([{"id": "NAO-EXISTE"}], item) is None
