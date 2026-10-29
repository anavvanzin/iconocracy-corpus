---
id: CRITERIO-VINCULOS-2026-10-29
versao: "1.0"
data: 2026-10-29
status: vigente
decisao: ../decisions/2026-10-29-atribuicao-territorial-politica-institucional.md
---

# Atribuição territorial, política e institucional dos objetos

Critério transversal do workflow da tese ICONOCRACIA, adotado por orientação
expressa de Ana em 29/10/2026 a partir de observação de Georges Martyn. Aplica-se
à seleção, catalogação, análise, montagem, redação, revisão e apresentação dos
resultados, inclusive a artigos como *O contrato visual*.

## Regra e alcance

Uma associação territorial, política ou institucional precisa dizer **qual
relação está sendo afirmada, em que data/contexto e com qual fundamento**.
Nacionalidade do artista, lugar de produção, localização atual e assunto
representado não autorizam, isoladamente, atribuir uma nacionalidade única ao
objeto. Tampouco uma autoria estrangeira exclui relação documentada com o Brasil.

É obrigatório verificar o alcance da afirmação usada, não preencher todas as
dimensões possíveis. Informação desconhecida permanece desconhecida. Um `gap`
não impede a entrada ou permanência no catálogo nem invalida outras afirmações
sustentadas sobre o mesmo objeto. Impede apresentar a associação sem fundamento
como fato ou usá-la para inclusão automática na demonstração da tese.

O núcleo analítico continua **Brasil, 1822–1922**, distinto do catálogo
transnacional histórico de 1800–2000 e de seus comparanda e exceções documentadas.
País continua variável analítica, sem gate nacional, pontuação agregada ou
reclassificação automática. Para cada caso mobilizado na demonstração do núcleo,
explicitar a relação documentada com o Brasil e a pertinência cronológica, bem
como o uso argumentativo. Material externo pode permanecer como comparandum ou
no catálogo, com função declarada. Preservar os estatutos catalográficos existentes.

## Relações que não se substituem

Consultar as dimensões pertinentes à afirmação, mantendo as demais como lacuna
quando não documentadas. A tabela é um roteiro de investigação, sem criar novos
campos obrigatórios no schema.

| Relação | O que registrar e o que a evidência não autoriza transferir |
|---|---|
| Autoria e trajetória do artista | Atribuição de autoria e nacionalidade/cidadania historicamente situada, quando pertinente; não definem por si a associação do objeto. |
| Produção | Oficina, lugar, agentes e data/intervalo de produção; distinguir concepção, execução, impressão, fundição e emissão quando a questão exigir. |
| Encomenda e patrocínio | Quem encomenda, financia, emite ou adota, com fonte; encomenda, patrocínio e uso institucional são relações distintas. |
| Tema ou entidade representada | País, território, Estado, instituição ou abstração identificados; representar uma entidade não prova produção, encomenda ou recepção por ela. |
| Contexto político e jurisdição | Autoridade, regime e circunscrição na data relevante; não projetar fronteiras, nacionalidades ou instituições atuais sobre o passado. |
| Circulação, instalação e uso | Onde, quando, por quais meios e em quais dispositivos o objeto circulou ou foi usado; não presumir público ou efeito. |
| Recepção | Leituras e respostas historicamente documentadas; presença física ou circulação não demonstram, sozinhas, apropriação ou influência. |
| Conservação e aquisição | Acervo, localização atual e datas de aquisição; guarda atual não prova produção local, e aquisição não data produção. |

Separar as datas do objeto, de sua circulação, de uma intervenção/reuso e de sua
incorporação ao acervo. Registrar denominação histórica e eventual equivalência
atual como informações distintas. Uma instituição imperial não se converte,
retroativamente, em órgão federal republicano.

## Evidência e registro com os campos existentes

Trabalhar nos três estratos da análise: **registro documental**, **filologia
conceitual** e **hipótese iconológica**. No primeiro, registrar o que a fonte
afirma ou mostra e seu localizador; no segundo, explicar vocabulário, categoria
e contexto histórico usados para interpretar a relação; no terceiro, formular
a hipótese e seus limites. Os estratos não são os estatutos `core`, `comparador`
e `apêndice`, nem autorizam promover uma interpretação a fato documental.

Um catálogo que atribui autoria ou procedência prova inicialmente **que esse
catálogo faz a atribuição**. Identificar sua base e eventuais divergências antes
de ampliar a afirmação histórica. Documentos independentes podem sustentar uma
relação e deixar outra em aberto.

Sem alterar o schema, usar `iconocode.interpretation` para formular a relação
precisa (`claim_type: attribution` ou `legal_context`, conforme o caso) e seu
estado `supported`, `tentative` ou `gap`. Em
`iconocode.validation.claim_ledger`, vincular o mesmo `claim_text` aos IDs das
evidências em `supports`, às contraditórias em `contradicts` e às lacunas em
`gaps`. Os IDs de evidência pertencem ao item; não inventar fontes, links ou
localizadores. Confiança numérica existente não substitui a justificativa.

