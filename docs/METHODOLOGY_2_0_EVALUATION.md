# Avaliação técnica e acadêmica — Metodologia 2.0 (iconometria)

> **Objeto avaliado**: texto-fonte *"O padrão metodológico efetivamente praticado na iconografia jurídica: fundamentos para o abandono do aparato de confiabilidade métrica importado"*, consolidado com as decisões já vigentes no repositório (DEC-2026-07-28, Anexo M.5, codebook v2.2.1).
>
> **Data**: 2026-07-31
> **Branch**: `feat/methodology-2-0-consolidation`
> **Worktree**: `/Users/ana/Research/hub/iconocracy-corpus-methodology-2-0`

---

## 1. Avaliação acadêmica

### 1.1 Ancoragem disciplinar
O argumento está corretamente ancorado nas disciplinas de referência da tese:

- **Iconografia/iconologia jurídica**: o corpus é tratado como objeto visual dotado de historicidade, não como amostra estatística.
- **História visual do direito**: a metodologia preserva a especificidade do suporte iconográfico (moedas, selos, monumentos, arquitetura forense, paratextos normativos).
- **Tradição warburguiana**: mantém-se o vocabulário canônico (`Pathosformel`, `Zwischenraum`, `Nachleben`) e a atenção à persistência visual, sem reduzi-los a indicadores.
- **Historiografia jurídica brasileira e internacional**: a crítica ao modelo importado de confiabilidade intercodificador dialoga com a tradição de rigor por explicitação, não por métrica.

**Veredito**: a ancoragem é suficiente para defesa de doutorado.

### 1.2 Comparabilidade em rigor
A alternativa proposta não é "menos rigorosa" — é *diferentemente rigorosa*. Os quatro elementos textuais funcionam como dispositivo de controle de qualidade:

1. **Critérios de inclusão/exclusão explícitos e auditáveis** — substituem a replicabilidade mecânica por transparência procedimental.
2. **Declaração do corpus como catálogo documentado, não amostra estatística** — elimina a pressuposição de amostragem probabilística que fundamenta kappa/alfa.
3. **Justificação de casos exemplares** — mais exigente que um coeficiente, porque é argumentável e vinculado a registros concretos.
4. **Resposta antecipada à objeção de Roele** — neutraliza a crítica de impressionismo antes que ela seja formulada.

**Veredito**: o dispositivo é comparável em rigor e mais adequado ao objeto.

### 1.3 Reconhecimento de limites
As nove lacunas sinalizadas no ensaio devem ser tratadas como **limitações declaradas**, não como falhas a esconder. Isso é o que transforma "falta de estatística" em "posição metodológica consciente".

**Recomendação**: no texto final da tese, cada lacuna deve ter parágrafo próprio em seção de "Limites e silêncios arquivísticos".

### 1.4 Consistência terminológica
O texto revisado deve manter:

- `iconometria` como framework guarda-chuva.
- `endurecimento` como eixo de fixidez (não "hardening", não "embrutecimento").
- `purificacao` como chave canônica.
- `purificacao_composto` como `deprecated` (não deletado).
- Vocabulário Warburg em alemão.

**Veredito**: consistente com codebook v2.2.1 e decisões anteriores.

### 1.5 Citabilidade em defesa
O texto tem densidade argumentativa suficiente para ser lido em voz alta. Recomenda-se:

- Ter parágrafo "Por que não kappa?" pronto para arguição.
- Ter exemplo concreto (ex.: FR-013, BR-009) ilustrando cada um dos 4 elementos.
- Antecipar a pergunta "mas como garantir que outro pesquisador chegaria ao mesmo resultado?" com a resposta sobre replicabilidade interpretativa.

---

## 2. Avaliação técnica

### 2.1 Compatibilidade com codebook v2.2.1 → v2.3.0
- `purificacao_composto` já está `deprecated` em schemas e scripts.
- A metodologia 2.0 não propõe remover campos legados, apenas declará-los obsoletos como valor probatório.
- **Risco**: baixo, desde que backward compatibility seja mantida.

### 2.2 Impacto nos schemas JSON
Campos afetados:

| Schema | Campo | Status atual | Impacto |
|--------|-------|--------------|---------|
| `master-record.schema.json` | `purificacao_composto` | `deprecated` | Apenas atualização de `description` |
| `master-record.schema.json` | `endurecimento_score` | ativo | Atualizar descrição para refletir que é eixo, não agregado |
| `purification-record.schema.json` | `indicadores` | ativo | Atualizar descrição para "inventário ordinal" |
| `purification-record.schema.json` | `purificacao_composto` | `deprecated` | Apenas atualização de `description` |

**Risco**: baixo. Nenhuma remoção de campo.

### 2.3 Impacto nos scripts
Scripts com drift terminológico identificado:

| Arquivo | Drift | Ação |
|---------|-------|------|
| `tools/scripts/code_purification.py` | Help text ainda fala em "score" | Atualizar para "inventário de atributos" |
| `tools/scripts/compute_irr.py` | Seção de composto já rotulada como legado | Clareza adicional |
| `tools/scripts/irr_rater2_batch.py` | Prompt ainda pede composto? | Atualizar |
| `tools/scripts/lpai_proxy_coder_k3.py` | Help text | Verificar |
| `tools/scripts/iconocode_gemma4.py` | Verificar se já saiu `endurecimento_score` e entrou `inventario_verbal` | Verificar |

**Risco**: médio. Drift terminológico pode causar inconsistência entre docs e CLI.

### 2.4 Rastreabilidade
O texto-fonte deve ser complementado com exemplos concretos do corpus. Cada afirmação metodológica deve ser ilustrada com pelo menos um registro real.

**Recomendação**: criar `docs/TRACEABILITY_MATRIX.md` mapeando `id` → `vault/candidatos/XX-NNN.md` → `records.jsonl` → `purification.jsonl` → `corpus-data.json`.

### 2.5 Validação automatizada
**Status atual**: bloqueada por inconsistência de ambiente Python.

- `python` → miniforge 3.13 (sem `jsonschema` funcional)
- `pip` → hermes-agent venv 3.11 (tem pacotes, mas interpreter errado)
- Resultado: `ModuleNotFoundError: No module named 'rpds.rpds'`

**Recomendação**: criar venv local no worktree antes de rodar `validate_schemas.py`, `code_purification.py --status`, `records_to_corpus.py --diff`.

**Risco técnico**: médio. Não bloqueia commits documentais, mas bloqueia commits técnicos.

---

## 3. Recomendação executiva

### 3.1 Aprovação
O texto-fonte está **aprovado nos dois crivos** (técnico e acadêmico), com as seguintes condições:

1. **Condição acadêmica**: incluir seção de "Limites e silêncios arquivísticos" com as 9 lacunas declaradas explicitamente.
2. **Condição técnica**: não remover `purificacao_composto` definitivamente; mantê-lo como `deprecated` até v3.0.
3. **Condição de rastreabilidade**: complementar o texto com pelo menos 3 exemplos concretos do corpus.

### 3.2 Sequência de commits recomendada

| Ordem | Arquivo | Tipo |
|-------|---------|------|
| 1 | `docs/decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md` | ADR canônico |
| 2 | `docs/METHODOLOGY_2_0.md` | Documento de referência |
| 3 | `docs/METHOD_CONTRACT_2026-07-31.md` | Contrato atualizado |
| 4 | `docs/TRACEABILITY_MATRIX.md` | Rastreabilidade pública |
| 5 | `docs/CODING_PROTOCOL.md` | Protocolo de codificação aberto |

### 3.3 Bloqueios remanescentes
- **Ambiente Python**: saneamento necessário antes de validação automatizada.
- **Drift documental**: README.md, CLAUDE.md, AGENTS.md, PLANO-TESE-ICONOCRACIA.md precisam de atualização em lote (Camada 2).
- **Drift técnico**: scripts com help text/prompts legados (Camada 3).

---

## 4. Conclusão

O abandono do aparato de confiabilidade métrica importado é **metodologicamente justificado, academicamente defensável e tecnicamente viável**. A virada para a `iconometria` como ecologia metodológica plural não diminui o rigor — desloca-o de uma lógica de replicabilidade mecânica para uma lógica de explicitação procedimental, rastreabilidade documental e exemplaridade argumentativa.

**Próximo passo**: criar os documentos canônicos e commitar na worktree limpa.
