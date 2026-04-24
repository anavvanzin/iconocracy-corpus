---
tipo: sessao-de-revisao
data: 2026-04-21
fase: pre-qualificacao-nov-2027
status: concluida-analise-pendente-artefatos
tags:
  - ultraplan
  - peer-review
  - qualificacao
  - 4-originais
  - continuacao
---

# Sessão 2026-04-21 — Peer Review do Ultraplan de Reposicionamento de Originalidade

## Contexto

Sessão solicitada para "deal with" o arquivo `~/Research/2026-04-17_ultraplan-qualificacao.md`. Após leitura, constatou-se que os 7 itens do ultraplan já estavam executados e commitados no repo (`4c10355`). O usuário então pediu uma análise de como melhorar ainda mais a arquitetura de 4 conceitos originais.

Foi executada uma **revisão full mode** (três revisores diferenciados + síntese editorial) conforme skill `academic-paper-reviewer`.

---

## Status dos 7 itens do ultraplan

| # | Item | Status | Commit |
|---|------|--------|--------|
| 1 | Criar ultraplan | ✅ Concluído pelo usuário | — |
| 2 | Atualizar CLAUDE.md (Mandatory Terminology) | ✅ Já presente | `4c10355` |
| 3 | Atualizar memo predecessor (4 originais) | ✅ Já presente | `4c10355` |
| 4 | Atualizar plano-capitulos (STEP 1 → 4) | ✅ Já presente | `4c10355` |
| 5 | Inserção A: Cap. 2 §2.2 (Carson + Legendre) | ✅ Já presente | `4c10355` |
| 6 | Inserção B: Cap. 5 §5.2 (Purificação Clássica) | ✅ Já presente | `4c10355` |
| 7 | Inserção C: Cross-link (Cap. 2 intro + Cap. 5 §5.2.5) | ✅ Já presente | `4c10355` |

---

## Resultado da Peer Review

### Revisores configurados

- **R1** — História do Direito Penal / Iconografia Jurídica (Ferrari, Grossi, Luminati, Martins)
- **R2** — Teoria Feminista / Teoria Decolonial / Teoria Política (Pateman, Mills, Davis, Lugones)
- **R3** — Estudos Visuais / Corpus Studies / História da Arte (Warburg, Bredekamp, Didi-Huberman, Drucker)

### Scores e vereditos

| Revisor | Score Ponderado | Recomendação |
|---------|-----------------|--------------|
| R1 | 70.4 | Minor Revision |
| R2 | 70.9 | Minor Revision |
| R3 | 67.8 | Minor Revision |

**Aggregate: 69.7 → Minor Revision com condição de escalonamento**

> Se os itens REQUIRED não forem atendidos, eleva-se para **Major Revision** na re-avaliação.

---

## Roadmap de revisão (copiado da síntese editorial)

### REQUIRED — bloqueiam defesa se ausentes

1. **Âncora em história do direito penal** (R1-C1)
   - A arquitetura precisa de um 5º eixo ou reformulação que articule iconografia com história da punição/processamento penal/normativa criminal brasileira.
   - Sugestões: conceito auxiliar "Pathosformel Penal"; ou reformular intro do Cap. 1 com Ferrari/Nunes/Santos.

2. **Protocolo de validação inter-observador** (R3-C1)
   - O documento precisa incluir subseção metodológica descrevendo: (a) n de codificadores, (b) subamostra, (c) coeficiente de concordância, (d) threshold (Kappa ≥ 0.70).
   - Sem isso, "operacionalizada empiricamente" é metodologicamente insustentável.

3. **Decisão sobre corpus racializado ou reformulação do conceito #3** (R2-C1)
   - Contrato Racial Visual precisa de: (a) subamostra com etiquetagem racial (mín. 20-30 peças), ou (b) rebaixamento a "proposição derivada".
   - A indecisão não é aceitável no documento de planejamento.

### STRONGLY RECOMMENDED — serão levantados na re-revisão

4. **Problematização do essentialismo de gênero** (R2-C2)
   - Adicionar nota metodológica declarando consciência da circularidade teórica (uso de "hystéra" como categoria analítica).

5. **Matriz de implicações entre os 4 conceitos** (R2-C3)
   - Tabela/figura mostrando relações de condição de possibilidade: economia política → efeito subjetivo → distribuição diferencial → mecanismo formal.

6. **Ponte Warburg ↔ indicadores** (R3-C3)
   - Explicitar como cada indicador captura (ou não) a dimensão gestual/pathosformel. Se não captura, declarar como limitação do instrumento.

7. **Elevação da nota de rodapé a seção epistemológica** (R3-C4)
   - Justificativa de exclusão de Lugones/Curiel e ciberfeminismo pós-2000 deve ocupar §1.3 ou §5.1, não apenas nota de rodapé.

### SUGGESTED — melhorias de qualidade

8. Incluir Bredekamp (*Bildakt*, 2010) e Drucker (*Graphesis*, 2014) na bibliografia de corpus visual.
9. Adicionar conceito auxiliar de escopo: "Binário Alegórico" — nota sobre restrição a figuras femininas binárias.
10. Subseção de "sensibilidade ao contexto nacional" no Cap. 5 (comportamento dos 10 indicadores em Brasil vs. França vs. Alemanha).

---

## Artefatos pendentes para produção na continuação

O assistente ofereceu, ao final da sessão, produzir os seguintes artefatos:

- [ ] **Draft do protocolo de validação inter-observador** (REQUIRED #2)
- [ ] **Matriz de implicações visual** (STRONGLY RECOMMENDED #5)
- [ ] **Reformulação do Cap. 1 intro com âncora em história do direito penal** (REQUIRED #1)
- [ ] **Nota metodológica sobre essentialismo de gênero** (STRONGLY RECOMMENDED #4)
- [ ] **Revisão do ultraplan propriamente dito** incorporando todos os pontos da peer review

---

## Arquivos referenciados nesta sessão

- `~/Research/2026-04-17_ultraplan-qualificacao.md` (fonte da análise — fora do repo)
- `~/Research/hub/iconocracy-corpus/CLAUDE.md`
- `~/Research/hub/iconocracy-corpus/vault/tese/ideias/2026-04-17_reposicionamento-originalidade-qualificacao.md`
- `~/Research/hub/iconocracy-corpus/vault/tese/plano-capitulos-2026-04-11.md`
- `~/Research/hub/iconocracy-corpus/vault/tese/capitulo-2.md`
- `~/Research/hub/iconocracy-corpus/vault/tese/capitulo-5.md`

---

## Próximo passo sugerido

Retomar esta sessão escolhendo um dos artefatos pendentes acima. A prioridade editorial é REQUIRED #2 (validação inter-observador), pois é a lacuna metodológica mais grave identificada por R3.
