#!/usr/bin/env python3
"""
Regenerate corpus/corpus-data-enriched.json from the canonical ledger
corpus/corpus-data.json (336 items), preserving overlay-only fields from a
FIXED overlay source for the legacy ids that exist in both.

The overlay source is resolved once and never drifts (review 2026-09-22, E1):
  1. corpus/corpus-data-enriched.legacy.json — committed pristine overlay
     (deliberate human choice; wins over everything);
  2. the OLDEST corpus-data-enriched.json.bak.* backup (sorted(glob)[0]);
  3. first-run bootstrap: a snapshot of the current enriched file is written
     as corpus-data-enriched.legacy.json and used from then on.
The chosen source is printed and recorded in the report.

Deterministic, offline, stdlib-only. Does NOT touch corpus-data.json, the site
copy at /Users/ana/Research/imagens/site/data/corpus-data-enriched.json, or
anything outside this repo.

Usage:
    python3 tools/scripts/regenerate_enriched.py [--dry-run]
    python3 tools/scripts/regenerate_enriched.py --validate-schema   # needs jsonschema
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
ENRICHED_PATH = REPO_ROOT / "corpus" / "corpus-data-enriched.json"
# Fixed overlay source (E1): committed snapshot, written once at bootstrap.
LEGACY_PATH = REPO_ROOT / "corpus" / "corpus-data-enriched.legacy.json"
REPORT_PATH = REPO_ROOT / "corpus" / "enrichment-report.md"
SCHEMA_PATH = Path("/Users/ana/Research/imagens/schemas/corpus-data-enriched.schema.json")
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
CROSSWALK_PATH = REPO_ROOT / "data" / "processed" / "id_crosswalk.jsonl"

# v2.3.0 purificacao fields propagated from records.jsonl into the enriched
# record (top level). Only emitted when the master record actually has them.
V230_FIELDS = [
    "atributos_iconograficos", "genero_atribuido", "familia_alegorica",
    "subtipo", "funcao_juridica", "vetor_colonial", "hipotese_racial",
    "referencia_genealogica", "programa_id", "ordem_no_programa",
    "dado_negativo", "finalidade_atribuida", "objetos_regalia",
    "marcas_corporais", "marcadores_cena_arquitetura",
    "relacao_com_repertorio_indigena", "disjuncao_representa_governa",
    "funcao_da_figura_masculina", "tipo_agencia_masculina",
    "funcao_atlanteana", "tipo_efluencia_hidrica",
    "substituicao_atributiva_hercules",
]

# Directories probed for local images matching <id>.* (relative to repo root).
# corpus/imagens/ does not exist on this machine (2026-06); kept for portability.
IMAGE_DIRS = ["corpus/imagens", "corpus/exemplares", "corpus/candidatos"]

# Import the existing keyword classifier (scenario C logic only; scenario B is
# network code and is never invoked here).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich_urls_and_regime import build_justification, classify_regime  # noqa: E402

# ─── Overlay fields preserved from the OLD enriched file (legacy ids only) ────
# The ledger owns: id, title, country, date, description, motif, url, regime,
# citation_abnt. Everything below is overlay-only.
OVERLAY_FIELDS = [
    "creator", "institution", "source_archive", "medium", "period", "rights",
    "thumbnail_url", "url_iiif", "url_image_download", "iiif_source",
    "iiif_note", "local_image_path", "citation_chicago", "tags",
    "regime_justificativa", "period_norm", "medium_norm",
]

# Fields that stay null for the 244 new items until a future network/IIIF pass.
NETWORK_PASS_FIELDS = [
    "iiif_source", "iiif_note", "url_iiif", "url_image_download",
    "thumbnail_url", "rights", "creator", "institution", "source_archive",
    "citation_chicago",
]

# Canonical medium taxonomy requested for NEW items (ledger support values and
# free-text variants are normalized into this list by keyword, in order).
CANONICAL_MEDIA = [
    "selo", "moeda", "papel-moeda", "estampa/gravura", "pintura",
    "monumento/escultura", "fotografia", "cartaz", "frontispício",
    "medalha", "cerâmica", "vitral",
]

COUNTRY_PT = {
    "France": "França",
    "Brazil": "Brasil",
    "United States": "Estados Unidos",
    "Germany": "Alemanha",
    "United Kingdom": "Reino Unido",
    "Italy": "Itália",
    "Portugal": "Portugal",
    "Belgium": "Bélgica",
    "Netherlands": "Países Baixos",
    "Spain": "Espanha",
    "Austria": "Áustria",
    "Denmark": "Dinamarca",
    "Mexico": "México",
    "Argentina": "Argentina",
    "Switzerland": "Suíça",
    "Uruguay": "Uruguai",
    "CL": "Chile",
}


def normalize_medium(support):
    """Map a ledger `support` value (canonical or free-text) to the canonical
    medium taxonomy. Keyword checks run in a deliberate order: more specific
    supports (frontispício, papel-moeda) before generic ones (gravura, moeda).
    Returns None for '?', None and 'None'."""
    if support is None:
        return None
    s = str(support).strip().lower()
    if s in ("", "?", "none"):
        return None
    rules = [
        (["frontispício", "frontispicio"], "frontispício"),
        (["papel-moeda", "cédula", "cedula"], "papel-moeda"),
        (["medalha"], "medalha"),
        (["cerâmica", "ceramica"], "cerâmica"),
        (["vitral"], "vitral"),
        (["selo", "brasão de armas"], "selo"),
        (["moeda"], "moeda"),
        (["cartaz", "pôster", "poster", "affiche"], "cartaz"),
        (["estampa", "gravura", "litografia", "ilustração"], "estampa/gravura"),
        (["escultura", "monumento", "plinto", "estátua"], "monumento/escultura"),
        (["fotografia", "foto"], "fotografia"),
        (["pintura"], "pintura"),
    ]
    for keywords, canonical in rules:
        if any(k in s for k in keywords):
            return canonical
    return None  # unmapped free text — flagged in the report


def derive_period(year, country):
    """Documented heuristic for NEW items (legacy items keep their old period).

    Brazil:
        ≤1822 Colonial · 1822–1889 Império · 1889–1930 República Velha ·
        1930–1945 Era Vargas · >1945 República
    France:
        ≤1789 Ancien Régime · 1789–1804 Révolution · 1804–1815 Empire ·
        1815–1848 Restauration/Monarchie de Juillet · 1848–1852 IIe République ·
        1852–1870 Second Empire · 1870–1940 IIIe République · >1940 Après-guerre
    All other countries: coarse pan-European/American buckets
        <1600 Early Modern (pre-1600) · 1600–1700 17th century ·
        1700–1800 18th century · 1800–1914 Long 19th century (1800–1914) ·
        1914–1918 World War I (1914–1918) · 1918–1939 Interwar (1918–1939) ·
        1939–1945 World War II (1939–1945) · 1945–1991 Cold War era
        (1945–1991) · >1991 Contemporary (1991–)

    period_norm for new items is left null: the old period_norm values use a
    mixed Portuguese taxonomy with no documented derivation, so inventing a
    mapping here would create a third, inconsistent vocabulary. A future pass
    should normalize legacy and new values together.
    """
    if not year:
        return None
    if country == "Brazil":
        if year <= 1822:
            return "Colonial"
        if year <= 1889:
            return "Império (1822–1889)"
        if year <= 1930:
            return "República Velha (1889–1930)"
        if year <= 1945:
            return "Era Vargas (1930–1945)"
        return "República (pós-1945)"
    if country == "France":
        if year <= 1789:
            return "Ancien Régime"
        if year <= 1804:
            return "Révolution (1789–1804)"
        if year <= 1815:
            return "Empire (1804–1815)"
        if year <= 1848:
            return "Restauration/Monarchie de Juillet (1815–1848)"
        if year <= 1852:
            return "IIe République (1848–1852)"
        if year <= 1870:
            return "Second Empire (1852–1870)"
        if year <= 1940:
            return "IIIe République (1870–1940)"
        return "Après-guerre (1940–)"
    # Generic buckets for all other countries.
    if year < 1600:
        return "Early Modern (pre-1600)"
    if year < 1700:
        return "17th century"
    if year < 1800:
        return "18th century"
    if year < 1914:
        return "Long 19th century (1800–1914)"
    if year <= 1918:
        return "World War I (1914–1918)"
    if year <= 1939:
        return "Interwar (1918–1939)"
    if year <= 1945:
        return "World War II (1939–1945)"
    if year <= 1991:
        return "Cold War era (1945–1991)"
    return "Contemporary (1991–)"


def extract_year(date_str):
    """First 3–4 digit number in the date string, as int; else None."""
    if not date_str:
        return None
    m = re.search(r"\d{3,4}", str(date_str))
    return int(m.group(0)) if m else None


def country_base(country):
    """Strip parenthetical provenance notes, e.g. 'Germany (Netherlands
    origin)' → 'Germany'."""
    return re.sub(r"\s*\(.*?\)\s*", "", str(country or "")).strip()


