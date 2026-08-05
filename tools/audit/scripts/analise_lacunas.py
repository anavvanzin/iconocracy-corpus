#!/usr/bin/env python3
"""Onde os não-codificados se concentram, e que agrupamentos os indicadores formam de fato."""
import json, collections, math, itertools

KEYS = ["desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
        "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
        "monocromatizacao","serialidade","inscricao_estatal"]
recs = [json.loads(l) for l in open('data/processed/records.jsonl')]
def ind(r):
    p = r.get('purificacao') or {}
    return {k: p.get(k, 0) for k in KEYS}
def zero(r): return all(ind(r)[k] == 0 for k in KEYS)
def reg(r): return (r.get('purificacao') or {}).get('regime_iconocratico') or '?'
def pais(r):
    for fonte in (r.get('input') or {}, r):
        for k in ('country','pais','place_hint','country_hint'):
            if isinstance(fonte, dict) and fonte.get(k): return str(fonte[k])
    return '?'

print("=== NÃO CODIFICADOS POR REGIME (viés de cobertura) ===")
tot = collections.Counter(reg(r) for r in recs)
zer = collections.Counter(reg(r) for r in recs if zero(r))
for g in ['fundacional','normativo','militar','contra-alegoria']:
    if tot[g]:
        print(f"  {g:<16} {zer[g]:>3}/{tot[g]:<4} não codificados = {zer[g]/tot[g]*100:>5.1f}%")

print("\n=== NÃO CODIFICADOS POR PAÍS/LOCAL (top 10) ===")
tp = collections.Counter(pais(r) for r in recs)
zp = collections.Counter(pais(r) for r in recs if zero(r))
for p, k in tp.most_common(10):
    print(f"  {p[:26]:<28} {zp[p]:>3}/{k:<4} = {zp[p]/k*100:>5.1f}%")

# --- agrupamento dos indicadores por correlação (subcorpus codificado) ---
codif = [r for r in recs if not zero(r)]
X = [[ind(r)[k] for k in KEYS] for r in codif]
n = len(X)
means = [sum(row[j] for row in X)/n for j in range(10)]
sds = [math.sqrt(sum((row[j]-means[j])**2 for row in X)/n) for j in range(10)]
def corr(a, b):
    if not sds[a] or not sds[b]: return 0.0
    return (sum((X[i][a]-means[a])*(X[i][b]-means[b]) for i in range(n))/n)/(sds[a]*sds[b])

print(f"\n=== MATRIZ DE CORRELAÇÃO (subcorpus codificado, {len(codif)}) ===")
print("      " + "".join(f"{k[:5]:>7}" for k in KEYS))
for a in range(10):
    print(f"{KEYS[a][:5]:<6}" + "".join(f"{corr(a,b):>7.2f}" for b in range(10)))

print("\n=== AGRUPAMENTO HIERÁRQUICO SIMPLES (ligação média, corte em r=0.55) ===")
grupos = [[k] for k in KEYS]
idx = {k: i for i, k in enumerate(KEYS)}
def sim(g1, g2):
    return sum(corr(idx[a], idx[b]) for a in g1 for b in g2)/(len(g1)*len(g2))
while True:
    melhor = (0.55, None, None)
    for g1, g2 in itertools.combinations(grupos, 2):
        s = sim(g1, g2)
        if s > melhor[0]: melhor = (s, g1, g2)
    if melhor[1] is None: break
    s, g1, g2 = melhor
    grupos = [g for g in grupos if g is not g1 and g is not g2] + [g1 + g2]
for i, g in enumerate(sorted(grupos, key=len, reverse=True), 1):
    coesao = sim(g, g) if len(g) > 1 else 1.0
    print(f"  cluster {i} (coesão {coesao:.2f}): {', '.join(g)}")

print("\n=== PARES QUASE REDUNDANTES NO SUBCORPUS (r >= 0.70) ===")
for a, b in itertools.combinations(range(10), 2):
    c = corr(a, b)
    if c >= 0.70:
        print(f"  {c:.2f}  {KEYS[a]} × {KEYS[b]}")
