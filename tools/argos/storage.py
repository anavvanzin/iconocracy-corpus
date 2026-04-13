"""Resolve the binary storage root for ARGOS.

SSD-first (per ADR-001); falls back to a gitignored staging directory
when the SSD is not mounted. A later migration helper (out of scope
for the initial implementation) can promote staged binaries to the
SSD once it comes back up.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

SSD_ROOT = Path("/Volumes/ICONOCRACIA/corpus/imagens")
# Repo-relative staging path; resolve_root() returns an absolute Path.
STAGING_RELATIVE = Path("data/raw/.staging")

REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_root() -> tuple[Path, str]:
    """Return ``(root_path, storage_tier)`` — SSD if mounted, else staging."""

    if SSD_ROOT.is_dir():
        return SSD_ROOT, "ssd"
    staging = (REPO_ROOT / STAGING_RELATIVE).resolve()
    staging.mkdir(parents=True, exist_ok=True)
    return staging, "staging"


def country_dir(country: str) -> Path:
    """Return the per-country sub-directory, creating it if needed."""

    root, _tier = resolve_root()
    # Use country code if short; otherwise first 3 letters of name.
    cc = country if country and len(country) <= 3 else (country or "UNK")[:3].upper()
    target = root / cc
    target.mkdir(parents=True, exist_ok=True)
    return target


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 digest of ``path``."""

    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def human_bytes(n: int) -> str:
    """Human-readable byte count for reports."""

    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024  # type: ignore[assignment]
    return f"{n:.1f} TB"


def relpath(path: Path) -> str:
    """Return a repo-relative or /Volumes-absolute string for manifest storage."""

    p = Path(path).resolve()
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)
