# progress.md — Artigo de História do Direito Penal
Fase: 2026-06-23-artigo-penal-malleus-cajada
Working title: "Até quando duvidam, punem"
Prazo: 30 de junho de 2026

## Status atual (2026-06-23)

- [x] Diretório `2026-06-23-artigo-penal-malleus-cajada/` criado (sign-off Ana).
- [x] `task_plan.md` v2 escrito (cronograma dia 30, caminho B faseada).
- [x] `findings.md` v2 escrito (T1a parcial: Levack + Behringer; T1b pendente dia 24-06).
- [x] Esqueleto Seção 1 (1 página, "O Malleus como evento discursivo") em task_plan.md §T5.
- [x] Script Playwright em `/tmp/playwright-penal-research.js` (multi-step, 7 fontes).
- [x] Firecrawl auth verificada: 2562 credits, ciclo 22-jun→22-jul; `/v1/scrape` + `/v1/search` funcionam; `/v2/research` (skill broken) 404.
- [x] Pivô locked: Cajada + Malleus historiografia (decisão Ana 23-06).
- [x] Decisões locked: D1 pivô único, D2 ICONOCRACIA em esboço, D3 recorte 1487-1810, D4 PT-BR.
- [ ] T1b: Roper 2013 cap. Malleus (Playwright scrape) — dia 24-06.
- [ ] T2: Playwright scrape 7 fontes — dia 24-06.
- [ ] T3: 1 pp. sobre pivô — dia 25-06.
- [ ] T4: 1 pp. recorte temporal — dia 25-06.
- [ ] T5: outline 5 seções refinado — dia 25-06.
- [ ] T6a: Seções 1-2 (~6 pp.) — dia 26-06.
- [ ] T6b: Seção 3 + início Seção 4 (~5 pp.) — dia 27-06.
- [ ] T6c: Seção 4 + Seção 5 esboço (~4 pp.) — dia 28-06.
- [ ] T7: self-review ABNT 6023:2025 — dia 29-06.
- [ ] ENTREGA dia 30-06: 15-20 pp., PDF + DOCX, sumário executivo.

## Bloqueios identificados
- Sem Playwright instalado no sandbox Hermes; script `/tmp/playwright-penal-research.js` é para Ana rodar localmente.
- ANTT / Torre do Tombo: fonte primária não consultada diretamente; Cruz de Araújo 2017 como mediação (cotejo direto previsto para 14/07).
- Memory overflow (2246/2200): bloqueia atualização de memory sobre 3 pontos errados (0-4 ordinal, IRR scripts, codebooks paralelos); decisions file §5/§9 são fonte de verdade substituta.
- Sign-off explícito pendente para commit + push (regra: "Require explicit OK for pushing to main").

## Pendências externas ao artigo (não bloqueiam)
- Banner `_DO_NOT_USE_AS_EVIDENCE_` no filename do report sintético (Reviewer 1 sugestão) — pendente, fora do escopo deste artigo.
- Honcho peer card update (3 correções materiais) — pendente, fora do escopo deste artigo.
- Rater-2 manual ICONOCRACIA — próxima fase da tese, não este artigo.
- Cron `weekly-iconocracy-drift` (drift-detector) — pendente, nice-to-have.

## Reflexões metodológicas (decisão dialética)

**Tese**: o artigo deve ter Cajada como **pivô** e não como caso central, porque a historiografia do Malleus é o eixo de leitura, e Cajada é o ponto onde discurso doutrinário e prática acusatória se cruzam.

**Antítese**: o risco de Cajada-como-pivô é virar Cajada-como-caso-central "por inércia" — o leitor pode tratar Cajada como o objeto do artigo e o Malleus como pano de fundo, invertendo a estrutura argumentativa.

**Síntese**: para evitar essa inversão, a Seção 1 ("O Malleus como evento discursivo") deve ser **mais longa** que a Seção 3 ("Cajada como caso-pivô"); a estrutura sinaliza, por proporção, que o Malleus é o objeto e Cajada é a entrada.
