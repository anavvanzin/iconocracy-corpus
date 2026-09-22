# tests/tools/test_refresh_dashboard.py
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "scripts"))

import refresh_dashboard as rd

TEMPLATE = """<html><script>
// == DATA:BEGIN ==
const DATA = [];
const AGENT_RUNS = [];
const META = {{"generated_at": null, "source": null}};
// == DATA:END ==
const CORES = [];
</script></html>"""


def _repo(tmp_path):
    (tmp_path / "corpus").mkdir()
    (tmp_path / "data" / "processed").mkdir(parents=True)
    (tmp_path / "corpus" / "corpus-data.json").write_text(json.dumps([
        {"id": "a", "date": "1943", "year": None, "thumbnail_url": None},
        {"id": "b", "date": None, "year": 1900, "thumbnail_url": "http://x/y.jpg"},
    ]), encoding="utf-8")
    (tmp_path / "corpus" / "agent-runs.json").write_text("[]", encoding="utf-8")
    (tmp_path / "corpus" / "DASHBOARD_CORPUS.html").write_text(TEMPLATE, encoding="utf-8")
    (tmp_path / "data" / "processed" / "records.jsonl").write_text("", encoding="utf-8")
    return tmp_path


def test_embed_entre_delimitadores_e_roundtrip(tmp_path):
    repo = _repo(tmp_path)
    result = rd.refresh_corpus_dashboard(repo)
    assert result["items"] == 2
    html = (repo / "corpus" / "DASHBOARD_CORPUS.html").read_text(encoding="utf-8")
    assert html.count("// == DATA:BEGIN ==") == 1
    for line in html.splitlines():
        if line.startswith("const DATA = "):
            data = json.loads(line[len("const DATA = "):].rstrip().rstrip(";"))
            assert len(data) == 2
            assert data[0]["year"] == 1943  # derivado


def test_idempotente(tmp_path):
    repo = _repo(tmp_path)
    rd.refresh_corpus_dashboard(repo)
    first = (repo / "corpus" / "DASHBOARD_CORPUS.html").read_text(encoding="utf-8")
    rd.refresh_corpus_dashboard(repo)
    second = (repo / "corpus" / "DASHBOARD_CORPUS.html").read_text(encoding="utf-8")
    assert first == second


def test_falha_sem_delimitadores(tmp_path):
    repo = _repo(tmp_path)
    (repo / "corpus" / "DASHBOARD_CORPUS.html").write_text("<html>sem delimitadores</html>", encoding="utf-8")
    try:
        rd.refresh_corpus_dashboard(repo)
        assert False, "deveria falhar"
    except SystemExit:
        pass
