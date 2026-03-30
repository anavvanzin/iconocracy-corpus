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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{--parchment:#F5F0E8;--ink:#1A1A2E;--sepia:#8B7355;--bordeaux:#6B2D3E;--navy:#16213E;--gold:#C4A265;--cream:#FAF7F0;--warmGray:#9B8E82;--lightSepia:#D4C5A9;--rust:#A0522D}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Cormorant Garamond',Georgia,serif;background:var(--parchment);color:var(--ink);line-height:1.7}
.mono{font-family:'IBM Plex Mono',monospace}
.header{background:var(--navy);border-bottom:3px solid var(--gold);padding:2.5rem 1rem;text-align:center}
.header .back{display:inline-block;margin-bottom:1rem;font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--lightSepia);text-decoration:none;letter-spacing:.08em;border:1px solid rgba(212,197,169,.3);padding:.25rem .75rem;border-radius:2px;transition:all .2s}
.header .back:hover{color:var(--gold);border-color:var(--gold)}
.header h1{font-size:1.8rem;color:var(--gold);letter-spacing:.15em;text-transform:uppercase}
.header p{color:var(--warmGray);font-style:italic;margin-top:.5rem;font-size:.9rem;max-width:600px;margin-left:auto;margin-right:auto}
.stats{display:flex;justify-content:center;gap:2.5rem;margin-top:1.5rem;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:2rem;color:var(--gold);font-weight:bold}
.stat-label{font-family:'IBM Plex Mono',monospace;font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:var(--warmGray);margin-top:.2rem}
nav{background:var(--cream);padding:.75rem 1rem;display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;border-bottom:1px solid var(--lightSepia);position:sticky;top:0;z-index:10}
nav a{color:var(--warmGray);text-decoration:none;font-family:'IBM Plex Mono',monospace;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;padding:.3rem .8rem;border:1px solid transparent;border-radius:2px;transition:all .2s}
nav a:hover,nav a.active{color:var(--bordeaux);border-color:rgba(107,45,62,.3);background:rgba(107,45,62,.05)}
.container{max-width:900px;margin:0 auto;padding:2rem 1rem}
.section-title{font-family:'IBM Plex Mono',monospace;font-size:.85rem;color:var(--gold);text-transform:uppercase;letter-spacing:.15em;border-bottom:1px solid var(--lightSepia);padding-bottom:.5rem;margin:2.5rem 0 1.5rem}
.card{background:var(--cream);border:1px solid var(--lightSepia);border-left:4px solid var(--sepia);margin-bottom:1.2rem;padding:1.5rem;border-radius:2px;transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--gold);box-shadow:0 2px 12px rgba(196,162,101,.12)}
.card.militar{border-left-color:var(--bordeaux)}
.card.normativo{border-left-color:var(--sepia)}
.card.fundacional{border-left-color:var(--navy)}
.card.negative{border-left-style:dashed;opacity:.8}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem;gap:.5rem}
.card-id{font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:var(--gold)}
.card-regime{font-family:'IBM Plex Mono',monospace;font-size:.62rem;padding:.2rem .6rem;border-radius:2px;text-transform:uppercase;letter-spacing:.1em;font-weight:500}
.regime-MILITAR{background:rgba(107,45,62,.1);color:var(--bordeaux);border:1px solid rgba(107,45,62,.25)}
.regime-NORMATIVO{background:rgba(139,115,85,.1);color:var(--sepia);border:1px solid rgba(139,115,85,.25)}
.regime-FUNDACIONAL{background:rgba(22,33,62,.1);color:var(--navy);border:1px solid rgba(22,33,62,.25)}
.conf{font-family:'IBM Plex Mono',monospace;font-size:.6rem;padding:.15rem .45rem;margin-right:.3rem;border-radius:2px;text-transform:uppercase}
.conf-alto{color:var(--sepia);border:1px solid rgba(139,115,85,.3)}
.conf-medio{color:var(--gold);border:1px solid rgba(196,162,101,.3)}
.conf-baixo{color:var(--bordeaux);border:1px solid rgba(107,45,62,.3)}
.card-title{font-size:1rem;color:var(--ink);font-weight:600;margin-bottom:.4rem}
.card-meta{font-family:'IBM Plex Mono',monospace;font-size:.74rem;color:var(--warmGray);margin-bottom:.5rem}
.card-meta span{margin-right:1rem}
.card-body{font-size:.88rem;color:var(--sepia);line-height:1.7;font-style:italic}
.card-end{font-size:.82rem;margin-top:.6rem;padding:.5rem .75rem;background:rgba(196,162,101,.08);border-left:2px solid var(--gold);border-radius:0 2px 2px 0}
.card-end strong{color:var(--gold)}
.card-link{display:inline-block;margin-top:.6rem;font-family:'IBM Plex Mono',monospace;font-size:.74rem;color:var(--bordeaux);text-decoration:none;letter-spacing:.04em}
.card-link:hover{text-decoration:underline;color:var(--gold)}
.card-note{font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:var(--bordeaux);font-style:italic;margin-top:.5rem}
.zw-card{background:var(--cream);border:1px solid rgba(196,162,101,.35);margin-bottom:1.2rem;padding:1.5rem;border-radius:2px}
.zw-card .card-title{color:var(--gold);font-size:.95rem;font-weight:600}
.theory-card{background:var(--cream);border:1px solid var(--lightSepia);border-left:3px solid var(--gold);padding:1rem 1.5rem;margin-bottom:.8rem;border-radius:2px}
.theory-name{color:var(--bordeaux);font-weight:700;font-size:.95rem;margin-bottom:.3rem}
.theory-desc{font-size:.86rem;color:var(--sepia);line-height:1.6}
.footer{background:var(--navy);text-align:center;padding:1.5rem 2rem;font-family:'IBM Plex Mono',monospace;color:var(--lightSepia);font-size:.7rem;letter-spacing:.1em;border-top:2px solid var(--gold);margin-top:3rem}
a{color:var(--bordeaux)}
@media(max-width:600px){.stats{gap:1rem}.card{padding:1rem}.header h1{font-size:1.3rem}}
</style>
</head>
<body>
<div class="header">
  <a href="/" class="back">← Companheiro de Pesquisa</a>
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
  CORPUS SCOUT · PPGD/UFSC · ${d.session}<br>
  ${d.total_candidates} candidatos · ${d.total_zwischenraume} painéis · ${d.theoretical_contributions.length} conceitos
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
