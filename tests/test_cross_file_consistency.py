#!/usr/bin/env python3
"""Cross-file consistency tests for the ICONOCRACY corpus.

Ensures records.jsonl, corpus-data.json, purification.jsonl,
and drive-manifest.json share consistent IDs and references.

Run: python3 -m pytest tests/test_cross_file_consistency.py -v
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load_records():
    with open(REPO / "data/processed/records.jsonl") as f:
        return [json.loads(l) for l in f if l.strip()]


def load_corpus():
    return json.load(open(REPO / "corpus/corpus-data.json"))


def load_purification():
    with open(REPO / "data/processed/purification.jsonl") as f:
        return [json.loads(l) for l in f if l.strip()]


def load_id_mapping():
    try:
        return json.load(open(REPO / "data/processed/id-mapping.json"))
    except FileNotFoundError:
        return {"mapping": []}


def load_manifest():
    try:
        return json.load(open(REPO / "data/raw/drive-manifest.json"))
    except FileNotFoundError:
        return {"items": []}


# ── Test 1: id-mapping coverage ──────────────────────────────────


def test_id_mapping_coverage():
    """At least 50% of records should have a corpus_id mapping (growing corpus)."""
    mapping = load_id_mapping()
    records = load_records()
    mapped = sum(1 for e in mapping.get("mapping", []) if e.get("corpus_id"))
    assert mapped / len(records) >= 0.5, (
        f"Only {mapped}/{len(records)} records mapped ({mapped/len(records)*100:.1f}%)"
    )


def test_id_mapping_no_duplicates():
    """Each record UUID should appear at most once in the mapping."""
    mapping = load_id_mapping()
    seen = set()
    for e in mapping.get("mapping", []):
        uid = e.get("item_id")
        assert uid not in seen, f"Duplicate item_id in mapping: {uid}"
        seen.add(uid)


# ── Test 2: records ↔ corpus cross-check ────────────────────────


def test_records_corpus_count_plausible():
    """Corpus should not have more items than records (records may have extra)."""
    records = load_records()
    corpus = load_corpus()
    assert len(corpus) <= len(records) * 1.1, (
        f"Corpus ({len(corpus)}) far exceeds records ({len(records)})"
    )


def test_corpus_items_have_required_fields():
    """Every corpus item must have title and regime (url may be empty for offline items)."""
    corpus = load_corpus()
    for i, c in enumerate(corpus):
        assert c.get("title"), f"Corpus item {i}: missing title"
        # regime can be empty string but must exist
        assert "regime" in c, f"Corpus item {i}: missing regime"


# ── Test 3: purification schema compliance ────────────────────────


def test_purification_all_valid():
    """All purification records must be valid JSON objects."""
    pur = load_purification()
    assert len(pur) > 0, "Purification file is empty"
    for i, rec in enumerate(pur):
        assert isinstance(rec, dict), f"Purification record {i}: not a dict"
        assert rec.get("id"), f"Purification record {i}: missing id"


def test_purification_count_aligned():
    """Purification count should be close to corpus count."""
    pur = load_purification()
    corpus = load_corpus()
    ratio = len(pur) / len(corpus) if corpus else 0
    assert 0.5 <= ratio <= 1.5, (
        f"Purification ({len(pur)}) vs corpus ({len(corpus)}) ratio: {ratio:.2f}"
    )


# ── Test 4: drive-manifest consistency ────────────────────────────


def test_drive_manifest_populated():
    """Drive manifest must contain items."""
    manifest = load_manifest()
    assert len(manifest.get("items", [])) > 0, "Drive manifest is empty"


def test_drive_manifest_items_have_ids():
    """Every manifest item must have an id."""
    manifest = load_manifest()
    for i, item in enumerate(manifest.get("items", [])):
        assert item.get("id"), f"Manifest item {i}: missing id"


# ── Test 5: id-mapping bidirectional ──────────────────────────────


def test_mapping_corpus_ids_exist():
    """Every corpus_id in the mapping must exist in corpus-data.json."""
    mapping = load_id_mapping()
    corpus = load_corpus()
    corpus_ids = {c.get("id", "") for c in corpus if c.get("id")}
    for e in mapping.get("mapping", []):
        cid = e.get("corpus_id", "")
        if cid:
            assert cid in corpus_ids, (
                f"Mapping has corpus_id '{cid}' not found in corpus"
            )
