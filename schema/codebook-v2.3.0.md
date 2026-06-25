---
codebook_id: lpai-v2-3-0
codebook_version: 2.3.0
codebook_version_anterior: 2.2.0
data_versao: "2026-06-25"
status: piloto
freeze_state: pre_freeze_piloto_v230
canonical_schema: tools/schemas/master-record.schema.json
canonical_records: data/processed/records.jsonl
master_vigente: schema/codebook-MASTER.md
documento_pai: data/docs/codebook.md
reenquadramento_epistemico: schema/lpai-v2-as-capta.md
documento_justificativo: schema/adendo-metodologico-v2.3.0.md
patch_origem: schema/codebook-v2.3.0-patch.md
pre_freeze_sample: true
regras_legado:
  - "Itens ja codificados em v2.2.0 NAO sao re-pontuados."
  - "Adocao de Masculino_Juridico e dos novos campos e opcional para legados; registrar codebook_version existente."
gates_tecnicos_para_freeze:
  - "tools/scripts/validate_schemas.py precisa ganhar suporte para: (i) minLength condicional em justificativa_genero quando genero_atribuido==masculino; (ii) interseccao de arrays para condicional substituicao_atributiva_hercules."
  - "Bloco aplicabilidade_por_familia_masculina (5 valores x 10 indicadores = 50 chaves potenciais) ainda nao modelado no schema JSON; ver secao 8."
  - "5 dos 10 indicadores_purificacao marcados nota_lacuna na base de evidencia deste piloto."
  - "8 referencias marcadas [verificar ABNT completa antes do commit]."
autor: Ana Vanzin
licenca: CC-BY-4.0
---

# Codebook LPAI v2.3.0 — patch opcional sobre v2.2.0 (Gramatica masculina)

> **Estado**: **pre_freeze_piloto_v230**. Esta versao **nao** substitui a
> master v2.2.0 (`schema/codebook-MASTER.md`). E um patch candidato que
> introduz uma familia nova (`Masculino_Juridico`), valores novos em
> `objetos_regalia` e `marcas_corporais`, e quatro campos novos opcionais em
> `purificacao`. Registros pre-existentes seguem validos contra o schema
> v2.2.0.

## 1. Capta: continuidade do principio v2.x

O LPAI v2.3.0 mantem a declaracao de capta: scores sao atos interpretativos
situados, nao dados neutros. A expansao da gramatica masculina **nao enfraquece**
essa declaracao; pelo contrario, ela **reforca** o principio ao tornar o
masculino auditavel por marcas e funcoes, em vez de trata-lo como
"default invisivel".

Declaracao recomendada para registros novos:

> LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros.

## 2. Mudancas resumidas vs v2.2.0

| Superficie | Mudanca | Status |
|---|---|---|
| `familia_alegorica` | enum expandido com `Masculino_Juridico` | aplicado no schema JSON |
| `objetos_regalia` | 6 valores novos: `Clava`, `Pele_Leao`, `Urna_Vertedora`, `Vaso_Fluvial`, `Tridente_Imperial`, `Ancora_Naval` | schema JSON usa `string` livre; vocabulario controlado documentado aqui |
| `marcas_corporais` | 6 valores novos: `Barba_Longa`, `Corpo_Ereto_Em_Esforco`, `Corpo_Semirrecosto_Fluvial`, `Musculatura_Exibida`, `Postura_De_Sustentacao`, `Gesto_Indicativo_Pedagogico` | idem |
| `funcao_da_figura_masculina` | novo campo opcional em `purificacao` | aplicado no schema JSON |
| `tipo_agencia_masculina` | novo campo opcional em `purificacao` | aplicado no schema JSON |
| `funcao_atlanteana` | novo campo opcional boolean em `purificacao` | aplicado no schema JSON |
| `tipo_efluencia_hidrica` | novo campo opcional enum em `purificacao` | aplicado no schema JSON |
| `substituicao_atributiva_hercules` | novo campo opcional object em `purificacao` | aplicado no schema JSON |
| `subtipo` por familia `Masculino_Juridico` | `Hercules`, `Atlante_Telamon`, `Rio_Barbado`, `Netuno_Oceanus`, `Genio_Protetor`, `Heroi_Civil`, `Outro_Masculino` | schema JSON usa `string` livre; valores controlados documentados aqui |
| `aplicabilidade_por_familia_masculina` (10 indicadores x 5 valores) | **nao modelado** no schema JSON | apenas YAML editorial, com gate declarado |

