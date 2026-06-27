```yaml
"$schema":
  codebook_id: lpai-v2
  codebook_version: 2.3.0
  codebook_version_anterior: 2.2.0
  data_versao: "(preencher)"
  documento_pai: data/docs/codebook.md
  reenquadramento_epistemico: schema/lpai-v2-as-capta.md
  documento_justificativo: schema/adendo-metodologico-v2.3.0.md
  patch_origem: schema/codebook-v2.3.0-patch.md
  status: piloto
  pre_freeze_sample: true
  descricao: >
    Schema LPAI v2.3.0 para codificar, como capta (tomadas interpretativas situadas), alegorias
    em dispositivos estatais/jurídicos brasileiros (brasões, moedas/cédulas, selos postais,
    arquitetura forense, frontispícios normativos, monumentos), com ênfase em Virtudes,
    Continentes e Oceanos/Rios, além de alegorias Nacionais e espaço para repertórios
    Afro-Brasileiros. Em v2.2.0 adicionou-se (i) um eixo explícito de temporalidade não-linear
    (anacronismo, constelação passado-presente, sobrevivências/Nachleben) e (ii) um eixo de
    contestação e afterlife (contramonumentalidade, remoções e intervenções). Em v2.3.0,
    adiciona-se (iii) um eixo explícito de gramática masculina (Hércules, Atlantes/Telamones,
    rios barbados, Netuno/Oceanus e casos brasileiros como o Gênio do Brasil), para que
    $$genero_atribuido = masculino$$ não opere como default invisível, mas como construção
    iconográfica auditável por marcas e funções recorrentes[^1][^2][^3][^4][^5][^6].

campos_capta_obrigatorios:
  nota_v230: >
    Em v2.3.0 não há novos capta obrigatórios universais. Regra de qualidade adicional:
    quando $$genero_atribuido = masculino$$ OU $$familia_alegorica = masculino_juridico$$,
    o campo justificativa_genero deve ser substantivo (>= 80 caracteres) e ancorado em
    marcas observáveis (p.ex. barba longa, postura de sustentação, semirrecosto fluvial,
    clava/atributos), evitando tratar o masculino como intuição ou neutralidade tácita;
    isto responde ao fato de que a barba/facial hair pode operar como significante hegemônico
    de autoridade e distinção social, e portanto exige auditabilidade explícita[^5].
  campos:
    - nome: capta_declaration
      tipo: string
      obrigatorio: true
      valor_fixo: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
      descricao: >
        Declaração fixa que marca todo registro como capta (não dado neutro), alinhando a
        exigência de reconceber dados como construídos/tomados e não como dados-dados[^1][^2].
      exemplo: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
    - nome: coder_id
      tipo: string
      obrigatorio: true
      descricao: Identificador do/a codificador/a responsável pelo registro.
      exemplo: coder_ana_001
    - nome: coded_at
      tipo: string
      obrigatorio: true
      formato: iso8601_datetime
      descricao: Data/hora da codificação (ISO 8601).
      exemplo: '2026-06-23T14:35:00-03:00'
    - nome: codebook_version
      tipo: string
      obrigatorio: true
      restricao: deve_igualar_codebook_version
      descricao: Deve ser igual à versão indicada neste arquivo.
      exemplo: '2.3.0'
    - nome: pre_freeze_sample
      tipo: bool
      obrigatorio: true
      descricao: Indica se o registro foi produzido em fase pré-freeze (piloto).
      exemplo: true
    - nome: coder_position_statement
      tipo: string
      obrigatorio: true
      max_chars: 500
      descricao: >
        Declaração curta de posição do/a codificador/a para tornar auditável a produção de capta,
        incluindo recortes de expertise, proximidade com o objeto e pressupostos interpretativos;
        operacionaliza a orientação de que dados/projetos são atravessados por poder, emoção,
        pluralidade e trabalho[^7].
      exemplo: >
        Historiadora da arte; foco em iconografia jurídica; codificação baseada em reprodução digital
        de catálogo institucional; atenção a convenções europeias de personificação.
    - nome: confianca_codificacao
      tipo: enum
      obrigatorio: true
      valores:
        - valor: alta
          label: Alta
          descricao: A evidência visual/documental é suficiente e estável.
        - valor: media
          label: Média
          descricao: Há ambiguidade relevante (atributos/estado de conservação/qualidade).
        - valor: baixa
          label: Baixa
          descricao: Atribuição depende fortemente de inferência e/ou a reprodução é inadequada.
      descricao: >
        Autoavaliação de confiança para explicitar a incerteza interpretativa inerente à leitura de
        ícones (ambiguidade do concreto) e a dependência de contexto/intenções do observador[^8][^9].
      exemplo: media
    - nome: motivo_incerteza
      tipo: string
      obrigatorio: false
      max_chars: 300
      condicional: 'obrigatorio_quando: confianca_codificacao != alta'
      descricao: Justificativa curta para incertezas (p.ex., imagem parcial, edição divergente).
      exemplo: Figura parcialmente coberta por carimbo; atributos não distinguíveis.

campos_identificacao:
  - nome: item_id
    tipo: string
    obrigatorio: true
    descricao: Identificador único do item no repositório.
    exemplo: LPAI-0001
  - nome: titulo
    tipo: string
    obrigatorio: true
    descricao: Título curto descritivo do item.
    exemplo: Efígie da República em moeda
  - nome: suporte
    tipo: enum
    obrigatorio: true
    valores:
      - valor: moeda
        label: Moeda
        descricao: Moeda oficial.
      - valor: cedula
        label: Cédula
        descricao: Papel-moeda oficial.
      - valor: selo_postal
        label: Selo postal
        descricao: Selo postal oficial.
      - valor: brasao_selo
        label: Brasão/Selo
        descricao: Brasão de armas, selo de Estado, emblema heráldico.
      - valor: frontispicio
        label: Frontispício
        descricao: Frontispício de obra normativa/compilação.
      - valor: arquitetura
        label: Arquitetura
        descricao: Fachada/interior de edifício judicial.
      - valor: monumento
        label: Monumento
        descricao: Monumento público.
      - valor: outro
        label: Outro
        descricao: Outro suporte; detalhar em notes.
    descricao: Categoria material do artefato/registro.
    exemplo: moeda
  - nome: data_suporte
    tipo: string
    obrigatorio: false
    descricao: Data do suporte (ano, intervalo, ou data completa, conforme disponível).
    exemplo: '1889'
  - nome: instituicao_origem
    tipo: string
    obrigatorio: false
    descricao: Instituição que emitiu/mandou produzir o item.
    exemplo: Casa da Moeda do Brasil
  - nome: localizacao_atual
    tipo: string
    obrigatorio: false
    descricao: Acervo/coleção onde o item está localizado.
    exemplo: Museu Histórico Nacional
  - nome: fonte_imagem
    tipo: string
    obrigatorio: true
    descricao: URL, referência de catálogo, arquivo local ou repositório de onde a imagem foi obtida.
    exemplo: https://acervo.exemplo.br/item/123
  - nome: edicao_suporte
    tipo: string
    obrigatorio: false
    descricao: >
      Edição/estado do suporte quando aplicável (p.ex., edição de livro, série de moedas, tiragem),
      reconhecendo que repertórios e atributos podem variar materialmente entre edições[^10][^11].
    exemplo: 2a edição ilustrada (estado A)
  - nome: tipo_reproducao
    tipo: enum
    obrigatorio: true
    valores:
      - valor: original
        label: Original
        descricao: Registro fotográfico do objeto original.
      - valor: reproducao_fotografica
        label: Reprodução fotográfica
        descricao: Foto de reprodução (catálogo, livro, etc.).
      - valor: gravura_impressa
        label: Gravura impressa
        descricao: Reprodução por gravura/litografia.
      - valor: digital
        label: Digital
        descricao: Nascido-digital ou digitalização.
      - valor: outro
        label: Outro
        descricao: Outro tipo; detalhar em notes.
    descricao: Tipo de reprodução utilizada para a codificação.
    exemplo: digital

campos_analiticos_principais:
  - nome: familia_alegorica
    tipo: enum
    obrigatorio: true
    valores:
      - valor: virtudes
        label: Virtudes
        descricao: Personificação de virtude cardinal/teologal/jurídica.
      - valor: continentes
        label: Continentes
        descricao: Personificação de continente/região.
      - valor: oceanos_rios
        label: Oceanos/Rios
        descricao: Corpo d’água personificado/simbolizado.
      - valor: nacional
        label: Nacional
        descricao: Alegoria de nação/república/liberdade/pátria.
      - valor: afro_brasileira
        label: Afro-Brasileira
        descricao: >
          Repertórios afro-diaspóricos/afro-brasileiros em circulação no espaço estatal/jurídico.
          Nota: categoria introduzida por exigência analítica de poder/beneficiários; base direta
          ainda é lacuna neste piloto[^7].
      - valor: masculino_juridico
        label: Masculino Jurídico
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Gramática masculina em contexto estatal/jurídico (p.ex., Hércules como dispositivo de
          decisão/pedagogia, Atlantes/Telamones como suporte, rios barbados como territorialização,
          e casos brasileiros como o Gênio do Brasil), evitando que $$genero_atribuido = masculino$$
          seja tratado como residual ou default invisível[^6][^4][^12].
      - valor: outra
        label: Outra
        descricao: Nenhuma das anteriores; justificar.
    descricao: Família iconográfica predominante.
    exemplo: nacional
    notas_v230: 'Enum expandido com masculino_juridico.'
    justificativa_teorica: >
      A codificação por famílias organiza repertórios transferíveis e prescritivos (p.ex., Ripa como
      handbook de alegorias) ao mesmo tempo em que exige explicitar efeitos de poder e exclusão na
      alegoria estatal; em v2.3.0, inclui-se uma família para a gramática masculina a fim de tornar
      auditável a masculinidade como construção e não como neutralidade implícita[^13][^14][^7][^5].

  - nome: subtipo
    tipo: enum
    obrigatorio: true
    valores_por_familia:
      virtudes:
        - valor: iustitia
          label: Iustitia
          descricao: Justiça como virtude/jurisdição.
        - valor: veritas
          label: Veritas
          descricao: Verdade.
        - valor: prudentia
          label: Prudência
          descricao: Prudência.
        - valor: fortaleza
          label: Fortaleza
          descricao: Fortaleza.
        - valor: temperanca
          label: Temperança
          descricao: Temperança.
        - valor: justica_e_paz
          label: Justiça e Paz
          descricao: Composição alegórica combinada.
        - valor: esperanca
          label: Esperança
          descricao: Virtude teologal.
        - valor: caridade
          label: Caridade
          descricao: Virtude teologal.
        - valor: fe
          label: Fé
          descricao: Virtude teologal.
        - valor: fama
          label: Fama
          descricao: Fama/Glória.
        - valor: outra_virtude
          label: Outra virtude
          descricao: Outra; justificar.
      continentes:
        - valor: europa
          label: Europa
          descricao: Europa como referência hierárquica em quarteto continental[^15].
        - valor: america
          label: América
          descricao: América (Novo Mundo) como personificação feminina frequentemente erotizada e subordinada[^16].
        - valor: africa
          label: África
          descricao: África como continente em quarteto.
        - valor: asia
          label: Ásia
          descricao: Ásia como continente em quarteto.
        - valor: america_do_sul
          label: América do Sul
          descricao: Subtipo regional quando a alegoria marca recorte sul-americano (não confundir com Brasil-nação).
        - valor: outro_continente
          label: Outro
          descricao: Outro; justificar.
      oceanos_rios:
        - valor: oceano
          label: Oceano
          descricao: Oceano personificado/simbolizado.
        - valor: rio_grande
          label: Rio grande
          descricao: Rio principal (p.ex., Amazonas).
        - valor: rio_menor
          label: Rio menor
          descricao: Afluente/curso menor.
        - valor: fonte
          label: Fonte
          descricao: Fonte/nascente.
        - valor: netuno
          label: Netuno
          descricao: Figura mitológica (mar) em variações de gênero e sentido histórico[^17].
        - valor: tetis
          label: Tétis
          descricao: Figura mitológica (mar) e recodificação feminina em certas tradições[^17].
        - valor: outro_hidrico
          label: Outro hídrico
          descricao: Outro; justificar.
      nacional:
        - valor: republica
          label: República
          descricao: Personificação da República (p.ex., efígie feminina).[^18][^19]
        - valor: liberdade
          label: Liberdade
          descricao: Liberdade como alegoria nacional.
        - valor: patria
          label: Pátria
          descricao: Pátria.
        - valor: brasil
          label: Brasil
          descricao: Brasil como nação (subtipo reservado aqui).[^20]
        - valor: outra_nacional
          label: Outra nacional
          descricao: Outra; justificar.
      afro_brasileira:
        - valor: orixa
          label: Orixá
          descricao: Referência a orixá(s) em repertório visual.
        - valor: entidade
          label: Entidade
          descricao: Entidade afro-diaspórica não classificada como orixá.
        - valor: simbolo_ritual
          label: Símbolo ritual
          descricao: Ferramenta/insígnia ritual em contexto estatal.
        - valor: outra_afro
          label: Outra afro-brasileira
          descricao: Outra; justificar.
      masculino_juridico:
        - valor: hercules
          label: Hércules
          descricao: >
            Figura masculina do tipo hercúleo (p.ex., nudez + clava) e/ou identificável por
            substituição atributiva em programas luso-brasileiros (cetro/vara manejado
            'como Hercules a sua clava')[^6][^12].
        - valor: atlante
          label: Atlante
          descricao: >
            Figura do tipo Atlas/Atlante (suporte do globo; operador de sustentação e conexão
            do mundo), distinta de telamon arquitetônico[^21].
        - valor: telamon
          label: Telamon
          descricao: >
            Figura masculina em função de suporte arquitetônico (atlantes/telamones como colunas
            antropomórficas) e ênfase em postura de sustentação[^4].
        - valor: rio_barbado
          label: Rio barbado
          descricao: >
            Personificação aquática masculina reconhecível por coocorrência de barba longa,
            semirrecosto e efluência hídrica (urna/vaso vertente)[^3][^5].
        - valor: netuno
          label: Netuno
          descricao: >
            Personificação do mar (Ocidente frequentemente masculina por Oceanus/Titã; Bizâncio
            frequentemente feminina por Tétis), com transformações iconográficas e semânticas ao
            longo do tempo[^17].
        - valor: genio_protetor
          label: Gênio protetor
          descricao: >
            Caso brasileiro de masculinidade ativa em chave de protetorado/união/poder
            (p.ex., Gênio do Brasil como guerreiro e protetor; instrumento de poder e união
            nacional em torno da monarquia)[^12].
        - valor: heroi_civil
          label: Herói civil
          descricao: Herói civil/figura masculina de autoridade; exigir justificativa.
        - valor: outro_masculino
          label: Outro masculino
          descricao: Outro; justificar.
      outra:
        - valor: outra
          label: Outra
          descricao: Outra; justificar.
    descricao: Especificação dentro da família.
    exemplo: republica
    notas_v230: 'Expandido com valores por familia masculino_juridico.'
    justificativa_teorica: >
      Subtipos estabilizam repertórios prescritivos, mas devem preservar que personificações
      são stand-ins alegóricos e não etnografia documental; no eixo masculino, subtipos reduzem
      a dependência de nomeação nominal e explicitam gramáticas de reconhecimento por postura,
      atributos e função (p.ex., clava; globo; semirrecosto + urna vertente)[^22][^3][^21][^6].

  - nome: objetos_regalia
    tipo: list
    obrigatorio: false
    valores:
      - valor: balanca
        label: Balança
        descricao: Balança (Iustitia).
      - valor: espada
        label: Espada
        descricao: Espada (força/coerção na justiça).[^23]
      - valor: venda
        label: Venda
        descricao: Venda/olhos vendados.
      - valor: espelho
        label: Espelho
        descricao: Espelho (p.ex., Veritas).
      - valor: tocha
        label: Tocha
        descricao: Tocha.
      - valor: globo
        label: Globo
        descricao: Globo/orbe.
      - valor: cornucopia
        label: Cornucópia
        descricao: Cornucópia.
      - valor: cetro
        label: Cetro
        descricao: Cetro.
      - valor: coroa
        label: Coroa
        descricao: Coroa.
      - valor: tridente
        label: Tridente
        descricao: Tridente (Netuno).
      - valor: fasces
        label: Fasces
        descricao: Fasces.
      - valor: bandeira
        label: Bandeira
        descricao: Bandeira.
      - valor: ramos_estrelas
        label: Ramos e estrelas
        descricao: Ramos/estrelas de brasão republicano.
      - valor: urna
        label: Urna
        descricao: Urna.
      - valor: incensario
        label: Incensário
        descricao: Incensário.
      - valor: clava
        label: Clava
        notas_v230: 'NOVO em 2.3.0.'
        descricao: Clava (atributo hercúleo).[^6]
      - valor: leao_pele
        label: Pele de leão
        notas_v230: 'NOVO em 2.3.0.'
        descricao: 'Pele de leão (atributo hercúleo). Nota: lacuna na base de evidência (busca neste piloto).'
      - valor: urna_vertedora
        label: Urna vertedora
        notas_v230: 'NOVO em 2.3.0.'
        descricao: 'Vasilha/urna associada à efluência hídrica em personificações aquáticas.'
      - valor: vaso_fluvial
        label: Vaso fluvial
        notas_v230: 'NOVO em 2.3.0.'
        descricao: 'Vaso/vasilha associada a rio/deus fluvial; quando vertente, codificar também tipo_efluencia_hidrica.'
      - valor: tridente_imperial
        label: Tridente imperial
        notas_v230: 'NOVO em 2.3.0.'
        descricao: 'Tridente em chave de soberania/insígnia; lacuna na base de evidência (busca neste piloto).'
      - valor: ancora_naval
        label: Âncora naval
        notas_v230: 'NOVO em 2.3.0.'
        descricao: 'Âncora como marcador de soberania marinha/infraestrutura; lacuna na base de evidência (busca neste piloto).'
      - valor: outro_objeto
        label: Outro objeto
        descricao: Outro; detalhar.
    descricao: Lista de objetos/regália visíveis (atributos materiais).[^13]
    exemplo:
      - balanca
      - espada
    notas_v230: 'Enum expandido para gramática masculina (Hércules, rios barbados, maritimidade).'
    justificativa_teorica: >
      A lógica de indexar elementos (objetos/animais/cores) aproxima a codificação de um método
      de decomposição de alegorias em componentes repetíveis; no eixo masculino, a clava e a urna
      vertente funcionam como atributos discriminantes de reconhecimento e devem ser controláveis
      como vocabulário[^13][^6][^3].

  - nome: marcas_corporais
    tipo: list
    obrigatorio: false
    valores:
      - valor: corpo_reclinado
        label: Corpo reclinado
        descricao: Pose reclinada (comum em alegorias de América/rios).[^16]
      - valor: barba
        label: Barba
        descricao: Barba (marcador corporal frequentemente masculinizado).
      - valor: corpo_ereto
        label: Corpo ereto
        descricao: Postura em pé.
      - valor: corpo_sentado
        label: Corpo sentado
        descricao: Postura sentada (p.ex., entronização).[^15]
      - valor: nudez_parcial
        label: Nudez parcial
        descricao: Nudez parcial.
      - valor: nudez_total
        label: Nudez total
        descricao: Nudez total (p.ex., América em convenção dominante).[^16]
      - valor: vestes_romanas
        label: Vestes romanas
        descricao: Classicismo (toga/estilo romano).[^19]
      - valor: vestes_indigenas
        label: Vestes indígenas
        descricao: Marcadores de indigenidade (quando visíveis).
      - valor: vestes_africanas
        label: Vestes africanas
        descricao: Marcadores afro-diaspóricos (quando visíveis).
      - valor: barba_longa
        label: Barba longa
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Barba longa como marcador de masculinidade/autoridade; pode operar como significante
          hegemônico e exige coocorrências para inferir personificação hídrica[^5].
      - valor: corpo_ereto_em_esforco
        label: Corpo ereto em esforço
        notas_v230: 'NOVO em 2.3.0.'
        descricao: Postura corporal em esforço/impulso (p.ex., decisão/ação).[^6]
      - valor: corpo_semirrecosto_fluvial
        label: Corpo semirrecosto fluvial
        notas_v230: 'NOVO em 2.3.0.'
        descricao: Postura de semirrecosto típica do tipo aquático (rio/mar) barbado.[^3]
      - valor: musculatura_exibida
        label: Musculatura exibida
        notas_v230: 'NOVO em 2.3.0.'
        descricao: Ênfase de corporeidade e força (frequente em gramáticas hercúleas/atlanteanas).[^6][^21]
      - valor: postura_de_sustentacao
        label: Postura de sustentação
        notas_v230: 'NOVO em 2.3.0.'
        descricao: Postura que indica suporte/carga (atlantes/telamones).[^4]
      - valor: gesto_indicativo_pedagogico
        label: Gesto indicativo pedagógico
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Gesto de indicar/mediar, p.ex. figura masculina 'vestida all’antica' que aponta a Justiça,
          operando como mediação entre esfera divina e do direito[^24].
      - valor: outro_marcador
        label: Outro
        descricao: Outro; detalhar.
    descricao: Lista de marcas corporais/poses/vestes (atributos do corpo).
    exemplo:
      - vestes_romanas
      - corpo_sentado
    notas_v230: 'Enum expandido com marcadores da gramática masculina (barba longa; semirrecosto; sustentação).'
    justificativa_teorica: >
      Separar atributos-corpo ajuda a evitar confundir convenção alegórica com documentação etnográfica;
      no eixo masculino, a barba deve ser tratada como marcador socialmente carregado e não como
      evidência autoevidente de tipo fluvial, exigindo coocorrências com postura e efluência[^22][^5][^3].

  - nome: marcadores_cena_arquitetura
    tipo: list
    obrigatorio: false
    valores:
      - valor: arco_e_flecha
        label: Arco e flecha
        descricao: Arco e flecha (convenção associada à América).[^16]
      - valor: cabeca_decepada
        label: Cabeça decepada
        descricao: Cabeça decepada (p.ex., América canibal).[^15]
      - valor: animais_exoticos
        label: Animais exóticos
        descricao: Animais exóticos.
      - valor: cobra
        label: Cobra
        descricao: Cobra.
      - valor: escorpiao
        label: Escorpião
        descricao: Escorpião.
      - valor: coroa_de_junco
        label: Coroa de junco
        descricao: Coroa de junco.
      - valor: ondas_maritimas
        label: Ondas marítimas
        descricao: Ondas/mar.
      - valor: outro_cena
        label: Outro
        descricao: Outro; detalhar.
    descricao: Marcadores de cena, ambiente, fauna/flora e/ou enquadramento.
    exemplo:
      - ondas_maritimas
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      Personificações continentais operam por accoutrements e stand-ins; codificar separadamente
      sustenta leituras coloniais sem confundir com etnografia literal[^22].

  - nome: genero_atribuido
    tipo: enum
    obrigatorio: true
    valores:
      - valor: feminino
        label: Feminino
        descricao: Figura claramente feminina.
      - valor: masculino
        label: Masculino
        descricao: Figura claramente masculina.
      - valor: neutro
        label: Neutro
        descricao: Sem marcadores de gênero.
      - valor: hibrido
        label: Híbrido
        descricao: Atributos dualizados.
      - valor: ausente
        label: Ausente
        descricao: Não há figura humana.
    descricao: Gênero predominante da personificação.
    exemplo: feminino
    notas_v230: 'Sem mudança em 2.3.0; regra de justificativa reforçada para masculino.'
    justificativa_teorica: >
      A alegoria estatal frequentemente mobiliza a forma feminina (República/Justiça), mas isso não
      implica inclusão política; em v2.3.0, o masculino também é tratado como construção iconográfica
      situada (p.ex., barba como marcador hegemônico de autoridade), exigindo justificativa explícita[^18][^25][^5].

  - nome: justificativa_genero
    tipo: string
    obrigatorio: false
    max_chars: 300
    condicional: 'obrigatorio_quando: genero_atribuido in [feminino, masculino]'
    regras_v230:
      - quando: 'genero_atribuido == masculino'
        min_chars: 80
      - quando: 'familia_alegorica == masculino_juridico'
        min_chars: 80
    descricao: >
      Justificativa curta baseada em marcadores visíveis (vestes, corpo, barba, postura, clava,
      semirrecosto/urna etc.), evitando que o gênero seja tratado como dado autoevidente.
    exemplo: >
      Figura masculina com barba longa e corpo semirrecostado; braço apoiado em urna vertente; conjunto
      de marcas sugere personificação aquática.
    notas_v230: 'Regra de substantividade adicionada para masculino (min_chars 80).'
    justificativa_teorica: >
      Leituras de gênero alegórico são historicamente instáveis e atravessadas por fantasias;
      exigir justificativa reduz o risco de codificação reificante; no masculino, reforça-se
      que marcas como barba operam como significantes hegemônicos e podem ser sobreinterpretadas
      se não forem contextualizadas por coocorrências[^26][^27][^5][^3].

  - nome: funcao_juridica
    tipo: enum
    obrigatorio: true
    valores:
      - valor: tribunal_consciencia
        label: Tribunal de consciência
        descricao: Igreja/barroco como espaço de legitimação pública/jurídica.
      - valor: frontispicio_normativo
        label: Frontispício normativo
        descricao: Frontispício de código/ordenação/compilação.
      - valor: moeda_cedula
        label: Moeda ou cédula
        descricao: Moeda/cédula oficial.
      - valor: selo_postal
        label: Selo postal
        descricao: Selo postal oficial.
      - valor: brasao
        label: Brasão
        descricao: Brasão de armas/selo de Estado.
      - valor: arquitetura_forense
        label: Arquitetura forense
        descricao: Tribunal/foro/palácio de justiça.
      - valor: monumento_publico
        label: Monumento público
        descricao: Monumento em espaço público.
      - valor: monumento_contestado
        label: Monumento contestado
        descricao: >
          Monumento cuja forma pública inclui contestação documentada (defaced/removido/contramonumentalizado)
          e cujo sentido passa a depender de afterlife e disputa no espaço comum[^28][^29].
      - valor: paratexto_normativo
        label: Paratexto normativo
        descricao: Capa/paratexto de norma.
      - valor: outro
        label: Outro
        descricao: Outro; justificar.
    descricao: Função do dispositivo no espaço jurídico-estatal.
    exemplo: moeda_cedula
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      A iconografia jurídica deve ser lida em conexão com renderizações visuais do direito e seus
      contextos "seen/sited" (imagem e sítio/arquitetura), e não apenas como lista de atributos[^30][^31].

  - nome: vetor_colonial
    tipo: enum
    obrigatorio: true
    valores:
      - valor: europeu_direto
        label: Europeu direto
        descricao: Repertório europeu aplicado no Brasil sem mediação lusa evidente.
      - valor: luso_brasileiro
        label: Luso-brasileiro
        descricao: Transmissão via Portugal e/ou cultura colonial.
      - valor: republicano_brasileiro
        label: Republicano brasileiro
        descricao: Produzido pelo Estado republicano brasileiro.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Sem dimensão colonial comparável.
    descricao: Rota de transmissão do repertório.
    exemplo: republicano_brasileiro
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      A circulação de repertórios alegóricos em múltiplos suportes sugere vetores de transferências
      e serialidade, inclusive para dispositivos estatais[^32].

  - nome: hipotese_racial
    tipo: string
    obrigatorio: false
    max_chars: 500
    descricao: >
      Campo interpretativo curto articulando como gênero e raça se cruzam na personificação; usar
      evidência visual e contexto de circulação, lembrando que alegorias de continentes não são
      evidência documental de "povos diversos", mas construções genericamente classicizantes[^22][^16].
    exemplo: >
      América como mulher nua reclinada; erotização e alteridade; contraste com Europa entronizada
      sugere hierarquia colonial.
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      A tradição figurativa do Novo Mundo produz terra feminilizada disponível à exploração e posse,
      articulando gênero e colonialidade[^16].

  - nome: referencia_genealogica
    tipo: list
    obrigatorio: true
    valores:
      - valor: ripa_1593_1603
        label: Ripa (1593/1603)
        descricao: Iconologia como dicionário/handbook.
      - valor: ortelius_1570
        label: Ortelius (1570)
        descricao: Theatrum Orbis Terrarum e personificações continentais.
      - valor: collaert_four_continents
        label: Collaert (Four Continents)
        descricao: Série de Quatro Continentes.
      - valor: carriera_four_continents
        label: Carriera (Four Continents)
        descricao: Série de Quatro Continentes.
      - valor: warner_1985
        label: Warner
        descricao: Crítica do feminino alegórico e agência.
      - valor: resnik_curtis_2011
        label: Resnik & Curtis (2011)
        descricao: Iconografia da justiça e espaço adjudicativo.
      - valor: souza_2014
        label: Souza (2014)
        descricao: América alegorizada e imaginários do Novo Mundo.
      - valor: ihering_der_zweck
        label: Ihering (Der Zweck)
        descricao: Teleologia do direito e luta.
      - valor: warburg_mnemosyne
        label: Warburg (Mnemosyne)
        descricao: Nachleben/Pathosformel e montagem-atlas.[^33][^34]
      - valor: didi_huberman_devant_le_temps
        label: Didi-Huberman (Devant le temps)
        descricao: Anacronismo como riqueza interior às imagens.[^35][^36]
      - valor: young_counter_monument
        label: Young (Counter-monument)
        descricao: Contramonumento e memória-processo (provoca, interação, change over time).[^37][^38][^39]
      - valor: panofsky_hercules_am_scheidewege
        label: Panofsky (Hercules am Scheidewege)
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Chave proposta para bibliografia canônica sobre o bivio ercúleo como cena pedagógica de
          distinção (falso/verdadeiro; virtude/vício). Nota: entrada funciona como ponte de
          rastreabilidade; lacuna na base de evidência para referência fechada (busca neste piloto)[^6].
      - valor: lubbock_atlantes
        label: Lubbock (Atlantes)
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Placeholder para bibliografia sobre atlantes/telamones como colunas antropomórficas de
          sustentação. Nota: lacuna na base de evidência para referência fechada (busca neste piloto)[^4].
      - valor: brazilian_republican_iconography
        label: Iconografia republicana brasileira (masculino)
        notas_v230: 'NOVO em 2.3.0.'
        descricao: >
          Placeholder para estudos sobre gramáticas masculinas no Brasil (Gênio do Brasil;
          rios colossais Amazonas/Prata; heroísmos civis). Nota: lacuna na base de evidência para
          referência fechada (busca neste piloto)[^12].
      - valor: outra
        label: Outra
        descricao: Outra referência; especificar.
    descricao: Chaves de referência genealógica predominante (pode ser múltipla).
    exemplo:
      - resnik_curtis_2011
      - ripa_1593_1603
      - didi_huberman_devant_le_temps
      - panofsky_hercules_am_scheidewege
    notas_v230: 'Expandida em 2.3.0 com três chaves para gramática masculina.'
    justificativa_teorica: >
      A codificação deve tornar explícitas mediações textuais/repertoriais (prescrição/circulação)
      e, em v2.2.0+, também mediações temporais e regimes de contestação/afterlife; em v2.3.0,
      inclui-se rastreabilidade específica para a gramática masculina (Hércules/atlantes/rios barbados)
      que opera por funções e marcas corporais recorrentes[^40][^13][^29][^3][^4][^6].

  - nome: dado_negativo
    tipo: bool
    obrigatorio: true
    descricao: >
      Marca itens em que a ausência de figura humana é analiticamente significativa (ex.: brasões
      estatais sem personificação), permitindo registrar ausências como parte do significado.
    exemplo: false
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      Como a leitura de signos depende de contextos e intenções, o “negativo” deve ser registrável
      como capta (ausência com efeito interpretativo), não como simples missing[^9][^1].

  - nome: power_at_stake
    tipo: string
    obrigatorio: false
    max_chars: 300
    descricao: >
      Quem se beneficia (e quem é marginalizado) pela circulação/codificação deste item; campo de
      auditoria de poder conforme a exigência de perguntar “who benefits” em projetos de dados[^7].
    exemplo: Elites republicanas; legitimação visual do regime por ícone classicizante.
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      Dados e projetos são atravessados por poder e objetivos priorizados; registrar isso torna a
      codificação responsiva a assimetrias[^7].

  - nome: finalidade_atribuida
    tipo: enum
    obrigatorio: true
    valores:
      - valor: legitimacao_juridica
        label: Legitimação jurídica
        descricao: Sustentar autoridade do direito/Estado.
      - valor: pedagogia_civica
        label: Pedagogia cívica
        descricao: Educar valores cívicos/virtudes.
      - valor: dissuasao
        label: Dissuasão
        descricao: Intimidar/dissuadir por símbolos de força.
      - valor: comemoracao
        label: Comemoração
        descricao: Comemorar evento/figura.
      - valor: branding_estatal
        label: Branding estatal
        descricao: Marcar identidade estatal/nacional por símbolo repetível.
      - valor: outro
        label: Outro
        descricao: Outro; justificar.
    descricao: >
      Finalidade social/política atribuída ao artefato (teleologia), explicitando o direito como meio
      para fins sociais e a função mediadora entre interesses[^41][^42].
    exemplo: branding_estatal
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      Em Ihering, o direito é “merely a means to an end” orientado à existência da sociedade;
      codificar finalidade torna a iconografia legível como condensação de Zweck institucional[^41].

  - nome: relacao_com_repertorio_indigena
    tipo: enum
    obrigatorio: true
    valores:
      - valor: ausente
        label: Ausente
        descricao: Sem repertório indígena identificável.
      - valor: apropriado
        label: Apropriado
        descricao: Repertório indígena apropriado/exotizado.
      - valor: coexistente
        label: Coexistente
        descricao: Coexistência sem fusão.
      - valor: hibridizado
        label: Hibridizado
        descricao: Hibridização de repertórios.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Item onde a categoria não faz sentido.
    descricao: >
      Relação do item com repertórios indígenas; se diferente de nao_aplicavel, aplicar
      subaltern_caution e explicitar a base de evidência.
    exemplo: ausente
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      Personificações coloniais podem feminilizar e hierarquizar alteridades, exigindo rastrear
      regimes de representação e poder[^16][^43].

  - nome: status_evidencia
    tipo: enum
    obrigatorio: true
    valores:
      - valor: core_verificado
        label: Core verificado
        descricao: Evidência visual/documental suficiente para uso em análises do corpus core.
      - valor: piloto
        label: Piloto
        descricao: Em codificação; gaps pendentes; evidência parcial.
      - valor: comparador
        label: Comparador
        descricao: Usado para genealogia comparativa; não entra em estatísticas do corpus core.
      - valor: apendice
        label: Apêndice
        descricao: Caso-limite citado em notes.
    descricao: >
      Status de evidência e inclusão (core vs comparador), com regra adicional para itens contestados,
      para evitar tratar remoções/contestações como endpoints sem trilha de afterlife/counterarchive[^29].
    exemplo: piloto
    notas_v230: 'Sem mudança em 2.3.0.'

  - nome: subaltern_caution
    tipo: bool
    obrigatorio: false
    descricao: >
      Marca cautela quando escalas/categorias são aplicadas a casos subalternizados, masculinos
      ou de ausência.
    exemplo: true
    notas_v230: 'Sem mudança em 2.3.0.'
    justificativa_teorica: >
      A ambiguidade dos ícones e a dependência de leitura contextual recomendam registrar cautelas
      e não naturalizar categorias como universais[^8][^9].

  - nome: notes
    tipo: string
    obrigatorio: false
    descricao: Observações livres para justificativas adicionais, conflitos de edição, etc.
    exemplo: Edição do catálogo não informa se a venda está presente; registrar como incerto.

  # --- CAMPOS V2.2.0: temporalidade/Warburg-Didi-Huberman ---
  - nome: nachleben_marker
    tipo: bool
    obrigatorio: false
    notas_v220: 'NOVO em 2.2.0.'
    descricao: >
      Marca a hipótese de sobrevivência/retorno (Nachleben) de uma forma/motivo, entendendo que
      formas não “morrem” e podem reaparecer com re-semantização em tempos posteriores[^33][^44].
    exemplo: true
    justificativa_teorica: >
      Nachleben descreve a pós-vida de formas e seu retorno re-semantizado; o campo evita tratar
      recorrências como mera repetição cronológica[^33].

  - nome: camadas_temporais
    tipo: list
    obrigatorio: false
    condicional: 'obrigatorio_quando: nachleben_marker == true'
    notas_v220: 'NOVO em 2.2.0.'
    descricao: >
      Lista de camadas temporais (tempo impuro) que compõem o sentido do item, reconhecendo que o
      anacronismo é uma riqueza interior às imagens e que “todos os tempos se encontram” nelas[^35][^36][^44].
    estrutura_itens:
      - campo: data_aprox
        tipo: string
        descricao: Data aproximada (YYYY, YYYY-MM, YYYY-MM-DD, ou 'c. YYYY').
      - campo: descricao
        tipo: string
        descricao: Descrição da camada (p.ex., barroca, republicana, recontextualização contemporânea).
      - campo: fonte_iconografica
        tipo: string
        descricao: Fonte/arquivo/modelo invocado (repertório, paratexto, catálogos).
    exemplo:
      - data_aprox: c. 1730
        descricao: Camada barroca/tridentina do repertório alegórico
        fonte_iconografica: '(preencher)'
      - data_aprox: c. 1900
        descricao: Reaparecimento em dispositivo estatal (re-semantização)
        fonte_iconografica: '(preencher)'
    justificativa_teorica: >
      A sobrevivência “anachronise” a história ao pensar um “tempo impuro”; logo, camadas devem
      ser registráveis para evitar homogeneizar tempos[^44][^45].

  - nome: pertencimento_atlas
    tipo: list
    obrigatorio: false
    notas_v220: 'NOVO em 2.2.0.'
    descricao: >
      IDs de pranchas/atlas (montagens) às quais o item pertence. A montagem separa e conecta,
      cria abalo e movimento, e escapa de teleologias, tornando visíveis sobrevivências e
      encontros de temporalidades contraditórias[^46][^47].
    exemplo:
      - atlas_justica_01
      - atlas_contestacao_03
    justificativa_teorica: >
      Como a montagem é método (e capta), o pertencimento a pranchas deve ser rastreável e
      revisável, não naturalizado como ordem “objetiva” do arquivo[^46][^47].

  - nome: posicao_no_atlas
    tipo: object
    obrigatorio: false
    condicional: 'obrigatorio_quando: pertencimento_atlas nao_vazio'
    notas_v220: 'NOVO em 2.2.0.'
    descricao: >
      Posição relacional do item em uma prancha (linha/coluna/papel), permitindo reconstruir e
      debater a constelação produzida pela montagem[^46].
    campos:
      - nome: prancha_id
        tipo: string
        obrigatorio: true
      - nome: linha
        tipo: integer
        obrigatorio: true
        minimo: 1
      - nome: coluna
        tipo: integer
        obrigatorio: true
        minimo: 1
      - nome: papel
        tipo: enum
        obrigatorio: true
        valores:
          - valor: nucleo
            label: Núcleo
            descricao: Imagem central da prancha.
          - valor: borda
            label: Borda
            descricao: Imagem periférica.
          - valor: contraste
            label: Contraste
            descricao: Imagem usada para choque/contraste.
          - valor: costura
            label: Costura
            descricao: Imagem mediadora/ponte.
          - valor: nao_definido
            label: Não definido
            descricao: Papel não especificado.
    exemplo:
      prancha_id: atlas_justica_01
      linha: 2
      coluna: 3
      papel: contraste
    justificativa_teorica: >
      A montagem produz intervalos e intermitências; registrar posição evita que a prancha seja
      tratada como síntese fechada, reintroduzindo teleologia que a montagem pretende desfazer[^46][^47].

  - nome: relacao_dialetica_com_item
    tipo: list
    obrigatorio: false
    notas_v220: 'NOVO em 2.2.0.'
    descricao: >
      Relações dialéticas entre itens (sobrevivência, contestação, montagem anacrônica), alinhadas
      à ideia de procedimento por fragmentos heterogêneos para obter imagem não-sintética do passado[^48].
    estrutura_itens:
      - campo: item_id_outro
        tipo: string
        descricao: Identificador do outro item (LPAI-####).
      - campo: tipo_relacao
        tipo: enum
        valores:
          - valor: sobrevivencia
            label: Sobrevivência
            descricao: Retorno/Nachleben entre itens.
          - valor: pathosformel_repetido
            label: Pathosformel repetido
            descricao: Reiteração de gesto/forma expressiva (mesmo que não nomeada nas fontes).[^34]
          - valor: contestacao_de
            label: Contestação de
            descricao: Item B contesta o item A.
          - valor: contramonumento_a
            label: Contramonumento a
            descricao: Item B opera como contramonumento em relação a A.
          - valor: reapropriacao
            label: Reapropriação
            descricao: Reuso com deslocamento de sentido.
          - valor: montagem_anacronica
            label: Montagem anacrônica
            descricao: Relação criada por prancha/atlas.
    exemplo:
      - item_id_outro: LPAI-0123
        tipo_relacao: contestacao_de
    justificativa_teorica: >
      O procedimento que opõe fragmentos heterogêneos permite codificar relações sem reduzir a
      história a sequência causal linear; a relação inter-itens torna a dialética auditável[^48][^49].

  # --- CAMPOS V2.2.0: contestação/contramonumento ---
  - nome: status_contestacao
    tipo: enum
    obrigatorio: false
    descricao: >
      Estado processual de contestação do item; coerente com a tese de que contra-monumentos
      provocam, demandam interação e podem mudar ao longo do tempo, e com o princípio de que
      remoções não devem ser ponto final (afterlife)[^37][^29].
    valores:
      - valor: integro
        label: Íntegro
        descricao: Sem contestação documentada.
      - valor: contestado_discursivamente
        label: Contestado discursivamente
        descricao: Contestação por debate público/documental, sem intervenção material.
      - valor: defaced
        label: Desfigurado
        descricao: Intervenção material (pichação/pintura/dano), sem remoção.
      - valor: parcialmente_removido
        label: Parcialmente removido
        descricao: Remoção parcial/segmentos.
      - valor: removido
        label: Removido
        descricao: Remoção total do espaço original.
      - valor: contramonumentalizado
        label: Contramonumentalizado
        descricao: Reconfigurado como contramonumento/anti-monumento.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Item fora de espaço público/fora do regime de contestação.
    exemplo: integro
    regra_obrigatoriedade: >
      Obrigatório quando funcao_juridica em [monumento_publico, monumento_contestado] OU suporte == monumento.

  - nome: tipo_intervencao
    tipo: enum
    obrigatorio: false
    condicional: 'obrigatorio_quando: status_contestacao != integro AND status_contestacao != nao_aplicavel'
    descricao: >
      Modalidade da intervenção, distinguindo repertórios de contestação além de derrubada física,
      incluindo pintar, grafitar, reconfigurar, restage e reimaginar em múltiplas maneiras[^28].
    valores:
      - valor: pichacao
        label: Pichação
        descricao: Inscrição/pichação.
      - valor: desfiguramento_fisico
        label: Desfiguramento físico
        descricao: Danos materiais (quebra, incêndio, etc.).
      - valor: remocao_oficial
        label: Remoção oficial
        descricao: Remoção por ato institucional.
      - valor: derrubada
        label: Derrubada
        descricao: Derrubada/toppling.
      - valor: recontextualizacao_curatorial
        label: Recontextualização curatorial
        descricao: Musealização/recontextualização.
      - valor: contramonumento_novo
        label: Contramonumento novo
        descricao: Novo artefato/instalação que contrasta o anterior.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Sem intervenção.
    exemplo: pichacao

  - nome: data_evento_contestacao
    tipo: string
    obrigatorio: false
    condicional: 'obrigatorio_quando: tipo_intervencao != nao_aplicavel'
    formato: iso8601_parcial
    descricao: >
      Data aproximada da intervenção (YYYY ou YYYY-MM ou YYYY-MM-DD), para registrar mudança no
      tempo (change over time) e evitar estabilizar a forma como se fosse invariável[^37].
    exemplo: '2021-07-24'

  - nome: ator_coletivo_contestacao
    tipo: object
    obrigatorio: false
    condicional: 'obrigatorio_quando: tipo_intervencao != nao_aplicavel'
    descricao: >
      Autoria coletiva e categoria do ator, alinhando-se à centralidade de ativismo de base e
      coletivos na contestação de monumentos e na produção de contra-arquivos[^50][^29].
    campos:
      - nome: nome_livre
        tipo: string
        obrigatorio: true
        descricao: Nome do coletivo/ator conforme a fonte.
      - nome: categoria
        tipo: enum
        obrigatorio: true
        valores:
          - valor: movimento_feminista
            label: Movimento feminista
            descricao: Coletivos e ações feministas (p.ex., Antimonumenta).[^51]
          - valor: movimento_indigena
            label: Movimento indígena
            descricao: Movimentos/organizações indígenas.
          - valor: movimento_negro
            label: Movimento negro
            descricao: Movimentos negros/antirracistas.
          - valor: movimento_lgbtqia
            label: Movimento LGBTQIA+
            descricao: Movimentos LGBTQIA+.
          - valor: sindicato
            label: Sindicato
            descricao: Organizações sindicais.
          - valor: poder_publico
            label: Poder público
            descricao: Estado/órgãos oficiais.
          - valor: outro
            label: Outro
            descricao: Outro; detalhar.
          - valor: desconhecido
            label: Desconhecido
            descricao: Sem informação.
    exemplo:
      nome_livre: '(preencher)'
      categoria: outro

  - nome: evidencia_visual_intervencao
    tipo: list
    obrigatorio: false
    condicional: 'obrigatorio_quando: tipo_intervencao != nao_aplicavel'
    descricao: >
      URLs ou referências arquivísticas para imagens antes/depois e fontes jornalísticas/relatos,
      porque a remoção/contestação não deve ser endpoint e exige afterlife documental/counterarchive[^29].
    exemplo:
      - '(URL imagem antes)'
      - '(URL imagem depois)'
      - '(fonte jornalística primária)'

  - nome: tipo_contramonumento
    tipo: enum
    obrigatorio: false
    condicional: 'obrigatorio_quando: status_contestacao == contramonumentalizado'
    descricao: >
      Diferencia contramonumento oficial/encomendado de formas insurgentes e de institucionalizações
      posteriores, evitando homogeneizar regimes de autoria e institucionalidade; dialoga com
      estratégias de disappearance/erasure e recusa de closure/permanência[^39][^38].
    valores:
      - valor: oficial_encomendado
        label: Oficial encomendado
        descricao: Projeto oficial/estatal.
      - valor: insurgente_nao_oficial
        label: Insurgente não oficial
        descricao: Intervenção de base não encomendada.
      - valor: institucionalizado_a_posteriori
        label: Institucionalizado a posteriori
        descricao: Intervenção insurgente posteriormente institucionalizada.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Não é contramonumento.
    exemplo: insurgente_nao_oficial

  # --- NOVOS CAMPOS V2.3.0: gramática masculina ---
  - nome: funcao_da_figura_masculina
    tipo: enum
    obrigatorio: false
    condicional: 'obrigatorio_quando: genero_atribuido == masculino'
    notas_v230: 'NOVO em 2.3.0.'
    valores:
      - valor: forca_sustentadora
        label: Força sustentadora
        descricao: Suporte/carga (atlantes/telamones; Atlas com globo).[^4][^21]
      - valor: soberania_territorial
        label: Soberania territorial
        descricao: Territorialização por rios/limites e metonímias geográficas.[^12]
      - valor: soberania_maritima
        label: Soberania marítima
        descricao: Domínio do mar (Oceanus/Netuno) e maritimidade como regime simbólico.[^17]
      - valor: mediacao_pedagogica
        label: Mediação pedagógica
        descricao: Dispositivo de conhecimento/decisão (bivio) e/ou gesto indicativo mediador.[^6][^24]
      - valor: protetorado_nacional
        label: Protetorado nacional
        descricao: Figura protetiva (guerreiro/protetor; união nacional) em programas brasileiros.[^12]
      - valor: heroismo_civil
        label: Heroísmo civil
        descricao: Heroísmo/autoridade civil (não necessariamente militar); exigir notes.
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Não aplicável.
    descricao: >
      Função/operatividade da figura masculina no programa iconográfico, para não reduzir o
      masculino a um rótulo de gênero: inclui decisão moral (bivio), sustentação (atlantes/Atlas),
      soberania territorial por rios e soberania marítima por personificações do mar[^6][^4][^12][^21][^17].
    exemplo: mediacao_pedagogica

  - nome: tipo_agencia_masculina
    tipo: enum
    obrigatorio: false
    notas_v230: 'NOVO em 2.3.0.'
    valores:
      - valor: protetorado
        label: Protetorado
        descricao: Agir como protetor/guardião (guerreiro/protetor).[^12]
      - valor: soberania
        label: Soberania
        descricao: Agir como soberano (poder, império, governo visual).
      - valor: mediacao_territorial
        label: Mediação territorial
        descricao: Mediar/organizar território (rios, limites, nomeação).[^12]
      - valor: sustentacao_arquitetonica
        label: Sustentação arquitetônica
        descricao: Suporte/carga em arquitetura (atlantes/telamones).[^4]
      - valor: pedagogia_moral
        label: Pedagogia moral
        descricao: Pedagogia da escolha/virtude vs vício (bivio).[^6]
      - valor: nao_aplicavel
        label: Não aplicável
        descricao: Não aplicável.
    descricao: >
      Modalidade de agência masculina, especialmente útil para casos brasileiros em que a fonte
      descreve explicitamente o masculino como ativo (guerreiro/protetor) e como instrumento de poder/união[^12].
    exemplo: protetorado

  - nome: funcao_atlanteana
    tipo: bool
    obrigatorio: false
    notas_v230: 'NOVO em 2.3.0.'
    condicional: 'obrigatorio_quando: subtipo in [atlante, telamon]'
    descricao: >
      Verdadeiro quando a figura masculina cumpre função explícita de suporte/sustentação (arquitetônica
      ou simbólica), como colunas antropomórficas e Atlas como suporte do globo[^4][^21].
    exemplo: true

  - nome: tipo_efluencia_hidrica
    tipo: enum
    obrigatorio: false
    notas_v230: 'NOVO em 2.3.0.'
    condicional: 'obrigatorio_quando: subtipo == rio_barbado'
    valores:
      - valor: urna_vertedora
        label: Urna vertedora
        descricao: Efluência por urna/vasilha vertente.[^3]
      - valor: vaso_inclinado
        label: Vaso inclinado
        descricao: Efluência por vaso inclinado.
      - valor: sem_efluencia
        label: Sem efluência
        descricao: Corpo hídrico sem sinal de efluência.
      - valor: outra
        label: Outra
        descricao: Outra; detalhar.
    descricao: >
      Tipo de efluência hídrica em personificações aquáticas masculinas; operacionaliza a regra
      de que barba isolada não basta para inferir rio, exigindo efluência/vaso como traço discriminante[^3][^5].
    exemplo: urna_vertedora

  - nome: substituicao_atributiva_hercules
    tipo: object
    obrigatorio: false
    notas_v230: 'NOVO em 2.3.0.'
    condicional: 'obrigatorio_quando: subtipo == hercules AND objetos_regalia nao_contem clava'
    descricao: >
      Registra identificação hercúlea por substituição atributiva (p.ex., cetro/vara manejado "como
      Hercules a sua clava"), tornando auditável a ponte inferencial quando o atributo canônico não
      está visível no suporte[^12].
    campos:
      - nome: atributo_canonico_substituido
        tipo: string
        obrigatorio: true
        exemplo: clava
      - nome: atributo_novo
        tipo: string
        obrigatorio: true
        exemplo: cetro_ou_vara
      - nome: justificativa
        tipo: string
        obrigatorio: true
        max_chars: 300
        exemplo: Paratexto descreve manejo do cetro como clava.

indicadores_purificacao:
  descricao_geral: >
    Conjunto de 10 indicadores ordinais (0-4) herdados do documento-pai. Os nomes abaixo incluem
    os cinco explicitamente mencionados no material disponível e cinco placeholders plausíveis,
    marcados com nota_lacuna quando o nome/definição exata não está na base de evidência deste
    piloto[^9].
  escala:
    minimo: 0
    maximo: 4
    interpretacao: '0 = mínimo/ausente; 4 = máximo'
  campos_por_indicador:
    - nome: desincorporacao
      escala: 0-4
      descricao: >
        Mede perda/retirada do corpo (especialmente corpo feminino) na passagem para signos mais
        abstratos/heráldicos.
      subaltern_caution_obrigatorio: true
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel_com_cautela
        outra: aplicavel_com_cautela
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel_com_cautela
        item_com_nachleben_marker: aplicavel_com_cautela
      aplicabilidade_por_familia_masculina:
        hercules: inverter_polaridade
        atlante_telamon: inverter_polaridade
        rio_barbado: aplicavel_com_subaltern_caution
        netuno: aplicavel_com_subaltern_caution
        genio_protetor: aplicavel_com_subaltern_caution
      nota_v230: >
        Em gramáticas masculinas, pode haver ênfase de corporeidade (Hércules nu com clava; Atlas/atlantes
        como suporte), o que pode inverter a polaridade intuitiva do indicador; exigir cautela e notes[^6][^4][^21].

    - nome: heraldizacao
      escala: 0-4
      descricao: Mede conversão em emblema/heráldica/selo.
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel_com_cautela
      aplicabilidade_por_familia_masculina:
        hercules: aplicavel_com_subaltern_caution
        atlante_telamon: aplicavel
        rio_barbado: aplicavel
        netuno: aplicavel
        genio_protetor: aplicavel
      nota_v230: >
        Nota: base de evidência ainda é parcial para mensurar heraldização em itens masculinos no corpus
        brasileiro; aplicar com cautela e registrar fontes. Lacuna na base de evidência (busca neste piloto)[^12].

    - nome: enquadramento_arquitetonico
      escala: 0-4
      descricao: Mede enquadramento por arquitetura (tribunais, igrejas, monumentos).
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: aplicavel
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel
      aplicabilidade_por_familia_masculina:
        hercules: aplicavel
        atlante_telamon: aplicavel
        rio_barbado: aplicavel
        netuno: aplicavel
        genio_protetor: aplicavel
      nota_v230: >
        Atlantes/telamones são, por definição, operadores arquitetônicos de sustentação, tornando o
        enquadramento arquitetônico central para sua leitura[^4].

    - nome: serialidade
      escala: 0-4
      descricao: Mede repetição seriada (moedas, selos, cédulas, impressos).
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: aplicavel_com_cautela
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel
      aplicabilidade_por_familia_masculina:
        hercules: aplicavel_com_subaltern_caution
        atlante_telamon: aplicavel
        rio_barbado: aplicavel
        netuno: aplicavel
        genio_protetor: aplicavel

    - nome: inscricao_estatal
      escala: 0-4
      descricao: Mede intensidade de inscrição estatal/autoridade institucional.
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel_com_cautela
      aplicabilidade_por_familia_masculina:
        hercules: aplicavel
        atlante_telamon: aplicavel
        rio_barbado: aplicavel
        netuno: aplicavel
        genio_protetor: aplicavel
      nota_v230: >
        A leitura do Gênio do Brasil como instrumento de poder e união nacional sugere alta inscrição
        estatal/imperial em certos programas, mas a validação empírica no corpus core permanece lacuna[^12].

    - nome: classicizacao
      escala: 0-4
      descricao: '[LACUNA] Grau de idealização classicizante (corpo/pose/vestes).'
      nota_lacuna: true
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: aplicavel_com_cautela
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel_com_cautela

    - nome: moralizacao
      escala: 0-4
      descricao: '[LACUNA] Intensidade de pedagogia moral explícita na cena/dispositivo.'
      nota_lacuna: true
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel_com_cautela
        nacional: aplicavel
        afro_brasileira: aplicavel
        masculino_juridico: aplicavel_com_cautela
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel_com_cautela
      nota_v230: >
        O bivio ercúleo é explicitamente formulado como problema de conhecimento e distinção entre
        falso/verdadeiro e virtude/vício, sugerindo moralização em cenas hercúleas[^6].

    - nome: depuracao_semantica
      escala: 0-4
      descricao: '[LACUNA] Redução de polissemia por fixação institucional de sentido.'
      nota_lacuna: true
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel_com_cautela
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel_com_cautela
        item_com_nachleben_marker: aplicavel_com_cautela

    - nome: neutralizacao_afetiva
      escala: 0-4
      descricao: '[LACUNA] Deslocamento de emoção/corporeidade para representação impessoal.'
      nota_lacuna: true
      subaltern_caution_obrigatorio: true
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel_com_cautela
        masculino_juridico: aplicavel_com_cautela
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel_com_cautela
        item_com_nachleben_marker: aplicavel_com_cautela

    - nome: monumentalizacao
      escala: 0-4
      descricao: '[LACUNA] Fixação em monumento/arquitetura como tecnologia de autoridade pública.'
      nota_lacuna: true
      subaltern_caution_obrigatorio: false
      aplicabilidade_por_familia:
        virtudes: aplicavel
        continentes: aplicavel
        oceanos_rios: aplicavel
        nacional: aplicavel
        afro_brasileira: aplicavel
        masculino_juridico: aplicavel
        outra: aplicavel
      aplicabilidade_contextual:
        item_contestado: inverter_polaridade
        item_em_atlas: aplicavel
        item_com_nachleben_marker: aplicavel_com_cautela
      nota_v230: >
        Rios colossais (Amazonas/Prata) aparecem como delimitação simbólica do Império brasileiro,
        sugerindo monumentalização territorial por hidrografia personificada; generalização exige cautela[^12].

protocolo_intercodificador:
  amostra_dupla_codificacao: 0.20
  metrica: krippendorff_alpha_por_campo
  limiar_aceitavel: 0.70
  limiar_alerta: 0.60
  campos_priorizados_para_teste:
    - familia_alegorica
    - subtipo
    - genero_atribuido
    - justificativa_genero
    - hipotese_racial
    - vetor_colonial
    - finalidade_atribuida
    - relacao_com_repertorio_indigena
    - confianca_codificacao
    - status_contestacao
    - tipo_intervencao
    - ator_coletivo_contestacao
    - nachleben_marker
    - funcao_da_figura_masculina
    - funcao_atlanteana
    - tipo_efluencia_hidrica
    - substituicao_atributiva_hercules
  adjudicacao_desacordo: >
    1) discussão entre codificadores/as com referência à fonte_imagem/edicao_suporte;
    2) se persistir, decisão de codificador/a sênior;
    3) registrar em adjudicacao_log e, se necessário, propor ajuste de enum/descrição.
  campo_log: adjudicacao_log
  nota_v230: >
    Em v2.3.0, os campos novos da gramática masculina são prioritários por alta carga interpretativa
    e por envolverem distinções finas (p.ex., barba como autoridade genérica vs. barba como índice
    aquático; Hércules com clava vs. por substituição atributiva).[^5][^3][^12].

protocolo_freeze:
  estados:
    - estado: pre_freeze
      descricao: 'Estado atual; pre_freeze_sample=true; mudanças de schema permitidas.'
    - estado: freeze_candidate
      descricao: >
        Mínimo de 50 itens; Krippendorff alpha >= 0.70 nos campos priorizados; PR submetido
        para revisão.
    - estado: freeze
      descricao: 'Schema travado; hash calculado sobre este YAML; hash armazenado em freeze_hash.'
    - estado: unfreeze
      descricao: >
        Apenas por erro crítico; requer reanotação completa dos itens afetados e registro de
        justificativa.
  freeze_hash: null
  nota_v230: >
    Gatilho para v3.0.0: se a inclusão de masculinidades afro-brasileiras (p.ex., Exu, Ogum) ou
    indígenas exigir família alegórica autônoma (não subordinada a masculino_juridico) ou reestrutura
    de unidade analítica, será necessário MAJOR upgrade; lacuna na base de evidência (busca neste piloto)[^7].

protocolo_contestacao:
  notas_v220: >
    Protocolo (v2.2.0) para modelar contestação/afterlife como processo (não estado final), coerente
    com a tese de que remoção não deve ser endpoint e requer afterlife/counterarchive[^29].
  modelagem:
    opcao_A_item_unico:
      descricao: 'Registrar o monumento e sua contestação no mesmo item, via status_contestacao + tipo_intervencao.'
      usar_quando:
        - a intervenção é pontual e não há autoria coletiva relevante documentada
    opcao_B_itens_duplos_relacionados:
      descricao: 'Criar um item para o monumento e outro para a intervenção/contramonumento, ligados por relacao_dialetica_com_item.tipo_relacao.'
      recomendar_quando:
        - a intervenção é produzida por coletivo identificado e possui afterlife discursiva própria
  evidencia_minima:
    exigir_quando_status_contestacao_ativo:
      - evidencia_visual_intervencao
      - data_evento_contestacao
      - ator_coletivo_contestacao
    justificativa: remoção/contestação não é ponto final; requer afterlife documental
  subaltern_caution:
    regra: >
      Se ator_coletivo_contestacao.categoria em [movimento_indigena, movimento_negro, movimento_feminista],
      exigir nota subaltern_caution explicando como a fonte nomeia o gesto (p.ex., pintura como transformação
      do corpo).[^52]
  coder_position_statement:
    regra: >
      Quando status_contestacao != integro e != nao_aplicavel, o coder_position_statement deve explicitar
      (i) como a fonte nomeia o gesto e (ii) qual critério foi usado no codebook para escolher a categoria
      (defaced, pichacao etc.).[^52][^28]

protocolo_atlas:
  notas_v220: >
    Protocolo (v2.2.0) para tratar prancha/atlas como montagem (capta), e não como índice neutro;
    a montagem separa e conecta e escapa de teleologias, tornando visíveis sobrevivências/anacronismos[^46][^47].
  id_prancha:
    padrao: atlas_<topico>_<nn>
    exemplo: atlas_justica_01
  papel_no_atlas:
    valores:
      - nucleo
      - borda
      - contraste
      - costura
      - nao_definido
  auditabilidade:
    regra: >
      Toda prancha/atlas deve ter metadados próprios (capta_declaration, coder_id, coded_at) e um
      campo de autoria/curadoria (quem montou). A montagem é capta: deve ser declarada e passível
      de revisão, não naturalizada como verdade do arquivo[^46][^1].

protocolo_reconhecimento_masculino:
  notas_v230: 'NOVO em 2.3.0.'
  regra_barba:
    descricao: >
      A barba pode operar como significante hegemônico de autoridade masculina e não é, por si só,
      prova de personificação aquática. Para inferir rio/mar barbado, exigir coocorrências de postura
      e efluência hídrica (urna/vaso vertente).[^5][^3]
    criterio_rio_barbado: >
      Codificar rio_barbado apenas quando houver coocorrência de (a) marcas_corporais contendo barba_longa
      OU barba e (b) marcas_corporais contendo corpo_semirrecosto_fluvial OU corpo_reclinado e (c)
      tipo_efluencia_hidrica != sem_efluencia.
  regra_substituicao_atributiva_hercules:
    descricao: >
      Permitir subtipo hercules quando há evidência contextual/paratextual de transposição do atributo
      (cetro/vara) para a função hercúlea (manejo "como Hercules a sua clava"), mesmo sem clava literal,
      desde que substituicao_atributiva_hercules esteja preenchido[^12].
  regra_justificativa_genero_masculino:
    descricao: >
      Quando genero_atribuido == masculino, justificativa_genero deve ser substantiva (>=80 chars) e
      ancorada em marcas observáveis (barba_longa; postura_de_sustentacao; corpo_semirrecosto_fluvial;
      gesto_indicativo_pedagogico; nudez_total; clava).[^5][^4][^3][^6]
  subaltern_caution:
    descricao: >
      Quando a figura masculina remete a masculinidades afro-brasileiras ou indígenas que não se encaixam
      na gramática clássica (Hércules/Atlas/river-god), aplicar subaltern_caution e registrar em notes.
      Nota: lacuna na base de evidência (busca neste piloto)[^7].

exemplos_registro:
  - item_id: LPAI-0001
    titulo: Efígie da República (moeda)
    suporte: moeda
    data_suporte: '1889'
    instituicao_origem: Casa da Moeda (Brasil)
    localizacao_atual: '(a preencher)'
    fonte_imagem: https://eidolonstation.com/eidolon_posts/efigie-da-republica-brazil/
    edicao_suporte: '(a preencher)'
    tipo_reproducao: digital
    capta_declaration: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
    coder_id: '(a preencher)'
    coded_at: '(a preencher)'
    codebook_version: '2.3.0'
    pre_freeze_sample: true
    coder_position_statement: '(a preencher)'
    confianca_codificacao: alta
    familia_alegorica: nacional
    subtipo: republica
    objetos_regalia:
      - coroa
    marcas_corporais:
      - vestes_romanas
    marcadores_cena_arquitetura: []
    genero_atribuido: feminino
    justificativa_genero: Mulher jovem com coroa de louros em estilo romano.
    funcao_juridica: moeda_cedula
    vetor_colonial: republicano_brasileiro
    hipotese_racial: >
      Efígie europeizada (romana) como personificação nacional; opera como legitimação visual
      por repertório transnacional.
    referencia_genealogica:
      - warner_1985
      - ripa_1593_1603
    dado_negativo: false
    power_at_stake: Legitimação/branding do regime republicano por ícone feminino representacional.
    finalidade_atribuida: branding_estatal
    relacao_com_repertorio_indigena: nao_aplicavel
    status_evidencia: piloto
    nachleben_marker: false
    camadas_temporais: []
    pertencimento_atlas: []
    status_contestacao: nao_aplicavel
    notes: Efígie descrita como jovem mulher com coroa de louros em estilo romano.
    indicadores_purificacao_scores:
      desincorporacao: 1
      heraldizacao: 2
      enquadramento_arquitetonico: 0
      serialidade: 4
      inscricao_estatal: 4
      classicizacao: 4
      moralizacao: 1
      depuracao_semantica: 3
      neutralizacao_afetiva: 2
      monumentalizacao: 0

  - item_id: LPAI-0002
    titulo: Iustitia em tribunal contemporâneo (camadas temporais)
    suporte: arquitetura
    data_suporte: '(a preencher)'
    instituicao_origem: '(a preencher)'
    localizacao_atual: '(a preencher)'
    fonte_imagem: '(a preencher)'
    edicao_suporte: '(a preencher)'
    tipo_reproducao: digital
    capta_declaration: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
    coder_id: '(a preencher)'
    coded_at: '(a preencher)'
    codebook_version: '2.3.0'
    pre_freeze_sample: true
    coder_position_statement: '(a preencher)'
    confianca_codificacao: media
    motivo_incerteza: '(a preencher: se necessário)'
    familia_alegorica: virtudes
    subtipo: iustitia
    objetos_regalia:
      - balanca
      - espada
    marcas_corporais:
      - vestes_romanas
    marcadores_cena_arquitetura: []
    genero_atribuido: feminino
    justificativa_genero: Figura feminina com vestes romanas; atributos de balança e espada.
    funcao_juridica: arquitetura_forense
    vetor_colonial: republicano_brasileiro
    hipotese_racial: '(a preencher)'
    referencia_genealogica:
      - resnik_curtis_2011
      - ripa_1593_1603
      - didi_huberman_devant_le_temps
    dado_negativo: false
    power_at_stake: '(a preencher)'
    finalidade_atribuida: legitimacao_juridica
    relacao_com_repertorio_indigena: nao_aplicavel
    status_evidencia: piloto
    nachleben_marker: true
    camadas_temporais:
      - data_aprox: antiguidade (modelo)
        descricao: Camada clássica/romana como gramática formal
        fonte_iconografica: '(preencher)'
      - data_aprox: c. 1600
        descricao: Camada prescritiva (Ripa)
        fonte_iconografica: ripa_1593_1603
      - data_aprox: '(a preencher)'
        descricao: Camada contemporânea no sítio judicial (seen/sited)
        fonte_iconografica: '(preencher: fonte_imagem/arquivo)'
    pertencimento_atlas:
      - atlas_justica_01
    posicao_no_atlas:
      prancha_id: atlas_justica_01
      linha: 1
      coluna: 1
      papel: nucleo
    relacao_dialetica_com_item:
      - item_id_outro: LPAI-0001
        tipo_relacao: sobrevivencia
    status_contestacao: nao_aplicavel
    notes: Registrar Nachleben como hipótese; detalhar evidência de transmissão em notes.
    indicadores_purificacao_scores:
      desincorporacao: 0
      heraldizacao: 0
      enquadramento_arquitetonico: 4
      serialidade: 0
      inscricao_estatal: 4
      classicizacao: 4
      moralizacao: 2
      depuracao_semantica: 2
      neutralizacao_afetiva: 2
      monumentalizacao: 3

  - item_id: LPAI-0003
    titulo: Estátua de Borba Gato (monumento contestado)
    suporte: monumento
    data_suporte: '(a preencher)'
    instituicao_origem: '(a preencher)'
    localizacao_atual: São Paulo (a preencher)
    fonte_imagem: '(a preencher)'
    edicao_suporte: '(a preencher)'
    tipo_reproducao: digital
    capta_declaration: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
    coder_id: '(a preencher)'
    coded_at: '(a preencher)'
    codebook_version: '2.3.0'
    pre_freeze_sample: true
    coder_position_statement: '(a preencher; mínimo 100 chars por status_contestacao ativo)'
    confianca_codificacao: media
    familia_alegorica: outra
    subtipo: outra
    objetos_regalia: []
    marcas_corporais: []
    marcadores_cena_arquitetura: []
    genero_atribuido: ausente
    funcao_juridica: monumento_contestado
    vetor_colonial: nao_aplicavel
    hipotese_racial: >
      Monumento associado a bandeirante; fonte jornalística indica captura e escravização de indígenas e negros,
      sugerindo disputa racial/colonial no presente.
    referencia_genealogica:
      - young_counter_monument
    dado_negativo: false
    power_at_stake: '(a preencher)'
    finalidade_atribuida: comemoracao
    relacao_com_repertorio_indigena: nao_aplicavel
    status_evidencia: piloto
    nachleben_marker: false
    camadas_temporais: []
    pertencimento_atlas:
      - atlas_contestacao_01
    posicao_no_atlas:
      prancha_id: atlas_contestacao_01
      linha: 1
      coluna: 1
      papel: nucleo
    status_contestacao: defaced
    tipo_intervencao: desfiguramento_fisico
    data_evento_contestacao: '2021-07-24'
    ator_coletivo_contestacao:
      nome_livre: Revolucao Periferica
      categoria: outro
    evidencia_visual_intervencao:
      - url1
      - url2
      - https://g1.globo.com/sp/noticia/2021/07/24/estatua-de-borba-gato-e-incendiada-por-grupo-em-sao-paulo.ghtml
    tipo_contramonumento: nao_aplicavel
    subaltern_caution: true
    notes: >
      Fonte jornalística: bandeirantes como Borba Gato capturaram e escravizaram indígenas e negros.
    indicadores_purificacao_scores:
      desincorporacao: 0
      heraldizacao: 0
      enquadramento_arquitetonico: 4
      serialidade: 0
      inscricao_estatal: 3
      classicizacao: 2
      moralizacao: 0
      depuracao_semantica: 0
      neutralizacao_afetiva: 0
      monumentalizacao: 4

  - item_id: LPAI-0004
    titulo: Gênio do Brasil (programa imperial com referência hercúlea)
    suporte: frontispicio
    data_suporte: '(a preencher)'
    instituicao_origem: '(a preencher)'
    localizacao_atual: '(a preencher)'
    fonte_imagem: http://www.dezenovevinte.net/obras/obras_amc.htm
    edicao_suporte: '(a preencher)'
    tipo_reproducao: digital
    capta_declaration: 'LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.'
    coder_id: '(a preencher)'
    coded_at: '(a preencher)'
    codebook_version: '2.3.0'
    pre_freeze_sample: true
    coder_position_statement: >
      (a preencher; explicitar que a identificação hercúlea depende de substituição atributiva e de
      descrição paratextual; registrar poder/beneficiários).
    confianca_codificacao: media
    familia_alegorica: masculino_juridico
    subtipo: genio_protetor
    objetos_regalia:
      - cetro
      - coroa
    marcas_corporais:
      - corpo_ereto
    marcadores_cena_arquitetura: []
    genero_atribuido: masculino
    justificativa_genero: >
      Fonte descreve explicitamente o Gênio como "masculino e ativo"; figura com postura majestática e
      cetro/vara como elemento de poder, em contraste com representações femininas passivas[^12].
    funcao_da_figura_masculina: protetorado_nacional
    tipo_agencia_masculina: protetorado
    substituicao_atributiva_hercules:
      atributo_canonico_substituido: clava
      atributo_novo: cetro_ou_vara
      justificativa: 'Texto descreve que o cetro se converterá em vara e será manejado como Hercules a sua clava.'
    funcao_juridica: frontispicio_normativo
    vetor_colonial: luso_brasileiro
    hipotese_racial: '(a preencher)'
    referencia_genealogica:
      - brazilian_republican_iconography
      - panofsky_hercules_am_scheidewege
    dado_negativo: false
    power_at_stake: >
      Imagem imperial para difundir união nacional e poder em torno da monarquia (beneficiários: elites imperiais).[^12]
    finalidade_atribuida: legitimacao_juridica
    relacao_com_repertorio_indigena: nao_aplicavel
    status_evidencia: piloto
    nachleben_marker: true
    camadas_temporais:
      - data_aprox: antiguidade (modelo)
        descricao: Gramática hercúlea de força e decisão
        fonte_iconografica: '(preencher)'
      - data_aprox: séc. XIX
        descricao: Recontextualização luso-brasileira (cetro/vara como clava)
        fonte_iconografica: http://www.dezenovevinte.net/obras/obras_amc.htm
    pertencimento_atlas:
      - atlas_masculino_01
    posicao_no_atlas:
      prancha_id: atlas_masculino_01
      linha: 1
      coluna: 1
      papel: nucleo
    status_contestacao: nao_aplicavel
    notes: >
      Registrar que o texto descreve o cetro convertido em vara e manejado como clava; e que o Gênio do
      Brasil é caracterizado como instrumento de poder e união nacional em torno da monarquia[^12].
    indicadores_purificacao_scores:
      desincorporacao: 0
      heraldizacao: 2
      enquadramento_arquitetonico: 2
      serialidade: 1
      inscricao_estatal: 4
      classicizacao: 3
      moralizacao: 3
      depuracao_semantica: 2
      neutralizacao_afetiva: 1
      monumentalizacao: 2

# Glossário de referências (verbete 80-150 palavras cada; texto em português; chaves em snake_case)
glossario_referencias:
  ripa_1593_1603: >
    A Iconologia de Cesare Ripa opera como um handbook/dicionário alegórico influente: em vez de
    descrever “retratos existentes”, Ripa personifica conceitos e inventa imagens a partir de
    termos universais, oferecendo descrições que podem ser usadas por poetas, pintores e
    escultores para representar virtudes, vícios e paixões[^13][^14][^40]. A estrutura
    de “dicionário” e a presença de índices de elementos (objetos, animais etc.) sustentam uma
    lógica de decomposição em atributos controláveis, útil para codebooks contemporâneos[^13].
    O verbete exige cuidado com variações materiais entre edições (nem todas as alegorias
    são ilustradas), afetando inferências de atributos e gênero[^10][^11].

  ortelius_1570: >
    No frontispício de Theatrum Orbis Terrarum (Ortelius), as figuras dos quatro continentes
    funcionam como stand-ins alegóricos: representam lugar e traços identificadores por
    meio de accoutrements, e não como “evidência documental” de povos diversos[^22].
    A composição estabelece Europa como referência dentro do quarteto feminino, estruturando
    uma alegoria de ordem mundial em que a soberania europeia é visualmente central[^15].

  collaert_four_continents: >
    Quatro Continentes designa um repertório seriável e circulável em múltiplos suportes
    (gravuras, metal, têxteis etc.), o que justifica reuso de esquemas continentais em artefatos
    estatais e impressos[^32]. Europa tende a aparecer entronizada/regal,
    enquanto América pode ser figurada por signos de ameaça e subordinação (p.ex., canibalismo),
    criando gramática para codificar hierarquias e violência colonial[^15].

  carriera_four_continents: >
    Séries de Quatro Continentes consolidam um léxico visual que codifica continentes como corpos
    femininos e como partes de uma ordem mundial hierarquizada; a circulação em diferentes mídias
    ajuda a explicar reuso em contextos estatais fora da Europa[^32].

  warner_1985: >
    Marina Warner é mobilizável como crítica à alegoria feminina: suas histórias exploram formas
    de agência com desejos irreconciliáveis e definições móveis, isto é, a figura feminina não deve
    ser lida como marcador direto de empoderamento[^26]. Warner discute ansiedades
    sociais e o undertow de racismo em mitos de “selvagens” e canibais, sugerindo que alegorias
    podem naturalizar hierarquias sociais[^27].

  resnik_curtis_2011: >
    Resnik e Curtis colocam a arte no centro ao focar renderizações visuais do direito para analisar
    a prática de justiça ao longo do tempo[^30]. A iconografia de Justiça (figura
    feminina com balança e espada, às vezes venda) sinaliza aspirações de imparcialidade e também
    reivindica poder, gerando controvérsias sobre forma física e venda[^25][^30].
    O vínculo entre imagem e espaço institucional (seen e sited) reforça registrar função jurídica
    e contexto arquitetônico, pois a mesma iconografia pode não significar justiça para todos[^31][^30].

  souza_2014: >
    A bibliografia sobre América alegorizada destaca a convenção: América como mulher reclinada e nua,
    com cocar, arco e flechas, acentuando erotização e características contraditórias do “novo mundo”[^16].
    Esse repertório se articula à terra feminilizada disponível à possessão e à substituição simbólica
    do corpo feminino pelo projeto nacional masculino, oferecendo eixo para codificar colonialidade[^16].

  ihering_der_zweck: >
    Ihering formula teleologia (“Keine Handlung ohne Zweck”) e concebe o direito como meio para um fim
    social (existência da sociedade), articulando política de força e mediação entre interesses[^53][^41][^42].
    A luta pelo direito afirma que paz é o fim e luta é o meio; a vida do direito é luta de povos,
    Estado, classes e indivíduos, o que ajuda a interpretar disputas simbólicas como parte do conflito
    por direitos[^54].

  warburg_mnemosyne: >
    Warburg importa por uma teoria de sobrevivência (Nachleben) em que formas não morrem e podem
    reaparecer/renascer com re-semantização[^33]. A operacionalização exige cautela
    porque Pathosformel pode não estar explicitamente nomeada nas fontes primárias, exigindo descrição
    de equivalentes funcionais (gestos, atributos, marcas expressivas)[^34].

  didi_huberman_devant_le_temps: >
    Didi-Huberman sustenta que o anacronismo é uma riqueza interior às imagens e condição de sua história,
    e que obras exigem ferramentas improváveis porque nelas todos os tempos se encontram[^35][^36].
    Para o LPAI, isso implica codificar temporalidade como propriedade analítica (camadas/constelações),
    e não apenas como data do suporte.

  young_counter_monument: >
    Young descreve contra-monumentos como dispositivos que provocam, demandam interação e podem mudar
    no tempo, insistindo que o trabalho da memória recaia sobre o/a espectador/a[^37].
    O conceito envolve estratégias de desaparecimento/apagamento e se conecta ao argumento de que a
    remoção não deve ser ponto final, exigindo afterlife e counterarchive[^39][^29].

  panofsky_hercules_am_scheidewege: >
    Chave proposta (v2.3.0) para rastrear bibliografia canônica sobre o “bivio erculeo” (Hércules na
    encruzilhada) como cena pedagógica de distinção entre virtude/vício e falso/verdadeiro. A necessidade
    desta chave decorre do fato de que o “bivio” é descrito como problema de conhecimento, e não como
    mero motivo ornamental, sugerindo papel epistêmico/pedagógico do masculino em programas de autoridade[^6].
    Nota: lacuna na base de evidência para referência ABNT fechada (busca neste piloto).

  lubbock_atlantes: >
    Placeholder (v2.3.0) para estudos sobre atlantes/telamones como colunas antropomórficas de suporte.
    No schema, atlantes são definidos como colunas antropomórficas cuja função simbólica é sustentar
    o peso da construção, o que justifica campos como funcao_atlanteana e marcadores de postura de sustentação[^4].
    Nota: lacuna na base de evidência para referência ABNT fechada (busca neste piloto).

  brazilian_republican_iconography: >
    Placeholder (v2.3.0) para bibliografia sobre gramáticas masculinas no Brasil (Império/República),
    incluindo o Gênio do Brasil como instrumento de poder e união nacional e a mobilização de rios
    colossais (Amazonas/Prata) como delimitação territorial e nomeação simbólica[^12].
    Nota: lacuna na base de evidência para referência ABNT fechada (busca neste piloto).

changelog:
  - versao: 2.0.0
    data: 2026-06-22
    mudanca: >
      Criação de campos para famílias alegóricas (Virtudes, Continentes, Oceanos/Rios) e campos associados
      (subtipo, atributos, gênero, função jurídica, vetor colonial, hipótese racial, referência genealógica).
    re_pontua_itens_anteriores: false
  - versao: 2.1.0
    data: 2026-06-23
    mudanca: >
      Patch de auditabilidade capta e refinamento do schema: divisão de atributos em três campos; inclusão
      de justificativa_genero, dado_negativo, power_at_stake e finalidade_atribuida; rastreabilidade de
      fonte/edição/tipo de reprodução; inclusão de afro_brasileira como família; protocolos de confiabilidade
      intercodificador e freeze.
    re_pontua_itens_anteriores: false
  - versao: 2.2.0
    data: '(preencher)'
    mudanca: >
      Introduz campos de temporalidade composta (Nachleben/anacronismo), montagem-atlas e contestação/afterlife
      (contramonumento) com validações condicionais e rastreabilidade documental para itens contestados.
    re_pontua_itens_anteriores: false
  - versao: 2.3.0
    data: '(preencher)'
    mudanca: >
      Introduz a família masculino_juridico e campos/regras para operacionalizar gramáticas masculinas (Hércules,
      atlantes/telamones, rios barbados, Netuno/Oceanus e casos brasileiros como o Gênio do Brasil), incluindo
      campos de função/agência e protocolos de reconhecimento (barba vs tipo aquático; substituição atributiva
      hercúlea). Não re-pontua itens anteriores.
    re_pontua_itens_anteriores: false
```

