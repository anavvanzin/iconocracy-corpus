#!/usr/bin/env python3
"""Auditable Elicit-to-corpus pipeline.

The pipeline keeps bibliographic discovery separate from visual-object corpus data.
Elicit literature rows can become source/dossier entries automatically; only rows
that explicitly describe concrete visual objects may become corpus candidates or
records.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

REPO = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO / "data" / "processed"
ELICIT_ROOT = REPO / "docs" / "research" / "elicit"
VAULT_CANDIDATES = REPO / "vault" / "candidatos"
RECORDS = DATA_DIR / "records.jsonl"
CORPUS_EXPORT = REPO / "corpus" / "corpus-data.json"
SOURCES_LEDGER = DATA_DIR / "elicit_sources.jsonl"
DECISIONS_LEDGER = DATA_DIR / "elicit_decisions.jsonl"

REQUIRED_COLUMNS = [
    "Title",
    "Abstract",
    "Authors",
    "DOI",
    "DOI link",
    "Venue",
    "Citation count",
    "Year",
    "Allegorical Specificity",
    'Reasoning for "Allegorical Specificity"',
    "Analytical Depth",
    'Reasoning for "Analytical Depth"',
    "Beyond Individual Women",
    'Reasoning for "Beyond Individual Women"',
    "Female Allegorical Focus",
    'Reasoning for "Female Allegorical Focus"',
    "Symbolic Paradox Analysis",
    'Reasoning for "Symbolic Paradox Analysis"',
    "Theoretical Framework",
    'Reasoning for "Theoretical Framework"',
    "Visual Political Culture",
    'Reasoning for "Visual Political Culture"',
    "Screening judgement",
    'Reasoning for "Screening judgement"',
    "Excluded by strict criterion",
    "Exclusion reason",
    "Screening score",
]

CRITERION_FIELDS = [
    "Allegorical Specificity",
    "Analytical Depth",
    "Beyond Individual Women",
    "Female Allegorical Focus",
    "Symbolic Paradox Analysis",
    "Theoretical Framework",
    "Visual Political Culture",
]
VISUAL_GATE_FIELDS = [
    "Allegorical Specificity",
    "Female Allegorical Focus",
    "Visual Political Culture",
]
VISUAL_TARGET_VALUES = {"visual_object", "corpus_candidate", "corpus", "object"}
COUNTRY_HINT_RE = re.compile(r"\b(Brazil|France|United States|Germany|United Kingdom|Belgium|Netherlands|Portugal|Italy|Austria|Spain|Switzerland|Uruguay|Mexico|Argentina)\b", re.I)


@dataclass(frozen=True)
class BatchPaths:
    batch_dir: Path
    manifest: Path
    sources: Path
    decisions: Path
    dossier: Path
    validation: Path
    candidates_dir: Path
    promote_plan: Path


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def slugify(value: str, max_len: int = 80) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value[:max_len].strip("-") or "batch")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_id(*parts: str, prefix: str = "ELICIT") -> str:
    raw = "||".join(p.strip() for p in parts if p and p.strip())
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def batch_paths(batch_dir: Path) -> BatchPaths:
    return BatchPaths(
        batch_dir=batch_dir,
        manifest=batch_dir / "manifest.json",
        sources=batch_dir / "elicit_sources.jsonl",
        decisions=batch_dir / "elicit_decisions.jsonl",
        dossier=batch_dir / "dossier.md",
        validation=batch_dir / "validation-report.md",
        candidates_dir=batch_dir / "candidates",
        promote_plan=batch_dir / "promote_plan.jsonl",
    )


def resolve_batch_dir(slug: str, date: str | None = None, batch_dir: str | None = None) -> Path:
    if batch_dir:
        return Path(batch_dir).resolve()
    return ELICIT_ROOT / f"{date or today()}-{slugify(slug)}"


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def upsert_jsonl(path: Path, rows: Sequence[dict], key: str) -> int:
    existing = {row[key]: row for row in read_jsonl(path) if key in row}
    for row in rows:
        existing[row[key]] = row
    ordered = sorted(existing.values(), key=lambda r: str(r.get(key, "")))
    return write_jsonl(path, ordered)


def normalize_answer(value: str) -> str:
    return (value or "").strip().lower()


def yes_or_maybe(value: str) -> bool:
    return normalize_answer(value) in {"yes", "maybe"}


def parse_score(value: str) -> float:
    value = (value or "").strip()
    if not value:
        return 0.0
    try:
        return float(value.replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"invalid Screening score: {value!r}") from exc


def traceable_url(row: dict[str, str]) -> str:
    return (row.get("DOI link") or row.get("DOI") or row.get("URL") or row.get("Url") or row.get("url") or "").strip()


def target_type(row: dict[str, str]) -> str:
    for name in ("Target type", "Corpus target type", "target_type", "Concrete target type"):
        value = normalize_answer(row.get(name, ""))
        if value:
            return value.replace("-", "_").replace(" ", "_")
    return "literature"


def is_visual_object(row: dict[str, str]) -> bool:
    return target_type(row) in VISUAL_TARGET_VALUES


def criterion_map(row: dict[str, str]) -> dict[str, str]:
    return {field: normalize_answer(row.get(field, "")) for field in CRITERION_FIELDS}


def is_high_confidence(row: dict[str, str]) -> bool:
    score = parse_score(row.get("Screening score", ""))
    judgement = normalize_answer(row.get("Screening judgement", ""))
    has_trace = bool(traceable_url(row))
    has_visual_signal = any(yes_or_maybe(row.get(field, "")) for field in VISUAL_GATE_FIELDS)
    return score >= 4.0 and judgement == "include" and has_trace and has_visual_signal


def classify_source(row: dict[str, str]) -> tuple[str, list[str]]:
    score = parse_score(row.get("Screening score", ""))
    judgement = normalize_answer(row.get("Screening judgement", ""))
    excluded = normalize_answer(row.get("Excluded by strict criterion", "")) in {"yes", "true", "1"}
    high = is_high_confidence(row)
    visual_object = is_visual_object(row)
    has_trace = bool(traceable_url(row))
    reasons: list[str] = []

    if excluded or judgement in {"exclude", "excluded", "reject", "rejected"}:
        reasons.append("strict exclusion or rejected screening judgement")
        return "reject", reasons
    if high and visual_object:
        reasons.append("high-confidence concrete visual object")
        return "candidate", reasons
    if high:
        reasons.append("high-confidence literature-only source row")
        return "include", reasons
    if visual_object:
        reasons.append("visual object declared but high-confidence gate not met")
        if not has_trace:
            reasons.append("missing DOI/URL")
        return "needs_verification", reasons
    if judgement == "include" and score >= 2.5:
        reasons.append("included by Elicit but below high-confidence gate")
        if not has_trace:
            reasons.append("missing DOI/URL")
        return "contextual", reasons
    if score >= 2.5:
        reasons.append("contextual score threshold met")
        return "contextual", reasons
    reasons.append("low score and no visual-object target")
    return "discarded", reasons


def validate_header(header: Sequence[str]) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    if missing:
        raise ValueError(f"Elicit CSV missing required columns: {', '.join(missing)}")


def load_elicit_csv(csv_path: Path, batch_id: str) -> tuple[list[dict], list[dict]]:
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        validate_header(reader.fieldnames or [])
        sources: list[dict] = []
        decisions: list[dict] = []
        seen_source_ids: dict[str, int] = {}
        for idx, row in enumerate(reader, 1):
            title = (row.get("Title") or "").strip()
            if not title:
                raise ValueError(f"row {idx} has empty Title")
            score = parse_score(row.get("Screening score", ""))
            base_source_id = stable_id(title, row.get("DOI", ""), row.get("DOI link", ""))
            duplicate_index = seen_source_ids.get(base_source_id, 0)
            seen_source_ids[base_source_id] = duplicate_index + 1
            source_id = base_source_id if duplicate_index == 0 else f"{base_source_id}-DUP{duplicate_index + 1:03d}"
            decision, reasons = classify_source(row)
            source = {
                "source_id": source_id,
                "base_source_id": base_source_id,
                "duplicate_of": base_source_id if duplicate_index else "",
                "batch_id": batch_id,
                "row_number": idx,
                "title": title,
                "abstract": (row.get("Abstract") or "").strip(),
                "authors": (row.get("Authors") or "").strip(),
                "doi": (row.get("DOI") or "").strip(),
                "doi_link": (row.get("DOI link") or "").strip(),
                "venue": (row.get("Venue") or "").strip(),
                "citation_count": (row.get("Citation count") or "").strip(),
                "year": (row.get("Year") or "").strip(),
                "screening_score": score,
                "screening_judgement": (row.get("Screening judgement") or "").strip(),
                "screening_rationale": (row.get('Reasoning for "Screening judgement"') or "").strip(),
                "excluded_by_strict_criterion": (row.get("Excluded by strict criterion") or "").strip(),
                "exclusion_reason": (row.get("Exclusion reason") or "").strip(),
                "target_type": target_type(row),
                "criteria": criterion_map(row),
                "rationales": {
                    col: (row.get(f'Reasoning for "{col}"') or "").strip()
                    for col in CRITERION_FIELDS
                }
                | {"screening": (row.get('Reasoning for "Screening judgement"') or "").strip()},
                "traceable_url": traceable_url(row),
                "high_confidence": is_high_confidence(row),
                "created_at": now_iso(),
            }
            sources.append(source)
            decisions.append(
                {
                    "decision_id": stable_id(batch_id, source_id, prefix="ELICIT-DECISION"),
                    "source_id": source_id,
                    "batch_id": batch_id,
                    "decision": decision,
                    "target_type": source["target_type"],
                    "high_confidence": source["high_confidence"],
                    "screening_score": score,
                    "reasons": reasons,
                    "rationale": "; ".join(reasons),
                    "evidence": {
                        "screening_judgement": source["screening_judgement"],
                        "screening_rationale": source["screening_rationale"],
                        "traceable_url": source["traceable_url"],
                    },
                    "requires_human_review": decision in {"needs_verification", "candidate"},
                    "decided_at": now_iso(),
                }
            )
    return sources, decisions


def ingest_files(batch_dir: Path, inputs: Sequence[Path], copy_raw: bool = False) -> dict:
    batch_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = batch_dir / "raw"
    seen: dict[str, str] = {}
    files = []
    for input_path in inputs:
        path = input_path.expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        digest = sha256_file(path)
        duplicate_of = seen.get(digest)
        copied_to = None
        if copy_raw and duplicate_of is None:
            raw_dir.mkdir(parents=True, exist_ok=True)
            target = raw_dir / path.name
            if target.exists() and sha256_file(target) != digest:
                target = raw_dir / f"{path.stem}-{digest[:8]}{path.suffix}"
            shutil.copy2(path, target)
            copied_to = str(target.relative_to(REPO)) if target.is_relative_to(REPO) else str(target)
        if duplicate_of is None:
            seen[digest] = path.name
        files.append(
            {
                "name": path.name,
                "source_path": str(path),
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "duplicate_of": duplicate_of,
                "copied_to": copied_to,
            }
        )
    manifest = {"created_at": now_iso(), "file_count": len(files), "files": files}
    atomic_write_text(batch_dir / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return manifest


def group_by_decision(sources: Sequence[dict], decisions: Sequence[dict]) -> dict[str, list[dict]]:
    by_source = {d["source_id"]: d for d in decisions}
    groups = {"core": [], "contextual": [], "candidate": [], "discarded": []}
    for source in sources:
        decision = by_source[source["source_id"]]["decision"]
        if decision == "include":
            groups["core"].append(source)
        elif decision in {"candidate", "needs_verification"}:
            groups["candidate"].append(source)
        elif decision == "contextual":
            groups["contextual"].append(source)
        else:
            groups["discarded"].append(source)
    return groups


def source_citation(source: dict) -> str:
    pieces = []
    if source.get("authors"):
        pieces.append(source["authors"])
    pieces.append(f"**{source['title']}**")
    if source.get("year"):
        pieces.append(str(source["year"]))
    if source.get("doi_link"):
        pieces.append(source["doi_link"])
    elif source.get("doi"):
        pieces.append(source["doi"])
    return ". ".join(pieces) + "."


def generate_dossier(batch_id: str, sources: Sequence[dict], decisions: Sequence[dict]) -> str:
    groups = group_by_decision(sources, decisions)
    lines = [
        "---",
        "documento: dossie-elicit",
        f"batch_id: {batch_id}",
        f"gerado_em: {now_iso()}",
        "status: triagem-gerada",
        "---",
        "",
        f"# Dossiê Elicit — {batch_id}",
        "",
        "> Literatura Elicit não é dado de corpus. Este dossiê separa fontes bibliográficas, candidatos visuais e descartes.",
        "",
    ]
    section_titles = {
        "core": "Fontes core",
        "contextual": "Fontes contextuais",
        "candidate": "Candidatos e verificações",
        "discarded": "Descartes justificados",
    }
    for key in ("core", "contextual", "candidate", "discarded"):
        lines += [f"## {section_titles[key]}", ""]
        if not groups[key]:
            lines += ["_Nenhum item nesta categoria._", ""]
            continue
        for source in groups[key]:
            decision = next(d for d in decisions if d["source_id"] == source["source_id"])
            lines += [
                f"### {source['title']}",
                "",
                f"- **ID**: `{source['source_id']}`",
                f"- **Decisão**: `{decision['decision']}`",
                f"- **Score**: {source['screening_score']}",
                f"- **Tipo alvo**: `{source['target_type']}`",
                f"- **DOI/URL**: {source.get('traceable_url') or 'ausente'}",
                f"- **Citação provisória**: {source_citation(source)}",
                f"- **Justificativa Elicit**: {source['rationales'].get('screening') or 'sem justificativa'}",
                "",
            ]
    return "\n".join(lines).rstrip() + "\n"


def country_hint(source: dict) -> str:
    text = " ".join([source.get("title", ""), source.get("abstract", "")])
    match = COUNTRY_HINT_RE.search(text)
    if match:
        return match.group(1)
    return "verificar"


def candidate_frontmatter(source: dict) -> dict[str, object]:
    high_confidence = bool(source.get("high_confidence")) and is_visual_target_source(source)
    status = "aprovado" if high_confidence else "verificar"
    return {
        "id": source["source_id"],
        "tipo": "corpus/candidato",
        "status": status,
        "titulo": source["title"],
        "url": source.get("traceable_url") or source.get("doi_link") or source.get("doi") or "",
        "pais": country_hint(source),
        "suporte": "verificar",
        "tags": ["corpus/candidato", "fonte/elicit", f"status/{status}"],
        "fonte_analise": "Elicit pipeline v1",
        "data_analise": today(),
        "elicit_source_id": source["source_id"],
        "target_type": source["target_type"],
        "screening_score": source["screening_score"],
    }


def dump_frontmatter(fm: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in fm.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            escaped = str(value).replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    return "\n".join(lines)


def candidate_note(source: dict) -> str:
    fm = candidate_frontmatter(source)
    return (
        f"{dump_frontmatter(fm)}\n\n"
        f"# {source['title']}\n\n"
        "## Resumo da fonte\n\n"
        f"{source.get('abstract') or 'Resumo ausente no CSV Elicit.'}\n\n"
        "## Relevância para ICONOCRACIA\n\n"
        f"- Score Elicit: {source['screening_score']}\n"
        f"- Julgamento Elicit: {source.get('screening_judgement') or 'n/a'}\n"
        f"- Tipo alvo: `{source['target_type']}`\n"
        f"- Racional de triagem: {source['rationales'].get('screening') or 'sem justificativa'}\n\n"
        "## Citação ABNT provisória\n\n"
        f"{source_citation(source)}\n\n"
        "## Verificação necessária\n\n"
        "> [!warning] Verificar\n"
        "> Candidato gerado a partir de triagem Elicit. Confirmar DOI/URL, objeto visual concreto, metadados iconográficos e aderência ao codebook antes de promoção canônica.\n"
    )


def write_candidate_notes(sources: Sequence[dict], decisions: Sequence[dict], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions_by_source = {d["source_id"]: d for d in decisions}
    written: list[Path] = []
    for source in sources:
        decision = decisions_by_source[source["source_id"]]["decision"]
        if decision not in {"candidate", "needs_verification"}:
            continue
        if not is_visual_target_source(source):
            continue
        filename = f"{source['source_id']} {slugify(source['title'], 70)}.md"
        path = output_dir / filename
        atomic_write_text(path, candidate_note(source))
        written.append(path)
    return written


def is_visual_target_source(source: dict) -> bool:
    return normalize_answer(str(source.get("target_type", ""))) in VISUAL_TARGET_VALUES


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if not line or line.startswith("  - ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip().strip('"')
    return fm


def load_existing_record_keys(path: Path = RECORDS) -> set[str]:
    keys: set[str] = set()
    for row in read_jsonl(path):
        inp = row.get("input") or {}
        if inp.get("input_url"):
            keys.add(str(inp["input_url"]).strip())
        if inp.get("title_hint"):
            keys.add(str(inp["title_hint"]).strip().lower())
    return keys


def master_record_from_candidate(fm: dict[str, str]) -> dict:
    title = fm.get("titulo") or fm.get("title") or fm.get("id") or "Elicit candidate"
    url = fm.get("url") or f"https://iconocracy.corpus/placeholder/{fm.get('id', stable_id(title))}"
    item_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"iconocracy-elicit-{fm.get('id', title)}"))
    now = now_iso()
    return {
        "master_record_version": "1.0",
        "batch_id": "00000000-1c0c-4842-8a1a-elicit000001",
        "item_id": item_uuid,
        "item_hash": hashlib.sha256(f"{url}||{title}".encode("utf-8")).hexdigest()[:16],
        "input": {
            "input_url": url,
            "title_hint": title,
            "date_hint": fm.get("data") or fm.get("periodo") or "",
            "place_hint": fm.get("pais") or "verificar",
        },
        "webscout": {
            "search_results": [
                {
                    "evidence_id": "elicit-v1",
                    "source_type": "primary_image",
                    "title": title,
                    "url": url,
                    "abnt_citation": title,
                    "iconclass_candidates": [],
                    "notes": f"Auto-promoted from Elicit candidate {fm.get('id', '')}",
                }
            ],
            "summary_evidence": title,
            "gaps": ["metadados visuais importados de Elicit exigem revisão humana"],
        },
        "iconocode": {
            "pre_iconographic": [{"motif": "Figura alegórica", "observed": True}],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.65,
        },
        "exports": {
            "abnt_citations": [],
            "audit_flags": ["elicit-import", "auto-promoted-high-confidence", "requires-human-review"],
        },
        "timestamps": {"created_at": now, "updated_at": now},
    }


def promote_candidates(candidates_dir: Path, apply: bool = False, records_path: Path = RECORDS) -> list[dict]:
    existing_keys = load_existing_record_keys(records_path)
    planned: list[dict] = []
    for note in sorted(candidates_dir.glob("*.md")):
        fm = parse_simple_frontmatter(note.read_text(encoding="utf-8"))
        status = normalize_answer(fm.get("status", ""))
        target = normalize_answer(fm.get("target_type", ""))
        if status not in {"aprovado", "approved", "auto-promote"}:
            continue
        if target not in VISUAL_TARGET_VALUES:
            continue
        record = master_record_from_candidate(fm)
        inp = record["input"]
        if inp["input_url"] in existing_keys or inp["title_hint"].lower() in existing_keys:
            continue
        planned.append(record)
    if apply and planned:
        with records_path.open("a", encoding="utf-8") as f:
            for record in planned:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        subprocess.run([sys.executable, str(REPO / "tools" / "scripts" / "records_to_corpus.py")], check=True)
    return planned


def cmd_ingest(args: argparse.Namespace) -> int:
    batch_dir = resolve_batch_dir(args.slug, args.date, args.batch_dir)
    manifest = ingest_files(batch_dir, [Path(p) for p in args.inputs], copy_raw=args.copy_raw)
    print(f"Manifest written: {batch_dir / 'manifest.json'} ({manifest['file_count']} files)")
    return 0


def cmd_triage(args: argparse.Namespace) -> int:
    batch_dir = resolve_batch_dir(args.slug, args.date, args.batch_dir)
    paths = batch_paths(batch_dir)
    batch_id = batch_dir.name
    sources, decisions = load_elicit_csv(Path(args.csv), batch_id=batch_id)
    write_jsonl(paths.sources, sources)
    write_jsonl(paths.decisions, decisions)
    upsert_jsonl(SOURCES_LEDGER, sources, "source_id")
    upsert_jsonl(DECISIONS_LEDGER, decisions, "decision_id")
    print(f"Triaged {len(sources)} rows into {paths.sources}")
    return 0


def cmd_dossier(args: argparse.Namespace) -> int:
    paths = batch_paths(Path(args.batch_dir).resolve())
    sources = read_jsonl(paths.sources)
    decisions = read_jsonl(paths.decisions)
    if not sources or not decisions:
        raise SystemExit("run triage before dossier")
    atomic_write_text(paths.dossier, generate_dossier(paths.batch_dir.name, sources, decisions))
    print(f"Dossier written: {paths.dossier}")
    return 0


def cmd_candidates(args: argparse.Namespace) -> int:
    paths = batch_paths(Path(args.batch_dir).resolve())
    sources = read_jsonl(paths.sources)
    decisions = read_jsonl(paths.decisions)
    output = Path(args.output_dir).resolve() if args.output_dir else paths.candidates_dir
    notes = write_candidate_notes(sources, decisions, output)
    print(f"Candidate notes written: {len(notes)}")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    paths = batch_paths(Path(args.batch_dir).resolve())
    candidates_dir = Path(args.candidates_dir).resolve() if args.candidates_dir else paths.candidates_dir
    planned = promote_candidates(candidates_dir, apply=args.apply)
    write_jsonl(paths.promote_plan, planned)
    verb = "Promoted" if args.apply else "Planned"
    print(f"{verb} {len(planned)} records; plan: {paths.promote_plan}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    paths = batch_paths(Path(args.batch_dir).resolve())
    sources = read_jsonl(paths.sources)
    decisions = read_jsonl(paths.decisions)
    source_ids = [s.get("source_id") for s in sources]
    duplicate_ids = sorted({sid for sid in source_ids if source_ids.count(sid) > 1})
    unresolved = [d for d in decisions if d.get("decision") in {"candidate", "needs_verification"}]
    missing_trace = [s for s in sources if not s.get("traceable_url")]
    report = [
        f"# Validation report — {paths.batch_dir.name}",
        "",
        f"- Sources: {len(sources)}",
        f"- Decisions: {len(decisions)}",
        f"- Duplicate source IDs: {len(duplicate_ids)}",
        f"- Unresolved review items: {len(unresolved)}",
        f"- Missing DOI/URL: {len(missing_trace)}",
        "",
    ]
    if duplicate_ids:
        report += ["## Duplicate IDs", "", *[f"- `{sid}`" for sid in duplicate_ids], ""]
    if unresolved:
        report += ["## Review queue", "", *[f"- `{d['source_id']}`: {d['decision']}" for d in unresolved], ""]
    atomic_write_text(paths.validation, "\n".join(report))
    print(f"Validation report written: {paths.validation}")
    return 1 if duplicate_ids else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="register/copy raw Elicit batch files")
    ingest.add_argument("--slug", required=True)
    ingest.add_argument("--date")
    ingest.add_argument("--batch-dir")
    ingest.add_argument("--copy-raw", action="store_true")
    ingest.add_argument("inputs", nargs="+")
    ingest.set_defaults(func=cmd_ingest)

    triage = sub.add_parser("triage", help="normalize the 27-column Elicit CSV")
    triage.add_argument("--csv", required=True)
    triage.add_argument("--slug", required=True)
    triage.add_argument("--date")
    triage.add_argument("--batch-dir")
    triage.set_defaults(func=cmd_triage)

    dossier = sub.add_parser("dossier", help="generate dossier Markdown")
    dossier.add_argument("--batch-dir", required=True)
    dossier.set_defaults(func=cmd_dossier)

    candidates = sub.add_parser("candidates", help="generate vault candidate notes")
    candidates.add_argument("--batch-dir", required=True)
    candidates.add_argument("--output-dir")
    candidates.set_defaults(func=cmd_candidates)

    promote = sub.add_parser("promote", help="promote approved visual-object candidates")
    promote.add_argument("--batch-dir", required=True)
    promote.add_argument("--candidates-dir")
    promote.add_argument("--apply", action="store_true")
    promote.set_defaults(func=cmd_promote)

    validate = sub.add_parser("validate", help="write batch validation report")
    validate.add_argument("--batch-dir", required=True)
    validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
