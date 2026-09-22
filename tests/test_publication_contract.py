"""Publication regression cases. Synthetic fixtures are not scholarly reviews."""
from copy import deepcopy

import pytest

from tools.scripts.publication_contract import (
    REQUIRED_FACTS, publication_issues, review_digest, reviewed_export, validate_aliases,
    publication_snapshot,
)
from tools.scripts.audit_publication import identity_candidates, normalize_url, vault_index, identity_index, resolve_identifier


@pytest.fixture
def record():
    row = {
        "item_id": "473ac4d7-a507-51c6-8215-983c2442fc23",
        "input": {"input_url": "https://www.loc.gov/item/95506508/"},
        "purificacao": {"serialidade": 0, "rigidez_postural": None},
        "publication": {
            "contract_version": "1.0.0", "editorialStatus": "published",
            "identity_status": "confirmed", "public_id": "TEST-001",
            "kind": "visual", "entity_type": "work", "method_version": "test-instrument",
            "primary_source_id": "institution",
            "evidence": [{"id": "institution", "url": "https://www.loc.gov/item/95506508/",
                          "accessed_at": "2026-09-16T12:00:00Z", "citation": "Synthetic test citation.",
                          "locator": "Catalogue entry"}],
            "catalog": {field: {"value": "Synthetic " + field, "status": "documented",
                                "source_ids": ["institution"]} for field in REQUIRED_FACTS},
            "media": {"examined": True, "source_ids": ["institution"], "locator": "Entire sheet",
                      "credit": "Test fixture", "url": "https://www.loc.gov/test.jpg",
                      "sha256": "a" * 64, "sufficient_resolution": True},
            "rights": {"statement": "Synthetic rights statement", "display_permitted": True,
                       "source_ids": ["institution"]},
            "description": "Synthetic observable description.", "interpretations": [],
            "aliases": [{"surface": "site", "id": "US-012", "source_ids": ["institution"]}],
            "review": {"reviewer": "Synthetic reviewer", "reviewed_at": "2026-09-16T12:00:00Z"},
        },
    }
    row["publication"]["review"]["content_sha256"] = review_digest(row)
    return row


def test_complete_fixture_and_export_preserve_original(record):
    original = deepcopy(record)
    assert publication_issues(record) == []
    result = reviewed_export(record)
    assert result["item_id"] == record["item_id"]
    assert result["id"] == "TEST-001"
    assert record == original
    assert record["purificacao"] == {"serialidade": 0, "rigidez_postural": None}
    assert "dessexualizacao" not in record["purificacao"]


def test_missing_editorial_status_never_publishes(record):
    del record["publication"]["editorialStatus"]
    assert publication_issues(record)
    with pytest.raises(ValueError):
        reviewed_export(record)


@pytest.mark.parametrize("field", ["title", "creator", "date"])
def test_placeholder_not_reviewed_even_with_fresh_digest(record, field):
    record["publication"]["catalog"][field]["value"] = "Unknown"
    record["publication"]["review"]["content_sha256"] = review_digest(record)
    assert f"catalog.{field}.missing" in publication_issues(record)


def test_justified_unknown_is_allowed(record):
    record["publication"]["catalog"]["creator"].update(
        value="Autoria desconhecida", status="unknown", justification="Catalogue explicitly states anonymous.")
    record["publication"]["review"]["content_sha256"] = review_digest(record)
    assert publication_issues(record) == []


@pytest.mark.parametrize("change", ["fact", "source", "method", "coding"])
def test_changed_content_invalidates_review(record, change):
    if change == "fact":
        record["publication"]["catalog"]["date"]["value"] = "1918"
    elif change == "source":
        record["publication"]["evidence"][0]["url"] = "https://www.loc.gov/item/different/"
    elif change == "method":
        record["publication"]["method_version"] = "different"
    else:
        record["purificacao"]["serialidade"] = 1
    assert "review.stale_or_missing_digest" in publication_issues(record)


