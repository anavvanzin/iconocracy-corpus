#!/usr/bin/env python3
"""
Regenerate corpus/corpus-data-enriched.json from the canonical ledger
corpus/corpus-data.json (335 items), preserving overlay-only fields from the
previous enriched file (95 items) for the 91 legacy ids that exist in both.

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
REPORT_PATH = REPO_ROOT / "corpus" / "enrichment-report.md"
SCHEMA_PATH = Path("/Users/ana/Research/imagens/schemas/corpus-data-enriched.schema.json")

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


def ledger_justification(item, regime_upper):
    coded_by = item.get("coded_by") or "desconhecido"
    coded_at = str(item.get("coded_at") or "")[:10] or "data desconhecida"
    return f"classificado no ledger por {coded_by} em {coded_at} → {regime_upper}"


def build_record(item, old_by_id, stats):
    """Merge one ledger item with its old-enriched overlay (if any)."""
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

    # ── medium / period for new items ───────────────────────────────────────
    support = item.get("support")
    if not is_legacy:
        support_clean = (
            None
            if support is None or str(support).strip().lower() in ("", "?", "none")
            else str(support)
        )
        record["medium"] = support_clean
        record["medium_norm"] = normalize_medium(support)
        if support_clean and record["medium_norm"] is None:
            stats["medium_unmapped"].append((item_id, support))
        record["period"] = derive_period(year, base_country)
        record["period_norm"] = None  # see derive_period docstring

    # ── local_image_path ────────────────────────────────────────────────────
    if not record.get("local_image_path"):
        record["local_image_path"] = find_local_image(item_id)

    # ── assemble (old enriched field order first, extras after) ─────────────
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
        "iconographic_metadata": {
            "visual_regime": regime_lower,
            "endurecimento_score": item.get("endurecimento_score"),
        },
    }
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
        if "visual_regime" not in meta or "endurecimento_score" not in meta:
            errors.append(f"{r['id']}: incomplete iconographic_metadata")
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

    lines = [
        "# Relatório de regeneração — corpus-data-enriched.json",
        "",
        f"**Data**: {today}",
        f"**Fonte autoritativa**: `corpus/corpus-data.json` ({stats['ledger_count']} itens)",
        f"**Enriched anterior**: {stats['old_count']} itens "
        f"({stats['legacy_overlays']} overlays legados preservados)",
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
        "- 22 itens sem `date` (ano derivado null).",
        "- `country` usa variantes com parênteses ('Germany (Netherlands origin)', "
        "'France (held in Austria)') e o código 'CL' em vez de 'Chile' — "
        "`country_pt` foi derivado do país-base.",
        "",
        "## Lacunas conhecidas dos 244 itens novos",
        "",
        "Nulos até uma futura passada de rede/IIIF: "
        + ", ".join(f"`{f}`" for f in NETWORK_PASS_FIELDS)
        + ". `period_norm` também é null para itens novos (ver docstring de "
        "`derive_period` no script). `local_image_path` é null para todos: "
        "`corpus/imagens/` não existe nesta máquina.",
        "",
        "## Follow-up",
        "",
        "- **Não sincronizado**: `/Users/ana/Research/imagens/site/data/corpus-data-enriched.json` "
        "(cópia do site) — atualizar em passo separado, fora deste repositório.",
        "- Decidir o destino dos 4 órfãos (reimportar ao ledger ou aposentar).",
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
    backup = ENRICHED_PATH.with_suffix(f".json.bak.{today}")
    # Idempotency: the "old enriched" overlay source must be the state BEFORE
    # this script first ran today. If today's backup exists, read overlays from
    # it; otherwise create the backup now and read from it. Re-running the
    # script later the same day therefore yields identical results instead of
    # treating its own output as legacy overlays.
    if backup.exists():
        print(f"Reading old overlays from today's backup: {backup.name}")
    else:
        backup.write_bytes(ENRICHED_PATH.read_bytes())
        print(f"Backup written: {backup}")
    old = json.loads(backup.read_text(encoding="utf-8"))
    old_by_id = {o["id"]: o for o in old}

    stats = {
        "ledger_count": len(ledger),
        "old_count": len(old),
        "legacy_overlays": 0,
        "orphans": [
            (o["id"], o.get("title", "?"))
            for o in old if o["id"] not in {i["id"] for i in ledger}
        ],
        "regime_incerto": [],
        "legacy_regime_changed": [],
        "medium_unmapped": [],
    }

    records = []
    for item in ledger:
        record, is_legacy = build_record(item, old_by_id, stats)
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


if __name__ == "__main__":
    main()
