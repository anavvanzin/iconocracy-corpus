// Motor de página — chips, revelações, contadores, sincronia do rail
(() => {
  // chips da capa → rolagem suave
  document.querySelectorAll("[data-goto]").forEach(b =>
    b.addEventListener("click", () => {
      const t = document.querySelector(b.dataset.goto);
      if (t) t.scrollIntoView({ behavior: U.REDUCE ? "auto" : "smooth" });
    }));

  // faixa de estatísticas (a partir de RPT)
  const statRow = document.getElementById("stat-row");
  if (statRow) {
    RPT.stats.forEach(st => {
      const d = document.createElement("div");
      d.className = "stat";
      d.setAttribute("data-drill-keep", "");
      d.style.cursor = "pointer";
      d.innerHTML = `<div class="num">0</div><div class="lbl">${st.lbl}</div>`;
      d.addEventListener("click", ev => U.showDrill({ ...st.drill, x: ev.clientX, y: ev.clientY }));
      statRow.appendChild(d);
      const numEl = d.querySelector(".num");
      if (U.REDUCE) { numEl.textContent = st.num.toLocaleString("pt-BR"); }
      else {
        const io = new IntersectionObserver(es => es.forEach(en => {
          if (en.isIntersecting) { U.countUp(numEl, { to: st.num }); io.disconnect(); }
        }), { threshold: 0.4 });
        io.observe(d);
      }
    });
  }

  // revelações de entrada
  const rvIO = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("on"); rvIO.unobserve(en.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll(".rv").forEach(el => {
    if (U.REDUCE) el.classList.add("on"); else rvIO.observe(el);
  });

  // sincronia do rail com a seção visível
  const secIO = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting && window.RAIL) window.RAIL.set(en.target.dataset.win);
  }), { rootMargin: "-38% 0px -52% 0px", threshold: 0 });
  document.querySelectorAll("[data-win]").forEach(s => secIO.observe(s));
})();
