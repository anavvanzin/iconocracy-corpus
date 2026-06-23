# Patch CHANGELOG v2.1.0 (v2.0.0 → v2.1.0) — Codebook LPAI v2 (Virtudes, Continentes, Oceanos/Rios)

## 1. Cabecalho do patch

Este patch propõe uma atualização implementável do Codebook v2.0.0 para v2.1.0 com foco em (i) maior auditabilidade da codificação como *capta* (isto é, construída e situada) e (ii) redução de ambiguidades classificatórias que afetam comparabilidade e confiabilidade. A justificativa metodológica se ancora na exigência de repensar “data as a given” como *capta* (tomada e construída) e na ênfase em contexto, poder e trabalho na produção de registros[^1][^2], bem como na advertência de que ícones são intrinsecamente ambíguos e dependem de leitores, contextos e intenções[^3][^4].

```yaml
patch_header:
  from_version: "2.0.0"
  to_version: "2.1.0"
  date: "2026-06-23"
  author: "(a preencher)"
  scope:
    - "Nao re-pontua itens anteriores ingestados em 2.0.0."
    - "Aplicavel apenas a novos ingestos; campos novos sao opcionais para legados (ver Plano de migracao)."
  motivacao:
    - "Operacionalizar capta com rastreabilidade do julgamento humano (posicao do/a codificador/a, quem se beneficia, confianca)."  # capta e poder[^1][^2]
    - "Separar descricao iconografica (componentes/atributos) de inferencias interpretativas, reduzindo ambiguidade e melhorando comparabilidade."  # ambiguidade e leituras multiplas[^3][^4][^5]
    - "Eliminar sobreposicoes e granularidades inconsistentes que dificultam interoperabilidade (ex.: 'Brasil' em subtipo de duas familias; atributos misturando objetos e marcas corporais)."  # indices/atributos e variacao editorial[^5][^6]
```

## 2. Resumo do diff conceitual

A tabela abaixo resume o *diff* conceitual por campo, com status e justificativa curta (com citações quando há base direta). O objetivo é tornar a alteração “colável” e rastreável, sem ensaio interpretativo. A necessidade de explicitar o quadro interpretativo é coerente com a crítica de que visualizações e convenções “escondem” o framework interpretativo de construção dos registros[^7].

| Campo | Status | Justificativa |
|---|---|---|
| `subtipo` | modificado | Remove sobreposição “Brasil” entre famílias; continentes operam como “allegorical stand-ins” (tipos convencionais), então “Brasil” deve permanecer como nacional e “America_do_Sul” pode cobrir regionalização quando necessário[^8][^9]. |
| `atributos_iconograficos` | dividido | Alinha-se a uma lógica de índices por elemento (objetos/plantas/cores etc.) e reduz mistura entre “coisas” e “corpo”, aumentando clareza para codificação sistemática sob ambiguidade dos ícones[^5][^3]. |
| `genero_atribuido` | modificado | Mantém enum, mas exige justificativa curta para tornar o julgamento explícito, dado que agência/definições são móveis e alegorias femininas podem “representar” sem “governar”[^10][^11]. |
| `dado_negativo` | novo | Ausência pode ser semanticamente relevante; como justiça pode ser “seen” ou “sited”, o não-figural também participa da gramática visual e precisa ser codificado[^12][^3]. |
| `coder_position_statement` | novo | Operacionaliza *capta* como tomada situada e não neutral; contexto e trabalho importam na produção do registro[^1][^2]. |
| `power_at_stake` | novo | Exige declarar “quem se beneficia” do registro, conforme checklist de poder em projetos de dados[^2]. |
| `confianca_codificacao` / `motivo_incerteza` | novo | A ambiguidade do ícone e a dependência de leitura por contexto exigem um canal para incerteza; variações editoriais (Ripa) afetam evidência disponível[^3][^4][^6]. |
| `finalidade_atribuida` | novo | Campo teleológico para explicitar o “fim” pretendido do dispositivo; conecta-se às “larger questions … about the goals of justice” (lacuna sobre Ihering neste piloto)[^13]. |
| `familia_alegorica` | modificado | Adiciona `Afro_Brasileira` para ampliar pluralidade/contexto na classificação (lacuna na base de evidencia direta neste piloto; mudança normativo-metodológica)[^2]. |
| `relacao_com_repertorio_indigena` | novo | Permite registrar apropriação/hibridização em repertórios onde o “novo mundo” foi feminilizado e disponibilizado para posse; evita reduzir o indígena a “ruído” fora do schema[^14][^15]. |
| `fonte_imagem` / `edicao_suporte` / `tipo_reproducao` | novo | Rastreia suporte/proveniência; relevante pois edições variam (nem tudo é ilustrado) e a circulação via reproduções impressas é parte do modo de existência do repertório[^6][^16]. |
| `adjudicacao_log` | novo | Encaminha desacordos num cenário em que o sentido depende de contexto e intenção; dá rastreabilidade ao trabalho de codificação[^4][^2]. |

