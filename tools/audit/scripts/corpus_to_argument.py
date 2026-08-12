#!/usr/bin/env python3
"""
corpus_to_argument.py — Gerador narrativo automático para o corpus Iconocracia
PPGD/UFSC · Ana Vitória Vanzin Mendes · 2026

Percorre records.jsonl e gera parágrafos argumentativos agrupados por:
  - País
  - Regime iconocrático
  - Motivo alegórico

Cada parágrafo termina com a referência ao ID do corpus.
Lacunas Panofsky aparecem como [LACUNA] no texto — forçando priorização visual.

Uso:
  python corpus_to_argument.py records.jsonl --mode cap3        # caso francês
  python corpus_to_argument.py records.jsonl --mode country BR  # por país
  python corpus_to_argument.py records.jsonl --mode regime FUNDACIONAL
  python corpus_to_argument.py records.jsonl --mode full        # relatório completo

Saída: Markdown com estrutura pronta para colar em Capítulo 3.
"""

import json
import argparse
import sys
import re
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# NORMALIZAÇÃO DE CAMPOS
# ─────────────────────────────────────────────────────────────────────────────

REGIME_NORM = {
    "FUNDACIONAL": "fundacional",
    "NORMATIVO": "normativo",
    "MILITAR": "militar",
    "CONTRA-ALEGORIA": "contra-alegoria",
    "CONTRA_ALEGORIA": "contra-alegoria",
}

COUNTRY_NAMES = {
    "France": "França",
    "Brazil": "Brasil",
    "United States": "Estados Unidos",
    "United Kingdom": "Reino Unido",
    "Germany": "Alemanha",
    "Italy": "Itália",
    "Portugal": "Portugal",
    "Belgium": "Bélgica",
    "Netherlands": "Países Baixos",
    "Spain": "Espanha",
    "Argentina": "Argentina",
    "Chile": "Chile",
}

def normalize_regime(raw: str) -> str:
    """Extrai e normaliza rótulo de regime da claim_text."""
    if not raw:
        return "pendente"
    m = re.search(r"REGIME\s+ICONOCRÁTICO[:\s]+([A-ZÁ\-_]+)", raw, re.IGNORECASE)
    if m:
        token = m.group(1).strip().upper().rstrip(".")
        # limpa sub-qualificadores entre parênteses
        token = re.sub(r"\s*\(.*\)", "", token).strip()
        return REGIME_NORM.get(token, token.lower())
    if "pendente" in raw.lower():
        return "pendente"
    return "pendente"

def extract_regime(record: dict) -> str:
    interps = record.get("iconocode", {}).get("interpretation", [])
    for i in interps:
        ct = i.get("claim_text", "")
        if "regime" in ct.lower() or "Regime" in ct:
            return normalize_regime(ct)
    return "pendente"

def extract_legal_context(record: dict) -> str:
    interps = record.get("iconocode", {}).get("interpretation", [])
    for i in interps:
        if i.get("claim_type") == "legal_context":
            return i.get("claim_text", "").strip()
    return ""

def extract_iconological(record: dict) -> str:
    """Extrai a interpretação iconológica mais rica (postcolonial_marker ou legal_context)."""
    interps = record.get("iconocode", {}).get("interpretation", [])
    # preferência: postcolonial_marker (mais elaborado), depois legal_context
    for ct in ["postcolonial_marker", "iconological", "legal_context"]:
        for i in interps:
            if i.get("claim_type") == ct:
                text = i.get("claim_text", "").strip()
                if len(text) > 40:
                    return text
    # fallback: qualquer interpretação com >40 chars
    for i in interps:
        text = i.get("claim_text", "").strip()
        if len(text) > 40:
            return text
    return ""

def extract_motifs(record: dict) -> list[str]:
    pre = record.get("iconocode", {}).get("pre_iconographic", [])
    return [m.get("motif", "") for m in pre if m.get("motif")]

