#!/usr/bin/env python3
"""Descriptive ordinal distributions by coder group; no scalar composite.

Different coder populations are not paired agreement estimates. Missing groups
remain unavailable. Identity/support come from records, observations from the
purification ledger, joined through the canonical ID mapping.
"""
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PURIFICATION = REPO_ROOT / 'data/processed/purification.jsonl'
INDICATORS = [
    'desincorporacao', 'rigidez_postural', 'dessexualizacao',
    'uniformizacao_facial', 'heraldizacao', 'enquadramento_arquitetonico',
    'apagamento_narrativo', 'monocromatizacao', 'serialidade', 'inscricao_estatal',
]


def load_items(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def distribution(items, indicator):
    values = [x[indicator] for x in items if indicator in x]
    return [values.count(v) for v in range(4)] if values else None


def comparison(a, b):
    result = {}
    for ind in INDICATORS:
        da, db = distribution(a, ind), distribution(b, ind)
        result[ind] = {'original': da, 'auto': db, 'delta_proportions': (
            [db[v] / sum(db) - da[v] / sum(da) for v in range(4)]
            if da is not None and db is not None else None
        )}
    return result


def metadata_index(records, mapping):
    by_id = {r['item_id']: r for r in records}
    aliases = {m['corpus_id']: m['item_id'] for m in mapping.get('mapping', [])}
    return by_id, aliases


def analyze(items, records, mapping):
    by_id, aliases = metadata_index(records, mapping)
    enriched = []
    unmatched = []
    for row in items:
        rec = by_id.get(aliases.get(row['id'], row['id']))
        if rec is None:
            # Same deterministic identity rule as the exporter, without URL guessing.
            import uuid
            uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"iconocracy-corpus-{row['id']}"))
            rec = by_id.get(uid)
        if rec is None:
            unmatched.append(row['id'])
        inp = (rec or {}).get('input') or {}
        meta = ((rec or {}).get('purificacao') or {}).get('record_metadata') or {}
        enriched.append({**row, '_country': str(inp.get('place_hint') or '?'),
                         '_support': meta.get('medium') or '?'})
    groups = {'overall': {'all': enriched}}
    for label, key in [('regime','regime_iconocratico'), ('country','_country'), ('support','_support')]:
        groups[label] = {}
        for row in enriched:
            groups[label].setdefault(row.get(key) or '?', []).append(row)
    report = {'unmatched_observation_ids': unmatched, 'groups': {},
              'limitation': 'Unpaired coder populations: descriptive distributions, not agreement or causal drift.'}
    for kind, buckets in groups.items():
        report['groups'][kind] = {}
        for label, rows in buckets.items():
            a = [r for r in rows if r.get('coded_by') != 'hermes-auto']
            b = [r for r in rows if r.get('coded_by') == 'hermes-auto']
            report['groups'][kind][label] = {'n_original':len(a), 'n_auto':len(b), 'indicators':comparison(a,b)}
    # Existing text is evidence; no thresholded list is fabricated as an inventory.
    report['qualitative_coverage'] = {
        'master_records':len(records),
        'with_attribute_text':sum(bool((r.get('purificacao') or {}).get('atributos_iconograficos')) for r in records),
        'with_verbal_inventory':sum(bool((r.get('purificacao') or {}).get('inventario_verbal')) for r in records),
        'observations':len(items),
        'observations_with_notes':sum(bool(r.get('notes')) for r in items),
    }
    return report


def main():
    report = analyze(load_items(PURIFICATION), load_items(REPO_ROOT / 'data/processed/records.jsonl'),
                     json.loads((REPO_ROOT / 'data/processed/id-mapping.json').read_text()))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
