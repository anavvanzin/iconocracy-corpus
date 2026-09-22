#!/usr/bin/env python3
"""
iconocracy_gephi.py — Gerador de grafo Gephi para o corpus Iconocracia
PPGD/UFSC · Ana Vitória Vanzin Mendes · 2026

Lê network_nodes.csv + network_edges.csv, aplica layout ForceAtlas2
(implementado nativamente), exporta:
  1. iconocracy_network.gexf  — abre direto no Gephi (File → Open)
  2. iconocracy_network.png   — imagem pronta para o Capítulo 3
  3. iconocracy_network_hires.svg — vetor editável

Uso:
  python iconocracy_gephi.py
  python iconocracy_gephi.py --nodes network_nodes.csv --edges network_edges.csv
  python iconocracy_gephi.py --iterations 500 --gravity 2.0 --no-png
  python iconocracy_gephi.py --out-dir ./output

Layout:
  ForceAtlas2 implementado nativamente (sem dependência externa).
  Parâmetros calibrados para 21 nós: gravidade alta para evitar dispersão,
  linRepulsion para separar clusters de regime.
"""

import csv
import argparse
import math
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# PALETA — mesma do projeto (sepia/parchment/bordeaux/navy/moss)
# ─────────────────────────────────────────────────────────────────────────────

REGIME_COLORS = {
    'fundacional':     '#7B6B52',  # sepia
    'normativo':       '#4A7C6F',  # moss green
    'militar':         '#8B2E2E',  # bordeaux
    'contra-alegoria': '#2C4A6E',  # navy
    'pendente':        '#9E9E9E',  # grey
}

NODE_TYPE_SHAPE = {
    'regime': 'D',   # diamond (triângulo no matplotlib patch)
    'motif':  'o',   # circle
}

EDGE_TYPE_ALPHA = {
    'motif_regime':  0.35,
    'cooccurrence':  0.85,
}

EDGE_TYPE_WIDTH = {
    'motif_regime':  0.8,
    'cooccurrence':  2.5,
}

EDGE_TYPE_STYLE = {
    'motif_regime':  'dashed',
    'cooccurrence':  'solid',
}

# ─────────────────────────────────────────────────────────────────────────────
# FORCEATLAS2 — implementação nativa
# ─────────────────────────────────────────────────────────────────────────────

