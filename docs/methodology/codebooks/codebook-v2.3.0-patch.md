---
documento: codebook-patch
versao_anterior: 2.2.0
versao_alvo: 2.3.0
data: "2026-06-25"
autor: "Ana Vanzin (consolidacao a partir do rascunho Elicit)"
escopo: "patch minor opcional; nao re-pontua itens anteriores"
documento_justificativo: schema/adendo-metodologico-v2.3.0.md
schema_json_canonico: tools/schemas/master-record.schema.json
codebook_editorial_vigente: schema/codebook-MASTER.md
companheiros:
  - schema/codebook-v2.3.0.md
origem_externa:
  fonte: "Elicit - CHANGELOG Patch v2.2.0 -> v2.3.0 (Gramatica Masculina)"
  data_importacao: "2026-06-25"
  observacao: "snake_case -> PascalCase; bloco 'aplicabilidade_por_familia_masculina' nao vai pro schema JSON nesta rodada (apenas YAML editorial)."
freeze_state: pre_freeze_piloto_v230
---

# Patch CHANGELOG v2.2.0 -> v2.3.0 (opcional) — Codebook LPAI v2 (Gramatica masculina)

> **Status**: patch **candidato** sobre a master v2.2.0. Nao e master
> vigente. A consolidacao master segue em [`schema/codebook-MASTER.md`](codebook-MASTER.md)
> ate decisao explicita de promover a v2.3.0.

## 1. Motivacao

Este patch formaliza, no schema LPAI, uma **gramatica masculina** de alegoria
juridico-estatal como contraponto sistematico ao foco predominante na
alegoria feminina (Warner), de modo a nao tratar `genero_atribuido =
masculino` como valor "neutro" ou residual, mas como construcao
iconografica reconhecivel por marcas e funcoes recorrentes.[^1][^2]

As mudancas se organizam em cinco motivos principais (com referencia ao
documento-pai justificativo [`schema/adendo-metodologico-v2.3.0.md`](adendo-metodologico-v2.3.0.md)):

- **Hercules juridico** como dispositivo de decisao moral/pedagogica (bivio) e como gramatica de autoridade por forca, reconhecivel por nudez/clava e postura de duvida/impulso, alem de recontextualizacoes luso-brasileiras (cetro -> vara -> clava).[^3][^4][^5]
- **Atlantes/telamones** como operadores de sustentacao arquitetonica/territorial (colunas antropomorficas) e como simbolo de "trazer o mundo junto" (infraestrutura/circulacao), justificando campos para suporte/carga e funcao de sustentacao.[^5][^6]
- **Deuses fluviais barbados** como tipo aquatico masculino (barba + semirrecosto + urna vertente) e como contraparte masculina de imagens femininas de abundancia, exigindo regra de coocorrencia para evitar que "barba" seja confundida com mera hierarquia generica de autoridade.[^3][^1]
- **Netuno e soberania maritima** como campo em que a personificacao do meio marinho nao tem genero fixo (Ocidente/Oceanus masculino versus Bizancio/Thetis feminina) e sofre transformacoes semanticas, requerendo cautela e justificativa de genero em subtipos maritimos.[^7][^8]
- **Casos brasileiros masculinos** (Genio do Brasil; Amazonas/Prata como rios colossais delimitadores) em que a masculinidade aparece explicitamente como agencia politica (guerreiro/protetor; instrumento de poder; delimitacao territorial por rios), exigindo campo de funcao/agencia alem do rotulo de genero.[^8][^5][^7]

## 2. Resumo do diff conceitual

A tabela abaixo sumariza, de forma operacional, os campos afetados, o tipo de
mudanca e a justificativa por sub-linhagem com base na evidencia disponivel.