def test_textual_document_requires_locator_not_reproduction(record):
    p = record["publication"]
    p["kind"], p["entity_type"] = "textual", "document"
    for key in ("url", "sha256", "sufficient_resolution"):
        del p["media"][key]
    p["review"]["content_sha256"] = review_digest(record)
    assert publication_issues(record) == []
    del p["media"]["locator"]
    assert "media.locator_or_credit_missing" in publication_issues(record)


def test_columbia_alias_is_scoped_and_ambiguity_rejected(record):
    other = deepcopy(record)
    other["item_id"] = "6c4a12c1-4949-52ec-bba2-160acf162ee9"
    other["publication"]["aliases"][0]["surface"] = "canonical-export"
    owners = validate_aliases([record, other])
    assert owners[("site", "US-012")] == record["item_id"]
    assert owners[("canonical-export", "US-012")] == other["item_id"]
    other["publication"]["aliases"][0]["surface"] = "site"
    with pytest.raises(ValueError, match="Ambiguous alias"):
        validate_aliases([record, other])


def test_shared_url_does_not_collapse_records(record):
    other = deepcopy(record)
    other["item_id"] = "6c4a12c1-4949-52ec-bba2-160acf162ee9"
    results = identity_candidates({"url": record["input"]["input_url"]}, [record, other])
    assert {r["item_id"] for r in results} == {record["item_id"], other["item_id"]}
    assert {r["status"] for r in results} == {"candidate"}


def test_url_path_case_is_preserved():
    assert normalize_url("https://institution.org/Object/A") != normalize_url("https://institution.org/object/a")
    assert normalize_url("https://www.loc.gov/item/95506508/") == normalize_url("https://loc.gov/item/95506508")


def test_vault_uuid_anchor_from_frontmatter_only(tmp_path, record):
    notes = tmp_path / "vault/candidatos/subdirectory"
    notes.mkdir(parents=True)
    (notes / "SCOUT-001 Note.md").write_text(f"---\nrecords_item_id: {record['item_id']}\n---\nContent\n")
    (notes / "SCOUT-002 Mention.md").write_text(f"Mention\nrecords_item_id: {record['item_id']}\n")
    by_uuid, _ = vault_index(tmp_path)
    assert by_uuid[record["item_id"]] == ["vault/candidatos/subdirectory/SCOUT-001 Note.md"]


def test_crosswalk_preserves_columbia_handles_and_mapping_conflict(record):
    first = record['item_id']
    second = '6c4a12c1-4949-52ec-bba2-160acf162ee9'
    rows = [record, {'item_id': second}]
    mapping = [{'corpus_id': 'US-017', 'item_id': rid} for rid in (first, second)]
    crosswalk = [{'handle': 'US-012', 'uuid': first}, {'handle': 'US-017', 'uuid': second}]
    index = identity_index(rows, mapping, crosswalk)
    assert resolve_identifier('US-012', index)['item_id'] == first
    result = resolve_identifier('US-017', index)
    assert result['item_id'] == second
    assert 'identity.alias_collision' in result['issues']
    assert 'identity.crosswalk_mapping_conflict' in result['issues']
    assert resolve_identifier(first, index)['basis'] == 'canonical_uuid'
    assert resolve_identifier(first, index)['item_id'] == first


def test_ambiguous_mapping_without_crosswalk_never_selects_last(record):
    ids = [record['item_id'], '6c4a12c1-4949-52ec-bba2-160acf162ee9']
    mapping = [{'corpus_id': 'US-017', 'item_id': rid} for rid in ids]
    for ordered in (mapping, list(reversed(mapping))):
        result = resolve_identifier('US-017', identity_index([{'item_id': rid} for rid in ids], ordered, []))
        assert result['item_id'] is None
        assert result['assertions']['mapping'] == sorted(ids)


def test_dangling_crosswalk_is_not_replaced_by_mapping(record):
    index = identity_index([record], [{'corpus_id': 'TEST', 'item_id': record['item_id']}],
                           [{'handle': 'TEST', 'uuid': 'missing'}])
    result = resolve_identifier('TEST', index)
    assert result['item_id'] is None
    assert 'identity.dangling_alias' in result['issues']


