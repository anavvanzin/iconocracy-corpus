---
name: ecc-iconocracy-guide
description: >
  Mapa de tarefas da tese ICONOCRACIA para as skills, modos do agente, comandos ECC
  e ferramentas MCP realmente disponíveis neste repositório. Use quando o usuário
  pedir "qual skill uso para X", "que ferramentas tenho", "guia ecc", "como faço Y na tese",
  ou estiver em dúvida sobre qual entrada acionar.
user-invocable: true
---

# Guia de Ferramentas — Tese ICONOCRACIA

Mapeia tarefas do projeto para o que está **de fato instalado e acionável** neste repositório.
Três camadas de escolha (priorizadas) + duas seções transversais (modos do agente, descoberta):

1. **Skills sob medida da tese** — vivem em `.claude/skills/` (projeto). São a primeira escolha.
2. **Plugin ECC** — `everything-claude-code` v1.10.0, instalado em escopo **usuário** (`~/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.10.0/`). Os comandos do plugin não vivem em `.claude/commands/` deste repo (essa pasta está vazia). Audite com `cat ~/.claude/plugins/marketplaces/everything-claude-code/.claude-plugin/plugin.json`.
3. **Ferramentas MCP** — Context7 (docs de bibliotecas), Exa (busca web), Firecrawl (busca web ativa, recomendada pelo CLAUDE.md global), scite (literatura — em setup).

> O agente também despacha por **palavras-gatilho** (modo routing do `CLAUDE.md`), que muitas vezes
> é o caminho mais direto — não precisa nomear a skill.

## 1. Skills sob medida da tese (prioridade)

| Tarefa | Skill | Gatilhos |
|---|---|---|
| Compilar a tese (DOCX/PDF) | `compilar-tese` | "compilar", "make tese", "gerar PDF" |
| Sincronizar corpus / validar schema | `sync-corpus` | "sync vault", "validar corpus", drift entre `records.jsonl` ↔ `corpus-data.json` |
| Deduplicar candidatos novos | `scout-dedupe` | "dedupe", "possível duplicata", após uma campanha SCOUT |
| Checar SSD / symlinks / ingest **(Linux-only)** | `ssd-health` | "ssd", "mount check", "ingest drive", "backup iconocracia" |
| Citações ABNT (pré-commit) | `abnt-precommit` | "checar ABNT", antes de fechar capítulo |
| Gestão de referências Zotero | `zotero-cite` | "citar", "zotero", inserir referência |
| Gate de release público | `release-gate` | "release", "publicar corpus", antes de exportar para HF |
| Fallback de download de arquivos | `archive-fallback` | invocada pelo modo SCOUT quando uma fonte falha |
| Conserto de pipeline Pandoc | `pandoc-fix` | erro de compilação Pandoc/LaTeX |

> Para o **umbrella** user-level que orquestra estes branches em modo agente, ver `iconocracy-agent` em `~/.claude/skills/` — descrita no `CLAUDE.md` do hub como "default umbrella" e não duplicada aqui porque vive fora do projeto.

## 2. Modos do agente (CLAUDE.md mode routing)

São o despacho primário da tese. Basta usar o gatilho:

| Gatilho | Modo | O que faz |
|---|---|---|
| `scout`, `campanha N`, `buscar`, `lacunas` | SCOUT | Busca em arquivos digitais, gera nota Obsidian, análise de lacunas |
| `argos`, `orquestrar aquisicao` | ARGOS | Monta manifesto e grupos de aquisição |
| `codificar`, `iconocode`, imagem recebida | ICONOCODE | Panofsky 3 níveis + 10 indicadores de endurecimento |
| `validar [arquivo]` | VALIDAR | Validação de schema JSON |
| `purificacao status/lote` | PURIFICAÇÃO | Codificação de endurecimento |
| `pesquisar`, `revisão de literatura` | PESQUISAR | Pesquisa acadêmica profunda |
| `redigir`, `escrever capítulo` | REDIGIR | Redação acadêmica |
| `revisar`, `peer review` | REVISAR | Revisão multi-perspectiva |
| `zwischenraum`, `painel comparativo` | ZWISCHENRAUM | Painéis comparativos warburguianos |

## 3. Comandos ECC de engenharia

Slash-commands genéricos do plugin `everything-claude-code`. **Não** são wrappers dos ~69 scripts em `tools/scripts/` — para esses, rode `python tools/scripts/<nome>.py` direto.

| Tarefa | Comando |
|---|---|
| Revisão de código Python | `/python-review`, `/code-review` |
| Varredura da config Claude (`.claude/`, settings, hooks, MCP) | `/security-scan` |
| Cobertura / qualidade de testes | `/test-coverage`, `/quality-gate` |
| Limpeza de código morto | `/refactor-clean` |
| Conserto de build | `/build-fix` |
| Atualizar documentação/codemaps | `/update-docs`, `/update-codemaps` |
| Planejar feature/refactor | `/plan`, `/feature-dev` |
| Escolher tier de modelo | `/model-route` |

## 4. Ferramentas MCP de pesquisa

| Tarefa | Ferramenta MCP | Estado |
|---|---|---|
| Busca web primária (extração de página, search com filtros) | **Firecrawl** (`mcp__firecrawl__firecrawl_search`, `_scrape`, `_extract`) | ativo |
| Docs atualizadas de bibliotecas (pandas, jsonschema, etc.) | **Context7** (`resolve-library-id` → `query-docs`) | ativo |
| Busca web acadêmica complementar | **Exa** (`web_search_exa`, `web_fetch_exa`) | ativo |
| Verificar afirmações, Smart Citations | **scite** | **em setup** — falta configurar MCP (`grep scite ~/.claude/settings.json` → 0 hits) |

## 5. Descoberta

- `/find-skill` — procurar uma skill por funcionalidade.
- `ls ~/.claude/plugins/cache/everything-claude-code/everything-claude-code/1.10.0/commands/` — lista os slash-commands do plugin instalados hoje.
- `cat ~/.claude/plugins/marketplaces/everything-claude-code/.claude-plugin/plugin.json` — audita versão atual do plugin antes de seguir este guia.
- O catálogo de skills do plugin (`deep-research`, `article-writing`, `eval-harness`,
  `verification-loop`, `strategic-compact`, `market-research`, …) é maior que o conjunto de slash-commands; muitas só são invocáveis via o tool `Skill`. Confirme com `/find-skill` antes de depender de uma delas.

> **Host:** macOS primário (`/Users/ana/...`, conda env `iconocracy` em `/opt/homebrew/Caskroom/miniforge/base/envs/`). Linux secundário em outra máquina via SSD (`/home/ana`, `/media/ana/SSD_DATA`) — usado para ingest e operações de SSD. Skills marcadas **Linux-only** (ex.: `ssd-health`) não rodam em sessões macOS.
