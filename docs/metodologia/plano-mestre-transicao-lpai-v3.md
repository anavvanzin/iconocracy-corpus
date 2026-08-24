---
documento: plano mestre de transição metodológica
id: PLAN-2026-07-31-LPAI-V3
data: 2026-07-31
autora: Ana Vitória Vanzin Mendes
status: proposta para deliberação
escopo: LPAI v2.3.0 para arquitetura metodológica v3
fundamentacao: nota-epistemologica-lpai-v3.md
---

# Plano mestre para a transição metodológica LPAI v3

> Este documento organiza a execução segura. A justificativa propriamente
> acadêmica da mudança, seus custos teóricos e as decisões que ainda exigem
> deliberação estão desenvolvidos na
> [nota epistemológica da transição](nota-epistemologica-lpai-v3.md). O plano
> não deve ser convertido em especificação técnica antes dessa deliberação.

## 1. Decisão de segurança: mudar o método sem reescrever a evidência

Esta transição altera o estatuto epistêmico do corpus, a arquitetura dos
atributos e a forma de argumento visual. Por isso, ela não será executada como
uma migração única. Até a aprovação dos marcos deste plano, ficam vedadas:

1. a conversão em massa dos zeros legados;
2. a recodificação do ledger canônico;
3. a alteração direta de `corpus/corpus-data.json`;
4. a reconstrução dos painéis como se a v3 já estivesse estabilizada; e
5. a reutilização de números produzidos pelo índice composto aposentado como
   evidência da tese.

O princípio operativo é **adição antes de substituição**: preservar o estado
v2.3.0, produzir a v3 em *staging*, comparar os dois estados e somente promover
uma transformação quando sua reversibilidade, sua proveniência e seu efeito
argumentativo estiverem documentados.

## 2. Invariantes que a mudança não pode romper

| Invariante | Regra verificável |
|---|---|
| Fonte canônica | `data/processed/records.jsonl` continua sendo o ledger operacional; exportações são derivadas. |
| Contagem | Toda análise declara o denominador efetivamente lido do ledger. O quick reference que informa 299 não governa a migração enquanto o ledger canônico tiver 328 registros; a divergência precisa ser explicada, não normalizada silenciosamente. |
| Identidade | Nenhum `id` é criado, apagado ou renomeado silenciosamente. |
| Proveniência | Cada valor v3 aponta para fonte, imagem, versão do instrumento, autora/agente, sessão, data e justificativa. |
| Ausência | `0`, `não codificado` e `não codificável` são estados semanticamente distintos. |
| Não agregação | Não se cria média, escore ou ranking global dos atributos. Valores legados permanecem identificados como congelados. |
| Hermenêutica | Métricas internas podem diagnosticar o instrumento, mas não funcionam como prova de recepção histórica nem como condição de validade da leitura. |
| Rastreabilidade | Cada item continua rastreável entre manifesto, nota do vault e ledger. |
| Reversibilidade | Toda promoção gera manifesto de migração, *before/after*, hash e procedimento de restauração. |

## 3. O conflito documental a resolver antes de qualquer implementação

A decisão do aparato mínimo substitui o pipeline de confiabilidade métrica por
catálogo documentado, leitura densa e montagem. O plano de recodificação anterior,
porém, ainda contém uma “Fase 4 — Confiabilidade” obrigatória. A v3 deve adotar a
seguinte separação, que impede tanto o positivismo residual quanto o abandono de
controles úteis:

- **prova disciplinar:** crítica de fonte, proveniência, disciplina contra o
  anacronismo, explicitação dos silêncios, justificativa dos casos exemplares e
  montagem argumentada;
- **controle técnico:** validação de schema, reexecução determinística, hashes,
  testes de migração, auditoria de links/fontes e cobertura;
- **diagnóstico reflexivo opcional:** comparação cega, contraste com proxy e
  medidas de concordância, usadas exclusivamente para localizar ambiguidade ou
  deriva do instrumento, nunca como selo de verdade.

Consequentemente, não haverá “gate de kappa”. Se um diagnóstico reflexivo for
realizado, seu resultado integra o diário de decisões e pode levar à revisão de
uma regra; sua ausência não invalida a leitura. O codificador-proxy tampouco será
tratado como codificador humano independente.

## 4. Arquitetura inovadora: trilha de evidência, não planilha de certezas

### 4.1 Estado epistêmico por afirmação

Cada observação v3 deve combinar **valor**, **estado epistêmico** e **base de
evidência**. A proposta mínima é:

```text
observado        fonte/imagem permite afirmar presença ou ausência
nao_codificado   ainda não houve leitura segundo a versão declarada
nao_codificavel  a fonte disponível não permite decidir, com causa tipada
contestado       leituras ou fontes sustentam alternativas relevantes
```

