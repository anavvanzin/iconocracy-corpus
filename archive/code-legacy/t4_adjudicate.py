#!/usr/bin/env python3
"""T4 LPAI Ingest Adjudication script for ICONOCRACIA corpus."""
import json
import sys
from difflib import SequenceMatcher

def load_jsonl(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records

def normalize(s):
    return s.lower().strip() if s else ""

def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def find_matches(staged, canonical):
    results = []
    for s in staged:
        s_inp = s.get('input', {})
        s_title = s_inp.get('title_hint', '')
        s_url = s_inp.get('input_url', '')
        s_date = s_inp.get('date_hint', '')
        s_place = s_inp.get('place_hint', '')
        s_ws = s.get('webscout', {})
        s_sr = s_ws.get('search_results', [{}])[0]
        s_citation = s_sr.get('abnt_citation', '')
        s_item_id = s.get('item_id', '')

        matches = []
        for c in canonical:
            c_inp = c.get('input', {})
            c_title = c_inp.get('title_hint', '')
            c_url = c_inp.get('input_url', '')
            c_date = c_inp.get('date_hint', '')
            c_place = c_inp.get('place_hint', '')
            c_ws = c.get('webscout', {})
            c_sr = c_ws.get('search_results', [{}])[0]
            c_citation = c_sr.get('abnt_citation', '')
            c_item_id = c.get('item_id', '')

            score = 0.0
            reasons = []

            # Exact URL match is strong signal
            if s_url and c_url and s_url == c_url:
                score += 1.0
                reasons.append('exact_url')

            # Title similarity
            title_sim = similarity(s_title, c_title)
            if title_sim > 0.7:
                score += title_sim * 0.6
                reasons.append(f'title_sim_{title_sim:.2f}')

            # Creator/citation overlap
            cit_sim = similarity(s_citation, c_citation)
            if cit_sim > 0.5:
                score += cit_sim * 0.4
                reasons.append(f'citation_sim_{cit_sim:.2f}')

            # Date match
            if s_date and c_date and similarity(s_date, c_date) > 0.8:
                score += 0.2
                reasons.append('date_match')

            # Place match
            if s_place and c_place and similarity(s_place, c_place) > 0.8:
                score += 0.1
                reasons.append('place_match')

            if score > 0.3:
                matches.append({
                    'canonical_item_id': c_item_id,
                    'canonical_title': c_title,
                    'canonical_url': c_url,
                    'score': score,
                    'reasons': reasons
                })

        matches.sort(key=lambda x: x['score'], reverse=True)
        results.append({
            'staged_item_id': s_item_id,
            'staged_title': s_title,
            'staged_url': s_url,
            'staged_date': s_date,
            'staged_place': s_place,
            'staged_citation': s_citation,
            'top_matches': matches[:5]
        })
    return results

if __name__ == '__main__':
    canonical = load_jsonl('data/processed/records.jsonl')
    staging = load_jsonl('data/staging/fichas-lpai-v2-parsed.jsonl')
    print(f'Loaded {len(canonical)} canonical records, {len(staging)} staged records')
    results = find_matches(staging, canonical)
    with open('data/staging/t4-adjudication-analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Wrote analysis to data/staging/t4-adjudication-analysis.json')
    for r in results:
        print(f"\n--- {r['staged_item_id']} ---")
        print(f"Title: {r['staged_title']}")
        print(f"URL: {r['staged_url']}")
        if r['top_matches']:
            for m in r['top_matches'][:3]:
                print(f"  MATCH score={m['score']:.2f} | {m['canonical_title']} | reasons={m['reasons']}")
        else:
            print("  NO MATCH")
