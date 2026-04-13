"""Generate the human-readable ARGOS run report.

The report is the entry point for operators: it summarises which items
succeeded, which need manual intervention, and why.
"""

from __future__ import annotations

import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import manifest, storage

REPORT_PATH = storage.REPO_ROOT / "data" / "raw" / "argos" / "report.md"

STATUS_ORDER = ["success", "partial", "failed", "manual", "tos_restricted", "pending"]


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=storage.REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        return out.stdout.strip() or "(unknown)"
    except OSError:
        return "(unknown)"


def _action_for(entry: dict[str, Any]) -> str:
    """Recommend a next step for manual-intervention items."""

    fc = entry.get("failure_class")
    if fc == "tos_restricted":
        return "Review site TOS; use authorised channel or drop from scope."
    if fc == "robots_denied":
        return "Respect robots.txt; contact archive for research-access programme."
    if fc == "403_block":
        return "Attempt manual download with browser session cookies."
    if fc == "cloudflare":
        return "Cloudflare challenge; requires interactive browser."
    if fc == "playwright_unavailable":
        return "Install playwright + chromium, then re-run ARGOS."
    if fc == "playwright_timeout":
        return "Page load exceeded timeout; retry manually or raise limit."
    if fc == "iiif_not_found":
        return "No IIIF manifest discovered; check archive documentation."
    if fc == "404_not_found":
        return "Source URL moved; locate replacement record."
    if fc == "network":
        return "Transient network failure; retry."
    return "Investigate manually."


def render_report(data: dict[str, Any] | None = None) -> str:
    """Return a Markdown report for the manifest ``data`` (loaded if None)."""

    if data is None:
        data = manifest.load_manifest()

    items: list[dict[str, Any]] = data.get("items", [])
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    status_counts = Counter(entry.get("status", "pending") for entry in items)
    status_counts_sorted = sorted(
        status_counts.items(),
        key=lambda kv: (STATUS_ORDER.index(kv[0]) if kv[0] in STATUS_ORDER else 99),
    )

    per_domain: dict[str, Counter] = defaultdict(Counter)
    for entry in items:
        per_domain[entry.get("source_domain") or "(unknown)"][
            entry.get("status", "pending")
        ] += 1

    failure_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in items:
        if entry.get("status") in {"failed", "manual", "tos_restricted"}:
            fc = entry.get("failure_class") or "unknown"
            failure_buckets[fc].append(entry)

    lines: list[str] = []
    lines.append("# ARGOS — Corpus Acquisition Report")
    lines.append("")
    lines.append(f"- **Generated:** {now}")
    lines.append(f"- **Git commit:** `{_git_sha()}`")
    lines.append(f"- **Storage tier:** `{data.get('storage_tier')}`")
    lines.append(f"- **Storage root:** `{data.get('storage_root')}`")
    lines.append(f"- **Manifest version:** {data.get('manifest_version')}")
    lines.append(f"- **Total items:** {len(items)}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---|")
    for status, count in status_counts_sorted:
        lines.append(f"| `{status}` | {count} |")
    lines.append("")

    # Per-domain table
    lines.append("## Per-domain stats")
    lines.append("")
    header_statuses = [s for s in STATUS_ORDER if any(s in c for c in per_domain.values())]
    lines.append("| Domain | " + " | ".join(header_statuses) + " |")
    lines.append("|---" + "|---" * len(header_statuses) + "|")
    for domain, counts in sorted(per_domain.items(), key=lambda kv: -sum(kv[1].values())):
        row = [domain] + [str(counts.get(s, 0)) for s in header_statuses]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # Failure taxonomy
    if failure_buckets:
        lines.append("## Failure taxonomy")
        lines.append("")
        for fc, entries in sorted(failure_buckets.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"### `{fc}` ({len(entries)})")
            lines.append("")
            for e in entries[:5]:
                reason = e.get("failure_reason") or "(no reason recorded)"
                lines.append(
                    f"- `{e['item_id']}` · {e.get('title', '')[:80]} "
                    f"· [{e.get('source_domain') or '?'}]({e.get('source_url') or '#'}) "
                    f"— {reason}"
                )
            if len(entries) > 5:
                lines.append(f"- _(... {len(entries) - 5} more)_")
            lines.append("")

    # Manual-intervention checklist
    manual_entries = [
        e for e in items if e.get("status") in {"manual", "failed", "tos_restricted"}
    ]
    if manual_entries:
        lines.append("## Manual-intervention checklist")
        lines.append("")
        for e in manual_entries:
            lines.append(
                f"- [ ] `{e['item_id']}` · {e.get('title', '')[:80]} · "
                f"{e.get('source_url') or '(no url)'} — **{_action_for(e)}**"
            )
        lines.append("")

    # Successes summary
    successes = [e for e in items if e.get("status") == "success"]
    if successes:
        lines.append("## Successful acquisitions")
        lines.append("")
        lines.append(f"_{len(successes)} items stored under `{data.get('storage_root')}`_")
        lines.append("")
        for e in successes[:20]:
            size = e.get("bytes")
            size_str = storage.human_bytes(size) if size else "?"
            lines.append(
                f"- `{e['item_id']}` · {e.get('title', '')[:70]} · "
                f"{size_str} · sha256 `{(e.get('sha256') or '')[:12]}…`"
            )
        if len(successes) > 20:
            lines.append(f"- _(... {len(successes) - 20} more)_")
        lines.append("")

    # Next-action suggestions
    lines.append("## Next-action suggestions")
    lines.append("")
    failed_domains = sorted(
        {e.get("source_domain") for e in items if e.get("status") in {"failed", "manual"}},
        key=lambda d: -per_domain[d or "(unknown)"]["failed"]
        if d
        else 0,
    )
    failed_domains = [d for d in failed_domains if d][:5]
    if failed_domains:
        lines.append(
            "- Consider a dedicated protocol adapter for: "
            + ", ".join(f"`{d}`" for d in failed_domains)
        )
    if any(e.get("failure_class") == "playwright_unavailable" for e in items):
        lines.append(
            "- Install Playwright (`pip install playwright && playwright install chromium`) "
            "and re-run to unlock JS-heavy sources."
        )
    if data.get("storage_tier") == "staging":
        lines.append(
            "- Binaries are in gitignored staging. Mount `/Volumes/ICONOCRACIA` and run the "
            "future `argos_migrate_staging_to_ssd.py` helper to promote."
        )
    lines.append("")

    return "\n".join(lines)


def write_report() -> Path:
    """Render and write ``report.md``; return its path."""

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(), encoding="utf-8")
    return REPORT_PATH
