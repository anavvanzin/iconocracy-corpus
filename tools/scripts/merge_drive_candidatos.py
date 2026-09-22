#!/usr/bin/env python3
"""
Merge Drive candidates (19/05 campaign) into NVMe records.jsonl.

The Drive contains 44 candidates from a search campaign on 2026-05-19
(sq1-4). The NVMe records.jsonl has 265 records but doesn't include these
44 items. This script transforms Drive format → master-record format and
merges them, avoiding duplicates.

Usage:
  python3 tools/scripts/merge_drive_candidatos.py [--dry-run] [--force]
"""

import json
import hashlib
import os
import sys
import uuid
import argparse
from datetime import datetime, timezone

DRIVE_BASE = "/Users/ana/Library/CloudStorage/GoogleDrive-tiacheese@gmail.com/My Drive/adasdsa/iconocracia-2026-05-19"
NVME_RECORDS = os.path.expanduser("~/Research/hub/iconocracy-corpus/data/processed/records.jsonl")
CORPUS_DATA = os.path.expanduser("~/Research/hub/iconocracy-corpus/corpus/corpus-data.json")

# Mapping: Drive fields → Master Record fields
FIELD_MAP = {
    "id": "item_id",
    "title": "input.title_hint",
    "date": "input.date_hint",
    "creator": "input.creator",
    "country": "input.place_hint",
    "url": "input.input_url",
    "url_iiif": "webscout.iiif_source",
    "thumbnail_url": "webscout.thumbnail_url",
    "url_image_download": "webscout.url_image_download",
    "iconclass_codes": "webscout.iconclass_candidates",
    "motif": "webscout.motif",
    "description": "webscout.description",
    "source_archive": "webscout.source_archive",
    "institution": "webscout.institution",
    "medium": "webscout.medium",
    "tags": "webscout.tags",
    "period": "webscout.period",
    "notes": "webscout.notes",
    "confidence": "webscout.confidence",
    "sq": "webscout.search_query",
    "citation_abnt": "exports.abnt_citations",
    "citation_chicago": "exports.chicago_citations",
}


def read_drive_candidates():
    """Read all candidates from Drive sq1-sq4 JSON files."""
    candidates = []
    for f in ["sq1_candidates.json", "sq2_candidates.json", "sq3_candidates.json", "sq4_candidates.json"]:
        fp = os.path.join(DRIVE_BASE, f)
        if os.path.exists(fp):
            with open(fp) as fh:
                data = json.load(fh)
            candidates.extend(data)
    return candidates


def read_nvme_records():
    """Read existing NVMe records."""
    records = []
    with open(NVME_RECORDS) as f:
        for line in f:
            records.append(json.loads(line))
    return records