Para estes estados, seguir a política de evidência vigente: `supported` exige
fontes suficientes para aquela relação e seu alcance; `tentative` declara a
atribuição provisória; `gap` declara insuficiência ou contradição não resolvida.
O número de fontes sozinho não resolve a pertinência. Notas de codificação
podem remeter à justificativa, sem criar um país categórico paralelo.

`input.place_hint`, `country`, `pais`, tags, prefixos de ID e nomes de campanhas
legados são pistas ou convenções de organização até que se esclareça a relação
que expressam. Não distribuir um valor ambíguo por todas as dimensões, não
renomear IDs nem sobrescrever o legado em massa. O schema admite os claims e o
ledger acima; esta revisão não exige migração ou preenchimento de novos campos.

## Verificação em cada etapa

| Etapa | Verificação e entrega |
|---|---|
| Seleção e busca | Tratar país de campanha, palavra no título e acervo como pistas. Declarar o vínculo procurado e a razão de pertinência; preservar candidatos com lacunas. |
| Catalogação | Separar as relações efetivamente documentadas, fonte/localizador, data relevante, contradições e incertezas. Preservar rótulos legados e seu sentido ainda desconhecido. |
| Análise e montagem | Explicitar o fundamento de comparação entre jurisdições, instituições, períodos e suportes. Semelhança visual ou personificação nacional não prova transferência nem influência. |
| Redação | Trocar rótulo nacional ambíguo por formulação relacional: “conservada em…”, “produzida em…”, “encomendada por…”, conforme a prova. Hipóteses permanecem qualificadas. |
| Revisão | Conferir cada associação substantiva e seu alcance; apontar o trecho, a fonte, o salto inferencial e a correção. Não exigir ficha completa para aceitar uma afirmação limitada bem sustentada. |
| Exportação e apresentação | Não interpretar filtros e contagens de `country` como nacionalidade comprovada ou pertencimento ao núcleo. Identificar a semântica e as ambiguidades; projeções não são confirmação independente. |

## Casos de aceitação e rejeição de inferências

Exemplos de procedimento, não adjudicações de objetos reais do corpus.

| Entrada ou evidência | Formulação admissível | Inferência a rejeitar |
|---|---|---|
| Apenas guarda em museu brasileiro | “Conservada no acervo brasileiro X”; produção permanece em aberto. | “Produzida no Brasil” ou “obra brasileira” como conclusão da guarda. |
| Artista estrangeiro e encomenda por instituição brasileira documentados | “Encomendada pela instituição brasileira X e executada por Y”, conforme as fontes; justificar sua pertinência ao recorte sem presumir local de produção. | Excluir por autoria estrangeira ou nacionalizar integralmente o objeto. |
| Campo legado `France` sem definição | Preservar `France` e registrar que o vínculo territorial está por esclarecer. | Copiar França para produção, encomenda, tema e recepção. |
| Data de aquisição de 1900 | Registrar aquisição em 1900; data de produção separada. | Datar a produção em 1900 ou usá-la como prova cronológica do núcleo. |
| Documento de uma instituição imperial | Nomear a instituição e jurisdição na data do documento. | Reescrever a encomenda como federal republicana por sua sucessora atual. |
| Busca sem localizar documento de encomenda | “Documento não localizado nas fontes consultadas”; registrar onde se procurou. | “Não houve encomenda” ou “não houve vínculo com o Brasil”. |
| Hipótese de circulação entre contextos | “Hipótese a verificar”, com fundamento, lacunas e fontes a buscar. | Influência, recepção ou inclusão no núcleo afirmadas automaticamente. |

## Revisão dos registros existentes

Abrir uma fila não destrutiva por **ID, formulação/valor legado, fundamento
observado, lacuna, correção proposta e estado/decisão de revisão**. Registrar a
versão e o local da fonte. Uma sugestão permanece proposta até revisão; mudança
aceita preserva o valor anterior e sua justificativa no histórico versionado.
Não concluir que todos os objetos estão errados porque um prompt era inadequado.

Começar pelos casos efetivamente usados na tese ou em artigos e pelos vínculos
comprimidos ou divergentes. Conferir cada justificativa de inclusão no núcleo
Brasil 1822–1922, sem excluir automaticamente os demais do catálogo. Distinguir
ausência de busca, documento inacessível e ausência historicamente demonstrada.

O [inventário inicial de auditoria](../research/auditoria-atribuicoes-territoriais-2026-10-29.md)
identifica alvos, sem corrigir os ledgers. Uma validação de schema confirma
compatibilidade estrutural; não comprova a atribuição histórica nem encerra a
auditoria do corpus.
