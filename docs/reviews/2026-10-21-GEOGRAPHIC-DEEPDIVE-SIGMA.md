# APROFUNDAMENTO GEOGRÁFICO QUANTITATIVO — ICONOCRACY
**Revisor:** Sigma (OpenMausBot) — lente `academic-geographer`
**Data:** 2026-10-21 · **Base:** árvore de trabalho em `84b256c` (main); complementa `2026-10-21-GEOGRAPHIC-VALIDATION-SIGMA.md` (commit 0ee2444)
**Dados:** `data/processed/records.jsonl` (337 registros vivos), `corpus_dataset.csv` (328 linhas, export stale)
**Regras honradas:** N é PROVISÓRIO — nenhuma contagem é tratada como inconsistência de N; nenhum arquivo do manuscrito foi editado.

---

## A. A dominância francesa é um efeito de composição temporal (reforça achado 1 da v1)
Partição por `date_hint` (ano explícito + séculos aproximados; 27 registros permanecem sem data):

| Período | N | França | Brasil | Leitura |
|---|---|---|---|---|
| 1500–1799 | 71 | 26 (37%) | 3 (4%) | França domina |
| 1800–1849 | 19 | 8 (42%) | 3 (16%) | França domina |
| 1850–1899 | 93 | 24 (26%) | **32 (34%)** | Brasil lidera |
| 1900–1949 | 107 | 22 (21%) | **29 (27%)** | Brasil lidera |
| 1950+ | 18 | 3 (17%) | **6 (33%)** | Brasil lidera |

O polo francês do catálogo (30,4% agregado, Cap.6:18) sustenta-se apenas antes de 1850; de 1850 em diante o Brasil é o maior país em todos os períodos. A "centralidade franco-atlântica" como traço do corpus é um artefato da sobre-amostragem do período moderno precoce — ou uma hipótese histórica sobre o período pré-1850, mas não um traço transversal.
**Caveat:** 27 registros sem data parseável (12 deles France com `date_hint` vazio). Se esses forem majoritariamente modernos precoces (aparência de gravuras Justitia), o efeito se **reforça**, não se reverte. Confiança alta.

## B. Metrópole × colônia: sistemático, não anedótico (estende achado 3 da v1)
Scan de `webscout.summary_evidence` + `title_hint` nos registros com `place_hint` de metrópole: **6 registros** registram circulação/produção colonial enquanto o país atribuído é a metrópole:
- France → Indochina: `jsonl:31` (Piastre de Commerce) e `jsonl:178` (1 Piastre — French Indochina)
- United Kingdom → cunhagem Bombay/Calcutta, circulação Hong Kong/Straits/Labuan: `jsonl:37` (Trade Dollar)
- Belgium → Congo: `jsonl:78` (Monument aux Pionniers Belges), `jsonl:133` (100 Francs Banque du Congo Belge), `jsonl:134` (20 Francs Belgian Congo)

Qualquer leitura territorial da tabela "País" subestima a geografia imperial desses 6 itens. Confiança alta.

## C. "Falha sistêmica" estadunidense não é o extremo do corpus (reforça achado 4 da v1)
Cruzamento país × `purificacao.regime_iconocratico` (337 registros):

| País | N | fund. | norm. | militar | contra-aleg. | militar % |
|---|---|---|---|---|---|---|
| France | 102 | 56 | 28 | 12 | 6 | 12% |
| Brazil | 73 | 34 | 31 | 5 | 2 | 7% |
| United States | 32 | 12 | 10 | 8 | 2 | **25%** |
| Germany | 27 | 15 | 8 | 3 | 1 | 11% |
| Italy | 20 | 5 | 4 | 11 | 0 | **55%** |
| Portugal | 11 | 5 | 1 | 5 | 0 | **45%** |
| Netherlands | 10 | 7 | 3 | 0 | 0 | 0% |

Itália (55% militar) e Portugal (45%) excedem largamente os EUA (25%). A narrativa do Cap.9:249 é seleção de casos, não o extremo empírico do corpus; a França tampouco é o paradigma isolado de purificação (Holanda 70% fundacional). Confiança alta nos números; a interpretação do painel permanece do autor.

## D. A tabela "País" do Cap.6 mistura proveniência de dados (novo)
- JSONL vivo, normalização ISO→nome: **França 102, Brasil 73**, EUA 32, Alemanha 27, R.U. 23 — total 337.
- CSV stale (328 linhas): França **97**, Brasil **72**.
- Tabela publicada (Cap.6:22, total 336): França **102** (fonte: JSONL vivo) e Brasil **72** (bate com o CSV stale, não com o JSONL: 73). O total 336 omite exatamente 1 registro; o bucket "demais = 80" coincide por construção.
Nenhuma dessas é inconsistência de N (N é provisório); o problema é a **proveniência mista e não declarada** numa única tabela que sustenta o achado central de distribuição. Confiança alta.

## E. Contagem francesa contém desvio interno de atribuição (novo, estende achado 2)
**9 registros com `place_hint='France'` têm título majoritariamente em alemão e `date_hint` vazio** (`jsonl:194, 196, 205, 210, 213, 214, 215` + `190, 212` mistos francês/alemão-italiano): "Allegorie auf die Gerechtigkeit…", "Putti als Allegorien der Gerechtigkeit…", "[Gerechtigkeit; Justice]", "Justitia (Gerechtigkeit)", etc. Um deles (`jsonl:196`) cita "Albert and Isabella" — corte de Bruxelas/Habsburgo. São ~9% dos 102 registros franceses; se remanejados, a França segue #1 (≈93), mas o "30,4%" publicado passa a ≈28% e a distância sobre o Brasil estreita. Necessária verificação de proveniência item a item (acervo de origem), não apenas título. Confiança média-alta (indício linguístico forte, não prova).

## F. Normalização silenciosa de grafias (estende achado 2)
26 grafias distintas → regra aplicada (ISO→nome) nunca declarada no manuscrito. Formatos ISO em 17 registros, em **3 formatos diferentes**: `'FR'` (4), `"['FR']"` (7), `'[FR]'` (1); idem BR/DE/ES/CL/BE. A regra de normalização usada na tabela do Cap.6 precisa virar nota de método; qualquer mudança de regra muda o ranking (ex.: Brasil 72↔73). Confiança alta.

## G. 12% do corpus sem data utilizável para análise temporal (novo)
41/337 `date_hint` não parseáveis por ano explícito ('17th century', 'Unknown', 'século XIX', 'séculos XVI–XVIII', vazio); com séculos aproximados, restam 27. Desse total, 20 são France — a estratificação temporal de qualquer país precisa declarar essa lacuna. Confiança alta.

---

## O que permanece não verificado
Inspeção das imagens, proveniência real dos 9 itens de título alemão, documentação histórica de circulação dos 6 itens coloniais, e a causa da omissão de 1 registro no total da tabela do Cap.6. Nada disto muda o diagnóstico: as conclusões espaciais do manuscrito dependem de regras de normalização e estratificação ainda não declaradas.
