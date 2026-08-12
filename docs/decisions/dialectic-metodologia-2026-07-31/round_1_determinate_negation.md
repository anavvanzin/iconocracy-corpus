# Round 1 — Negação Determinada (análise estrutural do orquestrador)

**Data:** 2026-07-31 · **Insumos:** `round_1_monk_A.md` (Fable) + `round_1_monk_B.md` (Opus) + briefing.
**Nota de execução autônoma:** o hard stop de Fase 4 (apresentar à usuária antes da síntese) foi adaptado — a sessão corre sem a Ana presente; esta análise e tudo que segue são **proposta para adjudicação a posteriori**, no padrão da casa ("nada aqui executa sozinho"). Os pontos onde a resposta dela redirecionaria o processo estão marcados com ⚖.

---

## 0. Checagem de descorrelação

Os monks divergiram em **framework**, não só em conclusão — descorrelação genuína:

- **Monk A** argumenta no plano da *pragmática epistêmica*: o que o coeficiente **reivindica** quando aparece num texto (uma epistemologia de medição), e o que sua exibição **faz** retoricamente perante a banca. Framework: teoria do ato de fala metodológico.
- **Monk B** argumenta no plano da *empiria do ledger* e da *crítica textual*: o que o coeficiente **é** materialmente (colação de testemunhos) e o que o repositório **contém de fato** (zero sobreposição; 48,5% de proveniência-rotina; três achados de integridade devidos ao IRR). Framework: filologia + inspeção forense do dado.

A heterogeneidade de modelos (Fable vs Opus) produziu diferença de *método probatório*: A cita decisões e estruturas; B foi contar linhas do JSONL. Nenhum dos dois é espelho do outro.

## 0.5 Convergências surpreendentes (mais importantes que as divergências)

1. **Ambos negam que o coeficiente seja "confiabilidade intercodificadora".** A: "não é confiabilidade intercodificadora — é outra coisa vestindo a roupa dela". B: "Chamá-lo assim é o erro que envenena os dois lados". **O aparato importado da análise de conteúdo está morto nos dois ensaios.** Ninguém na sala defende a posição que o relatório de deep research atacou. A pergunta original ("importar ou não o aparato da análise de conteúdo?") já foi respondida por unanimidade: **não** — e nem por isso a contradição desapareceu, o que prova que ela nunca foi sobre isso.
2. **Ambos terminam com a história IRR dentro do Cap. 2.** A: "narração, não deleção — citados no Cap. 2 como evidência de que a recusa foi conclusão de quem rodou o teste". B: "parágrafo curto no corpo, tabela integral no aparato". A distância textual entre "narrar o experimento com seu rastro" e "reportar o número com sua leitura" é milimétrica.
3. **Ambos rejeitam o F2.5 como está escrito.** A corta o alvo ≥ 0,67 e o item inteiro; B corta o alvo ≥ 0,67 e o nome. **Nenhum monk defende o statu quo do plano.** A compatibilização F4.5 ("IRR = auditoria interna, não fundamento epistêmico") é rejeitada pelos dois: A prova que ela desaba ("e se desse 0,3?"); B a torna desnecessária ao assumir abertamente o peso epistêmico (o α decide o que poola).

O desacordo residual real, depurado das convergências, é estreito e preciso:

| Eixo | Monk A | Monk B |
|---|---|---|
| A colação **continua sendo produzida** daqui em diante? | Não — experimento encerrado, `legacy_frozen`; `compute_irr.py` vira ferramenta de engenharia | Sim — conjunto de sobreposição entra em `purification.jsonl` (item novo na F1); colação vira rotina |
| O número tem **função probatória** sobre o que a tese pode afirmar? | Nenhuma — estratificação decidida por adjudicação, não por α | Sim — "regra de partição": α decide o que poola e o que estratifica |
| O número aparece **no corpo** do Cap. 2? | Só como narrativa histórica do experimento | Como parágrafo com valores + remissão ao aparato |

