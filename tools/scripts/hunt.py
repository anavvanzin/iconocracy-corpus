#!/usr/bin/env python3
"""
hunt.py — Allegory Hunter for the Iconocracy Corpus

Queries digital archive APIs to discover female allegorical figures
in legal/state contexts. Outputs corpus-compatible JSON candidates.

Usage:
    python hunt.py --country FR --period 1880-1920 --support moeda --limit 50
    python hunt.py --archive europeana --country UK --append
    python hunt.py --dry-run
"""

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

CORPUS_PATH = Path(__file__).resolve().parents[2] / "corpus" / "corpus-data.json"

COUNTRY_NAMES = {
    "FR": "France", "UK": "United Kingdom", "DE": "Germany",
    "US": "United States", "BE": "Belgium", "BR": "Brazil",
}

# Known engravers/artists of allegorical state imagery
KNOWN_CREATORS = [
    "Oscar Roty", "Louis-Oscar Roty", "Roty",
    "Daniel Dupuis", "Jean-Baptiste Daniel-Dupuis",
    "Chaplain", "Jules-Clément Chaplain",
    "Augustin Dupré", "Dupré",
    "Louis Merley", "Merley",
    "Alphée Dubois",
    "Lindauer",
    "Pierre-Alexandre Morlon", "Morlon",
    "Leonhard Posch",
    "Karl Friedrich Schinkel",
    "Benedetto Pistrucci", "Pistrucci",
    "George William de Saulles",
    "Christian Gobrecht", "Gobrecht",
    "Augustus Saint-Gaudens", "Saint-Gaudens",
    "Adolph Weinman", "Weinman",
    "Eliseu Visconti",
    "Girardet",
    "Godefroid Devreese",
]

# ─── Query Matrix ──────────────────────────────────────────────────────────

QUERY_MATRIX = {
    "FR": {
        "motifs": ["Marianne", "République allégorie", "Semeuse",
                   "Justice allégorie femme", "Liberté figure féminine",
                   "Roty Semeuse", "Chaplain République", "Dupré Liberté"],
        "europeana_qf": (
            'what:"allégorie" AND '
            '(what:"République" OR what:"Marianne" OR what:"Justice")'
        ),
        "europeana_alt": [
            'what:"Semeuse" AND (what:"monnaie" OR what:"timbre")',
            'what:"Marianne" AND (what:"buste" OR what:"sculpture" OR what:"monnaie")',
            '(what:"Roty" OR what:"Chaplain" OR what:"Dupré") AND what:"République"',
        ],
        "gallica_sru": (
            '(dc.subject all "allégorie") and '
            '(dc.subject all "République" or dc.subject all "Marianne")'
        ),
        "gallica_alt": [
            '(dc.subject all "Semeuse")',
            '(dc.subject all "Justice") and (dc.subject all "allégorie")',
            '(dc.subject all "Marianne") and (dc.type all "image")',
        ],
        "loc_query": None,
        "met_query": "Marianne allegory Republic France",
        "va_query": None,
    },
    "BR": {
        "motifs": ["República alegoria", "Efígie República",
                   "Justiça alegoria", "Liberdade figura feminina",
                   "Eliseu Visconti República", "moeda República efígie"],
        "europeana_qf": 'what:"alegoria" AND what:"República"',
        "europeana_alt": [
            'what:"República" AND (what:"moeda" OR what:"selo" OR what:"monumento")',
            'what:"Brasil" AND (what:"alegoria" OR what:"Republic")',
        ],
        "gallica_sru": '(dc.subject all "Brésil") and (dc.subject all "République" or dc.subject all "allégorie")',
        "gallica_alt": [
            '(dc.title all "Brésil") and (dc.type all "image")',
        ],
        "loc_query": "Brazil Republic allegory OR Brazil female figure statue",
        "met_query": "Brazil Republic allegory",
        "va_query": None,
    },
    "UK": {
        "motifs": ["Britannia", "Justice allegory",
                   "Liberty figure female", "Pistrucci Britannia",
                   "Britannia coin penny", "Justice Old Bailey"],
        "europeana_qf": (
            'what:"Britannia" OR '
            '(what:"Justice" AND what:"allegory")'
        ),
        "europeana_alt": [
            'what:"Britannia" AND (what:"coin" OR what:"penny" OR what:"medal")',
        ],
        "gallica_sru": None,
        "loc_query": "Britannia allegory OR Justice female figure",
        "met_query": "Britannia allegory coin",
        "va_query": "Britannia allegory",
    },
    "DE": {
        "motifs": ["Germania Allegorie", "Justitia",
                   "Freiheit Figur", "Germania Münze",
                   "Justitia Schwert Waage", "Germania Wacht am Rhein"],
        "europeana_qf": 'what:"Germania" AND what:"Allegorie"',
        "europeana_alt": [
            'what:"Justitia" AND (what:"Allegorie" OR what:"Gerechtigkeit")',
            'what:"Germania" AND (what:"Münze" OR what:"Medaille" OR what:"Denkmal")',
        ],
        "gallica_sru": None,
        "loc_query": "Germania allegory",
        "met_query": "Germania allegory OR Justitia allegory German",
        "va_query": None,
    },
    "US": {
        "motifs": ["Columbia allegory", "Liberty seated",
                   "Justice female figure", "Freedom statue",
                   "Saint-Gaudens Liberty", "Weinman Liberty",
                   "Gobrecht dollar seated", "Columbia coin"],
        "europeana_qf": '(what:"Columbia" OR what:"Liberty") AND what:"allegory"',
        "europeana_alt": [
            'what:"Liberty" AND (what:"coin" OR what:"dollar" OR what:"medal")',
        ],
        "gallica_sru": None,
        "loc_query": (
            "Columbia allegory female OR "
            "Liberty seated figure OR "
            "Justice female allegory"
        ),
        "loc_alt": [
            "seated Liberty coin dollar",
            "Columbia personification",
            "Freedom statue Capitol",
            "Saint-Gaudens Liberty gold",
        ],
        "met_query": "Liberty allegory seated coin OR Columbia allegory",
        "va_query": None,
    },
    "BE": {
        "motifs": ["Belgique allégorie", "Justice Palais Bruxelles",
                   "Belgica figure", "Devreese Belgique",
                   "Justice Palais de Justice Bruxelles"],
        "europeana_qf": (
            'what:"Belgique" AND what:"allégorie"'
        ),
        "europeana_alt": [
            '(what:"Belgique" OR what:"Belgica") AND (what:"monnaie" OR what:"médaille")',
            'what:"Justice" AND what:"Bruxelles"',
        ],
        "gallica_sru": None,
        "loc_query": None,
        "met_query": None,
        "va_query": None,
    },
}

