#!/usr/bin/env python3
"""Fix 43 drive-import records with schema violations.

The records from batch='drive-import-2026-05-19-*' were created by
ingest_research_candidates.py without post-processing. They have:
  - Old flat webscout format (no summary_evidence/gaps)
  - Missing purificacao block (all 10 indicators)
  - Old iconocode format (analysis_* instead of required fields)
  - abnt_citations as string instead of array
  - chicago_citations causing 'additional properties' error
  - Bad batch_id format

Usage:
    python tools/scripts/fix_drive_import_records.py          # dry-run (preview only)
    python tools/scripts/fix_drive_import_records.py --write  # apply fixes
    python tools/scripts/fix_drive_import_records.py --validate  # check schema after fix
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"

PURIFICACAO_DEFAULT = {
    "desincorporacao": 0,
    "rigidez_postural": 0,
    "dessexualizacao": 0,
    "uniformizacao_facial": 0,
    "heraldizacao": 0,
    "enquadramento_arquitetonico": 0,
    "apagamento_narrativo": 0,
    "monocromatizacao": 0,
    "serialidade": 0,
    "inscricao_estatal": 0,
    "purificacao_composto": 0.0,
    "regime_iconocratico": "fundacional",
    "coded_by": "",
    "coded_at": "",
    "notes": "registro importado — aguardando codificação de endurecimento",
}

def _now_iso() -> str:
    """Return current UTC ISO 8601 timestamp."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_drive_import(rec: dict) -> bool:
    bid = rec.get("batch_id", "")
    return "drive-import" in str(bid)


def fix_batch_id(rec: dict) -> list[str]:
    """Fix batch_id to match schema (UUID or pattern)."""
    changes = []
    bid = rec.get("batch_id", "")
    if bid and "drive-import" in str(bid):
        # Extract suffix for traceability
        squad = ""
        if "sq1" in bid: squad = "sq1"
        elif "sq2" in bid: squad = "sq2"
        elif "sq3" in bid: squad = "sq3"
        elif "sq4" in bid: squad = "sq4"
        # Generate a proper UUID-based batch_id that matches the pattern
        # Schema accepts: UUID or ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[a-z][a-z0-9]*[0-9]+$
        prefix = uuid.uuid4().hex[:8]
        new_bid = f"{prefix}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:4]}-driveimport{squad}"
        rec["batch_id"] = new_bid
        changes.append(f"batch_id: {bid} → {new_bid}")
    return changes


def fix_webscout(rec: dict) -> list[str]:
    """Restructure old webscout (flat fields) → new format (summary_evidence/gaps)."""
    changes = []
    ws = rec.get("webscout")
    if not isinstance(ws, dict):
        return changes

    # Check if already in new format
    if "summary_evidence" in ws and "gaps" in ws:
        return changes  # already valid

    # Build summary_evidence from available fields
    parts = []
    desc = ws.get("description", "")
    if desc:
        parts.append(desc)
    notes = ws.get("notes", "")
    if notes:
        parts.append(notes)
    period = ws.get("period", "")
    if period:
        parts.append(f"Período: {period}")

    ws["summary_evidence"] = " | ".join(parts) if parts else "(descrição não disponível)"
    ws["gaps"] = []

    # Remove old flat fields that cause "additional properties" error
    flat_fields = [
        "confidence", "description", "drive_fields", "iconclass_candidates",
        "iiif_source", "institution", "medium", "motif", "notes",
        "period", "search_query", "source_archive", "tags",
        "thumbnail_url", "url_image_download",
    ]
    removed = []
    for field in flat_fields:
        if field in ws:
            del ws[field]
            removed.append(field)

    changes.append(f"webscout: restructured, removed {removed}")
    return changes


def fix_iconocode(rec: dict) -> list[str]:
    """Replace old iconocode (analysis_*) with proper structure."""
    changes = []
    ic = rec.get("iconocode")
    if not isinstance(ic, dict):
        # Need to create iconocode block
        rec["iconocode"] = {
            "pre_iconographic": [],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.0,
        }
        changes.append("iconocode: created new block")
        return changes

    # If old analysis_* fields exist, replace entire block
    if any(k in ic for k in ("analysis_date", "analysis_notes", "analysis_status")):
        rec["iconocode"] = {
            "pre_iconographic": [],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.0,
        }
        changes.append("iconocode: replaced old analysis_* format")
        return changes

    # Check if already in new format
    if all(k in ic for k in ("pre_iconographic", "codes", "interpretation", "validation", "confidence")):
        int_ok = isinstance(ic.get("interpretation"), list)
        val_ok = isinstance(ic.get("validation"), dict) and "claim_ledger" in ic.get("validation", {})
        if int_ok and val_ok:
            return changes

    # Fix interpretation: must be array of objects
    interp = ic.get("interpretation")
    if isinstance(interp, str):
        ic["interpretation"] = [{
            "claim_text": interp,
            "claim_type": "iconographic",
            "status": "pending",
            "confidence": 0.0,
        }]
        changes.append("iconocode.interpretation: string → array")
    elif not isinstance(interp, list):
        ic["interpretation"] = []
        changes.append("iconocode.interpretation: created empty array")

    # Fix validation: must have claim_ledger
    val = ic.get("validation")
    if isinstance(val, dict):
        if "claim_ledger" not in val:
            val["claim_ledger"] = []
            for old in ("method", "result"):
                val.pop(old, None)
            changes.append("iconocode.validation: added claim_ledger")
    else:
        ic["validation"] = {"claim_ledger": []}
        changes.append("iconocode.validation: created with claim_ledger")

    return changes