## 3. Mudancas em campos existentes

Esta seção fornece blocos “ANTES/DEPOIS” em YAML, no formato mais próximo possível de um schema de codebook. As mudanças são formuladas para reduzir ambiguidades e tornar o julgamento auditável, coerente com a tese de que “data”/registros são construídos e que sua legibilidade pode esconder o framework interpretativo[^1][^7].

### 3.1 `subtipo`

A sobreposição de `Brasil` em `Continentes` e `Nacional` cria ambiguidade classificatória (um mesmo token nomeia entidade geopolítica e personificação nacional). Como as figuras dos continentes são “allegorical stand-ins” generalizantes e classicizantes (não evidência documental de povos diversos), faz sentido manter “Brasil” apenas como nacional e, quando necessário, introduzir um subtipo regional (p.ex. `America_do_Sul`) no bloco de continentes[^8].

**ANTES (v2.0.0)**

```yaml
subtipo:
  Continentes:
    - Europa
    - America
    - Africa
    - Asia
    - Brasil
    - outro_continente
  Nacional:
    - Republica
    - Liberdade
    - Patria
    - Brasil
    - outra_nacional
```

**DEPOIS (v2.1.0)**

```yaml
subtipo:
  Continentes:
    - Europa
    - America
    - America_do_Sul
    - Africa
    - Asia
    - outro_continente
  Nacional:
    - Republica
    - Liberdade
    - Patria
    - Brasil
    - outra_nacional
subtipo_rules:
  - rule: "Se a personificacao for 'Brasil' como nacao/Estado (efigie republicana, patria, etc.), codar em Nacional:Brasil."
  - rule: "Se a figura operar como continente/regiao em repertorio Four Continents ou frontispicios análogos, usar Continentes:America ou Continentes:America_do_Sul conforme legenda/atributos."
  - note: "Continentes sao tipos alegoricos genericizantes; nao equivalem a etnografia"  # stand-ins[^8]
```

### 3.2 `atributos_iconograficos`

O campo único misturava (i) objetos/regalias (balança, espada), (ii) marcas corporais (barba) e (iii) marcadores de cena/arquitetura (ondas marítimas). Ao dividir em três listas, o patch aproxima o schema de uma lógica de “índices de elementos” (animais, objetos etc.) e melhora interoperabilidade, sem negar que a leitura do signo é múltipla e dependente de contexto[^5][^4].

**ANTES (v2.0.0)**

```yaml
atributos_iconograficos:
  - balanca
  - espada
  - venda
  - espelho
  - tocha
  - globo
  - cornucopia
  - cetro
  - coroa
  - arco_e_flecha
  - cabeca_decepada
  - animais_exoticos
  - cobra
  - escorpiao
  - incensario
  - coroa_de_junco
  - urna
  - tridente
  - barrete_frigio
  - fasces
  - bandeira
  - ramos_estrelas
  - corpo_reclinado
  - barba
  - ondas_maritimas
  - outro
```

**DEPOIS (v2.1.0)**

