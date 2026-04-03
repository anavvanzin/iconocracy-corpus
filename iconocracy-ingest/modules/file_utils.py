"""
File discovery, hashing, and deduplication utilities.
"""

import hashlib
import re
from pathlib import Path
from typing import Optional

from config import SUPPORTED_EXTENSIONS, SOURCE_CODES


def compute_file_hash(filepath: Path) -> str:
    """SHA-256 hash of file contents — used as unique file_id."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_files(input_dir: Path) -> list[Path]:
    """
    Recursively find all supported image/PDF files in input_dir.
    Returns sorted list of absolute paths.
    """
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(input_dir.rglob(f"*{ext}"))
        files.extend(input_dir.rglob(f"*{ext.upper()}"))
    # Deduplicate (case-insensitive glob may return dupes on some OS)
    seen = set()
    unique = []
    for f in sorted(files):
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    return unique


def detect_source(filepath: Path) -> str:
    """
    Infer source institution from the file path (folder names, filename).
    Returns canonical code (BND, CAM, SEN, IA) or 'UNKNOWN'.
    """
    path_str = str(filepath).lower()
    for fragment, code in SOURCE_CODES.items():
        if fragment in path_str:
            return code
    return "UNKNOWN"


def extract_year(filepath: Path) -> Optional[str]:
    """
    Try to extract a 4-digit year from the filename.
    Looks for patterns like 1891, 1934, 2024.
    Returns the year string or None.
    """
    stem = filepath.stem
    # Prefer years in the 1500-2030 range; use lookaround for non-digit boundaries
    matches = re.findall(r"(?<!\d)(1[5-9]\d{2}|20[0-3]\d)(?!\d)", stem)
    if matches:
        return matches[0]
    return None


def sanitize_stem(stem: str) -> str:
    """
    Clean a filename stem for consistent naming:
    - lowercase
    - replace spaces/underscores with hyphens
    - remove non-alphanumeric chars (except hyphens)
    - collapse multiple hyphens
    - truncate to 60 chars
    """
    s = stem.lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    return s[:60]
