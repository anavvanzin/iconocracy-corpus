/* Gráficos assinatura · timeline de parede (P3) + fluxo de destino da genealogia (P2)
   Paleta alinhada aos tokens Mnemosyne Viva (css/style.css). */
(() => {
  const { clamp, showDrill } = window.U;
  const NS = "http://www.w3.org/2000/svg";
  const INK = "#1A1612", INKM = "#625A50", INKL = "#6B6157";
  const BLUE = "#1D2548", NEG = "#A8281F", GOLD = "#B8924A", TERRA = "#A04030";
  const LINELO = "rgba(26,22,18,.10)";
  const SERIF = '"Crimson Pro", Georgia, serif';
  const MONO = '"JetBrains Mono", ui-monospace, monospace';
  const VCOL = { era: INK, attr: INKM, neg: NEG, vft: GOLD, ripa: BLUE, br: TERRA };
  const SRC = id => (window.SOURCES.find(s => s.id === id) || {}).label || id;

  const el = (tag, attrs, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };

  // ───────────── P3 · LINHA DO TEMPO DA ALEGORIA ─────────────
  function wallchart(host) {
    const data = window.RPT.timeline;
    const W = 924;
    const years = data.map(d => d.sort);
    const min = Math.min(...years), max = Math.max(...years);
    const X = y => 46 + ((y - min) / (max - min)) * (W - 90);
    const plaques = data.map(d => {
      const w = Math.max(92, d.t.length * 5.6 + 30);
      return { d, x: X(d.sort), w, layer: 0 };
    });
    const placed = [];
    plaques.forEach(p => {
      let l = 0;
      for (;;) {
        const clash = placed.some(q => q.layer === l && Math.abs(q.x - p.x) < (q.w + p.w) / 2 + 8);
        if (!clash) break; l++;
      }
      p.layer = l; placed.push(p);
    });
    const maxLayer = Math.max(...plaques.map(p => p.layer));
    const H = 116 + (maxLayer + 1) * 52;
    const axisY = H - 56;

    const body = window.U.frame(host, {
      title: "Quatro milênios da alegoria — a venda é o acidente mais recente",
      sub: "CADA PLACA É UM MARCO VERIFICADO · LACRE = NASCE COMO SÁTIRA · NAVY = RIPA · TERRACOTA = BRASIL · CLIQUE PARA A FONTE",
      src: "Registro K1–K33 · compilação própria (2026)"
    });
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", role: "img" }, body);

    const eras = [
      [-2600, 500, "ANTIGUIDADE", .05], [500, 1450, "MEDIEVO", .03],
      [1450, 1600, "A MUTAÇÃO", .10], [1600, 1820, "CODIFICAÇÃO", .05], [1820, 2026, "SOBREVIVÊNCIAS", .03]
    ];
    eras.forEach(([a, b, lab, al]) => {
      el("rect", { x: X(a), y: axisY - 10, width: X(b) - X(a), height: 20, fill: INK, opacity: al }, svg);
      const t = el("text", { x: (X(a) + X(b)) / 2, y: axisY + 32, "text-anchor": "middle",
        "font-family": MONO, "font-size": 8.5, fill: INKL, "letter-spacing": ".12em" }, svg);
      t.textContent = lab;
    });
    el("line", { x1: 30, y1: axisY, x2: W - 30, y2: axisY, stroke: INK, "stroke-width": 1.6 }, svg);
    el("line", { x1: 30, y1: axisY + 5, x2: W - 30, y2: axisY + 5, stroke: INK, "stroke-width": .8 }, svg);
    [[-2600, "2600 a.C."], [0, "1 d.C."], [500, "500"], [1000, "1000"], [1500, "1500"], [2000, "2000"]]
      .forEach(([y, lab]) => {
        el("line", { x1: X(y), y1: axisY - 3, x2: X(y), y2: axisY + 8, stroke: INK, "stroke-width": 1 }, svg);
        const t = el("text", { x: X(y), y: axisY + 20, "text-anchor": "middle", "font-family": MONO, "font-size": 9, fill: INKM }, svg);
        t.textContent = lab;
      });

    const stems = el("g", {}, svg), plaq = el("g", {}, svg);
    plaques.forEach((p, i) => {
      const py = axisY - 26 - p.layer * 52;
      const col = VCOL[p.d.v];
      el("line", { x1: p.x, y1: axisY - 4, x2: p.x, y2: py + 15, stroke: col, "stroke-width": .9, opacity: .8 }, stems);
      el("circle", { cx: p.x, cy: axisY - 4, r: 2.6, fill: col }, stems);
      const g = el("g", { cursor: "pointer", opacity: 0 }, plaq);
      g.style.transition = `opacity .5s ${i * 60}ms`;
      const bx = clamp(p.x - p.w / 2, 6, W - p.w - 6);
      el("rect", { x: bx, y: py - 22, width: p.w, height: 38, fill: "#F8F5EE",
        stroke: col, "stroke-width": p.d.v === "neg" ? 1.6 : 1.1, rx: 1.5 }, g);
      const ty = el("text", { x: bx + 8, y: py - 9, "font-family": MONO, "font-size": 8.2, fill: col, "letter-spacing": ".06em" }, g);
      ty.textContent = p.d.y.toString().toUpperCase();
      const tt = el("text", { x: bx + 8, y: py + 5, "font-family": SERIF, "font-weight": 700, "font-size": 10.6, fill: INK }, g);
      let label = p.d.t;
      if (label.length * 6.1 > p.w - 14) label = label.slice(0, Math.floor((p.w - 14) / 6.1)) + "…";
      tt.textContent = label;
      g.addEventListener("click", e => {
        const kids = p.d.k.split(" ").map(k => SRC(k)).join(" · ");
        showDrill({ title: `${p.d.y} — ${p.d.t}`, value: "", sub: p.d.d, source: kids, x: e.clientX, y: e.clientY });
      });
      g.dataset.drillKeep = "1";
      requestAnimationFrame(() => requestAnimationFrame(() => g.style.opacity = 1));
    });
  }

  // ───────────── P2 · GENEALOGIA: fluxo de destino ─────────────
  function destiny(host) {
    const ents = window.RPT.genealogy, outs = window.RPT.outcomes;
    const W = 924, H = 470;
    const min = -2700, max = 2050;
    const X = y => 168 + ((y - min) / (max - min)) * (W - 460);
    const body = window.U.frame(host, {
      title: "De Maat à praça dos Três Poderes — para onde flui cada personificação",
      sub: "LINHAS DE VIDA DAS FIGURAS · AS FAIXAS CURVAM-SE PARA O REGIME QUE AS HERDA · CLIQUE NUMA FIGURA PARA O DETALHE",
      src: "Fitzwilliam Museum · Gallagher Law Library · Eszenyi · Judaism and Rome · TJAM/ESMAM"
    });
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%" }, body);
    [-2600, -2000, -1000, 0, 1000, 2000].forEach(y => {
      el("line", { x1: X(y), y1: 26, x2: X(y), y2: H - 30, stroke: LINELO, "stroke-width": 1 }, svg);
      const t = el("text", { x: X(y), y: 18, "text-anchor": "middle", "font-family": MONO, "font-size": 8.5, fill: INKL }, svg);
      t.textContent = y <= 0 ? (y === 0 ? "1" : `${-y} a.C.`) : `${y}`;
    });
    const rowH = (H - 110) / ents.length;
    ents.forEach((en, i) => {
      const y = 52 + i * rowH + rowH / 2;
      const modern = en.out === "moderna";
      const col = modern ? BLUE : INK;
      const nm = el("text", { x: 10, y: y + 3.5, "font-family": SERIF, "font-size": 12.5, "font-weight": modern ? 700 : 400, fill: col }, svg);
      nm.textContent = en.name;
      const nt = el("text", { x: 10, y: y + 16, "font-family": MONO, "font-size": 7.8, fill: INKL }, svg);
      nt.textContent = en.note.toUpperCase();
      const x1 = X(en.from), x2 = X(en.to);
      const line = el("line", { x1, y1: y, x2: x1, y2: y, stroke: col, "stroke-width": 6.5, "stroke-linecap": "round", opacity: .85 }, svg);
      line.style.transition = `x2 .9s ${i * 90}ms cubic-bezier(.2,.7,.2,1)`;
      requestAnimationFrame(() => requestAnimationFrame(() => line.setAttribute("x2", x2)));
      const g = el("g", { cursor: "pointer" }, svg);
      el("rect", { x: 0, y: y - rowH / 2, width: X(max) + 40, height: rowH, fill: "transparent" }, g);
      g.addEventListener("click", e => showDrill({
        title: en.name, value: `${en.from < 0 ? -en.from + " a.C." : en.from} → ${en.to < 0 ? -en.to + " a.C." : en.to}`,
        sub: en.note, source: "Registro K1–K33", x: e.clientX, y: e.clientY
      }));
      g.dataset.drillKeep = "1";
      const oi = outs.findIndex(o => o.id === en.out);
      const oy = 74 + oi * ((H - 160) / outs.length) + 26;
      const sx = x2, txp = W - 190;
      const path = el("path", {
        d: `M ${sx} ${y} C ${sx + 60} ${y}, ${txp - 70} ${oy}, ${txp} ${oy}`,
        fill: "none", stroke: col, "stroke-width": 2.2, opacity: .35
      }, svg);
      const len = path.getTotalLength();
      path.style.strokeDasharray = len; path.style.strokeDashoffset = len;
      path.style.transition = `stroke-dashoffset 1s ${.3 + i * .1}s ease`;
      requestAnimationFrame(() => requestAnimationFrame(() => path.style.strokeDashoffset = 0));
    });
    outs.forEach((o, i) => {
      const oy = 74 + i * ((H - 160) / outs.length) + 26;
      const modern = o.id === "moderna";
      const g = el("g", {}, svg);
      el("rect", { x: W - 186, y: oy - 20, width: 178, height: 40, fill: modern ? BLUE : "#F8F5EE",
        stroke: modern ? BLUE : INK, "stroke-width": 1.2, rx: 2 }, g);
      const a = el("text", { x: W - 176, y: oy - 4, "font-family": MONO, "font-size": 9, "font-weight": 700,
        "letter-spacing": ".08em", fill: modern ? "#EFE5CF" : INK }, g);
      a.textContent = o.label;
      const b = el("text", { x: W - 176, y: oy + 10, "font-family": MONO, "font-size": 8,
        fill: modern ? "#c9d2f0" : INKM }, g);
      b.textContent = o.sub;
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const h1 = document.getElementById("timeline-chart");
    if (h1) wallchart(h1);
    const h2 = document.getElementById("genealogy-chart");
    if (h2) destiny(h2);
  });
})();