SUPPORT_FILTERS = {
    "moeda": {
        "europeana_extra": '(what:"coin" OR what:"moeda" OR what:"monnaie" OR what:"Münze")',
        "loc_fa": "prints and photographs",
    },
    "selo": {
        "europeana_extra": '(what:"stamp" OR what:"selo" OR what:"timbre")',
        "loc_fa": "prints and photographs",
    },
    "monumento": {
        "europeana_extra": '(what:"monument" OR what:"statue" OR what:"sculpture")',
        "loc_fa": "prints and photographs",
    },
    "estampa": {
        "europeana_extra": '(what:"print" OR what:"engraving" OR what:"gravure")',
        "loc_fa": "prints and photographs",
    },
    "frontispicio": {
        "europeana_extra": '(what:"frontispiece" OR what:"frontispice")',
        "loc_fa": "rare book",
    },
    "papel-moeda": {
        "europeana_extra": '(what:"banknote" OR what:"paper money" OR what:"billet")',
        "loc_fa": "prints and photographs",
    },
    "cartaz": {
        "europeana_extra": '(what:"poster" OR what:"affiche" OR what:"cartaz")',
        "loc_fa": "prints and photographs",
    },
}

# ─── Relevance keywords ───────────────────────────────────────────────────

ALLEGORY_KW = [
    "allegory", "allégorie", "alegoria", "allegorie",
    "personification", "personificação", "personnification",
    "allegorical", "allégorique",
    "female figure", "figure féminine", "figura feminina",
    "weibliche figur",
]

MOTIF_KW = [
    "marianne", "britannia", "columbia", "germania", "belgique",
    "belgica", "república", "republic", "république", "republik",
    "justitia", "justice", "justiça", "semeuse",
    "liberté", "liberty", "liberdade", "freiheit",
    "minerva", "athena", "pallas", "ceres", "fortuna",
    "seated liberty", "standing liberty", "walking liberty",
]

LEGAL_STATE_KW = [
    "justice", "law", "droit", "direito", "recht", "legal",
    "état", "state", "staat", "estado",
    "constitution", "constituição", "tribunal", "court",
    "scales", "blindfold", "balança", "venda",
]

# ─── HTTP helper ───────────────────────────────────────────────────────────

def fetch_json(url, timeout=20):
    """Fetch JSON from URL, return dict or None."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 ICONOCRACIA-corpus/1.0",
            "Accept": "application/json",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"  [WARN] fetch failed: {url[:80]}… → {e}")
        return None


def fetch_xml(url, timeout=20):
    """Fetch XML from URL, return ElementTree root or None."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 ICONOCRACIA-corpus/1.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return ET.fromstring(resp.read())
    except Exception as e:
        log(f"  [WARN] fetch failed: {url[:80]}… → {e}")
        return None


