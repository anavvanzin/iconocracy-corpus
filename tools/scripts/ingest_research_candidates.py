#!/usr/bin/env python3
"""Ingest deep-research candidates into records.jsonl as provisional master records.

Reads a flat candidate JSON (the SHARED_SPEC schema produced by the 2026-05-19
research run), keeps only candidates that meet the corpus inclusion criteria
(one of the 6 countries + datable 1800–2000), and appends them to
data/processed/records.jsonl as schema-valid master records.

The candidates carry no IconoCode analysis (no regime / endurecimento), so the
records are written WITHOUT a `purificacao` block and flagged
`iconocode-pendente` in exports.audit_flags. Run the IconoCode pass later and
backfill. After ingest, regenerate corpus-data.json via records_to_corpus.py.

Idempotent: a candidate whose deterministic item_id already exists in
records.jsonl is skipped.

Usage:
    python tools/scripts/ingest_research_candidates.py --input corpus/candidatos/2026-05-19/candidatos-2026-05-19.json
    python tools/scripts/ingest_research_candidates.py --input <file> --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from csv_to_records import _item_uuid, item_to_record  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
RECORDS = REPO / "data" / "processed" / "records.jsonl"
CORPUS = REPO / "corpus" / "corpus-data.json"
TODAY = date.today().isoformat()

ALLOWED_COUNTRIES = {
    "France", "United Kingdom", "Germany", "United States", "Belgium", "Brazil",
}
PROVENANCE = "iconocracia-2026-05-19"
# Authors still under copyright in Brazil (70 y.p.m.a.) — block public release
COPYRIGHT_NAMES = ("portinari",)

# Curated KEEP set per the authoritative review on main
# (corpus/candidatos/review-2026-05-19.md). One country override for #2.
KEEP_SETS: dict[str, set[str]] = {
    "keep7": {
        "sq1-2026-05-19-baker-godwin-lincoln-005",
        "sq1-2026-05-19-gusman-justice-vengeance-003",
        "sq1-2026-05-19-inger-liberty-004",
        "sq1-2026-05-19-kimmel-outbreak-007",
        "sq1-2026-05-19-traubel-triumph-006",
        "sq2-2026-05-19-alegoria-lei-aurea-villares-004",
        "sq2-2026-05-19-republica-manoel-lopes-rodrigues-003",
    },
}
DEFAULT_COUNTRY_OVERRIDES: dict[str, str] = {
    # Prud'hon composition; French reproduction print — reviewer correction.
    "sq1-2026-05-19-gusman-justice-vengeance-003": "France",
}


def _years(date: str | None) -> list[int]:
    return [int(m) for m in re.findall(r"\d{4}", str(date or ""))]


def in_scope(cand: dict) -> bool:
    if cand.get("country") not in ALLOWED_COUNTRIES:
        return False
    ys = _years(cand.get("date"))
    return bool(ys) and min(ys) >= 1800 and any(1800 <= y <= 2000 for y in ys)


def candidate_to_corpus_item(cand: dict) -> dict:
    """Map the flat SHARED_SPEC candidate to the corpus-item shape item_to_record expects."""
    return {
        "id": cand["id"],
        "url": cand.get("url", ""),
        "title": cand.get("title", ""),
        "date": cand.get("date", ""),
        "country": cand.get("country", ""),
        "description": cand.get("description", ""),
        "motif": cand.get("motif", []),
        "citation_abnt": cand.get("citation_abnt", ""),
        "thumbnail_url": cand.get("thumbnail_url"),
        "in_scope": True,
        # Carry the candidate's ICONCLASS into webscout/iconocode via panofsky.iconographic
        "panofsky": {"iconographic": {"iconclass": cand.get("iconclass_codes", [])}},
        # No regime / indicadores / endurecimento_score → record stays uncoded (no purificacao)
    }


def _audit_flags(cand: dict, base: list[str] | None = None) -> list[str]:
    flags = [f for f in (base or []) if f != "fora-do-escopo"]
    flags += ["#verificar", "iconocode-pendente", f"provenance:{PROVENANCE}"]
    blob = (str(cand.get("creator", "")) + " " + str(cand.get("description", ""))).lower()
    if any(n in blob for n in COPYRIGHT_NAMES):
        flags.append("copyright-hold")
    return sorted(set(flags))


def build_record(cand: dict) -> dict:
    rec = item_to_record(candidate_to_corpus_item(cand), None)
    rec["exports"]["audit_flags"] = _audit_flags(cand, rec["exports"].get("audit_flags", []))
    return rec


def build_corpus_entry(cand: dict) -> dict:
    """Build a flat enriched corpus-data.json entry (uncoded; pending IconoCode)."""
    return {
        "id": cand["id"],
        "title": cand.get("title", ""),
        "date": str(cand.get("date", "")),
        "period": cand.get("period", ""),
        "creator": cand.get("creator", ""),
        "institution": cand.get("institution", ""),
        "source_archive": cand.get("source_archive", ""),
        "country": cand.get("country", ""),
        "medium": cand.get("medium", ""),
        "motif": cand.get("motif", []),
        "description": cand.get("description", ""),
        "url": cand.get("url", ""),
        "thumbnail_url": cand.get("thumbnail_url") or "",
        "rights": cand.get("rights", ""),
        "citation_abnt": cand.get("citation_abnt", ""),
        "citation_chicago": cand.get("citation_chicago", ""),
        "tags": cand.get("tags", []),
        "url_iiif": cand.get("url_iiif") or "",
        "url_image_download": cand.get("url_image_download") or "",
        "iiif_source": cand.get("iiif_source") or "",
        "panofsky": {"iconographic": {"iconclass": cand.get("iconclass_codes", [])}},
        "regime": "",
        "endurecimento_score": 0.0,
        "coded_by": "pending-iconocode",
        "coded_at": TODAY,
        "in_scope": True,
        "testemunho_repertoire": "",
        "audit_flags": _audit_flags(cand),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", "-i", type=Path, required=True)
    ap.add_argument("--records", type=Path, default=RECORDS)
    ap.add_argument("--corpus", type=Path, default=CORPUS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--keep-set",
        choices=sorted(KEEP_SETS.keys()),
        help="Use a curated id whitelist instead of the country+period gate "
             "(e.g. 'keep7' = the 7 KEEP items from the main review).",
    )
    args = ap.parse_args()

    candidates = json.loads(args.input.read_text(encoding="utf-8"))
    if args.keep_set:
        whitelist = KEEP_SETS[args.keep_set]
        # Apply country overrides from the review (e.g. #2 Gusman: UK → France)
        for c in candidates:
            if c["id"] in DEFAULT_COUNTRY_OVERRIDES:
                c["country"] = DEFAULT_COUNTRY_OVERRIDES[c["id"]]
        kept = [c for c in candidates if c["id"] in whitelist]
        skipped = len(candidates) - len(kept)
        print(f"Candidatos: {len(candidates)} | KEEP-set '{args.keep_set}' ({len(whitelist)}): {len(kept)} | fora: {skipped}")
    else:
        kept = [c for c in candidates if in_scope(c)]
        skipped = len(candidates) - len(kept)
        print(f"Candidatos: {len(candidates)} | dentro do escopo (6 países + 1800–2000): {len(kept)} | fora: {skipped}")

    # --- records.jsonl (canonical) ---
    existing_lines = args.records.read_text(encoding="utf-8").splitlines() if args.records.exists() else []
    existing_item_ids = {json.loads(l)["item_id"] for l in existing_lines if l.strip()}
    new_records = [build_record(c) for c in kept if _item_uuid(c["id"]) not in existing_item_ids]

    # --- corpus-data.json (public export) — append-only, existing items untouched ---
    corpus = json.loads(args.corpus.read_text(encoding="utf-8")) if args.corpus.exists() else []
    existing_corpus_ids = {c.get("id") for c in corpus}
    new_corpus = [build_corpus_entry(c) for c in kept if c["id"] not in existing_corpus_ids]

    print(f"records.jsonl: +{len(new_records)} novos (pulados {len(kept) - len(new_records)} já presentes)")
    print(f"corpus-data.json: +{len(new_corpus)} novos (pulados {len(kept) - len(new_corpus)} já presentes)")

    if not new_records and not new_corpus:
        print("Nada a fazer (idempotente).")
        return 0

    if args.dry_run:
        if new_records:
            print("\n[DRY-RUN] Amostra do primeiro registro novo (records.jsonl):")
            print(json.dumps(new_records[0], ensure_ascii=False, indent=2)[:1200])
        print(f"\n[DRY-RUN] records.jsonl: {len(existing_lines)} → {len(existing_lines) + len(new_records)} | "
              f"corpus-data.json: {len(corpus)} → {len(corpus) + len(new_corpus)}")
        return 0

    if new_records:
        with args.records.open("a", encoding="utf-8") as f:
            for rec in new_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if new_corpus:
        corpus.extend(new_corpus)
        args.corpus.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"OK: records.jsonl total {len(existing_lines) + len(new_records)} | corpus-data.json total {len(corpus)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
