from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
purification_path = ROOT / "data" / "processed" / "purification.jsonl"
out_dir = ROOT / "notebooks" / "01_exploratory" / "output"
out_dir.mkdir(parents=True, exist_ok=True)
out_csv = out_dir / "endurecimento_por_regime.csv"

regime_scores: dict[str, list[float]] = defaultdict(list)

with purification_path.open() as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        regime = record.get("regime_iconocratico") or record.get("regime", "?")
        score = record.get("score_endurecimento")
        if score is None:
            score = record.get("purificacao_composto")
        if score is None:
            continue
        regime_scores[regime].append(float(score))

with out_csv.open("w", encoding="utf-8") as f:
    f.write("regime,count,mean,min,max\n")
    for regime in sorted(regime_scores):
        scores = regime_scores[regime]
        if not scores:
            continue
        f.write(
            f"{regime},{len(scores)},{sum(scores) / len(scores):.2f},{min(scores):.2f},{max(scores):.2f}\n"
        )

print(f"ENDURECIMENTO summary saved to {out_csv}")
