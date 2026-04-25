"""Tests for tools/scripts/normalize_supports.py (Task T1).

Atomic-write and idempotency checks operate on a pytest tmp_path fixture —
the real corpus file is NEVER touched.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.scripts.normalize_supports import (
    apply_normalization,
    atomic_write_json,
    main,
)
from tools.scripts import normalize_supports as ns


# ---- Fixtures ---------------------------------------------------------


@pytest.fixture
def sample_items() -> list[dict]:
    """Small synthetic corpus covering every merge rule + out-of-canonical."""
    return [
        # country_pt merges
        {"id": "A1", "support": "moeda", "country_pt": "Estados Unidos",
         "country": "United States"},
        {"id": "A2", "support": "cartaz", "country_pt": "EUA",
         "country": "United States"},
        {"id": "A3", "support": "selo", "country_pt": "Alemanha",
         "country": "Germany"},
        # support merges (in-canonical)
        {"id": "B1", "support": "estampa", "country_pt": "França",
         "country": "France"},
        {"id": "B2", "support": "gravura", "country_pt": "França",
         "country": "France"},
        {"id": "B3", "support": "gravura/litografia", "country_pt": "Itália",
         "country": "Italy"},
        {"id": "B4", "support": "monumento", "country_pt": "Brasil",
         "country": "Brazil"},
        {"id": "B5", "support": "frontispicio", "country_pt": "Portugal",
         "country": "Portugal"},
        # out-of-canonical support (must stay as-is)
        {"id": "C1", "support": "pintura", "country_pt": "França",
         "country": "France"},
        {"id": "C2", "support": "fotografia", "country_pt": "EUA",
         "country": "United States"},
        {"id": "C3", "support": "texto", "country_pt": "Portugal",
         "country": "Portugal"},
        {"id": "C4", "support": "cerâmica", "country_pt": "França",
         "country": "France"},
        # already-canonical (must be unchanged)
        {"id": "D1", "support": "estampa/gravura", "country_pt": "EUA",
         "country": "United States"},
        {"id": "D2", "support": "monumento/escultura", "country_pt": "Brasil",
         "country": "Brazil"},
        {"id": "D3", "support": "frontispício", "country_pt": "Portugal",
         "country": "Portugal"},
        # None handling
        {"id": "E1", "support": None, "country_pt": None, "country": "France"},
    ]


@pytest.fixture
def corpus_file(tmp_path: Path, sample_items: list[dict]) -> Path:
    p = tmp_path / "corpus-data.json"
    p.write_text(json.dumps(sample_items, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    return p


# ---- Unit tests on apply_normalization --------------------------------


def test_country_pt_merge_estados_unidos_to_eua(sample_items):
    new, stats = apply_normalization(sample_items)
    # A1 had "Estados Unidos" -> "EUA"; A2 already "EUA"
    assert next(i for i in new if i["id"] == "A1")["country_pt"] == "EUA"
    assert next(i for i in new if i["id"] == "A2")["country_pt"] == "EUA"
    # Alemanha stays Alemanha (already canonical)
    assert next(i for i in new if i["id"] == "A3")["country_pt"] == "Alemanha"
    assert stats["country_pt_changed"] == 1  # only A1 changed


def test_support_estampa_variants_merge(sample_items):
    new, stats = apply_normalization(sample_items)
    for iid in ("B1", "B2", "B3"):
        assert next(i for i in new if i["id"] == iid)["support"] == "estampa/gravura"


def test_support_monumento_merge(sample_items):
    new, _ = apply_normalization(sample_items)
    assert next(i for i in new if i["id"] == "B4")["support"] == "monumento/escultura"


def test_support_frontispicio_accent_fix(sample_items):
    new, _ = apply_normalization(sample_items)
    assert next(i for i in new if i["id"] == "B5")["support"] == "frontispício"


def test_out_of_canonical_support_untouched(sample_items):
    new, stats = apply_normalization(sample_items)
    for iid, expected in (
        ("C1", "pintura"),
        ("C2", "fotografia"),
        ("C3", "texto"),
        ("C4", "cerâmica"),
    ):
        assert next(i for i in new if i["id"] == iid)["support"] == expected
    # And they are reported in the out-of-canonical counter.
    ooc = stats["support_out_of_canonical"]
    assert ooc["pintura"] == 1
    assert ooc["fotografia"] == 1
    assert ooc["texto"] == 1
    assert ooc["cerâmica"] == 1


def test_already_canonical_not_rechanged(sample_items):
    new, stats = apply_normalization(sample_items)
    for iid, expected in (
        ("D1", "estampa/gravura"),
        ("D2", "monumento/escultura"),
        ("D3", "frontispício"),
    ):
        assert next(i for i in new if i["id"] == iid)["support"] == expected
    # Canonical items shouldn't count as "changed".
    # D1 D2 D3 contribute zero to support_changed.
    # support_changed counts: B1 B2 B3 B4 B5 = 5
    assert stats["support_changed"] == 5


def test_none_values_preserved(sample_items):
    new, _ = apply_normalization(sample_items)
    e1 = next(i for i in new if i["id"] == "E1")
    assert e1["support"] is None
    assert e1["country_pt"] is None


def test_country_field_not_modified(sample_items):
    new, _ = apply_normalization(sample_items)
    # English `country` field must be untouched.
    for original, resulting in zip(sample_items, new):
        assert original["country"] == resulting["country"]


def test_field_order_and_other_fields_preserved():
    items = [
        {"id": "Z1", "title": "Some title", "support": "estampa",
         "country_pt": "Estados Unidos", "country": "United States",
         "extra_field": {"nested": [1, 2, 3]}},
    ]
    new, _ = apply_normalization(items)
    assert list(new[0].keys()) == list(items[0].keys())
    assert new[0]["extra_field"] == {"nested": [1, 2, 3]}
    assert new[0]["title"] == "Some title"


# ---- Idempotency ------------------------------------------------------


def test_idempotent_apply(sample_items):
    first, _ = apply_normalization(sample_items)
    second, stats2 = apply_normalization(first)
    assert first == second
    assert stats2["support_changed"] == 0
    assert stats2["country_pt_changed"] == 0


# ---- Atomic write -----------------------------------------------------


def test_atomic_write_produces_valid_json(tmp_path: Path, sample_items):
    target = tmp_path / "out.json"
    atomic_write_json(target, sample_items)
    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert loaded == sample_items


def test_atomic_write_replaces_existing_file(tmp_path: Path, sample_items):
    target = tmp_path / "corpus-data.json"
    target.write_text("OLD CONTENT", encoding="utf-8")
    atomic_write_json(target, sample_items)
    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert loaded == sample_items


def test_atomic_write_leaves_no_tmp_files(tmp_path: Path, sample_items):
    target = tmp_path / "corpus-data.json"
    atomic_write_json(target, sample_items)
    leftover = [p for p in tmp_path.iterdir()
                if p.name != target.name and p.name.startswith(target.name)]
    assert leftover == [], f"leftover tmp files: {leftover}"


# ---- CLI end-to-end (on synthetic file only) --------------------------


def test_cli_apply_then_second_run_zero_diff(corpus_file: Path, capsys):
    rc = main(["--path", str(corpus_file)])
    assert rc == 0
    after_first = corpus_file.read_text(encoding="utf-8")

    # Sanity: content actually changed on pass 1 vs the fixture baseline.
    # (The fixture has merge-eligible rows.)
    parsed = json.loads(after_first)
    eua_count = sum(1 for i in parsed if i.get("country_pt") == "EUA")
    assert eua_count >= 3  # A1+A2+C2+D1 = 4
    assert not any(i.get("country_pt") == "Estados Unidos" for i in parsed)
    assert not any(i.get("support") in {"estampa", "gravura",
                                         "gravura/litografia",
                                         "monumento", "frontispicio"}
                   for i in parsed)

    # Second run: byte-identical file.
    rc2 = main(["--path", str(corpus_file)])
    assert rc2 == 0
    after_second = corpus_file.read_text(encoding="utf-8")
    assert after_first == after_second


def test_cli_dry_run_makes_no_writes(corpus_file: Path):
    before = corpus_file.read_text(encoding="utf-8")
    rc = main(["--path", str(corpus_file), "--dry-run"])
    assert rc == 0
    after = corpus_file.read_text(encoding="utf-8")
    assert before == after


def test_cli_report_only_makes_no_writes(corpus_file: Path, capsys):
    before = corpus_file.read_text(encoding="utf-8")
    rc = main(["--path", str(corpus_file), "--report-only"])
    assert rc == 0
    after = corpus_file.read_text(encoding="utf-8")
    assert before == after
    out = capsys.readouterr().out
    assert "support counts" in out
    assert "country_pt counts" in out


def test_cli_bad_json_returns_nonzero(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    rc = main(["--path", str(bad)])
    assert rc == 1


def test_cli_missing_file_returns_nonzero(tmp_path: Path):
    rc = main(["--path", str(tmp_path / "does-not-exist.json")])
    assert rc == 1


# ---- Fix 2: exit code 2 on unexpected support variant ----------------


def test_cli_unexpected_support_returns_2_and_writes_file(tmp_path: Path):
    """An unexpected support value like 'lithography' must trigger rc=2,
    but the file should still be written normally (exit code is a signal,
    not a block)."""
    items = [
        # Triggers a normal merge (so a write happens).
        {"id": "X1", "support": "estampa", "country_pt": "Estados Unidos",
         "country": "United States"},
        # Unexpected support — not in SUPPORT_CANONICAL, not in SUPPORT_OUT_OF_CANONICAL.
        {"id": "X2", "support": "lithography", "country_pt": "EUA",
         "country": "United States"},
    ]
    target = tmp_path / "corpus-data.json"
    target.write_text(json.dumps(items, ensure_ascii=False, indent=2),
                      encoding="utf-8")

    rc = main(["--path", str(target)])
    assert rc == 2

    parsed = json.loads(target.read_text(encoding="utf-8"))
    # The expected merge happened.
    assert next(i for i in parsed if i["id"] == "X1")["support"] == "estampa/gravura"
    # The unexpected variant was NOT rewritten.
    assert next(i for i in parsed if i["id"] == "X2")["support"] == "lithography"


def test_cli_unexpected_support_rc2_even_when_no_writes_needed(tmp_path: Path):
    """If nothing needs writing but an unexpected variant is present,
    rc=2 still fires."""
    items = [
        {"id": "Y1", "support": "lithography", "country_pt": "EUA",
         "country": "United States"},
    ]
    target = tmp_path / "corpus-data.json"
    before = json.dumps(items, ensure_ascii=False, indent=2)
    target.write_text(before, encoding="utf-8")

    rc = main(["--path", str(target)])
    assert rc == 2
    # File unchanged (except for trailing newline policy — compare parsed).
    assert json.loads(target.read_text(encoding="utf-8")) == items


# ---- Fix 3: enumerate country_pt=None IDs in report -------------------


def test_report_enumerates_country_pt_none_ids(sample_items, capsys):
    """print_report must list the IDs where country_pt is None."""
    new, stats = apply_normalization(sample_items)
    ns.print_report(stats, header="test")
    out = capsys.readouterr().out
    # Fixture has one None entry: E1.
    assert "country_pt=null" in out
    assert "E1" in out


def test_report_country_pt_none_ids_sorted_and_counted():
    items = [
        {"id": "Z2", "support": "moeda", "country_pt": None,
         "country": "Germany"},
        {"id": "Z1", "support": "selo", "country_pt": None,
         "country": "France"},
        {"id": "Z3", "support": "cartaz", "country_pt": "EUA",
         "country": "United States"},
    ]
    _, stats = apply_normalization(items)
    # Stats must carry the sorted list of None IDs.
    assert stats["ids_country_pt_none"] == ["Z1", "Z2"]
