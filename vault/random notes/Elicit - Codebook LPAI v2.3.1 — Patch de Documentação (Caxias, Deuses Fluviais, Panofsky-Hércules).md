---
documento: codebook-patch
versao_anterior: 2.3.0
versao_alvo: 2.3.1
tipo_patch: "documentacao_apenas (sem novos campos)"
data: (preencher)
autor: (preencher)
escopo: "patch PATCH; nao altera schema; nao re-pontua itens; preenche tres lacunas declaradas em v2.3.0"
documento_justificativo: schema/adendo-lacunas-v2.3.1.md
schema_companheiro_inalterado: schema/codebook-v2.3.0.yaml
---

# Patch v2.3.1 de documentação do Codebook LPAI

## Cabecalho YAML front-matter

O front-matter YAML no topo deste arquivo formaliza o caráter de patch documental, isto é, um ajuste de rastreabilidade e de reconhecimento iconográfico orientado por evidências textuais e de acervo que tornam a interpretação verificável e auditável, em vez de depender apenas de “legados” escritos ou de nomeações não justificadas.[^1][^2]

A motivação substantiva do patch está ancorada em três blocos de evidência: (i) a tensão entre monumentalização e baixa legibilidade pública no caso de Caxias; (ii) o dinheiro como circuito de circulação de “mensagens” estatais, com organização faceada (anverso/reverso) e risco de inferência indevida de personificações fluviais; e (iii) Panofsky como exemplo de “method in application” e como advertência de contestabilidade na nomeação de “Hercules am Scheidewege”.[^3][^4][^5][^6][^7]

## 1. Motivacao em 4 bullets

Este patch responde a lacunas declaradas anteriormente e reorganiza o material recuperado como verbetes, regras e exemplos, porque a base textual indica que leituras iconográficas ampliam o campo interpretativo “para além” do que sociedades deixaram conscientemente como legado, exigindo documentação explícita das inferências e de seus suportes.[^1]

- A lacuna “Caxias em profundidade” decorre do contraste entre a visibilidade urbana do monumento e a baixa legibilidade cotidiana (“as pessoas não sabem nem quem é um nem quem é outro”), ao mesmo tempo em que Caxias é discursivamente estabilizado como “O Pacificador” ligado à “manutenção da ordem interna e da unidade nacional”.[^3][^8]
- A lacuna “deuses fluviais no papel-moeda brasileiro” decorre do fato de que as fontes recuperadas sustentam com força o dinheiro como meio de circulação de intenções políticas (“por meio de textos ou imagens”), e oferecem exemplos de alegorias territoriais no reverso (p.ex., “Amazônia”), mas não documentam, neste recorte, um exemplar inequívoco de deus fluvial barbado com atributos clássicos; por isso, o patch formaliza regras negativas de não-inferência.[^9][^10]
- A lacuna “Panofsky/Hercules am Scheidewege” decorre de duas indicações simultâneas: a abordagem é apresentada como “method in application” e como enraizada na tradição warburguiana, mas o próprio texto também registra “starke Bedenken” contra nomeações automáticas, exigindo que o codebook trate o motivo como hipótese justificável e potencialmente contestável.[^6][^7]
- A evidência disponível, embora suficiente para verbetes, regras e exemplos mínimos, ainda não sustenta (neste piloto) a introdução de novos campos, pois as próprias fontes enfatizam a necessidade de leitura iconográfica e de rastreabilidade do suporte, mais do que a necessidade de ampliar o vocabulário estrutural do schema.[^1][^10]

## 2. Resumo do diff conceitual

A tabela abaixo sumariza, de modo “commitável”, os elementos documentais adicionados por este patch e a qual lacuna eles respondem, bem como a citação mínima que ancora cada elemento em evidência recuperada.[^3][^9][^6]

