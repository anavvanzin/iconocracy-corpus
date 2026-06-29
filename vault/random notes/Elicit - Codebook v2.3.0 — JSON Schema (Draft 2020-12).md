```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lpai.example.org/schemas/codebook-v2.3.0.schema.json",
  "title": "Registro LPAI v2.3.0",
  "description": "Schema de validacao para registros LPAI v2.3.0 (capta, nao data). Estende v2.2.0 com gramatica masculina (Hercules, atlantes/telamones, rios barbados e Netuno/Oceanus) e reforca a auditabilidade do genero como construcao iconografica, nao como default invisivel.[^1][^2][^3][^4][^5][^6][^7]",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "capta_declaration",
    "coder_id",
    "coded_at",
    "codebook_version",
    "pre_freeze_sample",
    "coder_position_statement",
    "confianca_codificacao",
    "item_id",
    "titulo",
    "suporte",
    "data_suporte",
    "instituicao_origem",
    "localizacao_atual",
    "familia_alegorica",
    "subtipo",
    "genero_atribuido",
    "funcao_juridica",
    "vetor_colonial",
    "dado_negativo",
    "finalidade_atribuida",
    "status_evidencia"
  ],
  "$defs": {
    "objetos_regalia_enum": {
      "type": "string",
      "enum": [
        "balanca",
        "espada",
        "venda",
        "espelho",
        "tocha",
        "globo",
        "cornucopia",
        "cetro",
        "coroa",
        "tridente",
        "fasces",
        "bandeira",
        "ramos_estrelas",
        "urna",
        "incensario",
        "clava",
        "leao_pele",
        "urna_vertedora",
        "vaso_fluvial",
        "tridente_imperial",
        "ancora_naval",
        "outro_objeto"
      ],
      "description": "Vocabulrio controlado de objetos/regalia. Em v2.3.0, inclui atributos de gramatica masculina (p.ex. clava herculea) e marcadores hidricos (urna vertedora/vaso).[^3][^6]"
    },
    "marcas_corporais_enum": {
      "type": "string",
      "enum": [
        "corpo_reclinado",
        "barba",
        "corpo_ereto",
        "corpo_sentado",
        "nudez_parcial",
        "nudez_total",
        "vestes_romanas",
        "vestes_indigenas",
        "vestes_africanas",
        "barba_longa",
        "corpo_ereto_em_esforco",
        "corpo_semirrecosto_fluvial",
        "musculatura_exibida",
        "postura_de_sustentacao",
        "gesto_indicativo_pedagogico",
        "outro_marcador"
      ],
      "description": "Vocabulrio controlado de marcas corporais. Em v2.3.0, inclui marcadores para reconhecer gramatica masculina: barba longa como significante hegemonico de autoridade; postura de sustento (atlantes); semirrecosto fluvial com urna; gesto indicativo como mediacao (divino-direito).[^2][^4][^6][^8]"
    },
    "marcadores_cena_enum": {
      "type": "string",
      "enum": [
        "arco_e_flecha",
        "cabeca_decepada",
        "animais_exoticos",
        "cobra",
        "escorpiao",
        "coroa_de_junco",
        "ondas_maritimas",
        "outro_cena"
      ]
    },
    "familia_alegorica_enum": {
      "type": "string",
      "enum": [
        "Virtudes",
        "Continentes",
        "Oceanos_Rios",
        "Nacional",
        "Afro_Brasileira",
        "Masculino_Juridico",
        "Outra"
      ],
      "description": "Enum de familias iconograficas. Inclui Masculino_Juridico para tornar codificavel a masculinidade como gramatica (nao default), dado que marcas como barba operam como significantes hegemonicos de autoridade e distincoes de poder.[^2]"
    },
    "subtipo_masculino_enum": {
      "type": "string",
      "enum": [
        "Hercules",
        "Atlante",
        "Telamon",
        "Rio_barbado",
        "Netuno",
        "Genio_protetor",
        "Heroi_civil",
        "outro_masculino"
      ],
      "description": "Subtipos sob Masculino_Juridico. Hercules e reconhecivel por nudez/clava e (em alguns programas) pelo bivio como problema de conhecimento; Atlante/Telamon por funcao de sustento; Rio_barbado por barba longa + semirrecosto + efluencia; Netuno/Oceanus por personificacao marinha disputada (Ocidente masculino vs tradicoes femininas).[^3][^4][^6][^7]"
    },
    "funcao_figura_masculina_enum": {
      "type": "string",
      "enum": [
        "forca_sustentadora",
        "soberania_territorial",
        "soberania_maritima",
        "mediacao_pedagogica",
        "protetorado_nacional",
        "heroismo_civil",
        "nao_aplicavel"
      ],
      "description": "Funcoes tipicas da gramatica masculina no programa iconografico: sustento (atlantes/Atlas), soberania territorial por rios colossais, soberania maritima (Oceanus/Netuno), mediacao pedagógica (bivio/gesto indicativo), protetorado (Genio do Brasil).[^4][^9][^7][^3][^8]"
    },
    "tipo_agencia_masculina_enum": {
      "type": "string",
      "enum": [
        "protetorado",
        "soberania",
        "mediacao_territorial",
        "sustentacao_arquitetonica",
        "pedagogia_moral",
        "nao_aplicavel"
      ],
      "description": "Modalidades de agencia masculina em casos brasileiros e transnacionais (p.ex. Genio do Brasil como ente guerreiro/protetor e instrumento de poder/união).[^9]"
    },
    "tipo_efluencia_hidrica_enum": {
      "type": "string",
      "enum": [
        "urna_vertedora",
        "vaso_inclinado",
        "sem_efluencia",
        "outra"
      ],
      "description": "Tipo de efluencia hidrica em personificacoes aquáticas masculinas. A coocorrencia de semirrecosto + urna que verte agua e um marcador discriminante do tipo aquático barbado.[^6]"
    },
    "substituicao_hercules_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "atributo_canonico_substituido": {
          "type": "string",
          "minLength": 1,
          "description": "Atributo canonico ausente (p.ex. 'clava')."
        },
        "atributo_novo": {
          "type": "string",
          "minLength": 1,
          "description": "Atributo que aparece no suporte e realiza funcao equivalente (p.ex. 'cetro_ou_vara')."
        },
        "justificativa": {
          "type": "string",
          "minLength": 1,
          "maxLength": 300,
          "description": "Justificativa da substituicao atributiva (p.ex. paratexto descreve cetro convertido em vara e manejado 'como Hercules a sua clava').[^9]"
        }
      },
      "required": [
        "atributo_canonico_substituido",
        "atributo_novo",
        "justificativa"
      ]
    },
    "referencia_genealogica_enum": {
      "type": "string",
      "enum": [
        "Ripa_1593_1603",
        "Ortelius_1570",
        "Collaert_Four_Continents",
        "Carriera_Four_Continents",
        "Warner_1985",
        "Resnik_Curtis_2011",
        "Souza_2014",
        "Ihering_Der_Zweck",
        "Warburg_Mnemosyne",
        "Didi_Huberman_Devant_le_temps",
        "Young_Counter_Monument",
        "Panofsky_Hercules_am_Scheidewege",
        "Lubbock_Atlantes",
        "Brazilian_Republican_Iconography",
        "outra"
      ],
      "description": "Enum de chaves genealogicas. Em v2.3.0, inclui pontes para bibliografia sobre Hercules (bivio, decisao) e atlantes/telamones, e um placeholder para iconografia republicana/imperial brasileira em chave masculina (Genio do Brasil; rios colossais).[^3][^4][^9]"
    },
    "indicador_ordinal_0_4": {
      "type": "integer",
      "minimum": 0,
      "maximum": 4
    },
    "status_contestacao_enum": {
      "type": "string",
      "enum": [
        "integro",
        "contestado_discursivamente",
        "defaced",
        "parcialmente_removido",
        "removido",
        "contramonumentalizado",
        "nao_aplicavel"
      ]
    },
    "tipo_intervencao_enum": {
      "type": "string",
      "enum": [
        "pichacao",
        "desfiguramento_fisico",
        "remocao_oficial",
        "derrubada",
        "recontextualizacao_curatorial",
        "contramonumento_novo",
        "nao_aplicavel"
      ]
    },
    "ator_categoria_enum": {
      "type": "string",
      "enum": [
        "movimento_feminista",
        "movimento_indigena",
        "movimento_negro",
        "movimento_lgbtqia",
        "sindicato",
        "poder_publico",
        "outro",
        "desconhecido"
      ]
    },
    "papel_atlas_enum": {
      "type": "string",
      "enum": [
        "nucleo",
        "borda",
        "contraste",
        "costura",
        "nao_definido"
      ]
    },
    "tipo_relacao_dialetica_enum": {
      "type": "string",
      "enum": [
        "sobrevivencia",
        "pathosformel_repetido",
        "contestacao_de",
        "contramonumento_a",
        "reapropriacao",
        "montagem_anacronica"
      ]
    },
    "tipo_contramonumento_enum": {
      "type": "string",
      "enum": [
        "oficial_encomendado",
        "insurgente_nao_oficial",
        "institucionalizado_a_posteriori",
        "nao_aplicavel"
      ]
    },
    "status_evidencia_enum": {
      "type": "string",
      "enum": [
        "core_verificado",
        "piloto",
        "comparador",
        "apendice"
      ]
    },
    "camada_temporal_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "data_aprox": {
          "type": "string",
          "description": "Data aproximada (p.ex. YYYY, YYYY-MM, YYYY-MM-DD ou 'c. YYYY') para registrar temporalidade composta/anacronica.[^10][^11][^12]"
        },
        "descricao": {
          "type": "string",
          "minLength": 1,
          "description": "Descricao da camada temporal, tornando auditavel a heterogeneidade de tempos que coabitam na imagem.[^10][^11]"
        },
        "fonte_iconografica": {
          "type": "string",
          "description": "Fonte/repertorio/arquivo invocado para esta camada (quando aplicavel)."
        }
      },
      "required": [
        "data_aprox",
        "descricao"
      ]
    },
    "posicao_atlas_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "prancha_id": {
          "type": "string",
          "minLength": 1,
          "description": "Identificador da prancha/atlas (p.ex. 'atlas_justica_01'), pois a montagem deve ser rastreavel como capta, nao naturalizada.[^13][^14]"
        },
        "linha": {
          "type": "integer",
          "minimum": 0
        },
        "coluna": {
          "type": "integer",
          "minimum": 0
        },
        "papel": {
          "$ref": "#/$defs/papel_atlas_enum",
          "description": "Papel relacional do item na montagem (nucleo/borda/contraste/costura), coerente com montagem como operacao que separa e conecta para produzir abalo/movimento e tornar visiveis encontros temporais.[^13][^14]"
        }
      },
      "required": [
        "prancha_id",
        "papel"
      ]
    },
    "ator_coletivo_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "nome_livre": {
          "type": "string",
          "description": "Nome do ator/coletivo conforme a fonte."
        },
        "categoria": {
          "$ref": "#/$defs/ator_categoria_enum",
          "description": "Categoria do ator coletivo; reconhece ativismo de base em contestacoes de monumentos e a necessidade de explicitar sujeitos politicos na producao do afterlife/counterarchive.[^15][^16]"
        }
      },
      "required": [
        "categoria"
      ]
    },
    "relacao_dialetica_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "item_id_outro": {
          "type": "string",
          "pattern": "^LPAI-[0-9]{4,}$"
        },
        "tipo_relacao": {
          "$ref": "#/$defs/tipo_relacao_dialetica_enum",
          "description": "Tipo de relacao dialetica (sobrevivencia, contestacao, montagem). Apoia leitura por constelacao/montagem e coexistencia de passado/presente.[^17][^13][^14]"
        }
      },
      "required": [
        "item_id_outro",
        "tipo_relacao"
      ]
    },
    "aplicabilidade_contextual_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "item_contestado": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_cautela",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade contextual em itens contestados; 'inverter_polaridade' reflete que intervencoes podem reabrir sentidos/afeto e recusar closure da monumentalidade.[^18][^19]"
        },
        "item_em_atlas": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_cautela",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade contextual em itens organizados por montagem/atlas; a montagem separa e conecta e escapa de teleologias, exigindo cautela na interpretacao ordinal.[^13][^14]"
        },
        "item_com_nachleben_marker": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_cautela",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade contextual em itens com Nachleben; formas sobrevivem e podem reaparecer re-semantizadas, exigindo cautela em leituras lineares.[^20][^12]"
        }
      }
    },
    "aplicabilidade_por_familia_masculina_obj": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "Hercules": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade do indicador ao subtipo Hercules; pode haver polaridade invertida quando ha enfase de corporeidade (nudez + clava).[^3]"
        },
        "Atlante": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ]
        },
        "Telamon": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade do indicador a atlantes/telamones como colunas antropomorficas de sustento (corpo como suporte).[^4]"
        },
        "Rio_barbado": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ]
        },
        "Netuno": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ]
        },
        "Genio_protetor": {
          "type": "string",
          "enum": [
            "aplicavel",
            "aplicavel_com_subaltern_caution",
            "nao_aplicavel",
            "inverter_polaridade"
          ],
          "description": "Aplicabilidade do indicador a casos brasileiros de agencia masculina (instrumento de poder e uniao nacional).[^9]"
        }
      }
    },
    "indicador_v230": {
      "description": "Indicador ordinal 0-4 (capta interpretativa). Em v2.2.0, pode carregar aplicabilidade_contextual. Em v2.3.0, pode carregar aplicabilidade_por_familia_masculina para explicitar inversoes de polaridade (p.ex. desincorporacao) em gramaticas masculinas de enfase corporal/sustento.[^1][^21][^22][^13][^14][^3][^4]",
      "oneOf": [
        {
          "$ref": "#/$defs/indicador_ordinal_0_4"
        },
        {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "score": {
              "$ref": "#/$defs/indicador_ordinal_0_4"
            },
            "aplicabilidade_contextual": {
              "$ref": "#/$defs/aplicabilidade_contextual_obj"
            },
            "aplicabilidade_por_familia_masculina": {
              "$ref": "#/$defs/aplicabilidade_por_familia_masculina_obj"
            }
          },
          "required": [
            "score"
          ]
        }
      ]
    }
  },
  "properties": {
    "capta_declaration": {
      "type": "string",
      "const": "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.",
      "description": "Declaracao fixa que marca o registro como capta (tomado/construido) e nao como dado dado; alinhado a repensar 'data' como 'capta'.[^1][^23]"
    },
    "coder_id": {
      "type": "string",
      "minLength": 1,
      "description": "Identificador do/a codificador/a responsavel."
    },
    "coded_at": {
      "type": "string",
      "format": "date-time",
      "description": "Data/hora da codificacao em ISO 8601."
    },
    "codebook_version": {
      "type": "string",
      "const": "2.3.0",
      "description": "Versao do codebook; deve igualar 2.3.0."
    },
    "pre_freeze_sample": {
      "type": "boolean",
      "description": "Indica fase pre-freeze (piloto), em que ajustes de schema ainda sao permitidos."
    },
    "coder_position_statement": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "Declaracao curta de posicao para tornar auditavel o trabalho e o contexto do capta; reconhece que poder, emocao, pluralidade e trabalho atravessam projetos de dados/capta.[^24]"
    },
    "confianca_codificacao": {
      "type": "string",
      "enum": [
        "alta",
        "media",
        "baixa"
      ],
      "description": "Autoavaliacao de confianca; reconhece ambiguidade do icone e dependencia de leitura por observadores, contextos e intencoes.[^21][^22]"
    },
    "motivo_incerteza": {
      "type": "string",
      "maxLength": 300,
      "description": "Justificativa curta para incerteza; obrigatorio quando confianca_codificacao != 'alta'."
    },
    "item_id": {
      "type": "string",
      "pattern": "^LPAI-[0-9]{4,}$",
      "description": "Identificador unico do item."
    },
    "titulo": {
      "type": "string",
      "minLength": 3,
      "description": "Titulo curto do item."
    },
    "suporte": {
      "type": "string",
      "description": "Suporte material (p. ex., moeda, cedula, selo, brasao, arquitetura, monumento)."
    },
    "data_suporte": {
      "type": "string",
      "description": "Data do suporte; aceita ano (YYYY), intervalo (YYYY-YYYY) ou data completa (YYYY-MM-DD).",
      "oneOf": [
        {
          "pattern": "^[0-9]{4}$"
        },
        {
          "pattern": "^[0-9]{4}-[0-9]{4}$"
        },
        {
          "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        }
      ]
    },
    "instituicao_origem": {
      "type": "string",
      "minLength": 1,
      "description": "Instituicao emissora/produtora do item."
    },
    "localizacao_atual": {
      "type": "string",
      "minLength": 1,
      "description": "Acervo/colecao/localizacao atual do item."
    },
    "fonte_imagem": {
      "type": "string",
      "format": "uri",
      "description": "Rastreabilidade da imagem (URL ou referencia arquivistica); relevante pois edicoes variam e nem todas as alegorias sao ilustradas, afetando o que e visivel e codificavel.[^25]"
    },
    "edicao_suporte": {
      "type": "string",
      "description": "Edicao/estado do suporte quando aplicavel; relevante porque ha series de figuras proximas mas distintas e nem todas as alegorias sao ilustradas, o que afeta inferencias de atributos.[^25]"
    },
    "tipo_reproducao": {
      "type": "string",
      "enum": [
        "original",
        "reproducao_fotografica",
        "gravura_impressa",
        "digital",
        "outro"
      ],
      "description": "Tipo de reproducao usada para codificacao; impacta o que e visivel e, portanto, o capta (ambiguidade do concreto).[^21]"
    },
    "familia_alegorica": {
      "$ref": "#/$defs/familia_alegorica_enum",
      "description": "Familia iconografica predominante; em v2.3.0, inclui Masculino_Juridico para codificar gramatica masculina de autoridade/sustento/territorializacao (Hercules, Atlantes/Telamones, rios barbados, Netuno/Oceanus).[^3][^4][^9][^6][^7]"
    },
    "subtipo": {
      "type": "string",
      "description": "Subtipo dentro da familia; restringido por familia_alegorica via if/then. Em v2.3.0, inclui subtipos masculinos para evitar colapso interpretativo em 'outra'.[^3][^4][^9]"
    },
    "objetos_regalia": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/objetos_regalia_enum"
      },
      "uniqueItems": true,
      "description": "Lista de objetos/regalia visiveis; operacionaliza decomposicao em elementos alegoricos (objetos etc.) para comparabilidade.[^26]"
    },
    "marcas_corporais": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/marcas_corporais_enum"
      },
      "uniqueItems": true,
      "description": "Marcas corporais/poses/vestes; inclui marcadores para reconhecer gramatica masculina (barba longa; postura de sustentacao; semirrecosto fluvial; gesto indicativo).[^2][^4][^6][^8]"
    },
    "marcadores_cena_arquitetura": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/marcadores_cena_enum"
      },
      "uniqueItems": true,
      "description": "Marcadores de cena/ambiente/accoutrements; relevantes porque personificacoes continentais operam por accoutrements e hierarquias visuais (Europa entronizada etc.).[^27][^28]"
    },
    "genero_atribuido": {
      "type": "string",
      "enum": [
        "feminino",
        "masculino",
        "neutro",
        "hibrido",
        "ausente"
      ],
      "description": "Genero predominante da personificacao. Em v2.3.0, reforca-se que o masculino nao e default neutro, pois marcas (p.ex. barba) distinguem homens autoritativos e hierarquias sociais e precisam ser auditaveis na codificacao.[^2]"
    },
    "justificativa_genero": {
      "type": "string",
      "maxLength": 300,
      "description": "Justificativa baseada em marcadores visiveis para reduzir reificacao do genero na codificacao e reconhecer ambivalencia do icone. Em v2.3.0, quando genero_atribuido=masculino ou familia_alegorica=Masculino_Juridico, exige-se justificativa substantiva (minLength 80) para evitar default invisivel.[^21][^22][^2]"
    },
    "funcao_juridica": {
      "type": "string",
      "enum": [
        "tribunal_consciencia",
        "frontispicio_normativo",
        "moeda_cedula",
        "selo_postal",
        "brasao",
        "arquitetura_forense",
        "monumento_publico",
        "monumento_contestado",
        "paratexto_normativo",
        "outro"
      ],
      "description": "Funcao do dispositivo no espaco juridico-estatal; conecta visualidade a sitio/arquitetura (seen/sited) e a desejos de governos de sinalizar valores politico-juridicos. Inclui 'monumento_contestado' para casos em que a disputa/afterlife e parte substantiva do dispositivo.[^29][^18][^16]"
    },
    "vetor_colonial": {
      "type": "string",
      "enum": [
        "europeu_direto",
        "luso_brasileiro",
        "republicano_brasileiro",
        "nao_aplicavel"
      ],
      "description": "Rota de transmissao do repertorio; relevante porque esquemas (ex.: Quatro Continentes) circulam em multiplos suportes e contextos.[^30]"
    },
    "hipotese_racial": {
      "type": "string",
      "maxLength": 500,
      "description": "Campo interpretativo curto sobre como genero e raca se cruzam; recomendado. Cautela: stand-ins continentais nao sao evidencia documental de povos diversos e adotam ideais classicizantes generalizados.[^27][^31]"
    },
    "referencia_genealogica": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/referencia_genealogica_enum"
      },
      "uniqueItems": true,
      "description": "Chaves de referencia genealogica (pode ser multipla); explicita mediacao textual/repertorial e, em v2.3.0, inclui chaves para Hercules/atlantes e iconografia brasileira masculina como placeholders rastreaveis.[^32][^3][^9]"
    },
    "dado_negativo": {
      "type": "boolean",
      "description": "True quando a ausencia de figura humana e analiticamente significativa (nao mero missing), pois a leitura de signos depende de contexto e pode operar pelo negativo.[^21][^22]"
    },
    "power_at_stake": {
      "type": "string",
      "maxLength": 300,
      "description": "Quem se beneficia (e quem e marginalizado) pelo artefato/codificacao; operacionaliza a pergunta 'who benefits' em projetos de dados/capta.[^24]"
    },
    "finalidade_atribuida": {
      "type": "string",
      "enum": [
        "legitimacao_juridica",
        "pedagogia_civica",
        "dissuasao",
        "comemoracao",
        "branding_estatal",
        "outro"
      ],
      "description": "Finalidade social/politica atribuida (teleologia). Em Ihering, o direito e meio para um fim social; codificar finalidade alinha leitura iconografica a Zweck institucional.[^33][^34]"
    },
    "relacao_com_repertorio_indigena": {
      "type": "string",
      "enum": [
        "ausente",
        "apropriado",
        "coexistente",
        "hibridizado",
        "nao_aplicavel"
      ],
      "description": "Relacao com repertorios indigenas; cautela porque a colonialidade pode feminilizar e hierarquizar alteridades (terra feminilizada disponivel a posse).[^31][^35]"
    },
    "status_evidencia": {
      "$ref": "#/$defs/status_evidencia_enum",
      "description": "Status de evidencia e inclusao (core vs comparador). Regra: se status_contestacao != 'integro' e != 'nao_aplicavel', exige evidencia_visual_intervencao para classificar como core_verificado, pois remocao/contestacao nao deve ser ponto final e requer afterlife/counterarchive documental.[^16]"
    },
    "nachleben_marker": {
      "type": "boolean",
      "description": "Marca hipotese de sobrevivencia/retorno (Nachleben) de forma/motivo; formas nao param de sobreviver e podem reaparecer re-semantizadas, exigindo registrar camadas temporais e evitar linearidade.[^20][^12]"
    },
    "camadas_temporais": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/camada_temporal_obj"
      },
      "description": "Lista de camadas temporais do item; reconhece anacronismo como riqueza interior as imagens e que todos os tempos se encontram nelas, demandando registro auditavel da temporalidade composta.[^10][^11]"
    },
    "pertencimento_atlas": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      },
      "description": "IDs de pranchas/atlas (montagens). A montagem separa e conecta e escapa de teleologias, tornando visiveis sobrevivencias/anacronismos; por isso o pertencimento e um ato capta rastreavel.[^13][^14]"
    },
    "posicao_no_atlas": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/posicao_atlas_obj"
      },
      "description": "Posicoes (uma por prancha) para reconstruir e debater a constelacao produzida pela montagem; evita naturalizar a prancha como ordem objetiva.[^13][^14]"
    },
    "relacao_dialetica_com_item": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/relacao_dialetica_obj"
      },
      "description": "Relacoes dialeticas entre itens (sobrevivencia, contestacao, montagem). A imagem pode ser entendida como constelacao em que passado encontra o presente, implicando redes relacionais para alem de sequencias lineares.[^17][^13][^14]"
    },
    "status_contestacao": {
      "$ref": "#/$defs/status_contestacao_enum",
      "description": "Estado processual de contestacao/afterlife. Alinha-se a teoria do counter-monument e ao argumento de que a remocao nao deve ser endpoint, exigindo afterlife/counterarchive.[^36][^16]"
    },
    "tipo_intervencao": {
      "$ref": "#/$defs/tipo_intervencao_enum",
      "description": "Modalidade de intervencao (pichacao, desfiguramento etc.). Responde a repertorio plural de intervencoes: monumentos podem ser defaced, painted over, toppled, reconfigured, restaged, reimagined, etc.[^18]"
    },
    "data_evento_contestacao": {
      "type": "string",
      "pattern": "^[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?$",
      "description": "Data aproximada do evento de contestacao (YYYY ou YYYY-MM ou YYYY-MM-DD). Coerente com a possibilidade de mudanca ao longo do tempo em contramonumentos e com a necessidade de registrar trajeto/afterlife.[^36][^16]"
    },
    "ator_coletivo_contestacao": {
      "$ref": "#/$defs/ator_coletivo_obj",
      "description": "Autoria coletiva do ato de contestacao; registra sujeitos politicos e o papel de ativismo de base em expor consequencias do passado colonial no presente.[^15]"
    },
    "evidencia_visual_intervencao": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      },
      "description": "URLs/referencias para antes/depois e fontes; exigencia de afterlife/counterarchive para que remocao/contestacao nao seja tratada como ponto final.[^16]"
    },
    "tipo_contramonumento": {
      "$ref": "#/$defs/tipo_contramonumento_enum",
      "description": "Distingue contramonumento oficial/encomendado de formas insurgentes e de institucionalizacoes a posteriori; alinha-se a teoria de contra-monumentos e anti-monuments que recusam permanencia/closure.[^37][^19]"
    },
    "funcao_da_figura_masculina": {
      "$ref": "#/$defs/funcao_figura_masculina_enum",
      "description": "Funcao/operatividade da figura masculina no programa iconografico. Sustenta reconhecer o bivio como problema de conhecimento (distincao falso/verdadeiro; virtude/vicio), a funcao de sustento (atlantes/Atlas) e a territorializacao por rios colossais e agncia protetiva no Brasil (Genio do Brasil).[^3][^4][^9]"
    },
    "tipo_agencia_masculina": {
      "$ref": "#/$defs/tipo_agencia_masculina_enum",
      "description": "Modalidade de agencia masculina. Em casos brasileiros, o Genio do Brasil e descrito como masculino e ativo (ente guerreiro e protetor) e como instrumento de poder e uniao nacional.[^9]"
    },
    "funcao_atlanteana": {
      "type": "boolean",
      "description": "True quando a figura cumpre funcao explicita de suporte/sustentacao (atlantes/telamones como colunas antropomorficas; Atlas como suporte do mundo).[^4][^38]"
    },
    "tipo_efluencia_hidrica": {
      "$ref": "#/$defs/tipo_efluencia_hidrica_enum",
      "description": "Tipo de efluencia hidrica em personificacoes aquáticas masculinas. Codifica a presenca de urna que verte agua como marcador discriminante do tipo aquático barbado (rio/mar), evitando inferir a partir de barba isolada.[^6][^2]"
    },
    "substituicao_atributiva_hercules": {
      "$ref": "#/$defs/substituicao_hercules_obj",
      "description": "Objeto que registra reconhecimento de Hercules por substituicao atributiva (p.ex. cetro/vara manejado como clava). Torna auditavel a ponte inferencial quando o atributo canonico nao esta visivel no suporte.[^9]"
    },
    "indicadores_purificacao": {
      "type": "object",
      "additionalProperties": false,
      "description": "Indicadores ordinais (0-4) como capta interpretativa; leitura iconografica e ambigua e contextual e nao deve ser tratada como medida neutra. Em v2.3.0, adiciona-se opcionalmente aplicabilidade_por_familia_masculina para explicitar inversoes (p.ex. enfase do corpo em Hercules/atlantes pode inverter intuicoes de desincorporacao).[^1][^21][^22][^3][^4]",
      "properties": {
        "desincorporacao": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. Perda/retirada do corpo (especialmente feminino). Em gramatica masculina, pode haver polaridade invertida quando o corpo e enfatizado (nudez/clava; sustento).[^3][^4]"
        },
        "heraldizacao": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. Conversao em emblema/heraldica/selo."
        },
        "enquadramento_arquitetonico": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. Enquadramento por arquitetura (tribunais, igrejas, monumentos)."
        },
        "serialidade": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. Repeticao seriada (moedas, selos, cedulas, impressos)."
        },
        "inscricao_estatal": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. Intensidade de inscricao estatal/autoridade institucional."
        },
        "classicizacao": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. [nota_lacuna] Placeholder ate harmonizacao com documento-pai; ligado a ideals classicizantes generalizados.[^27]"
        },
        "moralizacao": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. [nota_lacuna] Placeholder ate harmonizacao com documento-pai."
        },
        "depuracao_semantica": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. [nota_lacuna] Placeholder ate harmonizacao com documento-pai."
        },
        "neutralizacao_afetiva": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. [nota_lacuna] Placeholder ate harmonizacao com documento-pai; atencao a emocao como contexto vital em projetos de dados/capta.[^24]"
        },
        "monumentalizacao": {
          "$ref": "#/$defs/indicador_v230",
          "description": "0-4. [nota_lacuna] Placeholder ate harmonizacao com documento-pai."
        }
      }
    },
    "adjudicacao_log": {
      "type": "string",
      "description": "Nota opcional de adjudicacao intercodificador (quando houver desacordo)."
    },
    "subaltern_caution": {
      "type": "string",
      "description": "Nota opcional/condicional de cautela quando escalas/categorias forem aplicadas a casos subalternizados, masculinos ou de ausencia; registrar base interpretativa (leituras dependem de espectadores e contextos).[^22]"
    },
    "notes": {
      "type": "string",
      "description": "Campo livre para notas adicionais (proveniencia, edicao, ambiguidades)."
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "confianca_codificacao": {
            "not": {
              "const": "alta"
            }
          }
        },
        "required": [
          "confianca_codificacao"
        ]
      },
      "then": {
        "required": [
          "motivo_incerteza"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "genero_atribuido": {
            "const": "feminino"
          }
        },
        "required": [
          "genero_atribuido"
        ]
      },
      "then": {
        "required": [
          "justificativa_genero"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "genero_atribuido": {
            "const": "masculino"
          }
        },
        "required": [
          "genero_atribuido"
        ]
      },
      "then": {
        "required": [
          "justificativa_genero"
        ],
        "properties": {
          "justificativa_genero": {
            "type": "string",
            "minLength": 80
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Masculino_Juridico"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "required": [
          "subtipo",
          "funcao_da_figura_masculina"
        ],
        "properties": {
          "subtipo": {
            "$ref": "#/$defs/subtipo_masculino_enum"
          },
          "justificativa_genero": {
            "type": "string",
            "minLength": 80
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Virtudes"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "properties": {
          "subtipo": {
            "enum": [
              "Iustitia",
              "Veritas",
              "Prudencia",
              "Fortaleza",
              "Temperanca",
              "Justica_e_Paz",
              "Esperanca",
              "Caridade",
              "Fe",
              "Fama",
              "outra_virtude"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Continentes"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "properties": {
          "subtipo": {
            "enum": [
              "Europa",
              "America_generica",
              "America_do_Sul",
              "Africa",
              "Asia",
              "outro_continente"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Oceanos_Rios"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "properties": {
          "subtipo": {
            "enum": [
              "Oceano",
              "Rio_grande",
              "Rio_menor",
              "Fonte",
              "Netuno",
              "Tetis",
              "outro_hidrico"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Nacional"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "properties": {
          "subtipo": {
            "enum": [
              "Republica",
              "Liberdade",
              "Patria",
              "Brasil",
              "outra_nacional"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "familia_alegorica": {
            "const": "Afro_Brasileira"
          }
        },
        "required": [
          "familia_alegorica"
        ]
      },
      "then": {
        "properties": {
          "subtipo": {
            "enum": [
              "Oxum",
              "Iemanja",
              "Exu",
              "orixa_outro",
              "afro_generica"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "nachleben_marker": {
            "const": true
          }
        },
        "required": [
          "nachleben_marker"
        ]
      },
      "then": {
        "required": [
          "camadas_temporais"
        ],
        "properties": {
          "camadas_temporais": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "status_contestacao": {
            "enum": [
              "contestado_discursivamente",
              "defaced",
              "parcialmente_removido",
              "removido",
              "contramonumentalizado"
            ]
          }
        },
        "required": [
          "status_contestacao"
        ]
      },
      "then": {
        "required": [
          "tipo_intervencao",
          "data_evento_contestacao",
          "ator_coletivo_contestacao",
          "evidencia_visual_intervencao"
        ],
        "properties": {
          "evidencia_visual_intervencao": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "status_contestacao": {
            "const": "contramonumentalizado"
          }
        },
        "required": [
          "status_contestacao"
        ]
      },
      "then": {
        "required": [
          "tipo_contramonumento"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "pertencimento_atlas": {
            "type": "array",
            "minItems": 1
          }
        },
        "required": [
          "pertencimento_atlas"
        ]
      },
      "then": {
        "required": [
          "posicao_no_atlas"
        ],
        "properties": {
          "posicao_no_atlas": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "funcao_juridica": {
            "enum": [
              "monumento_publico",
              "monumento_contestado"
            ]
          }
        },
        "required": [
          "funcao_juridica"
        ]
      },
      "then": {
        "required": [
          "status_contestacao"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "status_evidencia": {
            "const": "core_verificado"
          },
          "status_contestacao": {
            "enum": [
              "contestado_discursivamente",
              "defaced",
              "parcialmente_removido",
              "removido",
              "contramonumentalizado"
            ]
          }
        },
        "required": [
          "status_evidencia",
          "status_contestacao"
        ]
      },
      "then": {
        "required": [
          "evidencia_visual_intervencao"
        ],
        "properties": {
          "evidencia_visual_intervencao": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "status_contestacao": {
            "not": {
              "enum": [
                "integro",
                "nao_aplicavel"
              ]
            }
          }
        },
        "required": [
          "status_contestacao"
        ]
      },
      "then": {
        "properties": {
          "coder_position_statement": {
            "type": "string",
            "minLength": 100
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "subtipo": {
            "const": "Rio_barbado"
          }
        },
        "required": [
          "subtipo"
        ]
      },
      "then": {
        "required": [
          "tipo_efluencia_hidrica"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "subtipo": {
            "enum": [
              "Atlante",
              "Telamon"
            ]
          }
        },
        "required": [
          "subtipo"
        ]
      },
      "then": {
        "required": [
          "funcao_atlanteana"
        ],
        "properties": {
          "funcao_atlanteana": {
            "const": true
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "subtipo": {
            "const": "Hercules"
          },
          "objetos_regalia": {
            "type": "array",
            "not": {
              "contains": {
                "const": "clava"
              }
            }
          }
        },
        "required": [
          "subtipo",
          "objetos_regalia"
        ]
      },
      "then": {
        "required": [
          "substituicao_atributiva_hercules"
        ]
      }
    },
    {
      "if": {
        "properties": {
          "genero_atribuido": {
            "const": "masculino"
          }
        },
        "required": [
          "genero_atribuido"
        ]
      },
      "then": {
        "required": [
          "funcao_da_figura_masculina"
        ]
      }
    }
  ],
  "examples": [
    {
      "capta_declaration": "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.",
      "coder_id": "coder_exemplo_001",
      "coded_at": "2026-06-23T14:35:00-03:00",
      "codebook_version": "2.3.0",
      "pre_freeze_sample": true,
      "coder_position_statement": "Historiadora da arte; codificacao baseada em reproducao digital; atencao a convencoes de personificacao e a ambiguidade do signo.",
      "confianca_codificacao": "alta",
      "item_id": "LPAI-18890001",
      "titulo": "Efigie da Republica (moeda)",
      "suporte": "moeda",
      "data_suporte": "1889",
      "instituicao_origem": "Casa da Moeda do Brasil",
      "localizacao_atual": "(a preencher)",
      "fonte_imagem": "https://eidolonstation.com/eidolon_posts/efigie-da-republica-brazil/",
      "tipo_reproducao": "digital",
      "familia_alegorica": "Nacional",
      "subtipo": "Republica",
      "objetos_regalia": [
        "coroa"
      ],
      "marcas_corporais": [
        "vestes_romanas"
      ],
      "marcadores_cena_arquitetura": [],
      "genero_atribuido": "feminino",
      "justificativa_genero": "Figura feminina jovem com coroa de louros em estilo romano.",
      "funcao_juridica": "moeda_cedula",
      "vetor_colonial": "republicano_brasileiro",
      "dado_negativo": false,
      "finalidade_atribuida": "branding_estatal",
      "referencia_genealogica": [
        "Warner_1985",
        "Ripa_1593_1603"
      ],
      "status_evidencia": "piloto",
      "nachleben_marker": false,
      "camadas_temporais": [],
      "pertencimento_atlas": [],
      "posicao_no_atlas": [],
      "status_contestacao": "nao_aplicavel"
    },
    {
      "capta_declaration": "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.",
      "coder_id": "coder_exemplo_002",
      "coded_at": "2026-06-23T15:10:00-03:00",
      "codebook_version": "2.3.0",
      "pre_freeze_sample": true,
      "coder_position_statement": "Registro de monumento contestado; classificacao baseada em noticia e imagens antes/depois; atencao a disputa do gesto e ao principio de afterlife.",
      "confianca_codificacao": "media",
      "motivo_incerteza": "Nem todas as imagens antes/depois estao arquivadas em fonte institucional; base principal e jornalistica.",
      "item_id": "LPAI-20210724",
      "titulo": "Estatua de Borba Gato (monumento contestado)",
      "suporte": "monumento",
      "data_suporte": "1963",
      "instituicao_origem": "(a preencher)",
      "localizacao_atual": "Sao Paulo",
      "fonte_imagem": "https://g1.globo.com/sp/noticia/2021/07/24/estatua-de-borba-gato-e-incendiada-por-grupo-em-sao-paulo.ghtml",
      "tipo_reproducao": "digital",
      "familia_alegorica": "Outra",
      "subtipo": "outra",
      "objetos_regalia": [],
      "marcas_corporais": [],
      "marcadores_cena_arquitetura": [],
      "genero_atribuido": "ausente",
      "funcao_juridica": "monumento_contestado",
      "vetor_colonial": "nao_aplicavel",
      "dado_negativo": false,
      "finalidade_atribuida": "comemoracao",
      "referencia_genealogica": [
        "Young_Counter_Monument"
      ],
      "status_evidencia": "piloto",
      "nachleben_marker": false,
      "camadas_temporais": [],
      "pertencimento_atlas": [],
      "posicao_no_atlas": [],
      "status_contestacao": "defaced",
      "tipo_intervencao": "desfiguramento_fisico",
      "data_evento_contestacao": "2021-07-24",
      "ator_coletivo_contestacao": {
        "nome_livre": "Revolucao Periferica",
        "categoria": "outro"
      },
      "evidencia_visual_intervencao": [
        "https://exemplo.org/borba-gato-antes",
        "https://exemplo.org/borba-gato-depois",
        "https://g1.globo.com/sp/noticia/2021/07/24/estatua-de-borba-gato-e-incendiada-por-grupo-em-sao-paulo.ghtml"
      ],
      "tipo_contramonumento": "nao_aplicavel"
    },
    {
      "capta_declaration": "LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.",
      "coder_id": "coder_exemplo_003",
      "coded_at": "2026-06-24T10:00:00-03:00",
      "codebook_version": "2.3.0",
      "pre_freeze_sample": true,
      "coder_position_statement": "Identificacao herculea por substituicao atributiva; base em paratexto (cetro convertido em vara; manejo como clava). Registro torna explicita a ponte inferencial.",
      "confianca_codificacao": "media",
      "motivo_incerteza": "A imagem do suporte nao apresenta clava literal; a identificacao depende de descricao paratextual.",
      "item_id": "LPAI-18000001",
      "titulo": "Genio do Brasil como Hercules (substituicao atributiva)",
      "suporte": "frontispicio",
      "data_suporte": "(a preencher)",
      "instituicao_origem": "(a preencher)",
      "localizacao_atual": "(a preencher)",
      "fonte_imagem": "http://www.dezenovevinte.net/obras/obras_amc.htm",
      "tipo_reproducao": "digital",
      "familia_alegorica": "Masculino_Juridico",
      "subtipo": "Hercules",
      "objetos_regalia": [
        "leao_pele"
      ],
      "marcas_corporais": [
        "corpo_ereto"
      ],
      "marcadores_cena_arquitetura": [],
      "genero_atribuido": "masculino",
      "justificativa_genero": "Paratexto descreve explicitamente o Genio como masculino e ativo; postura majestatica com cetro/vara como elemento de poder; articulacao herculea por manejo do cetro como clava.",
      "funcao_juridica": "frontispicio_normativo",
      "vetor_colonial": "luso_brasileiro",
      "dado_negativo": false,
      "finalidade_atribuida": "legitimacao_juridica",
      "status_evidencia": "piloto",
      "referencia_genealogica": [
        "Brazilian_Republican_Iconography",
        "Panofsky_Hercules_am_Scheidewege"
      ],
      "status_contestacao": "nao_aplicavel",
      "funcao_da_figura_masculina": "protetorado_nacional",
      "tipo_agencia_masculina": "protetorado",
      "funcao_atlanteana": false,
      "nachleben_marker": true,
      "camadas_temporais": [
        {
          "data_aprox": "antiguidade (modelo)",
          "descricao": "Gramatica herculea de forca e decisao",
          "fonte_iconografica": "(preencher)"
        },
        {
          "data_aprox": "sec. XIX",
          "descricao": "Recontextualizacao luso-brasileira (cetro/vara como clava)",
          "fonte_iconografica": "http://www.dezenovevinte.net/obras/obras_amc.htm"
        }
      ],
      "substituicao_atributiva_hercules": {
        "atributo_canonico_substituido": "clava",
        "atributo_novo": "cetro_ou_vara",
        "justificativa": "Paratexto: o cetro se convertera em vara magica e sera manejado como Hercules a sua clava."
      }
    }
  ]
}
```

