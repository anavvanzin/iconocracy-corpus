from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STATUS_ORDER = ("pending", "success", "partial", "failed", "manual")


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_report_markdown(manifest: dict[str, Any]) -> str:
    items = manifest.get("items", [])
    summary = manifest.get("summary", {})
    domain_counts = _domain_breakdown(items)
    failure_counts = Counter(
        item.get("failure_class", "") for item in items if item.get("failure_class", "")
    )
    manual_items = [item for item in items if item.get("status") == "manual"]
    suggestions = _next_actions(items, failure_counts)

    lines: list[str] = [
        "# ARGOS acquisition report",
        "",
        "## 1. Run metadata",
        f"- Manifest version: {manifest.get('manifest_version', 'unknown')}",
        f"- Generated at: {manifest.get('generated_at', 'unknown')}",
        f"- Storage root: {manifest.get('storage_root', 'unknown')}",
        f"- Storage tier: {manifest.get('storage_tier', 'unknown')}",
        f"- Items covered: {len(items)}",
        "",
        "## 2. Summary counts",
    ]

    for status in STATUS_ORDER:
        lines.append(f"- {status}: {summary.get(status, 0)}")
    if "total_items" in summary:
        lines.insert(lines.index("## 2. Summary counts") + 1, f"- total_items: {summary.get('total_items', len(items))}")

    lines.extend(["", "## 3. Per-domain breakdown"])
    if domain_counts:
        lines.extend(["| Domain | Items | Statuses |", "| --- | ---: | --- |"])
        for domain in sorted(domain_counts):
            row = domain_counts[domain]
            statuses = ", ".join(f"{status}={count}" for status, count in row["statuses"])
            lines.append(f"| {domain} | {row['count']} | {statuses} |")
    else:
        lines.append("- No items in manifest.")

    lines.extend(["", "## 4. Failure taxonomy"])
    if failure_counts:
        lines.extend(["| Failure class | Count |", "| --- | ---: |"])
        for failure_class, count in sorted(failure_counts.items()):
            lines.append(f"| {failure_class} | {count} |")
    else:
        lines.append("- No failures recorded.")

    lines.extend(["", "## 5. Manual-intervention checklist"])
    if manual_items:
        for item in manual_items:
            lines.append(
                "- [ ] {item_id} | {domain} | {failure_class} | {reason} | {url}".format(
                    item_id=item.get("item_id", "unknown"),
                    domain=item.get("source_domain", "unknown"),
                    failure_class=item.get("failure_class", "unspecified"),
                    reason=item.get("failure_reason", "No reason provided"),
                    url=item.get("source_url", ""),
                )
            )
    else:
        lines.append("- No manual-intervention cases.")

    lines.extend(["", "## 6. Next-action suggestions"])
    for suggestion in suggestions:
        lines.append(f"- {suggestion}")

    lines.append("")
    return "\n".join(lines)


def write_report(manifest_path: Path, output_path: Path) -> str:
    manifest = load_manifest(manifest_path)
    markdown = build_report_markdown(manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return markdown


def _domain_breakdown(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    domain_counts: dict[str, dict[str, Any]] = defaultdict(lambda: {"count": 0, "statuses": Counter()})
    for item in items:
        domain = item.get("source_domain", "unknown")
        status = item.get("status", "unknown")
        domain_counts[domain]["count"] += 1
        domain_counts[domain]["statuses"][status] += 1

    normalized: dict[str, dict[str, Any]] = {}
    for domain, values in domain_counts.items():
        statuses = sorted(values["statuses"].items(), key=lambda pair: pair[0])
        normalized[domain] = {"count": values["count"], "statuses": statuses}
    return normalized


def _next_actions(items: list[dict[str, Any]], failure_counts: Counter[str]) -> list[str]:
    suggestions: list[str] = []
    if any(item.get("status") == "manual" for item in items):
        suggestions.append("Prioritize manual retrieval for blocked domains")
    if any(failure_class.endswith("_not_found") or failure_class.endswith("_client_error") for failure_class in failure_counts):
        suggestions.append("Re-check direct URLs returning permanent client errors")
    if any(failure_class.startswith("iiif_") for failure_class in failure_counts):
        suggestions.append("Retry IIIF discovery or image extraction")
    if not suggestions:
        suggestions.append("No immediate follow-up required; monitor pending acquisitions")
    return suggestions
