// P2 · Fluxo de destino — matrizes e mediações fluem para as iconocracias nacionais
(() => {
  const host = document.getElementById("flow-chart");
  if (!host) return;
  const P = U.PAL;
  const body = U.frame(host, {
    title: "As herdeiras nacionais são investiduras locais de uma gramática comum",
    sub: "LINHAS DE VIDA POR ANO DE NASCIMENTO · FITAS = DESCENDÊNCIA ICONOGRÁFICA DOCUMENTADA · TRACEJADO = CONTRACASO",
    src: "Síntese qualitativa do dossiê §8.2 (três camadas) · âncoras K6–K25",
  });

  const W = 880, rowH = 42;
  const xL = 218, xR = 618;                    // trilho das linhas de vida
  const X = y => xL + (y - 380) / (1900 - 380) * (xR - xL);

  // linhas: montar entidades com y de fileira
  const rows = [];
  RPT.flow.cohorts.forEach(c => {
    rows.push({ cohort: c.name });
    c.items.forEach(it => rows.push({ ...it, cohortName: c.name }));
  });
  const topPad = 34, H = topPad + rows.length * rowH + 66;
  let ry = topPad;
  rows.forEach(r => { r.yy = ry; ry += rowH; });

  // placas de desfecho ordenadas pela média das entradas (menos cruzamentos)
  const outs = RPT.flow.outcomes.map((o, i) => ({ ...o, i, inflow: [] }));
  rows.forEach(r => { if (r.out != null) outs[r.out].inflow.push(r.yy); });
  outs.forEach(o => o.my = o.inflow.reduce((a, b) => a + b, 0) / o.inflow.length);
  const order = outs.slice().sort((a, b) => a.my - b.my);
  const plaqueX = 652, plaqueW = 208, plaqueH = 46;
  order.forEach((o, j) => { o.py = topPad + 26 + j * (plaqueH + 26); });

  const svg = U.svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", role: "img",
    "aria-label": "Fluxo das camadas genealógicas para as alegorias nacionais" }, body);
  svg.style.display = "block"; svg.style.height = "auto";

  // banda da virada revolucionária
  U.svgEl("rect", { x: X(1789), y: topPad - 16, width: X(1900) - X(1789) + 46, height: H - topPad - 34,
    fill: "rgba(168,40,31,.05)" }, svg);
  U.svgText(svg, X(1789) + 6, topPad - 22, "1789 → A ICONOCRACIA DE ESTADO", { size: 7.5, fill: P.lacre, ls: 1.4, weight: 700, halo: false });

  const lineLayer = U.svgEl("g", {}, svg);
  const ribbonLayer = U.svgEl("g", {}, svg);
  const labelLayer = U.svgEl("g", {}, svg);
  const plaqueLayer = U.svgEl("g", {}, svg);

  const srcOf = k => (window.SRCS || []).find(s => s.k === k);

  // fitas (antes das placas e rótulos)
  rows.forEach(r => {
    if (r.out == null) return;
    const o = outs[r.out];
    const x1 = X(Math.min(o.y, 1900)), y1 = r.yy - 6;
    const x2 = plaqueX, y2 = o.py + plaqueH / 2;
    const mx = (x1 + x2) / 2;
    const path = `M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`;
    r._ribbon = U.svgEl("path", {
      d: path, fill: "none", stroke: o.i === 3 ? P.contra : P.lacre,
      "stroke-width": o.i === 3 ? 1.4 : 2, "stroke-dasharray": o.i === 3 ? "5 4" : "none",
      opacity: o.i === 3 ? 0.9 : 0.55, "stroke-linecap": "round",
    }, ribbonLayer);
  });

  // linhas de vida + rótulos
  rows.forEach(r => {
    if (r.cohort) {
      U.svgText(labelLayer, 30, r.yy - 2, r.cohort.toUpperCase(), { size: 8.5, fill: P.gold, ls: 2, weight: 700, halo: false });
      U.svgEl("line", { x1: 30, y1: r.yy + 6, x2: xR + 30, y2: r.yy + 6, stroke: P.line, "stroke-width": 0.7 }, labelLayer);
      return;
    }
    const o = outs[r.out];
    const x0 = X(r.y), x1 = X(Math.min(o.y, 1900));
    r._line = U.svgEl("line", { x1: x0, y1: r.yy - 6, x2: x1, y2: r.yy - 6, stroke: P.ink,
      "stroke-width": 2.4, "stroke-linecap": "round" }, lineLayer);
    U.svgEl("circle", { cx: x0, cy: r.yy - 6, r: 3, fill: P.ink }, lineLayer);
    U.svgText(labelLayer, x0, r.yy + 12, String(r.y), { size: 8, anchor: "middle", fill: P.inkLo, halo: false });
    const t = U.svgText(labelLayer, 30, r.yy - 2, r.n, { size: 12.5, font: U.SERIF, fill: P.ink, weight: r.contra ? 700 : 400 });
    if (r.contra) t.setAttribute("font-style", "italic");
    const g = U.svgEl("g", { cursor: "pointer", "data-drill-keep": "", tabindex: 0, role: "button",
      "aria-label": `${r.y} — ${r.n} — abrir base iconográfica` }, labelLayer);
    U.svgEl("rect", { x: 24, y: r.yy - 22, width: xR - 10, height: rowH - 6, fill: "transparent" }, g);
    const openRow = ev => {
      const s = srcOf(o.k);
      U.showDrill({ title: `${r.cohortName} · nasce ${r.y}`, value: r.n,
        sub: `Flui para: ${o.n}. ${r.contra ? "Contracaso — a linha não alimenta nenhum Estado; alimenta autoridade de mulher." : "Descendência iconográfica registrada no dossiê."}`,
        source: s ? `${o.k} · ${s.name} (${s.date})` : o.k, x: ev.clientX, y: ev.clientY });
    };
    g.addEventListener("click", openRow);
    g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openRow(ev); } });
  });

  // placas de desfecho
  outs.forEach(o => {
    const g = U.svgEl("g", { cursor: "pointer", "data-drill-keep": "", tabindex: 0, role: "button",
      "aria-label": `Desfecho ${o.n} — abrir base iconográfica` }, plaqueLayer);
    U.svgEl("rect", { x: plaqueX, y: o.py, width: plaqueW, height: plaqueH, fill: P.hi, stroke: P.ink, "stroke-width": 1.2 }, g);
    U.svgEl("rect", { x: plaqueX, y: o.py, width: 4, height: plaqueH, fill: o.i === 3 ? P.contra : P.lacre }, g);
    const words = o.n.toUpperCase().split(" ");
    const mid = Math.ceil(words.length / 2);
    U.svgText(g, plaqueX + 14, o.py + 19, words.slice(0, mid).join(" "), { size: 8.5, fill: P.ink, ls: 1.2, weight: 700, halo: false });
    U.svgText(g, plaqueX + 14, o.py + 32, words.slice(mid).join(" ") + "  ·  " + o.inflow.length + "×", { size: 8.5, fill: P.inkLo, ls: 1.2, halo: false });
    const openOut = ev => {
      const s = srcOf(o.k);
      U.showDrill({ title: `Desfecho · ${o.y}`, value: o.n,
        sub: `${o.inflow.length} linhas de filiação chegam a este regime. ${o.i === 3 ? "Fissura do regime: a alegoria feminina convertida em autoria." : "Iconocracia nacional moderna — a gramática herdada investida de poder de Estado."}`,
        source: s ? `${o.k} · ${s.name} (${s.date})` : o.k, x: ev.clientX, y: ev.clientY });
    };
    g.addEventListener("click", openOut);
    g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openOut(ev); } });
  });

  // entrada: linhas crescem → fitas desenham → placas surgem
  function animate() {
    if (U.REDUCE) return;
    rows.forEach(r => {
      if (r._line) {
        const len = r._line.getTotalLength();
        r._line.style.strokeDasharray = len; r._line.style.strokeDashoffset = len;
        r._line.style.transition = "stroke-dashoffset 1s cubic-bezier(.22,1,.36,1)";
      }
      if (r._ribbon) {
        const len = r._ribbon.getTotalLength();
        r._ribbon.style.strokeDasharray = r.out === 3 ? "5 4" : len;
        if (r.out !== 3) { r._ribbon.style.strokeDashoffset = len; r._ribbon.style.transition = "stroke-dashoffset 1.1s ease .5s"; }
        else { r._ribbon.style.opacity = 0; r._ribbon.style.transition = "opacity .8s ease .9s"; }
      }
    });
    plaqueLayer.style.opacity = 0; plaqueLayer.style.transition = "opacity .8s ease 1.2s";
    requestAnimationFrame(() => requestAnimationFrame(() => {
      rows.forEach(r => {
        if (r._line) r._line.style.strokeDashoffset = 0;
        if (r._ribbon) { if (r.out !== 3) r._ribbon.style.strokeDashoffset = 0; else r._ribbon.style.opacity = 0.9; }
      });
      plaqueLayer.style.opacity = 1;
    }));
  }
  if (U.REDUCE) { /* estado final estático */ }
  else {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { animate(); io.disconnect(); }
    }), { threshold: 0.15 });
    io.observe(svg);
  }
})();