[^1]: Humanities Approaches to Graphical Display.

[^2]: Bendall, 2022. Female Personifications and Masculine Forms: Gender, Armour and Allegory in the Habsburg–Valois Conflicts of Sixteenth‐Century Europe. Gender & History.

[^3]: Villari, 2015. L'«Ercole al bivio» di Domenico Beccafumi (1486-1551) e l'Ercole giraldiano.

[^4]: orioqueorionaove, 2012. A fachada do IPHAN | O RIO QUE O RIO NÃO VÊ.

[^5]: Lazzaro, 2011. River gods: personifying nature in sixteenth‐century Italy. Renaissance Studies.

[^6]: Estella, 2002. El llamado Neptuno (Río?) de la Colección del Carpio y su problemática identificación con una obra atribuida a Bernini, en Aranjuez. Archivo Espanol De Arte.

[^7]: López, 2017. La personificación del mar: Evolución y transformaciones iconográficas del mundo clásico al medioevo.

[^8]: Immagini della Giustizia: antiporte: Titius, Observationum ratiocinantium ... (1).

[^9]: 19&20 - O Gênio do Brasil e as Musas: Um manifesto ideológico numa
nação em construção, por Alberto Martín Chillón.

[^10]: Rromán, 2017. El tiempo de las imágenes. Notas acerca de la Historia del Arte según Didi-Huberman.

