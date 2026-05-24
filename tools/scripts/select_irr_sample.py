#!/usr/bin/env python3
import json
import random
from collections import defaultdict
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
ID_MAPPING_PATH = REPO_ROOT / "data" / "processed" / "id-mapping.json"
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
OUT_PATH = REPO_ROOT / "data" / "processed" / "irr_sample_metadata.jsonl"

def load_records(path=None):
    if path is None:
        path = RECORDS_PATH
    else:
        path = Path(path)
        
    # 1. Load id-mapping.json
    if not ID_MAPPING_PATH.exists():
        raise FileNotFoundError(f"Required dependency file not found: {ID_MAPPING_PATH}")
        
    item_to_corpus = {}
    with open(ID_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
        for m in mapping_data.get("mapping", []):
            item_to_corpus[m["item_id"]] = m["corpus_id"]
                
    # 2. Load corpus-data.json
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"Required dependency file not found: {CORPUS_PATH}")
        
    corpus_items = {}
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus_data = json.load(f)
        for item in corpus_data:
            corpus_items[item["id"]] = item
                
    # 3. Load records.jsonl and enrich with metadata
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                item_id = r.get("item_id", "")
                corpus_id = item_to_corpus.get(item_id, "")
                
                # Default values
                support = "monumento"
                regime = "NORMATIVO"
                
                # Check purificacao block for regime first
                purif = r.get("purificacao") or {}
                regime_iconocratico = purif.get("regime_iconocratico", "")
                if regime_iconocratico:
                    regime = regime_iconocratico.upper()
                
                # Look up in corpus-data.json
                if corpus_id and corpus_id in corpus_items:
                    c_item = corpus_items[corpus_id]
                    # Get support
                    if "support" in c_item and c_item["support"]:
                        support = c_item["support"]
                    # If regime not found in purificacao, look up in corpus
                    if not regime_iconocratico and "regime" in c_item and c_item["regime"]:
                        regime = c_item["regime"].upper()
                        
                r["metadata"] = {
                    "suporte": support,
                    "regime": regime
                }
                records.append(r)
    return records

def select_stratified(records, n=30):
    # Use local RNG for reproducibility
    local_random = random.Random(42)
    
    groups = defaultdict(list)
    for r in records:
        # Fallbacks to handle schema inconsistencies safely
        suporte = r.get("metadata", {}).get("suporte") or r.get("suporte", "monumento")
        regime = r.get("metadata", {}).get("regime") or r.get("regime", "NORMATIVO")
        groups[(suporte, regime)].append(r)
        
    selected = []
    group_keys = list(groups.keys())
    
    # Sort keys to ensure deterministic round-robin order
    group_keys.sort()
    
    # Round-robin selection across groups to ensure perfect stratification
    while len(selected) < n and group_keys:
        for key in list(group_keys):
            if len(selected) >= n:
                break
            if groups[key]:
                # Pick a random element from this group using local RNG
                item = local_random.choice(groups[key])
                selected.append(item)
                groups[key].remove(item)
            else:
                group_keys.remove(key)
                
    return selected

if __name__ == "__main__":
    records = load_records()
    sample = select_stratified(records, 30)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for record in sample:
            suporte = record.get("metadata", {}).get("suporte") or record.get("suporte", "monumento")
            regime = record.get("metadata", {}).get("regime") or record.get("regime", "NORMATIVO")
            simplified = {
                "item_id": record["item_id"],
                "suporte": suporte,
                "regime": regime
            }
            f.write(json.dumps(simplified, ensure_ascii=False) + "\n")
    print(f"Selected {len(sample)} stratified items for the IRR Pilot.")
