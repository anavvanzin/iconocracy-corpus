#!/usr/bin/env python3
import json

with open('data/processed/records.jsonl','r') as f:
    canonical = [json.loads(line) for line in f if line.strip()]

print("=== BRAZILIAN RECORDS ===")
for c in canonical:
    place = c.get('input',{}).get('place_hint','').lower()
    if 'brazil' in place or 'brasil' in place:
        print(f"{c['item_id']} | {c.get('input',{}).get('title_hint','')}")

print("\n=== FRENCH RECORDS (selected) ===")
for c in canonical:
    place = c.get('input',{}).get('place_hint','').lower()
    title = c.get('input',{}).get('title_hint','').lower()
    if 'france' in place or 'frança' in place:
        if any(k in title for k in ['marianne','république','liberté','justice','allégorie']):
            print(f"{c['item_id']} | {c.get('input',{}).get('title_hint','')}")
