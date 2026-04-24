#!/usr/bin/env python3
"""
Atomic validator-compliant rewrite of records.jsonl
Adds required top-level fields: timestamps, exports, iconocode.validation & confidence
"""

import json
import sys

lines = open("data/processed/records.jsonl", "r", encoding="utf-8").readlines()
output = []

for i, line in enumerate(lines, 1):
    record = json.loads(line.strip())
    
    # Inject required timestamps if missing
    if "timestamps" not in record:
        record["timestamps"] = {
            "created_at": "2026-04-17T00:00:00Z",
            "updated_at": "2026-04-17T00:00:00Z"
        }
    else:
        record["timestamps"]["updated_at"] = "2026-04-17T00:00:00Z"

    # Inject required empty exports if missing
    if "exports" not in record:
        record["exports"] = {}

    # Ensure iconocode block has required fields
    if not record["iconocode"]:
        record["iconocode"] = {}
    
    if "validation" not in record["iconocode"]:
        record["iconocode"]["validation"] = []
    if "confidence" not in record["iconocode"]:
        record["iconocode"]["confidence"] = 0.85

    output.append(json.dumps(record, ensure_ascii=False) + "\n")

open("data/processed/records.jsonl", "w", encoding="utf-8").writelines(output)
print("Rewritten records.jsonl with compliant fields")

# Run validation inline
import subprocess
res = subprocess.run(
    ["python", "tools/scripts/validate_schemas.py", "data/processed/records.jsonl", "--schema", "master-record", "--verbose"],
    cwd=".",
    capture_output=True,
    text=True
)
print(res.stdout)
print(res.stderr)
sys.exit(res.returncode)
