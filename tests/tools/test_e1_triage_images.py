# tests/tools/test_e1_triage_images.py
"""Tests for e1_triage_images.py — image-source resolution cascade."""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools" / "scripts"))

from e1_triage_images import (
    find_sigla,
    find_local_image,
    extract_vault_thumb,
    build_worklist,
)


def _record(item_id="uuid-1", url="https://ex.org/item1", title="Marianne"):
    return {
        "item_id": item_id,
        "input": {"input_url": url, "title_hint": title,
                  "date_hint": "1880", "place_hint": "France"},
        "webscout": {"search_results": [{"notes": "ver SCOUT-112"}]},
    }


def test_find_sigla_via_corpus_url_map():
    rec = _record()
    url_map = {"https://ex.org/item1": {"id": "FR-013", "url": "https://ex.org/item1"}}
    assert find_sigla(rec, url_map) == "FR-013"


def test_find_sigla_falls_back_to_item_id_prefix():
    rec = _record(item_id="abcdef123456789")
    assert find_sigla(rec, {}) == "abcdef123456"  # 12 chars


def test_find_local_image_matches_sigla_filename(tmp_path):
    (tmp_path / "FR-013.jpg").write_bytes(b"\xff\xd8fake")
    assert find_local_image("FR-013", [tmp_path]) == tmp_path / "FR-013.jpg"


def test_find_local_image_returns_none_when_absent(tmp_path):
    assert find_local_image("XX-999", [tmp_path]) is None


def test_extract_vault_thumb_imagem_pattern(tmp_path):
    note = tmp_path / "FR-013 Declaration.md"
    note.write_text("---\nacervo: BnF\n---\n[imagem](https://img.ex/13.jpg)\n")
    assert extract_vault_thumb("FR-013", tmp_path) == "https://img.ex/13.jpg"


def test_extract_vault_thumb_thumbnail_pattern(tmp_path):
    note = tmp_path / "SCOUT-112 Congo.md"
    note.write_text("---\nthumbnail: https://img.ex/112.png\n---\ncorpo\n")
    assert extract_vault_thumb("SCOUT-112", tmp_path) == "https://img.ex/112.png"


def test_extract_vault_thumb_none_when_no_image(tmp_path):
    note = tmp_path / "BR-001 Republica.md"
    note.write_text("---\nacervo: BN\n---\nsem imagem aqui\n")
    assert extract_vault_thumb("BR-001", tmp_path) is None


def test_build_worklist_local_beats_url(tmp_path):
    (tmp_path / "FR-013.jpg").write_bytes(b"\xff\xd8fake")
    note_dir = tmp_path / "vault"
    note_dir.mkdir()
    (note_dir / "FR-013 X.md").write_text("[imagem](https://img.ex/13.jpg)")
    url_map = {"https://ex.org/item1": {"id": "FR-013"}}
    work, excl = build_worklist(
        [_record()], url_map, [tmp_path], note_dir, head_check=False)
    assert len(work) == 1 and not excl
    assert work[0]["image_source"] == "local"
    assert work[0]["status"] == "pending"


def test_build_worklist_excludes_imageless(tmp_path):
    note_dir = tmp_path / "vault"
    note_dir.mkdir()
    work, excl = build_worklist([_record()], {}, [tmp_path], note_dir,
                                head_check=False)
    assert not work and len(excl) == 1
    assert excl[0]["reason"] == "no_image_source"
