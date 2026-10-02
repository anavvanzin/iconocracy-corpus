/* Módulos: matriz de verificação (P5) · cadeia VFT · edições de Ripa · tabela de atributos · correções · trilho */
(() => {
  const { showDrill, clamp } = window.U;
  const INK = "#1A1612", INKM = "#625A50", INKL = "#6B6157";
  const NAVY = "#1D2548", LACRE = "#A8281F", GOLD = "#B8924A", TERRA = "#A04030";
  const LINELO = "rgba(26,22,18,.10)", LINE = "#D4C19A";
  const SRC = id => (window.SOURCES.find(s => s.id === id) || {});
  const VERDICT = {
    ok:   { c: NAVY,  t: "CONFIRMADO" },
    warn: { c: GOLD,  t: "COM NUANCES" },
    fix:  { c: LACRE, t: "CORRIGIR" }
  };

  // ── P5 · MATRIZ DE VERIFICAÇÃO ──
  function matrix(host) {
    const rows = window.RPT.matrix;
    const tbl = document.createElement("table");
    tbl.className = "dt vmatrix";
    tbl.innerHTML = `<thead><tr>
      <th style="width:64px">NOTA</th><th>AFIRMAÇÃO DO RASCUNHO</th>
      <th style="width:170px">VEREDITO</th><th style="width:60px">FONTES</th></tr></thead>`;
    const tb = document.createElement("tbody");
    rows.forEach((r, i) => {
      const v = VERDICT[r.verdict];
      const tr = document.createElement("tr");
      tr.tabIndex = 0; tr.dataset.drillKeep = "1";
      tr.innerHTML = `
        <td class="mono">${r.n}</td>
        <td>${r.claim}</td>
        <td><span class="verdict" style="--vc:${v.c}"><i></i>${r.vtxt}</span></td>
        <td class="mono small">${r.k}</td>`;
      const open = e => {
        const ks = r.k.split(" ").map(k => SRC(k)).filter(s => s.label);
        showDrill({
          title: `Nota ${r.n} · ${v.t}`,
          value: "",
          sub: `<b>${r.claim}</b><br><br>${r.note}`,
          source: ks.map(s => s.label).join(" · "),
          x: e.clientX || innerWidth/2, y: e.clientY || 200
        });
      };
      tr.addEventListener("click", open);
      tr.addEventListener("keydown", e => { if (e.key === "Enter") open(e); });
      tr.style.opacity = 0; tr.style.transform = "translateY(8px)";
      tr.style.transition = `opacity .45s ${i*55}ms, transform .45s ${i*55}ms`;
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    host.appendChild(tbl);
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) {
        host.querySelectorAll("tbody tr").forEach(tr => { tr.style.opacity = 1; tr.style.transform = "none"; });
        io.disconnect();
      }
    }), { threshold: .12 });
    io.observe(host);
  }

  // ── CADEIA VERITAS FILIA TEMPORIS ──
  function vft(host) {
    const d = window.RPT.vft;
    host.innerHTML = `
      <div class="vft-grid">
        <div class="vft-node vft-origin">
          <p class="vft-k">ORIGEM LITERÁRIA</p>
          <p class="vft-t">${d.origem.t}</p>
          <p class="vft-d">${d.origem.d}</p>
        </div>
        <div class="vft-arrow">→</div>
        <div class="vft-node">
          <p class="vft-k">MEDIAÇÃO EMBLEMÁTICA</p>
          <p class="vft-t">${d.mediacoes[0].t}</p>
          <p class="vft-d">${d.mediacoes[0].d}</p>
        </div>
        <div class="vft-arrow">→</div>
        <div class="vft-branch">
          ${d.apropriacoes.map(a => `
            <div class="vft-node vft-side">
              <p class="vft-k">${a.lado}</p>
              <p class="vft-t">${a.t}</p>
              <p class="vft-d">${a.d}</p>
            </div>`).join("")}
        </div>
        <div class="vft-arrow">→</div>
        <div class="vft-node vft-reversal">
          <p class="vft-k">A REVERSÃO</p>
          <p class="vft-t">${d.reversao.t}</p>
          <p class="vft-d">${d.reversao.d}</p>
        </div>
      </div>`;
  }

  // ── EDIÇÕES DA ICONOLOGIA ──
  function ripa(host) {
    const NS = "http://www.w3.org/2000/svg";
    const el = (t,a,p) => { const n = document.createElementNS(NS,t); for (const k in a) n.setAttribute(k,a[k]); p && p.appendChild(n); return n; };
    const eds = window.RPT.ripa_edicoes.map(e => ({ ...e, yr: parseInt(String(e.y)) || 1764 }));
    const W = 800, H = 300;
    const langs = ["IT","FR","NL","DE","EN","ES"];
    const LCOL = { IT: INK, FR: INKM, NL: GOLD, DE: INKL, EN: NAVY, ES: LACRE };
    const body = window.U.frame(host, {
      title: "A Iconologia circulou pela Europa — mas não em espanhol",
      sub: "CADA PONTO = UMA EDIÇÃO (1593–1987) · A ÚNICA EM ESPANHOL É DE 1987, EM LACRE · A EDIÇÃO DE SENA (1613) CHEGOU A MINAS GERAIS",
      src: "Alchemy Website (lista de edições) · Martayan Lan · Zimmermann/DBNL"
    });
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%" }, body);
    const X = y => 56 + ((y-1580)/(2010-1580))*(W-100);
    const Y = l => 40 + langs.indexOf(l)*34;
    langs.forEach(l => {
      const t = el("text", { x: 12, y: Y(l)+4, "font-family": "'JetBrains Mono', ui-monospace, monospace", "font-size": 10, "font-weight": 700, fill: LCOL[l] }, svg);
      t.textContent = l;
      el("line", { x1: 40, y1: Y(l), x2: W-40, y2: Y(l), stroke: LINELO, "stroke-width": 1 }, svg);
    });
    [1600,1700,1800,1900,2000].forEach(y => {
      const t = el("text", { x: X(y), y: H-14, "text-anchor": "middle", "font-family": "'JetBrains Mono', ui-monospace, monospace", "font-size": 9, fill: INKL }, svg);
      t.textContent = y;
      el("line", { x1: X(y), y1: 30, x2: X(y), y2: H-26, stroke: LINELO, "stroke-width": 1 }, svg);
    });
    eds.forEach((e,i) => {
      const g = el("g", { cursor: "pointer" }, svg);
      const cx = X(e.yr), cy = Y(e.lang);
      const c = el("circle", { cx, cy, r: (e.yr===1987||e.yr===1613) ? 7 : 5, fill: LCOL[e.lang], opacity: 0 }, g);
      c.style.transition = `opacity .4s ${i*60}ms`;
      if (e.yr === 1613) {
        el("circle", { cx, cy, r: 11, fill: "none", stroke: NAVY, "stroke-width": 1.4, "stroke-dasharray": "3 2" }, g);
        const t = el("text", { x: cx, y: cy-17, "text-anchor": "middle", "font-family": "'JetBrains Mono', ui-monospace, monospace", "font-size": 9, "font-weight": 700, fill: NAVY }, g);
        t.textContent = "1613 · SENA → MINAS";
      }
      if (e.yr === 1987) {
        const t = el("text", { x: cx, y: cy-14, "text-anchor": "middle", "font-family": "'JetBrains Mono', ui-monospace, monospace", "font-size": 9, "font-weight": 700, fill: LACRE }, g);
        t.textContent = "1987 · AKAL — A PRIMEIRA";
      }
      g.addEventListener("click", ev => showDrill({
        title: `Iconologia · ${e.y} (${e.cidade})`, value: e.lang,
        sub: e.nota || "Edição registrada nas listas bibliográficas consolidadas.",
        source: "Alchemy Website — lista de edições", x: ev.clientX, y: ev.clientY
      }));
      g.dataset.drillKeep = "1";
      requestAnimationFrame(() => requestAnimationFrame(() => c.style.opacity = .9));
    });
  }

  // ── TABELA DE ATRIBUTOS ──
  function atributos(host) {
    const tbl = document.createElement("table");
    tbl.className = "dt";
    tbl.innerHTML = `<thead><tr><th>FIGURA</th><th>ATRIBUTOS CENTRAIS</th><th>REGIME VISUAL</th><th>FONTES</th></tr></thead>`;
    const tb = document.createElement("tbody");
    window.RPT.atributos.forEach(r => {
      const hot = /DISPUTADO|NUDEZ/.test(r.r);
      const tr = document.createElement("tr");
      tr.innerHTML = `<td><b>${r.f}</b></td><td>${r.a}</td>
        <td class="${hot ? "hot" : ""}">${r.r}</td><td class="mono small">${r.k}</td>`;
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    host.appendChild(tbl);
  }

  // ── CORREÇÕES ──
  function correcoes(host) {
    host.innerHTML = window.RPT.correcoes.map(c => `
      <div class="fix-row">
        <span class="fix-n">${c.n}</span>
        <span class="fix-note mono">${c.nota}</span>
        <p class="fix-txt">${c.txt}</p>
      </div>`).join("");
  }

  // ── TRILHO DIREITO ──
  function rail() {
    const cv = document.getElementById("dash-canvas");
    if (!cv) return;
    const secs = [...document.querySelectorAll("main section[id], footer[id]")];
    const names = {
      "sec-exec": "VEREDITO", "sec-feminino": "O FEMININO", "sec-iustitia": "IVSTITIA",
      "sec-veritas": "VERITAS", "sec-ripa": "RIPA", "sec-brasil": "BRASIL",
      "sec-sintese": "SÍNTESE", "sec-sources": "FONTES"
    };
    function draw(activeIdx, prog) {
      const r = cv.getBoundingClientRect();
      if (r.width < 4) return;
      const dpr = Math.min(devicePixelRatio||1, 2);
      cv.width = r.width*dpr; cv.height = r.height*dpr;
      const ctx = cv.getContext("2d");
      ctx.setTransform(dpr,0,0,dpr,0,0);
      ctx.clearRect(0,0,r.width,r.height);
      const x = 10, y0 = 34, y1 = r.height-34;
      ctx.strokeStyle = LINE; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x,y0); ctx.lineTo(x,y1); ctx.stroke();
      ctx.strokeStyle = NAVY;
      ctx.beginPath(); ctx.moveTo(x,y0); ctx.lineTo(x, y0+(y1-y0)*prog); ctx.stroke();
      secs.forEach((s,i) => {
        const y = y0+(y1-y0)*(secs.length===1?0:i/(secs.length-1));
        const on = i===activeIdx;
        ctx.fillStyle = on ? NAVY : INKL;
        ctx.beginPath(); ctx.arc(x,y,on?4:2.4,0,Math.PI*2); ctx.fill();
        if (on) {
          ctx.fillStyle = INK;
          ctx.font = "700 10px 'JetBrains Mono', ui-monospace, monospace";
          ctx.fillText(names[s.id]||s.id, x+14, y+3);
        }
      });
      // mini-balança viva
      const t = performance.now()/1000;
      const bx = r.width-46, by = 44, s = 1.5;
      const tilt = Math.sin(t*.7)*.12;
      ctx.save();
      ctx.translate(bx, by); ctx.rotate(tilt);
      ctx.strokeStyle = INK; ctx.lineWidth = 1.1;
      ctx.beginPath(); ctx.moveTo(0,-14*s); ctx.lineTo(0,8*s); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-10*s,-10*s); ctx.lineTo(10*s,-10*s); ctx.stroke();
      [[-10],[10]].forEach(([px])=>{
        ctx.beginPath();
        ctx.moveTo(px*s,-10*s); ctx.lineTo((px-3)*s,-2*s);
        ctx.moveTo(px*s,-10*s); ctx.lineTo((px+3)*s,-2*s);
        ctx.stroke();
        ctx.beginPath(); ctx.arc(px*s,-2*s,3*s,0,Math.PI); ctx.stroke();
      });
      ctx.restore();
      ctx.fillStyle = INKL;
      ctx.font = "8px 'JetBrains Mono', ui-monospace, monospace";
      ctx.textAlign = "center";
      ctx.fillText("AEQUITAS", bx, by+26);
      ctx.textAlign = "left";
    }
    let state = { ai: 0, prog: 0 };
    function measure() {
      const sc = scrollY;
      const total = document.body.scrollHeight - innerHeight;
      let ai = 0;
      secs.forEach((s,i) => { if (s.offsetTop - innerHeight*.45 <= sc) ai = i; });
      state = { ai, prog: Math.min(1, sc/Math.max(total,1)) };
    }
    addEventListener("scroll", measure, { passive: true });
    addEventListener("resize", measure);
    measure();
    (function loop(){ draw(state.ai, state.prog); requestAnimationFrame(loop); })();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const m = document.getElementById("matrix-host"); if (m) matrix(m);
    const v = document.getElementById("vft-host"); if (v) vft(v);
    const r = document.getElementById("ripa-chart"); if (r) ripa(r);
    const a = document.getElementById("atributos-host"); if (a) atributos(a);
    const c = document.getElementById("correcoes-host"); if (c) correcoes(c);
    rail();
    document.querySelectorAll("[data-goto]").forEach(b =>
      b.addEventListener("click", () =>
        document.querySelector(b.dataset.goto)?.scrollIntoView({ behavior: "smooth" })));
  });
})();
