#!/usr/bin/env python3
"""
e1_recode_zeros.py — Re-codifica os 29 itens com score 0.0 no pathosformel_index
usando descrições enriquecidas das notas do vault (SCOUT-XXX) + thumbnails.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
VAULT_DIR = REPO / "vault" / "candidatos"
PATHOS_INDEX = REPO / "data" / "processed" / "pathosformel_index.jsonl"
VAULT_RECORDS_PATH = REPO / "data" / "processed" / "vault_records.jsonl"

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma4"
OLLAMA_TIMEOUT = 300

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade", "inscricao_estatal",
]
REGIMES = ["fundacional", "normativo", "militar", "contra-alegoria"]

CODING_PROMPT = """Analyze this allegorical image and code the 10 purification indicators (0-3) and regime.

TITLE: {title}
COUNTRY: {place} | DATE: {date}
SOURCE: {acervo} | MEDIUM: {suporte}
THUMBNAIL: {thumb} (view this image for visual analysis)
DESCRIPTION: {summary}

Scale: 0=absent, 1=minimal, 2=moderate, 3=dominant/extreme

Fields: desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial, heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal (each 0-3), regime_iconocratico (fundacional|normativo|militar|contra-alegoria), notes (brief justification in Portuguese)

JSON:"""


def load_records() -> dict[str, dict]:
    with open(RECORDS_PATH) as f:
        return {json.loads(l)["item_id"]: json.loads(l) for l in f if l.strip()}


def load_pathos() -> dict[str, dict]:
    with open(PATHOS_INDEX) as f:
        return {json.loads(l)["item_id"]: json.loads(l) for l in f if l.strip()}


def read_vault_note(scout_id: int) -> dict:
    """Extract metadata from a vault note."""
    for f in VAULT_DIR.glob(f"SCOUT-{scout_id}*.md"):
        text = f.read_text(encoding="utf-8")
        
        # Frontmatter
        fm = {}
        fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip().strip('"')] = v.strip().strip('"')
        
        # Thumbnail URL
        thumb = ""
        # Pattern: [imagem](url)
        m = re.search(r'\[imagem\]\(((https?://[^)]+))\)', text)
        if m:
            thumb = m.group(1)
        # Pattern: thumbnail: url
        if not thumb:
            m = re.search(r'thumbnail[^:]*:\s*(https?://\S+)', text, re.IGNORECASE)
            if m:
                thumb = m.group(1).rstrip(")").rstrip(">")
        
        # Body text (after frontmatter)
        body = re.sub(r"^---.*?---\n?", "", text, count=1, flags=re.DOTALL).strip()
        
        return {
            "scout_id": scout_id,
            "acervo": fm.get("acervo", "").strip('"'),
            "suporte": fm.get("suporte", "").strip('"'),
            "motivo": fm.get("motivo_alegorico", "").strip('"'),
            "regime_fm": fm.get("regime", "").strip('"'),
            "data_estimada": fm.get("data_estimada", "").strip('"'),
            "thumb": thumb,
            "body": body[:500],
        }
    return {"scout_id": scout_id, "acervo": "", "suporte": "", "motivo": "", "regime_fm": "", "data_estimada": "", "thumb": "", "body": ""}


def find_scout_id(pathos_item: dict, records: dict) -> int | None:
    """Find SCOUT ID from a pathos item by matching records."""
    rec = records.get(pathos_item["item_id"])
    if not rec:
        return None
    # The Scout ID is encoded in the webscout search_results notes
    ws = rec.get("webscout", {})
    for sr in ws.get("search_results", []):
        notes = sr.get("notes", "")
        m = re.search(r"SCOUT-(\d+)", notes)
        if m:
            return int(m.group(1))
    return None


def call_ollama(prompt: str) -> str | None:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 2048}
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read())
            msg = data.get("message", {})
            content = msg.get("content", "") or ""
            thinking = msg.get("thinking", "") or ""
            return content or thinking or None
    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        return None


def parse_json(raw: str) -> dict | None:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:])
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    for pos in ["rfind", "find"]:
        fn = getattr(cleaned, pos)
        start = fn("{")
        end = cleaned.rfind("}")
        if 0 <= start < end:
            try:
                return json.loads(cleaned[start:end+1])
            except json.JSONDecodeError:
                pass
    return None


def main():
    print("=== E1 Re-code: 29 Zero-Score Items ===\n")
    
    records = load_records()
    pathos_items = load_pathos()
    
    zeros = {k: v for k, v in pathos_items.items() if v["purificacao_composto"] == 0.0}
    print(f"Zero-score items to re-code: {len(zeros)}\n")
    
    successes = 0
    failures = 0
    updated = []
    
    for i, (item_id, item) in enumerate(sorted(zeros.items())):
        scout_id = find_scout_id(item, records)
        if not scout_id:
            print(f"[{i+1}/{len(zeros)}] {item['sigla_id']}: NO SCOUT ID — skipping")
            failures += 1
            continue
        
        vault = read_vault_note(scout_id)
        rec = records.get(item_id, {})
        inp = rec.get("input", {})
        ws = rec.get("webscout", {})
        
        # Build enriched description
        summary = ws.get("summary_evidence", "") or ""
        # Add context from vault if summary is short
        if len(summary) < 100 and vault["body"]:
            summary = vault["body"]
        
        title = inp.get("title_hint", item["title"])
        place = inp.get("place_hint", item.get("place", "?"))
        date = inp.get("date_hint", item.get("date", ""))
        acervo = vault["acervo"] or "unknown"
        suporte = vault["suporte"] or "unknown"
        thumb = vault["thumb"]
        
        prompt = CODING_PROMPT.format(
            title=title[:120],
            place=place,
            date=date,
            acervo=acervo,
            suporte=suporte,
            thumb=thumb or "(no thumbnail available)",
            summary=summary[:600]
        )
        
        print(f"[{i+1}/{len(zeros)}] {item['sigla_id']:<15} (SCOUT-{scout_id})...", end=" ", flush=True)
        raw = call_ollama(prompt)
        if not raw:
            print("FAILED")
            failures += 1
            continue
        
        parsed = parse_json(raw)
        if not parsed:
            print("PARSE FAILED")
            print(f"  Raw: {raw[:150]}...")
            failures += 1
            continue
        
        # Validate
        indicators = {}
        for ind in INDICATORS:
            val = parsed.get(ind)
            if isinstance(val, (int, float)) and 0 <= val <= 3:
                indicators[ind] = int(val)
            else:
                indicators[ind] = 0
        
        regime = parsed.get("regime_iconocratico", "").strip().lower()
        if regime not in REGIMES:
            for r in REGIMES:
                if r in regime:
                    regime = r
                    break
            else:
                regime = item.get("regime_iconocratico", "fundacional")
        
        score = sum(indicators.values()) / len(indicators)
        notes = parsed.get("notes", "")
        if not isinstance(notes, str):
            notes = str(notes)
        
        updated_item = dict(item)
        updated_item.update(indicators)
        updated_item["purificacao_composto"] = round(score, 1)
        updated_item["regime_iconocratico"] = regime
        updated_item["notes"] = notes[:300]
        updated_item["coded_by"] = "e1-gemma4/gemma4-recode"
        updated_item["coded_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        updated.append(updated_item)
        print(f"OK (score={score:.1f}, regime={regime})")
        successes += 1
        
        if i < len(zeros) - 1:
            time.sleep(1)
    
    print(f"\n=== Summary ===")
    print(f"Success: {successes} | Failures: {failures}")
    
    if updated:
        # Merge with existing pathos index (keep scores > 0, replace zeros)
        all_items = {}
        for k, v in pathos_items.items():
            all_items[k] = v
        
        for u in updated:
            uid = u["item_id"]
            old_score = all_items.get(uid, {}).get("purificacao_composto", 0)
            if old_score == 0.0 or True:  # replace all recoded
                all_items[uid] = u
        
        # Write
        with open(PATHOS_INDEX, "w") as f:
            for item in sorted(all_items.values(), key=lambda x: x.get("sigla_id", "")):
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"\nUpdated {PATHOS_INDEX} with {len(all_items)} items ({successes} re-coded)")
    
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
