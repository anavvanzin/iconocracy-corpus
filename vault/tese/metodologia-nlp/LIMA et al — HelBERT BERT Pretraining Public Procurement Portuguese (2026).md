---
tipo: fichamento-metodologico
subtipo: nlp-corpus
status: fichado
autores:
  - "Lima, Weslley"
  - "Silva, Victor"
  - "Silva, Jasson"
  - "Rabelo, R. A. L."
  - "Paiva, A."
ano: 2026
titulo: "HelBERT: A BERT-Based Pretraining Model for Public Procurement Tasks in Portuguese"
publicacao: "Journal of the Brazilian Computer Society (JBCS)"
editora: SBC — Sociedade Brasileira de Computação
doi: "10.5753/jbcs.2026.5511"
url: "https://journals-sol.sbc.org.br/index.php/jbcs/article/view/5511"
idioma: en
tags:
  - metodologia/nlp
  - nlp/bert
  - nlp/juridico
  - nlp/portugues-br
  - nlp/domain-pretraining
  - nlp/licitacao
  - metodologia/corpus-digital
  - iconocracy/ferramentas
related:
  - "[[Metodologia do Corpus Iconográfico]]"
  - "[[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]]"
  - "[[CHALKIDIS et al — Legal-BERT (2020)]]"
  - "[[JUSTINO et al — BERT semantic retrieval Brazilian legal documents (2025)]]"
data_fichamento: 2026-04-08
---

## Referência ABNT NBR 6023:2025

LIMA, Weslley; SILVA, Victor; SILVA, Jasson; RABELO, R. A. L.; PAIVA, A. HelBERT: A BERT-Based Pretraining Model for Public Procurement Tasks in Portuguese. **Journal of the Brazilian Computer Society**, [S. l.], 2026. DOI: 10.5753/jbcs.2026.5511. Disponível em: https://journals-sol.sbc.org.br/index.php/jbcs/article/view/5511. Acesso em: 8 abr. 2026.

---

## Síntese

O HelBERT é um modelo BERT pré-treinado especificamente sobre corpus de licitações e contratações públicas em português brasileiro, incluindo leis, editais e contratos. O artigo preenche uma lacuna no ecossistema de PLN jurídico em PT-BR: até então, os modelos específicos de domínio legal brasileiro (BERTimbau para português geral, JurisBERT para jurisprudência) não cobriam o subdomínio específico de procurement público, com sua terminologia regulatória muito particular (CNPJ, pregão, habilitação técnica, dispensa de licitação). O corpus de pré-treinamento não é divulgado em detalhes, mas os autores indicam treinamento sobre documentos de organismos públicos de múltiplos níveis (federal, estadual, municipal).

Os resultados são reportados em duas tarefas: classificação de documentos de licitação (F1 score) e similaridade semântica entre cláusulas contratuais. O HelBERT supera o BERTimbau em 5 pontos percentuais em F1 na classificação, e o JurisBERT em 4 pontos percentuais. Na tarefa de similaridade semântica, o HelBERT obtém ganhos superiores a 3% sobre os modelos baseline. Os autores enfatizam que esses ganhos foram obtidos com recursos computacionais modestos e menor número de épocas de treinamento.

O artigo constitui evidência adicional de uma tendência clara no PLN jurídico brasileiro: a progressiva especialização de modelos de linguagem em subdomínios cada vez mais específicos do direito, com ganhos de desempenho proporcionais ao nível de especialização.

---

## Análise crítica

O HelBERT é o artigo mais recente fichado nesta sessão e documenta o estado atual (2026) do ecossistema de modelos BERT para direito brasileiro. Sua importância para a tese é sobretudo cartográfica: ele confirma que a ecologia de modelos jurídicos em PT-BR está madura o suficiente para ser usada como infraestrutura metodológica de uma pesquisa em história do direito, não apenas em pesquisa computacional stricto sensu.

A progressão documentada pelos artigos fichados — BERTimbau genérico (2020) > LEGAL-BERT em inglês (2020) > Legal-BERTimbau em PT-BR (2021, STJIRIS) > BumbaBERT específico de jurisprudência (2024) > HelBERT específico de procurement (2026) — constitui ela própria um objeto de interesse metodológico para qualquer pesquisadora que use esses modelos como ferramentas. A escolha de um ou outro modelo não é neutra: cada um carrega um viés de corpus que condiciona o que "parece" semanticamente próximo e o que "parece" distante.

Para o `iconocracy-corpus`, o HelBERT é provavelmente inadequado como modelo principal (o corpus é legislativo/licitatório, não doutrinário-iconográfico), mas é útil para processar textos específicos como editais de monumentos públicos, contratos de encomenda de obras, documentação administrativa de casas da moeda e projetos de construção de edifícios forenses — todos documentos que podem integrar o corpus de fontes primárias da tese.

A tendência de especialização progressiva sugere também uma direção de pesquisa futura que a tese pode indicar em suas considerações finais: o desenvolvimento de um modelo de linguagem para história do direito visual em PT-BR, treinado sobre um corpus histórico curado de textos jurídico-iconográficos do século XIX.

---

## Citações relevantes

> "Although pretrained BERT models exist for legal documents in some languages, none target public procurement documents in Portuguese." (p. 1)

> "HelBERT surpasses models such as BERTimbau and JurisBERT in classification tasks by achieving improvements of 5% and 4% in the F1 Score, respectively." (resumo)

> "The results highlight the effectiveness of domain-specific pretraining even when working with limited GPU resources." (seção de conclusão)

---

## Conexões com a tese

- Documenta o estado atual (2026) da ecologia de modelos BERT jurídicos para PT-BR
- Progressão de especialização BERTimbau > Legal-BERTimbau > HelBERT é argumento metodológico para a escolha de modelos no `iconocracy-corpus`
- Aplicável especificamente para processamento de documentação administrativa de encomendas de monumentos e contratos de obras iconográficas
- Indica direção de pesquisa futura: modelo BERT para história do direito visual em PT-BR
- Ver [[SOUZA_NOGUEIRA_LOTUFO — BERTimbau (2020)]] para o ponto de partida desta progressão