## 1. Tensões internas (onde a lógica de cada um se trai)

### Monk A
- **A1.** A defesa central de A — "o ledger é a auditoria mais rica; cada juízo tem nome, versão, data e juíza" — é **falsa como descrição do ledger atual**. B verificou: 48,5% do corpus tem como "codificador" o nome de uma rotina de ingestão; 15 registros têm assinatura `ana`. O melhor argumento de A descreve o ledger que a F1 *promete*, não o que existe. A prova de A depende de trabalho futuro tanto quanto a de B.
- **A2.** O discurso em primeira pessoa de A à banca ("rodei o seu teste seis vezes... o que aprendi com eles está no Capítulo 2") é **instável exatamente como A acusa o F4.5 de ser**. Narrar seis experimentos cujos resultados numéricos estão commitados num repositório público *sem dizer os números* convida a pergunta que B formulou: "por que os kappas sumiram do capítulo?". A "narração sem deleção" de A implica logicamente a exibição que A proíbe. No limite, a posição de A desaba na de B no único ponto em que se distinguem.
- **A3.** A concede que "a serialidade de uma moeda não se vota, se exibe" — admitindo uma classe de atributos onde propriedade estável + convergência de observadores **valem** (a epistemologia que A declarou "não fraca, falsa" em geral). A universalidade da alegação ontológica de A morre dentro do próprio ensaio; sobra uma tese *particional* que A nunca formaliza — mas B sim (regra de partição).

### Monk B
- **B1.** B expulsa o limiar pela porta ("cai o alvo ≥ 0,67 como portão de aprovação") e o readmite pela janela: a "regra de partição" — *o α decide o que poola* — é funcionalmente um limiar. Decidir exige um valor de corte; B nunca o declara, porque declará-lo reinstalaria a lógica de aprovação que ele acabou de condenar. O classificador sem corte declarado é um portão com a placa coberta.
- **B2.** O texto proposto por B para o Cap. 2 afirma que o coeficiente "mede quanto de cada atributo pertence à imagem e quanto pertence a quem a observa" — uma decomposição de variância que **instrumentos correlacionados não licenciam** (ponto de A que B nunca refuta: LLMs compartilham corpora de treino; o α = 0,874 opus×fable em `monocromatizacao` que B mesmo chama de "parentesco de família" prova que concordância alta ≠ propriedade da imagem). B usa contra si o próprio achado: se concordância alta pode ser parentesco, o coeficiente **não** separa imagem de observador — só separa observador de observador.
- **B3.** Ao responder "e se desse 0,3?" com "já deu, e o plano B é o plano vigente" — quatro regras sobre o que a tese *pode afirmar* —, B **confirma o argumento (d) de A**: o coeficiente carrega peso epistêmico pleno (decide o escopo das afirmações da tese). A tese de B é honesta nisso, mas então a briga não é "auditoria interna vs fundamento" — é *qual* fundamento. B ganhou a compatibilização F4.5 de presente e a devolveu.

## 2. Suposição compartilhada (a dobradiça)

**Ambos assumem que o significado do número é determinado pelo seu enquadramento textual** — A: a roupa importa o aparato normativo inteiro ("a roupa é que a banca vê"); B: mudar o nome ("auditoria de estabilidade", "colação") e o lugar (aparato, não corpo) muda o que o número é. Os dois acreditam em batismo: que se controla a recepção de um número controlando seu rótulo. ⚖ A experiência real de arguição diz outra coisa: a banca lê o número no registro *dela*, não no da tese — e é exatamente por isso que a pergunta pendente desde 2026-06-19 ("a banca aceita rigor = auditabilidade hermenêutica?") continua sendo o input-do-mundo-real que nenhum monk pode fornecer.

