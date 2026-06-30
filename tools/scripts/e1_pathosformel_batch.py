#!/usr/bin/env python3
"""
e1_pathosformel_batch.py — IMES E1 Pathosformel extraction batch runner.

Reads records.jsonl, identifies items without purification coding,
applies Gemma-4 (via Ollama) to code the 10 purification indicators,
and writes results to data/processed/pathosformel_index.jsonl.

Usage:
    python tools/scripts/e1_pathosformel_batch.py --dry-run     # Test on 5 items
    python tools/scripts/e1_pathosformel_batch.py --batch 50    # Code 50 items
    python tools/scripts/e1_pathosformel_batch.py --all          # Code all uncoded
    python tools/scripts/e1_pathosformel_batch.py --list         # List uncoded only
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
OUTPUT_PATH = REPO / "data" / "processed" / "pathosformel_index.jsonl"
PURIFICATION_PATH = REPO / "data" / "processed" / "purification.jsonl"

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma4"
OLLAMA_TIMEOUT = 300  # seconds per item (gemma4 is slow on MPS)

CITATION_ABNT = (
    "ITEM. In: ICONOCRACIA Corpus Digital de Alegorias Femininas. "
    "Florianópolis: PPGD/UFSC, 2026. "
    "Disponível em: https://iconocracia-companion.warholana.workers.dev. "
    "Acesso em: {date}."
)

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

REGIMES = ["fundacional", "normativo", "militar", "contra-alegoria"]

CODING_PROMPT = """Code the 10 purification indicators (0-3) and regime. Output ONLY valid JSON.

Item: {title} | {place} | {date}
Description: {summary}

Fields: desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial, heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal (each 0-3), regime_iconocratico (fundacional|normativo|militar|contra-alegoria), notes (brief justification)

JSON:"""


def load_records() -> list[dict]:
    with open(RECORDS_PATH) as f:
        return [json.loads(l) for l in f if l.strip()]


def load_corpus() -> dict[str, dict]:
    """Load corpus-data.json and index by URL for sigla lookup."""
    with open(CORPUS_PATH) as f:
        items = json.load(f)
    url_to_item: dict[str, dict] = {}
    for item in items:
        url = item.get("url", "")
        if url:
            url_to_item[url] = item
    return url_to_item


def build_url_map(records: list[dict]) -> dict[str, dict]:
    """Build URL -> record mapping."""
    url_map: dict[str, dict] = {}
    for r in records:
        url = r.get("input", {}).get("input_url", "")
        if url:
            url_map[url] = r
    return url_map


def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str | None:
    """Call Ollama API and return response content (thinking or content field)."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 2048}
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read())
            # Gemma-4 may output in 'thinking' field instead of 'content'
            msg = data.get("message", {})
            content = msg.get("content", "") or ""
            thinking = msg.get("thinking", "") or ""
            return content or thinking or None
    except Exception as e:
        print(f"  [ERROR] Ollama call failed: {e}", file=sys.stderr)
        return None


