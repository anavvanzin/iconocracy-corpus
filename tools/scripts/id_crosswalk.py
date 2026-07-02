#!/usr/bin/env python3
"""id_crosswalk.py — alias table linking human item handles to machine UUIDs.

The corpus uses several id styles side by side (XX-NNN, descriptive slugs
like BE-CONGO-100F-1912, SCOUT-NNN, raw UUIDs). None of them is "the"
canonical format — handles are stable once minted and never renamed
(exploratory posture: do not force a single pre-established id regime).

This tool maintains data/processed/id_crosswalk.jsonl mapping every known
handle to the records.jsonl item_id (UUID), so any tool can resolve any key.

Entry classes:
    derivable    — uuid5(ns, "iconocracy-corpus-" + handle) matches a
                   records.jsonl item_id (self-verifying; recomputed on build)
    uuid-native  — the corpus id IS the uuid (item has no human handle yet)
    url-matched  — linked to a records.jsonl item by unique normalized-URL
                   match (items that entered records with independent UUIDs)
    assigned     — handle attached later via `alloc` (stored mapping; the only
                   class that requires the crosswalk file as source of truth)

Usage:
    python tools/scripts/id_crosswalk.py build [--dry-run]
    python tools/scripts/id_crosswalk.py status
    python tools/scripts/id_crosswalk.py resolve <key>
    python tools/scripts/id_crosswalk.py alloc <uuid> --handle <HANDLE>
    python tools/scripts/id_crosswalk.py alloc <uuid> --prefix <XX>   # next XX-NNN
"""

import argparse
import json
import re
import sys
import uuid as uuidlib
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_JSONL = REPO_ROOT / "data" / "processed" / "records.jsonl"
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
PURIFICATION_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"
CROSSWALK_JSONL = REPO_ROOT / "data" / "processed" / "id_crosswalk.jsonl"

# Same namespace and prefix as csv_to_records.py::_item_uuid — keep in sync.
_NS = uuidlib.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # uuid.NAMESPACE_URL
_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def derive_uuid(handle):
    """Deterministic uuid for a handle (mirror of csv_to_records._item_uuid)."""
    return str(uuidlib.uuid5(_NS, f"iconocracy-corpus-{handle}"))


def is_uuid(value):
    return bool(_UUID_RE.match(str(value).lower()))


def load_jsonl(path):
    records = []
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records


