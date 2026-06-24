# Auditoria de Confound de Instrumento — opus × Fable-5 (queue #1, "o disparo que fundamenta")

**Data:** 2026-06-22 · **Resolve:** o resíduo central da dialética (Monk B "confound fatal" vs Monk A "sem confound") com **dado**, não opinião.

## Método
Conjunto de sobreposição: os 44 itens em-escopo recodificados pelo Fable-5 que TAMBÉM têm codificação prévia real (não-zero) em `records.jsonl::purificacao`. **N=28** (instrumento prévio: `iconocode-opus` 20 + `iconocode-opus-4.6-metadata-refined` 8). Os outros 15 do overlap eram zeros do Gemma (consertados pelo Fable-5 — história à parte, não comparação inter-instrumento). Métricas por indicador (escala ordinal 0–3): concordância exata, dentro de ±1, MAD (mean absolute difference) e viés direcional.

## Resultado
- **GERAL:** concordância exata **56%** · dentro de **±1 = 93%** · **MAD 0,53** · **viés de composto Fable-5−prévio = −0,12** (≈0) · MAD-composto 0,31.
- **Indicadores que CONCORDAM (quase-medida, Panofsky-1):** serialidade (82% exato, MAD 0,29) · monocromatização (68%, 0,32). → instrumento *não* importa; são data-like.
- **Indicadores INSTRUMENTO-SENSÍVEIS (juízo, Panofsky-2/3):** enquadramento_arquitetônico (43%, MAD 0,89, viés −0,54) · inscrição_estatal (43%, MAD 0,79, viés −0,57) · heraldicização (46%). → instrumento importa.
- **Viés direcional pequeno e MISTO** (alguns +, alguns −), sem deslocamento uniforme de severidade.

## Veredito (fundamentação)
**O confound de instrumento é REAL, mas brando e localizado — não fatal.**
- No nível de **composto/regime**: instrumentos são amplamente intercambiáveis (±1 = 93%, viés de composto ≈ 0). **Pooling no nível do headline é defensável** — refuta o "confound fatal" do Monk B *no agregado*.
- No nível de **indicador**: 2 indicadores (enquadramento_arquitetônico, inscrição_estatal) são instrumento-sensíveis (MAD ~0,8). **Não dá para poolar cegamente o dado indicador-a-indicador** — refuta o "sem confound" do Monk A *no detalhe*.

→ **Confirma empiricamente o candidato S (partição):** os indicadores quase-medida (serialidade, monocromatização) são poolável/congelável; os indicadores-juízo (enquadramento, inscrição_estatal) exigem instrumento único ou flag. A estrutura de duas camadas (Tier 1 medida / Tier 2 juízo) **aparece DENTRO do esquema de codificação, indicador por indicador** — não só entre tipos de alegação. (Era a queue #2, agora respondida junto.)

## Recomendação operacional
1. **Headline estatístico (regime, composto):** pode usar o N maior poolado (opus + Fable-5); o instrumento não move o sinal agregado. Reportar a auditoria no dataset card.
2. **Indicador-a-indicador:** para enquadramento_arquitetônico e inscrição_estatal, usar **um instrumento único** (Fable-5, que vê a imagem) ou marcar como instrumento-sensível.
3. **Formalizar:** rodar `compute_irr.py` / `calculate_irr.py` para Krippendorff α ordinal (κ ponderado) por indicador — o MAD/exato aqui é o atalho; α é o número para a banca.

## O que isto faz com o leque S/J/G/F
- **S** ganha suporte empírico (a partição é real e mensurável).
- **G** (escritor único) e **F** (moldura) permanecem vivos e ortogonais — não foram tocados por este dado.
- **J** (tensão tempo/deadline) permanece como resíduo não-empírico.
