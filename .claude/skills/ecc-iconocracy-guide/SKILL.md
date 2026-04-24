# ECC Skills — Guia de Uso para ICONOCRACY

Mapeamento entre tarefas do projeto ICONOCRACY e skills ECC instaladas em `~/.claude/skills/`.

## Skills mais relevantes para a tese

| Tarefa ICONOCRACY | Skill ECC | Quando usar |
|---|---|---|
| Pesquisa bibliográfica profunda | `deep-research`, `exa-search` | Revisão de literatura, buscar artigos e fontes |
| Redação de capítulos | `article-writing`, `brand-voice` | Escrever em voz acadêmica consistente |
| Revisão de qualidade | `verification-loop`, `eval-harness` | Validar coerência e completude de seções |
| Segurança de dados | `security-review` | Proteger dados do corpus e credenciais |
| Gerenciar contexto longo | `strategic-compact` | Sessões longas de análise ou escrita |
| Pesquisa de mercado/landscape | `market-research` | Mapear campo acadêmico, encontrar lacunas |
| Scripts Python do corpus | `coding-standards` | Manter qualidade dos 26 scripts em `tools/scripts/` |
| Buscar docs de bibliotecas | `documentation-lookup` | Referência rápida para pandas, jsonschema, etc. |
| Pesquisa antes de codificar | `search-first` | Verificar se já existe ferramenta antes de criar |

## Skills secundárias (úteis ocasionalmente)

| Skill | Quando |
|---|---|
| `frontend-design`, `frontend-patterns` | Ajustes no webiconocracy (React+Vite) |
| `api-design` | Se precisar de API para o corpus |
| `mcp-server-patterns` | Para o Gallica MCP server em `indexing/` |
| `product-capability` | Planejar features do corpus explorer |
| `claude-api` | Automações com a API da Anthropic |

## Skills que provavelmente não serão usadas

Estas vieram no pacote core mas são mais relevantes para projetos de engenharia de software: `backend-patterns`, `bun-runtime`, `nextjs-turbopack`, `e2e-testing`, `tdd-workflow`, `investor-materials`, `investor-outreach`, `crosspost`, `x-api`, `fal-ai-media`, `video-editing`, `dmux-workflows`, `agent-sort`.

Elas não atrapalham — simplesmente não serão ativadas se não houver trigger relevante.
