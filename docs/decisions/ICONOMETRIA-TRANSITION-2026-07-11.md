# Decisão — Transição conceitual: *endurecimento* → *iconometria*

- **Data:** 2026-07-11
- **Autora:** Ana Vanzin
- **Status:** Aceita (camada conceitual). Migração de dados/scripts/manuscrito **faseada e pendente de aprovação** (ver §5).
- **Registros relacionados:** `docs/decisions/DIALETICA-N165-vs-265.md`, `docs/decisions/DESENHO-2-0-ICONOCRACIA-2026-06-23.md`
- **Conceito-fonte:** [`concepts/iconometria.md`](../../concepts/iconometria.md)

---

## 1. Contexto

Até aqui, **endurecimento** era o eixo empírico central da metodologia: a *operacionalização da Purificação Clássica* por meio de **10 indicadores ordinais (0–3)**, com o objetivo de **quantificar a fixidez** de uma alegoria feminina (o grau em que a figura histórica é extraída e imobilizada no eterno alegórico). O escore agregado vivia no campo `endurecimento_score` (canônico em `data/processed/records.jsonl` → `corpus/corpus-data.json`), com o *ledger* de codificação em `data/processed/purification.jsonl`.

## 2. Decisão

Promover **iconometria** a **framework metodológico guarda-chuva** da tese: a **medição e análise de padrões iconográficos** no corpus — abordagem mais ampla e matizada que a mera quantificação de fixidez.

**Endurecimento não é abandonado nem renomeado 1:1.** Ele é **preservado como *um* eixo dentro da iconometria** — o **subíndice de fixidez/purificação** (os 10 indicadores). A iconometria comporta esse eixo e abre espaço para outros vetores mensuráveis (p.ex. seriação, vetor colonial, densidade narrativa) sob um mesmo aparato quantitativo.

> Em uma frase: **iconometria ⊇ endurecimento.** A iconometria é o *método de medição*; o endurecimento é *o que se mede* no eixo da fixidez alegórica.

## 3. Justificativa

- Alarga o escopo de "quantificar a fixidez de uma alegoria" para "medir e analisar padrões iconográficos", posicionando o aparato quantitativo como método geral (não como um único escore).
- Alinha-se ao nó conceitual `concepts/iconometria.md`, que já definia iconometria como *"quantitative approach to the analysis of images, focusing on measurable aspects and patterns"* — anterior a esta decisão, agora formalizado.
- Não sacrifica a genealogia jurídica: o endurecimento permanece a *operacionalização empírica da Purificação Clássica* (conceito autoral #4), agora explicitamente como **um eixo** do método iconométrico.

## 4. Escopo executado nesta passada (camada conceitual — reversível)

Arquivos alterados **apenas na definição/documentação**:

1. `docs/decisions/ICONOMETRIA-TRANSITION-2026-07-11.md` (este registro)
2. `concepts/iconometria.md` — definição canônica expandida (iconometria = guarda-chuva; endurecimento = eixo de fixidez)
3. `CLAUDE.md` — entrada de terminologia + nota de arquitetura
4. `AGENTS.md` — terminologia canônica + rótulo de codificação

> O stub `atlas/stubs/conceito/iconometria.md` é **gerado** por `atlas/_generate_stubs.py` a partir de `concepts/iconometria.md`; será atualizado ao rodar o gerador (não editado à mão).

## 5. **NÃO** alterado nesta passada (pendente de aprovação de Ana)

Nada de dado canônico, schema, script ou prosa de manuscrito foi tocado. Preservados intencionalmente:

- **Campo de dados `endurecimento_score`** — mantido como **chave estável** em `records.jsonl`, `purification.jsonl`, `corpus-data.json`, CSV e schemas. Renomear a chave é migração coordenada (schema + dados + 21 scripts + notebooks + CI) e exige decisão explícita.
- **Manuscrito** (`vault/tese/**`, `tese/manuscrito/**`) — prosa é a voz autoral; troca de termo só como sugestão, perto da defesa.
- **Snapshots congelados** — `Other/`, `data/training/*.jsonl` (SFT/eval): são registros históricos de *runs*; não se reescreve histórico.

## 6. Plano de migração faseado (para aprovação)

| Fase | Superfície | Ação | Risco | Reversão |
|------|-----------|------|-------|----------|
| **F0** ✅ | Conceito + docs | Esta passada | Baixo | git revert |
| **F1** | Manuscrito | Introduzir "iconometria" como método; endurecimento como eixo. **Como sugestão**, preservando voz. | Médio | diff por capítulo |
| **F2** | Notebooks 01–08 | Rótulos de exibição/prosa markdown → "iconometria (eixo endurecimento)"; **sem** renomear variáveis/colunas. | Médio | re-run |
| **F3** | Campo de dados | *Opcional.* Se decidir renomear `endurecimento_score` → manter alias/retrocompat; migrar schema + dados + scripts + CI juntos, com `validate_schemas.py` + `records_to_corpus.py --diff` verdes. | Alto | branch dedicada |

**Recomendação:** manter `endurecimento_score` como chave (estabilidade de dados/CI) e mudar apenas rótulos de exibição e prosa. F3 (renome de campo) só se houver ganho claro que justifique a migração coordenada.

## 7. Critérios de verificação (antes de qualquer merge que toque dados)

```bash
conda activate iconocracy
python tools/scripts/validate_schemas.py
python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record
python tools/scripts/records_to_corpus.py --diff   # deve reportar sincronizado
```
