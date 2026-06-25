---
documento: adendo-metodologico
versao_alvo_codebook: 2.3.0
data: "2026-06-25"
status: rascunho_para_revisao_pre_freeze
autor: "Ana Vanzin (consolidacao a partir do rascunho Elicit)"
documento_pai: schema/codebook-v2.2.0.yaml
documento_pai_editorial: schema/codebook-MASTER.md
companheiros:
  - schema/codebook-v2.3.0-patch.md
  - schema/codebook-v2.3.0.md
origem_externa:
  fonte: "Elicit - Adendo Metodologico v2.3.0 (Gramatica Masculina)"
  data_importacao: "2026-06-25"
  observacao: "Rascunho Elicit convertido de snake_case para PascalCase para casar com o master v2.2.0. Substantivo preservado; apenas enums e chaves normalizadas."
freeze_gate:
  estado_atual: pre_freeze_piloto_v230
  bloqueios_declarados:
    - "5 dos 10 indicadores_purificacao (classicizacao, moralizacao, depuracao_semantica, neutralizacao_afetiva, monumentalizacao) marcados nota_lacuna no codebook-patch original."
    - "9 referencias marcadas '[verificar ABNT completa antes do commit]'."
    - "Condicional 'obrigatorio_quando subtipo==hercules AND objetos_regalia nao_contem clava' exige validador com interseccao de arrays, nao coberto por tools/scripts/validate_schemas.py atual."
    - "Bloco 'aplicabilidade_por_familia_masculina' do codebook-patch original introduz 5 valores novos (aplicavel, aplicavel_com_cautela, aplicavel_com_subaltern_caution, inverter_polaridade) nao modelados no schema JSON; ficam apenas no YAML editorial."
---

# Adendo metodologico v2.3.0 — Gramatica masculina da alegoria estatal/juridica

> **Aviso de versao**: este adendo documenta a expansao para a v2.3.0 (patch
> opcional sobre a master v2.2.0). Ele **nao re-pontua** registros ja
> codificados em v2.2.0. Itens pre-existentes seguem validos; os campos novos
> sao opcionais ate decisao explicita de freeze da v2.3.0.

## 1. Tese do adendo

Sistematizar uma "gramatica masculina" para o LPAI v2.x e metodologicamente
necessario porque as evidencias reunidas mostram que figuras masculinas operam
como dispositivos de decisao moral e conducao cognitiva (Hercules no "bivio"),
como operadores de sustentacao arquitetonica/territorial (Atlas/atlantes) e
como personificacoes aquaticas de fertilidade e abundancia (deuses fluviais
barbados e, por extensao tipologica, o "Neptuno" barbado semirrecostado com
urna vertente).[^1][^2][^3][^4][^5]

Do ponto de vista do regime de visibilidade, essa gramatica masculina se
reconhece menos pela "identidade nominal" e mais por combinacoes de postura
corporal, marcadores de cena e objetos-regalia que estabilizam a leitura:
nudez e clava na mao direita (Hercules), globo sobre os ombros (Atlas), corpo
semirrecostado e urna que verte agua (tipo fluvial/marinho), e marcas de
mediacao entre esferas (o jovem "vestido all\'antica" que indica a Justica).[^1][^2][^5][^6]

Uma consequencia critica e que registrar `genero_atribuido = masculino` como
simples valor de enum, sem uma teoria de funcao e sem uma gramatica de
reconhecimento, tende a reproduzir a invisibilidade da masculinidade como
construcao iconografica (isto e, como sistema de marcas corporais e de
autoridade, e nao como "padrao neutro").[^7][^6]

Alem disso, a evidencia ja disponivel sugere que a gramatica masculina se
recontextualiza em programas politicos especificos (imperio, monarquia, destino
nacional, "uniao") por via de transposicoes atributivas: o cetro que "se
convertera" em "vara magica" e sera manejado "como Hercules a sua clava" no
discurso que le o "Genio do Brasil" como instrumento de poder e uniao nacional
em torno da monarquia.[^8]

Por fim, embora este adendo tenha sido desenhado para servir ao patch v2.3.0,
e preciso reconhecer que a base de evidencia ainda e assimetrica: ha trechos
robustos sobre o tipo herculeo, sobre Atlas/atlantes e sobre a tipologia do
deus fluvial/"Neptuno" barbado; porem ha lacunas para a especificidade
iberica e, sobretudo, para a iconografia juridica brasileira em suportes
estatais (moedas, selos, arquitetura forense) e para casos como Duque de
Caxias e bandeirantes em chave estritamente "juridico-estatal".[^8]

## 2. Sub-linhagem 1 — Hercules juridico

