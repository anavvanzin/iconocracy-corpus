---
codebook_id: lpai-v2
codebook_version: 2.0.0
data_versao: 2026-06-22
documento_pai: data/docs/codebook.md
reenquadramento_epistemico: schema/lpai-v2-as-capta.md
status: piloto
pre_freeze_sample: true
arquivos_companheiros:
  - schema/codebook-v2.0.0.yaml (versão legivel por máquina)
  - schema/codebook-v2.0.0.schema.json (validação automática)
autor: Ana Vanzin
licenca: CC-BY-4.0
---

# Codebook LPAI v2.0.0 (capta) — Alegorias de Virtudes, Continentes e Oceanos/Rios

## 1. Declaração de capta

> LPAI v2-capta: scores são atos interpretativos situados, não dados neutros.[^1]

Este codebook parte do pressuposto de que o que se registra como “dado” em projetos de humanidades visuais é, na prática, capturado e construído por atos interpretativos, isto é, capta, e não um “dado dado” pela realidade.[^1] Em particular, convenções de legibilidade (inclusive de codificação e de visualização) tendem a esconder os enquadramentos interpretativos originais que tornaram o registro possível, razão pela qual este schema obriga metadados de autoria, temporalidade e evidência para tornar rastreável o trabalho interpretativo.[^2] Adota-se também o princípio de que projetos de dados devem declarar e auditar contexto (poder, emoção, pluralidade e trabalho) porque “data are not neutral” e porque discrepâncias de poder exigem perguntar “who benefits” do produto de dados.[^3]

## 2. Escopo, justificativa e princípio de unidade analítica

O escopo do LPAI v2.0.0 é codificar programas iconográficos alegóricos relevantes para o regime jurídico-estatal brasileiro, tratando tais programas como artefatos visuais de legitimação e de produção pública do direito, em linha com abordagens que colocam “as renderizações visuais da lei” no centro da análise.[^4] A justificativa metodológica é que a iconografia estatal “pode reivindicar representar justiça” mas, sob disputa, pode operar como representação de poder e como dispositivo de consentimento, o que exige que o corpus registre tanto atributos quanto implantação institucional (função e lugar de circulação).[^5] Ao mesmo tempo, a alegoria é, por definição, ambígua e dependente de contextos, intenções e posições de leitura, de modo que este codebook separa campos descritivos (observáveis) de campos interpretativos (hipóteses) sempre que possível.[^6][^7]

### 2.1 Corpus core vs. comparador genealogico

A regra de inclusão do **corpus core** é restritiva: entram apenas itens que sejam dispositivos estatais/jurídicos brasileiros (p. ex., moedas, cédulas, selos, brasões, frontispícios normativos, arquitetura forense e monumentos públicos) com evidência documental de circulação no Brasil, pois o interesse analítico é a “arte encomendada, sancionada e mobilizada pelo Estado e seus órgãos”.[^5] Itens que sejam úteis apenas como genealogia comparativa (p. ex., gravuras europeias de “Four Continents”, entradas de repertórios como Ripa, Ortelius ou séries impressas) devem ser cadastrados como **comparador** e não contam para estatísticas do core, ainda que informem a transmissibilidade dos esquemas alegóricos em múltiplos suportes (gravuras, metalwork, pinturas, têxteis etc.).[^8]

### 2.2 Unidade analítica

Este codebook define que `item_id` representa um **programa iconográfico** (um conjunto coerente de figuras e inscrições em um mesmo dispositivo, ou uma série quando a repetição serial é o fenômeno) e não uma figura isolada, porque a análise se interessa pela forma como a alegoria é “sited” (implantada) em arquiteturas e suportes estatais, e não apenas por um motivo isolado em abstração.[^9] A consequência é que a codificação deve registrar a quantidade de figuras no programa e a justificativa do agrupamento, dado que as virtudes e alegorias historicamente aparecem tanto individualmente quanto “en conjunto”, e a decisão entre unidade singular e unidade coletiva muda o significado do registro e a comparabilidade.[^10]

Como o sentido de signos visuais depende de contexto e de intenções, a escolha da unidade analítica deve ser explicitada no próprio registro para evitar que a aparência de “simplicidade e legibilidade” apague o enquadramento interpretativo do/a codificador/a.[^2][^7]

Consequências operacionais obrigatórias nesta versão (v2.0.0), todas concebidas para tornar auditável a construção do capta:

- `n_figuras_no_item` é obrigatório e $$\ge 1$$, para que o registro do programa não naturalize uma unidade que não existe no suporte (p. ex., retábulo com múltiplas personificações).[^10][^7]
- `record_metadata.nota_metodologica` é obrigatório quando `n_figuras_no_item > 1`, para documentar o critério de agrupamento e tornar visível o trabalho interpretativo.[^3]
- Quando o programa contém múltiplas personificações que seriam subtipos diferentes, o `subtipo` deve usar o valor coletivo `Virtudes_conjunto` (quando aplicável), pois virtudes podem ser representadas em conjunto e com atributos distintivos distribuídos no espaço do programa (não em uma figura única).[^10]
- Para contagem de frequência de figuras individuais dentro de um programa, utiliza-se o campo opcional `figuras_inventariadas`, para que estatísticas não confundam “unidade de registro” com “unidade de motivo”.[^7]
- A alternativa hierárquica “item-pai / itens-filhos” (com `item_pai_id`) fica documentada como upgrade possível para versões futuras, reconhecendo que qualquer esquema de classificação é uma escolha situada e revisável, não um espelho neutro do mundo.[^6][^1]

## 3. Campos de capta obrigatórios

