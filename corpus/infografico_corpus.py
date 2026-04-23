#!/usr/bin/env python3
"""
Infografico do Corpus ICONOCRACIA
Gera visualizacao multi-painel com dados do corpus-data.json
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from collections import Counter, defaultdict
from pathlib import Path

# ── Paleta academica ────────────────────────────────────────────
COLORS = {
    "fundacional": "#C9963B",   # dourado
    "normativo": "#2B4C7E",     # azul-marinho
    "militar": "#8B1A1A",       # vermelho escuro
    "contra-alegoria": "#3A6B4C", # verde escuro
}
ACCENT = "#1B2838"        # quase-preto para textos
GRID_COLOR = "#E0E0E0"
BG_COLOR = "#FFFFFF"
BAR_BLUE = "#2B4C7E"
BAR_GRADIENT = ["#1B2838", "#2B4C7E", "#3D6098", "#5A82B4", "#7BA3CC",
                "#9DC0DD", "#B8D4E8", "#D0E4F0", "#E3EFF6", "#F0F6FA"]

# ── Normalizacao ────────────────────────────────────────────────
COUNTRY_MAP = {
    "France": "Franca", "Germany": "Alemanha",
    "United States": "EUA", "Estados Unidos": "EUA",
    "Franca": "Franca",
}

SUPPORT_MAP = {
    "Gravura/Estampe": "Gravura/Estampa",
    "Gravura": "Gravura/Estampa",
    "Estampa": "Gravura/Estampa",
    "gravura/litografia": "Gravura/Estampa",
    "Pintura/Desenho": "Pintura/Desenho",
    "Pintura": "Pintura/Desenho",
    "pintura": "Pintura/Desenho",
    "coin": "Moeda",
    "stamp": "Selo",
    "banknote": "Papel-moeda",
    "iluminura/manuscrito": "Outro",
    "?": "Outro",
}

INDICATOR_LABELS = [
    "Desincorporacao", "Rigidez\npostural", "Dessexualizacao",
    "Uniformizacao\nfacial", "Heraldicizacao", "Enquadramento\narquitetonico",
    "Apagamento\nnarrativo", "Monocromatizacao", "Serialidade",
    "Inscricao\nestatal",
]
INDICATOR_KEYS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]


def load_corpus():
    path = Path(__file__).parent / "corpus-data.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("items", [])


def normalize_country(item):
    c = item.get("country_pt") or item.get("country", "?")
    return COUNTRY_MAP.get(c, c)


def normalize_support(item):
    s = item.get("medium_norm", "Outro")
    return SUPPORT_MAP.get(s, s)


def get_regime(item):
    return item.get("regime", "?")


def main():
    items = load_corpus()
    n = len(items)

    # ── Dados ───────────────────────────────────────────────────
    countries = Counter(normalize_country(i) for i in items)
    supports = Counter(normalize_support(i) for i in items)
    regimes = Counter(get_regime(i) for i in items if get_regime(i) != "?")

    # Decadas por regime
    decade_regime = defaultdict(lambda: Counter())
    for item in items:
        y = item.get("year")
        r = get_regime(item)
        if y and r != "?":
            if y < 1800:
                decade_regime["<1800"][r] += 1
            else:
                decade_regime[f"{(y // 10) * 10}s"][r] += 1

    # ENDURECIMENTO por regime
    regime_scores = defaultdict(list)
    for item in items:
        r = get_regime(item)
        s = item.get("endurecimento_score")
        if r != "?" and s is not None:
            regime_scores[r].append(s)

    # Indicadores medios
    indicator_means = []
    for key in INDICATOR_KEYS:
        vals = [item["indicadores"][key] for item in items
                if item.get("indicadores") and key in item.get("indicadores", {})]
        indicator_means.append(np.mean(vals) if vals else 0)

    # ── Figura ──────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 24), facecolor=BG_COLOR, dpi=100)

    gs = gridspec.GridSpec(
        5, 2,
        height_ratios=[0.8, 3, 3.5, 3, 3.5],
        hspace=0.35, wspace=0.3,
        left=0.08, right=0.95, top=0.96, bottom=0.04,
    )

    # ── Header ──────────────────────────────────────────────────
    ax_header = fig.add_subplot(gs[0, :])
    ax_header.set_xlim(0, 1)
    ax_header.set_ylim(0, 1)
    ax_header.axis("off")

    ax_header.text(
        0.5, 0.72,
        "ICONOCRACIA",
        fontsize=38, fontweight="bold", color=ACCENT,
        ha="center", va="center", fontfamily="serif",
    )
    ax_header.text(
        0.5, 0.28,
        f"Corpus de Alegorias Femininas na Historia da Cultura Juridica",
        fontsize=16, color="#555555",
        ha="center", va="center", fontfamily="serif",
    )

    # KPI boxes
    kpis = [
        (f"{n}", "itens catalogados"),
        ("15", "paises"),
        ("1239-1975", "periodo"),
        ("1.42", "ENDURECIMENTO medio"),
    ]
    box_width = 0.18
    start_x = 0.5 - (len(kpis) * box_width + (len(kpis) - 1) * 0.03) / 2
    for idx, (val, label) in enumerate(kpis):
        x = start_x + idx * (box_width + 0.03)
        rect = FancyBboxPatch(
            (x, -0.35), box_width, 0.3,
            boxstyle="round,pad=0.02", facecolor="#F5F0E8",
            edgecolor=GRID_COLOR, linewidth=1,
            transform=ax_header.transAxes, clip_on=False,
        )
        ax_header.add_patch(rect)
        ax_header.text(
            x + box_width / 2, -0.12, val,
            fontsize=18, fontweight="bold", color=ACCENT,
            ha="center", va="center", transform=ax_header.transAxes,
        )
        ax_header.text(
            x + box_width / 2, -0.28, label,
            fontsize=9, color="#777777",
            ha="center", va="center", transform=ax_header.transAxes,
        )

    # ── A: Paises (barras horizontais) ──────────────────────────
    ax_a = fig.add_subplot(gs[1, 0])
    top_countries = countries.most_common(10)
    c_names = [c for c, _ in reversed(top_countries)]
    c_vals = [v for _, v in reversed(top_countries)]
    colors_a = BAR_GRADIENT[:len(c_names)][::-1]
    bars_a = ax_a.barh(c_names, c_vals, color=colors_a, edgecolor="white", height=0.7)
    for bar, val in zip(bars_a, c_vals):
        ax_a.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                  str(val), va="center", fontsize=11, fontweight="bold", color=ACCENT)
    ax_a.set_title("A. Distribuicao por pais", fontsize=14, fontweight="bold",
                    color=ACCENT, loc="left", pad=10)
    ax_a.set_xlim(0, max(c_vals) + 5)
    ax_a.spines[["top", "right", "bottom"]].set_visible(False)
    ax_a.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax_a.tick_params(axis="y", labelsize=11)
    ax_a.xaxis.grid(True, color=GRID_COLOR, linewidth=0.5)

    # ── B: Regimes (donut) ──────────────────────────────────────
    ax_b = fig.add_subplot(gs[1, 1])
    regime_order = ["fundacional", "normativo", "militar", "contra-alegoria"]
    r_vals = [regimes.get(r, 0) for r in regime_order]
    r_colors = [COLORS[r] for r in regime_order]
    total_regimes = sum(r_vals)
    r_labels = [f"{r.capitalize()}\n({v}, {v/total_regimes*100:.0f}%)"
                if total_regimes > 0 else f"{r.capitalize()}\n(0, 0%)"
                for r, v in zip(regime_order, r_vals)]

    wedges, texts = ax_b.pie(
        r_vals if total_regimes > 0 else [1], colors=r_colors if total_regimes > 0 else ["#D9D9D9"],
        startangle=90,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    )
    ax_b.text(0, 0, f"{total_regimes}", fontsize=28, fontweight="bold",
              color=ACCENT, ha="center", va="center")

    if total_regimes > 0:
        ax_b.legend(
            wedges, r_labels, loc="center left", bbox_to_anchor=(0.85, 0.5),
            fontsize=10, frameon=False,
        )
    ax_b.set_title("B. Regimes iconocraticos", fontsize=14, fontweight="bold",
                    color=ACCENT, loc="left", pad=10)

    # ── C: Timeline por decada ──────────────────────────────────
    ax_c = fig.add_subplot(gs[2, :])
    all_decades = sorted(decade_regime.keys(), key=lambda d: -1 if d == "<1800" else int(d[:-1]))
    bottom = np.zeros(len(all_decades))
    for regime in regime_order:
        vals = [decade_regime[d].get(regime, 0) for d in all_decades]
        ax_c.bar(range(len(all_decades)), vals, bottom=bottom,
                 color=COLORS[regime], label=regime.capitalize(),
                 edgecolor="white", linewidth=0.5, width=0.75)
        bottom += np.array(vals)

    ax_c.set_xticks(range(len(all_decades)))
    ax_c.set_xticklabels(all_decades, rotation=45, ha="right", fontsize=10)
    ax_c.set_ylabel("Itens", fontsize=12)
    ax_c.set_title("C. Distribuicao temporal por decada e regime", fontsize=14,
                    fontweight="bold", color=ACCENT, loc="left", pad=10)
    ax_c.spines[["top", "right"]].set_visible(False)
    ax_c.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    ax_c.legend(loc="upper left", fontsize=10, frameon=False, ncol=4)

    # Highlight 1910s
    idx_1910 = all_decades.index("1910s") if "1910s" in all_decades else None
    if idx_1910 is not None:
        total_1910 = sum(decade_regime["1910s"].values())
        ax_c.annotate(
            f"Pico: {total_1910} itens",
            xy=(idx_1910, total_1910), xytext=(idx_1910 + 1.5, total_1910 + 2),
            fontsize=11, fontweight="bold", color=COLORS["militar"],
            arrowprops=dict(arrowstyle="->", color=COLORS["militar"], lw=1.5),
        )

    # ── D: ENDURECIMENTO por regime ─────────────────────────────
    ax_d = fig.add_subplot(gs[3, 0])
    regime_display_order = ["contra-alegoria", "fundacional", "militar", "normativo"]
    d_means = [np.mean(regime_scores[r]) if regime_scores[r] else 0 for r in regime_display_order]
    d_stds = [np.std(regime_scores[r]) if regime_scores[r] else 0 for r in regime_display_order]
    d_colors = [COLORS[r] for r in regime_display_order]
    d_labels = [r.capitalize() for r in regime_display_order]

    bars_d = ax_d.bar(d_labels, d_means, color=d_colors, edgecolor="white",
                      width=0.6, yerr=d_stds, capsize=4,
                      error_kw=dict(lw=1.2, color="#666666"))
    for bar, mean in zip(bars_d, d_means):
        ax_d.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                  f"{mean:.2f}", ha="center", fontsize=12, fontweight="bold", color=ACCENT)

    ax_d.set_ylim(0, 3.2)
    ax_d.set_ylabel("Score medio (0-3)", fontsize=11)
    ax_d.set_title("D. ENDURECIMENTO por regime", fontsize=14, fontweight="bold",
                    color=ACCENT, loc="left", pad=10)
    ax_d.spines[["top", "right"]].set_visible(False)
    ax_d.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    ax_d.tick_params(axis="x", labelsize=10)

    # ── E: Suportes (barras horizontais) ────────────────────────
    ax_e = fig.add_subplot(gs[3, 1])
    top_supports = supports.most_common(8)
    s_names = [s for s, _ in reversed(top_supports)]
    s_vals = [v for _, v in reversed(top_supports)]
    bars_e = ax_e.barh(s_names, s_vals, color=BAR_BLUE, edgecolor="white",
                       height=0.65, alpha=0.85)
    for bar, val in zip(bars_e, s_vals):
        ax_e.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                  str(val), va="center", fontsize=11, fontweight="bold", color=ACCENT)
    ax_e.set_title("E. Distribuicao por suporte", fontsize=14, fontweight="bold",
                    color=ACCENT, loc="left", pad=10)
    ax_e.set_xlim(0, max(s_vals) + 6)
    ax_e.spines[["top", "right", "bottom"]].set_visible(False)
    ax_e.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax_e.tick_params(axis="y", labelsize=10)

    # ── F: Radar dos 10 indicadores ─────────────────────────────
    ax_f = fig.add_subplot(gs[4, :], polar=True)
    angles = np.linspace(0, 2 * np.pi, len(INDICATOR_KEYS), endpoint=False).tolist()
    values = indicator_means + [indicator_means[0]]
    angles += [angles[0]]

    ax_f.plot(angles, values, "o-", color=BAR_BLUE, linewidth=2, markersize=6)
    ax_f.fill(angles, values, alpha=0.15, color=BAR_BLUE)

    ax_f.set_xticks(angles[:-1])
    ax_f.set_xticklabels(INDICATOR_LABELS, fontsize=9)
    ax_f.set_ylim(0, 3)
    ax_f.set_yticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    ax_f.set_yticklabels(["0.5", "1.0", "1.5", "2.0", "2.5", "3.0"],
                          fontsize=8, color="#999999")
    ax_f.set_title("F. Media dos 10 indicadores de ENDURECIMENTO", fontsize=14,
                    fontweight="bold", color=ACCENT, loc="left", pad=20, x=-0.05)
    ax_f.spines["polar"].set_color(GRID_COLOR)
    ax_f.grid(color=GRID_COLOR, linewidth=0.5)

    # ── Salvar ──────────────────────────────────────────────────
    out_dir = Path(__file__).parent
    fig.savefig(out_dir / "infografico_corpus.png", dpi=300, bbox_inches="tight",
                facecolor=BG_COLOR, pad_inches=0.5)
    fig.savefig(out_dir / "infografico_corpus.pdf", bbox_inches="tight",
                facecolor=BG_COLOR, pad_inches=0.5)
    plt.close(fig)
    print(f"Infografico salvo em:")
    print(f"  PNG: {out_dir / 'infografico_corpus.png'}")
    print(f"  PDF: {out_dir / 'infografico_corpus.pdf'}")


if __name__ == "__main__":
    main()
