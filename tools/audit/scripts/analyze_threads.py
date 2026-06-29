#!/usr/bin/env python3
"""
ICONOCRACIA — Warburg Thread Analyzer
=====================================

Consumes one or more panel JSON exports from the Warburg canvas
(iconocracia-warburg-atlas-*.json) and the corpus-data.json, then produces:

1. A relational graph of threads with full corpus metadata
2. Cluster analysis by regime and motif
3. Strength metrics per cluster
4. A draft taxonomy of iconocratic relations

Usage:
    python analyze_threads.py corpus.json painel-1.json painel-2.json ...
    python analyze_threads.py corpus.json *.json
    python analyze_threads.py corpus.json --demo   # uses synthetic threads

Outputs:
    thread-analysis-report.md      (human-readable report)
    thread-analysis.json           (full structured data)
    thread-graph.svg               (network visualization)
"""

import json, sys, os
from pathlib import Path
from collections import defaultdict, Counter

# ============================================================================
# CONFIG — Taxonomy template (provisional; refines from data)
# ============================================================================

RELATION_TYPES = {
    'nachleben':            'Pathosformel survival — same visual gesture across centuries',
    'mimesis':              'Direct iconographic imitation — copy or close variant',
    'inversion':            'Reversal — same iconography deployed against itself',
    'translatio':           'Translation — same allegorical function, different national tradition',
    'contradiction':        'Contradiction — pieces stand in dialectical opposition',
    'genealogy':            'Genealogical descent — A produces B as visual heir',
    'serialization':        'Serial repetition — same image multiplied across media (coin/stamp/banknote)',
    'concretization':       'Concretization — abstract allegory becomes a specific named figure',
    'abstraction':          'Abstraction — specific scene becomes generalized allegory',
    'co-presence':          'Co-presence — items share a single political moment without genealogical link',
    'gendered-pair':        'Gendered counterpart — feminine allegory paired with masculine sovereign',
    'racialization':        'Racialization — same allegory whitened or darkened across versions',
    'martialization':       'Martialization — civic allegory dressed for war',
    'demilitarization':     'Demilitarization — wartime allegory disarmed in peacetime',
    'satirization':         'Satirization — solemn allegory turned grotesque or comic',
}

REGIME_COLORS = {
    'fundacional': '#16213E',
    'normativo':   '#8B7355',
    'militar':     '#6B2D3E',
    'contra-alegoria': '#C4A265',
    '': '#888076',
}

# ============================================================================
# Loading
# ============================================================================