A sub-linhagem herculea aparece, nas evidencias, como dispositivo de decisao
moral e de pedagogia da escolha, centrado no "momento del dubbio" e na
dificuldade de distinguir "il falso dal vero" e "la virtu dal vizio",
articuladas ao episodio do "bivio".[^1] O que importa para o codebook nao e
apenas a referencia ao mito, mas a funcao cognitiva explicita — o "problema
della conoscenza" — que transforma a figura masculina em operador de
discriminacao moral e epistmica.[^1]

Em termos de gramatica de reconhecimento, os fragmentos indicam elementos
visuais relativamente estaveis: Hercules e descrito como "imberbe e nudo, con
la clava nella mano destra", e a cena pode fixar a indecisao por marcas de
postura (olhar direcionado a mulher e perna avancando, como se o corpo
"quisesse mover-se" em direcao oposta a mente).[^1] A enfase na clava como
atributo de agencia e forca reaparece na recontextualizacao luso-brasileira:
no texto de Araujo Porto-Alegre, o cetro "se convertera n\'huma vara magica"
e o "braco juvenil" o manejara "como Hercules a sua clava".[^8]

Essa recontextualizacao nao e neutra: no mesmo discurso, a transformacao do
cetro em clava autoriza uma narrativa de "esmagamento" de "monstros"
moral-politicos (corrupcao, anarquia, impunidade, ignorancia), por analogia
aos "doze trabalhos" de Hercules, e inclui ate as "cataractas do rio das
Amazonas" na lista de obstaculos a serem vencidos.[^8] Para o LPAI, isso
sugere que o "Hercules juridico" pode operar como figura de soberania
"purificadora" (ordem publica) e nao apenas como emblema de escolha moral
individual.[^8][^1]

Ha tambem uma dimensao de circulacao politico-imperial em que alusoes a
Hercules sao "frequently exploited" em "displays of power" associados ao
Imperador Carlos V, e seu lema "PLVS VLTRA" se liga a "two pillars rising from
the sea" que "directly referenced Hercules".[^7] A conexao entre pilares
maritimos e potencia soberana e relevante para o codebook porque abre uma
ponte com outras sub-linhagens masculinas (Atlas/Atlantico;
Netuno/soberania marinha), em que o mar e a sustentacao se entrelacam como
programa iconografico coerente.[^7][^3]

## 3. Sub-linhagem 2 — Atlantes e Telamones (sustentacao)

Atlantes e telamones operam como colunas antropomorficas sustentando o peso
da construcao: tanto em fachada de companhia de navegacao (programa
modernista brasileiro) quanto em fachada manuelina/luso-brasileira, a figura
masculina aparece em chave de suporte arquitetonico e simbolico. A gramatica
de reconhecimento combina postura de sustentacao (corpo ereto curvado sob
peso), musculatura exibida, e por vezes globo sobre os ombros (Atlas como
"suporte do mundo").[^3][^9]

A ligacao com programas imperiais / de soberania e dupla: por um lado, o
atlante e operador de infraestrutura (estacao de trem, fachada de companhia
de navegacao); por outro, e marcador de "trazer o mundo junto" — gestao de
circulacao, transporte, territorio. Isso justifica campo especifico para
`funcao_atlanteana` (verdadeiro quando a figura masculina cumpre funcao
explicita de suporte/sustentacao), alem de `tipo_agencia_masculina` =
`Suporte_Arquitetonico` ou `Delimitacao_Territorial`.[^3][^5][^9]

Ha tambem uma dimensao iconografica de "marolas" e outros marcadores
ornamentais aquatico-maritimos que aparecem junto a atlantes em fachadas de
companhia de navegacao, o que vincula essa sub-linhagem a deuses fluviais e a
Netuno.[^3]

## 4. Sub-linhagem 3 — Deuses fluviais barbados e o tipo "Neptuno"

A sub-linhagem de deuses fluviais barbados e importante porque estabiliza
uma tipologia masculina aquatica reconhecivel por combinacao de marcas:
**barba longa** + **corpo semirrecosto** + **urna/vaso vertente**. A regra de
coocorrencia e critica: barba isolada nao basta para inferir deus fluvial
(pode ser marcador generico de autoridade masculina), nem semirrecosto
sozinho (tambem aparece em America reclinada). E a triade — barba + postura
+ efluencia hidrica — que constitui o tipo.[^3][^5]

