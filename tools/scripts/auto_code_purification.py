#!/usr/bin/env python3
"""Auto-codes all 99 pending purification items.

1. Generates sigla IDs (CC-NNN) for items without id
2. Infers endurecimento scores from available metadata
3. Writes to purification.jsonl
4. Updates corpus-data.json with IDs

Usage: python tools/scripts/auto_code_purification.py
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
PURIFICATION_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"
RECORDS_JSONL = REPO_ROOT / "data" / "processed" / "records.jsonl"

# Abbreviation mapping: place_hint -> country code
COUNTRY_CODES = {
    "France": "FR", "['FR']": "FR", "[FR]": "FR",
    "Brazil": "BR", "['BR']": "BR", "[BR]": "BR",
    "United Kingdom": "UK", "['UK']": "UK",
    "United States": "US", "['US']": "US",
    "Germany": "DE", "['DE']": "DE", "[DE]": "DE",
    "Belgium": "BE", "['BE']": "BE", "[BE]": "BE",
    "Argentina": "AR",
    "Austria": "AT",
    "Italy": "IT",
    "Mexico": "MX",
    "Netherlands": "NL",
    "Portugal": "PT",
    "Spain": "ES",
    "Switzerland": "CH",
    "Uruguay": "UY",
}


def load_jsonl(path):
    items = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def load_json(path):
    with open(path) as f:
        return json.load(f)


def infer_regime(item, rec):
    """Extract regime from IconoCode interpretation claims."""
    interp = rec.get("iconocode", {}).get("interpretation", [])
    for i in interp:
        text = i.get("claim_text", "").upper()
        if "FUNDACIONAL" in text:
            return "fundacional"
        if "NORMATIVO" in text:
            return "normativo"
        if "MILITAR" in text:
            return "militar"
        if "CONTRA" in text:
            return "contra-alegoria"
    # Fall back to regime field in corpus
    r = item.get("regime", "")
    if r in ("fundacional", "normativo", "militar", "contra-alegoria"):
        return r
    return "fundacional"  # sensible default


def infer_scores(item, rec):
    """Infer purification scores from available metadata."""
    title = (item.get("title") or "").lower()
    desc = (item.get("description") or "").lower()
    motifs = [m.lower() for m in item.get("motif", [])]
    title_hint = (rec.get("input", {}).get("title_hint") or "").lower()
    
    iconclass_codes = set()
    for se in rec.get("webscout", {}).get("search_results", []):
        for ic in se.get("iconclass_candidates", []):
            iconclass_codes.add(ic)
    for c in rec.get("iconocode", {}).get("codes", []):
        if c.get("scheme") == "iconclass":
            iconclass_codes.add(c.get("notation", ""))

    # Classify support type
    all_text = f"{title} {desc} {title_hint}"
    
    is_coin = any(w in all_text for w in ["moeda", "coin ", "franc", "pfennig", "centime",
                                            "mark", "penny", "réis", "reis", "piastre"])
    is_stamp = any(w in all_text for w in ["selo", "stamp", "timbre", "postage", "série"])
    is_banknote = any(w in all_text for w in ["cédula", "cedula", "banknote", "notgeld",
                                              "reichsmark", "mil réis", "milreis"])
    is_poster = any(w in all_text for w in ["cartaz", "poster", "affiche"])
    is_print = any(w in all_text for w in ["estamp", "gravura", "print", "litografia",
                                            "litograph", "engrav"])
    is_photo = any(w in all_text for w in ["fotografia", "photograph", "foto"])
    is_painting = any(w in all_text for w in ["pintura", "painting", "óleo", "oleo",
                                              "oil on"])
    is_sculpture = any(w in all_text for w in ["monumento", "escultura", "sculpture",
                                               "statue", "busto"])
    is_frontispiece = any(w in all_text for w in ["frontispício", "frontispice"])
    is_textual = any(w in all_text for w in ["textual", "literary", "prosopopeia",
                                              "dialogue"])
    is_medal = any(w in all_text for w in ["medal", "medalha", "medaille"])

    if is_coin or is_banknote:
        support_class = "currency"
    elif is_stamp:
        support_class = "stamp"
    elif is_medal:
        support_class = "medal"
    elif is_poster:
        support_class = "poster"
    elif is_print:
        support_class = "print"
    elif is_photo:
        support_class = "photo"
    elif is_painting:
        support_class = "painting"
    elif is_sculpture:
        support_class = "sculpture"
    elif is_frontispiece:
        support_class = "frontispiece"
    else:
        support_class = "other"

    # Has heraldic/state elements?
    has_heraldry = any(w in all_text for w in ["brasão", "brasao", "shield", "escudo",
                                               "herald", "blason", "emblema", "insignia"])
    has_arch_framing = any(w in all_text for w in ["arquitetônico", "arquitetonico",
                                                   "architectural", "frontão", "frontao",
                                                   "column", "coluna", "portal", "pedestal"])
    is_narrative = any(w in motifs for w in ["conversation", "diálogo", "dialogo",
                                              "dialogue", "scene", "cena", "interaction"])
    
    has_justitia = "justitia" in motifs or "justice" in motifs
    has_republica = "república" in motifs or "republica" in motifs or "republic" in motifs
    has_liberty = "liberdade" in motifs or "liberty" in motifs or "liberte" in motifs
    has_germania = "germania" in motifs
    has_britannia = "brittania" in motifs or "britannia" in motifs
    
    # === Score inference ===
    
    # desincorporacao: 0=naturalistic body, 3=no body
    if is_textual or is_frontispiece:
        desincorporacao = 3
    elif is_coin or is_banknote or is_stamp:
        desincorporacao = 2  # reduced body on small format
    elif is_sculpture:
        desincorporacao = 1
    elif is_photo or is_painting:
        desincorporacao = 0
    else:
        desincorporacao = 1
    
    # rigidez_postural: 0=dynamic, 3=hieratic
    if is_coin or is_banknote or is_stamp:
        rigidez = 3  # fixed profile/static
    elif is_sculpture:
        rigidez = 2
    elif is_photo:
        rigidez = 1
    elif is_poster:
        rigidez = 1
    else:
        rigidez = 1
    
    # dessexualizacao: 0=explicit, 3=covered
    if is_sculpture:
        dessex = 2  # classical nude idealized
    elif is_coin or is_stamp:
        dessex = 3  # fully covered
    elif has_justitia:
        dessex = 2  # usually draped
    elif has_republica or has_liberty:
        dessex = 1  # often bare-breasted
    else:
        dessex = 2
    
    # uniformizacao_facial: 0=individualized, 3=no face
    if is_coin or is_stamp or is_banknote:
        uniform = 3  # standardized profile
    elif is_sculpture:
        uniform = 2  # idealized
    elif is_photo:
        uniform = 0  # real face
    elif is_painting:
        uniform = 1  # expressive
    else:
        uniform = 2
    
    # heraldizacao: 0=integrated, 3=isolated emblems
    if is_coin or is_stamp or is_banknote:
        herald = 2  # attributes as design elements
    elif has_heraldry:
        herald = 3
    elif has_justitia:
        herald = 1  # sword/scales carried
    else:
        herald = 1
    
    # enquadramento_arquitetonico: 0=open space, 3=decorative
    if is_sculpture:
        arq = 2
    elif has_arch_framing:
        arq = 2
    elif is_coin or is_stamp or is_banknote:
        arq = 2
    elif is_frontispiece:
        arq = 2
    else:
        arq = 1
    
    # apagamento_narrativo: 0=complete narrative, 3=isolated
    if is_narrative or ("conversation" in motifs):
        narr = 0
    elif is_coin or is_stamp or is_banknote:
        narr = 3
    elif is_sculpture:
        narr = 2
    elif is_painting:
        narr = 1
    elif is_frontispiece:
        narr = 2
    elif is_photo:
        narr = 1
    else:
        narr = 2
    
    # monocromatizacao: 0=polychrome, 3=monochrome
    if is_coin:
        mono = 3
    elif is_stamp or is_banknote:
        mono = 3  # limited color
    elif is_print:
        mono = 3  # typically b/w
    elif is_photo:
        mono = 3  # b/w period
    elif is_sculpture:
        mono = 2  # stone/bronze
    elif is_painting:
        mono = 0
    elif is_poster:
        mono = 1
    else:
        mono = 2
    
    # serialidade: 0=unique, 3=mass reproduction
    if is_coin or is_stamp or is_banknote:
        serial = 3
    elif is_poster:
        serial = 2
    elif is_print:
        serial = 2
    elif is_medal:
        serial = 2
    elif is_photo:
        serial = 2
    elif is_sculpture:
        serial = 0
    elif is_painting:
        serial = 0
    else:
        serial = 1
    
    # inscricao_estatal: 0=autonomous, 3=state device
    if is_coin or is_stamp or is_banknote:
        estatal = 3
    elif is_medal:
        estatal = 2
    elif is_frontispiece:
        estatal = 2
    if has_heraldry:
        estatal = 3
    elif "state" in all_text or "república" in all_text or "republic" in all_text:
        estatal = 2
    else:
        estatal = 1
    
    return {
        "desincorporacao": desincorporacao,
        "rigidez_postural": rigidez,
        "dessexualizacao": dessex,
        "uniformizacao_facial": uniform,
        "heraldizacao": herald,
        "enquadramento_arquitetonico": arq,
        "apagamento_narrativo": narr,
        "monocromatizacao": mono,
        "serialidade": serial,
        "inscricao_estatal": estatal,
    }


def get_next_id(cc, coded_ids):
    """Get next available ID for a country code."""
    existing = [int(re.search(r'\d+$', eid).group()) 
                for eid in coded_ids 
                if re.match(rf'^{re.escape(cc)}-\d+$', eid)]
    if existing:
        return f"{cc}-{max(existing) + 1:03d}"
    return f"{cc}-001"


def main():
    print("=" * 60)
    print("  Auto-Purification Coding for pending items")
    print("=" * 60)
    
    # Load data
    corpus = load_json(CORPUS_JSON)
    coded_entries = load_jsonl(PURIFICATION_JSONL)
    records = load_jsonl(RECORDS_JSONL)
    
    # Build URL->record lookup
    url2rec = {}
    for r in records:
        url2rec[r.get("input", {}).get("input_url", "")] = r
        for se in r.get("webscout", {}).get("search_results", []):
            url2rec[se.get("url", "")] = r
    
    # Existing coded IDs
    coded_ids = set(e["id"] for e in coded_entries)
    
    # Items missing IDs
    no_id_items = [item for item in corpus if not item.get("id")]
    print(f"\nItems to code: {len(no_id_items)}")
    
    # Group by country for ID generation
    from collections import defaultdict
    by_country = defaultdict(list)
    for item in no_id_items:
        url = item.get("url", "")
        rec = url2rec.get(url)
        if rec:
            ph = rec.get("input", {}).get("place_hint", "")
            if isinstance(ph, list):
                ph = ph[0] if ph else ""
            cc = COUNTRY_CODES.get(str(ph), "XX")
        else:
            cc = "XX"
        by_country[cc].append((item, rec))
    
    print("\nItems by country code:")
    for cc in sorted(by_country):
        print(f"  {cc}: {len(by_country[cc])} items")
    
    # Generate IDs and code each item
    coded_count = 0
    new_entries = []
    items_updated = []
    
    for cc in sorted(by_country):
        country_items = by_country[cc]
        for item, rec in country_items:
            # Generate ID
            new_id = get_next_id(cc, coded_ids)
            coded_ids.add(new_id)
            
            # Infer scores
            scores = infer_scores(item, rec)
            regime = infer_regime(item, rec)
            composite = round(sum(scores.values()) / len(scores), 2)
            
            # Build entry
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            entry = {
                "id": new_id,
                "title": item.get("title", ""),
                "country": item.get("country", ""),
                "year": item.get("year"),
                "period": item.get("period"),
                "medium_norm": item.get("medium_norm"),
                **scores,
                "purificacao_composto": composite,
                "regime_iconocratico": regime,
                "coded_by": "hermes-auto",
                "coded_at": now,
                "notes": "Auto-coded — verify visual scores",
            }
            
            new_entries.append(entry)
            items_updated.append((item, new_id))
            coded_count += 1
            
            title_short = (item.get("title") or "?")[:50]
            print(f"  [{coded_count:3d}/{len(no_id_items)}] {new_id:20s} "
                  f"composite={composite:.2f} regime={regime:12s} | {title_short}")
    
    # Write new entries to purification.jsonl
    with open(PURIFICATION_JSONL, "a") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"\n  ✅ Wrote {len(new_entries)} entries to {PURIFICATION_JSONL}")
    
    # Update corpus-data.json with IDs
    for item, new_id in items_updated:
        item["id"] = new_id
    
    with open(CORPUS_JSON, "w") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    # Also add country fields if missing
    for item, new_id in items_updated:
        url = item.get("url", "")
        rec = url2rec.get(url)
        if rec:
            ph = rec.get("input", {}).get("place_hint", "")
            if isinstance(ph, list):
                ph = ph[0] if ph else ""
            cc = COUNTRY_CODES.get(str(ph), "")
            country_map = {"FR": "France", "BR": "Brazil", "UK": "United Kingdom",
                          "US": "United States", "DE": "Germany", "BE": "Belgium",
                          "AR": "Argentina", "AT": "Austria", "IT": "Italy",
                          "MX": "Mexico", "NL": "Netherlands", "PT": "Portugal",
                          "ES": "Spain", "CH": "Switzerland", "UY": "Uruguay",
                          "XX": ""}
            if not item.get("country") and cc in country_map:
                item["country"] = country_map[cc]
    
    # Rewrite with country updates too
    with open(CORPUS_JSON, "w") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Updated {len(items_updated)} items in {CORPUS_JSON} with IDs")
    
    # Show summary
    all_coded = set()
    with open(PURIFICATION_JSONL) as f:
        for line in f:
            e = json.loads(line)
            all_coded.add(e["id"])
    
    total = len(corpus)
    done = len(all_coded)
    print(f"\n{'=' * 50}")
    print(f"  Final: {done}/{total} coded ({done/total*100:.0f}%)")
    print(f"{'=' * 50}")
    
    # Stats
    composites = []
    regimes = Counter()
    with open(PURIFICATION_JSONL) as f:
        for line in f:
            e = json.loads(line)
            composites.append(e.get("purificacao_composto", 0))
            regimes[e.get("regime_iconocratico", "?")] += 1
    
    print(f"  Composite range: {min(composites):.2f} - {max(composites):.2f}")
    print(f"  Composite mean: {sum(composites)/len(composites):.2f}")
    print(f"  By regime: {dict(regimes)}")


if __name__ == "__main__":
    main()
