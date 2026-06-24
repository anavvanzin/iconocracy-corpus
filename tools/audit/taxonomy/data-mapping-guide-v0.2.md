# Data Mapping Guide — Taxonomia v0.2 → Sessão de 80 Fios

**Versão:** v0.2 (revisada após mini-validação 30 fios)
**Data:** 19 de junho de 2026
**Propósito:** guia prático de codificação para a sessão completa, com **alta confiança na estabilidade do output**

---

## I. O que mudou de v0.1 para v0.2

| Aspecto | v0.1 | v0.2 |
|---|---|---|
| Estrutura do vínculo | Apenas binário (A↔B) | **Binário + Cadeia (CHAIN)** |
| Endurecimento progressivo | Categoria binária | **Relação CHAIN** (≥3 itens) |
| Multi-tipo | Exceção | **Norma** (até 3 relações ordenadas por fio binário) |
| Genealogia | 1 categoria | 3 sub-tipos (canônica / tensional / ascendente) |
| Translatio | 1 categoria | 3 sub-tipos (republicana / imperial / fundacional) |
| Inversão | 1 categoria | 2 sub-tipos (sincrônica / diacrônica) |
| Contradição | 1 categoria | 3 sub-tipos (intra / transnacional / colonial) |
| Flags semânticos | Inexistentes | **5 flags** (modulam categorias sem multiplicar) |
| Total de distinções | 15 | **32** (15 base + 9 sub-tipos + 3 chains + 5 flags) |

A concordância projetada com este sistema sobe de **50% (v0.1)** para **≥75% (v0.2)**.

---

## II. Pipeline de execução

```
PASSO 1   Abrir mnemosyne-template-v0.2.xlsx
          → 11 sheets: README, P1–P8, Cadeias CHAIN, SÍNTESE

PASSO 2   Abrir o ICONOCRACIA Warburg Atlas (canvas)
          → carregar mnemosyne-threads-starter.json (sementes por painel)

PASSO 3   Para cada painel (~30min cada):
          a) Arrastar candidatos da biblioteca para o canvas
          b) Modo Fio → desenhar 10 fios binários
          c) Para o Painel 4: desenhar 2-3 CHAINS de 3+ itens
          d) Preencher cada fio na aba correspondente do XLSX
          e) Escrever o ensaio do painel no canvas

PASSO 4   Exportar JSON de cada painel do canvas (botão ↓ Export)
          → 8 arquivos iconocracia-painel-N.json

PASSO 5   Rodar:
          python3 analyze_threads_v2.py corpus.json iconocracia-painel-*.json
          → produz thread-analysis-report.md, chain-analysis.md, thread-analysis.json

PASSO 6   Comparar XLSX preenchido (sua classificação manual)
          contra report.md (classificação automática)
          → calcular taxa de concordância por painel

PASSO 7   Se concordância ≥70% em cada painel → declarar v1.0
          Se concordância <70% em algum painel → micro-iteração no classificador
```

**Tempo total estimado:** 8–10h de sessão + 2h de revisão pós-execução = 12h.

---

## III. Como decidir cada categoria — árvore de decisão prática

Quando você for desenhar um fio, **siga esta árvore mentalmente** antes de escolher a relação primária:

```
Pergunta 1: Os dois itens são do mesmo país?
  SIM → ativar flag 'internal_to_country'
        → Pergunta 1a: Mudam de regime entre A e B?
            SIM + score crescente → genealogia_ascendente
            SIM sem score crescente → genealogia_canonica ou martializacao/desmilitarizacao
            NÃO → mimesis ou serializacao ou genealogia_canonica

  NÃO → países diferentes
        → Pergunta 1b: Há registro colonial?
            SIM → translatio_imperial
            NÃO → Pergunta 1c: Os dois são fundacionais?
                    SIM + transmissão institucional documentável → translatio_fundacional + flag
                    SIM sem transmissão documentável → nachleben
                    NÃO → translatio_republicana

Pergunta 2: Há contra-alegoria em pelo menos um lado?
  SIM → ativar Família III
        → Δ temporal > 25 anos? → inversao_diacronica
        → Δ ≤ 25 anos? → inversao_sincronica + satirizacao (multi-tipo)
        → Há contradição interna do mesmo aparelho? → contradicao_intra ou colonial
        → Contra-alegorias seriais entre países? → genealogia_tensional

Pergunta 3: Os dois itens pertencem ao mesmo aparelho institucional?
  SIM + registro colonial → contradicao_colonial (substitui Contradição + Co-presença)
  SIM sem colonial → copresenca_institucional
  NÃO → copresenca_politica (se contemporâneos)

Pergunta 4: A relação envolve 3+ itens em sequência temporal?
  → Não use binário. Use CHAIN na aba "Cadeias CHAIN"
  → Score crescente monotônico? → endurecimento_progressivo
  → Score crescente + cruza países? → endurecimento_cross_country
  → Score não crescente mas contemporâneos? → constelacao_temporal
```

---

## IV. Casos paradigmáticos por painel — uso direto

### Painel 1 — Gênese (fundacional)

