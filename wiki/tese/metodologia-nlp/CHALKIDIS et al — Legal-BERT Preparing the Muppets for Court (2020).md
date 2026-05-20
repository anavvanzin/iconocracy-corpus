---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Chalkidis, Ilias"
  - "Fergadiotis, Manos"
  - "Malakasiotis, Prodromos"
  - "Aletras, Nikolaos"
  - "Androutsopoulos, Ion"
ano: 2020
titulo: "LEGAL-BERT: The Muppets straight out of Law School"
publicacao: "Findings of the Association for Computational Linguistics: EMNLP 2020"
editora: Association for Computational Linguistics
doi: "10.18653/v1/2020.findings-emnlp.261"
url: "https://aclanthology.org/2020.findings-emnlp.261"
idioma: en
tags:
  - metodologia/nlp
  - nlp/bert
  - nlp/juridico
  - nlp/domain-specific
  - nlp/legal-text
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]]"
  - "[[JUSTINO et al — BERT semantic retrieval Brazilian legal documents (2025)]]"
  - "[[LIMA et al — HelBERT (2026)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

CHALKIDIS, Ilias; FERGADIOTIS, Manos; MALAKASIOTIS, Prodromos; ALETRAS, Nikolaos; ANDROUTSOPOULOS, Ion. LEGAL-BERT: The Muppets straight out of Law School. In: **Findings of the Association for Computational Linguistics: EMNLP 2020**. [S. l.]: Association for Computational Linguistics, 2020. p. 2898-2904. DOI: 10.18653/v1/2020.findings-emnlp.261. Disponível em: https://aclanthology.org/2020.findings-emnlp.261. Acesso em: 8 abr. 2026.

---

## Síntese

O artigo introduz o LEGAL-BERT, uma família de modelos BERT especializados em texto jurídico em língua inglesa. O argumento central é que o BERT genérico, pré-treinado sobre Wikipedia e BookCorpus, carece das representações linguísticas necessárias para processar eficientemente documentos legais, cuja linguagem é altamente formalizada, repleta de terminologia especializada e estruturalmente distinta da prosa geral. Os autores exploram três estratégias de especialização: (a) uso direto do BERT original (baseline); (b) adaptação por pré-treinamento adicional em corpus jurídico (*domain-adaptive pretraining*); e (c) pré-treinamento completo desde o início em corpus jurídico (*pretraining from scratch*).

O corpus de treinamento legal compilado pelos autores abrange aproximadamente 12 GB de texto, incluindo legislação europeia (EUR-Lex), decisões do Tribunal Europeu dos Direitos Humanos (ECHR) e contratos comerciais americanos (SEC filings). Os modelos são avaliados em três tarefas de downstream: classificação multi-label de legislação da UE (EURLEX57K), análise de obrigações contratuais (ContractNLI) e detecção de violações de direitos humanos (ECHR). Em todas as tarefas, os modelos LEGAL-BERT superam o BERT genérico e o RoBERTa, com ganhos que chegam a 5 pontos percentuais em F1.

O conceito operacional mais relevante do artigo é o de *domain shift*: a hipótese, confirmada experimentalmente, de que a distância entre o texto de pré-treinamento de um modelo de linguagem e o texto de inferência determina diretamente a qualidade das representações produzidas. Quanto mais o domínio do corpus de aplicação se afasta do corpus de treinamento, pior o desempenho.

---

## Análise crítica

O LEGAL-BERT é o antecedente direto do Legal-BERTimbau e do HelBERT, suas variantes para o português jurídico. Para o `iconocracy-corpus`, o artigo importa menos como ferramenta direta — é treinado em inglês — e mais como enquadramento metodológico: ele justifica teoricamente por que a escolha do modelo de linguagem é uma decisão metodológica de primeira ordem, não um detalhe técnico substituível.

O argumento do *domain shift* tem um corolário importante para a tese: textos jurídicos históricos do século XIX constituem um domínio duplamente deslocado em relação ao treinamento de qualquer modelo contemporâneo, tanto pelo idioma histórico quanto pela distância temporal. O corpus de documentação do `iconocracy-corpus` envolve legislação imperial, jurisprudência oitocentista e iconografia acompanhada de legenda; nenhum dos modelos disponíveis foi pré-treinado sobre este tipo específico de texto. Isso não inviabiliza o uso de modelos BERT, mas exige cautela na interpretação dos resultados e possivelmente a construção de um conjunto de avaliação anotado manualmente para validar as predições do modelo sobre o corpus histórico.

Uma contribuição metodológica secundária do artigo é a proposta de avaliar modelos em múltiplas tarefas de NLP jurídico em vez de em tarefa única, o que sugere uma bateria de avaliação para validar o pipeline do `iconocracy-corpus`: não apenas NER de entidades alegóricas, mas também classificação de documentos por suporte (moeda, selo, monumento) e similaridade semântica entre legendas iconográficas de períodos distintos.

---

## Citações relevantes

> "We present LEGAL-BERT, a family of BERT models for the legal domain, intended to assist legal NLP research, computational law, and legal technology applications." (p. 2898)

> "Legal texts are written in a particular style and contain many domain-specific terms that are not covered by BERT's vocabulary." (p. 2899)

> "Domain-specific pretraining leads to significant improvements over the general-purpose BERT model across all tasks." (p. 2902)

---

## Conexões com a tese

- Referência metodológica para justificar a escolha do Legal-BERTimbau em detrimento do BERTimbau genérico ao processar textos doutrinários do corpus
- O conceito de *domain shift* nomeia o principal risco metodológico do uso de NLP em corpus histórico-jurídico do século XIX
- Para textos em inglês (documentos britânicos sobre Britannia, contratos coloniais americanos), o próprio LEGAL-BERT é aplicável diretamente
- Ver discussão paralela em [[LIMA et al — HelBERT (2026)]] e [[JUSTINO et al — BERT semantic retrieval (2025)]]
