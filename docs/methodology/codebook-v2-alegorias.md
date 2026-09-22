# Codebook v2 — Alegorias de Virtudes, Continentes e Oceanos/Rios

**Status:** rascunho v1 para piloto
**Codebook version:** 2.0.0
**Data:** 2026-06-22
**Documento-pai:** `data/docs/codebook.md` (10 indicadores ordinais de purificacao simbolica)
**Reenquadramento metodologico:** `schema/lpai-v2-as-capta.md` — todo output deste codebook e *capta*, nao *data*.

## 1. Escopo e justificativa

Este codebook estende o LPAI v2 para codificar tres novas familias alegoricas que funcionam como **comparador genealogico** e **vetor colonial/racial** do regime iconocratico brasileiro:

- **Virtudes** (Iustitia, Veritas, Prudencia, Fortaleza, Temperanca)
- **Continentes** (Europa, America, Africa, Asia)
- **Oceanos/Rios** (corpos d'agua personificados e sua distribuicao de genero)

A expansao nao amplia o escopo indiscriminadamente. O **corpus core** continua restrito a dispositivos estatais/juridicos brasileiros: brasoes, moedas, cedulas, selos postais, paratextos normativos, arquitetura forense e monumentos publicos. Material europeu, colonial ou comparador latino-americano fica em apendice/comparador.

## 2. Novos campos/categorias

### 2.1 `familia_alegorica`
Familia iconografica predominante do item.

| Valor | Quando usar |
|-------|-------------|
| `Virtudes` | A personificacao e uma virtude cardinal, teologal ou juridica |
| `Continentes` | A personificacao representa um continente ou regiao geografica |
| `Oceanos/Rios` | O objeto trata de corpo d'agua personificado ou simbolizado |
| `Nacional` | Alegoria da nacao/republica/liberdade/patria (uso herdado do codebook anterior) |
| `Outra` | Nenhuma das anteriores; justificar em `notes` |

### 2.2 `subtipo`
Especificacao dentro da familia.

**Virtudes:** `Iustitia`, `Veritas`, `Prudencia`, `Fortaleza`, `Temperanca`, `Justica_e_Paz`, `Esperanca`, `Caridade`, `Fé`, `Fama`, `outra_virtude`.

**Continentes:** `Europa`, `America`, `Africa`, `Asia`, `Brasil`, `outro_continente`.

**Oceanos/Rios:** `Oceano`, `Rio_grande`, `Rio_menor`, `Fonte`, `Netuno`, `Tetis`, `outro_hidrico`.

**Nacional:** `Republica`, `Liberdade`, `Patria`, `Brasil`, `outra_nacional`.

### 2.3 `atributos_iconograficos`
Lista de atributos visiveis presentes na representacao. Usar valores controlados quando possivel; novos atributos devem ser registrados em `CHANGELOG.md` do codebook.

Valores iniciais:

- `balanca`
- `espada`
- `venda`
- `espelho`
- `tocha`
- `globo`
- `cornucopia`
- `cetro`
- `coroa`
- `arco_e_flecha`
- `cabeca_decepada`
- `animais_exoticos`
- `cobra`
- `escorpiao`
- `incensario`
- `coroa_de_junco`
- `urna`
- `tridente`
- `barrete_frigio`
- `fasces`
- `bandeira`
- `ramos_estrelas` (brasao da Republica)
- `corpo_reclinado` (rios classicos)
- `barba` (atributo masculino de rios)
- `ondas_maritimas`
- `outro` (descrever em `notes`)

### 2.4 `genero_atribuido`
Genero predominante da personificacao.

| Valor | Definicao |
|-------|-----------|
| `feminino` | Figura claramente feminina |
| `masculino` | Figura claramente masculina |
| `neutro` | Figura sem marcadores de genero |
| `hibrido` | Atributos dualizados (ex. Africa de Collaert) |
| `ausente` | Nao ha figura humana (dado negativo, ex. brasao da Republica) |

### 2.5 `funcao_juridica`
Funcao do dispositivo no espaco juridico-estatal brasileiro.

| Valor | Definicao |
|-------|-----------|
| `tribunal_consciencia` | Igreja/barroco como espaco de legitimacao publica/juridica |
| `frontispicio_normativo` | Frontispicio de codigo, ordenacao, compilacao juridica |
| `moeda_cedula` | Moeda ou cedula oficial |
| `selo_postal` | Selo postal oficial |
| `brasao` | Brasao de armas, selo de Estado |
| `arquitetura_forense` | Fachada/interior de tribunal, foro, palacio de justica |
| `monumento_publico` | Monumento em espaco publico |
| `paratexto_normativo` | Outro paratexto de norma (ex. capa de codigo) |
| `outro` | Outro; justificar em `notes` |

### 2.6 `vetor_colonial`
Rota de transmissao do repertorio iconografico.

| Valor | Definicao |
|-------|-----------|
| `europeu_direto` | Repertorio europeu aplicado no Brasil sem mediacao lusa evidente |
| `luso_brasileiro` | Repertorio transmitido via Portugal e/ou cultura colonial brasileira |
| `republicano_brasileiro` | Repertorio produzido pelo Estado republicano brasileiro |
| `nao_aplicavel` | Item nao tem dimensao colonial comparavel |

### 2.7 `hipotese_racial`
Campo interpretativo curto (max. 500 caracteres) para articular, no caso de Continentes ou alegorias nacionais, como genero e raca se cruzam na personificacao. Exemplos:

- "America alegorizada como mulher seminua e selvagem, com tracos caucasianos — raca civilizacional branca sobre corpo colonial."
- "Efigie da Republica brasileira branca e a romana: adota gramatica europeia para corporificar nacao que se quer civilizada."
- "Brasao da Republica sem figura feminina: dado negativo que quebra a tradicao europeia de personificacao nacional feminina."

### 2.8 `referencia_genealogica`
Chave para a fonte genealogica predominante. Multiplas referencias podem ser listadas como array.

Valores iniciais:

- `Ripa_1593_1603`
- `Ortelius_1570`
- `Collaert_Four_Continents`
- `Carriera_Four_Continents`
- `Warner_1985`
- `Resnik_Curtis_2011`
- `Souza_2014`
- `Ihering_Der_Zweck`
- `outra` (especificar em `notes`)

## 3. Campos de capta obrigatorios

Todo registro codificado com este codebook deve incluir:

- `capta_declaration`: string fixa `"LPAI v2-capta: scores sao atos interpretativos situados, nao dados neutros."`
- `coder_id`: quem codificou.
- `coded_at`: ISO 8601.
- `codebook_version`: versao do codebook ativa (ex. `2.0.0`).
- `pre_freeze_sample`: `true` para o piloto (ainda nao ha freeze formal).

## 4. Uso dos 10 indicadores de purificacao com as novas familias

Os 10 indicadores ordinais do codebook-pai continuam aplicaveis, mas com ressalvas:

- `desincorporacao`: mede perda de corpo feminino. Quando `genero_atribuido` for `masculino` ou `ausente`, o indicador deve ser aplicado com `subaltern_caution: true` e nota explicando que a escala nasceu para figuras femininas.
- `heraldizacao`: especialmente relevante para brasoes, moedas e selos.
- `enquadramento_arquitetonico`: aplicavel a igrejas, tribunais e monumentos.
- `serialidade`: alta para moedas, cedulas e selos.
- `inscricao_estatal`: maxima para dispositivos oficiais brasileiros.

## 5. Regras de decisao: core vs. comparador

Um item so entra no **corpus core** se atender a **todos** os criterios:

1. `familia_alegorica` for uma das tres novas familias (ou `Nacional` quando hibrido).
2. `funcao_juridica` indicar dispositivo estatal/juridico brasileiro.
3. Existir evidencia documental de circulacao no Brasil (data, local, instituicao).

Itens que falhem o criterio 2 ou 3 vao para o **comparador genealogico** (wiki, apendice, prancha-atlas), nao para o corpus core.

## 6. Changelog

| Versao | Data | Mudanca | Re-pontua itens anteriores? |
|--------|------|---------|----------------------------|
| 2.0.0 | 2026-06-22 | Criacao dos campos familia_alegorica, subtipo, atributos_iconograficos, genero_atribuido, funcao_juridica, vetor_colonial, hipotese_racial, referencia_genealogica | Nao (aplicavel apenas a novos ingestos do piloto) |

## 7. Referencias

- RIPA, Cesare. **Iconologia**. Padova, 1618.
- WARNER, Marina. **Monuments and Maidens: The Allegory of the Female Form**. Berkeley: University of California Press, 2000.
- RESNIK, Judith; CURTIS, Dennis. **Representing Justice: Invention, Controversy, and Rights in City-States and Democratic Courtrooms**. New Haven; London: Yale University Press, 2011.
- SOUZA, Ana Cecilia Araujo Soares de. **A America alegorizada: imagens e visoes do Novo Mundo na iconografia europeia dos seculos XVI a XVIII**. Joao Pessoa: Editora da UFPB, 2014.
- Drucker, Johanna. Humanities Approaches to Graphical Display. *Digital Humanities Quarterly*, v. 5, n. 1, 2011.
- D'Ignazio, Catherine; Klein, Lauren. *Data Feminism*. Cambridge, MA: MIT Press, 2020.
