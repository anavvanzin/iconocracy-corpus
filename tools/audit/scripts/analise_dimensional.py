#!/usr/bin/env python3
"""Dimensionalidade real do esquema, sensibilidade ao limiar e origem das assinaturas suspeitas."""
import json, collections, math

KEYS = ["desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
        "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
        "monocromatizacao","serialidade","inscricao_estatal"]

recs = [json.loads(l) for l in open('data/processed/records.jsonl')]
def ind(r):
    p = r.get('purificacao') or {}
    return {k: p.get(k, 0) for k in KEYS}
def zero(r):
    d = ind(r)
    return all(d[k] == 0 for k in KEYS)

def jacobi_eigen(M, iters=200):
    import copy
    A = copy.deepcopy(M); m = len(A)
    for _ in range(iters):
        p = q = 0; mx = 0
        for i in range(m):
            for j in range(i+1, m):
                if abs(A[i][j]) > mx: mx, p, q = abs(A[i][j]), i, j
        if mx < 1e-9: break
        if A[p][p] == A[q][q]:
            theta = math.pi/4
        else:
            theta = 0.5*math.atan2(2*A[p][q], A[p][p]-A[q][q])
        c, s = math.cos(theta), math.sin(theta)
        Ap = [row[:] for row in A]
        for k in range(m):
            Ap[p][k] = c*A[p][k] + s*A[q][k]
            Ap[q][k] = -s*A[p][k] + c*A[q][k]
        A2 = [row[:] for row in Ap]
        for k in range(m):
            A2[k][p] = c*Ap[k][p] + s*Ap[k][q]
            A2[k][q] = -s*Ap[k][p] + c*Ap[k][q]
        A = A2
    return sorted((A[i][i] for i in range(m)), reverse=True)

def dimensionalidade(recs_subset, titulo):
    """Autovalores da matriz de correlação sobre um subconjunto de registros.
    Regenera o par de leituras que a Auditoria Hostil do PR #162 (achado
    GRAVE, ver review comment do Codex) apontou como não-reproduzível pelo
    script original: com os zeros de importação, e só sobre o codificado."""
    Xs = [[ind(r)[k] for k in KEYS] for r in recs_subset]
    ns = len(Xs)
    def colj(j): return [row[j] for row in Xs]
    ms = [sum(colj(j))/ns for j in range(10)]
    sd = [math.sqrt(sum((v-ms[j])**2 for v in colj(j))/ns) for j in range(10)]
    Rs = [[0.0]*10 for _ in range(10)]
    for a in range(10):
        for b in range(10):
            cov = sum((Xs[i][a]-ms[a])*(Xs[i][b]-ms[b]) for i in range(ns))/ns
            Rs[a][b] = cov/(sd[a]*sd[b]) if sd[a] and sd[b] else 0.0
    eig = jacobi_eigen(Rs)
    tot = sum(eig)
    print(f"=== DIMENSIONALIDADE EFETIVA — {titulo} (n={ns}) ===")
    acc = 0
    for i, e in enumerate(eig, 1):
        acc += e/tot
        print(f"  componente {i}: autovalor {e:5.2f}  variância {e/tot*100:5.1f}%  acumulada {acc*100:5.1f}%")
    kaiser = sum(1 for e in eig if e > 1)
    print(f"\n  componentes com autovalor > 1 (critério de Kaiser): {kaiser}")
    print(f"  → o esquema de 10 indicadores comporta-se como {kaiser} dimensão(ões)\n")
    return eig

dimensionalidade(recs, "com falsos zeros de importação")
dimensionalidade([r for r in recs if not zero(r)], "só registros efetivamente codificados")

# --- sensibilidade ao limiar ---
X = [[ind(r)[k] for k in KEYS] for r in recs]
n = len(X)
print("\n=== SENSIBILIDADE AO LIMIAR DE 'ATRIBUTO PRESENTE' (n=todos) ===")
for thr in (1, 2, 3):
    counts = [sum(1 for v in row if v >= thr) for row in X]
    zeros = sum(1 for c in counts if c == 0)
    sigs = len({tuple(k for k, v in zip(KEYS, row) if v >= thr) for row in X})
    print(f"  limiar >={thr}: média {sum(counts)/n:.1f} atributos | "
          f"itens sem atributo: {zeros} ({zeros/n*100:.0f}%) | assinaturas distintas: {sigs}")

# --- origem das assinaturas extremas ---
print("\n=== ORIGEM DAS ASSINATURAS EXTREMAS (auditoria) ===")
todos10 = [r for r in recs if all(ind(r)[k] >= 2 for k in KEYS)]
nenhum = [r for r in recs if all(ind(r)[k] == 0 for k in KEYS)]
for nome, grupo in (("todos os 10 atributos", todos10), ("todos os indicadores em zero", nenhum)):
    print(f"\n  {nome}: {len(grupo)} registros")
    for campo in ("coded_by", "regime_iconocratico"):
        c = collections.Counter((r.get('purificacao') or {}).get(campo) for r in grupo)
        print(f"    {campo}: {dict(c.most_common(5))}")

# --- suporte, pela via correta ---
print("\n=== SUPORTE (via purificacao.record_metadata.medium, com fallbacks) ===")
def medium(r):
    p = r.get('purificacao') or {}
    rm = p.get('record_metadata') or {}
    if rm.get('medium'):
        return rm['medium']
    ic = r.get('iconocode') or {}
    pre = ic.get('pre_iconographic')
    if isinstance(pre, dict) and pre.get('medium'):
        return pre['medium']
    for chave in ('medium', 'support', 'suporte'):
        for fonte in (r, r.get('input') or {}, ic):
            if isinstance(fonte, dict) and fonte.get(chave):
                return fonte[chave]
    return None
c = collections.Counter(medium(r) or 'não classificado' for r in recs)
for m, k in c.most_common(8):
    grupo = [r for r in recs if (medium(r) or 'não classificado') == m]
    med = sum(sum(1 for v in ind(r).values() if v >= 2) for r in grupo)/len(grupo)
    print(f"  {str(m)[:30]:<32} n={k:>3}  atributos médios={med:.1f}")
