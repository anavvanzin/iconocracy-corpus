---
codebook_id: lpai-master
codebook_version: 2.2.0
data_versao: 2026-06-24
status: pre_freeze
freeze_state: pre_freeze
canonical_schema: tools/schemas/master-record.schema.json
canonical_records: data/processed/records.jsonl
canonical_prompt_section: "§16 — Master prompt operacional"
replaces:
  - schema/lpai-v2-as-capta.md
  - docs/methodology/codebook-v2-alegorias.md
  - schemas/codebook-v2.1.0.schema.json
  - docs/decisions/ELICIT-CODEBOOK-PATCH-v2.1.0-2026-06-23.md
migration_policy: "compatibilidade preservada; campos v2.2.0 novos são opcionais até novo freeze"
score_migration_pending: false
autor: Ana Vanzin
licenca: CC-BY-4.0
---

# Codebook MASTER LPAI v2.2.0 — capta, corpus e master prompt

Este documento consolida o codebook operacional do LPAI usado no corpus ICONOCRACY. A fonte técnica de validação continua sendo `tools/schemas/master-record.schema.json`, que valida `data/processed/records.jsonl`. Este arquivo é a fonte editorial e metodológica única: explica o que os campos significam, quais decisões governam a codificação e qual prompt deve ser entregue a codificadores humanos ou LLMs.

## 1. Declaração de capta

O LPAI não mede imagens como se elas oferecessem dados neutros. Cada registro é capta: uma tomada situada, construída por uma pessoa, por um instrumento, por uma hipótese de tese e por uma cadeia documental. O score é útil como instrumento de atenção e auditoria, mas não tem autoridade epistêmica isolada. Nenhum resultado ordinal deve circular sem o registro de evidência, autoria, data de codificação e nota metodológica quando houver ambiguidade.

Declaração curta recomendada para registros e outputs derivados:

> LPAI v2-capta: scores são atos interpretativos situados, não dados neutros.

Esta declaração substitui variações anteriores. O objetivo não é apagar a quantificação, mas impedir que a quantificação apareça como evidência natural. Frequências, médias e gráficos só são defensáveis quando acompanhados do frame qualitativo, do estado de freeze e da distinção entre core, piloto, comparador e apêndice.

## 2. Princípios operacionais

1. Descrição visual e hipótese interpretativa são camadas diferentes. A primeira registra o que aparece; a segunda declara o sentido atribuído.
2. Ausência pode ser capta. Quando a ausência de corpo, gênero, atributo, inscrição ou figura humana é analiticamente relevante, registre como dado negativo, não como campo vazio.
3. A unidade canônica do ledger atual é o registro `master-record`; dentro dele, a codificação iconográfica vive em `purificacao`. O item pode representar uma figura individual ou um programa textual/visual já consolidado pela pipeline. A agregação por `programa_id` é opcional em v2.2.0.
4. O corpus canônico deve continuar validando contra `tools/schemas/master-record.schema.json`. Campos novos não podem invalidar os registros válidos sem uma migração explícita.
5. Subalternidade é sinal de cautela, não categoria automática. Quando categorias euro-imperiais forem aplicadas a repertórios indígenas, negros, populares ou híbridos, a codificação deve registrar a cautela interpretativa.
6. O codebook deve favorecer análise iconológica e tese, não acumular blocos terminológicos. Listas de países, repertórios ou taxonomias auxiliares entram apenas se sustentarem uma decisão de codificação.

## 3. Contrato técnico atual

O contrato técnico atual é o `MasterRecord`. Cada linha de `data/processed/records.jsonl` contém:

- metadados de pipeline: `master_record_version`, `batch_id`, `item_id`, `item_hash`, `timestamps`;
- entrada e evidência: `input`, `webscout`, `iconocode`;
- codificação LPAI: `purificacao`;
- exportação e auditoria: `exports`.

A seção `purificacao` é o núcleo interpretativo. Ela já contém os 10 indicadores canônicos em escala 0–3, o score composto, regime iconocrático, autoria da codificação, data, notas, confiança opcional, adjudicação e campos iconográficos (`familia_alegorica`, `subtipo`, `atributos_iconograficos`, `genero_atribuido`, `funcao_juridica`, `vetor_colonial`, `hipotese_racial`, `referencia_genealogica`, `capta_declaration`, `codebook_version`, `pre_freeze_sample`, `subaltern_caution`).

