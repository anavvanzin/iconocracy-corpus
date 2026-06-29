# Monk B — "O Corpus Congelado" (Fechamento) · Round 1

> Electric Monk, modelo: Claude (subagente). Crença plena, sem hedge.

# Uma alegação empírica sobre um objeto que não tem estado não é ciência

## a. O que É um corpus que sustenta uma alegação empírica

Comecemos pela ontologia, porque é onde tudo se decide. Um corpus que sustenta uma alegação empírica não é um serviço. Não é um repositório vivo, não é um pipeline, não é um branch que respira. É um **documento**: imutável, identificado por um hash, datado, citável, e — esta é a palavra que importa — **falsificável**. Quando a tese ICONOCRACIA afirma que a distribuição de endurecimento difere entre os regimes fundacional, normativo e militar, e sustenta isso com um Kruskal-Wallis, ela está fazendo uma afirmação que só significa alguma coisa se houver um objeto fixo contra o qual ela possa ser refutada. Um árbitro externo precisa poder pegar o *mesmo* corpus, rodar o *mesmo* teste, e ou confirmar ou derrubar o resultado. Essa é a definição mínima de uma alegação científica: existe um estado do mundo que a tornaria falsa, e esse estado é verificável por terceiros.

Agora olhe o estado real: records.jsonl tem **265**, corpus-data.json tem **264**, origin/main tem **~309**, o snapshot `Other/` tem **165**, o companion tem 165 stale, e o E1 Fable-5 tem **44**. A contagem *varia conforme o store que você abre*. Isto não é um detalhe administrativo. É uma catástrofe ontológica. Um corpus cujo N depende de qual arquivo você abriu **não tem estado**. E uma alegação empírica sobre um objeto sem estado é, por construção, **infalsificável** — não porque seja forte, mas porque não há nada de fixo para refutar. O p-valor de um Kruskal-Wallis rodado sobre "o corpus" quando "o corpus" é um intervalo de 44 a 309 não refuta absolutamente nada. Ele é decorativo. E uma ciência decorativa não é ciência: é ornamento com aparência de número.

## b. O melhor caso do oponente — nos termos que ele endossaria

O Corpus Vivo não é um tolo. Ele diria, com Johanna Drucker (2011): o que chamo de "dado" é na verdade *capta* — não algo dado pela natureza, mas algo **tomado**, construído, codependente do observador. A análise iconográfica de uma alegoria feminina não é uma medida de temperatura; é um juízo, e juízos melhoram. Logo um instrumento melhor (Fable-5, multimodal, que olha a imagem em vez de summaries fracos como a Gemma-4 que cuspiu 29 zeros) produz *capta mais fiel*; congelar agora fossilizaria dado inferior. Ele invocaria Goodman et al. (2016): existe reprodutibilidade *inferencial* (conclusões qualitativamente similares), não só computacional; e Lincoln & Guba (1985): a reprodutibilidade hermenêutica vive de **audit trail**, não de recomputação. Sob essa régua, o corpus deve permanecer vivo, e o deadline de nov/2027 é inimigo da verdade.

Esse é o caso dele, inteiro. E é por entendê-lo que vejo onde se autodestrói.

## c. O diagnóstico da falha dele

O Corpus Vivo falha por uma razão precisa: **ele invoca o teste estatístico E recusa o contrato do teste estatístico.** Ele já rodou Kruskal-Wallis e correspondência. O Cap. 3 está construído sobre o snapshot N=165, e os capítulos *afirmam N=165 no texto*. No momento em que você escreve um p-valor numa tese, você não está mais no regime de Drucker. Você assinou — como diz Da (2019) — um contrato frequentista que **importa seus padrões por inteiro**. Você não pode usar a estatística decorativamente, colhendo a autoridade do número e fugindo, quando cobrado pelo rigor, para "mas é *capta*". Isso não é pluralismo; é ter o bolo e comê-lo. A roupagem hermenêutica vira um **álibi**.

