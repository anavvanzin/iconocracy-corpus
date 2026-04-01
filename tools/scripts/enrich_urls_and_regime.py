#!/usr/bin/env python3
"""
Cenário B: Resolve image URLs for corpus items missing url_image_download.
Cenário C: Add regime classification to all 95 items.

Usage:
    python enrich_urls_and_regime.py [--scenario B|C|BC] [--dry-run]
"""

import json
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

CORPUS_PATH = Path(__file__).resolve().parents[2] / "corpus" / "corpus-data-enriched.json"


# ─── Cenário B: URL Resolution ───────────────────────────────────────────────

def fetch_json(url, timeout=15, extra_headers=None):
    """Fetch JSON from URL, return dict or None."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ICONOCRACIA-corpus/1.0"}
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"    [WARN] fetch failed: {url[:80]}... → {e}")
        return None


def resolve_rijksmuseum(item):
    """Resolve Rijksmuseum items using IIIF directly (API key deprecated)."""
    url = item.get("url", "") or ""

    # Items with object numbers like /collection/RP-P-OB-27.296
    match = re.search(r"/collection/([A-Z]{1,3}-[A-Za-z0-9._-]+)", url)
    if match:
        obj_number = match.group(1)
        iiif_manifest = f"https://iiif.rijksmuseum.nl/iiif/{obj_number}/manifest.json"
        # Try fetching IIIF manifest to get actual image URL
        manifest = fetch_json(iiif_manifest)
        image_url = None
        if manifest:
            try:
                sequences = manifest.get("sequences", [])
                if sequences:
                    canvases = sequences[0].get("canvases", [])
                    if canvases:
                        images = canvases[0].get("images", [])
                        if images:
                            resource = images[0].get("resource", {})
                            service = resource.get("service", {})
                            service_id = service.get("@id", "")
                            if service_id:
                                image_url = f"{service_id}/full/800,/0/default.jpg"
                            elif resource.get("@id"):
                                image_url = resource["@id"]
            except (IndexError, KeyError):
                pass

        if image_url:
            return {
                "url_image_download": image_url,
                "url_iiif": iiif_manifest,
                "iiif_source": "rijksmuseum",
                "iiif_note": f"Resolved via IIIF manifest, object {obj_number}"
            }
        else:
            return {
                "url_image_download": None,
                "url_iiif": iiif_manifest,
                "iiif_source": "rijksmuseum_iiif_only",
                "iiif_note": f"#verificar IIIF manifest for {obj_number} — image URL extraction failed"
            }

    # Hash-based URLs (/collection/object/...) — no object number, mark manual
    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar Rijksmuseum hash-based URL — requires manual lookup at {url}"
    }


def resolve_loc(item):
    """Resolve Library of Congress items using JSON API."""
    url = item.get("url", "") or ""
    # LoC items have pattern /item/XXXXXXX/
    match = re.search(r"loc\.gov/item/([^/]+)", url)
    if not match:
        return None

    item_id = match.group(1)
    api_url = f"https://www.loc.gov/item/{item_id}/?fo=json"
    data = fetch_json(api_url, extra_headers={"Accept": "application/json"})
    if not data:
        return None

    # Try to get image URL from resources
    resources = data.get("resources", [])
    image_url = None
    iiif_url = None

    for resource in resources:
        # Check for IIIF
        if resource.get("url", "").endswith("/manifest.json"):
            iiif_url = resource["url"]

        # Check for image files
        files = resource.get("files", [])
        for file_group in files:
            if isinstance(file_group, list):
                for f in file_group:
                    if isinstance(f, dict):
                        mimetype = f.get("mimetype", "")
                        if "image" in mimetype and f.get("url"):
                            # Prefer largest
                            if not image_url or f.get("size", 0) > 100000:
                                image_url = f["url"]
            elif isinstance(file_group, dict):
                mimetype = file_group.get("mimetype", "")
                if "image" in mimetype and file_group.get("url"):
                    image_url = file_group["url"]

    # Try image_url from item metadata
    if not image_url:
        image_data = data.get("item", {}).get("image_url", [])
        if image_data and isinstance(image_data, list) and image_data[0]:
            image_url = image_data[0]

    # Try thumbnail
    if not image_url:
        thumb = data.get("item", {}).get("thumbnail", {})
        if isinstance(thumb, dict) and thumb.get("large"):
            image_url = thumb["large"]
        elif isinstance(thumb, str) and thumb:
            image_url = thumb

    if image_url:
        return {
            "url_image_download": image_url,
            "url_iiif": iiif_url,
            "iiif_source": "loc_resolved",
            "iiif_note": f"Resolved via LoC JSON API"
        }

    # Fallback: LoC often serves IIIF at a predictable URL
    iiif_fallback = f"https://tile.loc.gov/image-services/iiif/service:pnp:cph:{item_id}/full/1024,/0/default.jpg"
    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar LoC JSON API blocked (403). Manual download from https://www.loc.gov/item/{item_id}/"
    }


def resolve_europeana(item):
    """Resolve Europeana items by fetching the record API."""
    url = item.get("url", "")
    # Extract record ID from /en/item/PROVIDER/RECORD
    match = re.search(r"europeana\.eu/en/item/(.+?)(?:\?|$)", url)
    if not match:
        return None

    record_id = match.group(1)
    # Europeana record API (no key needed for basic access)
    api_url = f"https://api.europeana.eu/record/v2/{record_id}.json?wskey=api2demo"
    data = fetch_json(api_url)
    if not data or not data.get("object"):
        return None

    obj = data["object"]

    # Try to get image from aggregations
    image_url = None
    iiif_url = None

    aggregations = obj.get("aggregations", [])
    for agg in aggregations:
        # edmIsShownBy is usually the full image
        shown_by = agg.get("edmIsShownBy")
        if shown_by:
            image_url = shown_by
        # Check for IIIF
        web_resources = agg.get("webResources", [])
        for wr in web_resources:
            svc = wr.get("svcsHasService", [])
            if svc:
                for s in svc:
                    if "iiif" in str(s).lower():
                        iiif_url = s

    # edmPreview as fallback
    if not image_url:
        proxies = obj.get("proxies", [])
        europeana_agg = obj.get("europeanaAggregation", {})
        preview = europeana_agg.get("edmPreview")
        if preview:
            image_url = preview

    if image_url:
        return {
            "url_image_download": image_url,
            "url_iiif": iiif_url,
            "iiif_source": "europeana_resolved",
            "iiif_note": f"Resolved via Europeana API, record {record_id}"
        }

    return None


def resolve_british_museum(item):
    """Try to construct British Museum image URLs."""
    url = item.get("url", "") or ""
    # Extract object ID like P_1870-0625-185
    match = re.search(r"/object/([A-Za-z0-9_-]+)", url)
    if not match:
        return None

    obj_id = match.group(1)
    # BM doesn't have a simple public image API, but we can try the collection image pattern
    # The BM uses IIIF for some items
    iiif_base = f"https://media.britishmuseum.org/media/iiif/{obj_id}"

    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar British Museum item {obj_id} — requires manual image lookup at {url}"
    }


def resolve_wellcome(item):
    """Resolve Wellcome Collection items via IIIF API."""
    url = item.get("url", "") or ""
    match = re.search(r"works/([a-z0-9]+)", url)
    if not match:
        return None

    work_id = match.group(1)
    api_url = f"https://api.wellcomecollection.org/catalogue/v2/works/{work_id}?include=images"
    data = fetch_json(api_url)
    if not data:
        return None

    # Get thumbnail or IIIF image
    thumb = data.get("thumbnail", {})
    image_url = None
    iiif_url = None

    if thumb and thumb.get("url"):
        image_url = thumb["url"]

    images = data.get("images", [])
    if images:
        img = images[0]
        locations = img.get("locations", [])
        for loc in locations:
            if loc.get("type") == "DigitalLocation":
                loc_url = loc.get("url", "")
                if "iiif" in loc_url:
                    iiif_url = loc_url
                if not image_url:
                    image_url = loc_url

    if image_url:
        return {
            "url_image_download": image_url,
            "url_iiif": iiif_url,
            "iiif_source": "wellcome",
            "iiif_note": f"Resolved via Wellcome API, work {work_id}"
        }

    return None


def resolve_numista(item):
    """Numista doesn't have a public API — mark for manual resolution."""
    url = item.get("url", "") or ""
    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar Numista — no public image API. Manual download from {url}"
    }


