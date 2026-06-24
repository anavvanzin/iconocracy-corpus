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
Três camadas:

1. **Skills sob medida da tese** — vivem em `.claude/skills/` (projeto). São a primeira escolha.
2. **Plugin ECC** (`ecc` v2.0.0-rc.1) — comandos de engenharia em `.claude/commands/` e catálogo de skills em `.claude/skills/ecc/`.
3. **Ferramentas MCP** — scite (literatura), Context7 (docs de bibliotecas), Exa (busca web).

> O agente também despacha por **palavras-gatilho** (modo routing do `CLAUDE.md`), que muitas vezes
> é o caminho mais direto — não precisa nomear a skill.

## 1. Skills sob medida da tese (prioridade)

| Tarefa | Skill | Gatilhos |
|---|---|---|
| Compilar a tese (DOCX/PDF) | `compilar-tese` | "compilar", "make tese", "gerar PDF" |
| Sincronizar corpus / validar schema | `sync-corpus` | "sync vault", "validar corpus", drift entre `records.jsonl` ↔ `corpus-data.json` |
| Deduplicar candidatos novos | `scout-dedupe` | "dedupe", "possível duplicata", após uma campanha SCOUT |
| Checar SSD / symlinks / ingest | `ssd-health` | "ssd", "mount check", "ingest drive", "backup iconocracia" |
| Citações ABNT (pré-commit) | `abnt-precommit` | "checar ABNT", antes de fechar capítulo |
| Gestão de referências Zotero | `zotero-cite` | "citar", "zotero", inserir referência |
| Gate de release público | `release-gate` | "release", "publicar corpus", antes de exportar para HF |
| Fallback de download de arquivos | `archive-fallback` | invocada pelo modo SCOUT quando uma fonte falha |
| Conserto de pipeline Pandoc | `pandoc-fix` | erro de compilação Pandoc/LaTeX |

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

## 3. Comandos ECC de engenharia (para os ~69 scripts em `tools/scripts/`)

Acionáveis como slash-commands do plugin `ecc`:

| Tarefa | Comando |
|---|---|
| Revisão de código Python | `/python-review`, `/code-review` |
| Varredura de segurança | `/security-scan` |
| Cobertura / qualidade de testes | `/test-coverage`, `/quality-gate` |
| Limpeza de código morto | `/refactor-clean` |
| Conserto de build | `/build-fix` |
| Atualizar documentação/codemaps | `/update-docs`, `/update-codemaps` |
| Planejar feature/refactor | `/plan`, `/feature-dev` |
| Escolher tier de modelo | `/model-route` |

## 4. Ferramentas MCP de pesquisa

| Tarefa | Ferramenta MCP |
|---|---|
| Verificar afirmações, achar artigos com Smart Citations | **scite** (`search_literature`, `search_grants`) |
| Docs atualizadas de bibliotecas (pandas, jsonschema, etc.) | **Context7** (`resolve-library-id` → `query-docs`) |
| Busca web ampla / descoberta | **Exa** (`web_search_exa`, `web_fetch_exa`) |

## 5. Descoberta

- `/find-skills` — procurar uma skill por funcionalidade.
- `/ecc-guide` — navegar agentes, skills, comandos e hooks do plugin ECC ao vivo.
- O catálogo completo `.claude/skills/ecc/` (`deep-research`, `article-writing`, `eval-harness`,
  `verification-loop`, `strategic-compact`, `market-research`, `scientific-thinking-literature-review`…)
  existe no disco; nem toda entrada aparece como slash-command. Confirme a disponibilidade real
  com `/find-skills` ou `/ecc-guide` antes de depender de uma delas.

> **Host:** Linux (`/home/ana`, SSD em `/media/ana/SSD_DATA`). Caminhos `/Users/...` e `/Volumes/...`
> em docs antigas são da era Mac e estão obsoletos.