def log(msg):
    """Print to stderr."""
    print(msg, file=sys.stderr)


# ─── Harvesters ────────────────────────────────────────────────────────────

def harvest_europeana(country, qf_query, support=None, period=None, limit=100):
    """Query Europeana Search API v2."""
    if not qf_query:
        return []

    base = "https://api.europeana.eu/record/v2/search.json"
    params = {
        "wskey": "api2demo",
        "query": qf_query,
        "qf": "TYPE:IMAGE",
        "rows": str(min(limit, 100)),
        "start": "1",
        "profile": "standard",
    }

    if support and support in SUPPORT_FILTERS:
        extra = SUPPORT_FILTERS[support].get("europeana_extra", "")
        if extra:
            params["query"] = f"({params['query']}) AND {extra}"

    if period:
        y1, y2 = _parse_period(period)
        if y1 and y2:
            params["qf"] = f"TYPE:IMAGE&qf=YEAR:[{y1} TO {y2}]"

    url = f"{base}?{urllib.parse.urlencode(params)}"
    log(f"  [europeana/{country}] {url[:120]}…")

    data = fetch_json(url)
    if not data:
        return []

    results = []
    for item in data.get("items", []):
        title_list = item.get("title", [])
        title = title_list[0] if title_list else ""

        # Get thumbnail
        thumb = ""
        previews = item.get("edmPreview", [])
        if previews:
            thumb = previews[0]

        # Get link to object
        link = ""
        shown_at = item.get("edmIsShownAt", [])
        if shown_at:
            link = shown_at[0]
        elif item.get("guid"):
            link = item["guid"]

        # Creator
        creators = item.get("dcCreator", [])
        creator = creators[0] if creators else ""

        # Provider
        providers = item.get("dataProvider", [])
        institution = providers[0] if providers else ""

        # Date
        dates = item.get("year", [])
        date_str = dates[0] if dates else ""

        # Description
        desc_list = item.get("dcDescription", [])
        desc = desc_list[0] if desc_list else ""

        # Rights
        rights_list = item.get("rights", [])
        rights = rights_list[0] if rights_list else ""

        results.append({
            "title": title,
            "url": link,
            "thumbnail_url": thumb,
            "description": desc,
            "creator": creator,
            "institution": institution,
            "date": date_str,
            "rights": rights,
            "source_archive": "Europeana",
            "hunt_source": "europeana",
        })

    log(f"    → {len(results)} results")
    return results


