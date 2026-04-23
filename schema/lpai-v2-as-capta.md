# LPAI v2 como *capta* — reenquadramento metodológico

> Esta especificação formaliza o reenquadramento proposto em [`docs/methodology.md`](../docs/methodology.md) e coloca a ferramenta LPAI v2 em diálogo explícito com a crítica feminista e pós-colonial ao score (Drucker 2011; Merry 2016; Haraway 1988; D'Ignazio & Klein 2020). Substitui, na prática, a autoridade epistêmica do índice sem descartar a sua utilidade operacional.

| Campo | Valor |
|---|---|
| Documento-pai | [`docs/methodology.md`](../docs/methodology.md) |
| Estado atual da ferramenta | Operacional (T4 ingest de 15 fichas SCOUT BR+FR em 2026-04-19) |
| Relatório de ingest | [`docs/T4-LPAI-INGEST-REPORT.md`](../docs/T4-LPAI-INGEST-REPORT.md) |
| Schema associado | [`tools/schemas/master-record.schema.json`](../tools/schemas/master-record.schema.json) |
| Autoridade epistêmica | **Capta**, não *data* |
| Data | 2026-04-23 |

## 1. Premissa epistemológica

> «All data is capta: data is taken, not given.» — Johanna Drucker, *Digital Humanities Quarterly*, v. 5, n. 1, 2011.

O LPAI v2 **não é um instrumento de medição neutra de imagens**. É uma operação de captura: decide quais eixos valem, quais graus existem, quais ausências contam. Cada pontuação é uma **performance interpretativa** sob aparência de descrição objetiva. O reenquadramento aqui especificado reconhece essa condição e ajusta o uso da ferramenta a ela.

## 2. Do que o LPAI v2 **deixa de ser**

- **Não é** uma métrica de «nível de militarização» ou «nível de iconocracia» de uma imagem.
- **Não é** base legítima para ranking, estatística inferencial ou comparação forte entre países, períodos ou tradições.
- **Não é** um contador de presença/ausência que possa ser tomado como representativo do universo de imagens jurídicas de um período.
- **Não é** input válido para modelos preditivos ou classificadores supervisionados sem que toda a cadeia de *capta* seja explicitada junto ao output.

## 3. O que o LPAI v2 **passa a ser**

### 3.1 Ferramenta de descoberta de corpus
A pontuação LPAI v2 funciona como **heurística de atenção** — um mapa provisório que sinaliza onde olhar. Um *score* alto em «militarização» não é verdade sobre a imagem, é ponteiro para inspeção iconológica aprofundada. A curadoria da prancha-atlas continua a ser o locus de julgamento crítico.

### 3.2 Instrumento de documentação de ausências
A não-ocorrência de combinações de indicadores em regiões, períodos ou suportes torna-se achado quantificável:

- *«Nenhuma Justitia negra ou indígena nos palácios brasileiros entre 1889 e 2000»* — formulável a partir dos eixos de *embodiment* do LPAI.
- *«República armada desaparece do corpus federal brasileiro entre 1937 e 1945»* — detectável pelo cruzamento dos eixos de militarização × período.
- *«Marianne mantém gládio até 1914; Liberty abandona-o após 1886»* — comparador legítimo se e somente se os corpora BR × FR × US forem declarados assimétricos.

Ausência é dado quando assumida como *capta negativa* — algo que **a ferramenta viu que não viu**.

### 3.3 Base de interoperabilidade
Os campos do LPAI v2 devem ser espelhados em **Iconclass** (11M31 Justitia, 44G411 República feminina, 44G51 Liberdade, 44A1 Personificação do Estado) para permitir descoberta federada em Erdteilallegorien, PHAROS e demais bases vinculadas.

## 4. Regras operacionais (LPAI v2-capta)

### 4.1 Declaração obrigatória de proveniência
Todo registro que carregue pontuação LPAI deve incluir:
- `capta_declaration`: string fixa *«LPAI v2 output is capta, not data. All scores are situated interpretive acts by the thesis author under the methodological framing documented in schema/lpai-v2-as-capta.md.»*
- `coder_id`: quem codificou.
- `coded_at`: ISO 8601.
- `codebook_version`: versão do codebook ativa no momento da codificação.

### 4.2 Changelog obrigatório em mudança de indicador
Toda alteração de eixo, grau, definição de indicador ou peso relativo deve:
1. Incrementar `codebook_version` em +1 minor (x.y → x.(y+1)) ou +1 major se a semântica mudar.
2. Abrir entrada no `CHANGELOG.md` do schema.
3. Registrar se a mudança **re-pontua itens já ingeridos** ou apenas se aplica a novos ingestos.
4. Justificar a mudança em três linhas: evidência empírica que motivou, problema teórico endereçado, risco de **reatividade** (Espeland & Sauder, 2007) avaliado.

### 4.3 Proibição de inferência antes do freeze
Nenhuma estatística, tabela de frequências, mapa ou gráfico publicado pode ser derivado do LPAI v2 antes do **freeze** formal do dataset. Sequência obrigatória:

```
teoria → codebook → amostragem → piloto → confiabilidade → freeze → análise
```

Publicações ou commits que violem esta sequência devem ser marcados com `pre_freeze_sample: true` e um aviso explícito de que não constituem evidência.

### 4.4 Par obrigatório score ↔ prancha
Nenhum resultado LPAI v2 circula sozinho. Todo bloco de scores deve vir acompanhado de pelo menos **uma prancha warburguiana** (docs/pilots/) que torne visível o que o score não consegue: *Pathosformel*, *Nachleben*, ruptura, iconoclasmo. O atlas é o controle qualitativo do score.

### 4.5 Subalternidade como sinal de cautela, não dado
Quando o LPAI v2 for aplicado a imagens de tradições subalternas (indígenas, negras, populares), o registro deve carregar `subaltern_caution: true` e nota metodológica explícita de que as categorias do codebook têm origem euro-imperial e **marginalizam sistematicamente** imagens fora desse cânone (Azoulay, Mirzoeff, Campt). O score nesse caso é ponteiro para revisão da categoria, não para classificação do objeto.

## 5. Campos novos a acrescentar em `master-record.schema.json`

Proposta técnica para implementação futura:

```json
{
  "lpai_capta_block": {
    "type": "object",
    "properties": {
      "capta_declaration": {"type": "string", "const": "LPAI v2 output is capta, not data."},
      "coder_id": {"type": "string"},
      "coded_at": {"type": "string", "format": "date-time"},
      "codebook_version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
      "pre_freeze_sample": {"type": "boolean", "default": true},
      "subaltern_caution": {"type": "boolean", "default": false},
      "paired_atlas_panel": {"type": "string", "description": "Reference to a prancha in docs/pilots/"}
    },
    "required": ["capta_declaration", "coder_id", "coded_at", "codebook_version"]
  }
}
```

Decisão de implementação permanece aberta até freeze do codebook.

## 6. Trajetória de decisão

### 6.1 Opções avaliadas
- **(a) Descartar o LPAI** — rejeitado: perde-se a infraestrutura operacional já construída (parser `tools/scripts/ingest_fichas_lpai.py`, schema validador, 15 fichas ingeridas) e perde-se a capacidade de documentar ausências.
- **(b) Reenquadrar como *capta*** — **recomendado e especificado neste documento**.
- **(c) Manter como índice com changelog explícito** — rejeitado: não endereça o problema epistêmico central de que o score **produz** a verdade que afirma descrever.

### 6.2 Estado da decisão
- Rascunho metodológico.
- Aguarda discussão com orientação PPGD/UFSC.
- Nenhum output LPAI v2 deve ser publicado em tese, apresentação ou paper enquanto esta decisão não for formalmente registrada em `CHANGELOG.md`.

## 7. Referências

D'IGNAZIO, Catherine; KLEIN, Lauren. *Data Feminism*. Cambridge, MA: MIT Press, 2020. DOI: 10.7551/mitpress/11805.001.0001.

DRUCKER, Johanna. Humanities Approaches to Graphical Display. *Digital Humanities Quarterly*, v. 5, n. 1, 2011. Disponível em: <http://www.digitalhumanities.org/dhq/vol/5/1/000091/000091.html>.

ESPELAND, Wendy Nelson; SAUDER, Michael. Rankings and reactivity: how public measures recreate social worlds. *American Journal of Sociology*, v. 113, n. 1, p. 1–40, 2007.

HARAWAY, Donna. Situated Knowledges: The Science Question in Feminism and the Privilege of Partial Perspective. *Feminist Studies*, v. 14, n. 3, p. 575–599, 1988.

MERRY, Sally Engle. *The Seductions of Quantification: Measuring Human Rights, Gender Violence, and Sex Trafficking*. Chicago: University of Chicago Press, 2016.

## Ligações

- Documento-pai: [`docs/methodology.md`](../docs/methodology.md)
- Schema atual do LPAI v2: [`tools/schemas/master-record.schema.json`](../tools/schemas/master-record.schema.json)
- Relatório T4 de ingest: [`docs/T4-LPAI-INGEST-REPORT.md`](../docs/T4-LPAI-INGEST-REPORT.md)
- ADR sobre canônico × público: [`docs/adr/005-github-and-hf-release-surfaces.md`](../docs/adr/005-github-and-hf-release-surfaces.md)
