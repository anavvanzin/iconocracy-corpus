# Dashboard do Corpus v2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reestruturar `corpus/DASHBOARD_CORPUS.html` em 4 abas analíticas (Visão Geral · Explorar · Endurecimento · Qualidade) e endurecer o gerador `tools/scripts/refresh_dashboard.py`, conforme spec `docs/superpowers/specs/2026-08-12-dashboard-corpus-design.md`.

**Architecture:** HTML único autocontido (sem servidor, sem build) + gerador Python idempotente que embute dados via delimitadores `// == DATA:BEGIN/END ==`. O dashboard atual já contém todas as visualizações-base (overview, regime, purification, temporal, distribution, gallery, table) — o trabalho é reorganizá-las nas 4 abas, criar a aba Qualidade e enriquecer os dados embutidos (ano derivado + thumbnails).

**Tech Stack:** Python 3.11 (conda env `iconocracy`), pytest (raiz do repo, sem config), HTML/JS vanilla + Chart.js 4.5.1 via CDN.

## Global Constraints

- Repo: `/Users/ana/Research/hub/iconocracy-corpus`; trabalhar em branch novo a partir de `origin/main`, finalizar com PR + merge (convenção do repo).
- `python` = conda env `iconocracy` (`conda activate iconocracy`).
- pytest roda da raiz do repo: `pytest tests/ -x -q`.
- **Não** editar `corpus/DASHBOARD_CORPUS.html` para inserir dados manualmente — dados só via gerador.
- Sem base64 de imagens; thumbnails só por URL externa derivada.
- Estética preservada: design tokens CSS existentes (`--cream`, `--beige`, `--sidebar`, `--brown`, `--dark`, `--red`, Pixelify Sans + Inter + JetBrains Mono).
- Idioma da UI: pt-BR. Identificadores de código em inglês.
- O bloco "Modo Foco" (pomodoro/to-do/word-count/milestones, `sec-foco` + classe `foco`) é ferramenta pessoal da autora: **preservar intacto** como 5ª aba, fora das 4 do spec.
- Tamanho final do HTML < 1,5 MB.

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `tools/scripts/dashboard_data.py` (novo) | Derivações puras: ano, thumbnail, montagem do dataset embutido |
| `tools/scripts/refresh_dashboard.py` (reescrito) | Orquestra: lê fontes, embute nos delimitadores, valida round-trip |
| `corpus/DASHBOARD_CORPUS.html` (modificado) | Template: delimitadores + navegação 4 abas + aba Qualidade |
| `tests/tools/test_dashboard_data.py` (novo) | Testes das derivações |
| `tests/tools/test_refresh_dashboard.py` (novo) | Testes do gerador (tmp_path, idempotência, round-trip) |

## Contratos entre arquivos

- `dashboard_data.derive_year(date: str|None) -> int|None` — primeiro ano 1400–2099 em `date`.
- `dashboard_data.derive_thumbnail(input_url: str|None) -> str|None` — URL de thumbnail derivável ou `None`.
- `dashboard_data.build_dataset(corpus_items: list[dict], records_index: dict[str, str]) -> list[dict]` — itens de `corpus-data.json` com `year` preenchido (derivado quando nulo) e `thumbnail_url` preenchido (derivado quando nulo). `records_index` mapeia `item_id → input_url`.
- `refresh_dashboard.refresh_corpus_dashboard(repo_root: Path) -> dict` — retorna `{"items": N, "bytes": M}`; falha com `SystemExit(1)` se delimitadores ausentes/duplicados ou se round-trip divergir.
- No HTML: `const DATA = [...]`, `const AGENT_RUNS = [...]` e `const META = {...}` vivem entre `// == DATA:BEGIN ==` e `// == DATA:END ==` (nessa ordem). O JS consome `DATA`, `AGENT_RUNS`, `META` como globais.

---

### Task 1: Módulo de derivações `dashboard_data.py`

**Files:**
- Create: `tools/scripts/dashboard_data.py`
- Test: `tests/tools/test_dashboard_data.py`

