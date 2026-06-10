# E1 Re-run com Fable 5 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recodificar os 265 itens do corpus com Fable 5 multimodal (instrumento único) no `pathosformel_index.jsonl`, com triagem de disponibilidade de imagem e exclusões documentadas, destravando o IRR re-run.

**Architecture:** Pipeline em 3 estágios — (1) `e1_triage_images.py` resolve a melhor fonte de imagem por item (local → URL remota → exclusão) e gera worklist + lista de excluídos; (2) subagentes `iconocode` codificam em lotes de ~25, um agente por item em paralelo; (3) `e1_append_batch.py` valida e grava atomicamente no index, marcando a worklist. Commit por lote = resumível.

**Tech Stack:** Python 3.12 (conda env `iconocracy`, `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12`), stdlib apenas (json, urllib, re, pathlib), pytest. Subagentes via Agent tool (`subagent_type: iconocode`).

**Spec:** `docs/superpowers/specs/2026-06-09-e1-fable5-recode-design.md`

---

## Contexto para quem nunca viu este repo

- **Canônico:** `data/processed/records.jsonl` — 265 registros, um JSON por linha.
  Campos relevantes: `item_id` (UUID), `input` (dict: `input_url`, `title_hint`,
  `date_hint`, `place_hint`), `webscout` (dict: `search_results[].notes` pode conter
  `SCOUT-NNN`), `purificacao` (coding antigo, NÃO tocar).
- **Sigla:** `corpus/corpus-data.json` é uma LISTA de itens; o lookup é por URL
  (`item["url"]` → `item.get("id", "")`). Ver helper `load_corpus()` em
  `tools/scripts/e1_pathosformel_batch.py:74-84` (existe só no checkout principal,
  untracked — replicar o padrão, não importar).
- **Index destino:** `data/processed/pathosformel_index.jsonl` — formato de linha
  (versão Gemma, a preservar com novos campos):
  `item_id, sigla_id, title, place, date, url, coded_by, coded_at,`
  10 indicadores (int 0–3): `desincorporacao, rigidez_postural, dessexualizacao,
  uniformizacao_facial, heraldizacao, enquadramento_arquitetonico,
  apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal`,
  `purificacao_composto` (média dos 10, float 1 casa), `regime_iconocratico`
  (enum: `fundacional|normativo|militar|contra-alegoria`), `notes`.
  Novos campos desta rodada: `coded_from: "image"`, `image_source: "local"|"url"`,
  `confidence: float 0-1`, `flags: []` (ex.: `low_res`).
- **Imagens locais:** nomeadas por sigla em
  `/Users/ana/Research/hub/iconocracy-corpus/binaries/Images-reacquired-2026-06-09/`
  (50 arquivos, ex. `BE-001.jpg`) e `/Users/ana/Research/hub/iconocracy-corpus/gallery/**`
  (16, nomes livres — só binaries é resolvível por sigla).
  **Atenção:** esses caminhos são do checkout PRINCIPAL; o worktree não os contém.
  Sempre passar via `--binaries-root` absoluto.
- **Vault notes:** `vault/candidatos/*.md`; thumbnail aparece como `[imagem](url)`
  ou `thumbnail: url` (regexes prontos em `e1_recode_zeros.py:77-87` do checkout
  principal — replicar).
- **Hooks:** PostToolUse roda `validate_schemas.py` em edits de `(corpus|data)/**/*.jsonl?`.
  Gravações via script Bash não disparam o hook — por isso o append valida sozinho.
- **Testes:** pytest da raiz do repo, sem config file. Convenção: `tests/tools/test_<script>.py`.
- **Python:** SEMPRE o caminho completo do env conda acima. Nunca system Python.

---

### Task 1: Triagem — `e1_triage_images.py`

**Files:**
- Create: `tools/scripts/e1_triage_images.py`
- Test: `tests/tools/test_e1_triage_images.py`

- [ ] **Step 1.1: Escrever os testes (falhando)**

```python
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
```

- [ ] **Step 1.2: Rodar e confirmar que falham**

Run: `cd <worktree> && /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/tools/test_e1_triage_images.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'e1_triage_images'`

- [ ] **Step 1.3: Implementar o script**