def load_corpus(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return {e.get('id'): e for e in data if e.get('id')}

def load_panels(paths):
    panels = []
    for p in paths:
        with open(p, encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, dict) and 'panelId' in data:
                    panels.append(data)
                elif isinstance(data, dict) and 'panels' in data:
                    # Full state dump
                    for pid, pdata in data['panels'].items():
                        panels.append({
                            'panelId': int(pid),
                            'panelName': f'Panel {pid}',
                            'placements': pdata.get('placements', []),
                            'threads': pdata.get('threads', []),
                            'essay': pdata.get('essay', {}),
                        })
            except Exception as e:
                print(f"⚠ Failed to load {p}: {e}")
    return panels

def make_demo_panels(corpus_by_id):
    """Generate synthetic panel data illustrating likely thread patterns."""
    # Pick representative items for each panel
    pick = lambda crit, n=4: [eid for eid, e in corpus_by_id.items() if crit(e)][:n]
    
    panels = []
    
    # Panel 1 — Gênese — French Revolutionary fundacional
    p1_items = pick(lambda e: (e.get('country') == 'France' and 
                                e.get('regime') == 'fundacional' and 
                                (e.get('year') or 0) <= 1830), n=5)
    panels.append({
        'panelId': 1, 'panelName': 'Gênese',
        'placements': [{'uid': f'p-1-{i}', 'id': eid, 'x':100+i*200, 'y':200} 
                       for i, eid in enumerate(p1_items)],
        'threads': [{'uid': f't-1-{i}', 'a': f'p-1-{i}', 'b': f'p-1-{i+1}'} 
                    for i in range(len(p1_items)-1)],
        'essay': {'title': 'Gênese', 'body': 'demo'},
    })
    
    # Panel 4 — ENDURECIMENTO — score progression
    sorted_by_score = sorted(
        [(eid, e) for eid, e in corpus_by_id.items() if (e.get('endurecimento_score') or 0) > 0],
        key=lambda x: x[1].get('endurecimento_score') or 0
    )
    p4_items = [eid for eid, _ in sorted_by_score[:3]] + [eid for eid, _ in sorted_by_score[-4:]]
    panels.append({
        'panelId': 4, 'panelName': 'ENDURECIMENTO',
        'placements': [{'uid': f'p-4-{i}', 'id': eid, 'x':100+i*200, 'y':200} 
                       for i, eid in enumerate(p4_items)],
        'threads': [{'uid': f't-4-{i}', 'a': f'p-4-{i}', 'b': f'p-4-{i+1}'} 
                    for i in range(len(p4_items)-1)],
        'essay': {'title': 'ENDURECIMENTO', 'body': 'demo'},
    })
    
    # Panel 2 — Justitia — cross-country
    p2_items = pick(lambda e: 'Justitia' in (e.get('motif') or []) and e.get('country'), n=6)
    panels.append({
        'panelId': 2, 'panelName': 'Justitia',
        'placements': [{'uid': f'p-2-{i}', 'id': eid, 'x':100+i*180, 'y':200} 
                       for i, eid in enumerate(p2_items)],
        'threads': [
            {'uid': f't-2-0', 'a': 'p-2-0', 'b': 'p-2-2'},
            {'uid': f't-2-1', 'a': 'p-2-1', 'b': 'p-2-3'},
            {'uid': f't-2-2', 'a': 'p-2-0', 'b': 'p-2-4'},
        ],
        'essay': {'title': 'Justitia', 'body': 'demo'},
    })
    
    # Panel 4-bis — Militar cluster
    p_mil_items = pick(lambda e: e.get('regime') == 'militar', n=5)
    panels.append({
        'panelId': 5, 'panelName': 'Pedra e Bronze',
        'placements': [{'uid': f'p-5-{i}', 'id': eid, 'x':100+i*180, 'y':200} 
                       for i, eid in enumerate(p_mil_items)],
        'threads': [{'uid': f't-5-{i}', 'a': f'p-5-{i}', 'b': f'p-5-{(i+1) % len(p_mil_items)}'} 
                    for i in range(len(p_mil_items))],
        'essay': {'title': 'Pedra e Bronze (demo)', 'body': 'demo'},
    })
    
    return panels

# ============================================================================
# Analysis
# ============================================================================

def expand_threads(panels, corpus_by_id):
    """Expand each thread into {a, b, panel_id, ...} with corpus metadata."""
    expanded = []
    for panel in panels:
        plac_by_uid = {p['uid']: p for p in panel.get('placements', [])}
        for t in panel.get('threads', []):
            a_uid, b_uid = t.get('a'), t.get('b')
            if a_uid not in plac_by_uid or b_uid not in plac_by_uid:
                continue
            a_id = plac_by_uid[a_uid].get('id')
            b_id = plac_by_uid[b_uid].get('id')
            a_entry = corpus_by_id.get(a_id, {})
            b_entry = corpus_by_id.get(b_id, {})
            expanded.append({
                'panel_id': panel.get('panelId'),
                'panel_name': panel.get('panelName'),
                'thread_uid': t.get('uid'),
                'a_id': a_id, 'b_id': b_id,
                'a_title': a_entry.get('title', '(?)'),
                'b_title': b_entry.get('title', '(?)'),
                'a_year': a_entry.get('year'), 'b_year': b_entry.get('year'),
                'a_country': a_entry.get('country', ''), 'b_country': b_entry.get('country', ''),
                'a_regime': a_entry.get('regime', ''), 'b_regime': b_entry.get('regime', ''),
                'a_score': a_entry.get('endurecimento_score', 0),
                'b_score': b_entry.get('endurecimento_score', 0),
                'a_motifs': a_entry.get('motif', []) or [],
                'b_motifs': b_entry.get('motif', []) or [],
                'a_pathos': get_pathos(a_entry),
                'b_pathos': get_pathos(b_entry),
            })
    return expanded

def get_pathos(entry):
    pan = entry.get('panofsky')
    if isinstance(pan, dict):
        ico = pan.get('iconographic')
        if isinstance(ico, dict):
            return ico.get('pathosformel', '')
    return ''

def classify_relation(thread):
    """Infer the most likely relation type from thread attributes."""
    types = []
    
    a_regime, b_regime = thread['a_regime'], thread['b_regime']
    a_country, b_country = thread['a_country'], thread['b_country']
    a_motifs = set(m.lower() for m in thread['a_motifs'])
    b_motifs = set(m.lower() for m in thread['b_motifs'])
    a_score, b_score = thread['a_score'] or 0, thread['b_score'] or 0
    a_year, b_year = thread['a_year'] or 0, thread['b_year'] or 0
    a_pathos, b_pathos = thread['a_pathos'], thread['b_pathos']
    
    # Same regime + same country = serialization or co-presence
    if a_regime == b_regime and a_country == b_country:
        if abs((a_year - b_year)) < 5:
            types.append(('co-presence', 0.8))
        else:
            types.append(('serialization', 0.6))
    
    # Different country, same motif, same regime = translatio
    if a_country != b_country and (a_motifs & b_motifs) and a_regime == b_regime:
        types.append(('translatio', 0.85))
    
    # Same country, fundacional → militar = martialization
    if a_country == b_country and a_year < b_year:
        if a_regime == 'fundacional' and b_regime == 'militar':
            types.append(('martialization', 0.9))
        if a_regime == 'normativo' and b_regime == 'militar':
            types.append(('martialization', 0.7))
    
    # Increasing endurecimento score over time = endurecimento (typed as serialization+genealogy)
    if a_year < b_year and b_score > a_score + 0.3:
        types.append(('genealogy', 0.7))
    
    # contra-alegoria endpoint = satirization
    if a_regime == 'contra-alegoria' or b_regime == 'contra-alegoria':
        types.append(('satirization', 0.85))
        types.append(('inversion', 0.6))
    
    # Shared pathosformel keywords = nachleben
    if a_pathos and b_pathos:
        a_words = set(w.lower() for w in a_pathos.split() if len(w) > 4)
        b_words = set(w.lower() for w in b_pathos.split() if len(w) > 4)
        if a_words & b_words:
            types.append(('nachleben', 0.9))
    
    # Far apart in time, same motif = nachleben
    if abs(a_year - b_year) > 100 and (a_motifs & b_motifs):
        types.append(('nachleben', 0.7))
    
    if not types:
        types.append(('co-presence', 0.3))
    
    types.sort(key=lambda x: -x[1])
    return types

def analyze(threads):
    """Run full analysis on expanded threads."""
    if not threads:
        return None
    
    # Classify each thread
    for t in threads:
        t['relations'] = classify_relation(t)
        t['primary_relation'] = t['relations'][0][0] if t['relations'] else 'unclassified'
    
    # Distributions
    rel_counts = Counter(t['primary_relation'] for t in threads)
    panel_counts = Counter(t['panel_name'] for t in threads)
    
    # Regime pair distribution
    regime_pairs = Counter()
    for t in threads:
        a, b = t['a_regime'] or '?', t['b_regime'] or '?'
        pair = tuple(sorted([a, b]))
        regime_pairs[pair] += 1
    
    # Country pair distribution
    country_pairs = Counter()
    for t in threads:
        a, b = t['a_country'] or '?', t['b_country'] or '?'
        pair = tuple(sorted([a, b]))
        country_pairs[pair] += 1
    
    # Motif co-occurrence in threads
    motif_pairs = Counter()
    for t in threads:
        common = set(m.lower() for m in t['a_motifs']) & set(m.lower() for m in t['b_motifs'])
        for m in common:
            motif_pairs[m] += 1
    
    # Per-regime relation breakdown
    regime_relation = defaultdict(Counter)
    for t in threads:
        for r in [t['a_regime'], t['b_regime']]:
            if r:
                regime_relation[r][t['primary_relation']] += 1
    
    # Average score delta per relation
    score_deltas = defaultdict(list)
    for t in threads:
        if t['a_score'] and t['b_score']:
            score_deltas[t['primary_relation']].append(abs(t['b_score'] - t['a_score']))
    
    return {
        'total_threads': len(threads),
        'relations': dict(rel_counts.most_common()),
        'panels': dict(panel_counts.most_common()),
        'regime_pairs': {f'{a}↔{b}': n for (a,b), n in regime_pairs.most_common()},
        'country_pairs': {f'{a}↔{b}': n for (a,b), n in country_pairs.most_common(10)},
        'shared_motifs': dict(motif_pairs.most_common(15)),
        'regime_relation_matrix': {r: dict(c) for r, c in regime_relation.items()},
        'avg_score_delta': {r: round(sum(v)/len(v), 2) for r, v in score_deltas.items() if v},
        'threads': threads,
    }

# ============================================================================
# Report generation
# ============================================================================

def build_report(analysis, panels):
    if not analysis:
        return "No threads found in input. Either no threads were drawn yet, or the export files contain no thread data.\n"
    
    a = analysis
    md = []
    md.append("# ICONOCRACIA — Relatório de Análise dos Fios Warburg\n")
    md.append(f"_Gerado automaticamente · {a['total_threads']} fios analisados · {len(panels)} painéis_\n")
    md.append("---\n")
    
    md.append("## 1. Visão geral\n")
    md.append(f"Total de fios analisados: **{a['total_threads']}**\n")
    md.append(f"Painéis com fios:\n")
    for p, n in a['panels'].items():
        md.append(f"- {p}: {n} fios")
    md.append("")
    
    md.append("## 2. Distribuição por tipo de relação\n")
    md.append("| Relação | Frequência | % | Definição |")
    md.append("|---|---:|---:|---|")
    total = a['total_threads']
    for rel, n in a['relations'].items():
        pct = round(100*n/total, 1)
        defn = RELATION_TYPES.get(rel, '—')
        md.append(f"| **{rel}** | {n} | {pct}% | {defn} |")
    md.append("")
    
    md.append("## 3. Cruzamento por regime\n")
    md.append("Pares de regime conectados (cada fio é contado uma vez):\n")
    md.append("| Par de regimes | Fios |")
    md.append("|---|---:|")
    for pair, n in a['regime_pairs'].items():
        md.append(f"| {pair} | {n} |")
    md.append("")
    
    md.append("### Matriz regime × relação\n")
    md.append("Qual tipo de relação aparece em cada regime:\n")
    md.append("| Regime | Top relação | 2ª | 3ª |")
    md.append("|---|---|---|---|")
    for r, c in a['regime_relation_matrix'].items():
        top3 = Counter(c).most_common(3)
        cells = [f"{name} ({n})" for name, n in top3]
        while len(cells) < 3: cells.append('—')
        md.append(f"| **{r}** | {cells[0]} | {cells[1]} | {cells[2]} |")
    md.append("")
    
    md.append("## 4. Cruzamento por país\n")
    md.append("Top 10 pares de país nos fios:\n")
    md.append("| Países | Fios |")
    md.append("|---|---:|")
    for pair, n in a['country_pairs'].items():
        md.append(f"| {pair} | {n} |")
    md.append("")
    
    md.append("## 5. Motivos compartilhados\n")
    md.append("Motivos iconográficos comuns aos dois extremos dos fios (top 15):\n")
    md.append("| Motivo | Fios |")
    md.append("|---|---:|")
    for m, n in a['shared_motifs'].items():
        md.append(f"| {m} | {n} |")
    md.append("")
    
    if a['avg_score_delta']:
        md.append("## 6. Delta médio de score por relação\n")
        md.append("Quanto o score de endurecimento varia entre os dois extremos do fio:\n")
        md.append("| Relação | Δ médio |")
        md.append("|---|---:|")
        for r, d in sorted(a['avg_score_delta'].items(), key=lambda x: -x[1]):
            md.append(f"| {r} | {d:.2f} |")
        md.append("")
    
    md.append("## 7. Catálogo completo de fios\n")
    by_panel = defaultdict(list)
    for t in a['threads']:
        by_panel[t['panel_name']].append(t)
    
    for pn, ts in by_panel.items():
        md.append(f"### Painel: {pn} ({len(ts)} fios)\n")
        for t in ts:
            rel = t['primary_relation']
            score = t['relations'][0][1] if t['relations'] else 0
            md.append(f"- **{rel}** ({score:.2f}) · `{t['a_id']}` ({t['a_year'] or '?'}, {t['a_country']}) ↔ `{t['b_id']}` ({t['b_year'] or '?'}, {t['b_country']})")
        md.append("")
    
    return '\n'.join(md)

def build_svg(analysis):
    """Produce a simple network graph SVG."""
    if not analysis or not analysis['threads']:
        return ''
    
    # Collect nodes
    nodes = {}
    for t in analysis['threads']:
        for side in ['a', 'b']:
            nid = t[f'{side}_id']
            if nid not in nodes:
                nodes[nid] = {
                    'id': nid,
                    'regime': t[f'{side}_regime'],
                    'year': t[f'{side}_year'],
                    'country': t[f'{side}_country'],
                    'connections': 0,
                }
            nodes[nid]['connections'] += 1
    
    # Simple layout: position by year (x) and regime (y)
    regime_y = {'fundacional': 100, 'normativo': 300, 'militar': 500, 'contra-alegoria': 700, '': 900}
    year_min = min((n['year'] for n in nodes.values() if n['year']), default=1800)
    year_max = max((n['year'] for n in nodes.values() if n['year']), default=2000)
    year_range = max(year_max - year_min, 1)
    width = 1200
    height = 1000
    
    def x_pos(year):
        if not year: return 100
        return 80 + (year - year_min) / year_range * (width - 160)
    
    def y_pos(regime):
        return regime_y.get(regime, 900)
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="IBM Plex Mono, monospace">']
    svg.append(f'<rect width="{width}" height="{height}" fill="#0E0E10"/>')
    
    # Regime band labels
    for regime, y in regime_y.items():
        if regime:
            svg.append(f'<text x="20" y="{y+5}" fill="#C4A265" font-size="11" font-weight="600">{regime}</text>')
            svg.append(f'<line x1="80" y1="{y}" x2="{width-20}" y2="{y}" stroke="#1f1f21" stroke-width="1" stroke-dasharray="2,4"/>')
    
    # Year axis
    for y_val in range(int(year_min/50)*50, int(year_max/50)*50 + 50, 50):
        x = x_pos(y_val)
        svg.append(f'<line x1="{x}" y1="60" x2="{x}" y2="{height-40}" stroke="#1a1a1c" stroke-width="0.5"/>')
        svg.append(f'<text x="{x}" y="{height-20}" fill="#888076" font-size="9" text-anchor="middle">{y_val}</text>')
    
    # Threads
    rel_colors = {
        'nachleben': '#C4A265', 'mimesis': '#8B7355', 'translatio': '#5EA888',
        'martialization': '#6B2D3E', 'genealogy': '#7A9DD4', 'serialization': '#DCA04E',
        'satirization': '#E07058', 'inversion': '#E07058', 'co-presence': '#444',
    }
    for t in analysis['threads']:
        ax = x_pos(t['a_year']); ay = y_pos(t['a_regime'])
        bx = x_pos(t['b_year']); by = y_pos(t['b_regime'])
        col = rel_colors.get(t['primary_relation'], '#888')
        svg.append(f'<path d="M {ax} {ay} Q {(ax+bx)/2} {(ay+by)/2-30} {bx} {by}" stroke="{col}" stroke-width="1.5" fill="none" opacity="0.55"/>')
    
    # Nodes
    for nid, n in nodes.items():
        x = x_pos(n['year']); y = y_pos(n['regime'])
        col = REGIME_COLORS.get(n['regime'], '#888076')
        r = 4 + min(n['connections'], 8)
        svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#F5F0E8" stroke-width="0.8"/>')
        if n['connections'] >= 3:
            svg.append(f'<text x="{x}" y="{y-r-3}" fill="#F5F0E8" font-size="8" text-anchor="middle">{nid}</text>')
    
    # Legend
    svg.append(f'<text x="20" y="40" fill="#F5F0E8" font-family="Cormorant Garamond, serif" font-size="18" font-weight="600">Atlas Warburg · Rede de Fios Iconocráticos</text>')
    
    legend_x = width - 240
    legend_y = 60
    svg.append(f'<rect x="{legend_x-10}" y="{legend_y-15}" width="240" height="200" fill="#161617" stroke="#2a2a2c"/>')
    svg.append(f'<text x="{legend_x}" y="{legend_y}" fill="#C4A265" font-size="10" font-weight="600">RELAÇÕES (cor do fio)</text>')
    for i, (rel, col) in enumerate(rel_colors.items()):
        y = legend_y + 20 + i * 16
        svg.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x+30}" y2="{y}" stroke="{col}" stroke-width="2"/>')
        svg.append(f'<text x="{legend_x+38}" y="{y+3}" fill="#F5F0E8" font-size="10">{rel}</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

# ============================================================================
# Main
# ============================================================================

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    corpus_path = argv[1]
    print(f"Loading corpus from {corpus_path}…")
    corpus_by_id = load_corpus(corpus_path)
    print(f"  {len(corpus_by_id)} entries indexed.\n")
    
    if '--demo' in argv:
        print("Generating demo panel data (no real threads given)…")
        panels = make_demo_panels(corpus_by_id)
    else:
        panel_paths = [p for p in argv[2:] if p.endswith('.json')]
        if not panel_paths:
            print("No panel JSON files given. Use --demo to see example output.")
            sys.exit(1)
        print(f"Loading {len(panel_paths)} panel file(s)…")
        panels = load_panels(panel_paths)
    
    print(f"  Loaded {len(panels)} panel(s)\n")
    
    threads = expand_threads(panels, corpus_by_id)
    print(f"Expanded {len(threads)} threads with metadata\n")
    
    analysis = analyze(threads)
    
    # Write outputs
    out_dir = Path(__file__).parent
    
    report = build_report(analysis, panels)
    (out_dir / 'thread-analysis-report.md').write_text(report, encoding='utf-8')
    print(f"✓ Wrote thread-analysis-report.md ({len(report)} chars)")
    
    with open(out_dir / 'thread-analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"✓ Wrote thread-analysis.json")
    
    svg = build_svg(analysis)
    if svg:
        (out_dir / 'thread-graph.svg').write_text(svg, encoding='utf-8')
        print(f"✓ Wrote thread-graph.svg")
    
    print(f"\n=== Quick summary ===")
    if analysis:
        print(f"Total threads: {analysis['total_threads']}")
        print(f"Top relations:")
        for rel, n in list(analysis['relations'].items())[:5]:
            print(f"  {rel}: {n}")

if __name__ == '__main__':
    main(sys.argv)