def harvest_gallica(country, sru_query, support=None, period=None, limit=50):
    """Query Gallica SRU endpoint."""
    if not sru_query:
        return []

    query = sru_query
    if period:
        y1, y2 = _parse_period(period)
        if y1 and y2:
            query = f"({query}) and (dc.date >= \"{y1}\" and dc.date <= \"{y2}\")"

    params = {
        "operation": "searchRetrieve",
        "version": "1.2",
        "query": query,
        "maximumRecords": str(min(limit, 50)),
        "startRecord": "1",
    }

    url = f"https://gallica.bnf.fr/SRU?{urllib.parse.urlencode(params)}"
    log(f"  [gallica/{country}] {url[:120]}…")

    root = fetch_xml(url)
    if root is None:
        return []

    # Define namespaces
    ns = {
        "srw": "http://www.loc.gov/zing/srw/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    }

    results = []
    for record in root.findall(".//srw:record", ns):
        data = record.find(".//oai_dc:dc", ns)
        if data is None:
            continue

        title = _xml_text(data, "dc:title", ns)
        creator = _xml_text(data, "dc:creator", ns)
        date_str = _xml_text(data, "dc:date", ns)
        rights = _xml_text(data, "dc:rights", ns)
        description = _xml_text(data, "dc:description", ns)

        # Extract ARK identifier for URL and thumbnail
        identifier = _xml_text(data, "dc:identifier", ns)
        ark_url = ""
        thumb = ""
        if identifier and "ark:" in identifier:
            ark_match = re.search(r"(ark:/12148/[a-z0-9]+)", identifier)
            if ark_match:
                ark = ark_match.group(1)
                ark_url = f"https://gallica.bnf.fr/{ark}"
                thumb = f"https://gallica.bnf.fr/{ark}/f1.thumbnail"

        if not ark_url and identifier:
            ark_url = identifier

        results.append({
            "title": title,
            "url": ark_url,
            "thumbnail_url": thumb,
            "description": description,
            "creator": creator,
            "institution": "Bibliothèque nationale de France",
            "date": date_str,
            "rights": rights,
            "source_archive": "Gallica/BnF",
            "hunt_source": "gallica",
        })

    log(f"    → {len(results)} results")
    return results


def harvest_loc(country, query_str, support=None, period=None, limit=50):
    """Query Library of Congress JSON API."""
    if not query_str:
        return []

    params = {
        "q": query_str,
        "fo": "json",
        "c": str(min(limit, 50)),
        "fa": "online-format:image",
    }

    if support and support in SUPPORT_FILTERS:
        fa = SUPPORT_FILTERS[support].get("loc_fa", "")
        if fa:
            params["fa"] += f"|access-restricted:false"

    if period:
        y1, y2 = _parse_period(period)
        if y1 and y2:
            params["dates"] = f"{y1}/{y2}"

    url = f"https://www.loc.gov/search/?{urllib.parse.urlencode(params)}"
    log(f"  [loc/{country}] {url[:120]}…")

    data = fetch_json(url)
    if not data:
        return []

    results = []
    for item in data.get("results", []):
        if not isinstance(item, dict):
            continue

        title = item.get("title", "")
        link = item.get("url", "") or item.get("id", "")
        if link and not link.startswith("http"):
            link = f"https://www.loc.gov{link}"

        # Image
        thumb = ""
        image_url = item.get("image_url", [])
        if isinstance(image_url, list) and image_url:
            thumb = image_url[0]
        elif isinstance(image_url, str):
            thumb = image_url

        # Creator
        creators = item.get("contributor", []) or item.get("creator", [])
        creator = creators[0] if creators else ""

        # Date
        dates = item.get("date", "") or ""
        if isinstance(dates, list):
            dates = dates[0] if dates else ""

        # Description
        desc_list = item.get("description", [])
        desc = desc_list[0] if isinstance(desc_list, list) and desc_list else str(desc_list) if desc_list else ""

        results.append({
            "title": title,
            "url": link,
            "thumbnail_url": thumb,
            "description": desc[:500],
            "creator": creator,
            "institution": "Library of Congress",
            "date": dates,
            "rights": item.get("rights", ""),
            "source_archive": "Library of Congress",
            "hunt_source": "loc",
        })

    log(f"    → {len(results)} results")
    return results


def harvest_met(country, query_str, support=None, period=None, limit=50):
    """Query Metropolitan Museum of Art Open Access API."""
    if not query_str:
        return []

    params = {"hasImages": "true", "q": query_str}
    if period:
        y1, y2 = _parse_period(period)
        if y1 and y2:
            params["dateBegin"] = str(y1)
            params["dateEnd"] = str(y2)

    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?{urllib.parse.urlencode(params)}"
    log(f"  [met/{country}] {url[:120]}...")

    data = fetch_json(url)
    if not data or not data.get("objectIDs"):
        log(f"    -> 0 results")
        return []

    object_ids = data["objectIDs"][:min(limit, 30)]  # cap detail fetches
    log(f"    -> {data.get('total', 0)} total, fetching {len(object_ids)} details...")

    results = []
    for oid in object_ids:
        obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}"
        obj = fetch_json(obj_url)
        if not obj:
            continue

        # Skip if not public domain and no image
        primary_image = obj.get("primaryImage", "")
        if not primary_image:
            continue

        title = obj.get("title", "")
        creator = obj.get("artistDisplayName", "")
        date_str = obj.get("objectDate", "")
        medium = obj.get("medium", "")
        department = obj.get("department", "")

        results.append({
            "title": title,
            "url": obj.get("objectURL", ""),
            "thumbnail_url": obj.get("primaryImageSmall", primary_image),
            "description": f"{medium}. {department}." if medium else "",
            "creator": creator,
            "institution": "The Metropolitan Museum of Art",
            "date": date_str,
            "rights": "Public Domain" if obj.get("isPublicDomain") else obj.get("rightsAndReproduction", ""),
            "source_archive": "Met Museum",
            "hunt_source": "met",
        })

        time.sleep(0.15)  # Met rate limit: ~80 req/s but be polite

    log(f"    -> {len(results)} with images")
    return results


