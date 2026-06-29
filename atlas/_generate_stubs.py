#!/usr/bin/env python3
"""Gera nós-stub do Atlas (knowledge graph) varrendo as superfícies documentais
do repositório.

Cada stub é um nó Obsidian Flavored Markdown que **resume e aponta** para um
arquivo-fonte canônico (não duplica conteúdo). Os stubs dão cobertura exaustiva
ao grafo; a "espinha" (nós escritos à mão) permanece a leitura curada.

Uso (a partir da raiz do repo):

    python atlas/_generate_stubs.py

Idempotente: regenera `atlas/stubs/` por inteiro a cada execução.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS = REPO / "atlas"
STUBS = ATLAS / "stubs"
TODAY = _dt.date.today().isoformat()

# (categoria, MOC de backlink, tag-extra, lista de globs relativos ao repo)
SURFACES: list[tuple[str, str, str, list[str]]] = [
    ("adr",        "ADRs e Decisões — MOC", "arquitetura", ["docs/adr/*.md"]),
    ("decisao",    "ADRs e Decisões — MOC", "decisao",     ["docs/decisions/*.md"]),
    ("schema",     "Esquemas JSON",         "dados",       ["tools/schemas/*.json"]),
    ("manuscrito", "Manuscrito — MOC",      "manuscrito",  ["tese/manuscrito/*.md"]),
    ("conceito",   "Conceitos — MOC",       "conceito",    ["concepts/*.md"]),
    ("entidade",   "Iconocracia — Mapa Central", "entidade", ["entities/*.md"]),
    ("doc",        "Iconocracia — Mapa Central", "doc",     ["docs/*.md"]),
    ("notebook",   "Hierarquia de Dados — MOC", "analise", ["notebooks/*.ipynb"]),
]

# Não gerar stub para arquivos-fonte protegidos / ruidosos.
EXCLUDE = re.compile(r"_original|/LEIAME\.md$|/README\.md$")

_FM = re.compile(r"^---\n.*?\n---\n", re.S)
_H = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def clean_summary(text: str) -> str:
    """Neutraliza marcação que não resolve fora do vault de origem: wikilinks,
    imagens e links Markdown viram texto puro (evita ghosts e paths quebrados)."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)          # imagens
    text = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?\|([^\]]+)\]\]", r"\2", text)  # [[a|b]]->b
    text = re.sub(r"\[\[([^\]|#]+)(?:[#][^\]]*)?\]\]", r"\1", text)           # [[a]]->a
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)      # [t](u)->t
    return text.strip()


def slug(name: str) -> str:
    return name.replace(".md", "").replace(".json", "").replace(".ipynb", "")


def title_summary(path: Path) -> tuple[str, str]:
    """Extrai (título, resumo curto) de um arquivo-fonte."""
    if path.suffix == ".json":
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            return d.get("title", path.stem), (d.get("description", "") or "").strip()
        except (json.JSONDecodeError, OSError):
            return path.stem, ""
    if path.suffix == ".ipynb":
        try:
            nb = json.loads(path.read_text(encoding="utf-8"))
            for cell in nb.get("cells", []):
                if cell.get("cell_type") == "markdown":
                    src = "".join(cell.get("source", []))
                    m = _H.search(src)
                    if m:
                        return m.group(1), ""
        except (json.JSONDecodeError, OSError):
            pass
        return path.stem, ""
    # markdown
    text = path.read_text(encoding="utf-8")
    body = _FM.sub("", text)
    m = _H.search(body)
    title = m.group(1) if m else path.stem
    summary = ""
    for line in body.splitlines():
        s = line.strip()
        if not s or s[0] in "#>|!-*" or s.startswith("<!--") or s.startswith("```"):
            continue
        summary = clean_summary(s)
        if summary:
            break
    return title, summary[:240]


def emit(path: Path, category: str, moc: str, tag: str) -> Path:
    rel_to_repo = path.relative_to(REPO)
    out = STUBS / category / (slug(path.name) + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    rel_link = os.path.relpath(path, out.parent)
    title, summary = title_summary(path)
    safe_title = title.replace('"', "'")
    fm = [
        "---",
        f'title: "{safe_title}"',
        "type: kg/stub",
        "generated: true",
        "generator: atlas/_generate_stubs.py",
        "tags:",
        "  - kg",
        "  - kg/stub",
        f"  - kg/{tag}",
        "  - projeto/iconocracia",
        "related:",
        f'  - "[[{moc}]]"',
        "sources:",
        f"  - {rel_link}",
        f"created: {TODAY}",
        f"updated: {TODAY}",
        "---",
        "",
        f"# {title}",
        "",
        "> [!info] Nó-stub gerado automaticamente",
        f"> Resumo-âncora de [`{rel_to_repo}`]({rel_link}). **Edite a fonte**, não",
        "> este stub — ele é regenerado por `atlas/_generate_stubs.py`.",
        "",
    ]
    if summary:
        fm += [summary, ""]
    fm += [
        f"- **Fonte:** [`{rel_to_repo}`]({rel_link})",
        f"- **MOC:** [[{moc}]]",
        f"- **Categoria:** `{category}`",
        "",
    ]
    out.write_text("\n".join(fm), encoding="utf-8")
    return out


def main() -> None:
    if STUBS.exists():
        shutil.rmtree(STUBS)
    STUBS.mkdir(parents=True)

    by_cat: dict[str, list[tuple[str, str]]] = {}
    total = 0
    for category, moc, tag, globs in SURFACES:
        for g in globs:
            for path in sorted(REPO.glob(g)):
                if EXCLUDE.search(path.as_posix()):
                    continue
                out = emit(path, category, moc, tag)
                title, _ = title_summary(path)
                by_cat.setdefault(category, []).append((title, out.stem))
                total += 1

    # Índice dos stubs
    idx = [
        "---",
        "title: Stubs — Índice",
        "type: kg/moc",
        "generated: true",
        "generator: atlas/_generate_stubs.py",
        "tags:",
        "  - kg",
        "  - kg/stub",
        "  - meta/moc",
        "  - projeto/iconocracia",
        "related:",
        '  - "[[Iconocracia — Mapa Central]]"',
        f"created: {TODAY}",
        f"updated: {TODAY}",
        "---",
        "",
        "# Stubs — Índice",
        "",
        "Cobertura exaustiva auto-gerada das superfícies documentais do repo.",
        f"**{total} stubs** em {len(by_cat)} categorias. Regenerar:",
        "`python atlas/_generate_stubs.py`.",
        "",
        "> [!warning] Não editar à mão",
        "> Estes nós são regenerados. Para mudar o conteúdo, edite o arquivo-fonte;",
        "> para mudar a estrutura, edite o gerador.",
        "",
    ]
    for category in sorted(by_cat):
        idx.append(f"## `{category}` ({len(by_cat[category])})")
        idx.append("")
        for title, stem in sorted(by_cat[category]):
            idx.append(f"- [[{stem}|{title}]]")
        idx.append("")
    (STUBS / "Stubs — Índice.md").write_text("\n".join(idx), encoding="utf-8")

    print(f"Gerados {total} stubs em {len(by_cat)} categorias → {STUBS.relative_to(REPO)}/")
    for category in sorted(by_cat):
        print(f"  {category}: {len(by_cat[category])}")


if __name__ == "__main__":
    main()