Cenário típico do fio: estampas de Necker 1781 ↔ estampa Le Barbier 1789.
- **internal_to_country**: SIM (FR)
- **cross_regime**: NÃO (ambos fundacional)
- **Δ temporal**: 8 anos
- **Decisão**: `mimesis` (primária) + `concretizacao` (secundária — a alegoria pré-revolucionária se concretiza em fiadora constitucional)

Fio típico Cross-country: Le Barbier 1789 ↔ Compromisso Constitucional BR-1896.
- **internal_to_country**: NÃO
- **Δ temporal**: 107 anos (diachronic)
- **Há transmissão institucional?**: SIM (Brasil olha explicitamente para França)
- **Decisão**: `translatio_fundacional` (primária) + flag `institutional_transmission`

### Painel 4 — ENDURECIMENTO (chain + binário)

**Caso paradigmático CHAIN:** FR-015 (1781, ⬥1.3) → FR-013 (1789, ⬥1.8) → FR-SEM-1898 (1898, ⬥2.5).
- **Min items**: 3 ✅
- **Score crescente**: ✅
- **Decisão chain**: `endurecimento_progressivo`

**Caso CHAIN com inflexão militar:** FR-SEM-1898 (norm, ⬥2.5) → FR-008 (mil, ⬥1.2) → FR-007 (mil, ⬥1.8).
- A queda 2.5→1.2 é "inflexão militar" — o regime militar opera por mobilização tópica que reduz purificação visual
- **Decisão chain**: `endurecimento_progressivo` com flag implícito de inflexão (o analisador detecta automaticamente)

**Caso binário dentro do mesmo painel:** FR-SEM-1898 (norm) ↔ FR-008 (mil) sem cadeia explícita.
- **cross_regime**: SIM
- **A precede B**: SIM
- **Decisão binária**: `martializacao` (primária) + `genealogia_canonica` (secundária — a Marianne militar é descendente da Marianne normativa)

### Painel 6 — Balança e Império (contradição colonial)

Fio típico: BE-002 (Palais Justice Bruxelles 1866) ↔ BE-CONGO-MON-1921 (Monumento aos Pioneiros Congo).
- **internal_to_country**: SIM (BE)
- **colonial_register**: SIM
- **mesma instituição**: SIM (aparelho belga)
- **Decisão**: `contradicao_colonial` (primária — caso especial substitui Contradição + Co-presença)

Fio típico imperial: BE-CONGO-100F-1912 ↔ FR-PIAST-1885 (Piastre Indochina).
- **internal_to_country**: NÃO
- **colonial_register**: SIM (ambos)
- **mesmos motivos**: SIM (Europa imperial + atributos)
- **Decisão**: `translatio_imperial` (primária) + `mimesis` (secundária — execução visual similar)

### Painel 8 — Fissuras (multi-tipo é a regra)

Fio típico: FR-031 (Madame Anastasie 1874) ↔ FR-033 (L'Empire c'est la paix 1870).
- **mesma época, mesmo país**: SIM
- **Ambos contra-alegoria**: SIM
- **Decisão multi-tipo**: `satirizacao` (primária) + `inversao_sincronica` (secundária) + `contradicao_intra` (terciária — os dois operam contradição diferente sobre o mesmo regime imperial/republicano)

Fio típico genealogia tensional: BR-019 (voto feminino) ↔ FR-031 (Madame Anastasie 1874).
- **Δ temporal**: ≥80 anos
- **Ambos contra-alegoria**: SIM
- **Decisão**: `genealogia_tensional` (primária — tradição satírica continua) + `nachleben` (secundária — pathosformel da censura ressurge)

---

## V. Flags — quando ativar cada um

| Flag | Quando ativar | Efeito downstream |
|---|---|---|
| `institutional_transmission` | Há documentação de cadeia ativa (carta, currículo, presença em arquivo de B citando A) | Distingue translatio_fundacional de nachleben |
| `colonial_register` | Pelo menos um item está em registro colonial (BE-CONGO, FR-PIAST, UK-trade, NL-Indes) | Aciona contradicao_colonial quando combinado com mesma instituição |
| `diachronic` | Δ temporal > 25 anos | Distingue inversao_diacronica de sincronica; ativa sugestão Nachleben |
| `internal_to_country` | A e B no mesmo país | Distingue Genealogia interna de Translatio |
| `cross_regime` | A e B em regimes diferentes | Ativa Martialização, Desmilitarização ou Endurecimento progressivo (chain) |

**Regra para o XLSX:** liste os flags na coluna "Flags" separados por vírgula.

---

## VI. Métricas de controle de qualidade

Ao final da sessão, calcule estas métricas e registre na aba SÍNTESE:

| Métrica | Alvo v1.0 | Como medir |
|---|---|---|
| **Fios binários completos** | 80 | Soma de fios preenchidos em P1–P8 |
| **Cadeias CHAIN** | ≥3 (no Painel 4) | Linhas preenchidas na aba "Cadeias CHAIN" |
| **Concordância manual ↔ auto plena** | ≥70% | `analyze_threads_v2.py` reporta automaticamente |
| **Concordância manual ↔ auto plena+parcial** | ≥85% | Idem |
| **Multi-tipo (≥2 relações em fios binários)** | ≥30% (algum acúmulo é a norma) | Conta automaticamente |
| **Painel 4 com ≥1 cadeia de 4+ itens** | obrigatório | Tese central exige |
| **Painel 8 com ≥1 fio genealogia_tensional** | obrigatório | Validação do sub-tipo novo |
| **Painel 6 com ≥1 fio contradicao_colonial** | obrigatório | Validação do sub-tipo novo |
| **Pelo menos 1 fio com cada sub-tipo novo** | recomendado | Validação completa dos 9 novos sub-tipos |

---

## VII. Critérios para declarar v1.0

A taxonomia pode passar de v0.2 → v1.0 quando, ao final da sessão:

- [ ] Os 80 fios binários estão preenchidos com pelo menos `relação primária` + `iconológico` não-vazio
- [ ] Pelo menos 3 cadeias CHAIN preenchidas (no Painel 4 ou cruzando painéis)
- [ ] Concordância plena ≥70% — em pelo menos 6 dos 8 painéis
- [ ] Concordância plena+parcial ≥85% — em pelo menos 7 dos 8 painéis
- [ ] Cada um dos 9 sub-tipos novos da v0.2 foi usado em pelo menos um fio
- [ ] Pelo menos um fio recebeu acumulação de 3 relações (primária + secundária + terciária)
- [ ] Ensaio do painel (na aba "essay" do Warburg) tem ≥150 palavras

Se algum critério falhar, **aplique micro-iteração no classificador** (`analyze_threads_v2.py`) antes de declarar v1.0. Documente as alterações no `taxonomy-v0.2-schema.json` → v0.3 (que se torna v1.0 quando os critérios são atendidos).

---

## VIII. Cronograma da sessão completa

| Sessão | Duração | Painéis | Saída |
|---|---|---|---|
| Dia 1 (manhã) | 2h | P1 Gênese + P4 ENDURECIMENTO (binários + chains) | 20 fios + 3 chains |
| Dia 1 (tarde) | 2h | P2 Justitia + P5 Pedra e Bronze | 20 fios |
| Dia 2 (manhã) | 2h | P3 Domesticação + P6 Balança e Império | 20 fios |
| Dia 2 (tarde) | 2h | P7 Branquitude + P8 Fissuras | 20 fios |
| Dia 3 (manhã) | 1h | Exportar JSONs + rodar analisador | reports |
| Dia 3 (tarde) | 1h | Revisar concordância + ajustes finos | v1.0 final |

**Total: 10h ao longo de 3 dias.** Pode ser distribuído ao longo de uma semana com sessões mais curtas.

---

## IX. Pontos de atenção

1. **Não force categoria primária quando multi-tipo se justifica.** Use a ordem (primária / secundária / terciária) para registrar dominância, mas registre o acúmulo.

2. **Flags são gratuitos.** Marque todos os que se aplicam; eles não competem entre si.

3. **Cadeias CHAIN não substituem fios binários.** Você pode ter, no Painel 4: 10 fios binários + 3 chains. Ambas estruturas convivem.

4. **Quando em dúvida entre dois sub-tipos, escolha o mais específico.** Translatio_fundacional > Translatio_republicana se houver transmissão institucional documentável.

5. **Contradição colonial é exclusiva.** Se você acionou esta categoria, NÃO precisa registrar também Co-presença institucional ou Contradição intra-nacional — `contradicao_colonial` já agrega ambas. Isto evita duplo-contagem na análise estatística.

6. **Sub-tipos não retiram a categoria-mãe.** Genealogia_canonica, _tensional e _ascendente são todas formas de Genealogia. Para análise agregada por família, o analisador soma todos os sub-tipos sob a família mãe.

7. **CHAINs são frágeis: revise as datas e os scores antes de declarar.** Uma cadeia com score [1.3, 1.8, 1.5, 2.5, 1.2] **passa** se a queda final estiver no regime militar (inflexão militar). Caso contrário, é uma constelação_temporal.

---

## X. Pacote completo de entregáveis (v0.2)

| Arquivo | Função |
|---|---|
| `taxonomy-v0.2-schema.json` | Schema completo (5 famílias + 21 tipos + 3 chains + 5 flags) |
| `analyze_threads_v2.py` | Classificador atualizado (binário + chain, multi-tipo, sub-tipos, flags) |
| `mnemosyne-template-v0.2.xlsx` | Caderno de trabalho (11 sheets) |
| `data-mapping-guide-v0.2.md` | Este documento — guia de codificação |

**Inputs necessários para começar:** apenas o `corpus.json` (já disponível no workspace).

**Outputs após sessão completa:**
- 8 JSONs exportados do Warburg
- XLSX preenchido
- `thread-analysis-report.md`, `chain-analysis.md`, `thread-analysis.json`

**Output meta:** a taxonomia ICONOCRACIA v1.0, defensável na qualificação.
