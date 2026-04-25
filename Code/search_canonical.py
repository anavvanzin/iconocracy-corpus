#!/usr/bin/env python3
import json, re

with open('data/processed/records.jsonl','r') as f:
    canonical = [json.loads(line) for line in f if line.strip()]

queries = [
    'clésinger',
    'unité indivisibilité',
    'rompu mes chaines',
    'peynot',
    'exposition internationale 1889',
    '1er mai',
    'steinlen 1894',
    'nadar république',
    'villares 1888',
    'lei de 13 de maio',
    'revista illustrada 566',
    'agostini 1889',
    'suffragistas',
    'feminismo triumphante'
]

for q in queries:
    print(f"\n=== QUERY: {q} ===")
    for c in canonical:
        text = json.dumps(c, ensure_ascii=False).lower()
        if q.lower() in text:
            title = c.get('input',{}).get('title_hint','')
            print(f"  {c['item_id']} | {title}")