| Elemento | Tipo de mudanca | Lacuna que atende | Citacao chave |
|---|---|---|---|
| Subentrada “Caxias” em `Brazilian_Republican_Iconography` | Verbete de glossário | caxias | Baixa legibilidade pública do monumento (“não sabem nem quem é um…”).[^3] |
| Subentrada “Rios em moeda e selo” em `Brazilian_Republican_Iconography` | Verbete de glossário + regra negativa | river_gods_money | Dinheiro como circulação de intenções políticas (“textos ou imagens”; “intenções políticas do Estado”).[^9] |
| `Panofsky_Hercules_am_Scheidewege` | Verbete de glossário | panofsky_hercules | “Method in application” + “starke Bedenken” contra nomeação automática.[^6][^7] |
| `regras_reconhecimento_v231` | Regras transversais de reconhecimento | multiple | Codificação como leitura iconográfica para além do legado escrito + rastreabilidade por anotação de acervo (“Estatua de Caxias”).[^1][^2] |
| Três exemplos curtos de codificação | Exemplos de aplicação (sem alterar schema) | multiple | Organização por suporte e por faces (anverso/reverso) + núcleo semântico Virtus/Voluptas no bivium.[^10][^7] |

## 3. O que NAO muda em v2.3.1

Este patch não pretende alterar o regime de validação nem reclassificar registros já codificados; ele apenas melhora a documentação de reconhecimento a partir de evidências que indicam (a) a necessidade de distinguir leitura iconográfica de simples nomeação e (b) a necessidade de preservar rastreabilidade do suporte e das anotações de acervo.[^1][^2][^7]

- Nenhum campo novo é introduzido, pois as necessidades evidenciadas no piloto dizem respeito sobretudo a regras de inferência e a verbetes de referência (p.ex., “O Pacificador”, “mensagens” em moedas, “Virtus” e “Voluptas”), que podem ser operacionalizados em `notes`, `referencia_genealogica` e nos campos já existentes sem expandir o schema.[^8][^9][^7]
- Nenhum enum existente é alterado, pois a evidência recuperada se concentra em descrições e advertências de reconhecimento (anverso/reverso; contestabilidade da nomeação; baixa legibilidade pública), e não em insuficiências taxonômicas do conjunto de valores disponíveis.[^10][^7]
- Nenhuma regra de obrigatoriedade é alterada, porque a necessidade explicitada é tornar a interpretação auditável por fontes e por observáveis (por exemplo, “Estatua de Caxias” em anotação de acervo; divisão anverso/reverso em descrição de cédula), e isso pode ser satisfeito por treinamento e documentação.[^2][^10]
- A `codebook_version` em registros já codificados permanece “2.3.0”, pois este patch se restringe a documentação e exemplos de preenchimento que reforçam como ler e justificar decisões, especialmente quando a nomeação do motivo é reconhecidamente “tentadora” mas sujeita a objeções (“starke Bedenken”).[^7]
- Os arquivos `schema/codebook-v2.3.0.yaml` e `schema/codebook-v2.3.0.schema.json` permanecem como schema canônico, porque o alvo do patch é explicitar “method in application” (procedimento de leitura) e salvaguardas de inferência, não um redesenho formal do validador.[^6][^7]

## 4. Verbetes de glossario

Os verbetes abaixo são redigidos para serem colados diretamente no glossário de referências, com foco em: (i) nomear o núcleo semântico quando ele é explicitado por fonte; (ii) registrar regras negativas de não-inferência quando a evidência é insuficiente; e (iii) explicitar contestabilidade quando o próprio autor de referência a enuncia.[^8][^9][^7]