def load_corpus_items():
    with open(CORPUS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("items", [])
    return [item for item in items if item.get("id")]


def load_corpus_ids():
    return [str(item["id"]) for item in load_corpus_items()]


def load_record_uuids():
    return {rec["item_id"] for rec in load_jsonl(RECORDS_JSONL) if rec.get("item_id")}


def norm_url(url):
    if not url:
        return ""
    return re.sub(r"^https?://(www\.)?", "", str(url).strip().rstrip("/")).lower()


def load_record_url_index():
    """normalized url -> set of item_ids (from input_url + webscout evidence urls)."""
    index = {}
    for rec in load_jsonl(RECORDS_JSONL):
        item_id = rec.get("item_id")
        if not item_id:
            continue
        urls = [rec.get("input", {}).get("input_url")]
        urls += [e.get("url") for e in rec.get("webscout", {}).get("search_results", [])]
        for url in urls:
            key = norm_url(url)
            if key:
                index.setdefault(key, set()).add(item_id)
    return index


def load_crosswalk():
    """Return list of crosswalk entries (may be empty)."""
    return load_jsonl(CROSSWALK_JSONL)


def build_index(entries):
    """handle -> entry and uuid -> [entries]."""
    by_handle = {}
    by_uuid = {}
    for entry in entries:
        by_handle[entry["handle"]] = entry
        by_uuid.setdefault(entry["uuid"], []).append(entry)
    return by_handle, by_uuid


def resolve_key(key, entries=None):
    """Resolve any key (handle or uuid) to (uuid, [entries]). None if unknown."""
    entries = entries if entries is not None else load_crosswalk()
    by_handle, by_uuid = build_index(entries)
    if key in by_handle:
        target = by_handle[key]["uuid"]
        return target, by_uuid.get(target, [])
    if is_uuid(key) and key in by_uuid:
        return key, by_uuid[key]
    return None, []


def cmd_build(dry_run=False):
    record_uuids = load_record_uuids()
    corpus_items = load_corpus_items()
    url_index = load_record_url_index()
    existing = load_crosswalk()
    # Assigned mappings are the only rows whose truth lives in this file — keep them.
    assigned = [e for e in existing if e.get("class") == "assigned"]
    assigned_handles = {e["handle"] for e in assigned}

    now = datetime.now(timezone.utc).isoformat()
    entries = list(assigned)
    unresolved = []

    for item in corpus_items:
        handle = str(item["id"])
        if handle in assigned_handles:
            continue
        if is_uuid(handle):
            if handle in record_uuids:
                entries.append({"handle": handle, "uuid": handle,
                                "class": "uuid-native", "source": "corpus-data.json",
                                "created_at": now})
            else:
                unresolved.append(handle)
            continue
        derived = derive_uuid(handle)
        if derived in record_uuids:
            entries.append({"handle": handle, "uuid": derived,
                            "class": "derivable", "source": "corpus-data.json",
                            "created_at": now})
            continue
        # Fallback: unique URL match (same normalization as reconcile_data.py).
        matches = url_index.get(norm_url(item.get("url")), set())
        if len(matches) == 1:
            entries.append({"handle": handle, "uuid": next(iter(matches)),
                            "class": "url-matched", "source": "corpus-data.json url",
                            "created_at": now})
        elif len(matches) > 1:
            unresolved.append(f"{handle} (URL ambígua: {len(matches)} registros — "
                              f"possível duplicata; resolver com `alloc`)")
        else:
            unresolved.append(f"{handle} (sem match)")

    # Ledger ids that resolve nowhere — surface, never guess.
    by_handle, _ = build_index(entries)
    ledger_ids = {rec["id"] for rec in load_jsonl(PURIFICATION_JSONL) if rec.get("id")}
    ledger_orphans = sorted(
        lid for lid in ledger_ids
        if lid not in by_handle and not (is_uuid(lid) and lid in record_uuids)
    )

    print(f"  records.jsonl uuids:   {len(record_uuids)}")
    print(f"  corpus-data ids:       {len(corpus_items)}")
    print(f"  crosswalk entries:     {len(entries)} "
          f"(derivable={sum(1 for e in entries if e['class'] == 'derivable')}, "
          f"uuid-native={sum(1 for e in entries if e['class'] == 'uuid-native')}, "
          f"url-matched={sum(1 for e in entries if e['class'] == 'url-matched')}, "
          f"assigned={len(assigned)})")
    if unresolved:
        print(f"  ⚠ unresolved corpus ids ({len(unresolved)}):")
        for handle in unresolved[:10]:
            print(f"      {handle}")
        if len(unresolved) > 10:
            print(f"      … and {len(unresolved) - 10} more")
    if ledger_orphans:
        print(f"  ⚠ purification.jsonl ids without crosswalk/uuid ({len(ledger_orphans)}):")
        for lid in ledger_orphans[:10]:
            print(f"      {lid}")
        if len(ledger_orphans) > 10:
            print(f"      … and {len(ledger_orphans) - 10} more")

    if dry_run:
        print("  (dry-run: nothing written)")
        return entries

    CROSSWALK_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CROSSWALK_JSONL, "w", encoding="utf-8") as f:
        for entry in sorted(entries, key=lambda e: e["handle"]):
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  ✅ wrote {CROSSWALK_JSONL}")
    return entries


