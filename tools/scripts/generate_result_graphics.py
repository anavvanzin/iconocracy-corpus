#!/usr/bin/env python3
"""Generate current result graphics for the Iconocracy corpus.

The script intentionally uses only the Python standard library so the figures
remain reproducible in the project environment even when plotting libraries are
not installed.
"""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from html import escape
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
PURIFICATION_PATH = REPO / "data" / "processed" / "purification.jsonl"
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
OUT_DIR = REPO / "data" / "processed" / "result_graphics"

INDICATORS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]

INDICATOR_LABELS = {
    "desincorporacao": "Desincorporacao",
    "rigidez_postural": "Rigidez postural",
    "dessexualizacao": "Dessexualizacao",
    "uniformizacao_facial": "Uniformizacao facial",
    "heraldizacao": "Heraldizacao",
    "enquadramento_arquitetonico": "Enquadramento arq.",
    "apagamento_narrativo": "Apagamento narrativo",
    "monocromatizacao": "Monocromatizacao",
    "serialidade": "Serialidade",
    "inscricao_estatal": "Inscricao estatal",
}

REGIME_ORDER = ["fundacional", "normativo", "militar", "contra-alegoria"]

REGIME_COLORS = {
    "fundacional": "#2f6f9f",
    "normativo": "#2a8a62",
    "militar": "#b6453d",
    "contra-alegoria": "#7a4ea3",
}

NEUTRAL = "#343a40"
GRID = "#d9dee6"
TEXT_MUTED = "#68707d"
BACKGROUND = "#ffffff"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_rows() -> list[dict]:
    purification = load_jsonl(PURIFICATION_PATH)
    corpus = {row["id"]: row for row in json.loads(CORPUS_PATH.read_text(encoding="utf-8"))}
    rows = []
    for row in purification:
        meta = corpus.get(row["id"], {})
        merged = dict(row)
        merged["country"] = meta.get("country") or "Sem pais"
        merged["support"] = meta.get("support") or "Sem suporte"
        merged["title"] = meta.get("title") or row["id"]
        rows.append(merged)
    return rows


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def group_scores(rows: list[dict], key: str) -> dict[str, list[float]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        value = row.get("purificacao_composto")
        if isinstance(value, (int, float)):
            grouped[str(row.get(key) or "Sem valor")].append(float(value))
    return grouped


def regime_keys(grouped: dict[str, list[float]]) -> list[str]:
    known = [regime for regime in REGIME_ORDER if regime in grouped]
    extra = sorted(regime for regime in grouped if regime not in REGIME_ORDER)
    return known + extra


def svg_wrap(width: int, height: int, body: str) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img">',
            f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
            body,
            "</svg>",
            "",
        ]
    )


def text(
    x: float,
    y: float,
    value: str,
    size: int = 14,
    weight: int | str = 400,
    fill: str = NEUTRAL,
    anchor: str = "start",
    rotate: float | None = None,
) -> str:
    transform = f' transform="rotate({rotate:.0f} {x:.1f} {y:.1f})"' if rotate is not None else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
        f'{transform}>{escape(value)}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 1) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"/>'


def rect(x: float, y: float, width: float, height: float, fill: str, stroke: str | None = None) -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(width, 0):.1f}" height="{max(height, 0):.1f}" '
        f'fill="{fill}"{stroke_attr}/>'
    )


def circle(x: float, y: float, r: float, fill: str, stroke: str = "none") -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}"/>'


def title_block(title: str, subtitle: str, width: int) -> list[str]:
    return [
        text(48, 46, title, size=24, weight=700),
        text(48, 72, subtitle, size=13, fill=TEXT_MUTED),
        line(48, 92, width - 48, 92, color="#edf0f4"),
    ]


def y_scale(value: float, top: float, bottom: float, domain_max: float) -> float:
    return bottom - (value / domain_max) * (bottom - top)


def fmt(value: float) -> str:
    return f"{value:.2f}"


