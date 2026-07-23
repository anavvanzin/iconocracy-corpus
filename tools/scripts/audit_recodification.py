#!/usr/bin/env python3
"""
audit_recodification.py
=======================
ICONOCRACY corpus audit tool — export low-confidence records to Google Sheets.

Usage
-----
    # From repo root, with gws CLI configured:
    python tools/scripts/audit_recodification.py

    # Specify custom paths:
    python tools/scripts/audit_recodification.py \
        --records data/processed/records.jsonl \
        --output-json tmp/audit_low_conf.json \
        --sheet-title "Iconocracy — Audit de Recodificação"

    # Dry-run: only parse and export JSON, skip Sheets upload:
    python tools/scripts/audit_recodification.py --dry-run

    # Re-upload to an existing sheet (update in place):
    python tools/scripts/audit_recodification.py \
        --spreadsheet-id 1AbCdEfGhIjKlMnOpQrSt...

What it does
------------
1. Reads data/processed/records.jsonl (canonical ledger).
2. Filters records where purificacao.coded_by is one of:
       vault-import | hermes-auto | migration | batch-tentative-*
3. Extracts all meaningful fields (input, purification indicators,
   regime, confidence, audit_flags, URLs, timestamps).
4. Adds a blank "review_status" column with a controlled vocabulary
   dropdown and three helper columns for the reviewer.
5. Writes the result to:
       - JSON: tmp/audit_low_conf.json  (local backup)
       - Google Sheet: "Iconocracy — Audit de Recodificação"
           Sheet1 "Registros"   — the full data table
           Sheet2 "LEGEND"      — vocabulary reference
           Sheet3 "Progresso"   — live summary formula
6. Applies formatting: frozen header, colored header row, column widths,
   data-validation dropdown for review_status.

Low-confidence agents
---------------------
These agents produced purification scores without performing a full
3-level Panofsky visual analysis. Their records need manual review
before being used in quantitative analysis chapters.

    vault-import              bulk ingest from Obsidian vault
    hermes-auto               automated pipeline (no visual input)
    migration                 schema migration carry-over (score=0.0)
    batch-tentative-*         provisional batch (flagged for review)

Review status vocabulary (review_status column)
-----------------------------------------------
    PENDENTE          not yet reviewed               (default)
    EM_REVISAO        reviewer has opened the record
    RECODIFICADO      full IconoCode analysis done; score updated
    CONFIRMADO        original score validated as acceptable
    EXCLUIR           record should be removed from core corpus
    COMPARADOR        move to comparador/apêndice section

Author: Ana Vanzin / PPGD-UFSC / Iconocracy corpus pipeline
Changelog:
    2026-07-17  initial version
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

LOW_CONFIDENCE_AGENTS = {
    "vault-import",
    "hermes-auto",
    "migration",
}

REVIEW_STATUS_OPTIONS = [
    "PENDENTE",
    "EM_REVISAO",
    "RECODIFICADO",
    "CONFIRMADO",
    "EXCLUIR",
    "COMPARADOR",
]

PURIFICATION_INDICATORS = [
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

DEFAULT_RECORDS_PATH = "data/processed/records.jsonl"
DEFAULT_OUTPUT_JSON = "tmp/audit_low_conf.json"
DEFAULT_SHEET_TITLE = "Iconocracy — Audit de Recodificação"

# Column definitions: (header_label, field_key, width_px)
COLUMNS = [
    # ── Identity ──────────────────────────────────────────
    ("item_id",                  "item_id",                    220),
    ("batch_id",                 "batch_id",                   220),
    # ── Source metadata ───────────────────────────────────
    ("title",                    "title",                      300),
    ("date_hint",                "date_hint",                  120),
    ("year",                     "year",                        70),
    ("place_hint",               "place_hint",                 150),
    ("url",                      "url",                        280),
    # ── Coding provenance ─────────────────────────────────
    ("coded_by",                 "coded_by",                   160),
    ("coded_at",                 "coded_at",                   175),
    ("confidence_iconocode",     "confidence_iconocode",       130),
    # ── Iconocratic classification ────────────────────────
    ("regime_iconocratico",      "regime_iconocratico",        155),
    ("familia_alegorica",        "familia_alegorica",          155),
    ("score_purificacao_composto","score_purificacao_composto", 130),
    # ── Motifs / interpretation ───────────────────────────
    ("motifs",                   "motifs",                     260),
    ("main_claim",               "main_claim",                 300),
    ("notes",                    "notes",                      300),
    ("referencia_genealogica",   "referencia_genealogica",     200),
    ("audit_flags",              "audit_flags",                200),
    # ── Purification indicators (10) ──────────────────────
    *[(f"ind_{k}", f"ind_{k}", 90) for k in PURIFICATION_INDICATORS],
    # ── Timestamps ────────────────────────────────────────
    ("created_at",               "created_at",                 175),
    ("updated_at",               "updated_at",                 175),
    # ── Audit / review columns (added by this script) ─────
    ("review_status",            "review_status",              160),
    ("revisor",                  "revisor",                    130),
    ("review_date",              "review_date",                120),
    ("review_notes",             "review_notes",               350),
]

HEADER = [col[0] for col in COLUMNS]
FIELD_KEYS = [col[1] for col in COLUMNS]
COL_WIDTHS = [col[2] for col in COLUMNS]


# ──────────────────────────────────────────────────────────────────────────────
# Parsing helpers
# ──────────────────────────────────────────────────────────────────────────────

def is_low_confidence(coded_by: str) -> bool:
    if not coded_by:
        return True
    cb = str(coded_by).lower().strip()
    if cb in LOW_CONFIDENCE_AGENTS:
        return True
    if "batch-tentative" in cb:
        return True
    return False


def safe_str(v, maxlen: int = 200) -> str:
    if v is None:
        return ""
    s = str(v)
    return s[:maxlen] if len(s) > maxlen else s


def extract_year(date_raw) -> str:
    if not date_raw:
        return ""
    m = re.search(r'\b(1[4-9]\d\d|20[012]\d)\b', str(date_raw))
    return m.group(1) if m else str(date_raw)[:10]


def extract_record(r: dict) -> dict:
    pur  = r.get("purificacao") or {}
    inp  = r.get("input")       or {}
    ic   = r.get("iconocode")   or {}
    exp  = r.get("exports")     or {}
    ts   = r.get("timestamps")  or {}

    if not isinstance(pur, dict): pur = {}
    if not isinstance(inp, dict): inp = {}
    if not isinstance(ic,  dict): ic  = {}
    if not isinstance(exp, dict): exp = {}
    if not isinstance(ts,  dict): ts  = {}

    coded_by = pur.get("coded_by", "")
    title    = (inp.get("title_hint") or inp.get("title") or "").strip()
    date_raw = inp.get("date_hint") or inp.get("date") or ""

    # Confidence — may be float or dict
    confidence = ic.get("confidence", "")
    if isinstance(confidence, dict):
        confidence = confidence.get("overall", "")

    # Motifs from pre_iconographic (list of dicts or single dict)
    pre = ic.get("pre_iconographic", [])
    if isinstance(pre, list):
        motifs = "; ".join(
            p.get("motif", "") for p in pre
            if isinstance(p, dict) and p.get("motif")
        )
    elif isinstance(pre, dict):
        motifs = pre.get("motif") or pre.get("title") or ""
    else:
        motifs = ""

    # Main claim from interpretation list
    interp = ic.get("interpretation", [])
    main_claim = ""
    if isinstance(interp, list) and interp:
        first = interp[0]
        if isinstance(first, dict):
            main_claim = first.get("claim_text", "")

    # Audit flags
    audit_flags = exp.get("audit_flags", [])
    if isinstance(audit_flags, list):
        audit_flags = "; ".join(str(f) for f in audit_flags)

    # Genealogical reference
    ref_gene = pur.get("referencia_genealogica", "")
    if isinstance(ref_gene, list):
        ref_gene = "; ".join(str(x) for x in ref_gene)

    row: dict = {
        "item_id":                   r.get("item_id", ""),
        "batch_id":                  r.get("batch_id", ""),
        "title":                     safe_str(title),
        "date_hint":                 safe_str(date_raw),
        "year":                      extract_year(date_raw),
        "place_hint":                safe_str(inp.get("place_hint", "")),
        "url":                       safe_str(inp.get("input_url", ""), maxlen=500),
        "coded_by":                  safe_str(coded_by),
        "coded_at":                  safe_str(pur.get("coded_at", "")),
        "confidence_iconocode":      safe_str(confidence),
        "regime_iconocratico":       safe_str(pur.get("regime_iconocratico", "")),
        "familia_alegorica":         safe_str(pur.get("familia_alegorica", "")),
        "score_purificacao_composto": pur.get("purificacao_composto", ""),
        "motifs":                    safe_str(motifs, 250),
        "main_claim":                safe_str(main_claim, 250),
        "notes":                     safe_str(pur.get("notes", ""), 250),
        "referencia_genealogica":    safe_str(ref_gene),
        "audit_flags":               safe_str(audit_flags),
        "created_at":                safe_str(ts.get("created_at", "")),
        "updated_at":                safe_str(ts.get("updated_at", "")),
        # Review columns — blank by default
        "review_status":             "PENDENTE",
        "revisor":                   "",
        "review_date":               "",
        "review_notes":              "",
    }

    # Purification indicators
    for k in PURIFICATION_INDICATORS:
        v = pur.get(k)
        row[f"ind_{k}"] = v if v is not None else ""

    return row


def parse_records(records_path: str) -> tuple[list[dict], list[dict]]:
    """Return (low_confidence_rows, high_confidence_rows)."""
    path = Path(records_path)
    if not path.exists():
        print(f"[ERROR] records.jsonl not found: {path}", file=sys.stderr)
        sys.exit(1)

    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[WARN] Skipping malformed line: {e}", file=sys.stderr)

    low_conf, high_conf = [], []
    for r in records:
        pur = r.get("purificacao") or {}
        if not isinstance(pur, dict):
            pur = {}
        coded_by = pur.get("coded_by", "")
        (low_conf if is_low_confidence(coded_by) else high_conf).append(
            extract_record(r)
        )

    return low_conf, high_conf


# ──────────────────────────────────────────────────────────────────────────────
# Summary / stats
# ──────────────────────────────────────────────────────────────────────────────

def print_summary(low_conf: list[dict], high_conf: list[dict]) -> None:
    total = len(low_conf) + len(high_conf)
    print(f"\n{'='*60}")
    print(f"  ICONOCRACY — Audit de Recodificação")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}")
    print(f"  Total records:          {total}")
    print(f"  Low-confidence (audit): {len(low_conf)}  ({100*len(low_conf)/total:.0f}%)")
    print(f"  High-confidence:        {len(high_conf)}  ({100*len(high_conf)/total:.0f}%)")
    print()
    print("  Low-confidence breakdown by coded_by:")
    cb_c = Counter(r["coded_by"] for r in low_conf)
    for agent, count in cb_c.most_common():
        pct = 100 * count / len(low_conf)
        print(f"    {agent or '(empty)':<40} {count:>3}  ({pct:.0f}%)")
    print()
    print("  Regime distribution (low-conf):")
    reg_c = Counter(r["regime_iconocratico"] for r in low_conf)
    for reg, count in reg_c.most_common():
        print(f"    {reg or '(none)':<30} {count:>3}")
    print()
    # Score stats for non-zero scores
    scores = [
        float(r["score_purificacao_composto"])
        for r in low_conf
        if r["score_purificacao_composto"] not in ("", None)
    ]
    if scores:
        import statistics
        print(f"  Score purificacao_composto (low-conf):")
        print(f"    n={len(scores)}  min={min(scores):.2f}  max={max(scores):.2f}"
              f"  mean={statistics.mean(scores):.2f}  median={statistics.median(scores):.2f}")
    print(f"{'='*60}\n")


# ──────────────────────────────────────────────────────────────────────────────
# Google Sheets upload via gws CLI
# ──────────────────────────────────────────────────────────────────────────────

def gws(params: dict, *args: str) -> dict:
    """Call the gws CLI with JSON params. Returns parsed JSON response."""
    cmd = ["gws"] + list(args) + ["--params", json.dumps(params)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"gws error ({' '.join(args)}):\n"
            f"  stdout: {result.stdout[:500]}\n"
            f"  stderr: {result.stderr[:500]}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout}


def col_letter(n: int) -> str:
    """Convert 0-based column index to letter(s): 0→A, 25→Z, 26→AA…"""
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def create_spreadsheet(title: str) -> str:
    """Create a new Google Sheets spreadsheet and return its ID."""
    resp = gws(
        {
            "resource": {
                "properties": {"title": title},
                "sheets": [
                    {"properties": {"title": "Registros", "index": 0}},
                    {"properties": {"title": "LEGEND",    "index": 1}},
                    {"properties": {"title": "Progresso", "index": 2}},
                ],
            }
        },
        "sheets", "spreadsheets", "create",
    )
    spreadsheet_id = resp["spreadsheetId"]
    print(f"[OK] Spreadsheet created: {spreadsheet_id}")
    print(f"     https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
    return spreadsheet_id


def get_sheet_id(spreadsheet_id: str, sheet_name: str) -> Optional[int]:
    resp = gws({"spreadsheetId": spreadsheet_id}, "sheets", "spreadsheets", "get")
    for s in resp.get("sheets", []):
        if s["properties"]["title"] == sheet_name:
            return s["properties"]["sheetId"]
    return None


def batch_update(spreadsheet_id: str, requests: list) -> None:
    gws(
        {"spreadsheetId": spreadsheet_id, "requests": requests},
        "sheets", "spreadsheets", "batchUpdate",
    )


def values_update(
    spreadsheet_id: str, range_: str, values: list[list]
) -> None:
    gws(
        {
            "spreadsheetId": spreadsheet_id,
            "range": range_,
            "valueInputOption": "USER_ENTERED",
            "resource": {"values": values},
        },
        "sheets", "spreadsheets", "values", "update",
    )


def write_registros(
    spreadsheet_id: str,
    sheet_id: int,
    rows: list[dict],
) -> None:
    """Write the main data table to Sheet1 (Registros)."""
    n_cols = len(HEADER)
    last_col = col_letter(n_cols - 1)
    total_rows = len(rows) + 1  # header + data

    # ── 1. Write values ────────────────────────────────────────────────────
    values: list[list] = [HEADER]
    for row in rows:
        values.append([safe_str(row.get(k, "")) for k in FIELD_KEYS])

    values_update(
        spreadsheet_id,
        f"Registros!A1:{last_col}{total_rows}",
        values,
    )
    print(f"[OK] Wrote {len(rows)} data rows + header → Registros")

    # ── 2. Batch formatting ────────────────────────────────────────────────
    reqs = []

    # Freeze header row
    reqs.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {"frozenRowCount": 1},
            },
            "fields": "gridProperties.frozenRowCount",
        }
    })

    # Header row: dark background, white bold text
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 1,
                "startColumnIndex": 0, "endColumnIndex": n_cols,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.067, "green": 0.067, "blue": 0.067},
                    "textFormat": {
                        "foregroundColor": {"red": 0.98, "green": 0.95, "blue": 0.88},
                        "bold": True,
                        "fontSize": 10,
                        "fontFamily": "DM Sans",
                    },
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "CLIP",
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)",
        }
    })

    # review_status column: sienna background on header cell
    review_col_idx = HEADER.index("review_status")
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 1,
                "startColumnIndex": review_col_idx, "endColumnIndex": review_col_idx + 1,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.545, "green": 0.227, "blue": 0.102},
                }
            },
            "fields": "userEnteredFormat.backgroundColor",
        }
    })

    # Alternating row colors for data rows
    reqs.append({
        "addBanding": {
            "bandedRange": {
                "bandedRangeId": 1,
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1, "endRowIndex": total_rows,
                    "startColumnIndex": 0, "endColumnIndex": n_cols,
                },
                "rowProperties": {
                    "headerColor":     {"red": 0.96, "green": 0.92, "blue": 0.85},
                    "firstBandColor":  {"red": 1.0,  "green": 0.98, "blue": 0.94},
                    "secondBandColor": {"red": 0.97, "green": 0.94, "blue": 0.88},
                },
            }
        }
    })

    # Color-code review_status data cells by value
    status_colors = {
        "PENDENTE":     {"red": 0.95, "green": 0.92, "blue": 0.87},
        "EM_REVISAO":   {"red": 0.98, "green": 0.96, "blue": 0.68},
        "RECODIFICADO": {"red": 0.72, "green": 0.92, "blue": 0.73},
        "CONFIRMADO":   {"red": 0.66, "green": 0.87, "blue": 0.98},
        "EXCLUIR":      {"red": 0.98, "green": 0.70, "blue": 0.70},
        "COMPARADOR":   {"red": 0.88, "green": 0.76, "blue": 0.98},
    }
    # We can't apply cell-level color per value without conditional formatting rules
    # Add conditional formatting rules for review_status column
    for status, color in status_colors.items():
        reqs.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": 1, "endRowIndex": total_rows,
                        "startColumnIndex": review_col_idx,
                        "endColumnIndex": review_col_idx + 1,
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [{"userEnteredValue": status}],
                        },
                        "format": {"backgroundColor": color},
                    },
                },
                "index": 0,
            }
        })

    # Data validation dropdown for review_status column
    reqs.append({
        "setDataValidation": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 1, "endRowIndex": total_rows,
                "startColumnIndex": review_col_idx,
                "endColumnIndex": review_col_idx + 1,
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": s} for s in REVIEW_STATUS_OPTIONS],
                },
                "showCustomUi": True,
                "strict": True,
            },
        }
    })

    # Column widths
    for idx, width in enumerate(COL_WIDTHS):
        reqs.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": idx,
                    "endIndex": idx + 1,
                },
                "properties": {"pixelSize": width},
                "fields": "pixelSize",
            }
        })

    # Row height for data rows (compact)
    reqs.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": 1,
                "endIndex": total_rows,
            },
            "properties": {"pixelSize": 20},
            "fields": "pixelSize",
        }
    })

    # Bold + slightly larger text for review columns
    for extra_col in ["review_status", "revisor", "review_date", "review_notes"]:
        ci = HEADER.index(extra_col)
        reqs.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1, "endRowIndex": total_rows,
                    "startColumnIndex": ci, "endColumnIndex": ci + 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontSize": 10, "fontFamily": "DM Sans"},
                    }
                },
                "fields": "userEnteredFormat.textFormat",
            }
        })

    batch_update(spreadsheet_id, reqs)
    print("[OK] Formatting applied to Registros")


def write_legend(spreadsheet_id: str, sheet_id: int) -> None:
    """Write vocabulary reference to Sheet2 (LEGEND)."""
    values = [
        ["COLUNA", "VALOR", "DESCRIÇÃO"],
        ["", "", ""],
        ["review_status", "PENDENTE",     "Registro ainda não revisado (estado inicial)"],
        ["review_status", "EM_REVISAO",   "Revisora abriu o registro — análise em andamento"],
        ["review_status", "RECODIFICADO", "Análise visual IconoCode completa realizada; score atualizado no records.jsonl"],
        ["review_status", "CONFIRMADO",   "Score original validado como metodologicamente aceitável"],
        ["review_status", "EXCLUIR",      "Registro deve ser removido do corpus core (duplicata, erro, fora de escopo)"],
        ["review_status", "COMPARADOR",   "Mover para seção comparador/apêndice (não entra na análise principal)"],
        ["", "", ""],
        ["coded_by", "vault-import",           "Importação em massa do vault Obsidian — sem análise visual"],
        ["coded_by", "hermes-auto",            "Pipeline automático Hermes — sem input visual direto"],
        ["coded_by", "migration",              "Migração de schema — score herdado, geralmente 0.0"],
        ["coded_by", "batch-tentative-*",      "Batch provisório — marcado para revisão desde a origem"],
        ["", "", ""],
        ["coded_by (alta confiança)", "iconocode-opus",            "Análise visual completa (3 níveis Panofsky)"],
        ["coded_by (alta confiança)", "iconocode-opus-4.6-image",  "IconoCode com análise de imagem"],
        ["coded_by (alta confiança)", "ana",                       "Codificação manual pela pesquisadora"],
        ["coded_by (alta confiança)", "opus-4.8",                  "IconoCode modelo 4.8"],
        ["", "", ""],
        ["Indicadores (0–3)", "0", "Ausente"],
        ["Indicadores (0–3)", "1", "Traços iniciais"],
        ["Indicadores (0–3)", "2", "Presente"],
        ["Indicadores (0–3)", "3", "Plenamente realizado"],
        ["", "", ""],
        ["Regimes", "fundacional",     "Constituição / fundação do Estado — alegoria como ato inaugural"],
        ["Regimes", "normativo",       "Uso ordinário no aparato legal-institucional"],
        ["Regimes", "militar",         "Contexto de guerra, ditadura, estado de exceção"],
        ["Regimes", "contra-alegoria", "Subversão, vandalismo, paródia — iconoclasmo"],
        ["", "", ""],
        ["Pipeline de recodificação", "", ""],
        ["1.", "Abrir URL do registro",    "Ver coluna 'url'"],
        ["2.", "Analisar visualmente",     "3 níveis Panofsky: pré-iconográfico → iconográfico → iconológico"],
        ["3.", "Preencher indicadores",    "cols ind_desincorporacao … ind_inscricao_estatal (0–3)"],
        ["4.", "Atualizar records.jsonl",  "python tools/scripts/code_purification.py --item ITEM_ID"],
        ["5.", "Marcar review_status",     "RECODIFICADO ou CONFIRMADO"],
        ["6.", "Commitar",                 "git commit -m 'recodif(ITEM_ID): visual analysis'"],
    ]

    values_update(spreadsheet_id, "LEGEND!A1:C100", values)

    sheet_id_legend = get_sheet_id(spreadsheet_id, "LEGEND")
    reqs = []
    # Header row formatting
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id_legend,
                "startRowIndex": 0, "endRowIndex": 1,
                "startColumnIndex": 0, "endColumnIndex": 3,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.067, "green": 0.067, "blue": 0.067},
                    "textFormat": {
                        "foregroundColor": {"red": 0.98, "green": 0.95, "blue": 0.88},
                        "bold": True, "fontSize": 10,
                    },
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat)",
        }
    })
    # Column widths
    for ci, w in enumerate([180, 260, 420]):
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id_legend, "dimension": "COLUMNS",
                          "startIndex": ci, "endIndex": ci+1},
                "properties": {"pixelSize": w},
                "fields": "pixelSize",
            }
        })
    batch_update(spreadsheet_id, reqs)
    print("[OK] LEGEND sheet written")


def write_progresso(
    spreadsheet_id: str,
    sheet_id: int,
    n_total: int,
    n_low: int,
) -> None:
    """Write live progress summary with COUNTIF formulas to Sheet3."""
    # Reference to Registros sheet
    ref = "Registros"
    status_col = col_letter(HEADER.index("review_status"))
    last_data_row = n_low + 1  # +1 for header

    values = [
        ["PROGRESSO DE RECODIFICAÇÃO", "", ""],
        ["Atualizado automaticamente via fórmulas. Não editar esta aba.", "", ""],
        ["", "", ""],
        ["Métrica", "Valor", "% do total auditável"],
        ["Total corpus",                  n_total,    ""],
        ["Total auditável (baixa conf.)", n_low,      ""],
        ["Alta confiança (excluídos da auditoria)", n_total - n_low, ""],
        ["", "", ""],
        ["Status", "Contagem", "% do auditável"],
    ]

    row_offset = len(values) + 1  # 1-based row for Sheets

    for status in REVIEW_STATUS_OPTIONS:
        values.append([
            status,
            f"=COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"{status}\")",
            f"=B{row_offset}/{n_low}",
        ])
        row_offset += 1

    values.append(["", "", ""])
    values.append([
        "Revisados (RECODIFICADO + CONFIRMADO + EXCLUIR + COMPARADOR)",
        f"=COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"RECODIFICADO\")"
        f"+COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"CONFIRMADO\")"
        f"+COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"EXCLUIR\")"
        f"+COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"COMPARADOR\")",
        f"=B{row_offset}/{n_low}",
    ])
    row_offset += 1
    values.append([
        "Pendentes",
        f"=COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"PENDENTE\")"
        f"+COUNTIF('{ref}'!{status_col}2:{status_col}{last_data_row},\"EM_REVISAO\")",
        f"=B{row_offset}/{n_low}",
    ])

    values_update(spreadsheet_id, "Progresso!A1:C50", values)

    sheet_id_prog = get_sheet_id(spreadsheet_id, "Progresso")
    reqs = []
    # Header formatting
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id_prog,
                "startRowIndex": 0, "endRowIndex": 1,
                "startColumnIndex": 0, "endColumnIndex": 3,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.067, "green": 0.067, "blue": 0.067},
                    "textFormat": {
                        "foregroundColor": {"red": 0.98, "green": 0.95, "blue": 0.88},
                        "bold": True, "fontSize": 12,
                    },
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat)",
        }
    })
    # Format % column as percentage
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id_prog,
                "startRowIndex": 1, "endRowIndex": 50,
                "startColumnIndex": 2, "endColumnIndex": 3,
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {"type": "PERCENT", "pattern": "0.0%"}
                }
            },
            "fields": "userEnteredFormat.numberFormat",
        }
    })
    for ci, w in enumerate([380, 120, 130]):
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id_prog, "dimension": "COLUMNS",
                          "startIndex": ci, "endIndex": ci+1},
                "properties": {"pixelSize": w},
                "fields": "pixelSize",
            }
        })
    batch_update(spreadsheet_id, reqs)
    print("[OK] Progresso sheet written with live COUNTIF formulas")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export low-confidence records to Google Sheets audit spreadsheet.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--records",
        default=DEFAULT_RECORDS_PATH,
        help=f"Path to records.jsonl (default: {DEFAULT_RECORDS_PATH})",
    )
    parser.add_argument(
        "--output-json",
        default=DEFAULT_OUTPUT_JSON,
        help=f"Local JSON backup path (default: {DEFAULT_OUTPUT_JSON})",
    )
    parser.add_argument(
        "--sheet-title",
        default=DEFAULT_SHEET_TITLE,
        help=f"Spreadsheet title (default: '{DEFAULT_SHEET_TITLE}')",
    )
    parser.add_argument(
        "--spreadsheet-id",
        default=None,
        help="Existing spreadsheet ID to update in place (skip create).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and export JSON only; skip Google Sheets upload.",
    )
    parser.add_argument(
        "--include-all-agents",
        action="store_true",
        help="Include ALL records, not only low-confidence ones.",
    )
    args = parser.parse_args()

    # ── 1. Parse ──────────────────────────────────────────────────────────
    print(f"[..] Parsing {args.records} …")
    low_conf, high_conf = parse_records(args.records)
    target_rows = low_conf if not args.include_all_agents else (low_conf + high_conf)
    print_summary(low_conf, high_conf)

    # ── 2. Save JSON backup ───────────────────────────────────────────────
    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_records": len(low_conf) + len(high_conf),
                "low_confidence_count": len(low_conf),
                "high_confidence_count": len(high_conf),
                "low_confidence_agents": list(LOW_CONFIDENCE_AGENTS) + ["batch-tentative-*"],
                "review_status_vocabulary": REVIEW_STATUS_OPTIONS,
                "rows": target_rows,
            },
            f,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    print(f"[OK] JSON backup → {out_path}  ({out_path.stat().st_size:,} bytes)")

    if args.dry_run:
        print("\n[DRY RUN] Skipping Google Sheets upload.")
        return

    # ── 3. Create or reuse spreadsheet ───────────────────────────────────
    if args.spreadsheet_id:
        spreadsheet_id = args.spreadsheet_id
        print(f"[..] Updating existing spreadsheet: {spreadsheet_id}")
        # Clear existing data in Registros
        gws(
            {
                "spreadsheetId": spreadsheet_id,
                "ranges": ["Registros!A:ZZ"],
            },
            "sheets", "spreadsheets", "values", "batchClear",
        )
    else:
        spreadsheet_id = create_spreadsheet(args.sheet_title)

    # ── 4. Get sheet IDs ─────────────────────────────────────────────────
    sheet_id_reg  = get_sheet_id(spreadsheet_id, "Registros")
    sheet_id_leg  = get_sheet_id(spreadsheet_id, "LEGEND")
    sheet_id_prog = get_sheet_id(spreadsheet_id, "Progresso")

    # ── 5. Write data ─────────────────────────────────────────────────────
    write_registros(spreadsheet_id, sheet_id_reg, target_rows)
    write_legend(spreadsheet_id, sheet_id_leg)
    write_progresso(
        spreadsheet_id,
        sheet_id_prog,
        n_total=len(low_conf) + len(high_conf),
        n_low=len(target_rows),
    )

    # ── 6. Done ───────────────────────────────────────────────────────────
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    print(f"\n{'='*60}")
    print(f"  ✓ Audit spreadsheet ready")
    print(f"  {url}")
    print(f"  {len(target_rows)} records · {len(COLUMNS)} columns")
    print(f"  Sheets: Registros | LEGEND | Progresso")
    print(f"{'='*60}\n")

    # Write spreadsheet ID to a local file for re-use
    id_file = Path("tmp/audit_spreadsheet_id.txt")
    id_file.parent.mkdir(exist_ok=True)
    id_file.write_text(f"{spreadsheet_id}\n{url}\n")
    print(f"[OK] Spreadsheet ID saved → {id_file}")


if __name__ == "__main__":
    main()