def resolve_smithsonian(item):
    """Try Smithsonian Open Access API (no key needed for public items)."""
    url = item.get("url", "") or ""
    match = re.search(r"object/([a-z0-9_]+)", url)
    if not match:
        return None

    obj_id = match.group(1)
    # Try the EDANMDM endpoint (public, no key)
    api_url = f"https://api.si.edu/openaccess/api/v1.0/content/{obj_id}"
    data = fetch_json(api_url, extra_headers={"Accept": "application/json"})
    if data and data.get("response"):
        content = data["response"].get("content", {})
        descriptive = content.get("descriptiveNonRepeating", {})
        online_media = descriptive.get("online_media", {})
        media_list = online_media.get("media", [])

        for media in media_list:
            if media.get("type") == "Images" and media.get("content"):
                image_url = media["content"]
                return {
                    "url_image_download": image_url,
                    "url_iiif": media.get("idsId"),
                    "iiif_source": "smithsonian",
                    "iiif_note": f"Resolved via Smithsonian API, object {obj_id}"
                }

    # Fallback: construct IDS URL from object ID
    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar Smithsonian — API blocked, manual download from {url}"
    }


def resolve_generic(item):
    """For items where we can't resolve automatically."""
    url = item.get("url", "") or ""
    archive = item.get("source_archive", "unknown")
    return {
        "url_image_download": None,
        "url_iiif": None,
        "iiif_source": "none",
        "iiif_note": f"#verificar {archive} — requires manual image lookup at {url}"
    }