```python
#!/usr/bin/env python3
# tools/scripts/e1_triage_images.py
"""E1 triage — resolve the best image source per record.

Cascade: local file (sigla-named) -> vault-note thumbnail URL -> excluded.
Outputs e1_worklist.json (codeable) and e1_excluded.json (#no-image).

Usage:
    python tools/scripts/e1_triage_images.py \
        --binaries-root /Users/ana/Research/hub/iconocracy-corpus/binaries/Images-reacquired-2026-06-09 \
        [--skip-head-check] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
VAULT_DIR = REPO / "vault" / "candidatos"
WORKLIST_PATH = REPO / "data" / "processed" / "e1_worklist.json"
EXCLUDED_PATH = REPO / "data" / "processed" / "e1_excluded.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
HEAD_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (iconocracy-corpus E1 triage; academic research)"


def load_records(path: Path = RECORDS_PATH) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def load_corpus_url_map(path: Path = CORPUS_PATH) -> dict[str, dict]:
    items = json.loads(path.read_text(encoding="utf-8"))
    return {it["url"]: it for it in items if it.get("url")}


def find_sigla(record: dict, url_map: dict[str, dict]) -> str:
    url = record.get("input", {}).get("input_url", "")
    item = url_map.get(url)
    if item and item.get("id"):
        return item["id"]
    # fallback: SCOUT id from webscout notes
    for sr in record.get("webscout", {}).get("search_results", []):
        m = re.search(r"((?:SCOUT|[A-Z]{2})-\d+)", sr.get("notes", ""))
        if m:
            return m.group(1)
    return record["item_id"][:12]


def find_local_image(sigla: str, roots: list[Path]) -> Path | None:
    for root in roots:
        for ext in IMAGE_EXTS:
            p = root / f"{sigla}{ext}"
            if p.is_file():
                return p
    return None


def extract_vault_thumb(sigla: str, vault_dir: Path = VAULT_DIR) -> str | None:
    for f in vault_dir.glob(f"{sigla}*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"\[imagem\]\((https?://[^)]+)\)", text)
        if m:
            return m.group(1)
        m = re.search(r"thumbnail[^:]*:\s*(https?://\S+)", text, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(")").rstrip(">")
    return None


def head_is_image(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=HEAD_TIMEOUT) as resp:
            ctype = resp.headers.get("Content-Type", "")
            return ctype.startswith("image/")
    except Exception:
        return False


def build_worklist(records: list[dict], url_map: dict[str, dict],
                   binaries_roots: list[Path], vault_dir: Path,
                   head_check: bool = True) -> tuple[list[dict], list[dict]]:
    now = datetime.now(timezone.utc).isoformat()
    worklist: list[dict] = []
    excluded: list[dict] = []
    for rec in records:
        sigla = find_sigla(rec, url_map)
        inp = rec.get("input", {})
        base = {
            "item_id": rec["item_id"],
            "sigla_id": sigla,
            "title": inp.get("title_hint", ""),
            "place": inp.get("place_hint", ""),
            "date": inp.get("date_hint", ""),
            "url": inp.get("input_url", ""),
        }
        local = find_local_image(sigla, binaries_roots)
        if local:
            worklist.append({**base, "image_source": "local",
                             "path_or_url": str(local), "status": "pending"})
            continue
        thumb = extract_vault_thumb(sigla, vault_dir)
        if thumb:
            if head_check and not head_is_image(thumb):
                excluded.append({**base, "reason": "not_an_image",
                                 "candidate_url": thumb, "checked_at": now})
                continue
            worklist.append({**base, "image_source": "url",
                             "path_or_url": thumb, "status": "pending"})
            continue
        excluded.append({**base, "reason": "no_image_source", "checked_at": now})
    return worklist, excluded


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--binaries-root", action="append", type=Path, default=[],
                    help="dir with sigla-named images (repeatable)")
    ap.add_argument("--skip-head-check", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    records = load_records()
    if args.limit:
        records = records[: args.limit]
    url_map = load_corpus_url_map()
    worklist, excluded = build_worklist(
        records, url_map, args.binaries_root, VAULT_DIR,
        head_check=not args.skip_head_check)

    WORKLIST_PATH.write_text(
        json.dumps(worklist, ensure_ascii=False, indent=1), encoding="utf-8")
    EXCLUDED_PATH.write_text(
        json.dumps(excluded, ensure_ascii=False, indent=1), encoding="utf-8")
    n_local = sum(1 for w in worklist if w["image_source"] == "local")
    print(f"worklist: {len(worklist)} (local={n_local}, "
          f"url={len(worklist) - n_local}) | excluded: {len(excluded)}")
    for reason in ("no_image_source", "not_an_image", "image_unreachable"):
        n = sum(1 for e in excluded if e["reason"] == reason)
        if n:
            print(f"  excluded/{reason}: {n}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 1.4: Rodar os testes e confirmar que passam**

Run: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/tools/test_e1_triage_images.py -v`
Expected: 9 passed

