---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Justino, A. F."
  - "Jacob Júnior, A. F. L."
  - "Marcacini, Ricardo M."
  - "Lobato, F."
ano: 2025
titulo: "Evaluating BERT Models for Semantic Retrieval in Long Portuguese Legal Documents"
publicacao: "Anais do XXII Encontro Nacional de Inteligência Artificial e Computacional (ENIAC 2025)"
editora: SBC — Sociedade Brasileira de Computação
doi: "10.5753/eniac.2025.14328"
url: "https://sol.sbc.org.br/index.php/eniac/article/view/38790"
idioma: pt
tags:
  - metodologia/nlp
  - nlp/bert
  - nlp/juridico
  - nlp/portugues-br
  - nlp/recuperacao-semantica
  - nlp/documentos-longos
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]]"
  - "[[CHALKIDIS et al — Legal-BERT (2020)]]"
  - "[[JUSTINO et al — Comparative BERT Brazilian legal precedents (2025)]]"
  - "[[LIMA et al — HelBERT (2026)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

JUSTINO, A. F.; JACOB JÚNIOR, A. F. L.; MARCACINI, Ricardo M.; LOBATO, F. Evaluating BERT Models for Semantic Retrieval in Long Portuguese Legal Documents. In: **ENCONTRO NACIONAL DE INTELIGÊNCIA ARTIFICIAL E COMPUTACIONAL (ENIAC), 22.**, 2025. **Anais [...].** Porto Alegre: SBC, 2025. DOI: 10.5753/eniac.2025.14328. Disponível em: https://sol.sbc.org.br/index.php/eniac/article/view/38790. Acesso em: 8 abr. 2026.

---

## Síntese

O artigo avalia sistematicamente cinco modelos BERT na tarefa de recuperação densa de informações (*dense retrieval*) em documentos judiciais longos em português brasileiro. O problema central que motiva a pesquisa é prático e urgente: o Judiciário brasileiro produz volumes crescentes de documentos digitais, mas os sistemas de busca tradicionais baseados em palavras-chave são insuficientes para identificar precedentes semanticamente relevantes em casos novos. Os autores implementam um pipeline baseado em segmentação de documentos longos (*chunking*) e recuperação vetorial via Elasticsearch.

Os cinco modelos testados distribuem-se em três categorias: modelos de uso geral para PT (BERTimbau), modelos específicos de domínio jurídico treinados sobre corpus brasileiro (BumbaBERT, JurisBERT, Legal-BERTimbau) e modelo específico de tarefa (SBERT-pt para similaridade semântica). O desempenho é medido pela coerência intra-cluster das representações vetoriais, em cenário *zero-shot* (sem fine-tuning adicional sobre o corpus de avaliação). O resultado principal é que o BumbaBERT (modelo específico do domínio jurídico brasileiro) alcança o melhor desempenho, confirmando a hipótese de que a especialização de domínio é decisiva para recuperação semântica eficaz em contexto jurídico.

A estratégia de *chunking* adotada para lidar com documentos longos é especialmente relevante: como o BERT processa sequências de até 512 tokens, documentos judiciais completos precisam ser segmentados e representados por múltiplos vetores que são depois agregados por pooling.

---

## Análise crítica

Este é o artigo mais diretamente aplicável à metodologia do `iconocracy-corpus` entre todos os fichados. Ele responde empiricamente, com corpus jurídico brasileiro, à questão que o artigo de Chalkidis et al. (2020) coloca teoricamente: qual modelo, dentre os disponíveis em PT-BR, produz as melhores representações para recuperação semântica de documentos jurídicos?

A resposta — BumbaBERT sobre BERTimbau genérico, com ganho estatisticamente significativo em cenário *zero-shot* — tem implicação direta para o pipeline do corpus. Para as tarefas de recuperação e agrupamento semântico de textos doutrinários e iconográficos do `iconocracy-corpus`, o BumbaBERT deve ser testado como alternativa ao Legal-BERTimbau. O cenário *zero-shot* reportado é relevante porque o corpus histórico da tese não dispõe de anotações de treino suficientes para fine-tuning supervisionado em escala.

Há, no entanto, uma limitação importante para o caso da tese: os documentos avaliados por Justino et al. são processos judiciais contemporâneos do Judiciário brasileiro, não textos históricos do século XIX. A transferência dos resultados para documentos oitocentistas exige cautela. O artigo funciona como piso metodológico, não como solução diretamente transplantável.

O pipeline de chunking + Elasticsearch descrito é reutilizável. Para o `iconocracy-corpus`, a segmentação de documentos longos (pareceres jurídicos, relatórios ministeriais, tratados doutrinários) em chunks de 512 tokens, com recuperação vetorial subsequente, pode ser implementada com o código disponível no repositório associado ao artigo.

---

## Citações relevantes

> "O BumbaBERT (específico de domínio) teve o melhor desempenho, confirmando que a especialização de domínio é crucial para a recuperação semântica eficaz em cenários de zero-shot no contexto jurídico brasileiro." (resumo)

> "A segmentação de documentos longos é um pré-requisito indispensável para o uso de modelos BERT em processos judiciais completos." (seção de metodologia)

---

## Conexões com a tese

- BumbaBERT como alternativa a testar para recuperação semântica no `iconocracy-corpus`
- Pipeline chunking + Elasticsearch diretamente adaptável para o corpus de textos doutrinários históricos
- Complementar com [[JUSTINO et al — Comparative BERT Brazilian legal precedents (2025)]] para abordagem via task-specific fine-tuning (SBERT-pt)
- Limitação a registrar na dissertação: todos os benchmarks disponíveis usam corpus contemporâneo, não histórico