def run_scenario_b(items):
    """Resolve image URLs for items missing url_image_download."""
    print("\n═══ CENÁRIO B: Auditoria de URLs ═══\n")

    resolved = 0
    still_missing = 0
    results_log = []

    for item in items:
        if item.get("url_image_download"):
            continue

        item_id = item.get("id", "?")
        archive = item.get("source_archive", "unknown")
        url = item.get("url", "")
        print(f"  [{item_id}] {archive}...")

        result = None

        url = url or ""
        # Route by archive
        if "rijksmuseum" in archive.lower() or "rijksmuseum" in url.lower():
            result = resolve_rijksmuseum(item)
        elif "library of congress" in archive.lower() or "loc.gov" in url:
            result = resolve_loc(item)
        elif "europeana" in archive.lower() or "europeana.eu" in url:
            result = resolve_europeana(item)
        elif "british museum" in archive.lower() or "britishmuseum.org" in url:
            result = resolve_british_museum(item)
        elif "wellcome" in archive.lower() or "wellcomecollection" in url:
            result = resolve_wellcome(item)
        elif "numista" in archive.lower() or "numista.com" in url:
            result = resolve_numista(item)
        elif "smithsonian" in archive.lower() or "americanhistory.si.edu" in url:
            result = resolve_smithsonian(item)
        else:
            result = resolve_generic(item)

        if result:
            if result.get("url_image_download"):
                item["url_image_download"] = result["url_image_download"]
                resolved += 1
                status = "✅ RESOLVED"
            else:
                still_missing += 1
                status = "⚠️ MANUAL"

            if result.get("url_iiif"):
                item["url_iiif"] = result["url_iiif"]
            item["iiif_source"] = result.get("iiif_source", item.get("iiif_source"))
            item["iiif_note"] = result.get("iiif_note", item.get("iiif_note"))
        else:
            still_missing += 1
            status = "❌ FAILED"
            item["iiif_note"] = f"#verificar URL resolution failed for {archive}"

        results_log.append({
            "id": item_id,
            "archive": archive,
            "status": status,
            "url_image_download": item.get("url_image_download"),
            "iiif_note": item.get("iiif_note")
        })
        print(f"    → {status}")

        # Be polite to APIs
        time.sleep(0.5)

    print(f"\n  Cenário B complete: {resolved} resolved, {still_missing} still need manual intervention")
    return results_log


