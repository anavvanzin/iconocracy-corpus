#!/usr/bin/env python3
"""Diagnóstico empírico dos 10 indicadores LPAI sobre o ledger canônico atual."""
import json, itertools, collections, math

KEYS = ["desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
        "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
        "monocromatizacao","serialidade","inscricao_estatal"]

recs = [json.loads(l) for l in open('data/processed/records.jsonl')]
print(f"registros: {len(recs)}\n")

def ind(r):
    p = r.get('purificacao') or {}
    return {k: p[k] for k in KEYS if isinstance(p.get(k), (int, float))}

def import_zero(r):
    """Bloco de 10 zeros herdado de importação (vault-import/migration), não
    juízo de codificação — mesmo critério usado em analise_lacunas.py e
    analise_dimensional.py. Um registro com formato completo mas neste estado
    não é 'codificado': é placeholder. Ver achado do Codex em #162 (a versão
    anterior deste script contava esses 10-zeros como codificação completa)."""
    d = ind(r)
    return len(d) == 10 and all(d[k] == 0 for k in KEYS)

completos = [r for r in recs if len(ind(r)) == 10]
coded = [r for r in completos if not import_zero(r)]
print(f"com os 10 indicadores completos (formato): {len(completos)}")
print(f"  dos quais, zeros de importação (não codificados): {sum(1 for r in completos if import_zero(r))}")
print(f"  efetivamente codificados: {len(coded)}")
print(f"com codificação parcial: {sum(1 for r in recs if 0 < len(ind(r)) < 10)}")
print(f"sem nenhum indicador: {sum(1 for r in recs if not ind(r))}\n")

# distribuição por indicador
print("=== DISTRIBUIÇÃO (0-3) e variância — sobre registros completos ===")
print(f"{'indicador':<30} {'0':>4}{'1':>4}{'2':>4}{'3':>4}  {'média':>6} {'var':>6} {'>=2':>5}")
stats = {}
for k in KEYS:
    vals = [ind(r)[k] for r in coded]
    c = collections.Counter(vals)
    m = sum(vals)/len(vals)
    var = sum((v-m)**2 for v in vals)/len(vals)
    pres = sum(1 for v in vals if v >= 2)
    stats[k] = dict(vals=vals, mean=m, var=var, pres=pres)
    print(f"{k:<30} {c[0]:>4}{c[1]:>4}{c[2]:>4}{c[3]:>4}  {m:>6.2f} {var:>6.2f} {pres:>5}")

# correlação de Pearson entre indicadores
def corr(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    num = sum((x-ma)*(y-mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x-ma)**2 for x in a)); db = math.sqrt(sum((y-mb)**2 for y in b))
    return num/(da*db) if da and db else 0.0

print("\n=== PARES MAIS CORRELACIONADOS (colinearidade = redundância do esquema) ===")
pares = []
for a, b in itertools.combinations(KEYS, 2):
    pares.append((corr(stats[a]['vals'], stats[b]['vals']), a, b))
pares.sort(reverse=True, key=lambda x: abs(x[0]))
for r, a, b in pares[:12]:
    print(f"  {r:+.2f}  {a} × {b}")

# poder discriminante por regime
print("\n=== PODER DISCRIMINANTE POR REGIME (média por indicador) ===")
regimes = collections.defaultdict(list)
for r in coded:
    regimes[(r.get('purificacao') or {}).get('regime_iconocratico') or '?'].append(ind(r))
ordem = [x for x in ['fundacional','normativo','militar','contra-alegoria'] if x in regimes]
print(f"{'indicador':<30}" + "".join(f"{g[:12]:>14}" for g in ordem) + f"{'amplitude':>11}")
disc = []
for k in KEYS:
    med = {g: sum(d[k] for d in regimes[g])/len(regimes[g]) for g in ordem}
    amp = max(med.values()) - min(med.values())
    disc.append((amp, k))
    print(f"{k:<30}" + "".join(f"{med[g]:>14.2f}" for g in ordem) + f"{amp:>11.2f}")
print("\n  n por regime: " + ", ".join(f"{g}={len(regimes[g])}" for g in ordem))
disc.sort(reverse=True)
print("\n  ranking de discriminação entre regimes:")
for amp, k in disc:
    print(f"    {amp:.2f}  {k}")

# padrões de co-ocorrência: assinaturas de atributos
print("\n=== ASSINATURAS DE ATRIBUTOS (>=2) MAIS FREQUENTES ===")
assin = collections.Counter()
for r in coded:
    d = ind(r)
    assin[tuple(k for k in KEYS if d[k] >= 2)] += 1
print(f"  assinaturas distintas: {len(assin)} em {len(coded)} registros")
for sig, n in assin.most_common(8):
    print(f"  {n:>3}x  ({len(sig)}) {', '.join(s[:14] for s in sig) if sig else '— nenhum atributo —'}")

# por suporte
print("\n=== ATRIBUTOS POR SUPORTE (contagem média de atributos >=2) ===")
sup = collections.defaultdict(list)
for r in coded:
    m = (r.get('purificacao') or {}).get('record_metadata', {}).get('medium')
    if not m:
        medium = ((r.get('iconocode') or {}).get('pre_iconographic') or {})
        m = medium.get('medium') if isinstance(medium, dict) else None
        if isinstance(medium, list):
            m = next((x.get('medium') for x in medium if isinstance(x, dict) and x.get('medium')), None)
    d = ind(r)
    sup[m or 'não classificado'].append(sum(1 for k in KEYS if d[k] >= 2))
for m, v in sorted(sup.items(), key=lambda x: -len(x[1]))[:10]:
    print(f"  {m[:28]:<30} n={len(v):>3}  média de atributos={sum(v)/len(v):.1f}")
