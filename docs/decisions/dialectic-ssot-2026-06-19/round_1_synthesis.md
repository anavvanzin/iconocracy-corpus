# Round 1 — Synthesis (Aufhebung)

## The synthesis
**O corpus da Iconocracia é um ARTEFATO HERMENÊUTICO VERSIONADO, governado por uma disciplina de APARATO CRÍTICO.** A fonte-única-da-verdade não é um banco vivo nem a prosa solta — é uma **sequência de RELEASES analíticos congelados, versionados no git**, cada um composto de:
1. um **snapshot legível** dos registros (o estado de codificação naquele corte),
2. um **aparato de codificação** — o racional dos juízos contestados/revisados e os motivos de quarentena (como *variant readings* numa edição crítica),
3. um **dataset card** — o que cada uma das 10 dimensões significa, o N e seus estratos por instrumento, e a declaração explícita dos DOIS sentidos de "reprodutibilidade".

## Por que é Aufhebung (não compromisso)
- **Cancela** o binário dataset-XOR-hermenêutica e DB-XOR-prosa.
- **Preserva** a falsifiabilidade/auditabilidade de A *e* a ontologia interpretativa + escassez-de-atenção de B.
- **Eleva** para uma tecnologia de proveniência **nativa das humanidades** (o apparatus criticus, 500 anos de filologia): torna o juízo interpretativo rastreável e contestável **sem** convertê-lo em medição com "valor verdadeiro".

## Os movimentos concretos
1. **Git É o log de eventos — de graça.** Cada release é um commit/tag; o diff entre releases é o "o que mudou e por quê" (a mensagem de commit carrega o racional). Não precisa de event-sourced DB separado para proveniência.
2. **Proveniência-de-juízo, não de-medição.** O aparato registra POR QUE um coding é o que é. Codings contestados/revisados levam nota — como leituras variantes. Satisfaz A (a leitora re-audita o juízo) sem o positivismo de B (é prosa+estrutura, não um log de transição de um valor-fantasma).
3. **Escritores consolidados pela disciplina de release**, não por lock de DB: entre releases, UMA cópia de trabalho é canônica (git main); ferramentas propõem mudanças como commits/PRs, não escrevendo em arquivos espalhados. (Resolve a raiz "multi-ferramenta → consolidar" via workflow git.)
4. **O DB é infra OPCIONAL e adiada — e INVERTIDA:** se/quando consulta/dashboards exigirem, um SQLite vira um **índice derivado**, reconstruído dos releases git — nunca o mestre. (Inverte a escolha inicial: DB como projeção; releases-git como verdade.)
5. **Renomear o alvo (misfit Foucault):** não "single source of truth" (fóssil de engenharia) — **"versão canônica de referência"** (versioned record). O nome importa metodologicamente.
6. **Declarar a indecidível (misfit Derrida):** o dataset card declara que "reprodutibilidade" tem dois sentidos — estatística (re-rodar) e hermenêutica (leitora competente chega a leitura comparável) — e que a tese reivindica o segundo, exibindo o primeiro como ilustração.

## Reversibility check (Boyd) — cada claim traça a um átomo
fixity→freeze; datability→git tag; justification-trace→aparato; falsifiability→juízo re-auditável; low-cost→git grátis + incremental; no-false-precision→racional em prosa; interpretive-ontology→modelo de variantes; single-writer→workflow git; deterministic-exports→releases. ✓ Sem claim órfão.

## Sequência (o "o que primeiro" — domínio estratégia exige)
1. **Reconciliar a divergência:** adotar o corpus verdadeiro atual (origin/main = 309) e resolver o fork local stale. *(Pré-requisito de tudo — sem isso não há o que congelar.)*
2. **Congelar `v-atual`** como primeiro release: snapshot + tag git + dataset card mínimo.
3. **Escrever o template do aparato** (campos: id, coding contestado, racional, revisões, motivo de quarentena).
4. **Declarar os dois sentidos de reprodutibilidade** no dataset card.
5. **Retomar a escrita** — o aparato ACRESCE por alegação analítica (quando um capítulo usa um coding, documenta-o), não upfront para os 309. Custo amortizado.

## Cost budget (owning the Adorno residue)
Custo único: template do aparato + primeiro release congelado + reconciliação do fork (~1–2 sessões). Depois, cada release é barato (tag + atualização do card). Justificado contra 2027: é o que torna os capítulos estatísticos defensáveis E é MUITO mais barato que manter um DB event-sourced vivo. O aparato cresce com a escrita, não a substitui.

## Model update
- **Antes:** "Preciso de um SQLite event-sourced como fonte única da verdade."
- **Depois:** "Preciso de uma disciplina de aparato crítico — releases congelados versionados no git + racional de codificação — como versão canônica de referência; o DB é índice derivado opcional."
- **Porque:** a contradição revelou que ambos os monks convergiam num snapshot congelado documentado, e que a proveniência-de-juízo (não de-medição) já tem uma tecnologia humanista nativa que o git implementa de graça.

## Dialectic queue (contradições abertas p/ rodadas futuras)
1. **Reconciliação multi-máquina:** o aparato resolve a verdade-do-conteúdo, mas a divergência Mac↔SSD-Linux↔GitHub é git-workflow — merece sua própria rodada (one canonical clone? quando sincroniza?).
2. **Confiabilidade inter-instrumento** (opus vs opus-4.6) — a validade analítica DENTRO de um release (o eixo da DIALETICA-N165).
3. **O aparato como objeto de escrita:** o racional de codificação É material de capítulo de metodologia? (funde dado e prosa — a fronteira que o monk B queria).
