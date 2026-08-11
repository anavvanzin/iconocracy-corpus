---
id: DEC-2026-07-31-METODOLOGIA-2-0
data: "2026-07-31"
autor: Ana Vanzin
escopo: "instrumento metodológico — abandono do aparato de confiabilidade métrica importado"
codebook_version_antes: "2.2.1"
codebook_version_depois: "2.3.0"
status: vigente
migracao: em_andamento
licenca: CC-BY-4.0
decisoes_anteriores:
  - DEC-2026-07-28-aposentadoria-do-indice-composto
  - CONTRA-ALEGORIAS-INTEGRATION-2026-06-26
  - anexo-m5-quarto-regime-epistemico
---

# DEC-2026-07-31-METODOLOGIA-2-0 — Iconometria como ecologia metodológica plural

## Decisão

Abandonar a exigência formal de instrumentos de confiabilidade importados da análise de conteúdo quantitativa — coeficiente kappa de Cohen, alfa de Krippendorff, teste-reteste intercodificador — como requisito de rigor metodológico para o corpus *Iconocracia*.

Esses instrumentos pressupõem uma lógica de amostragem probabilística, múltiplos codificadores independentes e um ideal de replicabilidade mecânica que é estranho tanto à tradição da iconografia/iconologia jurídica quanto à historiografia do direito. A pergunta de pesquisa não é "a codificação é rigorosa?", mas sim: **qual é o padrão de rigor que as disciplinas de referência da tese efetivamente praticam?**

## Estatuto epistêmico novo

A `iconometria` é promovida a framework guarda-chuva (medição/análise de padrões iconográficos). Dentro dela, o `endurecimento` é reclassificado como um único eixo de fixidez, não como agregado métrico principal.

| Elemento | Estatuto anterior | Estatuto novo |
|----------|-------------------|---------------|
| 10 indicadores ordinais (0–3) | Componentes de escala | **Capta** (paradigma indiciário, Ginzburg) |
| Inventário verbal de atributos | Dados para média | **Forma de argumentação** |
| Atlas/topologia | Visualização auxiliar | **Operador relacional** (Warburg: Pathosformel, Zwischenraum, Nachleben) |
| Contra-alegorias | Catálogo amplo | **Teste crítico do regime** |
| `purificacao_composto` | Valor probatório principal | **Deprecated** — legado apenas |

## O que muda

1. **Codebook**: v2.2.1 → v2.3.0. `purificacao_composto` permanece no schema como `deprecated`, não é removido.
2. **Schemas**: descrições atualizadas; nenhum campo removido.
3. **Scripts**: help texts, prompts e mensagens CLI atualizados para refletir a nova terminologia.
4. **Documentos**: `METHOD_CONTRACT`, `README`, `CLAUDE.md`, `AGENTS.md`, `PLANO-TESE-ICONOCRACIA.md` alinhados.
5. **Tese**: seção metodológica reescrita; apêndice com dispositivo de controle de qualidade alternativo.

## O que permanece

- Os 10 indicadores ordinais como dados brutos.
- Os 3 regimes iconocráticos.
- O campo `endurecimento_score` como chave estável do eixo de fixidez.
- A estrutura de `records.jsonl` e `purification.jsonl`.
- A backward compatibility em `corpus-data.json`.

## Lacunas sinalizadas

As nove lacunas do ensaio são tratadas como **limitações declaradas**, não como falhas a esconder:

1. Ausência de amostragem probabilística.
2. Corpus fechado por critério de relevância, não por sorteio.
3. Codificação por pesquisador único (ou equipe reduzida).
4. Impossibilidade de replicabilidade mecânica.
5. Viés de conservação arquivística.
6. Silêncio de suportes perecíveis.
7. Concentração em regimes iconocráticos específicos.
8. Dificuldade de comparação intercorpus.
9. Dependência de fontes secundárias para itens não acessíveis digitalmente.

Cada lacuna deve ter parágrafo próprio em seção de "Limites e silêncios arquivísticos" no texto final da tese.

## Matriz de impacto

| Arquivo | Tipo de impacto | Ação |
|---------|-----------------|------|
| `tools/schemas/master-record.schema.json` | Descrição | Atualizar `description` de `purificacao_composto`, `endurecimento_score`, `indicadores` |
| `tools/schemas/purification-record.schema.json` | Descrição | Idem |
| `tools/scripts/code_purification.py` | CLI/prompt | Atualizar help text |
| `tools/scripts/compute_irr.py` | Prompt | Clareza adicional |
| `tools/scripts/irr_rater2_batch.py` | Prompt | Atualizar |
| `tools/scripts/lpai_proxy_coder_k3.py` | Help text | Verificar |
| `tools/scripts/iconocode_gemma4.py` | Help text | Verificar |
| `docs/METHOD_CONTRACT_2026-04-23.md` | Documento | Marcar como legacy; criar `METHOD_CONTRACT_2026-07-31.md` |
| `README.md` | Documento | Atualizar snapshot |
| `CLAUDE.md` | Documento | Alinhar terminologia |
| `AGENTS.md` | Documento | Alinhar guardrails |
| `docs/PLANO-TESE-ICONOCRACIA.md` | Documento | Atualizar seção 4 |

## Dispositivo de controle de qualidade alternativo

Os quatro elementos textuais que substituem os coeficientes importados:

1. **Critérios de inclusão/exclusão explícitos e auditáveis** — transparência procedimental no lugar de replicabilidade mecânica.
2. **Declaração do corpus como catálogo documentado, não amostra estatística** — elimina a pressuposição de amostragem probabilística.
3. **Justificação de casos exemplares** — mais exigente que um coeficiente, porque é argumentável e vinculado a registros concretos.
4. **Resposta antecipada à objeção de Roele** — neutraliza a crítica de impressionismo antes que ela seja formulada.

## Referências

- DEC-2026-07-28-aposentadoria-do-indice-composto
- CONTRA-ALEGORIAS-INTEGRATION-2026-06-26
- Anexo M.5 — Quarto regime epistêmico (topological atlas como Path B)
- Codebook v2.2.1 → v2.3.0
- Ginzburg, C. (paradigma indiciário)
- Warburg, A. (Pathosformel, Zwischenraum, Nachleben)
- Roele, M. (objeção de impressionismo)
