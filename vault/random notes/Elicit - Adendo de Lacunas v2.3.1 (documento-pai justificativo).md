---
documento: adendo-lacunas
versao_alvo_codebook: 2.3.1
data: (preencher)
status: rascunho_para_revisao
autor: (preencher)
documento_pai: schema/codebook-v2.3.0.yaml
companheiros:
  - schema/codebook-v2.3.1-patch.md
---

# Adendo de lacunas v2.3.1 — Caxias, deuses fluviais no dinheiro e Panofsky/Hercules am Scheidewege

## 1. Escopo do adendo

Este documento é um patch de documentação para a versão v2.3.1: ele não altera o schema nem introduz campos novos, mas consolida três lacunas declaradas como críticas na expansão da gramática masculina do corpus (Caxias; deuses fluviais no dinheiro; e o motivo panofskyano de Hercules na encruzilhada).[^1][^2][^3][^4][^5]

O adendo cumpre três funções operacionais: (i) fornecer verbetes de glossário que ancorem o reconhecimento genealógico e o vocabulário mínimo de descrição; (ii) explicitar regras de reconhecimento iconográfico baseadas no que é observável no suporte e no contexto de circulação; e (iii) oferecer exemplos de codificação em YAML (ilustrativos) que indiquem como registrar o item sem “inflacionar” a interpretação para além da evidência disponível.[^6][^3][^7][^5]

Por fim, o adendo registra de forma explícita o que permanece insuficientemente coberto. Em particular, a base aqui recuperada traz indícios fortes para a função político-simbólica do monumento e do dinheiro como suportes de circulação de mensagens estatais, mas não traz, com a mesma granularidade, descrições iconográficas minuciosas (por exemplo, detalhes de fardamento, postura equestre, ou atributos clássicos completos de deus fluvial em cédulas específicas).[^8][^3][^7]

## 2. Lacuna 1 — Duque de Caxias

### 2.1 Sintese

A evidência recuperada estabelece dois pontos simultâneos: (a) o monumento/estátua de Caxias opera como dispositivo urbano de visibilidade pública (um marco em praça/avenida), mas sua legibilidade cotidiana pode ser baixa; e (b) a figura é enquadrada institucional e discursivamente como agente de “pacificação” e manutenção de ordem, com vocação a sustentar legitimidade estatal e militar no tempo.[^1][^2][^9][^10]

Quanto à legibilidade pública, a formulação “as pessoas não sabem nem quem é um nem quem é outro” quando atravessam o entorno do monumento indica que o reconhecimento do referente histórico (Caxias) e do dispositivo urbano (praça/monumento) não é automático nem estável, mesmo quando o programa está fisicamente instalado e exposto.[^1]

Quanto à gramática de pacificação, o enquadramento “Caxias é conhecido como ‘O Pacificador’” é explicitamente articulado à “manutenção da ordem interna e da unidade nacional”, e a mesma chave é reiterada como perfil de atuação no Segundo Império que “lhe valeu o título de ‘O Pacificador’”.[^2][^9]

### 2.2 Regras de reconhecimento iconografico

As regras abaixo são formuladas para maximizar rastreabilidade e minimizar inferência. Elas devem ser aplicadas priorizando evidência visual e evidência de acervo (metadados, anotações), antes de interpretações narrativas mais ambiciosas.[^6][^8]

1) **Âncora de identificação por evidência de acervo**. Quando houver documentação arquivística que nomeie diretamente o referente (por exemplo, anotações do próprio acervo indicando “Estatua de Caxias”), a identificação do item pode ser registrada como “Caxias” sem depender de reconhecimento facial ou de leitura do pedestal no local, desde que a fonte seja preservada no registro (link e/ou referência do acervo).[^8]

2) **Âncora de reconhecimento por situação urbana**. Quando o item for descrito em relação a sua situação urbana (travessia, praça, avenida), registrar o fato de que a visibilidade pública é alta, mas a legibilidade pode ser baixa, uma vez que o testemunho indica desconhecimento do público no entorno imediato do monumento.[^1]

3) **Âncora semântica por epíteto institucional**. Quando o item for Caxias e houver, no suporte ou em documentação de apoio, a associação explícita a “O Pacificador” e à “manutenção da ordem interna e da unidade nacional”, registrar essa associação como núcleo semântico do programa iconográfico (Caxias como figura de ordem/pacificação), evitando reduzir o item a “herói militar genérico”.[^2][^9]

