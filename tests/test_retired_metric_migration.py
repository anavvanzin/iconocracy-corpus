import copy
import json
from pathlib import Path
import pytest
from tools.scripts import strip_endurecimento as migration
from tools.scripts.records_to_corpus import export_corpus
from tools.scripts.analyze_purification_drift import comparison, analyze, INDICATORS
from tools.scripts.iconocode_gemma4 import uncoded_items
from tools.scripts.build_iconocracy_sft_dataset import build_purification_assistant


def test_atomic_failure_preserves_ledger(tmp_path, monkeypatch):
    path = tmp_path / 'records.jsonl'
    original = '{"purificacao_composto": 2, "desincorporacao": 3}\n'
    path.write_text(original)
    def fail(*args):
        raise OSError('simulated interruption before replacement')
    monkeypatch.setattr(migration.os, 'fsync', fail)
    with pytest.raises(OSError):
        migration.strip_jsonl(path)
    assert path.read_text() == original
    assert list(tmp_path.iterdir()) == [path]


def test_migration_preserves_observations_and_is_byte_idempotent(tmp_path):
    item = {'purificacao': {**dict.fromkeys(INDICATORS, 3), 'notes': 'endurecimento_score=0.60; endurecimento como conceito', 'purificacao_composto': 2}}
    path = tmp_path / 'records.jsonl'
    path.write_text(json.dumps(item) + '\n')
    migration.strip_jsonl(path)
    clean = json.loads(path.read_text())
    assert {k: clean['purificacao'][k] for k in INDICATORS} == dict.fromkeys(INDICATORS, 3)
    assert 'endurecimento como conceito' in clean['purificacao']['notes']
    assert 'endurecimento_score=' not in clean['purificacao']['notes']
    first = path.read_bytes()
    migration.strip_jsonl(path)
    assert path.read_bytes() == first


def test_unmatched_export_sanitizes_without_mutating_input():
    existing = {'orphan': {'id': 'orphan', 'endurecimento_score': 2, 'indicadores': {'serialidade':3}, 'iconographic_metadata': {'endurecimento_score':1}}}
    saved = copy.deepcopy(existing)
    result = export_corpus([], existing)
    assert 'endurecimento_score' not in result[0]
    assert 'indicadores' not in result[0]
    assert 'endurecimento_score' not in result[0]['iconographic_metadata']
    assert existing == saved


def test_direct_uuid_is_matched_without_url_guess():
    uid = 'dfe19295-505c-5df1-866e-e8bb695dbc5f'
    record = {'item_id':uid, 'input':{'title_hint':'Example'}, 'webscout':{'search_results':[{'url':'https://canonical.example/'}]}}
    result = export_corpus([record], {uid:{'id':uid,'url':'https://old.example/'}})
    assert len(result) == 1
    assert result[0]['url'] == 'https://canonical.example/'


def test_missing_coder_is_unavailable_and_zero_is_observation():
    zero = {**dict.fromkeys(INDICATORS, 0), 'id':'X', 'coded_by':'human'}
    report = comparison([zero], [])
    assert all(r['delta_proportions'] is None for r in report.values())
    assert report['serialidade']['original'] == [1,0,0,0]
    assert all(r['delta_proportions'] == [0,0,0,0] for r in comparison([zero],[zero]).values())


def test_gemma_complete_zero_row_not_selected(tmp_path):
    ledger = tmp_path/'purification.jsonl'
    ledger.write_text(json.dumps({'id':'A',**dict.fromkeys(INDICATORS,0)})+'\n')
    assert uncoded_items([{'id':'A'},{'id':'B'}], ledger) == [{'id':'B'}]


def test_sft_high_indicators_do_not_become_low_label():
    text = build_purification_assistant({'id':'A',**dict.fromkeys(INDICATORS,3)},0)
    assert 'purificação baixa' not in text
    assert 'composto None' not in text
    for k in INDICATORS:
        assert f'{k}: 3' in text