```yaml
glossario_referencias:
  Brazilian_Republican_Iconography:
    verbete: >
      Entrada guarda-chuva para programas estatais brasileiros em suportes de alta circulação
      (moedas/cédulas e monumentos), tratados como dispositivos de circulação de mensagens.
      As fontes indicam que o Estado veicula, nas moedas, intenções sobre políticas econômicas
      “por meio de textos ou imagens”, e que, ao fazê-las circular, faz circular também “as
      intenções políticas do Estado” por meio das mensagens nelas impressas.[^9]
      Em termos operacionais, isso exige rastrear onde a mensagem está localizada no suporte
      e como ela se organiza (por faces e por cenas), evitando inferir personificações
      específicas sem evidência visual suficiente.[^10]
    subentradas:
      - Caxias: >
          Caxias constitui um caso de monumentalização cívico-militar em que a função simbólica
          excede a mera comemoração: ele é descrito como “O Pacificador”, associado à “manutenção
          da ordem interna e da unidade nacional”, isto é, uma gramática de legitimação da ordem
          e da unidade como valores públicos.[^8]
          Ao mesmo tempo, há evidência de baixa legibilidade pública no presente, pois diante do
          monumento no espaço urbano “as pessoas não sabem nem quem é um nem quem é outro”.[^3]
          O verbete orienta o/a codificador/a a registrar separadamente (i) o enquadramento
          institucional pacificador e (ii) evidências de opacidade/baixa legibilidade cotidiana,
          quando disponíveis, sem pressupor reconhecimento automático como efeito necessário da
          monumentalização.[^3][^8]
      - "Rios em moeda e selo": >
          Programas monetários e filatélicos devem ser lidos como circuitos de circulação de
          mensagens estatais, uma vez que as fontes afirmam que os Estados veiculam em moedas
          suas intenções por “textos ou imagens” e que a circulação do dinheiro faz circular
          também as “intenções políticas do Estado”.[^9]
          Um exemplar descrito organiza o anverso como retrato e o reverso como cena alegórica
          territorial (por exemplo, “Amazônia” como riqueza natural e importância estratégica).[^10]
          Regra negativa: alegoria territorial/ambiental (p.ex., “Amazônia” ou fauna ameaçada)
          não equivale automaticamente a personificação hídrica; a categoria “deus fluvial” só
          deve ser aplicada quando houver sinais visuais inequívocos no próprio item. Lacuna na
          base de evidencia (busca neste piloto).[^10][^11]
      - "Genio do Brasil": >
          Ver também o adendo metodológico v2.3.0 (gramática masculina) para regras de
          reconhecimento do “gênio” como figura masculina de protetorado/heroísmo em programas
          estatais, especialmente quando há substituição atributiva (campo
          substituicao_atributiva_hercules).[^7]

  Panofsky_Hercules_am_Scheidewege:
    verbete: >
      Entrada para reconhecer o motivo “Hercules at the Crossroads” como programa de escolha
      moral e dispositivo pedagógico, não como Hercules genérico. A evidência caracteriza a
      abordagem como “method in application” e indica que o motivo está profundamente
      enraizado na tradição warburguiana, isto é, em uma genealogia de formas e sobrevivências.[^6]
      No núcleo semântico, o “Hercules Prodicius” aparece “zwischen ‘Virtus’ und ‘Voluptas’”,
      configurando a cena como escolha entre virtude e prazer.[^7]
      Cautela: a nomeação de imagens como “Hercules am Scheidewege” pode ser “verlockend”,
      mas o próprio texto registra que “starke Bedenken” podem se impor; portanto, quando a
      evidência visual for incompleta, registrar a identificação como hipótese e explicitar a
      justificativa da inferência em nota.[^7]

  Lubbock_Atlantes:
    nota_lacuna: "evidencia limitada neste piloto; manter como placeholder ate busca adicional"  # lacuna na base de evidencia (busca neste piloto)
```

## 5. Regras transversais de reconhecimento

As regras a seguir consolidam o que o piloto mostrou como risco de erro: (i) priorizar observáveis e rastreabilidade (anotações de acervo, descrição por faces) sobre rótulos; (ii) separar intenção institucional e recepção pública quando a fonte explicitamente aponta opacidade; e (iii) tratar a nomeação de motivos genealógicos como potencialmente contestável quando o próprio texto de referência registra objeções.[^3][^2][^10][^7]

