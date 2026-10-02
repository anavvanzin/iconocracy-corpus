from tools.audit.scripts import analyze_threads as a
from tools.audit.scripts import analyze_threads_v2 as v2


def test_cardinality_does_not_infer_genealogy():
    corpus = {'A': {'year':1800,'regime':'fundacional','country':'BR','indicadores':{'serialidade':0}},
              'B': {'year':1900,'regime':'normativo','country':'BR','indicadores':{'serialidade':3,'monocromatizacao':3}}}
    panels = [{'placements':[{'uid':'a','id':'A'},{'uid':'b','id':'B'}], 'threads':[{'a':'a','b':'b'}]}]
    result = a.analyze(a.expand_threads(panels,corpus, {key: a.indicator_values(row) for key, row in corpus.items()}))
    assert 'genealogy' not in [r[0] for r in result['threads'][0]['relations']]
    assert 'avg_attr_delta' not in result
    assert result['threads'][0]['indicator_transitions']['serialidade'] == [0,3]


def test_missing_observations_not_zero():
    t = a.expand_threads([{'placements':[{'uid':'a','id':'A'},{'uid':'b','id':'B'}], 'threads':[{'a':'a','b':'b'}]}], {'A':{},'B':{}})
    assert a.analyze(t)['threads'][0]['indicator_transitions'] == {}


def test_v2_chain_not_progressive_by_counts():
    corpus = {str(i): {'year':1800+i*10,'indicadores':{'serialidade':i}} for i in range(3)}
    result=v2.classify_chain({'item_ids':['0','1','2']},corpus)
    assert all(not k.startswith('endurecimento') for k,_ in result)


import json
from pathlib import Path
import pytest


def chain_for_dates(dates):
    corpus = {str(i): {'date': date} for i, date in enumerate(dates)}
    return {'item_ids': list(corpus)}, corpus


@pytest.mark.parametrize('dates, expected', [
    (['1781', 'ca. 1794', '1915'], 'weak_chain'),
    (['ca. 1794', '1800-XX-XX', '1810/1812'], 'constelacao_temporal'),
    (['1835-1841', '1800', '1900'], 'chain_unordered_temporally'),
    (['1800', None, '1820'], 'chain_dates_unavailable'),
    (['1800', 'undated', '1820'], 'chain_dates_unavailable'),
    ([None, None, None], 'chain_dates_unavailable'),
])
def test_v2_chain_uses_text_dates(dates, expected):
    chain, corpus = chain_for_dates(dates)
    assert v2.classify_chain(chain, corpus)[0][0] == expected


def test_v2_does_not_drop_missing_chain_members():
    chain, corpus = chain_for_dates(['1800', '1810', '1820', '1830'])
    del corpus['1']
    assert v2.classify_chain(chain, corpus) == [('incomplete_chain', 0.0)]


def test_v2_binary_dates_and_missingness():
    first = {'country': 'FR', 'regime': 'normativo', 'motif': ['Justitia'], 'date': '1781'}
    last = {**first, 'date': '1915'}
    classifications, flags = v2.classify_binary({'a_id': 'A', 'b_id': 'B'}, {'A': first, 'B': last})
    assert 'diachronic' in flags
    assert 'serializacao' not in dict(classifications)
    missing = {**last, 'date': None}
    classifications, flags = v2.classify_binary({'a_id': 'A', 'b_id': 'B'}, {'A': first, 'B': missing})
    assert 'diachronic' not in flags
    assert not {'serializacao', 'mimesis', 'nachleben'} & dict(classifications).keys()
    assert v2.temporal_score(first, missing, 'mimesis') is None


def pair_panel(first='A', last='B'):
    return [{'placements': [{'uid': 'a', 'id': first}, {'uid': 'b', 'id': last}],
             'threads': [{'a': 'a', 'b': 'b'}]}]


def test_canonical_ledger_overrides_projection_and_preserves_missing(tmp_path):
    ledger = tmp_path / 'purification.jsonl'
    ledger.write_text(json.dumps({'id': 'A', 'serialidade': 0}) + '\n')
    corpus = {'A': {'indicadores': {'serialidade': 3, 'monocromatizacao': 2}},
              'B': {'indicadores': {'serialidade': 3}}}
    observations = a.load_purification(ledger)
    result = a.analyze(a.expand_threads(pair_panel(), corpus, observations))
    assert result['threads'][0]['indicator_transitions'] == {'serialidade': [0, None]}
    assert a.analyze(a.expand_threads(pair_panel(), corpus))['threads'][0]['indicator_transitions'] == {}
    chain = {'item_ids': ['A', 'B'], 'panel_name': 'test'}
    report = v2.build_chain_report([chain], corpus, observations)
    assert "{'serialidade': 0}" in report
    assert 'monocromatizacao' not in report
    assert 'indisponíveis' in report


def test_live_be004_uses_canonical_observations():
    root = Path(__file__).resolve().parents[1]
    corpus = a.load_corpus(root / 'corpus/corpus-data.json')
    observations = a.load_purification(root / 'data/processed/purification.jsonl')
    result = a.analyze(a.expand_threads(pair_panel('BE-004', 'BE-004'), corpus, observations))
    assert result['threads'][0]['indicator_transitions'] == {
        name: [value, value] for name, value in observations['BE-004'].items()
    }


@pytest.mark.parametrize('rows', [[{'serialidade': 1}], [{'id': 'A'}, {'id': 'A'}]])
def test_ambiguous_ledger_fails(tmp_path, rows):
    ledger = tmp_path / 'ledger.jsonl'
    ledger.write_text('\n'.join(map(json.dumps, rows)))
    with pytest.raises(ValueError):
        a.load_purification(ledger)


def test_ledger_option_is_not_a_panel():
    args = a.parse_args(['audit', 'corpus.json', '--purification', 'ledger.jsonl', 'panel.json'])
    assert args.panels == ['panel.json']
    assert args.purification == Path('ledger.jsonl')