## 3. `familia_alegorica` expandido

```yaml
familia_alegorica:
  type: string
  enum:
    - Virtudes
    - Continentes
    - Oceanos/Rios
    - Nacional
    - Outra
    - Masculino_Juridico   # NOVO 2.3.0
```

Quando `familia_alegorica == Masculino_Juridico`, espera-se `subtipo` em um
dos valores abaixo e `genero_atribuido == masculino` (com tolerancia para
`hibrido` em casos de mediação divino-juridica, p.ex., figura jovem
"vestida all'antica" apontando a Justiça).

### 3.1 `subtipo` por familia Masculino_Juridico

| Valor | Descricao | Marcas discriminantes |
|---|---|---|
| `Hercules` | Dispositivo de decisao moral/pedagogica (bivio) | `Clava` ou `Pele_Leao`; opcionalmente `Nudez_Total` ou `Nudez_Parcial`; postura `Corpo_Ereto_Em_Esforco` |
| `Atlante_Telamon` | Suporte arquitetonico/territorial | `Postura_De_Sustentacao`; `Musculatura_Exibida`; opcionalmente `Globo` (sobre ombros) |
| `Rio_Barbado` | Personificacao hidrica masculina | `Barba_Longa` + `Corpo_Semirrecosto_Fluvial` + `tipo_efluencia_hidrica != Sem_Efluencia` |
| `Netuno_Oceanus` | Personificacao marinha masculina | `Tridente_Imperial` ou `Ancora_Naval`; ou `Barba_Longa` + `Ondas_Maritimas` |
| `Genio_Protetor` | Caso brasileiro: guerreiro/protetor nacional | `Cetro` ou `Coroa`; `Corpo_Ereto`; `Substituicao_Atributiva_Hercules` quando aplicavel |
| `Heroi_Civil` | Heroi civil/autoridade masculina | exige `justificativa_genero` >= 80 chars |
| `Outro_Masculino` | Outro; justificar | exige `justificativa_genero` >= 80 chars |

## 4. `objetos_regalia` — valores novos

```yaml
objetos_regalia:
  type: array
  items:
    type: string
  descricao: "Lista controlada de regalias/atributos materiais. Schema JSON aceita string livre; vocabulario controlado abaixo."
  vocabulario_controlado_v230:
    - Clava               # NOVO 2.3.0 (atributo herculeo)
    - Pele_Leao           # NOVO 2.3.0 (atributo herculeo; ver §14 lacuna L1)
    - Urna_Vertedora      # NOVO 2.3.0 (vasilha de efluencia hidrica)
    - Vaso_Fluvial        # NOVO 2.3.0 (vasilha fluvial)
    - Tridente_Imperial   # NOVO 2.3.0 (soberania marinha; ver §14 lacuna L2)
    - Ancora_Naval        # NOVO 2.3.0 (infraestrutura marinha; ver §14 lacuna L3)
```

## 5. `marcas_corporais` — valores novos

```yaml
marcas_corporais:
  type: array
  items:
    type: string
  vocabulario_controlado_v230:
    - Barba_Longa                  # NOVO 2.3.0 (significante hegemonico de autoridade)
    - Corpo_Ereto_Em_Esforco       # NOVO 2.3.0 (decisao/impulso, p.ex. Hercules no bivio)
    - Corpo_Semirrecosto_Fluvial   # NOVO 2.3.0 (tipo aquatico barbado)
    - Musculatura_Exibida          # NOXO 2.3.0 (herculeas/atlanteanas)
    - Postura_De_Sustentacao       # NOVO 2.3.0 (atlantes)
    - Gesto_Indicativo_Pedagogico  # NOVO 2.3.0 (mediacao divino-juridica)
```

