#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"


def _pending_items(items: list[dict]) -> list[dict]:
    return [item for item in items if item.get("status") == "pending"]


def _domain_buckets(items: list[dict]) -> list[dict]:
    buckets: dict[str, dict] = {}
    grouped_items: dict[str, list[dict]] = defaultdict(list)

    for item in _pending_items(items):
        domain = item.get("source_domain") or "unknown"
        grouped_items[domain].append(item)

    for domain, domain_items in grouped_items.items():
        item_ids = sorted(str(item.get("item_id")) for item in domain_items if item.get("item_id"))
        protocols = sorted({str(item.get("protocol") or "unknown") for item in domain_items})
        buckets[domain] = {
            "domain": domain,
            "count": len(item_ids),
            "item_ids": item_ids,
            "protocols": protocols,
        }

    return sorted(buckets.values(), key=lambda bucket: (-bucket["count"], bucket["domain"]))


def _standalone_group(bucket: dict) -> dict:
    protocol = bucket["protocols"][0] if len(bucket["protocols"]) == 1 else "mixed"
    return {
        "group_name": bucket["domain"],
        "protocol": protocol,
        "item_ids": bucket["item_ids"],
        "prompt_hint": (
            f"Handle {len(bucket['item_ids'])} pending item(s) from {bucket['domain']} "
            f"using the {protocol} workflow."
        ),
    }


def _longtail_group(buckets: list[dict]) -> dict:
    item_ids = sorted(item_id for bucket in buckets for item_id in bucket["item_ids"])
    protocols = sorted({protocol for bucket in buckets for protocol in bucket["protocols"]})
    domains = sorted(bucket["domain"] for bucket in buckets)
    protocol = protocols[0] if len(protocols) == 1 else "mixed"
    protocol_phrase = ", ".join(protocols)
    domain_phrase = ", ".join(domains)
    return {
        "group_name": "longtail",
        "protocol": protocol,
        "item_ids": item_ids,
        "prompt_hint": (
            "Bundle small or constrained sources into one dispatch group; "
            f"review domains {domain_phrase} and protocols {protocol_phrase}."
        ),
    }


def build_dispatch_groups(items: list[dict], max_groups: int = 6) -> list[dict]:
    if max_groups < 1:
        raise ValueError("max_groups must be at least 1")

    buckets = _domain_buckets(items)
    if not buckets:
        return []

    if len(buckets) <= max_groups:
        return [_standalone_group(bucket) for bucket in buckets]

    longtail_candidates = []
    standalone_candidates = []

    for bucket in buckets:
        protocols = set(bucket["protocols"])
        if "blocked" in protocols or "unknown" in protocols:
            longtail_candidates.append(bucket)
        else:
            standalone_candidates.append(bucket)

    standalone_count = len(standalone_candidates)
    longtail_count = 1 if longtail_candidates else 0
    while standalone_count + longtail_count > max_groups and standalone_candidates:
        smallest_bucket = min(standalone_candidates, key=lambda bucket: (bucket["count"], bucket["domain"]))
        standalone_candidates.remove(smallest_bucket)
        longtail_candidates.append(smallest_bucket)
        longtail_count = 1
        standalone_count = len(standalone_candidates)

    standalone_groups = [_standalone_group(bucket) for bucket in standalone_candidates]
    if not longtail_candidates:
        return standalone_groups[:max_groups]

    return standalone_groups + [_longtail_group(longtail_candidates)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare deterministic ARGOS dispatch groups from a manifest.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH, help="Path to ARGOS manifest.json")
    parser.add_argument("--max-groups", type=int, default=6, help="Maximum number of dispatch groups to emit")
    return parser.parse_args()


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    args = parse_args()
    manifest = _load_json(args.manifest)
    items = manifest.get("items", [])
    groups = build_dispatch_groups(items, max_groups=args.max_groups)
    print(json.dumps(groups, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