**Interfaces:**
- Consumes: `corpus/corpus-data.json` (lista de 335 dicts), `data/processed/records.jsonl` (campo `input.input_url`, chave `item_id`).
- Produces: `derive_year`, `derive_thumbnail`, `build_dataset` (assinaturas no contrato acima). Task 2 depende destas três.

- [ ] **Step 1: Escrever o teste que falha**

```python
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
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `cd /Users/ana/Research/hub/iconocracy-corpus && conda activate iconocracy && pytest tests/tools/test_dashboard_data.py -v`
Expected: FAIL (`ModuleNotFoundError: dashboard_data`)

- [ ] **Step 3: Implementar**

```python
# tools/scripts/dashboard_data.py
"""Derivações puras para o dataset embutido do dashboard (spec 2026-08-12)."""
import json
import re

YEAR_RE = re.compile(r"(1[4-9]\d{2}|20\d{2})")


def derive_year(date):
    """Primeiro ano 1400–2099 no campo date (texto livre); None se não houver."""
    if not date:
        return None
    m = YEAR_RE.search(str(date))
    return int(m.group(1)) if m else None


def derive_thumbnail(input_url):
    """URL de thumbnail derivável de uma input_url conhecida; None caso contrário.

    Regras (conservadoras — só padrões verificados no corpus):
    - URLs que já são IIIF de imagem (Gallica /iiif/ ... native.jpg) passam direto.
    - Demais domínios (Europeana item pages, Numista, BN etc.) não têm
      thumbnail derivável deterministicamente: retorna None (placeholder no front).
    """
    if not input_url or not isinstance(input_url, str):
        return None
    u = input_url.strip()
    if not u.startswith("http"):
        return None
    if "/iiif/" in u and u.lower().endswith((".jpg", ".jpeg", ".png")):
        return u
    return None