O chamado "Neptuno" da Colecao do Carpio (Estella 2002) ilustra a
instabilidade tipologica: um homem velho, de barba longa, semirrecostado,
apoiado em urna que verte agua. A pergunta "rio ou mar?" permanece em aberto
quando o suporte nao nomeia o corpo d\'agua. Para o LPAI, isso justifica:
(i) campo `tipo_efluencia_hidrica` com valores `Urna_Vertedora`,
`Vaso_Inclinado`, `Sem_Efluencia`, `Outro`; (ii) regra explicita de
coocorrencia para inferir tipo `Rio_Barbado` apenas quando barba +
semirrecosto + efluencia estao presentes; (iii) cautela tipologica quanto a
distinguir rio barbado de Oceanus barbado.[^3][^5][^10]

A evidencia de Lazzaro (2011) sobre o "ancient river god type" no
Renascimento italiano e sua apropriacao politica em festividades e
tapeçarias (Raphael/Leo X) sustenta que essa tipologia tem circulacao
prescritiva forte em programas europeus, com transferencia plausivel para
programas imperiais brasileiros.[^4]

## 5. Sub-linhagem 4 — Netuno e soberania maritima

A personificacao do meio marinho nao tem genero fixo: Lopez (2017) mostra
que a preferencia ocidental e por Oceanus (masculino), enquanto a escolha
bizantina foi por Thetis (feminino), com transformacoes iconograficas e
semanticas atraves dos periodos. Isso implica que o codebook nao pode
tratar `Netuno` (masculino) e `Tetis` (feminino) como opostos rigidos, mas
como duas respostas historicamente situadas a mesma questao
personificativa.[^10]

