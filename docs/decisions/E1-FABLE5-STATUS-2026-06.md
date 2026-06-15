# E1 Re-run com Fable 5 — Status Final

**Data:** 2026-06-13
**Branch:** `worktree-e1-fable5-recode`
**Spec:** `docs/superpowers/specs/2026-06-09-e1-fable5-recode-design.md`
**Plano:** `docs/superpowers/plans/2026-06-09-e1-fable5-recode.md`
**Instrumento:** Fable 5 multimodal, único rater-1 (`coded_by: "fable-5"`)

---

## 0. Atualização Stage A (2026-06-15) — reaquisição dos 7 motivos-núcleo

Reaquiri imagens corretas (firecrawl scrape/search → download → **verificação visual item a item**) e recodifiquei via o mesmo Workflow iconocode. **6 de 7 recuperados:**

| Sigla | Fonte nova | Regime |
|---|---|---|
| DE-013 Germania (Kaulbach) | DHM (imagem real, não o logo LeMO) | militar |
| UK-FLORIN-1902 Britannia | Museum Victoria, **verso** correto | militar |
| BR-006 Alegoria da República | Wikimedia Commons (MHN) | fundacional |
| UY-001 El Altar de la Patria | Wikimedia Commons | fundacional |
| UK-010 Two Forces (Britannia/Hibernia) | Wikimedia Commons (Punch 1881) | militar |
| DE-008 Justitia (Hameln) | mittelweser-tourismus (close-up real) | normativo |

Imagens em `binaries/Images-reacquired-2026-06-15/` (checkout principal).
**BE-002 (Palais de Justice)** NÃO recuperado: é arquitetura forense; só há foto do prédio, não uma figura feminina única → DECISÃO PENDENTE (excluir como arquitetura-sem-figura, ou escolher uma estátua de Justice específica). Permanece `excluded_bad_image`.

**Índice agora: 49 linhas · N analítico = 44** (era 38) + 5 fora_escopo.
Regimes (N=44): normativo 21 · fundacional 13 · **militar 8** (era 5) · contra-alegoria 2.

---

## 1. Funil (308 → 43 codificados) — histórico pré-Stage A

| Etapa | N | Observação |
|---|---|---|
| População (`records.jsonl`) | 308 | ledger canônico (origin/main, pós +43 candidatos de 08/06) |
| Triagem com imagem resolvível | 50 | 50 locais em `binaries/Images-reacquired-2026-06-09/`; 0 via vault-thumb |
| Sem imagem (`no_image_source`) | 258 | URLs são páginas de catálogo/PDF — campanha de reaquisição separada |
| **Codificados (índice)** | **43** | dry-run 5 + produção 38 |
| Imagem ruim → reaquisição | 7 | imagens reaquiridas em 09/06 vieram erradas/corrompidas (ver §4) |

`50 codificáveis = 43 codificados + 7 imagem-ruim`. `308 = 50 + 258`.

## 2. Índice Fable 5 — composição

- **43 linhas**, todas `coded_by: "fable-5"`, `coded_from: "image"`.
- **N analítico (em escopo): 38.**
- **fora_escopo: 5** — não-alegorias femininas, mantidas com flag + `motivo_exclusao`,
  indicadores/regime/composto nulos (Estratégia B):
  - `BE-5F-LEOPOLD-1832` (efígie de Léopold I), `PT-001` (figura masculina
    revolucionária) — do dry-run.
  - `US-020` (charge política de Keppler, capitalistas masculinos), `PT-003`
    (vanitas, leito de morte), `PT-004` (alegoria do Tempo/Morte) — produção.

### Regimes (N=38 em escopo)
| Regime | N |
|---|---|
| normativo | 20 |
| fundacional | 11 |
| militar | 5 |
| contra-alegoria | 2 |

### Indicadores (em escopo, % não-zero)
`purificacao_composto`: min 0.3 · máx 2.6 · média 1.66. **all-zero = 0** — o
colapso em zero do Gemma-4 (29/52) **não reapareceu**: codificar da imagem (não de
summary textual) resolveu a causa-raiz.

