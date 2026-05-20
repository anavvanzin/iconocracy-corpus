---
id: P-2026-014
titulo: NotebookLLM → Notion tese
llm_alvo: claude
lingua: pt
dominio: meta
versao: "1.0"
criado: 2026-04-17
ultimo_uso: 2026-04-17
output_ref:
tags: [migrado-de-notas]
fonte: "Notas e Textos/prompts_do_notebook_llm_pagina_para_notion_tese.md"
---

# NotebookLLM → Notion tese

## Prompt

```
# Prompts do notebook LLM (tese) — pronto para colar no Notion

Abaixo estão os prompts consolidados, em formato de página única, para acesso rápido. Copie e cole no seu notebook LLM conforme a necessidade.

## 1) Sistema (perfil do assistente)

```text
Você é um assistente acadêmico voltado a uma tese de doutorado em Direito, História do Direito e cultura visual. Seu foco é a iconografia jurídica e política, com atenção especial às personificações alegóricas femininas da Nação e da Justiça, e a uma leitura crítica materialista do gênero. O recorte é europeu (séculos XVIII–XX, com aberturas arqueogenealógicas quando indispensáveis).

Regras de escrita e método:
1) Produza análises coesas, com linguagem precisa e neutra; evite adjetivação vazia.
2) Evite a palavra “framework”. Prefira “plano conceitual”, “arquitetura analítica”, “procedimento” ou equivalentes.
3) Evite a construção “não apenas… mas também…”.
4) Não invente dados, páginas ou referências. Quando faltar paginação, marque como “paginação não informada no trecho fornecido”.
5) Para uso futuro, sempre diferencie: (a) citação direta; (b) paráfrase; (c) formulação própria do usuário, explicitamente identificada.
6) Em toda resposta extensa, inclua ao final uma referência ABNT completa do texto analisado, se houver metadados suficientes; caso contrário, liste os elementos faltantes.
7) Sempre inclua “Posição sugerida na tese” indicando, com placeholders, em qual Parte/Capítulo/Seção o resultado se encaixa.

Quando o usuário pedir “Resumo”, responda em 1 a 3 parágrafos, sem listas. Quando pedir “Fichamento crítico”, use 10 seções padronizadas.
```

## 2) Ingestão e triagem do texto (começo de qualquer leitura)

```text
Tarefa: preparar a leitura acadêmica do texto a seguir para uso em tese.

Entrada: (cole o trecho/capítulo/artigo)

Saída exigida:
1) Identificação do objeto: tema, problema, corpus, recorte temporal e espacial inferíveis a partir do trecho, sem extrapolar.
2) Metadados bibliográficos: autor, título, ano, periódico/editora, local, páginas do trecho (se presentes). Se faltar algo, liste “elementos ausentes”.
3) Vocabulário técnico presente no trecho: termos-chave e como aparecem no texto, com definições operacionais provisórias (provisórias porque dependem do conjunto da obra).
4) Diagnóstico de utilidade para a tese: em que ponto o texto ajuda (iconografia jurídica, alegoria, nacionalismo, gênero, Estado/direito, cultura visual, metodologia) e em que ponto é periférico.
5) Posição sugerida na tese (Parte/Capítulo/Seção, com placeholders).

Restrições: não inventar paginação nem referências; evitar “framework” e evitar “não apenas… mas também…”.
```

## 3) Fichamento crítico em 10 itens (padrão tese)

```text
Produza um Fichamento crítico em 10 itens do texto a seguir (cole o trecho).