```yaml
regras_reconhecimento_v231:
  - id: R1
    regra: "prioridade a marcas_corporais + objetos_regalia + marcadores_cena_arquitetura sobre atribuicao por inscricao"
    justificativa: >
      Estudos iconográficos são explicitamente apresentados como leitura de ícones/imagens que
      habilita interpretação “para além” do legado escrito; por isso, a codificação deve começar
      pelo que é observável no suporte e pelo que é rastreável, antes de estabilizar rótulos.[^1]

  - id: R2
    regra: "aplicar substituicao_atributiva_hercules quando atributos canonicos faltam mas a funcao narrativa do biviumo (escolha virtude/vicio) esta presente"
    justificativa: >
      O núcleo do motivo é a estrutura semântica “zwischen ‘Virtus’ und ‘Voluptas’”; logo, a
      presença do programa de escolha moral pode ser mais decisiva para reconhecimento do que a
      presença de um atributo isolado, desde que a inferência seja justificada e auditável.[^7]

  - id: R3
    regra: "regra de barba (reforcada): separar barba_longa generica (sabedoria/patriarca) de barba integrada a cena hidrica (Rio_barbado) por corpo_semirrecosto_fluvial + urna"
    justificativa: >
      A evidência monetária disponível neste piloto descreve cenas alegóricas territoriais (como
      “Amazônia”) sem nomear personificação hídrica; por isso, ‘rio’ só deve ser codificado quando
      houver evidência visual positiva, evitando que uma alegoria regional seja lida como deus fluvial.[^10]

  - id: R4
    regra: "marcar subaltern_caution: true quando rios brasileiros (Amazonas, Sao Francisco, Tiete) sao recontextualizados sob gramatica fluvial classica eurocentrica, sobrepondo-se a referenciais indigenas sobre os mesmos rios"
    justificativa: >
      As fontes descrevem programas monetários contemporâneos por temas ambientais (fauna ameaçada,
      sustentabilidade), o que evidencia a plasticidade temática do dinheiro; portanto, inferências
      sobre repertório clássico aplicado a rios brasileiros devem ser tratadas como interpretação
      situada e explicitadas com cautela subalterna quando houver risco de sobreposição cultural.[^11]

  - id: R5
    regra: "coder_position_statement substantivo (>= 100 chars) ao codificar monumento militar contestado discursivamente (Caxias e objeto de disputa historiografica recente)"
    justificativa: >
      O contraste entre monumentalização e baixa legibilidade pública (“as pessoas não sabem nem
      quem é um nem quem é outro”) exige registrar a posição interpretativa do/a codificador/a ao
      descrever o que está sendo tomado como evidência e o que está sendo inferido.[^3]

  - id: R6
    regra: "para itens com biviumo (escolha entre duas figuras femininas/alegoricas), preencher funcao_da_figura_masculina: mediacao_pedagogica e marcar indicador moralizacao como aplicavel"
    justificativa: >
      A formulação “zwischen ‘Virtus’ und ‘Voluptas’” explicita que o motivo é um programa de
      pedagogia moral (escolha), o que autoriza tratá-lo como mediação pedagógica e como eixo de
      moralização no regime alegórico.[^7]

  - id: R7
    regra: "monumentos equestres masculinos em pracas civicas (Caxias, bandeirantes) codificar com funcao_juridica: monumento_publico (ou monumento_contestado quando ha intervencao registrada) e familia_alegorica: Masculino_Juridico, subtipo Heroi_civil ou outro_masculino"
    justificativa: >
      O enquadramento institucional de Caxias como “O Pacificador” vincula a figura à manutenção
      de ordem e unidade, o que sustenta a leitura do monumento como dispositivo cívico-estatal,
      mesmo quando a recepção cotidiana seja opaca; isso justifica o tratamento do item como
      monumento público com gramática masculina de heroísmo/ordem.[^8][^3]
```

## 6. Exemplos de codificacao

Os três exemplos abaixo são propositadamente curtos e mostram apenas os campos analiticamente relevantes, porque a própria evidência recuperada enfatiza (a) rastreabilidade do suporte e (b) cautela com nomeações “tentadoras” e com inferências sem evidência visual positiva.[^2][^10][^7]

### 6.1 Caxias

```yaml
codebook_version: "2.3.0"  # schema inalterado; patch 2.3.1 e documentacao
familia_alegorica: Masculino_Juridico
subtipo: Heroi_civil
funcao_da_figura_masculina: heroismo_civil
tipo_agencia_masculina: protetorado
funcao_juridica: monumento_publico
referencia_genealogica:
  - Brazilian_Republican_Iconography

# Evidencia e justificativas
justificativa_genero: >
  A fonte enquadra Caxias como figura de ordem e unidade nacional ("O Pacificador"), o que
  sustenta o reconhecimento como heroi civico-militar em programa estatal; a codificacao
  nao presume reconhecimento automatico no presente.[^8][^3]

coder_position_statement: >
  Estou codificando a funcao do monumento a partir de evidencia textual institucional ("O Pacificador")
  e registro a tensao com a baixa legibilidade publica relatada ("as pessoas nao sabem...") para
  evitar colapsar intencao estatal e recepcao cotidiana.[^8][^3]
```