4) **Distinção entre intenção institucional e recepção pública**. Não colapsar, no registro, o epíteto institucional (“O Pacificador”) com a recepção cotidiana (“as pessoas não sabem…”). Tratar esses dois planos como dimensões distinguíveis: intenção de inculcação/legitimação versus reconhecimento efetivo no espaço público.[^1][^2]

5) **Cautela sobre detalhes iconográficos específicos**. As fontes aqui recuperadas não descrevem se o monumento é equestre, nem detalham fardamento, postura de comando, ou inscrições de pedestal; portanto, tais marcas só devem ser registradas quando a imagem primária ou documentação específica as suportar. Quando não suportar, registrar explicitamente como “lacuna na base de evidência (busca neste piloto)”.[^8]

### 2.3 Verbete de glossario

A seguir, um bloco curto, pronto para colar como subentrada no verbete mais amplo de iconografia republicana brasileira, com foco na figura de Caxias.

**Brazilian_Republican_Iconography (subentrada Caxias)** — Caxias constitui um caso de monumentalização cívico-militar em que a função simbólica do dispositivo não se reduz à comemoração: a figura é instituída como “O Pacificador”, associada à “manutenção da ordem interna e da unidade nacional”, oferecendo uma gramática de legitimação da ordem e da unidade como valores públicos.[^2][^9] Ao mesmo tempo, a recepção cotidiana pode permanecer opaca, pois há testemunho de que, diante do monumento no espaço urbano, “as pessoas não sabem nem quem é um nem quem é outro”.[^1] O verbete deve, portanto, orientar o/a codificador/a a registrar separadamente (i) o enquadramento institucional de pacificação/ordem e (ii) evidências de baixa legibilidade pública, quando disponíveis, em vez de pressupor reconhecimento automático como efeito necessário da monumentalização.[^1][^2]

### 2.4 Exemplo de codificacao

O exemplo abaixo é ilustrativo e deve ser adaptado ao schema vigente. Ele demonstra como manter rastreabilidade (fonte de acervo) e como explicitar a tensão entre pacificação/ordem e baixa legibilidade pública, sem inferir detalhes não documentados.[^1][^2][^8]

```yaml
item_id: LPAI-0000  # placeholder
titulo: "Estatua de Caxias (registro de acervo / programa cívico-militar)"  # nomeado no acervo[^8]
suporte: "fotografia (negativo em vidro)"  # suporte indicado pelo acervo[^8]
data_suporte: "(preencher)"
instituicao_origem: "(preencher)"
localizacao_atual: "(preencher)"
fonte_imagem: "https://acervos.ims.com.br/index.php/Detail/objects/198795"  # anotação menciona 'Estatua de Caxias'[^8]

# Campos analíticos (nomes conforme schema v2.3.0; preencher de modo capta-auditável)
notes: >
  O acervo registra explicitamente 'Estatua de Caxias'. Há evidência de baixa legibilidade pública
  no entorno urbano do monumento ('as pessoas não sabem nem quem é um nem quem é outro'),
  o que deve ser tratado como dimensão distinta do enquadramento institucional de Caxias como
  'O Pacificador' (ordem interna/unidade nacional).[^1][^2][^8]

# Campos cujo preenchimento depende de imagem primária detalhada
# (por exemplo: se é equestre, detalhes de fardamento, inscrições) -> lacuna na base de evidência[^8]
```

## 3. Lacuna 2 — Deuses fluviais no papel-moeda brasileiro

### 3.1 Sintese

A base recuperada fornece uma justificativa forte para tratar moeda e cédula como suportes de circulação de “intenções políticas do Estado”, veiculadas “por meio de textos ou imagens”, e cuja circulação pelo uso do dinheiro faz circular as mensagens políticas junto com a materialidade monetária.[^3]

Ela também oferece uma regra estrutural importante para o reconhecimento iconográfico em dinheiro: a hierarquia visual por faces (anverso/reverso). Em um exemplo concreto, o anverso traz o retrato do Barão do Rio Branco e o reverso apresenta “uma imponente cena alegórica da Amazônia”, com ênfase em “riqueza natural” e “importância estratégica” da região.[^7]

Ao mesmo tempo, a evidência disponível aqui não documenta, de forma direta, um exemplar em que um rio brasileiro apareça personificado como deus fluvial barbado (com atributos clássicos inequívocos), de modo que o adendo registra uma lacuna: por ora, há evidência de alegoria territorial (“Amazônia”) no reverso, mas não de “deus fluvial” específico.[^7]