```yaml
objetos_regalia:
  - balanca
  - espada
  - venda
  - espelho
  - tocha
  - globo
  - cornucopia
  - cetro
  - coroa
  - arco_e_flecha
  - cabeca_decepada
  - incensario
  - urna
  - tridente
  - barrete_frigio
  - fasces
  - bandeira
  - ramos_estrelas
  - outro_objeto  # descrever em notes

marcas_corporais:
  - corpo_reclinado
  - barba
  - outra_marca  # descrever em notes

marcadores_cena_arquitetura:
  - ondas_maritimas
  - animais_exoticos
  - cobra
  - escorpiao
  - coroa_de_junco
  - outro_marcador  # descrever em notes

migracao_atributos:
  balanca: objetos_regalia
  espada: objetos_regalia
  venda: objetos_regalia
  espelho: objetos_regalia
  tocha: objetos_regalia
  globo: objetos_regalia
  cornucopia: objetos_regalia
  cetro: objetos_regalia
  coroa: objetos_regalia
  arco_e_flecha: objetos_regalia
  cabeca_decepada: objetos_regalia
  incensario: objetos_regalia
  urna: objetos_regalia
  tridente: objetos_regalia
  barrete_frigio: objetos_regalia
  fasces: objetos_regalia
  bandeira: objetos_regalia
  ramos_estrelas: objetos_regalia
  corpo_reclinado: marcas_corporais
  barba: marcas_corporais
  ondas_maritimas: marcadores_cena_arquitetura
  animais_exoticos: marcadores_cena_arquitetura
  cobra: marcadores_cena_arquitetura
  escorpiao: marcadores_cena_arquitetura
  coroa_de_junco: marcadores_cena_arquitetura

atributos_note:
  - "A divisao assume que qualquer icone carrega ambiguidade e pode ter leituras multiplas; a separacao aqui e apenas para clareza descritiva."  # ambiguidade e leitura contextual[^3][^4]
  - "A inspiracao e compatibilizar com logica de indices/elementos da tradicao de dicionario alegorico."  # indices[^5]
```

### 3.3 `genero_atribuido` + `justificativa_genero`

O patch mantém o enum de gênero, mas cria uma exigência mínima de justificativa quando há atribuição binária (`feminino`/`masculino`). A razão é que a própria literatura mobilizada indica definições móveis e disputadas de agência e significado, e que a alegoria feminina pode operar como representação substitutiva (representa sem governar), devendo portanto ser documentado o fundamento do julgamento (marcadores, legenda, convenção, etc.)[^10][^11].

**ANTES (v2.0.0)**

```yaml
genero_atribuido:
  allowed_values:
    - feminino
    - masculino
    - neutro
    - hibrido
    - ausente
  notes:
    - "Figura claramente feminina/masculina..."
```

**DEPOIS (v2.1.0)**

```yaml
genero_atribuido:
  allowed_values:
    - feminino
    - masculino
    - neutro
    - hibrido
    - ausente

justificativa_genero:
  type: string
  max_length: 280
  required_when:
    genero_atribuido:
      - feminino
      - masculino
  instructions:
    - "Explicitar o criterio: marcadores corporais, vestimenta, legenda/inscricao, convencao iconografica, ou fonte secundaria."
    - "Se houver disputa/ambiguidade, marcar confianca_codificacao e registrar motivo_incerteza."  # ambiguidade e leituras[^3][^4]
  rationale:
    - "Atribuicoes de genero e agencia sao historicamente moveis; alegorias femininas podem operar como representacao substitutiva do poder."  # shifting definitions e 'nao governa'[^10][^11]
```

## 4. Novos campos

Esta seção especifica cada novo campo com tipo, valores permitidos, regra de obrigatoriedade, exemplo e justificativa. A inclusão de campos de auditabilidade responde à crítica de neutralidade dos dados e à recomendação de perguntar quem se beneficia de um projeto/produto de dados, explicitando poder, contexto e trabalho[^2].

### 4.1 `dado_negativo`

