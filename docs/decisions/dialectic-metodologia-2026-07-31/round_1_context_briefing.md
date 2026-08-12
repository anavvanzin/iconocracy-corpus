# Round 1 — Context Briefing (neutro)

**Dialética:** Confiabilidade métrica mínima vs. paradigma indiciário puro no capítulo metodológico
**Data:** 2026-07-31
**Domínio:** normativo-metodológico (com componente institucional: banca de PPGD)
**Monks:** 2 (Monk A = Recusa Íntegra / indiciário-catálogo · Monk B = Auditoria de Instrumento / coeficiente mínimo)
**Ancestralidade:** descendente direta da dialética 2026-06-19 (`docs/decisions/dialectic-corpus-2026-06-19/`) — síntese Tier 1/Tier 2 e item #2 da fila (partição Panofsky indicador-a-indicador). Esta rodada herda aquele vocabulário.

> Material `[SITUAÇÃO]` vem do estado real do repositório e das decisões da Ana. Material `[PESQUISA]` vem do relatório de deep research de 2026-07-31 e do lit-review de 2026-06-19. Os monks devem acreditar a partir do caso concreto, não de genéricos.

---

## 1. A contradição (enquadramento)

O relatório `docs/research/deep-research-padrao-metodologico-iconografia-juridica-2026-07-31.md` recomenda **descartar** o aparato de confiabilidade métrica importado da análise de conteúdo (kappa de Cohen, alfa de Krippendorff, teste-reteste) como exigência formal do capítulo metodológico, re-fundando o inventário verbal no **paradigma indiciário** (Ginzburg) e o corpus como **catálogo documentado** (Trouillot). O mesmo relatório, no passo (f), recomenda redigir a posição contrária como estresse-teste. O `docs/PLANO-VIRADA-POSSIBILIDADE.md` (F2.5), por sua vez, **mantém** um IRR da lente qualitativa: dupla codificação cega de 20–30% da amostra, kappa/α por indicador ordinal com alvo ≥ 0,67, concordância categórica para inventário verbal e tipologia de recusa, adjudicação da autora como instância final.

A contradição de superfície: *abandonar tudo* vs. *manter um coeficiente mínimo restrito ao inventário de atributos formais*. A contradição profunda (a ser testada pelos monks): **o que o coeficiente É dentro desta tese** — reivindicação epistêmica sobre a natureza do dado (medição), escudo retórico perante a banca, ou auditoria nativa de um pipeline computacional? E: **qual é a relação da tese com seus próprios instrumentos** — os codificadores LLM são *testemunhas* (cujo testemunho pede corroboração) ou *lentes* (cuja distorção pede caracterização)?

## 2. `[SITUAÇÃO]` O que torna este caso diferente do genérico

- **A virada POSSIBILIDADE já aconteceu.** DEC-2026-07-28-COMPOSTO aposentou o `endurecimento_score` (índice composto). Os 10 indicadores sobrevivem como grade de observação; a espinha da tese passa a operações (Entradas/Recusas/Coexistências); o inventário verbal + tipologia de recusas é o instrumento vigente. O enum verbal no schema **proíbe o número** — "a recusa da métrica está inscrita na estrutura do dado" (plano §6.1). Um coeficiente de concordância reintroduziria número *sobre* o dado, não *no* dado — mas reintroduziria.
- **Os codificadores NÃO são humanos independentes.** A codificação foi feita por instrumentos LLM (iconocode-opus, opus-4.6, Fable-5, proxy LPAI v2 sobre Kimi K3) + a autora como adjudicadora. O repositório já contém uma história densa de IRR *inter-instrumento*: `IRR-PILOTO-2026-05-30`, `IRR-RE-RUN-DESIGN-2026-06-09`, `IRR-INTER-INSTRUMENTO-2026-06-10`, `IRR-opus-gemini(-PRO)-2026-06-22`, `IRR-opus-fable-2026-06-22`, `2026-06-19-reliability-audit-design`. `compute_irr.py` está listado no plano §5 como o que "sobrevive intacto"; `purification.jsonl` (279 codificações) é chamado de "base natural do kappa por indicador". **Kappa aqui nunca foi concordância intersubjetiva humana clássica — sempre foi estabilidade entre instrumentos computacionais.**
- **A cultura do projeto é reflexividade em ledger.** `legacy_frozen` congela o escore aposentado como dado histórico *da pesquisa sobre a pesquisa*; o Cap. 2 narrará a virada com o rastro como evidência. A tese já pratica "a própria crítica metodológica inscrita no ledger".
- **Síntese herdada (2026-06-19):** alegações estatísticas (Tier 1) exigem estrato congelado de instrumento único; alegações interpretativas (Tier 2) são capta vivo com audit trail. **Porém**: a virada POSSIBILIDADE aposentou o principal consumidor do Tier 1 (o escore e suas análises Kruskal-Wallis etc. — notebooks re-destinados na F3). Pergunta aberta: sobra Tier 1? A fila #2 daquela rodada perguntava: quais dos 10 indicadores são Panofsky-1 (medida: monocromatização, serialidade, inscrição_estatal) vs Panofsky-2/3 (juízo: dessexualização, apagamento_narrativo)?
- **Corpus e prazo:** 328 registros (279 codificados = 85%), corpus aberto por decisão (N não-fixado, postura exploratória), defesa ~nov/2027 no PPGD/UFSC.
- **Contexto institucional:** banca brasileira de PPGD; vocabulário crítico corrente: "manualismo"/"reverencialismo" (Luciano Oliveira); historiografia jurídica de matriz Hespanha/Fonseca; a rodada de 2026-06-19 registrou como input-do-mundo-real pendente a pergunta "Prof. Diego Nunes / a banca aceitam a reformulação 'aparato estatístico = órgão de evidência, rigor = auditabilidade hermenêutica'?" — nunca respondida.
- **F2.5 é compromisso já assumido no plano** (proposta para adjudicação, não executada): IRR da lente qualitativa, alvo ≥ 0,67, autora como instância final. O cross-link F4.5 (2026-07-31) tenta compatibilizar: "IRR = auditoria interna de qualidade, não fundamento epistêmico perante a banca". Os monks podem atacar essa compatibilização como instável.

