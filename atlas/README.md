# Atlas — Knowledge Graph ICONOCRACIA

Camada de **mapa de conhecimento navegável** sobre o monorepo da tese
*ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)*.

> [!warning] Não confundir com o *Atlas Iconográfico*
> Esta pasta `atlas/` é o **grafo de conhecimento do repositório** (meta-camada
> de navegação). É distinta do conceito warburguiano **Atlas Iconográfico**
> (leitura do corpus como atlas mnemônico), documentado em
> [concepts/atlas-iconografico.md](../concepts/atlas-iconografico.md).

Estas notas **não duplicam** o conteúdo do repositório — elas **interligam** o
material que já existe disperso (conceitos, ADRs, esquemas JSON, capítulos,
pipeline, dados) em um único grafo consultável. Cada nó é um arquivo Markdown em
[Obsidian Flavored Markdown](<../vault/meta/Guia — Obsidian Flavored Markdown.md>)
com frontmatter padronizado, `[[wikilinks]]` para outros nós do grafo e links
Markdown relativos (`../`) para os arquivos-fonte reais.

> [!info] Ponto de entrada
> Abra **[[Iconocracia — Mapa Central]]**. É o hub que conecta todos os MOCs
> (Maps of Content) temáticos.

## Como abrir como vault

Esta pasta foi pensada para ser aberta diretamente no Obsidian:

```
Obsidian → Open folder as vault → iconocracy-corpus/knowledge-graph/
```

Os `[[wikilinks]]` resolvem entre os nós do grafo (estrutura plana, sem
subpastas). Os links para fontes fora do grafo (`../docs/...`, `../tools/...`,
`../tese/...`, `../concepts/...`) são links Markdown relativos — clicáveis tanto
no Obsidian quanto no GitHub.

## Convenção de frontmatter (para consultas Dataview)

Todo nó abre com:

```yaml
---
title: Nome do nó
aliases: []
type: kg/conceito        # kg/hub | kg/moc | kg/conceito | kg/pipeline | kg/dado | kg/esquema | kg/decisao | kg/manuscrito | kg/stub
tags:
  - kg
  - projeto/iconocracia
related:
  - "[[Outro nó]]"
sources:
  - ../docs/adr/003-jsonl-as-canonical.md
status: ativo
created: 2026-06-19
updated: 2026-06-19
---
```

Isso torna o grafo consultável. Exemplos (requer plugin **Dataview**):

````markdown
```dataview
LIST FROM #kg WHERE type = "kg/conceito" SORT file.name ASC
```
````

````markdown
```dataview
TABLE related, sources FROM #kg WHERE type = "kg/pipeline"
```
````

## Mapa dos MOCs

| MOC | Cobre |
| --- | --- |
| [[Iconocracia — Mapa Central]] | hub raiz: liga tudo |
| [[Conceitos — MOC]] | os 4 conceitos autorais + Warburg + regimes |
| [[Pipeline Dual-Agente — MOC]] | WebScout → IconoCode → ARGOS |
| [[Hierarquia de Dados — MOC]] | records.jsonl → corpus-data.json → purification → vault |
| [[ADRs e Decisões — MOC]] | 6 ADRs + decisões metodológicas |
| [[Manuscrito — MOC]] | capítulos e estado da redação |
| [[Stubs — Índice]] | stubs auto-gerados (cobertura exaustiva; contagem no índice) |

## Espinha curada vs. stubs gerados

O grafo tem **duas camadas**:

1. **Espinha** (escrita à mão, em `atlas/*.md`) — leitura curada: hub, 5 MOCs e
   os nós conceituais/pipeline/dados. É aqui que mora a interpretação.
2. **Stubs** (gerados, em `atlas/stubs/<categoria>/`) — um nó por arquivo-fonte
   (ADRs, decisões, esquemas, capítulos, conceitos, docs, notebooks), cada um com
   resumo-âncora + link para a fonte + backlink ao MOC. Dão **cobertura
   exaustiva** sem duplicar conteúdo.

```bash
python atlas/_generate_stubs.py   # regenera atlas/stubs/ por inteiro (idempotente)
```

> [!warning] Stubs são descartáveis
> Nunca edite `atlas/stubs/**` à mão — é regenerado. Para mudar o conteúdo,
> edite o arquivo-fonte; para mudar a estrutura/cobertura, edite o gerador
> (`SURFACES` em `_generate_stubs.py`).

## Regras de manutenção

- **Fonte da verdade permanece nos arquivos originais.** Os nós resumem e
  apontam; não substituem `docs/`, `tools/schemas/`, `tese/manuscrito/`.
- Terminologia obrigatória segue [`../CLAUDE.md`](../CLAUDE.md) §*Mandatory
  Terminology* (Endurecimento, Purificação Clássica, etc.).
- **Contagens não são fixadas neste grafo** — derivam a cada sync. Para o estado
  atual, ver [`../CLAUDE.md`](../CLAUDE.md) §*Known Data Issues* e
  `python tools/scripts/validate_schemas.py` / `records_to_corpus.py --diff`.
- Voz acadêmica: português formal, enquadramento jurídico em diálogo com antropologia e sociologia.
