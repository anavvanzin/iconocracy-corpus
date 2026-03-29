const SCOUT_DATA = {
  session: "2026-03-28",
  title: "CORPUS SCOUT — Sessao de Pesquisa Iconografica",
  thesis: "ICONOCRACY: Alegoria Feminina na Historia da Cultura Juridica (Sec. XIX-XX)",
  total_candidates: 6,
  candidates: [
    {
      id: "SCOUT-029a",
      titulo: "Notgeld Bielefeld 500 Mark (Stadtsparkasse) — Frau mit Geldsacken",
      acervo: "Numista / Stadtsparkasse Bielefeld",
      url: "https://en.numista.com/274388",
      data_estimada: "1923",
      pais: "DE",
      suporte: "papel-moeda",
      motivo_alegorico: "Alegoria satirica da ganancia / Anti-Republica",
      regime: "NORMATIVO",
      confianca: "alto",
      endurecimento: "nao — anti-ENDURECIMENTO radical",
      justificativa: "Nota de 500 Mark em seda. Mulher segurando sacos de dinheiro contra o peito, seios expostos. Citacao biblica de Mateus 23:17. O proprio meio de troca denuncia a corrupcao do sistema monetario.",
      atributos: ["postura frontal", "seios expostos", "sacos de dinheiro"]
    },
    {
      id: "SCOUT-032",
      titulo: "Medaille K. Goetz — Die Wacht an der Ruhr / Die Weisse Schmach",
      acervo: "Karl Goetz Archive / US Naval History and Heritage Command",
      url: "https://karlgoetz.com/ImageDetail.aspx?idImage=223",
      data_estimada: "1923",
      pais: "DE",
      suporte: "medalha (bronze)",
      motivo_alegorico: "Marianne (weaponizada/satirizada)",
      regime: "MILITAR",
      confianca: "alto",
      endurecimento: "sim — ENDURECIMENTO por grotesquizacao hostil",
      justificativa: "Medalha satirica. Anverso: Marianne com barrete frigio e chicote. Reverso: Marianne estrangulando homem alemao. Denuncia a ocupacao do Ruhr (1923).",
      atributos: ["barrete frigio", "chicote", "estrangulamento", "postura frontal"]
    },
    {
      id: "SCOUT-033",
      titulo: "Selo Postal Semeuse lignee — Oscar Roty",
      acervo: "Musee d'Orsay / Colecoes filatelicas",
      url: "https://www.musee-orsay.fr/en/artworks/la-semeuse-55299",
      data_estimada: "1903",
      pais: "FR",
      suporte: "selo postal",
      motivo_alegorico: "Marianne / La Semeuse",
      regime: "NORMATIVO",
      confianca: "alto",
      endurecimento: "nao — anti-ENDURECIMENTO deliberado",
      justificativa: "Mulher caminha semeando graos contra sol nascente, barrete frigio, vestimenta esvoacante. Serialidade maxima (35 anos, milhoes de copias) sem rigidez formal. Criticada por ser 'pacifica demais' comparada a Germania.",
      atributos: ["barrete frigio", "vestimenta esvoacante", "postura dinamica/perfil", "saco de sementes"]
    },
    {
      id: "SCOUT-034",
      titulo: "Medaille K. Goetz — Die Schwarze Schmach",
      acervo: "Yale University Art Gallery",
      url: "https://artgallery.yale.edu/collections/objects/165690",
      data_estimada: "1920",
      pais: "DE",
      suporte: "medalha (bronze)",
      motivo_alegorico: "A mulher alema (vitima) / Anti-Marianne",
      regime: "MILITAR",
      confianca: "alto",
      endurecimento: "sim — ENDURECIMENTO por vitimizacao",
      justificativa: "Propaganda contra tropas coloniais francesas no Reno. Mulher alema nua acorrentada a poste com capacete, bebe aos pes. Interseccao genero/raca na iconocracia.",
      atributos: ["nudez forcada", "correntes", "capacete militar", "bebe"],
      nota: "Conteudo racista explicito — inclusao justificada analiticamente"
    },
    {
      id: "SCOUT-029",
      titulo: "Notgeld — Grossgeldscheine inflacionarios com alegoria feminina",
      acervo: "Notgeld.com / Grabowski Katalog",
      url: "https://notgeld.com/notgeld-articles/inflation-1923/",
      data_estimada: "1922-1923",
      pais: "DE",
      suporte: "papel-moeda",
      motivo_alegorico: "Republik / Germania (desmilitarizada)",
      regime: "NORMATIVO",
      confianca: "medio",
      endurecimento: "incerto — ENDURECIMENTO fantasma: a forma persiste enquanto a substancia desaparece",
      justificativa: "Grossgeldscheine reutilizam vinhetas alegoricas do periodo imperial em denominacoes absurdas (milhoes, bilhoes de Marcos). A serialidade atinge apice patologico.",
      atributos: ["toga/vestimenta classica", "escudo/brasao", "postura frontal"]
    },
    {
      id: "SCOUT-030",
      titulo: "Notgeld satirico — Marianne no Ruhr (Serienscheine anti-franceses)",
      acervo: "University of Chicago Special Collections",
      url: "https://www.lib.uchicago.edu/e/scrc/findingaids/view.php?eadid=ICU.SPCL.NOTGELD",
      data_estimada: "1923",
      pais: "DE",
      suporte: "papel-moeda",
      motivo_alegorico: "Marianne / Francia (satirizada)",
      regime: "MILITAR",
      confianca: "alto",
      endurecimento: "sim — ENDURECIMENTO invertido/hostil",
      justificativa: "Notgeld com Marianne levantando saia para apanhar dinheiro, barrete frigio identificando-a como Franca. O meio de troca torna-se arma de propaganda contra o ocupante.",
      atributos: ["barrete frigio", "saia levantada", "dinheiro", "postura satirica"]
    }
  ],
  zwischenraume: [
    {
      id: "SCOUT-ZW-09",
      titulo: "Painel IX — A DESINTEGRACAO DO CORPO NORMATIVO: Notgeld e o Anti-ENDURECIMENTO (1922-1923)",
      pais: ["DE", "FR"],
      periodo: "1922-1923",
      polos: "Grossgeldscheine (ENDURECIMENTO fantasma) x Serienscheine satiricos (Anti-ENDURECIMENTO)",
      tese: "Tres destinos do corpo alegorico pos-colapso: persistencia fantasma, reversao satirica, weaponizacao. O ENDURECIMENTO depende de estabilidade institucional."
    },
    {
      id: "SCOUT-ZW-10",
      titulo: "Painel X — O DUPLO CORPO DE MARIANNE: Piastre de Commerce (1885) x Medalha Goetz (1923)",
      pais: ["FR", "DE"],
      periodo: "1885-1923",
      polos: "Marianne colonial (guardia) x Marianne satirizada (assassina)",
      tese: "A alegoria feminina e vulneravel a captura transnacional. O ENDURECIMENTO muda de agente: o Estado endurece sua alegoria; o inimigo a endurece contra ela."
    },
    {
      id: "SCOUT-ZW-11",
      titulo: "Painel XI — O CICLO DE VIDA DE MARIANNE: Semeuse (1903) -> Piastre (1885) -> Goetz (1923)",
      pais: ["FR", "DE"],
      periodo: "1885-1923",
      polos: "Semeuse (fluida/NORMATIVO) -> Piastre (petrificada/MILITAR) -> Goetz (grotesca/MILITAR)",
      tese: "A alegoria feminina nao tem morfologia intrinseca — e um recipiente vazio que a cultura juridica preenche. O barrete frigio permanece constante; tudo o mais muda. ENDURECIMENTO seletivo: fluido para o cidadao, rigido para o colonizado, grotesco para o inimigo."
    }
  ]
};