```yaml
dado_negativo:
  type: boolean
  default: false
  meaning:
    true: "Ausencia (p.ex., ausencia de figura humana) e interpretativamente significativa para o item."
    false: "Ausencia nao e tratada como traço significativo (ou ha figura humana)."
  required: true
  example:
    dado_negativo: true
    genero_atribuido: ausente
    notes: "Brasao/selo estatal sem figura; ausencia como escolha de linguagem." 
  justification:
    - "A gramática visual juridica depende de como a justica e 'seen' ou 'sited'; o nao-figural pode integrar a comunicacao institucional."[^12]
    - "Icones carregam ambiguidade; registrar ausencia reduz inferencias retroativas."[^3]
```

### 4.2 `coder_position_statement`

```yaml
coder_position_statement:
  type: string
  max_length: 500
  required: true
  instructions:
    - "Declaracao curta de posicao: vinculo institucional, proximidade com o tema, experiencia e limites (p.ex., 'sou pesquisador/a...')."
  example:
    coder_position_statement: "Pesquisadora branca, formada em direito e historia da arte; foco em iconografia estatal; reconheco limites de leitura sobre repertorios afro-indigenas."
  justification:
    - "Registros devem ser tratados como capta, tomados e construidos; declarar posicao torna o julgamento auditavel."[^1]
    - "Poder, emocao, pluralidade e trabalho afetam projetos de dados; a posicao do/a codificador/a integra o contexto."[^2]
```

### 4.3 `power_at_stake`

```yaml
power_at_stake:
  type: string
  max_length: 300
  required: true
  instructions:
    - "Responder em uma frase: quem se beneficia (ou e prejudicado) por esta codificacao/representacao?"
  example:
    power_at_stake: "Instituicao estatal reforca aspiracao de imparcialidade ao exibir Justica; publics subalternizados podem nao se ver incluidos."
  justification:
    - "Para identificar discrepancias de poder, e preciso perguntar quem se beneficia e quais objetivos sao priorizados por um projeto/produto de dados."[^2]
```

### 4.4 `confianca_codificacao` e `motivo_incerteza`

```yaml
confianca_codificacao:
  type: enum
  allowed_values: [alta, media, baixa]
  required: true

motivo_incerteza:
  type: string
  max_length: 300
  required_when:
    confianca_codificacao: [media, baixa]
  example:
    confianca_codificacao: media
    motivo_incerteza: "Reproducao em baixa resolucao; edicao/gravura nao permite ver se ha venda."
  justification:
    - "A leitura do signo varia com espectadores, contextos e intencoes; registrar confianca impede 'fechamento' indevido da ambiguidade."[^4][^3]
    - "Evidencia iconografica pode variar por edicao; nem todas as alegorias sao ilustradas, o que afeta inferencias de atributos."[^6]
```

### 4.5 `finalidade_atribuida`

```yaml
finalidade_atribuida:
  type: enum
  allowed_values:
    - legitimacao_juridica
    - pedagogia_civica
    - dissuasao
    - comemoracao
    - branding_estatal
    - outro
  required: true
  instructions:
    - "Escolher a finalidade social presumida do dispositivo, com base em suporte, local de exibicao e retorica visual."
    - "Se 'outro', descrever em notes."
  example:
    finalidade_atribuida: legitimacao_juridica
  justification:
    - "A iconografia da justica levanta questoes sobre os 'goals of justice'; explicitar finalidade torna a interpretacao comparavel."[^13]
    - "lacuna na base de evidencia (busca neste piloto): operacionalizacao direta de Ihering nao esta citada no conjunto atual; este campo mitiga o problema ao registrar teleologia do dispositivo."[^13][^4]
```

### 4.6 `familia_alegorica` com `Afro_Brasileira`

```yaml
familia_alegorica:
  allowed_values:
    - Virtudes
    - Continentes
    - Oceanos_Rios
    - Nacional
    - Afro_Brasileira
    - Outra

familia_alegorica_notes:
  - "Afro_Brasileira: usar quando a figura/remissao iconografica se ancora prioritariamente em repertorios afro-diasporicos no Brasil (p.ex., atributos, entidades, cenas, ou tradicoes rituais), mesmo em dispositivo estatal/juridico." 
  - "lacuna na base de evidencia (busca neste piloto): o conjunto de citacoes atual sustenta a importancia de pluralidade/contexto, mas nao fornece tipologia iconografica afro-brasileira para enum fechada."[^2]
```

