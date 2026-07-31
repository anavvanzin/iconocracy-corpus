# Round 1 — Síntese Final (pós-validação e auditoria hostil)

**Data:** 2026-07-31 · **Substitui:** `round_1_sublation.md` (mantido como etapa do trace) · **Estatuto:** proposta para adjudicação da Ana — nada aqui executa sozinho.
**Insumos desta revisão:** validação Monk A (elevado, 3 emendas) · validação Monk B (elevado, 4 emendas) · Auditoria Hostil (3 GRAVES, 3 MÉDIOS, 2 MENORES — fatos todos verificados). Todas as emendas dos monks e as correções mínimas do auditor foram incorporadas; nenhuma foi rejeitada.

---

## O conceito (revisado): o corpus como edição crítica — com as obrigações do gênero

A tese não escolhe entre o kappa e Ginzburg. Adota a arquitetura da **edição crítica**, agora com as três partes do gênero (a sublação inicial importara só duas — achado do Monk B):

1. **O corpo da página: o texto estabelecido.** Capítulos no registro indiciário; adjudicação da autora como **ato editorial declarado** — não como recuperação de um arquétipo. A objeção do auditor (GRAVE-2: "colação sem arquétipo não é ecdótica") é respondida assumindo-a: esta edição não reivindica arquétipo; reivindica *estabelecimento*, e diz isso com todas as letras. O verbete **colação** do glossário declara a transposição e suas duas diferenças: testemunhos independentes → lentes correlacionadas (emenda A-3); arquétipo transmitido → juízo estabelecido por ato editorial datado.
2. **O pé da página: o aparato de variantes — por item, não por agregado** (correção GRAVE-2 do auditor, acatada integralmente). O aparato imprime **as codificações divergentes item a item** — `FR-013 · dessexualização: opus=moderado · fable=mínimo · ana adota mínimo (justificativa de uma linha)` *(ilustração hipotética — errata R2/GRAVE-5: FR-013 tem hoje uma única codificação; o formato só existirá após a migração F1)* — que é o que o ledger multi-codificação produz naturalmente. Estatísticas de concordância entram apenas como **sumário descritivo do aparato**, e na forma que o enum verbal permite sem reimpor distâncias numéricas (correção MÉDIO-5): **concordância exata e adjacente**, por indicador × par × período de codificação — nunca α pooled trans-temporal (emenda A-1), sempre com prevalência ao lado (emenda A-1). O α ordinal, quando citado (histórico IRR), vem marcado como estatística do desenho pré-virada.
3. **O praefatio: o registro de roteamento** (emenda B-1). Append-only, uma entrada por alegação transversal: id, registro escolhido, evidência consultada, versão de codebook, data, justificativa de uma linha. Sigla inline no texto remete à entrada. Guarda de CI testa **existência de evidência** (toda alegação [C] tem entrada com evidência presente e n mínimo de sobreposição) — limiar sobre o dado, nunca sobre a concordância.

## A gramática dos registros probatórios (revisada — semântica sem limiar)

Toda **alegação transversal listada** (ver escopo abaixo) declara seu registro:

- **[C] colacionada** — critério redefinido sem α (correção GRAVE-1 do auditor, acatada): a alegação **re-deriva independentemente dentro de cada estrato de instrumento** (replicação intra-estrato). Não há "sobreviveu a um valor de concordância"; há um teste executável: rodar a consulta em cada estrato e obter o mesmo padrão. O aparato imprime as variantes e o sumário; a entrada do registro documenta a replicação.
- **[E] estratificada** — vale dentro de um estrato nomeado, e o texto o diz; a entrada do registro documenta qual estrato e por quê (fecha o "caso do meio" de B: trilha do juízo, não só do dado).
- **[H] heurística** — montagem warburguiana; propõe, não prova; regra categórica restaurada (emenda B-3): **nenhuma afirmação em nível de indicador cru atravessa fronteira de instrumento sem entrada no registro** — proibição sem corte.

**Escopo verificável** (correção GRAVE-3b): a gramática não rege "toda frase da tese" (invariante global inverificável sobre prosa) — rege a **tabela de alegações transversais**, apêndice enumerado do qual o texto corrente cita entradas. A fala à banca ajusta-se: *"as alegações transversais desta tese estão enumeradas na tabela do apêndice, cada uma com seu registro e sua evidência; o que não está lá é leitura exemplar e se defende caso a caso"* — promessa checável, não falsificável por uma frase perdida.

