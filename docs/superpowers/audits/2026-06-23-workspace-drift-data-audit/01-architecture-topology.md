# Audit Report — arquitetura/topologia/drift de workspace — lente de agente de governança
Escopo examinado: `/Users/ana/Research/AGENTS.md`; `/Users/ana/Research/CLAUDE.md`; `/Users/ana/Research/README.md`; `/Users/ana/Research/iconocracy-corpus` (symlink); `/Users/ana/Research/iconocracia-companion` (symlink); `/Users/ana/Research/hub/iconocracy-corpus`; `/Users/ana/Research/hub/iconocracy-corpus/AGENTS.md`; `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md`; `git worktree list` de `/Users/ana/Research/hub/iconocracy-corpus`; worktrees Claude/Codex/Copilot listados, sem varredura profunda de conteúdo.
Arquivos analisados: 8
Data: 2026-06-23

## Resumo executivo (≤5 linhas)

A fonte operacional medida é `/Users/ana/Research/hub/iconocracy-corpus`, não o symlink raiz `/Users/ana/Research/iconocracy-corpus`.
Há drift bloqueante entre documentos de governança: `hub/iconocracy-corpus/CLAUDE.md` ainda declara 278/234, enquanto os ledgers medidos e `AGENTS.md` local estão em 280/280/236.
A raiz `/Users/ana/Research` está corretamente descrita como meta-workspace, mas `CLAUDE.md`/`README.md` preservam contagens 264/265 e caminhos antigos.
O workspace tem 13 worktrees ativos (Codex, Copilot, Claude e PR fix), incluindo worktrees dentro do próprio repo canônico, o que exige exclusão mental/operacional de globbing amplo.
Riscos principais: symlink externo quebrado para `/Volumes/data`, path case drift em `/users/ana`, referências `~/Documents/...` e self-symlinks recursivos.

## Achados — CRITICAL (bloqueante)
- [C-01] Symlink raiz da tese aponta para destino externo inexistente · `/Users/ana/Research/iconocracy-corpus:symlink` · O atalho esperado por agentes resolve para `/Volumes/data/projetos/research/hub/iconocracy-corpus` e foi medido como `exists=False`, enquanto o repo canônico real existe em `/Users/ana/Research/hub/iconocracy-corpus`; isso cria risco alto de agentes alternarem entre path inexistente, mount externo e fonte correta. · Remediar removendo o symlink quebrado ou retargetando-o explicitamente para `/Users/ana/Research/hub/iconocracy-corpus`; até lá, instruir agentes a nunca usar `/Users/ana/Research/iconocracy-corpus` como fonte de verdade.
- [C-02] Documento autoritativo Claude do hub está stale frente ao estado medido · `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md:201` · `CLAUDE.md` declara `records.jsonl` = 278, `corpus-data.json` = 278 e `purification.jsonl` = 234 nas linhas 201–203, mas a medição read-only dos arquivos retornou 280, 280 e 236; `AGENTS.md` local já declara 280/280/236 nas linhas 7–9. Como sessões Claude leem este arquivo como governança primária, o drift pode propagar N incorreto para validação, release gate e escrita acadêmica. · Atualizar `CLAUDE.md` do hub para 280/280/236 ou substituir contagens fixas por comando de verificação; manter a distinção entre snapshot operacional e N analítico pendente.