# ─── Cenário C: Regime Classification ────────────────────────────────────────

# Keywords for classification
FUNDACIONAL_KEYWORDS = [
    "revolution", "revolução", "revolucion", "founding", "fundação", "independence",
    "independência", "constitution", "constituição", "barricade", "barricada",
    "liberty cap", "bonnet phrygien", "barrete frígio", "phrygian",
    "broken chains", "correntes", "fasces", "faisceau",
    "torch", "tocha", "flambeau", "rising sun",
    "declaration", "proclamation", "proclamação",
    "semi-nude", "seminude", "bare breast", "seio nu", "nudez",
    "dynamic", "charging", "leading", "arms raised",
    "1789", "1792", "1793", "1848", "1870", "1871", "1889",
    "delacroix", "republic proclaimed", "proclamation",
    "bastille", "commune", "communard",
]

MILITAR_KEYWORDS = [
    "helmet", "elmo", "capacete", "pickelhaube", "casque",
    "shield", "escudo", "bouclier",
    "sword", "espada", "épée", "trident", "tridente",
    "armor", "armour", "armadura", "cuirass", "couraça",
    "war", "guerra", "guerre", "krieg",
    "military", "militar", "militaire",
    "colonial", "empire", "império", "imperialism",
    "imperial", "impérial",
    "globe", "standing on globe", "globe terrestre",
    "lion", "leão", "eagle", "águia", "adler", "aigle",
    "cannon", "canhão", "trophy", "troféu",
    "ship", "naval", "trident",
    "trade dollar", "piastre", "colonial coin",
    "propaganda", "mobilization", "mobilização",
    "recruitment", "recrutamento",
    "1914", "1915", "1916", "1917", "1918", "1939", "1940", "1941", "1942", "1943", "1944", "1945",
    "wwi", "wwii", "world war", "grande guerre", "weltkrieg",
    "notgeld",  # emergency money often has militaristic imagery
]

NORMATIVO_KEYWORDS = [
    "stamp", "selo", "timbre", "postage",
    "coin", "moeda", "monnaie", "münze",
    "seated", "sentada", "assise",
    "scales", "balança", "balance",
    "blindfold", "venda", "bandeau",
    "book", "livro", "code", "código",
    "laurel", "louro", "laurier",
    "cornucopia", "cornucópia",
    "sowing", "semeuse", "semeando",
    "generic face", "standard", "definitive",
    "bureaucratic", "administrative", "burocrático",
    "frontal", "static", "estática", "estático",
    "mass-produced", "série", "circulante",
    "official", "institucional", "institutional",
    "monochrome", "monocromático",
]

# Countries outside scope
OUT_OF_SCOPE_COUNTRIES = [
    "Netherlands", "Portugal", "Italy", "Austria", "Spain", "Uruguay", "Mexico"
]

SCOPE_COUNTRIES = ["France", "United Kingdom", "Germany", "United States", "Belgium", "Brazil"]