A tabela a seguir lista os campos obrigatórios de capta, cujo objetivo é tornar rastreável a autoria, o momento, a versão e a qualidade de evidência do registro, em consonância com a exigência de “considerar contexto” (poder, trabalho, pluralidade) e de conceber os registros como capta construído.[^3][^1]

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|---|---|---|---|---|
| capta_declaration | string fixa | Declaração de capta a ser copiada literalmente para cada registro. | `"LPAI v2-capta: scores são atos interpretativos situados, não dados neutros."`[^1] | sim |
| coder_id | string | Identificador do/a codificador/a (nome curto, ORCID ou handle). | `"avanzin"`[^3] | sim |
| coded_at | string ISO 8601 | Data/hora da codificação (fuso incluso). | `"2026-06-23T10:45:00-03:00"`[^3] | sim |
| codebook_version | string | Deve ser `"2.0.0"` para registros deste schema. | `"2.0.0"`[^2] | sim |
| pre_freeze_sample | bool | Marca que o item pertence ao piloto pré-freeze, aceitando mudanças de schema. | `true`[^2] | sim |
| status_evidencia | enum | Estado do item quanto a elegibilidade e verificação de evidência (ver seção 16). | `piloto`[^2] | sim |
| score_evidencia | float 0.0–1.0 | Pontuação composta de evidência documental e rastreabilidade (ver abaixo). | `0.62`[^2] | sim |

Os campos acima operam como resposta ao problema metodológico de que a “simplicidade e legibilidade” de um registro pode esconder o trabalho interpretativo que o produz, exigindo que se registre o contexto e a qualidade da evidência.[^2][^3]

### 3.1 status_evidencia

O campo `status_evidencia` controla a fronteira entre corpus core e comparador e explicita o grau de verificação, porque a análise de imagens sancionadas pelo Estado depende de rastreabilidade da circulação e de cuidado com inferências contestáveis (por exemplo, quando “Justiça” representada pode não significar “justiça para todos”).[^5][^4]

Valores permitidos e definições operacionais:

- `core_verificado`: item elegível ao corpus core com evidência $$\ge 0.75$$, URL institucional verificada, imagem primária de alta resolução localizada e data documentada, para reduzir o risco de registrar como neutro o que é conjectura interpretativa.[^2]
- `piloto`: item em codificação com lacunas pendentes (busca web não executada ou parcial; imagem ainda não localizada; metadados incompletos), indicando que o registro é capta provisório e pode ser revisto.[^1][^2]
- `comparador`: item usado apenas para genealogia comparativa (por exemplo, repertórios europeus de personificação que funcionam como “stand-ins” alegóricos), não entrando em estatísticas do corpus core.[^11]
- `apendice`: caso-limite, citado apenas em notas, quando a relevância para o argumento é marginal e a evidência é insuficiente para codificação plena.[^7]

### 3.2 score_evidencia

O `score_evidencia` é uma composição para tornar visíveis as dimensões de evidência que usualmente ficam implícitas na aparência “legível” de um dataset, e deve ser entendido como capta (uma escolha de pesos e critérios) e não como medida natural do mundo.[^1][^2]

A fórmula recomendada (editável no piloto, mantendo rastreabilidade) é:

$$score\_evidencia = 0.35\,E_{circulacao} + 0.25\,E_{proveniencia} + 0.25\,E_{imagem} + 0.15\,E_{metadados}$$[^2]

Em que cada componente $$E\_i \in [0,1]$$ deve ser justificado em `record_metadata.nota_metodologica` quando $$< 0.75$$, para reduzir o risco de uma codificação que trate interpretações como dados “completamente desligados do julgamento humano”.[^3]

## 4. Campos de identificação do item

Os campos de identificação distinguem o “objeto” codificado do “ato” de codificar, porque a leitura de signos depende de suporte, meio e circulação, e porque a coleta pode ser motivada por interesse em artista, objeto, meio ou tema, afetando o recorte do corpus.[^8]

| Campo | Tipo | Descrição | Exemplo | Obrigatório |
|---|---|---|---|---|
| item_id | string | Identificador único: `LPAI-####` ou hash de 8 dígitos, persistente. | `LPAI-0123`[^2] | sim |
| titulo | string | Título curto e desambiguado do programa/suporte. | `"Iustitia — Nave da Matriz do Pilar (programa de virtudes)"`[^10] | sim |
| suporte | string | Tipo de suporte material (ex.: retábulo, nave, moeda, selo, frontispício). | `"arquitetura_religiosa"`[^12] | sim |
| data_suporte | string | Ano, intervalo ou data completa do suporte. | `"1731-1750"`[^12] | sim |
| instituicao_origem | string | Instituição de produção/uso (p. ex., igreja, Casa da Moeda, tribunal). | `"Igreja Matriz de N. Sra. do Pilar"`[^12] | sim |
| localizacao_atual | string | Onde se encontra hoje (cidade/UF, acervo). | `"Ouro Preto, MG"`[^12] | sim |
| fonte_imagem | string | URL ou referência arquivística da imagem usada na codificação. | `"ARQ-OP-IMG-00045"`[^2] | recomendado |
| tipo_reproducao | enum | `original` / `reproducao_fotografica` / `gravura_impressa` / `digital` / `outro`. | `digital`[^2] | recomendado |

## 5. Iconclass

A indexação Iconclass é adotada como tecnologia de interoperabilidade e busca, mas sua aplicação é tratada como decisão operacional situada, pois “qualquer ícone carrega a ambiguidade do concreto” e, portanto, códigos de classificação não esgotam o sentido e podem produzir anacronismos se aplicados sem regra explícita.[^6] Além disso, a própria tradição de repertórios (como Ripa) depende de índices de elementos (animais, objetos, plantas, cores, motti), oferecendo um paralelo metodológico entre indexação e extração de atributos, mas sem autorizar inferência automática de significado a partir de um índice.[^13]

### 5.1 Códigos primários por família

A tabela abaixo define os códigos primários **operacionais** adotados no piloto para facilitar busca e consistência, reconhecendo que há lacuna na base de evidência (busca neste piloto) quanto à validação bibliográfica específica dos números Iconclass para cada subtipo, e que a regra é, antes de tudo, de rastreabilidade interna do projeto.[^6][^13]