### 6.2 Deus fluvial em cédula ou selo

```yaml
codebook_version: "2.3.0"  # schema inalterado; patch 2.3.1 e documentacao
# caso generico ilustrativo; lacuna na base de evidencia (busca neste piloto)[^10]

familia_alegorica: Masculino_Juridico
subtipo: Rio_barbado
funcao_da_figura_masculina: soberania_territorial
funcao_juridica: moeda_cedula
vetor_colonial: republicano_brasileiro

objetos_regalia:
  - urna_vertedora
  - vaso_fluvial
marcas_corporais:
  - barba_longa
  - corpo_semirrecosto_fluvial

tipo_efluencia_hidrica: urna_vertedora

relacao_com_repertorio_indigena: ausente
subaltern_caution: >
  Marcado por cautela: neste piloto, as fontes descrevem cenas territoriais ("Amazonia") e
  programas ambientais (fauna/sustentabilidade), mas nao documentam um exemplar inequívoco
  de deus fluvial; evitar inferencia eurocentrica sem evidencia visual positiva.[^10][^11]

justificativa_genero: >
  A atribuicao de genero masculino para rio/deus fluvial exige evidencia visual positiva (p.ex.
  barba + postura fluvial classica + urna/vaso), o que deve ser confirmado no item primario; aqui
  permanece como exemplo de preenchimento, nao como achado empirico do piloto.[^10]
```

### 6.3 Hercules am Scheidewege

```yaml
codebook_version: "2.3.0"  # schema inalterado; patch 2.3.1 e documentacao
familia_alegorica: Masculino_Juridico
subtipo: Hercules
funcao_da_figura_masculina: mediacao_pedagogica
referencia_genealogica:
  - Panofsky_Hercules_am_Scheidewege

# objetos_regalia pode variar; o reconhecimento se ancora no programa (Virtus vs Voluptas)
objetos_regalia:
  - leao_pele

substituicao_atributiva_hercules:
  atributo_canonico_substituido: "clava"
  atributo_novo: "(ausente ou substituido no suporte)"
  justificativa: >
    O reconhecimento privilegia o programa de escolha moral (Hercules entre Virtus e Voluptas)
    e registra cautela porque o proprio texto observa que nomear automaticamente pode ser
    "verlockend" mas suscita "starke Bedenken" quando a evidencia e incompleta.[^7]

indicadores_purificacao:
  moralizacao: 3  # aplicavel quando a cena explicita escolha moral (bivium)[^7]
```

## 7. Lacunas que permanecem apos este patch

Mesmo após a busca focada, permanecem lacunas que precisam ser explicitadas para evitar que o glossário e as regras sejam lidos como fechamento do problema, especialmente porque a evidência recuperada inclui (i) baixa legibilidade pública e (ii) advertência de contestabilidade na nomeação de motivos, o que recomenda prudência antes de qualquer freeze forte.[^3][^7]

- Detalhamento iconográfico do monumento de Caxias (modalidade equestre, fardamento, inscrições de pedestal, programa em baixo-relevos): lacuna na base de evidencia (busca neste piloto).[^2]
- Identificação de exemplares específicos do papel-moeda brasileiro em que rios apareçam como deuses fluviais barbados com atributos clássicos inequívocos: lacuna na base de evidencia (busca neste piloto).[^10]
- Consolidação de fonte bibliográfica de referência para atlantes/telamones (entrada Lubbock): lacuna na base de evidencia (busca neste piloto).[^6]
- Série/década e catálogo sistemático para comparar programas monetários por anverso/reverso em longa duração: lacuna na base de evidencia (busca neste piloto).[^10][^11]
- Estudos específicos que articulem, no espaço público brasileiro, a distância entre intenção institucional e legibilidade cotidiana de monumentos (problema indicado por “as pessoas não sabem…”): lacuna na base de evidencia (busca neste piloto).[^3]

## 8. Entrada para CHANGELOG.md

```markdown
| 2.3.1 | <data> | Adendo de lacunas (documentacao apenas): verbetes de Caxias, deuses fluviais em moeda/selo e Panofsky-Hercules-am-Scheidewege; regras transversais de reconhecimento; exemplos de codificacao. Sem novos campos. | Nao |
```

