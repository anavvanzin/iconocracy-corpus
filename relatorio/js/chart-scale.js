// P18 · Balança-veredito — o instrumento de Iustitia pesa as duas leituras do paradoxo
// Codificação estrutural tripla: lado da evidência (topologia) + inclinação (peso)
// + pesos tracejados suspensos (condições de consolidação ainda não atendidas).
(() => {
  const host = document.getElementById("scale-chart");
  if (!host) return;
  const P = U.PAL;
  const body = U.frame(host, {
    title: "A estrutura pesa mais que a hipocrisia — com falseabilidade declarada",
    sub: "A INCLINAÇÃO É QUALITATIVA, NÃO UM ESCORE · PESOS TRACEJADOS = TESTES PENDENTES · CLIQUE NOS PESOS",
    src: "Dossiê §8.1 (três demonstrações) · âncoras K13, K20, K23, K15, K27",
  });

  const W = 880, H = 560, FX = 440, FY = 128, ARM = 252;
  const svg = U.svgEl("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%", role: "img",
    "aria-label": "Balança da Justiça pesando duas leituras do paradoxo iconocrático" }, body);
  svg.style.display = "block"; svg.style.height = "auto";

  const defs = U.svgEl("defs", {}, svg);
  const pat = U.svgEl("pattern", { id: "hatch-red", width: 7, height: 7, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, defs);
  U.svgEl("rect", { width: 7, height: 7, fill: "rgba(160,40,40,.10)" }, pat);
  U.svgEl("line", { x1: 0, y1: 0, x2: 0, y2: 7, stroke: P.neg, "stroke-width": 1.1 }, pat);

  const srcOf = k => (window.SRCS || []).find(s => s.k === k);
  const V = RPT.verdict;

  // pedestal e coluna
  const gBase = U.svgEl("g", {}, svg);
  U.svgEl("rect", { x: FX - 90, y: 492, width: 180, height: 10, fill: P.ink }, gBase);
  U.svgEl("rect", { x: FX - 62, y: 482, width: 124, height: 10, fill: P.ink }, gBase);
  U.svgEl("rect", { x: FX - 7, y: FY, width: 14, height: 482 - FY, fill: P.ink }, gBase);
  // placa-veredito pendurada na coluna
  U.svgEl("line", { x1: FX, y1: 208, x2: FX, y2: 224, stroke: P.gold, "stroke-width": 1.4 }, gBase);
  const plq = U.svgEl("g", { cursor: "pointer", "data-drill-keep": "", tabindex: 0, role: "button",
    "aria-label": "Veredito do dossiê — abrir síntese" }, gBase);
  U.svgEl("rect", { x: FX - 150, y: 224, width: 300, height: 66, fill: P.hi, stroke: P.gold, "stroke-width": 1.4 }, plq);
  U.svgText(plq, FX, 246, "VEREDITO DO DOSSIÊ", { size: 7.5, anchor: "middle", fill: P.gold, ls: 2.2, weight: 700, halo: false });
  U.svgText(plq, FX, 265, "O paradoxo não é uma contradição a explicar;", { size: 12.5, anchor: "middle", fill: P.ink, font: U.SERIF, style: "italic", halo: false });
  U.svgText(plq, FX, 281, "é a regra funcionando.", { size: 12.5, anchor: "middle", fill: P.ink, font: U.SERIF, style: "italic", halo: false });
  const openPlq = ev => U.showDrill({
    title: "Síntese §8.1", value: "Regra distribucional",
    sub: "Antiguidade e estabilidade (Siena, 1338) + sintaxe (hidrografia) + plasticidade ideológica (a venda). O Estado escolhe a forma feminina porque, na gramática herdada, o feminino é o significante do valor — e exclui as mulheres porque o exercício do poder foi distribuído ao masculino.",
    source: "K27 · Dossiê §8.1 (2026-09-26)", x: ev.clientX, y: ev.clientY });
  plq.addEventListener("click", openPlq);
  plq.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openPlq(ev); } });

  // mostrador do fulcro
  const gDial = U.svgEl("g", {}, svg);
  U.svgEl("path", { d: `M ${FX - 30} ${FY} A 30 30 0 0 1 ${FX + 30} ${FY}`, fill: "none", stroke: P.ink, "stroke-width": 1.4 }, gDial);
  for (const a of [-22, 0, 22]) {
    const r1 = 26, r2 = 31, rad = (a - 90) * Math.PI / 180;
    U.svgEl("line", { x1: FX + r1 * Math.cos(rad), y1: FY + r1 * Math.sin(rad),
      x2: FX + r2 * Math.cos(rad), y2: FY + r2 * Math.sin(rad), stroke: P.ink, "stroke-width": 1.2 }, gDial);
  }
  const needle = U.svgEl("line", { x1: FX, y1: FY, x2: FX, y2: FY - 27, stroke: P.lacre, "stroke-width": 2.2, "stroke-linecap": "round" }, gDial);
  U.svgEl("circle", { cx: FX, cy: FY, r: 4, fill: P.lacre }, gDial);

  // viga + pratos
  const beam = U.svgEl("line", { x1: FX - ARM, y1: FY, x2: FX + ARM, y2: FY, stroke: P.ink, "stroke-width": 4, "stroke-linecap": "round" }, svg);
  const panL = U.svgEl("g", {}, svg);
  const panR = U.svgEl("g", {}, svg);

  function weight(g, x, y, w, txt, opts = {}) {
    const wg = U.svgEl("g", { cursor: "pointer", "data-drill-keep": "",
      tabindex: opts.drill ? 0 : null, role: opts.drill ? "button" : null,
      "aria-label": opts.drill ? `${txt} — abrir base iconográfica` : null }, g);
    U.svgEl("path", {
      d: `M ${x - w / 2 + 8} ${y} L ${x + w / 2 - 8} ${y} L ${x + w / 2} ${y + 24} L ${x - w / 2} ${y + 24} Z`,
      fill: opts.solid ? P.ink : opts.dashed ? "none" : P.hi,
      stroke: opts.dashed ? P.gold : P.ink, "stroke-width": opts.dashed ? 1.3 : 1.4,
      "stroke-dasharray": opts.dashed ? "5 3" : "none",
    }, wg);
    U.svgEl("rect", { x: x - 7, y: y - 5, width: 14, height: 5, fill: opts.dashed ? "none" : opts.solid ? P.ink : P.hi,
      stroke: opts.dashed ? P.gold : P.ink, "stroke-width": 1.2, "stroke-dasharray": opts.dashed ? "4 2" : "none" }, wg);
    let s = txt; const budget = (w - 14) / 5.4;
    if (s.length > budget) {
      s = s.slice(0, Math.max(10, budget - 1));
      const sp = s.lastIndexOf(" ");
      if (sp > 8) s = s.slice(0, sp); // nunca corta palavra no meio
      s = s.replace(/[,;\s]+$/, "") + "…";
    }
    U.svgText(wg, x, y + 16.5, s, { size: 7.6, anchor: "middle", fill: opts.solid ? P.ivory : opts.dashed ? P.gold : P.ink, halo: false });
    if (opts.drill) {
      const openW = ev => U.showDrill({ ...opts.drill, x: ev.clientX, y: ev.clientY });
      wg.addEventListener("click", openW);
      wg.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openW(ev); } });
    }
    return wg;
  }

  let theta = 0;
  const CH = 52, PANW = 168;
  function layout() {
    const rad = theta * Math.PI / 180, c = Math.cos(rad), s = Math.sin(rad);
    const lx = FX - ARM * c, ly = FY - ARM * s;
    const rx = FX + ARM * c, ry = FY + ARM * s;
    beam.setAttribute("transform", `rotate(${theta} ${FX} ${FY})`);
    needle.setAttribute("transform", `rotate(${theta * 1.9} ${FX} ${FY})`);
    for (const [g, ex, ey, side] of [[panL, lx, ly, "L"], [panR, rx, ry, "R"]]) {
      g.innerHTML = "";
      const data = side === "L" ? V.left : V.right;
      const panY = ey + CH;
      // correntes
      U.svgEl("line", { x1: ex, y1: ey, x2: ex - PANW / 2 + 16, y2: panY, stroke: P.ink, "stroke-width": 1.2 }, g);
      U.svgEl("line", { x1: ex, y1: ey, x2: ex + PANW / 2 - 16, y2: panY, stroke: P.ink, "stroke-width": 1.2 }, g);
      // prato
      U.svgEl("path", { d: `M ${ex - PANW / 2} ${panY} Q ${ex} ${panY + 22} ${ex + PANW / 2} ${panY}`,
        fill: "none", stroke: P.ink, "stroke-width": 2.4 }, g);
      // nome do prato (abaixo do prato, fora da pilha de pesos)
      U.svgText(g, ex, panY + 38, data.name.toUpperCase(), { size: 7.8, anchor: "middle", fill: side === "R" ? P.lacre : P.inkMd, ls: 1.4, weight: 700 });
      // pesos empilhados do prato para cima
      const solid = side === "R";
      data.weights.forEach((wt, i) => {
        const wy = panY - (i + 1) * 29;
        const wpx = Math.min(PANW - 14, wt.t.length * 5.4 + 26);
        const s = srcOf(wt.k);
        const el = weight(g, ex, wy, wpx, wt.t, { solid,
          drill: { title: side === "R" ? "Evidência · leitura estrutural" : "Evidência · leitura contingente",
            value: wt.t, sub: side === "R" ? "Peso no prato da regra distribucional." : "Peso no prato da contingência — a leitura que o dossiê refuta.",
            source: s ? `${wt.k} · ${s.name} (${s.date})` : wt.k } });
        el.dataset.wi = i;
        if (!U.REDUCE) { el.style.opacity = 0; el.style.transform = "translateY(-90px)"; el.style.transition = "transform .7s cubic-bezier(.34,1.56,.64,1), opacity .4s"; }
      });
    }
  }
  layout();

  // gatilhos de consolidação (pesos tracejados suspensos fora dos pratos)
  const gTrig = U.svgEl("g", {}, svg);
  V.triggers.forEach((tr, i) => {
    const tx = i === 0 ? 104 : W - 104, ty = 44;
    const el = weight(gTrig, tx, ty, 168, tr.t, { dashed: true,
      drill: { title: "Teste pendente", value: tr.t,
        sub: "A leitura sobe de grau quando os testes pousarem nos pratos — o corpus de 336 itens é o laboratório.",
        source: "K27 · Dossiê §8.2 (2026-09-26)" } });
    const target = i === 0 ? FX - ARM + 30 : FX + ARM - 30;
    U.svgEl("path", { d: `M ${tx + (i === 0 ? 84 : -84)} ${ty + 14} Q ${(tx + target) / 2} ${ty + 34}, ${target} ${FY + 6}`,
      fill: "none", stroke: P.gold, "stroke-width": 1.1, "stroke-dasharray": "4 4", "marker-end": "none" }, gTrig);
    if (!U.REDUCE) { el.style.opacity = 0; el.style.transition = "opacity .8s ease 1.6s"; }
  });
  U.svgText(gTrig, FX, 66, "OS PESOS TRACEJADOS AINDA FLUTUAM: A LEITURA SE CONSOLIDA QUANDO POUSAM NOS PRATOS",
    { size: 7.5, anchor: "middle", fill: P.gold, ls: 1.6, weight: 700 });

  // faixa de falseabilidade
  const gFal = U.svgEl("g", { cursor: "pointer", "data-drill-keep": "", tabindex: 0, role: "button",
    "aria-label": "Linha de falseabilidade — abrir explicação" }, svg);
  U.svgEl("rect", { x: 60, y: H - 38, width: W - 120, height: 26, fill: "url(#hatch-red)", stroke: P.neg, "stroke-width": 1.2 }, gFal);
  U.svgText(gFal, FX, H - 21, "FALSEABILIDADE — " + V.falsification.toUpperCase(), { size: 8.2, anchor: "middle", fill: "#6e1b1b", ls: 0.8, weight: 700 });
  const openFal = ev => U.showDrill({
    title: "Linha de falseabilidade compartilhada", value: "A regra pode cair",
    sub: V.falsification + " A tese se declara refutável pelo próprio corpus — é esse o desenho do teste transnacional.",
    source: "K27 · Dossiê §8.2–8.3 (2026-09-26)", x: ev.clientX, y: ev.clientY });
  gFal.addEventListener("click", openFal);
  gFal.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openFal(ev); } });

  // coreografia: pesos pousam alternando → viga inclina → agulha deflete
  function animate() {
    if (U.REDUCE) { theta = 7; layout(); return; }
    const ws = [...panR.querySelectorAll("[data-wi]"), ...panL.querySelectorAll("[data-wi]")];
    ws.forEach((w, i) => setTimeout(() => { w.style.opacity = 1; w.style.transform = "translateY(0)"; }, 200 + i * 160));
    gTrig.querySelectorAll("g").forEach(el => { el.style.opacity = 1; });
    const t0 = performance.now(), dur = 1100, delay = 200 + ws.length * 160 + 200;
    setTimeout(function tween(now) {
      const t = U.clamp((performance.now() - t0 - 0) / dur, 0, 1);
      theta = 7 * (1 - Math.pow(1 - t, 3));
      layout(); // redesenha pratos; pesos já pousados perdem a animação → estado final
      panR.querySelectorAll("[data-wi]").forEach(w => { w.style.opacity = 1; w.style.transform = "none"; w.style.transition = "none"; });
      panL.querySelectorAll("[data-wi]").forEach(w => { w.style.opacity = 1; w.style.transform = "none"; w.style.transition = "none"; });
      if (t < 1) requestAnimationFrame(tween);
    }, delay);
  }
  if (U.REDUCE) animate();
  else {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { animate(); io.disconnect(); }
    }), { threshold: 0.25 });
    io.observe(svg);
  }
})();
