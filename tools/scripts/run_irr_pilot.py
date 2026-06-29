#!/usr/bin/env python3
"""
run_irr_pilot.py

Run the multimodal Gemini 1.5 Pro evaluation on the 30-item IRR sample.
Uses the modern google-genai SDK.

Usage:
    python tools/scripts/run_irr_pilot.py [--api-key KEY] [--dry-run] [--mock]
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    from pydantic import BaseModel, Field
except ImportError as e:
    raise ImportError(
        "Required libraries not found. Ensure you run this script using "
        "the correct Conda environment (e.g. iconocracy)."
    ) from e

# Repo Paths
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CODEBOOK_PATH = REPO_ROOT / "data" / "docs" / "codebook.md"
METADATA_PATH = REPO_ROOT / "data" / "processed" / "irr_sample_metadata.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "irr_pilot_synthetic_results.jsonl"
MOCK_OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "irr_pilot_synthetic_results_mock.jsonl"
ID_MAPPING_PATH = REPO_ROOT / "data" / "processed" / "id-mapping.json"
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
CACHE_DIR = REPO_ROOT / ".cache" / "iconocode-images"

# Manual fallbacks for known items without direct mappings or local files
MANUAL_IMAGE_FALLBACKS = {
    "787ce58d-f363-5bdb-bfbe-6a6a531624bd": "FR-PIAST-1885.jpg"  # Numista Piastre mapping
}


# Define Pydantic schema for structured output
class IndicadorScore(BaseModel):
    score: int = Field(..., ge=0, le=3, description="Nota inteira de 0 a 3 conforme o codebook.")
    justification: str = Field(..., description="Justificativa qualitativa concisa baseada no codebook e na análise visual.")

class Indicadores(BaseModel):
    desincorporacao: IndicadorScore
    rigidez_postural: IndicadorScore
    dessexualizacao: IndicadorScore
    uniformizacao_facial: IndicadorScore
    heraldizacao: IndicadorScore
    enquadramento_arquitetonico: IndicadorScore
    apagamento_narrativo: IndicadorScore
    monocromatizacao: IndicadorScore
    serialidade: IndicadorScore
    inscricao_estatal: IndicadorScore

class PilotCodingResult(BaseModel):
    item_id: str = Field(..., description="O item_id correspondente da imagem analisada.")
    indicadores: Indicadores


def get_gallica_iiif_url(url: str) -> Optional[str]:
    """Extract Gallica ARK identifier and build IIIF direct image link."""
    match = re.search(r"(ark:/12148/[a-z0-9]+)", url)
    if match:
        ark = match.group(1)
        return f"https://gallica.bnf.fr/iiif/{ark}/f1/full/full/0/native.jpg"
    return None


def download_image(url: str, dest_path: Path) -> bool:
    """Download an image file from a URL to dest_path."""
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        headers = {
            "User-Agent": "iconocracy-corpus-irr-pilot/1.0 (+https://github.com/anavvanzin/iconocracy-corpus)"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            dest_path.write_bytes(content)
        return True
    except Exception as e:
        print(f"  [Downloader] Error downloading from {url}: {e}", file=sys.stderr)
        return False


def resolve_image_path(item_id: str, corpus_id: str, record: Dict[str, Any]) -> Optional[Path]:
    """Find the image path on disk or SSD, falling back to download if Gallica URL."""
    # List of directories to search
    search_dirs = [
        Path("/media/ana/SSD_DATA/images"),
        Path("/media/ana/SSD_DATA"),
        REPO_ROOT / "images",
        REPO_ROOT / "Images",
        REPO_ROOT / "Images" / "Images",
        REPO_ROOT / "binaries" / "Images",
        CACHE_DIR,
    ]

    filenames_to_try = []

    # 1. Manual override check
    if item_id in MANUAL_IMAGE_FALLBACKS:
        filenames_to_try.append(MANUAL_IMAGE_FALLBACKS[item_id])

    # 2. Try corpus_id variants
    if corpus_id:
        filenames_to_try.extend([
            f"{corpus_id}.jpg", f"{corpus_id}.jpeg", f"{corpus_id}.png",
            f"{corpus_id.lower()}.jpg", f"{corpus_id.lower()}.jpeg", f"{corpus_id.lower()}.png",
            f"{corpus_id.upper()}.jpg", f"{corpus_id.upper()}.jpeg", f"{corpus_id.upper()}.png"
        ])

    # 3. Try item_id variants
    if item_id:
        filenames_to_try.extend([
            f"{item_id}.jpg", f"{item_id}.jpeg", f"{item_id}.png",
            f"{item_id.lower()}.jpg", f"{item_id.lower()}.jpeg", f"{item_id.lower()}.png",
            f"{item_id.upper()}.jpg", f"{item_id.upper()}.jpeg", f"{item_id.upper()}.png"
        ])

    # Search for files matching names exactly
    for sdir in search_dirs:
        if not sdir.exists():
            continue
        for fname in filenames_to_try:
            p = sdir / fname
            if p.exists() and p.is_file():
                return p

    # Case-insensitive stem search
    for sdir in search_dirs:
        if not sdir.exists():
            continue
        try:
            for file_path in sdir.iterdir():
                if file_path.is_file():
                    stem = file_path.stem.lower()
                    if corpus_id and stem == corpus_id.lower():
                        return file_path
                    if item_id and stem == item_id.lower():
                        return file_path
        except Exception:
            pass

    # 4. Fallback to download if it is a Gallica URL
    url = record.get("input", {}).get("input_url") or ""
    # Check webscout search results as fallback
    if not url:
        for res in record.get("webscout", {}).get("search_results", []):
            if res.get("url"):
                url = res["url"]
                break

    if "gallica.bnf.fr" in url:
        iiif_url = get_gallica_iiif_url(url)
        if iiif_url:
            dest = CACHE_DIR / f"{item_id}.jpg"
            print(f"  [Downloader] Found Gallica URL. Fetching IIIF image to {dest.name}...")
            if download_image(iiif_url, dest):
                return dest

    return None


def generate_mock_response(item_id: str) -> Dict[str, Any]:
    """Generate a valid mock JSON response for dry-run/mock testing."""
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
            "inscricao_estatal": {"score": 3, "justification": "Contains clear state decree text."}
        }
    }


def load_codebook() -> str:
    if not CODEBOOK_PATH.exists():
        raise FileNotFoundError(f"Codebook file not found: {CODEBOOK_PATH}")
    return CODEBOOK_PATH.read_text(encoding="utf-8")


def load_mapping() -> Dict[str, str]:
    item_to_corpus = {}
    if ID_MAPPING_PATH.exists():
        with open(ID_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping_data = json.load(f)
            for m in mapping_data.get("mapping", []):
                item_to_corpus[m["item_id"]] = m["corpus_id"]
    return item_to_corpus


def load_records() -> Dict[str, Dict[str, Any]]:
    records = {}
    if RECORDS_PATH.exists():
        with open(RECORDS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    if "item_id" in rec:
                        records[rec["item_id"]] = rec
    return records


def load_sample() -> List[Dict[str, Any]]:
    sample = []
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    sample.append(json.loads(line))
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multimodal Gemini pilot for IRR coding")
    parser.add_argument("--api-key", help="Gemini API Key (overrides GEMINI_API_KEY environment variable)")
    parser.add_argument("--dry-run", action="store_true", help="Resolve paths and render prompt without invoking API")
    parser.add_argument("--mock", action="store_true", help="Run full pipeline using mock JSON output (for testing)")
    args = parser.parse_args()

    # Load data
    print("Loading codebook, mapping, records, and sample...")
    codebook_content = load_codebook()
    item_to_corpus = load_mapping()
    records = load_records()
    sample = load_sample()

    if not sample:
        print(f"Error: Sample metadata file empty or not found: {METADATA_PATH}")
        sys.exit(1)

    print(f"Loaded {len(sample)} items in sample.")

    # Determine output path based on mock setting
    output_path = MOCK_OUTPUT_PATH if args.mock else OUTPUT_PATH

    # Initialize client if not dry-run or mock
    client = None
    if not args.dry_run and not args.mock:
        api_key = args.api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable or --api-key argument is required.")
            sys.exit(1)
        client = genai.Client(api_key=api_key)

    # Resume capability: load already processed items
    processed_ids = set()
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "item_id" in data:
                            processed_ids.add(data["item_id"])
                    except Exception:
                        pass
        print(f"Resuming: {len(processed_ids)} items already processed.")

    # Open output file in append mode
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success_count = 0
    skipped_count = 0

    with open(output_path, "a", encoding="utf-8") as out_file:
        for idx, item in enumerate(sample, 1):
            item_id = item["item_id"]
            if item_id in processed_ids:
                continue

            print(f"\n[{idx}/{len(sample)}] Processing item ID: {item_id}")

            # Find record info
            rec = records.get(item_id, {})
            title = rec.get("input", {}).get("title_hint", "Sem Título")
            place = rec.get("input", {}).get("place_hint", "Desconhecido")
            date = rec.get("input", {}).get("date_hint", "Desconhecida")
            support = item.get("suporte", rec.get("suporte", "Desconhecido"))
            regime = item.get("regime", rec.get("regime", "Desconhecido"))
            corpus_id = item_to_corpus.get(item_id, "")

            # Resolve image
            img_path = resolve_image_path(item_id, corpus_id, rec)
            if not img_path:
                print(f"  WARN: Image not found for item {item_id} (corpus_id: {corpus_id}). Skipping.")
                skipped_count += 1
                continue

            print(f"  Resolved image path: {img_path}")

            # Construct Prompt
            prompt = f"""Você é um codificador iconográfico sintético da tese de doutorado "ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)" (PPGD/UFSC).