[^1]: Humanities Approaches to Graphical Display.

[^2]: Why Digital Humanists Should Emphasize Situated Data over Capta | 10 |, 2025.

[^3]: Estella, 2002. El llamado Neptuno (Río?) de la Colección del Carpio y su problemática identificación con una obra atribuida a Bernini, en Aranjuez. Archivo Espanol De Arte.

[^4]: orioqueorionaove, 2012. A fachada do IPHAN | O RIO QUE O RIO NÃO VÊ.

[^5]: Bendall, 2022. Female Personifications and Masculine Forms: Gender, Armour and Allegory in the Habsburg–Valois Conflicts of Sixteenth‐Century Europe. Gender & History.

[^6]: Villari, 2015. L'«Ercole al bivio» di Domenico Beccafumi (1486-1551) e l'Ercole giraldiano.

[^7]: Mika, 2021. Book Review: Data Feminism. Journal of eScience Librarianship.

[^8]: Dennis et al., 2010. Essays Images of Justice.

[^9]: Hayaert, 2018. The Paradoxes of Lady Justice’s Blindfold.

[^10]: Emblèmes 1603 : Cesare Ripa, Iconologia... (2e éd.; 1ère éd. illustrée), Rome, L. Facii | Utpictura18.

[^11]: L’Iconologia, 2018.

