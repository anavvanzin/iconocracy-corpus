# Round 2 — Auditoria Hostil (agente fresco, barreira de abstração)

> Fase 6. O auditor leu apenas os dois ensaios R2 + a sublação R2 e verificou fatos contra o repositório (inclusive bibliografia e ledger). Parecer integral abaixo; disposição de cada achado em `round_2_sintese_final.md`.

## Auditoria Hostil — R2

Verifiquei todas as alegações numéricas contra o repositório. Passam: os **6 placeholders** (6 URLs distintas em `records.jsonl`), os **21 painéis Zwischenraum** (`companion-data.json`), e o defeito do glossário apontado por A (`concepts/glossario.md:43` traz "Purificação Clássica" sem definição — real). Segue o resto.

### Premortem (nov/2027)

**1. [GRAVE] A Semeuse é prata.** O emblema escolhido para "emissão fiduciária por construção" é o franco de 1898 — moeda de prata 0,835, União Monetária Latina: espécie metálica, lastro intrínseco, resgatável por fusão. O parecerista marxista pergunta uma frase ("a senhora sabe que essa moeda *era* o lastro?") e o corolário inteiro cai junto com o exemplo. *Correção mínima:* abandonar a moeda como caso de fiduciariedade e restringir a analogia ao suporte **papel-moeda** (que existe no corpus), ou abandonar a analogia.

**2. [GRAVE] Corrida ao banco está tecnicamente invertida.** Corrida é fenômeno de emissor **conversível** com reserva fracionária, que prometeu resgate e não honra. Emissor puramente fiduciário na própria unidade *não sofre corrida* — sofre inflação, repúdio, crise cambial. Logo, pelo mapeamento da própria síntese, "contra-alegoria = corrida ao banco" pertence ao regime **conversível**, isto é, ao lado da editora, não ao da iconocracia. O léxico se autocontradiz. Agrava: só **9 de 279** registros são `contra-alegoria` (3,2%) — o termo mais vistoso do corolário repousa em 9 itens.

**3. [GRAVE] Fiat é legítimo; ouro não é inocente.** Toda moeda moderna é inconversível e nem por isso ilegítima; a conversibilidade-ouro conviveu com extração colonial e escravista. "Conversível = legítimo / irresgatável = iconocrático" é normativamente vazio — prova o oposto do que a síntese quer. E *curso forçado* é ato legislado e datável (França 1848; 1870–1878; 1914), reversível: o contrário de "por construção". O parecerista de história do direito que despreza metáforas econômicas não precisa nem entrar: o marxista já demoliu, e ele conclui que a tese trocou análise por alegoria conceitual.

### Derrotadores (Pollock)

**4. [GRAVE] A premissa ontológica é um erro de tradução.** Toda a rodada assenta em `concepts/economia-iconica.md`, que glosa Mondzain como "a form of economic currency" citando *Image, a modern magic: the life of images in the west* (Stanford, 2002) — título que **não existe** na bibliografia canônica da tese. `vault/tese/references.bib:172` traz Mondzain 2002 = *Image, icône, économie: les sources byzantines de l'imaginaire contemporain*: a *oikonomia* patrística/bizantina (dispensação encarnacional, administração), explicitamente **não** economia monetária. O arquivo-fonte declarado na nota (`raw/articles/iconocracia-companion-web.md`) não existe no repositório. Derrotador direto de (i) e (ii): "fixar é emitir moeda" não é conceito do glossário da tese — é um deslize de nota derivada, e a bibliografia da própria autora o refuta.

**5. [GRAVE] O lastro não existe.** `purification.jsonl`: 279 registros, **279 ids únicos, zero itens com mais de uma codificação**. `FR-013` tem uma só codificação (`iconocode-opus`, `dessexualizacao: 2`, numérico) — sem `fable`, sem `ana`. O exemplo repetido em R1, nos dois monks e na síntese ("opus=moderado · fable=mínimo · ana adota mínimo") é **ficção, não registro**. A síntese afirma no presente e como estrutura ("a reserva co-circula **por construção**") algo que é migração F1 pendente. Pelo próprio critério, a nota da tese é hoje 100% fiduciária. *Correção mínima:* trocar todo o tempo verbal para condicional e tornar a conversibilidade uma **meta com pré-condição F1**, não uma propriedade.

**6. [MÉDIO] "Garante resgatabilidade, não atenção" não fecha (iii).** Combinado com o achado 5, o que se garante é resgatabilidade *nominal* sem reserva — a definição econômica de conversibilidade suspensa. E a objeção Trouillot fica intocada: a reserva é ela mesma artefato codificado; resgatar codificações não devolve o silêncio produzido na codificação.

### Mesmo-arranjo

**7. [GRAVE] É a rodada 1 rebatizada.** Consequência #1: "texto estabelecido + aparato + registro + gramática: tudo de pé". #7 é o item de A. #2 adia o gênero. As duas únicas regras executáveis novas — "nenhuma entrada de aparato sem as lições divergentes" e "atributo instável ⇒ divergência no corpo" — enunciam-se sem uma sílaba monetária. Teste: nomeie algo que R2 proíbe, R1 permitia, e que **exija** a palavra "lastro". Não há. Monk A venceu com o vocabulário de B.

### Reversibilidade (Boyd)

**8. [MÉDIO] O material monetário é ornamento não-fontado.** Nenhum teórico monetário é citado em R2 (nem Knapp, Ingham, Graeber, Simmel; nem UML, nem literatura sobre *cours forcé*). O domínio [PESQUISA] do briefing era ecdótica; a teoria monetária entrou como domínio novo e a própria síntese se autocertifica ("material externo declarado") — circular. Alegação órfã de fato, apesar do "sem alegações órfãs".

**9. [MÉDIO] Aritmética herdada sem inspeção.** "48,5%" = 159 (numerador de `purification.jsonl`, N=279) sobre 328 (`records.jsonl`). Pelo mesmo conjunto: **159/279 = 57,0%** (ou 130/279 = 46,6% na definição estrita de rotina). A síntese *eleva* esse número a "reserva não-escriturada" sem recalcular.

**10. [MENOR] A licença é CC0 1.0**, não "CC-BY-4.0" (Monk A §3d) — e ela é um dos quatro componentes da reserva.

### Executabilidade

**11. [GRAVE] O corolário não tem instrumento.** "Endurecimento = índice da distância entre a nota e a reserva destruída" exige medir a reserva; os 10 indicadores medem propriedades formais da imagem. Notebooks 01–08 rodam sobre escores; não há variável de reserva. Adotá-lo nos Caps. 5–6 é deriva de construto pós-hoc a 16 meses. **Colapsa primeiro:** validade de construto do Cap. 6; depois a tipologia de regimes (144/98/28/9). *Correção:* ficar na opção "quadro reflexivo do Cap. 2 apenas" de ⚖1.

**12. [MÉDIO] Risco de autoria.** Rotear o conceito autoral #4 (matriz jurídica Kantorowicz/Legendre/Hespanha) por uma ontologia derivada de Mondzain é exatamente a cessão que o CLAUDE.md pede para evitar.

### Compromise-check

**13. [GRAVE] "Ambos são emissões conversíveis; a epistemologia não decide" é abdicação.** Corpo+aparato (A) vs dossiê sinóptico (B) *era* a contradição da rodada. Um critério que não discrimina as duas alternativas que ele foi convocado a discriminar não é síntese — é divisão adiada. Conversibilidade só condena higiene de escrituração (placeholders, `coded_by`). Pela regra do próprio A, "um critério que não pode condenar é decoração".