**Segunda suposição compartilhada, mais profunda:** ambos assumem que a tese fará (ou não fará) **afirmações corpus-transversais** sem jamais perguntar *quais afirmações a tese fará*. A discute como se toda alegação probatória fosse leitura exemplar (caso a caso, indiciária); B discute como se a tese fosse afirmar padrões de corpus ("distribuição de recusas por suporte", "coexistência sincrônica em França 1900"). Nenhum verificou no plano o que a tese pós-virada realmente afirma. **Verificação do orquestrador:** o plano §6.5 mantém explicitamente "a economia de corpos executável — o corte sincrônico (Estado × ano × corpos ativos)... de tese em consulta reprodutível" — uma afirmação corpus-transversal viva; e §6.4 mantém co-presença de atributos como *heurística* de montagem ("a máquina propõe, a autora dispõe"). Ou seja: a tese pós-virada contém **os dois tipos de alegação**. A contradição entre os monks é a projeção de uma partição real e não-nomeada *dentro da tese*.

## 3. Proteção de posição

- **A protege a soberania do juízo da autora** — que nenhum número vincule a tese; a adjudicação como instância final não-subordinável.
- **B protege as alegações da tese contra o confound de instrumento** — que nenhum padrão afirmado seja artefato de qual máquina codificou qual lote.

Ambos protegem **a tese** contra modos de captura diferentes: captura epistêmica por um padrão alheio (A) vs captura empírica pelo próprio pipeline (B). Como na rodada de 2026-06-19, os dois guardiões vigiam portas diferentes da mesma casa — e nenhum ataque que um teme entra pela porta que o outro guarda.

## 4. A pergunta oculta

Não é "kappa ou não kappa". É: **que tipos de afirmação sobre o corpus-enquanto-corpus a tese pós-virada faz, e qual gramática probatória cada tipo exige?**

A disputa do coeficiente é uma guerra por procuração sobre essa partição não-declarada. Se toda afirmação probatória da tese for leitura exemplar (indiciária, caso a caso, adjudicada), o confound de B jamais toca uma alegação e a recusa de A é estruturalmente suficiente. Se a tese afirmar padrões transversais (§6.5 afirma), o silêncio sobre estabilidade inter-instrumento deixa essas frases específicas sem defesa — e nenhuma quantidade de Ginzburg as cobre, porque Ginzburg licencia o indício, não a agregação.

Corolário que nenhum monk enxergou por inteiro: **a resposta à pergunta "e se o α desse 0,3?" não é binária (mudar/não mudar a tese) — é "muda o escopo da frase"**. A afirmação corpus-transversal que não sobrevive à colação não é abandonada nem mantida: é **reescrita como leitura estratificada ou heurística de montagem**. O coeficiente não aprova nem decora: **roteia alegações entre registros probatórios**. A terceira resposta que A declarou inexistente existe — e B a praticou nas suas quatro regras sem nomeá-la.

## 5. Decomposição boydiana

**Partes atômicas (despidas da origem):** epistemologia-reivindicada-pelo-número · limiar-importa-aparato-normativo · número-fraco-exibido-pior-que-nenhum · ledger-como-auditoria · meio-kappa-recompõe-o-composto · narração-não-deleção · dilema-do-0,3 · colação-de-testemunhos · aparato-crítico-filológico · sobreposição-zero (fato) · proveniência-rotina-48,5% (fato) · três-achados-de-integridade (fato) · números-já-públicos · desacordo-como-medida-do-labor-da-adjudicadora · regra-de-partição · plano-B-já-vigente.

**Conexão trans-domínio (o material de fora):** a **edição crítica / ecdótica**. B a invocou como metáfora; nenhum dos dois a construiu como *arquitetura*. Na filologia: o **corpo da página imprime o texto estabelecido** (o juízo do editor, adjudicado, em prosa contínua); o **pé da página imprime o aparato de variantes** (a colação integral, técnica, com siglas de testemunhos); e há dois séculos ninguém acusa um editor crítico de "positivismo" por imprimir variantes, nem de "impressionismo" por estabelecer o texto. A disciplina que resolve "número exibido sem assinar epistemologia de medição" **existe, é das humanidades, e é anterior à análise de conteúdo**. O medo de A (exibir = assinar) é refutado por precedente disciplinar; a exigência de B (imprimir integral) é satisfeita estruturalmente subordinada.

