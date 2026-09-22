# Revisão completa — regeneração do corpus-data-enriched.json

**Data**: 2026-09-22
**Escopo**: `corpus/corpus-data-enriched.json` (regenerado), `tools/scripts/regenerate_enriched.py`, `corpus/enrichment-report.md`, merge dos 91 itens legados, órfãos.
**Método**: três auditorias independentes (dados, código, diff legado) sobre os arquivos atuais; todas read-only.

---

## 0. Resumo executivo

A regeneração é **fiel ao ledger**: zero perdas ou corrupções nos campos autoritativos, overlays legados preservados byte a byte, ordenação correta. Os riscos reais estão **a montante do arquivo** (cópia do site desatualizada, URLs de imagem quebradas, citações fora de ABNT, inconsistências de score no próprio ledger) e na **documentação** (o relatório atual descreve errado a própria execução). Há um bug estrutural no script (fonte de overlay) que já produziu efeito colateral no relatório vigente.

**Fato novo desde 17/09**: o ledger tem agora **336 itens** (o 336º é `324a90b6-…`, "La Nation, la Loi, le Roi… 1791", `coded_by: ana`, 2026-09-15) e o script foi re-executado em 19/09. O backup `bak.2026-09-19` capturou a saída de 335 itens (não o estado pré-regeneração), e o `enrichment-report.md` atual é artefato dessa segunda execução.

---

## 1. Críticos (resolver antes de qualquer consumo público)

### C1 — O site público não consome este arquivo
`imagens/site/data/corpus-data-enriched.json` segue com **95 itens** (mtime 2026-08-29). Todo o restante desta revisão afeta apenas a cópia do repo até que a sincronização seja feita.

### C2 — O relatório vigente está errado (artefato de dupla execução)
`corpus/enrichment-report.md` reporta `regime_incerto: 1` (o arquivo carrega **193** tags), "mudanças de regime legadas: **0**" (real: **51**), seção de órfãos **vazia** (existem 4) e "335 overlays legados" (somente 91 são legados de verdade). **Os dados estão corretos; o relatório não pode ser citado.** Causa raiz: bug de fonte de overlay no script (ver §3, E1).

### C3 — 18 itens com URLs internas/placeholder
`iconocracy.corpus/vault/…` ×8, `iconocracy.corpus/placeholder/…` ×6 (SCOUT-337 aponta para `placeholder/FR-040` — id divergente), `iconocracy-corpus.local/piloto/` ×3. Serão links mortos no site público.

### C4 — Todos os 78 `local_image_path` estão quebrados em disco
Apontam para `corpus/imagens/<CC>/<id>`, que não existe nesta máquina (78/78 ausentes). O relatório afirma "null para todos" — falso: são overlays legados carregados.

---

## 2. Problemas de dados (maior → menor)

| # | Severidade | Achado | Números |
|---|---|---|---|
| D1 | **Alto** | **Órfãos não foram excluídos — foram re-keyed.** FR-007, US-011, US-012, DE-NOTG-1921 existem no ledger sob novos ids (2b7a1a18…, 39ebfe77…, 473ac4d7…, DE-020) **sem os overlays** (creator, instituição, thumbnail, IIIF, rights, citação — todos null). US-012 ainda tem **duplicata interna**: `US-017` é o mesmo objeto (mesma URL LoC 95506508) | 4 itens + 1 duplicata |
| D2 | **Alto** | Justificativa tautológica: 203/336 itens (60%) têm `regime_justificativa` = "classificado no ledger por X em Y → REGIME" — nota de proveniência, não justificativa iconográfica. Apenas 40/91 legados mantiveram a justificativa substantiva | 203 itens |
| D3 | **Alto** | `endurecimento_score` ≠ média dos indicadores em **17 itens** (além dos 161 > 1.0 já documentados). Pior caso: **BE-004 score 0.0 com soma de indicadores 19 (média 1.9)** — o item foi re-codificado sem recomputar o score. O 336º item (`324a90b6…`) **não tem score** | 17 + 1 |
| D4 | Médio | `medium_norm` com vocabulário dividido: 84 legados fora da taxonomia canônica (`Gravura/Estampe` 26, `Outro` 20, `Gravura` 16…); 5 legados com `medium` mapeável mas `medium_norm: null` | 84 + 5 |
| D5 | Médio | `period` é uma sopa de ~50 rótulos (IIIe République / Third Republic / hífens divergentes; Império / Empire; República Velha / Early Republic / Old Republic). `period_norm` é null em todos os 245 itens novos | ~50 variantes |
| D6 | Médio | `year: null` em **41 itens** (não 22): 19 têm datas não parseáveis ("17th century", "século XIX", "c. séc. XIII"…). DE-002 tem `year: 1239` (abaixo do piso de sanidade; já marcado fora-do-escopo) | 41 |
| D7 | Médio | `citation_abnt` não é ABNT na maioria: **179/336** são o título verbatim; 128 não contêm ano de 4 dígitos (AGENTS.md exige NBR 6023:2025) | 179 |
| D8 | Médio | 27 itens `fora-do-escopo` permanecem no conjunto publicado — decisão explícita pendente | 27 |
| D9 | Baixo | `vault_note` perdido em 5 itens (SCOUT-114/115/116/118/119, o campo existia no enriched antigo e não foi carregado) | 5 |
| D10 | Baixo | `year` virou null em ~11 legados com data por século ("18th century" tinha ponto médio estimado no antigo, ex. EU-009 1850) | 11 |
| D11 | Baixo | Tag `regime_incerto` ausente em BR-001 e BR-004 apesar do flip de regime (cobertura 49/51) | 2 |
| D12 | Baixo | Rótulos de período em anos-limite: Brasil 1822 → "Colonial" (ano da independência); 13 itens BR de 1889 → "Império" (República proclamada em nov/1889); França 1789 dividida entre "Ancien Régime" (novos) e "French Revolution" (legados) | ~15 |
| D13 | Nit | Motif/tags: 394 tokens, 16 pares duplicados por caixa/acento; **19 itens com o token `descricao_pre_iconografica`** (nome de campo do pipeline vazando para motif → tags → site) | 19 |
| D14 | Nit | `audit_flags` é gaveta de bagunça (294/336): valores truncados, 18 `#verificar`, 8 flags `sem-url` obsoletas (os itens já têm URL) | 294 |
| D15 | Nit | 136 itens com title == description; prefixo de id ≠ país em 4 itens (DE-001→Suíça, DE-002/006/007→Itália); `country` não normalizado (`CL`, variantes com parênteses) | — |

