#!/usr/bin/env python3
"""
run_research_cluster.py — orquestrador de clusters temáticos de pesquisa.

Consome YAML validado contra tools/schemas/research-cluster.schema.json,
executa cascata Semantic Scholar → OpenAlex, aplica filtro disciplinar,
extrai campos tipados via Claude (abstract-only, NULL-se-ausente), e
renderiza notas Obsidian + CSV + sumário regenerável.

Uso:
  python tools/scripts/run_research_cluster.py <cluster.yaml> --stage search
  python tools/scripts/run_research_cluster.py <cluster.yaml> --stage extract
  python tools/scripts/run_research_cluster.py <cluster.yaml> --stage render
  python tools/scripts/run_research_cluster.py <cluster.yaml> --stage all

Stages idempotentes: state em <vault_root>/_generated/.state/*.jsonl.
Notas autorais com `manual_edits: true` NUNCA são sobrescritas.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    sys.exit("ERRO: PyYAML ausente. `conda run -n iconocracy pip install pyyaml`")

try:
    import requests
except ImportError:
    sys.exit("ERRO: requests ausente. `conda run -n iconocracy pip install requests`")

try:
    import jsonschema
except ImportError:
    sys.exit("ERRO: jsonschema ausente. `conda run -n iconocracy pip install jsonschema`")


# ---------- constantes ----------

USER_AGENT = "iconocracia-research-cluster/1.0 (mailto:ana.vanzin@posgrad.ufsc.br)"
S2_BASE = "https://api.semanticscholar.org/graph/v1"
OA_BASE = "https://api.openalex.org"
S2_RATE_SLEEP = 1.1
OPENALEX_RATE_SLEEP = 0.15
EXTRACT_MODEL = "claude-sonnet-4-5"
REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "tools" / "schemas" / "research-cluster.schema.json"


# ---------- modelos ----------

@dataclass
class Paper:
    dedup_key: str
    title: str
    year: int | None
    authors: list[str]
    abstract: str | None
    venue: str | None
    source: str  # "semantic_scholar" | "openalex"
    source_prompt_id: str
    citation_count: int = 0
    doi: str | None = None
    openalex_id: str | None = None
    s2_id: str | None = None
    url: str | None = None
    cluster_id: int = 0
    cluster_slug: str = ""
    extraction: dict[str, Any] = field(default_factory=dict)
    discipline_ok: bool | None = None
    discipline_reason: str | None = None


# ---------- helpers ----------

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:80] or "untitled"


def normalize_title(t: str) -> str:
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", t.lower())).strip()


def compute_dedup_key(doi: str | None, openalex_id: str | None, title: str, year: int | None) -> str:
    if doi:
        return f"doi:{doi.lower().strip()}"
    if openalex_id:
        return f"oa:{openalex_id.split('/')[-1]}"
    return f"tn:{normalize_title(title)}|{year or 0}"


def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def validate_cluster_doc(doc: dict) -> None:
    jsonschema.validate(doc, load_schema())


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def ensure_dirs(vault_root: Path, papers_sub: str, gen_sub: str) -> tuple[Path, Path, Path]:
    papers = vault_root / papers_sub
    generated = vault_root / gen_sub
    state = generated / ".state"
    for p in (papers, generated, state):
        p.mkdir(parents=True, exist_ok=True)
    return papers, generated, state


# ---------- Semantic Scholar ----------

S2_FIELDS = "paperId,title,year,authors.name,abstract,venue,citationCount,externalIds,openAccessPdf,url"


def s2_search(query: str, limit: int, year_range: tuple[int, int] | None, types: list[str] | None) -> list[dict]:
    params = {"query": query, "limit": min(limit, 100), "fields": S2_FIELDS}
    if year_range:
        params["year"] = f"{year_range[0]}-{year_range[1]}"
    if types:
        mapping = {"journal_article": "JournalArticle", "book": "Book", "book_chapter": "BookSection",
                   "conference_paper": "Conference", "thesis": "Thesis", "report": "Review"}
        mapped = [mapping[t] for t in types if t in mapping]
        if mapped:
            params["publicationTypes"] = ",".join(mapped)
    r = requests.get(f"{S2_BASE}/paper/search", params=params,
                     headers={"User-Agent": USER_AGENT}, timeout=30)
    if r.status_code == 429:
        time.sleep(60)
        return s2_search(query, limit, year_range, types)
    if not r.ok:
        return []
    time.sleep(S2_RATE_SLEEP)
    return r.json().get("data", []) or []


def parse_s2_paper(p: dict, prompt_id: str, cluster_id: int, cluster_slug: str) -> Paper | None:
    title = p.get("title") or ""
    if not title:
        return None
    year = p.get("year")
    doi = (p.get("externalIds") or {}).get("DOI")
    oa_id = None
    authors = [a.get("name", "") for a in (p.get("authors") or []) if a.get("name")]
    return Paper(
        dedup_key=compute_dedup_key(doi, oa_id, title, year),
        title=title, year=year, authors=authors,
        abstract=p.get("abstract"), venue=p.get("venue"),
        source="semantic_scholar", source_prompt_id=prompt_id,
        citation_count=p.get("citationCount") or 0,
        doi=doi, s2_id=p.get("paperId"),
        url=p.get("url") or ((p.get("openAccessPdf") or {}).get("url")),
        cluster_id=cluster_id, cluster_slug=cluster_slug,
    )


# ---------- OpenAlex ----------

def oa_search(query: str, limit: int, year_range: tuple[int, int] | None) -> list[dict]:
    filt = []
    if year_range:
        filt.append(f"from_publication_year:{year_range[0]}")
        filt.append(f"to_publication_year:{year_range[1]}")
    params = {"search": query, "per-page": min(limit, 50)}
    if filt:
        params["filter"] = ",".join(filt)
    r = requests.get(f"{OA_BASE}/works", params=params,
                     headers={"User-Agent": USER_AGENT}, timeout=30)
    if r.status_code == 429:
        time.sleep(60)
        return oa_search(query, limit, year_range)
    if not r.ok:
        return []
    time.sleep(OPENALEX_RATE_SLEEP)
    return r.json().get("results", []) or []


def reconstruct_abstract(inv: dict | None) -> str | None:
    if not inv:
        return None
    positions: list[tuple[int, str]] = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions) or None


def parse_oa_paper(w: dict, prompt_id: str, cluster_id: int, cluster_slug: str) -> Paper | None:
    title = w.get("title") or w.get("display_name") or ""
    if not title:
        return None
    doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
    oa_id = w.get("id")
    year = w.get("publication_year")
    authors = [a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or [])]
    authors = [a for a in authors if a]
    venue = (w.get("host_venue") or w.get("primary_location") or {}).get("display_name")
    abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
    return Paper(
        dedup_key=compute_dedup_key(doi, oa_id, title, year),
        title=title, year=year, authors=authors,
        abstract=abstract, venue=venue,
        source="openalex", source_prompt_id=prompt_id,
        citation_count=w.get("cited_by_count") or 0,
        doi=doi, openalex_id=oa_id,
        url=w.get("id"),
        cluster_id=cluster_id, cluster_slug=cluster_slug,
    )


# ---------- stage: search ----------

def stage_search(doc: dict, state_dir: Path, verbose: bool = True) -> list[Paper]:
    filt = doc.get("filtros_globais") or {}
    year_range = tuple(filt["anos"]) if filt.get("anos") else None
    types = filt.get("tipos")
    seen: dict[str, Paper] = {}

    for cluster in doc["clusters"]:
        cid = cluster["id"]
        cslug = cluster["slug"]
        limit = cluster.get("limite_papers", 50)
        prompts = cluster["prompts"] + [
            {"id": f"extra.{i}", "texto": b["query"]}
            for i, b in enumerate(cluster.get("buscas_extras") or [])
            if b.get("query")
        ]
        for pr in prompts:
            pid = pr["id"]
            q = pr["texto"]
            if verbose:
                print(f"[search] cluster={cid}/{cslug} prompt={pid} q={q[:80]!r}")
            for raw in s2_search(q, limit, year_range, types):
                p = parse_s2_paper(raw, pid, cid, cslug)
                if p and p.dedup_key not in seen:
                    seen[p.dedup_key] = p
            for raw in oa_search(q, limit, year_range):
                p = parse_oa_paper(raw, pid, cid, cslug)
                if p and p.dedup_key not in seen:
                    seen[p.dedup_key] = p

    papers = sorted(seen.values(), key=lambda x: (-x.citation_count, -(x.year or 0)))
    write_jsonl(state_dir / "search.jsonl", [asdict(p) for p in papers])
    if verbose:
        print(f"[search] total dedup'd = {len(papers)}")
    return papers


# ---------- stage: extract ----------

EXTRACTION_SYSTEM = """You are an abstract-only extractor for a legal-history thesis.

