#!/usr/bin/env python3
"""
purify-diff.py — CLI for diffing purification indicator coding sessions.

Allows comparing different codings for the same item over time (history),
or comparing two different items side-by-side.

Usage:
    python tools/scripts/purify-diff.py --id BR-017
    python tools/scripts/purify-diff.py --id BR-017 --history
    python tools/scripts/purify-diff.py --compare FR-013 FR-014
"""

import argparse
import json
import sys
from pathlib import Path

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
OUTPUT_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"

INDICATOR_KEYS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal"
]

INDICATOR_LABELS = {
    "desincorporacao": "Desincorporação",
    "rigidez_postural": "Rigidez Postural",
    "dessexualizacao": "Dessexualização",
    "uniformizacao_facial": "Uniformização Facial",
    "heraldizacao": "Heraldização",
    "enquadramento_arquitetonico": "Enquadr. Arquit.",
    "apagamento_narrativo": "Apagamento Narr.",
    "monocromatizacao": "Monocromatização",
    "serialidade": "Serialidade",
    "inscricao_estatal": "Inscrição Estatal"
}

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

def colorize(text, color, use_color):
    return f"{color}{text}{RESET}" if use_color else text

def load_purification_history():
    """Load all purification logs from JSONL grouped by item ID."""
    history = {}
    if OUTPUT_JSONL.exists():
        with open(OUTPUT_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rec = json.loads(line)
                        history.setdefault(rec["id"], []).append(rec)
                    except json.JSONDecodeError:
                        continue
    return history

def load_corpus_baselines():
    """Load baseline indicators from corpus-data.json."""
    baselines = {}
    if CORPUS_JSON.exists():
        with open(CORPUS_JSON, encoding="utf-8") as f:
            try:
                corpus = json.load(f)
                for item in corpus:
                    item_id = item.get("id")
                    if item_id:
                        baselines[item_id] = item
            except json.JSONDecodeError:
                pass
    return baselines

def print_diff_table(title, col1_header, col1_data, col2_header, col2_data, use_color):
    """Prints a beautiful side-by-side comparison table of indicators."""
    print(f"\n{colorize('=' * 80, BOLD, use_color)}")
    print(f"  {colorize(title, BOLD + CYAN, use_color)}")
    print(f"{colorize('=' * 80, BOLD, use_color)}")
    
    # Headers
    print(f"  {colorize('Indicator', BOLD, use_color):<25} | {colorize(col1_header, BOLD, use_color):<25} | {colorize(col2_header, BOLD, use_color):<25}")
    print(f"  {'-'*25}-+-{'-'*25}-+-{'-'*25}")
    
    # Rows
    for key in INDICATOR_KEYS:
        val1 = col1_data.get(key, "N/A")
        val2 = col2_data.get(key, "N/A")
        
        lbl = INDICATOR_LABELS.get(key, key)
        
        # Color difference
        if val1 != val2 and val1 != "N/A" and val2 != "N/A":
            diff_color = YELLOW
            val1_str = colorize(f"{val1} *", diff_color, use_color)
            val2_str = colorize(f"{val2} *", diff_color, use_color)
        else:
            val1_str = str(val1)
            val2_str = str(val2)
            
        print(f"  {lbl:<25} | {val1_str:<25} | {val2_str:<25}")
        
    print(f"  {'-'*25}-+-{'-'*25}-+-{'-'*25}")
    
    # Composites and metadata
    comp1 = col1_data.get("purificacao_composto", col1_data.get("endurecimento_score", "N/A"))
    comp2 = col2_data.get("purificacao_composto", col2_data.get("endurecimento_score", "N/A"))
    
    comp1_str = f"{comp1:.2f}" if isinstance(comp1, (int, float)) else str(comp1)
    comp2_str = f"{comp2:.2f}" if isinstance(comp2, (int, float)) else str(comp2)
    
    if comp1_str != comp2_str:
        comp1_str = colorize(comp1_str, GREEN if (isinstance(comp1, (int,float)) and isinstance(comp2, (int,float)) and comp1 < comp2) else RED, use_color)
        comp2_str = colorize(comp2_str, GREEN if (isinstance(comp1, (int,float)) and isinstance(comp2, (int,float)) and comp2 < comp1) else RED, use_color)
        
    print(f"  {colorize('Composite Score', BOLD, use_color):<25} | {comp1_str:<25} | {comp2_str:<25}")
    
    reg1 = col1_data.get("regime_iconocratico", col1_data.get("regime", "N/A"))
    reg2 = col2_data.get("regime_iconocratico", col2_data.get("regime", "N/A"))
    print(f"  {colorize('Regime', BOLD, use_color):<25} | {str(reg1).upper():<25} | {str(reg2).upper():<25}")
    
    coder1 = col1_data.get("coded_by", "baseline")
    coder2 = col2_data.get("coded_by", "baseline")
    print(f"  {colorize('Coder', BOLD, use_color):<25} | {coder1:<25} | {coder2:<25}")
    
    date1 = col1_data.get("coded_at", "N/A")
    date2 = col2_data.get("coded_at", "N/A")
    # Truncate dates for display
    if len(date1) > 19: date1 = date1[:19]
    if len(date2) > 19: date2 = date2[:19]
    print(f"  {colorize('Date', BOLD, use_color):<25} | {date1:<25} | {date2:<25}")
    
    # Print notes if present
    note1 = col1_data.get("notes", col1_data.get("analyst_notes", ""))
    note2 = col2_data.get("notes", col2_data.get("analyst_notes", ""))
    if note1 or note2:
        print(f"\n  {colorize('Notes / Explanations:', BOLD, use_color)}")
        if note1:
            print(f"    {colorize(col1_header + ':', BOLD, use_color)} {note1}")
        if note2:
            print(f"    {colorize(col2_header + ':', BOLD, use_color)} {note2}")
            
    print(f"{colorize('=' * 80, BOLD, use_color)}\n")

def main():
    parser = argparse.ArgumentParser(description="Diff purification indicator codings.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="Item ID to inspect (e.g. BR-017)")
    group.add_argument("--compare", nargs=2, metavar=("ID1", "ID2"), help="Compare two different items side-by-side")
    
    parser.add_argument("--history", action="store_true", help="For a given ID, compare first vs latest coding in history")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    args = parser.parse_args()
    use_color = not args.no_color and sys.stdout.isatty()
    
    history = load_purification_history()
    baselines = load_corpus_baselines()
    
    if args.compare:
        id1, id2 = args.compare
        
        # Get latest coding or fallback to baseline
        rec1 = history.get(id1, [{}])[-1]
        rec2 = history.get(id2, [{}])[-1]
        
        if not rec1 and id1 in baselines:
            item = baselines[id1]
            rec1 = {"id": id1, **item.get("indicadores", {}), "endurecimento_score": item.get("endurecimento_score"), "regime": item.get("regime")}
            
        if not rec2 and id2 in baselines:
            item = baselines[id2]
            rec2 = {"id": id2, **item.get("indicadores", {}), "endurecimento_score": item.get("endurecimento_score"), "regime": item.get("regime")}
            
        if not rec1 and not rec2:
            print(f"Error: Neither {id1} nor {id2} was found in purification history or corpus-data.json")
            sys.exit(1)
            
        title = f"Comparing {id1} vs {id2}"
        print_diff_table(title, f"{id1} (latest)", rec1, f"{id2} (latest)", rec2, use_color)
        
    elif args.id:
        item_id = args.id
        runs = history.get(item_id, [])
        
        if not runs:
            # Check baseline
            if item_id in baselines:
                item = baselines[item_id]
                rec = {"id": item_id, **item.get("indicadores", {}), "purificacao_composto": item.get("endurecimento_score"), "regime_iconocratico": item.get("regime"), "coded_by": item.get("coded_by", "baseline"), "coded_at": item.get("coded_at", "N/A")}
                print(f"\nItem {item_id} has no coding history in purification.jsonl.")
                print(f"Showing exported baseline from corpus-data.json:")
                print_diff_table(f"Baseline for {item_id}", "Exported values", rec, "N/A", {}, use_color)
            else:
                print(f"Error: Item {item_id} not found in purification.jsonl or corpus-data.json")
                sys.exit(1)
            return
            
        if args.history:
            if len(runs) < 2:
                print(f"\nItem {item_id} only has one coding run in history. Cannot perform historical diff.")
                print("Showing current latest coding:")
                print_diff_table(f"Latest Coding for {item_id}", "Latest Run", runs[-1], "N/A", {}, use_color)
            else:
                title = f"Historical diff for {item_id} (First vs Latest coding)"
                print_diff_table(title, f"First Run ({runs[0].get('coded_by', 'unk')})", runs[0], f"Latest Run ({runs[-1].get('coded_by', 'unk')})", runs[-1], use_color)
        else:
            # Diff latest coding against baseline in corpus-data.json
            base = {}
            if item_id in baselines:
                item = baselines[item_id]
                base = {
                    "id": item_id,
                    **item.get("indicadores", {}),
                    "purificacao_composto": item.get("endurecimento_score"),
                    "regime_iconocratico": item.get("regime"),
                    "coded_by": "baseline_export",
                    "coded_at": "N/A"
                }
            
            title = f"Latest coding vs Baseline for {item_id}"
            print_diff_table(title, "Baseline Export", base, "Latest Coding Run", runs[-1], use_color)

if __name__ == "__main__":
    main()
