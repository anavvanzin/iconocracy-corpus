#!/usr/bin/env python3
import json

with open('data/processed/records.jsonl','r') as f:
    canonical = [json.loads(line) for line in f if line.strip()]

# Find records matching titles
targets = [
    'Alegoria da República (Carlos Chambelland)',
    'Alegoria da República (Estados Unidos do Brasil)',
    'Alegoria da República (Décio Villares)',
    'A Justiça (Alfredo Ceschiatti, STF Brasília)',
    'La République aimable (Félicien Rops)',
    'La République nous appelle... (Steinlen)',
    "Liberté (d'après Moitte)",
    'Buste de la République',
    'République de Clésinger'
]
for t in targets:
    found = False
    for c in canonical:
        title = c.get('input',{}).get('title_hint','')
        if t.lower() in title.lower():
            print(f'FOUND: {title} | ID={c["item_id"]} | URL={c.get("input",{}).get("input_url","")}')
            found = True
            break
    if not found:
        print(f'NOT FOUND: {t}')