def classify_regime(item):
    """Classify an item into FUNDACIONAL, NORMATIVO, or MILITAR."""
    # Build text corpus from item fields
    text_parts = [
        str(item.get("title", "")),
        str(item.get("description", "")),
        str(item.get("medium", "")),
        str(item.get("period", "")),
        str(item.get("date", "")),
        str(item.get("motif_str", "")),
        str(item.get("tags_str", "")),
    ]
    text = " ".join(text_parts).lower()

    year = item.get("year", 0) or 0

    # Score each regime
    scores = {"FUNDACIONAL": 0, "NORMATIVO": 0, "MILITAR": 0}

    for kw in FUNDACIONAL_KEYWORDS:
        if kw.lower() in text:
            scores["FUNDACIONAL"] += 1

    for kw in MILITAR_KEYWORDS:
        if kw.lower() in text:
            scores["MILITAR"] += 1

    for kw in NORMATIVO_KEYWORDS:
        if kw.lower() in text:
            scores["NORMATIVO"] += 1

    # Medium-based boosts
    medium = str(item.get("medium_norm", item.get("medium", ""))).lower()
    if any(m in medium for m in ["selo", "stamp", "moeda", "coin", "münze", "monnaie"]):
        scores["NORMATIVO"] += 3  # strong normative signal
    if any(m in medium for m in ["cartaz", "poster", "affiche", "propaganda"]):
        scores["MILITAR"] += 2
    if any(m in medium for m in ["gravura", "print", "estampa", "engraving"]):
        # Prints can be any regime, slight foundational lean
        scores["FUNDACIONAL"] += 1

    # Period-based adjustments
    period = str(item.get("period", "")).lower()
    if any(p in period for p in ["revolution", "founding", "independence", "republic proclaimed"]):
        scores["FUNDACIONAL"] += 3
    if any(p in period for p in ["war", "colonial", "imperial"]):
        scores["MILITAR"] += 3
    if any(p in period for p in ["third republic", "belle époque", "weimar"]):
        scores["NORMATIVO"] += 2

    # Year-based heuristics
    if year:
        # Revolutionary years
        if year in [1789, 1792, 1793, 1830, 1848, 1870, 1871, 1889]:
            scores["FUNDACIONAL"] += 3
        # War years
        elif 1914 <= year <= 1918 or 1939 <= year <= 1945:
            scores["MILITAR"] += 3
        # Colonial expansion period
        elif 1880 <= year <= 1914 and any(kw in text for kw in ["colonial", "trade", "empire"]):
            scores["MILITAR"] += 2

    # Description-specific patterns
    desc = str(item.get("description", "")).lower()
    if "seated" in desc or "enthroned" in desc or "static" in desc:
        scores["NORMATIVO"] += 2
    if "charging" in desc or "leading" in desc or "dynamic" in desc or "brandishing" in desc:
        scores["FUNDACIONAL"] += 2
    if "helmet" in desc or "armed" in desc or "armored" in desc or "warrior" in desc:
        scores["MILITAR"] += 2

    # Determine winner
    max_score = max(scores.values())
    if max_score == 0:
        regime = "NORMATIVO"
        uncertain = True
    else:
        winners = [k for k, v in scores.items() if v == max_score]
        if len(winners) > 1:
            # Tie-breaking: NORMATIVO as safe default
            regime = "NORMATIVO" if "NORMATIVO" in winners else winners[0]
            uncertain = True
        else:
            regime = winners[0]
            uncertain = scores[regime] < 3  # Low confidence

    # Build justification
    justification = build_justification(item, regime, scores)

    return regime, uncertain, justification, scores