O valor ordinal só existe em `observado`. `nao_codificavel` exige uma causa como
`resolucao_inadequada`, `imagem_ausente`, `oclusao`, `fonte_insuficiente` ou
`nao_aplicavel`. Assim, a incerteza deixa de ser um vazio e passa a ser parte
auditável do argumento.

### 4.2 Pacote de evidência por item

Em vez de sobrescrever uma célula, cada sessão de leitura produz um pacote
imutável em *staging*:

```text
record_id + codebook_version + session_id + actor_id + blind
+ image_hash + source_ids + observations + justifications + timestamp
```

Uma promoção explícita materializa a leitura aceita no ledger. Isso permite
reconstruir quem afirmou o quê, sobre qual arquivo e sob qual regra, sem confundir
história da codificação com conteúdo da codificação.

### 4.3 Cartão de argumento visual

Cada caso exemplar e cada painel terá um cartão legível por humanos contendo:

1. tese local do painel;
2. casos incluídos e razão da inclusão;
3. fonte e contexto institucional de cada imagem;
4. indícios visuais mobilizados e alternativas consideradas;
5. lacunas, casos negativos e contraexemplos;
6. limite da inferência: produção/disponibilização de sentido, não recepção; e
7. versão do corpus e do instrumento que sustentam a montagem.

O cartão transforma o atlas em argumento verificável, e não em ilustração de uma
estatística ausente.

## 5. Programa em sete marcos, com *stop/go*

### Marco 0 — Congelamento forense e reconciliação (antes de codificar)

**Entregáveis**

- snapshot somente leitura do ledger v2.3.0, com SHA-256, contagem e inventário
  de IDs;
- relatório que reconcilie os 328 registros encontrados no ledger com a menção
  documental a 299, sem “corrigir” nenhuma das fontes durante a investigação;
- matriz de consumidores de `purificacao`, `purificacao_composto`,
  `endurecimento_score`, indicadores e regimes;
- registro das alegações da tese que dependem desses campos.

**Gate 0:** não avançar enquanto denominador, origem dos 106 falsos zeros e
universo real da migração não forem reproduzíveis por script.

### Marco 1 — Contrato metodológico e modelo de ameaça

Realizar uma oficina de decisão com a autora e, idealmente, orientação. Aprovar:

- pergunta que cada estrato pode responder;
- critérios de inclusão, exclusão e escolha de casos exemplares;
- taxonomia de estados epistêmicos e causas de não codificabilidade;
- estatuto exclusivamente diagnóstico das métricas de concordância;
- política para imagens insuficientes, fontes conflitantes e casos fronteiriços;
- critérios explícitos para revisar, dividir ou aposentar um atributo.

Produzir um registro de ameaças à validade: anacronismo, viés de digitalização,
seleção confirmatória, deriva interpretativa, ancoragem na codificação anterior,
automação persuasiva e falsa precisão colorimétrica.

**Gate 1:** aprovação humana de um ADR metodológico único que resolva a
contradição entre “abandono da confiabilidade” e a antiga Fase 4.

### Marco 2 — Especificação v3 em paralelo

Criar o codebook e o schema v3 sem modificar ainda o contrato canônico. Para
cada campo, documentar definição, pergunta, estrato, valores permitidos,
evidência mínima, contraexemplo, regra de ausência e regra de aplicabilidade.

A monocromatização automatizada deve ser tratada como **medida condicionada ao
arquivo digital**, não como propriedade transparente do artefato histórico:
perfil de cor, digitalização, compressão, fundo e restauração podem alterar o
resultado. Serialidade técnica somente entra no estrato documental quando a
fonte sustentar a atribuição.

**Gate 2:** fixtures positivas, negativas, limítrofes e não codificáveis passam
no schema; v2 continua validando; exportação pública não muda.

### Marco 3 — Laboratório de 30 casos

Selecionar os casos por diversidade deliberada, e não por pretensão amostral:
regime, país, período, suporte, qualidade de imagem, nível de documentação,
presença/ausência e casos fronteiriços. Publicar a regra de seleção e manter uma
lista-reserva.

Cada caso recebe leitura densa, pacote de evidência e cartão de argumento. O
proxy pode produzir uma leitura separada, rotulada como provocação diagnóstica.
A comparação procura ambiguidades, fontes faltantes e efeitos de ancoragem; não
produz nota de aprovação do método.

**Gate 3:** nenhuma regra sem exemplo; nenhuma observação sem justificativa;
todas as divergências classificadas; tempo e carga cognitiva reais registrados.
Se mais de 20% dos julgamentos dependerem de fonte/imagem insuficiente, retornar
ao Marco 2 em vez de ampliar a escala.

### Marco 4 — Migração simulada e ensaio de restauração

Construir uma transformação idempotente sobre cópia descartável. Ela deve:

1. distinguir falsos zeros sem converter zeros observados;
2. preservar valores legados e sua proveniência;
3. emitir log linha a linha e resumo por país, regime e suporte;
4. falhar de forma atômica diante de ID, estado ou schema inesperado;
5. gerar *diff* semântico, não apenas textual; e
6. restaurar exatamente o snapshot inicial em ensaio documentado.

**Gate 4:** duas execuções produzem o mesmo hash; o rollback reproduz o hash de
origem; revisão humana aprova uma amostra dirigida de todas as classes de mudança.

### Marco 5 — Recodificação em ondas argumentativas

Iniciar pelo regime militar, cuja alegação permanece suspensa, e pelo Brasil,
caso central. A ordem posterior depende do diagnóstico do Marco 0, não das
contagens antigas. Cada onda é um lote independente e promove apenas itens
aprovados.

O health check semanal mostra **cobertura**, nunca desempenho: número observado,
não codificado, não codificável e contestado, por estrato e recorte. Sessões são
curtas, e o diário registra alterações de regra. Alteração do codebook durante
uma onda exige nova versão e análise explícita dos itens já lidos.

**Gate 5 por onda:** schemas, rastreabilidade, revisão dos estados alterados,
auditoria das fontes, *diff* de exportação e lista das alegações liberadas ou
ainda suspensas.

### Marco 6 — Atlas, análise de sensibilidade e redação

Reconstruir os painéis apenas quando os recortes que os sustentam passarem pelo
Gate 5. Em vez de um índice, usar:

- matrizes de presença/ausência com denominadores visíveis;
- pequenos múltiplos por estrato, país, regime ou suporte;
- redes de coocorrência apenas descritivas, com filtro de cobertura;
- faixas de sensibilidade para decisões contestadas;
- galeria explícita de contraexemplos e ausências substantivas; e
- cartões de argumento visual anexos aos painéis.

Toda figura deve informar versão, fonte, universo, dados ausentes e texto
alternativo; funcionar em escala de cinza; não usar cor como único canal; e vir
acompanhada de tabela acessível. Títulos devem enunciar o achado, não apenas o
tipo de gráfico.

**Gate 6:** cada proposição do capítulo aponta para fontes, casos e versão do
corpus; nenhuma legenda excede o que a evidência permite afirmar; contraexemplos
relevantes estão visíveis.

## 6. Painel de governança

| Pergunta semanal | Evidência |
|---|---|
| O ledger continua íntegro? | hash, contagem, IDs e schema |
| O que foi efetivamente lido? | cobertura por estado epistêmico e estrato |
| O que mudou na regra? | versão do codebook e changelog |
| O que mudou no argumento? | mapa alegação → casos → fontes |
| Onde a evidência falha? | causas tipadas de `nao_codificavel` |
| A automação influenciou a leitura? | ordem temporal e marcação `blind` |
| É possível voltar? | último ensaio de restauração e manifesto |

Semáforo: **verde** quando invariantes e gate atual passam; **amarelo** para
lacuna declarada que não corrompe dados; **vermelho** para perda de proveniência,
mudança silenciosa de denominador, uso de falso zero ou alegação sustentada por
recorte ainda não promovido. Vermelho interrompe a onda.

## 7. Sequência técnica de mudanças futuras

Cada item abaixo deve ser uma alteração pequena e reversível, preferencialmente
um PR separado:

1. auditoria reproduzível de contagem, IDs, falsos zeros e consumidores;
2. ADR que consolida o contrato metodológico;
3. codebook v3 e fixtures, sem tocar dados;
4. schema v3 paralelo e testes de compatibilidade;
5. formato dos pacotes de evidência e validador de *staging*;
6. ferramenta de *diff* semântico e manifesto de migração;
7. piloto de 30 casos em *staging*;
8. revisão e versionamento do instrumento;
9. migração simulada, teste de idempotência e rollback;
10. ondas de recodificação com promoção explícita;
11. exportadores atualizados, mantendo campos legados claramente rotulados;
12. reconstrução dos painéis e redação metodológica final.

## 8. Critério de conclusão da transição

A v3 estará concluída quando: (a) o universo canônico estiver reconciliado; (b)
todo item tiver estado epistêmico explícito por observação aplicável; (c) nenhuma
ausência de leitura estiver representada como zero; (d) as transformações forem
reexecutáveis e reversíveis; (e) os painéis declararem denominadores e lacunas;
(f) as alegações centrais estiverem ligadas a casos, fontes e justificativas; e
(g) o capítulo metodológico distinguir claramente prova disciplinar, controle
técnico e diagnóstico reflexivo.

O sucesso não é obter concordância máxima nem completar todas as células. É
construir uma cadeia de evidência na qual se possa localizar, verificar e
contestar cada passagem entre fonte, observação, montagem e argumento.