def fix_id(rec: dict) -> list[str]:
    """Remove top-level 'id' if present — schema doesn't allow it."""
    changes = []
    if "id" in rec:
        del rec["id"]
        changes.append("id: removed (not in schema)")
    return changes


def fix_purificacao(rec: dict) -> list[str]:
    """Add missing purificacao block."""
    changes = []
    pu = rec.get("purificacao")
    if isinstance(pu, dict) and all(k in pu for k in (
        "desincorporacao", "rigidez_postural", "dessexualizacao",
        "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
        "apagamento_narrativo", "monocromatizacao", "serialidade", "inscricao_estatal"
    )):
        return changes  # already present and complete

    rec["purificacao"] = dict(PURIFICACAO_DEFAULT)
    rec["purificacao"]["coded_at"] = _now_iso()
    changes.append("purificacao: added default (all 0, uncoded)")
    return changes


def fix_exports(rec: dict) -> list[str]:
    """Fix exports block: abnt_citations as array, remove chicago_citations."""
    changes = []
    ex = rec.get("exports")
    if not isinstance(ex, dict):
        rec["exports"] = {"abnt_citations": [], "audit_flags": ["drive-import-fix"]}
        changes.append("exports: created new block")
        return changes

    # Wrap abnt_citations in array if it's a string
    abnt = ex.get("abnt_citations")
    if isinstance(abnt, str):
        ex["abnt_citations"] = [abnt]
        changes.append("exports.abnt_citations: wrapped string in array")

    # Remove unexpected chicago_citations
    if "chicago_citations" in ex:
        del ex["chicago_citations"]
        changes.append("exports: removed chicago_citations")

    # Add audit flag
    if "audit_flags" not in ex:
        ex["audit_flags"] = []
    if "drive-import-fix" not in ex.get("audit_flags", []):
        ex.setdefault("audit_flags", []).append("drive-import-fix")

    return changes


def fix_timestamps(rec: dict) -> list[str]:
    """Ensure timestamps block exists."""
    changes = []
    ts = rec.get("timestamps")
    if not isinstance(ts, dict):
        rec["timestamps"] = {"created_at": None, "updated_at": None}
        changes.append("timestamps: created")
    return changes


def fix_record(rec: dict) -> list[str]:
    """Apply all fixes and return list of changes made."""
    changes = []
    changes.extend(fix_id(rec))
    changes.extend(fix_batch_id(rec))
    changes.extend(fix_webscout(rec))
    changes.extend(fix_iconocode(rec))
    changes.extend(fix_purificacao(rec))
    changes.extend(fix_exports(rec))
    changes.extend(fix_timestamps(rec))
    return changes


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
            records.append(json.loads(stripped))
    return records


def write_jsonl_atomic(path: Path, records: list[dict[str, Any]]) -> None:
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
        ) as f:
            tmp_path = Path(f.name)
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False, sort_keys=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path is not None and tmp_path.exists():
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass


def validate_schema() -> bool:
    """Quick schema validation check using the validate script."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(REPO / "tools" / "scripts" / "validate_schemas.py")],
        capture_output=True, text=True, cwd=REPO,
    )
    print(result.stdout[:500])
    if result.returncode == 0:
        print("✓ Schema validation PASSED")
        return True
    else:
        # Count valid vs failed
        for line in result.stdout.splitlines():
            if "valid" in line or "failed" in line:
                print(f"  {line.strip()}")
        return False


def main() -> int:
    write = "--write" in sys.argv
    validate = "--validate" in sys.argv

    records = load_jsonl(RECORDS_PATH)
    total_records = len(records)
    fixed = 0
    all_changes: Counter[str] = Counter()

    print(f"Verificando {total_records} registros em {RECORDS_PATH}")
    print()

    for i, rec in enumerate(records):
        if not is_drive_import(rec):
            continue
        changes = fix_record(rec)
        if changes:
            fixed += 1
            if not write:
                print(f"  [{i+1:>3}] batch_id={rec.get('batch_id','')[:30]}...:")
                for c in changes:
                    print(f"         → {c}")
            for c in changes:
                all_changes[c.split(":")[0]] += 1

    print()
    print(f"Drive-import records encontrados: {fixed}")
    print()

    if fixed == 0:
        print("Nenhum registro drive-import encontrado — já foram corrigidos?")
        return 0

    print("Resumo de correções:")
    for field, count in all_changes.most_common():
        print(f"  {field}: {count}")

    print()
    if write:
        write_jsonl_atomic(RECORDS_PATH, records)
        print(f"✓ {RECORDS_PATH} atualizado atomicamente")
        if validate:
            print()
            ok = validate_schema()
            return 0 if ok else 1
        return 0
    else:
        print("Dry-run: nenhum arquivo foi alterado. Use --write para aplicar.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