def harvest_va(country, query_str, support=None, period=None, limit=50):
    """Query Victoria & Albert Museum API v2."""
    if not query_str:
        return []

    params = {
        "q": query_str,
        "images_exist": "true",
        "page_size": str(min(limit, 50)),
        "page": "1",
    }
    if period:
        y1, y2 = _parse_period(period)
        if y1 and y2:
            params["year_made_from"] = str(y1)
            params["year_made_to"] = str(y2)

    url = f"https://api.vam.ac.uk/v2/objects/search?{urllib.parse.urlencode(params)}"
    log(f"  [va/{country}] {url[:120]}...")

    data = fetch_json(url)
    if not data:
        return []

    results = []
    for record in data.get("records", []):
        obj_type = record.get("objectType", "")
        primary_title = record.get("_primaryTitle", "")
        title = primary_title if primary_title else obj_type
        place = record.get("_primaryPlace", "")

        # V&A image URL
        images = record.get("_images", {})
        primary = images.get("_primary_thumbnail", "")
        iiif = images.get("_iiif_image_base_url", "")
        thumb = primary
        if iiif:
            thumb = f"{iiif}full/400,/0/default.jpg"

        maker = ""
        maker_data = record.get("_primaryMaker", {})
        if isinstance(maker_data, dict):
            maker = maker_data.get("name", "")

        date_str = record.get("_primaryDate", "")

        # Build richer description from sparse V&A data
        desc_parts = [obj_type, place, f"query: {query_str}"]
        description = ". ".join(p for p in desc_parts if p)

        results.append({
            "title": title,
            "url": f"https://collections.vam.ac.uk/item/{record.get('systemNumber', '')}",
            "thumbnail_url": thumb,
            "description": description,
            "creator": maker,
            "institution": "Victoria and Albert Museum",
            "date": date_str,
            "rights": "",
            "source_archive": "V&A Museum",
            "hunt_source": "va",
        })

    log(f"    -> {len(results)} results")
    return results


# ─── Auto-enrichment ──────────────────────────────────────────────────────

# Regime classification keywords (from enrich_urls_and_regime.py)
_FUNDACIONAL_KW = [
    "revolution", "revolução", "founding", "fundação", "independence",
    "independência", "constitution", "constituição", "phrygian",
    "broken chains", "fasces", "torch", "tocha", "proclamation",
    "semi-nude", "bare breast", "dynamic", "charging", "leading",
    "bastille", "commune", "republic proclaimed",
]
_MILITAR_KW = [
    "helmet", "elmo", "capacete", "shield", "escudo", "sword", "espada",
    "armor", "armour", "war", "guerra", "military", "militar",
    "colonial", "empire", "império", "imperial", "lion", "eagle",
    "águia", "cannon", "propaganda", "wwi", "wwii", "world war",
    "notgeld",
]
_NORMATIVO_KW = [
    "stamp", "selo", "timbre", "coin", "moeda", "monnaie", "münze",
    "seated", "sentada", "scales", "balança", "blindfold", "venda",
    "book", "livro", "laurel", "cornucopia", "semeuse", "standard",
    "definitive", "frontal", "static", "official", "circulante",
]

_WAR_YEARS = set(range(1914, 1919)) | set(range(1939, 1946))
_FOUNDING_YEARS = {1789, 1792, 1793, 1830, 1848, 1870, 1871, 1889}


def classify_regime(candidate):
    """Lightweight regime classification for hunt candidates."""
    text = f"{candidate.get('title', '')} {candidate.get('description', '')}".lower()
    year = candidate.get("year") or 0

    scores = {"fundacional": 0, "normativo": 0, "militar": 0}
    for kw in _FUNDACIONAL_KW:
        if kw in text:
            scores["fundacional"] += 1
    for kw in _MILITAR_KW:
        if kw in text:
            scores["militar"] += 1
    for kw in _NORMATIVO_KW:
        if kw in text:
            scores["normativo"] += 1

    if year in _FOUNDING_YEARS:
        scores["fundacional"] += 3
    elif year in _WAR_YEARS:
        scores["militar"] += 3

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best


def infer_support(candidate):
    """Infer support type from title/description/medium."""
    text = f"{candidate.get('title', '')} {candidate.get('description', '')}".lower()
    if any(w in text for w in ["coin", "moeda", "monnaie", "münze", "penny", "franc", "dollar", "pfennig", "réis"]):
        return "moeda"
    if any(w in text for w in ["stamp", "selo", "timbre", "postage"]):
        return "selo"
    if any(w in text for w in ["monument", "statue", "sculpture", "monumento", "estátua", "denkmal"]):
        return "monumento"
    if any(w in text for w in ["print", "engraving", "gravure", "estampa", "etching", "lithograph"]):
        return "estampa"
    if any(w in text for w in ["frontispiece", "frontispice", "frontispício"]):
        return "frontispicio"
    if any(w in text for w in ["banknote", "paper money", "billet", "cédula", "papel-moeda"]):
        return "papel-moeda"
    if any(w in text for w in ["poster", "affiche", "cartaz", "propaganda"]):
        return "cartaz"
    if any(w in text for w in ["medal", "médaille", "medalha", "medaille"]):
        return "medalha"
    return None


