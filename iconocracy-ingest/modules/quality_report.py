"""
Generate an HTML quality report for low-confidence OCR pages.
Groups by file, highlights worst pages, and provides actionable guidance.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from config import CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


@dataclass
class LowConfEntry:
    """A single low-confidence page entry."""
    original_filename: str
    renamed_filename: str
    source_institution: str
    page_number: int
    confidence: float
    word_count: int
    text_preview: str  # first 200 chars


def generate_quality_report(
    entries: list[LowConfEntry],
    total_files: int,
    total_pages: int,
    skipped_files: int,
    output_dir: Path,
    report_name: str = "quality_report.html",
) -> Path:
    """
    Generate an HTML quality report and save to output_dir.
    Returns the path to the report.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / report_name

    # Group entries by file
    by_file: dict[str, list[LowConfEntry]] = {}
    for e in entries:
        key = e.renamed_filename or e.original_filename
        by_file.setdefault(key, []).append(e)

    affected_files = len(by_file)
    total_low_pages = len(entries)

    # Build HTML
    html_parts = [_header(total_files, total_pages, affected_files,
                          total_low_pages, skipped_files)]

    if not entries:
        html_parts.append(
            '<div class="ok">All pages passed the confidence threshold '
            f'({CONFIDENCE_THRESHOLD}%). No manual review needed.</div>'
        )
    else:
        # Summary table
        html_parts.append(_summary_table(by_file))
        # Detailed entries
        html_parts.append('<h2>Detailed page-level report</h2>')
        for fname, pages in sorted(by_file.items()):
            html_parts.append(_file_detail(fname, pages))

    html_parts.append(_footer())

    report_path.write_text("\n".join(html_parts), encoding="utf-8")
    logger.info("Quality report saved: %s", report_path)
    return report_path


# ── HTML building blocks ─────────────────────────────────────────────────────

def _header(
    total_files: int,
    total_pages: int,
    affected_files: int,
    total_low_pages: int,
    skipped_files: int,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>OCR Quality Report — Iconocracy Ingest</title>
<style>
  body {{ font-family: "Segoe UI", system-ui, sans-serif; max-width: 960px;
         margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; }}
  h1 {{ border-bottom: 3px solid #6b21a8; padding-bottom: .5rem; }}
  h2 {{ color: #6b21a8; margin-top: 2rem; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 1rem; margin: 1.5rem 0; }}
  .stat {{ background: #f8f7ff; border-radius: 8px; padding: 1rem;
           text-align: center; border: 1px solid #e0dff0; }}
  .stat .num {{ font-size: 2rem; font-weight: 700; color: #6b21a8; }}
  .stat .label {{ font-size: .85rem; color: #555; }}
  .ok {{ background: #ecfdf5; border: 1px solid #86efac; border-radius: 8px;
         padding: 1.5rem; margin: 2rem 0; text-align: center;
         font-size: 1.1rem; color: #166534; }}
  table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
  th {{ background: #6b21a8; color: white; padding: .6rem .8rem; text-align: left; }}
  td {{ padding: .5rem .8rem; border-bottom: 1px solid #e5e7eb; }}
  tr:hover {{ background: #f8f7ff; }}
  .badge {{ display: inline-block; padding: .15rem .5rem; border-radius: 4px;
            font-size: .8rem; font-weight: 600; }}
  .badge-poor {{ background: #fee2e2; color: #991b1b; }}
  .badge-fair {{ background: #fef3c7; color: #92400e; }}
  .preview {{ font-size: .8rem; color: #666; max-width: 400px;
              overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .file-block {{ background: #fafafa; border: 1px solid #e5e7eb;
                 border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
  .file-block h3 {{ margin: 0 0 .5rem 0; color: #1a1a2e; font-size: 1rem; }}
  footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;
            font-size: .8rem; color: #888; }}
</style>
</head>
<body>
<h1>OCR Quality Report</h1>
<p>Generated {now} &mdash; confidence threshold: <strong>{CONFIDENCE_THRESHOLD}%</strong></p>

<div class="stats">
  <div class="stat"><div class="num">{total_files}</div><div class="label">Files processed</div></div>
  <div class="stat"><div class="num">{total_pages}</div><div class="label">Total pages</div></div>
  <div class="stat"><div class="num">{affected_files}</div><div class="label">Files with issues</div></div>
  <div class="stat"><div class="num">{total_low_pages}</div><div class="label">Low-confidence pages</div></div>
  <div class="stat"><div class="num">{skipped_files}</div><div class="label">Skipped (duplicates)</div></div>
</div>
"""


def _confidence_badge(conf: float) -> str:
    if conf < 40:
        return f'<span class="badge badge-poor">{conf:.0f}%</span>'
    else:
        return f'<span class="badge badge-fair">{conf:.0f}%</span>'


def _summary_table(by_file: dict[str, list[LowConfEntry]]) -> str:
    rows = []
    for fname, pages in sorted(by_file.items()):
        worst = min(p.confidence for p in pages)
        page_nums = ", ".join(str(p.page_number) for p in pages)
        src = pages[0].source_institution
        rows.append(
            f"<tr><td>{fname}</td><td>{src}</td>"
            f"<td>{len(pages)}</td><td>{_confidence_badge(worst)}</td>"
            f"<td>{page_nums}</td></tr>"
        )
    return (
        "<h2>Summary: files requiring review</h2>"
        "<table><tr><th>File</th><th>Source</th><th>Low pages</th>"
        "<th>Worst</th><th>Page numbers</th></tr>"
        + "\n".join(rows) + "</table>"
    )


def _file_detail(fname: str, pages: list[LowConfEntry]) -> str:
    rows = []
    for p in sorted(pages, key=lambda x: x.page_number):
        preview = p.text_preview.replace("<", "&lt;").replace(">", "&gt;")
        rows.append(
            f"<tr><td>{p.page_number}</td>"
            f"<td>{_confidence_badge(p.confidence)}</td>"
            f"<td>{p.word_count}</td>"
            f'<td class="preview">{preview}</td></tr>'
        )
    return (
        f'<div class="file-block"><h3>{fname}</h3>'
        "<table><tr><th>Page</th><th>Confidence</th><th>Words</th>"
        "<th>Text preview</th></tr>"
        + "\n".join(rows) + "</table></div>"
    )


def _footer() -> str:
    return """
<footer>
  <p><strong>What to do with low-confidence pages:</strong></p>
  <ul>
    <li>Pages below 40%: likely image-only, heavily degraded, or wrong language detection. Check manually.</li>
    <li>Pages 40–60%: partial OCR success. Consider re-scanning at higher DPI or applying manual correction.</li>
    <li>For systematic issues (e.g., all pages from one source are low), check scan quality at the source archive.</li>
  </ul>
  <p>Pipeline: <code>iconocracy-ingest</code> &mdash; Iconocracy Doctoral Research, PPGD/UFSC</p>
</footer>
</body>
</html>"""