| Campo | Status | Sub-linhagem justificativa | Obrigatoriedade |
|---|---|---|---|
| `familia_alegorica` | modificado (novo valor) | Teoria do masculino como gramatica (nao "default"): adicionar `Masculino_Juridico` ao enum. | requerido (campo ja obrigatorio; enum expandido) |
| `subtipo` | modificado (valores por familia) | Distinguir `Hercules`, `Atlante_Telamon`, `Rio_Barbado`, `Netuno_Oceanus`, `Genio_Protetor`, `Heroi_Civil`, `Outro_Masculino`. | requerido (ja obrigatorio; validacao por familia) |
| `objetos_regalia` | modificado (enum estendido) | Hercules exige `Clava`; rios/Netuno exigem registro de `Urna_Vertedora` / `Vaso_Fluvial`; soberania maritima demanda `Ancora_Naval` / `Tridente_Imperial` como regalia possivel.[^3] + lacuna para parte "Pele_Leao / Ancora_Naval / Tridente_Imperial" (busca neste piloto). | opcional (lista; valores novos adicionados ao vocabulario) |
| `marcas_corporais` | modificado (enum estendido) | `Barba_Longa`, `Corpo_Semirrecosto_Fluvial`, `Postura_De_Sustentacao`, `Musculatura_Exibida`, `Corpo_Ereto_Em_Esforco`, `Gesto_Indicativo_Pedagogico`.[^3][^1][^6][^2] | opcional (lista; novos valores adicionados) |
| `referencia_genealogica` | modificado (novas chaves) | Placeholders para `panofsky_hercules_am_scheidewege` (ja usado), `brazilian_republican_iconography` (placeholder). | opcional (lista de chaves) |
| `justificativa_genero` | regra (reforco de uso) | "Barba" como significante hegemonico de masculinidade e autoridade indica que genero nao deve ser codificado como intuicao; exige justificativa substantiva tambem para masculino. | condicional (regra: `>= 80` caracteres quando `genero_atribuido == masculino` OU `familia_alegorica == Masculino_Juridico`). **Gate tecnico**: enforce depende de upgrade do `validate_schemas.py` para checar minLength condicional. |
| `funcao_da_figura_masculina` | novo | Masculino como dispositivo de decisao/conhecimento (bivio) e mediacao (figura intermediaria indicando Justica), suporte (atlantes) e agencia (guerreiro/protetor; delimitacao territorial por rios). | opcional nesta rodada; planeja-se tornar obrigatorio apos migracao dos candidatos. |
| `tipo_agencia_masculina` | novo | Casos brasileiros explicitam agencia (guerreiro/protetor; instrumento de poder/uniao). | opcional nesta rodada. |
| `funcao_atlanteana` | novo (bool) | Verdadeiro quando a figura masculina cumpre funcao explicita de suporte/sustentacao (arquitetonica ou simbolica). | opcional; condicionada por subtipo `Atlante_Telamon` no codebook editorial. |
| `tipo_efluencia_hidrica` | novo (enum) | Distingue `Urna_Vertedora`, `Vaso_Inclinado`, `Sem_Efluencia`, `Outro` em personificacoes aquaticas. | opcional; condicionada por subtipo `Rio_Barbado` no codebook editorial. |
| `substituicao_atributiva_hercules` | novo (object) | Torna auditavel a ponte inferencial quando o atributo canonico (`Clava`) nao esta materialmente presente, mas o paratexto opera a transposicao (cetro -> vara -> clava). | opcional; condicionada a `subtipo == Hercules AND objetos_regalia nao contem Clava` no codebook editorial. **Gate tecnico**: enforce depende de upgrade do `validate_schemas.py` para condicional com interseccao de arrays.[^12] |

## 3. Mudancas em campos existentes

### 3.1 `familia_alegorica` (enum expandido)

**ANTES (v2.2.0)**

```yaml
familia_alegorica:
  type: string
  enum:
    - Virtudes
    - Continentes
    - Oceanos/Rios
    - Nacional
    - Outra
```

**DEPOIS (v2.3.0)**

```yaml
familia_alegorica:
  type: string
  enum:
    - Virtudes
    - Continentes
    - Oceanos/Rios
    - Nacional
    - Outra
    - Masculino_Juridico   # NOVO em 2.3.0
```

### 3.2 `objetos_regalia` (valores novos adicionados ao vocabulario)

Adicoes ao vocabulario controlado:

- `Clava` (NOVO 2.3.0) — atributo herculeo.[^3]
- `Pele_Leao` (NOVO 2.3.0) — atributo herculeo; nota_lacuna na base de evidencia deste piloto.
- `Urna_Vertedora` (NOVO 2.3.0) — vasilha/urna associada a efluencia hidrica em personificacoes aquaticas.
- `Vaso_Fluvial` (NOVO 2.3.0) — vaso/vasilha associada a rio/deus fluvial.
- `Tridente_Imperial` (NOVO 2.3.0) — tridente em chave de soberania/insignia; nota_lacuna.
- `Ancora_Naval` (NOVO 2.3.0) — ancora como marcador de soberania marinha/infraestrutura; nota_lacuna.

### 3.3 `marcas_corporais` (valores novos adicionados)

