---
id: P-2026-002
titulo: Auth gh CLI — howto
llm_alvo: claude
lingua: pt
dominio: meta
versao: "1.0"
criado: 2026-04-17
ultimo_uso: 2026-04-17
output_ref:
tags: [migrado-de-notas]
fonte: "Notas e Textos/# Authenticate gk auth login # Navigate to a git.md"
---

# Auth gh CLI — howto

## Prompt

```
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Authenticate gk auth login  \# Navigate to a git repo directory on your filesystem cd ./path/to/repo  \# Then create a Work Item and the current directory \# will be automatically added to the Work Item gk work create "My new work item"  \# Edit files... \# ...  \# Commit your changes using AI gk work commit --ai  \# Push your changes gk work push  \# Create a Pull Request gk work pr create --ai

Esse trecho que você colou é, na prática, um mini–tutorial de fluxo de trabalho com o GitKraken CLI (`gk`) para trabalhar em um repositório Git com “Work Items” e commits/PRs assistidos por IA.[^1_5]

Vou reescrever em passos claros e explicar o que cada comando faz:

## Visão geral

A sequência propõe este fluxo:

1. Autenticar o GitKraken CLI na sua conta.
2. Entrar no diretório de um repositório Git local.
3. Criar um “Work Item” associado a esse diretório.
4. Editar arquivos normalmente.
5. Fazer commit usando sugestão de IA.
6. Fazer push das alterações.
7. Criar um Pull Request com ajuda de IA.[^1_8][^1_10][^1_5]

## Passo a passo explicado

### 1. Autenticar

```bash
gk auth login
```

- Abre o fluxo de autenticação do GitKraken CLI na sua conta GitKraken (e, por consequência, nos provedores conectados, como GitHub, GitLab etc.).[^1_2][^1_5]
- Normalmente ele abre o navegador para você autorizar o CLI.


### 2. Ir para o repositório

```bash
cd ./path/to/repo
```

- Navega até o diretório do repositório Git em que você quer trabalhar.
- É importante estar dentro de um repositório Git inicializado (`.git` presente).[^1_5][^1_8]


### 3. Criar um Work Item

```bash
gk work create "My new work item"
```

- Cria um “Work Item” no GitKraken com esse título.
- O diretório atual (seu repo) é automaticamente associado a esse Work Item, o que permite ao GitKraken acompanhar o contexto de trabalho, branches, commits etc.[^1_12][^1_14][^1_5]


### 4. Editar arquivos

```bash
# Edit files...
# ...
```

- Aqui você edita o código normalmente, com seu editor/IDE preferido.
- Git funciona como sempre: você altera, adiciona, remove arquivos.


### 5. Commit com IA

```bash
gk work commit --ai
```

- Cria um commit relacionado ao Work Item atual.
- A flag `--ai` pede ao GitKraken que gere automaticamente a mensagem de commit usando IA com base nas alterações feitas.[^1_10][^1_14][^1_8]
- Você pode revisar/ajustar a mensagem antes de confirmar, dependendo da configuração do CLI.


### 6. Enviar alterações (push)

```bash
gk work push
```

- Faz push das alterações (commits) para o repositório remoto associado ao Work Item.[^1_8][^1_5]
- Em geral, está ligado à branch que o Work Item está usando.


### 7. Criar Pull Request com IA

```bash
gk work pr create --ai
```

- Cria um Pull Request (em GitHub, GitLab etc., conforme o seu provedor) a partir da branch do Work Item.[^1_14][^1_10][^1_5]
- A flag `--ai` gera título e descrição do PR com IA, com base no diff. Você pode revisar antes de concluir.


## Tabela-resumo dos comandos

| Comando | Função principal |
| :-- | :-- |
| `gk auth login` | Autenticar o GitKraken CLI na sua conta |
| `cd ./path/to/repo` | Entrar no diretório do repositório Git |
| `gk work create "..."` | Criar Work Item ligado ao repo atual |
| `gk work commit --ai` | Commit com mensagem gerada por IA |
| `gk work push` | Enviar commits para o remoto do Work Item |
| `gk work pr create --ai` | Criar Pull Request com título/descrição gerados por IA |

Você quer que eu transforme esse fluxo em um pequeno script ou snippet de documentação comentada para você colar no seu repositório (por exemplo, em `CONTRIBUTING.md` ou num template de README)?
<span style="display:none">[^1_1][^1_11][^1_13][^1_15][^1_3][^1_4][^1_6][^1_7][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://cli.github.com/manual/gh_auth_login

[^1_2]: https://help.gitkraken.com/cli/cli-home/

[^1_3]: https://gitkraken.github.io/gk-cli/docs/gk_provider_list.html

[^1_4]: https://stackoverflow.com/questions/78890002/how-to-do-gh-auth-login-when-run-in-headless-mode

[^1_5]: https://github.com/gitkraken/gk-cli

[^1_6]: https://github.com/gitkraken/gk-cli/blob/main/README.md

[^1_7]: https://mcpservers.org/servers/gitkraken/gk-cli

[^1_8]: https://libraries.io/npm/@gitkraken%2Fgk

[^1_9]: https://docs.cloud.google.com/sdk/gcloud/reference/auth/login

[^1_10]: https://www.mdskills.ai/skills/gk-cli

[^1_11]: https://cloud.google.com/kubernetes-engine/enterprise/identity/accessing

[^1_12]: https://almc.es/en/mcpserver/version-control/gitkraken

[^1_13]: https://www.youtube.com/watch?v=r_T2EQUTaK0

[^1_14]: https://eliteai.tools/mcp/gitkraken-gk-cli

[^1_15]: https://www.reddit.com/r/googlecloud/comments/1dsgx53/after_using_gcloud_command_line_should_i_log_out/
```