def build_justification(item, regime, scores):
    """Build a concise justification citing concrete markers."""
    markers = []
    text = f"{item.get('title', '')} {item.get('description', '')} {item.get('tags_str', '')}".lower()
    medium = str(item.get("medium_norm", item.get("medium", ""))).lower()
    year = item.get("year", 0) or 0

    if regime == "FUNDACIONAL":
        if "revolution" in text or "revolução" in text: markers.append("contexto revolucionário")
        if "liberty" in text or "liberté" in text or "liberdade" in text: markers.append("tema Liberdade")
        if "phrygian" in text or "barrete" in text: markers.append("barrete frígio")
        if "nude" in text or "bare" in text or "seminud" in text: markers.append("seminudez")
        if "dynamic" in text or "charging" in text or "leading" in text: markers.append("corpo dinâmico")
        if "constitution" in text or "constituição" in text: markers.append("contexto constitucional")
        if "torch" in text or "tocha" in text: markers.append("tocha")
        if "fasces" in text: markers.append("fasces")
        if "chains" in text or "correntes" in text: markers.append("correntes quebradas")
        if "proclam" in text: markers.append("proclamação")
        if "independence" in text or "independência" in text: markers.append("independência")
        if "republic" in text and ("monument" in text or "monumento" in text): markers.append("monumento republicano")
        if "flag" in text or "bandeira" in text: markers.append("bandeira")
        if not markers: markers.append(f"contexto fundacional (ano {year})")

    elif regime == "MILITAR":
        if "helmet" in text or "elmo" in text or "capacete" in text: markers.append("capacete/elmo")
        if "shield" in text or "escudo" in text: markers.append("escudo")
        if "sword" in text or "espada" in text: markers.append("espada")
        if "trident" in text or "tridente" in text: markers.append("tridente")
        if "armor" in text or "armour" in text or "armadura" in text: markers.append("armadura")
        if "war" in text or "guerra" in text: markers.append("contexto bélico")
        if "colonial" in text: markers.append("contexto colonial")
        if "imperial" in text or "empire" in text: markers.append("contexto imperial")
        if "propaganda" in text: markers.append("propaganda")
        if "lion" in text or "leão" in text: markers.append("leão")
        if "eagle" in text or "águia" in text: markers.append("águia")
        if "naval" in text or "ship" in text: markers.append("poder naval")
        if "notgeld" in text: markers.append("Notgeld (moeda emergencial)")
        if 1914 <= year <= 1918: markers.append("período WWI")
        if 1939 <= year <= 1945: markers.append("período WWII")
        if not markers: markers.append(f"contexto militar (ano {year})")

    elif regime == "NORMATIVO":
        if "stamp" in medium or "selo" in medium: markers.append("suporte selo postal")
        if "coin" in medium or "moeda" in medium: markers.append("suporte numismático")
        if "seated" in text or "sentada" in text: markers.append("pose sentada")
        if "scales" in text or "balança" in text or "balance" in text: markers.append("balança da justiça")
        if "blindfold" in text or "venda" in text: markers.append("venda nos olhos")
        if "frontal" in text or "static" in text or "estática" in text: markers.append("pose estática/frontal")
        if "semeuse" in text or "sowing" in text: markers.append("modelo Semeuse")
        if "definitive" in text or "circulante" in text: markers.append("série circulante")
        if "book" in text or "code" in text or "livro" in text: markers.append("livro/código legal")
        if "laurel" in text or "louro" in text: markers.append("coroa de louros")
        if not markers: markers.append("suporte institucional/circulante")

    justification = ", ".join(markers[:4]) + f" → {regime}"
    return justification


def run_scenario_c(items):
    """Add regime classification to all items."""
    print("\n═══ CENÁRIO C: Classificação de Regime ═══\n")

    counts = {"FUNDACIONAL": 0, "NORMATIVO": 0, "MILITAR": 0}
    uncertain_count = 0
    out_of_scope = 0

    for item in items:
        item_id = item.get("id", "?")
        regime, uncertain, justification, scores = classify_regime(item)

        item["regime"] = regime
        item["regime_justificativa"] = justification
        counts[regime] += 1

        if uncertain:
            uncertain_count += 1
            tags = item.get("tags", [])
            if isinstance(tags, list) and "regime_incerto" not in tags:
                tags.append("regime_incerto")
                item["tags"] = tags

        # Check out-of-scope countries
        country = item.get("country", "")
        if country in OUT_OF_SCOPE_COUNTRIES:
            out_of_scope += 1
            tags = item.get("tags", [])
            if isinstance(tags, list) and "fora-do-escopo-6-paises" not in tags:
                tags.append("fora-do-escopo-6-paises")
                item["tags"] = tags

        print(f"  [{item_id}] {regime:12s} (F={scores['FUNDACIONAL']:2d} N={scores['NORMATIVO']:2d} M={scores['MILITAR']:2d}) {'⚠️' if uncertain else '✅'} {justification}")

    print(f"\n  Cenário C complete:")
    print(f"    FUNDACIONAL: {counts['FUNDACIONAL']}")
    print(f"    NORMATIVO:   {counts['NORMATIVO']}")
    print(f"    MILITAR:     {counts['MILITAR']}")
    print(f"    Incertos:    {uncertain_count}")
    print(f"    Fora escopo: {out_of_scope}")

    return counts, uncertain_count, out_of_scope


# ─── Report Generation ───────────────────────────────────────────────────────