| Família | Cluster Iconclass primário | Observação operacional |
|---|---|---|
| Virtudes cardinais | 11M3x (Iustitia = 11M31; Prudentia = 11M32; Fortitudo = 11M33; Temperantia = 11M34) [^13] | Mapeamento adotado para indexação; lacuna na base de evidência (busca neste piloto) para citação direta do catálogo Iconclass. [^6] |
| Virtudes teologais | 11M4x (Fides, Spes, Caritas) [^13] | Mapeamento adotado para indexação; lacuna na base de evidência (busca neste piloto) para citação direta do catálogo Iconclass. [^6] |
| Continentes | 23E (Continentes) com subcódigos por região [^11] | Personificações continentais funcionam como “stand-ins” alegóricos, não etnografia; a indexação deve ser acompanhada por campos de racialização observável e hipótese interpretativa. [^11] |
| Oceanos/Rios | 25H (Personificações de água) e 92B (deuses fluviais clássicos) [^14] | A tradição clássica individualiza águas como ninfas ou deuses; a indexação deve ser acompanhada por descrição do gênero e da função soberana. [^14] |
| República feminina | 44G411 (República como mulher) [^15] | Aplicável apenas a itens produzidos em ou após 1889; lacuna na base de evidência (busca neste piloto) para ancoragem Iconclass direta do código numérico. [^16] |

### 5.2 Regra de anacronismo

Regra obrigatória do piloto: **o código Iconclass 44G411 (República como mulher) é PROIBIDO para itens coloniais anteriores a 1889**; aplicação equivocada desse código a virtudes barrocas mineiras configura contaminação analítica e deve ser corrigida durante codificação ou em auditoria intercodificador, pois a própria iconografia republicana brasileira é historicamente situada e não representa “ruptura radical” em relação ao regime anterior, sendo anacrônico projetar a forma política “República” como categoria visual sobre a arquitetura colonial.[^16][^2]

Exemplo positivo (aplicável): efígie feminina da República em suportes republicanos (moedas/cédulas), quando documentada como “national personification” e como presença em moedas e cédulas no Brasil.[^17]

Exemplo negativo (não aplicável): Iustitia em retábulo colonial de Ouro Preto (c. 1731), cuja função é litúrgica e moral no “regime mimético” e de decoro da arquitetura católica, não uma alegoria de República; lacuna na base de evidência (busca neste piloto) para exemplos iconclass documentados do caso específico, devendo o item ser classificado como Virtude (Iustitia) e não como República.[^12]

## 6. Famílias e subtipos

O esquema de família/subtipo é inspirado na tradição de repertórios que “personificam conceitos” e inventam imagens para termos, oferecendo um vocabulário de personificações (virtudes, paixões, regiões, rios) e suas explicações, o que torna plausível a codificação por categorias controladas.[^18] Ao mesmo tempo, como repertórios variam por edição e nem todas as alegorias são ilustradas, este codebook exige que codificações sejam sustentadas por evidência visual no item (ou anotadas como incerteza), evitando supor equivalência material entre entradas de repertório e exemplares brasileiros.[^19]

### 6.1 familia_alegorica

A tabela seguinte define o enum `familia_alegorica` como tipologia primária de classificação do programa, reconhecendo que a alegoria é uma tecnologia móvel e ambígua e que a escolha de família é sempre situada.[^6]

| Valor | Quando usar |
|---|---|
| Virtudes | Quando a personificação representa virtude cardinal, teologal ou jurídica, individualmente ou em conjunto.[^10] |
| Continentes | Quando a personificação representa continente/região (Europa, América etc.) como “stand-in” alegórico por atributos e accoutrements.[^11] |
| Oceanos_Rios | Quando há personificação/simbolização de corpo d’água (rio, oceano, fonte) como identidade individualizada (ninfa/deus).[^14] |
| Nacional | Quando a personificação é da nação/República/liberdade/pátria, inclusive efígies femininas em dispositivos de Estado republicano.[^17][^15] |
| Outra | Quando não se enquadra nas anteriores; justificar em `notes` e registrar a ambiguidade da escolha.[^6] |

### 6.2 subtipo

O campo `subtipo` é um enum dependente de `familia_alegorica` e deve ser preenchido como o “nome do conceito personificado” (no sentido de repertório alegórico) e não como descrição livre, porque a tradição de Ripa se organiza como um “dicionário alegórico” voltado a permitir que artistas “depictem virtudes, vícios, sentimentos e paixões” de forma repetível.[^20] 

Listas controladas por família (com a regra de não sobreposição de “Brasil” entre Continentes e Nacional, para evitar colapsar território continental em personificação nacional):[^7]

- **Virtudes:** `Iustitia`, `Veritas`, `Prudencia`, `Fortaleza`, `Temperanca`, `Justica_e_Paz`, `Esperanca`, `Caridade`, `Fe`, `Fama`, `Virtudes_conjunto`, `outra_virtude`.[^10]
- **Continentes:** `Europa`, `America_generica`, `America_do_Sul`, `Africa`, `Asia`, `outro_continente` (nota: `Brasil` NUNCA aqui).[^21][^11]
- **Oceanos_Rios:** `Oceano`, `Rio_grande`, `Rio_menor`, `Fonte`, `Netuno`, `Tetis`, `outro_hidrico`.[^14]
- **Nacional:** `Republica`, `Liberdade`, `Patria`, `Brasil`, `outra_nacional` (nota: `Brasil` como personificação nacional/republicana vai aqui).[^17][^22]

## 7. Campos específicos para Virtudes

As Virtudes são tratadas como campo crítico porque a arquitetura religiosa pode operar como “representação permanente das virtudes cristãs” com função pedagógica e moral (“conduzir virtuosamente o fiel”), o que justifica registrar a relação entre virtude e regime institucional (litúrgico vs estatal).[^12] Além disso, como virtudes podem ser representadas individualmente ou em conjunto e desde cedo com “atributos distintivos”, a codificação precisa discriminar tipo de virtude e função no programa.[^10]

### 7.1 tipo_virtude

`tipo_virtude` (enum) captura a tradição de diferenciação entre virtudes cardinais e teologais e a possível presença de uma virtude “jurídica secular” em contextos de Estado (p. ex., alegorias da Justiça em tribunais).[^20][^4]

Valores permitidos:

- `cardinal`: Iustitia, Prudentia, Fortitudo, Temperantia, quando identificáveis no programa por atributos e/ou inscrição.[^10]
- `teologal`: Fides, Spes, Caritas, quando identificáveis no programa por atributos e/ou inscrição.[^12]
- `juridica_secular`: quando a virtude aparece em circuito estatal/jurídico e a codificação privilegia a função pública do signo (por exemplo, em arquitetura forense), reconhecendo que o sentido é disputável e não necessariamente “justiça para todos”.[^4]
- `hibrida`: quando há mistura explícita de gramática cristã e função pública, pois o regime de decoro e representação católica pode se articular a razões de Estado e práticas de legitimação.[^12]

