#!/usr/bin/env python3
"""
e3_firecrawl_recode.py — Terceira passagem: extrai descrições via Firecrawl
para os itens com score 0.0 e re-codifica com Gemma-4.

Uso:
    python3 tools/scripts/e3_firecrawl_recode.py    # roda todos os 29
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
PATHOS_INDEX = REPO / "data" / "processed" / "pathosformel_index.jsonl"
FC_EXTRACT_DIR = REPO / "data" / "processed" / "fc_descriptions"
FC_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

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
SOURCE DESCRIPTION: {description}

Scale: 0=absent, 1=minimal, 2=moderate, 3=dominant/extreme

Fields (all 0-3): desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial, heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal

regime_iconocratico: fundacional|normativo|militar|contra-alegoria
notes: brief justification in Portuguese (1 sentence)

Output ONLY valid JSON. No thinking. No preamble. Just:
{{"desincorporacao":0,"rigidez_postural":0,"dessexualizacao":0,"uniformizacao_facial":0,"heraldizacao":0,"enquadramento_arquitetonico":0,"apagamento_narrativo":0,"monocromatizacao":0,"serialidade":0,"inscricao_estatal":0,"regime_iconocratico":"","notes":""}}"""


def load_pathos() -> dict[str, dict]:
    with open(PATHOS_INDEX) as f:
        items = {}
        for l in f:
            try:
                item = json.loads(l)
                items[item["item_id"]] = item
            except:
                pass
        return items


def load_records() -> dict[str, dict]:
    with open(RECORDS_PATH) as f:
        return {json.loads(l)["item_id"]: json.loads(l) for l in f if l.strip()}


def firecrawl_extract(url: str, sigla: str) -> str | None:
    """Extract content from URL via firecrawl CLI."""
    cache_file = FC_EXTRACT_DIR / f"{sigla}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")[:800]
    
    try:
        result = subprocess.run(
            ["npx", "-y", "firecrawl-cli@latest", "scrape", url, "--format", "markdown"],
            capture_output=True, text=True, timeout=30
        )
        text = (result.stdout or "") + (result.stderr or "")
        # Clean up
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 50:
            cache_file.write_text(text[:1500])
            return text[:800]
        return None
    except Exception as e:
        print(f"    FC error: {e}", file=sys.stderr)
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
            return msg.get("content", "") or msg.get("thinking", "") or None
    except Exception as e:
        print(f"  [Ollama ERR] {e}", file=sys.stderr)
        return None


def parse_json(raw: str) -> dict | None:
    cleaned = raw.strip()
    for prefix in ["```json", "```", "json"]:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Find last JSON object
    start = cleaned.rfind("{")
    end = cleaned.rfind("}")
    if 0 <= start < end:
        try:
            return json.loads(cleaned[start:end+1])
        except json.JSONDecodeError:
            pass
    return None


def main():
    print("=== E3 Firecrawl Recode ===\n")
    
    all_items = load_pathos()
    records = load_records()
    
    # Find items with score 0.0
    zeros = {k: v for k, v in all_items.items() if v["purificacao_composto"] == 0.0}
    print(f"Items to recode: {len(zeros)}\n")
    
    successes = 0
    failures = 0
    updated = []
    
    for i, (item_id, item) in enumerate(sorted(zeros.items())):
        rec = records.get(item_id, {})
        inp = rec.get("input", {})
        url = inp.get("input_url", "") or item.get("url", "")
        title = inp.get("title_hint", item.get("title", ""))
        place = inp.get("place_hint", item.get("place", ""))
        date = inp.get("date_hint", item.get("date", ""))
        
        print(f"[{i+1}/{len(zeros)}] {item['sigla_id']:<15} FC extracting...", end=" ", flush=True)
        
        # Extract via Firecrawl
        desc = firecrawl_extract(url, item.get("sigla_id", str(i)))
        if not desc:
            # Fallback to existing summary
            ws = rec.get("webscout", {})
            desc = ws.get("summary_evidence", "") or title
            print(f"(using fallback)", end=" ")
        else:
            print(f"(FC: {len(desc)}ch)", end=" ")
        
        prompt = CODING_PROMPT.format(
            title=str(title)[:100],
            place=str(place),
            date=str(date),
            description=str(desc)[:700],
        )
        
        print("coding...", end=" ", flush=True)
        raw = call_ollama(prompt)
        if not raw:
            print("FAILED")
            failures += 1
            continue
        
        parsed = parse_json(raw)
        if not parsed:
            print("PARSE FAIL")
            failures += 1
            continue
        
        # Validate indicators
        indicators = {}
        for ind in INDICATORS:
            val = parsed.get(ind)
            if isinstance(val, (int, float)) and 0 <= val <= 3:
                indicators[ind] = int(val)
            else:
                indicators[ind] = 0
        
        # Parse regime
        regime_raw = parsed.get("regime_iconocratico", "")
        if isinstance(regime_raw, dict):
            regime_raw = str(list(regime_raw.values())[0]) if regime_raw.values() else ""
        regime = str(regime_raw).strip().lower()
        if regime not in REGIMES:
            for r in REGIMES:
                if r in regime:
                    regime = r
                    break
            else:
                regime = item.get("regime_iconocratico", "fundacional")
        
        score = sum(indicators.values()) / len(indicators)
        notes = parsed.get("notes", "")
        if isinstance(notes, dict):
            notes = str(list(notes.values())[0]) if notes.values() else ""
        notes = str(notes)[:300]
        
        updated_item = dict(item)
        updated_item.update(indicators)
        updated_item["purificacao_composto"] = round(score, 1)
        updated_item["regime_iconocratico"] = regime
        updated_item["notes"] = notes
        updated_item["coded_by"] = "e1-gemma4/gemma4-fcrecode"
        updated_item["coded_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        updated.append(updated_item)
        print(f"score={score:.1f}, regime={regime}")
        successes += 1
        
        if i < len(zeros) - 1:
            time.sleep(1)
    
    print(f"\n=== Summary ===")
    print(f"Success: {successes} | Failures: {failures}")
    
    if updated:
        # Merge: replace zeros, keep the rest
        for u in updated:
            all_items[u["item_id"]] = u
        
        with open(PATHOS_INDEX, "w") as f:
            for item in sorted(all_items.values(), key=lambda x: x.get("sigla_id", "")):
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"\nWrote {len(all_items)} items to {PATHOS_INDEX}")
    
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