[^12]: 19&20 - O Gênio do Brasil e as Musas: Um manifesto ideológico numa
nação em construção, por Alberto Martín Chillón.

[^13]: Maffei & Procaccioli, 2012. Cesare Ripa, Iconologia. A cura di Sonia Maffei. Testo stabilito da Paolo Procaccioli.

[^14]: English Translations and Adaptations of Cesare Ripa's Iconologia: From the 17th to the 19th Century Hans-Joachim Zimmermann, De Zeventiende Eeuw. Jaargang 11 - DBNL.

[^15]: Neumann, 2009. Imagining European community on the title page of Ortelius' Theatrum Orbis Terrarum (1570). Word & Image.

[^16]: Detsi-Diamanti, 2006. Politicizing Aesthetics. Anachronist.

[^17]: López, 2017. La personificación del mar: Evolución y transformaciones iconográficas del mundo clásico al medioevo.

[^18]: Nazario, 2026. Quem é a pessoa por trás do rosto nas moedas brasileiras? - Super Rádio Tupi.

[^19]: Efígie da República (Brazil) - Eidolon Station, 2026.

[^20]: Jurt, 2014. Brazil: a Nation-state in the Making. Actes De La Recherche En Sciences Sociales.

[^21]: Schröder, 2014. Images and messages in the embellishment of metropolitan railway stations (1850-1950).

