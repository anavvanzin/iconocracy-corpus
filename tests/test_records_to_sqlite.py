import json
import sqlite3

from tools.scripts.records_to_sqlite import (
    _deterministic_item_id,
    _load_mapping,
    build_database,
)


def _write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_sqlite_projection_preserves_local_evidence_ids_and_coding_rounds(tmp_path):
    records_file = tmp_path / "records.jsonl"
    purification_file = tmp_path / "purification.jsonl"
    mapping_file = tmp_path / "id-mapping.json"
    sqlite_db = tmp_path / "corpus.sqlite"

    records = []
    for item_id, corpus_id in (("item-1", "BR-001"), ("item-2", "FR-001")):
        records.append(
            {
                "item_id": item_id,
                "input": {
                    "title_hint": corpus_id,
                    "place_hint": "Brazil" if corpus_id.startswith("BR") else "France",
                    "date_hint": "1901",
                },
                "webscout": {
                    "search_results": [
                        {
                            "evidence_id": "e1",
                            "source_type": "primary_image",
                            "title": corpus_id,
                            "url": f"https://example.org/{corpus_id}",
                        }
                    ]
                },
                "iconocode": {"codes": []},
                "timestamps": {
                    "created_at": "2026-08-12T00:00:00Z",
                    "updated_at": "2026-08-12T00:00:00Z",
                },
            }
        )

    codings = []
    for coder, round_number, prompt_version in (
        ("ana", 1, "iconocode-v1"),
        ("ana", 1, "iconocode-v2"),
    ):
        codings.append(
            {
                "id": "BR-001",
                **{field: 0 for field in (
                    "desincorporacao",
                    "rigidez_postural",
                    "dessexualizacao",
                    "uniformizacao_facial",
                    "heraldizacao",
                    "enquadramento_arquitetonico",
                    "apagamento_narrativo",
                    "monocromatizacao",
                    "serialidade",
                    "inscricao_estatal",
                )},
                "regime_iconocratico": "normativo",
                "coded_by": coder,
                "coded_at": f"2026-08-{10 + round_number:02d}T00:00:00Z",
                "coding_round": round_number,
                "prompt_version": prompt_version,
            }
        )

    _write_jsonl(records_file, records)
    _write_jsonl(purification_file, codings)
    mapping_file.write_text(
        json.dumps(
            {
                "mapping": [
                    {"corpus_id": "BR-001", "item_id": "item-1"},
                    {"corpus_id": "FR-001", "item_id": "item-2"},
                ]
            }
        ),
        encoding="utf-8",
    )

    stats = build_database(
        records_file=records_file,
        purification_file=purification_file,
        mapping_file=mapping_file,
        sqlite_db=sqlite_db,
        verify=False,
    )

    assert stats == {
        "items": 2,
        "purification": 2,
        "evidence": 2,
        "iconclass": 0,
    }
    with sqlite3.connect(sqlite_db) as db:
        assert db.execute("SELECT COUNT(*) FROM evidence").fetchone()[0] == 2
        assert db.execute("SELECT COUNT(*) FROM purification").fetchone()[0] == 2
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        keys = db.execute(
            "SELECT item_id, evidence_id FROM evidence ORDER BY item_id"
        ).fetchall()
        assert keys == [("item-1", "e1"), ("item-2", "e1")]


def test_ambiguous_crosswalk_only_assigns_deterministic_public_identity(tmp_path):
    mapping_file = tmp_path / "id-mapping.json"
    deterministic = _deterministic_item_id("BR-001")
    mapping_file.write_text(
        json.dumps(
            {
                "mapping": [
                    {"corpus_id": "BR-001", "item_id": "legacy-item"},
                    {"corpus_id": "BR-001", "item_id": deterministic},
                ]
            }
        ),
        encoding="utf-8",
    )

    corpus_to_item, item_to_corpus = _load_mapping(mapping_file)

    assert corpus_to_item == {"BR-001": deterministic}
    assert item_to_corpus == {deterministic: "BR-001"}
