#!/usr/bin/env python3
import json

with open('data/processed/records.jsonl','r') as f:
    canonical = [json.loads(line) for line in f if line.strip()]

with open('data/staging/fichas-lpai-v2-parsed.jsonl','r') as f:
    staging = [json.loads(line) for line in f if line.strip()]

def show_canonical(item_id):
    for c in canonical:
        if c['item_id'] == item_id:
            inp = c.get('input',{})
            ws = c.get('webscout',{})
            sr = ws.get('search_results',[{}])[0]
            print(f"CANONICAL {item_id}")
            print(f"  Title: {inp.get('title_hint','')}")
            print(f"  URL: {inp.get('input_url','')}")
            print(f"  Date: {inp.get('date_hint','')}")
            print(f"  Place: {inp.get('place_hint','')}")
            print(f"  Citation: {sr.get('abnt_citation','')[:200]}")
            print()
            return
    print(f"CANONICAL {item_id} NOT FOUND")

def show_staged(idx):
    s = staging[idx]
    inp = s.get('input',{})
    ws = s.get('webscout',{})
    sr = ws.get('search_results',[{}])[0]
    print(f"STAGED [{idx}] {s['item_id']}")
    print(f"  Title: {inp.get('title_hint','')}")
    print(f"  URL: {inp.get('input_url','')}")
    print(f"  Date: {inp.get('date_hint','')}")
    print(f"  Place: {inp.get('place_hint','')}")
    print(f"  Citation: {sr.get('abnt_citation','')[:200]}")
    print()

# Show specific canonical records we care about
canonical_ids = [
    'ad43ba55-c523-5f19-a667-0bd5872a9867',  # Carlos Chambelland
    '8db149b7-2f6e-5f2b-9f94-7163e2633cbb',  # Estados Unidos do Brasil placeholder
    'bfac2d3e-5230-5a27-970b-625e5eb7ed24',  # Décio Villares (existing)
    '9eecda17-15eb-59ad-9071-d882725f90f5',  # Ceschiatti
    'eac80e8f-9794-5610-8a38-962119d0cd14',  # Rops aimable
    '894174a1-4d8d-50e3-8066-dbb26d18a056',  # Steinlen appelle
    'e933260c-9011-5c67-ad04-4128dd7fcbb3',  # Liberté d'après Moitte
    '4d84fe99-7db7-5ea5-96cd-bca3bd57a189',  # Buste de la République
]
for cid in canonical_ids:
    show_canonical(cid)

# Show staged records we need to adjudicate
for i in range(len(staging)):
    show_staged(i)
