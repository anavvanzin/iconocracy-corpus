# Audit Sistemático — Indicadores Panofsky no Subcorpus Francês

**Tese:** ICONOCRACIA — Alegoria Feminina na História da Cultura Jurídica (Séc. XIX–XX), PPGD/UFSC
**Data do audit:** 19 de junho de 2026
**Fonte:** `iconocracy-corpus/corpus/corpus-data.json` (commit atual, 116 entries)
**Subset:** 34 entradas francesas (FR-*)
**Auditor:** verificação automatizada com revisão manual cruzada

---

## Sumário Executivo

A pergunta original priorizava seis entradas (FR-013, FR-014, FR-015, FR-016, FR-017, FR-021). O audit completo do subcorpus francês mostra que **a lacuna é estrutural, não pontual**: 24 das 34 entradas francesas (70,6%) não possuem o objeto `panofsky` no JSON do corpus. As seis entradas inicialmente sinalizadas são apenas a ponta visível.

### Tabela de cobertura por campo

| Campo Panofsky               | Entradas com dado | Entradas sem dado | Cobertura |
|------------------------------|:-----------------:|:-----------------:|:---------:|
| `pre_iconographic`           | 10                | 24                | 29,4%     |
| `iconographic` (nível 2)     | 10                | 24                | 29,4%     |
| `iconological.regime` (texto)| 10                | 24                | 29,4%     |
| `iconological.funcao`        | 10                | 24                | 29,4%     |
| `description` geral          | 23                | 11                | 67,6%     |
| `indicadores` (10 ordinais)  | 24                | 10                | 70,6%     |
| `regime` (tag categórica)    | 24                | 10                | 70,6%     |

### Achado adicional crítico: duplicata

- **FR-012** "La Liberté guidant le peuple (Eugène Delacroix)" — 1830, regime `fundacional`, score 0,1
- **FR-021** "Liberty Leading the People" — 1830, regime vazio, score 0

Trata-se da **mesma obra** (Delacroix, Louvre) com dois IDs no corpus. **Deduplicar antes da submissão.** Decidir qual entrada manter (sugerido: FR-012, que já tem indicadores parciais e regime atribuído) e excluir FR-021.

---

## Quadro Geral das 34 Entradas Francesas

Legenda: ✅ OK — ⚠ Thin (texto < 30 caracteres) — ❌ Missing

| ID                | Ano  | Regime          | ⬥    | Pré-Ic. | Ico. | Reg. Pan. | Função | Indicadores |
|-------------------|:----:|:----------------|:----:|:-------:|:----:|:---------:|:------:|:-----------:|
| FR-020            | 1250 | fundacional     | 1.2  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-011            | 1531 | fundacional     | 1.1  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-015            | 1781 | fundacional     | 1.3  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-016            | 1781 | fundacional     | 1.3  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-017            | 1781 | fundacional     | 1.3  | ❌      | ❌   | ❌        | ❌     | ✅          |
| **FR-013**        | 1789 | fundacional     | 1.8  | ❌      | ❌   | ❌        | ❌     | ✅          |
| **FR-014**        | 1789 | fundacional     | 1.8  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-018            | 1796 | fundacional     | 1.5  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-012            | 1830 | fundacional     | 0.1  | ❌      | ❌   | ❌        | ❌     | ✅          |
| **FR-021**        | 1830 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-003            | 1859 | fundacional     | 1.2  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-004            | 1859 | normativo       | 1.2  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-001            | 1865 | fundacional     | 0.6  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-002            | 1865 | fundacional     | 0.5  | ✅      | ✅   | ✅        | ✅     | ✅          |
| FR-010            | 1868 | contra-alegoria | 0.3  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-HERC-1870      | 1870 | fundacional     | 1.5  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-005            | 1871 | contra-alegoria | 0.8  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-PIAST-1885     | 1885 | militar         | 2.3  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-006            | 1887 | normativo       | 0.9  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-SEM-1898       | 1898 | normativo       | 2.5  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-SEM-SELO-1903  | 1903 | normativo       | 1.7  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-022            | 1909 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-008            | 1915 | militar         | 0.8  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-019            | 1915 | militar         | 1.1  | ❌      | ❌   | ❌        | ❌     | ✅          |
| FR-023            | 1916 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-030            | 1916 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-007            | 1917 | militar         | 1.8  | ✅      | ✅   | ⚠         | ✅     | ✅          |
| FR-024            | 1917 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-027            | 1918 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-025            | 1920 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-026            | 1920 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-028            | 1920 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-029            | 1920 | —               | 0    | ❌      | ❌   | ❌        | ❌     | ❌          |
| FR-009            | 1950 | normativo       | 2.4  | ✅      | ✅   | ⚠         | ✅     | ✅          |

Itens em **negrito** são os priorizados na pergunta inicial.

---

## Análise dos Padrões