## 4. Campos v2.2.0 opcionais

A versão 2.2.0 acrescenta campos opcionais ao bloco `purificacao`, preservando compatibilidade com registros anteriores:

| Campo | Função | Status |
|---|---|---|
| `programa_id` | agrupar figuras ou registros que pertencem ao mesmo programa iconográfico | opcional |
| `ordem_no_programa` | posição da figura no programa quando `programa_id` existir | opcional |
| `dado_negativo` | marcar ausência analiticamente significativa | opcional |
| `finalidade_atribuida` | finalidade jurídico-política atribuída ao artefato | opcional |
| `power_at_stake` | quem se beneficia ou é marginalizado pelo artefato/codificação | opcional |
| `coder_position_statement` | posição e limites do/a codificador/a | opcional |
| `confianca_codificacao` | confiança qualitativa (`alta`, `media`, `baixa`) | opcional |
| `motivo_incerteza` | justificativa quando a confiança não for alta | condicional, se `confianca_codificacao` for `media` ou `baixa` |
| `relacao_com_repertorio_indigena` | ausência, apropriação, coexistência ou hibridização de repertórios indígenas | opcional |
| `disjuncao_representa_governa` | figura representa poder sem governar | opcional |
| `objetos_regalia` | decomposição opcional dos objetos antes reunidos em `atributos_iconograficos` | opcional |
| `marcas_corporais` | decomposição opcional de corpo, pose e vestes | opcional |
| `marcadores_cena_arquitetura` | decomposição opcional de cena, animais, ambiente e arquitetura | opcional |

Esses campos são expansão de auditabilidade. Eles não substituem os campos legados e não entram no índice composto sem decisão posterior de freeze.

## 5. Famílias e subtipos

O campo `familia_alegorica` permanece enxuto: `Virtudes`, `Continentes`, `Oceanos/Rios`, `Nacional`, `Outra`. A versão master evita blocos longos de países e terminologias paralelas. A decisão de família deve ser guiada pela função da figura no artefato, não por nacionalidade isolada.

`subtipo` permanece string livre no schema canônico para preservar registros válidos e evitar falsas rejeições. O codebook recomenda, porém, vocabulário controlado quando possível: `Iustitia`, `Prudencia`, `Fortaleza`, `Temperanca`, `Fe`, `Esperanca`, `Caridade`, `Veritas`, `Europa`, `America`, `Africa`, `Asia`, `Oceano`, `Rio`, `Republica`, `Liberdade`, `Patria`, `Brasil`, ou outro subtipo justificado em `notes`.

## 6. Atributos iconográficos

O campo canônico atual é `atributos_iconograficos`, uma lista simples de strings. Ele deve ser mantido para compatibilidade. Em v2.2.0, quando houver tempo e evidência suficiente, o codificador pode preencher também três listas derivadas:

- `objetos_regalia`: balança, espada, venda, espelho, tocha, globo, cornucópia, cetro, coroa, tridente, fasces, bandeira, urna, incensário ou outro objeto.
- `marcas_corporais`: corpo reclinado, barba, nudez, vestes romanas, vestes indígenas, vestes africanas, corpo ereto, corpo sentado ou outro marcador corporal.
- `marcadores_cena_arquitetura`: ondas, animais, serpente, escorpião, arco e flecha, cabeça decepada, moldura, frontão, brasão, paisagem ou outro marcador de cena.

A decomposição é opcional porque ela aumenta custo de codificação. Use-a quando ajudar a separar descrição visual de interpretação iconológica.

## 7. Gênero, raça e hipótese interpretativa

`genero_atribuido` registra a leitura predominante da figura: `feminino`, `masculino`, `neutro`, `hibrido` ou `ausente`. Quando a atribuição for decisiva para o argumento, explique em `notes` quais marcas visuais sustentam a leitura.

`hipotese_racial` deve permanecer explicitamente interpretativa. Não substitui descrição visual e não deve converter sinais convencionais de repertório em etnografia. Se o item mobilizar repertórios indígenas, negros ou populares, use `subaltern_caution` e, quando aplicável, `relacao_com_repertorio_indigena`.