Estrutura obrigatória:
1) Referência completa ABNT (se faltar dado, explicitar o que falta).
2) Identificação do objeto: tema, problema, corpus, recorte temporal e espacial.
3) Tese central e objetivos do autor.
4) Arquitetura do argumento: passos, conceitos-chave e evidências.
5) Metodologia e posição teórica do autor (apenas o que o texto permite afirmar).
6) Contribuições, limites e ambiguidades.
7) Relações úteis: conexões diretas com iconografia jurídica, alegorias femininas da Nação/Justiça, crítica materialista do gênero, e com autores correlatos quando houver base textual.
8) Citações relevantes com paginação (somente se a paginação estiver visível; caso contrário, indicar ausência).
9) Vocabulário-chave com definições operacionais.
10) Itens de uso prático: o que incorporar em quais seções da tese, quais notas de rodapé redigir, quais imagens/documentos legais cotejar.

Ao final: “Posição sugerida na tese: Parte X, Capítulo Y, Seção Z (proposta)”.
Restrições: não inventar dados; evitar “framework”; evitar “não apenas… mas também…”.
```

## 4) Extração de citações com páginas (para Obsidian)

```text
Extraia do texto a seguir (cole o trecho) de 6 a 12 citações diretas que sejam reutilizáveis na tese.

Para cada citação:
1) transcreva fielmente;
2) indique a página exata. Se não houver paginação no trecho, marque “paginação não informada” e não invente;
3) justifique em 1 a 2 frases por que a citação é útil (conceito, definição, passagem metodológica, formulação histórica).

Feche com:
a) 5 palavras-chave do conjunto das citações;
b) “Posição sugerida na tese” (Parte/Capítulo/Seção).
```

## 5) Mapa de conceitos (formato Obsidian)

```text
A partir do texto a seguir (cole o trecho), produza um mapa de conceitos em formato compatível com Obsidian, com links no padrão [[conceito]].

Saída:
1) Uma nota principal com o título: [[Autor, ano — conceito central]] contendo 2 parágrafos de síntese.
2) Uma seção “Conceitos e relações” com pares do tipo: [[conceito A]] → relação → [[conceito B]], acompanhados de 1 frase de explicação.
3) Uma seção “Pontes para a tese” com 5 pontes concretas: qual subproblema da tese isso alimenta, e qual evidência visual ou jurídico-textual pode ser acoplada.
4) “Posição sugerida na tese” (Parte/Capítulo/Seção).

Restrições: não inventar páginas, evitar “framework”, evitar “não apenas… mas também…”.
```

## 6) Quadro comparativo (tabela + síntese)

```text
Compare os dois textos/trechos a seguir (A e B), com foco na sua tese (iconografia jurídica, alegoria feminina, nacionalismo, gênero, materialidade do poder).

Saída:
1) Uma tabela com: (i) tese; (ii) conceitos operacionais; (iii) método; (iv) evidências mobilizadas; (v) implicações para o direito/Estado; (vi) utilidade e riscos para a sua argumentação.
2) Depois da tabela, escreva 1 parágrafo interpretativo indicando convergências, fricções e um caminho de síntese possível para um capítulo.
3) “Posição sugerida na tese”.

Restrições: não inventar dados; evitar “framework”; evitar “não apenas… mas também…”.
```

## 7) Integração ao sumário da tese (texto incorporável + notas ABNT)

```text
Objetivo: transformar o texto a seguir (cole o trecho) em material imediatamente incorporável à tese.

Saída:
1) Uma proposta de subseção (título e 2 a 4 parágrafos) escrita em voz acadêmica, sem copiar frases longas do original.
2) Um bloco de 3 a 6 notas de rodapé em estilo ABNT (modelos), com placeholders quando faltar dado, e com indicação do local exato em que cada nota entra no texto.
3) Uma lista curta de “evidências a cotejar” (imagens, frontispícios, moedas, selos, constituições, catecismos cívicos, manuais escolares, repertórios iconográficos), baseada no que o trecho sugere, sem extrapolar.
4) “Posição sugerida na tese: Parte X, Capítulo Y, Seção Z”.

Restrições: não inventar referências; evitar “framework”; evitar “não apenas… mas também…”.
```

## 8) Análise iconográfica em três níveis (descrição ou texto descritivo)

```text
Aplique um procedimento de análise iconográfica em três níveis ao material a seguir.

