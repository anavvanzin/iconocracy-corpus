---
tipo: "moc"
tags: [corpus, moc]
---

# Corpus Iconocracia — Mapa de Conteúdo

> Índice das fichas catalográficas do corpus (~300 itens previstos, 66 catalogados).
> Cada ficha segue o template [[ficha-catalografica]].

## Por país

### 🇫🇷 França (13)
<!-- fichas aqui -->

### 🇩🇪 Alemanha (11)
<!-- fichas aqui -->

### 🇧🇷 Brasil (10)
<!-- fichas aqui -->

### 🇺🇸 EUA (9)
<!-- fichas aqui -->

### 🇵🇹 Portugal (5)
<!-- fichas aqui -->

### 🇧🇪 Bélgica (4)
<!-- fichas aqui -->

### 🇮🇹 Itália (4)
<!-- fichas aqui -->

### 🇬🇧 Reino Unido (4)
<!-- fichas aqui -->

### 🇳🇱 Países Baixos (3)
<!-- fichas aqui -->

### 🇦🇹 Áustria (2)
<!-- fichas aqui -->

### 🇨🇭 Suíça (1)
<!-- fichas aqui -->

## Por regime iconocrático

### Fundacional
<!-- fichas de momentos constituintes -->

### Normativo
<!-- fichas de rotinização: selos, moedas, edifícios -->

### Militar
<!-- fichas de hardening bélico/autoritário -->

## Estatísticas (Dataview)

```dataview
TABLE
  pais AS "País",
  periodo AS "Período",
  suporte AS "Suporte",
  regime_iconocratico AS "Regime",
  round(mean([purificacao.desincorporacao, purificacao.rigidez_postural, purificacao.dessexualizacao, purificacao.uniformizacao_facial, purificacao.heraldizacao, purificacao.enquadramento_arquitetonico, purificacao.apagamento_narrativo, purificacao.monocromatizacao, purificacao.serialidade, purificacao.inscricao_estatal]), 1) AS "Índice"
FROM "corpus"
WHERE tipo != "moc"
SORT pais ASC
```

## Fontes de dados

| Recurso | Localização |
|---------|-------------|
| JSONL canônico | `data/processed/records.jsonl` |
| Dashboard HTML | `corpus/DASHBOARD_CORPUS.html` |
| JSON navegável | `corpus/corpus-data.json` |
| Codebook | [[codebook]] |
