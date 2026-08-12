"""Unit tests for the Hugging Face release builder's safety contract."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from tools.scripts import build_hf_release as release


def test_load_jsonl_skips_blank_lines(tmp_path: Path):
    source = tmp_path / "records.jsonl"
    source.write_text('{"id": "A"}\n\n  {"id": "B"}  \n', encoding="utf-8")

    assert release.load_jsonl(source) == [{"id": "A"}, {"id": "B"}]


def test_compute_stats_uses_fallbacks_and_ignores_non_numeric_scores():
    corpus = [
        {
            "country": "BR",
            "regime": "normativo",
            "support": "moeda",
            "endurecimento_score": 1,
        },
        {
            "country": "BR",
            "medium_norm": "cartaz",
            "endurecimento_score": 2.5,
        },
        {"medium": "selo", "endurecimento_score": "3"},
        {},
    ]
    records = [
        {"master_record_version": "2.0"},
        {"master_record_version": "1.0"},
        {},
    ]
    purification = [{"id": "BR-001"}, {"id": "BR-001"}, {"id": "FR-001"}, {}]

    stats = release.compute_stats(corpus, records, purification)

    assert stats["corpus_items"] == 4
    assert stats["records_items"] == 3
    assert stats["purification_rows"] == 4
    assert stats["coded_items"] == 2
    assert stats["country_count"] == 2
    assert stats["schema_versions"] == ["1.0", "2.0", "unknown"]
    assert stats["regime_counts"] == {"normativo": 1, "unknown": 3}
    assert stats["top_supports"] == {"moeda": 1, "cartaz": 1, "selo": 1, "unknown": 1}
    assert stats["mean_endurecimento"] == 1.75
    assert stats["corpus_records_delta"] == 1


def test_compute_stats_returns_none_when_scores_are_absent():
    stats = release.compute_stats([{"id": "A"}], [], [])

    assert stats["mean_endurecimento"] is None


@pytest.mark.parametrize(
    ("delta", "expected"),
    [
        (0, "No corpus/records drift detected."),
        (2, "has 2 more item(s)"),
        (-1, "has 1 fewer item(s)"),
    ],
)
def test_render_readme_describes_drift_direction(delta: int, expected: str):
    stats = {
        "schema_versions": [],
        "mean_endurecimento": None,
        "corpus_records_delta": delta,
        "generated_at": "2026-08-09T00:00:00Z",
        "corpus_items": 2,
        "records_items": 2 - delta,
        "coded_items": 1,
        "country_count": 1,
    }

    readme = release.render_readme("owner/dataset", "v1", stats, "- note\n")

    assert expected in readme
    assert "Mean endurecimento score: **n/a**" in readme
    assert "Master-record schema versions: `unknown`" in readme


def test_render_changelog_supplies_default_note():
    result = release.render_changelog([], {"corpus_items": 3, "records_items": 3, "coded_items": 2})

    assert result == (
        "- Generated from the local release pipeline.\n"
        "- Snapshot counts: corpus=3, records=3, coded=2.\n"
    )


def test_validate_local_contract_runs_both_validators(monkeypatch: pytest.MonkeyPatch):
    calls = []
    monkeypatch.setattr(release.subprocess, "run", lambda command, **kwargs: calls.append((command, kwargs)))
    monkeypatch.setattr(release, "load_json", lambda _path: [{"id": "A"}])
    monkeypatch.setattr(release, "load_jsonl", lambda path: [{"id": "A"}])

    release.validate_local_contract()

    assert len(calls) == 2
    assert calls[0][0][-3:] == ["--schema", "master-record", "--verbose"]
    assert calls[1][0][-3:] == ["--schema", "purification-record", "--verbose"]
    assert all(kwargs == {"check": True} for _, kwargs in calls)


def test_validate_local_contract_rejects_count_drift(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(release.subprocess, "run", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(release, "load_json", lambda _path: [{"id": "A"}, {"id": "B"}])
    monkeypatch.setattr(release, "load_jsonl", lambda _path: [{"id": "A"}])

    with pytest.raises(SystemExit, match=r"corpus=2, records=1, delta=1"):
        release.validate_local_contract()


def test_ensure_hf_auth_requires_cli(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(release.shutil, "which", lambda _name: None)

    with pytest.raises(SystemExit, match="hf CLI not found"):
        release.ensure_hf_auth()


def test_ensure_hf_auth_rejects_unauthenticated_cli(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(release.shutil, "which", lambda _name: "/usr/bin/hf")
    result = subprocess.CompletedProcess([], returncode=1)
    monkeypatch.setattr(release.subprocess, "run", lambda *_args, **_kwargs: result)

    with pytest.raises(SystemExit, match="not authenticated"):
        release.ensure_hf_auth()


def test_write_sha256sums_covers_every_release_artifact(tmp_path: Path):
    names = [
        "corpus-data.json",
        "records.jsonl",
        "purification.jsonl",
        "release.json",
        "CHANGELOG.md",
        "README.md",
    ]
    for name in names:
        (tmp_path / name).write_text(name, encoding="utf-8")

    release.write_sha256sums(tmp_path)

    lines = (tmp_path / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    assert len(lines) == len(names)
    for name, line in zip(names, lines):
        expected = hashlib.sha256(name.encode()).hexdigest()
        assert line == f"{expected}  {name}"


def test_publish_snapshot_constructs_dataset_upload(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    calls = []
    monkeypatch.setattr(release, "ensure_hf_auth", lambda: calls.append("auth"))
    monkeypatch.setattr(release.subprocess, "run", lambda command, **kwargs: calls.append((command, kwargs)))

    release.publish_snapshot("owner/dataset", tmp_path, "v1", ["first", "second"])

    assert calls[0] == "auth"
    command, kwargs = calls[1]
    assert command[:4] == ["hf", "upload", "owner/dataset", str(tmp_path)]
    assert command[command.index("--commit-message") + 1] == "release: dataset snapshot v1"
    assert command[command.index("--commit-description") + 1] == "first\nsecond"
    assert kwargs == {"check": True}


def test_release_manifest_is_valid_json_shape():
    """Protect the JSON assumptions shared by README generation and publishing."""
    stats = release.compute_stats([], [], [])
    manifest = {"dataset_repo": "owner/dataset", "release_tag": "v1", "stats": stats, "notes": []}

    assert json.loads(json.dumps(manifest))["stats"]["corpus_items"] == 0
