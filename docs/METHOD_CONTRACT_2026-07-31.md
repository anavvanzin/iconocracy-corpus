# Contrato metodológico ICONOCRACY — 2026-07-31

> **Vigente a partir de**: 2026-07-31
> **Decisão formal**: [DEC-2026-07-31-METODOLOGIA-2-0](decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md)
> **Documento anterior**: [METHOD_CONTRACT_2026-04-23.md](METHOD_CONTRACT_2026-04-23.md) (legacy/histórico)

---

## Números canônicos

- **Corpus público atual**: ~328 itens em `corpus/corpus-data.json`.
- **Ledger canônico atual**: ~328 registros em `data/processed/records.jsonl`.
- **Codificação de purificação atual**: ~279 itens em `data/processed/purification.jsonl`.
- **Cartões de vault**: ~413 em `vault/candidatos/`.

> **Nota**: N é intencionalmente não-fixo até a defesa. Tratar números como *instantâneo de trabalho*, não como base congelada de resultados.

---

## Escala canônica

Os 10 indicadores de endurecimento usam escala ordinal 0–3.

- 0: ausente
- 1: baixo
- 2: médio
- 3: alto

Não usar escala 0–4 em texto final, artigo derivado ou prompts ativos.

---

## Estatuto epistêmico

A `iconometria` é o framework guarda-chuva (medição/análise de padrões iconográficos). Dentro dela, o `endurecimento` é um único eixo de fixidez, operacionalizado pelos 10 indicadores ordinais.

- `purificacao_composto` está **deprecated** como valor probatório. Permanece no schema e nos dados legados apenas para backward compatibility.
- O inventário verbal de atributos é a forma de argumentação, não dado para agregação estatística.
- O atlas topológico é operador relacional (Warburg: Pathosformel, Zwischenraum, Nachleben).
- As contra-alegorias são teste crítico do regime, não catálogo amplo.

---

## Relação entre iconometria e endurecimento

A iconometria organiza a montagem metodológica e não reduz a tese a uma mensuração. O endurecimento é uma camada operacional da iconometria: capta sinais formais da Purificação Clássica, discrimina regimes iconocráticos e orienta comparação entre casos.

---

## Terminologia

- Usar `endurecimento`, não `hardening` ou `embrutecimento`.
- Usar `Contrato Sexual Visual` como conceito autoral.
- Usar `Feminilidade de Estado` como conceito autoral.
- Usar `Contrato Racial Visual` como conceito autoral.
- Usar `Purificação Clássica` como conceito autoral.
- Manter `Pathosformel`, `Zwischenraum` e `Nachleben` em alemão.
- Usar `iconometria` como framework guarda-chuva.

---

## Regra de contagem nos capítulos

Quando o capítulo tratar do corpus atual, escrever `~328 itens`.
Quando tratar da purificação efetivamente codificada, escrever `~279 itens codificados`.
Quando mencionar números de fases anteriores, deixar claro que se trata de snapshot analítico histórico.

---

## Rastreabilidade

Cada item do corpus deve existir em três lugares:

1. Google Drive + `data/raw/drive-manifest.json`
2. `vault/candidatos/XX-NNN Title.md`
3. `data/processed/records.jsonl`

A rastreabilidade pública substitui a confiabilidade estatística como dispositivo de controle de qualidade.

---

## Critérios de inclusão (todos obrigatórios)

1. Figura alegórica feminina explícita.
2. Função jurídico-política explícita.
3. Datável entre 1800–2000.
4. Suporte iconográfico aceito (moeda, selo, monumento/escultura, arquitetura forense, estampa/gravura, frontispício, papel-moeda, cartaz).

País é variável analítica, **não** gate de inclusão.

---

## Protocolo de codificação aberto

O protocolo está em `docs/CODING_PROTOCOL.md`. Inclui:
- Critérios de inclusão/exclusão explícitos e auditáveis.
- Dicionário de atributos.
- Regras de decisão.
- Exemplos de codificação.

---

## Dispositivo de controle de qualidade

A metodologia 2.0 substitui instrumentos de confiabilidade importados (kappa, alfa, teste-reteste) por quatro elementos textuais:

1. Critérios de inclusão/exclusão explícitos e auditáveis.
2. Declaração do corpus como catálogo documentado, não amostra estatística.
3. Justificação de casos exemplares.
4. Resposta antecipada à objeção de impressionismo (Roele).

---

## Limites e silêncios arquivísticos

1. Ausência de amostragem probabilística.
2. Corpus fechado por relevância, não por sorteio.
3. Codificação por pesquisador único (ou equipe reduzida).
4. Impossibilidade de replicabilidade mecânica.
5. Viés de conservação arquivística.
6. Silêncio de suportes perecíveis.
7. Concentração em regimes iconocráticos específicos.
8. Dificuldade de comparação intercorpus.
9. Dependência de fontes secundárias para itens não acessíveis digitalmente.

Cada limite deve ter parágrafo próprio na seção "Limites e silêncios arquivísticos" do texto final da tese.

---

## Referências

- DEC-2026-07-31-METODOLOGIA-2-0
- DEC-2026-07-28-aposentadoria-do-indice-composto
- CONTRA-ALEGORIAS-INTEGRATION-2026-06-26
- Anexo M.5 — Quarto regime epistêmico (topological atlas como Path B)
- Codebook v2.2.1 → v2.3.0
