---
id: SESSAO-NLP-2026-04-08
tipo: sessao-fichamentos
data: 2026-04-08
tema: "Metodologia digital: NLP para análise de corpus jurídico em PT-BR"
total_fichamentos: 5
tags:
  - metodologia/nlp
  - metodologia/corpus-digital
  - nlp/bert
  - nlp/juridico
  - nlp/portugues-br
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[DB1 Corpus Iconográfico]]"
  - "[[IconoCode -- Protocolo]]"
---

## Resumo da sessão

Esta sessão fichei a literatura acadêmica central sobre frameworks de processamento de linguagem natural (PLN) aplicados a corpus jurídico em português brasileiro. Os artigos foram selecionados a partir de uma pesquisa comparativa de frameworks NLP conduzida em abril de 2026, com foco nos critérios: suporte a PT-BR, aplicabilidade a textos jurídicos históricos, integração com Python/Jupyter e comunidade ativa de desenvolvimento.

---

## Fichamentos produzidos

| # | Fichamento | Ano | Relevância para o corpus |
|---|-----------|-----|--------------------------|
| 1 | [[SOUZA_NOGUEIRA_LOTUFO — BERTimbau Pretrained BERT Models for Brazilian Portuguese (2020)]] | 2020 | Modelo base para todos os pipelines em PT-BR |
| 2 | [[CHALKIDIS et al — Legal-BERT Preparing the Muppets for Court (2020)]] | 2020 | Enquadramento metodológico: domain shift e especialização jurídica |
| 3 | [[QI et al — Stanza Python NLP Toolkit Many Human Languages (2020)]] | 2020 | Anotação morfossintática, corpus em francês e multilíngue |
| 4 | [[JUSTINO et al — BERT Models Semantic Retrieval Brazilian Legal Documents (2025)]] | 2025 | Pipeline de recuperação semântica em corpus jurídico BR contemporâneo |
| 5 | [[OLIVEIRA_NASCIMENTO — Similarities Brazilian Legal Documents Transformers (2023)]] | 2023 | Similaridade semântica; escala para fine-tuning (210k documentos) |
| 6 | [[LIMA et al — HelBERT BERT Pretraining Public Procurement Portuguese (2026)]] | 2026 | Estado atual (2026) da ecologia de modelos BERT jurídicos em PT-BR |

---

## Linha do tempo dos modelos PT-BR

```
2020 — BERTimbau (Souza et al.) ─── fundação do ecossistema PT-BR
2020 — LEGAL-BERT (Chalkidis et al.) ─── especialização jurídica em inglês
2021 — Legal-BERTimbau (STJIRIS) ─── especialização jurídica em PT (30k documentos)
2023 — Oliveira & Nascimento ─── fine-tuning em 210k processos BR
2024 — BumbaBERT ─── jurisprudência BR (recuperação semântica zero-shot)
2025 — Justino et al. ─── benchmark de recuperação semântica jurídica PT-BR
2026 — HelBERT (Lima et al.) ─── procurement público BR
```

---

## Pipeline recomendado para o `iconocracy-corpus`

```
Textos históricos PT-BR
  → spaCy pt_core_news_lg (pré-processamento, tokenização, lematização)
    → BERTimbau / Legal-BERTimbau (embeddings semânticos)
      → BumbaBERT ou HelBERT (para subdomínios específicos)
        → Elasticsearch / FAISS (recuperação vetorial, clustering)

Textos em francês (Marianne, Troisième République)
  → Stanza `fr` (anotação morfossintática UD)
    → CamemBERT / XLM-RoBERTa (embeddings semânticos)

Análise temática do corpus
  → Gensim LDA (modelagem de tópicos sobre corpus completo)
```

---

## Conceito-chave transversal: domain shift

Todos os artigos fichados convergem para o mesmo problema metodológico central: *domain shift*, a degradação do desempenho de modelos de linguagem quando aplicados a textos de domínio distinto do corpus de treinamento. Para o `iconocracy-corpus`, o *domain shift* opera em duas dimensões simultâneas:

1. **Domínio temático:** textos jurídico-iconográficos históricos versus corpus web/jornalístico contemporâneo (BERTimbau, LEGAL-BERT)
2. **Dimensão temporal:** linguagem jurídica do século XIX versus linguagem contemporânea (todos os modelos disponíveis)

A estratégia de mitigação recomendada pela literatura é o fine-tuning incremental, mesmo com corpus reduzido, combinado com avaliação manual sobre um conjunto de validação anotado especificamente para o domínio histórico.

---

## Lacunas identificadas

- Ausência de modelos de linguagem treinados sobre corpus jurídico histórico em PT-BR (oportunidade de pesquisa futura)
- Nenhum benchmark disponível para texto jurídico do século XIX em qualquer língua
- Escassez de corpus anotados de iconografia jurídica textualmente descrita
- Legal-BERTimbau (STJIRIS) é treinado sobre jurisprudência portuguesa (Portugal), não brasileira — diferença lexical e sintática relevante

---

## Próximas buscas sugeridas

1. `CamemBERT French legal pretraining` — para corpus em francês
2. `historical legal text NLP 19th century` — para metodologia em corpus histórico
3. `CLIP visual text alignment iconography` — para alinhamento imagem-texto no corpus iconográfico
4. `BrWaC Brazilian web corpus 19th century historical` — verificar se há corpus histórico disponível
