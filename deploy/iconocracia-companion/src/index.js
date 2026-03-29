import DATA from "./scout-data.json";

const SCOUT_DATA = DATA;

function renderCard(c) {
  const regime = (c.regime || "").toUpperCase();
  const regimeClass = regime === "MILITAR" ? "militar" : regime === "FUNDACIONAL" ? "fundacional" : "normativo";
  const isNeg = (c.tipo || "").includes("controle");
  return `
  <div class="card ${regimeClass}${isNeg ? " negative" : ""}">
    <div class="card-header">
      <span class="card-id">${c.id}</span>
      <div>
        ${c.confianca ? `<span class="conf conf-${c.confianca}">${c.confianca}</span>` : ""}
        <span class="card-regime regime-${regime}">${regime || "?"}</span>
      </div>
    </div>
    <div class="card-title">${c.titulo || ""}</div>
    <div class="card-meta">
      <span>${c.pais || ""} | ${c.data_estimada || ""}</span>
      <span>${c.suporte || ""}</span>
    </div>
    ${c.justificativa ? `<div class="card-body">${c.justificativa}</div>` : ""}
    ${c.endurecimento ? `<div class="card-end"><strong>ENDURECIMENTO:</strong> ${c.endurecimento}</div>` : ""}
    ${c.url && c.url !== "null" ? `<a class="card-link" href="${c.url}" target="_blank" rel="noopener">Ver no acervo &rarr;</a>` : ""}
    ${isNeg ? `<div class="card-note">Controle negativo — documenta ausencia de alegoria</div>` : ""}
  </div>`;
}

function renderZW(z) {
  return `
  <div class="zw-card">
    <div class="card-header">
      <span class="card-id">${z.id}</span>
      <span class="card-meta">${(z.pais || "").toString().replace(/[\[\]]/g, "")} | ${z.periodo || ""}</span>
    </div>
    <div class="card-title">${z.titulo || ""}</div>
  </div>`;
}

function renderTheory(t) {
  return `
  <div class="theory-card">
    <div class="theory-name">${t.name}</div>
    <div class="theory-desc">${t.desc}</div>
  </div>`;
}

