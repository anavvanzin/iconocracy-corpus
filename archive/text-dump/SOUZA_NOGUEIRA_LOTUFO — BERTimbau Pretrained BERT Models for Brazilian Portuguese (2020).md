---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Souza, Fábio"
  - "Nogueira, Rodrigo"
  - "Lotufo, Roberto"
ano: 2020
titulo: "BERTimbau: Pretrained BERT Models for Brazilian Portuguese"
publicacao: "Intelligent Systems. BRACIS 2020. Lecture Notes in Computer Science, v. 12542"
editora: Springer
doi: "10.1007/978-3-030-61377-8_28"
url: "https://link.springer.com/chapter/10.1007/978-3-030-61377-8_28"
idioma: en
tags:
  - metodologia/nlp
  - nlp/bert
  - nlp/portugues-br
  - nlp/pre-training
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[CHALKIDIS — Legal-BERT (2020)]]"
  - "[[QI et al — Stanza (2020)]]"
  - "[[JUSTINO et al — BERT semantic retrieval Brazilian legal documents (2025)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

SOUZA, Fábio; NOGUEIRA, Rodrigo; LOTUFO, Roberto. BERTimbau: Pretrained BERT Models for Brazilian Portuguese. In: CERRI, Ricardo; PRATI, Ronaldo C. (ed.). **Intelligent Systems: 9th Brazilian Conference, BRACIS 2020**. Lecture Notes in Computer Science, v. 12542. Cham: Springer, 2020. p. 403-417. DOI: 10.1007/978-3-030-61377-8_28. Disponível em: https://link.springer.com/chapter/10.1007/978-3-030-61377-8_28. Acesso em: 8 abr. 2026.

---

## Síntese

O artigo apresenta o BERTimbau, o primeiro modelo BERT pré-treinado exclusivamente em português brasileiro em larga escala. A tese central é simples e de grande alcance operacional: modelos de linguagem treinados monolingualmente em português superam sistematicamente tanto modelos multilíngues (como o mBERT do Google) quanto modelos treinados para português europeu em tarefas de processamento de linguagem natural (PLN) no domínio brasileiro. Os autores treinaram dois modelos de tamanhos distintos (base e large) sobre o corpus brWaC (Brazilian Web as Corpus), composto por aproximadamente 2,68 bilhões de palavras extraídas da web em PT-BR.

A arquitetura segue fielmente o BERT original de Devlin et al. (2019): encoder bidirecional baseado em Transformer, pré-treinado por duas tarefas não supervisionadas: Masked Language Model (MLM) e Next Sentence Prediction (NSP). O diferencial está no vocabulário: enquanto o mBERT compartilha um vocabulário de 119.000 tokens entre 104 línguas, o BERTimbau foi construído com vocabulário dedicado de 30.000 tokens para o português, o que resulta em representações mais eficientes e semanticamente ricas. Os modelos foram avaliados em três tarefas de downstream: Reconhecimento de Entidades Nomeadas (REN), Similaridade Semântica Textual (STS) e Reconhecimento de Implicação Textual (RTE). Em todas elas, o BERTimbau base e large superam os modelos multilíngues com margens expressivas.

---

## Análise crítica

Para o `iconocracy-corpus`, o BERTimbau é a fundação operacional mais relevante de toda a literatura revisada. A análise de textos jurídico-históricos em PT-BR — sejam eles legislação imperial, doutrina oitocentista ou iconografia acompanhada de legenda textual — exige um modelo que compreenda as nuances morfossintáticas e semânticas do português legal brasileiro. O mBERT, treinado para 104 línguas simultaneamente, inevitavelmente dilui sua capacidade representacional para qualquer língua específica.

O ponto mais relevante para a metodologia da tese não está na tarefa de STS ou RTE, mas no Reconhecimento de Entidades Nomeadas (REN). Identificar automaticamente nomes de figuras alegóricas, datas, instituições e suportes materiais nos textos do corpus é tarefa que o BERTimbau viabiliza diretamente, especialmente quando combinado com fine-tuning sobre textos jurídicos (cf. Legal-BERTimbau de Lima et al., 2021). Uma tensão metodológica a registrar: os autores avaliam o modelo sobre corpus contemporâneo da web, enquanto o `iconocracy-corpus` lida com textos históricos do século XIX. A deriva de domínio (domain shift) entre a linguagem jurídica oitocentista e o brWaC é uma variável que precisa ser gerenciada, possivelmente por fine-tuning supervisionado ou pela escolha do Legal-BERTimbau como modelo de partida.

O texto de Souza, Nogueira e Lotufo é incontornável como referência metodológica porque constitui a evidência empírica de que o português brasileiro requer tratamento especializado e não pode ser subsumido ao processamento multilíngue genérico, argumento que ressoa com a própria premissa teórica da tese: a especificidade cultural-jurídica brasileira não é redutível a categorias universais.

---

## Citações relevantes

> "We show that our monolingual models achieve state-of-the-art results in all three downstream tasks in comparison to multilingual BERT models." (p. 404)

> "The vocabulary was built with 30,000 subword units using the WordPiece algorithm, trained exclusively on the brWaC corpus." (p. 406)

---

## Conexões com a tese

- Pipeline sugerido para o corpus: BERTimbau (base) + fine-tuning sobre corpus jurídico → NER de entidades iconográficas (nomes alegóricos, datas de circulação, instituições emissoras)
- Complementar com [[Legal-BERTimbau (Lima et al., 2021)]] para análise semântica de textos doutrinários
- Ver também [[Justino et al. 2025]] para aplicação direta em recuperação semântica de documentos jurídicos brasileiros