const REGIME_COLORS = {
  FUNDACIONAL: "#2563eb",
  NORMATIVO: "#059669",
  MILITAR: "#dc2626"
};

function renderScoutPage() {
  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CORPUS SCOUT — Iconocracia</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Georgia', serif; background: #0f0f0f; color: #e0ddd5; line-height: 1.7; }
  .header { background: #1a1a1a; border-bottom: 2px solid #c9a84c; padding: 2rem; text-align: center; }
  .header h1 { font-size: 1.6rem; color: #c9a84c; letter-spacing: 0.15em; text-transform: uppercase; }
  .header p { color: #888; font-style: italic; margin-top: 0.5rem; font-size: 0.9rem; }
  .stats { display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; }
  .stat { text-align: center; }
  .stat-num { font-size: 1.8rem; color: #c9a84c; font-weight: bold; }
  .stat-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #666; }
  .container { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }
  .section-title { font-size: 1.1rem; color: #c9a84c; text-transform: uppercase; letter-spacing: 0.15em; border-bottom: 1px solid #333; padding-bottom: 0.5rem; margin: 2.5rem 0 1.5rem; }
  .card { background: #1a1a1a; border: 1px solid #2a2a2a; border-left: 4px solid #059669; margin-bottom: 1.5rem; padding: 1.5rem; transition: border-color 0.2s; }
  .card:hover { border-color: #c9a84c; }
  .card.militar { border-left-color: #dc2626; }
  .card.normativo { border-left-color: #059669; }
  .card.fundacional { border-left-color: #2563eb; }
  .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
  .card-id { font-family: monospace; font-size: 0.8rem; color: #c9a84c; }
  .card-regime { font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 2px; text-transform: uppercase; letter-spacing: 0.1em; font-weight: bold; }
  .regime-MILITAR { background: #dc262622; color: #f87171; border: 1px solid #dc262644; }
  .regime-NORMATIVO { background: #05966922; color: #6ee7b7; border: 1px solid #05966944; }
  .regime-FUNDACIONAL { background: #2563eb22; color: #93c5fd; border: 1px solid #2563eb44; }
  .card-title { font-size: 1.05rem; color: #e0ddd5; margin-bottom: 0.5rem; }
  .card-meta { font-size: 0.8rem; color: #888; margin-bottom: 0.75rem; }
  .card-meta span { margin-right: 1rem; }
  .card-body { font-size: 0.9rem; color: #aaa; }
  .card-endurecimento { font-size: 0.8rem; margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: #111; border-left: 2px solid #c9a84c; }
  .card-endurecimento strong { color: #c9a84c; }
  .card-attrs { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem; }
  .attr-tag { font-size: 0.7rem; padding: 0.15rem 0.5rem; background: #222; border: 1px solid #333; color: #999; }
  .card-link { display: inline-block; margin-top: 0.75rem; font-size: 0.8rem; color: #c9a84c; text-decoration: none; }
  .card-link:hover { text-decoration: underline; }
  .card-note { font-size: 0.75rem; color: #f87171; font-style: italic; margin-top: 0.5rem; }
  .zw-card { background: #1a1a1a; border: 1px solid #c9a84c33; margin-bottom: 1.5rem; padding: 1.5rem; }
  .zw-card .card-title { color: #c9a84c; }
  .zw-polos { font-size: 0.85rem; color: #aaa; margin: 0.5rem 0; font-style: italic; }
  .zw-tese { font-size: 0.9rem; color: #e0ddd5; margin-top: 0.75rem; padding: 0.75rem; background: #111; border-left: 2px solid #c9a84c; }
  .footer { text-align: center; padding: 2rem; color: #444; font-size: 0.75rem; border-top: 1px solid #222; margin-top: 3rem; }
  a { color: #c9a84c; }
</style>
</head>
<body>
<div class="header">
  <h1>Corpus Scout</h1>
  <p>${SCOUT_DATA.thesis}</p>
  <div class="stats">
    <div class="stat"><div class="stat-num">${SCOUT_DATA.candidates.length}</div><div class="stat-label">Candidatos</div></div>
    <div class="stat"><div class="stat-num">${SCOUT_DATA.zwischenraume.length}</div><div class="stat-label">Zwischenraume</div></div>
    <div class="stat"><div class="stat-num">${SCOUT_DATA.session}</div><div class="stat-label">Sessao</div></div>
  </div>
</div>
<div class="container">
  <div class="section-title">Candidatos ao Corpus</div>
  ${SCOUT_DATA.candidates.map(c => `
  <div class="card ${c.regime.toLowerCase()}">
    <div class="card-header">
      <span class="card-id">${c.id}</span>
      <span class="card-regime regime-${c.regime}">${c.regime}</span>
    </div>
    <div class="card-title">${c.titulo}</div>
    <div class="card-meta">
      <span>${c.pais} | ${c.data_estimada}</span>
      <span>${c.suporte}</span>
      <span>${c.acervo}</span>
    </div>
    <div class="card-body">${c.justificativa}</div>
    <div class="card-endurecimento"><strong>ENDURECIMENTO:</strong> ${c.endurecimento}</div>
    <div class="card-attrs">${c.atributos.map(a => `<span class="attr-tag">${a}</span>`).join('')}</div>
    ${c.url ? `<a class="card-link" href="${c.url}" target="_blank">Ver no acervo &rarr;</a>` : ''}
    ${c.nota ? `<div class="card-note">${c.nota}</div>` : ''}
  </div>`).join('')}

  <div class="section-title">Zwischenraume (Paineis Comparativos)</div>
  ${SCOUT_DATA.zwischenraume.map(z => `
  <div class="zw-card">
    <div class="card-header">
      <span class="card-id">${z.id}</span>
      <span class="card-meta">${z.pais.join(', ')} | ${z.periodo}</span>
    </div>
    <div class="card-title">${z.titulo}</div>
    <div class="zw-polos">${z.polos}</div>
    <div class="zw-tese">${z.tese}</div>
  </div>`).join('')}
</div>
<div class="footer">
  CORPUS SCOUT — PPGD/UFSC — ${SCOUT_DATA.session}<br>
  Skill: <code>corpus-scout</code> | Claude Code
</div>
</body>
</html>`;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Existing diary API
    if (url.pathname === "/api/diary") {
      const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
      };
      if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
      if (request.method === "GET") {
        const data = await env.DIARY_KV.get("diary", "text");
        return new Response(data || "[]", { headers });
      }
      if (request.method === "PUT") {
        const body = await request.text();
        await env.DIARY_KV.put("diary", body);
        return new Response(JSON.stringify({ ok: true }), { headers });
      }
      return new Response("Method not allowed", { status: 405, headers });
    }

    // Scout API — JSON
    if (url.pathname === "/api/scout") {
      return new Response(JSON.stringify(SCOUT_DATA, null, 2), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }

    // Scout viewer — HTML
    if (url.pathname === "/scout") {
      return new Response(renderScoutPage(), {
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    // Fall through to static assets
    return env.ASSETS.fetch(request);
  },
};