Por fim, há indicação de que repertórios mitológicos clássicos aparecem como referência em descrições sobre iconografia monetária (“deusas da mitologia grega”), o que mantém aberta (mas ainda não provada neste recorte) a hipótese de transferências iconográficas clássicas em programas monetários brasileiros.[^11]

### 3.2 Regras de reconhecimento

As regras abaixo visam prevenir um erro recorrente: confundir alegoria territorial/ambiental (Amazônia, fauna, “sustentabilidade”) com personificação hídrica (rio/oceano como figura).[^7][^12]

1) **Regra do suporte como mensageiro estatal**. Tratar a presença de imagens em moedas/cédulas como veículo de mensagens estatais, pois as fontes afirmam que o Estado “veicula nas moedas suas intenções” e que, ao fazê-las circular, “fazemos as intenções políticas do Estado circularem”.[^3]

2) **Regra anverso versus reverso**. Registrar separadamente o programa do anverso (por exemplo, retrato/efígie) e o programa do reverso (tema alegórico), uma vez que a própria descrição organiza a leitura por “anverso” e “reverso” e localiza a alegoria territorial (“Amazônia”) no reverso.[^7]

3) **Regra de não-inferência de deus fluvial**. Não codificar “deus fluvial” apenas porque há uma cena alegórica territorial (como “Amazônia”), já que a descrição disponível qualifica a cena como alegoria da região e de sua riqueza/estratégia, sem nomear nem descrever personificação hídrica.[^7]

4) **Regra de tema ambiental contemporâneo**. Distinguir programas contemporâneos de temática ambiental (fauna ameaçada, “viés da sustentabilidade”) de personificações clássicas; quando houver fauna como tema principal do verso, registrar como programa ambiental, não como alegoria hídrica por default.[^12]

5) **Regra de rastreabilidade do exemplar**. Quando o item for cédula, registrar o exemplar por sua descrição faceada (anverso/reverso) e manter o vínculo com a fonte de descrição, para que a interpretação permaneça auditável (por exemplo, “Amazônia no reverso”).[^7]

### 3.3 Verbete de glossario

**Brazilian_Republican_Iconography (subentrada rios em moedas cédulas selos)** — Programas monetários e filatélicos devem ser tratados como dispositivos de circulação de mensagens estatais: as fontes indicam que o Estado “veicula nas moedas suas intenções” por textos e imagens e que, ao fazê-las circular, “fazemos as intenções políticas do Estado circularem” junto com as “mensagens nelas impressas”.[^3] No nível iconográfico, a leitura deve respeitar a hierarquia do suporte (anverso/reverso), pois um exemplar descrito organiza o anverso como retrato (Barão do Rio Branco) e o reverso como cena alegórica (Amazônia, riqueza natural e importância estratégica).[^7] O verbete deve incluir uma regra negativa: alegoria territorial/ambiental não equivale automaticamente a personificação hídrica; a categoria “deus fluvial” só deve ser aplicada quando houver sinais visuais inequívocos de personificação de rio/oceano no próprio item (lacuna na base de evidência neste piloto).[^7]

### 3.4 Exemplo de codificacao

Como a evidência não traz um exemplar específico de “deus fluvial barbado” em cédula brasileira, o exemplo abaixo é explicitamente genérico e serve apenas para demonstrar como registrar (i) a estrutura anverso/reverso e (ii) a regra negativa que impede inferência de personificação hídrica quando a descrição é territorial/estratégica (Amazônia).[^7]

```yaml
item_id: LPAI-0001  # placeholder
titulo: "Cédula com retrato no anverso e alegoria territorial no reverso (ex.: Amazônia)"[^7]
suporte: "cédula"  # suporte monetário[^3]
data_suporte: "(preencher)"
fonte_imagem: "https://numismaticanordeste.com.br/product/cedula-5-cruzeiros-cr5-barao-do-rio-branco-autografada-1a-estampa/"[^7]

notes: >
  A descrição separa anverso (retrato do Barão do Rio Branco) e reverso (cena alegórica da Amazônia).
  Este registro NÃO infere personificação hídrica/deus fluvial, pois a fonte caracteriza a cena como
  alegoria territorial (riqueza natural e importância estratégica) sem indicar atributos clássicos de
  deus fluvial. 'Deus fluvial no papel-moeda' permanece lacuna na base de evidência (busca neste piloto).[^7]
```

