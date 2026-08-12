import csv
import json

import pytest

from tools.scripts import elicit_pipeline as ep


def _base_row(**overrides):
    row = {
        "Title": "Allegory and the Republic",
        "Abstract": "A study of female allegorical imagery in republican visual culture.",
        "Authors": "Researcher, A.",
        "DOI": "10.1234/example",
        "DOI link": "https://doi.org/10.1234/example",
        "Venue": "Journal of Legal Iconography",
        "Citation count": "12",
        "Year": "2024",
        "Allegorical Specificity": "yes",
        'Reasoning for "Allegorical Specificity"': "Treats allegory as an explicit visual device.",
        "Analytical Depth": "yes",
        'Reasoning for "Analytical Depth"': "Sustained interpretation.",
        "Beyond Individual Women": "yes",
        'Reasoning for "Beyond Individual Women"': "The woman figure is symbolic, not biographical.",
        "Female Allegorical Focus": "yes",
        'Reasoning for "Female Allegorical Focus"': "Female allegory is central.",
        "Symbolic Paradox Analysis": "maybe",
        'Reasoning for "Symbolic Paradox Analysis"': "Notes tension between inclusion and exclusion.",
        "Theoretical Framework": "yes",
        'Reasoning for "Theoretical Framework"': "Uses iconography and political theory.",
        "Visual Political Culture": "yes",
        'Reasoning for "Visual Political Culture"': "Discusses visual representations.",
        "Screening judgement": "Include",
        'Reasoning for "Screening judgement"': "Strongly relevant source.",
        "Excluded by strict criterion": "",
        "Exclusion reason": "",
        "Screening score": "4.5",
    }
    row.update(overrides)
    return row


def _write_csv(path, rows, header=None):
    header = header or ep.REQUIRED_COLUMNS
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_load_elicit_csv_handles_v1_columns_and_literature_include(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    _write_csv(csv_path, [_base_row()])

    sources, decisions = ep.load_elicit_csv(csv_path, "2026-07-07-test")

    assert len(sources) == 1
    assert len(decisions) == 1
    assert sources[0]["criteria"]["Visual Political Culture"] == "yes"
    assert sources[0]["target_type"] == "literature"
    assert decisions[0]["decision"] == "include"
    assert "literature-only" in decisions[0]["rationale"]


def test_load_elicit_csv_preserves_long_rationales(tmp_path):
    long_reason = "Long rationale. " * 80
    csv_path = tmp_path / "elicit.csv"
    _write_csv(csv_path, [_base_row(**{'Reasoning for "Screening judgement"': long_reason})])

    sources, decisions = ep.load_elicit_csv(csv_path, "batch")

    assert sources[0]["screening_rationale"] == long_reason.strip()
    assert decisions[0]["evidence"]["screening_rationale"] == long_reason.strip()


def test_load_elicit_csv_tolerates_blank_optional_bibliographic_fields(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    _write_csv(csv_path, [_base_row(DOI="", **{"DOI link": "", "Venue": "", "Citation count": ""})])

    sources, decisions = ep.load_elicit_csv(csv_path, "batch")

    assert sources[0]["doi"] == ""
    assert sources[0]["venue"] == ""
    assert decisions[0]["decision"] in {"contextual", "needs_verification"}
    assert "missing DOI/URL" in decisions[0]["rationale"]


def test_load_elicit_csv_rejects_missing_required_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    header = [column for column in ep.REQUIRED_COLUMNS if column != "Screening score"]
    _write_csv(csv_path, [_base_row()], header=header)

    with pytest.raises(ValueError, match="Screening score"):
        ep.load_elicit_csv(csv_path, "batch")


def test_concrete_visual_object_row_becomes_candidate_note(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    header = ep.REQUIRED_COLUMNS + ["Target type"]
    row = _base_row(**{"Target type": "visual_object"})
    _write_csv(csv_path, [row], header=header)
    sources, decisions = ep.load_elicit_csv(csv_path, "batch")

    assert decisions[0]["decision"] == "candidate"

    written = ep.write_candidate_notes(sources, decisions, tmp_path / "candidates")

    assert len(written) == 1
    note = written[0].read_text(encoding="utf-8")
    assert 'status: "aprovado"' in note
    assert 'target_type: "visual_object"' in note
    assert "## Verificação necessária" in note


def test_low_score_row_is_discarded(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    _write_csv(csv_path, [_base_row(**{"Screening score": "1.5", "Screening judgement": "Include"})])

    _, decisions = ep.load_elicit_csv(csv_path, "batch")

    assert decisions[0]["decision"] == "discarded"


def test_literature_only_row_never_generates_candidate_note(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    _write_csv(csv_path, [_base_row()])
    sources, decisions = ep.load_elicit_csv(csv_path, "batch")

    written = ep.write_candidate_notes(sources, decisions, tmp_path / "candidates")

    assert written == []


def test_duplicate_source_ids_get_stable_suffix(tmp_path):
    csv_path = tmp_path / "elicit.csv"
    row_one = _base_row(Authors="Honni van Rijswijk")
    row_two = _base_row(Authors="H. Rijswijk")
    _write_csv(csv_path, [row_one, row_two])

    sources, decisions = ep.load_elicit_csv(csv_path, "batch")

    assert sources[0]["source_id"] == sources[0]["base_source_id"]
    assert sources[1]["source_id"].startswith(f"{sources[0]['base_source_id']}-DUP")
    assert sources[1]["duplicate_of"] == sources[0]["base_source_id"]
    assert decisions[0]["source_id"] != decisions[1]["source_id"]


def test_promote_requires_approved_visual_object_candidate(tmp_path):
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    (candidates / "pending.md").write_text(
        """---
id: ELICIT-pending
tipo: fonte_elicit
status: verificar
titulo: Pending Allegory
url: https://example.test/pending
target_type: visual_object
---
""",
        encoding="utf-8",
    )
    records = tmp_path / "records.jsonl"
    records.write_text("", encoding="utf-8")
    assert ep.promote_candidates(candidates, records_path=records) == []

    (candidates / "approved.md").write_text(
        """---
id: ELICIT-approved
tipo: fonte_elicit
status: aprovado
titulo: Approved Allegory
url: https://example.test/approved
pais: France
target_type: visual_object
---
""",
        encoding="utf-8",
    )
    planned = ep.promote_candidates(candidates, records_path=records)

    assert len(planned) == 1
    assert planned[0]["input"]["input_url"] == "https://example.test/approved"
    assert "elicit-import" in planned[0]["exports"]["audit_flags"]
    assert records.read_text(encoding="utf-8") == ""


def test_promote_skips_existing_record_url(tmp_path):
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    (candidates / "approved.md").write_text(
        """---
id: ELICIT-approved
tipo: fonte_elicit
status: aprovado
titulo: Approved Allegory
url: https://example.test/approved
target_type: visual_object
---
""",
        encoding="utf-8",
    )
    records = tmp_path / "records.jsonl"
    records.write_text(
        json.dumps({"input": {"input_url": "https://example.test/approved"}}) + "\n",
        encoding="utf-8",
    )

    assert ep.promote_candidates(candidates, records_path=records) == []
