# Revisão aprofundada — ICONOCRACIA weekly corpus gate

- **Data:** 2026-09-24T12:06:22Z
- **Objeto:** execução semanal em `/Users/ana/Research/hub/iconocracy-corpus`
- **Confiança:** alta para estado local, GitHub e Supabase; média para a classificação normativa do gate
- **Método:** comandos locais, GitHub API, pesquisa oficial no GitHub, Supabase read-only e Context7

## Resumo executivo

A execução anterior foi mecanicamente correta: todos os comandos pedidos foram executados no checkout real, o repositório não foi alterado e `check_thesis_terms.py` retornou `1`. Sob o contrato estrito da automação, o rótulo geral **Failed** é defensável.

A interpretação, porém, precisa de precisão. Das três ocorrências de `hardening`, duas (linhas 46 e 318) explicam por que a tradução é recusada e satisfazem o caso de exceção documentado pelo próprio script; uma (linha 197, `iconographic hardening`) é uso substantivo incompatível com a terminologia canônica. Há ainda conflito de governança: `CLAUDE.md` chama a checagem de referência não bloqueante durante rascunhos, enquanto `tools/scripts/check_thesis_terms.py`, povoado em 2026-09-22, declara os termos sempre errados e exige o gate antes de commits.

O estado mais fiel é, portanto:

- **Gate mecânico:** Failed, porque um comando obrigatório saiu com código 1.
- **Integridade do corpus:** OK — 337/337 registros válidos e projeção 337/337 sincronizada.
- **Pesquisa/codificação:** Attention — 286/337 codificados, 51 pendentes e zero itens de arquitetura forense.
- **Terminologia:** Attention com um uso substantivo e duas ocorrências explicativas passíveis de exceção.
- **Git:** Attention — branch local sem upstream, 26 commits à frente de `main` e árvore suja.

## Cronologia verificada

| Data | Evidência | Efeito |
|---|---|---|
| 2026-06-23 | Commit `6f87b6f` desabilita restrições terminológicas | Origina a política não bloqueante ainda registrada em `CLAUDE.md`. |
| 2026-09-22 | Commit `043a1d7` repovoa `check_thesis_terms.py` | O script passa a dizer “always-wrong” e “run before every commit”. |
| 2026-09-22 | `origin/main` chega a `988e507` | GitHub e referência local coincidem neste SHA. |
| 2026-09-24 | Gate semanal | Todos os checks de corpus passam; terminologia sai com código 1. |

## Revisão do gate semanal

### O que foi executado corretamente

- O checkout canônico foi resolvido antes do julgamento.
- O interpretador exigido existia e foi usado: Python 3.12.14.
- Todos os oito comandos definidos pela automação foram tentados.
- Divergência, sujeira, esquema, purificação, vault, projeção e terminologia foram separados.
- Nenhum arquivo do repositório foi editado na execução do gate.

### Achados que exigem reclassificação cuidadosa

1. **Terminologia:** o comando falha de fato, mas o resumo “três violações” seria excessivo. As linhas 46 e 318 discutem a regra e se enquadram na exceção `<!-- termos-ok -->`; a linha 197 usa a tradução na argumentação e é o achado substantivo.
2. **Política conflitante:** `CLAUDE.md:119-121` diz que a checagem não é guardrail de rascunho; `check_thesis_terms.py:2-11` afirma o contrário. A automação pediu expressamente a execução, mas não resolve qual documento governa a severidade.
3. **Vault:** `vault_sync.py status` retornou contagens e código 0; ele não demonstrou, sozinho, uma equivalência 1:1 entre 337 registros e 411 notas. O resultado deve permanecer como status informativo, não como prova de rastreabilidade completa.
4. **Git remoto:** a GitHub API confirmou `main` em `988e507`; a branch `docs/auditoria-inferencial-2026-09-22` não existe no remoto. Assim, 26 à frente/0 atrás é confirmado, mas descreve trabalho exclusivamente local.

