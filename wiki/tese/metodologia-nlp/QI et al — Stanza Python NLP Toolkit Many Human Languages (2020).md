---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Qi, Peng"
  - "Zhang, Yuhao"
  - "Zhang, Yuhui"
  - "Bolton, Jason"
  - "Manning, Christopher D."
ano: 2020
titulo: "Stanza: A Python Natural Language Processing Toolkit for Many Human Languages"
publicacao: "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations"
editora: Association for Computational Linguistics
doi: "10.18653/v1/2020.acl-demos.14"
url: "https://aclanthology.org/2020.acl-demos.14"
idioma: en
tags:
  - metodologia/nlp
  - nlp/multilíngue
  - nlp/anotacao
  - nlp/universal-dependencies
  - nlp/portuguese
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]]"
  - "[[CHALKIDIS et al — Legal-BERT (2020)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

QI, Peng; ZHANG, Yuhao; ZHANG, Yuhui; BOLTON, Jason; MANNING, Christopher D. Stanza: A Python Natural Language Processing Toolkit for Many Human Languages. In: **Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations**. [S. l.]: Association for Computational Linguistics, 2020. p. 101-108. DOI: 10.18653/v1/2020.acl-demos.14. Disponível em: https://aclanthology.org/2020.acl-demos.14. Acesso em: 8 abr. 2026.

---

## Síntese

O Stanza é um toolkit de PLN desenvolvido pelo Stanford NLP Group que oferece uma pipeline neural completa para mais de 60 línguas, incluindo português. O argumento fundador do sistema é a universalidade arquitetural: a mesma rede neural, com parâmetros treinados sobre os treebanks do projeto Universal Dependencies (UD), generaliza competitivamente para todas as línguas testadas, sem adaptações arquiteturais por língua. O sistema cobre as etapas fundamentais de análise linguística: tokenização, segmentação de sentenças, etiquetagem morfossintática (POS), análise de dependências, lematização e Reconhecimento de Entidades Nomeadas (REN).

Para o português, o Stanza oferece dois modelos distintos: `pt` (baseado no treebank UD Portuguese Bosque) e `pt_br` (baseado no treebank UD Portuguese GSD), treinados sobre corpus anotado com análise de dependências universais. Os modelos neurais utilizam representações LSTM bidirecionais e, nas versões mais recentes, camadas de atenção inspiradas nos Transformers. O sistema está disponível como pacote Python e é instalável em uma linha de código, com download automático dos modelos. A integração com Jupyter é nativa e as anotações são exportáveis em formato CoNLL-U, padrão universal para corpus anotados linguisticamente.

Uma funcionalidade relevante é a interface Python para o Stanford CoreNLP (em Java), que estende o Stanza para tarefas adicionais como resolução de co-referência, extração de relações e análise de sentimento, ausentes no módulo Python nativo.

---

## Análise crítica

O Stanza ocupa, no pipeline metodológico do `iconocracy-corpus`, um nicho distinto e complementar ao BERTimbau. Enquanto o BERTimbau é superior para tarefas de compreensão semântica de alto nível (similaridade, classificação, NER com contexto), o Stanza é mais adequado para anotação morfossintática precisa e análise de estrutura gramatical, especialmente quando o objetivo é criar um corpus linguisticamente anotado compatível com padrões internacionais (UD/CoNLL-U).

Para a tese, há dois contextos de uso privilegiados. O primeiro é o processamento de textos em francês: o Stanza oferece modelos de alta qualidade para o francês (`fr`, treinado sobre o treebank GSD), o que é relevante para os documentos relacionados a Marianne, à legislação da Terceira República e à iconografia da *Semeuse* de Roty. O segundo contexto é a análise comparativa de estruturas sintáticas em textos jurídicos de períodos históricos distintos, por exemplo, comparar a estrutura argumental de decretos imperiais brasileiros com a de leis republicanas posteriores.

Um ponto de atenção: o Stanza para português histórico (século XIX) não foi treinado sobre esse tipo de texto. O UD Portuguese Bosque é um corpus contemporâneo de jornais. A distância histórica pode introduzir erros de lematização e de POS tagging, particularmente em formas verbais arcaicas e vocabulário jurídico específico. Este é o mesmo problema do *domain shift* identificado no artigo de Chalkidis et al. (2020), mas aplicado à dimensão temporal em vez da dimensão temática.

O artigo demonstra que a abordagem UD é produtiva precisamente por sua universalidade: toda anotação produzida pelo Stanza pode ser comparada diretamente com corpus em outras línguas que usem o mesmo padrão. Isso abre a possibilidade metodológica de construir um corpus anotado multilíngue comparativo (textos FR, DE, UK, BR, US sobre alegorias femininas), com análise de dependências unificada.

---

## Citações relevantes

> "Stanza is built with a strong focus on getting accurate models for as many human languages as possible." (p. 101)

> "The same neural architecture generalizes well and achieves competitive performance on all languages tested." (p. 102)

> "Stanza includes a native Python interface to the widely used Java Stanford CoreNLP software, which further extends its functionality." (p. 107)

---

## Conexões com a tese

- Uso prioritário para corpus em francês (textos sobre Marianne, legislação da Terceira República)
- Possibilidade de anotação UD comparativa multilíngue (FR, DE, UK, BR, US)
- Complementar ao BERTimbau na pipeline de análise do corpus
- Exportação em CoNLL-U compatível com padrões internacionais de corpus histórico digital
- Ver [[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]] para a camada semântica que complementa a anotação morfossintática do Stanza