def infer_motifs(candidate):
    """Extract likely motif tags from title/description."""
    text = f"{candidate.get('title', '')} {candidate.get('description', '')}".lower()
    motifs = []
    motif_map = {
        "marianne": "Marianne",
        "semeuse": "Semeuse",
        "britannia": "Britannia",
        "columbia": "Columbia",
        "germania": "Germania",
        "belgique": "Belgique",
        "belgica": "Belgica",
        "justitia": "Justitia",
        "justice": "Justice",
        "liberté": "Liberté",
        "liberty": "Liberty",
        "liberdade": "Liberdade",
        "freiheit": "Freiheit",
        "república": "República",
        "republic": "Republic",
        "république": "République",
        "minerva": "Minerva",
        "athena": "Athena",
        "pallas": "Pallas",
        "ceres": "Ceres",
        "fortuna": "Fortuna",
        "seated liberty": "Seated Liberty",
        "standing liberty": "Standing Liberty",
        "walking liberty": "Walking Liberty",
    }
    for kw, label in motif_map.items():
        if kw in text and label not in motifs:
            motifs.append(label)
    return motifs


def generate_abnt_citation(candidate):
    """Generate a basic ABNT NBR 6023:2025 citation for a hunt candidate."""
    parts = []

    creator = candidate.get("creator", "")
    if creator:
        # Simple surname inversion
        name_parts = creator.strip().split()
        if len(name_parts) > 1:
            parts.append(f"{name_parts[-1].upper()}, {' '.join(name_parts[:-1])}.")
        else:
            parts.append(f"{creator.upper()}.")

    title = candidate.get("title", "")
    if title:
        parts.append(f"**{title}**.")

    date_str = candidate.get("date", "")
    if date_str:
        parts.append(f"{date_str}.")

    institution = candidate.get("institution", "")
    if institution:
        parts.append(f"{institution}.")

    url = candidate.get("url", "")
    if url:
        parts.append(f"Disponível em: {url}.")
        parts.append(f"Acesso em: {date.today().strftime('%d %b. %Y')}.")

    return " ".join(parts)


def enrich_candidate(candidate):
    """Auto-enrich a candidate with regime, support, motifs, citation."""
    candidate["regime"] = classify_regime(candidate)
    candidate["support"] = infer_support(candidate)
    candidate["motif"] = infer_motifs(candidate)
    candidate["citation_abnt"] = generate_abnt_citation(candidate)

    # Add creator-based tags
    creator = (candidate.get("creator") or "").lower()
    for known in KNOWN_CREATORS:
        if known.lower() in creator:
            if "known-creator" not in candidate["tags"]:
                candidate["tags"].append("known-creator")
            break

    return candidate


# ─── Helpers ───────────────────────────────────────────────────────────────

def _xml_text(parent, tag, ns):
    """Get text content of first matching XML element."""
    el = parent.find(tag, ns)
    return el.text.strip() if el is not None and el.text else ""


