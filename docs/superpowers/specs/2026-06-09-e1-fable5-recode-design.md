# E1 Re-run com Fable 5 — Design

**Status:** aprovado (brainstorm 2026-06-09, sessão Fable 5)
**Criado:** 2026-06-09
**Referências:** `docs/decisions/IRR-RE-RUN-DESIGN-2026-06-09.md` · `docs/decisions/DIALETICA-N165-vs-265.md`
**Branch de trabalho:** `worktree-e1-fable5-recode` (worktree isolado, base `origin/main`)

---

## 1. Problema

O E1 (extração pathosformel / 10 indicadores de purificação) está travado:

- `pathosformel_index.jsonl` tem **52/265 itens**, dos quais **29 com score
  zero** — artefato de summaries textuais fracos passados ao Gemma-4 via proxy
  Hermes (caído). O recode (`e1_recode_zeros.py`, PID 11926) morreu sem gravar.
- O pré-requisito do IRR re-run é E1 completo, e o IRR é o degrau para o E2
  (cluster por regime visual).
- A codificação por texto intermediário reproduz o problema de proveniência
  que motivou o DIALETICA-N (6 instrumentos misturados em `coded_by`).

## 2. Decisões (registradas no brainstorm)

| Decisão | Escolha | Alternativas rejeitadas |
|---|---|---|
| Prioridade | Destravar E1 | DIALETICA-N primeiro; Cap 1; fechar branch de imagens |
| Escopo | **265 itens** (E1 completo) | Só os 29 zeros; zeros + amostra IRR |
| Instrumento | **Fable 5 codifica os 265** do zero (rater-1 homogêneo) | Manter 23 válidos do Gemma (rater-1 híbrido); comparar antes |
| Sem imagem | **Flag `#no-image` + exclusão da população E1/IRR** | Fallback textual marcado; reaquisição prévia |
| Execução | **A — Triagem + lotes de ~25 com subagentes iconocode** | B — script API headless (custo de billing); C — fan-out único (frágil) |

## 3. Arquitetura

```
records.jsonl (265)
      │
      ▼
[1] e1_triage_images.py ──► e1_worklist.json  (codificáveis: fonte local|url)
      │                  └─► e1_excluded.json (#no-image, com motivo)
      ▼
[2] Lotes de ~25 — subagente iconocode por item (Fable 5 multimodal)
      │   imagem local → Read · imagem remota → fetch
      ▼
[3] e1_append_batch.py ──► pathosformel_index.jsonl (novo, fable-5)
      │   valida range 0-3 + enum regime; gravação atômica
      ▼
[4] commit por lote (resumível) ──► estatística-resumo final
```

### 3.1 Triagem — `tools/scripts/e1_triage_images.py`

- **Input:** `records.jsonl` (265) + fontes de imagem em cascata:
  1. Local: `binaries/Images-reacquired-2026-06-09/` e `gallery/**` do
     checkout principal (`/Users/ana/Research/hub/iconocracy-corpus/`) —
     parâmetro `--binaries-root`, leitura por caminho absoluto (worktree não
     contém os binários).
  2. Remota: URL de imagem direta na vault note (`vault/candidatos/`) ou em
     `corpus/corpus-data.json`; validada com requisição HEAD exigindo
     `Content-Type: image/*` (não-imagens HTML/PDF caem na exclusão — foi a
     contaminação do piloto IRR de 30/05).
  3. Nada → exclusão.
- **Output:**
  - `data/processed/e1_worklist.json` — por item: `item_id`, `image_source`
    (`local`|`url`), `path_or_url`, dimensões quando local, `regime` atual
    (se houver, para estratificação IRR futura), `status` (`pending`|`done`).
  - `data/processed/e1_excluded.json` — `item_id`, `reason`
    (`no_image_source`|`image_unreachable`|`not_an_image`), data.

### 3.2 Codificação — lotes de ~25 via subagente `iconocode`

- Um subagente por item, despachados em paralelo dentro do lote.
- Protocolo: Panofsky 3 níveis + **10 indicadores de purificação (0–3)** +
  regime (`fundacional`|`normativo`|`militar`|`contra-alegoria`), conforme
  agente `iconocode` existente.
- Saída por item (JSON): 10 indicadores, `regime`, `confidence`,
  `coded_by: "fable-5"`, `coded_at` (ISO), `coded_from: "image"`,
  `image_source` (`local`|`url`), flags opcionais (`low_res` para <100px).
- **Dry-run obrigatório:** lote piloto de 5 itens antes do volume, para
  calibrar prompt e validar o formato de saída.

### 3.3 Gravação — `tools/scripts/e1_append_batch.py`

- Valida: indicadores inteiros 0–3, regime no enum, `item_id` existente em
  `records.jsonl`, sem duplicata no index.
- Gravação atômica (temp file + rename). Hook `validate_schemas.py` roda no
  PostToolUse como segunda camada.
- O index Gemma atual (52 itens, untracked no checkout principal) é copiado
  para `data/processed/pathosformel_index_gemma4_archived_2026-06-09.jsonl`
  antes da primeira gravação — preservado para comparação inter-instrumento
  futura (insumo possível do DIALETICA-N).

### 3.4 Controle

- Branch `worktree-e1-fable5-recode`; **commit por lote** → resumível em
  qualquer ponto da fila de 8–9 lotes.
- Worklist marca `status: done` por item gravado; retomada lê apenas
  `pending`.

## 4. Tratamento de erros

| Falha | Ação |
|---|---|
| Fetch remoto falha | 1 retry; depois `image_unreachable` → `e1_excluded.json` |
| HEAD retorna não-imagem | `not_an_image` → exclusão imediata |
| Imagem <100px (ex.: BR-005 93×140) | Codifica com flag `low_res` (entra na população, sinalizada) |
| Subagente retorna JSON inválido | 1 redispatch; depois item volta a `pending` com nota |
| Indicador fora de 0–3 | `e1_append_batch.py` rejeita o item inteiro (não grava parcial) |

## 5. Critério de pronto

1. Todos os itens da worklist com `status: done`.
2. `e1_excluded.json` documenta cada exclusão com motivo (artefato citável no
   dataset card do Cap. 2).
3. Estatística-resumo: distribuição por indicador, % não-zero, contagem por
   regime — sanity check contra a tabela de estratos do IRR re-run
   (fundacional ~100 · normativo ~60 · militar ~20 · contra-alegoria ~8).
4. População final ≥ ~186 itens reais → IRR re-run pode sortear a amostra
   estratificada (seed `20260611`).

## 6. Fora de escopo

- O IRR re-run em si (design próprio, doc de 2026-06-09).
- Reaquisição de imagens para os excluídos (campanha separada, branch
  `data/reacquire-images-*`).
- Decisão N=145 vs N=223 do DIALETICA-N (ganha insumo novo deste E1, mas é
  decisão da Ana).
- Atualização de `records.jsonl`/`corpus-data.json` — o E1 grava apenas no
  `pathosformel_index.jsonl`.