def parse_llm_response(raw: str) -> dict | None:
    """Try to parse JSON from LLM response, handling thinking prefix."""
    cleaned = raw.strip()
    
    # Strip markdown fences if present
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:])
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    if cleaned.startswith("json"):
        cleaned = cleaned[4:].strip()

    # Try parsing the whole thing first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Find the LAST JSON object in the text (model outputs thinking first, then JSON)
    # Look for the last occurrence of '{' that starts a valid JSON ending with '}'
    last_start = cleaned.rfind("{")
    last_end = cleaned.rfind("}")
    
    if last_start >= 0 and last_end > last_start:
        candidate = cleaned[last_start:last_end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    
    # Try the first JSON block
    first_start = cleaned.find("{")
    first_end = cleaned.rfind("}")
    if first_start >= 0 and first_end > first_start:
        candidate = cleaned[first_start:first_end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    
    return None


def get_webscout_text(record: dict) -> str:
    """Extract webscout description from a record."""
    ws = record.get("webscout", {})
    summary = ws.get("summary_evidence", "")
    results = ws.get("search_results", [])
    extra = []
    for r in results:
        notes = r.get("notes", "")
        if notes:
            extra.append(notes)
    all_text = summary
    if extra:
        all_text += " " + " ".join(extra[:3])
    return all_text.strip() or "No description available."


def code_item(record: dict, corpus_url_map: dict[str, dict]) -> dict | None:
    """Code a single item using Gemma-4 via Ollama."""
    item_id = record["item_id"]
    inp = record.get("input", {})
    url = inp.get("input_url", "")
    title = inp.get("title_hint", "Untitled")
    place = inp.get("place_hint", "Unknown")
    date_hint = inp.get("date_hint", "")

    summary = get_webscout_text(record)

    # Get sigla from corpus URL map
    sigla = ""
    corpus_item = corpus_url_map.get(url)
    if corpus_item:
        sigla = corpus_item.get("id", "")
    else:
        # Fallback: search by URL match
        # We already verified all 52 map, so this shouldn't trigger
        sigla = item_id[:12]

    # Build prompt
    prompt = CODING_PROMPT.format(
        title=title[:100],
        place=place,
        date=date_hint,
        summary=summary[:500]
    )

    print(f"  Calling Gemma-4 for {sigla or item_id[:12]}...", end=" ", flush=True)
    raw = call_ollama(prompt)
    if not raw:
        print("FAILED (no response)")
        return None

    parsed = parse_llm_response(raw)
    if not parsed:
        print("FAILED (parse error)")
        print(f"    Raw: {raw[:200]}...")
        return None

    # Validate indicators
    indicators = {}
    for ind in INDICATORS:
        val = parsed.get(ind)
        if isinstance(val, (int, float)) and 0 <= val <= 3:
            indicators[ind] = int(val)
        else:
            indicators[ind] = 0  # default on bad parse

    regime = parsed.get("regime_iconocratico", "").strip().lower()
    if regime not in REGIMES:
        # Try to match
        for r in REGIMES:
            if r in regime:
                regime = r
                break
        else:
            regime = "fundacional"  # safe default

    composto = sum(indicators.values()) / len(indicators)
    notes = parsed.get("notes", "")
    if not isinstance(notes, str):
        notes = str(notes)
    notes = notes[:200]

    coded_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = {
        "item_id": item_id,
        "sigla_id": sigla,
        "title": title,
        "place": place,
        "date": date_hint,
        "url": url,
        "coded_by": f"e1-gemma4/{OLLAMA_MODEL}",
        "coded_at": coded_at,
        **indicators,
        "purificacao_composto": round(composto, 1),
        "regime_iconocratico": regime,
        "notes": notes,
    }

    print(f"DONE (score={composto:.1f}, regime={regime})")
    return result


def write_output(results: list[dict], output_path: Path):
    """Merge results into pathosformel_index.jsonl, deduped by item_id.

    Idempotent: re-running with the same results does not duplicate entries.
    Existing items are preserved; matching item_ids are overwritten.
    """
    merged: dict[str, dict] = {}
    if output_path.exists():
        with open(output_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    merged[item["item_id"]] = item
                except (json.JSONDecodeError, KeyError):
                    continue
    for r in results:
        merged[r["item_id"]] = r
    with open(output_path, "w") as f:
        for item in merged.values():
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(results)} items to {output_path} ({len(merged)} total)")


def list_uncoded(records: list[dict], corpus_url_map: dict[str, dict]):
    """List all uncoded items with metadata."""
    uncoded = [r for r in records
               if r.get("purificacao", {}).get("purificacao_composto") in (None, -1)]
    print(f"\nUncoded items: {len(uncoded)}\n")
    print(f"{'SIGLA':<15} {'TITLE':<55} {'PLACE':<12} {'DATE':<15}")
    print("-" * 100)
    for r in uncoded:
        url = r.get("input", {}).get("input_url", "")
        corpus_item = corpus_url_map.get(url, {})
        sigla = corpus_item.get("id", "???")
        inp = r.get("input", {})
        print(f"{sigla:<15} {inp.get('title_hint','?')[:53]:<55} "
              f"{inp.get('place_hint','?'):<12} {inp.get('date_hint','?'):<15}")


def main():
    parser = argparse.ArgumentParser(description="E1 Pathosformel batch runner")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="Test on 5 items")
    group.add_argument("--batch", type=int, metavar="N", help="Code N items")
    group.add_argument("--all", action="store_true", help="Code all uncoded items")
    group.add_argument("--list", action="store_true", help="List uncoded items")
    parser.add_argument("--start", type=int, default=0, help="Skip first N uncoded items")
    args = parser.parse_args()

    if not any([args.dry_run, args.batch, args.all, args.list]):
        parser.print_help()
        sys.exit(1)

    print("=== E1 Pathosformel Extraction ===\n")

    records = load_records()
    corpus_url_map = load_corpus()

    uncoded = [r for r in records
               if r.get("purificacao", {}).get("purificacao_composto") in (None, -1)]

    if args.list:
        list_uncoded(records, corpus_url_map)
        return

    if not uncoded:
        print("All items already coded. Nothing to do.")
        return

    print(f"Records: {len(records)} | Uncoded: {len(uncoded)}")

    # Determine how many to process
    if args.dry_run:
        count = min(5, len(uncoded))
    elif args.all:
        count = len(uncoded)
    else:
        count = min(args.batch, len(uncoded))

    start = args.start
    target = uncoded[start:start + count]

    print(f"Processing: {len(target)} items (offset={start})\n")

    results = []
    failures = 0

    for i, record in enumerate(target):
        print(f"[{start + i + 1}/{len(uncoded)}] ", end="")
        result = code_item(record, corpus_url_map)
        if result:
            results.append(result)
        else:
            failures += 1
            print(f"  -> SKIPPED")

        # Small delay between items to avoid hammering ollama
        if i < len(target) - 1:
            time.sleep(1)

    print(f"\n=== Summary ===")
    print(f"Success: {len(results)} | Failures: {failures}")

    if results:
        if args.dry_run:
            print(f"\nDry-run results (NOT written):")
            for r in results:
                print(f"  {r['sigla_id']:<12} score={r['purificacao_composto']:.1f} "
                      f"regime={r['regime_iconocratico']:<15} notes={r['notes'][:60]}")
            print(f"\nTo write, run with --batch N or --all")
        else:
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            write_output(results, OUTPUT_PATH)
            print(f"\nOutput schema ({len(INDICATORS)} indicators + regime + score)")
            if results:
                print(json.dumps(list(results[0].keys()), ensure_ascii=False))

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
