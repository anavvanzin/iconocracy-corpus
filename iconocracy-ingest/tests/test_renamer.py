"""Tests for renamer module."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.renamer import SequenceCounter, build_new_name, rename_file


def test_build_new_name_basic():
    name = build_new_name(
        Path("constituicao_1891.pdf"),
        seq_number=1,
        source="BND",
        year="1891",
    )
    assert name == "BND_1891_0001_constituicao-1891.pdf"


def test_build_new_name_no_year():
    name = build_new_name(
        Path("mystery_document.tiff"),
        seq_number=42,
        source="UNKNOWN",
        year=None,
    )
    assert "0000" in name
    assert "0042" in name
    assert name.endswith(".tiff")


def test_build_new_name_preserves_extension():
    name = build_new_name(Path("image.JP2"), seq_number=1, source="GAL", year="1850")
    assert name.endswith(".jp2")


def test_sequence_counter_starts_at_1():
    with tempfile.TemporaryDirectory() as tmpdir:
        counter = SequenceCounter(Path(tmpdir))
        assert counter.next() == 1
        assert counter.next() == 2


def test_sequence_counter_reads_existing():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir)
        (d / "BND_1891_0005_doc.pdf").write_bytes(b"")
        (d / "CAM_1934_0003_other.tiff").write_bytes(b"")
        counter = SequenceCounter(d)
        assert counter.next() == 6  # max(5, 3) + 1


def test_rename_file_copy():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "original.pdf"
        src.write_bytes(b"%PDF-fake")
        out_dir = Path(tmpdir) / "renamed"
        result = rename_file(src, out_dir, seq_number=1, source="BND", year="1891", copy=True)
        assert result.exists()
        assert src.exists()  # original preserved


def test_rename_file_move():
    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "original.pdf"
        src.write_bytes(b"%PDF-fake")
        out_dir = Path(tmpdir) / "renamed"
        result = rename_file(src, out_dir, seq_number=1, source="BND", year="1891", copy=False)
        assert result.exists()
        assert not src.exists()  # original moved
