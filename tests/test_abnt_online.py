"""Pandoc/citeproc regressions for the thesis CSL (requires Pandoc >= 2.11).

Fixtures reproduce PR #234 at 550edfa25093353c6e9636419afc64a1e307ca5e.
Removing either bibliography access call must fail the corresponding tests.
"""

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "vault/tese/abnt.csl"
FIXTURES = ROOT / "tests/fixtures/abnt-online"


def pandoc(*args, source=""):
    result = subprocess.run(
        ["pandoc", *map(str, args)], input=source, text=True,
        capture_output=True, check=True,
    )
    assert not result.stderr, result.stderr
    return result.stdout.strip()


@pytest.fixture(scope="module")
def references():
    return {entry["id"]: entry for entry in json.loads(pandoc(
        "-f", "biblatex", "-t", "csljson", FIXTURES / "references.bib"
    ))}


@pytest.mark.parametrize("key", ["agamben2009", "mondzain2001entretien"])
@pytest.mark.parametrize("locators", [False, True])
@pytest.mark.parametrize("fields", ["both", "url-only", "accessed-only", "neither"])
def test_online_access_preserves_reference_body(references, tmp_path, key, locators, fields):
    entry = dict(references[key])
    assert entry["accessed"]["date-parts"] == [[2026, 10, 6]]
    url = entry["URL"]
    if fields in ("accessed-only", "neither"):
        entry.pop("URL")
    if fields in ("url-only", "neither"):
        entry.pop("accessed")
    if locators:
        entry.update(volume="2", page="14-22")
    bibliography = tmp_path / "references.json"
    bibliography.write_text(json.dumps([entry]), encoding="utf-8")
    actual = pandoc(
        "--citeproc", "--csl", STYLE, "--bibliography", bibliography,
        "--metadata=lang:pt-BR",
        "--wrap=none", "-t", "plain",
        source="---\nnocite: |\n  @" + key + "\n---\n",
    )
    baseline = json.loads((FIXTURES / "offline.json").read_text(encoding="utf-8"))[
        key + ("-locators" if locators else "")
    ]
    access = []
    if fields in ("both", "url-only"):
        access.append(f"Disponível em: <{url}>")
    if fields in ("both", "accessed-only"):
        access.append("Acesso em: 6 out. 2026")
    expected = baseline
    if access:
        expected = baseline.rstrip(". ") + ". " + ". ".join(access) + "."
    assert actual == expected


def test_original_bibtex_entries_render_with_citeproc():
    actual = pandoc(
        FIXTURES / "sample.md", "--citeproc", "--csl", STYLE,
        "--bibliography", FIXTURES / "references.bib",
        "--metadata=lang:pt-BR", "--wrap=none", "-t", "plain",
    )
    assert actual.count("Disponível em:") == 2
    assert actual.count("Acesso em: 6 out. 2026.") == 2
