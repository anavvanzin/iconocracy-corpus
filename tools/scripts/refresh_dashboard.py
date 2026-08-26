#!/usr/bin/env python3
"""Refresh dashboard HTML: embute corpus + agent-runs entre delimitadores.

Uso:
    python tools/scripts/refresh_dashboard.py           # corpus + agents
    python tools/scripts/refresh_dashboard.py --corpus
    python tools/scripts/refresh_dashboard.py --agents

Idempotente: rodar 2x produz arquivo idêntico. Falha alto (exit 1) se os
delimitadores estiverem ausentes/duplicados ou se o round-trip divergir.
"""
import argparse
import json
import sys
from pathlib import Path

from dashboard_data import build_dataset, load_records_index

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BEGIN = "// == DATA:BEGIN =="
END = "// == DATA:END =="
KEEP_FIELDS = [
    'id', 'title', 'date', 'year', 'country_pt', 'country', 'medium_norm',
    'support', 'period_norm', 'regime', 'endurecimento_score', 'indicadores',
    'motif', 'motif_str', 'tags', 'tags_str', 'description', 'url',
    'thumbnail_url', 'source_archive', 'creator', 'institution',
    'coded_by', 'coded_at', 'in_scope', 'citation_abnt'
]


def _load_json(path, default):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _embed_block(html: str, block: str) -> str:
    if html.count(BEGIN) != 1 or html.count(END) != 1:
        sys.exit(f"ERRO: delimitadores ausentes ou duplicados "
                 f"(BEGIN={html.count(BEGIN)}, END={html.count(END)})")
    pre, rest = html.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{BEGIN}\n{block}{END}{post}"


def _roundtrip_check(html: str, expected_items: int) -> None:
    for line in html.splitlines():
        if line.startswith("const DATA = "):
            data = json.loads(line[len("const DATA = "):].rstrip().rstrip(";"))
            if len(data) != expected_items:
                sys.exit(f"ERRO round-trip: embutido {len(data)} != fonte {expected_items}")
            return
    sys.exit("ERRO round-trip: const DATA não encontrada após embed")


def refresh_corpus_dashboard(repo_root: Path) -> dict:
    repo_root = Path(repo_root)
    corpus = _load_json(repo_root / "corpus" / "corpus-data.json", [])
    items = corpus if isinstance(corpus, list) else corpus.get("items") or corpus.get("records") or []
    compact = [{k: it.get(k) for k in KEEP_FIELDS} for it in items]
    index = load_records_index(repo_root / "data" / "processed" / "records.jsonl")
    dataset = build_dataset(compact, index)
    agent_runs = _load_json(repo_root / "corpus" / "agent-runs.json", [])
    n_year = sum(1 for d in dataset if d.get("year"))
    meta = {"items": len(dataset),
            "year_coverage": round(n_year / len(dataset), 3) if dataset else 0,
            "source": "corpus-data.json"}

    block = (
        "const DATA = " + json.dumps(dataset, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "const AGENT_RUNS = " + json.dumps(agent_runs, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "const META = " + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n"
    )
    html_path = repo_root / "corpus" / "DASHBOARD_CORPUS.html"
    html = html_path.read_text(encoding="utf-8")
    new_html = _embed_block(html, block)
    _roundtrip_check(new_html, len(dataset))
    html_path.write_text(new_html, encoding="utf-8")
    print(f"Corpus dashboard refreshed: {len(dataset)} items, year_coverage {meta['year_coverage']:.1%}")
    return {"items": len(dataset), "bytes": len(new_html.encode("utf-8"))}


def refresh_agents_dashboard(repo_root: Path) -> dict:
    """Mantido por compatibilidade com DASHBOARD_AGENTS.html (legado)."""
    print("Agents dashboard: sem mudanças nesta versão (fora do escopo do spec v2)")
    return {"items": 0, "bytes": 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", action="store_true")
    ap.add_argument("--agents", action="store_true")
    args = ap.parse_args()
    both = not (args.corpus or args.agents)
    if args.corpus or both:
        refresh_corpus_dashboard(REPO_ROOT)
    if args.agents or both:
        refresh_agents_dashboard(REPO_ROOT)


if __name__ == "__main__":
    main()
