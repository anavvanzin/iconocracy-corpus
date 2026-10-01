// P5 · Matriz de distribuição de gênero — tabela DOM com semântica de calor
// ametista = feminino (voz arquivística) · navy = masculino · hachura terracota = fissura
(() => {
  const host = document.getElementById("matrix-chart");
  if (!host) return;
  const body = U.frame(host, {
    title: "O gênero se distribui por função — não por gramática",
    sub: "SÍNTESE QUALITATIVA DO CORPUS, NÃO CONTAGEM · CLIQUE NAS CÉLULAS DE GÊNERO PARA A BASE ICONOGRÁFICA",
    src: "Dossiê §6.3 e Tabela 2 · âncoras K12–K22",
  });

  const GLBL = { fem: "Feminino", masc: "Masculino", contra: "Fissura" };
  const tbl = document.createElement("table");
  tbl.className = "dt mtx rv";
  tbl.innerHTML = `<thead><tr>
    <th style="width:27%">Categoria alegórica</th>
    <th style="width:15%">${RPT.matrix.cols[0]}</th>
    <th style="width:24%">${RPT.matrix.cols[1]}</th>
    <th>${RPT.matrix.cols[2]}</th>
  </tr></thead>`;
  const tb = document.createElement("tbody");
  RPT.matrix.rows.forEach(r => {
    const tr = document.createElement("tr");
    if (r.g === "contra") tr.className = "hl";
    tr.innerHTML = `
      <td class="rowname">${r.name}<span>${r.sub}</span></td>
      <td class="cell c-${r.g}" data-drill-keep tabindex="0" role="button" aria-label="${r.name}: ${GLBL[r.g]} — abrir base">${GLBL[r.g]}</td>
      <td class="dim">${r.pos}</td>
      <td class="dim">${r.ex}</td>`;
    const cell = tr.querySelector(".cell");
    const s = (window.SRCS || []).find(x => x.k === r.k);
    const open = ev => U.showDrill({
      title: `${r.name} · ${GLBL[r.g]}`, value: r.pos, sub: r.drill,
      source: s ? `${r.k} · ${s.name} (${s.date})` : r.k, x: ev.clientX, y: ev.clientY,
    });
    cell.addEventListener("click", open);
    cell.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(ev); } });
    tb.appendChild(tr);
  });
  tbl.appendChild(tb);
  body.appendChild(tbl);

  const leg = document.createElement("p");
  leg.className = "chart-sub";
  leg.style.marginTop = "10px";
  leg.innerHTML = `<span style="color:#4a3560">■</span> FEMININO · VALOR-CONTEMPLADO &nbsp;&nbsp;
    <span style="color:${U.PAL.navy}">■</span> MASCULINO · POTÊNCIA-EXERCIDA &nbsp;&nbsp;
    <span style="color:${U.PAL.contra}">▨</span> FISSURA · A REGRA CONTESTADA`;
  body.appendChild(leg);
})();