## Achados — MAJOR
- [M-01] Governança da raiz preserva contagens antigas do corpus · `/Users/ana/Research/CLAUDE.md:47` · O `CLAUDE.md` da raiz ainda afirma `corpus-data.json` = 264 e `records.jsonl` = 265; o `README.md` repete 264 itens nas linhas 11 e 26. Isso conflita com o hub medido em 280/280 e com `/Users/ana/Research/hub/iconocracy-corpus/AGENTS.md:7`. · Remediar removendo contagens estáticas da raiz ou trocando por “consulte `hub/iconocracy-corpus/CLAUDE.md` + ledgers medidos”.
- [M-02] Parent-context paths em `CLAUDE.md` do hub apontam para layout antigo · `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md:12` · As linhas 12–13 apontam para `~/Documents/CLAUDE.md` e `~/Documents/projetos/research/CLAUDE.md`, mas o workspace auditado e a raiz real são `/Users/ana/Research`; isso é path drift herdado de migração e pode levar agentes a buscar governança fora do escopo atual. · Remediar substituindo por `/Users/ana/Research/CLAUDE.md` e, se necessário, documentar o histórico `~/Documents` apenas como legado não operacional.
- [M-03] Topologia de worktrees é densa e inclui árvores dentro do repo canônico · `/Users/ana/Research/hub/iconocracy-corpus/.git:worktrees` · Foram medidos 13 worktrees: 1 canônico, 3 Codex, 6 Copilot, 1 `iconocracy-corpus-pr85-fix` detached e 2 Claude sob `.claude/worktrees/`; essa distribuição aumenta risco de globbing amplo, cópias stale e edições no worktree errado. · Remediar com um mapa fixo “canônico vs worktree efêmero” em governança e com regra para não varrer `.codex/`, `copilot-worktrees/`, `hub/iconocracy-corpus-pr85-fix` nem `.claude/worktrees/` salvo tarefa explícita.
- [M-04] Identidade Git medida diverge do briefing de recon · `/Users/ana/Research/hub/iconocracy-corpus/.git:HEAD` · O briefing declarou branch `feat/codebook-master-v2.2.0` em `86e4cce`, mas a medição local retornou branch `feat/alegorias-piloto-v2`, HEAD `5f06c87`, mensagem `docs(thesis): write Section 4 (Comparative Matrix) of positivist freeze draft`; isso indica drift entre instrução operacional e checkout real. · Antes de qualquer remediação futura, confirmar com Ana se o audit deve seguir o checkout atual ou trocar para o branch pretendido; para agentes futuros, registrar o branch esperado no ticket da tarefa e validar `git branch --show-current`.
- [M-05] Symlink de app usa path com casing não canônico · `/Users/ana/Research/iconocracia-companion:symlink` · O symlink aponta para `/users/ana/Research/apps/iconocracia-companion`; em macOS isso resolveu, mas o path canônico observado é `/Users/ana/Research/apps/iconocracia-companion`, e o casing minúsculo cria fragilidade para ferramentas case-sensitive, logs e sincronização. · Remediar retargetando para `/Users/ana/Research/apps/iconocracia-companion` ou removendo o atalho se não for necessário.
- [M-06] Self-symlinks recursivos existem em subprojetos irmãos · `/Users/ana/Research/labs/iuris-visio-roadmap/iuris-visio-roadmap:symlink` · Foram medidos self-symlinks em `labs/iuris-visio-roadmap/iuris-visio-roadmap`, `apps/iconocracia-space/iconocracia-space` e `shared/iconclass-data/iconclass-data`, todos resolvendo para o próprio diretório pai; isso pode criar recursão em scripts ingênuos de backup, indexação ou contagem. · Remediar com exclusão explícita em inventários e, se forem legados acidentais, remover após confirmação do dono de cada repo.

## Achados — MINOR
- [m-01] Drift de ambiente Python entre documentos · `/Users/ana/Research/CLAUDE.md:82` · A raiz declara `iconocracy` como Python 3.12, o hub declara Python 3.11 em `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md:22`, e `/Users/ana/Research/AGENTS.md:102` já contém um exemplo `drift-pin` sobre 3.12 vs 3.11; é drift de ambiente, não de topologia, mas afeta comandos de validação. · Remediar fazendo a versão real vir de `environment.yml`/`python --version` e evitando número fixo em governança de alto nível.
- [m-02] Caminho de capítulos está divergente no `README.md` · `/Users/ana/Research/README.md:23` · O `README.md` ainda lista `vault/tese/` como “Capítulos da tese”, enquanto `/Users/ana/Research/CLAUDE.md:44` e `/Users/ana/Research/AGENTS.md:45` dizem que o lar canônico dos capítulos é `tese/manuscrito/`, com `vault/tese/` apenas para Makefile/pipeline. · Remediar alinhando o `README.md` à regra “texto em `tese/manuscrito/`; compilação em `vault/tese/`”.
- [m-03] `ROADMAP.md` é symlink relativo para documento datado · `/Users/ana/Research/hub/iconocracy-corpus/ROADMAP.md:symlink` · O symlink resolve corretamente para `docs/ROADMAP-2026-04-29.md`, mas a natureza datada pode ser confundida com roadmap vivo. · Remediar mantendo o symlink se ele for intencional, mas rotular no roadmap se é histórico, vigente ou índice.
- [m-04] Snapshot `Other/` está corretamente documentado como não fonte de verdade, mas é zona de confusão · `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md:209` · `CLAUDE.md` informa que `Other/corpus-data.json` tem 165 itens e duplica notebooks 01–08 como cópia stale; isso está documentado, porém continua sendo um ponto provável de drift se agentes lerem por globbing. · Remediar com exclusão explícita em tarefas de contagem/treino, preservando o snapshot até decisão de Ana sobre N analítico.