### 4.7 `relacao_com_repertorio_indigena`

```yaml
relacao_com_repertorio_indigena:
  type: enum
  allowed_values: [ausente, apropriado, coexistente, hibridizado, nao_aplicavel]
  required: true
  instructions:
    - "Codar a relacao entre a representacao e repertorios/figuras indígenas (motivos, corpos, armas, aderecos, presencas sociais)."
    - "Aplicar subaltern_caution: true quando houver apropriacao/hibridizacao ou quando o indigena for reduzido a tipo generico."
  example:
    relacao_com_repertorio_indigena: apropriado
    subaltern_caution: true
  justification:
    - "Repertorios coloniais feminilizam o Novo Mundo para exploracao/posse; este campo permite registrar essa operacao quando passa por figuras indígenas."[^14]
    - "Ha formulacoes explicitas de que, desde a conquista, nativos foram conceitualizados como femininos; isso requer registro analitico e nao apenas nota solta."[^15]
```

### 4.8 `fonte_imagem`, `edicao_suporte`, `tipo_reproducao`

```yaml
fonte_imagem:
  type: string
  required: true
  instructions:
    - "URL, arquivo, acervo, catalogo ou referencia bibliografica da imagem usada na codificacao."

edicao_suporte:
  type: string
  required: false
  instructions:
    - "Se aplicavel: edicao/ano/tipo de suporte (p.ex., 'litografia em jornal', 'edicao 1603', 'moeda 1910')."

tipo_reproducao:
  type: enum
  allowed_values: [foto_in_situ, scan_documento, fac-simile, catalogo, recorte_midia, outra]
  required: true

example:
  fonte_imagem: "Museu X, catalogo Y, item 12 (scan)"
  edicao_suporte: "litografia em revista (1891)"
  tipo_reproducao: scan_documento

justification:
  - "Ripa varia por series/edicoes e nem tudo e ilustrado; registrar edicao e suporte reduz erro de inferencia por ausencia material."[^6]
  - "A circulacao republicana e estudada via reproducoes impressas (jornais, revistas, panfletos); rastrear suporte e crucial para evidencia de circulacao."[^16]
```

## 5. Protocolo de confiabilidade intercodificador

A ambiguidade do ícone e a dependência do sentido em relação a contextos e intenções tornam necessário um protocolo explícito de dupla codificação e adjudicação, para não confundir “legibilidade” com neutralidade do framework interpretativo[^3][^4][^7].

```yaml
intercoder_reliability_protocol:
  enabled: true
  double_coding_sample:
    rate: 0.20  # 20% dos itens novos
    stratify_by:
      - funcao_juridica
      - familia_alegorica
  metric:
    name: krippendorff_alpha
    compute_per_field:
      - familia_alegorica
      - subtipo
      - genero_atribuido
      - objetos_regalia
      - marcas_corporais
      - marcadores_cena_arquitetura
      - vetor_colonial
      - finalidade_atribuida
  minimum_threshold:
    alpha: 0.67
    note: "Abaixo do limiar, revisar definicoes/treinamento e repetir rodada."
  disagreement_resolution:
    process:
      - "Revisao conjunta do item e das fontes/imagens (fonte_imagem, edicao_suporte, tipo_reproducao)."
      - "Registro de decisao final no log de adjudicacao."
    adjudicacao_log:
      type: array
      item_schema:
        item_id: string
        field: string
        coder_a: string
        coder_b: string
        decision: string
        rationale: string
        decided_at: "ISO-8601"
  justification:
    - "Como a leitura do signo depende de espectadores, contexto e intencoes, o desacordo e esperado e deve ser tratado como dado do processo, nao como erro invisivel."[^4]
```

## 6. Protocolo de freeze

Como repertórios e edições variam e o próprio processo de codificação incorpora trabalho e contexto, o freeze deve ser explicitado como etapa de governança do schema, evitando deriva silenciosa e tornando o trabalho visível[^6][^2].