def extract_abnt(record: dict) -> str:
    cits = record.get("exports", {}).get("abnt_citations", [])
    if cits:
        return cits[0]
    # fallback
    inp = record.get("input", {})
    title = inp.get("title_hint", "s.t.")
    date = inp.get("date_hint", "s.d.")
    url = inp.get("input_url", "")
    return f"{title.upper()}. {date}. Disponível em: {url}."

def has_full_panofsky(record: dict) -> bool:
    """Verifica se tem os três níveis minimamente preenchidos."""
    ic = record.get("iconocode", {})
    has_pre = bool(ic.get("pre_iconographic"))
    has_interp = bool(ic.get("interpretation"))
    # verifica se interpretação tem conteúdo rico (não só tag monossilábica)
    rich = any(
        len(i.get("claim_text", "")) > 60
        for i in ic.get("interpretation", [])
    )
    return has_pre and has_interp and rich

def confidence_str(record: dict) -> str:
    c = record.get("iconocode", {}).get("confidence", None)
    if c is None:
        return ""
    if c >= 0.8:
        return "alta confiança"
    elif c >= 0.6:
        return "confiança moderada"
    else:
        return "confiança baixa — verificar"

def get_date(record: dict) -> str:
    return record.get("input", {}).get("date_hint", "s.d.")

def get_title(record: dict) -> str:
    return record.get("input", {}).get("title_hint", "[sem título]")

def get_country(record: dict) -> str:
    raw = record.get("input", {}).get("place_hint", "?")
    return COUNTRY_NAMES.get(raw, raw)

def get_item_id(record: dict) -> str:
    return record.get("item_id", "??")[:12]

def get_url(record: dict) -> str:
    results = record.get("webscout", {}).get("search_results", [])
    if results:
        return results[0].get("url", "")
    return record.get("input", {}).get("input_url", "")

def get_summary_evidence(record: dict) -> str:
    return record.get("webscout", {}).get("summary_evidence", "")

def has_flag(record: dict, flag: str) -> bool:
    flags = record.get("exports", {}).get("audit_flags", [])
    return any(flag in f for f in flags)


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR DE PARÁGRAFO POR REGISTRO
# ─────────────────────────────────────────────────────────────────────────────

def make_paragraph(record: dict, lacuna_marker: bool = True) -> str:
    """
    Gera um parágrafo argumentativo a partir de um registro.
    Se o registro tem Panofsky incompleto, insere [LACUNA] visível.
    """
    title = get_title(record)
    date = get_date(record)
    country = get_country(record)
    motifs = extract_motifs(record)
    regime = extract_regime(record)
    legal_ctx = extract_legal_context(record)
    iconological = extract_iconological(record)
    abnt = extract_abnt(record)
    item_id = get_item_id(record)
    conf = confidence_str(record)
    summary = get_summary_evidence(record)
    full_panof = has_full_panofsky(record)
    no_thumbnail = has_flag(record, "sem-thumbnail") or has_flag(record, "no-image")

    motif_str = ", ".join(motifs[:4]) if motifs else "[motivo não identificado]"

    # cabeçalho do parágrafo
    lines = []

    # marcador de lacuna no início, se aplicável
    lacuna_tag = ""
    if not full_panof and lacuna_marker:
        lacuna_tag = " `[LACUNA PANOFSKY]`"
    if no_thumbnail and lacuna_marker:
        lacuna_tag += " `[SEM IMAGEM]`"

    # primeira frase: contextualização factual (nível pré-iconográfico)
    if summary:
        opening = summary[:300].rstrip(".") + "."
    else:
        opening = f"*{title}* ({date}, {country}) representa {motif_str.lower()}."

    # segunda frase: interpretação iconográfica
    if legal_ctx and len(legal_ctx) > 40:
        second = legal_ctx
        if not second.endswith("."):
            second += "."
    else:
        second = ""

    # terceira frase: leitura iconológica / hipótese
    if iconological and len(iconological) > 40:
        # truncar se muito longo
        third = iconological[:500]
        if not third.endswith("."):
            third = third.rstrip() + "."
    else:
        third = f"[LACUNA: interpretação iconológica ausente — codificar antes do freeze]{lacuna_tag}"

    # referência
    ref_note = f"(corpus: `{item_id}`, regime: **{regime}**"
    if conf:
        ref_note += f", {conf}"
    ref_note += ")"

    # montar parágrafo
    paragraph = f"{opening}"
    if second:
        paragraph += f" {second}"
    paragraph += f" {third}"
    if lacuna_tag and full_panof:  # thumbnail ausente mas panofsky ok
        paragraph += lacuna_tag
    paragraph += f"\n\n> {ref_note}\n> {abnt}"

    return paragraph.strip()


