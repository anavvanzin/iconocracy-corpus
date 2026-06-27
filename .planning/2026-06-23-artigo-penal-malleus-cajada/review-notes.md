---
title: "Review notes — artigo Duvidam Punem (v2.3)"
data: 2026-06-27
branch: artigo/duvidam-punem-v2
artigo: artigo_v2_redacao_limpa.md
prazo: 30-jun-2026
---

# Review notes — "Até quando duvidam, punem" (v2.3)

Handoff durável. Captura a revisão de 4 agentes, o que foi aplicado, o que ficou
pendente, e o veredito da dialética sobre como usar os 3 dias até a entrega.

## 1. Revisão de 4 agentes (2026-06-27)

Disparados em paralelo sobre o v2 (`87dec4a`), todos read-only:

- **Peer-review** (academic-paper-reviewer): veredito **"aceitar com revisões menores"**.
  Tese clara/original/sustentada; arquitetura cumprida; "embustes e enganos" é a pedra
  angular. Risco estrutural: Seção 4 (Federici) puxando uma 2ª tese.
- **Histórico-jurídico** (legal-historian): **nenhum CRÍTICO**. Enquadramentos travados
  firmes (Malleus como ausência produtiva; Inquisição hegemônica; degredo). Achado nº1:
  "soberania" anacrônica (contradiz Hespanha citado). A2: deriva sociológica (Patterson/Merry).
- **Verificação empírica** (general-purpose+web): 4 erros factuais (ver §2).
- **ABNT** (abnt-checker): 19 itens (11 formatação + 6 cross-ref + 2 desambiguação).

## 2. Aplicado ao v2.1 (commit `25424b5`)

**Factual (Tier 1):** edições do Malleus 14/16 destrocadas · "Instrução de 1613/1618"
inexistentes removidas, caso Cajada ancorado no Regimento de 1552 · "embustes e enganos"
movido pra folha de rosto (não sentença) · Logroño 1.384/420 = inquiridos (não acusados)
· "coevo"→"uma geração depois" · "Lisboa 1590"→"final do séc. XVI".

**ABNT (Tier 2):** +CERTEAU 1982, +GLUCKMAN 1955 (citados sem entrada) · Hespanha
2012→2018 · Malleus citado 2009 · SBRICCOLI 2011a/2011b · Federici 2021 · Monter/Behringer
citados (saíram de órfãs) · Hespanha 1994 órfã removida · Local/páginas em periódicos ·
formato tese/Malleus/Eymerich.

**Substância (Tier 3):** Federici subordinada ao argumento penal (Seção 4 + Conclusão;
marcada contestada) · soberania→jurisdição nos usos penais, **mantida** nos 2 usos
iconográficos (Seção 5 + "visibilidade da soberania" = objeto da tese).

Verificado: 0 travessões, 0 citações Malleus em 1487.

## 3. Pendente

**Verificações de fonte (classe omissão — conferir na fonte primária):**
- Latim da Question Six (`Quare mulierum praestantius solum...`) — suspeita de corrupção
  gramatical; conferir na edição Mackay 2009.
- Data do processo de Lisboa de Cajada — conferir em Cruz de Araújo (2017).
- Paginação Federici p. 184 / p. 11 — conferir na ed. Elefante (2021).
- Certeau 1982 — confirmar se a obra é *A escrita da história* (1982) para "efeito de
  retorno do arquivo".
- Menores: páginas REIS (pus 57-81), tradutor do Eymerich, Hespanha 2018 p. 159-175.

**Decisão de voz (NÃO é verificação nem cosmético):**
- Patterson "morte social" (legal-historian A2, severidade Alta): subordinar ao registro
  penal. **Deferido por tipo** para a integração da tese (14/07), não para 30-jun.

**Polimento opcional:** desagregar "ibérica" (PT operacional vs ES probatório) · "genocídio
de gênero" já marcado como retrospectivo/contestado · capitalização cosmética de títulos.

**Mecânico:** PDF com template ABNT · PR v2→main.

## 4. Dialética — como usar os 3 dias (veredito 2026-06-27)

Dois monges comprometidos. **TESE** (congelar): em repo caótico todo toque é loteria de
regressão; os pendentes são checklist fechado; "a coragem é não-tocar". **ANTÍTESE**
(investir): o artefato doutoral é julgado pela confiabilidade na margem; os pendentes são
furos por onde a banca entra; "você tem medo de abrir o Malleus e descobrir que citou errado".

