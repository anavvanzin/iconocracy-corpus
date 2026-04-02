#!/usr/bin/env python3
"""
hunt.py — Automated corpus candidate hunter for ICONOCRACY.

Searches multiple digital archive APIs for female allegorical figures
with juridical-political function (1800–2000) and outputs candidates
as JSON or appends directly to corpus-data.json.

Archives supported:
  - Gallica (BnF) — SRU/CQL search + IIIF
  - Europeana — REST search API
  - Library of Congress — JSON API

Usage:
    python tools/scripts/hunt.py --limit 50
    python tools/scripts/hunt.py --country FR --period 1880-1920
    python tools/scripts/hunt.py --country DE --archive europeana --support moeda
    python tools/scripts/hunt.py --country UK --append
    python tools/scripts/hunt.py --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
CANDIDATES_DIR = REPO_ROOT / "vault" / "candidatos"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ICONOCRACIA-hunt/1.0"

# When --json is used, progress goes to stderr so stdout is clean JSON
_log_stream = sys.stderr  # set by main() if --json


def _log(msg: str = "") -> None:
    """Print progress message (stderr when --json, stdout otherwise)."""
    print(msg, file=_log_stream)

COUNTRY_CODES = {
    "FR": "France",
    "UK": "United Kingdom",
    "DE": "Germany",
    "US": "United States",
    "BE": "Belgium",
    "BR": "Brazil",
}

# Canonical allegorical figures per country
FIGURES = {
    "FR": ["Marianne", "République", "Justice", "Liberté", "allégorie féminine"],
    "UK": ["Britannia", "Justice", "Hibernia", "Scotia"],
    "DE": ["Germania", "Justitia", "Minerva"],
    "US": ["Columbia", "Lady Justice", "Liberty", "America"],
    "BE": ["Belgique", "allégorie féminine", "Justice"],
    "BR": ["República", "Justiça", "alegoria feminina"],
}

# Accepted support types and their search terms per language
SUPPORTS = {
    "moeda": ["coin", "monnaie", "medal", "Münze", "moeda"],
    "selo": ["stamp", "timbre-poste", "postage stamp", "Briefmarke", "selo postal"],
    "monumento": ["statue", "monument", "sculpture", "Denkmal", "monumento"],
    "estampa": ["print", "engraving", "estampe", "gravure", "Druckgrafik", "gravura"],
    "frontispicio": ["frontispiece", "frontispice", "title page"],
    "papel-moeda": ["banknote", "billet de banque", "paper money", "Banknote"],
    "cartaz": ["poster", "affiche", "placard", "Plakat", "cartaz"],
}

# SSL context for sites with cert issues
SSL_UNVERIFIED = ssl.create_default_context()
SSL_UNVERIFIED.check_hostname = False
SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _fetch_curl(url: str, timeout: int = 20, accept: str = "*/*") -> bytes | None:
    """Fallback: fetch via curl subprocess (handles TLS 1.3 on macOS)."""
    try:
        result = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout),
             "-H", f"User-Agent: {USER_AGENT}",
             "-H", f"Accept: {accept}",
             url],
            capture_output=True, timeout=timeout + 5,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def _fetch(url: str, timeout: int = 20, accept: str = "*/*") -> bytes | None:
    """Fetch raw bytes from URL. Tries urllib, falls back to curl for TLS issues."""
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep((attempt + 1) * 3)
                continue
            if e.code in (403, 404):
                # 403 might be TLS issue masquerading — try curl once
                return _fetch_curl(url, timeout, accept)
            if attempt < 2:
                time.sleep(2)
                continue
            return None
        except (ssl.SSLCertVerificationError, ssl.SSLError, ConnectionResetError, OSError):
            # TLS handshake failure — curl has its own TLS stack on macOS
            return _fetch_curl(url, timeout, accept)
        except Exception:
            if attempt < 2:
                time.sleep(2)
                continue
            return None
    return None


def _fetch_json(url: str, timeout: int = 20) -> dict | None:
    """Fetch and parse JSON from URL."""
    data = _fetch(url, timeout=timeout, accept="application/json")
    if data:
        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    return None


def _fetch_xml(url: str, timeout: int = 20) -> ET.Element | None:
    """Fetch and parse XML from URL."""
    data = _fetch(url, timeout=timeout, accept="application/xml, text/xml")
    if data:
        try:
            return ET.fromstring(data)
        except ET.ParseError:
            return None
    return None


# ---------------------------------------------------------------------------
# Query builders
# ---------------------------------------------------------------------------


def _build_queries(
    country: str | None,
    period: str | None,
    support: str | None,
) -> dict[str, list[str]]:
    """Build search queries per archive. Returns {archive: [queries]}."""

    countries = [country] if country else list(FIGURES.keys())
    year_from, year_to = _parse_period(period)
    support_terms = SUPPORTS.get(support, []) if support else []

    queries: dict[str, list[str]] = {"gallica": [], "europeana": [], "loc": []}

    for cc in countries:
        figures = FIGURES.get(cc, [])
        for fig in figures[:3]:  # top 3 figures per country to avoid explosion
            # --- Gallica (French-oriented) ---
            if cc in ("FR", "BE"):
                cql = f'dc.subject all "{fig}"'
                if year_from and year_to:
                    cql += f' and dc.date within "{year_from} {year_to}"'
                if support_terms:
                    cql += f' and dc.type all "{support_terms[0]}"'
                queries["gallica"].append(cql)

            # --- Europeana (all countries) ---
            q_parts = [f'what:"{fig}"', 'what:"allegory" OR what:"allégorie"']
            if year_from and year_to:
                q_parts.append(f"when:[{year_from} TO {year_to}]")
            if support_terms:
                q_parts.append(f'what:"{support_terms[0]}"')
            # Country filter via DATA_PROVIDER or COUNTRY
            if cc in ("FR", "DE", "BE", "UK"):
                country_name = COUNTRY_CODES.get(cc, "")
                q_parts.append(f'COUNTRY:"{country_name}"')
            queries["europeana"].append(" AND ".join(q_parts))

            # --- Library of Congress (US-oriented) ---
            if cc == "US":
                loc_q = f'{fig} allegory'
                if support_terms:
                    loc_q += f' {support_terms[0]}'
                queries["loc"].append(loc_q)

    return queries


def _parse_period(period: str | None) -> tuple[str | None, str | None]:
    """Parse period string like '1880-1920' into (from, to)."""
    if not period:
        return ("1800", "2000")
    m = re.match(r"(\d{4})\s*[-–]\s*(\d{4})", period)
    if m:
        return m.group(1), m.group(2)
    # Single year
    m2 = re.match(r"(\d{4})", period)
    if m2:
        y = m2.group(1)
        return y, y
    return ("1800", "2000")


# ---------------------------------------------------------------------------
# Archive-specific search functions
# ---------------------------------------------------------------------------

# Namespace map for Gallica SRU XML
SRU_NS = {
    "srw": "http://www.loc.gov/zing/srw/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
}


def search_gallica(cql_query: str, limit: int = 15) -> list[dict]:
    """Search Gallica via SRU/CQL and return candidate dicts."""
    params = urllib.parse.urlencode({
        "operation": "searchRetrieve",
        "version": "1.2",
        "query": cql_query,
        "maximumRecords": str(min(limit, 50)),
        "startRecord": "1",
    })
    url = f"https://gallica.bnf.fr/SRU?{params}"
    root = _fetch_xml(url, timeout=30)
    if root is None:
        return []

    results = []
    for record in root.findall(".//srw:record", SRU_NS):
        dc_data = record.find(".//oai_dc:dc", SRU_NS)
        if dc_data is None:
            continue

        title = _dc_text(dc_data, "title")
        identifier = _dc_text(dc_data, "identifier")
        date = _dc_text(dc_data, "date")
        creator = _dc_text(dc_data, "creator")
        subject = _dc_text(dc_data, "subject")
        doc_type = _dc_text(dc_data, "type")

        # Extract ARK identifier
        ark = None
        for ident_el in dc_data.findall("dc:identifier", SRU_NS):
            text = (ident_el.text or "").strip()
            if "ark:" in text:
                ark_match = re.search(r"(ark:/12148/[a-z0-9]+)", text)
                if ark_match:
                    ark = ark_match.group(1)
                    break

        if not ark:
            continue

        gallica_url = f"https://gallica.bnf.fr/{ark}"
        iiif_url = f"https://gallica.bnf.fr/iiif/{ark}/manifest.json"
        image_url = f"https://gallica.bnf.fr/iiif/{ark}/f1/full/full/0/native.jpg"

        results.append({
            "title": title or "(sem título)",
            "date": date,
            "creator": creator,
            "url": gallica_url,
            "url_iiif": iiif_url,
            "url_image_download": image_url,
            "iiif_source": "gallica",
            "source_archive": "Gallica (BnF)",
            "country_hint": "FR",
            "subject": subject,
            "doc_type": doc_type,
            "ark": ark,
            "_query": cql_query,
        })

        time.sleep(0.3)  # polite delay

    return results


def _dc_text(dc_elem: ET.Element, field: str) -> str | None:
    """Extract text from a Dublin Core field."""
    el = dc_elem.find(f"dc:{field}", SRU_NS)
    return el.text.strip() if el is not None and el.text else None


def search_europeana(query: str, limit: int = 15) -> list[dict]:
    """Search Europeana REST API. Uses demo key (rate-limited)."""
    params = urllib.parse.urlencode({
        "wskey": "api2demo",
        "query": query,
        "rows": str(min(limit, 50)),
        "qf": "TYPE:IMAGE",
        "profile": "standard",
    })
    url = f"https://api.europeana.eu/record/v2/search.json?{params}"
    data = _fetch_json(url, timeout=30)
    if not data or "items" not in data:
        return []

    results = []
    for item in data["items"]:
        title_list = item.get("title", [])
        title = title_list[0] if title_list else "(sem título)"

        # Extract year
        year_list = item.get("year", [])
        date = year_list[0] if year_list else None

        # Image URLs
        preview = None
        edmPreview = item.get("edmPreview", [])
        if edmPreview:
            preview = edmPreview[0]

        # Build Europeana URL from ID
        euro_id = item.get("id", "")
        euro_url = f"https://www.europeana.eu/en/item{euro_id}" if euro_id else None

        # Data provider
        provider_list = item.get("dataProvider", [])
        provider = provider_list[0] if provider_list else None

        # Country
        country_list = item.get("country", [])
        country_hint = _europeana_country_code(country_list[0] if country_list else "")

        results.append({
            "title": title,
            "date": date,
            "creator": None,
            "url": euro_url,
            "url_iiif": None,
            "url_image_download": preview,
            "iiif_source": "europeana",
            "source_archive": f"Europeana ({provider})" if provider else "Europeana",
            "country_hint": country_hint,
            "subject": None,
            "doc_type": item.get("type"),
            "_query": query,
        })

    return results


def _europeana_country_code(name: str) -> str:
    """Map Europeana country name to our 2-letter code."""
    mapping = {
        "france": "FR", "germany": "DE", "belgium": "BE",
        "united kingdom": "UK", "netherlands": "NL", "portugal": "PT",
        "spain": "ES", "italy": "IT", "brazil": "BR",
    }
    return mapping.get(name.lower().strip(), "EU")


def search_loc(query: str, limit: int = 15) -> list[dict]:
    """Search Library of Congress prints & photographs collection."""
    # Use the collections API which is more permissive than /search/
    params = urllib.parse.urlencode({
        "q": query,
        "fo": "json",
        "c": str(min(limit, 50)),
    })
    # Try prints & photographs first, fall back to general collections
    urls_to_try = [
        f"https://www.loc.gov/collections/prints-and-photographs/?{params}",
        f"https://www.loc.gov/pictures/search/?{params}",
    ]

    data = None
    for url in urls_to_try:
        data = _fetch_json(url, timeout=30)
        if data and "results" in data:
            break

    if not data or "results" not in data:
        return []

    results = []
    for item in data["results"]:
        if not isinstance(item, dict):
            continue

        title = item.get("title", "(sem título)")
        date = item.get("date")
        loc_url = item.get("url") or item.get("id")
        if loc_url and not loc_url.startswith("http"):
            loc_url = f"https://www.loc.gov{loc_url}"

        # Image
        image_url = None
        thumb = item.get("image_url", [])
        if isinstance(thumb, list) and thumb:
            image_url = thumb[0]
        elif isinstance(thumb, str):
            image_url = thumb

        results.append({
            "title": title,
            "date": date,
            "creator": item.get("contributor", [None])[0] if item.get("contributor") else None,
            "url": loc_url,
            "url_iiif": None,
            "url_image_download": image_url,
            "iiif_source": "loc",
            "source_archive": "Library of Congress",
            "country_hint": "US",
            "subject": "; ".join(item.get("subject", [])[:5]) if item.get("subject") else None,
            "doc_type": item.get("original_format", [None])[0] if item.get("original_format") else None,
            "_query": query,
        })

    return results


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def _candidate_hash(c: dict) -> str:
    """Generate hash for deduplication based on URL + title."""
    content = f"{c.get('url', '')}|{c.get('title', '')}".lower().strip()
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _load_existing_hashes() -> set[str]:
    """Load hashes of existing corpus items for dedup."""
    if not CORPUS_PATH.exists():
        return set()
    with open(CORPUS_PATH, encoding="utf-8") as f:
        items = json.load(f)
    hashes = set()
    for item in items:
        content = f"{item.get('url', '')}|{item.get('title', '')}".lower().strip()
        hashes.add(hashlib.sha256(content.encode("utf-8")).hexdigest()[:16])
    return hashes


def _load_existing_ids() -> set[str]:
    """Load existing corpus IDs."""
    if not CORPUS_PATH.exists():
        return set()
    with open(CORPUS_PATH, encoding="utf-8") as f:
        items = json.load(f)
    return {item["id"] for item in items}


# ---------------------------------------------------------------------------
# Candidate → corpus item conversion
# ---------------------------------------------------------------------------


def _next_id(country: str, existing_ids: set[str]) -> str:
    """Generate next sequential ID for a country (e.g., FR-014)."""
    prefix = country + "-"
    max_num = 0
    for eid in existing_ids:
        if eid.startswith(prefix):
            # Handle compound IDs like US-EDUC-1896-02
            parts = eid[len(prefix):]
            m = re.match(r"^(\d+)$", parts)
            if m:
                max_num = max(max_num, int(m.group(1)))
    return f"{prefix}{max_num + 1:03d}"


def _candidate_to_corpus_item(candidate: dict, item_id: str) -> dict:
    """Convert a hunt candidate to a corpus-data.json item (scaffold)."""
    country_code = candidate.get("country_hint", "EU")
    country_name = COUNTRY_CODES.get(country_code, country_code)
    title = candidate.get("title", "(sem título)")
    date = candidate.get("date")

    # Parse year
    year = None
    if date:
        m = re.search(r"(\d{4})", str(date))
        if m:
            year = int(m.group(1))

    return {
        "id": item_id,
        "title": title,
        "date": str(date) if date else None,
        "period": None,
        "creator": candidate.get("creator"),
        "institution": None,
        "source_archive": candidate.get("source_archive"),
        "country": country_name,
        "medium": candidate.get("doc_type"),
        "motif": [],
        "description": None,
        "url": candidate.get("url"),
        "thumbnail_url": candidate.get("url_image_download"),
        "url_image_download": candidate.get("url_image_download"),
        "url_iiif": candidate.get("url_iiif"),
        "iiif_source": candidate.get("iiif_source"),
        "rights": None,
        "citation_abnt": None,
        "citation_chicago": None,
        "tags": ["hunt-candidate", "#verificar"],
        "year": year,
        "medium_norm": None,
        "country_pt": None,
        "period_norm": None,
        "regime": None,
        "endurecimento_score": None,
        "indicadores": None,
        "coded_by": None,
        "coded_at": None,
        "support": None,
        "in_scope": None,
        "scope_note": "Auto-discovered by hunt.py — requires manual review and IconoCode analysis",
    }


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def hunt(
    country: str | None = None,
    period: str | None = None,
    archive: str | None = None,
    support: str | None = None,
    limit: int = 20,
    dry_run: bool = False,
    append: bool = False,
) -> list[dict]:
    """Run the hunt across archives and return deduplicated candidates."""

    queries = _build_queries(country, period, support)
    existing_hashes = _load_existing_hashes()

    all_candidates: list[dict] = []
    seen_hashes: set[str] = set()

    # Determine which archives to search
    archives_to_search = []
    if archive:
        archives_to_search = [archive.lower()]
    else:
        archives_to_search = ["gallica", "europeana", "loc"]

    per_archive_limit = max(5, limit // len(archives_to_search))

    for arch in archives_to_search:
        arch_queries = queries.get(arch, [])
        if not arch_queries:
            continue

        _log(f"\n{'='*60}")
        _log(f"  Archive: {arch.upper()}")
        _log(f"  Queries: {len(arch_queries)}")
        _log(f"{'='*60}")

        for i, q in enumerate(arch_queries):
            if len(all_candidates) >= limit:
                break

            remaining = limit - len(all_candidates)
            q_limit = min(per_archive_limit, remaining)

            _log(f"\n  [{i+1}/{len(arch_queries)}] {q[:80]}...")

            if dry_run:
                _log(f"    (dry-run) would search {arch} with limit={q_limit}")
                continue

            if arch == "gallica":
                results = search_gallica(q, limit=q_limit)
            elif arch == "europeana":
                results = search_europeana(q, limit=q_limit)
            elif arch == "loc":
                results = search_loc(q, limit=q_limit)
            else:
                _log(f"    Unknown archive: {arch}")
                continue

            _log(f"    Found {len(results)} raw results")

            # Deduplicate
            new = 0
            for c in results:
                h = _candidate_hash(c)
                if h in existing_hashes or h in seen_hashes:
                    continue
                seen_hashes.add(h)
                all_candidates.append(c)
                new += 1
                if len(all_candidates) >= limit:
                    break

            _log(f"    New candidates: {new}")
            time.sleep(1)  # polite delay between queries

    _log(f"\n{'='*60}")
    _log(f"  Total unique candidates: {len(all_candidates)}")
    _log(f"{'='*60}")

    # If --append, convert and add to corpus
    if append and all_candidates and not dry_run:
        _append_to_corpus(all_candidates)

    return all_candidates


def _append_to_corpus(candidates: list[dict]) -> None:
    """Append candidates to corpus-data.json."""
    existing_ids = _load_existing_ids()

    with open(CORPUS_PATH, encoding="utf-8") as f:
        corpus = json.load(f)

    added = 0
    for c in candidates:
        country_code = c.get("country_hint", "EU")
        item_id = _next_id(country_code, existing_ids)
        existing_ids.add(item_id)

        item = _candidate_to_corpus_item(c, item_id)
        corpus.append(item)
        added += 1
        _log(f"  + {item_id}: {item['title'][:60]}")

    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    _log(f"\n  Appended {added} items to {CORPUS_PATH}")
    _log(f"  Corpus now has {len(corpus)} items")
    _log(f"  NOTE: Items tagged #verificar — run IconoCode analysis before using")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hunt for corpus candidates across digital archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --limit 50                           # All countries, all archives
  %(prog)s --country FR --period 1880-1920      # French archives, specific period
  %(prog)s --country DE --archive europeana     # German items via Europeana
  %(prog)s --country UK --append                # British items, add to corpus
  %(prog)s --dry-run                            # Show queries without calling APIs
  %(prog)s --support moeda --country FR         # French coins only
""",
    )
    parser.add_argument(
        "--country", "-c",
        choices=list(COUNTRY_CODES.keys()),
        help="Filter by country code (FR, UK, DE, US, BE, BR)",
    )
    parser.add_argument(
        "--period", "-p",
        help="Date range, e.g. 1880-1920 (default: 1800-2000)",
    )
    parser.add_argument(
        "--archive", "-a",
        choices=["gallica", "europeana", "loc"],
        help="Search only this archive",
    )
    parser.add_argument(
        "--support", "-s",
        choices=list(SUPPORTS.keys()),
        help="Filter by support type",
    )
    parser.add_argument(
        "--limit", "-l",
        type=int, default=20,
        help="Max candidates to return (default: 20)",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append candidates directly to corpus-data.json (tagged #verificar)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show queries without calling APIs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON to stdout",
    )

    args = parser.parse_args()

    # Route progress to stderr when --json so stdout is clean JSON
    global _log_stream
    if args.json:
        _log_stream = sys.stderr

    _log(f"ICONOCRACY hunt.py — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    _log(f"  Country: {args.country or 'ALL'}")
    _log(f"  Period:  {args.period or '1800-2000'}")
    _log(f"  Archive: {args.archive or 'ALL'}")
    _log(f"  Support: {args.support or 'ALL'}")
    _log(f"  Limit:   {args.limit}")
    if args.dry_run:
        _log(f"  MODE: DRY RUN")
    if args.append:
        _log(f"  MODE: APPEND to corpus")

    candidates = hunt(
        country=args.country,
        period=args.period,
        archive=args.archive,
        support=args.support,
        limit=args.limit,
        dry_run=args.dry_run,
        append=args.append,
    )

    if args.json and candidates:
        # Clean internal fields
        for c in candidates:
            c.pop("_query", None)
        json.dump(candidates, sys.stdout, ensure_ascii=False, indent=2)
        print()
    elif candidates and not args.json:
        _log(f"\n--- Candidates ---\n")
        for i, c in enumerate(candidates, 1):
            _log(f"  {i:3d}. [{c.get('country_hint', '??')}] {c['title'][:65]}")
            _log(f"       {c.get('source_archive', '?')} | {c.get('date', '?')} | {c.get('url', '')[:70]}")
    elif not args.dry_run:
        _log("\n  No new candidates found.")


if __name__ == "__main__":
    main()