def cmd_status():
    entries = load_crosswalk()
    if not entries:
        print("  crosswalk empty — run `build` first")
        return 1
    by_class = {}
    for entry in entries:
        by_class.setdefault(entry["class"], 0)
        by_class[entry["class"]] += 1
    print(f"  entries: {len(entries)}")
    for cls in sorted(by_class):
        print(f"    {cls:12s} {by_class[cls]}")

    # Integrity: duplicate handles; derivable rows must recompute correctly.
    seen, dupes, bad_derive = set(), [], []
    for entry in entries:
        if entry["handle"] in seen:
            dupes.append(entry["handle"])
        seen.add(entry["handle"])
        if entry["class"] == "derivable" and derive_uuid(entry["handle"]) != entry["uuid"]:
            bad_derive.append(entry["handle"])
    if dupes:
        print(f"  ✗ duplicate handles: {dupes[:5]}")
    if bad_derive:
        print(f"  ✗ derivable rows failing uuid5 recompute: {bad_derive[:5]}")
    if not dupes and not bad_derive:
        print("  ✓ integrity: handles unique, derivable rows verified")
    return 1 if (dupes or bad_derive) else 0


def cmd_resolve(key):
    target, entries = resolve_key(key)
    if target is None:
        print(f"  ✗ '{key}' not found in crosswalk (or records.jsonl)")
        return 1
    print(f"  uuid: {target}")
    for entry in entries:
        print(f"  handle: {entry['handle']}  [{entry['class']}]")
    return 0


def next_prefixed_handle(prefix, handles):
    """Next XX-NNN for a prefix, considering only strict XX-NNN handles."""
    numbers = [int(m.group(1)) for h in handles
               if (m := re.match(rf"^{re.escape(prefix)}-(\d{{3}})$", h))]
    return f"{prefix}-{(max(numbers) + 1) if numbers else 1:03d}"


def cmd_alloc(uuid_key, handle=None, prefix=None):
    if not is_uuid(uuid_key):
        print(f"  ✗ '{uuid_key}' is not a uuid")
        return 1
    record_uuids = load_record_uuids()
    if uuid_key not in record_uuids:
        print(f"  ✗ uuid not present in records.jsonl — refuse to alias unknown item")
        return 1
    entries = load_crosswalk()
    by_handle, by_uuid = build_index(entries)

    if handle is None:
        all_handles = set(by_handle) | set(load_corpus_ids())
        handle = next_prefixed_handle(prefix, all_handles)
    if handle in by_handle or handle in set(load_corpus_ids()):
        print(f"  ✗ handle '{handle}' already in use")
        return 1
    existing_human = [e for e in by_uuid.get(uuid_key, []) if e["class"] != "uuid-native"]
    if existing_human:
        print(f"  ⚠ uuid already has handle(s): {[e['handle'] for e in existing_human]} — adding alias anyway")

    entry = {"handle": handle, "uuid": uuid_key, "class": "assigned",
             "source": "id_crosswalk.py alloc",
             "created_at": datetime.now(timezone.utc).isoformat()}
    CROSSWALK_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(CROSSWALK_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  ✅ {handle} → {uuid_key} [assigned]")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="rebuild crosswalk from records/corpus (keeps assigned rows)")
    p_build.add_argument("--dry-run", action="store_true")

    sub.add_parser("status", help="counts + integrity check")

    p_resolve = sub.add_parser("resolve", help="resolve a handle or uuid")
    p_resolve.add_argument("key")

    p_alloc = sub.add_parser("alloc", help="attach a human handle to a uuid (on demand)")
    p_alloc.add_argument("uuid")
    group = p_alloc.add_mutually_exclusive_group(required=True)
    group.add_argument("--handle", help="explicit handle (any stable format)")
    group.add_argument("--prefix", help="allocate next NNN under this prefix (e.g. BR)")

    args = parser.parse_args()
    if args.cmd == "build":
        cmd_build(dry_run=args.dry_run)
        return
    if args.cmd == "status":
        sys.exit(cmd_status())
    if args.cmd == "resolve":
        sys.exit(cmd_resolve(args.key))
    if args.cmd == "alloc":
        sys.exit(cmd_alloc(args.uuid, handle=args.handle, prefix=args.prefix))


if __name__ == "__main__":
    main()