- `Barba_Longa` (NOVO 2.3.0) — marcador de masculinidade/autoridade; pode operar como significante hegemonico.
- `Corpo_Ereto_Em_Esforco` (NOVO 2.3.0) — postura de impulso/decisao (p.ex., Hercules no bivio).
- `Corpo_Semirrecosto_Fluvial` (NOVO 2.3.0) — postura de semirrecosto tipica do tipo aquatico (rio/mar) barbado.
- `Musculatura_Exibida` (NOVO 2.3.0) — enfase de corporeidade/forca (frequente em gramaticas herculeas/atlanteanas).
- `Postura_De_Sustentacao` (NOVO 2.3.0) — postura que indica suporte/carga (atlantes/telamones).
- `Gesto_Indicativo_Pedagogico` (NOVO 2.3.0) — gesto de indicar/mediar entre esfera divina e do direito.

## 4. Novos campos opcionais (v2.3.0)

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
  descricao: >
    Funcao explicita da figura masculina em contexto juridico-estatal. Torna
    auditavel a agencia masculina (decisao/conhecimento, suporte, delimitacao,
    protetorado, soberania, mediacao) sem depender apenas do rotulo de genero.
  exemplo: Protetorado_Nacional
  notas_v230: "Opcional nesta rodada. Promover a obrigatorio apos migracao dos candidatos."

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
  descricao: >
    Tipo especifico de agencia masculina, util para casos brasileiros em que a
    fonte descreve explicitamente o masculino como ativo (guerreiro/protetor)
    e como instrumento de poder/uniao.
  exemplo: Protetorado

funcao_atlanteana:
  type: boolean
  descricao: >
    Verdadeiro quando a figura masculina cumpre funcao explicita de
    suporte/sustentacao (arquitetonica ou simbolica), como colunas
    antropomorficas e Atlas como suporte do globo.
  exemplo: true
  notas_v230: "Condicionada a subtipo == Atlante_Telamon no codebook editorial (gate tecnico: enforce depende de validate_schemas.py)."

tipo_efluencia_hidrica:
  type: string
  enum:
    - Urna_Vertedora
    - Vaso_Inclinado
    - Sem_Efluencia
    - Outro
  descricao: >
    Tipo de efluencia hidrica em personificacoes aquaticas; operacionaliza a
    regra de que barba isolada nao basta para inferir rio, exigindo
    efluencia/vaso como traco discriminante.
  exemplo: Urna_Vertedora
  notas_v230: "Condicionada a subtipo == Rio_Barbado no codebook editorial."

substituicao_atributiva_hercules:
  type: object
  properties:
    atributo_canonico_substituido:
      type: string
      example: Clava
    atributo_novo:
      type: string
      example: Cetro_Ou_Vara
    justificativa:
      type: string
      maxLength: 300
      example: "Paratexto descreve manejo do cetro como clava."
  required: [atributo_canonico_substituido, atributo_novo, justificativa]
  descricao: >
    Registra identificacao herculea por substituicao atributiva
    (p.ex., cetro/vara manejado "como Hercules a sua clava"), tornando
    auditavel a ponte inferencial quando o atributo canonico nao esta visivel
    no suporte.
  notas_v230: "Condicionada a subtipo == Hercules AND objetos_regalia nao contem Clava (gate tecnico).[^12]"
