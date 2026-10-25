"""Exercise the real thesis Makefile against disposable build directories."""
import re
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[1]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

@pytest.fixture
def thesis(tmp_path):
    for folder in ('tese/manuscrito', 'vault/tese'):
        dest = tmp_path / folder
        dest.mkdir(parents=True)
        for source in (ROOT / folder).iterdir():
            if source.is_file() and source.suffix in ('.md', '.csl', '.bib', '.yaml') or source.name in ('Makefile', 'template.docx'):
                shutil.copy(source, dest)
    return tmp_path / 'vault/tese'


def make(thesis, *args):
    return subprocess.run(['make', '-C', str(thesis), *args], capture_output=True, text=True)


def paragraphs(path):
    with ZipFile(path) as z:
        doc = ET.fromstring(z.read('word/document.xml'))
    return [''.join(p.itertext()) for p in doc.findall('.//w:p', NS)]


def test_docx_has_only_editorial_numbering(thesis):
    result = make(thesis, 'docx')
    assert result.returncode == 0, result.stdout + result.stderr
    texts = paragraphs(thesis / 'output/tese_completa.docx')
    assert 'CAPÍTULO 4' in texts
    assert '4.6 Metadados e imagem: sensibilidade e limites da recodificação' in texts
    assert not any(re.match(r'^\d+CAPÍTULO', t) for t in texts)
    assert not any('§2.6' in t for t in texts if 'episódio exploratório' in t)
    assert not any('[@' in t for t in texts)
    assert any('MONDZAIN' in t for t in texts)


@pytest.mark.parametrize('target', ['docx', 'pdf', 'capitulo-4.docx', 'capitulo-4.pdf'])
def test_bibliography_required_for_every_build(thesis, target):
    (thesis / 'references.bib').unlink()
    result = make(thesis, target)
    assert result.returncode != 0
    assert 'bibliografia é obrigatória' in result.stderr
    assert not list((thesis / 'output').glob('*'))


def test_single_chapter_uses_canonical_source(thesis):
    # Diverge the mirror deliberately: the compiled text must follow manuscrito.
    (thesis / 'capitulo-4.md').write_text('# MIRROR SENTINEL\n')
    result = make(thesis, 'capitulo-4.docx')
    assert result.returncode == 0, result.stdout + result.stderr
    texts = paragraphs(thesis / 'output/capitulo-4.docx')
    assert 'CAPÍTULO 4' in texts
    assert 'MIRROR SENTINEL' not in texts


def test_default_make_builds_docx(thesis):
    result = make(thesis)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (thesis / 'output/tese_completa.docx').exists()
