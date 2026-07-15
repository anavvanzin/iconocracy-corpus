---
tipo: nota-tecnica
titulo: "AI Agent Super-Skill — guia de referência para construir agentes de IA"
fonte: "https://www.perplexity.ai/computer/skills/SpTJD44kSSKQ0gFgKLxrkA?skillId=4a94c90f-8e24-4922-90d2-016028bc6b90"
tags:
  - ferramentas/ia
  - skills/ai-agent-super-skill
data: 2026-07-10
---

# AI Agent Super-Skill: guia de referência para construir agentes de IA

A [ai-agent-super-skill](https://www.perplexity.ai/computer/skills/SpTJD44kSSKQ0gFgKLxrkA?skillId=4a94c90f-8e24-4922-90d2-016028bc6b90) é uma skill de referência abrangente que funde os padrões de orquestração de agentes do Claude Code com a infraestrutura de implantação do Perplexity Computer. Ela cobre doze domínios — da arquitetura de um único agente até sistemas de produção com múltiplos agentes coordenados, servidores MCP, pipelines RAG, e monitoramento contínuo. Este artigo sintetiza essas doze áreas em prosa contínua, mantendo as tabelas de decisão que tornam a skill operacional no dia a dia.

## 1. Arquitetura e padrões de agentes

Todo agente segue o mesmo laço fundamental: observar, pensar, agir, observar novamente. O que distingue uma arquitetura de outra é a profundidade do planejamento antes de agir e a forma como os resultados de ferramentas são tratados. Quatro padrões cobrem a maior parte dos casos de uso:

- **ReAct** (Razão + Ação) — intercala pensamento e ação em um único fio de conversa; ideal para pesquisa aberta e suporte ao cliente, onde o caminho não é conhecido de antemão.
- **Plan-and-Execute** — um planejador gera a lista completa de passos antes de qualquer execução; ideal para relatórios estruturados e geração de código, onde auditabilidade e checkpoints importam.
- **Reflexion** — o agente avalia sua própria tentativa, armazena uma reflexão e tenta de novo; ideal para depuração de código e escrita, onde a qualidade melhora a cada ciclo de autocrítica.
- **Tool-Use (function calling nativo)** — usa o recurso de chamada de ferramentas do próprio modelo; menor latência, menos engenharia de prompt.

| Objetivo | Padrão recomendado |
|---|---|
| Pesquisa aberta | ReAct |
| Relatório multi-etapas | Plan-Execute |
| Depuração de código | Reflexion |
| Integração de API | Tool-Use |
| Suporte ao cliente | ReAct + Tool-Use (híbrido) |

Quando um único agente não basta, a skill descreve quatro topologias multiagente: **hub-and-spoke** (orquestrador que decompõe e distribui para especialistas), **pipeline** (linha de montagem em estágios sequenciais), **competitivo/debate** (dois agentes divergentes avaliados por um juiz) e **rede de pares** (coordenação por consenso, útil em simulação, mas de alto custo de coordenação para automação de produção).

## 2. Construção de servidores MCP

Um servidor MCP (Model Context Protocol) de produção segue um processo de quatro fases que não deve ser abreviado: pesquisa e planejamento da API-alvo, implementação (com templates prontos em TypeScript ou Python/FastMCP), revisão e teste via MCP Inspector, e criação de dez perguntas de avaliação — read-only, verificáveis por comparação de string, exigindo três ou mais chamadas de ferramenta. O checklist de design de ferramentas exige nomes no padrão `serviço_verbo_substantivo`, anotações explícitas (`readOnlyHint`, `destructiveHint`, `idempotentHint`) e mensagens de erro que sugerem uma ação corretiva em vez de apenas relatar a falha — a diferença entre "Not found" e "Item '{id}' não encontrado. Use service_list_items para localizar IDs válidos."

## 3. Construção de sistemas RAG

O pipeline RAG completo tem duas metades: ingestão (documento → *chunker* → *embedder* → banco vetorial) e consulta (pergunta → embed → busca vetorial → *reranker* → LLM). A escolha da estratégia de *chunking* depende da estrutura do texto:

| Estratégia | Tamanho do bloco | Melhor uso |
|---|---|---|
| Tamanho fixo | 500–1000 tokens | Texto geral, estrutura desconhecida |
| Por sentença | 3–5 sentenças | Notícias, documentação |
| Semântica | Variável | Artigos de pesquisa, livros |
| Recursiva/hierárquica | Pai-filho | Documentos longos com cabeçalhos |

A seleção do banco vetorial segue critério semelhante: Pinecone para produção sem operação própria, Qdrant para baixa latência crítica, Weaviate para busca híbrida (palavra-chave + vetor), Chroma para prototipagem local, pgvector quando já existe stack Postgres. A qualidade do pipeline é medida por métricas concretas — relevância de contexto acima de 0,80, fidelidade da resposta acima de 0,90, precisão de recuperação top-5 acima de 0,70 — não por impressão subjetiva.

## 4. Coordenação de subagentes

O princípio central é simples de enunciar e fácil de violar: subagente novo por tarefa, mais revisão em dois estágios — primeiro conformidade com a especificação, só depois qualidade de código. A ordem importa porque revisar qualidade de código que ainda não atende à especificação desperdiça ciclos de revisão inteiros. Os erros mais comuns listados pela skill: despachar múltiplos agentes implementadores em paralelo no mesmo repositório (conflito de merge garantido), deixar o subagente ler arquivos de plano em vez de receber o texto completo da tarefa já injetado no prompt, e aceitar conformidade "razoável" quando o revisor encontrou problemas reais.

## 5. Planejamento e verificação de execução

Duas ou mais tarefas independentes que não escrevem no mesmo recurso podem ser despachadas em paralelo; tarefas relacionadas ou que tocam os mesmos arquivos devem ser sequenciais, sob pena de conflito. A execução em lotes com checkpoints — por padrão, três tarefas por lote — exige leitura do plano, criação de lista de tarefas, execução com verificação explícita a cada passo, e um relatório de checkpoint antes de avançar ao lote seguinte. Três níveis de verificação (smoke, funcional, aceitação) escalam a exigência: do "a aplicação inicia sem erros" ao "a funcionalidade funciona de ponta a ponta conforme especificado, com revisão de segurança aprovada".

## 6. Engenharia e otimização de prompts

| Padrão | Quando usar | Custo em tokens |
|---|---|---|
| Zero-shot | Tarefas simples e bem definidas | Mínimo |
| Few-shot (3–5 exemplos) | Tarefas complexas, formato consistente | Médio |
| Chain-of-Thought | Raciocínio, lógica multi-etapas | Médio |
| Saída estruturada | Necessidade de JSON/XML parseável | Baixo (alta confiabilidade) |
| Tree-of-Thought | Resolução complexa com retrocesso | Alto |
| Meta-prompting | Gerar ou otimizar outros prompts | Alto |

O fluxo de otimização recomendado é iterativo: estabelecer uma linha de base, identificar o problema específico (saída ambígua → especificar formato; resultados inconsistentes → adicionar enquadramento de papel; raciocínio pobre → adicionar gatilho de cadeia de pensamento), aplicar a otimização, comparar contra a linha de base, e só aceitar a mudança se a qualidade subir e o custo não passar de 1,2× o original.

## 7. Integração de ML para agentes

Uma camada de abstração de provedor de LLM permite alternar entre Anthropic, OpenAI e outros sem reescrever a lógica do agente, com *fallback* automático quando o provedor primário falha. Para servir agentes em produção, a skill compara estratégias: FastAPI/Uvicorn para APIs REST de baixa latência, Ray Serve para pipelines multi-modelo em alta escala, inferência serverless para cargas de trabalho intermitentes. O monitoramento inclui detecção de *drift* na distribuição de entradas (via teste de Kolmogorov-Smirnov sobre o comprimento das consultas) e limiares de alerta para latência p95, taxa de erro, custo por consulta e taxa de falha de ferramentas.

## 8. Criação e empacotamento de skills

Toda skill do Perplexity Computer segue um formato exato de `SKILL.md`: front matter YAML com `name`, `description`, `license` e `metadata` (autor e versão entre aspas), seguido de seções obrigatórias — quando usar, conceitos centrais, processo passo a passo, exemplos, erros comuns. O campo `description` é o gatilho de carregamento e precisa ser calibrado: nem tão vago que dispare sempre, nem tão restrito à frase exata que perca a maioria das invocações reais — o objetivo é disparar por intenção, não por correspondência literal de texto.

## 9. Infraestrutura de backend para agentes

Para memória persistente entre sessões sem provisionar um servidor dedicado, a skill propõe o padrão CGI-bin com SQLite: endpoints HTTP simples para sessões, mensagens e fatos aprendidos, todos implantados junto com o frontend. O mesmo padrão sustenta um receptor de webhooks com verificação de assinatura HMAC para disparar agentes a partir de eventos externos, e um *message bus* de publicação/assinatura para comunicação agente-a-agente — publicar em um tópico, assinar tópicos de interesse, buscar mensagens pendentes por *polling*.

## 10. Deploy e monitoramento em produção

O checklist de implantação cobre quatro frentes: infraestrutura (endpoint de saúde, encerramento gracioso, limitação de taxa, *circuit breaker*), observabilidade (logging estruturado em JSON com IDs de correlação, métricas de latência p50/p95/p99, custo e uso de tokens), segurança (chaves de API só em variáveis de ambiente, sanitização de entrada contra injeção de prompt, filtragem de saída para dados sensíveis) e controle de custo (orçamento de tokens por requisição, limites de gasto diário/mensal com alerta, cadeia de *fallback* do modelo caro para o barato). A escala recomendada varia de SQLite local para um único usuário até filas assíncronas e cluster de banco vetorial multirregião para mais de 500 usuários simultâneos.

## 11. Capacidades exclusivas do Perplexity Computer

O que distingue esta skill de um manual genérico de agentes é a camada final: mais de 400 integrações de serviços externos acessíveis via `list_external_tools` → `describe_external_tools` → `call_external_tool`, o que permite construir agentes ricos em integração sem escrever conectores customizados. A isso se somam agentes de monitoramento agendados (preço, menção de marca, regressão de desempenho, *drift* de dados), pesquisa fundamentada em tempo real via busca web, busca vertical e extração de URL — algo que um LLM isolado não tem por definição — e a possibilidade de publicar a interface de um agente como aplicação web ao vivo, com frontend e backend CGI implantados juntos, sem provisionamento de servidor separado.

## Referência rápida: quando usar o quê

| Situação | Seção aplicável |
|---|---|
| Construir um agente do zero | Arquitetura e padrões (§1) |
| Integrar uma API externa como ferramenta | Servidores MCP (§2) |
| Responder a partir de documentos privados | Sistemas RAG (§3) |
| Tarefas sequenciais com portões de qualidade | Coordenação de subagentes (§4) |
| Prompt com saída inconsistente | Engenharia de prompts (§6) |
| Estado persistente entre sessões | Infraestrutura de backend (§9) |
| Implantar em produção | Deploy e monitoramento (§10) |

## Modos de falha comuns

| Falha | Sintoma | Correção |
|---|---|---|
| Overflow de contexto | Agente perde histórico e resultados de ferramentas | Janela deslizante de memória, resumo de turnos antigos |
| Alucinação de chamada de ferramenta | Agente invoca ferramentas inexistentes | Enumerar ferramentas explicitamente; usar API nativa de tool calling |
| Injeção de prompt | Entrada do usuário sobrescreve instruções | Envolver entrada do usuário em tags XML |
| Loop infinito em ReAct | Agente nunca chega à resposta final | Contador de iterações explícito |
| Conflito entre agentes paralelos | Dois agentes editam o mesmo arquivo | Mapear arquivos por agente antes do despacho |
| Alucinação em RAG | Resposta sai do contexto recuperado | "Responda apenas com base no contexto; diga que não sabe se não estiver lá" |

---

Fonte: skill [ai-agent-super-skill](https://www.perplexity.ai/computer/skills/SpTJD44kSSKQ0gFgKLxrkA?skillId=4a94c90f-8e24-4922-90d2-016028bc6b90), biblioteca de skills do usuário.