function renderPage() {
  const d = SCOUT_DATA;
  const countries = [...new Set(d.candidates.map(c => (c.pais || "").replace(/[\[\]]/g, "").trim()))].filter(Boolean);
  const regimes = { MILITAR: 0, NORMATIVO: 0, FUNDACIONAL: 0 };
  d.candidates.forEach(c => { const r = (c.regime || "").toUpperCase(); if (regimes[r] !== undefined) regimes[r]++; });

  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CORPUS SCOUT — Iconocracia</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,serif;background:#0f0f0f;color:#e0ddd5;line-height:1.7}
.header{background:#1a1a1a;border-bottom:2px solid #c9a84c;padding:2.5rem 1rem;text-align:center}
.header h1{font-size:1.8rem;color:#c9a84c;letter-spacing:.15em;text-transform:uppercase}
.header p{color:#888;font-style:italic;margin-top:.5rem;font-size:.9rem;max-width:600px;margin-left:auto;margin-right:auto}
.stats{display:flex;justify-content:center;gap:2.5rem;margin-top:1.5rem;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:2rem;color:#c9a84c;font-weight:bold}
.stat-label{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#666}
nav{background:#151515;padding:.75rem 1rem;display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;border-bottom:1px solid #222;position:sticky;top:0;z-index:10}
nav a{color:#888;text-decoration:none;font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;padding:.3rem .8rem;border:1px solid transparent;transition:all .2s}
nav a:hover,nav a.active{color:#c9a84c;border-color:#c9a84c33}
.container{max-width:900px;margin:0 auto;padding:2rem 1rem}
.section-title{font-size:1.1rem;color:#c9a84c;text-transform:uppercase;letter-spacing:.15em;border-bottom:1px solid #333;padding-bottom:.5rem;margin:2.5rem 0 1.5rem}
.card{background:#1a1a1a;border:1px solid #2a2a2a;border-left:4px solid #059669;margin-bottom:1.2rem;padding:1.5rem;transition:border-color .2s}
.card:hover{border-color:#c9a84c}
.card.militar{border-left-color:#dc2626}
.card.normativo{border-left-color:#059669}
.card.fundacional{border-left-color:#2563eb}
.card.negative{border-left-style:dashed;opacity:.85}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem;gap:.5rem}
.card-id{font-family:monospace;font-size:.8rem;color:#c9a84c}
.card-regime{font-size:.65rem;padding:.2rem .5rem;border-radius:2px;text-transform:uppercase;letter-spacing:.1em;font-weight:bold}
.regime-MILITAR{background:#dc262622;color:#f87171;border:1px solid #dc262644}
.regime-NORMATIVO{background:#05966922;color:#6ee7b7;border:1px solid #05966944}
.regime-FUNDACIONAL{background:#2563eb22;color:#93c5fd;border:1px solid #2563eb44}
.conf{font-size:.6rem;padding:.15rem .4rem;margin-right:.3rem;border-radius:2px;text-transform:uppercase}
.conf-alto{color:#6ee7b7;border:1px solid #05966944}
.conf-medio{color:#fbbf24;border:1px solid #f59e0b44}
.conf-baixo{color:#f87171;border:1px solid #dc262644}
.card-title{font-size:1rem;color:#e0ddd5;margin-bottom:.4rem}
.card-meta{font-size:.78rem;color:#888;margin-bottom:.5rem}
.card-meta span{margin-right:1rem}
.card-body{font-size:.85rem;color:#aaa;line-height:1.6}
.card-end{font-size:.8rem;margin-top:.6rem;padding:.5rem .75rem;background:#111;border-left:2px solid #c9a84c}
.card-end strong{color:#c9a84c}
.card-link{display:inline-block;margin-top:.6rem;font-size:.78rem;color:#c9a84c;text-decoration:none}
.card-link:hover{text-decoration:underline}
.card-note{font-size:.72rem;color:#f87171;font-style:italic;margin-top:.5rem}
.zw-card{background:#1a1a1a;border:1px solid #c9a84c33;margin-bottom:1.2rem;padding:1.5rem}
.zw-card .card-title{color:#c9a84c;font-size:.95rem}
.theory-card{background:#1a1a1a;border:1px solid #2a2a2a;padding:1rem 1.5rem;margin-bottom:.8rem}
.theory-name{color:#c9a84c;font-weight:bold;font-size:.9rem;margin-bottom:.3rem}
.theory-desc{font-size:.82rem;color:#aaa}
.footer{text-align:center;padding:2rem;color:#444;font-size:.72rem;border-top:1px solid #222;margin-top:3rem}
a{color:#c9a84c}
@media(max-width:600px){.stats{gap:1rem}.card{padding:1rem}.header h1{font-size:1.3rem}}
</style>
</head>
<body>
<div class="header">
  <h1>Corpus Scout</h1>
  <p>${d.thesis}</p>
  <div class="stats">
    <div class="stat"><div class="stat-num">${d.total_candidates}</div><div class="stat-label">Candidatos</div></div>
    <div class="stat"><div class="stat-num">${d.total_zwischenraume}</div><div class="stat-label">Zwischenraume</div></div>
    <div class="stat"><div class="stat-num">${countries.length}</div><div class="stat-label">Paises</div></div>
    <div class="stat"><div class="stat-num">${d.theoretical_contributions.length}</div><div class="stat-label">Contribuicoes teoricas</div></div>
  </div>
</div>
<nav>
  <a href="#candidatos">Candidatos</a>
  <a href="#zwischenraume">Zwischenraume</a>
  <a href="#teoria">Teoria</a>
</nav>
<div class="container">
  <div class="section-title" id="candidatos">Candidatos ao Corpus (${d.total_candidates})</div>
  ${d.candidates.map(renderCard).join("")}
  <div class="section-title" id="zwischenraume">Zwischenraume — Paineis Comparativos (${d.total_zwischenraume})</div>
  ${d.zwischenraume.map(renderZW).join("")}
  <div class="section-title" id="teoria">Contribuicoes Teoricas Emergentes</div>
  ${d.theoretical_contributions.map(renderTheory).join("")}
</div>
<div class="footer">
  CORPUS SCOUT — PPGD/UFSC — ${d.session}<br>
  21 candidatos · 8 paineis · 8 conceitos · 7 paises<br>
  Skill: <code>corpus-scout</code> · Claude Code
</div>
</body>
</html>`;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/diary") {
      const headers = { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, PUT, OPTIONS" };
      if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
      if (request.method === "GET") { const data = await env.DIARY_KV.get("diary", "text"); return new Response(data || "[]", { headers }); }
      if (request.method === "PUT") { const body = await request.text(); await env.DIARY_KV.put("diary", body); return new Response(JSON.stringify({ ok: true }), { headers }); }
      return new Response("Method not allowed", { status: 405, headers });
    }

    if (url.pathname === "/api/scout") {
      return new Response(JSON.stringify(SCOUT_DATA, null, 2), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }

    if (url.pathname === "/scout") {
      return new Response(renderPage(), {
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
