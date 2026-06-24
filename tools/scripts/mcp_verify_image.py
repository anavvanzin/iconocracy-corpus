#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_FILE = REPO_ROOT / "data" / "processed" / "records.jsonl"
MAPPING_FILE = REPO_ROOT / "data" / "processed" / "id-mapping.json"
PURIFICATION_FILE = REPO_ROOT / "data" / "processed" / "purification.jsonl"

def load_mapping():
    """Load UUID mapping to corpus ID (e.g., BR-007)."""
    mapping = {}
    if MAPPING_FILE.exists():
        try:
            with open(MAPPING_FILE, encoding="utf-8") as f:
                data = json.load(f)
                for entry in data.get("mapping", []):
                    c_id = entry.get("corpus_id")
                    item_id = entry.get("item_id")
                    if c_id and item_id:
                        mapping[c_id] = item_id
        except Exception:
            pass
    return mapping

def load_record_by_uuid(uuid):
    """Load a specific master record by its UUID."""
    if RECORDS_FILE.exists():
        with open(RECORDS_FILE, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        rec = json.loads(line)
                        if rec.get("item_id") == uuid:
                            return rec
                    except json.JSONDecodeError:
                        continue
    return None

def load_from_purification_log(corpus_id):
    """Fallback: load latest record from purification.jsonl directly by corpus ID."""
    latest_rec = None
    if PURIFICATION_FILE.exists():
        with open(PURIFICATION_FILE, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        rec = json.loads(line)
                        if rec.get("id") == corpus_id:
                            latest_rec = rec
                    except json.JSONDecodeError:
                        continue
    return latest_rec

def verify_image_grounding(corpus_id: str, indicator: str, claimed_value: int) -> dict:
    """MCP tool helper to verify visual indicator claims in thesis text.

    Args:
        corpus_id: The ID of the corpus item (e.g., 'BR-007')
        indicator: The purification indicator name (e.g., 'desincorporacao')
        claimed_value: The score claimed (0-3)

    Returns:
        A status dictionary detailing whether the claim is validated or mismatched.
    """
    mapping = load_mapping()
    purif_data = None
    source = "unresolved"

    # Step 1: Try checking master records in records.jsonl via mapping
    if corpus_id in mapping:
        uuid = mapping[corpus_id]
        master_record = load_record_by_uuid(uuid)
        if master_record and "purificacao" in master_record:
            purif_data = master_record["purificacao"]
            source = "records.jsonl (master)"

    # Step 2: Fall back to purification.jsonl
    if not purif_data:
        purif_data = load_from_purification_log(corpus_id)
        if purif_data:
            source = "purification.jsonl (log)"

    if not purif_data:
        return {
            "status": "ERROR",
            "reason": f"Item {corpus_id} not found in master records or purification log."
        }

    actual_value = purif_data.get(indicator)
    if actual_value is None:
        return {
            "status": "ERROR",
            "reason": f"Indicator '{indicator}' is not coded for {corpus_id}."
        }

    try:
        actual_val_int = int(actual_value)
        claimed_val_int = int(claimed_value)
    except ValueError:
        return {
            "status": "ERROR",
            "reason": f"Non-integer values encountered: actual={actual_value}, claimed={claimed_value}."
        }

    if actual_val_int != claimed_val_int:
        return {
            "status": "MISMATCH",
            "corpus_id": corpus_id,
            "indicator": indicator,
            "actual_value": actual_val_int,
            "claimed_value": claimed_val_int,
            "source": source,
            "reason": f"Methodological warning: LLM claimed {indicator}={claimed_val_int}, but validated database says {actual_val_int}."
        }

    return {
        "status": "VALIDATED",
        "corpus_id": corpus_id,
        "indicator": indicator,
        "actual_value": actual_val_int,
        "source": source
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python mcp_verify_image.py <corpus_id> <indicator> <claimed_value>")
        print("Example: python mcp_verify_image.py BR-007 desincorporacao 3")
        sys.exit(1)
        
    c_id = sys.argv[1]
    ind = sys.argv[2]
    try:
        val = int(sys.argv[3])
    except ValueError:
        print("Error: Claimed value must be an integer.")
        sys.exit(1)
        
    res = verify_image_grounding(c_id, ind, val)
    print(json.dumps(res, indent=2, ensure_ascii=False))