## 6. Novos campos em `purificacao` (todos opcionais nesta rodada)

```yaml
funcao_da_figura_masculina:
  type: string
  enum:
    - Pedagogia_Do_Bivio
    - Suporte_Arquitetonico
    - Delimitacao_Territorial
    - Protetorado_Nacional
    - Soberania_Maritima
    - Mediacao_Divino_Juridica
    - Outro
  obrigatorio_apos_migracao: true  # gate para promover a obrigatorio
  gate_tecnico: "validate_schemas.py precisa suportar required-when enum"

tipo_agencia_masculina:
  type: string
  enum:
    - Pedagogia_Do_Bivio
    - Suporte_Arquitetonico
    - Delimitacao_Territorial
    - Protetorado
    - Soberania_Maritima
    - Mediacao_Divino_Juridica
    - Outro

funcao_atlanteana:
  type: boolean
  condicional_editorial: "subtipo == Atlante_Telamon"

tipo_efluencia_hidrica:
  type: string
  enum:
    - Urna_Vertedora
    - Vaso_Inclinado
    - Sem_Efluencia
    - Outro
  condicional_editorial: "subtipo == Rio_Barbado"

substituicao_atributiva_hercules:
  type: object
  properties:
    atributo_canonico_substituido:
      type: string
    atributo_novo:
      type: string
    justificativa:
      type: string
      maxLength: 300
  required: [atributo_canonico_substituido, atributo_novo, justificativa]
  condicional_editorial: "subtipo == Hercules AND objetos_regalia nao contem Clava"
  gate_tecnico: "validate_schemas.py precisa de interseccao de arrays"
```

## 7. Regra reforcada para `justificativa_genero`

Quando `genero_atribuido == masculino` OU `familia_alegorica == Masculino_Juridico`, o campo `justificativa_genero` (ja existente em v2.2.0) deve ser substantivo (`>= 80` caracteres) e ancorado em marcas observaveis (p.ex., barba longa, postura de sustentacao, semirrecosto fluvial, clava/atributos). Justificativa curta ou ausente deve marcar `confianca_codificacao: baixa`.

**Gate tecnico**: o `tools/scripts/validate_schemas.py` atual nao enforca essa condicional. O freeze real da v2.3.0 depende de upgrade do validador.

## 8. Bloco `aplicabilidade_por_familia_masculina` (NAO no schema JSON)

O rascunho Elicit original definiu, para cada um dos 10 indicadores de
purificacao, um bloco `aplicabilidade_por_familia_masculina` com 5 valores
possiveis:

- `aplicavel`
- `aplicavel_com_cautela`
- `aplicavel_com_subaltern_caution`
- `inverter_polaridade` (regime masculino com enfase de corporeidade pode
  exigir inversao de polaridade do indicador `desincorporacao`)
- `nao_aplicavel` (nao especificado explicitamente, implicito)

**Decisao**: este bloco **nao** foi modelado no schema JSON nesta rodada.
Justificativas:

1. Exigiria 10 propriedades novas por registro, com 5 valores cada.
2. O `tools/scripts/validate_schemas.py` atual nao suporta enums aninhados
   com essa profundidade.
3. 5 dos 10 indicadores (`classicizacao`, `moralizacao`, `depuracao_semantica`,
   `neutralizacao_afetiva`, `monumentalizacao`) tem `nota_lacuna` na base de
   evidencia deste piloto; modelar antes da evidencia so geraria falsos
   positivos.
4. A autora (Ana Vanzin) autorizou **quebrar o schema** nesta frente para
   avancar com os 4 campos opcionais ja validados (semanticamente e
   estruturalmente) e deixar o bloco de aplicabilidade como pendencia
   declarada.

O bloco permanece documentado aqui como **referencia editorial** e sera
avaliado para freeze numa futura v2.4.0 ou v3.0.0.

## 9. Indicadores_purificacao — observacoes da v2.3.0

Quando `familia_alegorica == Masculino_Juridico`:

- `desincorporacao`: pode exigir `inverter_polaridade` (Herculeas/atlanteanas
  com forte corporeidade nao estao em movimento de "desincorporacao").
  Gate: a sub-linhagem e o subtipo determinam a polaridade. Aplicar com
  cautela e registrar em `notes`.
- `heraldizacao`: aplicavel, com cautela para `Hercules` (programa
  monumental/imperial).
- `enquadramento_arquitetonico`: aplicavel; central para `Atlante_Telamon`.
- `serialidade`: aplicavel; cautela para `Hercules` (programa monumental
  pode nao ser seriado).
- `inscricao_estatal`: aplicavel; alta para `Genio_Protetor` em programas
  imperiais; cautela para casos contestados.
- `classicizacao`: aplicavel; mensurar intensidade de idealizacao
  classicizante (corpo/pose/vestes). **nota_lacuna** (ver §14 lacuna L4).
- `moralizacao`: aplicavel_com_cautela; central para `Hercules` (bivio e
  pedagogia moral). **nota_lacuna** na base de evidencia deste piloto.
- `depuracao_semantica`: aplicavel_com_cautela. **nota_lacuna** (ver §14 lacuna L5).
- `neutralizacao_afetiva`: aplicavel_com_cautela. **nota_lacuna**.
- `monumentalizacao`: aplicavel_com_cautela; alta para `Rio_Barbado` em
  programas imperiais (estatuas colossais); **nota_lacuna** para o resto.

## 10. Plano de migracao (resumo)

1. Itens ja codificados em v2.2.0 permanecem validos.
2. Identificar candidatos a migracao para `Masculino_Juridico` por marcas
   claras (clava/nudez; postura de suporte; barba+semirrecosto+urna; gesto
   indicativo).
3. Migrar primeiro itens com `genero_atribuido == masculino` para preencher
   `justificativa_genero` >= 80 chars.
4. Em Hercules sem `Clava`, preencher `substituicao_atributiva_hercules`.
5. Rios personificados: priorizar "sentado e recostado" para testar
   coocorrencia (barba+semirrecosto+efluencia).
6. Gatilho de v3.0.0: caso masculinidades afro-brasileiras/indigenas demandem
   familia autonoma nao subordinada ao eixo classico.

## 11. Exemplo de registro v2.3.0 (piloto)

```yaml
item_id: LPAI-0004-v230  # exemplo piloto, nao inserir em records.jsonl nesta rodada
titulo: Genio do Brasil (programa imperial com referencia herculea)
suporte: frontispicio
codebook_version: "2.3.0"
pre_freeze_sample: true
familia_alegorica: Masculino_Juridico
subtipo: Genio_Protetor
objetos_regalia: [Cetro, Coroa]
marcas_corporais: [Corpo_Ereto]
genero_atribuido: masculino
justificativa_genero: >
  Fonte descreve explicitamente o Genio como "masculino e ativo"; figura com
  postura majestica e cetro/vara como elemento de poder, em contraste com
  representacoes femininas passivas.
funcao_da_figura_masculina: Protetorado_Nacional
tipo_agencia_masculina: Protetorado
substituicao_atributiva_hercules:
  atributo_canonico_substituido: Clava
  atributo_novo: Cetro_Ou_Vara
  justificativa: "Texto descreve que o cetro se converterá em vara e será manejado como Hercules a sua clava."
finalidade_atribuida: legitimacao_juridica
status_evidencia: piloto
```

## 12. Glossario minimo (verbetes curtos)

- **Masculino_Juridico**: familia iconografica introduzida na v2.3.0 para
  sistematizar a gramatica masculina em contexto estatal/juridico,
  evitando que `genero_atribuido = masculino` opere como default invisivel.
- **Bivio erculeo**: episodio canonico do Hercules no momento da escolha
  entre virtude e vicio; funciona como gramatica de decisao moral/cognitiva.