E há o pecado mais grave: **o batch effect dos múltiplos instrumentos.** A literatura de 2026 (Variance-Aware LLM Annotation) declara que *provider/version drift* e *cross-model disagreement* são confounds em datasets anotados por LLM. Chen, Zaharia & Zou (2023) mostraram GPT-4 oscilando 97.6%→2.4% entre versões — dois "GPT-4" **não são o mesmo instrumento**. E a lógica de batch effect (Leek; Soneson) é cristalina: a pergunta decisiva não é "cada instrumento é confiável?", é **"a identidade do instrumento está confundida com a variável analítica?"**. No caso da Ana, está: Fable-5 codifica *só itens-com-imagem*; opus pegou os lotes anteriores; logo `coded_by` correlaciona com data, fonte e provavelmente regime. Quando ela reportar que o regime militar tem endurecimento mais alto, ela não *poderá saber* se é fato sobre as imagens ou artefato de qual modelo codificou quais imagens. Instrumento e sinal "inter-misturados e indistinguíveis". Cada instrumento novo é uma nova batelada confundida.

## d. O princípio mais profundo

**Conhecibilidade é anterior a qualidade.** O Corpus Vivo otimiza qualidade; mas um corpus de qualidade superior cujo estado é desconhecível vale empiricamente *menos* que um corpus modesto cujo estado é fixo e auditável. A ciência empírica não troca em "o melhor dado possível"; troca em "uma afirmação que pode ser provada falsa". Dado magnífico sobre o qual nada pode ser refutado é lixo bonito. A virtude que torna um número defensável não é acurácia: é a **imutabilidade do referente**. Gelman & Loken (2013) provam o resto: cada escolha contingente ao dado (qual item, qual instrumento, qual corte de regime) é um nó no *garden of forking paths* que infla falso-positivo **sem p-hacking consciente**. A única saída é a parede: **pré-especificar e congelar protocolo e N.**

## e. O extremo

Com nov/2027 chegando, **cada recode adicional é autossabotagem.** Cada ferramenta nova é uma batelada de confound; cada sessão paralela escrevendo no corpus é mais um caminho no jardim. O padrão generativo da Ana, virtude em qualquer outro contexto, *aqui é a doença*. Não há instrumento bom o bastante para salvar uma tese cujo objeto não para de se mover; superioridade técnica que aprofunda o confound é desvantagem.

A ação é uma, hoje. **Pare o churn.** Quarentene os 41 não-codificados (ausência, não N). Escolha **UM instrumento** rater-1: o estrato IconoCode homogêneo, viés constante e *caracterizável*. Não misture Fable-5 com opus sem um conjunto-âncora de sobreposição — sem overlap, não há harmonização, ponto. Corte um release: tag `corpus-v1.0`, hash, DOI, **dataset card** (Gebru) numa página. Substitua "N=165" por "N=[estrato], congelado em [data], coded_by [instrumento único]". E **escreva a tese contra esse objeto morto e defenda.** O corpus precisa morrer para a tese viver.

## f. Esqueleto inferencial

**Premissas.** (P1) Alegação empírica só é científica se falsificável por terceiros. (P2) Falsificabilidade exige referente imutável e identificado. (P3) A tese já invocou estatística frequentista, importando o contrato por inteiro (Da). (P4) O corpus não tem estado único (N 44–309 por store) e tem `coded_by` confundido com a variável (batch effect). (P5) Cada melhoria sob churn é grau de liberdade que infla falso-positivo (Gelman & Loken).

**Passos.** P1+P2 → congelar para que a alegação signifique algo. P3 → a fuga hermenêutica está vedada. P4 → congelar o estado atual não basta; descontaminar o confound antes (quarentenar, instrumento único, estratificar). P5 → descontaminação anterior ao corte; depois, a melhoria **para**.

**Load-bearing.** Tudo repousa em P2+P4: **o confound de instrumento impede representar o corpus como UM release honesto sem antes escolher/estratificar.** Se isso caísse — se uma auditoria de sobreposição mostrasse `coded_by` independente de regime/fonte/data — o pooling seria legítimo e o Corpus Vivo venceria. Mas sem conjunto-âncora essa independência é *esperada*, não demonstrada. Esperança não é proveniência. Enquanto o confound não for refutado, a única operação honesta é congelar um instrumento único. Congele o que você testa. Hoje.