ABSOLUTE RULE: if the abstract does not explicitly contain the requested information, return NULL for that field. Do NOT infer, do NOT guess, do NOT use your training knowledge of the paper. Abstract-only.

Return a JSON object matching the requested schema exactly."""


def build_extraction_prompt(paper: Paper, schema: list[dict]) -> str:
    fields_txt = "\n".join(
        f"- {f['nome']} ({f['tipo']}): {f['instrucao']}" for f in schema
    )
    return f"""Paper:
Title: {paper.title}
Year: {paper.year}
Authors: {", ".join(paper.authors[:5])}
Abstract: {paper.abstract or "[NO ABSTRACT AVAILABLE]"}

Extract the following fields as JSON. Use null if the abstract does not contain the info.

{fields_txt}

Return ONLY a JSON object. No prose."""


def build_discipline_prompt(paper: Paper, disc_filter: str) -> str:
    return f"""Classifier for thesis inclusion.

Filter rule: {disc_filter}

Paper:
Title: {paper.title}
Abstract: {paper.abstract or "[NO ABSTRACT]"}

Return JSON: {{"ok": bool, "reason": "<one short sentence>"}}"""


def call_claude(system: str, user: str) -> dict:
    try:
        import anthropic
    except ImportError:
        sys.exit("ERRO: anthropic SDK ausente. `pip install anthropic`")
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=EXTRACT_MODEL, max_tokens=1024, system=system,
        messages=[{"role": "user", "content": user}],
    )
    txt = resp.content[0].text.strip()
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}


def stage_extract(doc: dict, state_dir: Path, limit: int | None = None, verbose: bool = True) -> list[Paper]:
    papers_raw = load_jsonl(state_dir / "search.jsonl")
    if not papers_raw:
        sys.exit("ERRO: rode --stage search primeiro.")
    existing = {r["dedup_key"]: r for r in load_jsonl(state_dir / "extracted.jsonl")}

    schema_by_cluster = {c["id"]: c["extraction_schema"] for c in doc["clusters"]}
    disc_filter = (doc.get("filtros_globais") or {}).get("disciplinary_filter")

    out: list[Paper] = []
    done = 0
    for row in papers_raw:
        key = row["dedup_key"]
        if key in existing:
            out.append(Paper(**{k: v for k, v in existing[key].items() if k in Paper.__annotations__}))
            continue
        if limit and done >= limit:
            # preserva extracted anteriores + sem-extração novos
            out.append(Paper(**{k: v for k, v in row.items() if k in Paper.__annotations__}))
            continue

        paper = Paper(**{k: v for k, v in row.items() if k in Paper.__annotations__})
        schema = schema_by_cluster.get(paper.cluster_id, [])
        if paper.abstract and schema:
            if verbose:
                print(f"[extract] {paper.title[:70]!r}")
            paper.extraction = call_claude(EXTRACTION_SYSTEM, build_extraction_prompt(paper, schema))
        if disc_filter and paper.abstract:
            dres = call_claude("You are a strict disciplinary classifier.",
                               build_discipline_prompt(paper, disc_filter))
            paper.discipline_ok = bool(dres.get("ok"))
            paper.discipline_reason = dres.get("reason")
        out.append(paper)
        done += 1

    write_jsonl(state_dir / "extracted.jsonl", [asdict(p) for p in out])
    if verbose:
        print(f"[extract] novos={done} total={len(out)}")
    return out


# ---------- stage: render ----------

PAPER_TEMPLATE = """---
title: "{title}"
year: {year}
authors: {authors_yaml}
doi: {doi}
openalex_id: {oa_id}
venue: "{venue}"
source: {source}
cluster_id: {cluster_id}
cluster_slug: {cluster_slug}
source_prompt_id: "{prompt_id}"
citation_count: {citations}
discipline_ok: {disc_ok}
tags: {tags_yaml}
manual_edits: false
---

