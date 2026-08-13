# tests/tools/test_dashboard_data.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "scripts"))

from dashboard_data import derive_year, derive_thumbnail, build_dataset


def test_derive_year_simples():
    assert derive_year("1943") == 1943
    assert derive_year("c. 1560") == 1560
    assert derive_year("1926/1934") == 1926
    assert derive_year("1931-XX-XX") == 1931


def test_derive_year_indisponivel():
    assert derive_year("17th century") is None
    assert derive_year("Unknown") is None
    assert derive_year(None) is None
    assert derive_year("") is None


def test_derive_thumbnail_europeana():
    url = "https://www.europeana.eu/en/item/9200518/ark__12148_btv1b8577655f"
    assert derive_thumbnail(url) is None or derive_thumbnail(url).startswith("http")


def test_derive_thumbnail_gallica_iiif():
    url = "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8577655f/f1/full/512,/0/native.jpg"
    assert derive_thumbnail(url) == url


def test_derive_thumbnail_none_para_desconhecido():
    assert derive_thumbnail(None) is None
    assert derive_thumbnail("") is None


def test_build_dataset_preenche_year_e_preserva_existente():
    items = [
        {"id": "a", "date": "1943", "year": None},
        {"id": "b", "date": "1806", "year": 1806},
    ]
    out = build_dataset(items, {})
    assert out[0]["year"] == 1943
    assert out[1]["year"] == 1806


def test_build_dataset_deriva_thumbnail_via_records_index():
    items = [{"id": "x", "thumbnail_url": None}]
    index = {"x": "https://gallica.bnf.fr/iiif/ark:/12148/abc/f1/full/512,/0/native.jpg"}
    out = build_dataset(items, index)
    assert out[0]["thumbnail_url"].startswith("https://gallica.bnf.fr")