- **Substituicao_Atributiva_Hercules**: ponte inferencial que torna
  auditavel a identificacao herculea sem o atributo canonico (clava)
  estar materialmente presente (p.ex., cetro/vara manejados "como Hercules
  a sua clava").
- **Atlante/Telamon**: coluna antropomorfica sustentando peso; por extensao,
  qualquer figura masculina em postura de suporte arquitetonico/territorial.
- **Rio_Barbado**: tipo aquatico masculino definido pela triade barba longa
  + corpo semirrecosto + efluencia hidrica visivel. Coocorrencia obrigatoria.
- **Netuno_Oceanus**: figura marinha masculina canonica da tradicao ocidental;
  em chave bizantina, contraparte feminina e Thetis (registrar como
  `Tetis` em `Oceanos/Rios`).

## 13. Referencias (formato ABNT NBR 6023:2025)

Movimento 3 do freeze plan (commit cc0bb31 "Bloqueios para freeze real").
5 das 8 refs foram normalizadas via busca em `api.crossref.org` e
`api.openalex.org` (Movimento 3.4); 3 refs marcadas como
`nota_lacuna_bibliografica` para a proxima rodada Elicit (mesmo principio
das 5 lacunas de §14).

### 13.1. Referencias normalizadas (5)

VILLARI, Susanna. **L'«Ercole al bivio» di Domenico Beccafumi
(1486-1551) e l'Ercole giraldiano**. *Studi giraldiani. Letteratura e
teatro*, Milano, v. 1, n. 0, p. 69-110, 2015.
DOI: 10.6092/2421-4191/2015.1.69-110. Disponivel em:
https://doi.org/10.6092/2421-4191/2015.1.69-110. Acesso em: 25 jun. 2026.

BENDALL, Sarah A. **Female Personifications and Masculine Forms: Gender,
Armour and Allegory in the Habsburg-Valois Conflicts of Sixteenth-Century
Europe**. *Gender & History*, Hoboken, v. 35, n. 1, p. 42-67, 2023.
DOI: 10.1111/1468-0424.12592. Disponivel em:
https://doi.org/10.1111/1468-0424.12592. Acesso em: 25 jun. 2026.

LAZZARO, Claudia. **River gods: personifying nature in sixteenth-century
Italy**. *Renaissance Studies*, Hoboken, v. 25, n. 1, p. 70-94, 2011.
DOI: 10.1111/j.1477-4658.2010.00708.x. Disponivel em:
https://doi.org/10.1111/j.1477-4658.2010.00708.x. Acesso em: 25 jun. 2026.

ESTELLA, Margarita M. **El llamado Neptuno (Rio?) de la Coleccion del
Carpio y su problematica identificacion con una obra atribuida a Bernini,
en Aranjuez**. *Archivo Espanol de Arte*, Madrid, v. 75, n. 298,
p. 117-128, 2002. DOI: 10.3989/aearte.2002.v75.i298.343. Disponivel em:
https://doi.org/10.3989/aearte.2002.v75.i298.343. Acesso em: 25 jun. 2026.

RODRIGUEZ LOPEZ, Maria Isabel. **La personificacion del mar: Evolucion
y transformaciones iconograficas del mundo clasico al medioevo**.
*Revista digital de iconografia medieval*, Madrid, v. 9, n. 17,
p. 125-140, 2017. ISSN: 2254-7312. Disponivel em:
https://dialnet.unirioja.es/servlet/articulo?codigo=6058727.
Acesso em: 25 jun. 2026.

### 13.2. Referencias com `nota_lacuna_bibliografica` (3)

As 3 referencias abaixo foram marcadas com `[verificar ABNT completa antes
do commit]` no rascunho Elicit e **nao foram encontradas** em
crossref/openalex/google scholar no piloto de 2026-06-25. Seguem o mesmo
principio das 5 `nota_lacuna` de §14: registrar a lacuna em vez de
inventar dados bibliograficos. A promocao da v2.3.0 a `master_record`
**nao depende** destas 3 (sao fontes secundarias para casos brasileiros),
mas a proxima rodada Elicit (julho-agosto 2026) deve cobri-las.

#### 13.2.1. CHILLON, Alberto Martin. **O Genio do Brasil e as Musas: um
manifesto ideologico numa nacao em construcao**. *19&20* (DezenoveVinte),
Sao Paulo, [data a verificar], [volume/issue/pags a verificar].
**nota_lacuna_bibliografica**: URL provavel
`https://www.dezenove20.com.br/` (site ativo, mas artigo especifico nao
indexado em crossref/openalex em 2026-06-25). Substituir por citacao
completa apos busca dirigida.

#### 13.2.2. **[Autor a verificar]** (orioqueorionaove). **A fachada do
IPHAN**. *O Rio que o rio nao ve*, Rio de Janeiro, 2012.
**nota_lacuna_bibliografica**: blog/site sem DOI, sem ISSN, sem autor
formal identificado. URL: `http://orioqueorionaove.com` (confirmada ativa
em 2026-06-25 com tag "fachada" e tag "IPHAN"). Conteudo relevante para
atlantes/companhias de navegacao. Substituir por citacao completa apos
contato com o autor ou migracao para formato academico.

#### 13.2.3. **ALUCINACAO SUSPEITA** -- "[Titius, Observationum
ratiocinantium ... (1)]" / "Immagini della Giustizia: antiporte".
**nota_lacuna_bibliografica + flag de qualidade**: crossref e openalex
**nao retornaram correspondencia exata** com esta referencia em
2026-06-25. Crossref retornou 20 itens sobre "Immagini di giustizia"
mas nenhum casa com o titulo do codebook. Titius pode ser errata de
Titian (Ticiano) ou autor real mas obscuro. **Recomendacao**: **remover**
do codebook ate verificacao independente. Se for genuina, re-adicionar
com citacao completa apos busca em arquivo italiano (BMC, Archivio di
Stato). Se for alucinacao do Elicit (improvavel mas possivel),
a remocao documenta o controle de qualidade.

