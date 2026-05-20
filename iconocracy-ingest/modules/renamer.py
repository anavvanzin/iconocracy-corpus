"""
Consistent file renaming following the project convention:
    {SOURCE}_{YEAR}_{SEQ:04d}_{sanitized-stem}.{ext}

Examples:
    BND_1891_0001_constituicao-federal.pdf
    CAM_1934_0002_anais-assembleia-constituinte.tiff
    SEN_0000_0003_documento-sem-data.jpg
    IA_1824_0004_charter-of-brazil.pdf
"""

import shutil
from pathlib import Path
from typing import Optional

from config import RENAME_PATTERN
from modules.file_utils import detect_source, extract_year, sanitize_stem


class SequenceCounter:
    """
    Thread-safe(ish) counter that persists across a run.
    Reads the current max sequence from existing renamed files in output_dir.
    """

    def __init__(self, output_dir: Path, source_code: str = ""):
        self._counter = 0
        self._source = source_code
        # Scan existing files to avoid collisions
        if output_dir.exists():
            for f in output_dir.iterdir():
                parts = f.stem.split("_")
                if len(parts) >= 3:
                    try:
                        seq = int(parts[2])
                        if seq > self._counter:
                            self._counter = seq
                    except ValueError:
                        pass

    def next(self) -> int:
        self._counter += 1
        return self._counter

    @property
    def current(self) -> int:
        return self._counter


def build_new_name(
    filepath: Path,
    seq_number: int,
    source: Optional[str] = None,
    year: Optional[str] = None,
) -> str:
    """
    Build the new filename string (without directory).
    """
    if source is None:
        source = detect_source(filepath)
    if year is None:
        year = extract_year(filepath) or "0000"

    stem = sanitize_stem(filepath.stem)
    ext = filepath.suffix.lstrip(".").lower()

    return RENAME_PATTERN.format(
        source=source,
        year=year,
        seq=seq_number,
        stem=stem,
        ext=ext,
    )


def rename_file(
    filepath: Path,
    output_dir: Path,
    seq_number: int,
    source: Optional[str] = None,
    year: Optional[str] = None,
    copy: bool = True,
) -> Path:
    """
    Rename (copy or move) a file to output_dir with the new name.
    Returns the new path.
    """
    new_name = build_new_name(filepath, seq_number, source, year)
    new_path = output_dir / new_name

    output_dir.mkdir(parents=True, exist_ok=True)

    if copy:
        shutil.copy2(str(filepath), str(new_path))
    else:
        shutil.move(str(filepath), str(new_path))

    return new_path
