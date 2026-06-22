#!/usr/bin/env python3
"""
irr_rater2_batch.py — Cross-model blind coding for IRR re-run (Rater-2).

Loads IRR sample metadata, finds best image URLs, sends to rater-2 model
(Claude Sonnet 4 via OpenRouter) with blind IconoCode prompt, saves results.

Usage:
    python tools/scripts/irr_rater2_batch.py --sample data/processed/irr_re_run/sample_metadata.jsonl --dry-run
    python tools/scripts/irr_rater2_batch.py --sample data/processed/irr_re_run/sample_metadata.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai library required. Install with: pip install openai", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CODEBOOK_PATH = REPO_ROOT / "data" / "docs" / "codebook.md"

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


def load_codebook() -> str:
    if not CODEBOOK_PATH.exists():
        raise FileNotFoundError(f"Codebook file not found: {CODEBOOK_PATH}")
    return CODEBOOK_PATH.read_text(encoding="utf-8")


def load_sample_metadata(sample_path: Path) -> list[dict]:
    if not sample_path.exists():
        raise FileNotFoundError(f"Sample metadata not found: {sample_path}")
    items = []
    with open(sample_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items


def get_best_image_url(record: dict) -> str | None:
    """
    Find the best available image URL from records.jsonl webscout data.
    Priority: Gallica IIIF > direct image URLs > search result URLs
    """
    ws = record.get("webscout", {})
    search_results = ws.get("search_results", [])
    input_url = record.get("input", {}).get("input_url", "")

    # 1. Gallica IIIF direct image
    for res in search_results:
        url = res.get("url", "")
        if "gallica.bnf.fr" in url and "ark:/" in url:
            # Convert to IIIF
            import re
            match = re.search(r"(ark:/12148/[a-z0-9]+)", url)
            if match:
                ark = match.group(1)
                return f"https://gallica.bnf.fr/iiif/{ark}/f1/full/full/0/native.jpg"

    # 2. Direct image URLs from primary_image results
    for res in search_results:
        if res.get("source_type") == "primary_image":
            url = res.get("url", "")
            # Check if it's a direct image URL
            if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                return url

    # 3. Any URL from primary_image (might be HTML page with image)
    for res in search_results:
        if res.get("source_type") == "primary_image":
            url = res.get("url", "")
            if url:
                return url

    # 4. Input URL
    if input_url:
        return input_url

    # 5. First search result URL
    for res in search_results:
        url = res.get("url", "")
        if url:
            return url

    return None


def load_records() -> dict[str, dict]:
    """Load records.jsonl indexed by item_id."""
    records_path = REPO_ROOT / "data" / "processed" / "records.jsonl"
    records = {}
    if records_path.exists():
        with open(records_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    if "item_id" in rec:
                        records[rec["item_id"]] = rec
    return records


BLIND_PROMPT_TEMPLATE = """Você é um codificador iconográfico sintético da tese de doutorado "ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)" (PPGD/UFSC).

Sua tarefa é analisar a imagem fornecida e avaliar os 10 indicadores de Purificação Clássica (endurecimento) descritos no Codebook oficial abaixo.

### CODEBOOK DE REFERÊNCIA
{codebook}

### METADADOS DO ITEM EM ANÁLISE
- ID do Item: {item_id}
- Título do Item: {title}
- Suporte/Meio Material: {support}
- País/Local: {place}
- Data/Período: {date}

### INSTRUÇÕES DE AVALIAÇÃO
1. Analise cuidadosamente os aspectos visuais e de contexto do item à luz do Codebook.
2. Para cada um dos 10 indicadores ordinais, atribua uma nota inteira de 0 a 3:
   - 0: Ausente
   - 1: Fraco / vestigial
   - 2: Moderado / parcial
   - 3: Forte / dominante
3. Atribua também um regime iconocrático: fundacional | normativo | militar | contra-alegoria
4. Avalie a condição da imagem: visivel | parcialmente_visivel | ilegivel | nao_carregou
5. Forneça uma justificativa qualitativa concisa e fundamentada para cada nota baseada no que é visível na imagem e nos metadados fornecidos.
6. Responda estritamente no formato JSON estruturado definido, sem textos adicionais fora do JSON.

IMPORTANTE: Você NÃO tem acesso aos scores de outros codificadores. Esta é uma avaliação CEGA independente.
"""

# JSON Schema for structured output
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "item_id": {"type": "string"},
        "indicadores": {
            "type": "object",
            "properties": {
                "desincorporacao": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "rigidez_postural": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "dessexualizacao": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "uniformizacao_facial": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "heraldizacao": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "enquadramento_arquitetonico": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "apagamento_narrativo": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "monocromatizacao": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "serialidade": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
                "inscricao_estatal": {"type": "object", "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 3}, "justification": {"type": "string"}}},
            },
            "required": ["desincorporacao", "rigidez_postural", "dessexualizacao", "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico", "apagamento_narrativo", "monocromatizacao", "serialidade", "inscricao_estatal"],
        },
        "regime_iconocratico": {"type": "string", "enum": ["fundacional", "normativo", "militar", "contra-alegoria"]},
        "image_condition": {"type": "string", "enum": ["visivel", "parcialmente_visivel", "ilegivel", "nao_carregou"]},
    },
    "required": ["item_id", "indicadores", "regime_iconocratico", "image_condition"],
}


def call_openrouter(client: OpenAI, prompt: str, image_url: str, model: str) -> dict | None:
    """Call OpenRouter API with image URL and prompt."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            response_format={"type": "json_schema", "json_schema": {"name": "irr_coding", "schema": RESPONSE_SCHEMA, "strict": True}},
            temperature=0.1,
            max_tokens=4096,
        )
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
    except Exception as e:
        print(f"  [API Error] {e}", file=sys.stderr)
    return None