### 13.3. Notas sobre a normalizacao

- **DOI优先**: refs com DOI sao citadas优先 pelo DOI (ABNT NBR 6023:2025,
  §7.7.1) por serem identificadores permanentes; URL e data de acesso
  sao complementares.
- **Local de publicacao inferido**: para journals academicos, o local
  frequentemente vem do publisher (Hoboken = Wiley; Madrid = CSIC para
  Archivo Espanol de Arte). Marcado como inferido quando nao declarado
  explicitamente no metadata; pode ser corrigido em revisao futura.
- **Errata do rascunho Elicit**: o rascunho marcava a ref Bendall como
  "2022"; a publicacao efetiva foi 2023 (DOI resolution confirma). O
  codebook v2.3.0 usa 2023 como ano correto.
- **Ref Lopez foi expandida**: o rascunho Elicit registrava so "Lopez,
  2017"; a busca revelou autora completa (Maria Isabel Rodriguez Lopez)
  e periodico (Revista digital de iconografia medieval). Citacao
  significativamente mais robusta.


## 14. Lacunas documentadas (nota_lacuna)

Este patch (v2.3.0) foi promovido a `pre_freeze_piloto_v230` com **5 lacunas
explicitamente documentadas** em vez de tapadas com "evidencia fraca". Cada
lacuna abaixo representa um item onde a busca Elicit deste piloto nao
produziu evidencia direta suficiente para um freeze real; a decisao
consciente e registrar a lacuna, nao inventar conteudo.