### 7.2 funcao_liturgica_vs_estatal

`funcao_liturgica_vs_estatal` (enum) registra a função dominante do programa, porque a codificação precisa capturar a migração (ou coexistência) entre “encenar decorosamente as matérias da fé” e operar como visibilidade de valores públicos e jurídicos, compatível com a ideia de que a justiça pode ser “seen” e “sited”.[^12][^9]

Valores permitidos:

- `liturgica_pura`: quando a virtude opera como parte de um programa estritamente catequético/litúrgico.[^12]
- `liturgica_com_carga_civica`: quando o programa litúrgico inclui alegorias que organizam um regime de governo moral e disciplinar compatível com “razão de estado católica” e com decoro de corte, exigindo registro da dimensão pública.[^12]
- `estatal_secularizada`: quando a virtude aparece em dispositivos de Estado (moedas, tribunais, frontispícios normativos), com função de legitimação visual do poder ou de seus valores.[^23][^4]
- `estatal_com_resquicio_liturgico`: quando o dispositivo estatal mantém gramáticas religiosas (por exemplo, mitos e iconografias de origem religiosa mobilizadas como símbolo nacional), sugerindo continuidade/hibridização e não ruptura radical.[^22]
- `nao_aplicavel`: quando o item não permite inferência razoável; registrar em `notes` a lacuna na base de evidência (busca neste piloto).[^19]

### 7.3 posicao_arquitetonica

`posicao_arquitetonica` (enum) codifica o regime de visibilidade da virtude no espaço, porque, conforme Resnik & Curtis, a justiça (e por extensão a virtude) pode ser “sited” em arquiteturas e a relação entre obra e “brick and mortar” compõe mensagens sobre valores institucionais e participação.[^9]

Valores permitidos:

`retabulo_principal`, `retabulo_lateral`, `nave_teto`, `nave_paredes`, `fachada_igreja`, `frontispicio_codigo`, `fachada_tribunal`, `sala_tribunal`, `monumento_publico`, `peca_serial`, `outra_posicao`.[^9]

## 8. Campos específicos para Continentes

A codificação de Continentes se justifica porque as personificações continentais são repertórios circuláveis e hierarquizantes: Europa pode aparecer “regally enthroned above the other parts of the world”, e séries como a do Theatrum de Ortelius formulam uma “new allegory of world order” em quarteto feminino (Europa/Ásia/África/América).[^21] Ao mesmo tempo, tais figuras são “allegorical stand-ins” e “not meant to serve as documentary evidence”, razão pela qual este codebook separa descrição observável de hipótese interpretativa e obriga registrar hierarquia e dimensão territorial do signo.[^11]

### 8.1 dimensao_territorial

`dimensao_territorial` (enum) registra o que o corpo alegórico está representando (continente inteiro, sub-região, nação dentro de continente etc.), porque as personificações são generalizadas e podem condensar múltiplas características “contraditórias” do “novo mundo”, exigindo cuidado com a escala do referente.[^24]

Valores permitidos:

`continente_inteiro`, `sub_regiao`, `nacao_dentro_de_continente`, `figura_generica_sem_territorio`, `nao_aplicavel`.[^11]

### 8.2 hierarquia_continental

`hierarquia_continental` (enum) codifica se há hierarquia explícita/implícita, pois a ordem e a posição de Europa como “reference point” e como trono soberano operam como enunciado político visual sobre civilização e domínio global.[^21]

Valores permitidos:

`europa_no_topo_explicita`, `europa_no_topo_implicita`, `hierarquia_invertida`, `sem_hierarquia`, `continente_unico_no_quadro`, `nao_aplicavel`.[^21]

### 8.3 racializacao_observavel

`racializacao_observavel` (objeto estruturado) registra apenas descrições observáveis (sem interpretação), porque as personificações continentais são “generalised and generic” e não documentação etnográfica, e porque o sentido racial opera por sinais convencionais (pele, vestimenta, adornos) mais do que por referência direta a povos “diversos”.[^11]

Subcampos obrigatórios quando o objeto for preenchido:

- `pele_descrita` (string)
- `cabelo_descrito` (string)
- `vestimenta_indicativa` (string)
- `adornos_indicativos` (string)
- `corpo_postura` (string)

A escolha por descrição observável é reforçada pela advertência de que signos podem ser lidos de “muitas maneiras” segundo contextos e intenções, exigindo que a interpretação (hipótese racial) venha depois e seja marcada como tal.[^7]

## 9. Campos específicos para Oceanos/Rios

A codificação de Oceanos/Rios se apoia na tradição clássica que individualiza águas “como ninfas ou deuses” e combina antropomorfismo com propriedades localizadas, o que sustenta a ideia de que corpos d’água podem ser alegorizados como sujeitos com atributos e, por vezes, gênero.[^14] Em contextos amazônicos, narrativas de “Amazonas” e figuras de mulheres guerreiras associadas ao grande rio mostram que a nomeação e personificação do rio podem ser politicamente carregadas e demandam registro cuidadoso do modo como gênero e soberania são mobilizados.[^25]

### 9.1 corpo_hidrico_nomeado

`corpo_hidrico_nomeado` (string) registra o nome do corpo d’água (ex.: “Rio Amazonas”, “Atlântico Sul”, “Fonte do Ipiranga”) ou `generico`, porque a tradição de repertório inclui “cidades e rios do país” e porque a localidade é parte do dispositivo de personificação.[^18]

### 9.2 dimensao_soberania

`dimensao_soberania` (enum) registra a função política do hídrico (fronteira, domínio imperial, recurso econômico etc.), pois a iconografia estatal pode operar como legitimação e como projeção de valores/pretensões, inclusive de “poder” e de “policy of power” (em chave teleológica) em contextos de direito e Estado.[^26]

Valores permitidos:

`marca_fronteira_nacional`, `marca_dominio_imperial`, `recurso_economico_personificado`, `figura_mitologica_pura`, `nao_aplicavel`.[^26]

### 9.3 atributo_gendrado_hidrico

`atributo_gendrado_hidrico` (string descritiva) registra a marcação de gênero (rio barbado masculino, ninfa feminina etc.) com referência visual direta, porque a codificação não deve inferir gênero apenas pela categoria “rio/água”, mas por sinais observáveis e por convenções, dado o risco de ocultar interpretação sob aparência de neutralidade.[^2][^14]

## 10. Atributos iconográficos

A codificação por atributos se inspira na lógica de índices de elementos alegóricos (animais, objetos, plantas, cores, motti) e no uso de atributos distintivos para identificar virtudes, o que legitima listas controladas para extração de traços visuais comparáveis.[^13][^10] Contudo, como “qualquer ícone” é ambíguo e como os significados dependem de contexto, atributos são tratados como descrição parcial e não como chave semântica única, devendo ser combinados com função jurídica, posição e hipótese interpretativa.[^6][^9]

### 10.1 atributos_iconograficos

`atributos_iconograficos` (lista de enum) — campo legado, mantido unificado em v2.0.0 para compatibilidade com itens já codificados no piloto; a divisão ortogonal por tipo de atributo está prevista para v2.1.0 (lacuna na base de evidência: busca neste piloto).[^2]

Valores controlados:

`balanca`, `espada`, `venda`, `espelho`, `tocha`, `globo`, `cornucopia`, `cetro`, `coroa`, `arco_e_flecha`, `cabeca_decepada`, `animais_exoticos`, `cobra`, `escorpiao`, `incensario`, `coroa_de_junco`, `urna`, `tridente`, `barrete_frigio`, `fasces`, `bandeira`, `ramos_estrelas`, `corpo_reclinado`, `barba`, `ondas_maritimas`, `outro`.[^13][^24]

### 10.2 Nota de design

Esta lista mistura atributos de objeto, marcas corporais e marcadores de cena; essa mistura é reconhecida como limitação (lacuna conhecida) porque pode reduzir comparabilidade intercodificador ao confundir “o que a figura segura” com “como o corpo é apresentado” e “que cena/accoutrements simbolizam o lugar”.[^7][^6]

## 11. Gênero, racialização e hipótese racial

Esta seção formaliza a separação entre descrição e interpretação, porque signos visuais podem ser lidos de muitas maneiras e porque a forma feminina na alegoria pode operar como mecanismo que representa valores enquanto mascaram exclusões (por exemplo, a figura feminina “não governa, ela representa”).[^7][^15]

### 11.1 genero_atribuido

`genero_atribuido` (enum) registra o gênero predominante da personificação, reconhecendo que a tradição de repertório personifica conceitos segundo o gênero gramatical do termo (no caso italiano) e que isso pode influenciar a codificação visual de gênero, mas sem impor equivalência automática entre gramática e imagem em suportes brasileiros.[^18]

Valores permitidos:

- `feminino`: figura com marcadores femininos claros (corpo, vestimenta, rosto), documentados na imagem.[^24]
- `masculino`: figura com marcadores masculinos claros (corpo, barba etc.), documentados na imagem.[^14]
- `neutro`: figura humana sem marcadores suficientes, exigindo nota de incerteza, pois o sentido depende de contexto e intenção.[^7]
- `hibrido`: coexistência de marcadores dualizados, exigindo descrição no campo `notes`, em consonância com a ambiguidade do ícone.[^6]
- `ausente`: não há figura humana (dado negativo descritivo), devendo a interpretação ser feita com cautela para não reificar ausência como “nada”.[^6]

### 11.2 racializacao_observavel

`racializacao_observavel` (objeto) é reutilizável para todas as famílias quando relevante, porque alegorias podem adotar “ideais classicizantes” de corpo e postura, e ainda assim operar como racialização por convenção (por exemplo, América nudez/penas/arco e flecha), exigindo registro observável antes de hipótese.[^11][^24]

### 11.3 hipotese_racial_interpretativa

`hipotese_racial_interpretativa` (string, max 500 caracteres) é explicitamente interpretativa e deve ser preenchida apenas após `racializacao_observavel`, porque a codificação deve tornar visível o trabalho interpretativo e evitar que uma hipótese pareça “dado” neutro; além disso, projetos devem perguntar “who benefits” do modo como categorias são estabilizadas.[^3][^2]

Exemplos de preenchimento (modelos; adaptar ao item):

- “América alegorizada como mulher recostada, nua, com cocar e arco e flechas; eroticização persistente e disponibilidade para exploração/posse, compatível com o imaginário colonial de terra feminilizada.”[^24]
- “Efígie republicana como jovem mulher com coroa de louros em estilo romano, operando como personificação nacional em suportes estatais seriados; hipótese: europeização do corpo nacional como gramática de legitimação visual.”[^17]

## 12. Função jurídica e vetor colonial

A função jurídica registra como a imagem participa de um regime institucional, porque a iconografia estatal não é apenas decoração: ela sinaliza valores, reivindica imparcialidade e pode operar como legitimação do poder e da violência estatal, em tensão com ideais de justiça para os vulneráveis.[^9][^5]

### 12.1 funcao_juridica

`funcao_juridica` (enum) identifica o tipo de dispositivo e sua inserção no espaço jurídico-estatal, em consonância com a ênfase em justiça “seen” e “sited” (no edifício, na moeda, no documento).[^9]

Valores permitidos:

`tribunal_consciencia`, `frontispicio_normativo`, `moeda_cedula`, `selo_postal`, `brasao`, `arquitetura_forense`, `monumento_publico`, `paratexto_normativo`, `outro`.[^9]

### 12.2 vetor_colonial

`vetor_colonial` (enum) registra a rota de transmissão do repertório iconográfico, pois séries alegóricas (Ripa, Four Continents) circulam em múltiplos suportes e podem ser apropriadas em contextos nacionais, inclusive quando os símbolos republicanos não indicam “ruptura radical” e se apoiam em tradições anteriores.[^8][^16]

Valores permitidos:

- `europeu_direto`: repertório europeu aplicado no Brasil sem mediação lusa evidente (registrar evidência em `notes`).[^8]
- `luso_brasileiro`: repertório transmitido via Portugal e/ou cultura colonial brasileira (ex.: decoro e programas de virtudes em arquitetura católica).[^12]
- `republicano_brasileiro`: repertório produzido e institucionalizado pelo Estado republicano brasileiro, frequentemente por circulação de imagens de mulheres, bandeiras e hinos como meios acessíveis e universais de legitimação visual.[^23]
- `nao_aplicavel`: quando o item não comporta comparação colonial ou o vetor é irrelevante; justificar a decisão em `notes` para não transformar ausência em neutralidade.[^2]

## 13. Referência genealógica

`referencia_genealogica` (lista de enum) registra chaves de repertórios e bibliografias que informam a leitura do item, pois repertórios alegóricos são textualmente mediados e funcionam como “handbook” influente de símbolos e alegorias, estruturado como dicionário explicativo e índices de elementos.[^13]

Valores permitidos:

`Ripa_1593_1603`, `Ortelius_1570`, `Collaert_Four_Continents`, `Carriera_Four_Continents`, `Warner_1985`, `Resnik_Curtis_2011`, `Souza_2014`, `Ihering_Der_Zweck`, `outra`.[^13][^4]

### 13.1 Regra de rastreabilidade

Cada valor de `referencia_genealogica` deve ter entrada correspondente em bibliografia do repositório (arquivo .bib ou verbete .md com ABNT completa), porque abreviações são apenas ponteiros e não substituem a evidência textual; isso é crucial quando edições diferem e nem todas as alegorias são ilustradas, pois a escolha de edição e a disponibilidade de imagem afetam o que pode ser inferido com segurança.[^19]

## 14. Indicadores de purificação

Os 10 indicadores ordinais herdados do documento-pai são mantidos nesta versão como instrumento de comparação interna, mas devem ser tratados como capta ordinal e não como métrica objetiva, pois a visualização e a quantificação podem ocultar o enquadramento interpretativo que os produz.[^2][^1] Além disso, como alegorias de justiça e de Estado são contestadas e “podem não significar justiça para todos”, a aplicação dos indicadores deve ser acompanhada por `subaltern_caution` quando a escala tiver sido construída para um tipo de figura (p. ex., corpo feminino) e o item codificado envolver ausência de figura ou masculinização.[^4]

Indicadores (nomes herdados; lacuna na base de evidência: busca neste piloto para validação integral dos nomes e definições do documento-pai):[^1]

1. `desincorporacao`
2. `heraldizacao`
3. `enquadramento_arquitetonico`
4. `serialidade`
5. `inscricao_estatal`
6. `classicizacao`
7. `moralizacao`
8. `depuracao_semantica`
9. `neutralizacao_afetiva`
10. `monumentalizacao`

Para cada indicador, preencher um valor inteiro 0–4 e, quando necessário, adicionar `subaltern_caution` em `notes`, pois a leitura do signo depende de contexto e intenção e não deve ser estabilizada como se fosse unívoca.[^7]

### 14.1 Aplicabilidade por família

A tabela abaixo orienta a aplicabilidade dos indicadores por família, tratando a decisão como heurística de piloto (capta) e não como regra ontológica, pois o sentido da iconografia é ambíguo e dependente de contexto institucional e de circulação.[^6][^9]

| Indicador | Virtudes | Continentes | Oceanos_Rios | Nacional |
|---|---|---|---|---|
| desincorporacao | aplicável (especialmente quando há corpo feminino como molde moral) [^12] | aplicável com subaltern_caution (gênero/nudez podem operar como erotização colonial) [^24] | aplicável com subaltern_caution (depende de sinais observáveis de gênero do hídrico) [^14] | aplicável (efígie feminina em moedas/cédulas) [^17] |
| heraldizacao | aplicável (quando virtude migra para brasões/insígnias) [^13] | aplicável (atributos/accoutrements como stand-ins) [^11] | aplicável (quando hídrico vira emblema) [^14] | aplicável (bandeira/brasão/hino como símbolos) [^22] |
| enquadramento_arquitetonico | aplicável (posição em nave/retábulo) [^12] | aplicável (frontispícios e programas) [^11] | aplicável (monumentos e cenas) [^14] | aplicável (edifícios públicos e artes de Estado) [^17] |
| serialidade | aplicável (quando reproduzida em gravuras/impresso) [^19] | aplicável (repertório circula em múltiplos suportes) [^8] | aplicável (repetição de Netuno/Tétis etc.) [^14] | aplicável (moedas/cédulas seriadas) [^17] |
| inscricao_estatal | aplicável quando em circuito estatal ou com carga cívica explícita [^9] | aplicável (quando incorporada em dispositivos de Estado) [^5] | aplicável (quando hídrico marca soberania estatal) [^26] | aplicável (símbolos republicanos oficiais) [^22] |
| classicizacao | aplicável (trajes clássicos e decoro) [^12] | aplicável (ideais classicizantes) [^11] | aplicável (mitologia clássica) [^14] | aplicável (coroa de louros romana) [^17] |
| moralizacao | aplicável (conduzir virtuosamente o fiel) [^12] | aplicável com subaltern_caution (hierarquias civilizatórias) [^21] | aplicável (finalidades morais/políticas podem ser projetadas) [^26] | aplicável (pedagogia cívica por imagens) [^23] |
| depuracao_semantica | aplicável (redução a atributos) [^13] | aplicável (stand-ins simplificados) [^11] | aplicável (estereótipos mitológicos) [^14] | aplicável (efígie como emblema simplificador) [^17] |
| neutralizacao_afetiva | aplicável (decoro e controle afetivo) [^12] | aplicável com subaltern_caution (erotização e medo colonial podem coexistir) [^24] | aplicável com subaltern_caution (gênero do hídrico pode ser afetivamente marcado) [^25] | aplicável (símbolos pretendem universalidade) [^23] |
| monumentalizacao | aplicável (fachadas e templos) [^12] | aplicável (frontispícios e programas de ordem mundial) [^21] | aplicável (estátuas e fontes) [^14] | aplicável (monumentos e edifícios governamentais) [^17] |

