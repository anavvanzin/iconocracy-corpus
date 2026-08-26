# Especificação do Dataset v1 — ICONOCRACY SFT

## 1. Formato

Cada linha do dataset deve ser um objeto JSON com, no mínimo:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "metadata": {
    "task_type": "record_analysis",
    "source_file": "data/processed/records.jsonl"
  }
}
```

O treino SFT deve aprender **respostas completas do assistant**. O conteúdo do `system` pode ser constante ou controlado por famílias de tarefa.

---

## 2. Famílias de tarefa

### A. `guardrails`
Ensina identidade do projeto, terminologia, proibições e fluxo correto.

Exemplos:
- corrigir uso indevido de termos
- recusar tradução de `endurecimento`
- reafirmar cadeia de rastreabilidade
- distinguir tese vs. projeto

### B. `chapter_planning`
Ensina estrutura da tese, dependências, riscos e lógica entre capítulos.

Exemplos:
- qual capítulo depende de qual
- qual é o caminho crítico
- como justificar a transição QUAN → QUAL
- quais riscos estão mapeados

### C. `record_analysis`
Transforma um registro do `records.jsonl` em uma nota analítica inicial.

Entrada típica:
- título, data, lugar, resumo de evidência, motivos observados, códigos, claims

Saída típica:
- 1 a 3 parágrafos
- linguagem acadêmica clara
- sem inventar evidência além do registro
- com conexão ao léxico da tese quando suportado

### D. `purification_analysis`
Interpreta linhas de `purification.jsonl`.

Entrada típica:
- 10 indicadores
- `purificacao_composto`
- `regime_iconocratico`

Saída típica:
- diagnóstico de intensidade
- leitura dos indicadores dominantes
- comentário sobre endurecimento/purificação quando cabível

### E. `method_explainer`
Explica método, corpus, protocolo e desenho de pesquisa.

Fontes:
- `AGENT_CONFIG_ICONOCRACIA.md`
- planos aprovados

---

## 3. Regras de ouro para as respostas

1. Não inventar fatos não presentes na entrada.
2. Não transformar qualquer registro em argumento forte sem suporte.
3. Não traduzir `endurecimento`.
4. Não atribuir `Feminilidade de Estado` a Mondzain.
5. Não quebrar a voz jurídico-histórica.
6. Não descrever a IA como substituta do trabalho interpretativo humano.

---

## 4. Regras por família

### `record_analysis`
A resposta deve, quando possível:
- situar o item no repertório alegórico
- mencionar suporte/medium
- distinguir observação de inferência
- usar cautela epistêmica
- sugerir relevância analítica sem sobre-afirmar

### `purification_analysis`
A resposta deve:
- classificar aproximadamente o composto em baixo/médio/alto
- comentar os indicadores mais salientes
- manter coerência com o regime iconocrático informado
- não inferir imagem ausente

### `chapter_planning`
A resposta deve:
- ancorar-se nos planos existentes
- deixar claro dependências e riscos
- priorizar a lógica já aprovada pela autora

---

## 5. Faixas recomendadas de tamanho

- `guardrails`: 80–220 palavras
- `chapter_planning`: 120–300 palavras
- `record_analysis`: 120–220 palavras
- `purification_analysis`: 90–180 palavras
- `method_explainer`: 120–260 palavras

---

## 6. Estratégia de qualidade

### Revisão manual mínima
Antes do treino principal, revisar manualmente pelo menos:
- 20 exemplos de `guardrails`
- 20 de `chapter_planning`
- 30 de `record_analysis`
- 30 de `purification_analysis`

### Critérios de descarte
Descartar exemplos que estejam:
- redundantes demais
- formulaicos em excesso
- com prosa ruim
- com extrapolação indevida
- com termos inconsistentes com a tese

---

## 7. Split recomendado

- `train`: 90–95%
- `validation`: 5–10%

Fazer split por linha depois de congelar o dataset, ou gerar arquivos separados.

---

## 8. Convenções de metadados

Metadados recomendados:

```json
{
  "task_type": "record_analysis",
  "source_file": "data/processed/records.jsonl",
  "record_id": "...",
  "language": "pt-BR",
  "style": "juridico-historico"
}
```

---

## 9. Critério para futura fase DPO

Só vale avançar para DPO quando houver pares comparativos reais do tipo:
- resposta preferida vs. resposta rejeitada
- mais aderente vs. menos aderente à tese
- mais rigorosa vs. mais genérica

Antes disso, SFT é a etapa correta.
