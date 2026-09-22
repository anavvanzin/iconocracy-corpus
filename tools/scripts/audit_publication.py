"""Inventory every canonical record and external projection without promoting data.

Run with --site-root and --out; optional --hf-dir points to a frozen HF download.
Matching reports candidates. It does not certify object identity or visual review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid5
from urllib.parse import urlsplit, urlunsplit

try:
    from .reconcile_data import normalize_title
    from .publication_contract import publication_issues, real_url
except ImportError:
    from reconcile_data import normalize_title
    from publication_contract import publication_issues, real_url

ROOT = Path(__file__).resolve().parents[2]
NS = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def normalize_url(value):
    """Candidate matching only: preserve case-sensitive paths and query strings."""
    if not value:
        return ""
    parsed = urlsplit(value.strip())
    return urlunsplit(("", parsed.netloc.lower().removeprefix("www."),
                       parsed.path.rstrip("/"), parsed.query, ""))


def vault_index(root):
    by_uuid, by_code = defaultdict(list), defaultdict(list)
    for note in sorted((root / "vault/candidatos").rglob("*.md")):
        path = str(note.relative_to(root))
        content = note.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", content, re.S)
        anchor = re.search(r"^records_item_id:\s*[\"']?([0-9a-f-]{36})[\"']?\s*$",
                           frontmatter[1], re.M) if frontmatter else None
        if anchor:
            by_uuid[anchor[1]].append(path)
        by_code[note.name.split(" ", 1)[0]].append(path)
    return by_uuid, by_code


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def source_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state(root):
    def run(*args):
        return subprocess.check_output(["git", "--no-optional-locks", "-C", str(root), *args], text=True).strip()
    return {"commit": run("rev-parse", "HEAD"), "branch": run("branch", "--show-current"),
            "status": run("status", "--porcelain=v1", "-uall").splitlines()}


def identity_candidates(item, records):
    """Never select a first URL collision. Report all corroborated candidates."""
    result = []
    url = normalize_url(item.get("url", ""))
    title = normalize_title(item.get("title", ""))
    for r in records:
        inp = r.get("input", {})
        urls = [inp.get("input_url", "")] + [s.get("url", "") for s in r.get("webscout", {}).get("search_results", [])]
        same_url = bool(url) and any(url == normalize_url(u) for u in urls)
        same_title = bool(title) and title == normalize_title(inp.get("title_hint", ""))
        same_date = bool(item.get("date")) and str(item["date"]) == str(inp.get("date_hint", ""))
        if same_url or same_title:
            result.append({"item_id": r["item_id"], "url": same_url, "title": same_title, "date": same_date,
                           "status": "corroborated_candidate" if same_url and same_title else "candidate"})
    return result


def identity_index(records, mapping, crosswalk):
    """Preserve every assertion; a legacy mapping collision cannot disappear."""
    live = {r["item_id"] for r in records}
    indexes = {"crosswalk": defaultdict(set), "mapping": defaultdict(set)}
    for row in crosswalk:
        indexes["crosswalk"][row["handle"]].add(row["uuid"])
    for row in mapping:
        indexes["mapping"][row["corpus_id"]].add(row["item_id"])
    return live, indexes


def resolve_identifier(identifier, index):
    """Resolve explicit UUID/crosswalk first; report conflicts even when anchored."""
    live, indexes = index
    assertions = {name: sorted(values.get(identifier, set())) for name, values in indexes.items()}
    issues = []
    if any(len(v) > 1 for v in assertions.values()):
        issues.append("identity.alias_collision")
    if assertions["crosswalk"] and assertions["mapping"] and assertions["crosswalk"] != assertions["mapping"]:
        issues.append("identity.crosswalk_mapping_conflict")
    if any(rid not in live for values in assertions.values() for rid in values):
        issues.append("identity.dangling_alias")
    if identifier in live:
        anchor, basis = identifier, "canonical_uuid"
    elif assertions["crosswalk"]:
        values = assertions["crosswalk"]
        anchor = values[0] if len(values) == 1 and values[0] in live else None
        basis = "crosswalk"
    elif assertions["mapping"]:
        values = assertions["mapping"]
        anchor = values[0] if len(values) == 1 and values[0] in live else None
        basis = "mapping"
    else:
        derived = str(uuid5(NS, f"iconocracy-corpus-{identifier}"))
        anchor = derived if derived in live else None
        basis = "derived_uuid"
    return {"item_id": anchor, "basis": basis, "assertions": assertions, "issues": issues}


def build_inventory(root, site_root, hf_dir=None):
    records = read_jsonl(root / "data/processed/records.jsonl")
    corpus = read_json(root / "corpus/corpus-data.json")
    site = read_json(site_root / "site/data/corpus-data-enriched.json")
    mapping = read_json(root / "data/processed/id-mapping.json")["mapping"]
    crosswalk = read_jsonl(root / "data/processed/id_crosswalk.jsonl")
    index = identity_index(records, mapping, crosswalk)
    by_uuid = {r["item_id"]: r for r in records}
    if len(by_uuid) != len(records):
        raise ValueError("Duplicate canonical UUID")
    codes = defaultdict(list)
    identity_issues = defaultdict(set)
    identifier_resolutions = []
    unresolved_export = []
    for c in corpus:
        resolution = resolve_identifier(c["id"], index)
        identifier_resolutions.append({"surface": "export", "id": c["id"], **resolution})
        anchor = resolution["item_id"]
        if anchor in by_uuid:
            codes[anchor].append(c)
            identity_issues[anchor].update(resolution["issues"])
        else:
            unresolved_export.append({"id": c["id"], "candidates": identity_candidates(c, records)})
    site_matches = []
    for s in site:
        resolution = resolve_identifier(s["id"], index)
        site_matches.append({"site_id": s["id"], "title": s["title"],
                             "resolution": resolution, "candidates": identity_candidates(s, records)})
    site_by_uuid = defaultdict(list)
    for s, match in zip(site, site_matches):
        anchor = match["resolution"]["item_id"]
        candidates = ([{"item_id": anchor, "status": "identifier_anchor"}] if anchor
                      else match["candidates"])
        for c in candidates:
            site_by_uuid[c["item_id"]].append((s, c))
            identity_issues[c["item_id"]].update(match["resolution"]["issues"])
    manifest = read_json(root / "data/raw/drive-manifest.json")
    drive = {i["id"]: i for i in manifest.get("items", [])}
    notes_uuid, notes_code = vault_index(root)
    source_owners = defaultdict(list)
    for record in records:
        url = record.get("input", {}).get("input_url", "")
        if real_url(url):
            source_owners[normalize_url(url)].append(record["item_id"])
    hf = {r["item_id"]: r for r in read_jsonl(hf_dir / "records.jsonl")} if hf_dir else {}
    rows = []
    for r in sorted(records, key=lambda r: r["item_id"]):
        rid = r["item_id"]
        exports = codes[rid]
        public_codes = sorted({c["id"] for c in exports if c["id"] != rid}
                              | {c["handle"] for c in crosswalk if c["uuid"] == rid})
        flags = list(identity_issues[rid])
        if not exports:
            flags.append("identity.export_unresolved")
        if len(exports) > 1:
            flags.append("identity.multiple_export_codes")
        url = r.get("input", {}).get("input_url", "")
        if not real_url(url):
            flags.append("source.missing_or_placeholder")
        peers = sorted(set(source_owners[normalize_url(url)]) - {rid})
        if peers:
            flags.append("identity.shared_source_requires_review")
        candidates = site_by_uuid[rid]
        for s, match in candidates:
            if s["id"] not in public_codes:
                flags.append("identity.site_code_differs")
            if match["status"] != "identifier_anchor":
                flags.append("identity.site_requires_disambiguation")
            for field in ("citation_abnt", "rights", "url", "description"):
                if not s.get(field):
                    flags.append(f"site.{field}.missing")
        for c in exports:
            if normalize_title(c.get("title", "")) != normalize_title(r.get("input", {}).get("title_hint", "")):
                flags.append("identity.export_title_conflict")
        drive_rows = [drive[c] for c in public_codes if c in drive]
        anchored_notes = notes_uuid[rid]
        filename_notes = sorted({n for c in public_codes for n in notes_code[c]})
        vault_notes = sorted(set(anchored_notes + filename_notes))
        if not drive_rows:
            flags.append("traceability.manifest_missing")
        if not any(real_url(d.get("drive_url")) for d in drive_rows):
            flags.append("traceability.drive_unverified")
        if not vault_notes:
            flags.append("traceability.vault_missing")
        pur = r.get("purificacao", {}) or {}
        if "pendente" in str(pur.get("notes", "")).lower() or pur.get("coded_by") in ("vault-import", "migration"):
            flags.append("coding.legacy_requires_review")
        if hf_dir and rid not in hf:
            flags.append("hf.record_missing")
        elif hf_dir and hf[rid] != r:
            flags.append("hf.record_differs")
        media = [str((site_root / "site/assets/acervo" / (s["id"] + ".webp")).relative_to(site_root))
                 for s, _ in candidates if (site_root / "site/assets/acervo" / (s["id"] + ".webp")).is_file()]
        rows.append({"item_id": rid, "public_ids": public_codes, "title": r.get("input", {}).get("title_hint", ""),
                     "source_url": url, "source_count": len(r.get("webscout", {}).get("search_results", [])),
                     "site_ids": sorted({s["id"] for s, _ in candidates}), "site_media": sorted(set(media)),
                     "vault_notes": vault_notes, "manifest_ids": [d["id"] for d in drive_rows],
                     "vault_uuid_anchors": anchored_notes, "shared_source_item_ids": peers,
                     "method_version": pur.get("codebook_version"), "review_status": "not_reviewed",
                     "issues": sorted(set(flags)), "publication_blockers": publication_issues(r)})
    return {"summary": {"records": len(records), "export": len(corpus), "site": len(site), "hf": len(hf) if hf_dir else None,
                         "publication_eligible": sum(not r["publication_blockers"] for r in rows),
                         "issues": dict(sorted(Counter(i for r in rows for i in r["issues"]).items()))},
            "records": rows, "site_matches": site_matches, "unresolved_export": unresolved_export,
            "identifier_resolutions": identifier_resolutions,
            "alias_collisions": [{"surface": surface, "id": key, "item_ids": sorted(values)}
                                 for surface, aliases in index[1].items()
                                 for key, values in sorted(aliases.items()) if len(values) > 1],
            "unmatched_site_ids": sorted(s["site_id"] for s in site_matches if not s["candidates"]),
            "hf_only_ids": sorted(set(hf) - set(by_uuid))}


def select_pilot(rows):
    required = ("BR-009", "US-008", "US-017", "BE-004", "BR-007")
    selected = []
    for code in required:
        candidates = [r for r in rows if code in r["public_ids"]]
        if len(candidates) != 1:
            raise ValueError(f"Pilot anchor unresolved: {code}")
        if candidates[0] not in selected:
            selected.append(candidates[0])
        # Columbia's institutional URL currently occurs in two canonical records.
        # Include both for review; a shared URL is not a merge decision.
        if code == "US-017":
            for peer in sorted(candidates[0]["shared_source_item_ids"]):
                row = next(r for r in rows if r["item_id"] == peer)
                if row not in selected:
                    selected.append(row)
    covered = {i for r in selected for i in r["issues"]}
    while len(selected) < min(12, len(rows)):
        remaining = [r for r in rows if r not in selected]
        choice = min(remaining, key=lambda r: (-len(set(r["issues"]) - covered), not bool(r["site_ids"]), r["item_id"]))
        selected.append(choice)
        covered.update(choice["issues"])
    return [{"item_id": r["item_id"], "public_ids": r["public_ids"], "title": r["title"],
             "selection_issues": r["issues"], "review_status": "pending_documentary_and_visual_review"} for r in selected]


def write_audit(root, site_root, out, hf_dir=None, at=None):
    result = build_inventory(root, site_root, hf_dir)
    files = ["data/processed/records.jsonl", "corpus/corpus-data.json", "data/processed/purification.jsonl",
             "data/processed/id-mapping.json", "data/processed/id_crosswalk.jsonl", "data/raw/drive-manifest.json"]
    provenance = {"generated_at": at or datetime.now(timezone.utc).isoformat(), "corpus": git_state(root),
                  "site": git_state(site_root), "sha256": {f: source_digest(root / f) for f in files},
                  "site_source_sha256": source_digest(site_root / "site/data/corpus-data-enriched.json")}
    if hf_dir:
        provenance["hf"] = {"sha256": {p.name: source_digest(p) for p in sorted(hf_dir.iterdir()) if p.is_file()}}
    pilot = select_pilot(result["records"])
    ordered = sorted(result["records"], key=lambda r: (not bool(r["site_ids"]), url_host(r["source_url"]), r["item_id"]))
    batches = [{"batch": i // 20 + 1, "item_ids": [r["item_id"] for r in ordered[i:i + 20]], "status": "not_reviewed"}
               for i in range(0, len(ordered), 20)]
    out.mkdir(parents=True, exist_ok=True)
    for name, payload in (("inventory.json", result), ("provenance.json", provenance), ("pilot.json", pilot), ("batches.json", batches)):
        (out / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (out / "inventory.csv").write_text("item_id,public_ids,site_ids,issue_count,publication_blockers\n" + "".join(
        f"{r['item_id']},{'|'.join(r['public_ids'])},{'|'.join(r['site_ids'])},{len(r['issues'])},{len(r['publication_blockers'])}\n" for r in result["records"]))
    return result


def url_host(url):
    from urllib.parse import urlsplit
    return urlsplit(url).netloc.lower()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--hf-dir", type=Path)
    parser.add_argument("--at")
    args = parser.parse_args()
    result = write_audit(ROOT, args.site_root, args.out, args.hf_dir, args.at)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
