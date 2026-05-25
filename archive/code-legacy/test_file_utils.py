"""Tests for file_utils module."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.file_utils import (
    compute_file_hash,
    detect_source,
    discover_files,
    extract_year,
    sanitize_stem,
)


def test_compute_file_hash_deterministic():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"test content")
        f.flush()
        h1 = compute_file_hash(Path(f.name))
        h2 = compute_file_hash(Path(f.name))
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex digest


def test_compute_file_hash_differs():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f1:
        f1.write(b"content A")
        f1.flush()
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f2:
            f2.write(b"content B")
            f2.flush()
            assert compute_file_hash(Path(f1.name)) != compute_file_hash(Path(f2.name))


def test_detect_source_bnd():
    assert detect_source(Path("/data/bndigital/doc.pdf")) == "BND"
    assert detect_source(Path("/data/biblioteca nacional/doc.pdf")) == "BND"


def test_detect_source_gallica():
    assert detect_source(Path("/downloads/gallica/image.jpg")) == "GAL"


def test_detect_source_loc():
    assert detect_source(Path("/batch/loc.gov/item.tiff")) == "LOC"


def test_detect_source_unknown():
    assert detect_source(Path("/random/folder/file.pdf")) == "UNKNOWN"


def test_extract_year_from_filename():
    assert extract_year(Path("constituicao_1891.pdf")) == "1891"
    assert extract_year(Path("anais_1934_vol2.tiff")) == "1934"
    assert extract_year(Path("charter_1824_brazil.pdf")) == "1824"


def test_extract_year_no_year():
    assert extract_year(Path("document_without_year.pdf")) is None


def test_extract_year_ignores_non_year_numbers():
    # 1234 is outside 1500-2030 range
    assert extract_year(Path("page1234.pdf")) is None


def test_sanitize_stem_basic():
    assert sanitize_stem("Hello World") == "hello-world"
    assert sanitize_stem("Constituição_Federal") == "constituio-federal"
    assert sanitize_stem("doc  with   spaces") == "doc-with-spaces"


def test_sanitize_stem_special_chars():
    assert sanitize_stem("file (copy).v2") == "file-copyv2"


def test_sanitize_stem_truncates():
    long_name = "a" * 100
    assert len(sanitize_stem(long_name)) == 60


def test_discover_files_finds_pdfs():
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "doc.pdf").write_bytes(b"%PDF")
        (Path(tmpdir) / "image.jpg").write_bytes(b"\xff\xd8")
        (Path(tmpdir) / "notes.txt").write_text("not an image")
        found = discover_files(Path(tmpdir))
        names = {f.name for f in found}
        assert "doc.pdf" in names
        assert "image.jpg" in names
        assert "notes.txt" not in names
