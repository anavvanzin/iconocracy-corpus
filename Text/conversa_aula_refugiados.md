# Conversa: Aula — Direito dos Refugiados (Relações Internacionais)

**Data:** Quarta-feira, 22 de abril de 2026  
**Espaço:** metodologia  
**Tarefa:** Preparar aula completa sobre Direito dos Refugiados para turma de graduação em Relações Internacionais — plano de aula, roteiro de fala e slides PPTX.

---

## Mensagem do Usuário (1)

> Use the 'research-knowledge-super-skill' skill. prepare uma aula acerca de direito dos refugiados para uma turma de relações internacionais. faça o plano de aula, roteiro de fala, e depois slides

---

## Plano de Trabalho (aprovado sem modificação)

O agente propôs e o usuário aprovou o seguinte plano:

- **Pesquisa de fontes** — instrumentos primários (Convenção 1951, Protocolo 1967, Lei 9.474/97), literatura acadêmica recente (2020–2025), dados ACNUR Global Trends 2024
- **Plano de aula** — estrutura em 7 blocos temáticos, 120 min, com referências ABNT NBR 6023:2025
- **Roteiro de fala** — texto corrido por bloco, marcadores de tempo, pausas pedagógicas, indicações de slide
- **Slides PPTX** — 22 slides com design system próprio (azul marinho + dourado), QA visual iterativo

---

## Execução

### Fase 1 — Pesquisa

Pesquisa paralela em múltiplas fontes:

**Instrumentos primários:**
- Convenção de 1951: https://www.acnur.org/fileadmin/Documentos/portugues/BDL/Convencao_relativa_ao_Estatuto_dos_Refugiados.pdf
- Protocolo de 1967: https://www.acnur.org/fileadmin/Documentos/portugues/BDL/Protocolo_de_1967_Relativo_ao_Estatuto_dos_Refugiados.pdf
- Lei 9.474/97: https://www.planalto.gov.br/ccivil_03/leis/l9474.htm

**Dados estatísticos:**
- UNHCR Global Trends 2024 (123,2 milhões de deslocados forçados ao fim de 2024): https://reliefweb.int/report/world/global-trends-forced-displacement-2024-enar
- UNHCR Projected Resettlement Needs 2025 (2,9 milhões precisam de reassentamento): https://reliefweb.int/report/world/unhcr-projected-global-resettlement-needs-2025

**Literatura acadêmica (ABNT NBR 6023:2025):**
- BÉRES, Nóra. "The anatomy of non-refoulement" (2024). DOI: 10.47078/2024.1.31-49
- MORSHED, Md. Tarik; FERDOUSY, Mumtahena. "Reconceptualising non-refoulement in climate-induced migration" (2025). DOI: 10.3329/dulj.v36i1.85144
- CLARO, Carolina. "A proteção jurídica dos 'refugiados ambientais' nas três vertentes" — REMHU (2020): https://www.scielo.br/j/remhu/a/fggZzvX45NgzBhQQYLbdTrP/?lang=pt
- PIJNENBURG, Annick. "Containment Instead of Refoulement" (2020). DOI: 10.2139/ssrn.3418365
- WHITE, Benjamin; RAHAL, Malika. "UNHCR and the Algerian war of independence" (2022). DOI: 10.1017/S1740022821000449

**Jurisprudência/procedimento:**
- REMHU — RSD no Brasil: https://www.scielo.br/j/remhu/a/nfvG8RFv9mJHNtcrwWK6Kyw/
- Caso Teitiota v. Nova Zelândia (CCPR/ONU, 2020): https://tbinternet.ohchr.org/_layouts/15/treatybodyexternal/Download.aspx?symbolno=CCPR%2FC%2F127%2FD%2F2728%2F2016

---

### Fase 2 — Plano de Aula

**Arquivo gerado:** `/home/user/workspace/plano_aula_refugiados.md`

**Estrutura em 7 blocos temáticos (120 minutos):**

| Bloco | Tema | Duração |
|-------|------|---------|
| 1 | Contexto histórico pré-1951 | 15 min |
| 2 | Arquitetura normativa — Convenção de 1951 e Protocolo de 1967 | 25 min |
| 3 | Definição de refugiado, cláusulas de exclusão, non-refoulement | 20 min |
| 4 | ACNUR — mandato, estrutura, limites | 15 min |
| 5 | Desafios contemporâneos: deslocamento climático, IDPs, externalização | 20 min |
| 6 | Brasil e América Latina: CONARE, Declaração de Cartagena, casos recentes | 15 min |
| 7 | Discussão e encerramento | 10 min |

---

### Fase 3 — Roteiro de Fala

**Arquivo gerado:** `/home/user/workspace/roteiro_aula_refugiados.md`