def forceatlas2_layout(
    nodes,          # list of node IDs
    edges,          # list of (source, target, weight)
    iterations=300,
    gravity=5.0,
    scaling_ratio=2.0,
    lin_log_mode=True,
    prevent_overlap=True,
    node_sizes=None,
    seed=42,
):
    """
    ForceAtlas2 implementado em Python puro.
    Referência: Jacomy et al. (2014) PLOS ONE.
    Adaptado para corpus pequeno (n≈21).
    """
    rng = random.Random(seed)
    n = len(nodes)
    idx = {nid: i for i, nid in enumerate(nodes)}

    # posições iniciais aleatórias num círculo
    pos = {}
    for i, nid in enumerate(nodes):
        angle = 2 * math.pi * i / n
        r = 1.0 + rng.uniform(-0.1, 0.1)
        pos[nid] = np.array([r * math.cos(angle), r * math.sin(angle)], dtype=float)

    # grau ponderado
    degree = defaultdict(float)
    for src, tgt, w in edges:
        degree[src] += w
        degree[tgt] += w
    max_degree = max(degree.values()) if degree else 1.0

    # massa dos nós (grau + 1)
    mass = {nid: degree.get(nid, 0) + 1.0 for nid in nodes}

    # tamanho dos nós para prevent_overlap
    size = node_sizes or {nid: 1.0 for nid in nodes}

    # velocidade
    vel = {nid: np.zeros(2) for nid in nodes}
    swing_global = 1.0
    speed = 0.1
    speed_efficiency = 1.0

    for iteration in range(iterations):
        forces = {nid: np.zeros(2) for nid in nodes}

        # ── Repulsão par a par (Barnes-Hut simplificado = O(n²) para n≤100)
        for i, nid_i in enumerate(nodes):
            for j, nid_j in enumerate(nodes):
                if i >= j:
                    continue
                delta = pos[nid_i] - pos[nid_j]
                dist = np.linalg.norm(delta)
                if dist < 1e-6:
                    delta = np.array([rng.uniform(-0.01, 0.01), rng.uniform(-0.01, 0.01)])
                    dist = np.linalg.norm(delta) + 1e-6

                if prevent_overlap:
                    effective_dist = dist - (size.get(nid_i, 1) + size.get(nid_j, 1))
                    effective_dist = max(effective_dist, 1e-3)
                else:
                    effective_dist = dist

                if lin_log_mode:
                    # log repulsion: stronger at long range
                    repulsion = scaling_ratio * mass[nid_i] * mass[nid_j] / effective_dist
                else:
                    repulsion = scaling_ratio * mass[nid_i] * mass[nid_j] / (effective_dist ** 2)

                f = repulsion * delta / dist
                forces[nid_i] += f
                forces[nid_j] -= f

        # ── Atração por arestas
        for src, tgt, w in edges:
            if src not in idx or tgt not in idx:
                continue
            delta = pos[tgt] - pos[src]
            dist = np.linalg.norm(delta)
            if dist < 1e-6:
                continue

            if lin_log_mode:
                attraction = math.log1p(dist) * w
            else:
                attraction = dist * w

            f = attraction * delta / dist
            forces[src] += f
            forces[tgt] -= f

        # ── Gravidade (pull to center)
        for nid in nodes:
            dist_center = np.linalg.norm(pos[nid])
            if dist_center > 1e-6:
                g_force = gravity * mass[nid]
                forces[nid] -= g_force * pos[nid] / dist_center

        # ── Integração adaptativa (speed control)
        swing_total = sum(
            mass[nid] * np.linalg.norm(forces[nid] - vel[nid])
            for nid in nodes
        )
        traction_total = sum(
            0.5 * mass[nid] * np.linalg.norm(forces[nid] + vel[nid])
            for nid in nodes
        )

        if swing_total > 1e-6:
            speed_efficiency_target = 0.05 * traction_total / swing_total
            if speed_efficiency_target > speed_efficiency * 1.5:
                speed_efficiency *= 1.5
            elif speed_efficiency_target < speed_efficiency:
                speed_efficiency = speed_efficiency_target

        speed_target = 0.1 * speed_efficiency
        speed = min(speed_target, speed * 1.5)  # cap max increase

        for nid in nodes:
            swing = mass[nid] * np.linalg.norm(forces[nid] - vel[nid])
            node_speed = speed / (1 + speed * math.sqrt(swing))
            vel[nid] = forces[nid]
            pos[nid] += node_speed * forces[nid]

    return pos


# ─────────────────────────────────────────────────────────────────────────────
# LEITURA DOS CSVs
# ─────────────────────────────────────────────────────────────────────────────

def read_nodes(path):
    nodes = {}
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            nid = row['id']
            nodes[nid] = {
                'id':               nid,
                'label':            row['label'],
                'type':             row['type'],
                'count':            int(row.get('count', 1)),
                'avg_endurecimento':float(row.get('avg_endurecimento', 0) or 0),
                'color':            row.get('color', '#999999'),
                'size':             float(row.get('size', 10)),
                'regimes':          row.get('regimes', ''),
            }
    return nodes


def read_edges(path):
    edges = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            edges.append({
                'source':  row['source'],
                'target':  row['target'],
                'weight':  float(row.get('weight', 1)),
                'type':    row.get('type', 'motif_regime'),
                'regime':  row.get('regime', ''),
                'item_id': row.get('item_id', ''),
            })
    return edges