def interpolate_color(low: str, high: str, t: float) -> str:
    t = max(0.0, min(1.0, t))
    low_rgb = tuple(int(low[i : i + 2], 16) for i in (1, 3, 5))
    high_rgb = tuple(int(high[i : i + 2], 16) for i in (1, 3, 5))
    rgb = tuple(round(a + (b - a) * t) for a, b in zip(low_rgb, high_rgb))
    return "#" + "".join(f"{channel:02x}" for channel in rgb)


def figure_regime_means(rows: list[dict]) -> tuple[str, str]:
    grouped = group_scores(rows, "regime_iconocratico")
    keys = regime_keys(grouped)
    width, height = 980, 620
    left, right, top, bottom = 96, 48, 130, 500
    plot_width = width - left - right
    bar_gap = 42
    bar_width = (plot_width - bar_gap * (len(keys) - 1)) / len(keys)

    parts = title_block(
        "Endurecimento medio por regime iconocratico",
        f"Fonte: purification.jsonl + corpus-data.json | N={len(rows)} | escala 0-3",
        width,
    )
    for tick in [0, 0.75, 1.5, 2.25, 3.0]:
        y = y_scale(tick, top, bottom, 3)
        parts.append(line(left, y, width - right, y))
        parts.append(text(left - 14, y + 5, f"{tick:.2g}", size=12, fill=TEXT_MUTED, anchor="end"))
    parts.append(text(34, (top + bottom) / 2, "Score medio", size=13, fill=TEXT_MUTED, anchor="middle", rotate=-90))

    for index, key in enumerate(keys):
        scores = grouped[key]
        value = mean(scores)
        x = left + index * (bar_width + bar_gap)
        y = y_scale(value, top, bottom, 3)
        color = REGIME_COLORS.get(key, "#5a6675")
        parts.append(rect(x, y, bar_width, bottom - y, color))
        parts.append(text(x + bar_width / 2, y - 12, fmt(value), size=18, weight=700, anchor="middle"))
        parts.append(text(x + bar_width / 2, bottom + 26, key, size=13, weight=600, anchor="middle"))
        parts.append(text(x + bar_width / 2, bottom + 48, f"n={len(scores)}", size=12, fill=TEXT_MUTED, anchor="middle"))
        min_y = y_scale(min(scores), top, bottom, 3)
        max_y = y_scale(max(scores), top, bottom, 3)
        mid_x = x + bar_width / 2
        parts.append(line(mid_x, max_y, mid_x, min_y, color="#23272f", width=1.5))
        parts.append(circle(mid_x, max_y, 4, "#23272f"))
        parts.append(circle(mid_x, min_y, 4, "#23272f"))

    parts.append(text(left, height - 44, "Barras = media; linha vertical = intervalo minimo-maximo dentro do regime.", size=12, fill=TEXT_MUTED))
    filename = "fig_01_endurecimento_por_regime.svg"
    return filename, svg_wrap(width, height, "\n".join(parts))


