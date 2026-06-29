#!/usr/bin/env python3
"""Ingest LPAI v2 ficha catalográfica DOCX into staging artifacts.

T4 (staging phase): parses 15 LPAI v2 fichas from the SCOUT campaign DOCX,
writes JSONL stubs shaped for `master-record.schema.json`, plus per-ficha
draft Obsidian notes. Runs dedup against `corpus/corpus-data.json` and
`data/processed/records.jsonl`. All writes go under `data/staging/` —
canonical files (`records.jsonl`, `corpus-data.json`, `vault/candidatos/`,
`data/processed/purification.jsonl`) are *never* touched.

Exit codes:
    0  success (all fichas parsed + validated)
    1  parse error or IO error (nothing written)
    2  at least one ficha failed master-record validation (staging still
       written; caller reviews `docs/T4-LPAI-INGEST-REPORT.md`)

The companion script `tools/scripts/records_to_corpus.py` is the merge
path the human runs *after* reviewing the staging outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urlsplit, urlunsplit

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DOCX = Path("/Users/ana/Downloads/Documents/Fichas_LPAI_v2_Campanha_SCOUT_BR_FR.docx")
DEFAULT_STAGE_DIR = REPO_ROOT / "data" / "staging"
STAGING_JSONL_NAME = "fichas-lpai-v2-parsed.jsonl"
STAGING_DRAFTS_DIR_NAME = "vault-drafts-lpai-v2"
STAGING_IMAGES_SUBDIR = "_images"

LPAI_NAMESPACE = uuid.UUID("f5b4c8a0-1cd2-4e5f-b0a3-1f0a1c0d2e3f")  # deterministic batch
BATCH_ID_FALLBACK = "00000000-0000-4000-8000-lpaiv2scout0001"

# Field labels we extract verbatim from the DOCX tables. These are the
# uniform field keys of the LPAI v2 ficha format (discovered empirically
# from the DOCX — 15/15 fichas use them).
LPAI_FIELDS = {
    "id": "ID",
    "title": "Título",
    "creator": "Autoria",
    "date": "Data",
    "source": "Fonte",
    "url": "URL",
    "url_download": "URL download",
    "support": "Suporte",
    "dimensions": "Dimensões",
    "lpai_code": "CÓDIGO LPAI v2",
    "classe": "CLASSE",
    "atributos": "ATRIBUTOS",
    "iconclass": "ICONCLASS",
    "regime": "REGIME",
    "modo": "MODO",
    "nota_analitica": "NOTA ANALÍTICA",
    "ref_abnt": "REF. ABNT",
}

# Optional fields only present in the "complete" ficha (BR-SCOUT-005, 24-row FR fichas)
LPAI_OPTIONAL_FIELDS = {
    "corpo": "CORPO (B)",
    "medium_sub": "MÉDIUM (M)",
    "contexto": "CONTEXTO (P)",
    "genero": "GÊNERO (G)",
    "nacional_ext": "NACIONAL (+)",
    "satirico_ext": "SATÍRICO (+)",
    "comp_flag": "COMP",
}

SEPARATOR_MARKERS = {"═══  LPAI v2 RECORD  ═══", "───────────────────"}

# Placeholder URL used when a ficha has no URL. Master-record + webscout-output
# schemas both require `format: uri`, so we cannot leave it empty. The
# companion `placeholder_url_BLOCK_PROMOTE` audit flag acts as an all-caps,
# grep-clean marker so downstream promote tooling can refuse to merge these
# records until a real URL lands.
PLACEHOLDER_URL = "https://example.org/lpai-placeholder"

# Known archive hosts whose http/https variants describe the same resource.
# Used by `_canonicalize_url` to coerce `http` → `https` before matching, so
# pre-2018 legacy links in `corpus-data.json` collide with current https ones.
KNOWN_ARCHIVE_HOSTS = frozenset(
    {
        "gallica.bnf.fr",
        "europeana.eu",
        "loc.gov",
        "numista.com",
        "bildindex.de",
        "rijksmuseum.nl",
        "bn.gov.br",
        "bndigital.bnportugal.gov.pt",
    }
)


# ---------------------------------------------------------------------------
# DOCX parsing
# ---------------------------------------------------------------------------
def _import_docx():
    try:
        from docx import Document  # type: ignore
    except ImportError as exc:  # pragma: no cover
        print(
            "Error: python-docx is required. Install with: pip install python-docx",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    return Document


def is_ficha_table(table) -> bool:
    """Heuristic: a ficha table starts with a 'LPAI v2 RECORD' banner row
    and has a 2-column structure with 'ID' as second row's first cell.
    """
    if len(table.columns) != 2 or len(table.rows) < 5:
        return False
    try:
        header = table.rows[0].cells[0].text.strip()
        first_field = table.rows[1].cells[0].text.strip()
    except IndexError:
        return False
    return "LPAI v2 RECORD" in header and first_field == "ID"


def parse_ficha_table(table) -> Dict[str, Any]:
    """Extract a single ficha's fields from a 2-column table.

    Returns a dict keyed by canonical LPAI field names (from LPAI_FIELDS +
    LPAI_OPTIONAL_FIELDS). Separator/banner rows are skipped. Unknown
    labels land under `extra` so nothing is silently dropped.
    """
    fields: Dict[str, str] = {}
    extra: Dict[str, str] = {}
    label_to_key = {v: k for k, v in LPAI_FIELDS.items()}
    label_to_key.update({v: k for k, v in LPAI_OPTIONAL_FIELDS.items()})

    for row in table.rows:
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 2:
            continue
        label, value = cells[0], cells[1]
        if not label or label in SEPARATOR_MARKERS:
            continue
        # Same-cell duplicates (separator row echoes across both cells)
        if label == value and label.startswith("═"):
            continue
        key = label_to_key.get(label)
        if key is None:
            extra[label] = value
        else:
            fields[key] = value

    if extra:
        fields["_extra"] = json.dumps(extra, ensure_ascii=False)
    return fields


def parse_docx(docx_path: Path) -> List[Dict[str, Any]]:
    Document = _import_docx()
    doc = Document(str(docx_path))
    fichas: List[Dict[str, Any]] = []
    for idx, table in enumerate(doc.tables):
        if is_ficha_table(table):
            f = parse_ficha_table(table)
            f["_docx_table_index"] = idx
            fichas.append(f)
    return fichas


# ---------------------------------------------------------------------------
# Normalization / mapping to master-record shape
# ---------------------------------------------------------------------------
def infer_country_from_id(ficha_id: str) -> Optional[str]:
    m = re.match(r"^([A-Z]{2})-", ficha_id or "")
    return m.group(1) if m else None


def country_code_to_name(code: str) -> str:
    return {
        "BR": "Brasil",
        "FR": "França",
        "UK": "Reino Unido",
        "DE": "Alemanha",
        "US": "Estados Unidos",
        "BE": "Bélgica",
    }.get(code, code)


YEAR_RE = re.compile(r"\b(1[789]\d{2}|20\d{2})\b")


def extract_year(date_str: str) -> Optional[int]:
    if not date_str:
        return None
    m = YEAR_RE.search(date_str)
    return int(m.group(1)) if m else None


REGIME_RE = re.compile(r"(FUNDACIONAL|NORMATIVO|MILITAR)", re.IGNORECASE)


def normalize_regime(regime_str: str) -> Optional[str]:
    if not regime_str:
        return None
    m = REGIME_RE.search(regime_str)
    if not m:
        return None
    base = m.group(1).lower()
    # contra-alegoria hint
    if "contra" in regime_str.lower() or "+730" in regime_str:
        return "contra-alegoria"
    return base


def build_abnt_from_ficha(f: Dict[str, Any]) -> List[str]:
    citations = []
    if f.get("ref_abnt"):
        citations.append(f["ref_abnt"].strip())
    return citations


def item_hash_for(ficha: Dict[str, Any]) -> str:
    seed = json.dumps(
        {
            "id": ficha.get("id", ""),
            "title": ficha.get("title", ""),
            "url": ficha.get("url", ""),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def item_uuid_for(ficha: Dict[str, Any]) -> str:
    return str(uuid.uuid5(LPAI_NAMESPACE, ficha.get("id", "") + "|" + ficha.get("url", "")))


def build_staging_record(
    ficha: Dict[str, Any],
    *,
    batch_id: str,
    now_iso: str,
) -> Dict[str, Any]:
    """Build a master-record-shaped dict for staging.

    The LPAI ficha doesn't natively carry WebScout search evidence or
    IconoCode analysis; we synthesize minimal stubs that validate against
    the schema so the human can promote without an extra transform step.
    Coders still need to populate `purificacao` via IconoCode — that's
    the T3 queue.
    """
    ficha_id = ficha.get("id", "").strip()
    url = (ficha.get("url") or ficha.get("url_download") or "").strip()
    title = ficha.get("title", "").strip()
    country_code = infer_country_from_id(ficha_id)
    place_hint = country_code_to_name(country_code) if country_code else ""

    abnt_list = build_abnt_from_ficha(ficha)
    audit_flags: List[str] = []
    url_for_record = url or PLACEHOLDER_URL
    if not url:
        audit_flags.append("missing_url")
        # All-caps, grep-clean marker so a downstream promote step can refuse
        # to merge placeholder-URL records into the canonical ledger.
        audit_flags.append("placeholder_url_BLOCK_PROMOTE")
    if not title:
        audit_flags.append("missing_title")
    if ficha.get("_extra"):
        audit_flags.append("extra_fields_present")
    audit_flags.append("lpai_v2_ingest")

    iconclass_candidates: List[str] = []
    raw_iconclass = ficha.get("iconclass", "")
    for tok in re.findall(r"[0-9]{2}[A-Z][0-9]*[A-Z]?[0-9]*", raw_iconclass or ""):
        if tok and tok not in iconclass_candidates:
            iconclass_candidates.append(tok)

    webscout_stub = {
        "search_results": [
            {
                "evidence_id": "lpai-src",
                "source_type": "primary_image",
                "title": title or ficha_id,
                "url": url_for_record,
                "abnt_citation": abnt_list[0]
                if abnt_list
                else f"[{ficha_id}] sem ABNT no ficha v2.",
                "iconclass_candidates": iconclass_candidates,
                "notes": "Imported from LPAI v2 ficha; human-authored evidence.",
            }
        ],
        "summary_evidence": (
            ficha.get("nota_analitica", "").strip()
            or f"Ficha LPAI v2 {ficha_id}: {title}"
        ),
        "gaps": [g for g in (
            "pending_iconocode_coding" if not ficha.get("_coded") else None,
        ) if g],
    }

    iconocode_stub = {
        "pre_iconographic": [],
        "codes": [
            {
                "scheme": "iconclass",
                "notation": tok,
                "code_role": "depicts",
                "confidence": 0.5,
                "evidence_source_id": "lpai-src",
            }
            for tok in iconclass_candidates
        ],
        "interpretation": [
            {
                "claim_text": f"Regime {normalize_regime(ficha.get('regime','')) or 'nao-classificado'} "
                              f"(LPAI v2 classe {ficha.get('classe','?')}).",
                "claim_type": "iconographic",
                "status": "tentative",
                "confidence": 0.5,
            }
        ],
        "validation": {"claim_ledger": []},
        "confidence": 0.5,
    }

    record: Dict[str, Any] = {
        "master_record_version": "1.0",
        "batch_id": batch_id,
        "item_id": item_uuid_for(ficha),
        "item_hash": item_hash_for(ficha),
        "input": {
            "input_url": url_for_record,
            "title_hint": title,
            "date_hint": ficha.get("date", ""),
            "place_hint": place_hint,
        },
        "webscout": webscout_stub,
        "iconocode": iconocode_stub,
        "exports": {
            "abnt_citations": abnt_list,
            "audit_flags": audit_flags,
        },
        "timestamps": {"created_at": now_iso, "updated_at": now_iso},
    }
    return record


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------
def _normalize_title(s: str) -> str:
    import unicodedata

    s = (s or "").lower().strip()
    # Strip diacritics so 'república' matches 'republica'
    s = "".join(
        ch for ch in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(ch)
    )
    s = re.sub(r"[—–\-_,.;:!?\"']", " ", s)
    # Strip parenthetical content so "La République aimable (Félicien Rops)"
    # reduces to "la republique aimable" for substring matching.
    s = re.sub(r"\([^)]*\)", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _canonicalize_url(url: str) -> str:
    """Canonicalize a URL so http/https and www/non-www variants collide.

    Rules:
    - lowercase host, strip leading `www.`
    - drop trailing `/` on the path (unless the path is the sole `/`)
    - force `https` scheme when the host (bare, minus `www.`) matches a
      known archive host in `KNOWN_ARCHIVE_HOSTS`
    - preserve query and fragment
    - if the input is not a parseable URL or has no host, return it
      stripped of trailing slash / lowercased-ish (best effort)
    """
    if not url:
        return ""
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return url.strip().rstrip("/")
    scheme = (parts.scheme or "").lower()
    host = (parts.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    # Force https on known archive hosts — matches `host` itself or any
    # suffix-match like `en.numista.com` against `numista.com`.
    if scheme == "http" and host:
        for known in KNOWN_ARCHIVE_HOSTS:
            if host == known or host.endswith("." + known):
                scheme = "https"
                break
    path = parts.path or ""
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, host, path, parts.query, parts.fragment))


# Minimum length for the title-substring dedup pass. Guards against the
# shortest substrings collapsing to "a" / "the" / "la" and matching every
# item in the corpus.
TITLE_SUBSTRING_MIN_CHARS = 8


@dataclass
class DedupIndex:
    url_to_id: Dict[str, str] = field(default_factory=dict)
    title_to_id: Dict[str, str] = field(default_factory=dict)
    ids: set = field(default_factory=set)

    @classmethod
    def from_files(cls, corpus_json: Path, records_jsonl: Path) -> "DedupIndex":
        idx = cls()
        if corpus_json.exists():
            with corpus_json.open("r", encoding="utf-8") as f:
                for item in json.load(f):
                    iid = item.get("id") or ""
                    if iid:
                        idx.ids.add(iid)
                    url = _canonicalize_url(item.get("url") or "")
                    if url and url not in idx.url_to_id:
                        idx.url_to_id[url] = iid
                    t = _normalize_title(item.get("title", ""))
                    if t and t not in idx.title_to_id:
                        idx.title_to_id[t] = iid
        if records_jsonl.exists():
            with records_jsonl.open("r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    iid = rec.get("item_id") or ""
                    if iid:
                        idx.ids.add(iid)
                    inp = rec.get("input") or {}
                    url = _canonicalize_url(inp.get("input_url") or "")
                    if url and url not in idx.url_to_id:
                        idx.url_to_id[url] = iid
                    t = _normalize_title(inp.get("title_hint", ""))
                    if t and t not in idx.title_to_id:
                        idx.title_to_id[t] = iid
        return idx

    def classify(
        self, ficha_id: str, url: str, title: str
    ) -> Tuple[str, Optional[str], List[str]]:
        """Return (status, matched_existing_id, signals) where status is:
        'NEW' | 'MATCHES' | 'PARTIAL'.

        `signals` is a list of the signal names that hit — one of:
        `id`, `url`, `title_exact`, `title_substring`. Exposed so the
        dedup report can distinguish weak (title_substring) from strong
        (title_exact) title matches.
        """
        hits: List[Tuple[str, str]] = []
        if ficha_id and ficha_id in self.ids:
            hits.append(("id", ficha_id))
        canon_url = _canonicalize_url(url)
        if canon_url and canon_url in self.url_to_id:
            hits.append(("url", self.url_to_id[canon_url]))
        nt = _normalize_title(title)
        title_signal_kind: Optional[str] = None
        if nt and nt in self.title_to_id:
            hits.append(("title_exact", self.title_to_id[nt]))
            title_signal_kind = "title_exact"
        elif nt and len(nt) >= TITLE_SUBSTRING_MIN_CHARS:
            # Second pass: title substring match. Iterates the (small,
            # ~200 entries) title index and promotes weaker similarity.
            for stored, stored_id in self.title_to_id.items():
                if len(stored) < TITLE_SUBSTRING_MIN_CHARS:
                    continue
                if nt in stored or stored in nt:
                    hits.append(("title_substring", stored_id))
                    title_signal_kind = "title_substring"
                    break
        if not hits:
            return "NEW", None, []
        signals = [name for name, _ in hits]
        if len(hits) == 1:
            return "PARTIAL", hits[0][1], signals
        # ≥2 orthogonal signals → strong match
        return "MATCHES", hits[0][1], signals


# ---------------------------------------------------------------------------
# Vault draft rendering
# ---------------------------------------------------------------------------
def _slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9À-ÿ\- ]", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s[:80]


def render_vault_draft(ficha: Dict[str, Any], record: Dict[str, Any]) -> Tuple[str, str]:
    """Return (filename, markdown_body) for a draft Obsidian note."""
    ficha_id = ficha.get("id", "UNKNOWN")
    title = ficha.get("title", "Sem título")
    filename = f"{ficha_id} {_slug(title)}.md".strip().replace("  ", " ")
    country_code = infer_country_from_id(ficha_id) or ""
    regime = normalize_regime(ficha.get("regime", "")) or "nao-classificado"

    tags: List[str] = [
        "corpus/candidato",
        f"pais/{country_code}" if country_code else "",
        f"regime/{regime}",
        "fonte/lpai-v2",
    ]
    tags = [t for t in tags if t]

    abnt = ficha.get("ref_abnt", "").strip()
    note = ficha.get("nota_analitica", "").strip()
    url = ficha.get("url", "").strip()
    url_dl = ficha.get("url_download", "").strip()
    today = datetime.now(timezone.utc).date().isoformat()

    lines = [
        "---",
        f'title: "{title}"',
        f"id: {ficha_id}",
        f"aliases: []",
        "tags:",
    ]
    for t in tags:
        lines.append(f"  - {t}")
    lines.extend(
        [
            f"status: staging-lpai-v2",
            f"pais: {country_code_to_name(country_code) if country_code else ''}",
            f"data: {ficha.get('date','')}",
            f"autor: {ficha.get('creator','')}",
            f"suporte: {ficha.get('support','')}",
            f"fonte: {ficha.get('source','')}",
            f"url: {url}",
            f"url_download: {url_dl}",
            f"regime: {regime}",
            f"modo: {ficha.get('modo','')}",
            f"iconclass: {ficha.get('iconclass','')}",
            f"lpai_v2_code: {ficha.get('lpai_code','')}",
            f"created: {today}",
            f"updated: {today}",
            "---",
            "",
            f"# {title}",
            "",
            "> [!note] LPAI v2 — ficha em staging",
            f"> Gerada por `tools/scripts/ingest_fichas_lpai.py` em {today}.",
            "> Revise antes de promover a `vault/candidatos/`.",
            "",
            "## Metadados",
            "",
            f"- **ID proposto:** `{ficha_id}`",
            f"- **Autoria:** {ficha.get('creator','—')}",
            f"- **Data:** {ficha.get('date','—')}",
            f"- **Fonte:** {ficha.get('source','—')}",
            f"- **Suporte:** {ficha.get('support','—')}",
            f"- **Dimensões:** {ficha.get('dimensions','—')}",
            f"- **URL:** {url or '—'}",
            f"- **URL download:** {url_dl or '—'}",
            "",
            "## Classificação LPAI v2",
            "",
            f"- **Código LPAI v2:** `{ficha.get('lpai_code','—')}`",
            f"- **Classe:** {ficha.get('classe','—')}",
            f"- **Atributos:** {ficha.get('atributos','—')}",
            f"- **Iconclass:** {ficha.get('iconclass','—')}",
            f"- **Regime:** {ficha.get('regime','—')}",
            f"- **Modo:** {ficha.get('modo','—')}",
        ]
    )
    for opt_key, label in LPAI_OPTIONAL_FIELDS.items():
        val = ficha.get(opt_key)
        if val:
            lines.append(f"- **{label}:** {val}")
    lines.extend(
        [
            "",
            "## Análise Panofsky (stub — a ser preenchida por IconoCode)",
            "",
            "### 1. Pré-iconográfica",
            "",
            "- [ ] Motivos observáveis",
            "",
            "### 2. Iconográfica",
            "",
            "- [ ] Códigos Iconclass confirmados",
            "",
            "### 3. Iconológica",
            "",
            "- [ ] Claims, status, evidência",
            "",
            "## Nota analítica (LPAI v2)",
            "",
            note or "_Não fornecida na ficha._",
            "",
            "## Indicadores de endurecimento (pendente)",
            "",
            "> [!warning] A codificação dos 10 indicadores não é feita na ingestão.",
            "> Execute `python tools/scripts/code_purification.py --item <id>` após a promoção.",
            "",
            "## Referência ABNT",
            "",
            abnt or "_Não fornecida na ficha._",
            "",
            "## Conexões",
            "",
            "- [[SCOUT-SESSION-2026-04-19]]",
            "",
        ]
    )
    if ficha.get("_extra"):
        lines.extend(
            [
                "## Campos extras preservados",
                "",
                "```json",
                ficha["_extra"],
                "```",
                "",
            ]
        )

    return filename, "\n".join(lines)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_record(record: Dict[str, Any]) -> List[str]:
    """Return list of schema violations (empty list → valid)."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker, RefResolver
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(f"jsonschema required: {exc}") from exc

    schema_dir = REPO_ROOT / "tools" / "schemas"
    if not schema_dir.exists():  # sandbox: load from alt dir
        schema_dir = Path(__file__).resolve().parent.parent / "schemas"
    master = json.loads((schema_dir / "master-record.schema.json").read_text(encoding="utf-8"))
    store: Dict[str, Any] = {}
    for sf in schema_dir.glob("*.schema.json"):
        sc = json.loads(sf.read_text(encoding="utf-8"))
        if "$id" in sc:
            store[sc["$id"]] = sc
    resolver = RefResolver(base_uri="https://example.org/schemas/", referrer=master, store=store)
    validator = Draft202012Validator(master, resolver=resolver, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
    return [f"{list(e.path) or 'root'}: {e.message}" for e in errors]


# ---------------------------------------------------------------------------
# Image extraction
# ---------------------------------------------------------------------------
def extract_docx_images(docx_path: Path, out_dir: Path) -> List[str]:
    """Extract inline media from DOCX into `out_dir`. Returns list of
    relative filenames written (may be empty).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written: List[str] = []
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                target = out_dir / Path(name).name
                with z.open(name) as src, target.open("wb") as dst:
                    dst.write(src.read())
                written.append(target.name)
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(
    docx_path: Path,
    stage_dir: Path,
    *,
    dry_run: bool = False,
    skip_images: bool = False,
    batch_id: Optional[str] = None,
) -> Dict[str, Any]:
    batch_id = batch_id or BATCH_ID_FALLBACK
    now = _now_iso()

    if not docx_path.exists():
        raise FileNotFoundError(f"DOCX not found: {docx_path}")

    fichas = parse_docx(docx_path)
    if not fichas:
        raise RuntimeError("No ficha tables detected in DOCX.")

    corpus_path = REPO_ROOT / "corpus" / "corpus-data.json"
    records_path = REPO_ROOT / "data" / "processed" / "records.jsonl"
    dedup = DedupIndex.from_files(corpus_path, records_path)

    per_ficha: List[Dict[str, Any]] = []
    records: List[Dict[str, Any]] = []
    # Intra-batch dedup: detect copy-paste duplicates inside the DOCX (same
    # ficha_id or URL appearing twice across distinct ficha tables). The
    # second (and later) occurrence gets an `intra_batch_duplicate` audit
    # flag. We do not skip or hard-fail — the user adjudicates during
    # promote review.
    seen_keys: Set[Tuple[str, str]] = set()
    intra_batch_dup_count = 0
    for f in fichas:
        record = build_staging_record(f, batch_id=batch_id, now_iso=now)
        errors = validate_record(record)
        dedup_status, matched, signals = dedup.classify(
            f.get("id", ""), f.get("url", ""), f.get("title", "")
        )
        ficha_id = (f.get("id") or "").strip()
        canon = _canonicalize_url(f.get("url") or "")
        key = (ficha_id, canon)
        intra_batch_dup = False
        # Only flag when at least one of (id, url) is non-empty — an all-empty
        # key would collapse every malformed ficha onto the same bucket.
        if (ficha_id or canon) and key in seen_keys:
            intra_batch_dup = True
            intra_batch_dup_count += 1
            record["exports"]["audit_flags"].append("intra_batch_duplicate")
        else:
            seen_keys.add(key)
        per_ficha.append(
            {
                "ficha": f,
                "record": record,
                "validation_errors": errors,
                "dedup_status": dedup_status,
                "dedup_match_id": matched,
                "dedup_signals": signals,
                "intra_batch_duplicate": intra_batch_dup,
            }
        )
        records.append(record)

    jsonl_path = stage_dir / STAGING_JSONL_NAME
    drafts_dir = stage_dir / STAGING_DRAFTS_DIR_NAME
    images_dir = drafts_dir / STAGING_IMAGES_SUBDIR

    written_files: List[str] = []
    if not dry_run:
        stage_dir.mkdir(parents=True, exist_ok=True)
        drafts_dir.mkdir(parents=True, exist_ok=True)
        with jsonl_path.open("w", encoding="utf-8") as out:
            for rec in records:
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        written_files.append(str(jsonl_path))
        for entry in per_ficha:
            fname, body = render_vault_draft(entry["ficha"], entry["record"])
            p = drafts_dir / fname
            p.write_text(body, encoding="utf-8")
            written_files.append(str(p))
        if not skip_images:
            imgs = extract_docx_images(docx_path, images_dir)
            written_files.append(str(images_dir))
            extracted_images = imgs
        else:
            extracted_images = []
    else:
        extracted_images = []

    validation_failed = any(entry["validation_errors"] for entry in per_ficha)
    return {
        "fichas": per_ficha,
        "jsonl_path": str(jsonl_path),
        "drafts_dir": str(drafts_dir),
        "images_dir": str(images_dir),
        "written_files": written_files,
        "extracted_images": extracted_images,
        "validation_failed": validation_failed,
        "intra_batch_duplicates": intra_batch_dup_count,
        "batch_id": batch_id,
        "now": now,
        "dry_run": dry_run,
    }


def _print_summary(result: Dict[str, Any]) -> None:
    fichas = result["fichas"]
    print(f"LPAI v2 ingest: {len(fichas)} fichas parsed", file=sys.stderr)
    by_country: Dict[str, int] = {}
    for e in fichas:
        cc = infer_country_from_id(e["ficha"].get("id", "")) or "??"
        by_country[cc] = by_country.get(cc, 0) + 1
    print(f"  distribution: {by_country}", file=sys.stderr)
    dedup_counts: Dict[str, int] = {}
    for e in fichas:
        dedup_counts[e["dedup_status"]] = dedup_counts.get(e["dedup_status"], 0) + 1
    print(f"  dedup: {dedup_counts}", file=sys.stderr)
    intra = result.get("intra_batch_duplicates", 0)
    print(f"  intra-batch duplicates: {intra}", file=sys.stderr)
    fails = sum(1 for e in fichas if e["validation_errors"])
    print(f"  validation: {len(fichas) - fails}/{len(fichas)} pass", file=sys.stderr)
    if result["dry_run"]:
        print("  DRY-RUN — no files written", file=sys.stderr)
    else:
        print(f"  wrote: {len(result['written_files'])} paths under {result['jsonl_path']}", file=sys.stderr)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--input", type=Path, default=DEFAULT_DOCX, help="Path to LPAI v2 DOCX")
    p.add_argument("--stage-dir", type=Path, default=DEFAULT_STAGE_DIR, help="Staging output directory")
    p.add_argument("--dry-run", action="store_true", help="Parse + report only, no writes")
    p.add_argument("--skip-images", action="store_true", help="Do not extract DOCX inline images")
    p.add_argument("--batch-id", type=str, default=None, help="Override generated batch_id")
    args = p.parse_args(argv)

    try:
        result = run(
            args.input,
            args.stage_dir,
            dry_run=args.dry_run,
            skip_images=args.skip_images,
            batch_id=args.batch_id,
        )
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"ingest failed: {exc}", file=sys.stderr)
        return 1
    _print_summary(result)
    return 2 if result["validation_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
