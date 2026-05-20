---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Oliveira, Raphael Souza de"
  - "Nascimento, Erick Giovani Sperandio"
ano: 2023
titulo: "Analysing similarities between legal court documents using natural language processing approaches based on Transformers"
publicacao: "PLOS ONE"
editora: Public Library of Science
doi: "10.1371/journal.pone.0320244"
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11978053/"
idioma: en
tags:
  - metodologia/nlp
  - nlp/bert
  - nlp/juridico
  - nlp/portugues-br
  - nlp/similaridade
  - nlp/transformers
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]]"
  - "[[JUSTINO et al — BERT semantic retrieval Brazilian legal documents (2025)]]"
  - "[[CHALKIDIS et al — Legal-BERT (2020)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

OLIVEIRA, Raphael Souza de; NASCIMENTO, Erick Giovani Sperandio. Analysing similarities between legal court documents using natural language processing approaches based on Transformers. **PLOS ONE**, [S. l.], v. 19, 2023. DOI: 10.1371/journal.pone.0320244. Disponível em: https://pmc.ncbi.nlm.nih.gov/articles/PMC11978053/. Acesso em: 8 abr. 2026.

---

## Síntese

O artigo aplica oito modelos de linguagem baseados na arquitetura Transformer ao problema de detecção de similaridade entre processos judiciais brasileiros, utilizando um corpus de 210.000 documentos do sistema judiciário do país. Os modelos testados incluem BERT, GPT-2, RoBERTa e LlaMA, pré-treinados sobre corpus de propósito geral em português brasileiro e posteriormente submetidos a fine-tuning sobre corpus jurídico. O objetivo operacional é clusterizar processos judicialmente similares para apoiar decisões de precedente e reduzir o trabalho manual de triagem.

A metodologia combina duas etapas: geração de representações vetoriais (embeddings) de cada documento via modelo de linguagem, seguida de agrupamento por similaridade vetorial (clustering). A qualidade dos clusters é avaliada por métricas internas (coesão intra-cluster) e externas (comparação com categorias judiciais pré-definidas). O corpus de fine-tuning é inteiramente em PT-BR e abrange múltiplos ramos do direito, com concentração em processos cíveis e trabalhistas do Tribunal Regional do Trabalho.

O resultado central confirma que modelos de linguagem fine-tunados sobre corpus jurídico brasileiro superam modelos genéricos na tarefa de similaridade, com ganhos mais expressivos na detecção de processos sobre o mesmo tema jurídico do que na detecção de processos com desfecho idêntico (distinção relevante para compreender os limites metodológicos).

---

## Análise crítica

Este artigo é relevante para a tese sobretudo pelo que demonstra sobre a escala necessária para fine-tuning efetivo: 210.000 documentos jurídicos. Este número contrasta fortemente com o `iconocracy-corpus`, que opera em escala muito menor. A conclusão não é de impossibilidade, mas de ajuste de expectativas: o fine-tuning supervisionado sobre o corpus histórico da tese provavelmente não atingirá o desempenho reportado aqui; a abordagem mais viável é o *zero-shot* ou o *few-shot learning*, com eventual anotação manual de um conjunto de validação de tamanho manejável.

O uso de GPT-2 como modelo generativo (além dos modelos encoder como BERT e RoBERTa) abre uma questão metodológica interessante para a tese: é possível usar modelos generativos para produzir descrições textuais automáticas de itens iconográficos a partir de suas fichas de metadados? A resposta provável é sim, com os modelos adequados (GPT-4, Claude), mas o artigo demonstra que a tarefa de similaridade semântica entre documentos jurídicos é melhor servida por modelos encoder (BERT/RoBERTa) do que por modelos generativos (GPT-2).

Uma implicação metodológica para a análise iconográfica: a similaridade entre iconografias (comparar duas representações de Justitia de países diferentes) pode ser modelada como tarefa de similaridade semântica entre as legendas textuais e os campos de metadados dos itens, utilizando exatamente o pipeline descrito por Oliveira e Nascimento. O corpus iconográfico da tese não é composto de textos jurídicos longos, mas de metadados estruturados com campos textuais (título, descrição, legenda inscrita). A técnica é diretamente transferível neste nível de abstração.

---

## Citações relevantes

> "The transformer-based models utilised — BERT, GPT-2, RoBERTa, and LlaMA — were pre-trained on general-purpose corpora of Brazilian Portuguese and subsequently fine-tuned for the legal sector using a dataset of 210,000 legal proceedings." (resumo)

> "Fine-tuning on domain-specific data yields consistently superior results compared to zero-shot inference, but the quality of the fine-tuning corpus is as important as its size." (seção de discussão)

---

## Conexões com a tese

- Demonstra a escala necessária para fine-tuning supervisionado: 210k documentos, inatingível para o corpus histórico da tese
- Indica *zero-shot* e *few-shot* como abordagens realistas para o `iconocracy-corpus`
- Similaridade entre metadados textuais de itens iconográficos como tarefa análoga à detecção de similaridade entre processos jurídicos
- Encoders (BERT/RoBERTa) superam geradores (GPT-2) na tarefa de similaridade, o que justifica a escolha do BERTimbau/Legal-BERTimbau na pipeline