# ─────────────────────────────────────────────────────────────────────────────
# MODOS DE SAÍDA
# ─────────────────────────────────────────────────────────────────────────────

def mode_country(records: list, country_filter: str) -> str:
    """Gera narrativa agrupada por regime para um país específico."""
    # normalizar filtro
    country_map_rev = {v: k for k, v in COUNTRY_NAMES.items()}
    country_filter_en = country_map_rev.get(country_filter, country_filter)

    filtered = [
        r for r in records
        if country_filter_en.lower() in r.get("input", {}).get("place_hint", "").lower()
        or country_filter.lower() in r.get("input", {}).get("place_hint", "").lower()
    ]

    if not filtered:
        return f"Nenhum registro encontrado para: {country_filter}"

    country_name = COUNTRY_NAMES.get(filtered[0].get("input", {}).get("place_hint", ""), country_filter)
    
    out = [f"# Narrativa do corpus — {country_name}\n"]
    out.append(f"*{len(filtered)} registros · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n")

    # estatísticas
    by_regime = defaultdict(list)
    for r in filtered:
        by_regime[extract_regime(r)].append(r)

    out.append("## Distribuição por regime\n")
    for reg, recs in sorted(by_regime.items(), key=lambda x: -len(x[1])):
        lacunas = sum(1 for r in recs if not has_full_panofsky(r))
        out.append(f"- **{reg}**: {len(recs)} registros ({lacunas} com lacuna Panofsky)")
    out.append("")

    # parágrafos por regime
    regime_order = ["fundacional", "normativo", "militar", "contra-alegoria", "pendente"]
    for reg in regime_order:
        recs = by_regime.get(reg, [])
        if not recs:
            continue
        out.append(f"## Regime {reg} ({len(recs)} registros)\n")
        # ordenar por data
        recs_sorted = sorted(recs, key=lambda r: r.get("input", {}).get("date_hint", "0"))
        for rec in recs_sorted:
            out.append(make_paragraph(rec))
            out.append("")

    return "\n".join(out)


def mode_regime(records: list, regime_filter: str) -> str:
    """Gera narrativa agrupada por país para um regime específico."""
    norm = REGIME_NORM.get(regime_filter.upper(), regime_filter.lower())
    
    filtered = [r for r in records if extract_regime(r) == norm]
    if not filtered:
        # tenta match parcial
        filtered = [r for r in records if regime_filter.lower() in extract_regime(r)]

    if not filtered:
        return f"Nenhum registro para regime: {regime_filter}"

    out = [f"# Narrativa do corpus — Regime {norm}\n"]
    out.append(f"*{len(filtered)} registros · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n")

    by_country = defaultdict(list)
    for r in filtered:
        country = get_country(r)
        by_country[country].append(r)

    # estatísticas
    out.append("## Distribuição geográfica\n")
    for c, recs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        lacunas = sum(1 for r in recs if not has_full_panofsky(r))
        out.append(f"- **{c}**: {len(recs)} registros ({lacunas} com lacuna Panofsky)")
    out.append("")

    # parágrafos por país
    for country, recs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        out.append(f"## {country} ({len(recs)} registros)\n")
        recs_sorted = sorted(recs, key=lambda r: r.get("input", {}).get("date_hint", "0"))
        for rec in recs_sorted:
            out.append(make_paragraph(rec))
            out.append("")

    return "\n".join(out)