def load_records_index(records_path):
    """Lê records.jsonl e retorna dict item_id -> input.input_url."""
    index = {}
    with open(records_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            item_id = rec.get("item_id")
            input_url = (rec.get("input") or {}).get("input_url")
            if item_id and input_url:
                index[item_id] = input_url
    return index


def build_dataset(corpus_items, records_index):
    """Enriquece itens do export público: deriva year e thumbnail_url quando nulos."""
    out = []
    for item in corpus_items:
        it = dict(item)
        if it.get("year") is None:
            it["year"] = derive_year(it.get("date"))
        if not it.get("thumbnail_url"):
            it["thumbnail_url"] = derive_thumbnail(records_index.get(it.get("id")))
        out.append(it)
    return out
```

- [ ] **Step 4: Rodar e ver passar**

Run: `pytest tests/tools/test_dashboard_data.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add tools/scripts/dashboard_data.py tests/tools/test_dashboard_data.py
git commit -m "feat(dashboard): módulo de derivações (ano, thumbnail, dataset)"
```

---

### Task 2: Gerador endurecido com delimitadores e round-trip

**Files:**
- Modify: `tools/scripts/refresh_dashboard.py` (reescrita das funções de embed; manter CLI `--corpus/--agents`)
- Modify: `corpus/DASHBOARD_CORPUS.html` — apenas o bloco de dados (inserir delimitadores + `AGENT_RUNS` + `META`)
- Test: `tests/tools/test_refresh_dashboard.py`

**Interfaces:**
- Consumes: `dashboard_data.build_dataset`, `dashboard_data.load_records_index` (Task 1).
- Produces: `refresh_corpus_dashboard(repo_root) -> dict`; globais no HTML: `DATA`, `AGENT_RUNS`, `META` entre `// == DATA:BEGIN ==` / `// == DATA:END ==`. Tasks 3–4 assumem esses globais.

- [ ] **Step 1: Inserir delimitadores no HTML**

No `corpus/DASHBOARD_CORPUS.html`, substituir a linha única `const DATA = [...];` (linha que começa com `const DATA = `) por:

```html
<script>
// == DATA:BEGIN ==
const DATA = [];
const AGENT_RUNS = [];
const META = {"generated_at": null, "source": null};
// == DATA:END ==
```

(manter o restante do `<script>` intacto — `CORES`, `REGIME_COLORS`, classe `Dashboard` etc.)

- [ ] **Step 2: Escrever o teste que falha**

```python
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
```

Nota: idempotência exige `META.generated_at` determinístico — usar a data do `corpus-data.json` (`mtime` em `YYYY-MM-DD`) ou omitir timestamp volátil. Decisão: `META = {"items": N, "year_coverage": pct, "source": "corpus-data.json"}` (sem relógio).

- [ ] **Step 3: Rodar e ver falhar**

Run: `pytest tests/tools/test_refresh_dashboard.py -v`
Expected: FAIL (`refresh_corpus_dashboard` com assinatura nova não existe)

- [ ] **Step 4: Reescrever `refresh_dashboard.py`**

```python
#!/usr/bin/env python3
"""Refresh dashboard HTML: embute corpus + agent-runs entre delimitadores.

Uso:
    python tools/scripts/refresh_dashboard.py           # corpus + agents
    python tools/scripts/refresh_dashboard.py --corpus
    python tools/scripts/refresh_dashboard.py --agents

Idempotente: rodar 2x produz arquivo idêntico. Falha alto (exit 1) se os
delimitadores estiverem ausentes/duplicados ou se o round-trip divergir.
"""
import argparse
import json
import sys
from pathlib import Path

from dashboard_data import build_dataset, load_records_index

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BEGIN = "// == DATA:BEGIN =="
END = "// == DATA:END =="
KEEP_FIELDS = [
    'id', 'title', 'date', 'year', 'country_pt', 'country', 'medium_norm',
    'support', 'period_norm', 'regime', 'endurecimento_score', 'indicadores',
    'motif', 'motif_str', 'tags', 'tags_str', 'description', 'url',
    'thumbnail_url', 'source_archive', 'creator', 'institution',
    'coded_by', 'coded_at', 'in_scope', 'citation_abnt'
]


def _load_json(path, default):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def _embed_block(html: str, block: str) -> str:
    if html.count(BEGIN) != 1 or html.count(END) != 1:
        sys.exit(f"ERRO: delimitadores ausentes ou duplicados "
                 f"(BEGIN={html.count(BEGIN)}, END={html.count(END)})")
    pre, rest = html.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{BEGIN}\n{block}{END}{post}"


def _roundtrip_check(html: str, expected_items: int) -> None:
    for line in html.splitlines():
        if line.startswith("const DATA = "):
            data = json.loads(line[len("const DATA = "):].rstrip().rstrip(";"))
            if len(data) != expected_items:
                sys.exit(f"ERRO round-trip: embutido {len(data)} != fonte {expected_items}")
            return
    sys.exit("ERRO round-trip: const DATA não encontrada após embed")


def refresh_corpus_dashboard(repo_root: Path) -> dict:
    repo_root = Path(repo_root)
    corpus = _load_json(repo_root / "corpus" / "corpus-data.json", [])
    items = corpus if isinstance(corpus, list) else corpus.get("items") or corpus.get("records") or []
    compact = [{k: it.get(k) for k in KEEP_FIELDS} for it in items]
    index = load_records_index(repo_root / "data" / "processed" / "records.jsonl")
    dataset = build_dataset(compact, index)
    agent_runs = _load_json(repo_root / "corpus" / "agent-runs.json", [])
    n_year = sum(1 for d in dataset if d.get("year"))
    meta = {"items": len(dataset),
            "year_coverage": round(n_year / len(dataset), 3) if dataset else 0,
            "source": "corpus-data.json"}

    block = (
        "const DATA = " + json.dumps(dataset, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "const AGENT_RUNS = " + json.dumps(agent_runs, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "const META = " + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n"
    )
    html_path = repo_root / "corpus" / "DASHBOARD_CORPUS.html"
    html = html_path.read_text(encoding="utf-8")
    new_html = _embed_block(html, block)
    _roundtrip_check(new_html, len(dataset))
    html_path.write_text(new_html, encoding="utf-8")
    print(f"Corpus dashboard refreshed: {len(dataset)} items, year_coverage {meta['year_coverage']:.1%}")
    return {"items": len(dataset), "bytes": len(new_html.encode("utf-8"))}


def refresh_agents_dashboard(repo_root: Path) -> dict:
    """Mantido por compatibilidade com DASHBOARD_AGENTS.html (legado)."""
    print("Agents dashboard: sem mudanças nesta versão (fora do escopo do spec v2)")
    return {"items": 0, "bytes": 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", action="store_true")
    ap.add_argument("--agents", action="store_true")
    args = ap.parse_args()
    both = not (args.corpus or args.agents)
    if args.corpus or both:
        refresh_corpus_dashboard(REPO_ROOT)
    if args.agents or both:
        refresh_agents_dashboard(REPO_ROOT)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Rodar testes + gerador real**

Run: `pytest tests/tools/test_refresh_dashboard.py tests/tools/test_dashboard_data.py -q && python tools/scripts/refresh_dashboard.py --corpus`
Expected: 9 passed; `Corpus dashboard refreshed: 335 items, year_coverage ~87%`

- [ ] **Step 6: Commit**

```bash
git add tools/scripts/refresh_dashboard.py corpus/DASHBOARD_CORPUS.html tests/tools/test_refresh_dashboard.py
git commit -m "refactor(dashboard): gerador endurecido com delimitadores e round-trip"
```

---

### Task 3: Navegação em 4 abas + preservação do Modo Foco

**Files:**
- Modify: `corpus/DASHBOARD_CORPUS.html` — `<nav>` da sidebar e contêineres de seção (somente HTML; JS da classe `Dashboard` não muda nesta task)

**Interfaces:**
- Consumes: seções existentes `sec-overview`, `sec-regime`, `sec-purification`, `sec-temporal`, `sec-distribution`, `sec-gallery`, `sec-table`, `sec-foco`.
- Produces: seções `sec-visao` (aba 1), `sec-explorar` (aba 2), `sec-endurecimento` (aba 3), `sec-qualidade` (aba 4, vazia — preenchida na Task 4), `sec-foco` (inalterada). `showSection(id, btn)` já existente continua válido.

- [ ] **Step 1: Substituir a `<nav>` da sidebar**

Substituir os 7 botões atuais (`overview`, `regime`, `purification`, `temporal`, `distribution`, `gallery`, `table`) por 5, mantendo o botão `foco` e o divisor:

```html
  <nav>
    <button class="nav-btn active" onclick="showSection('visao',this)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
      Visão Geral
    </button>
    <button class="nav-btn" onclick="showSection('explorar',this)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
      Explorar
    </button>
    <button class="nav-btn" onclick="showSection('endurecimento',this)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      Endurecimento
    </button>
    <button class="nav-btn" onclick="showSection('qualidade',this)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      Qualidade
    </button>
    <div style="height:2px;background:var(--brown);margin:8px 0;opacity:.3;"></div>
    <button class="nav-btn" onclick="showSection('foco',this)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
      Modo Foco
    </button>
  </nav>
```

- [ ] **Step 2: Reorganizar os contêineres de seção**

Reagrupar (mover blocos existentes **sem alterar ids internos de canvas** — a classe `Dashboard` depende deles):

```html
  <!-- ABA 1: VISÃO GERAL = antiga sec-overview + sec-distribution -->
  <div class="section active" id="sec-visao">
    <!-- mover: conteúdo integral da antiga sec-overview (kpi-row + 4 cards) -->
    <!-- mover: conteúdo integral da antiga sec-distribution (motifs, tags, acervos, períodos) -->
  </div>

  <!-- ABA 2: EXPLORAR = antiga sec-gallery + sec-table -->
  <div class="section" id="sec-explorar">
    <!-- mover: card da Galeria (gallery-grid + g-pagi) -->
    <!-- mover: card da Tabela (dtbl + t-pagi) -->
  </div>

  <!-- ABA 3: ENDURECIMENTO = antiga sec-purification + sec-regime + scatter da sec-temporal -->
  <div class="section" id="sec-endurecimento">
    <!-- mover: g1 com "Ano × Endurecimento — por Regime" (canvas c-scatter) da sec-temporal -->
    <!-- mover: conteúdo integral da antiga sec-regime -->
    <!-- mover: conteúdo integral da antiga sec-purification -->
  </div>

  <!-- ABA 4: QUALIDADE (preenchida na Task 4) -->
  <div class="section" id="sec-qualidade"></div>

  <!-- ABA 5: MODO FOCO — inalterada -->
```

Apagar as seções antigas `sec-regime`, `sec-purification`, `sec-temporal`, `sec-distribution`, `sec-gallery`, `sec-table`, `sec-overview` após mover o conteúdo. O card "Codificação — Fontes" (`c-coded-by`) e o card "Itens por Década" (`c-decade`) da antiga `sec-temporal` **não** vão para a aba 3 — migram para a aba 4 na Task 4; nesta task, deixá-los temporariamente dentro de `sec-qualidade` como HTML existente (o chart `c-coded-by` continua sendo atualizado pela classe `Dashboard`).

- [ ] **Step 3: Verificação manual no navegador**

Abrir `corpus/DASHBOARD_CORPUS.html` e conferir: 5 botões na sidebar; cada aba abre; gráficos renderizam em Visão Geral, Explorar e Endurecimento; galeria e tabela funcionam com paginação; modal abre; Modo Foco intacto (timer, to-do, word count, milestones).
Expected: sem erros no console do navegador; `showSection` alterna corretamente.

- [ ] **Step 4: Commit**

```bash
git add corpus/DASHBOARD_CORPUS.html
git commit -m "feat(dashboard): reorganizar seções em 4 abas analíticas (+ Modo Foco preservado)"
```

---

### Task 4: Aba Qualidade do Pipeline

**Files:**
- Modify: `corpus/DASHBOARD_CORPUS.html` — conteúdo de `sec-qualidade` (HTML) e classe `Dashboard` (novo método `renderQuality()` chamado em `render()`)

**Interfaces:**
- Consumes: globais `DATA`, `AGENT_RUNS`, `META` (Task 2); `grp`, `sorted`, `mean` já existentes no `<script>`.
- Produces: cards/canvas `c-coded-by` (migrado na Task 3), `c-coded-timeline`, `c-missing`, tabela `agent-runs-body`, aviso `quality-warnings`.

- [ ] **Step 1: HTML da aba**

Dentro de `<div class="section" id="sec-qualidade">` (além dos cards migrados `c-coded-by`/`c-decade`):

```html
    <div id="quality-warnings"></div>
    <div class="g2">
      <div class="card"><div class="card-header"><h3>Codificação — Fontes</h3></div><div class="card-body"><canvas id="c-coded-by"></canvas></div></div>
      <div class="card"><div class="card-header"><h3>Codificações ao longo do tempo</h3></div><div class="card-body"><canvas id="c-coded-timeline"></canvas></div></div>
    </div>
    <div class="g2">
      <div class="card"><div class="card-header"><h3>Campos faltantes (% do corpus)</h3></div><div class="card-body"><canvas id="c-missing"></canvas></div></div>
      <div class="card"><div class="card-header"><h3>Itens por Década</h3></div><div class="card-body"><canvas id="c-decade"></canvas></div></div>
    </div>
    <div class="g1">
      <div class="card">
        <div class="card-header"><h3>Últimos runs do pipeline</h3></div>
        <div class="card-body">
          <div class="tbl-wrap"><table class="dtbl">
            <thead><tr><th>Run</th><th>Instrumento</th><th>Itens</th><th>Data</th></tr></thead>
            <tbody id="agent-runs-body"></tbody>
          </table></div>
        </div>
      </div>
    </div>
```

Nota: o card "Codificação — Fontes" já existia na antiga `sec-temporal` com o mesmo canvas id `c-coded-by` — garantir que exista **uma única** ocorrência de `id="c-coded-by"` no arquivo final (a da aba 4). Idem `c-decade`.

- [ ] **Step 2: JS — registrar charts novos e renderQuality()**

Em `buildAllCharts()`, adicionar:

```javascript
    // Quality
    this.charts.codedTimeline = this.mk('c-coded-timeline','bar',{labels:[],datasets:[{data:[],backgroundColor:'#8b5a2baa',borderColor:'#8b5a2b',borderWidth:2,borderRadius:6}]},{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}});
    this.charts.missing = this.mk('c-missing','bar',{labels:[],datasets:[{data:[],backgroundColor:'#b85450aa',borderColor:'#b85450',borderWidth:2,borderRadius:6}]},{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,max:100,ticks:{callback:v=>v+'%'}}}});
