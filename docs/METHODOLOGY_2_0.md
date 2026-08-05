# Metodologia 2.0 — Iconometria como ecologia metodológica plural

> **Versão**: 2.3.0
> **Data**: 2026-07-31
> **Autor**: Ana Vanzin
> **Status**: vigente
> **Decisão formal**: [DEC-2026-07-31-METODOLOGIA-2-0](decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md)

---

## 1. Problema

O corpus core de 328 registros (moedas, selos, brasões, monumentos, arquitetura forense, paratextos normativos) foi codificado com um inventário verbal de atributos e uma tipologia de recusas iconocráticas. Resta indeterminado, porém, se esse aparato de codificação deve ser acompanhado de instrumentos de confiabilidade importados da análise de conteúdo quantitativa — coeficiente kappa de Cohen, alfa de Krippendorff, teste-reteste intercodificador.

Esses instrumentos pressupõem uma lógica de amostragem probabilística, múltiplos codificadores independentes e um ideal de replicabilidade mecânica que é estranho tanto à tradição da iconografia/iconologia jurídica quanto à historiografia do direito. A pergunta de pesquisa, portanto, não é "a codificação é rigorosa?", mas sim:

> **Qual é o padrão de rigor que as disciplinas de referência da tese — iconografia jurídica, história visual do direito, história da arte de inspiração warburguiana, historiografia jurídica brasileira e internacional — efetivamente praticam, e o que esse padrão exige do aparato metodológico da Iconocracia?**

---

## 2. Fundamentação disciplinar

### 2.1 Iconografia/iconologia jurídica
O corpus é tratado como objeto visual dotado de historicidade, não como amostra estatística. O rigor não vem da replicabilidade mecânica, mas da explicitação do procedimento de leitura iconográfica.

### 2.2 História visual do direito
A metodologia preserva a especificidade do suporte iconográfico (moedas, selos, monumentos, arquitetura forense, paratextos normativos). Cada suporte carrega constraints técnicas e simbólicas que não são capturáveis por indicadores agregados.

### 2.3 Tradição warburguiana
Mantém-se o vocabulário canônico (`Pathosformel`, `Zwischenraum`, `Nachleben`) e a atenção à persistência visual, sem reduzi-los a indicadores. O atlas topológico é operador relacional, não mera visualização.

### 2.4 Historiografia jurídica brasileira e internacional
A crítica ao modelo importado de confiabilidade intercodificador dialoga com a tradição de rigor por explicitação, não por métrica. O que as disciplinas de referência efetivamente praticam é a transparência procedimental.

---

## 3. Estatuto epistêmico novo

A `iconometria` é promovida a framework guarda-chuva (medição/análise de padrões iconográficos). Dentro dela, o `endurecimento` é reclassificado como um único eixo de fixidez, não como agregado métrico principal.

| Elemento | Estatuto anterior | Estatuto novo |
|----------|-------------------|---------------|
| 10 indicadores ordinais (0–3) | Componentes de escala | **Capta** (paradigma indiciário, Ginzburg) |
| Inventário verbal de atributos | Dados para média | **Forma de argumentação** |
| Atlas/topologia | Visualização auxiliar | **Operador relacional** (Warburg: Pathosformel, Zwischenraum, Nachleben) |
| Contra-alegorias | Catálogo amplo | **Teste crítico do regime** |
| `purificacao_composto` | Valor probatório principal | **Deprecated** — legado apenas |

---

## 4. Dispositivo de controle de qualidade alternativo

Os quatro elementos textuais que substituem os coeficientes importados:

### 4.1 Critérios de inclusão/exclusão explícitos e auditáveis
Transparência procedimental no lugar de replicabilidade mecânica. Cada registro do corpus deve ter seu critério de entrada declarado e auditável.

### 4.2 Declaração do corpus como catálogo documentado, não amostra estatística
Elimina a pressuposição de amostragem probabilística que fundamenta kappa/alfa. O corpus é um catálogo construído por relevância, não por sorteio.

### 4.3 Justificação de casos exemplares
Mais exigente que um coeficiente, porque é argumentável e vinculado a registros concretos. Cada caso exemplar deve ter sua escolha justificada.

### 4.4 Resposta antecipada à objeção de Roele
Neutraliza a crítica de impressionismo antes que ela seja formulada. A objeção de que a análise é "meramente impressionista" é respondida proceduralmente, não estatisticamente.

---

## 5. O que muda

1. **Codebook**: v2.2.1 → v2.3.0. `purificacao_composto` permanece no schema como `deprecated`, não é removido.
2. **Schemas**: descrições atualizadas; nenhum campo removido.
3. **Scripts**: help texts, prompts e mensagens CLI atualizados para refletir a nova terminologia.
4. **Documentos**: `METHOD_CONTRACT`, `README`, `CLAUDE.md`, `AGENTS.md`, `PLANO-TESE-ICONOCRACIA.md` alinhados.
5. **Tese**: seção metodológica reescrita; apêndice com dispositivo de controle de qualidade alternativo.

