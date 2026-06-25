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
    - Pele_Leao           # NOVO 2.3.0 (atributo herculeo; nota_lacuna)
    - Urna_Vertedora      # NOVO 2.3.0 (vasilha de efluencia hidrica)
    - Vaso_Fluvial        # NOVO 2.3.0 (vasilha fluvial)
    - Tridente_Imperial   # NOVO 2.3.0 (soberania marinha; nota_lacuna)
    - Ancora_Naval        # NOVO 2.3.0 (infraestrutura marinha; nota_lacuna)
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
  classicizante (corpo/pose/vestes). **nota_lacuna** na base de evidencia
  deste piloto.
- `moralizacao`: aplicavel_com_cautela; central para `Hercules` (bivio e
  pedagogia moral). **nota_lacuna** na base de evidencia deste piloto.
- `depuracao_semantica`: aplicavel_com_cautela. **nota_lacuna**.
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

## 13. Referencias (placeholders — verificar ABNT completa antes do freeze)

- Villari, 2015. L\'«Ercole al bivio» di Domenico Beccafumi.
- Bendall, 2022. Female Personifications and Masculine Forms. Gender & History.
- Lazzaro, 2011. River gods. Renaissance Studies.
- Estella, 2002. El llamado Neptuno. Archivo Espanol De Arte.
- Lopez, 2017. La personificacion del mar.
- DezenoveVinte (Martin Chillon). O Genio do Brasil e as Musas.
- orioqueorionaove, 2012. A fachada do IPHAN.
- Immagini della Giustizia: antiporte: Titius.

> **Aviso**: as 8 referencias acima preservam a marcacao `[verificar ABNT
> completa antes do commit]` herdada do rascunho Elicit. O freeze real da
> v2.3.0 depende de normalizacao ABNT completa.
