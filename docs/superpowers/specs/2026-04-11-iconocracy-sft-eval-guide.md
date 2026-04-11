# Guia de avaliação pós-treino — ICONOCRACY SFT v1.1

## Objetivo

Avaliar se o modelo fine-tunado passou a operar como assistente especializado da tese, e não apenas como um instruct model genérico com algum vocabulário novo.

Arquivo de prompts:
- `data/training/iconocracy_eval_prompts_v1_1.jsonl`

---

## 1. O que checar

### A. Terminologia e guardrails
O modelo deve:
- manter `ENDURECIMENTO` em português
- não atribuir `Feminilidade de Estado` a Mondzain
- respeitar a cadeia de rastreabilidade do corpus
- tratar claims do pipeline como hipóteses, não como prova final

### B. Método
O modelo deve:
- explicar corretamente o desenho QUAN→QUAL→síntese
- identificar o papel do IconoCode
- distinguir `records.jsonl` de `purification.jsonl`

### C. Planejamento da tese
O modelo deve:
- responder com aderência aos planos aprovados
- reconhecer o caminho crítico
- justificar transições entre capítulos
- diferenciar projeto prudente e tese consolidada

### D. Transformação de corpus em análise
O modelo deve:
- produzir prosa útil, mas cautelosa
- distinguir observação de inferência
- usar léxico da tese sem inflar o argumento
- evitar inventar contexto não presente no registro

### E. Interpretação de indicadores
O modelo deve:
- ler compostos baixos, médios e altos adequadamente
- identificar indicadores dominantes
- manter a interpretação em nível comparativo
- não descrever imagem ausente

---

## 2. Escala sugerida

Para cada prompt, atribuir nota 0–2 em cada eixo:

- `correção conceitual`
- `aderência terminológica`
- `prudência epistêmica`
- `qualidade da prosa`
- `utilidade para a tese`

Escala:
- `0` = falho
- `1` = parcialmente adequado
- `2` = adequado

Pontuação total por prompt: 0–10.

---

## 3. Sinais de sucesso

O fine-tune está funcionando se o modelo:
- usar espontaneamente o vocabulário correto sem soar mecânico;
- parar de responder como assistente generalista de humanidades;
- converter registros do corpus em notas analíticas preliminares úteis;
- manter cautela diante de hipóteses já contidas no pipeline;
- responder perguntas de método e planejamento com boa aderência aos documentos do projeto.

---

## 4. Sinais de fracasso

O fine-tune ainda está fraco se o modelo:
- traduzir `ENDURECIMENTO`;
- atribuir conceitos originais da tese a autores de referência;
- transformar toda resposta em retórica grandiosa e pouco controlada;
- tomar claims do pipeline como fatos estabelecidos;
- voltar a um português genérico, pouco jurídico-histórico;
- perder a distinção entre corpus canônico, espelho do vault e saídas derivadas.

---

## 5. Procedimento recomendado

1. Rodar todos os prompts do arquivo JSONL.
2. Salvar respostas do modelo base e do modelo fine-tunado.
3. Comparar lado a lado.
4. Marcar onde o fine-tune melhorou, piorou ou ficou igual.
5. Usar os piores casos como matéria-prima para um futuro dataset DPO ou nova rodada de SFT.

---

## 6. Próximo uso dos resultados

- Se o modelo melhorar claramente em terminologia + método + análise de registros, o dataset v1.1 já justifica uma rodada maior.
- Se melhorar só em estilo, mas não em prudência/metodologia, o próximo passo deve ser ampliar exemplos de guardrails e método.
- Se piorar fluência ou começar a soar excessivamente rígido, o dataset está overfit em templates e precisa de mais variação.
