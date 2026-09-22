"""Tests for tools/scripts/id_crosswalk.py — alias table handle ↔ uuid."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "scripts" / "id_crosswalk.py"

spec = importlib.util.spec_from_file_location("id_crosswalk", SCRIPT)
xw = importlib.util.module_from_spec(spec)
sys.modules["id_crosswalk"] = xw
spec.loader.exec_module(xw)


@pytest.fixture
def fake_repo(tmp_path, monkeypatch):
    # Arrange: minimal records.jsonl + corpus-data.json + empty ledger
    handles = ["BR-001", "BE-CONGO-100F-1912", "SCOUT-435"]
    uuids = {h: xw.derive_uuid(h) for h in handles}
    orphan_uuid = "12345678-1234-5678-1234-567812345678"

    records = tmp_path / "records.jsonl"
    with open(records, "w", encoding="utf-8") as f:
        for u in list(uuids.values()) + [orphan_uuid]:
            f.write(json.dumps({"item_id": u}) + "\n")

    corpus = tmp_path / "corpus-data.json"
    corpus_ids = handles + [orphan_uuid, "XX-GHOST-999"]
    with open(corpus, "w", encoding="utf-8") as f:
        json.dump([{"id": i} for i in corpus_ids], f)

    purification = tmp_path / "purification.jsonl"
    purification.write_text(json.dumps({"id": "BR-001"}) + "\n", encoding="utf-8")

    crosswalk = tmp_path / "id_crosswalk.jsonl"

    monkeypatch.setattr(xw, "RECORDS_JSONL", records)
    monkeypatch.setattr(xw, "CORPUS_JSON", corpus)
    monkeypatch.setattr(xw, "PURIFICATION_JSONL", purification)
    monkeypatch.setattr(xw, "CROSSWALK_JSONL", crosswalk)
    return {"uuids": uuids, "orphan_uuid": orphan_uuid, "crosswalk": crosswalk}


@pytest.mark.unit
def test_derive_uuid_matches_csv_to_records_convention():
    # The uuid5 namespace/prefix must mirror csv_to_records._item_uuid exactly.
    # Note: the repo hardcodes 6ba7b810-… (the NAMESPACE_DNS value) even though
    # its comment says NAMESPACE_URL — the hardcoded value is the ground truth.
    import uuid as uuidlib
    ns = uuidlib.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    expected = str(uuidlib.uuid5(ns, "iconocracy-corpus-BR-001"))
    assert xw.derive_uuid("BR-001") == expected


@pytest.mark.unit
def test_build_classifies_derivable_uuid_native_and_unresolved(fake_repo, capsys):
    # Act
    entries = xw.cmd_build(dry_run=False)

    # Assert
    by_class = {}
    for e in entries:
        by_class.setdefault(e["class"], []).append(e["handle"])
    assert sorted(by_class["derivable"]) == ["BE-CONGO-100F-1912", "BR-001", "SCOUT-435"]
    assert by_class["uuid-native"] == [fake_repo["orphan_uuid"]]
    out = capsys.readouterr().out
    assert "XX-GHOST-999" in out  # unresolved surfaced, never guessed
    assert fake_repo["crosswalk"].exists()


@pytest.mark.unit
def test_resolve_by_handle_and_by_uuid(fake_repo):
    xw.cmd_build(dry_run=False)

    uuid_br = fake_repo["uuids"]["BR-001"]
    target, entries = xw.resolve_key("BR-001")
    assert target == uuid_br

    target2, entries2 = xw.resolve_key(uuid_br)
    assert target2 == uuid_br
    assert entries2[0]["handle"] == "BR-001"

    missing, _ = xw.resolve_key("NAO-EXISTE")
    assert missing is None


@pytest.mark.unit
def test_alloc_assigns_handle_and_survives_rebuild(fake_repo):
    xw.cmd_build(dry_run=False)

    # Act: attach a human handle to the uuid-native item
    rc = xw.cmd_alloc(fake_repo["orphan_uuid"], prefix="BR")
    assert rc == 0

    target, entries = xw.resolve_key("BR-002")  # next after BR-001
    assert target == fake_repo["orphan_uuid"]

    # Rebuild must keep assigned rows (their truth lives only in the file)
    xw.cmd_build(dry_run=False)
    target_after, _ = xw.resolve_key("BR-002")
    assert target_after == fake_repo["orphan_uuid"]


@pytest.mark.unit
def test_alloc_refuses_taken_handle_and_unknown_uuid(fake_repo):
    xw.cmd_build(dry_run=False)

    rc_taken = xw.cmd_alloc(fake_repo["orphan_uuid"], handle="BR-001")
    assert rc_taken == 1

    rc_unknown = xw.cmd_alloc("99999999-9999-9999-9999-999999999999", handle="ZZ-001")
    assert rc_unknown == 1