| Indicador | %≠0 |
|---|---|
| dessexualizacao | 95 |
| uniformizacao_facial | 95 |
| heraldizacao | 95 |
| rigidez_postural | 89 |
| apagamento_narrativo | 89 |
| monocromatizacao | 87 |
| desincorporacao | 84 |
| inscricao_estatal | 76 |
| serialidade | 68 |
| enquadramento_arquitetonico | 66 |

## 3. Validação metodológica

- **Auto-correção de item_id:** o agente alucinou o UUID de `PT-001` (e o append
  o corrigiu via `sigla_id`, casando com a worklist — fonte da verdade da
  identidade). Mecanismo testado e ativo para toda a produção.
- **Recusa correta de codificar imagem ruim:** o pipeline sinalizou `fora_escopo`
  em vez de fabricar scores para imagens não-analisáveis (ver §4). Verificado
  manualmente em 3 casos (DE-013 logo "LeMO", BR-006 placeholder abstrato,
  UK-FLORIN anverso do rei) — diagnósticos do agente confirmados.

## 4. Reaquisição necessária (7 itens, motivos-núcleo)

Imagens reaquiridas em 09/06 vieram **erradas/corrompidas** — itens IN SCOPE
roteados para `e1_excluded.json` (`reason: bad_image_reacquire`) e marcados
`excluded_bad_image` na worklist (NÃO codificados como fora de escopo):

| Sigla | Motivo da imagem ruim |
|---|---|
| `DE-013` (Germania) | arquivo é logo "LeMO", não a obra |
| `BR-006` (Alegoria da República) | placeholder/asset abstrato corrompido |
| `UK-FLORIN-1902` (Britannia) | anverso (efígie do rei); Britannia no verso, ausente |
| `UK-010` (Britannia/Hibernia) | capa do livro "Cartoons by Tenniel" |
| `UY-001` (Altar de la Patria) | foto de figura masculina |
| `BE-002` (Palais de Justice) | retrato do arquiteto Poelaert |
| `DE-008` (Justitia, Hameln) | fachada; relevo da Justitia minúsculo/indiscernível |

**QA:** a campanha de reaquisição de 09/06 (fallback og:image → twitter:image →
img-tag) capturou logos/capas/lados errados nesses 7 — alvo para uma próxima
rodada com verificação visual.

## 5. Readiness do IRR re-run

O `IRR-RE-RUN-DESIGN-2026-06-09.md` assumia população ~186 com estratos
fundacional ~100 / normativo ~60 / militar ~20 / contra ~8 → amostra 25-30.
**Realidade após E1:** N=38, estratos normativo 20 / fundacional 11 / militar 5 /
contra-alegoria 2.

Consequências:
- O desenho amostral do IRR precisa ser **revisto para baixo**: contra-alegoria
  (2) e militar (5) são finos demais para amostragem estratificada — provável
  censo desses estratos.
- O IRR exige **rater-2** recodificando uma amostra dos 38 (este E1 é só rater-1).
- Reaquirir os 7 (§4) + codificar mais dos 258 (reaquisição) aumentaria N e
  reabriria a amostragem estratificada original.

## 6. Decisões pendentes (Ana)

1. **Reaquisição dos 7** motivos-núcleo (Germania, Britannia×2, República,
   Justitia, etc.) — campanha curta de imagem antes de fechar o N do E1?
2. **Aceitar N=38 como rater-1** e desenhar o IRR re-run sobre ele (com estratos
   revistos), ou expandir antes via reaquisição dos 258?
3. **`corpus/corpus-data.json`**: há uma modificação enorme e alheia ao E1
   (7552/8747 linhas, reembaralhamento — provável regeneração de outra sessão)
   parada no working tree do worktree. Não tocada por este trabalho. Commitar,
   descartar, ou investigar?
