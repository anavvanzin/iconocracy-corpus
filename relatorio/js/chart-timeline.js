// P3 · Linha do tempo mural — 405–1896, três camadas genealógicas
(() => {
  const host = document.getElementById("timeline-chart");
  if (!host) return;
  const P = U.PAL;
  const body = U.frame(host, {
    title: "A estrutura já estava completa em 1338 — o Estado moderno só a herdou",
    sub: "VINTE MARCOS · CORES POR FAMÍLIA ALEGÓRICA · PLACAS ACIMA E ABAIXO DO EIXO · CLIQUE NAS PLACAS PARA A BASE",
    src: "Dossiê §4–§7, com âncoras K6–K25 · compilação 2026-09-26",
  });

  const FAM = {
    virtudes:    { c: P.ink,     lbl: "Virtudes",              sh: "Virtudes" },
    continentes: { c: P.gold,    lbl: "Continentes",           sh: "Continentes" },
    oceanos:     { c: P.navy,    lbl: "Oceanos e rios",        sh: "Oceanos" },
    iconocracia: { c: P.lacre,   lbl: "Iconocracia nacional",  sh: "Iconocracia" },
    contracaso:  { c: P.contra,  lbl: "Contracaso",            sh: "Contracaso" },
  };
  const evs = RPT.timeline.slice().sort((a, b) => a.y - b.y);
  const W = 880, mL = 46, mR = 34;
  const X = y => mL + (y - 380) / (1910 - 380) * (W - mL - mR);

  // medição real de texto (canvas) — a estimativa por caractere deixava
  // o título transbordar da placa e colidir com a vizinha no cluster denso
  const mctx = document.createElement("canvas").getContext("2d");
  const monoFont = `700 7.5px ${U.MONO}`;
  const serifFont = `700 11px ${U.SERIF}`;
  const measure = (str, font, ls = 0) => {
    mctx.font = font;
    return mctx.measureText(str).width + ls * Math.max(0, str.length - 1);
  };
  const fitTitle = (str, maxW) => {
    if (measure(str, serifFont) <= maxW) return str;
    let lo = 8, hi = str.length;
    while (lo < hi) {
      const mid = (lo + hi + 1) >> 1;
      if (measure(str.slice(0, mid).replace(/[,;\s]+$/, "") + "…", serifFont) <= maxW) lo = mid;
      else hi = mid - 1;
    }
    return str.slice(0, lo).replace(/[,;\s]+$/, "") + "…";
  };

  // camadas gananciosas nos DOIS lados do eixo: para cada marco, escolhe o
  // lado onde a placa sobe menos — o cluster 1753–1896 se reparte e o eixo
  // respira; as extremidades deixam de empilhar numa única coluna
  const layerH = 52, plaqueH = 40, gap = 10;
  const lanesUp = [], lanesDn = [];
  const fits = (lanes, L, x, wpx) => !lanes[L].some(p => Math.abs(p.x - x) < (p.w + wpx) / 2 + gap);
  const needLane = (lanes, x, wpx) => {
    let L = 0;
    for (;;) { lanes[L] = lanes[L] || []; if (fits(lanes, L, x, wpx)) return L; L++; }
  };
  const placed = evs.map(e => {
    const head = e.y + " · " + FAM[e.fam].sh.toUpperCase();
    const wHead = measure(head, monoFont, 1);
    const wFull = measure(e.t, serifFont);
    const wpx = U.clamp(Math.max(wHead, Math.min(wFull, 150)) + 16, 84, 166);
    const title = fitTitle(e.t, wpx - 12);
    const x = U.clamp(X(e.y), mL + 4 + wpx / 2, W - 8 - wpx / 2);
    const La = needLane(lanesUp, x, wpx), Lb = needLane(lanesDn, x, wpx);
    const up = La <= Lb;
    const L = up ? La : Lb;
    (up ? lanesUp : lanesDn)[L].push({ x, w: wpx });
    return { ...e, x, w: wpx, L, up, title };
  });
  const nUp = lanesUp.length, nDn = lanesDn.length;
  const axisY0 = nUp * layerH + 108;
  const H = axisY0 + nDn * layerH + 92;
  const topY = axisY0 - nUp * layerH - 30;
  const botY = axisY0 + nDn * layerH + 26;

  const svg = U.svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", role: "img",
    "aria-label": "Linha do tempo de 405 a 1896 com vinte marcos da gramática alegórica" }, body);
  svg.style.display = "block"; svg.style.height = "auto";

  // faixas de era (camadas genealógicas)
  RPT.eras.forEach((e, i) => {
    const x0 = X(e.from), x1 = X(e.to);
    U.svgEl("rect", { x: x0, y: topY - 34, width: x1 - x0, height: botY - topY + 34,
      fill: i % 2 ? "rgba(184,146,74,.07)" : "rgba(29,37,72,.045)" }, svg);
    const lbl = e.name.toUpperCase();
    const half = lbl.length * 3.4; // meia-largura estimada (mono 8.5px + ls)
    const cx = U.clamp((x0 + x1) / 2, mL + half, W - 10 - half);
    U.svgText(svg, cx, topY - 44 - (i % 2) * 13, lbl, { size: 8.5, fill: P.inkLo, anchor: "middle", ls: 1.6, weight: 700, halo: true });
  });

  // eixo duplo
  const ax = U.svgEl("g", {}, svg);
  U.svgEl("line", { x1: mL - 10, y1: axisY0, x2: W - mR + 10, y2: axisY0, stroke: P.ink, "stroke-width": 1.6 }, ax);
  U.svgEl("line", { x1: mL - 10, y1: axisY0 + 4, x2: W - mR + 10, y2: axisY0 + 4, stroke: P.ink, "stroke-width": 0.6 }, ax);
  for (let y = 400; y <= 1900; y += 100) {
    const x = X(y);
    U.svgEl("line", { x1: x, y1: axisY0 - 5, x2: x, y2: axisY0 + 9, stroke: P.ink, "stroke-width": 1 }, ax);
    U.svgText(ax, x, axisY0 + 26, String(y), { size: 9.5, anchor: "middle", fill: P.inkMd });
  }

  const stemLayer = U.svgEl("g", {}, svg);
  const plaqueLayer = U.svgEl("g", {}, svg);

  const srcOf = k => (window.SRCS || []).find(s => s.k === k);
  placed.forEach((e, i) => {
    const f = FAM[e.fam];
    const py = e.up ? axisY0 - (e.L + 1) * layerH + 6
                    : axisY0 + 12 + e.L * layerH;
    // haste + ponto
    U.svgEl("line", { x1: e.x, y1: e.up ? py + plaqueH : py, x2: e.x, y2: axisY0 + (e.up ? -3 : 3),
      stroke: f.c, "stroke-width": 0.8, "stroke-dasharray": e.L > 0 ? "2 2" : "none", opacity: .55 }, stemLayer);
    U.svgEl("circle", { cx: e.x, cy: axisY0, r: 3, fill: f.c }, stemLayer);
    // placa
    const g = U.svgEl("g", { cursor: "pointer", tabindex: 0, role: "button",
      "aria-label": `${e.y} — ${e.t}` }, plaqueLayer);
    g.setAttribute("data-drill-keep", "");
    const rect = U.svgEl("rect", { x: e.x - e.w / 2, y: py, width: e.w, height: plaqueH, rx: 1.5,
      fill: P.hi, stroke: f.c, "stroke-width": e.fam === "iconocracia" ? 1.8 : 1.1 }, g);
    U.svgText(g, e.x, py + 14, e.y + " · " + f.sh.toUpperCase(), { size: 7.5, anchor: "middle", fill: f.c, ls: 1, weight: 700 });
    U.svgText(g, e.x, py + 30, e.title, { size: 11, anchor: "middle", fill: P.ink, font: U.SERIF, weight: 700, halo: false });
    const open = ev => {
      const s = srcOf(e.k);
      U.showDrill({ title: `${e.y} · ${f.lbl}`, value: e.t, sub: e.d,
        source: s ? `${e.k} · ${s.name} (${s.date})` : e.k, x: ev.clientX, y: ev.clientY });
    };
    // hover/foco: a placa sobe ao primeiro plano, engrossa o traço e revela o título inteiro.
    // O reparent (appendChild) só pode acontecer no hover: no foco de teclado, mover o
    // elemento no DOM durante o evento de focus faz o Chromium devolvê-lo ao body.
    const baseSW = rect.getAttribute("stroke-width");
    const lift = reparent => { if (reparent) plaqueLayer.appendChild(g); rect.setAttribute("stroke-width", 2.6); };
    const drop = () => { rect.setAttribute("stroke-width", baseSW); U.hideTip(); };
    g.addEventListener("mouseenter", ev => { lift(true); U.showTip(`<b>${e.y}</b> · ${e.t}`, ev.clientX, ev.clientY); });
    g.addEventListener("mousemove", ev => U.showTip(`<b>${e.y}</b> · ${e.t}`, ev.clientX, ev.clientY));
    g.addEventListener("mouseleave", drop);
    g.addEventListener("focus", () => { lift(false); const r = g.getBoundingClientRect(); U.showTip(`<b>${e.y}</b> · ${e.t}`, r.left + r.width / 2, r.top); });
    g.addEventListener("blur", drop);
    g.addEventListener("click", open);
    g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(ev); } });
    // entrada escalonada
    if (!U.REDUCE) {
      g.style.opacity = 0; g.style.transition = "opacity .5s ease";
      g.style.transform = "translateY(10px)"; g.style.transition += ", transform .5s cubic-bezier(.22,1,.36,1)";
    }
    e._g = g; e._i = i;
  });

  // legenda
  const leg = U.svgEl("g", {}, svg);
  let lx = mL;
  Object.values(FAM).forEach(f => {
    U.svgEl("rect", { x: lx, y: H - 30, width: 10, height: 10, fill: f.c }, leg);
    const t = U.svgText(leg, lx + 16, H - 21, f.lbl.toUpperCase(), { size: 8, fill: P.inkMd, ls: 1.2, weight: 700, halo: false });
    lx += 16 + f.lbl.length * 6 + 26;
  });

  // entrada em IO: placas da esquerda para a direita
  const reveal = () => placed.forEach(e => setTimeout(() => {
    e._g.style.opacity = 1; e._g.style.transform = "translateY(0)";
  }, U.REDUCE ? 0 : e._i * 70));
  if (U.REDUCE) reveal();
  else {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { reveal(); io.disconnect(); }
    }), { threshold: 0.15 });
    io.observe(svg);
  }
})();