## 4. Lacuna 3 — Panofsky e Hercules am Scheidewege

### 4.1 Sintese

A evidência recuperada situa a leitura de Panofsky sobre “Hercules at the Crossroads” como um exercício metodológico que explicita “method in application” e destaca a inserção do motivo na tradição warburguiana.[^4]

No nível iconográfico-semântico, a própria formulação “Hercules Prodicius … zwischen ‘Virtus’ und ‘Voluptas’” torna explícito o núcleo alegórico da cena como escolha entre Virtude e Voluptuosidade (prazer), isto é, um programa pedagógico de decisão moral, e não apenas a presença de um herói mitológico isolado.[^5]

A evidência também alerta para uma cautela de nomeação: é “tentador” chamar um pequeno quadro de “Hercules am Scheidewege”, mas “starke Bedenken” podem se impor contra essa solução, o que implica que a própria identificação do motivo pode ser controversa e deve ser tratada como capta auditável (com indicação de incerteza quando necessário).[^5]

### 4.2 Regras de reconhecimento

As regras abaixo são formuladas para reduzir o risco de “Hercules genérico” e para preservar o caráter metodológico (não meramente taxonômico) da entrada panofskyana no repertório.[^4][^5]

1) **Regra do programa de escolha**. Só reconhecer “Hercules am Scheidewege” quando a cena sustentar a estrutura mínima de escolha moral, explicitada como estar “entre ‘Virtus’ e ‘Voluptas’”.[^5]

2) **Regra da cautela de nomeação**. Quando a identificação do motivo for inferida com base em semelhanças formais frágeis, registrar a identificação como hipótese e explicitar que a própria nomeação pode ser “tentadora”, mas sujeita a “fortes objeções”.[^5]

3) **Regra do método como evidência**. Tratar o uso de Panofsky não como “autoridade para rotular”, mas como modelo de “method in application”, isto é, um procedimento de leitura genealógica; quando o motivo aparecer em suportes estatais/jurídicos brasileiros, registrar quais elementos do programa (escolha, pedagogia, encenação) estão efetivamente presentes no item e quais dependem de mediações textuais externas.[^4]

4) **Regra da linhagem warburguiana**. Quando a codificação reivindicar a chave “Hercules at the Crossroads”, registrar (em nota ou justificativa) que o motivo está “profundamente enraizado” na tradição de Warburg, para tornar explícito que se trata de uma genealogia de formas (sobrevivências e transferências) e não de uma semelhança atemporal.[^4]

### 4.3 Verbete de glossario

**Panofsky_Hercules_am_Scheidewege** — Entrada para reconhecer o motivo “Hercules at the Crossroads” como programa alegórico de escolha moral e método de leitura. A evidência recuperada descreve a abordagem como “method in application” e aponta que o motivo está “profundamente enraizado” na tradição warburguiana, isto é, em uma genealogia de formas e de sobrevivências iconográficas.[^4] No núcleo semântico, o “Hercules Prodicius” é explicitado como estando “entre ‘Virtus’ e ‘Voluptas’”, configurando a cena como dispositivo pedagógico de discernimento (virtude versus prazer).[^5] O verbete deve incluir cautela de atribuição: é “tentador” nomear imagens como “Hercules am Scheidewege”, mas o próprio texto registra que “fortes objeções” podem se impor, recomendando que a identificação seja tratada como hipótese quando a evidência visual for incompleta.[^5]

### 4.4 Implicacao para o codebook

A implicação direta para a codificação de programas estatais/jurídicos é que “Hercules am Scheidewege” deve ser tratado como cena de escolha moral (Virtus versus Voluptas) e, portanto, como alegoria de pedagogia normativa, em vez de “Hercules” como simples marca de força ou heroísmo.[^5] Dado que a tradição é apresentada como warburguiana e orientada por “method in application”, a codificação deve privilegiar o registro do que está efetivamente presente no suporte (configuração de escolha) e explicitar quando o reconhecimento depende de inferência e pode ser contestado (“starke Bedenken”).[^4][^5]

## 5. Regras transversais

As regras abaixo consolidam as três lacunas em um conjunto de cautelas operacionais voltadas a rastreabilidade e auditabilidade, sobretudo quando se codifica um item como programa (monumento; dinheiro) com alta carga político-simbólica.[^6][^3]