A promocao a `master_record` (v2.3.0 efetiva) depende de a proxima rodada
Elicit cobrir, no minimo, **L1, L2, L3** (os 3 valores enum novos de
`objetos_regalia`, sem os quais os campos viram "etiquetas sem lastro
operacional"). **L4, L5** (indicadores) sao nice-to-have para v2.4.0.

### L1. `Pele_Leao` (atributo herculeo)

- **Onde aparece**: enum `objetos_regalia` em `purificacao`.
- **Por que e lacuna**: o atributo iconografico e central para a gramatica
  herculea (nudez + clava + pele), porem a busca Elicit deste piloto nao
  produziu fontes primarias brasileiras que registrem uso iconografico
  direto em programas imperiais ou republicanos.
- **Sub-linhagem afetada**: Hercules juridico (adendo §2).
- **Recomendacao v2.4.0+**: busca dirigida em Portinari, Debret, Rugendas
  e iconografia monumental brasileira (Caxias, Tamandare, etc.).

### L2. `Tridente_Imperial` (soberania marinha)

- **Onde aparece**: enum `objetos_regalia` em `purificacao`.
- **Por que e lacuna**: marcador canonico de Netuno/Oceanus em programas
  imperiais ocidentais; no entanto, a busca Elicit deste piloto nao
  confirmou uso em programas imperiais brasileiros (moeda, selo, brasao).
- **Sub-linhagem afetada**: Netuno e soberania maritima (adendo §5).
- **Recomendacao v2.4.0+**: busca em colecao Numista + Rijksmuseum (ja ha
  18 imagens re-adquiridas em 2026-06-04 que podem cobrir parcialmente).

### L3. `Ancora_Naval` (infraestrutura marinha)

- **Onde aparece**: enum `objetos_regalia` em `purificacao`.
- **Por que e lacuna**: marcador de "ancoragem simbolica" do Estado no
  territorio maritimo; faltam fontes primarias que mostrem Ancora_Naval
  como atributo iconografico autonomo (vs. mero elemento decorativo).
- **Sub-linhagem afetada**: Atlantes/telamones + soberania maritima
  (adendo §3, §5).
- **Recomendacao v2.4.0+**: cruzar com frontispicios de atlas portuarios
  brasileros (século XIX) e emblemas da marinha.

### L4. `classicizacao` (indicador de purificacao)

- **Onde aparece**: lista `indicadores_purificacao` (ordinal 0-3).
- **Por que e lacuna**: o indicador pretende mensurar intensidade de
  idealizacao classicizante (corpo nu, pose conotativa, vestes all'antica),
  mas faltam criterios operacionais para pontuar 0/1/2/3 de forma
  reprodutivel entre codificadores.
- **Sub-linhagem afetada**: transversal a Hercules + Atlantes + Rio_Barbado.
- **Recomendacao v2.4.0+**: calibracao IRR (inter-rater reliability) com
  2-3 codificadores em N=20 registros pre-selecionados.

### L5. `depuracao_semantica` (indicador de purificacao)

- **Onde aparece**: lista `indicadores_purificacao` (ordinal 0-3).
- **Por que e lacuna**: o indicador visa capturar a "limpeza semantica" pela
  qual uma figura particular (mulher guerreira, genio nacional) e
  despolitizada em pura abstracao (Justica, Patria). A teoria esta clara
  (Warner, Drucker); falta ancora operacional para a pontuacao.
- **Sub-linhagem afetada**: transversal, especialmente Genio do Brasil
  (adendo §6).
- **Recomendacao v2.4.0+**: tabela de exemplos canonicos com pontuacao
  esperada; rodar IRR piloto para calibrar.

### Justificativa epistemologica do freeze com lacunas

A decisao de promover v2.3.0 com 5 lacunas documentadas em vez de tapalas
segue o principio **capta** (Drucker): dados sao tomados e construidos,
nao encontrados. Inventar conteudo para fechar lacunas seria pior do que
registra-las, porque:

1. A `validate_schemas.py`升级 (commit 49caba3) **emite warnings** para
   usos problematicos (HERCULES_INCOERENTE, JUSTIFICATIVA_CURTA), nao
   bloqueia. Promover lacunas a "conteudo provisorios" sem lastro violaria
   o proprio principio que o codebook encarna.
2. A consulta Elicit deste piloto foi desenhada para validar a *estrutura*
   do patch (5 campos novos, regra de genero, validacao), nao para
   esgotar a evidencia de cada valor enum. Esgotar evidencia e trabalho
   da v2.4.0+.
3. O `pre_freeze_piloto_v230` e honesto: o corpus pode ser codificado com
   os campos novos **vazios** (opcionais), e os registros que usam
   L1/L2/L3/L4/L5 ficam sinalizados para tratamento prioritario.

Refs:
  - commit 49caba3 (validator升级 com 3 regras condicionais)
  - commit cc0bb31 (patch v2.3.0 original; "Bloqueios para freeze real")
  - docs/decisions/2026-06-25-lacunas-v2.3.0.md (ADR formal deste registro)
