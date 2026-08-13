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