**Segunda conexão:** dilema-do-0,3 × plano-B-já-vigente → **roteamento de alegações** (a terceira resposta). A gramática de registros: cada frase corpus-transversal da tese declara seu registro — *colacionada* (sobreviveu à sobreposição; número ao lado), *estratificada* (vale dentro de um instrumento/lote; dito), *heurística* (montagem warburguiana; propõe, não prova). O α é a **evidência** que a adjudicadora usa para rotear — não o roteador. Isso desfaz B1 (não há corte: quem roteia é a autora, com o número na mesa e trilha no ledger) e desfaz o dilema de A (o número compromete — mas compromete a *gramática da frase*, não a tese).

## 6. Registro de desajuste (misfit register)

- A alegação de B de que o coeficiente separa "imagem de observador" **não sobrevive** (B2) — a versão sóbria é "separa observador de observador", e é suficiente para o roteamento.
- A alegação de A de que "o ledger é mais rico que o número" **não sobrevive como está** (A1) — depende da F1; a versão sóbria é "o ledger *completado* + colação são camadas complementares".
- O resíduo institucional segue vivo e é **input do mundo real**: ⚖ a banca aceita a gramática de registros? (herdeiro direto da pergunta pendente de 2026-06-19; só a Ana/orientação responde).
- Resíduo técnico novo, produzido pela verificação de B: **a "base natural do kappa" está vazia** (zero sobreposição em `purification.jsonl`). Qualquer que seja a decisão, o estado atual não sustenta *nem* a narração de A (que pressupõe experimentos bem-formados sobre o corpus vigente v2) *nem* a colação de B — os IRRs de maio–junho rodaram sobre o desenho pré-virada. ⚖ Se houver colação futura, ela precisa ser re-executada sob o codebook v2.2.x.

## 7. Critérios de sublação (herdados do briefing + agudizados)

1. Não pode ser salomônica → o teste agora é específico: não pode ser "A fica com o corpo do texto, B fica com o apêndice" **sem uma regra que os conecte** (a gramática de roteamento é essa regra; sem ela, é só divisão de território).
2. Teste abdutivo: deve tornar previsível por que A e B existem → cada um universalizou um registro probatório da tese (A: exemplar; B: transversal) que a tese pós-virada realmente contém em §6.4/§6.5.
3. Autoridade real: deve dizer o que a Ana adjudica e o que o texto responde por si.
4. Consequência operacional: destino de F2.5, F1, Cap. 2, apêndice, boletim IRR.

## 8. Anti-pattern-matching: comparação com o palpite inicial

Palpite pré-ensaios (registrado em scratchpad antes da Fase 3): "realocar o coeficiente de fundamento epistêmico para auditoria de instrumento em apêndice; cortar o alvo 0,67; leitura perspectivista; pergunta oculta = relação da tese com seus instrumentos". **O palpite acertou a realocação e errou o essencial:** (i) não previu que ambos os monks matariam a "confiabilidade intercodificadora" — a realocação já era consenso, não síntese; (ii) não previu a arquitetura da edição crítica (corpo/aparato) como precedente disciplinar que dissolve o medo de A; (iii) não previu a gramática de roteamento de alegações nem a terceira resposta ao dilema do 0,3; (iv) não previu os dois fatos empíricos que mudam o problema (sobreposição zero; proveniência-rotina 48,5%). A síntese da Fase 5 deve ser construída sobre (ii)–(iv), que não estavam no palpite — se ela se reduzir ao palpite, terá sido pattern-matching e deve ser refeita.
