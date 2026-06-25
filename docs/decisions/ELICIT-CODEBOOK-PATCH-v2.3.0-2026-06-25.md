# Patch CHANGELOG v2.2.0 -> v2.3.0 — Codebook LPAI v2 (Gramatica masculina)

> **Status**: patch **candidato** sobre a master v2.2.0. A master vigente
> continua em [`schema/codebook-MASTER.md`](../../schema/codebook-MASTER.md)
> ate decisao explicita de promover a v2.3.0.

## 0. Parecer metodologico (Ana Vanzin, 2026-06-25)

### 0.1 O que esta bem

O rascunho Elicit (3 docs: adendo + CHANGELOG + codebook YAML consolidado) tem
tres pontos fortes claros:

1. **Tese central articulada**: masculino nao pode ser default invisivel;
   precisa ser codificado como construcao por marcas (clava+bivio;
   globo+sustentacao; barba+semirrecosto+urna; gesto indicativo all'antica).
   Coerente com a virada capta da v2.2.0 e com a regra de coocorrencia
   (barba != rio sozinha).
2. **Cinco motivos canonicos** (Hercules, Atlantes, Deuses fluviais barbados,
   Netuno, Genio do Brasil) cobrem repertorio europeu + luso-brasileiro com
   bibliografia especifica (Villari 2015; Bendall 2022; Lazzaro 2011;
   Estella 2002; Lopez 2017; Martin Chillon).
3. **Migracao incremental declarada honestamente**: v2.3.0 nao re-pontua
   legados, `familia_alegorica=Masculino_Juridico` e opcional, gatilho de
   v3.0.0 explicitado para masculinidades afro/indigena. E o padrao correto
   pre-freeze.

### 0.2 O que precisa revisao antes do freeze

1. **Convencao de enums quebra o master v2.2.0**. Adendo veio em
   snake_case (`masculino_juridico`, `hercules`, `clava`, `barba_longa`),
   master v2.2.0 usa PascalCase com underscores compostos (`Iustitia_E_Paz`,
   `America_do_Sul`, `Oceanos/Rios`). **Decisao tomada**: converter para
   PascalCase na importacao. Resultado: `Masculino_Juridico`, `Hercules`,
   `Clava`, `Barba_Longa`. Documentado em `schema/codebook-v2.3.0-patch.md`.

2. **Campos obrigatorios_condicionais pouco testaveis**.
   `funcao_da_figura_masculina` planejado como obrigatorio quando
   `genero_atribuido==masculino` reprovaria 100% dos 299 registros atuais
   se rodarmos o validador sem flag de migracao. **Decisao**: entrar como
   opcional nesta rodada; promover a obrigatorio apos migracao dos
   candidatos (gate declarado no codebook editorial).

3. **9 das 9 referencias estao marcadas `[verificar ABNT completa antes do
   commit]`**. Preservadas no import como declaracao explicita de pendencia
   editorial. Freeze real depende de normalizacao.

4. **5 dos 10 indicadores_purificacao tem `nota_lacuna`** (`classicizacao`,
   `moralizacao`, `depuracao_semantica`, `neutralizacao_afetiva`,
   `monumentalizacao`). **Decisao**: nao modelar o bloco
   `aplicabilidade_por_familia_masculina` (5 valores x 10 indicadores = 50
   chaves potenciais) no schema JSON nesta rodada; fica apenas no YAML
   editorial como referencia para v2.4.0/v3.0.0.

5. **`substituicao_atributiva_hercules`** e brilliant metodologicamente,
   mas a condicional `obrigatorio_quando subtipo==hercules AND
   objetos_regalia nao_contem clava` exige validador com interseccao de
   arrays. `tools/scripts/validate_schemas.py` atual nao cobre. **Decisao**:
   campo entra como opcional sem enforce; gate tecnico declarado no codebook
   editorial.

6. **Duplicacao com adendo anterior (Warner/capta, 2026-06-23)**. v2.1.0 ja
   tinha sido consolidado e marcado superseded em v2.2.0. v2.3.0 entra como
   minor patch opcional, com mesmo tratamento: adendo marcado como superseded
   por patch candidato, sem promover a master.

### 0.3 Decisoes explicitas (Ana Vanzin, autorizando quebra controlada)

- **Quebrar o schema e aceitavel** para fins de patch piloto v2.3.0. A
  expansao fica isolada em campos opcionais; registros pre-existentes nao
  re-pontuados; master v2.2.0 segue vigente.
- **Fugir dos 10 indicadores_e aceitavel** para esta rodada. O bloco
  `aplicabilidade_por_familia_masculina` nao vai pro schema JSON; fica
  apenas no YAML editorial. Indicadores continuarao sendo preenchidos com os
  5 valores ja existentes no schema JSON.
- **Nao tocar `codebook-MASTER.md`**: v2.2.0 permanece master vigente.
- **Nao tocar `data/processed/records.jsonl`**: nenhum registro recebe
  `Masculino_Juridico` automaticamente; a migracao fica para fase posterior
  (gate tecnico + decisao de freeze).

## 1. Cabecalho do patch

```yaml
patch_header:
  from_version: "2.2.0"
  to_version: "2.3.0"
  date: "2026-06-25"
  author: "Ana Vanzin (consolidacao a partir do rascunho Elicit)"
  scope:
    - "Nao re-pontua itens anteriores ingestados em 2.2.0."
    - "Aplicavel apenas a novos ingestos; campos novos sao opcionais para legados (ver Plano de migracao)."
  motivacao:
    - "Sistematizar gramatica masculina de alegoria juridico-estatal como construcao reconhecivel por marcas e funcoes (Hércules, Atlantes, deuses fluviais barbados, Netuno, Gênio do Brasil)."
    - "Tornar masculino auditavel: barba + postura + efluencia como coocorrencia obrigatoria para inferir Rio_Barbado; clava + nudez para Hercules; postura de sustentacao para Atlante_Telamon."
    - "Permitir registro de substituicao atributiva herculea (cetro -> vara -> clava) sem depender da presenca material da clava."
```

## 2. Documentos produzidos neste patch

| Arquivo | Funcao |
|---|---|
| `schema/adendo-metodologico-v2.3.0.md` | Adendo metodologico com a tese da gramatica masculina, 4 sub-linhagens, casos brasileiros, lacunas declaradas, 8 referencias marcadas `[verificar ABNT]`. snake_case -> PascalCase aplicado. |
| `schema/codebook-v2.3.0-patch.md` | CHANGELOG operacional: diff conceitual, mudancas em campos existentes, novos campos opcionais, gates tecnicos. snake_case -> PascalCase aplicado. |
| `schema/codebook-v2.3.0.md` | Versao editorial em MD do YAML consolidado, com `freeze_state: pre_freeze_piloto_v230`, vocabulario controlado para `objetos_regalia` e `marcas_corporais`, subtipos por familia, exemplo de registro piloto. |
| `tools/schemas/master-record.schema.json` | Schema JSON canonico expandido: `familia_alegorica` enum ganha `Masculino_Juridico`; 5 campos novos opcionais em `purificacao` (ver secao 3). |

## 3. Mudancas aplicadas no schema JSON canonico

### 3.1 `familia_alegorica` (enum expandido)

```diff
   "familia_alegorica": {
     "type": "string",
     "enum": [
       "Virtudes",
       "Continentes",
       "Oceanos/Rios",
       "Nacional",
-      "Outra"
+      "Outra",
+      "Masculino_Juridico"
     ]
   }
```

### 3.2 Novos campos opcionais em `purificacao.properties`

| Campo | Tipo | Enum |
|---|---|---|
| `funcao_da_figura_masculina` | string | `Pedagogia_Do_Bivio`, `Suporte_Arquitetonico`, `Delimitacao_Territorial`, `Protetorado_Nacional`, `Soberania_Maritima`, `Mediacao_Divino_Juridica`, `Outro` |
| `tipo_agencia_masculina` | string | `Pedagogia_Do_Bivio`, `Suporte_Arquitetonico`, `Delimitacao_Territorial`, `Protetorado`, `Soberania_Maritima`, `Mediacao_Divino_Juridica`, `Outro` |
| `funcao_atlanteana` | boolean | — |
| `tipo_efluencia_hidrica` | string | `Urna_Vertedora`, `Vaso_Inclinado`, `Sem_Efluencia`, `Outro` |
| `substituicao_atributiva_hercules` | object | `{ atributo_canonico_substituido: string, atributo_novo: string, justificativa: string (maxLength 300) }` |

**Todos opcionais nesta rodada.** Sem condicional `required` no JSON Schema.
Regras condicionais ficam no YAML editorial.

## 4. Mudancas NAO aplicadas (e por que)

| Item | Por que nao foi aplicado |
|---|---|
| Bloco `aplicabilidade_por_familia_masculina` (10 indicadores x 5 valores) | Exigiria 50 chaves novas por registro; `validate_schemas.py` nao suporta enums aninhados com essa profundidade; 5 indicadores com `nota_lacuna`. Fica apenas no YAML editorial. |
| `subtipo` enum controlado por familia `Masculino_Juridico` | Schema JSON usa `string` livre em `subtipo`; vocabulario controlado documentado em `schema/codebook-v2.3.0.md` secao 3.1. |
| Enforce condicional `obrigatorio_quando` em `funcao_da_figura_masculina`, `funcao_atlanteana`, `tipo_efluencia_hidrica`, `substituicao_atributiva_hercules` | `validate_schemas.py` nao cobre; gate tecnico declarado. |
| `justificativa_genero` com `minLength: 80` condicional | idem. |
| Promocao de v2.2.0 -> v2.3.0 como master vigente | Master NAO e tocada. `codebook-MASTER.md` segue como v2.2.0; v2.3.0 fica como patch candidato. |
| Migracao automatica de registros pre-existentes para `Masculino_Juridico` | Nenhum registro recebe o valor automaticamente; migracao fica para fase posterior com gate tecnico + decisao de freeze. |

## 5. Compatibilidade

- Schema JSON e **retrocompativel**: enum `familia_alegorica` ganha 1 valor
  (`Masculino_Juridico`); registros que usam valores anteriores continuam
  validando. Os 5 campos novos sao `optional` no schema, ou seja, registros
  que nao os usam continuam validos.
- `data/processed/records.jsonl` (299 linhas) **nao foi tocado** nesta
  rodada.
- `codebook-MASTER.md` (v2.2.0) **nao foi tocado**.

## 6. Validacao executada

- `python tools/scripts/validate_schemas.py` (a executar; ver secao 7 do
  relatorio de import).

## 7. Proximos passos sugeridos

1. Revisar vocabulario controlado para `objetos_regalia` e `marcas_corporais`
   (novos valores introduzidos em v2.3.0) e decidir se migrar para enum
   rigido no schema JSON.
2. Implementar `validate_schemas.py` suporte para:
   - `minLength` condicional em `justificativa_genero`;
   - `required` quando enum-match em outro campo;
   - interseccao de arrays para `substituicao_atributiva_hercules`.
3. Normalizar 8 referencias marcadas `[verificar ABNT]` antes de promover
   v2.3.0 a master.
4. Buscar evidencia direta para os 9 itens lacunares declarados no adendo
   (Duque de Caxias; deuses fluviais em papel-moeda; masculinidades
   afro-brasileiras; masculinidades indigenas; atlantes manuelinos; etc.).
5. Decidir se o bloco `aplicabilidade_por_familia_masculina` fica para
   v2.4.0 (com schema JSON estendido) ou v3.0.0 (com reorganizacao mais
   ampla).