[^11]: Dorléac, 2001. Georges Didi-Huberman. Devant le temps : histoire de l’art et anachronisme des images.

[^12]: 박기현, 2015. 현대 프랑스 시각 문화 비평.

[^13]: Nepomuceno, 2022. Sobrevivências do trágico: "páthos" e tragédia. Art research journal.

[^14]: Taccetta, 2021. Anacronismo, dialéctica y sublevación. O de cómo pensar la imagen a contrapelo. Revista de Filosofía Universidad Iberoamericana.

[^15]: Prescott & Lahti, 2022. Looking Globally at Monuments, Violence, and Colonial Legacies. Journal of Genocide Research.

[^16]: Coomasaru et al., 2023. Monuments Must Fall. British Art Studies.

[^17]: Tavares, 2012. O(s) Tempo(s) da Imagem : uma investigação sobre o estatuto temporal da imagem a partir da obra de Didi-Huberman.

[^18]: Abraham, 2021. Toppled Monuments and Black Lives Matter: Race, Gender, and Decolonization in the Public Space. An Interview with Charmaine A. Nelson. Atlantis.

[^19]: Ponocná, 2025. Interrupting Memory: Anti-monuments and the Transformation of Commemoration in Mexico City. Cargo Journal.

[^20]: Marconi & Almeida, 2023. In search of a queer pathos: Connections between Aby Warburg and Queer Studies. Acta Poética.

