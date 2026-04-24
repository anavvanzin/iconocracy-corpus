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
    manifest_summary = manifest.get("summary", {})
    derived_summary = _derive_summary(items)
    summary_mismatches = _summary_mismatches(manifest_summary, derived_summary)
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
        f"- total_items: {derived_summary['total_items']}",
    ]

    for status in STATUS_ORDER:
        lines.append(f"- {status}: {derived_summary.get(status, 0)}")

    if summary_mismatches:
        lines.extend([
            "",
            "## 2a. Manifest summary warnings",
            "- Warning: manifest summary does not match counts derived from items.",
            "| Metric | Manifest | Derived |",
            "| --- | ---: | ---: |",
        ])
        for key, manifest_value, derived_value in summary_mismatches:
            lines.append(f"| {key} | {manifest_value} | {derived_value} |")

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
                "- [ ] {item_id} | {domain} | {failure_class} | {reason} | {guidance} | {url}".format(
                    item_id=item.get("item_id", "unknown"),
                    domain=item.get("source_domain", "unknown"),
                    failure_class=item.get("failure_class", "unspecified"),
                    reason=item.get("failure_reason", "No reason provided"),
                    guidance=_manual_guidance(item),
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


def _derive_summary(items: list[dict[str, Any]]) -> dict[str, int]:
    status_counts = Counter(item.get("status", "unknown") for item in items)
    summary = {"total_items": len(items)}
    for status in STATUS_ORDER:
        summary[status] = status_counts.get(status, 0)
    return summary


def _summary_mismatches(manifest_summary: dict[str, Any], derived_summary: dict[str, int]) -> list[tuple[str, Any, int]]:
    mismatches: list[tuple[str, Any, int]] = []
    for key, derived_value in derived_summary.items():
        if key in manifest_summary and manifest_summary.get(key) != derived_value:
            mismatches.append((key, manifest_summary.get(key), derived_value))
    return mismatches


def _manual_guidance(item: dict[str, Any]) -> str:
    failure_class = item.get("failure_class", "")
    status = item.get("status", "")

    if failure_class in {"403_block", "manual_required"}:
        return "Open the source URL in a logged-in browser, capture the canonical image, and record provenance notes."
    if failure_class in {"playwright_unavailable", "playwright_empty_capture", "playwright_error"}:
        return "Run the Playwright fallback on a machine with browser dependencies, then verify the captured asset before closing the case."
    if failure_class == "ssl_error":
        return "Verify TLS trust settings or fetch from a trusted network before attempting manual browser capture."
    if failure_class == "unexpected_content_type":
        return "Inspect the landing page for embedded media or alternate download links and document the confirmed asset URL."
    if failure_class == "content_too_small":
        return "Check whether the source exposes a thumbnail placeholder and locate the full-resolution asset manually."
    if failure_class.startswith("iiif_"):
        return "Inspect the IIIF manifest or viewer manually, confirm the image service endpoint, and record the resolved image URL."
    if failure_class.startswith("404") or failure_class.startswith("4xx"):
        return "Confirm whether the record moved or was withdrawn and update the source URL before retrying acquisition."
    if status == "manual":
        return "Review the source manually, retrieve the best available asset, and document the acquisition path."
    return "Review the failure details, retrieve the asset manually if possible, and capture provenance notes."


def _next_actions(items: list[dict[str, Any]], failure_counts: Counter[str]) -> list[str]:
    suggestions: list[str] = []
    manual_failure_classes = {item.get("failure_class", "") for item in items if item.get("status") == "manual"}
    failure_classes = set(failure_counts)

    if {"403_block", "manual_required"} & manual_failure_classes:
        suggestions.append(
            "Prioritize manual browser retrieval for blocked or policy-gated sources and log the operator workflow."
        )
    elif manual_failure_classes:
        suggestions.append(
            "Review manual-queue items and capture provenance notes for each hand-retrieved asset."
        )

    if {"playwright_unavailable", "playwright_empty_capture", "playwright_error"} & failure_classes:
        suggestions.append(
            "Repair or rerun the Playwright fallback environment before retrying browser-dependent captures."
        )
    if "ssl_error" in failure_classes:
        suggestions.append(
            "Resolve TLS or certificate validation problems before issuing additional network retries."
        )
    if "5xx_upstream" in failure_classes:
        suggestions.append(
            "Schedule a later retry window for upstream 5xx failures and avoid treating them as permanent losses."
        )
    if "unexpected_content_type" in failure_classes:
        suggestions.append(
            "Inspect content-type mismatches for HTML landing pages, redirects, or API responses before downloading again."
        )
    if "content_too_small" in failure_classes:
        suggestions.append(
            "Reject undersized captures and locate the full-resolution asset or a higher-fidelity endpoint."
        )
    if any(failure_class.startswith("iiif_") for failure_class in failure_classes):
        suggestions.append(
            "Audit IIIF manifests and image-service URLs before retrying IIIF discovery or extraction."
        )
    if any(
        failure_class.startswith("404")
        or failure_class.startswith("4xx")
        or failure_class.endswith("_not_found")
        or failure_class.endswith("_client_error")
        for failure_class in failure_classes
    ):
        suggestions.append(
            "Re-check direct URLs returning 404/4xx responses; treat them as moved, withdrawn, or mistyped until confirmed otherwise."
        )
    if not suggestions:
        suggestions.append("No immediate follow-up required; monitor pending acquisitions")
    return suggestions
