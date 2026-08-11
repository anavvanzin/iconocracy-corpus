# Dialética — Metodologia da ICONOCRACIA (rodadas 1–2)

**Data:** 2026-07-31 · **Domínio:** normativo-metodológico + institucional (banca PPGD) · **Origem:** passo (f) do relatório `docs/research/deep-research-padrao-metodologico-iconografia-juridica-2026-07-31.md`; descendente da dialética 2026-06-19 (fila #2).
**Rodada 1:** coeficiente mínimo × recusa indiciária (A = Fable, B = Opus). **Rodada 2** (direção 3, escolhida pela Ana): estabelecimento sem arquétipo — autoria editorial × Purificação da editora (A = Opus, B = Fable, invertidos).

**Nota de execução:** rodada executada autonomamente (sessão remota, Ana ausente); o hard stop de Fase 4 e a escolha de recursão da Fase 7 foram convertidos em **pontos de adjudicação a posteriori** — nada aqui executa sozinho. Auditor hostil aplicado (obrigatório teria sido só na rodada 2; antecipado por rigor).

## Relação com DEC-2026-07-29-APARATO-MINIMO (vigente)

Esta dialética foi conduzida sem conhecimento de `docs/decisions/2026-07-29-aparato-minimo-suficiente.md` — decisão redigida em 2026-07-29 (véspera desta rodada) mas que só chegou ao `main` em 2026-08-04, via #162, depois que esta dialética já estava concluída (esteve em PR aberto, #161/#162, durante toda a execução abaixo). DEC-2026-07-29 é hoje a decisão **vigente** do projeto e chega, por pesquisa independente, à mesma conclusão de fundo da Rodada 1: descartar kappa/alfa/teste-reteste como exigência de protocolo; tratar o corpus core como catálogo documentado; preservar o inventário verbal e a tipologia de recusas sob paradigma indiciário (Morelli–Ginzburg); manter rastreabilidade, disciplina antianacrônica e declaração dos silêncios do corpus.

O que esta dialética acrescenta a DEC-2026-07-29, e que a decisão vigente não cobre:

- **Rodada 1** dá especificidade operacional à determinação de DEC-2026-07-29 de que o inventário "é preservado sob paradigma indiciário": a arquitetura de edição crítica (aparato de variantes por item, registro de roteamento, gramática [C]/[E]/[H] com [C] definida por replicação intra-estrato) é uma implementação concreta, testável em CI, do que DEC-2026-07-29 deixa como princípio.
- **Rodada 2** aborda uma pergunta que DEC-2026-07-29 não coloca: se o próprio ato de estabelecer/fixar uma leitura reproduz formalmente a Purificação Clássica que a tese denuncia. A resposta (Bédier: o arquétipo lachmanniano *é* a Purificação Clássica da filologia; três condições formais de legitimidade editorial) é contribuição nova, não versão operacional de nada em DEC-2026-07-29.

**Leitura recomendada:** tratar DEC-2026-07-29 como o texto de decisão citável no capítulo metodológico; esta dialética como o dossiê de trabalho que (a) chegou à mesma conclusão por caminho independente — reforço, não redundância vazia — e (b) resolve as duas questões operacionais que DEC-2026-07-29 deixou em aberto.

**Divergência numérica não reconciliada.** Esta dialética trabalhou com `purification.jsonl` (279 registros, 57,0% de proveniência-rotina). DEC-2026-07-29 e o diagnóstico de #162 trabalham com `records.jsonl` (335 registros atuais, 106 linhas de indicadores zerados = 229 codificados, 68,4% — e o próprio apêndice mesclado em #162 ainda usa o denominador desatualizado de 328/222, achado de revisão pós-merge do Codex ainda não corrigido). São arquivos e métricas diferentes sobre a mesma pergunta — quanto do corpus está de fato codificado — e não foram reconciliados entre os dois esforços. Fica como pendência ⚖ adicional.

## Trace (ordem de leitura)

1. `round_1_context_briefing.md` — briefing neutro (situação real + evidência dos dois lados + 5 fatos incômodos + pergunta ontológica)
2. `round_1_monk_A_prompt.md` · `round_1_monk_B_prompt.md` — prompts calibrados (correções anti-espantalho)
3. `round_1_monk_A.md` — Recusa Íntegra (Fable)
4. `round_1_monk_B.md` — Auditoria de Instrumento (Opus; verificou o ledger)
5. `round_1_determinate_negation.md` — análise estrutural (convergências surpreendentes, tensões internas, suposição compartilhada, pergunta oculta, decomposição boydiana, anti-pattern-matching)
6. `round_1_sublation.md` — primeira síntese (o corpus como edição crítica; gramática de registros)
7. `round_1_validation_monk_A.md` — elevado, 3 emendas
8. `round_1_validation_monk_B.md` — elevado, 4 emendas (o "praefatio" que faltava)
9. `round_1_auditoria_hostil.md` — 3 GRAVES, 3 MÉDIOS, 2 MENORES; fatos confirmados
10. **`round_1_sintese_final.md`** — síntese revisada da rodada 1 com todas as emendas e correções
11. `dialectic_queue.md` — direções abertas (a Ana escolhe)

## Trace — Rodada 2 (ordem de leitura)

12. `round_2_context_briefing.md` — a contradição (autoria × Purificação da editora), 5 fatos incômodos, material de fora (Lachmann/Bédier, copy-text, McGann, crítica genética)
13. `round_2_monk_A_prompt.md` · `round_2_monk_B_prompt.md` — prompts calibrados
14. `round_2_monk_A.md` — Autoria Declarada (Opus): o arquétipo como Purificação Clássica da filologia; assinatura formal em três condições
15. `round_2_monk_B.md` — A Purificação da Editora (Fable): fixar é cunhar; os 10 indicadores sobre a operação editorial; recusa de emitir
16. `round_2_determinate_negation.md` — negação com criatividade lateral R2 (oxímoros, injeção Special:Random, três metáforas); o lastro como termo faltante
17. `round_2_sublation.md` — sublação monetária (emissão conversível; corolário substantivo) — **posteriormente refutada**
18. `round_2_validation_monk_A.md` — elevado, 5 emendas · `round_2_validation_monk_B.md` — elevado, 4 emendas
19. `round_2_auditoria_hostil.md` — 7 GRAVES: Semeuse é prata; corrida ao banco invertida; glosa de Mondzain inexistente; lastro inexistente (FR-013 = ficção); mesmo-arranjo; corolário sem instrumento; abdicação no gênero
20. **`round_2_sintese_final.md`** — salvamento parcial honesto ← **começar por aqui se for ler um só**

## Model Update — Rodada 2 (o que mudou)

- **Antes:** "A rodada 1 respondeu ao arquétipo (GRAVE-2) por assunção; resta saber se o estabelecimento editorial reproduz a Purificação Clássica que a tese denuncia — e a resposta parecia exigir um critério distintivo novo."
- **Depois:** "O arquétipo tem resposta *argumentada*: ele é a Purificação Clássica da filologia (Bédier) — recusá-lo é o ponto rigoroso da analogia, e o que se fixa é responsabilidade datada, não origem. O critério distintivo existe e enuncia-se sem metáfora: datação do fundamento (com a assimetria temporal da arguição), inseparabilidade do material divergente (leitura destacada = inválida) e distribuição dos meios de re-estabelecimento (duas vias: impressa e executável). A tentativa de elevá-lo a teoria do objeto ('iconocracia = emissão irresgatável') foi **refutada pela auditoria** (Semeuse é prata; corrida ao banco invertida; a glosa de Mondzain era um erro — a *oikonomia* real não é moeda; o lastro alegado não existe no ledger) — e a refutação, inscrita no dossiê, é o exercício ao vivo da cultura 'crítica metodológica no ledger'. O gênero do Cap. 6 (corpo+aparato × dossiê sinótico) termina em **aporia declarada**: decisão de voz, não de epistemologia."
- **Porque:** os critérios de cunhagem morreram nos fatos incômodos (a Semeuse é assinada; o Estado revisa; a banca é estatal); o termo faltante (lastro) seduziu por prometer um critério derivado do objeto, e caiu porque derivava de uma glosa não-verificada — a lição: critérios reflexivos derivam-se de conceitos verificados na bibliografia da tese, não de notas de segunda ordem.

## Model Update — Rodada 1 (o que mudou)

- **Antes:** "O capítulo metodológico deve manter um coeficiente de confiabilidade mínimo (F2.5, alvo ≥ 0,67) OU abandonar o aparato métrico e fundar tudo no paradigma indiciário — decisão binária pendente, com a compatibilização 'IRR interno, não epistêmico' como ponte."
- **Depois:** "A 'confiabilidade intercodificadora' morreu por unanimidade — nenhum dos dois lados a defendia; o kappa desta tese sempre foi estabilidade inter-instrumento LLM. A ponte 'interno mas não epistêmico' é instável (dilema do 0,3) e cai. A questão real era a **partição não-declarada das alegações da tese**: leituras exemplares (indiciárias, caso a caso) vs alegações corpus-transversais (§6.5). A forma resolvida: **o corpus como edição crítica** — texto estabelecido no corpo (ato editorial declarado, sem arquétipo), **aparato de variantes por item** no pé (não tabela de α; concordância exata/adjacente como sumário descritivo), **registro de roteamento** como praefatio (trilha do juízo, guarda de CI de existência de evidência), e a **gramática de registros probatórios** [C]olacionada/[E]stratificada/[H]eurística sobre uma tabela enumerada de alegações transversais — com [C] definida por **replicação intra-estrato**, sem limiar de concordância em lugar nenhum."
- **Porque:** os monks convergiram em tudo menos três eixos estreitos (colação continua? número tem função probatória? aparece no corpo?); a negação revelou que cada um universalizava um registro probatório que a tese pós-virada realmente contém; o auditor esvaziou e forçou a reconstrução da semântica de [C] (replicação, não concordância) e devolveu a metáfora ecdótica às suas obrigações (variantes por item).

## Estado dos fatos verificados (por B e confirmados pelo auditor)

`purification.jsonl`: 279 itens, **zero** com codificação dupla (a "base natural do kappa" está vazia) · `coded_by`: 11 rótulos, 15 `ana`, **57,0% das codificações com proveniência de rotina** (159/279; errata R2/MÉDIO-9 — o 48,5% anterior misturava denominadores) · IRRs pré-virada: α 0,601 (opus×fable), 0,393 (opus×Gemini-Pro brief rico), −0,02 (brief condensado); regime 0,61–0,71; monocromatização 0,874→0,103 conforme par · schema do ledger ainda `integer 0–3` + `additionalProperties: false` (colação nova é inexecutável sem migração).

## ⚖ Adjudicação da Ana (consolidada na síntese final, §últimos)

1. Escala única 0–3 vs 0–4 (bloqueante; já era §7.3). 2. Destino de §6.5 sob replicação (custo de contribuição-vitrine declarado). 3. Nomenclatura autoral. 4. Levar a gramática à orientação (pergunta institucional de 2026-06-19, operacionalizada). 5. Orçamento/momento da migração de schema e do conjunto de sobreposição no prazo nov/2027.

## Consequência para o PLANO-VIRADA-POSSIBILIDADE

A síntese final propõe: F2.5 **reescrito** (colação e aparato; sem alvo numérico; registro de roteamento; guarda de CI de evidência), F1 **+2 itens bloqueantes** (migração de schema do ledger; multi-codificação), F4.5 **emendado** (a compatibilização "IRR interno, não epistêmico" é substituída pela gramática de registros — os dois monks a derrubaram). Edições ao plano só após adjudicação.
