// Utilitários compartilhados — ICONOCRACIA · relatório interativo
// Paleta re-tematizada para Mnemosyne Viva / Iuris Memoria (tokens literais do design system).
window.U = (() => {
  const TAU = Math.PI * 2;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = t => t * t * (3 - 2 * t);
  const ease = (cur, tgt, dt, dur) => cur + (tgt - cur) * (1 - Math.exp(-dt / dur));
  const REDUCE = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function makeRng(seed) {
    let s = seed >>> 0;
    return () => {
      s += 0x6d2b79f5; let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Mnemosyne Viva: vellum + iron-gall ink + terracotta (margem viva) + gold + amethyst (voz feminina)
  const PAL = {
    paper: "#EFE5CF", hi: "#F8F5EE", ivory: "#E8DCC4",
    ink: "#1A1612", inkMd: "#625A50", inkLo: "#6B6157",
    line: "#D4C19A", lineLo: "rgba(26,22,18,.10)",
    accent: "#A04030", accentHi: "#7C2D12", accentSoft: "rgba(160,64,48,.14)",
    lacre: "#A8281F", gold: "#B8924A", goldBright: "#D4A85E",
    amethyst: "#8A5FA8", amethystSoft: "rgba(138,95,168,.15)",
    navy: "#1D2548", navySoft: "rgba(29,37,72,.10)",
    neg: "#A02828",
    fem: "#8A5FA8", masc: "#1D2548", contra: "#A04030",
  };
  const SERIES = [PAL.accent, PAL.gold, PAL.navy, PAL.amethyst];
  const SERIF = '"Crimson Pro", Georgia, serif';
  const DISPLAY = '"Instrument Serif", Georgia, serif';
  const MONO = '"JetBrains Mono", ui-monospace, monospace';

  function bindCanvas(canvas) {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const fit = () => {
      const r = canvas.getBoundingClientRect();
      canvas.width = Math.round(r.width * dpr);
      canvas.height = Math.round(r.height * dpr);
      const ctx = canvas.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { w: r.width, h: r.height, cx: r.width / 2, cy: r.height / 2 };
    };
    return { fit, ctx: canvas.getContext("2d") };
  }

  function countUp(el, { from = 0, to = 1, dur = 1100, fmt = v => Math.round(v).toLocaleString("pt-BR") } = {}) {
    if (REDUCE) { el.textContent = fmt(to); return () => {}; }
    let raf = 0, t0 = null;
    const tick = ts => {
      if (t0 == null) t0 = ts;
      const t = clamp((ts - t0) / dur, 0, 1);
      const e = 1 - Math.pow(1 - t, 3);
      el.textContent = fmt(lerp(from, to, e));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }

  // ── Drill-down ──
  const drill = document.getElementById("drill-card");
  let drillOpen = false;
  function showDrill({ title, value, sub, source, x, y }) {
    if (!drill) return;
    // acionamento por teclado não tem coordenadas de ponteiro — centraliza o cartão
    if (!x && !y) { x = window.innerWidth / 2 - 160; y = window.innerHeight / 2; }
    drill.innerHTML = `<button class="d-close" aria-label="Fechar">✕</button>
      <div class="d-title">${title}</div>
      <div class="d-val">${value}</div>
      ${sub ? `<div class="d-sub">${sub}</div>` : ""}
      ${source ? `<div class="d-src">Fonte · ${source}</div>` : ""}`;
    drill.hidden = false; drillOpen = true;
    const r = drill.getBoundingClientRect();
    let left = clamp(x + 14, 8, window.innerWidth - r.width - 8);
    let top = clamp(y - r.height - 14, 8, window.innerHeight - r.height - 8);
    if (y - r.height - 14 < 8) top = clamp(y + 18, 8, window.innerHeight - r.height - 8);
    drill.style.left = left + "px"; drill.style.top = top + "px";
    drill.querySelector(".d-close").onclick = hideDrill;
  }
  function hideDrill() { if (drill) drill.hidden = true; drillOpen = false; }
  document.addEventListener("click", e => {
    if (drillOpen && drill && !drill.contains(e.target)) {
      if (!e.target.closest("[data-drill-keep]")) hideDrill();
    }
  }, true);
  document.addEventListener("keydown", e => { if (e.key === "Escape") hideDrill(); });

  // ── Tooltip ──
  const tip = document.createElement("div");
  tip.className = "tip"; document.body.appendChild(tip);
  function showTip(html, x, y) {
    tip.innerHTML = html; tip.style.opacity = 1;
    tip.style.left = clamp(x + 12, 4, window.innerWidth - 250) + "px";
    tip.style.top = (y - 34) + "px";
  }
  function hideTip() { tip.style.opacity = 0; }

  // ── Chart frame trio ──
  function frame(el, { title, sub, src }) {
    el.classList.add("chart-frame");
    const head = document.createElement("div");
    if (title) head.innerHTML = `<p class="chart-title">${title}</p>${sub ? `<p class="chart-sub">${sub}</p>` : ""}`;
    el.appendChild(head);
    const body = document.createElement("div");
    body.className = "chart-body";
    el.appendChild(body);
    if (src) {
      const s = document.createElement("p");
      s.className = "chart-src"; s.innerHTML = "Fonte · " + src;
      el.appendChild(s);
    }
    return body;
  }

  // SVG helpers (paint-order halo para texto sobre linhas)
  const SVGNS = "http://www.w3.org/2000/svg";
  function svgEl(tag, attrs = {}, parent) {
    const n = document.createElementNS(SVGNS, tag);
    for (const k in attrs) { if (attrs[k] != null) n.setAttribute(k, attrs[k]); }
    if (parent) parent.appendChild(n);
    return n;
  }
  function svgText(parent, x, y, str, { font = MONO, size = 10, fill = PAL.inkMd, anchor = "start", ls = 0, halo = true, weight = 400, style = "" } = {}) {
    const t = svgEl("text", {
      x, y, "font-family": font, "font-size": size, fill,
      "text-anchor": anchor, "letter-spacing": ls, "font-weight": weight, "font-style": style,
    }, parent);
    if (halo) { t.setAttribute("paint-order", "stroke"); t.setAttribute("stroke", PAL.paper); t.setAttribute("stroke-width", 4); t.setAttribute("stroke-linejoin", "round"); }
    t.textContent = str;
    return t;
  }

  return { TAU, clamp, lerp, smooth, ease, REDUCE, makeRng, PAL, SERIES, SERIF, DISPLAY, MONO,
           bindCanvas, countUp, showDrill, hideDrill, showTip, hideTip, frame, svgEl, svgText };
})();
