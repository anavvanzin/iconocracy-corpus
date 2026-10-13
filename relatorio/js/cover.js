// Capa · estado A — recursão infinita da figura alegórica.
// O que recursa é o OBJETO: a personificação feminina (Iustitia e suas variantes de
// atributo), que o zoom contínuo reduz a uma célula de um array maior de figuras —
// o atlas do corpus. Oito variantes de anel por posição, invariantes por nível,
// garantem o loop sem costura (auto-similaridade 3×).
(() => {
  const cv = document.getElementById("cover-canvas");
  if (!cv) return;
  const medal = document.querySelector(".cover-3d");
  const hasMedal = () => medal?.dataset.state === "ready" && getComputedStyle(medal).display !== "none";
  addEventListener("cover3dstate", () => { if (U.REDUCE) draw(0.58); });
  const { fit, ctx } = U.bindCanvas(cv);
  const P = U.PAL;
  let V = fit();
  addEventListener("resize", () => { V = fit(); if (U.REDUCE) draw(0.58); });

  // ── Figura alegórica em linha (tintas do sistema: ink + gold + lacre) ──
  // variant: 0=Iustitia(hero) · 1 tocha · 2 cornucópia · 3 âncora · 4 fasces
  //          5 espelho · 6 orbe/coroa (Europa) · 7 lança+escudo · 8 palma+livro
  function drawFigure(px, py, cs, variant, alpha) {
    if (alpha <= 0.01 || cs < 4) return;
    const s = cs;
    const lw = Math.max(0.8, s * 0.011);
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.lineWidth = lw; ctx.lineCap = "round"; ctx.lineJoin = "round";
    const baseY = py + 0.44 * s, headY = py - 0.28 * s, headR = 0.055 * s;
    const shY = headY + headR + 0.035 * s;               // ombros
    const shL = px - 0.085 * s, shR = px + 0.085 * s;

    // pedestal
    ctx.strokeStyle = P.ink;
    ctx.beginPath();
    ctx.moveTo(px - 0.20 * s, baseY + 0.045 * s); ctx.lineTo(px + 0.20 * s, baseY + 0.045 * s);
    ctx.moveTo(px - 0.17 * s, baseY + 0.045 * s); ctx.lineTo(px - 0.17 * s, baseY + 0.005 * s);
    ctx.moveTo(px + 0.17 * s, baseY + 0.045 * s); ctx.lineTo(px + 0.17 * s, baseY + 0.005 * s);
    ctx.moveTo(px - 0.20 * s, baseY + 0.005 * s); ctx.lineTo(px + 0.20 * s, baseY + 0.005 * s);
    ctx.stroke();

    // manto (trapézio flamejante) + dobras
    ctx.beginPath();
    ctx.moveTo(shL, shY);
    ctx.quadraticCurveTo(px - 0.11 * s, py + 0.10 * s, px - 0.165 * s, baseY);
    ctx.lineTo(px + 0.165 * s, baseY);
    ctx.quadraticCurveTo(px + 0.11 * s, py + 0.10 * s, shR, shY);
    ctx.stroke();
    ctx.globalAlpha = alpha * 0.55;
    ctx.beginPath();
    ctx.moveTo(px - 0.045 * s, shY + 0.03 * s); ctx.quadraticCurveTo(px - 0.06 * s, py + 0.16 * s, px - 0.075 * s, baseY);
    ctx.moveTo(px + 0.045 * s, shY + 0.03 * s); ctx.quadraticCurveTo(px + 0.06 * s, py + 0.16 * s, px + 0.075 * s, baseY);
    ctx.stroke();
    ctx.globalAlpha = alpha;

    // cabeça + cabelo
    ctx.beginPath(); ctx.arc(px, headY, headR, 0, U.TAU); ctx.stroke();
    ctx.beginPath(); ctx.arc(px, headY - headR * 0.25, headR * 1.25, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke();

    const hand = (hx, hy, fromX) => { ctx.beginPath(); ctx.moveTo(fromX, shY); ctx.quadraticCurveTo((fromX + hx) / 2, (shY + hy) / 2 - 0.02 * s, hx, hy); ctx.stroke(); };

    if (variant === 0) {
      // IUSTITIA — venda em lacre, balança à esquerda, espada à direita
      const hxL = px - 0.21 * s, hyL = headY - 0.01 * s;
      const hxR = px + 0.17 * s, hyR = headY + 0.10 * s;
      hand(hxL, hyL, shL); hand(hxR, hyR, shR);
      // balança
      ctx.strokeStyle = P.gold;
      const beamY = hyL - 0.16 * s;
      ctx.beginPath();
      ctx.moveTo(hxL, hyL); ctx.lineTo(hxL, beamY);
      ctx.moveTo(hxL - 0.10 * s, beamY); ctx.lineTo(hxL + 0.10 * s, beamY);
      for (const sgn of [-1, 1]) {
        const bx = hxL + sgn * 0.10 * s;
        ctx.moveTo(bx, beamY); ctx.lineTo(bx - 0.028 * s, beamY + 0.075 * s);
        ctx.moveTo(bx, beamY); ctx.lineTo(bx + 0.028 * s, beamY + 0.075 * s);
        ctx.moveTo(bx - 0.028 * s, beamY + 0.075 * s); ctx.quadraticCurveTo(bx, beamY + 0.105 * s, bx + 0.028 * s, beamY + 0.075 * s);
      }
      ctx.stroke();
      // espada (lâmina para cima)
      ctx.strokeStyle = P.ink;
      ctx.beginPath();
      ctx.moveTo(hxR, hyR); ctx.lineTo(hxR, hyR - 0.24 * s);
      ctx.moveTo(hxR - 0.035 * s, hyR - 0.03 * s); ctx.lineTo(hxR + 0.035 * s, hyR - 0.03 * s);
      ctx.stroke();
      // venda — lacre, o atributo-tese
      if (cs > 26) {
        ctx.fillStyle = P.lacre; ctx.globalAlpha = alpha * 0.92;
        ctx.fillRect(px - headR * 1.05, headY - headR * 0.28, headR * 2.1, headR * 0.55);
      }
    } else {
      const hx = px + 0.18 * s, hy = headY + (variant % 2 ? -0.06 : 0.06) * s;
      hand(hx, hy, shR);
      hand(px - 0.16 * s, shY + 0.14 * s, shL); // braço esquerdo cai ao longo do corpo
      ctx.strokeStyle = P.gold;
      ctx.beginPath();
      if (variant === 1) {           // tocha
        ctx.moveTo(hx, hy); ctx.lineTo(hx, hy - 0.17 * s);
        ctx.moveTo(hx, hy - 0.17 * s);
        ctx.quadraticCurveTo(hx - 0.045 * s, hy - 0.21 * s, hx, hy - 0.26 * s);
        ctx.quadraticCurveTo(hx + 0.045 * s, hy - 0.21 * s, hx, hy - 0.17 * s);
      } else if (variant === 2) {    // cornucópia
        ctx.moveTo(hx, hy); ctx.quadraticCurveTo(hx + 0.10 * s, hy - 0.05 * s, hx + 0.07 * s, hy - 0.14 * s);
        ctx.moveTo(hx, hy); ctx.quadraticCurveTo(hx + 0.03 * s, hy - 0.10 * s, hx + 0.07 * s, hy - 0.14 * s);
      } else if (variant === 3) {    // âncora
        ctx.moveTo(hx, hy - 0.14 * s); ctx.lineTo(hx, hy + 0.10 * s);
        ctx.moveTo(hx, hy - 0.16 * s); ctx.arc(hx, hy - 0.16 * s, 0.022 * s, 0, U.TAU);
        ctx.moveTo(hx - 0.06 * s, hy - 0.02 * s); ctx.lineTo(hx + 0.06 * s, hy - 0.02 * s);
        ctx.moveTo(hx - 0.07 * s, hy + 0.02 * s); ctx.quadraticCurveTo(hx, hy + 0.13 * s, hx + 0.07 * s, hy + 0.02 * s);
      } else if (variant === 4) {    // fasces
        for (let i = -2; i <= 2; i++) { ctx.moveTo(hx + i * 0.018 * s, hy - 0.16 * s); ctx.lineTo(hx + i * 0.018 * s, hy + 0.12 * s); }
        ctx.moveTo(hx - 0.05 * s, hy - 0.04 * s); ctx.lineTo(hx + 0.05 * s, hy - 0.04 * s);
        ctx.moveTo(hx - 0.05 * s, hy + 0.03 * s); ctx.lineTo(hx + 0.05 * s, hy + 0.03 * s);
      } else if (variant === 5) {    // espelho (Prudência/Veritas)
        ctx.moveTo(hx, hy); ctx.lineTo(hx, hy - 0.10 * s);
        ctx.moveTo(hx, hy - 0.16 * s); ctx.arc(hx, hy - 0.16 * s, 0.055 * s, 0, U.TAU);
      } else if (variant === 6) {    // orbe + coroa (Europa régia)
        ctx.moveTo(hx, hy); ctx.lineTo(hx, hy - 0.06 * s);
        ctx.moveTo(hx, hy - 0.11 * s); ctx.arc(hx, hy - 0.11 * s, 0.05 * s, 0, U.TAU);
        ctx.moveTo(hx, hy - 0.16 * s); ctx.lineTo(hx, hy - 0.21 * s);
        ctx.moveTo(hx - 0.025 * s, hy - 0.185 * s); ctx.lineTo(hx + 0.025 * s, hy - 0.185 * s);
        ctx.stroke();
        ctx.beginPath();             // coroa
        ctx.moveTo(px - 0.05 * s, headY - headR * 1.15); ctx.lineTo(px - 0.05 * s, headY - headR * 1.7);
        ctx.lineTo(px - 0.02 * s, headY - headR * 1.3); ctx.lineTo(px, headY - headR * 1.8);
        ctx.lineTo(px + 0.02 * s, headY - headR * 1.3); ctx.lineTo(px + 0.05 * s, headY - headR * 1.7);
        ctx.lineTo(px + 0.05 * s, headY - headR * 1.15);
      } else if (variant === 7) {    // lança + escudo
        ctx.moveTo(hx, hy - 0.30 * s); ctx.lineTo(hx, hy + 0.16 * s);
        ctx.stroke();
        ctx.beginPath();
        ctx.ellipse(px - 0.19 * s, py + 0.02 * s, 0.075 * s, 0.10 * s, 0, 0, U.TAU);
      } else {                       // palma + livro
        ctx.moveTo(hx, hy); ctx.quadraticCurveTo(hx + 0.02 * s, hy - 0.16 * s, hx + 0.07 * s, hy - 0.20 * s);
        for (let i = 0; i < 3; i++) {
          ctx.moveTo(hx + 0.012 * s, hy - 0.06 * s - i * 0.05 * s);
          ctx.quadraticCurveTo(hx - 0.03 * s, hy - 0.09 * s - i * 0.05 * s, hx - 0.045 * s, hy - 0.10 * s - i * 0.05 * s);
        }
        ctx.stroke();
        ctx.strokeStyle = P.ink; ctx.beginPath();
        ctx.rect(px - 0.24 * s, shY + 0.16 * s, 0.11 * s, 0.08 * s);
      }
      ctx.stroke();
    }
    ctx.restore();
  }

  // Anel da grade 3×3 em ordem BFS (ortogonais primeiro), variante por posição
  const RING = [
    { dx: 0, dy: -1, v: 1 }, { dx: -1, dy: 0, v: 5 }, { dx: 1, dy: 0, v: 2 }, { dx: 0, dy: 1, v: 3 },
    { dx: -1, dy: -1, v: 6 }, { dx: 1, dy: -1, v: 7 }, { dx: -1, dy: 1, v: 8 }, { dx: 1, dy: 1, v: 4 },
  ];

  function draw(t) {
    const { w: W, h: H } = V;
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = P.paper; ctx.fillRect(0, 0, W, H);

    const narrow = W < 760;
    const cx = narrow ? W * 0.5 : (W < 1050 ? W * 0.72 : W - 182);
    const cy = H * 0.52;
    const S0 = Math.min(H * 0.80, W * 0.62); // tamanho da figura-heroína em t=0
    const u = S0 / Math.pow(3, t);          // tamanho de tela da célula-mundo unitária

    // níveis: de fora para dentro
    for (let n = 8; n >= 1; n--) {
      const cellW = Math.pow(3, n - 1);     // célula do anel (unidades-mundo)
      const gridW = cellW * 3;
      const gridPx = gridW * u;
      if (gridPx > Math.max(W, H) * 2.6) continue;
      const cellPx = cellW * u;
      if (cellPx < 5) continue;
      // nascimento do anel: entra quando a grade encolhe abaixo de ~2.35×S0
      const birth = U.clamp((2.35 * S0 - gridPx) / (1.15 * S0), 0, 1);
      if (birth <= 0) continue;
      for (let o = 0; o < RING.length; o++) {
        const r = RING[o];
        const a = U.clamp(birth * 1.7 - o * 0.085, 0, 1);
        if (a <= 0) continue;
        const px = cx + r.dx * cellW * u;
        const py = cy + r.dy * cellW * u;
        // flash de lacre no nascimento
        if (a < 1 && cellPx > 30) {
          ctx.save(); ctx.globalAlpha = (1 - a) * 0.85;
          ctx.strokeStyle = P.lacre; ctx.lineWidth = Math.max(1, cellPx * 0.012);
          ctx.strokeRect(px - cellPx / 2, py - cellPx / 2, cellPx, cellPx);
          ctx.restore();
        }
        drawFigure(px, py, cellPx * 0.96, r.v, a);
      }
    }
    // nível 0: a heroína — Iustitia (onde o medalhão 3D está visível, o centro é dele)
    if (!hasMedal() || narrow) drawFigure(cx, cy, u * 0.96, 0, 1);

    // viewfinder dourado: a moldura que acompanha o átomo encolhendo a célula
    if (u > 40) {
      const vfA = 0.55 + 0.40 * Math.cos(U.TAU * t);
      const m = u * 0.52, L = Math.max(14, u * 0.10);
      ctx.save(); ctx.globalAlpha = vfA; ctx.strokeStyle = P.gold; ctx.lineWidth = 1.6;
      for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
        ctx.beginPath();
        ctx.moveTo(cx + sx * m, cy + sy * m - sy * L); ctx.lineTo(cx + sx * m, cy + sy * m); ctx.lineTo(cx + sx * m - sx * L, cy + sy * m);
        ctx.stroke();
      }
      ctx.restore();
    }

    // véu de leitura sobre a coluna de texto
    if (!narrow) {
      const g = ctx.createLinearGradient(0, 0, W * 0.62, 0);
      g.addColorStop(0, "rgba(239,229,207,0.97)");
      g.addColorStop(0.62, "rgba(239,229,207,0.93)");
      g.addColorStop(1, "rgba(239,229,207,0)");
      ctx.fillStyle = g; ctx.fillRect(0, 0, W * 0.62, H);
    } else {
      // tela estreita: o atlas inteiro recua para trás da prosa —
      // a recursão continua viva, mas como fantasma sob o papel
      ctx.fillStyle = "rgba(239,229,207,0.90)"; ctx.fillRect(0, 0, W, H);
      const g2 = ctx.createLinearGradient(0, 0, 0, H);
      g2.addColorStop(0, "rgba(239,229,207,0.35)");
      g2.addColorStop(0.45, "rgba(239,229,207,0.75)");
      g2.addColorStop(1, "rgba(239,229,207,0.95)");
      ctx.fillStyle = g2; ctx.fillRect(0, 0, W, H);
    }

    // legenda de fase (alterna com o zoom, sem flicker)
    const capA = t < 0.5 ? 1 : 0, ph = t < 0.5 ? t * 2 : (t - 0.5) * 2;
    const fade = U.clamp(Math.min(ph, 1 - ph) * 4, 0, 1);
    ctx.save();
    ctx.globalAlpha = Math.max(0.28, fade);
    ctx.font = `700 10px ${U.MONO}`; ctx.textAlign = "right";
    ctx.fillStyle = P.inkLo;
    const cap = capA ? "CAPA A · RECURSÃO — CADA FIGURA É UMA CÉLULA DE UM ATLAS MAIOR"
                     : "O ATLAS DO CORPUS · 336 ITENS · 17 PAÍSES · 1239–2021";
    ctx.fillText(cap, W - 28, H - 26);
    ctx.restore();
  }

  if (U.REDUCE) { requestAnimationFrame(() => { V = fit(); draw(0.58); }); return; }
  const LOOP = 15000;
  let start = null;
  function tick(ts) {
    if (start == null) start = ts;
    draw(((ts - start) % LOOP) / LOOP);
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
