#!/usr/bin/env python3
"""
calculate_irr.py — Calculate Inter-Rater Reliability (Krippendorff's Alpha)
between human canonical ratings and synthetic pilot ratings.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import numpy as np

try:
    import krippendorff
except ImportError as e:
    raise ImportError("krippendorff library required. Install with: pip install krippendorff") from e

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
SYNTHETIC_PATH = REPO_ROOT / "data" / "processed" / "irr_pilot_synthetic_results.jsonl"
MOCK_SYNTHETIC_PATH = REPO_ROOT / "data" / "processed" / "irr_pilot_synthetic_results_mock.jsonl"
LOG_PATH = REPO_ROOT / "logs" / "irr_discrepancies.log"

INDICATORS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate Krippendorff's Alpha and log IRR discrepancies.")
    parser.add_argument("--mock", action="store_true", help="Use mock synthetic results file for calculation.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output.")
    return parser.parse_args()

def load_human_ratings():
    ratings = {}
    if not RECORDS_PATH.exists():
        print(f"Error: Records file not found at {RECORDS_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(RECORDS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            item_id = record.get("item_id")
            purificacao = record.get("purificacao")
            if item_id and purificacao:
                # Store the exact 10 indicator scores
                ratings[item_id] = {ind: purificacao.get(ind) for ind in INDICATORS if ind in purificacao}
    return ratings

def load_synthetic_ratings(use_mock=False):
    ratings = {}
    path = MOCK_SYNTHETIC_PATH if use_mock else SYNTHETIC_PATH
    if not path.exists():
        print(f"Error: Synthetic results file not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            item_id = record.get("item_id")
            indicadores = record.get("indicadores")
            if item_id and indicadores:
                ratings[item_id] = {}
                for ind in INDICATORS:
                    val = indicadores.get(ind)
                    if val is not None and isinstance(val, dict):
                        ratings[item_id][ind] = {
                            "score": val.get("score"),
                            "justification": val.get("justification", "")
                        }
    return ratings

def calculate_irr_metrics(human_ratings, synthetic_ratings, verbose=False):
    # Match items
    matched_ids = [item_id for item_id in synthetic_ratings if item_id in human_ratings]
    if not matched_ids:
        print("Error: No overlapping item IDs found between human and synthetic files.", file=sys.stderr)
        sys.exit(1)
        
    if verbose:
        print(f"Matched {len(matched_ids)} items for IRR calculation.")
    
    # 1. Calculate per-indicator Alphas
    alphas = {}
    for ind in INDICATORS:
        coder_human = []
        coder_synthetic = []
        for item_id in matched_ids:
            h_score = human_ratings[item_id].get(ind)
            s_data = synthetic_ratings[item_id].get(ind)
            s_score = s_data.get("score") if s_data else None
            
            if h_score is not None and s_score is not None:
                coder_human.append(h_score)
                coder_synthetic.append(s_score)
        
        # Build 2xN reliability matrix
        reliability_data = np.array([coder_human, coder_synthetic])
        if len(coder_human) > 0 and len(set(coder_human).union(set(coder_synthetic))) > 1:
            try:
                alpha = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement='ordinal')
                alphas[ind] = alpha
            except Exception as e:
                alphas[ind] = float('nan')
                if verbose:
                    print(f"Warning: Failed to compute alpha for {ind}: {e}")
        else:
            alphas[ind] = float('nan')
            
    # 2. Calculate pooled global Alpha
    pooled_human = []
    pooled_synthetic = []
    for ind in INDICATORS:
        for item_id in matched_ids:
            h_score = human_ratings[item_id].get(ind)
            s_data = synthetic_ratings[item_id].get(ind)
            s_score = s_data.get("score") if s_data else None
            if h_score is not None and s_score is not None:
                pooled_human.append(h_score)
                pooled_synthetic.append(s_score)
                
    reliability_data_pooled = np.array([pooled_human, pooled_synthetic])
    pooled_alpha = float('nan')
    if len(pooled_human) > 0 and len(set(pooled_human).union(set(pooled_synthetic))) > 1:
        try:
            pooled_alpha = krippendorff.alpha(reliability_data=reliability_data_pooled, level_of_measurement='ordinal')
        except Exception as e:
            print(f"Error computing pooled alpha: {e}", file=sys.stderr)
            
    # Calculate average of indicator alphas (excluding NaNs)
    valid_alphas = [a for a in alphas.values() if not np.isnan(a)]
    mean_alpha = np.mean(valid_alphas) if valid_alphas else float('nan')
    
    return matched_ids, alphas, pooled_alpha, mean_alpha

def detect_and_log_discrepancies(matched_ids, human_ratings, synthetic_ratings):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    discrepancies = []
    
    with open(LOG_PATH, "w", encoding="utf-8") as log_file:
        log_file.write(f"IRR DISCREPANCY LOG — Generated on {datetime.now().isoformat()}\n")
        log_file.write("=" * 80 + "\n\n")
        
        for item_id in matched_ids:
            for ind in INDICATORS:
                h_score = human_ratings[item_id].get(ind)
                s_data = synthetic_ratings[item_id].get(ind)
                s_score = s_data.get("score") if s_data else None
                s_just = s_data.get("justification", "") if s_data else ""
                
                if h_score is not None and s_score is not None:
                    diff = abs(h_score - s_score)
                    if diff >= 2:
                        discrepancies.append({
                            "item_id": item_id,
                            "indicator": ind,
                            "human": h_score,
                            "synthetic": s_score,
                            "justification": s_just
                        })
                        
                        log_file.write("=" * 80 + "\n")
                        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        log_file.write(f"Item ID: {item_id}\n")
                        log_file.write(f"Indicator: {ind}\n")
                        log_file.write(f"Human Score: {h_score}\n")
                        log_file.write(f"Synthetic Score: {s_score}\n")
                        log_file.write(f"Difference: {diff}\n")
                        log_file.write(f"Synthetic Justification:\n{s_just}\n")
                        log_file.write("=" * 80 + "\n\n")
                        
    return discrepancies

def main():
    args = parse_args()
    human = load_human_ratings()
    synthetic = load_synthetic_ratings(args.mock)
    
    if args.verbose:
        print(f"Loaded {len(human)} human canonical records.")
        print(f"Loaded {len(synthetic)} synthetic records.")
        
    matched_ids, alphas, pooled_alpha, mean_alpha = calculate_irr_metrics(human, synthetic, args.verbose)
    discrepancies = detect_and_log_discrepancies(matched_ids, human, synthetic)
    
    print("\n" + "=" * 50)
    print("INTER-RATER RELIABILITY (IRR) PILOT RESULTS")
    print("=" * 50)
    print(f"Matched Items: {len(matched_ids)}")
    print(f"Pooled Global Alpha (pooled data):    {pooled_alpha:.4f}")
    print(f"Averaged Dimension Alpha (mean):       {mean_alpha:.4f}")
    print("-" * 50)
    print("Alphas per Indicator:")
    for ind in INDICATORS:
        alpha_val = alphas.get(ind, float('nan'))
        status = f"{alpha_val:.4f}" if not np.isnan(alpha_val) else "N/A (insufficient variance)"
        print(f"  - {ind:<28}: {status}")
    print("=" * 50)
    print(f"Detected {len(discrepancies)} critical discrepancies (difference >= 2).")
    print(f"Detailed discrepancy log written to {LOG_PATH}")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