```yaml
freeze_protocol:
  states:
    pre_freeze:
      description: "Piloto; campos e enums podem mudar."
      flag_field: pre_freeze_sample
      flag_value: true
    freeze_candidate:
      description: "Schema estabilizado; apenas correcoes menores permitidas."
      requirements:
        - "intercoder_reliability_protocol.executed == true"
        - "alpha >= minimum_threshold.alpha para campos centrais"
    freeze:
      description: "Versao congelada; mudancas exigem patch versionado."
      record:
        freeze_date: "(a preencher)"
        codebook_version: "2.1.0"
        hash: "(a preencher)"
  unfreeze_triggers:
    - "Descoberta de sobreposicao sistemica (campo/enum) que impede classificacao."
    - "Evidencia material nova (edicao/suporte) que invalida definicoes anteriores."  # variacao editorial e evidencia material[^6]
    - "Mudanca de escopo do corpus-core documentada."
```

## 7. Aplicacao dos 10 indicadores de purificacao por familia

A tabela abaixo é uma proposta operacional para explicitar, por família alegórica, a aplicabilidade dos 10 indicadores herdados do documento-pai. A justificativa geral é evitar que a “simplicidade e legibilidade” esconda o framework interpretativo (isto é, que um mesmo indicador seja aplicado sem explicitar condições e cautelas)[^7][^4].

| Indicador (doc-pai) | Virtudes | Continentes | Oceanos_Rios | Nacional |
|---|---|---|---|---|
| desincorporacao | aplicavel; registrar justificativa (corpo/atributos) e admitir ambiguidade do icone[^3] | aplicavel com subaltern_caution; continentes sao tipos genericizantes e generificados[^8][^9] | aplicavel com subaltern_caution; aguas podem ser personificadas e antropomorfizadas[^17] | aplicavel; alegorias nacionais femininas podem representar sem governar (atenção a substituição)[^11] |
| heraldizacao | aplicavel; atributos podem operar como indices de elementos (objetos) em suportes oficiais[^5] | aplicavel; repertorio circula em multiplos suportes e pode ser transposto para brasoes/sinais[^18] | aplicavel; suportes podem transformar figura em emblema generico (ver ambiguidade)[^3] | aplicavel; simbolos republicanos circulam com bandeiras/brasoes/hino e imagens acessiveis[^19] |
| enquadramento_arquitetonico | aplicavel; virtudes em espacos religiosos funcionam como representacao permanente e pedagogica[^20] | aplicavel; frontispicios/arquitetura enquadram continentes como stand-ins[^8] | aplicavel; agua pode ser “sited” em espaco/arquitetura e nao apenas vista como figura[^12] | aplicavel; justica pode ser “seen” ou “sited” e depende do lugar institucional[^12] |
| serialidade | aplicavel; repertorio indexavel permite repeticao de atributos por tipo[^5] | aplicavel; Four Continents circula em muitos meios e favorece repeticao[^18] | aplicavel; antropomorfismo de aguas e tradicao, permitindo repeticao tipologica[^17] | aplicavel; efígie/alegoria republicana aparece em pinturas/esculturas e em moedas/cedulas[^21] |
| inscricao_estatal | aplicavel quando em dispositivo estatal; estado pode usar iconografia para aspiracoes e poder[^22] | aplicavel quando em dispositivo estatal; hierarquia continental pode ser mobilizada como ordem do mundo[^9] | aplicavel quando em dispositivo estatal; registrar finalidade e contexto para evitar naturalizacao[^7] | aplicavel; iconografia comissionada pelo Estado pode representar “power” sob nome de justica[^23] |
| sacralizacao | aplicavel; arquitetura religiosa encena materias da fe e conduz o fiel[^20] | aplicavel; continentes podem aparecer em repertorios sacralizados por ordem do mundo (lacuna especifica no piloto)[^9][^4] | aplicavel; antropomorfismo pode adquirir tons miticos/rituais (lacuna especifica no piloto)[^17][^4] | aplicavel; regime republicano pode adaptar inspiracoes religiosas em mitos/simbolos[^24] |
| moralizacao | aplicavel; virtudes como governo moral e decoro pedagogico[^20] | aplicavel; America pode ser eroticizada e moralizada como “savage/cannibal” em hierarquia colonial[^9][^14] | aplicavel; se personificacao servir a narrativa moral/colonial (lacuna específica no piloto)[^4] | aplicavel; iconografia pode eliciar consentimento e sustentar claim de poder[^23] |
| despolitizacao | aplicavel; requer power_at_stake para evitar neutralizacao do conflito[^2] | aplicavel; stand-ins classicizantes podem mascarar violencia colonial sob genericidade[^8][^14] | aplicavel; registrar finalidade e quem se beneficia para evitar naturalizacao[^2] | aplicavel; Justica pode nao significar Justica para todos (risco de despolitizar desigualdade)[^13] |
| higienizacao | aplicavel; depende de leitura contextual e intencoes do observador[^4] | aplicavel; hierarquias europeias podem “civilizar” a ordem do mundo via imagem[^9] | aplicavel; cuidado com inferencias por genericidade (ambiguidade)[^3] | aplicavel; simbolos republicanos podem manter continuidade com tradicao anterior (limpa ruptura)[^25] |
| abstracao | aplicavel; atributos como indices permitem abstrair conceitos em figura[^26][^5] | aplicavel; continentes sao por definicao tipologias alegoricas (nao etnografia)[^8] | aplicavel; aguas personificadas combinam antropomorfismo e propriedades localizadas (abstracao localizada)[^17] | aplicavel; a alegoria estatal reivindica aspiracao de imparcialidade e poder via forma abstrata[^22] |