def mode_cap3(records: list) -> str:
    """
    Modo especial: Capítulo 3 — O caso francês.
    Gera narrativa cronológica dos 90 registros franceses,
    com seções por regime e parágrafo de lacunas consolidado no final.
    """
    french = [
        r for r in records
        if "france" in r.get("input", {}).get("place_hint", "").lower()
    ]

    out = [
        "# Capítulo 3 — O caso francês: alegoria feminina e legitimação jurídica",
        f"*(corpus: {len(french)} registros · gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')})*",
        "",
        "> **Nota metodológica:** Este texto foi gerado automaticamente a partir do corpus codificado.",
        "> Parágrafos marcados com `[LACUNA PANOFSKY]` indicam registros com codificação incompleta.",
        "> Parágrafos marcados com `[SEM IMAGEM]` indicam registros sem thumbnail verificado.",
        "> Todos os itens devem ser revisados antes do freeze do dataset.",
        "",
    ]

    by_regime = defaultdict(list)
    for r in french:
        by_regime[extract_regime(r)].append(r)

    # sumário
    out.append("## 3.0 Estado do corpus francês\n")
    total_lacunas = sum(1 for r in french if not has_full_panofsky(r))
    out.append(f"O corpus francês conta com **{len(french)} registros** distribuídos em quatro regimes "
               f"iconocráticos. Destes, **{total_lacunas} apresentam lacuna Panofsky** — codificação "
               f"iconológica ausente ou monossilábica — e devem ser priorizados antes do freeze.\n")

    for reg, recs in sorted(by_regime.items(), key=lambda x: -len(x[1])):
        lacunas = sum(1 for r in recs if not has_full_panofsky(r))
        datas = [r.get("input", {}).get("date_hint", "s.d.") for r in recs]
        datas_sorted = sorted(d for d in datas if d != "s.d.")
        span = f"{datas_sorted[0]}–{datas_sorted[-1]}" if len(datas_sorted) >= 2 else (datas_sorted[0] if datas_sorted else "s.d.")
        out.append(f"- **{reg}**: {len(recs)} registros ({span}) · {lacunas} com lacuna")
    out.append("")

    # seções por regime
    regime_order = ["fundacional", "normativo", "militar", "contra-alegoria", "pendente"]
    regime_subtitles = {
        "fundacional": "3.1 O regime fundacional: alegoria como fundação republicana (1789–1870)",
        "normativo": "3.2 O regime normativo: codificação e estabilização iconográfica (1870–1940)",
        "militar": "3.3 O regime militar: endurecimento e mobilização bélica (1870–1945)",
        "contra-alegoria": "3.4 Contra-alegoria: inversão, sátira e conflito de imagens",
        "pendente": "3.5 Registros pendentes de classificação [NÃO INCLUIR NO DRAFT FINAL]",
    }

    for reg in regime_order:
        recs = by_regime.get(reg, [])
        if not recs:
            continue
        
        subtitle = regime_subtitles.get(reg, f"## Regime {reg}")
        out.append(f"## {subtitle}\n")

        # parágrafo introdutório do regime
        intro = _regime_intro_fr(reg, recs)
        out.append(intro)
        out.append("")

        # parágrafos individuais, ordenados cronologicamente
        recs_sorted = sorted(recs, key=lambda r: r.get("input", {}).get("date_hint", "0"))
        for rec in recs_sorted:
            out.append(make_paragraph(rec))
            out.append("---")
            out.append("")

    # consolidação de lacunas no final
    lacunas_list = [(r, extract_regime(r)) for r in french if not has_full_panofsky(r)]
    if lacunas_list:
        out.append("## Apêndice 3.A — Registros com lacuna Panofsky (prioridade de codificação)\n")
        out.append(f"*{len(lacunas_list)} registros aguardando codificação iconológica completa.*\n")
        out.append("| ID | Título | Data | Regime | Tipo de lacuna |")
        out.append("|---|---|---|---|---|")
        for rec, reg in sorted(lacunas_list, key=lambda x: x[0].get("input", {}).get("date_hint", "0")):
            item_id = get_item_id(rec)
            title = get_title(rec)[:50]
            date = get_date(rec)
            no_thumb = "sem imagem" if has_flag(rec, "sem-thumbnail") else ""
            no_rich = "interp. monossilábica" if not extract_iconological(rec) else ""
            tipo = ", ".join(t for t in [no_thumb, no_rich] if t) or "incompleto"
            out.append(f"| `{item_id}` | {title} | {date} | {reg} | {tipo} |")

    return "\n".join(out)