def find_local_image(item_id):
    """Look for corpus/imagens/**/<id>.* (and a couple of sibling dirs).
    Returns the repo-relative path as a string, or None."""
    for rel in IMAGE_DIRS:
        base = REPO_ROOT / rel
        if not base.is_dir():
            continue
        matches = sorted(base.rglob(f"{item_id}.*"))
        if matches:
            return str(matches[0].relative_to(REPO_ROOT))
    return None


def resolve_overlay_source():
    """Resolve the FIXED overlay source, in priority order (review E1):

    1. corpus-data-enriched.legacy.json — committed pristine overlay;
    2. the OLDEST corpus-data-enriched.json.bak.* (sorted(glob)[0]);
    3. first-run bootstrap: snapshot the current enriched file as
       corpus-data-enriched.legacy.json and use it.

    The date-stamped "backup of today, else backup the current file" logic is
    gone: it made the script's own output become the overlay on the next day,
    silently redefining "legacy" and freezing derived fields (E1/E2).

    Returns (path, origin_label, overlay_records).
    """
    if LEGACY_PATH.exists():
        path, origin = LEGACY_PATH, "legacy.json commitado"
    else:
        backups = sorted(ENRICHED_PATH.parent.glob(
            f"{ENRICHED_PATH.name}.bak.*"))
        if backups:
            path, origin = backups[0], f"backup mais antigo ({backups[0].name})"
        else:
            if not ENRICHED_PATH.exists():
                sys.exit(
                    f"Nenhuma fonte de overlay e {ENRICHED_PATH} não existe — "
                    "nada para fazer bootstrap.")
            path, origin = LEGACY_PATH, (
                "bootstrap (snapshot do enriched atual — verifique se é o "
                "overlay pristino; substitua por um legacy.json deliberado se não for)")
            path.write_bytes(ENRICHED_PATH.read_bytes())
    try:
        overlay = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Fonte de overlay {path} ilegível: {e}")
    if not isinstance(overlay, list) or not all(
            isinstance(o, dict) and o.get("id") for o in overlay):
        sys.exit(
            f"Fonte de overlay {path} não é uma lista de objetos com 'id'.")
    return path, origin, overlay


