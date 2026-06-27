# task_plan.md — Reconstrução do artigo Malleus/Cajada (ambiente nuvem)

Fase: 2026-06-27-artigo-malleus-cajada-reconstrucao
Working title: "Até quando duvidam, punem: o Malleus Maleficarum, Maria Gonçalves Cajada e a construção atlântica do tipo penal de bruxaria"
Prazo do artigo: 30/06/2026.

## Contexto / por que esta fase existe

A tarefa pedida era *continuar a revisão* (Phases 2–4) de um draft de ~35.000
caracteres em `Text/artigo-malleus-cajada-bruxaria-atlantica.md`, com a Phase 1
já completa, e um plano de revisão em
`.planning/2026-06-23-artigo-malleus-cajada-revisao/task_plan.md`.

**Bloqueio descoberto:** nenhum desses arquivos existe neste ambiente de nuvem.
Verificado em: working tree, todo o histórico git (todas as refs, reflog, stash),
branch remota e repositório `Research`. Buscas por conteúdo (Brízida, Cartagena,
Salzburgo, White, "generificação", Sbriccoli fama) retornaram zero. O único
planejamento presente é o da fase de **criação** (`2026-06-23-artigo-penal-
malleus-cajada/`), cujo `progress.md`/`task_plan.md` registram o artigo como
"draft 0%".

**Conclusão:** o draft + Phase 1 + plano de revisão estão apenas no Mac da Ana,
não commitados/pushados. O container de nuvem clonou só o que estava no GitHub.

**Decisão (Ana: "no preference" + "let's continue"):** não fabricar uma revisão
de um draft inexistente; em vez disso, redigir do zero uma RECONSTRUÇÃO honesta
a partir somente das fontes verificadas no repositório, já na estrutura-alvo das
fases pendentes, com marcadores [EXPANDIR]/[VERIFICAR] onde o conteúdo só existe
no draft local.

## Entregável

`Text/artigo-malleus-cajada-bruxaria-atlantica_DRAFT-FONTES-VERIFICADAS.md`
(nome distinto de propósito, para nunca colidir com o draft canônico quando a
Ana o pushar). ~10 seções + resumo + referências ABNT NBR 6023:2025.

## Fontes verificadas usadas (todas no repo)

- `.planning/2026-06-23-artigo-penal-malleus-cajada/findings.md` (Levack 2015,
  Behringer 2004/2009, Roper 2013, Cruz de Araújo, ANPUH).
- `Text/Handout — O Malleus Maleficarum e a construção da bruxaria.md`
  (Broedel 2003, Sbriccoli 2011 p.459-504, Meccarelli 2018, Souza 1986,
  Vainfas 1997, Capistrano de Abreu 1925/1935, Cajada, ANTT 10748, Regimentos).
- `Text/Apresentação Malleus Maleficarum — roteiro falado.md` (narrativa
  Innsbruck/Scheuberin; Cajada; gênero+raça; tese "até quando duvidam, punem").
- `wiki/.../Tabela — Processos inquisitoriais da Bahia e Brasil colonial.md`
  (11 processos ANTT verificados: Tourinho, Filipa de Sousa, Ana Rodrigues,
  Simão do Congo, Luzia Pinta, Jacinto etc.) → base da seção 8.
- `wiki/.../memoriais/Memorial 02 — Justiça hegemônica...md` (Sbriccoli/
  Meccarelli/Hespanha/Costa; "antropólogo involuntário"; ponte ICONOCRACIA).

## Como a estrutura implementa as fases pendentes

- **Phase 2 (ordem narrativa):** Cajada (seções 5–7) vem ANTES da seção
  comparativa/em série (seção 8). Innsbruck consolidado na seção 3 (Malleus),
  apenas tangenciado na introdução — sem dupla aparição. Enquadramento teórico
  (Sbriccoli/Hespanha no corpo; Meccarelli + circulação) concentrado na seção 2.
- **Phase 3 (tese e conclusão):** conclusão (seção 10) responde diretamente
  "até quando duvidam, punem" (a dúvida recai sobre a ré, a certeza sobre o
  tipo). Regimento do Santo Ofício português como canal de circulação na
  seção 4. Sbriccoli citado com faixa de páginas (p. 459-504).
- **Phase 4 (polimento):** usa "marcação de gênero e raça" (não "generificação",
  seção 9); desenvolve "circulação/transformação forçada" (seções 8 e 10);
  referências em ABNT NBR 6023:2025.

## Status

- [x] Diagnóstico do bloqueio (draft ausente) documentado.
- [x] Leitura integral de todas as fontes verificadas no repo.
- [x] Artigo reconstruído redigido (~10 seções + resumo + referências).
- [x] Banner de proveniência no topo do arquivo.
- [x] task_plan.md desta fase.
- [ ] Commit + push na branch claude/peaceful-cerf-0gywv8.
- [ ] Abrir PR (draft) na anavvanzin/iconocracy-corpus.

## Pendências para a Ana (merge com o draft local)

1. **Decidir a fonte de verdade:** seu draft local vs. esta reconstrução.
   Provavelmente: manter o seu draft e importar daqui o que faltar
   (seção 8 em série a partir da Tabela; seção 9 "marcação de gênero e raça";
   conclusão respondendo o título; menção aos Regimentos).
2. **[EXPANDIR] casos europeus** (Brízida, Cartagena, Salzburgo) + citação de
   White com tradução — só existem no seu draft.
3. **[EXPANDIR] referências** Costa (corpo), Nunes/Dal Ri/Martyn (notas).
4. **[VERIFICAR]** página exata de Sbriccoli para a *fama* denunciante.
5. **[VERIFICAR]** recorte temporal: plano fixou 1487–1810; Tabela indica
   extinção do Tribunal em 1821. Reconciliar.
6. **[VERIFICAR]** Roper (título/ano), Ankarloo&Clark cap.15 (autoria/páginas),
   Hespanha 1993 (título/edição), Araújo 2016 dissertação vs. 2017 livro,
   datas dos Regimentos (1552/1613/1640).
