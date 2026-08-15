# Design — Documento C: "Paradigma indiciário e padrões de prova na iconografia jurídica"

- **Data**: 2026-08-14
- **Status**: aprovado (decisões em sessão 2026-07-31 → 2026-08-06)
- **Issues**: #168 (este estágio C) · #169 (B, bloqueado) · #170 (A, bloqueado)
- **Origem**: síntese Consensus "Iconografia Jurídica Feminista: Paradigma Indiciário e Evidência Metodológica" (jul/2026) + discussão em sessão.

## Objetivo

O capítulo de metodologia (`tese/manuscrito/Capitulo4_metodologia.md`) valida **operacionalmente** (deltas metadados × imagem, §2.5) mas não legitima **epistemologicamente** o padrão de prova. O documento C lapida essa defesa **antes** de tocar o manuscrito, numa sequência C → B → A decidida pela autora:

- **C** — dossiê teórico autônomo (este design);
- **B** — revisão ampla do Capítulo 2 integrando os três fios transversalmente;
- **A** — seção integrada final "§2.X Paradigma indiciário e padrões de prova".

## Decisões registradas

| Decisão | Valor |
|---|---|
| Abordagem | **1 — Dossiê modular** (3 módulos + síntese), escolhida sobre ensaio único e matriz de defesa |
| Local do arquivo | `tese/manuscrito/notas/paradigma-indiciario_padroes-de-prova.md` |
| Formato | arquivo único, módulos como seções de nível 1, ~6–7 mil palavras |
| Rastreamento | GitHub Issues `anavvanzin/iconocracy-corpus` #168/#169/#170 |
| Ancoragem bibliográfica | plugin scholar, antes da redação de cada fio |

## Estrutura do documento

- **M1 — Posição estratificada (~2.000 pal.)**: objeção empiricista; tabela nível panofskiano × natureza das unidades × medida cabível; passo analógico Rau & Shih → iconografia **construído** (3 condições do κ violadas, evidência interna FR-025/026/028/029); codificadores-IA (confiabilidade recolocada como reprodutibilidade de protocolo + validação humana por amostragem); fecho: padrão epistêmico (Moran; Braman).
- **M2 — Legitimação indiciária (~2.000 pal.)**: Ginzburg (paradigma indiciário × galileano; Morelli/Freud/Holmes); homologia iconometria = semiótica do vestígio; Warburg via Didi-Huberman (Nachleben, montagem como forma de conhecimento → legitima Atlas Iconocrático); Panofsky direto (cada nível com critério de correção próprio); fecho: filiação a outra tradição de evidência.
- **M3 — Silêncio arquivístico visual (~2.000 pal.)**: Hartman (fabulação crítica); Fuentes (violência epistêmica); ausência alegórica como dado constitutivo (US-020; `#ausencia-alegorica`); declaração de limites como validação (N aberto, dupla codificação, viés de acervo); por que não é "anything goes" (Braman + protocolo + rastreabilidade).
- **Síntese (1–2 pp.)**: argumento integrado em prosa corrida = embrião da seção do estágio A (#170).
- **Referências**: ABNT NBR 6023:2025.

## Ancoragem scholar (executada 2026-08-14, CSVs em `/Users/ana/Research/.tmp/scholar/`)

| Referência | Status |
|---|---|
| Ginzburg, "Clues: Roots of a Scientific Paradigm" (Theory and Society, 1979); "Morelli, Freud and Sherlock Holmes" (History Workshop, 1980) | ✅ confirmado |
| Didi-Huberman, *Atlas ou le gai savoir inquiet* (Minuit, 2011) | ✅ confirmado |
| Goodrich, *Legal Emblems and the Art of Law* (Cambridge UP) | ✅ confirmado (ano errado no scholar "1945"; real 2014) |
| Goodrich & Hayaert, *Genealogies of Legal Vision* (2015) | ✅ confirmado |
| Resnik & Curtis, *Representing Justice* (Yale UP, 2011) | ✅ confirmado |
| Douzinas & Nead, *Law and the Image* (U. Chicago Press, 1999) | ✅ confirmado |
| Goldenfein, "The profiling potential of computer vision…" (FAT*, 2019) | ✅ confirmado (bônus, para M1.4) |
| Roele, crítica do "dodging empiricism" | ⚠ **não localizado** no scholar; no documento fica com flag `#verificar` até confirmação no Zotero |

## Critérios de validação

- Voz acadêmica formal em português; ABNT NBR 6023:2025;
- Warburg em alemão (*Pathosformel*, *Zwischenraum*, *Nachleben*); Mondzain sempre 2002; "endurecimento" sempre em PT;
- Não ceder autoria dos 4 conceitos originais (Contrato Sexual Visual; Feminilidade de Estado; Contrato Racial Visual; Purificação Clássica);
- Iconclass oficial 44/11M44; não afirmar 48C51 como rótulo oficial;
- N do corpus descrito provisionalmente (ledger operacional × amostra analítica);
- Nunca "ciberfeminismo";
- Gate final: peer review simulado (skill academic-paper-reviewer) + revisão da Ana.

## Fora de escopo (neste estágio)

- Qualquer edição de `Capitulo4_metodologia.md` ou demais capítulos (estágio B, #169);
- Compilação Pandoc do manuscrito;
- Codificação de novos itens do corpus;
- Commit (matriz de propriedade de paths não lista este harness; arquivos ficam no working tree para a Ana versionar).