---

## 3. Revisão do script `tools/scripts/regenerate_enriched.py`

### E1 — MAJOR: execuções em dias diferentes redefinem "legado" silenciosamente
A fonte de overlay é "backup de hoje, senão backup novo do arquivo atual". No dia seguinte, o overlay vira a **própria saída do script** (336 itens) → todo item passa a ser "legado": filas de revisão zeram no relatório (`regime_incerto: 0`, órfãos vazios, mudanças de regime: 0) **sem nenhuma mudança nos dados**. É exatamente o artefato que está no repo hoje.
**Correção**: fixar a fonte de overlay — o backup mais antigo (`sorted(glob)[0]`) ou um `corpus-data-enriched.legacy.json` commitado.

### E2 — MAJOR: precedência do ledger quebra para itens novos em execuções posteriores
Mesma raiz: um item novo presente no backup passa a ser tratado como legado e seus `medium`, `period`, `tags`, `regime_justificativa` deixam de ser re-derivados do ledger. Demonstrado: alterar `support` no ledger não propaga para `medium` na saída.

### E3 — MAJOR: números hardcoded no relatório
"22 itens sem date", "4 órfãos", "244 itens novos", "local_image_path é null para todos" (já falso: 78/336 preenchidos). Computar todos a partir dos dados.

### E4–E8 — MINOR
- `country: None` no ledger → `KeyError` (ordenação antes da validação estrutural).
- Falhas (backup corrompido, enriched ausente) crasham com traceback cru; nenhuma escreve saída parcial (seguro, mas opaco).
- `--dry-run` ainda grava o backup (mensagem "no files written" incorreta).
- O classificador não conhece CONTRA-ALEGORIA → os 15 itens desse regime são sempre marcados `regime_incerto` (ruído estrutural).
- `regime` vazio no ledger degrada silenciosamente para `""`.

### Sólido (verificado)
- Classificador é **import**, não cópia — sem drift; sem efeitos colaterais de rede.
- Idempotência no mesmo dia confirmada (JSON byte-idêntico).
- Ledger vence em todos os campos autoritativos; ids duplicados abortam antes de escrever; UTF-8 consistente.

---

## 4. O que está verificado como correto

- Fidelidade exaustiva (336/336): title, country, date, description, motif, url, citation_abnt, regime, score, indicadores, proveniência — **0 divergências** vs ledger.
- Derivações: year, country_pt, motif_str/tags_str, iconographic_metadata — **0 erros**.
- 9 campos overlay preservados byte a byte nos 91 legados; 51/51 flips de regime == ledger; 0 justificativas stale (todas as preservadas citam o regime correto).
- Campos obrigatórios do schema presentes e não vazios em 336/336 (date = "" exatamente nos 22 documentados).
- Indicadores: 10 chaves canônicas, 3.360 valores numéricos em 0–3.
- Distribuições (regime 164/103/54/15; países; histograma por década com pico 1880–1910) plausíveis e consistentes com o relatório.
- Testes do repo: 21 passed (export idempotente, consistência cross-file, crosswalk de ids).

---

## 5. Plano de ação recomendado (ordem)

1. **Corrigir o script** (E1–E3): fonte de overlay fixa + números computados. ~1h.
2. **Re-executar a partir do overlay pristino** (`bak.2026-09-17`) para restaurar o relatório verdadeiro: 181–193 divergências de regime, 51 flips, 4 órfãos.
3. **Merge dos órfãos** (D1): transferir overlays de FR-007/US-011/US-012/DE-NOTG-1921 para as contrapartes re-keyed; restaurar ids legados se possível; resolver duplicata US-017.
4. **Recomputar scores** dos 17 inconsistentes + preencher o do 336º item; decidir normalização ÷3 vs schema máx 3.
5. **Decidir antes de publicar**: 18 URLs placeholder, 78 local_image_path quebrados, 27 fora-do-escopo.
6. **Só então sincronizar** `imagens/site/data/corpus-data-enriched.json`.
7. Backlog de qualidade: citações ABNT (179), period_norm, medium_norm legado, year null (41), motif `descricao_pre_iconografica` (19), vault_note (5).

---

*Gerado a partir de três auditorias independentes (dados, código, diff legado). Números computados diretamente dos arquivos em 2026-09-22.*