[^21]: Dennis et al., 2010. Essays Images of Justice.

[^22]: Hayaert, 2018. The Paradoxes of Lady Justice’s Blindfold.

[^23]: Why Digital Humanists Should Emphasize Situated Data over Capta | 10 |, 2025.

[^24]: Mika, 2021. Book Review: Data Feminism. Journal of eScience Librarianship.

[^25]: Emblèmes 1603 : Cesare Ripa, Iconologia... (2e éd.; 1ère éd. illustrée), Rome, L. Facii | Utpictura18.

[^26]: Maffei & Procaccioli, 2012. Cesare Ripa, Iconologia. A cura di Sonia Maffei. Testo stabilito da Paolo Procaccioli.

[^27]: Sutton, 2009. Mapping Meaning: Ethnography and Allegory in Netherlandish Cartography, 1570-1655. Itinerario: International Journal on the History of European Expansion and Global Interaction.

[^28]: Neumann, 2009. Imagining European community on the title page of Ortelius' Theatrum Orbis Terrarum (1570). Word & Image.

[^29]: Tait, 2012. What We Didn’t See Before. Yale journal of law and the humanities.

[^30]: Corbeiller, 1961. Miss America and Her Sisters: Personifications of the Four Parts of the World. Metropolitan Museum of Art Bulletin.

[^31]: Detsi-Diamanti, 2006. Politicizing Aesthetics. Anachronist.

[^32]: English Translations and Adaptations of Cesare Ripa's Iconologia: From the 17th to the 19th Century Hans-Joachim Zimmermann, De Zeventiende Eeuw. Jaargang 11 - DBNL.

[^33]: Seagle, 1945. Rudolf von Jhering: Or Law as a Means to an End. University of Chicago Law Review.

[^34]: Sampaio, 2014. O jurista alemão Rudolf von Ihering e a luta pelo Direito - Conjur.

[^35]: Canessa, 2008. Sex And The Citizen: Barbies And Beauty Queens In The Age Of Evo Morales1. Journal of Latin American Cultural Studies.

[^36]: Deturk, 2017. Memory of absence: Contemporary counter-monuments.

[^37]: Stubblefield, 2012. Do Disappearing Monuments Simply Disappear?: The Counter-Monument in Revision. Future Anterior.

[^38]: Schröder, 2014. Images and messages in the embellishment of metropolitan railway stations (1850-1950).