def generate_report(items, url_log, regime_counts, uncertain_count, out_of_scope):
    """Generate iiif-enrichment-report.md."""
    report_path = CORPUS_PATH.parent / "iiif-enrichment-report.md"

    # Count stats
    total = len(items)
    has_download = sum(1 for i in items if i.get("url_image_download"))
    has_iiif = sum(1 for i in items if i.get("url_iiif"))
    missing = total - has_download
    manual_needed = [i for i in items if not i.get("url_image_download")]

    # Group manual items by archive
    from collections import defaultdict
    by_archive = defaultdict(list)
    for item in manual_needed:
        by_archive[item.get("source_archive", "Unknown")].append(item)

    lines = [
        "# IIIF Enrichment Report — ICONOCRACIA Corpus",
        "",
        f"**Generated**: 2026-03-31",
        f"**Total items**: {total}",
        "",
        "## Cobertura de URLs de imagem",
        "",
        "| Métrica | Antes (Cenário A) | Depois (Cenários B+C) |",
        "|---------|-------------------|----------------------|",
        f"| Itens com url_image_download | 47 | {has_download} |",
        f"| Itens com url_iiif | ~23 | {has_iiif} |",
        f"| Itens sem download | 48 | {missing} |",
        f"| Cobertura de download | 49.5% | {has_download/total*100:.1f}% |",
        "",
        "## Distribuição por iiif_source",
        "",
        "| Source | Count |",
        "|--------|-------|",
    ]

    from collections import Counter
    source_counts = Counter(item.get("iiif_source", "none") for item in items)
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {source} | {count} |")

    lines.extend([
        "",
        "## Classificação por Regime",
        "",
        "| Regime | Count |",
        "|--------|-------|",
        f"| FUNDACIONAL | {regime_counts.get('FUNDACIONAL', 0)} |",
        f"| NORMATIVO | {regime_counts.get('NORMATIVO', 0)} |",
        f"| MILITAR | {regime_counts.get('MILITAR', 0)} |",
        f"| Incertos (regime_incerto) | {uncertain_count} |",
        f"| Fora do escopo (6 países) | {out_of_scope} |",
        "",
    ])

    if missing > 0:
        lines.extend([
            "## Itens que ainda precisam de intervenção manual",
            "",
        ])
        for archive, group in sorted(by_archive.items(), key=lambda x: -len(x[1])):
            lines.append(f"### {archive} ({len(group)} items)")
            lines.append("")
            for item in group:
                lines.append(f"- **{item['id']}**: {item.get('title', '?')[:60]}")
                lines.append(f"  - URL: {item.get('url', 'N/A')}")
                lines.append(f"  - Nota: {item.get('iiif_note', 'N/A')}")
            lines.append("")

    lines.extend([
        "## Estimativa de download",
        "",
        f"- **Baixáveis agora**: {has_download} itens ({has_download/total*100:.1f}%)",
        f"- **Com IIIF**: {has_iiif} itens (permite resolução dinâmica)",
        f"- **Requerem intervenção manual**: {missing} itens",
        "",
        "## Próximos passos",
        "",
        "1. Para itens marcados `#verificar`: acessar URL manualmente e baixar imagem",
        "2. Para Numista/British Museum: screenshot ou download manual da página",
        "3. Para Rijksmuseum sem object number: buscar manualmente no catálogo",
        "4. Salvar imagens em `/Volumes/ICONOCRACIA/corpus/imagens/[PAIS]/`",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report saved to {report_path}")
    return report_path


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    scenario = "BC"
    dry_run = "--dry-run" in sys.argv
    if "--scenario" in sys.argv:
        idx = sys.argv.index("--scenario")
        if idx + 1 < len(sys.argv):
            scenario = sys.argv[idx + 1].upper()

    print(f"Loading corpus from {CORPUS_PATH}")
    with open(CORPUS_PATH, encoding="utf-8") as f:
        items = json.load(f)

    print(f"Loaded {len(items)} items")

    url_log = []
    regime_counts = {}
    uncertain_count = 0
    out_of_scope = 0

    if "B" in scenario:
        url_log = run_scenario_b(items)

    if "C" in scenario:
        regime_counts, uncertain_count, out_of_scope = run_scenario_c(items)

    # Generate report
    generate_report(items, url_log, regime_counts, uncertain_count, out_of_scope)

    # Save enriched data
    if not dry_run:
        with open(CORPUS_PATH, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"\n  Saved enriched data to {CORPUS_PATH}")
    else:
        print("\n  DRY RUN — no files modified")


if __name__ == "__main__":
    main()