Para o caso brasileiro, soberania maritima evoca ainda Gal. 4:13 ("a vista
do mar e um documento"), com alusoes a Carlos V e os "two pillars rising
from the sea" como marcador herculeo-maritimo do programa "PLVS VLTRA".[^7][^11]

A v2.3.0 introduz, no eixo de `objetos_regalia`, `Tridente_Imperial` e
`Ancora_Naval` como marcadores de soberania marinha em chave masculina; ambos
carregam `nota_lacuna` na base de evidencia deste piloto, indicando que a
busca direta em moedas/selos brasileiros e suporte prioritario para um
futuro freeze.[^7][^10]

## 6. Casos brasileiros — Genio do Brasil, Amazonas, Prata

O caso brasileiro mais explicito do eixo masculino como agencia politica e o
"Genio do Brasil" descrito por Araujo Porto-Alegre: guerreiro, protetor,
instrumento de poder e uniao nacional em torno da monarquia. O discurso
canoniza o cetro como "vara magica" manejada "como Hercules a sua clava",
produzindo uma transposicao atributiva (`Substituicao_Atributiva_Hercules`)
que torna o item auditavel como leitura herculea sem o atributo canonico
(clava) estar materialmente presente.[^8]

Os rios Amazonas e Prata aparecem como estatuas colossais recostadas, em
chave de delimitacao territorial do Imperio. A representacao opera por
monumentalizacao (estatuas colossais em fachada/portal) e por
delimitacao_geografica (fronteiras naturais do territorio). Isso justifica
`tipo_agencia_masculina = Delimitacao_Territorial` e o subtipo
`Rio_Barbado` quando a combinacao de marcas se confirmar.[^8][^5]

O Genio do Brasil entra como `subtipo = Genio_Protetor` e
`funcao_da_figura_masculina = Protetorado_Nacional`. A identificacao
herculea depende do registro explicito de `substituicao_atributiva_hercules`
quando o atributo canonico nao aparece.[^8]

## 7. Lacunas declaradas (gate pro freeze)

- **Duque de Caxias** em profundidade (iconografia e funcao juridico-estatal): lacuna na base de evidencia (busca neste piloto).[^5]
- **Deuses fluviais especificos** do papel-moeda brasileiro e/ou selos oficiais (alem de descricoes textuais de programas e festividades): lacuna na base de evidencia (busca neste piloto).[^6][^7]
- **Masculinidades afro-brasileiras** (p.ex., Exu, Ogum) e seu encaixe (ou nao) na gramatica "Masculino_Juridico": lacuna na base de evidencia (busca neste piloto).[^8]
- **Masculinidades indigenas** em iconografia estatal/juridica brasileira: lacuna na base de evidencia (busca neste piloto).[^7]
- **Panofsky e a bibliografia canonica** sobre "Hercules am Scheidewege" aplicada a frontispicios normativos/estatais: lacuna na base de evidencia (busca neste piloto).[^5]
- **Atlantes em portais manuelinos** e sua transmissao para fachadas coloniais brasileiras e palacios republicanos: lacuna na base de evidencia (busca neste piloto).[^6]
- **Criterios de distincao "rio barbado" vs "mar barbado"** (Netuno/Oceanus) quando o suporte nao nomeia o corpo d\'agua: lacuna na base de evidencia (busca neste piloto).[^3][^8]
- **Validacao empirica** da aplicacao dos 10 indicadores de purificacao a gramatica masculina (incluindo casos de polaridade invertida em `desincorporacao`): lacuna na base de evidencia (busca neste piloto).[^3][^5]
- **Regra condicional `substituicao_atributiva_hercules`**: exige validador com interseccao de arrays (`objetos_regalia` nao contem `Clava`); `tools/scripts/validate_schemas.py` atual nao cobre. Gate tecnico antes do freeze.[^12]

## 12. Referencias

> **Aviso**: 8 das 8 referencias abaixo foram marcadas como
> "[verificar ABNT completa antes do commit]" no rascunho Elicit original.
> Esta consolidacao **preserva** essas marcas como declaracao explicita de
> pendencia editorial, nao como correcao. O freeze da v2.3.0 deve ser
> condicionado a normalizacao ABNT completa.

- [verificar ABNT completa antes do commit] Estudo sobre o "bivio erculeo" e descricao de pintura/tabua no Museu Bardini (Florenca), com Hercules nu, imberbe e com clava; discussao do "momento del dubbio", do "bivio" e do "problema della conoscenza".[^1]
- [verificar ABNT completa antes do commit] Texto em ingles sobre integracao de imaginario classico (Hercules) em armaduras germanicas e sobre usos politicos de Hercules por Carlos V ("PLVS VLTRA" e pilares).[^7]
- [verificar ABNT completa antes do commit] Ensaio sobre a apropriacao renascentista do "ancient river god type" e seu uso politico em festividades e tapecarias (Raphael/Leo X).[^4]
- [verificar ABNT completa antes do commit] Artigo/nota (AEA, LXXV, 2002) descrevendo o "llamado Neptuno" como homem velho, de barba longa, semirrecostado, apoiado em urna que verte agua.[^5]
- [verificar ABNT completa antes do commit] Pagina/ensaio sobre antiporta com Justica (balanca e espada) e figura masculina jovem "vestida all\'antica" como mediador entre esfera divina e do direito, com gesto indicativo.[^6]
- [verificar ABNT completa antes do commit] Portal DezenoveVinte (artigo sobre Araujo Porto-Alegre e o "Genio do Brasil"), com passagens sobre o cetro que vira "vara magica" e o "braco juvenil" que o maneja "como Hercules a sua clava", e sobre o Genio como instrumento de poder e uniao nacional em torno da monarquia; inclui descricao dos rios Amazonas e Prata como estatuas colossais recostadas e como delimitadores do Imperio.[^8]
- [verificar ABNT completa antes do commit] Texto de divulgacao sobre "a fachada do IPHAN" (orioqueorionaove.com), com definicao de atlantes como colunas antropomorficas sustentadoras do peso da construcao e com justificativa para Atlas em fachada de companhia de navegacao, alem de marcador ornamental de "marolas".[^3]
- [verificar ABNT completa antes do commit] Artigo em espanhol/ingles sobre personificacoes do meio marinho (Antiguidade–Idade Media), distinguindo preferencia ocidental por Oceanus (masculino) e escolha bizantina por Thetis (mar feminino), e declarando o foco em transformacoes iconograficas e semanticas.[^10]

[^1]: Villari, 2015. L\'«Ercole al bivio» di Domenico Beccafumi (1486-1551) e l\'Ercole giraldiano.

[^2]: Schroder, 2014. Images and messages in the embellishment of metropolitan railway stations (1850-1950).

[^3]: orioqueorionaove, 2012. A fachada do IPHAN | O RIO QUE O RIO NAO VE.

[^4]: Lazzaro, 2011. River gods: personifying nature in sixteenth-century Italy. Renaissance Studies.

[^5]: Estella, 2002. El llamado Neptuno (Rio?) de la Coleccion del Carpio y su problematica identificacion con una obra atribuida a Bernini, en Aranjuez. Archivo Espanol De Arte.

[^6]: Immagini della Giustizia: antiporte: Titius, Observationum ratiocinantium ... (1).

[^7]: Bendall, 2022. Female Personifications and Masculine Forms: Gender, Armour and Allegory in the Habsburg-Valois Conflicts of Sixteenth-Century Europe. Gender & History.

[^8]: 19&20 - O Genio do Brasil e as Musas: Um manifesto ideologico numa nacao em construcao, por Alberto Martin Chillon.

[^10]: Lopez, 2017. La personificacion del mar: Evolucion y transformaciones iconograficas del mundo clasico al medioevo.

[^11]: Immagini della Giustizia: antiporte: Titius, Observationum ratiocinantium ... (1).

[^12]: tools/scripts/validate_schemas.py — limitacao documentada para condicionais com interseccao de arrays.