**Onde se traem:** A achata um conjunto heterogêneo de risco num "não-toque" (mas latim
errado/data falsa não são mecânicos). B infla um lookup de horas em "encher 3 dias" (mas
verificação ≠ reescrita). **Suposição compartilhada:** ambos tratam a decisão como um dial
("quanto tocar") e temem a mesma coisa — erro na banca — só que A teme erro de *comissão*
(novo) e B de *omissão* (existente).

**Síntese (material de fora: code freeze + fact-check pass da engenharia/jornalismo):**

> **Freeze agora + fact-check pass limitado + gate de hotfix, triado por classe-de-erro por item.**

Sequência:
- **Dia 1 — fact-check (omissão):** só os 4 itens de credibilidade, contra a fonte. Binário:
  *confirmado* (não edita) ou *errado* (hotfix cirúrgico no worktree, re-verificado no commit).
- **Dia 2 — freeze declarado:** "ibérica" desagregada (1 frase). Patterson FORA do 30-jun (vai pra 14/07).
- **Dia 3 — formato/PDF/PR sob freeze:** zero edição de conteúdo.

**Default = não-tocar** (dissenso de A preservado): editar só com defeito *confirmado*. Se o
fact-check voltar tudo-confirmado, a jogada certa é literalmente não tocar.

**Resíduo (aporia):** Patterson não cabe no frame fact-check — deferido por tipo, não por tempo.

**Model update:** Antes: "entregar vs polir, escolher um ponto no dial." Depois: "freeze +
fact-check com gate; cada pendente classificado por comissão/omissão; o tempo não se gasta,
se porteia."

## 5. Próximas ações

1. Executar Dia 1 (fact-check dos 4 itens) — agentes de verificação de fonte.
2. Aplicar hotfixes confirmados via worktree + gate (regra git-parallel-safety).
3. "ibérica" (1 edit) + freeze.
4. PDF (instalar tectonic/weasyprint) + PR v2→main.
5. Pós-30/06: Patterson, Seção 5 expansão ICONOCRACIA (14/07).

## 6. Fact-check EXECUTADO e resolvido (2026-06-27) — v2.3

**Dia 1 — 4 verificações paralelas (read-only):**
- **Certeau 1982:** CONFIRMADO (*A escrita da história*, Forense Universitária, 1982). Sem edição; só ajustada a paráfrase ("no que se pode ler, com Certeau").
- **Latim Question Six:** ERRADO. String espúria → corrigida para *Cur in tam fragili sexu femineo plures reperiantur maleficae quam in viris* (commit `03a4da2`).
- **Federici:** páginas eram da ed. inglesa Autonomedia. Corrigido: Elefante **2017** (não 2021), p.184→**328**, p.11→**22**, +tradutor Coletivo Sycorax (`03a4da2`). ⚠ conferir se o exemplar físico é a 2ª ed. 2023 (re-diagramada → páginas mudam).
- **Cajada lugar:** ERRADO. Julgada na **Bahia/Salvador**, não Lisboa (só os autos foram a Lisboa). Corrigido (`03a4da2`).

**Mergulho proc. 10748 (1 agente deep-dive, ANTT+scholar):**
- **Tortura:** NÃO há registro no caso. Removida; substituída pela sentença documentada (carocha, vela, auto público, degredo ao Reino; isenta de açoites por estar doente; sentença 24/01/1593). Commit `788f1d9`.
- **Âncora "embustes e enganos":** CONFIRMADA verbatim no **fl.1** do proc. 10748 (ANTT/DigitArq). NÃO é de Cruz de Araújo (que não traz a frase) nem do Conselho Geral — é despacho da **Mesa inquisitorial**. Re-atribuída + enriquecida com o contexto de jurisdição (prova só por confissão extrajudicial, sem testemunhas, "pertençe mais ao ordinário que à Inquisição"). +entrada ANTT/DigitArq na bibliografia. Commit `788f1d9`.

**Dia 3 — compile:** tectonic 0.16.9 instalado; PDF + DOCX da v2.3 gerados e entregues.

**Estado: v2.3, em condição de entrega para 30-jun.**

**Ainda aberto (Ana / pós-entrega):** conferir edição Elefante (2017 vs 2023) + grafia exata do fl.1 no fac-símile DigitArq antes de publicar; deferido 14/07 = Patterson (voz), Seção 5 (ICONOCRACIA), "ibérica" desagregação, capitalização ABNT cosmética.

**Commits da branch:** `87dec4a` (v2) → `25424b5` (v2.1) → `a837539` (notes) → `03a4da2` (fact-check) → `788f1d9` (cluster) → este.