## GitHub — investigação em quatro rodadas

### Rodada 1 — repositório e documentação oficial

O repositório `anavvanzin/iconocracy-corpus` é público e usa `main`. O README remoto ainda apresenta 335 registros, “defense 2026” e a tradução “hardening”, enquanto o checkout validado tem 337 registros e política terminológica mais recente.

### Rodada 2 — descoberta

A busca oficial encontrou a mesma política não bloqueante em `CLAUDE.md` no `main`, confirmando que a divergência não é apenas local.

### Rodada 3 — PRs, issues e evolução

- PR #222 consolidou a sanitização que forma o `main` atual.
- PR #221 removeu gitlinks órfãos, mas o checkout corrente ainda mostra `AutoResearchClaw` sujo porque a branch local contém história anterior/divergente.
- PR #208, ainda aberto, propõe corrigir contagens, cronologia e licenças do README; por isso o README público atual não deve ser tratado como fotografia canônica.
- PR #210 permanece aberto para harmonização de suportes antes da amostragem.

### Rodada 4 — histórico e branch

O `origin/main` local e o GitHub apontam para `988e507`. O `HEAD` local é `2d51871`, sem upstream, com 26 commits exclusivos. A branch não foi encontrada no GitHub.

## Supabase

O projeto `gcuxtaohtoomweyrgpgk` (`ICONOCRACIA 1.0`) está `ACTIVE_HEALTHY`. A consulta live confirmou:

| Relação | Linhas | RLS |
|---|---:|---|
| `public.corpus_items` | 335 | habilitada; leitura para `anon`/`authenticated` |
| `public.lab_owners` | 1 | habilitada; leitura do próprio owner |
| `public.lab_investigations` | 2 | habilitada; owner autenticado |
| `public.lab_investigation_revisions` | 2 | habilitada; owner autenticado |

Os 335 itens são um freeze documentado, não drift contra o ledger operacional de 337. O advisor de segurança encontrou três avisos:

- `public.rls_auto_enable()` é `SECURITY DEFINER` e executável por `PUBLIC`, `anon` e `authenticated`.
- Proteção contra senhas vazadas está desabilitada.
- Quatro índices de `corpus_items` aparecem sem uso; são avisos informativos de performance, não autorização para removê-los.

As orientações atuais do Supabase confirmam o princípio de menor privilégio: RLS deve anteceder grants e funções `SECURITY DEFINER` não destinadas ao público devem ter `EXECUTE` revogado de `PUBLIC`, `anon` e `authenticated`.

## Remotion e plugins auxiliares

Não existe projeto Remotion ativo no checkout. As ocorrências são documentação de uma skill genérica de edição de vídeo; o router `remotion-best-practices` não manda carregar criação, markup, renderização ou Studio para esta tarefa.

Education Agent Skills e Tool Advisor não expuseram ferramentas ou workflows chamáveis nesta sessão e não eram necessários para validar o gate.

## Repo Audit Report — iconocracy-corpus

Generated: 2026-09-24T12:06:22Z

Session Config commands: test=`npm test` typecheck=`npm run typecheck` lint=`npm run lint` (defaults do plugin; inadequados ao monorepo Python)

| Categoria | Pass | Fail | Warn | Skipped |
|---|---:|---:|---:|---:|
| 1. Configuration | 1 | 3 | 1 | 0 |
| 2. Code Quality | 1 | 2 | 0 | 3 |
| 3. Git Hygiene | 0 | 3 | 1 | 0 |
| 4. CI/CD | 4 | 0 | 0 | 1 |
| 5. Testing | 0 | 1 | 1 | 3 |
| 6. Security | 3 | 1 | 3 | 2 |
| 7. Documentation | 2 | 1 | 0 | 0 |
| 8. Clank Integration | 0 | 0 | 0 | 4 |
| 9. MCP Configuration | 0 | 1 | 0 | 3 |
| **Total** | **11** | **12** | **6** | **16** |

