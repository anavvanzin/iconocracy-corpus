---
title: "Codebook Elicit — Glossário ICONOCRACIA"
subtitle: "Instrumento de extração para completar tese/manuscrito/Glossario.md"
author: "Ana Vanzin"
lang: pt-BR
type: instrumento-pesquisa
tool: "Elicit (plano Scale)"
created: 2026-06-26
tags: [glossario, elicit, codebook, extracao, metodo]
---

# Codebook Elicit — Glossário ICONOCRACIA

Instrumento para **completar iterativamente** o `tese/manuscrito/Glossario.md` usando o
Elicit (plano Scale). Cobre os três usos do Elicit: **(A) Find Papers**, **(B) Extract /
colunas de extração** (o codebook propriamente dito) e **(C) Systematic review** com
critérios. Trabalhe **um bloco temático por vez** (warburguiano, iconologia, teóricos,
alegorias) — não rode tudo de uma vez.

> [!warning] Regra inviolável (cole no topo de toda sessão Elicit)
> **NÃO** redefinir nem atribuir a terceiros os 4 conceitos autorais da tese — *Contrato
> Sexual Visual, Feminilidade de Estado, Contrato Racial Visual, Purificação Clássica*.
> O Elicit serve para fundamentar o **andaime teórico externo** (Warburg, Panofsky,
> Iconclass, teóricos do corpo político, alegorias nacionais) e para mapear **raízes
> genealógicas** desses conceitos — nunca para autoria. Recorte: **história da cultura
> jurídica / iconografia jurídico-política**, não cultura visual genérica nem antropologia.

---

## A · Prompt de pesquisa (Find Papers)

Cole no campo de pergunta do Elicit, **substituindo `<TERMO>` e `<AUTOR>`** a cada rodada:

```
Authoritative scholarly definition, origin, and canonical reference of the concept
"<TERMO>" (<AUTOR>) as used in art history, visual studies, and the history of legal
culture. I need: (1) a precise short definition; (2) who originated the term and in which
work/year; (3) how it has been applied to political iconography, female national
allegories, and the visual representation of law, justice, and the State (19th–20th
centuries). Prioritize primary sources and authoritative secondary literature. Exclude
generic visual-culture or pop-culture usages.
```

Variante para **alegorias nacionais** (Marianne, Germania, Columbia, Britannia, La
Belgique, A República/A Justiça, Justitia):

```
Origin, dating, and juridical-political function of the female national allegory
"<ALEGORIA>" (<PAÍS>): when and why it emerged, what State/legal value it personifies,
and key scholarship analyzing it as a personification of law, justice, the republic, or
the nation. Focus on the long nineteenth century (1789–1914) and on its use on coins,
stamps, monuments, courthouse architecture, and prints.
```

---

## B · Codebook — colunas de extração (Extract)

Crie estas colunas na tabela do Elicit. Use os **nomes** como título e a **instrução**
como descrição da coluna (o Elicit extrai por artigo seguindo a instrução). A saída
mapeia 1:1 nos campos de cada verbete do glossário.

| # | Coluna (nome) | Instrução de extração (cole na descrição da coluna) | → Campo no Glossário |
|:--:|---|---|---|
| 1 | `termo_canonico` | Forma canônica do termo conforme usado pela fonte; manter na língua original quando for convenção (alemão p/ Warburg; latim p/ Iustitia). | cabeçalho do verbete |
| 2 | `definicao_curta` | Definição em **1–2 frases**, fiel ao sentido da fonte; sem paráfrase vaga. Português. | corpo do verbete |
| 3 | `autor_origem` | Quem **cunhou/originou** o termo (nome completo). Se a fonte só *usa* o termo, registrar "uso, não origem". | proveniência |
| 4 | `obra_ano_editora` | Obra de referência onde o termo é definido: título, ano, editora, cidade. | referência ABNT |
| 5 | `citacao_textual` | **Citação literal** (verbatim) que define o termo, com número de página. Se ausente, "não disponível". | base p/ citação direta |
| 6 | `campo_disciplinar` | Campo da fonte (história da arte, teoria do direito, filosofia, estudos de gênero, etc.). | curadoria/recorte |
| 7 | `uso_juridico_iconografico` | Como o termo se aplica a **direito, justiça, Estado, alegoria feminina** (séc. XIX–XX). Se a fonte não fizer essa ponte, escrever "sem ponte jurídica explícita". | coluna "Uso na tese" |
| 8 | `relacao_conceitos_tese` | A qual eixo da tese se conecta (Purificação Clássica · Contrato Sexual Visual · Feminilidade de Estado · Contrato Racial Visual · regime fundacional/normativo/militar). **Apenas relação, nunca atribuição de autoria.** | mapa conceitual |
| 9 | `lingua_e_traducao` | Manter no original ou traduzir? Tradução PT recomendada e termo a **evitar** (ex.: nunca "hardening"/"embrutecimento" p/ endurecimento; nunca "ciberfeminismo"). | nota de convenção |
| 10 | `referencia_abnt` | Referência **já formatada em ABNT NBR 6023:2025**. | seção Referências |
| 11 | `confianca_flags` | Nível de confiança (alta/média/baixa) + flag `#verificar` se ano/edição/atribuição estiverem incertos ou se houver risco de ceder autoria de conceito da tese. | flags do verbete |