1) **Priorizar observáveis sobre rótulos**. Antes de aplicar um rótulo forte (por exemplo, “O Pacificador” como núcleo semântico; “Hercules am Scheidewege” como motivo), registrar a evidência explícita que sustenta o rótulo (citação textual ou anotação de acervo).[^2][^8][^5]

2) **Separar intenção institucional e recepção pública**. Quando houver evidência simultânea de enquadramento institucional e de baixa legibilidade pública, manter ambos no registro sem forçar coerência: “Caxias é conhecido como ‘O Pacificador’” pode coexistir com “as pessoas não sabem…”.[^1][^2]

3) **Regra do suporte como circuito**. Tratar dinheiro como circuito de circulação de intenções estatais, dado que a fonte explicita que a circulação das moedas faz circular as “intenções políticas do Estado” e suas “mensagens”.[^3]

4) **Regra de faceamento em dinheiro**. Em cédulas e moedas, registrar a organização por anverso/reverso, pois o suporte (e a descrição disponível) distribui hierarquicamente retrato e cena alegórica entre faces, e isso condiciona a leitura do programa iconográfico como conjunto.[^7]

5) **Regra de não-inferência de personificação hídrica**. Não inferir “deus fluvial” sem evidência, mesmo quando o tema seja territorial/ambiental (“Amazônia”, fauna ameaçada), pois as descrições disponíveis não estabelecem personificação hídrica específica neste recorte.[^7][^12]

6) **Regra de contestabilidade do motivo**. Quando uma identificação genealógica é reconhecidamente controversa, registrar isso como parte do próprio achado: a nomeação de “Hercules am Scheidewege” pode ser “tentadora”, mas sujeita a “fortes objeções”.[^5]

7) **Regra de rastreabilidade de acervo**. Quando o item estiver ancorado em um registro de acervo, preservar no registro o suporte e as anotações (por exemplo, “Suporte Negativo - Vidro” e a listagem “Estatua de Caxias”), para permitir comparação e verificação sem depender exclusivamente de narrativa secundária.[^8]

## 6. Atualizacoes do glossario_referencias

O bloco abaixo está pronto para colagem no arquivo de glossário em formato YAML, mantendo as entradas concisas e orientadas por regras de reconhecimento e cautela.

```yaml
Brazilian_republican_iconography: >
  Entrada guarda-chuva para programas estatais brasileiros em suportes de alta circulação
  (monumentos públicos e dinheiro), tratados como dispositivos de circulação de mensagens
  políticas. As fontes indicam que, ao veicular “intenções” em moedas por “textos ou imagens”,
  o Estado expõe mensagens e, ao fazer as moedas circularem, faz circular também suas intenções
  políticas por meio dessas mensagens.[^3]
  Subentrada Caxias: a figura é enquadrada como “O Pacificador”, ligada à manutenção da ordem
  interna e da unidade nacional, mas a legibilidade pública pode ser baixa no entorno do
  monumento (“as pessoas não sabem…”).[^2][^1]
  Subentrada dinheiro: recomenda-se leitura por faces (anverso/reverso), pois um exemplar
  descreve anverso como retrato (Barão do Rio Branco) e reverso como cena alegórica territorial
  (Amazônia).[^7]

Panofsky_hercules_am_scheidewege: >
  Entrada para o motivo “Hercules at the Crossroads” como programa de escolha moral e
  dispositivo pedagógico. A evidência recuperada caracteriza a abordagem como “method in
  application” e afirma que o motivo é profundamente enraizado na tradição de Warburg.[^4]
  No núcleo semântico, o “Hercules Prodicius” aparece entre “Virtus” e “Voluptas”, o que
  orienta o reconhecimento como cena de escolha (virtude versus prazer) em vez de Hercules
  genérico.[^5]
  Incluir cautela: a nomeação pode ser tentadora, mas há “fortes objeções”, de modo que a
  identificação deve ser registrada como hipótese quando a evidência visual for incompleta.[^5]

Lubbock_atlantes: >
  Placeholder mantido. Lacuna na base de evidência (busca neste piloto).[^4]
```

## 7. Lacunas que permanecem

Mesmo após a busca focada, permanecem lacunas que devem ser explicitamente tratadas como pendências de pesquisa antes de qualquer freeze que pretenda estabilizar regras de reconhecimento fino para a gramática masculina.[^8][^7][^5]

