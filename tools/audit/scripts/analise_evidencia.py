#!/usr/bin/env python3
"""Que evidência visual existe hoje para recodificar? Sem imagem não há codificação."""
import json, collections
from urllib.parse import urlparse

recs = [json.loads(l) for l in open('data/processed/records.jsonl')]
KEYS = ["desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
        "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
        "monocromatizacao","serialidade","inscricao_estatal"]
IMG = {'.jpg','.jpeg','.png','.webp','.gif','.tif','.tiff'}

def zero(r):
    p = r.get('purificacao') or {}
    return all((p.get(k) or 0) == 0 for k in KEYS)

def classifica(url):
    if not url: return 'sem url'
    path = urlparse(url).path.lower()
    ext = '.' + path.rsplit('.', 1)[-1] if '.' in path.rsplit('/', 1)[-1] else ''
    if ext in IMG: return 'imagem direta'
    if ext == '.pdf': return 'pdf'
    if ext in ('.html', '.htm', ''): return 'página web (precisa navegar)'
    return f'outro ({ext})'

print("=== EVIDÊNCIA VISUAL DISPONÍVEL (todos os 328) ===")
c = collections.Counter(classifica((r.get('input') or {}).get('input_url')) for r in recs)
for k, v in c.most_common():
    print(f"  {k:<34} {v:>4}  ({v/len(recs)*100:.0f}%)")

print("\n=== POR ESTADO DE CODIFICAÇÃO ===")
for nome, grupo in (("não codificados (106)", [r for r in recs if zero(r)]),
                    ("codificados (222)", [r for r in recs if not zero(r)])):
    c = collections.Counter(classifica((r.get('input') or {}).get('input_url')) for r in grupo)
    print(f"  {nome}: " + " | ".join(f"{k}={v}" for k, v in c.most_common()))

print("\n=== DOMÍNIOS DE ACERVO (top 12) ===")
doms = collections.Counter()
for r in recs:
    u = (r.get('input') or {}).get('input_url')
    if u:
        doms[urlparse(u).netloc.replace('www.', '')] += 1
for d, n in doms.most_common(12):
    print(f"  {d[:44]:<46} {n:>4}")

print("\n=== CAMPOS DE APOIO À RECODIFICAÇÃO ===")
tem = collections.Counter()
for r in recs:
    ic = r.get('iconocode') or {}
    ws = r.get('webscout') or {}
    if isinstance(ic.get('pre_iconographic'), list) and ic['pre_iconographic']: tem['motivos pré-iconográficos'] += 1
    if ic.get('interpretation'): tem['interpretação registrada'] += 1
    if ic.get('codes'): tem['códigos Iconclass'] += 1
    if ws.get('summary_evidence'): tem['evidência webscout'] += 1
    if (r.get('input') or {}).get('date_hint'): tem['data'] += 1
    if (r.get('input') or {}).get('title_hint'): tem['título'] += 1
for k, v in tem.most_common():
    print(f"  {k:<32} {v:>4}/328  ({v/len(recs)*100:.0f}%)")

print("\n=== VOLUME DE TRABALHO POR CENÁRIO ===")
for nome, n in (("recodificar tudo", 328), ("só os não codificados", 106),
                ("codificados a revisar", 222)):
    for min_item in (8, 15, 25):
        horas = n * min_item / 60
        print(f"  {nome:<26} a {min_item:>2} min/item = {horas:>5.1f} h "
              f"= {horas/4:>4.1f} semanas a 4h/semana")
    print()