```

## 5. Bloco `aplicabilidade_por_familia_masculina` (apenas YAML editorial)

> **Gate tecnico declarado**: o codebook-patch original do Elicit introduz um
> bloco `aplicabilidade_por_familia_masculina` em cada indicador_purificacao
> com valores `aplicavel`, `aplicavel_com_cautela`,
> `aplicavel_com_subaltern_caution` e `inverter_polaridade`. Este bloco **nao
> e modelado no schema JSON nesta rodada** porque: (i) exigiria 10x4 = 40
> propriedades novas por registro; (ii) o `tools/scripts/validate_schemas.py`
> atual nao suporta enums aninhados com essa profundidade; (iii) 5 dos 10
> indicadores tem `nota_lacuna` na base de evidencia deste piloto. O bloco
> permanece no YAML editorial `schema/codebook-v2.3.0.md` para revisao futura,
> mas o schema JSON nao o enforca. **Decisao consciente de quebrar escopo
> controlado**: a opcao por quebrar o schema foi declarada e aprovada pela
> autora.

## 6. Migracao de registros pre-existentes

A migracao e incremental e orientada por identificacao de candidatos, priorizando itens onde as marcas visuais estao claramente descritas (clava/nudez; postura de suporte; barba+semirrecosto+urna; gesto indicativo), pois esses padroes sao os melhor suportados na evidencia disponivel.[^3][^6][^2]

- Itens ja codificados em v2.2.0 **nao sao re-pontuados**; a adocao de `Masculino_Juridico` e dos novos campos e opcional para legados (registrar `coded_in_version: 2.2.0` no campo `codebook_version` existente).
- Recomenda-se migrar primeiro itens com `genero_atribuido = masculino` para preencher `justificativa_genero` de forma substantiva, dado que a masculinidade aparece como sistema de distincao e poder (p.ex., barba).[^1]
- Em itens marcados como `Hercules` sem `Clava` em `objetos_regalia`, preencher `substituicao_atributiva_hercules` quando a identificacao se apoiar em transposicao textual (cetro -> vara -> clava).[^4]
- Para itens com rios personificados, priorizar aqueles com evidencia de postura de recosto e atributos (p.ex., "sentado e recostado") para testar a regra de coocorrencia e evitar confundir barba/autoridade com "rio".[^6][^1]
- Gatilho potencial de v3.0.0: caso a inclusao de masculinidades afro-brasileiras/indigenas demande familia autonoma nao subordinada ao eixo classico (Hercules/Atlas/river-god), por insuficiencia estrutural do enum atual; lacuna na base de evidencia (busca neste piloto).[^8]

## 7. Lacunas declaradas

As lacunas abaixo sao declaradas explicitamente para orientar busca adicional antes de qualquer freeze do v2.3.0.

- Duque de Caxias em profundidade (iconografia e funcao juridico-estatal): lacuna na base de evidencia (busca neste piloto).[^5]
- Deuses fluviais especificos do papel-moeda brasileiro e/ou selos oficiais (alem de descricoes textuais de programas e festividades): lacuna na base de evidencia (busca neste piloto).[^6][^7]
- Masculinidades afro-brasileiras (p.ex., Exu, Ogum) e seu encaixe (ou nao) na gramatica "Masculino_Juridico": lacuna na base de evidencia (busca neste piloto).[^8]
- Masculinidades indigenas em iconografia estatal/juridica brasileira: lacuna na base de evidencia (busca neste piloto).[^7]
- Panofsky e a bibliografia canonica sobre "Hercules am Scheidewege" aplicada a frontispicios normativos/estatais: lacuna na base de evidencia (busca neste piloto).[^5]
- Atlantes em portais manuelinos e sua transmissao para fachadas coloniais brasileiras e palacios republicanos: lacuna na base de evidencia (busca neste piloto).[^6]
- Criterios de distincao "rio barbado" vs "mar barbado" (Netuno/Oceanus) quando o suporte nao nomeia o corpo d\'agua: lacuna na base de evidencia (busca neste piloto).[^3][^8]
- Validacao empirica da aplicacao dos 10 indicadores de purificacao a gramatica masculina (incluindo casos de polaridade invertida em `desincorporacao`): lacuna na base de evidencia (busca neste piloto).[^3][^5]
- Regra condicional `substituicao_atributiva_hercules`: exige validador com interseccao de arrays; nao coberto por `tools/scripts/validate_schemas.py` (gate tecnico antes do freeze).[^12]

## 8. Referencias

- [^1]: Immagini della Giustizia: antiporte: Titius, Observationum ratiocinantium ... (1).
- [^2]: Estella, 2002. El llamado Neptuno (Rio?) de la Coleccion del Carpio. Archivo Espanol De Arte.
- [^3]: Villari, 2015. L\'«Ercole al bivio» di Domenico Beccafumi. Ercole giraldiano.
- [^4]: Lazzaro, 2011. River gods: personifying nature in sixteenth-century Italy. Renaissance Studies.
- [^5]: Bendall, 2022. Female Personifications and Masculine Forms: Gender, Armour and Allegory. Gender & History.
- [^6]: 19&20 - O Genio do Brasil e as Musas: Um manifesto ideologico numa nacao em construcao, por Alberto Martin Chillon.
- [^7]: Lopez, 2017. La personificacion del mar: Evolucion y transformaciones iconograficas del mundo clasico al medioevo.
- [^8]: orioqueorionaove, 2012. A fachada do IPHAN | O RIO QUE O RIO NAO VE.
- [^12]: tools/scripts/validate_schemas.py — limitacao documentada para condicionais com interseccao de arrays.

> **Aviso**: referencias preservam a marcacao `[verificar ABNT completa antes
> do commit]` herdada do rascunho Elicit. O freeze da v2.3.0 deve ser
> condicionado a normalizacao ABNT completa.
