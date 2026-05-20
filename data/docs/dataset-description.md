# Descrição do Dataset — Corpus Iconocracia

## Visão Geral

O corpus reúne representações alegóricas femininas vinculadas ao poder estatal
(Justiça, República, Liberdade, Nação) produzidas entre os séculos XVI e XX,
com ênfase no eixo transatlântico Europa–Américas.

## Unidade de Análise

Cada registro (`master record`) corresponde a **um item iconográfico** —
uma imagem ou objeto com metadados catalográficos, códigos iconográficos
(Iconclass, Getty AAT/TGN/ULAN) e interpretação analítica.

## Estrutura do Master Record

Ver schema: [`tools/schemas/master-record.schema.json`](../../tools/schemas/master-record.schema.json)

| Bloco | Descrição |
|-------|-----------|
| `input` | URL de origem, dicas de título/data/local |
| `webscout` | Metadados coletados pelo agente WebScout |
| `iconocode` | Análise iconográfica pelo agente IconoCode |
| `exports` | Citações ABNT geradas + flags de auditoria |
| `timestamps` | Datas de criação e atualização |

## Arquivos Derivados

| Arquivo | Formato | Gerado por |
|---------|---------|------------|
| `records.jsonl` | JSONL (1 registro/linha) | Pipeline dual-agent |
| `corpus_dataset.csv` | CSV tabular | Script de exportação |
| `corpus-data.json` | JSON (array) | `make_index.py` |

## Cobertura Geográfica

França, Alemanha, Brasil, EUA, Portugal, Bélgica, Itália, Reino Unido,
Países Baixos, Áustria, Suíça.

## Cobertura Temporal

Séculos XVI–XX, com concentração nos períodos:
- Revolução Francesa e era napoleônica (1789–1815)
- Independências americanas (1776–1830)
- República brasileira (1889–1930)

## Licença

CC BY 4.0 — ver [LICENSE](../../LICENSE)