# {title}

**Autores:** {authors_inline}
**Ano:** {year} · **Venue:** {venue}
**DOI:** {doi} · **Citações:** {citations}
**Fonte:** {source} (prompt `{prompt_id}`)
**Filtro disciplinar:** {disc_ok} — {disc_reason}

## Resumo

{abstract}

## Extração

{extraction_block}

## URL

{url}
"""


def yaml_list(xs: list[str]) -> str:
    if not xs:
        return "[]"
    return "[" + ", ".join(f'"{x}"' for x in xs) + "]"


def render_paper(p: Paper, tags: list[str]) -> str:
    ex_lines = []
    for k, v in (p.extraction or {}).items():
        ex_lines.append(f"- **{k}**: {v if v is not None else '_NULL_'}")
    return PAPER_TEMPLATE.format(
        title=p.title.replace('"', "'"),
        year=p.year or "null",
        authors_yaml=yaml_list(p.authors),
        authors_inline=", ".join(p.authors) or "—",
        doi=p.doi or "null",
        oa_id=p.openalex_id or "null",
        venue=(p.venue or "").replace('"', "'"),
        source=p.source,
        cluster_id=p.cluster_id,
        cluster_slug=p.cluster_slug,
        prompt_id=p.source_prompt_id,
        citations=p.citation_count,
        disc_ok="null" if p.discipline_ok is None else str(p.discipline_ok).lower(),
        disc_reason=p.discipline_reason or "—",
        tags_yaml=yaml_list(tags),
        abstract=p.abstract or "_[sem abstract]_",
        extraction_block="\n".join(ex_lines) or "_[sem extração]_",
        url=p.url or "—",
    )


def has_manual_edits(path: Path) -> bool:
    if not path.exists():
        return False
    head = path.read_text()[:2000]
    return bool(re.search(r"^manual_edits:\s*true", head, re.MULTILINE))


def stage_render(doc: dict, vault_root: Path, papers_sub: str, gen_sub: str,
                 state_dir: Path, verbose: bool = True) -> None:
    papers_dir, gen_dir, _ = ensure_dirs(vault_root, papers_sub, gen_sub)
    rows = load_jsonl(state_dir / "extracted.jsonl")
    if not rows:
        rows = load_jsonl(state_dir / "search.jsonl")
    tags_by_cluster = {c["id"]: c.get("tags_vault", []) for c in doc["clusters"]}

    written = skipped = 0
    csv_rows: list[dict] = []
    for row in rows:
        p = Paper(**{k: v for k, v in row.items() if k in Paper.__annotations__})
        slug = f"{p.cluster_slug}--{slugify(p.title)}"
        out = papers_dir / f"{slug}.md"
        if has_manual_edits(out):
            skipped += 1
        else:
            out.write_text(render_paper(p, tags_by_cluster.get(p.cluster_id, [])))
            written += 1
        csv_rows.append({
            "cluster_id": p.cluster_id, "cluster_slug": p.cluster_slug,
            "prompt_id": p.source_prompt_id, "title": p.title, "year": p.year,
            "doi": p.doi, "openalex_id": p.openalex_id, "venue": p.venue,
            "citations": p.citation_count, "source": p.source,
            "discipline_ok": p.discipline_ok, "url": p.url,
            **{f"x_{k}": v for k, v in (p.extraction or {}).items()},
        })

    if csv_rows:
        keys = sorted({k for r in csv_rows for k in r})
        with (gen_dir / "extracao.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(csv_rows)

    # sumário
    total = len(rows)
    by_year: dict[int, int] = {}
    disc_ok = disc_no = disc_null = 0
    for r in rows:
        y = r.get("year") or 0
        by_year[y] = by_year.get(y, 0) + 1
        d = r.get("discipline_ok")
        if d is True: disc_ok += 1
        elif d is False: disc_no += 1
        else: disc_null += 1
    sumario = [
        f"# Sumário — {doc['workflow_name']}",
        "",
        f"- **Total papers:** {total}",
        f"- **Escritos:** {written} · **Pulados (manual_edits):** {skipped}",
        f"- **Disciplinar ok/no/null:** {disc_ok}/{disc_no}/{disc_null}",
        "",
        "## Distribuição por ano",
        "",
    ]
    for y in sorted(by_year):
        sumario.append(f"- {y or '—'}: {by_year[y]}")
    (gen_dir / "_sumario.md").write_text("\n".join(sumario) + "\n")

    if verbose:
        print(f"[render] written={written} skipped={skipped} total={total}")


# ---------- CLI ----------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cluster_yaml", type=Path)
    ap.add_argument("--stage", choices=["search", "extract", "render", "all"], default="all")
    ap.add_argument("--extract-limit", type=int, default=None,
                    help="Cap de papers novos a extrair (controle de custo Claude)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    doc = load_yaml(args.cluster_yaml)
    validate_cluster_doc(doc)

    vault_root = REPO_ROOT / doc["destinos"]["vault_root"]
    papers_sub = doc["destinos"].get("papers_subdir", "papers/")
    gen_sub = doc["destinos"].get("generated_subdir", "_generated/")
    _, _, state_dir = ensure_dirs(vault_root, papers_sub, gen_sub)

    verbose = not args.quiet
    if args.dry_run:
        print(f"[dry-run] vault_root={vault_root} clusters={len(doc['clusters'])}")
        return

    if args.stage in ("search", "all"):
        stage_search(doc, state_dir, verbose)
    if args.stage in ("extract", "all"):
        stage_extract(doc, state_dir, args.extract_limit, verbose)
    if args.stage in ("render", "all"):
        stage_render(doc, vault_root, papers_sub, gen_sub, state_dir, verbose)


if __name__ == "__main__":
    main()
