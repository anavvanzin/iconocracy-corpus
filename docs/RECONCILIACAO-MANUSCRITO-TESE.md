# Reconciliação do Manuscrito — ICONOCRACIA

> Gerado em 2026-06-04. Diagnóstico read-only do estado real do manuscrito espalhado
> pelo repo `iconocracy-corpus`. Decisão de estrutura registrada: **híbrida**
> (front matter teórico-metodológico + estudos de caso).
> Nada foi movido nem apagado — este documento é o mapa para a execução (Claude Code).

---

## 1. Estrutura canônica (decisão: híbrida)

Front matter (base) seguido dos estudos de caso. Proposta de slots:

| Slot | Capítulo | Origem da prosa viva hoje |
|------|----------|---------------------------|
| 00 | Introdução — o paradoxo iconocrático | `tese/manuscrito/Introducao_rev.md` (5355w, único) |
| 01 | Quadro teórico (4 clusters) | a definir — hoje embutido na Introdução/Cap1 |
| 02 | Metodologia (Panofsky + endurecimento + corpus) | **decisão pendente** — 3 variantes (ver §3) |
| 03 | Análise quantitativa | `Capitulo3_analise_quantitativa.md` (552w stub) + seções 3.2/3.3 em `vault/tese/drafts/` |
| 04 | Gênese: alegoria na Revolução e Estados liberais (1789–1870) | a remapear |
| 05 | Consolidação: alegorias nacionais e impérios (1870–1918) | a remapear |
| 06 | Tradução tropical: a República brasileira (1822–1945) | caso-âncora |
| 07 | Crise e contestação: iconoclasmo e redemocratização (1930–1988) | `vault/tese/capitulo-6*` (?) |
| 08 | Conclusão — A Justiça ainda é mulher? | `vault/tese/conclusao.md` (291w stub) |

> Os números de capítulo do plano (6 casos) e os arquivos escritos (metodologia/quantitativo)
> divergiam; a estrutura híbrida reconcilia: base teórico-metodológica **e** casos.

---

## 2. Reconciliação por hash — 3 baldes

### Balde A — Duplicatas EXATAS (seguro arquivar; manter 1 cópia canônica)

Mesmo md5 = conteúdo idêntico. Lar canônico = `tese/manuscrito/`; redundantes → `_archive/manuscrito-dups-2026-06-04/`.

| Conteúdo | Cópias idênticas | Manter |
|----------|------------------|--------|
| `Capitulo1_rev` (3236w) | `Text/`, `tese/manuscrito/` | manuscrito |
| `Capitulo1_original_v2` (3311w) | `Text/`, `tese/manuscrito/` | manuscrito |
| `conclusao` (291w) | `wiki/tese/`, `Text/(2)`, `vault/tese/` | vault→manuscrito |
| `introducao` stub (506w) | `wiki/`, `Text/(2)`, `vault/` | 1 cópia |
| `sumario-iconocracia` (2661w) | `wiki/drafts`, `Text/`, `vault/drafts` | 1 cópia |
| `capitulo-2` (1590w) | `wiki/`, `Text/(2)`, `vault/` | 1 cópia |
| `capitulo-6` (1476w) | `wiki/`, `Text/(2)`, `vault/` | 1 cópia |
| `capitulo-6-sessao` (2981w) | `wiki/`, `Text/(2)`, `vault/` | 1 cópia |
| stubs `capitulo-1,3,4,7,8,9` (69–106w) | `Text/(2)` + `vault/` | esqueleto: 1 cópia |

### Balde B — ÚNICOS (preservar; cópia só existe em um lugar)