[^22]: Sutton, 2009. Mapping Meaning: Ethnography and Allegory in Netherlandish Cartography, 1570-1655. Itinerario: International Journal on the History of European Expansion and Global Interaction.

[^23]: A Luta Pelo Direito - Rudolf von Ihering.

[^24]: Immagini della Giustizia: antiporte: Titius, Observationum ratiocinantium ... (1).

[^25]: Resnik & Curtis, 2007. Representing Justice: From Renaissance Iconography to Twenty-First Century Courthouses.

[^26]: Propst, 2016. From Vogue to the Virgin Mary: Marina Warner and Constructions of Female Agency in 1970s Feminism. Women's Studies.

[^27]: Warner, 1994. Managing monsters : six myths of our time : the 1994 Reith Lectures.

[^28]: Abraham, 2021. Toppled Monuments and Black Lives Matter: Race, Gender, and Decolonization in the Public Space. An Interview with Charmaine A. Nelson. Atlantis.

[^29]: Coomasaru et al., 2023. Monuments Must Fall. British Art Studies.

[^30]: Lee, 2012. Book Review: Justice For All?.

[^31]: Tait, 2012. What We Didn’t See Before. Yale journal of law and the humanities.

[^32]: Corbeiller, 1961. Miss America and Her Sisters: Personifications of the Four Parts of the World. Metropolitan Museum of Art Bulletin.