def figure_histogram(rows: list[dict]) -> tuple[str, str]:
    scores = [float(row["purificacao_composto"]) for row in rows if isinstance(row.get("purificacao_composto"), (int, float))]
    bins = [i * 0.25 for i in range(13)]
    counts = [0] * 12
    for score in scores:
        index = min(11, max(0, int(math.floor(score / 0.25))))
        counts[index] += 1

    width, height = 980, 600
    left, right, top, bottom = 92, 48, 130, 500
    plot_width = width - left - right
    bar_width = plot_width / len(counts)
    max_count = max(counts) if counts else 1
    parts = title_block(
        "Distribuicao do score composto de endurecimento",
        f"Media={fmt(mean(scores))} | mediana={fmt(median(scores))} | N={len(scores)}",
        width,
    )
    for tick in range(0, max_count + 1, max(1, math.ceil(max_count / 5))):
        y = bottom - (tick / max_count) * (bottom - top)
        parts.append(line(left, y, width - right, y))
        parts.append(text(left - 12, y + 5, str(tick), size=12, fill=TEXT_MUTED, anchor="end"))
    for index, count in enumerate(counts):
        x = left + index * bar_width + 3
        y = bottom - (count / max_count) * (bottom - top)
        fill = interpolate_color("#cfe2f3", "#2f6f9f", count / max_count)
        parts.append(rect(x, y, bar_width - 6, bottom - y, fill))
        if count:
            parts.append(text(x + (bar_width - 6) / 2, y - 7, str(count), size=11, fill=NEUTRAL, anchor="middle"))
    for tick in [0, 0.75, 1.5, 2.25, 3.0]:
        x = left + (tick / 3) * plot_width
        parts.append(line(x, bottom, x, bottom + 7, color=NEUTRAL))
        parts.append(text(x, bottom + 28, f"{tick:.2g}", size=12, fill=TEXT_MUTED, anchor="middle"))
    mean_x = left + (mean(scores) / 3) * plot_width
    parts.append(line(mean_x, top, mean_x, bottom, color="#b6453d", width=2))
    parts.append(text(mean_x + 8, top + 20, f"media {fmt(mean(scores))}", size=12, weight=700, fill="#b6453d"))
    parts.append(text(width / 2, height - 42, "Score composto (0-3)", size=13, fill=TEXT_MUTED, anchor="middle"))
    parts.append(text(34, (top + bottom) / 2, "Frequencia", size=13, fill=TEXT_MUTED, anchor="middle", rotate=-90))
    filename = "fig_02_distribuicao_endurecimento.svg"
    return filename, svg_wrap(width, height, "\n".join(parts))


def figure_heatmap(rows: list[dict]) -> tuple[str, str]:
    width, height = 1180, 560
    left, top = 168, 146
    cell_w, cell_h = 92, 58
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("regime_iconocratico") or "Sem regime")].append(row)
    keys = regime_keys({key: [1] for key in grouped})

    parts = title_block(
        "Media dos 10 indicadores por regime",
        "Cada celula mostra a media ordinal 0-3; tons mais escuros indicam maior endurecimento.",
        width,
    )
    for col, indicator in enumerate(INDICATORS):
        x = left + col * cell_w + cell_w / 2
        parts.append(text(x, top - 18, INDICATOR_LABELS[indicator], size=11, fill=TEXT_MUTED, anchor="end", rotate=-45))
    for row_index, key in enumerate(keys):
        y = top + row_index * cell_h
        parts.append(text(left - 18, y + cell_h / 2 + 5, f"{key} (n={len(grouped[key])})", size=13, weight=600, anchor="end"))
        for col, indicator in enumerate(INDICATORS):
            values = [float(item[indicator]) for item in grouped[key] if isinstance(item.get(indicator), (int, float))]
            value = mean(values)
            color = interpolate_color("#f4f1e7", "#9e2f35", value / 3)
            x = left + col * cell_w
            parts.append(rect(x, y, cell_w - 2, cell_h - 2, color, stroke="#ffffff"))
            parts.append(text(x + cell_w / 2, y + cell_h / 2 + 5, fmt(value), size=13, weight=700, fill="#222222", anchor="middle"))
    parts.append(text(left, height - 46, "Leitura: comparar linhas para perfis de regime; comparar colunas para indicadores mais sensiveis.", size=12, fill=TEXT_MUTED))
    filename = "fig_03_heatmap_indicadores_por_regime.svg"
    return filename, svg_wrap(width, height, "\n".join(parts))


