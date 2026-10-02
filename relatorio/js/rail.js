// P14 · Rail de contexto persistente — canvas fixo à direita, troca com a seção
(() => {
  const cv = document.getElementById("dash-canvas");
  if (!cv) return;
  const { fit, ctx } = U.bindCanvas(cv);
  const P = U.PAL;
  let V = fit();
  addEventListener("resize", () => { V = fit(); draw(); });

  const WINS = {
    sumario:  { no: "§0", t: "Sumário executivo", phase: -1, note: "O paradoxo é a regra funcionando" },
    tempo:    { no: "§1", t: "A gramática em obras", phase: 3, note: "405–1896 · três camadas" },
    regra:    { no: "§2", t: "A regra de distribuição", phase: 0, note: "Feminino = valor · masculino = potência" },
    camadas:  { no: "§3", t: "Herança", phase: 1, note: "Quem alimenta quem" },
    vitrine:  { no: "✦",  t: "Arquivo vivo", phase: 2, note: "A metamorfose das herdeiras · 3D" },
    veredito: { no: "§4", t: "Síntese", phase: 2, note: "A balança pesa o próprio regime" },
    fontes:   { no: "K",  t: "Fontes & método", phase: -1, note: "28 âncoras datadas" },
  };
  const PHASES = ["Matrizes", "Mediações", "Herdeiras"];
  let cur = "sumario";
  let hits = [];

  // histograma de marcos por meio-século (dos dados da linha do tempo)
  const bins = new Array(31).fill(0);
  RPT.timeline.forEach(e => { const b = Math.floor((e.y - 380) / 50); if (bins[b] != null) bins[b]++; });
  const famCount = {};
  RPT.timeline.forEach(e => famCount[e.fam] = (famCount[e.fam] || 0) + 1);

  function draw() {
    const { w: W, h: H } = V;
    if (W < 40) return;
    ctx.clearRect(0, 0, W, H);
    hits = [];
    const m = 44, cw = W - m * 2;
    let y = 84;
    const w = WINS[cur] || WINS.sumario;

    // distintivo da janela
    ctx.fillStyle = P.ink;
    ctx.fillRect(m, y, 46, 24);
    ctx.fillStyle = P.paper; ctx.font = `700 12px ${U.MONO}`; ctx.textAlign = "center";
    ctx.fillText(w.no, m + 23, y + 16.5);
    ctx.textAlign = "left"; ctx.fillStyle = P.ink; ctx.font = `400 21px ${U.DISPLAY}`;
    ctx.fillText(w.t, m, y + 52);
    ctx.fillStyle = P.inkLo; ctx.font = `400 11px ${U.SERIF}`; ctx.font = `italic 400 13px ${U.SERIF}`;
    ctx.fillText(w.note, m, y + 72);
    y += 96;

    // barra de fases (camadas genealógicas)
    ctx.font = `700 8.5px ${U.MONO}`; 
    const segW = (cw - 16) / 3;
    PHASES.forEach((ph, i) => {
      const x = m + i * (segW + 8);
      const on = w.phase === 3 || w.phase === i;
      ctx.fillStyle = on ? P.amethyst : "transparent";
      ctx.strokeStyle = on ? P.amethyst : P.line; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.rect(x, y, segW, 30); ctx.fill(); ctx.stroke();
      ctx.fillStyle = on ? "#fff" : P.inkLo;
      ctx.textAlign = "center"; ctx.fillText(ph.toUpperCase(), x + segW / 2, y + 19);
    });
    ctx.textAlign = "left";
    y += 52;

    // spark-histograma de marcos
    ctx.fillStyle = P.inkLo; ctx.font = `700 8px ${U.MONO}`;
    ctx.fillText("MARCOS POR MEIO-SÉCULO · 380–1910", m, y);
    y += 10;
    const bh = 54, bw = cw / bins.length;
    bins.forEach((v, i) => {
      const h = v ? (v / 3) * (bh - 8) + 4 : 1.5;
      ctx.fillStyle = v ? P.lacre : P.line;
      ctx.fillRect(m + i * bw + 1, y + bh - h, bw - 2.5, h);
    });
    ctx.strokeStyle = P.ink; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(m, y + bh + 0.5); ctx.lineTo(m + cw, y + bh + 0.5); ctx.stroke();
    ctx.fillStyle = P.inkLo; ctx.font = `400 8px ${U.MONO}`;
    ctx.fillText("405", m, y + bh + 14); ctx.textAlign = "right"; ctx.fillText("1896", m + cw, y + bh + 14); ctx.textAlign = "left";
    y += bh + 34;

    // quatro blocos de estatística (clicáveis)
    const sg = 12, sw = (cw - sg) / 2;
    RPT.stats.forEach((st, i) => {
      const x = m + (i % 2) * (sw + sg), sy = y + Math.floor(i / 2) * 74;
      ctx.strokeStyle = P.line; ctx.lineWidth = 1; ctx.strokeRect(x, sy, sw, 64);
      ctx.fillStyle = P.gold; ctx.fillRect(x, sy, 3, 64);
      ctx.fillStyle = P.lacre; ctx.font = `400 26px ${U.DISPLAY}`; ctx.textAlign = "left";
      ctx.fillText(st.num.toLocaleString("pt-BR"), x + 14, sy + 30);
      ctx.fillStyle = P.inkLo; ctx.font = `700 7.5px ${U.MONO}`;
      const words = st.lbl.toUpperCase().split(" ");
      words.forEach((wd, wi) => ctx.fillText(wd, x + 14, sy + 46 + wi * 9));
      hits.push({ x, y: sy, w: sw, h: 64, drill: st.drill });
    });
    y += 2 * 74 + 22;

    // células de coorte (famílias na linha do tempo)
    ctx.fillStyle = P.inkLo; ctx.font = `700 8px ${U.MONO}`;
    ctx.fillText("MARCOS POR FAMÍLIA ALEGÓRICA", m, y);
    y += 12;
    const FAMS = [["virtudes", "Virtudes", P.ink], ["continentes", "Continentes", P.gold],
      ["oceanos", "Oceanos e rios", P.navy], ["iconocracia", "Iconocracia", P.lacre], ["contracaso", "Contracaso", P.contra]];
    FAMS.forEach(([key, lbl, c]) => {
      const n = famCount[key] || 0;
      ctx.fillStyle = P.inkMd; ctx.font = `400 11.5px ${U.SERIF}`;
      ctx.fillText(lbl, m, y + 12);
      for (let i = 0; i < n; i++) {
        ctx.fillStyle = c; ctx.fillRect(m + 130 + i * 15, y + 3, 11, 11);
      }
      ctx.fillStyle = P.inkLo; ctx.font = `700 9px ${U.MONO}`;
      ctx.fillText("×" + n, m + 130 + n * 15 + 6, y + 12);
      y += 24;
    });

    // regra de ouro no rodapé do rail
    ctx.strokeStyle = P.gold; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(m, H - 64); ctx.lineTo(m + cw, H - 64); ctx.stroke();
    ctx.fillStyle = P.inkLo; ctx.font = `italic 400 12.5px ${U.SERIF}`;
    ctx.fillText("Reconhecimento sem reciprocidade:", m, H - 42);
    ctx.fillText("a figura é mulher; o poder, não.", m, H - 26);
  }

  cv.addEventListener("click", ev => {
    const r = cv.getBoundingClientRect();
    const x = ev.clientX - r.left, y = ev.clientY - r.top;
    const hit = hits.find(h => x >= h.x && x <= h.x + h.w && y >= h.y && y <= h.y + h.h);
    if (hit) U.showDrill({ ...hit.drill, x: ev.clientX, y: ev.clientY });
  });

  window.RAIL = { set(win) { if (WINS[win] && win !== cur) { cur = win; draw(); } }, redraw: draw };
  draw();
})();
