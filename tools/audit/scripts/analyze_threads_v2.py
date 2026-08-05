#!/usr/bin/env python3
"""
ICONOCRACIA — Warburg Thread Analyzer v2
=========================================

Consumes panel JSON exports + corpus and produces relational analysis
grounded in the iconocratic-relations taxonomy v0.2.

Key changes from v1:
- Supports CHAIN relations (≥3 items) for Endurecimento progressivo
- Multi-type classification: up to 3 ordered types per binary link
- Sub-type expansion: Genealogia, Translatio, Inversão, Contradição
- Semantic flags: institutional_transmission, colonial_register, diachronic, internal_to_country, cross_regime

Usage:
    python analyze_threads_v2.py corpus.json --demo
    python analyze_threads_v2.py corpus.json painel-1.json painel-2.json ...

Outputs:
    thread-analysis-report.md
    thread-analysis.json
    thread-graph.svg
    chain-analysis.md           (new — dedicated chain report)
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
# Composto aposentado no codebook v2.2.1 (DEC-2026-07-28): ordenação e
# comparação passam a usar o inventário de atributos, não o escore agregado.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tools.scripts.lpai_indicators import attribute_count, attribute_inventory  # noqa: E402


# ============================================================================
# TAXONOMY v0.2 — full type system
# ============================================================================

RELATION_TYPES = {
    'nachleben':                {'family': 'I',  'name': 'Nachleben'},
    'mimesis':                  {'family': 'I',  'name': 'Mimesis'},
    'genealogia_canonica':      {'family': 'I',  'name': 'Genealogia canônica'},
    'genealogia_tensional':     {'family': 'I',  'name': 'Genealogia tensional'},
    'genealogia_ascendente':    {'family': 'I',  'name': 'Genealogia ascendente'},
    'serializacao':             {'family': 'I',  'name': 'Serialização'},
    'translatio_republicana':   {'family': 'II', 'name': 'Translatio republicana'},
    'translatio_imperial':      {'family': 'II', 'name': 'Translatio imperial'},
    'translatio_fundacional':   {'family': 'II', 'name': 'Translatio fundacional'},
    'concretizacao':            {'family': 'II', 'name': 'Concretização'},
    'par_genderizado':          {'family': 'II', 'name': 'Par genderizado'},
    'inversao_sincronica':      {'family': 'III','name': 'Inversão sincrônica'},
    'inversao_diacronica':      {'family': 'III','name': 'Inversão diacrônica'},
    'satirizacao':              {'family': 'III','name': 'Satirização'},
    'contradicao_intra':        {'family': 'III','name': 'Contradição intra-nacional'},
    'contradicao_transnacional':{'family': 'III','name': 'Contradição transnacional'},
    'contradicao_colonial':     {'family': 'III','name': 'Contradição colonial'},
    'martializacao':            {'family': 'IV', 'name': 'Martialização'},
    'desmilitarizacao':         {'family': 'IV', 'name': 'Desmilitarização'},
    'copresenca_politica':      {'family': 'V',  'name': 'Co-presença política'},
    'copresenca_institucional': {'family': 'V',  'name': 'Co-presença institucional'},
}

CHAIN_RELATIONS = {
    'endurecimento_progressivo':  {'name': 'Endurecimento progressivo', 'min_items': 3},
    'endurecimento_cross_country':{'name': 'Endurecimento transnacional', 'min_items': 3},
    'constelacao_temporal':       {'name': 'Constelação temporal', 'min_items': 3},
}

FLAGS = ['institutional_transmission', 'colonial_register', 'diachronic',
         'internal_to_country', 'cross_regime']

COLONIAL_ID_PREFIXES = ('BE-CONGO', 'FR-PIAST', 'UK-TRADE')
COLONIAL_KEYWORDS = ['colonial', 'colonie', 'congo', 'império', 'empire']

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
        try:
            with open(p, encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'panelId' in data:
                panels.append(data)
            elif isinstance(data, dict) and 'panels' in data:
                for pid, pdata in data['panels'].items():
                    panels.append({
                        'panelId': int(pid),
                        'panelName': pdata.get('panelName', f'Panel {pid}'),
                        'placements': pdata.get('placements', []),
                        'threads': pdata.get('threads', []),
                        'chains': pdata.get('chains', []),
                        'essay': pdata.get('essay', {}),
                    })
        except Exception as e:
            print(f"⚠ Failed to load {p}: {e}", file=sys.stderr)
    return panels

# ============================================================================
# Flag detection
# ============================================================================

def is_colonial(entry):
    if not entry: return False
    eid = entry.get('id', '')
    if any(eid.startswith(p) for p in COLONIAL_ID_PREFIXES):
        return True
    title_desc = (entry.get('title','') + ' ' + str(entry.get('description',''))).lower()
    if any(k in title_desc for k in COLONIAL_KEYWORDS):
        return True
    return False

def detect_flags(a_entry, b_entry, panel=None):
    flags = []
    a_year = a_entry.get('year') or 0
    b_year = b_entry.get('year') or 0
    delta_year = abs(a_year - b_year)
    a_country = a_entry.get('country', '')
    b_country = b_entry.get('country', '')
    a_regime = a_entry.get('regime', '')
    b_regime = b_entry.get('regime', '')

    if delta_year > 25:
        flags.append('diachronic')
    if a_country and a_country == b_country:
        flags.append('internal_to_country')
    if a_regime and b_regime and a_regime != b_regime:
        flags.append('cross_regime')
    if is_colonial(a_entry) or is_colonial(b_entry):
        flags.append('colonial_register')

    # institutional_transmission cannot be auto-detected reliably
    # (requires archival evidence); only set if manually flagged in panel data

    return flags

# ============================================================================
# Score helpers
# ============================================================================

def semantic_score(a_entry, b_entry):
    a_motifs = a_entry.get('motif', []) or []
    b_motifs = b_entry.get('motif', []) or []
    if isinstance(a_motifs, str): a_motifs = [a_motifs]
    if isinstance(b_motifs, str): b_motifs = [b_motifs]
    a_set = set(str(m).lower() for m in a_motifs)
    b_set = set(str(m).lower() for m in b_motifs)
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / max(len(a_set | b_set), 1)

def temporal_score(a_entry, b_entry, relation_type):
    a_year = a_entry.get('year') or 0
    b_year = b_entry.get('year') or 0
    delta = abs(a_year - b_year)
    if relation_type == 'nachleben':
        return min(delta / 100.0, 1.0)
    if relation_type == 'mimesis':
        return max(1.0 - delta / 50.0, 0.0)
    if relation_type in ('serializacao',):
        return max(1.0 - delta / 25.0, 0.0)
    if relation_type.startswith('inversao_sincronica'):
        return max(1.0 - delta / 25.0, 0.0)
    if relation_type.startswith('inversao_diacronica'):
        return min(delta / 50.0, 1.0)
    return 0.5

def regime_score(a_entry, b_entry, relation_type):
    a_r = a_entry.get('regime', '') or 'unknown'
    b_r = b_entry.get('regime', '') or 'unknown'
    if relation_type == 'martializacao':
        if a_r in ('fundacional', 'normativo') and b_r == 'militar':
            return 0.95
        if a_r == 'militar' and b_r in ('fundacional', 'normativo'):
            return 0.3  # wrong direction
        return 0.0
    if relation_type == 'desmilitarizacao':
        if a_r == 'militar' and b_r in ('fundacional', 'normativo'):
            return 0.95
        return 0.0
    if relation_type.startswith('translatio'):
        if a_r == b_r and a_r:
            return 0.85
        return 0.4
    if relation_type.startswith('contradicao'):
        return 0.7  # contradiction allows any regime pairing
    if relation_type.startswith('genealogia'):
        return 0.6
    if relation_type == 'serializacao':
        if a_r == b_r:
            return 0.9
        return 0.4
    return 0.5

# ============================================================================
# Multi-type classification (v0.2)
# ============================================================================

def classify_binary(thread, corpus_by_id):
    """Return list of (type_id, confidence) tuples, sorted by confidence descending."""
    a = corpus_by_id.get(thread['a_id'], {})
    b = corpus_by_id.get(thread['b_id'], {})
    if not a or not b:
        return [('unclassified', 0.1)]

    flags = detect_flags(a, b)
    candidates = []

    a_year = a.get('year') or 0
    b_year = b.get('year') or 0
    delta_year = abs(a_year - b_year)
    a_country = a.get('country', '')
    b_country = b.get('country', '')
    a_regime = a.get('regime', '')
    b_regime = b.get('regime', '')
    a_motifs = set(str(m).lower() for m in (a.get('motif') or []))
    b_motifs = set(str(m).lower() for m in (b.get('motif') or []))
    shared_motifs = a_motifs & b_motifs
    sem_score = semantic_score(a, b)

    # === Sub-types of Genealogia ===
    if 'internal_to_country' in flags and 'cross_regime' in flags:
        a_attrs = attribute_count(a)
        b_attrs = attribute_count(b)
        if a_year < b_year and b_attrs > a_attrs:
            candidates.append(('genealogia_ascendente', 0.85))
    if a_regime == 'contra-alegoria' or b_regime == 'contra-alegoria':
        if shared_motifs and delta_year < 100:
            candidates.append(('genealogia_tensional', 0.75))
    if shared_motifs and a_regime == b_regime and a_regime in ('normativo', 'fundacional'):
        if delta_year > 25:
            candidates.append(('genealogia_canonica', 0.7))

    # === Nachleben ===
    if 'diachronic' in flags and delta_year > 50 and shared_motifs:
        candidates.append(('nachleben', 0.85))

    # === Mimesis ===
    if delta_year <= 50 and sem_score > 0.5 and 'internal_to_country' in flags:
        candidates.append(('mimesis', 0.8))

    # === Serialização ===
    if a_regime == b_regime and a_regime and 'internal_to_country' in flags:
        if delta_year <= 25:
            candidates.append(('serializacao', 0.75))

    # === Sub-types of Translatio ===
    if a_country and b_country and a_country != b_country and shared_motifs:
        if 'colonial_register' in flags:
            candidates.append(('translatio_imperial', 0.85))
        elif a_regime == 'fundacional' and b_regime == 'fundacional':
            candidates.append(('translatio_fundacional', 0.85))
        else:
            candidates.append(('translatio_republicana', 0.8))

    # === Sub-types of Contradição ===
    if 'colonial_register' in flags and 'internal_to_country' in flags:
        candidates.append(('contradicao_colonial', 0.9))
    elif 'colonial_register' in flags and a_country != b_country:
        candidates.append(('contradicao_transnacional', 0.7))
    elif a_country and a_country == b_country and a_regime != b_regime:
        candidates.append(('contradicao_intra', 0.55))

    # === Sub-types of Inversão ===
    if (a_regime == 'contra-alegoria') != (b_regime == 'contra-alegoria'):
        # exactly one side is contra-alegoria → inversion
        if 'diachronic' in flags:
            candidates.append(('inversao_diacronica', 0.75))
        else:
            candidates.append(('inversao_sincronica', 0.7))

    # === Satirização ===
    if a_regime == 'contra-alegoria' or b_regime == 'contra-alegoria':
        candidates.append(('satirizacao', 0.7))

    # === Martialização / Desmilitarização ===
    if a_year < b_year:
        if a_regime in ('fundacional', 'normativo') and b_regime == 'militar':
            candidates.append(('martializacao', 0.9))
        if a_regime == 'militar' and b_regime in ('fundacional', 'normativo'):
            candidates.append(('desmilitarizacao', 0.85))
    else:
        if b_regime in ('fundacional', 'normativo') and a_regime == 'militar':
            candidates.append(('desmilitarizacao', 0.85))

    # === Par genderizado === (can't auto-detect from current corpus; skip)

    # === Co-presença política ===
    if a_country and a_country != b_country and not shared_motifs and delta_year < 25:
        candidates.append(('copresenca_politica', 0.6))

    # === Co-presença institucional ===
    a_arch = a.get('source_archive', '') or a.get('institution', '')
    b_arch = b.get('source_archive', '') or b.get('institution', '')
    if a_arch and a_arch == b_arch and not shared_motifs:
        if 'colonial_register' not in flags:
            candidates.append(('copresenca_institucional', 0.7))
        # If colonial, contradicao_colonial already covers it

    if not candidates:
        candidates.append(('copresenca_politica', 0.3))

    # Sort by confidence descending, deduplicate by type_id keeping highest
    seen = {}
    for tid, score in candidates:
        if tid not in seen or score > seen[tid]:
            seen[tid] = score
    sorted_c = sorted(seen.items(), key=lambda x: -x[1])

    return sorted_c, flags

# ============================================================================
# Chain detection
# ============================================================================

def classify_chain(chain, corpus_by_id):
    """A chain is a list of placement uids forming an ordered sequence (≥3)."""
    item_ids = chain.get('item_ids', [])
    if len(item_ids) < 3:
        return [('not_a_chain', 0.0)]

    entries = [corpus_by_id.get(iid, {}) for iid in item_ids]
    entries = [e for e in entries if e]
    if len(entries) < 3:
        return [('incomplete_chain', 0.0)]

    years = [e.get('year') or 0 for e in entries]
    attrs = [attribute_count(e) for e in entries]
    countries = [e.get('country', '') for e in entries]

    if not all(years[i] <= years[i+1] for i in range(len(years)-1)):
        return [('chain_unordered_temporally', 0.2)]

    candidates = []

    # Endurecimento progressivo (strict monotonic OR with militar inflection)
    # Acréscimo de atributos ao longo da cadeia — cardinalidade, não curva.
    monotonic_score = all(attrs[i] <= attrs[i+1] for i in range(len(attrs)-1))
    regimes = [e.get('regime', '') for e in entries]

    # Detect 'militar inflection': cadeia que acumula atributos até atingir regime
    # militar, depois pode quebrar (o regime militar tende a reduzir o número de
    # atributos marcados por mobilização tópica)
    has_militar_inflection = False
    if 'militar' in regimes:
        idx_first_militar = regimes.index('militar')
        pre_militar = attrs[:idx_first_militar]  # excludes militar item itself
        if len(pre_militar) >= 2 and all(pre_militar[i] <= pre_militar[i+1] for i in range(len(pre_militar)-1)):
            if pre_militar[-1] - pre_militar[0] >= 1:
                has_militar_inflection = True

    # Deltas em CONTAGEM de atributos (inteiros), não em média de escore.
    delta_pre_max = max(attrs) - attrs[0] if len(attrs) >= 2 else 0
    delta_total = attrs[-1] - attrs[0] if len(attrs) >= 2 else 0

    if monotonic_score and delta_total >= 2:
        if len(set(countries)) >= 2:
            candidates.append(('endurecimento_cross_country', 0.9))
        else:
            candidates.append(('endurecimento_progressivo', 0.95))
    elif has_militar_inflection and delta_pre_max >= 2:
        # Cadeia válida com inflexão militar
        if len(set(countries)) >= 2:
            candidates.append(('endurecimento_cross_country', 0.8))
        else:
            candidates.append(('endurecimento_progressivo', 0.85))

    # Constelação temporal
    if not monotonic_score and (max(years) - min(years)) <= 30:
        candidates.append(('constelacao_temporal', 0.7))

    if not candidates:
        candidates.append(('weak_chain', 0.3))

    return sorted(candidates, key=lambda x: -x[1])

# ============================================================================
# Expansion
# ============================================================================

def expand_threads_v2(panels, corpus_by_id):
    binary, chains = [], []
    for panel in panels:
        plac_by_uid = {p['uid']: p for p in panel.get('placements', [])}

        # Binary threads
        for t in panel.get('threads', []):
            a_uid, b_uid = t.get('a'), t.get('b')
            if a_uid not in plac_by_uid or b_uid not in plac_by_uid:
                continue
            a_id = plac_by_uid[a_uid].get('id')
            b_id = plac_by_uid[b_uid].get('id')
            thread = {
                'panel_id': panel.get('panelId'),
                'panel_name': panel.get('panelName'),
                'thread_uid': t.get('uid'),
                'a_id': a_id, 'b_id': b_id,
                'manual_primary': t.get('manual_primary', ''),
                'manual_secondary': t.get('manual_secondary', ''),
                'manual_tertiary': t.get('manual_tertiary', ''),
                'manual_flags': t.get('manual_flags', []),
            }
            classifications, flags = classify_binary(thread, corpus_by_id)
            thread['auto_classifications'] = classifications
            thread['auto_primary'] = classifications[0][0] if classifications else 'unclassified'
            thread['auto_primary_confidence'] = classifications[0][1] if classifications else 0
            thread['detected_flags'] = flags
            thread['all_classifications_above_0_5'] = [c for c in classifications if c[1] >= 0.5]
            binary.append(thread)

        # Chains
        for c in panel.get('chains', []):
            item_uids = c.get('item_uids', [])
            item_ids = [plac_by_uid.get(uid, {}).get('id') for uid in item_uids]
            item_ids = [i for i in item_ids if i]
            if len(item_ids) < 3:
                continue
            chain = {
                'panel_id': panel.get('panelId'),
                'panel_name': panel.get('panelName'),
                'chain_uid': c.get('uid'),
                'item_ids': item_ids,
                'manual_primary': c.get('manual_primary', ''),
            }
            classifications = classify_chain(chain, corpus_by_id)
            chain['auto_classifications'] = classifications
            chain['auto_primary'] = classifications[0][0] if classifications else 'unclassified'
            chains.append(chain)

    return binary, chains

# ============================================================================
# Demo generator
# ============================================================================

def make_demo_panels(corpus_by_id):
    """Synthetic panels including a CHAIN for endurecimento."""
    panels = []

    # Panel 4 with both binary threads and a CHAIN
    chain_items = ['FR-015', 'FR-013', 'FR-018', 'FR-SEM-1898', 'FR-008', 'FR-007']
    chain_items = [c for c in chain_items if c in corpus_by_id]
    placements = [{'uid': f'p-4-{i}', 'id': cid, 'x': 200+i*150, 'y': 300}
                  for i, cid in enumerate(chain_items)]
    panels.append({
        'panelId': 4, 'panelName': 'ENDURECIMENTO',
        'placements': placements,
        'threads': [
            {'uid': 't-4-0', 'a': 'p-4-3', 'b': 'p-4-4', 'manual_primary': 'martializacao'},
        ],
        'chains': [
            {'uid': 'c-4-0', 'item_uids': [p['uid'] for p in placements[:5]],
             'manual_primary': 'endurecimento_progressivo'},
        ],
    })

    # Panel 6 with colonial contradiction
    p6_items = ['BE-002', 'BE-CONGO-100F-1912', 'BE-CONGO-1912', 'BE-CONGO-MON-1921']
    p6_items = [c for c in p6_items if c in corpus_by_id]
    placements6 = [{'uid': f'p-6-{i}', 'id': cid, 'x': 200+i*180, 'y': 300}
                   for i, cid in enumerate(p6_items)]
    panels.append({
        'panelId': 6, 'panelName': 'Balança e Império',
        'placements': placements6,
        'threads': [
            {'uid': 't-6-0', 'a': 'p-6-0', 'b': 'p-6-3', 'manual_primary': 'contradicao_colonial'},
            {'uid': 't-6-1', 'a': 'p-6-1', 'b': 'p-6-2', 'manual_primary': 'mimesis'},
        ],
        'chains': [],
    })

    # Panel 8 with tensional clustering
    p8_items = ['FR-031', 'FR-033', 'US-019', 'FR-022']
    p8_items = [c for c in p8_items if c in corpus_by_id]
    placements8 = [{'uid': f'p-8-{i}', 'id': cid, 'x': 200+i*180, 'y': 300}
                   for i, cid in enumerate(p8_items)]
    panels.append({
        'panelId': 8, 'panelName': 'Fissuras',
        'placements': placements8,
        'threads': [
            {'uid': 't-8-0', 'a': 'p-8-0', 'b': 'p-8-1',
             'manual_primary': 'satirizacao', 'manual_secondary': 'contradicao_intra'},
            {'uid': 't-8-1', 'a': 'p-8-2', 'b': 'p-8-3',
             'manual_primary': 'genealogia_tensional', 'manual_secondary': 'contradicao_transnacional'},
        ],
        'chains': [],
    })

    return panels

# ============================================================================
# Reporting
# ============================================================================

def analyze(binary, chains):
    n_binary = len(binary)
    n_chains = len(chains)

    # Concordance manual vs auto
    concordance_full = 0
    concordance_partial = 0
    no_manual = 0
    for t in binary:
        manual = t.get('manual_primary', '')
        if not manual:
            no_manual += 1
            continue
        auto_primary = t.get('auto_primary', '')
        auto_above = [c[0] for c in t.get('all_classifications_above_0_5', [])]
        if manual == auto_primary:
            concordance_full += 1
        elif manual in auto_above:
            concordance_partial += 1

    # Family distribution
    fam_counts = Counter()
    for t in binary:
        ap = t.get('auto_primary')
        if ap in RELATION_TYPES:
            fam_counts[RELATION_TYPES[ap]['family']] += 1

    # Flag distribution
    flag_counts = Counter()
    for t in binary:
        for f in t.get('detected_flags', []):
            flag_counts[f] += 1

    # Multi-type rate
    multi_type_count = sum(1 for t in binary if len(t.get('all_classifications_above_0_5', [])) >= 2)

    # Per-relation breakdown
    rel_counts = Counter(t.get('auto_primary', 'unclassified') for t in binary)

    # Chain primary counts
    chain_counts = Counter(c.get('auto_primary', 'unclassified') for c in chains)

    return {
        'n_binary': n_binary,
        'n_chains': n_chains,
        'concordance_full': concordance_full,
        'concordance_partial': concordance_partial,
        'concordance_no_manual': no_manual,
        'family_distribution': dict(fam_counts),
        'flag_distribution': dict(flag_counts),
        'multi_type_count': multi_type_count,
        'multi_type_rate': round(100 * multi_type_count / max(n_binary,1), 1),
        'relation_counts': dict(rel_counts.most_common()),
        'chain_counts': dict(chain_counts),
    }

def build_report(binary, chains, analysis, panels):
    md = []
    md.append("# ICONOCRACIA — Relatório de Análise dos Fios Warburg (v0.2)\n")
    md.append(f"_Gerado automaticamente · {analysis['n_binary']} fios binários · {analysis['n_chains']} cadeias · {len(panels)} painéis_\n")
    md.append("---\n")

    md.append("## 1. Resumo executivo\n")
    md.append(f"- **Fios binários**: {analysis['n_binary']}")
    md.append(f"- **Cadeias (chains)**: {analysis['n_chains']}")
    n_with_manual = analysis['n_binary'] - analysis['concordance_no_manual']
    if n_with_manual > 0:
        c_full_pct = round(100 * analysis['concordance_full'] / n_with_manual, 1)
        c_partial_pct = round(100 * analysis['concordance_partial'] / n_with_manual, 1)
        md.append(f"- **Concordância manual vs. automática**: {analysis['concordance_full']}/{n_with_manual} plena ({c_full_pct}%) + {analysis['concordance_partial']}/{n_with_manual} parcial ({c_partial_pct}%)")
    md.append(f"- **Multi-tipo** (≥2 classificações com confiança ≥0.5): {analysis['multi_type_count']}/{analysis['n_binary']} ({analysis['multi_type_rate']}%)")
    md.append("")

    md.append("## 2. Distribuição por família taxonômica\n")
    fam_names = {'I':'I. Genealógicas','II':'II. Estruturais','III':'III. Tensionais','IV':'IV. Transicionais','V':'V. Sincrônicas'}
    md.append("| Família | Fios | % |")
    md.append("|---|---:|---:|")
    total = analysis['n_binary']
    for f, n in sorted(analysis['family_distribution'].items()):
        pct = round(100*n/max(total,1), 1)
        md.append(f"| {fam_names.get(f, f)} | {n} | {pct}% |")
    md.append("")

    md.append("## 3. Distribuição de flags semânticos\n")
    md.append("| Flag | Frequência |")
    md.append("|---|---:|")
    for flag, n in sorted(analysis['flag_distribution'].items(), key=lambda x: -x[1]):
        md.append(f"| {flag} | {n} |")
    md.append("")

    md.append("## 4. Tipos de relação detectados (auto-classificação primária)\n")
    md.append("| Tipo | Família | Fios |")
    md.append("|---|---|---:|")
    for rel, n in analysis['relation_counts'].items():
        fam = RELATION_TYPES.get(rel, {}).get('family', '—')
        name = RELATION_TYPES.get(rel, {}).get('name', rel)
        md.append(f"| {name} | {fam} | {n} |")
    md.append("")

    if chains:
        md.append("## 5. Cadeias (CHAIN — relações ternárias)\n")
        md.append(f"Total: {analysis['n_chains']} cadeias.\n")
        md.append("| Tipo | Cadeias |")
        md.append("|---|---:|")
        for tid, n in analysis['chain_counts'].items():
            name = CHAIN_RELATIONS.get(tid, {}).get('name', tid)
            md.append(f"| {name} | {n} |")
        md.append("")
        md.append("### Detalhes\n")
        for c in chains:
            primary = c.get('auto_primary')
            primary_name = CHAIN_RELATIONS.get(primary, {}).get('name', primary)
            md.append(f"- **{c['panel_name']}** · {primary_name}: `{' → '.join(c['item_ids'])}`")
        md.append("")

    md.append("## 6. Catálogo completo de fios binários\n")
    by_panel = defaultdict(list)
    for t in binary:
        by_panel[t['panel_name']].append(t)
    for pn, ts in by_panel.items():
        md.append(f"### {pn} ({len(ts)} fios)\n")
        for t in ts:
            primary_id = t['auto_primary']
            primary_name = RELATION_TYPES.get(primary_id, {}).get('name', primary_id)
            confidence = t.get('auto_primary_confidence', 0)
            multi = ', '.join(RELATION_TYPES.get(c[0], {}).get('name', c[0])
                              for c in t.get('all_classifications_above_0_5', [])[:3])
            flags_str = ', '.join(t.get('detected_flags', []))
            manual = t.get('manual_primary', '—')
            md.append(f"- `{t['a_id']}` ↔ `{t['b_id']}` · auto: **{primary_name}** ({confidence:.2f}) · multi: [{multi}] · flags: [{flags_str}] · manual: {manual}")
        md.append("")

    return '\n'.join(md)

def build_chain_report(chains, corpus_by_id):
    md = ["# Análise das Cadeias (CHAIN) — v0.2\n"]
    md.append(f"_{len(chains)} cadeias analisadas_\n")
    md.append("---\n")
    for c in chains:
        primary = c.get('auto_primary')
        primary_name = CHAIN_RELATIONS.get(primary, {}).get('name', primary)
        md.append(f"## {c['panel_name']} · {primary_name}\n")
        md.append(f"**Cadeia:** `{' → '.join(c['item_ids'])}`\n")
        md.append(f"**Manual:** {c.get('manual_primary', '—')}\n")
        scores_str = ''
        for iid in c['item_ids']:
            e = corpus_by_id.get(iid, {})
            scores_str += (f"- `{iid}` ({e.get('year','?')}) · {e.get('regime','-')} · "
                           f"⬥{attribute_count(e)} atributos"
                           + (f" [{', '.join(attribute_inventory(e))}]" if attribute_inventory(e) else "")
                           + f" · {e.get('country','-')}\n")
        md.append("**Itens:**\n" + scores_str + "\n")
    return '\n'.join(md)

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
    print(f"  {len(corpus_by_id)} entries\n")

    if '--demo' in argv:
        print("Generating demo with chains + binary threads…")
        panels = make_demo_panels(corpus_by_id)
    else:
        panel_paths = [p for p in argv[2:] if p.endswith('.json') and p != corpus_path]
        if not panel_paths:
            print("No panel JSONs given. Use --demo for example output.")
            sys.exit(1)
        panels = load_panels(panel_paths)

    binary, chains = expand_threads_v2(panels, corpus_by_id)
    print(f"Expanded {len(binary)} binary threads + {len(chains)} chains\n")

    analysis = analyze(binary, chains)

    out_dir = Path(__file__).parent
    (out_dir / 'thread-analysis-report.md').write_text(
        build_report(binary, chains, analysis, panels), encoding='utf-8')
    (out_dir / 'thread-analysis.json').write_text(
        json.dumps({'binary': binary, 'chains': chains, 'analysis': analysis},
                   ensure_ascii=False, indent=2), encoding='utf-8')
    if chains:
        (out_dir / 'chain-analysis.md').write_text(
            build_chain_report(chains, corpus_by_id), encoding='utf-8')

    print("=== Summary ===")
    print(f"Binary threads: {analysis['n_binary']}")
    print(f"Chains: {analysis['n_chains']}")
    print(f"Multi-type rate: {analysis['multi_type_rate']}%")
    if analysis['concordance_full'] + analysis['concordance_partial'] > 0:
        n_with_manual = analysis['n_binary'] - analysis['concordance_no_manual']
        if n_with_manual > 0:
            print(f"Concordance: {analysis['concordance_full']}/{n_with_manual} full, {analysis['concordance_partial']}/{n_with_manual} partial")
    print(f"\n✓ Reports written")

if __name__ == '__main__':
    main(sys.argv)
