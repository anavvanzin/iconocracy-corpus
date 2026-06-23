# IRR opus-4.8 × Gemini-3.1-Pro (cross-instrumento DIRETO, brief rico) — 2026-06-22 — CITÁVEL

Audit direto do lote opus-4.8, versão LIMPA (controla os confounds do run Flash preliminar). rater-1 = opus-4.8 (14 itens coded, cohort principal); rater-2 = **Gemini 3.1 Pro (High)** via `agy`, **codificação cega** com **o mesmo brief rico** (PT, Panofsky + ancoragem 0–3 detalhada) que o opus usou. Krippendorff α ordinal.

## Resultado (N=14)
- **α global = 0.393** · composto MAD **0.65** · **regime exato 0.71**.
- opus comp. médio 0.84 vs Gemini-Pro 1.03 (offset sistemático quase nulo, +0.19).
- α por indicador (decrescente): heraldicizacao 0.562 · rigidez_postural 0.527 · inscricao_estatal 0.491 · uniformizacao_facial 0.455 · apagamento_narrativo 0.449 · desincorporacao 0.429 · dessexualizacao 0.345 · serialidade 0.282 · enquadramento_arquitetonico 0.191 · monocromatizacao 0.103.
- **Nenhum indicador atinge poolável (≥0.667).**

## Comparação das 3 auditorias
| par | α global | comp MAD | regime exato | N |
|---|---|---|---|---|
| opus-legado × fable-5 | 0.601 | 0.31 | 0.61 | 28 |
| opus-4.8 × Gemini-3.5-Flash (terse) | −0.02 | 1.17 | 0.50 | 14 |
| opus-4.8 × Gemini-3.1-Pro (rich) | 0.393 | 0.65 | 0.71 | 14 |

O run Flash (−0.02) era artefato de tier+prompt (offset de calibração): com Pro+brief rico o offset some e α sobe a 0.393.

## Veredito (2 instrumentos independentes: fable + Gemini)
1. **Regime: robusto cross-instrumento** (Gemini 0.71, fable 0.61) → análise no nível de regime é defensável.
2. **Composto: moderado** (MAD 0.65) → usável com cautela.
3. **Indicador cru: NÃO transfere** (α global 0.393, nenhum ≥0.667). Os pooláveis do opus×fable NÃO generalizam (monocromatizacao 0.87→0.10). Valores de indicador são instrumento-dependentes → analisar DENTRO de um estrato, nunca poolar entre instrumentos.
4. fable (0.601) era otimista (classe próxima do opus); Gemini independente dá 0.393.

## Implicação para #8 (integração do opus-4.8)
Integrar/analisar no nível **regime** (lastreado por 2 instrumentos independentes) é defensável; o **composto** com cautela; **indicadores ficam estratificados por instrumento** e nunca poolados. Caveat: N=14.

Ferramenta: `agy` (antigravity CLI; Gemini 3.1 Pro headless via `-p` + `@imagem`). Substitui o preliminar `IRR-opus-gemini-2026-06-22` (Flash). Artefato: `IRR-opus-gemini-PRO-2026-06-22.json`.