`disjuncao_representa_governa` pode ser usado quando uma figura feminina representa Estado, Justiça, República ou Pátria sem corresponder a participação política real de mulheres no regime representado.

## 8. Função jurídica, finalidade e poder

`funcao_juridica` indica o tipo de dispositivo: tribunal de consciência, frontispício normativo, moeda/cédula, selo, brasão, arquitetura forense, monumento público, paratexto normativo ou outro. `vetor_colonial` indica a rota interpretativa principal: europeu direto, luso-brasileiro, republicano brasileiro ou não aplicável.

`finalidade_atribuida` é opcional e deve ser usada com parcimônia: `legitimacao_juridica`, `pedagogia_civica`, `dissuasao`, `comemoracao`, `branding_estatal` ou `outro`. `power_at_stake` responde, em linguagem curta, quem ganha autoridade, visibilidade ou naturalização com a imagem, e quem fica fora dela.

## 9. Genealogia e repertórios

`referencia_genealogica` pode ser string ou lista. Use como ponteiro para repertórios, tradições ou bibliografia que sustentam a leitura: Ripa, Ortelius, Four Continents, Warner, Resnik & Curtis, Souza, Ihering ou outra referência documentada. Abreviações não substituem bibliografia completa: todo ponteiro usado em análise publicada deve ter referência ABNT em arquivo bibliográfico ou nota de tese.

## 10. Indicadores canônicos de purificação

Os 10 indicadores canônicos são os do documento-pai `data/docs/codebook.md`, em escala ordinal 0–3:

| Indicador | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `desincorporacao` | corpo naturalista | idealizado | genérico | geométrico/ausente |
| `rigidez_postural` | movimento dinâmico | pose contida | rígida/frontal | hieratismo total |
| `dessexualizacao` | erotismo/nudez explícita | sugestão corporal | coberto mas generificado | gênero indeterminado/encoberto |
| `uniformizacao_facial` | rosto individualizado | idealizado | genérico | sem rosto/máscara |
| `heraldizacao` | atributo integrado | portado | destacado | emblema isolado |
| `enquadramento_arquitetonico` | espaço aberto | fundo discreto | moldura dominante | absorvido por edifício/selo |
| `apagamento_narrativo` | cena completa | narrativa sugerida | figura isolada com vestígio | fundo neutro/isolamento total |
| `monocromatizacao` | policromia | paleta reduzida | bicromia/restrita | monocromático |
| `serialidade` | obra única | tiragem limitada | média escala | reprodução massiva |
| `inscricao_estatal` | sem vínculo estatal | encomenda oficial | insígnia estatal | dispositivo estatal |

O índice composto é a média dos 10 indicadores. Ele é uma heurística de endurecimento/purificação simbólica, não prova autônoma. Indicadores suplementares como classicização, moralização, depuração semântica, neutralização afetiva e monumentalização podem aparecer em notas iconológicas, mas não integram o score canônico em v2.2.0.

## 11. Programa iconográfico

`programa_id` e `ordem_no_programa` são opcionais. Use-os apenas quando a análise exigir relação entre figuras de um mesmo conjunto. O registro continua válido sem esses campos. Quando usados, `programa_id` deve identificar o conjunto e `ordem_no_programa` deve indicar a posição relativa da figura ou entrada dentro dele.

Esta regra evita reabrir toda a unidade de análise do corpus. A tese pode analisar programas por agregação, sem invalidar registros já codificados como linhas independentes.

## 12. Adjudicação, confiança e cautela

O schema canônico já aceita `confidence_score` e `adjudication_status`. A expansão v2.2.0 adiciona `confianca_codificacao` (`alta`, `media`, `baixa`) e `motivo_incerteza` para leitura humana. Quando os dois sistemas coexistirem, use ambos: `confidence_score` para cálculo e `confianca_codificacao` para legibilidade metodológica.

`subaltern_caution` deve ser acionado quando a escala ou o repertório foram produzidos para figuras canônicas euro-imperiais e o item analisado desloca esse cânone. Cautela não significa exclusão; significa que a categoria é observada como problema.

## 13. Naming, freeze e governança

Arquivos pré-freeze não devem usar o sufixo `final`. O estado de freeze deve ser declarado por versão, hash e changelog. A sequência recomendada permanece:

```text
teoria → codebook → amostragem → piloto → confiabilidade → freeze → análise
```

Qualquer mudança de campo, enum, escala ou indicador deve registrar no changelog: evidência empírica, problema teórico e risco de reatividade.

## 14. Relação com artefatos anteriores

Este master preserva os artefatos anteriores como contexto histórico, não como fontes concorrentes. Se houver divergência entre arquivos, a ordem de autoridade é:

1. `tools/schemas/master-record.schema.json` para validação técnica do corpus;
2. `schema/codebook-MASTER.md` para interpretação e prompt de codificação;
3. `schema/CHANGELOG.md` para decisões de versão;
4. documentos anteriores, mantidos como contexto e rastreabilidade.

## 15. Exemplo mínimo de bloco `purificacao`

```yaml
purificacao:
  desincorporacao: 2
  rigidez_postural: 2
  dessexualizacao: 2
  uniformizacao_facial: 1
  heraldizacao: 2
  enquadramento_arquitetonico: 3
  apagamento_narrativo: 1
  monocromatizacao: 2
  serialidade: 3
  inscricao_estatal: 3
  purificacao_composto: 2.1
  regime_iconocratico: normativo
  coded_by: avanzin
  coded_at: "2026-06-24T18:00:00-03:00"
  notes: "Codificação situada; fonte visual parcial; manter como piloto."
  familia_alegorica: Nacional
  subtipo: Republica
  genero_atribuido: feminino
  funcao_juridica: moeda_cedula
  vetor_colonial: republicano_brasileiro
  capta_declaration: "LPAI v2-capta: scores são atos interpretativos situados, não dados neutros."
  codebook_version: "2.2.0"
  pre_freeze_sample: true
  dado_negativo: false
  finalidade_atribuida: branding_estatal
```

## 16. Master prompt operacional

Use este bloco como instrução para um codificador humano ou LLM. Não inclua blocos terminológicos longos; consulte o codebook quando precisar de enum.

```text
Você é um codificador LPAI v2.2.0 para o corpus ICONOCRACY. Sua tarefa é produzir capta iconográfico situado, não dados neutros.

1. Leia a evidência disponível: imagem, metadados, fonte, data, suporte, local e notas anteriores.
2. Declare se a imagem permite codificação visual suficiente. Se não permitir, reduza confiança e explique em notes.
3. Classifique os 10 indicadores canônicos em escala 0–3: desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial, heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal.
4. Calcule purificacao_composto como média simples dos 10 indicadores.
5. Atribua regime_iconocratico apenas se houver base suficiente: fundacional, normativo, militar ou contra-alegoria.
6. Preencha familia_alegorica, subtipo, genero_atribuido, funcao_juridica e vetor_colonial quando a evidência sustentar a decisão.
7. Separe descrição de hipótese. Use atributos_iconograficos para sinais observáveis e hipotese_racial apenas para interpretação declarada.
8. Se a ausência for significativa, marque dado_negativo. Se a categoria for subalternizada ou deslocar repertório euro-imperial, marque subaltern_caution.
9. Se houver programa iconográfico, use programa_id e ordem_no_programa sem alterar item_id existente.
10. Declare finalidade_atribuida e power_at_stake apenas quando o contexto institucional permitir inferência responsável.
11. Registre coded_by, coded_at, codebook_version, capta_declaration e notes.
12. Nunca trate score como prova isolada. Todo output deve preservar a condição de capta e a incerteza documentada.
```

## 17. Referências mínimas

As referências completas permanecem no aparato bibliográfico da tese. Este master depende, no mínimo, de Drucker para capta, D'Ignazio e Klein para dados situados e poder, Haraway para saberes situados, Merry para crítica da quantificação, Espeland e Sauder para reatividade, Warner para alegoria feminina, Resnik e Curtis para justiça vista/situada, e bibliografia iconográfica específica para cada família alegórica.

## 18. Changelog resumido

- v2.0.0: codebook independente piloto, com expansão de famílias e campos iconográficos.
- v2.1.0: schema experimental/orphan com campos avançados; preservado como contexto, mas não governa `records.jsonl`.
- v2.2.0: consolidação master; preserva o schema canônico validado, alinha indicadores ao documento-pai 0–3 e torna a expansão opcional.
