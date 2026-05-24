"""
Master CSV management with deduplication.
Appends new records without duplicating files already processed.
Uses file_id (SHA-256 hash) as the deduplication key.
"""

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

from config import MASTER_CSV_COLUMNS, MASTER_CSV_NAME

logger = logging.getLogger(__name__)


def load_master_csv(output_dir: Path) -> pd.DataFrame:
    """
    Load existing master CSV or create an empty DataFrame with correct columns.
    """
    csv_path = output_dir / MASTER_CSV_NAME
    if csv_path.exists():
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
        # Ensure all expected columns exist (forward compatibility)
        for col in MASTER_CSV_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        return pd.DataFrame(columns=MASTER_CSV_COLUMNS)


def get_processed_hashes(df: pd.DataFrame) -> set[str]:
    """Return set of file_id hashes already in the master CSV."""
    if "file_id" in df.columns:
        return set(df["file_id"].dropna().unique())
    return set()


def append_record(
    df: pd.DataFrame,
    file_id: str,
    original_filename: str,
    renamed_filename: str,
    source_institution: str,
    detected_language: str,
    ocr_language_used: str,
    total_pages: int,
    mean_confidence: float,
    min_confidence: float,
    low_conf_pages: list[int],
    caption_count: int,
    has_figures: bool,
    year_detected: Optional[str],
    input_folder: str,
    notes: str = "",
) -> pd.DataFrame:
    """
    Append a single record to the DataFrame.
    Does NOT write to disk — call save_master_csv for that.
    """
    row = {
        "file_id": file_id,
        "original_filename": original_filename,
        "renamed_filename": renamed_filename,
        "source_institution": source_institution,
        "detected_language": detected_language,
        "ocr_language_used": ocr_language_used,
        "total_pages": str(total_pages),
        "mean_confidence": str(round(mean_confidence, 1)),
        "min_confidence": str(round(min_confidence, 1)),
        "low_conf_pages": ",".join(str(p) for p in low_conf_pages),
        "caption_count": str(caption_count),
        "has_figures": str(has_figures),
        "year_detected": year_detected or "",
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        "input_folder": input_folder,
        "notes": notes,
    }
    new_row = pd.DataFrame([row])
    return pd.concat([df, new_row], ignore_index=True)


def save_master_csv(df: pd.DataFrame, output_dir: Path) -> Path:
    """Write the master CSV to disk. Returns path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / MASTER_CSV_NAME
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_ALL)
    logger.info("Master CSV saved: %s (%d records)", csv_path, len(df))
    return csv_path