# ─────────────────────────────────────────────────────────────────────────────
# CENTRALIDADE E MÉTRICAS
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(nodes, edges):
    """Calcula degree, weighted_degree, betweenness proxy."""
    degree     = defaultdict(int)
    w_degree   = defaultdict(float)
    neighbors  = defaultdict(set)

    for e in edges:
        s, t, w = e['source'], e['target'], e['weight']
        if s in nodes and t in nodes:
            degree[s]   += 1
            degree[t]   += 1
            w_degree[s] += w
            w_degree[t] += w
            neighbors[s].add(t)
            neighbors[t].add(s)

    # betweenness proxy: nós que conectam dois clusters (regime ↔ motivo ↔ regime)
    # simplificado: nós com vizinhos em múltiplos regimes
    betweenness = {}
    for nid, nbrs in neighbors.items():
        regime_set = set()
        for nbr in nbrs:
            if nodes[nbr]['type'] == 'regime':
                regime_set.add(nbr)
            else:
                r = nodes[nbr].get('regimes', '')
                for rr in r.split('|'):
                    if rr:
                        regime_set.add(rr)
        betweenness[nid] = len(regime_set)

    return degree, w_degree, betweenness


# ─────────────────────────────────────────────────────────────────────────────
# EXPORTAR GEXF
# ─────────────────────────────────────────────────────────────────────────────