Entrada: (i) descrição da imagem OU (ii) trecho que descreve/evoca a imagem

Saída:
1) Nível descritivo: inventário do que aparece (figuras, atributos, gestos, inscrições, cenário, objetos jurídicos).
2) Nível convencional: identificação de motivos e repertórios (alegorias, atributos da Justiça/Nação, sinais de soberania, figuras marianas secularizadas quando houver base).
3) Nível histórico-problemático: qual operação política e jurídico-simbólica a imagem sustenta; como o corpo feminino é mobilizado como autoridade visual; quais tensões com a exclusão jurídica das mulheres o material permite sustentar.
4) Indique 2 a 4 comparáveis (tipos de imagem) a cotejar.
5) “Posição sugerida na tese”.

Regra: se o dado não estiver na descrição, não inferir como fato; marcar como hipótese interpretativa.
```

## 9) Auditoria terminológica e anacronismo (Estado, soberania, cidadania)

```text
Faça uma auditoria terminológica do texto a seguir (cole o trecho), com foco em evitar anacronismos e imprecisões, especialmente em: Estado, estatal, soberania, nação, povo, cidadania, representação, corpo político.

Saída:
1) Termos potencialmente anacrônicos ou vagos: liste e explique por que são problemáticos.
2) Sugestões de substituição conceitualmente mais rigorosas (sem alterar o sentido do autor).
3) Uma versão revisada de 1 parágrafo do trecho (escolha o parágrafo mais crítico), mantendo o conteúdo, elevando a precisão.
4) “Posição sugerida na tese”.

Restrições: não inventar dados; preservar a intenção do autor; evitar “framework”.
```

## 10) Tradução acadêmica com notas em ABNT (parágrafo a parágrafo)

```text
Traduza para o português acadêmico o trecho a seguir, preservando o sentido com máxima fidelidade e evitando paráfrases que apaguem a estrutura do argumento.

Regras:
1) Inserir chamadas numeradas de nota de rodapé no corpo do texto quando houver notas no original, e posicionar as notas ao final do parágrafo traduzido.
2) Traduzir literalmente as notas, mantendo títulos de obras citadas no idioma original.
3) Ao final de cada parágrafo traduzido, listar as referências completas em ABNT correspondentes às notas usadas naquele parágrafo, sinalizadas pelos mesmos números.
4) Evitar negrito e itálico.
5) Se faltar dado bibliográfico, usar placeholders e listar “dados ausentes”.

Fechar com: “Posição sugerida na tese”, se o trecho traduzido for incorporável.
```

## 11) Perguntas-guia para seminário (com pistas de resposta)

```text
Com base no texto a seguir (cole o trecho), formule 10 perguntas-guia de seminário voltadas a uma discussão de pós-graduação, com ênfase em:
a) método e evidência;
b) relação entre imagem e autoridade jurídico-política;
c) figurações do feminino e exclusão material.

Para cada pergunta, acrescente 2 a 3 linhas de “pistas de resposta” baseadas no trecho, sem inventar dados.

Fechar com: “Posição sugerida na tese”.
```

## 12) Bibliografia de continuidade + strings de busca (bases acadêmicas)

```text
A partir do texto a seguir (cole o trecho), proponha uma bibliografia de continuidade em duas camadas:
1) Núcleo indispensável (5 a 8 itens) diretamente pertinente ao problema do trecho.
2) Expansão estratégica (8 a 12 itens) para ampliar debate historiográfico, cultura visual e história do direito.

Para cada item: referência em ABNT (com placeholders se faltar dado) e 1 frase justificando a pertinência.

Depois, gere 12 strings de busca, em português, inglês e francês, adequadas para bases como HeinOnline, JSTOR, Project MUSE, Cairn e catálogos de bibliotecas.

Fechar com: “Posição sugerida na tese”.
Restrições: não inventar dados; sinalizar incerteza quando necessário.
```
```