def load_master_records():
    """Index data/processed/records.jsonl by item_id (uuid) and build a
    handle -> uuid map from the crosswalk, so ledger items addressed by
    corpus handle (FR-007) can reach their master record. Returns
    (records_by_uuid, handle_to_uuid). Missing files yield empty maps —
    the regeneration then behaves exactly as before (no Panofsky overlay)."""
    records_by_uuid = {}
    if RECORDS_PATH.exists():
        with RECORDS_PATH.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("item_id"):
                    records_by_uuid[r["item_id"]] = r
    handle_to_uuid = {}
    if CROSSWALK_PATH.exists():
        with CROSSWALK_PATH.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                handle, uuid = d.get("handle"), d.get("uuid")
                if handle and uuid:
                    handle_to_uuid[handle] = uuid
    return records_by_uuid, handle_to_uuid


def resolve_master_record(item_id, records_by_uuid, handle_to_uuid):
    """Ledger ids are corpus handles (FR-007) for legacy items or UUIDs for
    vault imports. Resolve to the master record either way."""
    if item_id in records_by_uuid:
        return records_by_uuid[item_id]
    uuid = handle_to_uuid.get(item_id)
    if uuid:
        return records_by_uuid.get(uuid)
    return None


def ledger_justification(item, regime_upper):
    coded_by = item.get("coded_by") or "desconhecido"
    coded_at = str(item.get("coded_at") or "")[:10] or "data desconhecida"
    return f"classificado no ledger por {coded_by} em {coded_at} → {regime_upper}"