## 15. Convenções de nomenclatura de arquivos

A nomenclatura de arquivos é parte do “trabalho” que deve ser tornado visível, porque o processo de coleta e codificação é um produto humano, e a clareza do versionamento evita que artefatos de piloto pareçam “finais” e neutros.[^3][^2]

Regras:

- Arquivos de corpus: `corpus/piloto-v<MAJOR.MINOR.PATCH>-<topico>.json` (ex.: `corpus/piloto-v2.0.0-alegorias.json`), pois o estado de piloto deve ser explicitado para não produzir falsa legibilidade de completude.[^2]
- É proibido usar o sufixo `final` em arquivos pré-freeze, porque “dados” são construídos e revisáveis, e a marcação de estabilidade deve ser um estado formal, não um nome retórico.[^1]
- Codebook: `schema/codebook-v<MAJOR.MINOR.PATCH>.md` (este arquivo).[^3]
- Schema YAML: `schema/codebook-v<MAJOR.MINOR.PATCH>.yaml`.[^3]
- Schema JSON: `schema/codebook-v<MAJOR.MINOR.PATCH>.schema.json`.[^3]
- CHANGELOG: `schema/CHANGELOG.md` (arquivo único, versionado em sequência).[^3]

## 16. Convenções de status de evidência

Esta seção operacionaliza `status_evidencia` e `score_evidencia` como controles contra a tendência de visualizações e tabelas esconderem os enquadramentos interpretativos e a incompletude documental do corpus, isto é, contra a produção de “simplicidade e legibilidade” enganosa.[^2]

A tabela abaixo indica limiares e ações mínimas para reclassificação, reconhecendo que esses limiares são capta e podem ser ajustados no piloto com justificativa explícita.[^1]

| status_evidencia | Limiar score_evidencia | Lacunas toleráveis | Ações para promover |
|---|---:|---|---|
| core_verificado | $$\ge 0.75$$ [^2] | mínimas; sem lacuna de circulação e com imagem primária [^2] | verificar URL institucional, localizar imagem em alta resolução, documentar data e instituição de origem [^2] |
| piloto | $$0.40$$ a $$0.74$$ [^2] | lacunas parciais de imagem/URL/metadados [^2] | executar busca, registrar fonte, completar metadados e justificativas [^1] |
| comparador | qualquer [^11] | ausência de circulação brasileira pode ser total [^11] | manter fora de estatísticas; usar para genealogia com rastreabilidade de edição/suporte [^19] |
| apendice | $$< 0.40$$ [^2] | lacunas severas e relevância marginal [^7] | ou descartar, ou mover para comparador com nota de lacuna na base de evidência (busca neste piloto) [^7] |

Regra adicional obrigatória: quando a busca web/documental ainda não foi executada (campo de processo a registrar em `record_metadata`), o item deve ser automaticamente rebaixado para `status_evidencia: piloto`, pois a ausência de verificação torna explícito que o registro é capta provisório e pode esconder pressupostos interpretativos.[^2][^1]

## 17. Exemplo de registro completo

O exemplo abaixo ilustra um registro de Virtudes em arquitetura religiosa, explicitando unidade analítica (programa), quantidade de figuras, e separação entre descrição observável e hipótese interpretativa, pois a arquitetura pode ser “representação permanente das virtudes cristãs” orientada a conduzir o fiel, e porque alegorias podem ser representadas em conjunto com atributos distintivos.[^12][^10]

```yaml
capta_declaration: "LPAI v2-capta: scores são atos interpretativos situados, não dados neutros."
coder_id: "avanzin"
coded_at: "2026-06-23T10:45:00-03:00"
codebook_version: "2.0.0"
pre_freeze_sample: true
status_evidencia: "piloto" # gaps de URL/imagem ainda existem (busca neste piloto)
score_evidencia: 0.62

item_id: "LPAI-0123"
titulo: "Programa de Virtudes — Matriz de Nossa Senhora do Pilar (nave)"
suporte: "arquitetura_religiosa"
data_suporte: "1731-1750"
instituicao_origem: "Igreja Matriz de Nossa Senhora do Pilar"
localizacao_atual: "Ouro Preto, MG"
fonte_imagem: "lacuna na base de evidência (busca neste piloto)"
tipo_reproducao: "outro"

record_metadata:
  nota_metodologica: "O programa completo da nave é tratado como unidade iconográfica única; virtudes aparecem em conjunto no teto e sua função é pedagógica e moral no regime de decoro católico."

n_figuras_no_item: 8
figuras_inventariadas: ["Iustitia", "Prudencia", "Fortaleza", "Temperanca", "Fe", "Esperanca", "Caridade", "Veritas"]

familia_alegorica: "Virtudes"
subtipo: "Virtudes_conjunto"

tipo_virtude: "hibrida"
funcao_liturgica_vs_estatal: "liturgica_com_carga_civica"
posicao_arquitetonica: "nave_teto"

iconclass_principais: ["11M31", "11M32", "11M33", "11M34", "11M41", "11M42", "11M43"]

atributos_iconograficos: ["balanca", "espada", "outro"]

genero_atribuido: "feminino"

racializacao_observavel:
  pele_descrita: "figuras femininas brancas (descrição provisória)"
  cabelo_descrito: "lacuna na base de evidência (busca neste piloto)"
  vestimenta_indicativa: "vestes classicizantes (descrição provisória)"
  adornos_indicativos: "lacuna na base de evidência (busca neste piloto)"
  corpo_postura: "lacuna na base de evidência (busca neste piloto)"

hipotese_racial_interpretativa: "Racialização implícita pela gramática barroca luso-ibérica; figuras brancas naturalizam a virtude como atributo da civilização cristã no regime de decoro."

funcao_juridica: "tribunal_consciencia"
vetor_colonial: "luso_brasileiro"

referencia_genealogica: ["Ripa_1593_1603", "Warner_1985"]

indicadores_purificacao:
  desincorporacao: 2
  heraldizacao: 1
  enquadramento_arquitetonico: 4
  serialidade: 0
  inscricao_estatal: 1
  classicizacao: 3
  moralizacao: 4
  depuracao_semantica: 2
  neutralizacao_afetiva: 2
  monumentalizacao: 3

notes: "Atribuições dependem de confirmação imagética; manter como piloto até localizar fonte de imagem e verificar metadados." 
```