### Padrão 1 — Codificação em três coortes históricas
A inspeção do campo `coded_by` revela três grupos:
- **`iconocode-opus`** (14 entradas, FR-001 a FR-010 aproximadamente): coorte mais antiga, com Panofsky parcial; campo `iconological.regime` aparece como string curta ("FUNDACIONAL", "NORMATIVO") em vez de texto interpretativo.
- **`iconocode-opus-4.6-image`** (10 entradas, principalmente as numismáticas e medievais): tem `indicadores` completos e `endurecimento_score`, mas **sem Panofsky textual**.
- **`None`** (10 entradas, principalmente Emprunts da Défense Nationale, 1916–1920): **codificação não iniciada**.

### Padrão 2 — Cluster temático com lacuna total
Todas as **dez entradas dos Emprunts de la Défense Nationale (1916–1920)** estão sem qualquer codificação. Trata-se de um cluster militar/normativo de transição que pode ser codificado em lote: cartazes de empréstimo de guerra com iconografia republicana, mesmo gênero, mesmo período, mesma função propagandística. Sugere campanha única de codificação.

### Padrão 3 — Indicadores presentes, Panofsky ausente (irregular)
Entradas como FR-013, FR-014, FR-015–017, FR-018, FR-PIAST-1885, FR-SEM-1898, FR-HERC-1870 têm `indicadores` preenchidos e `endurecimento_score` legado, **mas o texto Panofsky que justificaria essa codificação não foi registrado.** Esta lacuna foi uma das razões da aposentadoria do índice composto no codebook v2.2.1 (DEC-2026-07-28): o número sobrevivia sozinho, sem a descrição que o sustentaria. Para a tese ser defensável, cada indicador marcado precisa de texto descritivo de suporte. **Esta é a lacuna mais crítica.**

### Padrão 4 — Campo `iconological.regime` em texto curto
Para as 10 entradas com Panofsky parcial, o `iconological.regime` aparece como rótulo categórico (ex.: "FUNDACIONAL", "NORMATIVO transitioning to NORMATIVO") em vez de **análise iconológica de regime**. O campo deveria conter o terceiro nível de Panofsky — leitura simbólica do regime iconocrático em que a obra opera —, não apenas redundância da tag categórica `regime`.

---

## Checklist de Resolução Pré-Submissão

### TIER 1 — Bloqueadores citados no Capítulo 3 (urgência alta)

- [ ] **FR-013** (Le Barbier, Déclaration 1789) — citada como pivô do argumento. Preencher `panofsky.pre_iconographic`, `iconographic`, `iconological.regime`, `iconological.funcao`. Justificar score 1.8 com base nos 10 indicadores.
- [ ] **FR-014** (Declaração 1789, variante anônima) — idem FR-013. Pode usar mesma base interpretativa, ajustando para a variante.
- [ ] **FR-015** (Necker 1781, frontispício original) — Preencher Panofsky completo. Tese: alegoria como ornamento contábil pré-revolucionário.
- [ ] **FR-016** (Necker 1781, variante 2) — idem FR-015.
- [ ] **FR-017** (Necker 1781, variante 3) — idem FR-015.
- [ ] **FR-018** (Ernouf, 1796) — Preencher Panofsky completo. Tese: modulação directorial, fusão alegoria/retrato individual.
- [ ] **FR-012 vs FR-021** (Delacroix duplicado) — Decidir entrada canônica. Sugerido: manter **FR-012**; excluir FR-021 do corpus. Atualizar JSON, atlas, citações.
- [ ] **FR-021** (Delacroix sem regime) — se for mantida em vez de FR-012, completar `regime`, `indicadores` (10), inventário verbal de atributos e Panofsky completo. Não calcular composto (aposentado em v2.2.1).

### TIER 2 — Entradas fundacionais e numismáticas citáveis (urgência média)

- [ ] **FR-020** (Decretum Gratiani 1250) — Preencher Panofsky. Importante para argumentar herança medieval da Iustitia.
- [ ] **FR-011** (Calendrier 1531) — Preencher Panofsky.
- [ ] **FR-HERC-1870** (5 Francs Hercule) — Preencher Panofsky. Importante: numismática de transição IIIª República.
- [ ] **FR-PIAST-1885** (Piastre coloniale) — Preencher Panofsky. Crítico: único item militar coberto antes de 1915, cobertura colonial.
- [ ] **FR-SEM-1898** (Semeuse 1 Franc) — Preencher Panofsky. Já citada como item de score máximo (2.5), exemplar do regime normativo.
- [ ] **FR-SEM-SELO-1903** (Semeuse selo) — Preencher Panofsky.
- [ ] **FR-019** (Journée du Poilu 1915) — Preencher Panofsky.

### TIER 3 — Cluster Emprunts de la Défense Nationale (codificação em lote)

Codificação ausente nas 10 entradas a seguir; mesmo gênero, podem ser codificadas em campanha única:

- [ ] **FR-022** Notre-Dame des colonies (Veber, 1909)
- [ ] **FR-023** Bons de la Défense nationale (1916)
- [ ] **FR-030** En avant Armée de l'Epargne (1916)
- [ ] **FR-024** French Republic — 3rd National Defense loan (1917)
- [ ] **FR-027** Emprunt de la Libération (1918)
- [ ] **FR-025** Emprunt national — Société générale (1920)
- [ ] **FR-026** National loan 1920 — Banque Nationale de Paris (1920)
- [ ] **FR-028** Prêtez à la France (1920)
- [ ] **FR-029** Emprunt national 1920 — Société centrale des banques (1920)

Para cada uma: atribuir `regime` (provável: militar ou normativo-militar), preencher os 10 `indicadores`, registrar o inventário verbal dos atributos marcados e redigir Panofsky completo. Não calcular composto (aposentado em v2.2.1).

### TIER 4 — Aprimoramento dos campos "Thin" existentes

Estas entradas têm Panofsky parcial mas `iconological.regime` em formato categórico (texto curto). Reescrever como análise iconológica de regime (não apenas tag):

- [ ] **FR-001** "FUNDACIONAL" → expandir para análise de 2–3 frases sobre o regime icnocrático específico
- [ ] **FR-003** "FUNDACIONAL with delegation" → expandir
- [ ] **FR-004** "NORMATIVO" → expandir
- [ ] **FR-005** "CONTRA-ALEGORIA" → expandir
- [ ] **FR-006** "NORMATIVO (at crisis point)" → expandir
- [ ] **FR-007** "MILITAR" → expandir
- [ ] **FR-008** "MILITAR" → expandir
- [ ] **FR-009** "NORMATIVO (paradigmatic)" → expandir
- [ ] **FR-010** "CONTRA-ALEGORIA" → expandir

### TIER 5 — Validação cruzada e consistência

- [ ] **Auditoria de inter-rater**: 24 dos 34 itens foram codificados por `iconocode-opus-4.6-image` (apenas indicadores) sem segunda passagem humana. Para cumprir o método exposto no Cap. 4, fazer segunda codificação manual em pelo menos 10% (3–4 itens) e calcular Cohen's Kappa.
- [ ] **Discrepância FR-018**: campo `year` = 1796; `citation_abnt` = "c. 1793–1800". Harmonizar via consulta ao registro Gallica original.
- [ ] **Discrepância FR-012/FR-021**: deduplicação (ver Tier 1).
- [ ] **Verificar campo `coded_by`** em todas as 24 entradas com Panofsky pendente. Documentar quem codifica cada uma após o preenchimento (para rastreabilidade ABNT).
- [ ] **Campo `motif_str` vazio em FR-021**, `motif` vazio em vários itens do cluster Emprunts. Preencher após codificação Panofsky.

### TIER 6 — Articulação com o Atlas e o Capítulo 3

- [ ] Após preenchimento dos Tiers 1–3, **republicar o atlas** (`/home/user/workspace/iconocracy-atlas/`) regenerando `data.json` a partir do corpus atualizado.
- [ ] **Atualizar a seção do Cap. 3** (case study francês) removendo as 6 notas de revisão sobre Panofsky ausente. Confirmar que cada citação de score (1.3, 1.8, 1.5, etc.) agora se apoia em texto descritivo no JSON.
- [ ] **Verificar coerência regime ↔ score**: itens com `regime = fundacional` e score > 2.0 ou < 0.5 devem ter justificativa explícita no Panofsky (são exceções à curva esperada).

---

## Métricas de Progresso

Estado atual: **29,4% de cobertura Panofsky completa** (10/34 com os 4 campos preenchidos).

Para chegar a 100% antes da submissão, faltam:
- **24 entradas a codificar Panofsky completo** (Tiers 1–3)
- **9 entradas a expandir `iconological.regime`** (Tier 4)
- **1 deduplicação** (FR-012/FR-021)
- **1 harmonização de data** (FR-018)

Estimativa de esforço: aproximadamente **6 a 10 horas de codificação dedicada** se aplicado o agente IconoCode com revisão manual subsequente; ou **2 a 3 horas** se as 9 entradas Tier 4 forem expandidas em campanha única e os 10 Emprunts (Tier 3) forem codificados em lote como cluster homogêneo.

---

## Anexo — Saída técnica

O audit JSON completo (todos os campos por entrada, status por campo, valores atuais) foi gerado em:

`/home/user/workspace/cap3-french-audit.json`

Carregar com:
```python
import json
with open('cap3-french-audit.json') as f:
    audit = json.load(f)
# Filtrar bloqueadores Tier 1
tier1 = [a for a in audit if a['id'] in ['FR-013','FR-014','FR-015','FR-016','FR-017','FR-018','FR-012','FR-021']]
```