- [ ] **Step 1.5: Commit**

```bash
git add tools/scripts/e1_triage_images.py tests/tools/test_e1_triage_images.py
git commit -m "feat(e1): triage de fontes de imagem (local -> vault thumb -> exclusao)"
```

---

### Task 2: Gravação — `e1_append_batch.py`

**Files:**
- Create: `tools/scripts/e1_append_batch.py`
- Test: `tests/tools/test_e1_append_batch.py`

- [ ] **Step 2.1: Escrever os testes (falhando)**

```python
# tests/tools/test_e1_append_batch.py
"""Tests for e1_append_batch.py — validated atomic append to the index."""
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools" / "scripts"))

from e1_append_batch import validate_item, append_batch, INDICATORS


def _coded(item_id="uuid-1", **over):
    base = {
        "item_id": item_id, "sigla_id": "FR-013", "title": "Marianne",
        "place": "France", "date": "1880", "url": "https://ex.org/1",
        "coded_by": "fable-5", "coded_at": "2026-06-09T20:00:00Z",
        "coded_from": "image", "image_source": "local",
        "confidence": 0.9, "flags": [], "notes": "ok",
        "regime_iconocratico": "normativo",
    }
    base.update({ind: 2 for ind in INDICATORS})
    base.update(over)
    return base


def test_validate_ok():
    assert validate_item(_coded(), known_ids={"uuid-1"}, indexed_ids=set()) == []


def test_validate_rejects_out_of_range():
    errs = validate_item(_coded(desincorporacao=4),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("desincorporacao" in e for e in errs)


def test_validate_rejects_bad_regime():
    errs = validate_item(_coded(regime_iconocratico="imperial"),
                         known_ids={"uuid-1"}, indexed_ids=set())
    assert any("regime" in e for e in errs)


def test_validate_rejects_unknown_item():
    errs = validate_item(_coded(), known_ids={"other"}, indexed_ids=set())
    assert any("records.jsonl" in e for e in errs)


def test_validate_rejects_duplicate():
    errs = validate_item(_coded(), known_ids={"uuid-1"}, indexed_ids={"uuid-1"})
    assert any("duplicado" in e for e in errs)


def test_append_batch_writes_composto_and_marks_worklist(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps(
        [{"item_id": "uuid-1", "status": "pending"}]))
    ok, errors = append_batch([_coded()], index, worklist,
                              known_ids={"uuid-1"})
    assert ok == 1 and not errors
    row = json.loads(index.read_text().strip())
    assert row["purificacao_composto"] == 2.0
    wl = json.loads(worklist.read_text())
    assert wl[0]["status"] == "done"


def test_append_batch_rejects_whole_invalid_item(tmp_path):
    index = tmp_path / "index.jsonl"
    worklist = tmp_path / "worklist.json"
    worklist.write_text(json.dumps(
        [{"item_id": "uuid-1", "status": "pending"}]))
    ok, errors = append_batch([_coded(serialidade=-1)], index, worklist,
                              known_ids={"uuid-1"})
    assert ok == 0 and errors
    assert not index.exists() or index.read_text() == ""
    assert json.loads(worklist.read_text())[0]["status"] == "pending"
```

- [ ] **Step 2.2: Rodar e confirmar que falham**