## 18. Regras de versionamento e governança

O versionamento é tratado como mecanismo de transparência do trabalho interpretativo, pois categorias e pesos são construídos e devem permanecer revisáveis até o freeze formal, evitando que o dataset adquira aparência de neutralidade e fechamento prematuro.[^1][^2]

### 18.1 Incrementos

- **MAJOR (3.0.0):** mudança estrutural que invalida codificações anteriores e exige reanotação ampla, reconhecendo que a infraestrutura classificatória molda o que se pode ver e inferir.[^2]
- **MINOR (2.1.0):** novos campos/valores sem reanotar o legado, documentando expansão como trabalho incremental e preservando rastreabilidade da construção do capta.[^3]
- **PATCH (2.0.1):** correções textuais sem alteração semântica, para manter consistência operacional sem reclassificação substantiva.[^3]

### 18.2 Freeze

Estados de freeze (placeholder do piloto): `pre_freeze` (atual) → `freeze_candidate` → `freeze` (com hash SHA-256 do arquivo) → `unfreeze` (apenas por erro crítico), pois a estabilidade deve ser um evento governado e rastreável e não um efeito retórico de “simplicidade”.[^2]

Critério recomendado para `freeze_candidate`: ao menos 50 itens codificados e auditoria intercodificador com limiar mínimo (lacuna na base de evidência: busca neste piloto para definição métrica e protocolo), dado que a interpretação de signos é dependente de contextos e intenções e, portanto, exige teste de consistência entre leitores.[^7]

## 19. Referências

A lista completa em ABNT deve ser mantida no repositório em arquivo bibliográfico (para rastreabilidade), incluindo Ripa como “handbook” influente de alegorias, Resnik & Curtis como referência de iconografia judicial e espaço de adjudicação, e Drucker e D’Ignazio & Klein como base do reenquadramento capta e do princípio “data are not neutral”.[^13][^27][^1][^3]

## 20. Changelog

A tabela abaixo registra apenas a entrada de v2.0.0, pois versões futuras serão documentadas em arquivos separados para preservar rastreabilidade do trabalho e das decisões classificatórias.[^3]

| Versão | Data | Mudança | Re-pontua itens anteriores? |
|---|---|---|---|
| 2.0.0 | 2026-06-22 | Criação do codebook independente versionado; introdução de `status_evidencia`/`score_evidencia`; regra de anacronismo Iconclass; campos específicos para Virtudes (tipo_virtude, funcao_liturgica_vs_estatal, posicao_arquitetonica); campos específicos para Continentes (dimensao_territorial, hierarquia_continental, racializacao_observavel); campos específicos para Oceanos_Rios (corpo_hidrico_nomeado, dimensao_soberania, atributo_gendrado_hidrico); separação racializacao_observavel vs hipotese_racial_interpretativa; decisão de unidade analítica como programa iconográfico. [^3][^2][^12][^21] | Não [^3] |


[^1]: Humanities Approaches to Graphical Display.

[^2]: Why Digital Humanists Should Emphasize Situated Data over ...

[^3]: Mika, 2021. Book Review: Data Feminism. Journal of eScience Librarianship.

[^4]: Lee, 2012. Book Review: Justice For All?.

[^5]: Isiksel, 2013. Representing justice: Invention, controversy and rights in city-states and democratic courtrooms. Contemporary Political Theory.

[^6]: Dennis et al., 2010. Essays Images of Justice.

[^7]: Hayaert, 2018. The Paradoxes of Lady Justice’s Blindfold.

[^8]: Corbeiller, 1961. Miss America and Her Sisters: Personifications of the Four Parts of the World. Metropolitan Museum of Art Bulletin.

[^9]: Tait, 2012. What We Didn’t See Before. Yale journal of law and the humanities.

[^10]: Castañeda, 2023. La Virtud como alegoría de las Virtudes Cardinales. Philostrato Revista de Historia y Arte.

[^11]: Sutton, 2009. Mapping Meaning: Ethnography and Allegory in Netherlandish Cartography, 1570-1655. Itinerario: International Journal on the History of European Expansion and Global Interaction.

[^12]: Bastos, 2009. A maravilhosa fábrica de virtudes: o decoro na arquitetura religiosa de Vila Rica, Minas Gerais (1711-1822).

[^13]: Maffei & Procaccioli, 2012. Cesare Ripa, Iconologia. A cura di Sonia Maffei. Testo stabilito da Paolo Procaccioli.

[^14]: Taylor, 2009. River Raptures: Containment And Control Of Water In Greek And Roman Constructions Of Identity.

[^15]: Nazario, 2026. Quem é a pessoa por trás do rosto nas moedas brasileiras? - Super Rádio Tupi.

[^16]: Jurt, 2014. Brazil: a Nation-state in the Making. Actes De La Recherche En Sciences Sociales.

[^17]: Efígie da República (Brazil) - Eidolon Station, 2026.

[^18]: Akademie. Cesare Ripa »Iconologia«.

[^19]: Emblèmes 1603 : Cesare Ripa, Iconologia... (2e éd.; 1ère éd. illustrée), Rome, L. Facii | Utpictura18.

[^20]: English Translations and Adaptations of Cesare Ripa's Iconologia: From the 17th to the 19th Century Hans-Joachim Zimmermann, De Zeventiende Eeuw. Jaargang 11 - DBNL.

[^21]: Neumann, 2009. Imagining European community on the title page of Ortelius' Theatrum Orbis Terrarum (1570). Word & Image.

[^22]: O Brasil: um Estado-nação a ser contruído. O papel dos símbolos nacionais, do Império à República.

[^23]: Formation of Souls, 2023.

[^24]: Detsi-Diamanti, 2006. Politicizing Aesthetics. Anachronist.

[^25]: Em busca do País das Amazonas: o mito, o mapa, a fronteira.

[^26]: Seagle, 1945. Rudolf von Jhering: Or Law as a Means to an End. University of Chicago Law Review.

[^27]: Spaulding, 2012. Facades of Justice. Michigan law review.