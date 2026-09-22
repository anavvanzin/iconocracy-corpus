---
titulo: "Plano Semanal — Transição Atlas-Based + T4 Closure"
data: 2026-04-22
semana: 17–23 abril 2026
status: ativo
prioridade: alta
---

# Plano Semanal: T4 Encerramento + Transição Atlas-Based

## Contexto

T4 adjudicação concluída em 2026-04-22 via método Council & Santa. Estado atual do corpus:

| Métrica | Valor |
|---|---|
| records.jsonl | 165 itens (100% válidos) |
| corpus-data.json | 165 itens |
| orphans/divergentes | 0 |
| uncoded (sem indicadores) | 19 |
| nulled (purificação removida) | 11 |
| com refs atlas | 14 |

**T4 resultado:** 4 registros enriquecidos (BR-009, FR-008, FR-009, FR-038); 2 aprovados para promoção como novos (BR-SCOUT-001, BR-SCOUT-003).

---

## Objetivo central da semana

Executar a **transição de framing score-based → atlas-based** na arquitetura da tese. Isso não significa abandonar os indicadores de endurecimento — eles permanecem como ferramenta operacional de composição dos painéis — mas reposicioná-los: de *produto* (resultados estatísticos em caps. 6–7) para *instrumento* (critério de seleção e ordenação das imagens nos oito painéis do Atlas).

---

## Dia a dia

### Terça 22/04 — T4 Closure + Promoção

- [x] Adjudicação Council & Santa (6 PARTIALs resolvidos)
- [ ] Promover 2 novos registros (BR-SCOUT-001, BR-SCOUT-003) para records.jsonl
- [ ] Rodar `records_to_corpus.py --diff` → aplicar
- [ ] Validar schemas + reconciliação
- [ ] Fazer commit do pacote T4
- [ ] Revisar draft vault notes dos 15 LPAI e copiar os 2 novos + os 8 NEW restantes para `vault/candidatos/`

### Quarta 23/04 — Atlas Reframing I: Manuscrito

- [ ] Reescrever §I.7 (Mapa de Leitura) em `introducao.md`:
  - Parte III = "preparação do corpus e instrumentos de composição do Atlas"
  - Cap. 6–7 = "análise para montagem dos painéis", não "resultados estatísticos"
  - Parte IV = "síntese visual-argumentativa; os painéis como demonstração, não ilustração"
- [ ] Atualizar `capitulo-5.md` §5.2: indicadores como "protocolo de seleção e ordenação atlas", não como "escala de mensuração quantitativa"
- [ ] Inserir nota de método em `capitulo-8.md` (ainda esqueleto): princípios warburguianos de montagem (Nachleben, Pathosformel, Zwischenraum)

### Quinta 24/04 — Atlas Reframing II: Corpus + Coding

- [ ] Executar IconoCode nos 2 novos itens promovidos
- [ ] Rodar `code_purification.py --status` → mapear backlog real
- [ ] Priorizar coding dos 19 uncoded por relevância para painéis do Atlas:
  - Painel I (Gênese): itens fundacionais BR/FR sem código
  - Painel VI (Normativo máximo): bustos Marianne faltantes
  - Painel VII (Contra-alegoria): satiras e críticas
- [ ] Atualizar campos `atlas_panel` nos registros já codificados (14 têm; completar os demais)

### Sexta 25/04 — Caso Brasileiro + ARGOS

- [ ] Continuar 2-week Brazilian case action plan (commit 110e365)
- [ ] Resolver image acquisition para BR-SCOUT-001 (Wikimedia Commons) e BR-SCOUT-003 (Google Arts) via ARGOS ou download direto
- [ ] Verificar se `download_corpus_images.py` cobre os novos URLs; se não, adicionar handlers
- [ ] Atualizar `drive-manifest.json` se imagens forem armazenadas no Google Drive

### Sáb 26/04 — Síntese + Compilação

- [ ] Compilar tese (`make -C vault/tese/ docx`) e verificar se reframing quebrou cross-references
- [ ] Revisar `corpus/DASHBOARD_CORPUS.html` — está modificado no working tree; verificar se precisa de rebuild
- [ ] Escrever nota de sessão em `vault/sessoes/SCOUT-SESSION-2026-04-W3.md`

### Dom 27/04 — Revisão + Planejamento W4

- [ ] Revisar todo o diff da semana
- [ ] Rodar suite completa: validate → reconcile → vault_sync status → code_purification --status
- [ ] Preparar plano da semana 4 (abril)

---

## Decisões-chave do Council & Santa (T4)

| Candidato | Existente | Decisão | Método | Racional |
|---|---|---|---|---|
| BR-SCOUT-001 | BR-005 | **NEW** | Santa | title_substring noise; objetos distintos (Agostini vs Villares) |
| BR-SCOUT-003 | BR-005 | **NEW** | Santa | title_substring noise; objetos distintos (Lopes Rodrigues vs Villares) |
| BR-SCOUT-005 | BR-009 | **ENRICH** | Council | mesmo objeto (Ceschiatti); título LPAI omite atribuição |
| FR-SCOUT-002 | FR-008 | **ENRICH** | Council | mesmo objeto, estado diferente (état avec remarque); atlas não precisa de painel separado |
| FR-SCOUT-005 | FR-009 | **ENRICH** | Council | mesma família de objetos; série fotográfica enriquece o busto |
| FR-SCOUT-006 | FR-038 | **ENRICH** | Santa | mesmo objeto; LPAI fornece URL Gallica e atribuição Janinet |

Artefatos:
- Log: `data/staging/t4-adjudication-log.json`
- Report atualizado: `docs/T4-LPAI-INGEST-REPORT.md`

---

## Riscos e bloqueios

1. **Image acquisition**: BR-SCOUT-003 usa Google Arts & Culture (artsandculture.google.com) — pode exigir Playwright ou fallback manual. Mitigação: priorizar download de thumbnail via API pública; se bloqueado, marcar como `manual_required` e seguir.

2. **Corpus size**: após promoção dos 2 novos, corpus vai para 167 itens. Verificar se `corpus-data.json` aceita append sem quebra de ordenação. Mitigação: `records_to_corpus.py` já usa atomic write + UUID5 matching.

3. **Atlas refs incompletas**: apenas 14 de 165 itens têm referências atlas. Transição atlas-based exige que a maioria dos itens-coded receba designação de painel. Mitigação: priorizar os 46 normativos + 31 militares (mais definidos) antes dos 78 fundacionais.

4. **Tempo de coding**: 19 uncoded + 2 novos = 21 itens na fila T3. A ~15 min/item (IconoCode batch), são ~5h de trabalho. Mitigação: usar `iconocode-batch` skill com subagents paralelos.

---

## Critérios de sucesso da semana

- [ ] `records.jsonl` e `corpus-data.json` sincronizados com 167 itens
- [ ] `introducao.md` refletindo arquitetura atlas-based
- [ ] ≥5 itens novos codificados (reduzir uncoded de 19 para ≤14)
- [ ] ≥10 itens com campo `atlas_panel` preenchido
- [ ] Imagens adquiridas para BR-SCOUT-001 e BR-SCOUT-003
- [ ] Commit limpo no branch principal