def build_record(item, old_by_id, stats, master=None):
    """Merge one ledger item with its old-enriched overlay (if any) and with
    the master record from records.jsonl (Panofsky 3 níveis + campos v2.3.0,
    when resolvable)."""
    item_id = item["id"]
    old = old_by_id.get(item_id)
    is_legacy = old is not None

    regime_lower = (item.get("regime") or "").strip().lower()
    regime_upper = regime_lower.upper()
    motif = item.get("motif") if isinstance(item.get("motif"), list) else []
    year = extract_year(item.get("date"))
    base_country = country_base(item.get("country"))
    country_pt = COUNTRY_PT.get(base_country, item.get("country"))

    # ── regime_justificativa ────────────────────────────────────────────────
    # Legacy items keep the old text UNLESS the ledger regime changed.
    old_regime = (old or {}).get("regime")
    regime_changed = is_legacy and old_regime and old_regime != regime_upper
    if regime_changed:
        stats["legacy_regime_changed"].append(
            (item_id, old_regime, regime_upper))

    # ── tags / regime_incerto ───────────────────────────────────────────────
    if is_legacy and isinstance(old.get("tags"), list):
        tags = list(old["tags"])
    else:
        tags = list(motif)

    justificativa = None
    if is_legacy and not regime_changed and old.get("regime_justificativa"):
        justificativa = old["regime_justificativa"]
    else:
        # (Re)generate: run the keyword classifier against a pseudo-item.
        pseudo = {
            "title": item.get("title") or "",
            "description": item.get("description") or "",
            "medium": (old or {}).get("medium") or item.get("support") or "",
            "medium_norm": (old or {}).get("medium_norm")
            or normalize_medium(item.get("support")) or "",
            "period": (old or {}).get("period") or derive_period(year, base_country) or "",
            "date": item.get("date") or "",
            "motif_str": ", ".join(motif),
            "tags_str": ", ".join(tags),
            "year": year or 0,
        }
        clf_regime, uncertain, clf_just, _scores = classify_regime(pseudo)
        if clf_regime == regime_upper and not uncertain:
            justificativa = clf_just
        else:
            justificativa = ledger_justification(item, regime_upper)
            if clf_regime != regime_upper:
                # Classifier actively disagrees → flag for review.
                if "regime_incerto" not in tags:
                    tags.append("regime_incerto")
                stats["regime_incerto"].append(
                    (item_id, regime_upper, clf_regime))

    # ── overlay fields ──────────────────────────────────────────────────────
    record = {}
    for field in OVERLAY_FIELDS:
        if is_legacy and old.get(field) not in (None, "", []):
            record[field] = old[field]
        else:
            record[field] = None

    # ── medium / period: precedência do ledger, overlay curado preservado ────
    # Qualquer item presente no ledger tem seus campos derivados do ledger
    # (review E2). O overlay NÃO congela mais a derivação: para itens novos
    # tudo é derivado; para itens legados, valores curados do overlay são
    # preservados e o ledger só preenche lacunas que o overlay não tem
    # (gap-fill — neutro nos dados atuais: 0 disparos). Assim o resultado é
    # uma função pura de (ledger, fonte de overlay fixa), idempotente entre
    # execuções.
    support = item.get("support")
    support_clean = (
        None
        if support is None or str(support).strip().lower() in ("", "?", "none")
        else str(support)
    )
    if not is_legacy:
        record["medium"] = support_clean
        record["medium_norm"] = normalize_medium(support)
        if support_clean and record["medium_norm"] is None:
            stats["medium_unmapped"].append((item_id, support))
        record["period"] = derive_period(year, base_country)
        record["period_norm"] = None  # see derive_period docstring
    else:
        if not record.get("medium") and support_clean:
            record["medium"] = support_clean
        if record.get("medium_norm") is None:
            record["medium_norm"] = normalize_medium(support)
        if support_clean and record.get("medium_norm") is None:
            stats["medium_unmapped"].append((item_id, support))
        if not record.get("period") and year:
            record["period"] = derive_period(year, base_country)

    # ── local_image_path ────────────────────────────────────────────────────
    if not record.get("local_image_path"):
        record["local_image_path"] = find_local_image(item_id)

    # ── assemble (old enriched field order first, extras after) ─────────────
    iconographic_metadata = {"visual_regime": regime_lower}
    if item.get("endurecimento_score") is not None:
        iconographic_metadata["endurecimento_score"] = item["endurecimento_score"]
    # Panofsky 3 níveis + attributes/iconclass mapped from the master record
    # into the schema's canonical vocabulary (regenerate validates against
    # imagens/schemas/corpus-data-enriched.schema.json).
    if master:
        ico = master.get("iconocode") or {}
        pur_m = master.get("purificacao") or {}
        panofsky = {}
        if ico.get("pre_iconographic"):
            panofsky["pre_iconographic"] = ico["pre_iconographic"]
        if ico.get("codes"):
            panofsky["codes"] = ico["codes"]
        if ico.get("interpretation"):
            panofsky["interpretation"] = ico["interpretation"]
        if ico.get("confidence") is not None:
            panofsky["confidence"] = ico["confidence"]
        if panofsky:
            iconographic_metadata["panofsky"] = panofsky
        if pur_m.get("atributos_iconograficos"):
            iconographic_metadata["attributes"] = pur_m["atributos_iconograficos"]
        notations = [
            c["notation"] for c in (ico.get("codes") or [])
            if c.get("scheme") == "iconclass" and c.get("notation")
        ]
        if notations:
            iconographic_metadata["iconclass"] = notations

    out = {
        "id": item_id,
        "title": item.get("title") or "",
        "date": item.get("date") or "",  # schema requires string; "" when missing
        "period": record.get("period"),
        "creator": record.get("creator"),
        "institution": record.get("institution"),
        "source_archive": record.get("source_archive"),
        "country": item.get("country"),
        "medium": record.get("medium"),
        "motif": motif,
        "description": item.get("description") or "",
        "url": item.get("url"),
        "thumbnail_url": record.get("thumbnail_url"),
        "rights": record.get("rights"),
        "citation_abnt": item.get("citation_abnt"),
        "citation_chicago": record.get("citation_chicago"),
        "tags": tags,
        "year": year,
        "medium_norm": record.get("medium_norm"),
        "country_pt": country_pt,
        "period_norm": record.get("period_norm"),
        "motif_str": ", ".join(motif),
        "tags_str": ", ".join(tags),
        "url_iiif": record.get("url_iiif"),
        "url_image_download": record.get("url_image_download"),
        "iiif_source": record.get("iiif_source"),
        "iiif_note": record.get("iiif_note"),
        "regime": regime_upper,
        "regime_justificativa": justificativa,
        "local_image_path": record.get("local_image_path"),
        # Ledger provenance, preserved verbatim (schema allows additional props):
        "support": support,
        "coded_by": item.get("coded_by"),
        "coded_at": item.get("coded_at"),
        "audit_flags": item.get("audit_flags"),
        "endurecimento_score": item.get("endurecimento_score"),
        "indicadores": item.get("indicadores"),
        "iconographic_metadata": iconographic_metadata,
    }
    # v2.3.0 purificacao fields (atributos, gênero, família alegórica, agência
    # masculina etc.) — only emitted when present in the master record.
    if master:
        pur = master.get("purificacao") or {}
        for field in V230_FIELDS:
            if pur.get(field) not in (None, "", []):
                out[field] = pur[field]
        if pur:
            stats["with_master"] += 1
        if pur.get("atributos_iconograficos"):
            stats["with_atributos"] += 1
    if "panofsky" in iconographic_metadata:
        stats["with_panofsky"] += 1
    # The old enriched file never emitted nulls for string-typed optional
    # fields — it omitted the keys (the schema types them as "string" only).
    # Null is kept only where the schema explicitly allows it.
    NULL_ALLOWED = {
        "url", "url_iiif", "url_image_download", "thumbnail_url",
        "local_image_path", "iiif_note", "iiif_source", "year",
    }
    out = {
        k: v for k, v in out.items()
        if v is not None or k in NULL_ALLOWED
    }
    return out, is_legacy