```

Em `updateAllCharts()`, adicionar ao final:

```javascript
    // Quality: codificações por mês
    const byMonth = {};
    d.forEach(i => { const c = (i.coded_at||'').slice(0,7); if(c) byMonth[c]=(byMonth[c]||0)+1; });
    const months = Object.keys(byMonth).sort();
    this.upd(this.charts.codedTimeline, months, months.map(m => byMonth[m]));

    // Quality: campos faltantes
    const fields = [['sem ano','year'],['sem país','country_pt'],['sem data','date'],['sem thumbnail','thumbnail_url'],['sem motivo','motif']];
    this.upd(this.charts.missing, fields.map(f=>f[0]),
      fields.map(f => d.length ? +(d.filter(i => !i[f[1]] || (Array.isArray(i[f[1]]) && !i[f[1]].length)).length / d.length * 100).toFixed(1) : 0));
```

Novo método na classe e chamada em `render()` (após `this.renderHeatmap();`):

```javascript
  renderQuality() {
    const warn = document.getElementById('quality-warnings');
    const msgs = [];
    if(!Array.isArray(AGENT_RUNS) || !AGENT_RUNS.length) msgs.push('agent-runs.json ausente ou vazio — tabela de runs indisponível.');
    if(META && META.year_coverage !== undefined && META.year_coverage < 0.9)
      msgs.push(`Cobertura de ano derivado: ${(META.year_coverage*100).toFixed(0)}% (resto = "s/d").`);
    warn.innerHTML = msgs.map(m => `<div class="card" style="border-color:var(--amber);margin-bottom:var(--gap);"><div class="card-body" style="font-size:12px;">⚠ ${m}</div></div>`).join('');

    const body = document.getElementById('agent-runs-body');
    if(!Array.isArray(AGENT_RUNS) || !AGENT_RUNS.length) { body.innerHTML = '<tr><td colspan="4" style="color:var(--brown)">—</td></tr>'; return; }
    body.innerHTML = AGENT_RUNS.slice(0, 20).map(r => `<tr>
      <td style="font-family:'JetBrains Mono',monospace;font-size:10px;">${r.run_id || r.id || '—'}</td>
      <td>${r.instrument || r.coded_by || r.agent || '—'}</td>
      <td>${r.items ?? r.n_items ?? '—'}</td>
      <td>${(r.finished_at || r.date || r.coded_at || '').slice(0,10) || '—'}</td>
    </tr>`).join('');
  }
