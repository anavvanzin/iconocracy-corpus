"""Publication eligibility. Structural checks never claim scholarly review."""
from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from datetime import datetime
from urllib.parse import urlsplit
from uuid import UUID

CONTRACT_VERSION = "1.0.0"
REQUIRED_FACTS = ("title", "creator", "date", "country", "type", "institution", "context")


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(value):
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def review_digest(record):
    """Bind a review to its actual content; timestamps/status cannot certify changes."""
    publication = record.get("publication", {})
    return sha256({
        "record": {key: record.get(key) for key in
                   ("item_id", "input", "webscout", "iconocode", "purificacao")},
        "publication": {key: value for key, value in publication.items()
                        if key not in ("review", "editorialStatus", "history")},
    })


def real_url(value):
    if not isinstance(value, str):
        return False
    try:
        url = urlsplit(value)
    except ValueError:
        return False
    return (url.scheme in ("https", "http") and bool(url.hostname)
            and not any(word in value.lower() for word in
                        ("placeholder", "example.", "iconocracy.corpus", ".local/")))


def iso_datetime(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except (ValueError, AttributeError, TypeError):
        return False


@lru_cache(maxsize=1)
def publication_validator():
    from jsonschema import Draft202012Validator, FormatChecker
    schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/publication.schema.json").read_text())
    return Draft202012Validator(schema, format_checker=FormatChecker())


def publication_issues(record):
    """Return all blockers. Legacy records are retained but never auto-published."""
    p = record.get("publication") or {}
    structural = list(publication_validator().iter_errors(p))
    if structural:
        return sorted({"publication.schema:" + "/".join(map(str, e.absolute_path)) for e in structural})
    issues = []
    try:
        UUID(record["item_id"])
    except (ValueError, KeyError, TypeError):
        issues.append("identity.invalid_uuid")
    if p.get("contract_version") != CONTRACT_VERSION:
        issues.append("publication.contract_missing")
    if p.get("editorialStatus") != "published":
        issues.append("publication.not_approved")
    if p.get("identity_status") != "confirmed":
        issues.append("identity.not_confirmed")
    if not p.get("entity_type"):
        issues.append("identity.entity_type_missing")
    if not p.get("method_version"):
        issues.append("review.method_version_missing")
    if not p.get("public_id"):
        issues.append("identity.public_id_missing")
    evidence = p.get("evidence") or []
    evidence_ids = [e.get("id") for e in evidence]
    valid_sources = {e.get("id") for e in evidence
                     if e.get("id") and real_url(e.get("url"))
                     and iso_datetime(e.get("accessed_at"))
                     and e.get("citation") and e.get("locator")}
    if len(evidence_ids) != len(set(evidence_ids)):
        issues.append("evidence.duplicate_id")
    if not valid_sources:
        issues.append("evidence.no_consulted_source")
    if len(valid_sources) != len(evidence):
        issues.append("evidence.invalid_source")
    if p.get("primary_source_id") not in valid_sources:
        issues.append("evidence.primary_source_missing")
    for linked in p.get("aliases", []) + p.get("relations", []) + p.get("history", []):
        if not set(linked["source_ids"]) <= valid_sources:
            issues.append("identity_or_history.unsubstantiated")
    facts = p.get("catalog") or {}
    for field in REQUIRED_FACTS:
        fact = facts.get(field) or {}
        value = str(fact.get("value") or "").strip()
        if not value or value.lower() in ("unknown", "n/a", "tbd", "todo", "(sem título)"):
            issues.append(f"catalog.{field}.missing")
        if not fact.get("source_ids") or not set(fact["source_ids"]) <= valid_sources:
            issues.append(f"catalog.{field}.unsubstantiated")
        if fact.get("status") not in ("documented", "unknown", "approximate"):
            issues.append(f"catalog.{field}.unreviewed")
        if fact.get("status") in ("unknown", "approximate") and not fact.get("justification"):
            issues.append(f"catalog.{field}.unjustified_uncertainty")
    media = p.get("media") or {}
    kind = p.get("kind")
    if kind not in ("visual", "textual"):
        issues.append("media.kind_missing")
    if media.get("examined") is not True or not media.get("source_ids") or not set(media["source_ids"]) <= valid_sources:
        issues.append("media.not_examined")
    if not media.get("locator") or not media.get("credit"):
        issues.append("media.locator_or_credit_missing")
    if kind == "visual":
        if not real_url(media.get("url")) or not re.fullmatch(r"[0-9a-f]{64}", media.get("sha256", "")):
            issues.append("media.reproduction_missing")
        if media.get("sufficient_resolution") is not True:
            issues.append("media.insufficient_resolution")
    rights = p.get("rights") or {}
    if (not rights.get("statement") or rights.get("display_permitted") is not True
            or not rights.get("source_ids") or not set(rights["source_ids"]) <= valid_sources):
        issues.append("rights.unresolved")
    if not p.get("description"):
        issues.append("description.missing")
    for claim in p.get("interpretations", []):
        if not claim.get("text") or not claim.get("source_ids") or not set(claim["source_ids"]) <= valid_sources:
            issues.append("interpretation.unsubstantiated")
    review = p.get("review") or {}
    if not review.get("reviewer") or not iso_datetime(review.get("reviewed_at")):
        issues.append("review.missing")
    if review.get("content_sha256") != review_digest(record):
        issues.append("review.stale_or_missing_digest")
    if p.get("blockers"):
        issues.append("review.open_blockers")
    return sorted(set(issues))


def reviewed_export(record):
    """The public projection uses reviewed canonical facts, never a website fallback."""
    issues = publication_issues(record)
    if issues:
        raise ValueError(f"{record.get('item_id')}: {', '.join(issues)}")
    p = record["publication"]
    primary = next(e for e in p["evidence"] if e["id"] == p["primary_source_id"])
    facts = {key: value["value"] for key, value in p["catalog"].items()}
    return {
        "item_id": record["item_id"], "id": p["public_id"],
        "title": facts["title"], "creator": facts["creator"], "date": facts["date"],
        "country": facts["country"], "medium": facts["type"], "institution": facts["institution"],
        "context": facts["context"], "description": p["description"],
        "url": primary["url"], "citation_abnt": primary["citation"],
        "rights": p["rights"]["statement"], "thumbnail_url": p["media"].get("url", ""),
        "regime": p.get("regime", ""), "editorialStatus": "published",
        "publication": p,
    }


def validate_aliases(records):
    owners = {}
    for record in records:
        p = record.get("publication", {})
        for alias in p.get("aliases", []):
            key = (alias["surface"], alias["id"])
            if key in owners and owners[key] != record["item_id"]:
                raise ValueError(f"Ambiguous alias: {key}")
            owners[key] = record["item_id"]
    return owners


def publication_snapshot(records):
    """Create a deterministic reviewed projection and a separate private audit.

    This is a shared input for site/HF adapters, not a deployable HF release.
    Separate purification reviews and publication adapters remain required.
    """
    from copy import deepcopy

    rows = sorted(deepcopy(records), key=lambda row: row["item_id"])
    ids = [row["item_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical item_id")
    for rid in ids:
        if str(UUID(rid)) != rid:
            raise ValueError("Non-canonical UUID: " + rid)

    eligible, withheld = [], []
    for row in rows:
        issues = publication_issues(row)
        if issues:
            withheld.append({"item_id": row["item_id"], "issues": issues})
        else:
            eligible.append(row)

    # Check claims from structurally valid unpublished rows too: withholding a
    # rival claimant cannot silently resolve an identity conflict.
    valid_rows = [row for row in rows if not list(
        publication_validator().iter_errors(row.get("publication") or {}))]
    aliases = validate_aliases(valid_rows)
    public_ids = {}
    for row in valid_rows:
        code = row["publication"].get("public_id")
        if code:
            previous = public_ids.setdefault(code, row["item_id"])
            if previous != row["item_id"]:
                raise ValueError("Ambiguous public_id: " + code)
            owner = aliases.get(("site", code))
            if owner is not None and owner != row["item_id"]:
                raise ValueError("Public ID shadows site alias: " + code)

    eligible_ids = {row["item_id"] for row in eligible}
    corpus = [reviewed_export(row) for row in eligible]
    payload = {
        "contract_version": CONTRACT_VERSION,
        "corpus": corpus,
        "records": eligible,
        "aliases": [{"surface": surface, "id": alias, "item_id": owner}
                    for (surface, alias), owner in sorted(aliases.items())
                    if owner in eligible_ids],
    }
    snapshot = {
        "snapshot_id": sha256(payload),
        "counts": {"corpus": len(corpus), "records": len(eligible)},
        **payload,
    }
    audit = {
        "input_sha256": sha256(rows), "snapshot_id": snapshot["snapshot_id"],
        "counts": {"input": len(rows), "eligible": len(eligible), "withheld": len(withheld)},
        "withheld": withheld,
        "release_ready": False,
        "pending": ["site_adapter", "hf_adapter", "purification_review_and_identity"],
    }
    return snapshot, audit


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build local reviewed snapshot; never publishes.")
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    records = [json.loads(line) for line in args.records.read_text().splitlines() if line.strip()]
    snapshot, audit = publication_snapshot(records)
    # Refuse reuse so stale public files cannot survive a rebuild.
    args.out.mkdir(parents=True, exist_ok=False)
    for name, value in (("snapshot.json", snapshot), ("audit-private.json", audit)):
        (args.out / name).write_text(canonical_json(value) + "\n", encoding="utf-8")
    print(canonical_json({"snapshot_id": snapshot["snapshot_id"], **audit["counts"], "release_ready": False}))
