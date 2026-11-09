#!/usr/bin/env python3
"""ICONOCRACIA — validador e consolidador.

Reads sq{1..4}_candidates.json, dedups against dedup_urls.txt,
validates schema, normalizes ICONCLASS codes, emits:
- candidatos-2026-05-19.json  (master JSON ready for merge)
- candidatos-2026-05-19.md    (runbook YAML-style summary)
"""
import json, os, sys, re
from urllib.parse import urlparse
from datetime import date

PIPE = '/home/user/workspace/pipeline_run'
OUTDIR = '/home/user/workspace/corpus/candidatos'
os.makedirs(OUTDIR, exist_ok=True)

REQUIRED = ['id','title','date','creator','institution','source_archive',
            'country','medium','motif','description','url','citation_abnt']
RECOMMENDED = ['period','thumbnail_url','rights','citation_chicago','tags',
               'iconclass_codes','url_iiif','url_image_download','iiif_source',
               'confidence','sq','notes']

def canon_url(u):
    if not u: return ''
    u = u.strip().lower().rstrip('/')
    try:
        p = urlparse(u)
        netloc = p.netloc.replace('www.','')
        path = p.path.rstrip('/')
        return f"{p.scheme}://{netloc}{path}"
    except: return u

# Load dedup pool
with open(f'{PIPE}/dedup_urls.txt') as f:
    dedup = set(line.strip() for line in f if line.strip())
print(f"Dedup pool: {len(dedup)} canonical URLs")

# Collect all candidates
all_items = []
per_sq = {}
for sq in ['sq1','sq2','sq3','sq4']:
    path = f'{PIPE}/{sq}_candidates.json'
    if not os.path.exists(path):
        per_sq[sq] = {'count':0, 'with_iiif':0, 'rejected_dedup':0, 'rejected_schema':0}
        continue
    data = json.load(open(path))
    rej_dedup = rej_schema = 0
    kept = []
    for it in data:
        # Schema check
        missing = [k for k in REQUIRED if not it.get(k)]
        if missing:
            rej_schema += 1
            print(f"  [{sq}] SCHEMA REJECT {it.get('id','?')}: missing {missing}")
            continue
        # Dedup check
        cu = canon_url(it.get('url',''))
        if cu in dedup:
            rej_dedup += 1
            print(f"  [{sq}] DEDUP REJECT {it.get('id','?')}: {cu}")
            continue
        # Ensure sq field
        it['sq'] = sq.upper()
        kept.append(it)
        dedup.add(cu)  # avoid intra-batch duplicates too
    all_items.extend(kept)
    per_sq[sq] = {
        'count': len(kept),
        'with_iiif': sum(1 for x in kept if x.get('url_iiif')),
        'rejected_dedup': rej_dedup,
        'rejected_schema': rej_schema,
    }
    print(f"[{sq}] kept={len(kept)}  IIIF={per_sq[sq]['with_iiif']}  rej_dedup={rej_dedup}  rej_schema={rej_schema}")

# ICONCLASS coverage normalization
ICONCLASS_VOCAB = {
    '44G': 'administração da justiça',
    '44G3': 'autoridades judiciais',
    '48C51': 'alegoria/personificação',
    '11MM31': 'Iustitia (alegoria da Justiça)',
    '11MM': 'virtudes',
    '44A31': 'emblemas nacionais',
    '92': 'mitologia clássica',
    '25F': 'animais simbólicos',
}
for it in all_items:
    codes = it.get('iconclass_codes') or []
    if isinstance(codes, str):
        codes = [c.strip() for c in re.split(r'[,;|]', codes) if c.strip()]
    # If empty but description/motif suggest Iustitia, seed 11MM31
    if not codes:
        text = (it.get('description','') + ' '.join(it.get('motif',[]))).lower()
        seeded = []
        if any(w in text for w in ['justiça','justitia','iustitia','justice','justicia','giustizia']):
            seeded.append('11MM31')
        if 'alegoria' in text or 'allegory' in text or 'allegorie' in text or 'allegoria' in text:
            seeded.append('48C51')
        codes = seeded
    it['iconclass_codes'] = codes

# Sort: SQ then id
all_items.sort(key=lambda x: (x.get('sq',''), x.get('id','')))

# Final stats
total = len(all_items)
with_iiif = sum(1 for x in all_items if x.get('url_iiif'))
with_iconclass = sum(1 for x in all_items if x.get('iconclass_codes'))

# Write JSON output
out_json = f'{OUTDIR}/candidatos-2026-05-19.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_json}: {total} items, {with_iiif} with IIIF, {with_iconclass} with ICONCLASS")

# Stats JSON for the markdown writer
stats = {
    'date': '2026-05-19',
    'total': total,
    'with_iiif': with_iiif,
    'with_iconclass': with_iconclass,
    'per_sq': per_sq,
    'dedup_pool_size': len([l for l in open(f'{PIPE}/dedup_urls.txt') if l.strip()]),
}
with open(f'{PIPE}/stats.json','w') as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)
print(json.dumps(stats, ensure_ascii=False, indent=2))