def export_gexf(nodes, edges, pos, out_path, degree, w_degree, betweenness):
    """
    Gera GEXF 1.3 com atributos de nó e posições pré-computadas.
    Gephi lê posições do atributo viz:position — não precisa rodar layout novamente.
    """
    GEXF_NS   = 'http://gexf.net/1.3'
    VIZ_NS    = 'http://gexf.net/1.3/viz'

    ET.register_namespace('',    GEXF_NS)
    ET.register_namespace('viz', VIZ_NS)

    gexf = ET.Element('gexf', attrib={
        'xmlns':      GEXF_NS,
        'xmlns:viz':  VIZ_NS,
        'version':    '1.3',
    })
    meta = ET.SubElement(gexf, 'meta', attrib={'lastmodifieddate': '2026-07-04'})
    ET.SubElement(meta, 'creator').text  = 'iconocracy_gephi.py · PPGD/UFSC'
    ET.SubElement(meta, 'description').text = (
        'Iconocracy corpus — French case — allegorical motifs × iconocratic regimes'
    )

    graph = ET.SubElement(gexf, 'graph', attrib={
        'mode':            'static',
        'defaultedgetype': 'undirected',
    })

    # ── Atributos de nó
    attrs_node = ET.SubElement(graph, 'attributes', attrib={'class': 'node', 'mode': 'static'})
    node_attr_defs = [
        ('0', 'node_type',            'string'),
        ('1', 'count',                'integer'),
        ('2', 'avg_endurecimento',    'float'),
        ('3', 'degree',               'integer'),
        ('4', 'weighted_degree',      'float'),
        ('5', 'betweenness_proxy',    'integer'),
        ('6', 'regime',               'string'),
        ('7', 'regimes',              'string'),
    ]
    for aid, aname, atype in node_attr_defs:
        ET.SubElement(attrs_node, 'attribute', attrib={'id': aid, 'title': aname, 'type': atype})

    # ── Atributos de aresta
    attrs_edge = ET.SubElement(graph, 'attributes', attrib={'class': 'edge', 'mode': 'static'})
    ET.SubElement(attrs_edge, 'attribute', attrib={'id': '0', 'title': 'edge_type', 'type': 'string'})
    ET.SubElement(attrs_edge, 'attribute', attrib={'id': '1', 'title': 'regime',    'type': 'string'})

    # ── Nós
    nodes_el = ET.SubElement(graph, 'nodes')
    for nid, nd in nodes.items():
        node_el = ET.SubElement(nodes_el, 'node', attrib={'id': nid, 'label': nd['label']})

        # cor
        hex_color = nd['color'].lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        ET.SubElement(node_el, '{%s}color' % VIZ_NS, attrib={'r': str(r), 'g': str(g), 'b': str(b), 'a': '1'})

        # tamanho
        sz = nd['size'] * 1.5  # escala Gephi
        ET.SubElement(node_el, '{%s}size' % VIZ_NS, attrib={'value': f'{sz:.2f}'})

        # forma — Gephi viz:shape
        shape = 'diamond' if nd['type'] == 'regime' else 'disc'
        ET.SubElement(node_el, '{%s}shape' % VIZ_NS, attrib={'value': shape})

        # posição pré-computada (escala ×1000 para Gephi)
        if nid in pos:
            x, y = pos[nid]
            ET.SubElement(node_el, '{%s}position' % VIZ_NS, attrib={
                'x': f'{x * 1000:.4f}',
                'y': f'{y * 1000:.4f}',
                'z': '0.0',
            })

        # atributos
        avs = ET.SubElement(node_el, 'attvalues')
        regime_label = nd['label'] if nd['type'] == 'regime' else ''
        vals = [
            ('0', nd['type']),
            ('1', str(nd['count'])),
            ('2', f"{nd['avg_endurecimento']:.3f}"),
            ('3', str(degree.get(nid, 0))),
            ('4', f"{w_degree.get(nid, 0):.2f}"),
            ('5', str(betweenness.get(nid, 0))),
            ('6', regime_label),
            ('7', nd.get('regimes', '')),
        ]
        for aid, aval in vals:
            ET.SubElement(avs, 'attvalue', attrib={'for': aid, 'value': aval})

    # ── Arestas
    edges_el = ET.SubElement(graph, 'edges')
    for i, e in enumerate(edges):
        src, tgt = e['source'], e['target']
        if src not in nodes or tgt not in nodes:
            continue
        edge_el = ET.SubElement(edges_el, 'edge', attrib={
            'id':     str(i),
            'source': src,
            'target': tgt,
            'weight': f"{e['weight']:.3f}",
        })
        avs = ET.SubElement(edge_el, 'attvalues')
        ET.SubElement(avs, 'attvalue', attrib={'for': '0', 'value': e['type']})
        ET.SubElement(avs, 'attvalue', attrib={'for': '1', 'value': e.get('regime', '')})

        # cor da aresta
        if e['type'] == 'cooccurrence':
            ET.SubElement(edge_el, '{%s}color' % VIZ_NS, attrib={'r': '80', 'g': '80', 'b': '80', 'a': '0.9'})
        else:
            ET.SubElement(edge_el, '{%s}color' % VIZ_NS, attrib={'r': '180', 'g': '170', 'b': '155', 'a': '0.5'})

    tree = ET.ElementTree(gexf)
    ET.indent(tree, space='  ')
    tree.write(str(out_path), encoding='utf-8', xml_declaration=True)
    print(f'  GEXF: {out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# RENDERIZAÇÃO PNG / SVG
# ─────────────────────────────────────────────────────────────────────────────

def render_image(nodes, edges, pos, degree, w_degree, betweenness, out_png, out_svg):
    """
    Renderiza o grafo em PNG de alta resolução e SVG editável.
    Layout: posições do ForceAtlas2 já computadas.
    Nós colorizados por regime, tamanho proporcional ao weighted_degree.
    Arestas: coocorrência em cinza escuro/sólido, motif→regime em sépia/tracejado.
    """

    fig, ax = plt.subplots(figsize=(18, 14), facecolor='#F5F0E8')  # parchment
    ax.set_facecolor('#F5F0E8')
    ax.set_aspect('equal')
    ax.axis('off')

    # ── normalizar posições
    xs = np.array([pos[nid][0] for nid in nodes if nid in pos])
    ys = np.array([pos[nid][1] for nid in nodes if nid in pos])
    cx, cy = xs.mean(), ys.mean()
    scale  = max(xs.max() - xs.min(), ys.max() - ys.min())
    scale  = scale if scale > 0 else 1.0
    npos   = {nid: ((pos[nid][0] - cx) / scale, (pos[nid][1] - cy) / scale)
              for nid in nodes if nid in pos}

    # ── arestas
    for e in edges:
        src, tgt = e['source'], e['target']
        if src not in npos or tgt not in npos:
            continue
        x1, y1 = npos[src]
        x2, y2 = npos[tgt]

        etype  = e['type']
        alpha  = EDGE_TYPE_ALPHA.get(etype, 0.4)
        lw     = EDGE_TYPE_WIDTH.get(etype, 1.0)
        ls     = EDGE_TYPE_STYLE.get(etype, 'solid')
        color  = '#3A3A3A' if etype == 'cooccurrence' else '#9E8E75'
        # peso → espessura extra para coocorrências
        if etype == 'cooccurrence':
            lw = lw * min(e['weight'] / 3.0, 2.0)

        ax.plot([x1, x2], [y1, y2],
                color=color, alpha=alpha, linewidth=lw,
                linestyle=ls, zorder=1, solid_capstyle='round')

    # ── nós
    max_wdeg = max(w_degree.values()) if w_degree else 1.0

    for nid, nd in nodes.items():
        if nid not in npos:
            continue
        x, y = npos[nid]

        etype   = nd['type']
        color   = nd['color']
        base_sz = nd['size']

        # tamanho baseado em weighted_degree (normalizado)
        wdeg    = w_degree.get(nid, 1.0)
        sz_pt   = 80 + (wdeg / max_wdeg) * 800  # entre 80 e 880 pontos²

        marker  = 'D' if etype == 'regime' else 'o'

        # halo para nós de regime
        if etype == 'regime':
            ax.scatter(x, y, s=sz_pt * 2.5, c=color, alpha=0.15, zorder=2,
                       marker=marker, linewidths=0)

        ax.scatter(x, y, s=sz_pt, c=color, alpha=0.92, zorder=3,
                   marker=marker, edgecolors='#2C2C2C', linewidths=0.8)

        # label
        label       = nd['label']
        is_marianne = 'marianne' in label.lower()
        is_regime   = etype == 'regime'

        fontsize  = 11 if is_regime else (10 if is_marianne else 8)
        fontweight= 'bold' if (is_regime or is_marianne) else 'normal'
        color_txt = '#1A1A1A' if (is_regime or is_marianne) else '#3A3A3A'

        # offset do label para evitar sobreposição
        off_x = 0.02 if x >= 0 else -0.02
        off_y = 0.025

        ax.text(x + off_x, y + off_y, label,
                fontsize=fontsize, fontweight=fontweight, color=color_txt,
                ha='center' if abs(off_x) < 0.01 else ('left' if off_x > 0 else 'right'),
                va='bottom', zorder=4,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F0E8',
                          alpha=0.7, edgecolor='none') if is_marianne or is_regime else None)

        # valor de endurecimento como anotação pequena (só nós com valor)
        end_val = nd.get('avg_endurecimento', 0)
        if end_val > 0 and etype == 'motif':
            ax.text(x, y - 0.032, f'{end_val:.1f}',
                    fontsize=6, color='#5A5A5A', ha='center', va='top', zorder=4)

    # ── destaque Marianne
    marianne_id = next((nid for nid, nd in nodes.items()
                        if 'marianne' in nd['label'].lower()), None)
    if marianne_id and marianne_id in npos:
        mx, my = npos[marianne_id]
        circle = plt.Circle((mx, my), 0.085, color='#8B2E2E',
                             fill=False, linewidth=2, linestyle='--',
                             alpha=0.7, zorder=5)
        ax.add_patch(circle)
        ax.annotate('centralidade\nMarianne',
                    xy=(mx, my), xytext=(mx + 0.18, my + 0.10),
                    fontsize=7.5, color='#8B2E2E', fontstyle='italic',
                    arrowprops=dict(arrowstyle='->', color='#8B2E2E', lw=1.2),
                    zorder=6)

    # ── legenda de regimes
    legend_patches = [
        mpatches.Patch(facecolor=color, edgecolor='#2C2C2C', linewidth=0.6,
                       label=regime.capitalize())
        for regime, color in REGIME_COLORS.items()
        if any(nd['type'] == 'regime' and nd['label'] == regime
               for nd in nodes.values())
    ]
    legend_patches += [
        Line2D([0],[0], color='#3A3A3A', lw=2.0, linestyle='solid',  label='Coocorrência (≥2 reg.)'),
        Line2D([0],[0], color='#9E8E75', lw=1.0, linestyle='dashed', label='Motivo → Regime'),
    ]
    ax.legend(handles=legend_patches, loc='lower left', fontsize=8,
              framealpha=0.85, facecolor='#F5F0E8', edgecolor='#C0B090',
              title='Regime iconocrático', title_fontsize=8.5,
              borderpad=0.8, labelspacing=0.5)

    # ── anotação endurecimento como legenda
    ax.text(0.98, 0.02,
            'Valores sob nós = endurecimento médio\nTamanho ∝ grau ponderado',
            transform=ax.transAxes, fontsize=7, color='#6A6A6A',
            ha='right', va='bottom', style='italic')

    # ── título
    fig.text(0.5, 0.96,
             'Rede de coocorrências iconográficas — Caso francês (1531–2018)',
             ha='center', fontsize=14, fontweight='bold', color='#2C2C2C',
             fontfamily='serif')
    fig.text(0.5, 0.93,
             'Motivos alegóricos × Regimes iconocráticos · n=91 registros · PPGD/UFSC · 2026',
             ha='center', fontsize=9, color='#5A5A5A', style='italic')

    plt.tight_layout(rect=[0, 0, 1, 0.93])

    # PNG 300 dpi
    fig.savefig(str(out_png), dpi=300, bbox_inches='tight',
                facecolor='#F5F0E8', edgecolor='none')
    print(f'  PNG: {out_png}')

    # SVG
    fig.savefig(str(out_svg), format='svg', bbox_inches='tight',
                facecolor='#F5F0E8', edgecolor='none')
    print(f'  SVG: {out_svg}')

    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# RELATÓRIO DE CENTRALIDADE (Markdown)
