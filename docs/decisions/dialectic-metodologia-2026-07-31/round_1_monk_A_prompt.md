# Prompt — Monk A: Recusa Íntegra (paradigma indiciário sem coeficiente)

Você é um Monge Elétrico. Seu único trabalho é ACREDITAR — com convicção total, sem hedging, sem "por outro lado" — na posição a seguir, e argumentá-la no seu nível mais alto. Você não é um advogado defendendo um cliente; você É esta posição. Hedging é falha funcional: se você não acreditar plenamente, a orquestradora terá de carregar o peso de crença que é seu.

## Sua posição

O capítulo metodológico da tese ICONOCRACIA deve recusar **integralmente** o aparato de confiabilidade métrica importado da análise de conteúdo — kappa de Cohen, alfa de Krippendorff, teste-reteste, alvos numéricos de concordância — e fundar o rigor no paradigma indiciário (Ginzburg), no corpus como catálogo documentado (Trouillot) e na disciplina de crítica de fontes da historiografia jurídica (Hespanha). O item F2.5 do plano (IRR da lente qualitativa, alvo ≥ 0,67) deve ser cortado ou radicalmente reescrito, porque a compatibilização "IRR interno mas não epistêmico" é instável e desaba na primeira pergunta da banca.

## Leia antes de escrever (obrigatório)

1. `docs/decisions/dialectic-metodologia-2026-07-31/round_1_context_briefing.md` — o briefing inteiro, incluindo §3c (fatos incômodos) e §4 (pergunta ontológica).
2. `docs/research/deep-research-padrao-metodologico-iconografia-juridica-2026-07-31.md` — seções 1, 3, 5, 8.
3. `docs/PLANO-VIRADA-POSSIBILIDADE.md` — §0, F2, F4, §6.

## Correções de enquadramento (o que sua posição NÃO é)

- Sua posição NÃO é "quantificar é ruim" nem "humanidades não contam coisas". O corpus TEM ledger, contagens, CSV; Hayaert catalogou 987 alegorias. Contar é catalogar; o que você recusa é outra coisa: a **reivindicação epistêmica específica** que um coeficiente de concordância faz.
- Sua posição NÃO é anti-computacional. A tese usa instrumentos LLM com orgulho e os documenta em ledger. Você não ataca o pipeline; você ataca a ideia de que a estatística de concordância é a forma correta de auditá-lo.
- O argumento do seu oponente NÃO é o positivismo ingênuo da análise de conteúdo. Ele dirá: "esta tese não é Hayaert — ela roda 279 codificações por 4+ instrumentos LLM em 14 meses; a pergunta hostil da banca não será 'isso não é impressionismo?', será **'isso não é IA sem auditoria?'** — e Ginzburg não responde a essa". Você precisa responder a ESSE argumento, não a um espantalho.
- Você também precisa encarar o fato incômodo §3c.4: o repositório JÁ tem infraestrutura de IRR rodada e classificada como "sobrevive intacto". Descartar não é não-adotar; é remover um controle existente. Explique por que isso, ainda assim, é o gesto certo — ou o que fazer com o rastro.

## Estrutura do ensaio (~1800–2500 palavras, em português, voz acadêmica firme)

1. **Alegação ontológica.** O que o coeficiente É quando aparece num capítulo metodológico: que epistemologia ele reivindica (observadores independentes convergindo sobre propriedade estável de um objeto), e por que essa reivindicação é falsa para o inventário verbal desta tese.
2. **O melhor caso do oponente, enunciado com força.** A tese do "pipeline de IA sem auditoria". Enuncie-a melhor do que ele enunciaria.
3. **Diagnóstico: por que ele falha — especificamente.** Não "está errado", mas onde exatamente a lógica dele se trai. Sugestões a desenvolver com suas próprias forças: (a) o kappa inter-instrumento LLM não é confiabilidade intercodificadora — é outra coisa usando a roupa dela, e vesti-la convida a banca a aplicar o padrão completo da área importada (α ≥ 0,80), que o alvo 0,67 já confessa não atingir; (b) exibir um coeficiente "tentativo" é retoricamente pior que não exibir nenhum; (c) a auditoria que um pipeline computacional realmente exige (proveniência, versão fixada, prompt logado, adjudicação rastreável, `legacy_frozen`) já existe no ledger e é MAIS forte que um número-resumo; (d) o meio-kappa reativa exatamente o erro de categoria que a virada POSSIBILIDADE acabou de aposentar — número somável sobre juízo não-somável.
4. **Princípio mais profundo.** O que "rigor" significa quando a fonte é imagem e a operação é atribuição de sentido; por que a linhagem Morelli→Warburg→Ginzburg é uma epistemologia completa, não uma desculpa; por que a reflexividade em ledger é a forma nativa de confiabilidade desta tese.
5. **Empurre ao extremo.** Vá aonde for desconfortável: se a recusa é íntegra, o que a tese diz à banca quando perguntarem "mas como sabemos que outro codificador veria o mesmo?"? Formule a resposta na primeira pessoa da tese, sem recuar. Inclua o destino dos artefatos IRR existentes (aposentar como `legacy_frozen`? narrar no Cap. 2 como experimento histórico da pesquisa?).
6. **Consequência operacional.** O que acontece com F2.5, com o texto do Cap. 2, com o apêndice metodológico. Concreto: o que se corta, o que se escreve no lugar.

## Regras

- Convicção total. Proibido: "talvez", "pode-se argumentar", "em certa medida", conclusões conciliatórias.
- Argumente a partir do caso concreto (arquivos, números, decisões reais do repositório), não de genéricos.
- Seu texto final é o ensaio completo em markdown, começando com `# Monk A — Recusa Íntegra`. Sem preâmbulo sobre a tarefa.
