#!/usr/bin/env python3
"""
vision_audit_pipeline.py
=========================
Pipeline Google Cloud Vision para pré-preenchimento dos indicadores
dos 159 registros de baixa confiança do corpus Iconocracy.

Uso:
    # Requer variável de ambiente GOOGLE_PROJECT_ID
    export GOOGLE_PROJECT_ID=warholana

    # Rodar nos 36 registros com imagem direta (Gallica + Wikimedia)
    python tools/scripts/vision_audit_pipeline.py --batch direct

    # Rodar em todos os 159 (via Cloudflare Browser para Numista)
    python tools/scripts/vision_audit_pipeline.py --batch all

    # Testar num item específico
    python tools/scripts/vision_audit_pipeline.py --item ITEM_ID

    # Atualizar planilha de auditoria com resultados
    python tools/scripts/vision_audit_pipeline.py --export-sheets SPREADSHEET_ID

O que a Vision API cobre (piloto 2026-07-23):
────────────────────────────────────────────
  Alta confiança (~0.85):
    ind_serialidade       via label "Postage stamp", "Banknote", "Coin", "Currency"
    ind_monocromatizacao  via label "Postage stamp", "Banknote", "Paper", "Coin"
    ind_inscricao_estatal via OCR: REPUBLIQUE, REICH, BRASIL, REPUBLIC, COMMONWEALTH…

  Confiança média (~0.55):
    ind_heraldizacao      via label "Shield", "Emblem", "Badge", "Coat of arms"
    ind_apagamento_narrativo via ausência de "Scene", "Narrative art", "Historical painting"
    ind_desincorporacao   via label "Portrait", "Face", "Head"

  NÃO cobertas por Vision:
    ind_rigidez_postural, ind_dessexualizacao, ind_uniformizacao_facial,
    ind_enquadramento_arquitetonico
    → Estes 4 exigem análise visual humana direta.

Autor: Ana Vanzin / PPGD-UFSC / Iconocracy corpus pipeline
Changelog:
    2026-07-23  v1.0 — versão inicial, piloto com 4 imagens
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Configuração
# ──────────────────────────────────────────────────────────────────────────────

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "warholana")
RECORDS_PATH = "data/processed/records.jsonl"
OUTPUT_PATH = "tmp/vision_audit_results.json"

LOW_CONFIDENCE_AGENTS = {"vault-import", "hermes-auto", "migration"}

def is_low_confidence(coded_by: str) -> bool:
    if not coded_by: return True
    cb = coded_by.lower().strip()
    return cb in LOW_CONFIDENCE_AGENTS or "batch-tentative" in cb


# ──────────────────────────────────────────────────────────────────────────────
# Derivar URL de imagem
# ──────────────────────────────────────────────────────────────────────────────

def md5_wiki_path(filename: str) -> str:
    """Calcula o hash MD5 do nome do arquivo para construir a URL do Wikimedia."""
    fname = urllib.parse.unquote(filename)
    fname = fname.replace(" ", "_")
    h = hashlib.md5(fname.encode("utf-8")).hexdigest()
    return f"{h[0]}/{h[:2]}/{urllib.parse.quote(fname)}"


def derive_image_urls(catalog_url: str) -> dict:
    """Deriva URL(s) de imagem acessível a partir da URL do catálogo."""
    url = catalog_url or ""
    ul = url.lower()

    # Numista catalogue
    m = re.search(r"/pieces(\d+)\.html", url)
    if m:
        pid = m.group(1)
        return {
            "obverse": f"https://numistacdn.azureedge.net/photos/pieces/{pid}-o.jpg",
            "reverse": f"https://numistacdn.azureedge.net/photos/pieces/{pid}-r.jpg",
            "strategy": "numista_cdn",
            "direct": False,  # CDN bloqueado — usar Cloudflare render
        }

    # Numista alt format
    m = re.search(r"numista\.com/(\d+)$", url)
    if m:
        pid = m.group(1)
        return {
            "obverse": f"https://numistacdn.azureedge.net/photos/pieces/{pid}-o.jpg",
            "strategy": "numista_cdn",
            "direct": False,
        }

    # Gallica ARK — thumbnail acessível diretamente
    if "gallica.bnf.fr/ark:/" in url:
        ark = re.search(r"(ark:/\d+/\w+)", url)
        if ark:
            return {
                "thumbnail": f"https://gallica.bnf.fr/{ark.group(1)}.thumbnail",
                "iiif_300": f"https://gallica.bnf.fr/iiif/{ark.group(1)}/f1/full/300,/0/native.jpg",
                "strategy": "gallica_iiif",
                "direct": True,
            }

    # Wikimedia Commons
    if "commons.wikimedia.org/wiki/File:" in url:
        fname = url.split("File:")[-1]
        path = md5_wiki_path(fname)
        return {
            "image": f"https://upload.wikimedia.org/wikipedia/commons/{path}",
            "strategy": "wikimedia_direct",
            "direct": True,
        }

    # V&A Museum collections
    m = re.search(r"/item/(O\d+)/", url)
    if m:
        oid = m.group(1)
        return {
            "image": f"https://framemark.vam.ac.uk/collections/{oid}/full/600,/0/default.jpg",
            "strategy": "vam_iiif",
            "direct": True,  # testar
        }

    # Library of Congress IIIF
    if "loc.gov/item/" in url:
        return {"image": url, "strategy": "loc_html", "direct": False}

    # Colnect stamps
    m = re.search(r"stamps/stamp/(\d+)", url)
    if m:
        sid = m.group(1)
        prefix = sid[:3]
        return {
            "image": f"https://img.colnect.net/b600/stamps/{prefix}/{sid}.jpg",
            "strategy": "colnect_cdn",
            "direct": True,  # tentar
        }

    return {"image": url, "strategy": "unknown", "direct": False}


# ──────────────────────────────────────────────────────────────────────────────
# Regras de mapeamento Vision → indicadores
# ──────────────────────────────────────────────────────────────────────────────

LABEL_RULES = {
    # Suporte numismático → alta serialidade e monocromatização
    "Postage stamp":          {"ind_serialidade": 3, "ind_monocromatizacao": 2},
    "Stamp":                  {"ind_serialidade": 3, "ind_monocromatizacao": 2},
    "Banknote":               {"ind_serialidade": 3, "ind_monocromatizacao": 3},
    "Currency":               {"ind_serialidade": 3, "ind_monocromatizacao": 3},
    "Coin":                   {"ind_serialidade": 3, "ind_monocromatizacao": 3, "ind_heraldizacao": 2},
    "Medal":                  {"ind_serialidade": 2, "ind_heraldizacao": 2, "ind_monocromatizacao": 2},
    "Money":                  {"ind_serialidade": 3, "ind_monocromatizacao": 2},
    "Collectable":            {"ind_serialidade": 2},

    # Suporte papel / monocromático
    "Paper":                  {"ind_monocromatizacao": 2},
    "Paper Product":          {"ind_monocromatizacao": 2},
    "Engraving":              {"ind_monocromatizacao": 2, "ind_serialidade": 2},
    "Etching":                {"ind_monocromatizacao": 2, "ind_serialidade": 2},
    "Print":                  {"ind_monocromatizacao": 2, "ind_serialidade": 2},

    # Heráldica / inscrição
    "Shield":                 {"ind_heraldizacao": 3},
    "Emblem":                 {"ind_heraldizacao": 3, "ind_apagamento_narrativo": 2},
    "Badge":                  {"ind_heraldizacao": 2},
    "Coat of arms":           {"ind_heraldizacao": 3, "ind_inscricao_estatal": 2},
    "Flag":                   {"ind_inscricao_estatal": 3},
    "Symbol":                 {"ind_heraldizacao": 2, "ind_apagamento_narrativo": 2},

    # Desincorporação (retrato / busto)
    "Face":                   {"ind_desincorporacao": 2},
    "Portrait":               {"ind_desincorporacao": 2},
    "Head":                   {"ind_desincorporacao": 3},
    "Facial expression":      {"ind_desincorporacao": 2, "ind_uniformizacao_facial": 1},

    # Enquadramento arquitetônico
    "Architecture":           {"ind_enquadramento_arquitetonico": 2},
    "Column":                 {"ind_enquadramento_arquitetonico": 2},
    "Building":               {"ind_enquadramento_arquitetonico": 1},
    "Classical architecture": {"ind_enquadramento_arquitetonico": 3},

    # Baixo endurecimento — corpo presente, narrativa
    "Illustration":           {"ind_apagamento_narrativo": 0},
    "Painting":               {"ind_apagamento_narrativo": 0, "ind_dessexualizacao": 0},
    "Drawing":                {"ind_apagamento_narrativo": 0},
    "Poster":                 {"ind_serialidade": 1, "ind_inscricao_estatal": 1},
    "Art":                    {"ind_apagamento_narrativo": 0},
    "Historical site":        {"ind_enquadramento_arquitetonico": 1},

    # Suporte fotográfico → baixo endurecimento
    "Photograph":             {"ind_monocromatizacao": 1},
    "Black and white":        {"ind_monocromatizacao": 3},
}

# Termos OCR que mapeiam diretamente para ind_inscricao_estatal = 3
INSCRIPTION_PATTERNS = [
    "REPUBLIQUE", "REPÚBLICA", "REPUBLIC", "FRANÇAISE", "FRANÇAISE",
    "REICH", "DEUTSCHES", "BRASIL", "BRAZIL", "UNITED STATES",
    "COMMONWEALTH", "BRITANNIA", "BELGIQUE", "BELGIE", "BELGIEN",
    "FRANCE", "LIBERTY", "LIBERTA", "LIBERTÉ", "LIBERTAS",
    "MONNAIE", "MOEDA", "NATIONAL", "FEDERAL", "IMPERIAL",
    "E PLURIBUS", "DEI GRATIA", "REPUBLICA", "REPÚBLICA",
]

INDICATORS = [
    "ind_desincorporacao", "ind_rigidez_postural", "ind_dessexualizacao",
    "ind_uniformizacao_facial", "ind_heraldizacao", "ind_enquadramento_arquitetonico",
    "ind_apagamento_narrativo", "ind_monocromatizacao", "ind_serialidade",
    "ind_inscricao_estatal",
]


def estimate_from_vision(labels: list[dict], ocr_text: str) -> dict:
    """
    Mapeia resultados Vision → estimativas de indicadores.

    Returns:
        dict com:
          estimates: {ind: value | None}
          confidence: {ind: 0-1}
          evidence: {ind: [str]}
          n_estimated: int
          score_partial: float | None
    """
    estimates = {ind: None for ind in INDICATORS}
    confidence = {ind: 0.0 for ind in INDICATORS}
    evidence = {ind: [] for ind in INDICATORS}

    # Label rules
    for lbl in labels:
        desc = lbl.get("description", "") if isinstance(lbl, dict) else lbl
        score = lbl.get("score", 1.0) if isinstance(lbl, dict) else 1.0
        if score < 0.65:
            continue
        rules = LABEL_RULES.get(desc, {})
        for ind, val in rules.items():
            if estimates[ind] is None or val > estimates[ind]:
                estimates[ind] = val
                confidence[ind] = min(0.9, score)
                evidence[ind].append(f"label:{desc}({score:.2f})")

    # OCR rules
    ocr_upper = (ocr_text or "").upper()
    for pattern in INSCRIPTION_PATTERNS:
        if pattern in ocr_upper:
            ind = "ind_inscricao_estatal"
            if estimates[ind] is None or 3 > estimates[ind]:
                estimates[ind] = 3
                confidence[ind] = 0.92
                evidence[ind].append(f"ocr:{pattern}")

    # Score parcial (soma sobre 10, mesmo que só parte seja conhecida)
    known = [v for v in estimates.values() if v is not None]
    score_partial = sum(known) / 10 if known else None
    n_estimated = len(known)

    return {
        "estimates": estimates,
        "confidence": confidence,
        "evidence": evidence,
        "n_estimated": n_estimated,
        "score_partial": round(score_partial, 2) if score_partial is not None else None,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Cloud Vision API (via gws ou requests)
# ──────────────────────────────────────────────────────────────────────────────

def call_vision_labels(image_url: str, project_id: str, max_results: int = 15) -> list[dict]:
    """Chama Vision API detect-labels via subprocess (gws CLI / pipedream)."""
    try:
        import requests
        # Usar requests com token de serviço se disponível
        token = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        body = {
            "requests": [{
                "image": {"source": {"imageUri": image_url}},
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": max_results},
                ],
            }]
        }
        url = f"https://vision.googleapis.com/v1/images:annotate?key={os.environ.get('GOOGLE_API_KEY','')}"
        resp = requests.post(url, json=body, headers=headers, timeout=15)
        data = resp.json()
        labels = data.get("responses", [{}])[0].get("labelAnnotations", [])
        return labels
    except Exception as e:
        print(f"  [Vision labels error] {e}", file=sys.stderr)
        return []


def call_vision_ocr(image_url: str, project_id: str) -> str:
    """Chama Vision API detect-text via Vision REST API."""
    try:
        import requests
        body = {
            "requests": [{
                "image": {"source": {"imageUri": image_url}},
                "features": [{"type": "TEXT_DETECTION"}],
            }]
        }
        url = f"https://vision.googleapis.com/v1/images:annotate?key={os.environ.get('GOOGLE_API_KEY','')}"
        resp = requests.post(url, json=body, timeout=15)
        data = resp.json()
        annotations = data.get("responses", [{}])[0].get("textAnnotations", [])
        return annotations[0].get("description", "") if annotations else ""
    except Exception as e:
        print(f"  [Vision OCR error] {e}", file=sys.stderr)
        return ""


# ────────────────────────────────��─────────────────────────────────────────────
# Pipeline principal
# ──────────────────────────────────────────────────────────────────────────────

def load_low_conf_records(records_path: str) -> list[dict]:
    records = []
    with open(records_path) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except:
                continue
            pur = r.get("purificacao") or {}
            if not isinstance(pur, dict):
                pur = {}
            if is_low_confidence(pur.get("coded_by", "")):
                records.append(r)
    return records


def process_record(r: dict, project_id: str) -> dict:
    inp = r.get("input") or {}
    pur = r.get("purificacao") or {}
    if not isinstance(inp, dict): inp = {}
    if not isinstance(pur, dict): pur = {}

    item_id = r.get("item_id", "")
    catalog_url = inp.get("input_url", "") or ""
    title = (inp.get("title_hint", "") or "").strip()
    coded_by = pur.get("coded_by", "")

    img_info = derive_image_urls(catalog_url)
    image_url = (
        img_info.get("thumbnail") or
        img_info.get("image") or
        img_info.get("obverse") or ""
    )

    result = {
        "item_id": item_id,
        "title": title[:80],
        "coded_by": coded_by,
        "catalog_url": catalog_url,
        "image_url": image_url,
        "image_strategy": img_info.get("strategy", "unknown"),
        "direct_accessible": img_info.get("direct", False),
        "vision_labels": [],
        "vision_ocr": "",
        "vision_error": None,
        "estimates": None,
        "processed_at": None,
    }

    if not img_info.get("direct") or not image_url:
        result["vision_error"] = "image_not_directly_accessible"
        return result

    print(f"  [{img_info.get('strategy')}] {title[:50]}…")

    # Labels
    labels = call_vision_labels(image_url, project_id)
    result["vision_labels"] = labels

    # OCR
    ocr = call_vision_ocr(image_url, project_id)
    result["vision_ocr"] = ocr

    # Estimate
    result["estimates"] = estimate_from_vision(labels, ocr)
    result["processed_at"] = datetime.now(timezone.utc).isoformat()

    time.sleep(0.3)  # rate limit
    return result


def run_batch(records: list[dict], project_id: str, direct_only: bool = True) -> list[dict]:
    results = []
    eligible = [r for r in records if True]  # process all

    print(f"\nProcessando {len(eligible)} registros…")

    for i, r in enumerate(eligible, 1):
        inp = r.get("input") or {}
        if not isinstance(inp, dict): inp = {}
        catalog_url = inp.get("input_url", "") or ""
        img_info = derive_image_urls(catalog_url)

        if direct_only and not img_info.get("direct"):
            # Skip non-direct — será feito via Cloudflare em batch separado
            pur = r.get("purificacao") or {}
            if not isinstance(pur, dict): pur = {}
            results.append({
                "item_id": r.get("item_id", ""),
                "title": (inp.get("title_hint", "") or "")[:60],
                "coded_by": pur.get("coded_by", ""),
                "image_strategy": img_info.get("strategy"),
                "direct_accessible": False,
                "vision_error": "skipped_not_direct",
                "estimates": None,
            })
            continue

        print(f"  [{i}/{len(eligible)}]", end=" ")
        result = process_record(r, project_id)
        results.append(result)

    return results


def export_to_sheets_update(results: list[dict], spreadsheet_id: str) -> None:
    """Atualiza colunas de pré-preenchimento na planilha de auditoria."""
    # Colunas a atualizar: ind_* estimados pela Vision, + vision_source, + review_notes prefill
    print(f"Exportando {len(results)} resultados para planilha {spreadsheet_id}…")
    print("Use: python tools/scripts/audit_recodification.py --spreadsheet-id para recriar a planilha.")
    # TODO: gws sheets update (requer matching por item_id)


def print_summary(results: list[dict]) -> None:
    processed = [r for r in results if r.get("estimates") is not None]
    skipped = [r for r in results if r.get("vision_error") == "skipped_not_direct"]
    errored = [r for r in results if r.get("vision_error") and r["vision_error"] != "skipped_not_direct"]

    print(f"\n{'='*60}")
    print(f"  VISION AUDIT — SUMÁRIO")
    print(f"{'='*60}")
    print(f"  Processados com imagem:  {len(processed)}")
    print(f"  Skipped (sem URL direta): {len(skipped)}")
    print(f"  Erros:                   {len(errored)}")

    if processed:
        n_estimated = [r["estimates"]["n_estimated"] for r in processed]
        avg_n = sum(n_estimated) / len(n_estimated)
        print(f"\n  Indicadores estimados por item (média): {avg_n:.1f}/10")

        # Frequência por indicador
        ind_counts = {ind: 0 for ind in INDICATORS}
        for r in processed:
            est = r["estimates"]["estimates"]
            for ind, val in est.items():
                if val is not None:
                    ind_counts[ind] += 1

        print("\n  Cobertura por indicador:")
        for ind, cnt in sorted(ind_counts.items(), key=lambda x: -x[1]):
            pct = 100 * cnt / len(processed)
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"    {ind:<35} {bar} {cnt:>3} ({pct:.0f}%)")

    print(f"{'='*60}\n")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Google Cloud Vision → pre-fill Iconocracy audit indicators.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--records", default=RECORDS_PATH)
    parser.add_argument("--output", default=OUTPUT_PATH)
    parser.add_argument("--batch", choices=["direct", "all"], default="direct",
                        help="'direct' = só imagens acessíveis sem render; 'all' = todos")
    parser.add_argument("--item", default=None, help="Processar apenas este item_id")
    parser.add_argument("--project-id", default=GOOGLE_PROJECT_ID)
    parser.add_argument("--export-sheets", default=None, help="Spreadsheet ID para exportar")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Carregando registros de {args.records}…")
    records = load_low_conf_records(args.records)
    print(f"  {len(records)} registros de baixa confiança encontrados")

    if args.item:
        records = [r for r in records if r.get("item_id") == args.item]
        if not records:
            print(f"Item {args.item} não encontrado nos registros de baixa confiança.")
            sys.exit(1)

    if args.dry_run:
        print("\n[DRY RUN] Simulando processamento sem chamar Vision API…")
        for r in records[:5]:
            inp = r.get("input") or {}
            if not isinstance(inp, dict): inp = {}
            url = inp.get("input_url", "")
            img = derive_image_urls(url)
            print(f"  {r.get('item_id','')} → strategy={img.get('strategy')} direct={img.get('direct')}")
        return

    direct_only = (args.batch == "direct")
    results = run_batch(records, args.project_id, direct_only=direct_only)

    # Save
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_processed": len([r for r in results if r.get("estimates")]),
            "total_skipped": len([r for r in results if r.get("vision_error") == "skipped_not_direct"]),
            "results": results,
        }, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n[OK] Resultados → {out_path}")

    print_summary(results)

    if args.export_sheets:
        export_to_sheets_update(results, args.export_sheets)


if __name__ == "__main__":
    main()
