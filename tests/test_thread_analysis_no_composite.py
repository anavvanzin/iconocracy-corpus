from tools.audit.scripts import analyze_threads as a
from tools.audit.scripts import analyze_threads_v2 as v2


def test_cardinality_does_not_infer_genealogy():
    corpus = {'A': {'year':1800,'regime':'fundacional','country':'BR','indicadores':{'serialidade':0}},
              'B': {'year':1900,'regime':'normativo','country':'BR','indicadores':{'serialidade':3,'monocromatizacao':3}}}
    panels = [{'placements':[{'uid':'a','id':'A'},{'uid':'b','id':'B'}], 'threads':[{'a':'a','b':'b'}]}]
    result = a.analyze(a.expand_threads(panels,corpus))
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