A descrição desta entrada enfatiza que as mudanças são de reconhecimento e rastreabilidade (por exemplo, distinção entre enquadramento institucional de “O Pacificador” e baixa legibilidade pública, e cautela contra nomeação automática com “starke Bedenken”), porque são esses os pontos explicitamente sustentados pela evidência recuperada.[^3][^8][^7]

## 9. Plano de aplicacao

A aplicação deste patch é deliberadamente conservadora e orientada à auditabilidade, porque as fontes indicam, de um lado, funções simbólicas fortes (pacificação/ordem; circulação de intenções estatais em moedas) e, de outro, riscos de opacidade pública e de contestabilidade de rótulos, exigindo que o treinamento enfatize justificativas e evidências em cada registro.[^8][^9][^3][^7]

- Este patch deve ser incorporado como documentação (glossário + regras + exemplos) para orientar codificação em casos-limite e reduzir inferências indevidas, especialmente em dinheiro (anverso/reverso; tema territorial/ambiental) e em motivos genealógicos (bivium Virtus/Voluptas).[^10][^11][^7]
- Recomenda-se usar as citações como material de treinamento: Caxias como “O Pacificador” e a evidência de baixa legibilidade pública; moedas como circulação de intenções políticas; Panofsky como método aplicado e cautela de nomeação.[^8][^3][^9][^6][^7]
- Não se requer recodificação do corpus já anotado; o efeito esperado é aumentar consistência interpretativa e rastreabilidade documental, sobretudo quando houver anotação de acervo que nomeie o referente (“Estatua de Caxias”).[^2]
- O piloto deve continuar a orientar buscas adicionais para (i) exemplares monetários com personificação fluvial inequívoca e (ii) estudos iconográficos detalhados do monumento de Caxias, dado que a base atual privilegia descrições gerais e regras negativas de não-inferência.[^10][^3]
- Após incorporar este patch, atualizar `CHANGELOG.md` com a linha da seção 8 e vincular, no repositório, o presente patch ao documento justificativo `schema/adendo-lacunas-v2.3.1.md` para manter rastreabilidade da decisão interpretativa enquanto capta.[^1][^6]


[^1]: Bittencourt, 2016. Iconografia Numismática: os dobrões de ouro cunhados na casa da moeda de Vila Rica, Minas Gerais (1724-1727).

[^2]: Acervo IMS : Documento/obra : Monumento em homenagem a Duque de Caxias; ao fundo, a Igreja de Nossa Senhora da Glória do Outeiro [007_IMG_3906.jpg].

[^3]: Ribeiro, 2006. Tradição, nacionalismo e modernidade: o monumento Duque de Caxias.

[^4]: Rodrigues & Maciel, 2019. Pacificação à brasileira? O paradigma de Caxias e os militares no governo de Jair Bolsonaro.

[^5]: Ribeiro, 2005. A unidade dos projetos estético e ideológico e a potencialidade do monumento no espaço urbano: o caso do monumento às Bandeiras e do monumento Duque de Caxias. Atas do ...

[^6]: Wuttke, 2007. Panofsky et Warburg. L'"Hercule à la croisée des chemins" d'Erwin Panofsky: L'ouvrage et son importance pour l'histoire des sciences de l'art.

[^7]: Panofsky, Erwin <Prof. Dr.>: Hercules am Scheidewege und andere antike Bildstoffe in der neueren Kunst (Studien der Bibliothek Warburg, Leipzig ,  Berlin, 1930).

[^8]: Duque de Caxias: o Pacificador e Patrono do Exército Brasileiro - Blog do Exército Brasileiro.

[^9]: Amaral, 2024. Dinheiro na mão é vendaval e moeda no lixo é bom sinal: elementos do cotidiano e representações de intenções políticas do Estado brasileiro na cunhagem de moedas metálicas entre 1969 e 1978. Revista de arqueología.

[^10]: Cédula 5 Cruzeiros (Cr$5) – Barão do Rio Branco - AUTOGRAFADA - 1ª Estampa - Numismatica Nordeste, 2025.

[^11]: Continente. Iconografia do papel-moeda brasileiro - Revista Continente.