def test_review_preview_is_deterministic_and_never_promotes(tmp_path):
    import json
    from uuid import UUID
    from tools.scripts.build_pilot_review import build
    audit = tmp_path / 'audit'
    audit.mkdir()
    rows = [{'item_id': str(UUID(int=i)), 'public_ids': [f'TEST-{i}'],
             'title': '<script>alert(1)</script>', 'source_url': 'javascript:alert(1)'} for i in range(1,13)]
    (audit/'inventory.json').write_text(json.dumps({'records':rows}))
    (audit/'pilot.json').write_text(json.dumps(rows))
    evidence = tmp_path/'evidence.json'
    evidence.write_text('{}')
    before = {p.name:p.read_bytes() for p in audit.iterdir()}
    first, second = tmp_path/'one',tmp_path/'two'
    build(audit,evidence,first)
    build(audit,evidence,second)
    assert {p.name:p.read_bytes() for p in first.iterdir()} == {p.name:p.read_bytes() for p in second.iterdir()}
    assert {p.name:p.read_bytes() for p in audit.iterdir()} == before
    assert len(list(first.glob('*.html'))) == 13
    page = (first/(rows[0]['item_id']+'.html')).read_text()
    assert '<script>' not in page
    assert 'href="javascript:' not in page
    assert 'Não examinado' in page


def test_snapshot_is_deterministic_and_preserves_coding(record):
    legacy = {'item_id': '6c4a12c1-4949-52ec-bba2-160acf162ee9',
              'input': {'title': 'PRIVATE UNREVIEWED TITLE'}}
    original = deepcopy(record)
    first, audit = publication_snapshot([record, legacy])
    second, reversed_audit = publication_snapshot([legacy, record])
    assert first == second
    assert audit == reversed_audit
    assert first['counts'] == {'corpus': 1, 'records': 1}
    assert audit['counts'] == {'input': 2, 'eligible': 1, 'withheld': 1}
    assert 'PRIVATE UNREVIEWED TITLE' not in str(first)
    assert first['records'][0]['purificacao'] == original['purificacao']
    assert first['corpus'][0]['publication'] == original['publication']
    assert record == original
    first['records'][0]['publication']['description'] = 'Mutated output'
    assert record == original


def test_snapshot_duplicate_uuid_rejected(record):
    with pytest.raises(ValueError, match='Duplicate canonical'):
        publication_snapshot([record, deepcopy(record)])


def test_snapshot_withheld_alias_claim_cannot_be_hidden(record):
    other = deepcopy(record)
    other['item_id'] = '6c4a12c1-4949-52ec-bba2-160acf162ee9'
    other['publication']['editorialStatus'] = 'review'
    with pytest.raises(ValueError, match='Ambiguous alias'):
        publication_snapshot([record, other])


def test_snapshot_public_id_cannot_shadow_legacy_site_alias(record):
    other = deepcopy(record)
    other['item_id'] = '6c4a12c1-4949-52ec-bba2-160acf162ee9'
    other['publication']['aliases'] = []
    other['publication']['public_id'] = 'US-012'
    other['publication']['review']['content_sha256'] = review_digest(other)
    with pytest.raises(ValueError, match='shadows site alias'):
        publication_snapshot([record, other])


def test_empty_snapshot_never_claims_release_readiness():
    snapshot, audit = publication_snapshot([])
    assert snapshot['corpus'] == snapshot['records'] == []
    assert audit['release_ready'] is False


def test_snapshot_changes_only_after_valid_new_review(record):
    original, _ = publication_snapshot([record])
    record['publication']['description'] = 'Revised observed description.'
    blocked, audit = publication_snapshot([record])
    assert blocked['counts']['records'] == 0
    assert 'review.stale_or_missing_digest' in audit['withheld'][0]['issues']
    record['publication']['review']['content_sha256'] = review_digest(record)
    revised, _ = publication_snapshot([record])
    assert revised['counts']['records'] == 1
    assert original['snapshot_id'] != revised['snapshot_id']