def validate_structural(records):
    """Cheap structural checks that need no third-party libraries."""
    errors = []
    required = ["id", "title", "country", "date", "regime", "url", "motif"]
    ids = [r["id"] for r in records]
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    if dupes:
        errors.append(f"duplicate ids: {dupes}")
    for r in records:
        for field in required:
            if field not in r:
                errors.append(f"{r['id']}: missing required field '{field}'")
        if not isinstance(r.get("motif"), list):
            errors.append(f"{r['id']}: motif is not a list")
        meta = r.get("iconographic_metadata") or {}
        if "visual_regime" not in meta:
            errors.append(f"{r['id']}: iconographic_metadata missing visual_regime")
        if "endurecimento_score" in meta and not isinstance(
                meta["endurecimento_score"], (int, float)):
            errors.append(f"{r['id']}: endurecimento_score is not a number")
    return errors


def validate_with_schema(records):
    """Optional full JSON-Schema validation (requires `jsonschema`)."""
    try:
        import jsonschema
    except ImportError:
        print("jsonschema not importable in this interpreter — skipped.")
        return None
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    id_pattern_failures = 0
    score_range_failures = 0
    other = []
    for err in validator.iter_errors(records):
        msg = err.message
        # UUID-style ids are a known, accepted warning class.
        if "does not match" in msg and "^[A-Z]" in msg and list(err.absolute_path)[:-1] and str(err.absolute_path[-1]) == "id":
            id_pattern_failures += 1
        elif "greater than the maximum" in msg and str(err.absolute_path[-1]) == "endurecimento_score":
            score_range_failures += 1
        else:
            other.append(f"{list(err.absolute_path)}: {msg}")
    return {
        "id_pattern_failures": id_pattern_failures,
        "score_range_failures": score_range_failures,
        "other_violations": other,
    }