def figure_horizontal_means(
    rows: list[dict],
    key: str,
    title: str,
    subtitle: str,
    filename: str,
    min_n: int = 1,
    limit: int = 14,
) -> tuple[str, str]:
    grouped = group_scores(rows, key)
    items = [
        (name, scores, mean(scores))
        for name, scores in grouped.items()
        if len(scores) >= min_n
    ]
    items.sort(key=lambda item: (item[2], len(item[1]), item[0]), reverse=True)
    items = items[:limit]

    width = 1080
    height = 160 + len(items) * 42 + 70
    left, right, top = 250, 70, 132
    plot_width = width - left - right
    bar_h = 24
    row_h = 42
    parts = title_block(title, subtitle, width)
    for tick in [0, 0.75, 1.5, 2.25, 3.0]:
        x = left + (tick / 3) * plot_width
        parts.append(line(x, top - 12, x, top + row_h * len(items) - 12))
        parts.append(text(x, top + row_h * len(items) + 20, f"{tick:.2g}", size=12, fill=TEXT_MUTED, anchor="middle"))
    for index, (name, scores, value) in enumerate(items):
        y = top + index * row_h
        bar_width = (value / 3) * plot_width
        color = interpolate_color("#d7eadc", "#2a8a62", value / 3)
        parts.append(text(left - 16, y + 18, name, size=13, weight=600, anchor="end"))
        parts.append(rect(left, y, bar_width, bar_h, color))
        parts.append(text(left + bar_width + 10, y + 17, f"{fmt(value)}  n={len(scores)}", size=12, fill=NEUTRAL))
    parts.append(text(left + plot_width / 2, height - 38, "Media do score composto (0-3)", size=13, fill=TEXT_MUTED, anchor="middle"))
    return filename, svg_wrap(width, height, "\n".join(parts))


def figure_regime_counts(rows: list[dict]) -> tuple[str, str]:
    counts = Counter(str(row.get("regime_iconocratico") or "Sem regime") for row in rows)
    keys = regime_keys({key: [1] for key in counts})
    total = sum(counts.values())
    width, height = 980, 560
    left, right, top, bottom = 96, 48, 128, 454
    plot_width = width - left - right
    max_count = max(counts.values()) if counts else 1
    bar_gap = 42
    bar_width = (plot_width - bar_gap * (len(keys) - 1)) / len(keys)
    parts = title_block(
        "Composicao do corpus por regime iconocratico",
        f"Contagem de itens codificados no ledger atual | total={total}",
        width,
    )
    for tick in range(0, max_count + 1, max(1, math.ceil(max_count / 5))):
        y = bottom - (tick / max_count) * (bottom - top)
        parts.append(line(left, y, width - right, y))
        parts.append(text(left - 12, y + 5, str(tick), size=12, fill=TEXT_MUTED, anchor="end"))
    for index, key in enumerate(keys):
        count = counts[key]
        x = left + index * (bar_width + bar_gap)
        y = bottom - (count / max_count) * (bottom - top)
        color = REGIME_COLORS.get(key, "#5a6675")
        parts.append(rect(x, y, bar_width, bottom - y, color))
        parts.append(text(x + bar_width / 2, y - 11, f"{count}", size=18, weight=700, anchor="middle"))
        parts.append(text(x + bar_width / 2, y - 32, f"{count / total:.1%}", size=12, fill=TEXT_MUTED, anchor="middle"))
        parts.append(text(x + bar_width / 2, bottom + 28, key, size=13, weight=600, anchor="middle"))
    parts.append(text(34, (top + bottom) / 2, "Itens", size=13, fill=TEXT_MUTED, anchor="middle", rotate=-90))
    filename = "fig_06_composicao_por_regime.svg"
    return filename, svg_wrap(width, height, "\n".join(parts))


def figure_indicator_ranking(rows: list[dict]) -> tuple[str, str]:
    items = []
    for indicator in INDICATORS:
        values = [float(row[indicator]) for row in rows if isinstance(row.get(indicator), (int, float))]
        items.append((INDICATOR_LABELS[indicator], values, mean(values)))
    items.sort(key=lambda item: item[2], reverse=True)

    width, height = 1080, 640
    left, right, top = 260, 68, 132
    plot_width = width - left - right
    row_h, bar_h = 42, 24
    parts = title_block(
        "Indicadores com maior media no corpus",
        "Ranking dos 10 componentes ordinais do protocolo de endurecimento.",
        width,
    )
    for tick in [0, 0.75, 1.5, 2.25, 3.0]:
        x = left + (tick / 3) * plot_width
        parts.append(line(x, top - 12, x, top + row_h * len(items) - 12))
        parts.append(text(x, top + row_h * len(items) + 20, f"{tick:.2g}", size=12, fill=TEXT_MUTED, anchor="middle"))
    for index, (name, values, value) in enumerate(items):
        y = top + index * row_h
        bar_width = (value / 3) * plot_width
        color = interpolate_color("#f1d6ce", "#b6453d", value / 3)
        parts.append(text(left - 16, y + 18, name, size=13, weight=600, anchor="end"))
        parts.append(rect(left, y, bar_width, bar_h, color))
        parts.append(text(left + bar_width + 10, y + 17, fmt(value), size=12, fill=NEUTRAL))
    parts.append(text(left + plot_width / 2, height - 42, "Media ordinal (0-3)", size=13, fill=TEXT_MUTED, anchor="middle"))
    filename = "fig_07_ranking_indicadores.svg"
    return filename, svg_wrap(width, height, "\n".join(parts))