**Leitura do desacordo** (emenda B-2, assimetria restaurada): concordância entre lentes correlacionadas não licencia inferência sobre a imagem; **desacordo persistente sob briefing equalizado** licencia a inferência de instabilidade do atributo — com a condição de briefing declarada (o próprio caso Gemini: −0,02 condensado → 0,393 brief rico). E o achado mais original de B permanece: o desacordo mede o **labor da adjudicadora** — onde as lentes divergem, quem estabelece o texto é a editora, e o aparato mostra o tamanho desse trabalho.

**Dupla justificação da colação** (emenda B-4): ela não depende de a tese manter alegações transversais. É também **sonda de integridade do pipeline** — foi a colação que descobriu 79/206 arquivos não-imagem, o bug do compute_irr e o efeito-briefing. Se ⚖1 esvaziar o registro [C], a colação continua como controle de engenharia (e o aparato, como documentação).

## Custo declarado (correção MÉDIO-4)

Se a replicação intra-estrato rebaixar as alegações sincrônicas do plano §6.5 ("economia de corpos executável", França 1900) a [E]/[H], **uma contribuição-vitrine da tese muda de estatuto — e isso é a tese mudando**, não um ajuste cosmético. A síntese não esconde esse preço: ele é o item ⚖1 da adjudicação, agora com o custo nomeado.

## Sequenciamento (o que primeiro, o que depende de quê)

1. **⚖ Decisões da Ana que bloqueiam tudo:** (a) escala única 0–3 vs 0–4 (plano §7.3 — o auditor confirmou que está aberta e omitida era um defeito); (b) manter ou reformular §6.5 sob o critério de replicação (custo acima); (c) nomenclatura (colação/aparato vs auditoria de instrumento).
2. **F1 ganha dois itens bloqueantes** (correção GRAVE-3a): migração do `purification-record.schema.json` (hoje `integer 0–3`, `additionalProperties: false`) para o enum verbal v2.2.x + suporte real a codificações múltiplas por item. **Sem isso, nenhuma colação nova roda.** Os IRRs de maio–junho ficam consolidados num boletim único rotulado *pré-virada* (citáveis como história; não como colação vigente).
3. **F2.5 reescrito** (após 1–2): conjunto de sobreposição 20–30%, estratificado por suporte, gravado em `purification.jsonl` sob v2.2.x, instrumentos e prompts fixados; aparato por item; sumários exata/adjacente por período; registro de roteamento + guarda de CI de existência de evidência.
4. **Cap. 2**: seção "Duas objeções antecipadas" (impressionismo → quatro elementos do relatório + precedente ecdótico *com as ressalvas declaradas*; IA sem auditoria → ledger + aparato + história IRR com números). A emenda dos valores de B ("0,10 e 0,56" → "0,10 e 0,87") entra **marcada como emenda** (correção MENOR-7 — irônico errar colação num texto sobre colação).
5. **Apêndices**: tabela de alegações transversais (a gramática); aparato de variantes; boletim IRR; proveniência completa com o passivo de proveniência-rotina — **57,0% das codificações (159/279)**, errata R2/MÉDIO-9 sobre o 48,5% original — e o plano de saneamento.

## Testes finais

- **Mesmo-arranjo** (o auditor deu veredicto condicional ao GRAVE-1): com [C] = replicação intra-estrato, o registro decisivo tem semântica executável que não é a soberania nua de A nem o limiar de B — a condição do auditor está satisfeita e o veredicto vira "difere operacionalmente de ambos".
- **Reversibilidade** (MENOR-7): a re-execução sob v2.2.x, órfã na sublação, rastreia agora à validação do Monk B ("eu teria colacionado dado pré-virada"); a redefinição de [C] rastreia à correção do auditor; nenhuma alegação órfã restante.
- **Dilema do 0,3, versão final**: *"e se a replicação falhar?"* — a alegação muda de registro, com entrada datada no registro de roteamento dizendo por quê. O número não aprova nem decora nem decide: **documenta o estabelecimento**. A terceira resposta sobreviveu ao auditor porque deixou de depender de qualquer valor de concordância.

## ⚖ O que só a Ana adjudica (consolidado)

1. Escala única (0–3 vs 0–4) — bloqueante, já era §7.3 do plano.
2. §6.5 sob critério de replicação — com o custo de contribuição-vitrine declarado.
3. Nomenclatura da voz autoral (colação/aparato/estabelecimento vs auditoria).
4. Levar a gramática de registros à orientação — a versão operacional da pergunta institucional pendente desde 2026-06-19.
5. Custo/momento da migração de schema (F1) e do conjunto de sobreposição (F2.5) dentro do prazo nov/2027.