## 3. `[PESQUISA]` Evidência disponível aos dois lados

### 3a. A favor da recusa íntegra (relatório 2026-07-31)
- **Nenhum autor canônico de iconografia jurídica usa coeficiente** — nem quando quantifica: Hayaert catalogou 987 alegorias (1450–1850) e valida por aprofundamento de esquemas exemplares ("some schemas have been studied in depth"), não por margem de erro. Sbriccoli: tipologia casuística sem tabulação. Resnik & Curtis: ~220+ imagens, exame narrativo.
- **Rigor na historiografia jurídica = crítica de fontes + antianacronismo** (Hespanha: "análise rigorosa e confiável" definida como respeito à lógica interna da fonte; Fonseca: contra a lógica imposta ao passado). Não replicabilidade estatística.
- **Prática das teses brasileiras de história do direito** (Bechara 2019, UFSC): maioria não declara aparato metodológico formalizado importado; a anomalia punível é falta de crítica de fonte e de recorte, não falta de kappa.
- **Custo documentado da quantificação iconográfica** (Pavlek/Winters/Morin 2022, numismática): padronizar exige abstração e perda de detalhe interpretativo; codificação específica demais introduz ruído estatístico; sem padrão consensual mesmo no subcampo mais maduro.
- **Paradigma indiciário** (Ginzburg/Morelli): tipologia de atributos com validade probatória por lógica indiciária, não amostral. **Catálogo documentado** (Trouillot): lacunas como objeto, não ruído.
- **O par Hayaert/Roele**: a crítica real que um livro de referência recebeu não foi "cadê o kappa?", foi "eschews empiricism" — ausência de trabalho empírico sobre a *recepção* (encontro obra-espectador). Um coeficiente de concordância entre codificadores **não responde** à crítica de Roele; responde-se declarando limites (o que a tese prova: sentido produzido/disponibilizado; o que não prova: recepção efetiva).

### 3b. A favor do coeficiente mínimo (lit-review 2026-06-19 + estado do repo)
- **LLM-as-annotator drift é real e documentado** (Chen/Zaharia/Zou 2023: GPT-4 mar→jun oscilou 97,6%→2,4% numa tarefa). Best practice: fixar modelo+versão+prompt, logar proveniência, **computar concordância antes de adotar novo instrumento**. Dois snapshots do "mesmo" modelo não são o mesmo instrumento.
- **A tese usa pipeline computacional que Hayaert nunca teve.** O precedente disciplinar (Sbriccoli à mão, Hayaert com fichário) não cobre o caso "279 codificações geradas por 4+ instrumentos LLM ao longo de 14 meses". A pergunta hostil da banca pode não ser "isso não é impressionismo?" mas **"isso não é IA sem auditoria?"** — e Ginzburg não responde a essa.
- **Confound de instrumento** (rodada 2026-06-19, resíduo nunca testado): `coded_by` pode correlacionar com regime/data/fonte. Concordância em conjunto de sobreposição é o único teste conhecido.
- **Limiares e paradoxos:** Krippendorff: α ≥ 0,80 confiável; 0,667–0,80 apenas "tentativo". Paradoxo do kappa sob prevalência desbalanceada (relevante: indicadores quase-automáticos por suporte — serialidade em moeda). **Atenção: o alvo F2.5 (≥ 0,67) está na faixa que o próprio Krippendorff chama de tentativa** — munição para os dois lados.
- **Perspectivismo** (Aroyo & Welty): desacordo entre anotadores é sinal, não ruído — terceira leitura do que um "IRR baixo" significaria.

### 3c. Fatos incômodos que NENHUM monk pode ignorar
1. O kappa desta tese mede estabilidade **inter-instrumento LLM**, não concordância humana intersubjetiva. Chamá-lo de "confiabilidade intercodificador" no sentido da análise de conteúdo é imprecisão dos dois lados.
2. O alvo F2.5 (≥ 0,67) é "tentativo" pelo próprio padrão da área importada — um coeficiente exibido e fraco pode ser retoricamente pior que nenhum.
3. A crítica documentada ao campo (Roele) pede empiria da *recepção*, que nenhum coeficiente de codificação fornece.
4. A infraestrutura de IRR já existe, já rodou e está classificada como "sobrevive intacto" — descartar não é não-adotar, é **remover controle existente**.
5. A autora é a instância final de adjudicação — qualquer coeficiente coexiste com uma adjudicação que o sobrepõe.

## 4. Pergunta ontológica (para os dois prompts)

**O que o coeficiente de concordância É dentro de uma tese de iconografia jurídica cujos codificadores são instrumentos computacionais — e o que ele FAZ (epistemicamente e retoricamente) quando aparece no capítulo metodológico?**

## 5. Critérios de uma boa síntese (a verificar na Fase 5)

- Não pode ser divisão salomônica ("um pouco de kappa, um pouco de Ginzburg").
- Deve tornar a contradição *previsível* (teste abdutivo): por que os dois lados existem e têm evidência genuína?
- Deve engajar a estrutura de autoridade real (banca de PPGD; quem decide é a Ana; a banca argui) — síntese intelectualmente linda mas institucionalmente irrelevante falha.
- Deve dizer o que acontece com F2.5 do plano (manter, reescrever, realocar, cortar) e com o texto do Cap. 2 — consequência operacional, não só conceito.
