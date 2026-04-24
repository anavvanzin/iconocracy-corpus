import pytest

from tools.scripts.fix_records_schema_issues import normalize_record, write_jsonl


def test_normalize_date_only_created_at_to_utc_datetime():
    record = {"timestamps": {"created_at": "2026-04-07", "updated_at": "2026-04-08T12:30:00Z"}}
    changed = normalize_record(record)
    assert changed == ["timestamps.created_at"]
    assert record["timestamps"]["created_at"] == "2026-04-07T00:00:00Z"
    assert record["timestamps"]["updated_at"] == "2026-04-08T12:30:00Z"


def test_percent_encode_unescaped_bndigital_query_url_in_two_locations():
    raw = "https://bndigital.bnportugal.gov.pt/records/search?q=república&DocumentType=Iconografia"
    expected = "https://bndigital.bnportugal.gov.pt/records/search?q=rep%C3%BAblica&DocumentType=Iconografia"
    record = {
        "input": {"input_url": raw},
        "webscout": {"search_results": [{"url": raw}]},
        "timestamps": {"created_at": "2026-04-07T00:00:00Z", "updated_at": "2026-04-08T12:30:00Z"},
    }
    changed = normalize_record(record)
    assert changed == ["input.input_url", "webscout.search_results.0.url"]
    assert record["input"]["input_url"] == expected
    assert record["webscout"]["search_results"][0]["url"] == expected


def test_write_jsonl_keeps_target_unchanged_when_serialization_fails(tmp_path):
    target = tmp_path / "records.jsonl"
    original_content = '{"id":"original"}\n'
    target.write_text(original_content, encoding="utf-8")

    with pytest.raises(TypeError):
        write_jsonl(target, [{"bad": object()}])

    assert target.read_text(encoding="utf-8") == original_content


def test_already_valid_record_is_unchanged():
    record = {
        "input": {"input_url": "https://example.org/a?q=rep%C3%BAblica"},
        "webscout": {"search_results": [{"url": "https://example.org/a?q=rep%C3%BAblica"}]},
        "timestamps": {"created_at": "2026-04-07T00:00:00Z", "updated_at": "2026-04-08T12:30:00Z"},
    }
    changed = normalize_record(record)
    assert changed == []
    assert record["timestamps"]["created_at"] == "2026-04-07T00:00:00Z"