[^33]: Marconi & Almeida, 2023. In search of a queer pathos: Connections between Aby Warburg and Queer Studies. Acta Poética.

[^34]: Oswald, 2013. Aby Warburgs "Pathosformel".

[^35]: Rromán, 2017. El tiempo de las imágenes. Notas acerca de la Historia del Arte según Didi-Huberman.

[^36]: Dorléac, 2001. Georges Didi-Huberman. Devant le temps : histoire de l’art et anachronisme des images.

[^37]: Deturk, 2017. Memory of absence: Contemporary counter-monuments.

[^38]: Ponocná, 2025. Interrupting Memory: Anti-monuments and the Transformation of Commemoration in Mexico City. Cargo Journal.

[^39]: Stubblefield, 2012. Do Disappearing Monuments Simply Disappear?: The Counter-Monument in Revision. Future Anterior.

[^40]: Akademie. Cesare Ripa »Iconologia«.

[^41]: Seagle, 1945. Rudolf von Jhering: Or Law as a Means to an End. University of Chicago Law Review.

[^42]: Rapone, 2012. Der Zweckbegriff im Werk Rudolf von Jherings. Jahrbuch der Juristischen Zeitgeschichte.

[^43]: Canessa, 2008. Sex And The Citizen: Barbies And Beauty Queens In The Age Of Evo Morales1. Journal of Latin American Cultural Studies.