## 8. Atualizacao do bloco capta_required

O bloco de obrigatórios é ampliado para tornar capta auditável, dado que “data are not neutral” e que contexto/poder/trabalho afetam o projeto[^2]. Abaixo estão os blocos “ANTES/DEPOIS” prontos para colagem.

**ANTES (v2.0.0)**

```yaml
capta_required:
  capta_declaration: "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros."
  coder_id: "(obrigatorio)"
  coded_at: "(ISO 8601)"
  codebook_version: "2.0.0"
  pre_freeze_sample: true
```

**DEPOIS (v2.1.0)**

```yaml
capta_required:
  capta_declaration: "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros."
  coder_id: "(obrigatorio)"
  coded_at: "(ISO 8601)"
  codebook_version: "2.1.0"
  pre_freeze_sample: true
  coder_position_statement: "(obrigatorio; max 500 chars)"
  confianca_codificacao: "(obrigatorio; alta/media/baixa)"
```

## 9. Entrada no CHANGELOG.md

O trecho abaixo segue um formato de entrada pronto para colagem, preservando o estilo “mudança / re-pontua?”.

```markdown
| Versao | Data | Mudanca | Re-pontua itens anteriores? |
|--------|------|---------|----------------------------|
| 2.1.0 | 2026-06-23 | (i) Resolve sobreposicao de `subtipo` removendo `Brasil` de Continentes e criando `America_do_Sul`; (ii) divide `atributos_iconograficos` em `objetos_regalia`, `marcas_corporais`, `marcadores_cena_arquitetura`; (iii) adiciona `justificativa_genero`; (iv) adiciona campos de auditabilidade capta (`coder_position_statement`, `power_at_stake`, `confianca_codificacao`, `motivo_incerteza`); (v) adiciona rastreabilidade de suporte (`fonte_imagem`, `edicao_suporte`, `tipo_reproducao`); (vi) introduz `dado_negativo`, `finalidade_atribuida`, `relacao_com_repertorio_indigena`; (vii) adiciona `Afro_Brasileira` em `familia_alegorica`; (viii) define protocolo de confiabilidade intercodificador e freeze. | Nao (aplicavel apenas a novos ingestos a partir de 2.1.0) |
```

## 10. Plano de migracao

Este plano busca estabilidade e rastreabilidade do trabalho, reconhecendo que as leituras dependem de contexto e que a produção do registro envolve trabalho interpretativo[^4][^2].