Sua tarefa é analisar a imagem fornecida e avaliar os 10 indicadores de Purificação Clássica (endurecimento) descritos no Codebook oficial abaixo.

### CODEBOOK DE REFERÊNCIA
{codebook_content}

### METADADOS DO ITEM EM ANÁLISE
- ID do Item: {item_id}
- Título do Item: {title}
- Suporte/Meio Material: {support}
- Regime Iconocrático Declarado: {regime}
- País/Local: {place}
- Data/Período: {date}

### INSTRUÇÕES DE AVALIAÇÃO
1. Analise cuidadosamente os aspectos visuais e de contexto do item à luz do Codebook.
2. Para cada um dos 10 indicadores ordinais, atribua uma nota inteira de 0 a 3:
   - 0: Ausente
   - 1: Fraco / vestigial
   - 2: Moderado / parcial
   - 3: Forte / dominante
3. Forneça uma justificativa qualitativa concisa e fundamentada para cada nota baseada no que é visível na imagem e nos metadados fornecidos.
4. Responda estritamente no formato JSON estruturado definido, sem textos adicionais fora do JSON.
"""

            if args.dry_run:
                print("  [Dry-Run] Prompt generated and image path verified. Skipping API call.")
                success_count += 1
                continue

            # Load and process image
            result_dict = None
            try:
                with Image.open(img_path) as img:
                    img.load()

                    # API Call or Mock
                    if args.mock:
                        print("  [Mock] Generating mock coding result...")
                        mock_dict = generate_mock_response(item_id)
                        validated_obj = PilotCodingResult.model_validate(mock_dict)
                        result_dict = validated_obj.model_dump()
                    else:
                        print("  [Gemini] Calling Gemini 1.5 Pro...")
                        try:
                            response = client.models.generate_content(
                                model="gemini-1.5-pro",
                                contents=[img, prompt],
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json",
                                    response_schema=PilotCodingResult,
                                    temperature=0.1,
                                )
                            )
                            validated_obj = PilotCodingResult.model_validate_json(response.text)
                            result_dict = validated_obj.model_dump()
                        except Exception as e:
                            print(f"  Error: Gemini API call or validation failed: {e}", file=sys.stderr)
                            # Retry once after 5 seconds
                            print("  Retrying in 5 seconds...")
                            time.sleep(5)
                            try:
                                response = client.models.generate_content(
                                    model="gemini-1.5-pro",
                                    contents=[img, prompt],
                                    config=types.GenerateContentConfig(
                                        response_mime_type="application/json",
                                        response_schema=PilotCodingResult,
                                        temperature=0.1,
                                    )
                                )
                                validated_obj = PilotCodingResult.model_validate_json(response.text)
                                result_dict = validated_obj.model_dump()
                            except Exception as e2:
                                print(f"  Error: Gemini API call retry or validation failed: {e2}", file=sys.stderr)
                                skipped_count += 1
            except (Image.UnidentifiedImageError, OSError) as e:
                print(f"  WARN: Failed to open or load image {img_path}: {e}")
                try:
                    img_path.resolve().relative_to(CACHE_DIR.resolve())
                    is_downloaded = True
                except ValueError:
                    is_downloaded = False

                if is_downloaded and img_path.exists():
                    try:
                        img_path.unlink()
                        print(f"  [Cleanup] Deleted corrupt downloaded image: {img_path}")
                    except Exception as unlink_err:
                        print(f"  Error deleting corrupt image: {unlink_err}", file=sys.stderr)
                skipped_count += 1

            if result_dict is None:
                continue

            # Write output
            out_file.write(json.dumps(result_dict, ensure_ascii=False) + "\n")
            out_file.flush()
            print("  Successfully processed and saved results.")
            success_count += 1

            # Brief sleep to avoid hitting rate limits
            if not args.mock and not args.dry_run:
                time.sleep(2)

    print(f"\nExecution finished. Success: {success_count}, Skipped: {skipped_count}.")
    print(f"Results output path: {output_path}")


if __name__ == "__main__":
    main()