[^44]: 박기현, 2015. 현대 프랑스 시각 문화 비평.

[^45]: Ingravallo, 2007. The Grotta dei Cervi (Otranto – Lecce). Documenta Praehistorica.

[^46]: Nepomuceno, 2022. Sobrevivências do trágico: "páthos" e tragédia. Art research journal.

[^47]: Taccetta, 2021. Anacronismo, dialéctica y sublevación. O de cómo pensar la imagen a contrapelo. Revista de Filosofía Universidad Iberoamericana.

[^48]: Sabogal, 2013. Imágenes dialécticas y anacronismo en la historia del arte (según Georges Didi-Huberman).

[^49]: Tavares, 2012. O(s) Tempo(s) da Imagem : uma investigação sobre o estatuto temporal da imagem a partir da obra de Didi-Huberman.

[^50]: Prescott & Lahti, 2022. Looking Globally at Monuments, Violence, and Colonial Legacies. Journal of Genocide Research.

[^51]: Gutiérrez, 2026. FEMINISTS VERSUS MONUMENTS
 ? From Protests to Anti‐monuments in Mexico City. International Journal of Urban and Regional Research.

[^52]: Padovan, 2025. CONTRA-FEITIÇO, CONTRA-MONUMENTO. Pixo.

[^53]: Jansen, 2018. Rudolf von Jhering (1818-1892) und der Zweck im Recht (1877/1883) in den Niederlanden.

[^54]: Sampaio, 2014. O jurista alemão Rudolf von Ihering e a luta pelo Direito - Conjur.