- Itens já ingestados sob `codebook_version: 2.0.0` **não são re-pontuados** neste patch; permanecem como registros históricos do framework interpretativo vigente à época (evita “reescrever” o trabalho passado)[^2].
- Para itens legados, os novos campos podem ser preenchidos como **opcionais**, desde que se registre `coded_in_version: 2.0.0` (campo livre em `notes` ou novo campo administrativo local), preservando rastreabilidade de versão sob variação editorial/material de fontes[^6].
- Para novos ingestos em 2.1.0, `coder_position_statement`, `confianca_codificacao`, `power_at_stake`, `fonte_imagem` e `tipo_reproducao` passam a ser **obrigatórios**, pois contexto/poder/trabalho e a construção capta são parte do objeto metodológico do projeto[^2][^1].
- O piloto continua marcado como `pre_freeze_sample: true`, e o freeze fica condicionado à execução do protocolo de confiabilidade, dado que o sentido do signo é dependente de contexto e intenção e exige governança explícita do schema[^4].


[^1]: Humanities Approaches to Graphical Display.

[^2]: Mika, 2021. Book Review: Data Feminism. Journal of eScience Librarianship.

[^3]: Dennis et al., 2010. Essays Images of Justice.

[^4]: Hayaert, 2018. The Paradoxes of Lady Justice’s Blindfold.

[^5]: Maffei & Procaccioli, 2012. Cesare Ripa, Iconologia. A cura di Sonia Maffei. Testo stabilito da Paolo Procaccioli.

[^6]: Emblèmes 1603 : Cesare Ripa, Iconologia... (2e éd.; 1ère éd. illustrée), Rome, L. Facii | Utpictura18.

[^7]: Why Digital Humanists Should Emphasize Situated Data over ...

[^8]: Sutton, 2009. Mapping Meaning: Ethnography and Allegory in Netherlandish Cartography, 1570-1655. Itinerario: International Journal on the History of European Expansion and Global Interaction.

[^9]: Neumann, 2009. Imagining European community on the title page of Ortelius' Theatrum Orbis Terrarum (1570). Word & Image.

[^10]: Propst, 2016. From Vogue to the Virgin Mary: Marina Warner and Constructions of Female Agency in 1970s Feminism. Women's Studies.

[^11]: Nazario, 2026. Quem é a pessoa por trás do rosto nas moedas brasileiras? - Super Rádio Tupi.

[^12]: Tait, 2012. What We Didn’t See Before. Yale journal of law and the humanities.

[^13]: Lee, 2012. Book Review: Justice For All?.

[^14]: Detsi-Diamanti, 2006. Politicizing Aesthetics. Anachronist.

[^15]: Canessa, 2008. Sex And The Citizen: Barbies And Beauty Queens In The Age Of Evo Morales1. Journal of Latin American Cultural Studies.

[^16]: Marianne à brasileira: imagens republicanas e os d... - BV FAPESP, 2020.

[^17]: Taylor, 2009. River Raptures: Containment And Control Of Water In Greek And Roman Constructions Of Identity.

[^18]: Corbeiller, 1961. Miss America and Her Sisters: Personifications of the Four Parts of the World. Metropolitan Museum of Art Bulletin.

[^19]: Formation of Souls, 2023.

[^20]: Bastos, 2009. A maravilhosa fábrica de virtudes: o decoro na arquitetura religiosa de Vila Rica, Minas Gerais (1711-1822).

[^21]: Efígie da República (Brazil) - Eidolon Station, 2026.

[^22]: Resnik & Curtis, 2007. Representing Justice: From Renaissance Iconography to Twenty-First Century Courthouses.

[^23]: Isiksel, 2013. Representing justice: Invention, controversy and rights in city-states and democratic courtrooms. Contemporary Political Theory.

[^24]: Jurt, 2012. O Brasil: um Estado-nação a ser contruído. O papel dos símbolos nacionais, do Império à República.

[^25]: Jurt, 2014. Brazil: a Nation-state in the Making. Actes De La Recherche En Sciences Sociales.

[^26]: English Translations and Adaptations of Cesare Ripa's Iconologia: From the 17th to the 19th Century Hans-Joachim Zimmermann, De Zeventiende Eeuw. Jaargang 11 - DBNL.