## Pontos fortes (o que NÃO mexer)
- `/Users/ana/Research/AGENTS.md:9` define corretamente a raiz como meta-workspace, não codebase/monorepo; essa distinção deve permanecer.
- `/Users/ana/Research/AGENTS.md:15` e `/Users/ana/Research/CLAUDE.md:80` impõem contenção de sub-repos e evitam `git add` acidental na raiz; manter.
- `/Users/ana/Research/AGENTS.md:44` roteia trabalho de tese para `hub/iconocracy-corpus/` e manda ler o `CLAUDE.md` do hub; a regra está correta, embora o `CLAUDE.md` precise atualização.
- `/Users/ana/Research/hub/iconocracy-corpus/CLAUDE.md:69` define a hierarquia conceitual correta: `records.jsonl` operacional, `corpus-data.json` export público, `purification.jsonl` ledger de endurecimento, `vault/candidatos/` espelho auxiliar.
- `/Users/ana/Research/hub/iconocracy-corpus/AGENTS.md:66` proíbe edição manual de `corpus/corpus-data.json`; manter a regra de export via scripts.

## Métricas mensuradas
- arquivos de governança lidos: 5 (`AGENTS.md`, `CLAUDE.md`, `README.md` na raiz; `AGENTS.md`, `CLAUDE.md` no hub)
- ledgers de dados contados: 3 (`records.jsonl`, `purification.jsonl`, `corpus-data.json`)
- `data/processed/records.jsonl`: 280 registros não vazios
- `corpus/corpus-data.json`: 280 itens
- `data/processed/purification.jsonl`: 236 registros não vazios
- worktrees Git de `iconocracy-corpus`: 13
- worktrees detached: 3 (`/Users/ana/.codex/worktrees/34b4/iconocracy-corpus`, `/Users/ana/.codex/worktrees/7bca/iconocracy-corpus`, `/Users/ana/Research/hub/iconocracy-corpus-pr85-fix`)
- worktrees Codex: 3
- worktrees Copilot: 6
- worktrees Claude dentro do repo canônico: 2
- branch medido do hub canônico: `feat/alegorias-piloto-v2`
- HEAD medido do hub canônico: `5f06c87`
- symlinks externos/atalhos examinados: 3 (`iconocracy-corpus`, `iconocracia-companion`, `ROADMAP.md`)
- symlinks quebrados examinados: 1 (`/Users/ana/Research/iconocracy-corpus`)
- self-symlinks de primeiro nível encontrados em subprojetos irmãos: 3

## Dependências inter-domínio
- [C-02] depende de auditoria de dados/release gate: as contagens 280/280/236 precisam ser confirmadas como snapshot operacional antes de atualizar documentação que orienta releases.
- [M-01] conflita com domínio de documentação pública: `README.md` é humano-facing e deve evitar números que mudam a cada aquisição.
- [M-03] depende de governança de agentes: Codex/Copilot/Claude precisam de regra comum para classificar worktree como efêmero, não fonte canônica.
- [m-04] depende da decisão metodológica de N analítico: o snapshot 165 em `Other/` não deve ser apagado por auditoria de topologia sem decisão de tese.
- [m-01] depende de domínio ambiente/build: comandos de validação só devem declarar Python após medir o conda env real.

## Recomendações priorizadas (top 5)
1. Declarar como fonte de verdade para agentes: raiz meta = `/Users/ana/Research`; repo canônico da tese = `/Users/ana/Research/hub/iconocracy-corpus`; dados operacionais = `data/processed/records.jsonl` → `corpus/corpus-data.json` → `data/processed/purification.jsonl`; `vault/candidatos/` é espelho auxiliar; worktrees são efêmeros.
2. Corrigir imediatamente o symlink quebrado `/Users/ana/Research/iconocracy-corpus` e normalizar `/Users/ana/Research/iconocracia-companion` para casing `/Users/ana`, ou remover ambos se os atalhos não forem necessários.
3. Atualizar `hub/iconocracy-corpus/CLAUDE.md`, `/Users/ana/Research/CLAUDE.md` e `/Users/ana/Research/README.md` para remover contagens 264/265/278/234 e refletir a medição 280/280/236, mantendo N analítico explicitamente como decisão pendente.
4. Registrar uma tabela “não usar como fonte de verdade” para `/Users/ana/.codex/worktrees/*`, `/Users/ana/copilot-worktrees/*`, `/Users/ana/Research/hub/iconocracy-corpus-pr85-fix`, `/Users/ana/Research/hub/iconocracy-corpus/.claude/worktrees/*`, `Other/` e self-symlinks.
5. Substituir paths legados (`/Volumes/data/...`, `/users/ana/...`, `~/Documents/projetos/research/...`) por paths canônicos ou notas de legado, com linha datada quando a referência histórica precisar permanecer.