Texto corrido por blocos com:
- Marcadores de tempo `[⏱]`
- Pausas pedagógicas `[P]`
- Indicações de transição `[→SLIDE]`
- Pergunta de discussão final: cenário Tuvalu/refugiado climático (caso Teitiota)

---

### Fase 4 — Slides PPTX

#### Design System

| Elemento | Especificação |
|----------|---------------|
| Cor de acento | `#1B3A5C` (azul marinho escuro) |
| Dourado | `#C08C2A` |
| Superfície | `#F8F7F4` (bege off-white) |
| Texto | `#1A1917` |
| Fontes | Trebuchet MS Bold (títulos), Calibri (corpo) |
| Total de slides | 22 |

**Estrutura cromática:**
- Slides escuros (1, 9, 14, 20): fundo `#1B3A5C`, barras douradas no topo e na base
- Slides claros (demais): fundo `#F8F7F4`, barra azul fina no topo

#### Iterações de QA

**v1 → v2 (correções críticas):**
- Slide 11: números `01/02/03` quebravam em múltiplas linhas → alterados para algarismos romanos `I/II/III` como caracteres únicos
- Slide 12: nota de rodapé e fonte sobrepostas → separadas em posições `y` distintas
- Slide 14: cards de prévia com estilo só de contorno (invisíveis) → preenchimento sólido `accentMid`
- Slide 2 (roteiro): layout de 2 colunas com card órfão → alterado para 3 colunas

**v2 → v3 (correções remanescentes):**
- Slides 6 e 17: cabeçalhos de tabela com texto invisível → substituição da função `addTable()` do pptxgenjs por helper manual `addTableWithHeader()` que desenha explicitamente o cabeçalho com retângulo azul marinho + texto branco
- Slide 9: barra dourada ausente no topo → `addGoldBar(s,'both')` adicionado
- Slide 1: barra dourada ausente na base → `addGoldBar(s,'both')` adicionado
- Slide 21: último item com fundo escuro → todos os itens com fundos claros alternados
- Slide 8: cards inferiores inconsistentes → todos os 5 cards com preenchimento `accentLt`

**v3 → v4 (correções pós-QA visual final a 300 DPI):**

O subagente de QA reportou "BUG CRÍTICO" nas tabelas dos slides 6 e 17. Inspeção direta a 300 DPI confirmou que o texto branco estava correto — o subagente estava vendo artefatos de compressão JPEG a 150 DPI. As correções efetivamente aplicadas foram:

- Slide 19: borda lateral do card "Síria" em verde `#437A22` (fora da paleta) → alterada para `accentMid` (azul marinho)
- Slide 21: alternância de fundo entre `accentLt` (`#D6E4F0`) e `#F0F4F8` era imperceptível → alternância agora entre `accentLt` e `bg` (`#F8F7F4`) com borda sutil, maior contraste visual
- Slide 22: numeração "22 / 22" encoberta pela faixa de rodapé institucional → numeração movida para acima da faixa (`y: H-0.85`)

#### Arquivo final entregue

`/home/user/workspace/aula_refugiados_final.pptx` — 22 slides, design system completo, fontes hiperlinked em rodapé de cada slide de conteúdo.

---

## Mensagem do Usuário (2)

> save this conversation as a whole as a markdown

---

## Resposta do Agente

Conversa exportada para `/home/user/workspace/conversa_aula_refugiados.md`.

---

## Arquivos Produzidos

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `plano_aula_refugiados.md` | Plano de aula com 7 blocos e referências ABNT NBR 6023:2025 | Entregue |
| `roteiro_aula_refugiados.md` | Roteiro de fala por blocos com marcadores de tempo e slide | Entregue |
| `aula_refugiados_final.pptx` | 22 slides — design system azul marinho + dourado | Entregue |
| `slides_refugiados_v3.js` | Script pptxgenjs v3 (penúltima versão) | Referência |
| `slides_refugiados_v4.js` | Script pptxgenjs v4 — versão final com correções de QA | Referência |
| `conversa_aula_refugiados.md` | Este arquivo — histórico completo da conversa | Entregue |

---

## Skills e Configurações

**Skills carregadas:**
- `research-knowledge-super-skill` (skill do usuário) — pesquisa e síntese de fontes
- `office/pptx` (built-in) — geração de apresentações com pptxgenjs
- `design-foundations` (built-in, dependência automática) — sistema de design, tipografia, paleta

**Instruções de integridade acadêmica aplicadas (do perfil do usuário):**
- Referências ABNT NBR 6023:2025 com DOI onde disponível
- Nenhuma fonte fabricada ou invista — apenas fontes rastreáveis
- Separação explícita entre: (a) citação direta, (b) tradução própria, (c) interpretação do agente
- Um termo estável por conceito, instituição e autor (sem deriva terminológica)
- Idioma dos artefatos: Português (Brasil)
