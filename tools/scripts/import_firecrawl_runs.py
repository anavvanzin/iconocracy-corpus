#!/usr/bin/env python3
"""Import notes from firecrawl runs/extract-data-2026-07-12 (1).json into vault/candidatos/."""
import json, re, os
from datetime import date
from pathlib import Path

REPO = Path("/Users/ana/Research/hub/iconocracy-corpus")
VAULT = REPO / "vault" / "candidatos"
SRC = REPO / "firecrawl runs" / "extract-data-2026-07-12 (1).json"

with open(REPO / "corpus" / "corpus-data.json") as f:
    corpus = json.load(f)
corpus_urls, corpus_titles = set(), set()
for c in corpus:
    for k in ["url", "source_url"]:
        v = c.get(k, "")
        if v: corpus_urls.add(v.lower().strip())
    t = c.get("title") or c.get("titulo") or ""
    if t: corpus_titles.add(t.lower().strip())

with open(SRC) as f:
    items = json.load(f)["national_allegory_items"]

cc_map = {"FRANCE":"FR","UNITED KINGDOM":"UK","UK":"UK","GERMANY":"DE","USA":"US",
          "UNITED STATES":"US","BELGIUM":"BE","BRAZIL":"BR"}

def is_victoria(t): return "victoria" in t.lower()
def suporte(m):
    m = m.lower()
    if "banknote" in m: return "papel-moeda"
    if "stamp" in m: return "selo"
    if "coin" in m: return "moeda"
    return "outro"
def endure(d):
    t = d.lower(); p = []
    if "clothed" in t or "armored" in t or "draped" in t or "breastplate" in t:
        p.append("dessexualização alta: corpo coberto/armado")
    elif "semi-nude" in t or "breast exposed" in t:
        p.append("dessexualização baixa: seio exposto (Type 1 Standing Liberty)")
    else: p.append("dessexualização média")
    if "seated" in t: p.append("rigidez postural alta: sentada")
    elif "standing" in t: p.append("rigidez postural baixa: em pé/em movimento")
    else: p.append("rigidez postural: estável")
    if "shield" in t or "trident" in t or "flag" in t or "union" in t:
        p.append("heraldicização alta: atributos imperiais")
    p.append("serialidade alta")
    return "; ".join(p)
def attrs(d):
    t = d.lower(); a = []
    mp = {"balança":"scales","espada":"sword","barrete frígio":"phrygian","tridente":"trident",
          "escudo":"shield","leão":"lion","capacete":"helmet","cetro":"scepter","bandeira":"flag",
          "tocha":"torch","livro":"book","coroa":"crown","venda":"blindfold","fasces":"fasces"}
    for pt, kw in mp.items():
        if kw in t: a.append(pt)
    return a
def motivo(it):
    t = it["item_title"].lower(); d = it["visual_description_body_posture"].lower()
    if is_victoria(t): return "Britannia (Victoria, monarca-personificada)"
    if "britannia" in d: return "Britannia"
    if "marianne" in t: return "Marianne"
    if "liberty" in t: return "Seated/Standing Liberty"
    if "réis" in t or "republic" in t: return "A República"
    return "Alegoria feminina"

groups = {}
for it in items:
    cc = cc_map.get(it["country"].upper(), "XX")
    groups.setdefault(cc, []).append(it)

def next_ids(cc, n):
    mx = 0
    for p in VAULT.glob(f"{cc}-*.md"):
        m = re.match(rf"^{cc}-(\d+)", p.stem)
        if m: mx = max(mx, int(m.group(1)))
    return [f"{cc}-{mx+i+1:03d}" for i in range(n)]

gen = 0
for cc, its in groups.items():
    new = []
    for it in its:
        url = (it.get("source_url") or "").lower()
        title = it.get("item_title", "").lower()
        if url in corpus_urls or any(title in t or t in title for t in corpus_titles if len(t) > 5):
            print(f"  SKIP dup: {it['item_title']}")
            continue
        new.append(it)
    ids = next_ids(cc, len(new))
    for it, iid in zip(new, ids):
        monarch = is_victoria(it["item_title"])
        d = it["visual_description_body_posture"] + " " + it["visual_description_attributes"]
        regime = "MILITAR" if monarch else "NORMATIVO"
        sup = suporte(it["medium"])
        end = endure(d); ats = attrs(d); mot = motivo(it)
        tags = ["corpus/candidato", f"pais/{cc}", f"suporte/{sup}", f"regime/{regime.lower()}",
                f"motivo/{mot.lower().replace(' ', '-').replace('(','').replace(')','')}",
                "fonte/firecrawl-agent-2026-07-12", "verificar"]
        if monarch: tags.append("tipo/monarca-personificada")
        tags_md = "\n".join(f"  - {t}" for t in tags)
        attrs_md = "\n".join(f"- [{'x' if a in ats else ' '}] {a}" for a in
            ["balança","espada","barrete frígio","tridente","escudo/brasão","leão","capacete/couraça",
             "bandeira","tocha","livro/constituição","coroa de louros","venda nos olhos","fasces","toga/vestimenta clássica"])
        related = f'  - "[[Regime {regime}]]"\n  - "[[Nachleben]]"\n  - "[[Contrato Sexual Visual]]"'
        if monarch:
            related += '\n  - "[[Marina Warner — Monuments & Maidens]]"\n  - "[[Thatcher como Britannia]]"'
        today = date.today().isoformat()
        content = f"""---
id: {iid}
tipo: corpus-candidato
status: candidato
titulo: "{it['item_title']}"
acervo: "Firecrawl Agent (Numista/Colnect)"
url: {it['source_url']}
url_iiif: null
data_estimada: "{it['year']}"
pais: {cc}
suporte: {sup}
motivo_alegorico: "{mot}"
regime: {regime}
confianca: medio
tags:
{tags_md}
related:
{related}
hf_synced: false
data_scout: {today}
fonte_scout: firecrawl-agent-2026-07-12
---

## Identificação

**Título:** {it['item_title']}
**Acervo:** Firecrawl Agent (Numista/Colnect)
**URL de acesso:** {it['source_url']}
**URL da imagem:** {it['image_url']}
**URL IIIF:** null
**Data estimada:** {it['year']}
**País:** {cc}
**Suporte:** {sup}

---

## Análise preliminar

**Motivo alegórico:** {mot}
**Regime iconocrático:** {regime}
**Descrição (Firecrawl):** {d}

**Atributos identificados:**
{attrs_md}

**endurecimento detectado:** {end}

---

## Próximos passos

- [ ] Verificar imagem em alta resolução
- [ ] Confirmar data de emissão
- [ ] Verificar duplicata no corpus
- [ ] Análise visual (iconocode-analyze)
- [ ] Código de purificação (code_purification.py)
"""
        safe = re.sub(r'[<>:"/\\|?*]', '', it['item_title'])
        (VAULT / f"{iid} {safe}.md").write_text(content, encoding="utf-8")
        gen += 1
        print(f"  ✓ {iid}: {it['item_title']}")

print(f"\n{gen} notas geradas em {VAULT}/")