def mode_full(records: list) -> str:
    """Relatório completo com todos os países e regimes."""
    out = [
        "# Corpus Iconocracia — Relatório Narrativo Completo",
        f"*{len(records)} registros · {datetime.now().strftime('%d/%m/%Y %H:%M')}*",
        "",
    ]

    # estatísticas globais
    by_country = defaultdict(list)
    by_regime = defaultdict(list)
    for r in records:
        by_country[get_country(r)].append(r)
        by_regime[extract_regime(r)].append(r)

    total_lacunas = sum(1 for r in records if not has_full_panofsky(r))
    out.append(f"**Cobertura Panofsky completa:** {len(records) - total_lacunas}/{len(records)} "
               f"({100*(len(records)-total_lacunas)//len(records)}%)\n")

    out.append("## Distribuição por regime\n")
    for reg, recs in sorted(by_regime.items(), key=lambda x: -len(x[1])):
        out.append(f"- **{reg}**: {len(recs)}")
    out.append("")

    out.append("## Distribuição por país\n")
    for c, recs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        lacunas = sum(1 for r in recs if not has_full_panofsky(r))
        out.append(f"- **{c}**: {len(recs)} ({lacunas} lacunas)")
    out.append("")

    # narrativa por país × regime
    for country in sorted(by_country.keys(), key=lambda c: -len(by_country[c])):
        recs = by_country[country]
        out.append(f"---\n\n# {country} ({len(recs)} registros)\n")
        
        country_by_regime = defaultdict(list)
        for r in recs:
            country_by_regime[extract_regime(r)].append(r)
        
        for reg in ["fundacional", "normativo", "militar", "contra-alegoria", "pendente"]:
            sub = country_by_regime.get(reg, [])
            if not sub:
                continue
            out.append(f"## {country} — {reg} ({len(sub)} registros)\n")
            sub_sorted = sorted(sub, key=lambda r: r.get("input", {}).get("date_hint", "0"))
            for rec in sub_sorted:
                out.append(make_paragraph(rec))
                out.append("")

    return "\n".join(out)