| Arquivo | Words | Data | Local | Observação |
|---------|-------|------|-------|------------|
| `Introducao_rev.md` | 5355 | 25/abr | `tese/manuscrito/` | introdução viva |
| `Capitulo2_metodologia.md` | 2937 | **25/mai** | `tese/manuscrito/` | metodologia mais recente (curta) |
| `Capitulo3_analise_quantitativa.md` | 552 | **25/mai** | `tese/manuscrito/` | stub — conteúdo real nas seções abaixo |
| `capitulo-2-reescrito.md` | **7961** | 30/abr | `vault/tese/metodologia/` | metodologia longa (única!) |
| `capitulo-2-imes.md` | 6713 | 30/abr | `vault/tese/metodologia/` | metodologia variante longa |
| `capitulo-3-secao-3.2-DRAFT.md` | 1687 | 29/abr | `vault/tese/drafts/` | seção real do Cap3 |
| `capitulo-3-secao-3.3-DRAFT.md` | 2078 | 29/abr | `vault/tese/drafts/` | seção real do Cap3 |
| `capitulo-5.md` | 1003 | 25/abr | `vault/tese/` | possível material de caso |

### Balde C — VARIANTES DIVERGENTES (decisão editorial sua — NÃO arquivar no escuro)

| Tema | Variantes (words / data / local) |
|------|----------------------------------|
| **Introdução** | manuscrito `Introducao_rev` 5355w · `Text/Introducao_rev` 5318w (hash diferente!) · stubs 506w |
| **Metodologia (Cap2)** | manuscrito 2937w (25/mai) · vault `capitulo-2-reescrito` **7961w** · vault `capitulo-2-imes` 6713w · `Text/capitulo-2-reescrito` 3852w · stub 1590w |
| **Cap2 original v2** | manuscrito `Introducao_original_v2` 5348w vs `Text/Introducao_original_v2` 5348w (hashes diferentes — micro-diff) |

---

## 3. A decisão que destrava o Cap2 (metodologia)

Há **cinco** arquivos de metodologia, e o mais recente por data (2937w, maio) é o **mais curto**;
os longos (7961w, 6713w) são de abril e estão só no `vault/`. Preciso saber:

- O `Capitulo2_metodologia.md` (maio, 2937w) é uma **versão enxugada deliberada**, ou um recorte que perdeu o corpo?
- Ou o `capitulo-2-reescrito.md` (7961w) é a versão de trabalho real e o de maio é um resumo?

A resposta define qual vira o Cap2 canônico e quais viram `_archive`/insumo.

---

## 4. Bug do compile (make)

- `make -C vault/tese/` compila os **stubs de abril** (`vault/tese/capitulo-1..9.md`, 69–106w).
- `Makefile` + `abnt.csl` existem **só** em `vault/tese/`.
- **Correção:** mover o harness (`Makefile`, `abnt.csl`, `_sumario.md`) para o lar canônico do
  manuscrito e apontar as fontes para os capítulos vivos — OU manter `vault/tese/` como dir de
  build mas com os capítulos canônicos lá dentro. (Decidir junto com §1.)

---

## 5. Plano faseado

**Fase A — mecânica, segura (script com dry-run, git mv, quarentena):**
1. Eleger `tese/manuscrito/` como lar único do manuscrito.
2. Arquivar todas as duplicatas exatas do Balde A → `_archive/manuscrito-dups-2026-06-04/`.
3. Mover os ÚNICOS do Balde B para `tese/manuscrito/` (preservando como drafts).
4. Mover o harness de compile para junto da prosa viva; corrigir paths no `Makefile`.
5. Rodar `validate_schemas.py` antes/depois (teste de não-regressão) + compile smoke test.

**Fase B — editorial, sua:**
1. Resolver as variantes do Balde C (§3) — em especial o Cap2.
2. Remapear a prosa para os slots 00–08 da estrutura híbrida.
3. Atualizar `docs/PLANO-TESE-ICONOCRACIA.md` para refletir a híbrida.

---

## 6. Próximo passo

Resolver §3 (qual metodologia é canônica). Com isso eu fecho o mapa de `git mv` e gero o
`reorganizar-tese-manuscrito.sh` (dry-run por padrão) para você rodar no Claude Code.