def _parse_period(period_str):
    """Parse '1880-1920' into (1880, 1920)."""
    m = re.match(r"(\d{4})\s*-\s*(\d{4})", period_str)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def _normalize(text):
    """Lowercase, strip accents, strip punctuation."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


# ─── Relevance Scoring ─────────────────────────────────────────────────────

def score_relevance(result):
    """Score a raw result for relevance to the corpus (0.0–1.0)."""
    text = f"{result.get('title', '')} {result.get('description', '')}".lower()
    score = 0.0

    # Allegory keywords (+0.3)
    if any(kw in text for kw in ALLEGORY_KW):
        score += 0.3

    # Specific motif names (+0.3)
    if any(kw in text for kw in MOTIF_KW):
        score += 0.3

    # Legal/state context (+0.2)
    if any(kw in text for kw in LEGAL_STATE_KW):
        score += 0.2

    # Has image (+0.1)
    if result.get("thumbnail_url"):
        score += 0.1

    # Has institution (+0.1)
    if result.get("institution"):
        score += 0.1

    return min(score, 1.0)


# ─── Deduplication ─────────────────────────────────────────────────────────

def build_dedup_index(corpus):
    """Build sets for fast dedup lookup."""
    titles = set()
    urls = set()
    for item in corpus:
        t = item.get("title", "")
        if t:
            titles.add(_normalize(t)[:40])
        u = item.get("url", "")
        if u:
            urls.add(u.rstrip("/"))
    return titles, urls


def is_duplicate(result, title_set, url_set):
    """Check if a result duplicates an existing corpus item."""
    t = _normalize(result.get("title", ""))[:40]
    if t and t in title_set:
        return True
    u = (result.get("url", "") or "").rstrip("/")
    if u and u in url_set:
        return True
    return False


# ─── Output ────────────────────────────────────────────────────────────────

def make_candidate(result, country_code, seq, query_used):
    """Convert a raw result to a corpus-compatible candidate dict."""
    return {
        "id": f"HUNT-{country_code}-{seq:03d}",
        "title": result.get("title", ""),
        "date": result.get("date", ""),
        "year": _extract_year(result.get("date", "")),
        "period": None,
        "creator": result.get("creator", ""),
        "institution": result.get("institution", ""),
        "source_archive": result.get("source_archive", ""),
        "country": COUNTRY_NAMES.get(country_code, country_code),
        "medium": None,
        "motif": [],
        "description": result.get("description", ""),
        "url": result.get("url", ""),
        "thumbnail_url": result.get("thumbnail_url", ""),
        "rights": result.get("rights", ""),
        "tags": ["hunt-candidate", "#verificar"],
        "regime": None,
        "support": None,
        "in_scope": None,
        "hunt_score": round(score_relevance(result), 2),
        "hunt_source": result.get("hunt_source", ""),
        "hunt_query": query_used,
        "hunt_date": str(date.today()),
    }


def _extract_year(date_str):
    """Extract a 4-digit year from a date string."""
    if not date_str:
        return None
    m = re.search(r"(\d{4})", str(date_str))
    return int(m.group(1)) if m else None


# ─── Main orchestration ───────────────────────────────────────────────────

def run_hunt(countries, archives, support, period, limit, dry_run=False):
    """Run the hunt across specified countries and archives."""
    # Load corpus for dedup
    corpus = []
    if CORPUS_PATH.exists():
        with open(CORPUS_PATH, encoding="utf-8") as f:
            corpus = json.load(f)
    title_set, url_set = build_dedup_index(corpus)
    log(f"Loaded {len(corpus)} existing items for dedup")

    all_raw = []
    all_filtered = []
    all_candidates = []
    stats = {"by_country": {}, "by_archive": {}}

    for cc in countries:
        qm = QUERY_MATRIX.get(cc)
        if not qm:
            log(f"  [SKIP] No query matrix for {cc}")
            continue

        country_results = []

        # Europeana
        if "europeana" in archives and qm.get("europeana_qf"):
            if dry_run:
                log(f"  [DRY-RUN] europeana/{cc}: {qm['europeana_qf'][:80]}")
            else:
                results = harvest_europeana(cc, qm["europeana_qf"],
                                             support, period, limit)
                country_results.extend(results)
                time.sleep(0.5)

        # Gallica
        if "gallica" in archives and qm.get("gallica_sru"):
            if dry_run:
                log(f"  [DRY-RUN] gallica/{cc}: {qm['gallica_sru'][:80]}")
            else:
                results = harvest_gallica(cc, qm["gallica_sru"],
                                           support, period, limit)
                country_results.extend(results)
                time.sleep(0.5)

        # Library of Congress
        if "loc" in archives and qm.get("loc_query"):
            if dry_run:
                log(f"  [DRY-RUN] loc/{cc}: {qm['loc_query'][:80]}")
            else:
                results = harvest_loc(cc, qm["loc_query"],
                                       support, period, limit)
                country_results.extend(results)
                time.sleep(0.5)
                # LoC alt queries
                for alt_q in qm.get("loc_alt", []):
                    results = harvest_loc(cc, alt_q, support, period,
                                           max(10, limit // 3))
                    country_results.extend(results)
                    time.sleep(0.5)

        # Met Museum
        if "met" in archives and qm.get("met_query"):
            if dry_run:
                log(f"  [DRY-RUN] met/{cc}: {qm['met_query'][:80]}")
            else:
                results = harvest_met(cc, qm["met_query"],
                                       support, period, limit)
                country_results.extend(results)
                time.sleep(0.5)

        # V&A Museum
        if "va" in archives and qm.get("va_query"):
            if dry_run:
                log(f"  [DRY-RUN] va/{cc}: {qm['va_query'][:80]}")
            else:
                results = harvest_va(cc, qm["va_query"],
                                      support, period, limit)
                country_results.extend(results)
                time.sleep(0.5)

        # Europeana alt queries
        if "europeana" in archives and not dry_run:
            for alt_q in qm.get("europeana_alt", []):
                results = harvest_europeana(cc, alt_q, support, period,
                                             max(10, limit // 3))
                country_results.extend(results)
                time.sleep(0.5)

        # Gallica alt queries
        if "gallica" in archives and not dry_run:
            for alt_q in qm.get("gallica_alt", []):
                results = harvest_gallica(cc, alt_q, support, period,
                                           max(10, limit // 3))
                country_results.extend(results)
                time.sleep(0.5)

        all_raw.extend(country_results)

        # Score and filter
        scored = [(r, score_relevance(r)) for r in country_results]
        filtered = [(r, s) for r, s in scored if s >= 0.3]
        all_filtered.extend(filtered)

        # Dedup
        seq = len([c for c in all_candidates if c["id"].startswith(f"HUNT-{cc}-")]) + 1
        for r, s in filtered:
            if is_duplicate(r, title_set, url_set):
                continue
            query_used = r.get("hunt_source", "")
            candidate = make_candidate(r, cc, seq, query_used)
            enrich_candidate(candidate)
            all_candidates.append(candidate)
            # Add to dedup index
            t = _normalize(candidate["title"])[:40]
            if t:
                title_set.add(t)
            u = (candidate["url"] or "").rstrip("/")
            if u:
                url_set.add(u)
            seq += 1

            stats["by_country"][cc] = stats["by_country"].get(cc, 0) + 1
            src = r.get("hunt_source", "?")
            stats["by_archive"][src] = stats["by_archive"].get(src, 0) + 1

    # Apply global limit
    if limit and len(all_candidates) > limit:
        all_candidates = all_candidates[:limit]

    # Report
    log(f"\n{'=' * 50}")
    log(f"  HUNT REPORT")
    log(f"{'=' * 50}")
    log(f"  Archives queried: {', '.join(archives)}")
    log(f"  Countries: {', '.join(countries)}")
    log(f"  Total raw results: {len(all_raw)}")
    log(f"  After relevance filter (>=0.3): {len(all_filtered)}")
    log(f"  After dedup: {len(all_candidates)}")
    if limit:
        log(f"  Limit: {limit}")
    log(f"")
    if stats["by_country"]:
        log(f"  By country: {', '.join(f'{k}={v}' for k, v in sorted(stats['by_country'].items()))}")
    if stats["by_archive"]:
        log(f"  By archive: {', '.join(f'{k}={v}' for k, v in sorted(stats['by_archive'].items()))}")
    log(f"{'=' * 50}")

    return all_candidates


def main():
    parser = argparse.ArgumentParser(
        description="Hunt for female allegory images in digital archive APIs"
    )
    parser.add_argument("--country", type=str, default=None,
                        help="Country code(s), comma-separated (FR,UK,DE,US,BE,BR)")
    parser.add_argument("--period", type=str, default=None,
                        help="Period range, e.g. 1880-1920")
    parser.add_argument("--support", type=str, default=None,
                        help="Support type filter (moeda, selo, monumento, estampa, ...)")
    parser.add_argument("--limit", type=int, default=100,
                        help="Max candidates to emit (default: 100)")
    parser.add_argument("--archive", type=str, default=None,
                        help="Archive(s), comma-separated (europeana, gallica, loc)")
    parser.add_argument("--append", action="store_true",
                        help="Append candidates to corpus-data.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show queries without making API calls")

    args = parser.parse_args()

    # Resolve countries
    if args.country:
        countries = [c.strip().upper() for c in args.country.split(",")]
    else:
        countries = list(QUERY_MATRIX.keys())

    # Resolve archives
    if args.archive:
        archives = [a.strip().lower() for a in args.archive.split(",")]
    else:
        archives = ["europeana", "gallica", "loc", "met", "va"]

    log(f"ICONOCRACIA Hunt — {date.today()}")
    log(f"Countries: {countries} | Archives: {archives}")
    if args.period:
        log(f"Period: {args.period}")
    if args.support:
        log(f"Support: {args.support}")
    log("")

    candidates = run_hunt(
        countries=countries,
        archives=archives,
        support=args.support,
        period=args.period,
        limit=args.limit,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        log("\nDry run complete — no API calls made.")
        return

    if not candidates:
        log("\nNo candidates found.")
        return

    if args.append:
        corpus = []
        if CORPUS_PATH.exists():
            with open(CORPUS_PATH, encoding="utf-8") as f:
                corpus = json.load(f)
        corpus.extend(candidates)
        with open(CORPUS_PATH, "w", encoding="utf-8") as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)
        log(f"\nAppended {len(candidates)} candidates to {CORPUS_PATH}")
        log(f"Corpus now has {len(corpus)} items")
    else:
        # Output to stdout
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        log(f"\n{len(candidates)} candidates printed to stdout")


if __name__ == "__main__":
    main()