Run: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/tools/test_e1_append_batch.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'e1_append_batch'`

- [ ] **Step 2.3: Implementar o script**

```python
#!/usr/bin/env python3
# tools/scripts/e1_append_batch.py
"""Validated atomic append of coded E1 batches to pathosformel_index.jsonl.

Input: a JSON file with a LIST of coded items (one per subagent output).
Each item must carry the 10 indicators (int 0-3), regime, provenance fields.
Computes purificacao_composto. Rejects invalid items whole (no partial rows).
Marks corresponding worklist entries as done.

Usage:
    python tools/scripts/e1_append_batch.py batch_NN.json
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
INDEX_PATH = REPO / "data" / "processed" / "pathosformel_index.jsonl"
WORKLIST_PATH = REPO / "data" / "processed" / "e1_worklist.json"

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]
REGIMES = {"fundacional", "normativo", "militar", "contra-alegoria"}
REQUIRED = {"item_id", "sigla_id", "coded_by", "coded_at", "coded_from",
            "image_source", "regime_iconocratico"}


def validate_item(item: dict, known_ids: set[str],
                  indexed_ids: set[str]) -> list[str]:
    errs: list[str] = []
    missing = REQUIRED - item.keys()
    if missing:
        errs.append(f"campos ausentes: {sorted(missing)}")
    for ind in INDICATORS:
        v = item.get(ind)
        if not isinstance(v, int) or not 0 <= v <= 3:
            errs.append(f"{ind}={v!r} fora de 0-3")
    if item.get("regime_iconocratico") not in REGIMES:
        errs.append(f"regime invalido: {item.get('regime_iconocratico')!r}")
    if item.get("item_id") not in known_ids:
        errs.append(f"item_id {item.get('item_id')!r} nao existe em records.jsonl")
    if item.get("item_id") in indexed_ids:
        errs.append(f"item_id {item.get('item_id')!r} duplicado no index")
    return errs


def _atomic_append_lines(path: Path, lines: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(existing)
        for line in lines:
            f.write(line + "\n")
    os.replace(tmp, path)


def append_batch(items: list[dict], index_path: Path, worklist_path: Path,
                 known_ids: set[str]) -> tuple[int, list[str]]:
    indexed_ids: set[str] = set()
    if index_path.exists():
        for line in index_path.open(encoding="utf-8"):
            if line.strip():
                indexed_ids.add(json.loads(line)["item_id"])

    errors: list[str] = []
    valid: list[dict] = []
    for it in items:
        errs = validate_item(it, known_ids, indexed_ids)
        if errs:
            errors.append(f"{it.get('sigla_id', it.get('item_id', '?'))}: "
                          + "; ".join(errs))
            continue
        it = dict(it)  # nao mutar o input
        it["purificacao_composto"] = round(
            sum(it[ind] for ind in INDICATORS) / len(INDICATORS), 2)
        valid.append(it)
        indexed_ids.add(it["item_id"])

    if valid:
        _atomic_append_lines(
            index_path,
            [json.dumps(v, ensure_ascii=False) for v in valid])
        done_ids = {v["item_id"] for v in valid}
        wl = json.loads(worklist_path.read_text(encoding="utf-8"))
        wl = [{**w, "status": "done"} if w["item_id"] in done_ids else w
              for w in wl]
        worklist_path.write_text(
            json.dumps(wl, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(valid), errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("batch_file", type=Path)
    ap.add_argument("--index", type=Path, default=INDEX_PATH)
    ap.add_argument("--worklist", type=Path, default=WORKLIST_PATH)
    args = ap.parse_args()

    items = json.loads(args.batch_file.read_text(encoding="utf-8"))
    known_ids = {json.loads(l)["item_id"]
                 for l in RECORDS_PATH.open(encoding="utf-8") if l.strip()}
    ok, errors = append_batch(items, args.index, args.worklist, known_ids)
    print(f"gravados: {ok}/{len(items)}")
    for e in errors:
        print(f"  REJEITADO {e}")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.4: Rodar os testes e confirmar que passam**

Run: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/tools/test_e1_append_batch.py -v`
Expected: 7 passed

- [ ] **Step 2.5: Rodar a suíte inteira (regressão)**

Run: `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/ -q`
Expected: tudo verde (mesma contagem de falhas pré-existentes, se houver — anotar)

- [ ] **Step 2.6: Commit**

```bash
git add tools/scripts/e1_append_batch.py tests/tools/test_e1_append_batch.py
git commit -m "feat(e1): append validado e atomico ao pathosformel_index"
```

---

### Task 3: Arquivar index Gemma + rodar triagem real

**Files:**
- Create: `data/processed/pathosformel_index_gemma4_archived_2026-06-09.jsonl` (cópia)
- Create: `data/processed/e1_worklist.json`, `data/processed/e1_excluded.json` (gerados)

- [ ] **Step 3.1: Arquivar o index Gemma (do checkout principal)**

```bash
cp /Users/ana/Research/hub/iconocracy-corpus/data/processed/pathosformel_index.jsonl \
   data/processed/pathosformel_index_gemma4_archived_2026-06-09.jsonl
wc -l data/processed/pathosformel_index_gemma4_archived_2026-06-09.jsonl
```
Expected: `52`

- [ ] **Step 3.2: Rodar a triagem completa (com HEAD check)**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 \
  tools/scripts/e1_triage_images.py \
  --binaries-root /Users/ana/Research/hub/iconocracy-corpus/binaries/Images-reacquired-2026-06-09
```
Expected: stdout com `worklist: N (local=~50, url=...)` e `excluded: M`, N+M=265.
Sanity: N entre ~150 e ~220 (projeção do IRR design: ~186-200). Se N < 120,
PARAR e investigar (regex de thumbnail ou siglas não casando) antes de seguir.

- [ ] **Step 3.3: Inspecionar amostra da worklist e dos excluídos**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 - <<'EOF'
import json
wl = json.load(open("data/processed/e1_worklist.json"))
ex = json.load(open("data/processed/e1_excluded.json"))
print("worklist:", len(wl), "| excluded:", len(ex))
for w in wl[:5]: print(" ", w["sigla_id"], w["image_source"], w["path_or_url"][:70])
for e in ex[:5]: print(" X", e["sigla_id"], e["reason"])
EOF
```
Expected: siglas plausíveis (XX-NNN), paths locais existentes, URLs http(s).

- [ ] **Step 3.4: Commit**

```bash
git add data/processed/pathosformel_index_gemma4_archived_2026-06-09.jsonl \
        data/processed/e1_worklist.json data/processed/e1_excluded.json
git commit -m "data(e1): arquiva index gemma4 e gera worklist/excluidos da triagem"
```

---

### Task 4: Dry-run — lote piloto de 5 itens

**Files:**
- Create: `data/processed/e1_batches/batch_00_dryrun.json` (saída dos subagentes)

- [ ] **Step 4.1: Selecionar 5 itens pending (preferindo 3 local + 2 url)**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 - <<'EOF'
import json
wl = json.load(open("data/processed/e1_worklist.json"))
pend = [w for w in wl if w["status"] == "pending"]
local = [w for w in pend if w["image_source"] == "local"][:3]
url = [w for w in pend if w["image_source"] == "url"][:2]
for w in local + url:
    print(json.dumps(w, ensure_ascii=False))
EOF
```

- [ ] **Step 4.2: Despachar 5 subagentes iconocode em paralelo (um por item)**

Para cada item, Agent tool com `subagent_type: "iconocode"` e este prompt
(substituir os campos `{...}`):

```
Codifique este item do corpus ICONOCRACIA pelo protocolo IconoCode completo
(Panofsky 3 níveis + 10 indicadores de purificação 0-3 + regime iconocrático).

ITEM: {sigla_id} — {title} ({place}, {date})
IMAGEM: {path_or_url}
  - Se caminho local: leia com a ferramenta Read.
  - Se URL: busque a imagem com WebFetch.
FONTE ORIGINAL: {url}

Responda APENAS com um objeto JSON válido, sem markdown, neste formato exato:
{"item_id": "{item_id}", "sigla_id": "{sigla_id}", "title": "{title}",
 "place": "{place}", "date": "{date}", "url": "{url}",
 "coded_by": "fable-5", "coded_at": "<ISO-8601 UTC agora>",
 "coded_from": "image", "image_source": "{image_source}",
 "desincorporacao": 0-3, "rigidez_postural": 0-3, "dessexualizacao": 0-3,
 "uniformizacao_facial": 0-3, "heraldizacao": 0-3,
 "enquadramento_arquitetonico": 0-3, "apagamento_narrativo": 0-3,
 "monocromatizacao": 0-3, "serialidade": 0-3, "inscricao_estatal": 0-3,
 "regime_iconocratico": "fundacional|normativo|militar|contra-alegoria",
 "confidence": 0.0-1.0, "flags": [], "notes": "<2-3 frases justificando>"}

Regras: indicadores são INTEIROS 0-3. Se a imagem tiver lado menor < 100px,
adicione "low_res" a flags e reduza confidence. Se NÃO conseguir ver a imagem
(falha de leitura/fetch), retorne {"item_id": "{item_id}", "error": "image_unreachable"}
em vez de inventar scores.
```

- [ ] **Step 4.3: Coletar as 5 respostas num batch JSON**

Gravar a lista (apenas itens SEM `"error"`) em
`data/processed/e1_batches/batch_00_dryrun.json` (criar a pasta).
Itens com `"error": "image_unreachable"`: registrar à mão em
`e1_excluded.json` com `reason: "image_unreachable"` e remover da worklist
(status segue `pending` até decisão; anotar no commit).

- [ ] **Step 4.4: Gravar via append e validar**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 \
  tools/scripts/e1_append_batch.py data/processed/e1_batches/batch_00_dryrun.json
wc -l data/processed/pathosformel_index.jsonl
```
Expected: `gravados: 5/5` (ou menos com REJEITADO listado); index com 5 linhas.

- [ ] **Step 4.5: REVISÃO HUMANA DO PILOTO (gate)**

Mostrar à Ana os 5 itens codificados (indicadores + regime + notes) ao lado
das imagens. Critérios: scores plausíveis (não tudo 0, não tudo 3), regime
coerente com o motivo, notes específicas (não genéricas). SÓ avançar para a
Task 5 com aprovação explícita.

- [ ] **Step 4.6: Commit**

```bash
git add data/processed/e1_batches/batch_00_dryrun.json \
        data/processed/pathosformel_index.jsonl data/processed/e1_worklist.json
git commit -m "data(e1): dry-run fable-5 com 5 itens (piloto aprovado)"
```

---

### Task 5: Lotes de produção (~25 itens × 8-9 lotes)

**Files:**
- Create: `data/processed/e1_batches/batch_NN.json` (um por lote)
- Modify: `data/processed/pathosformel_index.jsonl`, `e1_worklist.json`, `e1_excluded.json`

Repetir até worklist sem `pending`:

- [ ] **Step 5.1: Selecionar próximos 25 pending** (mesmo one-liner da Step 4.1,
  sem o filtro local/url, `[:25]`)
- [ ] **Step 5.2: Despachar 25 subagentes iconocode em paralelo** — mesmo prompt
  da Step 4.2, verbatim
- [ ] **Step 5.3: Coletar em `data/processed/e1_batches/batch_NN.json`**
  (NN = 01, 02, ...). JSON inválido de subagente: 1 redispatch; persiste →
  deixar fora do batch (fica `pending`, anotar em notes do commit)
- [ ] **Step 5.4: Append + checagem**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 \
  tools/scripts/e1_append_batch.py data/processed/e1_batches/batch_NN.json
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 - <<'EOF'
import json
wl = json.load(open("data/processed/e1_worklist.json"))
done = sum(1 for w in wl if w["status"] == "done")
print(f"progresso: {done}/{len(wl)}")
EOF
```

- [ ] **Step 5.5: Commit do lote**

```bash
git add data/processed/e1_batches/ data/processed/pathosformel_index.jsonl \
        data/processed/e1_worklist.json data/processed/e1_excluded.json
git commit -m "data(e1): lote NN fable-5 (+K itens, total D/N)"
```

- [ ] **Step 5.6: A cada 2 lotes, sanity-check de deriva**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 - <<'EOF'
import json, collections
rows = [json.loads(l) for l in open("data/processed/pathosformel_index.jsonl")]
inds = ["desincorporacao","rigidez_postural","dessexualizacao",
        "uniformizacao_facial","heraldizacao","enquadramento_arquitetonico",
        "apagamento_narrativo","monocromatizacao","serialidade","inscricao_estatal"]
zero = sum(1 for r in rows if all(r[i] == 0 for i in inds))
reg = collections.Counter(r["regime_iconocratico"] for r in rows)
comp = [r["purificacao_composto"] for r in rows]
print(f"n={len(rows)} all-zero={zero} regimes={dict(reg)}")
print(f"composto: min={min(comp):.1f} max={max(comp):.1f} "
      f"mean={sum(comp)/len(comp):.2f}")
EOF
```
Expected: `all-zero=0` (o problema do Gemma NÃO deve reaparecer); composto
espalhado (não colapsado num único valor); 4 regimes presentes ao longo do tempo.

---

### Task 6: Estatística final + readiness check do IRR

**Files:**
- Create: `docs/decisions/E1-FABLE5-STATUS-2026-06.md`

- [ ] **Step 6.1: Gerar o relatório final**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 - <<'EOF'
import json, collections
rows = [json.loads(l) for l in open("data/processed/pathosformel_index.jsonl")]
ex = json.load(open("data/processed/e1_excluded.json"))
inds = ["desincorporacao","rigidez_postural","dessexualizacao",
        "uniformizacao_facial","heraldizacao","enquadramento_arquitetonico",
        "apagamento_narrativo","monocromatizacao","serialidade","inscricao_estatal"]
print(f"# E1 Fable 5 — população final: {len(rows)} codificados, {len(ex)} excluídos")
print("\n## Distribuição por indicador (0/1/2/3)")
for i in inds:
    c = collections.Counter(r[i] for r in rows)
    nz = 100 * sum(v for k, v in c.items() if k > 0) / len(rows)
    print(f"  {i:<28} {c[0]:>3}/{c[1]:>3}/{c[2]:>3}/{c[3]:>3}  ({nz:.0f}% nao-zero)")
print("\n## Regimes (vs estratos IRR: fund~100 norm~60 mil~20 contra~8)")
for k, v in collections.Counter(
        r["regime_iconocratico"] for r in rows).most_common():
    print(f"  {k:<16} {v}")
print("\n## Exclusões por motivo")
for k, v in collections.Counter(e["reason"] for e in ex).most_common():
    print(f"  {k:<20} {v}")
EOF
```

- [ ] **Step 6.2: Escrever `docs/decisions/E1-FABLE5-STATUS-2026-06.md`** com a
  saída acima + decisões do spec (instrumento único, exclusões) + verificação
  do critério de pronto do IRR (população ≥ ~150 com 4 estratos povoados:
  apto a sortear amostra 25-30 com seed 20260611). Apontar para o spec e
  para `IRR-RE-RUN-DESIGN-2026-06-09.md` como próximo passo.

- [ ] **Step 6.3: Suíte completa + commit final**

```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pytest tests/ -q
git add docs/decisions/E1-FABLE5-STATUS-2026-06.md
git commit -m "docs(e1): status final do re-run fable-5 e readiness do IRR"
```

- [ ] **Step 6.4: Apresentar à Ana** — resumo do funil (265 → codificados/excluídos),
  flag de qualquer estrato abaixo do mínimo do IRR, e a pergunta: abrir PR do
  branch ou seguir direto para o sorteio da amostra IRR.

---

## Self-review (feito na escrita)

- **Cobertura do spec:** triagem cascata + HEAD check (§3.1 → Task 1/3), lotes
  com subagente iconocode e prompt fixo (§3.2 → Tasks 4-5), append atômico
  validado + arquivamento Gemma (§3.3 → Tasks 2-3), commit por lote/resumível
  (§3.4 → Task 5), tratamento de erros (§4 → Steps 4.2-4.3, 5.3, validação),
  critério de pronto (§5 → Task 6). Fora de escopo respeitado (sem IRR, sem
  records.jsonl).
- **Placeholders:** nenhum TBD; todo step com código/comando/prompt completo.
- **Consistência de tipos:** `INDICATORS`/`REGIMES` idênticos nos dois scripts
  e no prompt; shape da worklist igual entre Task 1 (produz) e Task 2 (consome);
  composto calculado só no append (subagente não calcula).
