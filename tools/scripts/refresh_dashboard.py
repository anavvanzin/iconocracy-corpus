#!/usr/bin/env python3
"""Refresh dashboard HTML files by re-embedding the latest corpus and agent data.

Usage:
    python tools/scripts/refresh_dashboard.py           # refresh both dashboards
    python tools/scripts/refresh_dashboard.py --corpus   # refresh corpus dashboard only
    python tools/scripts/refresh_dashboard.py --agents   # refresh agents dashboard only

Idempotent — safe to run multiple times.
"""
import argparse
import json
import os
import re

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
CORPUS_JSON = os.path.join(REPO_ROOT, 'corpus', 'corpus-data.json')
AGENT_RUNS = os.path.join(REPO_ROOT, 'corpus', 'agent-runs.json')
CORPUS_HTML = os.path.join(REPO_ROOT, 'corpus', 'DASHBOARD_CORPUS.html')
AGENTS_HTML = os.path.join(REPO_ROOT, 'corpus', 'DASHBOARD_AGENTS.html')

# Fields to keep in compact corpus data
KEEP_FIELDS = [
    'id', 'title', 'date', 'year', 'country_pt', 'country', 'medium_norm',
    'support', 'period_norm', 'regime', 'endurecimento_score', 'indicadores',
    'motif', 'motif_str', 'tags', 'tags_str', 'description', 'url',
    'thumbnail_url', 'source_archive', 'creator', 'institution',
    'coded_by', 'coded_at', 'in_scope', 'citation_abnt'
]


def compact_corpus(data):
    """Strip corpus data to dashboard-relevant fields."""
    compact = []
    for item in data:
        c = {k: item.get(k) for k in KEEP_FIELDS}
        compact.append(c)
    return compact


def replace_data_block(html, var_name, new_data_json):
    """Replace `const VAR = [...];` or `const VAR = {...};` in HTML."""
    pattern = rf'(const\s+{var_name}\s*=\s*)(\[[\s\S]*?\]|\{{[\s\S]*?\}});'
    match = re.search(pattern, html)
    if match:
        return html[:match.start(2)] + new_data_json + html[match.end(2):]
    print(f"  WARNING: Could not find 'const {var_name} = ...' block")
    return html


def refresh_corpus_dashboard():
    """Re-embed corpus-data.json into DASHBOARD_CORPUS.html."""
    if not os.path.exists(CORPUS_JSON):
        print(f"ERROR: {CORPUS_JSON} not found")
        return False
    if not os.path.exists(CORPUS_HTML):
        print(f"ERROR: {CORPUS_HTML} not found")
        return False

    with open(CORPUS_JSON, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    compact = compact_corpus(corpus)
    data_js = json.dumps(compact, ensure_ascii=False, separators=(',', ':'))

    with open(CORPUS_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    html = replace_data_block(html, 'DATA', data_js)

    with open(CORPUS_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Corpus dashboard refreshed: {len(compact)} items, {len(html):,} bytes")
    return True


def refresh_agents_dashboard():
    """Re-embed agent-runs.json into DASHBOARD_AGENTS.html."""
    if not os.path.exists(AGENTS_HTML):
        print(f"ERROR: {AGENTS_HTML} not found")
        return False

    runs = []
    if os.path.exists(AGENT_RUNS):
        with open(AGENT_RUNS, 'r', encoding='utf-8') as f:
            runs = json.load(f)

    runs_js = json.dumps(runs, ensure_ascii=False, separators=(',', ':'))

    with open(AGENTS_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    html = replace_data_block(html, 'RUNS', runs_js)

    with open(AGENTS_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Agents dashboard refreshed: {len(runs)} runs, {len(html):,} bytes")
    return True


def main():
    parser = argparse.ArgumentParser(description='Refresh dashboard HTML files')
    parser.add_argument('--corpus', action='store_true', help='Refresh corpus dashboard only')
    parser.add_argument('--agents', action='store_true', help='Refresh agents dashboard only')
    args = parser.parse_args()

    do_both = not args.corpus and not args.agents
    results = []

    if do_both or args.corpus:
        results.append(('corpus', refresh_corpus_dashboard()))
    if do_both or args.agents:
        results.append(('agents', refresh_agents_dashboard()))

    ok = all(r[1] for r in results)
    summary = ', '.join(f'{r[0]}:{"OK" if r[1] else "FAIL"}' for r in results)
    print(f"\nResult: {summary}")
    return {
        'status': 'success' if ok else 'error',
        'summary': f'Dashboard refresh: {summary}',
        'next_actions': [] if ok else ['Check file paths and permissions'],
        'artifacts': [CORPUS_HTML, AGENTS_HTML]
    }


if __name__ == '__main__':
    main()