> [!tip] Coluna de controle anti-erro
> Acrescente uma coluna `risco_autoria` com a instrução: *"A fonte atribui a algum autor
> externo um dos 4 conceitos autorais da tese (Contrato Sexual Visual, Feminilidade de
> Estado, Contrato Racial Visual, Purificação Clássica)? Se sim, sinalizar ⚠ e citar o
> trecho."* Isso captura automaticamente o risco mais grave.

---

## C · Critérios (Systematic review)

- **Inclusão:** fonte acadêmica (livro/capítulo/artigo revisado por pares ou catálogo de
  museu/instituição) que **define, origina ou aplica** o termo a iconografia
  político-jurídica, alegoria feminina, ou representação visual de direito/justiça/Estado.
- **Exclusão:** uso meramente ilustrativo; cultura visual genérica sem recorte jurídico;
  fontes não acadêmicas (blogs, enciclopédias colaborativas) **exceto** como pista a
  confirmar; recorte fora de 1789–2000 (salvo genealogia da Antiguidade p/ Iustitia).
- **Idiomas:** PT, EN, FR, DE, IT, ES.

---

## D · Queries-semente por termo (rode em lotes)

> Os 4 conceitos autorais **não** entram aqui (não se pesquisa externamente a definição).
> Pesquisar apenas as **raízes genealógicas** quando indicado.

### Bloco 1 — Léxico warburguiano
| Termo | `<AUTOR>` | Nota |
|---|---|---|
| Pathosformel | Aby Warburg | + Agamben, Didi-Huberman como secundários |
| Nachleben (der Antike) | Aby Warburg | "afterlife of antiquity" |
| Zwischenraum / Denkraum | Aby Warburg | espaço-entre / espaço de pensamento |
| Mnemosyne / Bilderatlas | Aby Warburg | ed. Warnke (Akademie, 2000) |

### Bloco 2 — Iconologia / classificação
| Termo | `<AUTOR>` | Nota |
|---|---|---|
| Níveis pré-iconográfico/iconográfico/iconológico | Erwin Panofsky | *Studies in Iconology*, 1939 |
| Iconologia (método) | Panofsky / círculo Warburg | distinguir de iconografia |
| Iconclass (sistema; códigos 44, 11M44) | Henri van de Waal | **48C51 = "painting", NÃO feminista** (já verificado) |

### Bloco 3 — Teóricos do corpo político / matriz jurídica
| Termo | `<AUTOR>` | Nota (papel na tese) |
|---|---|---|
| Dois corpos do rei | Ernst Kantorowicz | matriz jurídica da Purificação Clássica |
| Institution des images / juiz totêmico | Pierre Legendre | raiz da Feminilidade de Estado |
| Cultura jurídica | António M. Hespanha | enquadramento histórico-jurídico |
| Contrato sexual (não-visual) | Carole Pateman | **fonte**, não autoria do Contrato Sexual Visual |
| Economia icônica | Marie-José Mondzain | ed. 2002; fonte de "iconocracia" |
| Hystéra / poluição feminina | Anne Carson | raiz da Feminilidade de Estado |
| Visiocracia | Peter Goodrich | poder do visual no direito |

### Bloco 4 — Extensão ferramental
| Termo | `<AUTOR>` | Nota |
|---|---|---|
| Purificação / tradução | Bruno Latour | 1991; **ferramental**, não filiação |
| Ciborgue / fronteiras natureza-cultura | Donna Haraway | 1985; **nunca** rotular "ciberfeminismo" |
| Figuração / formas do visível | Philippe Descola | *Les Formes du visible*, 2021 |

### Bloco 5 — Alegorias femininas nacionais (use o prompt de alegorias)
`Marianne` · `La République` · `La Liberté` · `La Justice` (FR) · `Britannia` · `Justice`
· `Hibernia` (UK) · `Germania` · `Justitia` (DE) · `Columbia` · `Lady Liberty` (US) ·
`La Belgique` (BE) · `A República` · `A Justiça` (BR) · `Iustitia/Lady Justice` (genealogia romana).

---

## E · Como devolver ao glossário

1. Exporte a tabela do Elicit (CSV).
2. Para cada linha aprovada, escreva o verbete em `tese/manuscrito/Glossario.md` na seção
   correspondente, usando `definicao_curta` + `uso_juridico_iconografico`.
3. Adicione a `referencia_abnt` à seção Referências e crie a chave no
   `vault/tese/references.bib` (`@autorANO`).
4. Marque `#verificar` onde `confianca_flags` ≠ alta.
5. Me mande o CSV (ou cole as linhas) que eu integro ao glossário e ao `.bib`.

> [!note] Pilotos prioritários
> Comece pelos verbetes hoje marcados `#verificar` no glossário: **Carson/hystéra**
> (achar *Men in the Off Hours*, 2000) e **Resnik & Curtis, Representing Justice** (2011),
> que ainda não têm chave no `.bib`.