def drive_to_master_record(drive_item):
    """Transform a Drive candidate into a master-record format."""
    now = datetime.now(timezone.utc).isoformat()
    
    # Generate UUID-style item_id if Drive uses non-UUID format
    raw_id = drive_item.get("id", drive_item.get("item_id", ""))
    try:
        item_uuid = str(uuid.UUID(raw_id))
    except ValueError:
        # Drive uses IDs like "sq1-2026-05-19-schwind-justitia-001"
        # Generate UUID from hash of the ID
        uid = hashlib.sha256(raw_id.encode()).hexdigest()
        item_uuid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
    
    # Build master record
    master = {
        "master_record_version": "1.0",
        "batch_id": f"drive-import-2026-05-19-{raw_id[:10]}",
        "item_id": item_uuid,
        "item_hash": hashlib.sha256(
            json.dumps(drive_item, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest(),
        "input": {
            "input_url": drive_item.get("url", ""),
            "title_hint": drive_item.get("title", ""),
            "date_hint": drive_item.get("date", ""),
            "place_hint": drive_item.get("country", ""),
        },
        "webscout": {
            "search_results": [],  # Drive items don't have search_results
            "iconclass_candidates": drive_item.get("iconclass_codes", []),
            "motif": drive_item.get("motif", []),
            "description": drive_item.get("description", ""),
            "source_archive": drive_item.get("source_archive", ""),
            "institution": drive_item.get("institution", ""),
            "medium": drive_item.get("medium", ""),
            "tags": drive_item.get("tags", []),
            "period": drive_item.get("period", ""),
            "notes": drive_item.get("notes", ""),
            "iiif_source": drive_item.get("url_iiif", ""),
            "thumbnail_url": drive_item.get("thumbnail_url", ""),
            "url_image_download": drive_item.get("url_image_download", ""),
            "confidence": drive_item.get("confidence", None),
            "search_query": drive_item.get("sq", ""),
        },
        "iconocode": {
            "analysis_status": "pending",
            "analysis_date": None,
            "analysis_notes": "Imported from Drive (19/05 campaign). Awaiting iconocode analysis.",
        },
        "purificacao": {},
        "exports": {
            "abnt_citations": drive_item.get("citation_abnt", []),
            "chicago_citations": drive_item.get("citation_chicago", []),
            "audit_flags": ["drive-import-2026-06-04"],
        },
        "timestamps": {
            "created_at": now,
            "updated_at": now,
        },
    }
    
    # Preserve Drive-specific fields in webscout.notes for traceability
    drive_extra = {k: v for k, v in drive_item.items() 
                   if k not in ["id", "title", "date", "creator", "country", "url",
                               "url_iiif", "thumbnail_url", "url_image_download",
                               "iconclass_codes", "motif", "description", "source_archive",
                               "institution", "medium", "tags", "period", "notes",
                               "confidence", "sq", "citation_abnt", "citation_chicago"]}
    if drive_extra:
        master["webscout"]["drive_fields"] = drive_extra
    
    return master


def main():
    parser = argparse.ArgumentParser(description="Merge Drive candidates into NVMe records")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite without backup")
    args = parser.parse_args()
    
    # Read data
    print("Reading Drive candidates...")
    drive_items = read_drive_candidates()
    print(f"  Found {len(drive_items)} candidates")
    
    print("Reading NVMe records...")
    nvme_records = read_nvme_records()
    print(f"  Found {len(nvme_records)} records")
    
    # Check for duplicates (compare by url or title)
    existing_urls = {r.get("input", {}).get("input_url", "") for r in nvme_records}
    existing_titles = {r.get("input", {}).get("title_hint", "") for r in nvme_records}
    
    new_items = []
    duplicates = []
    
    for item in drive_items:
        url = item.get("url", "")
        title = item.get("title", "")
        
        if url in existing_urls:
            duplicates.append(f"  URL: {url[:80]}...")
        elif title in existing_titles:
            duplicates.append(f"  Title: {title[:80]}...")
        else:
            new_items.append(item)
    
    print(f"\nNew items to import: {len(new_items)}")
    print(f"Duplicates found: {len(duplicates)}")
    
    if duplicates:
        print("\nDuplicates:")
        for d in duplicates:
            print(d)
    
    if not new_items:
        print("\nNothing new to import. All Drive candidates already in NVMe.")
        return
    
    if args.dry_run:
        print("\n--- DRY RUN: Would import the following ---")
        for item in new_items:
            title = item.get("title", "?")[:60]
            date = item.get("date", "?")
            country = item.get("country", "?")
            print(f"  {item['id']} — {title} ({date}) — {country}")
        print(f"\nTotal would be: {len(nvme_records) + len(new_items)} records")
        return
    
    # Transform and merge
    print("\nTransforming Drive → Master Record format...")
    master_records = []
    for item in new_items:
        master = drive_to_master_record(item)
        master_records.append(master)
    
    all_records = nvme_records + master_records
    
    # Write atomically
    print(f"Writing {len(all_records)} records to {NVME_RECORDS}...")
    tmp_file = NVME_RECORDS + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    
    # Backup old file
    if not args.force and os.path.exists(NVME_RECORDS):
        backup = NVME_RECORDS + f".backup-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        os.replace(NVME_RECORDS, backup)
        print(f"Backed up old file to: {backup}")
    
    os.replace(tmp_file, NVME_RECORDS)
    print(f"✓ Wrote {len(all_records)} records to {NVME_RECORDS}")
    
    # Update corpus-data.json if needed
    if os.path.exists(CORPUS_DATA):
        print("\nUpdating corpus-data.json...")
        with open(CORPUS_DATA) as f:
            corpus = json.load(f)
        print(f"  Before: {len(corpus)} items")
        
        # Re-generate from records
        import tools.scripts.records_to_corpus as r2c
        # Use the script to regenerate
        os.system(f'cd {os.path.dirname(NVME_RECORDS)} && python tools/scripts/records_to_corpus.py')
        print(f"  ✓ corpus-data.json regenerated")
    
    # Validate
    print("\nValidating...")
    os.system(f'cd {os.path.dirname(NVME_RECORDS)} && python tools/scripts/validate_schemas.py')
    
    # Summary
    print("\n=== Summary ===")
    print(f"Drive candidates: {len(drive_items)}")
    print(f"Already in NVMe: {len(duplicates)}")
    print(f"Newly imported: {len(new_items)}")
    print(f"Total NVMe records: {len(all_records)}")
    
    # Country breakdown
    countries = {}
    for item in new_items:
        c = item.get("country", "Unknown")
        countries[c] = countries.get(c, 0) + 1
    print(f"\nCountries imported:")
    for c, n in sorted(countries.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