def write_report(records, stats, today):
    regimes = Counter(r["regime"] for r in records)
    countries = Counter(r["country"] for r in records)
    missing_date = [r["id"] for r in records if not r["date"]]
    missing_support = [
        r["id"] for r in records
        if r.get("support") is None or str(r.get("support")).strip().lower() in ("", "?", "none")
    ]
    coverage_fields = [
        "creator", "institution", "source_archive", "medium", "medium_norm",
        "period", "rights", "thumbnail_url", "url_iiif", "url_image_download",
        "iiif_source", "iiif_note", "local_image_path", "citation_chicago",
        "citation_abnt", "year",
    ]
    coverage = {
        f: sum(1 for r in records if r.get(f) not in (None, "", []))
        for f in coverage_fields
    }
    score_over_one = [
        (r["id"], r["endurecimento_score"]) for r in records
        if isinstance(r.get("endurecimento_score"), (int, float))
        and r["endurecimento_score"] > 1
    ]

    new_items = len(records) - stats["legacy_overlays"]
    orphan_count = len(stats["orphans"])
    lip_filled = coverage["local_image_path"]
    lip_null = len(records) - lip_filled

    lines = [
        "# Relatório de regeneração — corpus-data-enriched.json",
        "",
        f"**Data**: {today}",
        f"**Fonte autoritativa**: `corpus/corpus-data.json` ({stats['ledger_count']} itens)",
        f"**Fonte de overlay (fixa)**: `{stats.get('overlay_source', 'desconhecida')}` "
        f"— {stats['old_count']} itens, origem: {stats.get('overlay_origin', 'desconhecida')}",
        f"**Overlays legados preservados**: {stats['legacy_overlays']} ids presentes em ambos",
        f"**Saída**: `corpus/corpus-data-enriched.json` ({len(records)} itens, "
        "ordenados por país + id)",
        "",
        "## Órfãos do enriched anterior (revisão necessária)",
        "",
        "Presentes no enriched antigo, **ausentes do ledger** — excluídos da regeneração:",
        "",
    ]
    for oid, title in stats["orphans"]:
        lines.append(f"- **{oid}** — {title}")
    lines += [
        "",
        "## Distribuição por regime",
        "",
        "| Regime | Itens |",
        "|--------|-------|",
    ]
    for k, v in sorted(regimes.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Distribuição por país",
        "",
        "| País (ledger) | Itens |",
        "|---------------|-------|",
    ]
    for k, v in sorted(countries.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Qualidade e lacunas",
        "",
        f"- Itens com `regime_incerto` (classificador diverge do ledger): "
        f"**{len(stats['regime_incerto'])}**",
        f"- Itens sem `date` no ledger (emitidos com `date: \"\"`): **{len(missing_date)}**",
        f"- Itens sem `support` útil (None/'?'): **{len(missing_support)}**",
        f"- Itens legados cujo regime mudou em relação ao enriched antigo "
        f"(ledger vence, justificativa regenerada): **{len(stats['legacy_regime_changed'])}**",
        f"- Valores de `support` em texto livre sem mapeamento canônico: "
        f"**{len(stats['medium_unmapped'])}**",
        "",
        "### Cobertura de campos",
        "",
        "| Campo | Itens preenchidos |",
        "|-------|-------------------|",
    ]
    for f, n in coverage.items():
        lines.append(f"| {f} | {n}/{len(records)} |")
    lines += [
        "",
        "## Anomalias do ledger",
        "",
        f"- **{len(score_over_one)} itens com `endurecimento_score` > 1.0** "
        f"(máx. {max((s for _, s in score_over_one), default=0)}). A escala "
        "real parece ser 0–3 (média dos 10 indicadores, cada um 0–3), não 0–1. "
        "O schema externo exige máximo 1 — esses itens falham na validação de "
        "intervalo (classe conhecida). Recomendado: normalizar dividindo por 3 "
        "ou revisar o schema.",
        f"- {len(missing_date)} itens sem `date` (ano derivado null).",
        "- `country` usa variantes com parênteses ('Germany (Netherlands origin)', "
        "'France (held in Austria)') e o código 'CL' em vez de 'Chile' — "
        "`country_pt` foi derivado do país-base.",
        "",
        f"## Lacunas conhecidas dos {new_items} itens novos",
        "",
        "Nulos até uma futura passada de rede/IIIF: "
        + ", ".join(f"`{f}`" for f in NETWORK_PASS_FIELDS)
        + ". `period_norm` também é null para itens novos (ver docstring de "
        "`derive_period` no script). "
        + (f"`local_image_path` é null em {lip_null}/{len(records)} "
           f"({lip_filled} preenchidos via overlay legado — verificar "
           "existência em disco)." if lip_filled else
           f"`local_image_path` é null para todos os {len(records)}: "
           "`corpus/imagens/` não existe nesta máquina."),
        "",
        "## Follow-up",
        "",
        "- **Não sincronizado**: `/Users/ana/Research/imagens/site/data/corpus-data-enriched.json` "
        "(cópia do site) — atualizar em passo separado, fora deste repositório.",
        f"- Decidir o destino dos {orphan_count} órfãos "
        "(reimportar ao ledger ou aposentar).",
        "- Revisar itens com `regime_incerto` listados abaixo.",
        "",
        "### Itens com regime_incerto (ledger ≠ classificador)",
        "",
    ]
    for item_id, led, clf in stats["regime_incerto"]:
        lines.append(f"- {item_id}: ledger={led}, classificador={clf}")
    if stats["legacy_regime_changed"]:
        lines += ["", "### Regimes alterados em itens legados", ""]
        for item_id, old_r, new_r in stats["legacy_regime_changed"]:
            lines.append(f"- {item_id}: {old_r} → {new_r}")
    if stats["medium_unmapped"]:
        lines += ["", "### Support sem mapeamento canônico", ""]
        for item_id, sup in stats["medium_unmapped"]:
            lines.append(f"- {item_id}: {sup!r}")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main():
    dry_run = "--dry-run" in sys.argv
    validate_only = "--validate-schema" in sys.argv

    if validate_only:
        records = json.loads(ENRICHED_PATH.read_text(encoding="utf-8"))
        result = validate_with_schema(records)
        if result is None:
            sys.exit(2)
        print(f"itens: {len(records)}")
        print(f"id pattern failures (UUID, classe conhecida): {result['id_pattern_failures']}")
        print(f"endurecimento_score > 1 (classe conhecida): {result['score_range_failures']}")
        print(f"outras violações: {len(result['other_violations'])}")
        for v in result["other_violations"][:30]:
            print("  -", v)
        return

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    today = datetime.date.today().isoformat()
    # Fixed overlay source (E1): legacy.json > oldest .bak.* > bootstrap
    # snapshot. Never the script's own output of a previous day.
    overlay_path, overlay_origin, old = resolve_overlay_source()
    print(f"Fonte de overlay (fixa): {overlay_path.name} — {overlay_origin}")
    old_by_id = {o["id"]: o for o in old}

    try:
        overlay_display = str(overlay_path.relative_to(REPO_ROOT))
    except ValueError:
        overlay_display = str(overlay_path)
    stats = {
        "ledger_count": len(ledger),
        "old_count": len(old),
        "overlay_source": overlay_display,
        "overlay_origin": overlay_origin,
        "legacy_overlays": 0,
        "orphans": [
            (o["id"], o.get("title", "?"))
            for o in old if o["id"] not in {i["id"] for i in ledger}
        ],
        "regime_incerto": [],
        "legacy_regime_changed": [],
        "medium_unmapped": [],
        "with_master": 0,
        "with_panofsky": 0,
        "with_atributos": 0,
    }

    records_by_uuid, handle_to_uuid = load_master_records()

    records = []
    for item in ledger:
        master = resolve_master_record(
            item["id"], records_by_uuid, handle_to_uuid)
        record, is_legacy = build_record(item, old_by_id, stats, master)
        if is_legacy:
            stats["legacy_overlays"] += 1
        records.append(record)

    records.sort(key=lambda r: (r["country"] or "", r["id"]))

    errors = validate_structural(records)
    if errors:
        print("STRUCTURAL ERRORS:")
        for e in errors[:50]:
            print("  -", e)
        sys.exit(1)
    print(f"Structural check OK: {len(records)} items, required fields present, no duplicate ids.")

    if dry_run:
        print("DRY RUN — no files written.")
        return

    with ENRICHED_PATH.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(records)} records to {ENRICHED_PATH}")

    write_report(records, stats, today)
    print(f"Report written: {REPORT_PATH}")

    print(f"Legacy overlays preserved: {stats['legacy_overlays']}")
    print(f"Orphans excluded: {[o for o, _ in stats['orphans']]}")
    print(f"regime_incerto: {len(stats['regime_incerto'])}")
    print(f"Legacy regime changes: {len(stats['legacy_regime_changed'])}")
    print(f"Unmapped support values: {len(stats['medium_unmapped'])}")
    print(f"Master records resolved: {stats['with_master']}")
    print(f"With Panofsky (pre_iconographic): {stats['with_panofsky']}")
    print(f"With atributos_iconograficos (v2.3.0): {stats['with_atributos']}")


if __name__ == "__main__":
    main()