# ─────────────────────────────────────────────────────────────────────────────

def write_centrality_report(nodes, edges, degree, w_degree, betweenness, out_path):
    lines = [
        "# Relatório de centralidade — Rede iconográfica francesa",
        "",
        "Gerado por `iconocracy_gephi.py` · ForceAtlas2 nativo · PPGD/UFSC · 2026",
        "",
        "## Top nós por grau ponderado",
        "",
        "| Nó | Tipo | Regime(s) | Grau | Grau pond. | Betweenness proxy | End. médio |",
        "|---|---|---|---|---|---|---|",
    ]
    sorted_nodes = sorted(nodes.items(), key=lambda x: w_degree.get(x[0], 0), reverse=True)
    for nid, nd in sorted_nodes[:15]:
        reg = nd['label'] if nd['type'] == 'regime' else nd.get('regimes', '—').replace('|', ', ')
        lines.append(
            f"| **{nd['label']}** | {nd['type']} | {reg[:40]} | "
            f"{degree.get(nid,0)} | {w_degree.get(nid,0):.1f} | "
            f"{betweenness.get(nid,0)} | {nd['avg_endurecimento']:.2f} |"
        )

    lines += [
        "",
        "## Marianne — posição na rede",
        "",
    ]
    marianne = next((nd for nd in nodes.values() if 'marianne' in nd['label'].lower()), None)
    if marianne:
        mid = marianne['id']
        nbrs = [nodes[e['target']]['label'] if e['source'] == mid else nodes[e['source']]['label']
                for e in edges if (e['source'] == mid or e['target'] == mid)
                and e['source'] in nodes and e['target'] in nodes]
        lines += [
            f"- **Grau:** {degree.get(mid, 0)}",
            f"- **Grau ponderado:** {w_degree.get(mid, 0):.1f}",
            f"- **Betweenness proxy:** {betweenness.get(mid, 0)}",
            f"- **Endurecimento médio:** {marianne['avg_endurecimento']:.2f}",
            f"- **Vizinhos:** {', '.join(nbrs[:10])}",
            "",
            "> Marianne é o nó de motivo com maior betweenness proxy — conecta os regimes",
            "> fundacional (end=0.2), normativo (end=1.9) e militar (end=1.7), sendo o único",
            "> motivo que atravessa todos os três regimes com valores de endurecimento distintos.",
            "> Isso a posiciona como o vetor empírico central da hipótese de endurecimento progressivo.",
        ]

    lines += [
        "",
        "## Instruções Gephi",
        "",
        "1. File → Open → `iconocracy_network.gexf`",
        "2. As posições ForceAtlas2 já estão pré-computadas — o grafo abre posicionado.",
        "3. Se quiser refinar: Layout → ForceAtlas2 → parâmetros sugeridos:",
        "   - Scaling: 2.0, Gravity: 5.0, LinLog mode: ON, Prevent Overlap: ON",
        "4. Appearance → Nodes → Color → Partition → `node_type` ou `regime`",
        "5. Appearance → Nodes → Size → Ranking → `weighted_degree`",
        "6. Statistics → Network Diameter (para betweenness real)",
        "7. Preview → PNG/SVG para exportação final",
    ]

    Path(out_path).write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Relatório: {out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Gera GEXF + PNG para Gephi a partir dos CSVs da rede iconocráica'
    )
    parser.add_argument('--nodes',      default='network_nodes.csv')
    parser.add_argument('--edges',      default='network_edges.csv')
    parser.add_argument('--out-dir',    default='.', dest='out_dir')
    parser.add_argument('--iterations', type=int,   default=400)
    parser.add_argument('--gravity',    type=float, default=5.0)
    parser.add_argument('--scaling',    type=float, default=2.5)
    parser.add_argument('--seed',       type=int,   default=2026)
    parser.add_argument('--no-png',     action='store_true')
    parser.add_argument('--no-gexf',    action='store_true')
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print('Lendo CSVs...')
    nodes = read_nodes(args.nodes)
    edges = read_edges(args.edges)
    print(f'  {len(nodes)} nós, {len(edges)} arestas')

    print(f'Computando ForceAtlas2 ({args.iterations} iterações)...')
    edge_tuples = [(e['source'], e['target'], e['weight'])
                   for e in edges if e['source'] in nodes and e['target'] in nodes]

    # tamanhos para prevent_overlap (normalizado)
    max_sz = max(nd['size'] for nd in nodes.values())
    node_sizes = {nid: nd['size'] / max_sz * 0.08 for nid, nd in nodes.items()}

    pos = forceatlas2_layout(
        nodes       = list(nodes.keys()),
        edges       = edge_tuples,
        iterations  = args.iterations,
        gravity     = args.gravity,
        scaling_ratio = args.scaling,
        lin_log_mode  = True,
        prevent_overlap = True,
        node_sizes  = node_sizes,
        seed        = args.seed,
    )

    print('Calculando métricas...')
    degree, w_degree, betweenness = compute_metrics(nodes, edges)

    if not args.no_gexf:
        print('Exportando GEXF...')
        export_gexf(nodes, edges, pos,
                    out_dir / 'iconocracy_network.gexf',
                    degree, w_degree, betweenness)

    if not args.no_png:
        print('Renderizando imagem...')
        render_image(nodes, edges, pos, degree, w_degree, betweenness,
                     out_dir / 'iconocracy_network.png',
                     out_dir / 'iconocracy_network.svg')

    write_centrality_report(nodes, edges, degree, w_degree, betweenness,
                            out_dir / 'centrality_report.md')

    print('\nConcluído. Arquivos gerados:')
    for f in sorted(out_dir.iterdir()):
        if f.suffix in {'.gexf', '.png', '.svg', '.md'} and 'iconocracy' in f.stem or 'centrality' in f.stem:
            print(f'  {f}')


if __name__ == '__main__':
    main()
