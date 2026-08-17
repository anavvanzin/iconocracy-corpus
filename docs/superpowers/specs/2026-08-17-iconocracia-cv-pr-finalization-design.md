# ICONOCRACIA-CV — design de encerramento acadêmico da branch

**Data:** 2026-08-17  
**Branch:** `codex/consolidate-iconocracia-cv`  
**Base:** `main`  
**Decisão:** abrir uma Pull Request de encerramento, priorizando máxima rastreabilidade acadêmica.

## 1. Objetivo

Integrar à história principal do `iconocracy-corpus` a superfície pública do
ICONOCRACIA-CV, o dossiê da disciplina e seu sistema de design, preservando em
uma única Pull Request as evidências de validação, a proveniência dos artefatos
e as limitações atuais do dataset.

A PR não apresentará o corpus como integralmente pronto para treinamento
visual. Ela distinguirá três estados:

1. a aplicação e os documentos da disciplina estão concluídos;
2. o dataset de metadados publicado no Hugging Face está operacional e coincide
   com os arquivos canônicos locais;
3. a preparação de uma coorte visual reproduzível ainda depende de imagens,
   reconciliação do vault, maior cobertura de codificação e rastreabilidade de
   evidências.

## 2. Unidade acadêmica da entrega

O ICONOCRACIA-CV é uma camada derivada do corpus integral, criada para a
disciplina de Visão Computacional. Não constitui um corpus autônomo e não altera
a hierarquia de fontes do projeto:

1. `data/processed/records.jsonl` — ledger canônico;
2. `corpus/corpus-data.json` — exportação pública;
3. `data/processed/purification.jsonl` — observações de endurecimento;
4. `vault/candidatos/` — espelho auxiliar de catalogação.

A PR deverá manter essa relação explícita em seu título, resumo e seção de
limitações.

## 3. Conteúdo da Pull Request

### 3.1 Artefatos integrados

- página estática e build do site em `deploy/iconocracia-cv/`;
- recursos visuais públicos: selo solar, Justitia pixelada e banner acadêmico;
- dossiê integrado da disciplina;
- memorando estratégico e versões PT/EN do sistema de design;
- figura do pipeline ICONOCRACIA-CV;
- gerador versionado do dossiê.

### 3.2 Evidências obrigatórias no corpo da PR

| Evidência | Resultado aceito |
|---|---|
| Suíte Python | `279 passed` |
| Build do site | Worker com 11 rotas |
| Schemas | 335/335 registros válidos |
| Exportação | 335 registros em ambos os estratos; delta zero |
| Purificação | 286/335 codificados; 49 pendentes |
| Snapshot local | `2026-08-17-finalization-audit` |
| Hugging Face | `corpus=335`, `records=335`, `purification=286` |
| Integridade remota | SHA-256 local e remoto idênticos para os três arquivos de dados |
| Viewer | preview, viewer, busca, filtros e estatísticas válidos |

Os resultados deverão ser registrados como evidência datada, e não como
garantia permanente sobre estados futuros do repositório ou do serviço remoto.

## 4. Limitações declaradas

A PR deverá registrar, sem tentar corrigir no mesmo escopo:

- 49 itens ainda sem codificação de endurecimento;
- regime militar com 28 de 54 itens codificados;
- zero itens na categoria `ARQUITETURA FORENSE`;
- 76 suportes classificados como `?` e sete como `unknown`;
- divergência de URLs entre ledger e vault: 38 somente em `records.jsonl` e 46
  somente no vault;
- 42 registros sem nota vault correspondente identificada por título;
- taxa de rastreabilidade estruturada de evidências de 3,3%, com 639 ocorrências
  de `missing_evidence`;
- ausência de bytes de imagem ou coluna `Image` no dataset público;
- 172 entradas do `drive-manifest.json` ainda dependentes de
  `PLACEHOLDER_FOLDER_ID`;
- oito avisos de marcadores `pytest.mark.unit` não registrados.

Essas limitações bloqueiam uma nova release apresentada como expansão ou como
dataset visual treinável, mas não invalidam a integração da superfície da
disciplina nem o dataset de metadados já publicado.

## 5. Estratégia de integração

1. manter `main` incorporada à branch, preservando o conserto dos testes Argos;
2. versionar esta especificação na branch;
3. publicar a branch atualizada no remoto sem force-push;
4. abrir uma nova PR de `codex/consolidate-iconocracia-cv` para `main`;
5. usar o corpo da PR como relatório de proveniência e gate;
6. aguardar todos os checks obrigatórios;
7. realizar o merge somente após aprovação explícita da Ana;
8. preservar o worktree enquanto houver revisão ou feedback na PR.

### 5.1 PR sucessora para a camada visual

As imagens do corpus não serão incorporadas nesta entrega. O corpo da PR deverá
registrar uma continuação independente, dedicada a tornar a coorte visual
reproduzível sem misturar metadados, binários e decisões de direitos autorais.

Essa PR sucessora deverá definir, antes de qualquer upload:

- correspondência canônica `item_id → arquivo visual`;
- checksum SHA-256, formato, dimensões e tamanho de cada arquivo;
- instituição, URL de origem e situação de direitos ou licença;
- estado explícito para imagens ausentes ou ainda não verificadas;
- substituição dos valores `PLACEHOLDER_FOLDER_ID` no manifesto do Drive;
- cobertura do manifesto em relação aos 335 registros;
- política de publicação: bytes no Hugging Face somente quando autorizados;
- configuração visual independente, como `images` ou `cv`, sem alterar as
  configurações `corpus`, `records` e `purification`.

A única dependência entre as duas PRs será o `item_id`. A PR atual não criará
arquivos visuais provisórios, URLs fictícias nem garantias de disponibilidade.

### Título proposto

`Finalize ICONOCRACIA-CV course surface and academic dossier`

## 6. O que não será feito

- não publicar um novo snapshot no Hugging Face, pois os arquivos de dados
  locais e remotos são idênticos;
- não completar as 49 codificações dentro desta PR;
- não reconciliar automaticamente ledger e vault;
- não mover imagens do Google Drive para Git ou Hugging Face;
- não criar nesta PR o manifesto visual definitivo; esse trabalho pertence à PR
  sucessora descrita na seção 5.1;
- não normalizar suportes, países ou evidências sem adjudicação metodológica;
- não alterar a tese ou o codebook como efeito colateral do encerramento;
- não apagar a branch ou o worktree enquanto a PR estiver aberta.

## 7. Tratamento de falhas

- Se o push for rejeitado, atualizar as referências e diagnosticar a divergência;
  não usar force-push sem autorização explícita.
- Se um check da PR falhar, manter branch e worktree, corrigir apenas regressões
  introduzidas por esta entrega e repetir a validação afetada.
- Se a falha já existir em `main`, registrá-la separadamente e não atribuí-la ao
  ICONOCRACIA-CV.
- Se os arquivos do Hugging Face mudarem antes da abertura da PR, repetir a
  comparação de hashes e atualizar o relatório antes do merge.

## 8. Critérios de conclusão

A entrega estará concluída quando:

1. a PR existir e apontar para `main`;
2. o corpo da PR registrar artefatos, validações, hashes e limitações;
3. todos os checks obrigatórios estiverem verdes; eventuais falhas herdadas
   deverão ser corrigidas ou retiradas do conjunto obrigatório por decisão de
   governança registrada separadamente, nunca apenas ignoradas nesta PR;
4. Ana aprovar explicitamente o merge;
5. o commit integrado permanecer rastreável a partir de `main`;
6. os endereços públicos do site continuarem operacionais após o merge.
