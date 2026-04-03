#!/usr/bin/env python3
"""
iconocracy-ingest — Repeatable ingestion pipeline for scanned archival material.

Sources: Biblioteca Nacional Digital, Câmara dos Deputados, Senado, Internet Archive.
Features:
  - Automatic language detection (PT, ES, FR, IT, EN, DE, LA)
  - Tesseract OCR with per-page confidence scoring
  - Caption and figure-mention extraction
  - Consistent file renaming
  - Master CSV with deduplication (SHA-256)
  - HTML quality report for low-confidence pages
  - Rerunnable: skips already-processed files

Usage:
    python ingest.py /path/to/new/batch/folder
    python ingest.py /path/to/folder --output /custom/output/dir
    python ingest.py /path/to/folder --no-copy          # rename in-place (moves files)
    python ingest.py /path/to/folder --confidence 70     # custom threshold
    python ingest.py /path/to/folder --dry-run           # preview without processing
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tqdm import tqdm

import config
from modules.caption_extractor import (
    CaptionMatch,
    captions_to_text,
    extract_captions_from_pages,
)
from modules.csv_manager import (
    append_record,
    get_processed_hashes,
    load_master_csv,
    save_master_csv,
)
from modules.file_utils import (
    compute_file_hash,
    detect_source,
    discover_files,
    extract_year,
)
from modules.ocr_engine import FileOCRResult, ocr_file
from modules.quality_report import LowConfEntry, generate_quality_report
from modules.renamer import SequenceCounter, rename_file

logger = logging.getLogger("iconocracy-ingest")


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def save_ocr_text(ocr_result: FileOCRResult, output_dir: Path, filename: str) -> Path:
    """Save full OCR text to a .txt file."""
    text_dir = output_dir / config.OCR_TEXT_DIR
    text_dir.mkdir(parents=True, exist_ok=True)
    out_path = text_dir / f"{Path(filename).stem}.txt"
    out_path.write_text(ocr_result.full_text, encoding="utf-8")
    return out_path


def save_captions(
    captions: list[CaptionMatch], output_dir: Path, filename: str
) -> Path:
    """Save extracted captions to a .txt file."""
    cap_dir = output_dir / config.CAPTIONS_DIR
    cap_dir.mkdir(parents=True, exist_ok=True)
    out_path = cap_dir / f"{Path(filename).stem}_captions.txt"
    out_path.write_text(captions_to_text(captions), encoding="utf-8")
    return out_path


def save_run_log(
    output_dir: Path,
    input_dir: Path,
    processed: int,
    skipped: int,
    errors: int,
    duration_s: float,
) -> Path:
    """Save a JSON run log for audit trail."""
    log_dir = output_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"run_{ts}.json"
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "files_processed": processed,
        "files_skipped_duplicate": skipped,
        "files_with_errors": errors,
        "duration_seconds": round(duration_s, 1),
        "confidence_threshold": config.CONFIDENCE_THRESHOLD,
    }
    log_path.write_text(json.dumps(log_data, indent=2, ensure_ascii=False))
    return log_path


def process_file(
    filepath: Path,
    output_dir: Path,
    seq_counter: SequenceCounter,
    copy_files: bool,
) -> tuple[dict, FileOCRResult, list[CaptionMatch], list[LowConfEntry]]:
    """
    Process a single file through the full pipeline:
    1. Detect source institution
    2. Run OCR with language detection
    3. Extract captions
    4. Rename file
    5. Return record dict, OCR result, captions, low-conf entries
    """
    source = detect_source(filepath)
    year = extract_year(filepath)
    file_hash = compute_file_hash(filepath)

    # OCR
    ocr_result = ocr_file(filepath)

    if ocr_result.error:
        logger.warning("OCR error on %s: %s", filepath.name, ocr_result.error)

    # Caption extraction
    pages_data = [
        (p.page_number, p.text) for p in ocr_result.pages
    ]
    captions = extract_captions_from_pages(pages_data)

    # Rename
    seq = seq_counter.next()
    renamed_path = rename_file(
        filepath,
        output_dir / config.RENAMED_DIR,
        seq,
        source=source,
        year=year,
        copy=copy_files,
    )

    # Save OCR text
    save_ocr_text(ocr_result, output_dir, renamed_path.name)

    # Save captions
    save_captions(captions, output_dir, renamed_path.name)

    # Collect low-confidence entries for quality report
    low_entries = []
    for page in ocr_result.pages:
        if page.is_low_confidence:
            low_entries.append(LowConfEntry(
                original_filename=filepath.name,
                renamed_filename=renamed_path.name,
                source_institution=source,
                page_number=page.page_number,
                confidence=page.confidence,
                word_count=page.word_count,
                text_preview=page.text[:200],
            ))

    # Build CSV record
    record = {
        "file_id": file_hash,
        "original_filename": filepath.name,
        "renamed_filename": renamed_path.name,
        "source_institution": source,
        "detected_language": ocr_result.detected_language,
        "ocr_language_used": ocr_result.ocr_language_used,
        "total_pages": ocr_result.total_pages,
        "mean_confidence": ocr_result.mean_confidence,
        "min_confidence": ocr_result.min_confidence,
        "low_conf_pages": ocr_result.low_conf_pages,
        "caption_count": len(captions),
        "has_figures": len(captions) > 0,
        "year_detected": year,
        "input_folder": str(filepath.parent),
        "notes": ocr_result.error or "",
    }

    return record, ocr_result, captions, low_entries


def main():
    parser = argparse.ArgumentParser(
        description="Iconocracy ingest pipeline for scanned archival material.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Folder containing scanned files (PDFs, TIFFs, images).",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help=f"Output directory (default: ./{config.DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Move files instead of copying when renaming.",
    )
    parser.add_argument(
        "--confidence", "-c",
        type=int,
        default=None,
        help=f"Override confidence threshold (default: {config.CONFIDENCE_THRESHOLD}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover files and show what would be processed, without OCR.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging.",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    input_dir = args.input_dir.resolve()
    if not input_dir.is_dir():
        logger.error("Input directory does not exist: %s", input_dir)
        sys.exit(1)

    output_dir = (args.output or Path(config.DEFAULT_OUTPUT_DIR)).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.confidence is not None:
        config.CONFIDENCE_THRESHOLD = args.confidence
        logger.info("Confidence threshold overridden to %d", args.confidence)

    # ── Discovery ────────────────────────────────────────────────────────
    logger.info("Scanning %s for files...", input_dir)
    all_files = discover_files(input_dir)
    logger.info("Found %d supported files.", len(all_files))

    if not all_files:
        logger.warning("No supported files found. Exiting.")
        sys.exit(0)

    # ── Deduplication ────────────────────────────────────────────────────
    master_df = load_master_csv(output_dir)
    existing_hashes = get_processed_hashes(master_df)
    logger.info("Master CSV has %d existing records.", len(existing_hashes))

    # Pre-hash all files for dedup check
    files_to_process = []
    skipped_count = 0
    for f in all_files:
        fhash = compute_file_hash(f)
        if fhash in existing_hashes:
            logger.debug("Skipping duplicate: %s", f.name)
            skipped_count += 1
        else:
            files_to_process.append((f, fhash))

    logger.info(
        "%d new files to process, %d skipped (already in master CSV).",
        len(files_to_process),
        skipped_count,
    )

    if args.dry_run:
        print("\n=== DRY RUN — Files that would be processed ===\n")
        for f, fhash in files_to_process:
            src = detect_source(f)
            yr = extract_year(f) or "????"
            print(f"  [{src}] {yr}  {f.name}")
        print(f"\n  Total: {len(files_to_process)} new, {skipped_count} skipped\n")
        sys.exit(0)

    if not files_to_process:
        logger.info("Nothing new to process. Master CSV is up to date.")
        sys.exit(0)

    # ── Processing ───────────────────────────────────────────────────────
    import time
    start_time = time.time()

    seq_counter = SequenceCounter(output_dir / config.RENAMED_DIR)
    all_low_entries: list[LowConfEntry] = []
    total_pages = 0
    error_count = 0
    copy_files = not args.no_copy

    for filepath, _ in tqdm(files_to_process, desc="Processing files", unit="file"):
        try:
            record, ocr_result, captions, low_entries = process_file(
                filepath, output_dir, seq_counter, copy_files
            )
            master_df = append_record(master_df, **record)
            all_low_entries.extend(low_entries)
            total_pages += ocr_result.total_pages

        except Exception as e:
            logger.error("Failed to process %s: %s", filepath.name, e)
            error_count += 1
            continue

    # ── Save outputs ─────────────────────────────────────────────────────
    csv_path = save_master_csv(master_df, output_dir)

    report_path = generate_quality_report(
        entries=all_low_entries,
        total_files=len(files_to_process),
        total_pages=total_pages,
        skipped_files=skipped_count,
        output_dir=output_dir,
    )

    duration = time.time() - start_time
    log_path = save_run_log(
        output_dir, input_dir,
        processed=len(files_to_process) - error_count,
        skipped=skipped_count,
        errors=error_count,
        duration_s=duration,
    )

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  ICONOCRACY INGEST — Run Complete")
    print("=" * 60)
    print(f"  Files processed:   {len(files_to_process) - error_count}")
    print(f"  Files skipped:     {skipped_count} (duplicates)")
    print(f"  Files with errors: {error_count}")
    print(f"  Total pages OCR'd: {total_pages}")
    print(f"  Low-conf pages:    {len(all_low_entries)}")
    print(f"  Duration:          {duration:.0f}s")
    print(f"  Master CSV:        {csv_path}")
    print(f"  Quality report:    {report_path}")
    print(f"  Run log:           {log_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