def _regime_intro_fr(regime: str, recs: list) -> str:
    """Gera parágrafo introdutório para cada seção do caso francês."""
    count = len(recs)
    dates = sorted(
        r.get("input", {}).get("date_hint", "s.d.") for r in recs
        if r.get("input", {}).get("date_hint", "s.d.") != "s.d."
    )
    span = f"{dates[0]}–{dates[-1]}" if len(dates) >= 2 else (dates[0] if dates else "s.d.")
    
    motifs_all = []
    for r in recs:
        motifs_all.extend(extract_motifs(r))
    from collections import Counter
    top_motifs = [m for m, _ in Counter(motifs_all).most_common(5) if m]
    motif_str = ", ".join(top_motifs[:4]) if top_motifs else "alegoria feminina"

    intros = {
        "fundacional": (
            f"O regime fundacional agrupa {count} registros franceses no período {span}, "
            f"concentrando motivos como {motif_str}. Esses objetos operam como dispositivos "
            f"de legitimação de uma nova ordem jurídico-política, inscrevendo a feminilidade de Estado "
            f"no instante mesmo em que a República se constitui — e antes que qualquer mulher real "
            f"pudesse participar dessa constituição. A simultaneidade entre proliferação iconográfica "
            f"e exclusão política é o paradoxo que a análise panofskiana deste corpus deve sustentar."
        ),
        "normativo": (
            f"O regime normativo reúne {count} registros ({span}) marcados pela estabilização "
            f"e codificação da alegoria feminina em suportes institucionais de longa duração: {motif_str}. "
            f"Se o regime fundacional é o momento de invenção, o normativo é o de sedimentação — "
            f"a alegoria torna-se rotina burocrática, circula em moedas, selos e paratextos legais "
            f"sem que sua presença requeira mais justificação. O reconhecimento sem reciprocidade "
            f"atingiu, aqui, sua forma mais silenciosa."
        ),
        "militar": (
            f"O regime militar concentra {count} registros franceses ({span}) em que a alegoria "
            f"feminina é instrumentalizada por lógicas de mobilização, defesa nacional e legitimação "
            f"de exceção. Os motivos predominantes — {motif_str} — revelam o endurecimento progressivo "
            f"descrito pela hipótese central da tese: a feminilidade de Estado não desaparece em "
            f"contextos de crise, mas se reorganiza, tornando-se veículo de discursos de sacrifício "
            f"e purificação simbólica que aprofundam, paradoxalmente, a exclusão das mulheres reais."
        ),
        "contra-alegoria": (
            f"O regime de contra-alegoria agrupa {count} registros ({span}) em que a personificação "
            f"feminina é submetida a inversão, sátira ou conflito ativo de imagens. Presentes em "
            f"suportes como {motif_str}, esses objetos são os únicos do corpus que tornam visível "
            f"o mecanismo iconocrático ao contestá-lo — o iconoclasmo como negativo fotográfico "
            f"da iconocracia. A análise deste segmento é central para a hipótese do iconoclasmo "
            f"tropical, testada em perspectiva comparada com o caso brasileiro."
        ),
        "pendente": (
            f"Os {count} registros pendentes de classificação ({span}) não serão incluídos na análise "
            f"quantitativa do Capítulo 3 antes do freeze. Listados aqui para rastreabilidade, "
            f"aguardam codificação iconológica completa conforme o protocolo Panofsky v2.2.0."
        ),
    }
    return intros.get(regime, f"Regime {regime}: {count} registros ({span}), motivos: {motif_str}.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Corpus Iconocracia → Narrativa argumentativa automática"
    )
    parser.add_argument("jsonl", help="Caminho para records.jsonl")
    parser.add_argument("--mode", choices=["cap3", "country", "regime", "full"],
                        default="cap3", help="Modo de geração")
    parser.add_argument("--filter", default=None,
                        help="Filtro para modos 'country' ou 'regime' (ex: France, FUNDACIONAL)")
    parser.add_argument("--out", default=None, help="Arquivo de saída (padrão: stdout)")
    parser.add_argument("--no-lacuna-markers", action="store_true",
                        help="Omite marcadores [LACUNA] no texto")
    args = parser.parse_args()

    records = []
    with open(args.jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    lacuna = not args.no_lacuna_markers

    if args.mode == "cap3":
        text = mode_cap3(records)
    elif args.mode == "country":
        filt = args.filter or "France"
        text = mode_country(records, filt)
    elif args.mode == "regime":
        filt = args.filter or "FUNDACIONAL"
        text = mode_regime(records, filt)
    elif args.mode == "full":
        text = mode_full(records)
    else:
        text = mode_cap3(records)

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Salvo em: {args.out}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