def summary_markdown(rows: list[dict], filenames: list[str]) -> str:
    scores = [float(row["purificacao_composto"]) for row in rows if isinstance(row.get("purificacao_composto"), (int, float))]
    regimes = group_scores(rows, "regime_iconocratico")
    countries = group_scores(rows, "country")
    supports = group_scores(rows, "support")
    top_regime_lines = [
        f"- {key}: n={len(regimes[key])}, media={fmt(mean(regimes[key]))}"
        for key in regime_keys(regimes)
    ]
    top_country_lines = [
        f"- {name}: n={len(values)}, media={fmt(mean(values))}"
        for name, values in sorted(countries.items(), key=lambda item: len(item[1]), reverse=True)[:8]
    ]
    top_support_lines = [
        f"- {name}: n={len(values)}, media={fmt(mean(values))}"
        for name, values in sorted(supports.items(), key=lambda item: len(item[1]), reverse=True)[:8]
    ]
    figure_lines = [f"- [`{name}`]({name})" for name in filenames]
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    return "\n".join(
        [
            "# Result graphics - Iconocracy corpus",
            "",
            f"Generated at: `{generated_at}`",
            "",
            "Sources:",
            "",
            f"- `{PURIFICATION_PATH.relative_to(REPO)}`",
            f"- `{CORPUS_PATH.relative_to(REPO)}`",
            "",
            "Snapshot:",
            "",
            f"- Rows visualized: **{len(rows)}**",
            f"- Composite score: min={fmt(min(scores))}, max={fmt(max(scores))}, mean={fmt(mean(scores))}, median={fmt(median(scores))}",
            "",
            "By regime:",
            "",
            *top_regime_lines,
            "",
            "Most represented countries:",
            "",
            *top_country_lines,
            "",
            "Most represented supports:",
            "",
            *top_support_lines,
            "",
            "Figures:",
            "",
            *figure_lines,
            "",
            "Caveat:",
            "",
            "- These graphics visualize the current canonical coding ledger.",
            "- They do not replace image-store validation or inter-rater reliability review.",
            "- See `docs/decisions/IRR-PILOTO-2026-05-30.md` for the current validity warning.",
            "",
        ]
    )


def main() -> None:
    rows = load_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    figures = [
        figure_regime_means(rows),
        figure_histogram(rows),
        figure_heatmap(rows),
        figure_horizontal_means(
            rows,
            key="country",
            title="Paises com maior media de endurecimento",
            subtitle="Inclui apenas paises com n>=3; ordenado por media do score composto.",
            filename="fig_04_paises_media_endurecimento.svg",
            min_n=3,
            limit=14,
        ),
        figure_horizontal_means(
            rows,
            key="support",
            title="Suportes com maior media de endurecimento",
            subtitle="Todos os suportes do ledger atual; ordenado por media do score composto.",
            filename="fig_05_suportes_media_endurecimento.svg",
            min_n=1,
            limit=14,
        ),
        figure_regime_counts(rows),
        figure_indicator_ranking(rows),
    ]
    filenames = []
    for filename, content in figures:
        (OUT_DIR / filename).write_text(content, encoding="utf-8")
        filenames.append(filename)
    (OUT_DIR / "README.md").write_text(summary_markdown(rows, filenames), encoding="utf-8")
    print(f"Wrote {len(filenames)} SVG figures and README.md to {OUT_DIR.relative_to(REPO)}")


if __name__ == "__main__":
    main()
