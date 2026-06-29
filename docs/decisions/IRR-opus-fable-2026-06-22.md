# IRR opus-legado × fable-5 (Krippendorff α ordinal) — 2026-06-22

Formaliza `dialectic-corpus-2026-06-19/confound_audit_2026-06-22.md` com α de Krippendorff (o estatístico para a banca). Rodado via `tools/scripts/compute_irr.py --rater2 <fable5>`.

## N e método
- **N=28** (válido): itens com coding opus-legado real (`iconocode-opus` 20 + `opus-4.6-metadata-refined` 8) recodificados pelo fable-5.
- ⚠️ **Bug do script:** o default puxa N=44 e cai em placeholders `migration`/zeros para os 16 sem coding opus → α≈0.03 (artefato). `get_rater1_purification` deveria PULAR migration/batch-tentative, não fazer fallback. Usar N=28.

## α por indicador (N=28)
| indicador | α | leitura |
|---|---|---|
| monocromatizacao | 0.874 | poolável (bom) |
| serialidade | 0.820 | poolável (bom) |
| inscricao_estatal | 0.529 | instrumento-sensível |
| apagamento_narrativo | 0.501 | instrumento-sensível |
| rigidez_postural | 0.495 | instrumento-sensível |
| uniformizacao_facial | 0.467 | instrumento-sensível |
| heraldicizacao | 0.464 | instrumento-sensível |
| desincorporacao | 0.455 | instrumento-sensível |
| enquadramento_arquitetonico | 0.405 | instrumento-sensível (pior) |
| dessexualizacao | 0.278 | instrumento-sensível (pior) |

**Global α=0.601** · composto MAD 0.31 · regime exato 0.61 · ±1=93%.

## Veredito
Confirma a **partição de duas camadas (candidato S do council)**: quase-medida (serialidade, monocromatização) poolável (α>0.8); juízo não-poolável. **Composto/regime intercambiáveis** entre instrumentos → headline poolável; **indicador-a-indicador NÃO** (sobretudo enquadramento_arquitetonico 0.41 e inscricao_estatal 0.53).

## Implicação para integração do opus-4.8 (#8)
- Poolar no nível composto/regime: defensável. Indicador-a-indicador: manter estratificado por instrumento.
- α global 0.601 < 0.667 → confiabilidade inter-instrumento marginal; moldar o dataset card e o Cap.3 em torno do composto/regime, não do indicador cru.
- **Lacuna:** isto é opus-legado×fable, não opus-4.8 direto. Dupla-codificar amostra dos 31 (2º instrumento) para audit direto = passo pendente.

Artefatos: `IRR-opus-fable-2026-06-22.json` (N=28 diagnóstico). lib `krippendorff` instalada na env iconocracy (3.11).