- Detalhamento iconográfico do monumento de Caxias (por exemplo, modalidade equestre, fardamento, inscrições de pedestal e programa em baixo-relevos): lacuna na base de evidência (busca neste piloto).[^8]
- Identificação de exemplares específicos do papel-moeda brasileiro em que rios apareçam como deuses fluviais barbados com atributos clássicos inequívocos (por exemplo, figura reclinada e vaso vertente): lacuna na base de evidência (busca neste piloto).[^7]
- Consolidação de fonte bibliográfica de referência para “atlantes/telamones” (entrada Lubbock): lacuna na base de evidência (busca neste piloto).[^4]
- Série/decênio e catálogo sistemático para comparar programas monetários por anverso/reverso em longa duração: lacuna na base de evidência (busca neste piloto).[^7][^12]
- Estudos específicos que articulem, no espaço público brasileiro, a distância entre intenção institucional e legibilidade cotidiana de monumentos (problema indicado pelo testemunho “as pessoas não sabem…”): lacuna na base de evidência (busca neste piloto).[^1]

## 8. Entrada para CHANGELOG.md

`2.3.1 | <data> | Adendo de lacunas: verbetes e regras de reconhecimento para Caxias, deuses fluviais em moeda/selo, e Panofsky-Hercules; sem novos campos. | Nao`[^1][^3][^4][^5]

## 9. Plano de aplicacao

A aplicação deste patch é deliberadamente conservadora e orientada à auditabilidade, dado que as fontes recuperadas combinam afirmações institucionais fortes e indícios de baixa legibilidade pública, além de alertas explícitos de contestabilidade de nomeação (Panofsky).[^1][^2][^5]

- v2.3.1 é patch apenas de documentação e glossário, sem novos campos ou migrações de schema.[^4]
- Os achados substantivos recuperados aqui devem ser incorporados como base citável para treinamento de codificação e para justificativas de reconhecimento (Caxias como “O Pacificador”; dinheiro como circulação de intenções; Panofsky como “method in application”).[^2][^3][^4]
- Recodificação do corpus não é requerida por este adendo; o efeito esperado é reduzir inferências indevidas e aumentar rastreabilidade (por exemplo, anotações de acervo e faceamento anverso/reverso).[^8][^7]
- O piloto deve continuar marcado como pre-freeze, e as lacunas listadas acima devem orientar a próxima rodada de busca dirigida (em especial, exemplares monetários com personificação fluvial inequívoca e estudos iconográficos detalhados do monumento de Caxias).[^8][^7]


[^1]: Ribeiro, 2006. Tradição, nacionalismo e modernidade: o monumento Duque de Caxias.

[^2]: Duque de Caxias: o Pacificador e Patrono do Exército Brasileiro - Blog do Exército Brasileiro.

[^3]: Amaral, 2024. Dinheiro na mão é vendaval e moeda no lixo é bom sinal: elementos do cotidiano e representações de intenções políticas do Estado brasileiro na cunhagem de moedas metálicas entre 1969 e 1978. Revista de arqueología.

[^4]: Wuttke, 2007. Panofsky et Warburg. L'"Hercule à la croisée des chemins" d'Erwin Panofsky: L'ouvrage et son importance pour l'histoire des sciences de l'art.

[^5]: Panofsky, Erwin <Prof. Dr.>: Hercules am Scheidewege und andere antike Bildstoffe in der neueren Kunst (Studien der Bibliothek Warburg, Leipzig ,  Berlin, 1930).

[^6]: Bittencourt, 2016. Iconografia Numismática: os dobrões de ouro cunhados na casa da moeda de Vila Rica, Minas Gerais (1724-1727).

[^7]: Cédula 5 Cruzeiros (Cr$5) – Barão do Rio Branco - AUTOGRAFADA - 1ª Estampa - Numismatica Nordeste, 2025.

[^8]: Acervo IMS : Documento/obra : Monumento em homenagem a Duque de Caxias; ao fundo, a Igreja de Nossa Senhora da Glória do Outeiro [007_IMG_3906.jpg].

[^9]: Rodrigues & Maciel, 2019. Pacificação à brasileira? O paradigma de Caxias e os militares no governo de Jair Bolsonaro.

[^10]: Rodrigues & Maciel, 2019. Pacificação à brasileira? O paradigma de Caxias e os militares no governo de Jair Bolsonaro.

[^11]: Continente. Iconografia do papel-moeda brasileiro.

[^12]: Continente. Iconografia do papel-moeda brasileiro - Revista Continente.