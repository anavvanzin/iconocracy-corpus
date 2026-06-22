---
title: Endurecimento
aliases:
  - endurecimento_score
type: kg/conceito
tags:
  - kg
  - projeto/iconocracia
  - conceito/autoral
  - metodo/quantitativo
  - "#endurecimento"
related:
  - "[[Purificação Clássica]]"
  - "[[Regimes Iconocráticos]]"
  - "[[IconoCode]]"
  - "[[Hierarquia de Dados — MOC]]"
  - "[[Esquemas JSON]]"
sources:
  - ../CLAUDE.md
  - ../tools/schemas/purification-record.schema.json
  - ../data/processed/purification.jsonl
status: ativo
created: 2026-06-19
updated: 2026-06-19
---

# Endurecimento

Operacionalização **empírica** da [[Purificação Clássica]]. Mede, em escala
**ordinal 0–3**, o grau em que uma alegoria feminina foi extraída da história e
fixada como signo rígido do Estado.

> [!warning] Terminologia (obrigatória)
> Sempre em português: **Endurecimento**. NUNCA "hardening" nem "embrutecimento".
> `endurecimento_score = 0` é um **escore válido** (baixa purificação), não
> "não codificado".

## Os 10 indicadores

Cada indicador é um inteiro **ordinal 0–3** (`minimum: 0, maximum: 3` no
[esquema de purificação](../tools/schemas/purification-record.schema.json) — **não
há `enum`** para os indicadores). As chaves do schema são **ASCII, sem acento**:

| # | Chave (`purification-record`) | Lê |
| --- | --- | --- |
| 1 | `desincorporacao` | corpo vivo → corpo abstrato/ausente |
| 2 | `rigidez_postural` | gesto → pose hierática |
| 3 | `dessexualizacao` | corpo sexuado → corpo neutralizado |
| 4 | `uniformizacao_facial` | rosto individual → tipo facial |
| 5 | `heraldizacao` | figura → emblema/brasão |
| 6 | `enquadramento_arquitetonico` | cena → nicho/fachada forense |
| 7 | `apagamento_narrativo` | narrativa → ícone isolado |
| 8 | `monocromatizacao` | cor → metal/pedra/monocromia |
| 9 | `serialidade` | obra única → série (moeda, selo) |
| 10 | `inscricao_estatal` | imagem → imagem com legenda/insígnia do Estado |

> [!note] Escore composto e regime (mesmo schema)
> Além dos 10 indicadores, o `purification-record` traz `purificacao_composto`
> (0–3) e `regime_iconocratico` — este sim um `enum`:
> `fundacional · normativo · militar · contra-alegoria` (ver
> [[Regimes Iconocráticos]]).
>
> Os rótulos humanos **acentuados** (ex.: "heraldicização") aparecem em
> [`../CLAUDE.md`](../CLAUDE.md); o **contrato de dados** usa as chaves ASCII
> acima.

## Da medida ao regime

O perfil dos 10 indicadores posiciona a imagem num dos
[[Regimes Iconocráticos]]: baixos escores → FUNDACIONAL; altos e seriais →
MILITAR. A subversão deliberada desses indicadores caracteriza a CONTRA-ALEGORIA.

## Onde vive o dado

- **Ledger de codificação:** [`../data/processed/purification.jsonl`](../data/processed/purification.jsonl) — ledger de endurecimento (contagem ao vivo: `code_purification.py --status`).
- **Esquema:** [[Esquemas JSON]] → `purification-record.schema.json`.
- **Itens codificados (com `regime`):** subconjunto do corpus — cobertura **parcial**.
- **Produzido por:** [[IconoCode]] (3 níveis Panofsky + 10 indicadores).
- **Política de cobertura parcial:** dossiê de decisões → [DIALÉTICA do N](../docs/decisions/DIALETICA-N165-vs-265.md).

> [!question] Tensão metodológica aberta
> Os itens **sem `regime`** (não codificados) implicam que o total bruto do corpus
> **não é um N analítico válido**. Os tamanhos correntes vivem em
> [`../CLAUDE.md`](../CLAUDE.md) §*Known Data Issues*. Ver [[ADRs e Decisões — MOC]]
> e [a dialética do N](../docs/decisions/DIALETICA-N165-vs-265.md).

## Comandos

```bash
python tools/scripts/code_purification.py --status      # progresso da codificação
python tools/scripts/code_purification.py --export-csv  # regenera corpus_dataset.csv
```