---

## 6. O que permanece

- Os 10 indicadores ordinais como dados brutos.
- Os 3 regimes iconocráticos.
- O campo `endurecimento_score` como chave estável do eixo de fixidez.
- A estrutura de `records.jsonl` e `purification.jsonl`.
- A backward compatibility em `corpus-data.json`.

---

## 7. Lacunas declaradas — Limites e silêncios arquivísticos

As nove lacunas do ensaio são tratadas como **limitações declaradas**, não como falhas a esconder. Isso é o que transforma "falta de estatística" em "posição metodológica consciente".

1. **Ausência de amostragem probabilística** — o corpus não é uma amostra, é um catálogo construído por relevância.
2. **Corpus fechado por critério de relevância, não por sorteio** — a seleção é intencional, não aleatória.
3. **Codificação por pesquisador único (ou equipe reduzida)** — a replicabilidade é interpretativa, não mecânica.
4. **Impossibilidade de replicabilidade mecânica** — a análise iconográfica é, por natureza, interpretativa.
5. **Viés de conservação arquivística** — o corpus reflete o que sobreviveu, não o que existiu.
6. **Silêncio de suportes perecíveis** — tecidos, madeira, pinturas murais desaparecem; o corpus privilegia suportes duráveis.
7. **Concentração em regimes iconocráticos específicos** — a tese foca em regimes que deixaram rastros visuais abundantes.
8. **Dificuldade de comparação intercorpus** — não há outro corpus iconográfico jurídico com a mesma metodologia para comparar.
9. **Dependência de fontes secundárias para itens não acessíveis digitalmente** — alguns registros são conhecidos apenas por descrição ou reprodução em literatura especializada.

Cada lacuna deve ter parágrafo próprio em seção de "Limites e silêncios arquivísticos" no texto final da tese.

---

## 8. Exemplos concretos do corpus

Cada um dos 4 elementos textuais é ilustrado com registros reais do corpus.

### 8.1 Critérios de inclusão/exclusão — FR-013
A *Déclaration des droits* (FR-013, 1789) entra no corpus porque materializa o Contrato Sexual Visual em suporte normativo (paratexto). Seu critério de inclusão é explícito: documento normativo + alegoria feminina + função simbólica de Estado. A nota de vault documenta a fonte primária (BnF/Gallica), os atributos observados (Liberdade com barrete frígio, Justiça com balança) e a classificação Iconclass 44A1, permitindo auditoria completa do procedimento de inclusão.

### 8.2 Catálogo documentado — BR-009
O registro BR-009 (escultura em bronze de Alfredo Ceschiatti, 1975, Sala dos Bustos do STF) é documentado em `vault/candidatos/BR-009.md` com fonte primária, atributos observados e inferência realizada. Ele não é uma amostra de esculturas forenses brasileiras, é um item de um catálogo documentado. O contexto de iconoclasmo (ataque de 8 de janeiro de 2023) ilustra como o corpus captura não apenas a imagem, mas sua vida posterior (Nachleben).

### 8.3 Caso exemplar — FR-013 e operador relacional
FR-013 é também caso exemplar para o atlas topológico: sua posição no Zwischenraum entre texto legal e alegoria feminina ilustra o operador relacional warburguiano. A gravura não "representa" a Declaração — ela a encena visualmente, fazendo da alegoria uma terceira instância entre norma e espectador.

### 8.4 Resposta à objeção de Roele — procedimento de codificação aberto
A metodologia responde à crítica de impressionismo por meio de um procedimento de codificação aberto: critérios de inclusão/exclusão explícitos, dicionário de atributos público e regras de decisão documentadas. Isso permite replicabilidade interpretativa — outro pesquisador pode seguir o mesmo procedimento e chegar a resultados comparáveis, ainda que não idênticos.

---

## 9. Rastreabilidade

A rastreabilidade pública substitui a confiabilidade estatística. Para cada registro:

```
id → vault/candidatos/XX-NNN.md → records.jsonl → purification.jsonl → corpus-data.json
```

A matriz completa está em `docs/TRACEABILITY_MATRIX.md`.

---

## 10. Protocolo de codificação aberto

O protocolo de codificação aberto está em `docs/CODING_PROTOCOL.md`. Ele inclui:
- Critérios de inclusão/exclusão
- Dicionário de atributos
- Regras de decisão
- Exemplos de codificação

---

## 11. Referências

- DEC-2026-07-28-aposentadoria-do-indice-composto
- CONTRA-ALEGORIAS-INTEGRATION-2026-06-26
- Anexo M.5 — Quarto regime epistêmico (topological atlas como Path B)
- Codebook v2.2.1 → v2.3.0
- Ginzburg, C. (paradigma indiciário)
- Warburg, A. (Pathosformel, Zwischenraum, Nachleben)
- Roele, M. (objeção de impressionismo)