**Overall:** FAIL contra o baseline genérico do Session Orchestrator.

### Leitura proporcional ao projeto

- `CLAUDE.md` existe, mas tem 289 linhas, acima do baseline de 50–100.
- `.claude/settings.json` existe; `.claude/rules/` e `.mcp.json` não existem no repo.
- `.gitignore` cobre `.env`, `node_modules`, `build` e `dist`, mas não cobre `.env.local`/`.env*`.
- Não há `package.json` raiz; por isso os três defaults npm falham com `ENOENT`.
- O teste canônico, com o ambiente ativado, passa: **429 passed, 2 xfailed**.
- Ruff está configurado em `pyproject.toml`, mas não está instalado no ambiente `iconocracy`.
- O CI cobre validação de esquemas, consistência, idempotência, rastreabilidade, testes, terminologia, CodeQL, dependency review e deploy.
- Não há Husky/lint-staged, commitlint ou Gitleaks configurados.
- Nenhum token de alto sinal foi encontrado nos arquivos rastreados ou em `.claude/settings*.json`.
- Não há `.env.example` raiz.
- Clank não foi detectado e foi corretamente marcado como `skipped`.
- `mcporter` não está instalado; o probe MCP foi ignorado.

## Achados críticos

1. A configuração do Session Orchestrator não conhece os comandos reais do projeto e produz falhas npm artificiais.
2. A política terminológica está contraditória entre `CLAUDE.md` e o script/AGENTS mais recentes.
3. Há um uso substantivo de `hardening` no artigo inglês; duas ocorrências são explicativas.
4. `.env.local` não é ignorado e não existe `.env.example` raiz.
5. Ruff é configurado, mas ausente no ambiente declarado.
6. `public.rls_auto_enable()` expõe execução privilegiada a papéis públicos no Supabase.
7. O README público está defasado em relação ao corpus e à terminologia atuais.

## Ações recomendadas

1. Resolver a autoridade entre `CLAUDE.md` e o guard terminológico; só então decidir se a automação deve classificar esse check como `Failed` ou `Attention`.
2. Tratar a linha 197 como achado substantivo e as linhas 46/318 conforme a exceção já documentada no script.
3. Se o Session Orchestrator continuar em uso, registrar comandos Python em `.orchestrator/policy/quality-gates.json` e marcar typecheck Node como `skip`.
4. Restringir `EXECUTE` de `public.rls_auto_enable()` aos papéis realmente necessários e revisar a proteção de senhas vazadas.
5. Decidir o destino do PR #208 ou atualizar o README público por outra via canônica.

## Fontes

- GitHub: <https://github.com/anavvanzin/iconocracy-corpus>
- README atual: <https://github.com/anavvanzin/iconocracy-corpus/blob/main/README.md>
- CLAUDE atual: <https://github.com/anavvanzin/iconocracy-corpus/blob/main/CLAUDE.md>
- PR #208: <https://github.com/anavvanzin/iconocracy-corpus/pull/208>
- PR #221: <https://github.com/anavvanzin/iconocracy-corpus/pull/221>
- PR #222: <https://github.com/anavvanzin/iconocracy-corpus/pull/222>
- Repo-audit v5.3.0: <https://github.com/Kanevry/session-orchestrator/blob/v5.3.0/skills/repo-audit/SKILL.md>
- Supabase advisor: <https://supabase.com/docs/guides/database/database-linter?lint=0028_anon_security_definer_function_executable>

## Confiança

- **Alta:** resultados locais, contagens, testes, SHAs, branch remota, políticas RLS e advisors Supabase.
- **Média:** severidade normativa do gate terminológico, porque as fontes internas estão em conflito.
- **Baixa:** nenhuma afirmação central depende de fonte social, opinião ou inferência externa.