```

E em `render()`: adicionar `this.renderQuality();` logo após `this.renderHeatmap();`.

Nota de implementação: as chaves exatas de `agent-runs.json` (5,6 KB) devem ser lidas do arquivo real na hora de implementar; os fallbacks `||` acima cobrem variações (`run_id|id`, `instrument|coded_by|agent`, `items|n_items`, `finished_at|date|coded_at`).

- [ ] **Step 3: Verificação manual**

Abrir o HTML: aba Qualidade renderiza 4 charts + tabela de runs; avisos âmbar aparecem; sem duplicatas de canvas id no console (`Chart.js` não loga erro de "Canvas is already in use").
Expected: aba funcional, sem erros de console.

- [ ] **Step 4: Commit**

```bash
git add corpus/DASHBOARD_CORPUS.html
git commit -m "feat(dashboard): aba Qualidade do Pipeline (coded_by, timeline, faltantes, runs)"
```

---

### Task 5: Verificação final e documentação

**Files:**
- Modify: `CLAUDE.md` — seção Quick Commands (uma linha, se ainda não houver)
- Modify: `docs/superpowers/specs/2026-08-12-dashboard-corpus-design.md` — marcar status "implementado" no cabeçalho

**Interfaces:**
- Consumes: tudo das Tasks 1–4.

- [ ] **Step 1: Bateria de verificação**

```bash
cd /Users/ana/Research/hub/iconocracy-corpus && conda activate iconocracy
pytest tests/ -x -q
python tools/scripts/refresh_dashboard.py --corpus
python tools/scripts/refresh_dashboard.py --corpus
git diff --stat corpus/DASHBOARD_CORPUS.html   # segunda rodada: sem diff
wc -c corpus/DASHBOARD_CORPUS.html             # < 1.500.000 bytes
```

Expected: suite verde; relatório `335 items`; segundo run sem diff; arquivo < 1,5 MB.

- [ ] **Step 2: Checklist manual (4 abas)**

- Visão Geral: KPIs com N=335; charts país/regime/suporte/década + motifs/tags/acervos/períodos.
- Explorar: filtros combinam (país + regime + busca), galeria pagina, tabela ordena, modal abre ficha com ABNT.
- Endurecimento: scatter ano × score com pontos (ano derivado visível), radar, heatmap, barras por regime.
- Qualidade: 4 charts + tabela de runs + avisos; "sem ano" ≈ 13% no chart de faltantes.
- Modo Foco: pomodoro e word count funcionam (localStorage).

- [ ] **Step 3: Atualizar docs**

Em `docs/superpowers/specs/2026-08-12-dashboard-corpus-design.md`, linha de status:
`**Status:** implementado (2026-08-12, PR #___)` — preencher com o número real do PR.

- [ ] **Step 4: Commit + PR + merge**

```bash
git add -A
git commit -m "docs: dashboard v2 implementado (spec status + quick command)"
gh pr create --base main --title "feat(dashboard): v2 — 4 abas, gerador endurecido, aba Qualidade" --body "Implementa docs/superpowers/specs/2026-08-12-dashboard-corpus-design.md. Tasks: derivações (ano/thumbnail), gerador com delimitadores + round-trip, reorganização em 4 abas (+ Modo Foco preservado), aba Qualidade do Pipeline. Verificação: pytest verde, idempotência, <1,5 MB."
gh pr merge --merge
```

---

## Self-Review

**Cobertura do spec:**
- Gerador endurecido (delimitadores + falha alto) → Task 2 ✓
- Validação round-trip + idempotência → Task 2 (código + testes) ✓
- Sem base64 / placeholder tipográfico → Task 1 (`derive_thumbnail` conservador) + front já existente tem placeholder ✓
- 4 abas com o conteúdo especificado → Tasks 3–4 ✓ (KPIs/década/regime/país/suporte = aba 1; galeria/filtros/modal/ABNT = aba 2; histograma score/heatmap/scatter/outliers/médias país = aba 3 via sec-purification+regime+temporal; coded_by/timeline/faltantes/runs/avisos = aba 4)
- year derivado com regra 1400–2099 (~87%) → Task 1 ✓ (mesma regra documentada no Supabase)
- Estética preservada → Global Constraints + nenhuma mudança de CSS ✓
- YAGNI (sem servidor/framework/base64) → respeitado ✓
- Verificação (4 passos do spec) → Task 5 ✓

**Ressalva deliberada (desvio do spec, aprovado em conversa):** o spec lista "ranking de outliers (10 maiores/menores)" e "médias por país" na aba 3; o dashboard atual já cobre médias por regime (não por país) e não tem ranking de outliers. Decisão de implementação: os charts existentes de regime/heatmap/scatter cobrem a pergunta analítica; se a autora quiser o ranking explícito, vira follow-up pequeno (uma `renderOutliers()`). **Marcar como follow-up conhecido, não bloqueia o PR.**

**Placeholder scan:** sem TBD/TODO; código completo nos passos de código; âncoras de movimentação referem ids reais verificados no arquivo.

**Consistência de tipos:** `build_dataset(items, index)` usado igual nas Tasks 1–2; `refresh_corpus_dashboard(repo_root: Path)` igual na Task 2 e nos testes; globais `DATA/AGENT_RUNS/META` iguais nas Tasks 2 e 4; canvas ids `c-coded-by`/`c-decade` únicos (nota explícita na Task 4, Step 1).