def generate_mock_response(item_id: str) -> dict:
    """Generate a valid mock JSON response for dry-run testing."""
    return {
        "item_id": item_id,
        "indicadores": {
            "desincorporacao": {"score": 2, "justification": "Idealized figure, moderate abstraction of natural form."},
            "rigidez_postural": {"score": 1, "justification": "Contained pose but holds dynamic flag."},
            "dessexualizacao": {"score": 2, "justification": "Draped in classical toga, low eroticism."},
            "uniformizacao_facial": {"score": 2, "justification": "Neoclassical face mask, typical profile."},
            "heraldizacao": {"score": 1, "justification": "Carrying standard and scales."},
            "enquadramento_arquitetonico": {"score": 3, "justification": "Fully framed inside medal circular border."},
            "apagamento_narrativo": {"score": 3, "justification": "Isolated portrait on neutral background."},
            "monocromatizacao": {"score": 3, "justification": "Printed in monochrome ink on paper."},
            "serialidade": {"score": 3, "justification": "Mass printed document/periodical."},
            "inscricao_estatal": {"score": 3, "justification": "Contains clear state decree text."},
        },
        "regime_iconocratico": "fundacional",
        "image_condition": "visivel",
    }


def main():
    parser = argparse.ArgumentParser(description="Cross-model blind coding for IRR re-run (Rater-2)")
    parser.add_argument("--sample", type=Path, default=REPO_ROOT / "data" / "processed" / "irr_re_run" / "sample_metadata.jsonl",
                        help="Path to sample metadata JSONL")
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "data" / "processed" / "irr_re_run" / "rater2_results.jsonl",
                        help="Output path for rater-2 results")
    parser.add_argument("--model", default="anthropic/claude-sonnet-4",
                        help="OpenRouter model identifier (default: anthropic/claude-sonnet-4)")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY env)")
    parser.add_argument("--dry-run", action="store_true", help="Use mock responses for testing")
    parser.add_argument("--resume", action="store_true", help="Resume from existing output file")
    args = parser.parse_args()

    print("=== IRR Re-run Rater-2 Batch Coding ===\n")

    # Load codebook
    print("Loading codebook...")
    codebook = load_codebook()

    # Load sample metadata
    print(f"Loading sample metadata from {args.sample}...")
    sample_items = load_sample_metadata(args.sample)
    print(f"  Loaded {len(sample_items)} items")

    # Load records for metadata enrichment
    records = load_records()

    # Check for API key
    if not args.dry_run:
        api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OpenRouter API key required. Set OPENROUTER_API_KEY or pass --api-key", file=sys.stderr)
            sys.exit(1)
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        print(f"Using model: {args.model}")

    # Resume capability
    processed_ids = set()
    if args.resume and args.output.exists():
        with open(args.output, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "item_id" in data:
                            processed_ids.add(data["item_id"])
                    except Exception:
                        pass
        print(f"Resuming: {len(processed_ids)} items already processed")

    # Prepare output
    args.output.parent.mkdir(parents=True, exist_ok=True)

    success_count = 0
    skipped_count = 0

    with open(args.output, "a", encoding="utf-8") as out_file:
        for idx, item in enumerate(sample_items, 1):
            item_id = item["item_id"]
            if item_id in processed_ids:
                continue

            print(f"\n[{idx}/{len(sample_items)}] Processing item: {item_id}")

            # Get record for metadata
            record = records.get(item_id, {})
            inp = record.get("input", {})
            title = inp.get("title_hint", "Sem Título")
            place = inp.get("place_hint", "Desconhecido")
            date_hint = inp.get("date_hint", "Desconhecida")
            support = item.get("support", "Desconhecido")

            # Find best image URL
            image_url = get_best_image_url(record)
            if not image_url:
                print(f"  WARN: No image URL found for {item_id}. Skipping.")
                skipped_count += 1
                continue

            print(f"  Image URL: {image_url[:80]}")

            # Build prompt
            prompt = BLIND_PROMPT_TEMPLATE.format(
                codebook=codebook,
                item_id=item_id,
                title=title,
                support=support,
                place=place,
                date=date_hint,
            )

            if args.dry_run:
                print("  [Mock] Generating mock coding result...")
                result = generate_mock_response(item_id)
            else:
                print(f"  [API] Calling {args.model}...")
                result = call_openrouter(client, prompt, image_url, args.model)
                if not result:
                    print(f"  ERROR: Failed to get valid response for {item_id}")
                    skipped_count += 1
                    continue

            # Validate and enrich
            result["item_id"] = item_id
            result["coded_by"] = f"rater2-{args.model.replace('/', '-')}"
            result["coded_at"] = datetime.now(timezone.utc).isoformat()
            result["sample_index"] = item.get("sample_index", idx)

            # Calculate composite score
            scores = [result["indicadores"][ind]["score"] for ind in INDICATORS]
            result["purificacao_composto"] = round(sum(scores) / len(scores), 2)

            # Write output
            out_file.write(json.dumps(result, ensure_ascii=False) + "\n")
            out_file.flush()
            print(f"  ✅ Success: composite={result['purificacao_composto']:.2f}, regime={result['regime_iconocratico']}")
            success_count += 1

            # Rate limiting
            if not args.dry_run:
                time.sleep(1.5)

    print(f"\n=== Summary ===")
    print(f"Total items: {len(sample_items)}")
    print(f"Success: {success_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Output: {args.output}")

    return 0 if skipped_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())