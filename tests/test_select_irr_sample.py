from collections import defaultdict

import pytest

import tools.scripts.select_irr_sample as select_irr_module
from tools.scripts.select_irr_sample import load_records, select_stratified


def test_select_stratified_sample():
    # Setup dummy records with different supports and regimes
    dummy_records = [
        {"item_id": f"ITEM-{i}", "suporte": s, "regime": r}
        for i, (s, r) in enumerate([
            ("moeda", "FUNDACIONAL"), ("selo", "FUNDACIONAL"), ("monumento", "FUNDACIONAL"),
            ("moeda", "NORMATIVO"), ("selo", "NORMATIVO"), ("monumento", "NORMATIVO"),
            ("moeda", "MILITAR"), ("selo", "MILITAR"), ("monumento", "MILITAR"),
            ("arquitetura forense", "FUNDACIONAL"), ("arquitetura forense", "NORMATIVO"), ("arquitetura forense", "MILITAR")
        ] * 4) # 48 total items
    ]

    # Test the actual select_stratified function
    selected = select_stratified(dummy_records, 30)
    assert len(selected) == 30

    # Track the count of each stratum in the sample
    counts = defaultdict(int)
    for x in selected:
        suporte = x.get("metadata", {}).get("suporte") or x.get("suporte")
        regime = x.get("metadata", {}).get("regime") or x.get("regime")
        counts[(suporte, regime)] += 1

    # Assert that all 12 unique strata are represented
    assert len(counts) == 12

    # Assert that the counts are balanced (each stratum has either 2 or 3 items selected)
    for stratum, count in counts.items():
        assert count in (2, 3), f"Stratum {stratum} has unbalanced count of {count}"

def test_load_records_missing_dependencies(tmp_path, monkeypatch):
    # Set dependency paths to non-existent files to trigger FileNotFoundError
    monkeypatch.setattr(select_irr_module, "ID_MAPPING_PATH", tmp_path / "non_existent_mapping.json")
    monkeypatch.setattr(select_irr_module, "CORPUS_PATH", tmp_path / "non_existent_corpus.json")

    with pytest.raises(FileNotFoundError) as excinfo:
        load_records()
    assert "Required dependency file not found" in str(excinfo.value)
