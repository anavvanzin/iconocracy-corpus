# AGENTS.md — Corpus Scout Agent
# ICONOCRACY · PPGD/UFSC · anavvanzin/iconocracy-corpus

## Papel deste projeto

Este é o ambiente de trabalho do agente CORPUS SCOUT para a tese
ICONOCRACY: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX).

Ao operar neste diretório, o Codex assume automaticamente o papel do
Corpus Scout conforme definido em SKILL.md. Não é necessário reintroduzir
o papel a cada sessão.

---

## Estrutura de diretórios esperada

```
iconocracy-corpus/
├── AGENTS.md                  ← este arquivo
├── SKILL.md                   ← definição do agente
├── data/
│   ├── raw/                   ← manifestos do bruto + links Drive; subpastas locais se houver
│   │   └── drive-manifest.json
│   ├── interim/               ← dados em processamento
│   └── processed/
│       └── records.jsonl      ← registros mestre do corpus
├── vault/                     ← notas Obsidian geradas pelo Scout
│   ├── candidatos/            ← notas SCOUT-XXX
│   └── sessoes/               ← notas SCOUT-SESSION-XXX
├── docs/                      ← ADRs, esquemas Notion e especificações do pipeline
├── corpus/                    ← corpus tabular e derivados analíticos
└── tools/
    ├── scripts/               ← scripts de sync, validação e processamento
    └── schemas/               ← schemas JSON do pipeline
```

---

## Comportamento padrão

Quando a pesquisadora digitar qualquer um dos seguintes, execute
diretamente sem pedir confirmação:

- `campanha N` → executa a campanha N conforme SKILL.md §7
- `scout [descrição livre]` → interpreta como query e executa
- `auditoria` → executa Campanha 16 com os arquivos em vault/candidatos/
- `lacunas` → idem
- `validar [arquivo]` → valida JSON/JSONL com `tools/scripts/validate_schemas.py`
  usando o schema pertinente; default: `data/processed/records.jsonl` + `master-record`
- `rastreabilidade [arquivo]` ou `evidencias [arquivo]` → roda
  `tools/scripts/trace_evidence.py`; default: `data/processed/records.jsonl`
- `citacoes [arquivo]` → gera/exporta citações ABNT com
  `tools/scripts/abnt_citations.py`
- `purificacao status` → mostra progresso da codificação
- `purificacao item [ID]` → roda `tools/scripts/code_purification.py --item [ID]`
- `purificacao lote [SIGLA]` → roda `tools/scripts/code_purification.py --batch [SIGLA]`
- `purificacao exportar` → roda `tools/scripts/code_purification.py --export-csv`
- `rede feminista [raiz opcional]` → roda `tools/scripts/extract_feminist_network.py`
- `lote exemplo` → roda `tools/scripts/batch_example.py`
- `sync vault pull|push|sync|diff|status` → usa `tools/scripts/vault_sync.py`;
  sincroniza `data/processed/records.jsonl` ↔ `vault/candidatos/` bidirecionalmente
- `sync notion pull|push|sync` → **DESCONTINUADO** — redireciona para vault_sync.py

Quando a pesquisadora digitar `salvar`, grave a última nota gerada
em vault/candidatos/ com o nome correto (SCOUT-[ID] [título].md).

Quando a pesquisadora digitar `sessão`, grave a nota de síntese
em vault/sessoes/ com o nome SCOUT-SESSION-[data].md.

---

## Rastreabilidade — regra inviolável

Cada item do corpus deve ser rastreável em três pontos:

| Onde | O quê |
|---|---|
| Google Drive + `data/raw/drive-manifest.json` | origem do bruto e vínculo com `item_id` |
| `vault/candidatos/` | nota Obsidian com metadados e análise |
| `data/processed/records.jsonl` | registro mestre canônico em JSONL |

Quando houver cópia local do bruto, ela pode ser organizada em
`data/raw/[pais]/`, mas o vínculo com o Drive deve continuar explícito.

`records.jsonl` é a fonte canônica do corpus. O vault Obsidian (`vault/candidatos/`)
funciona como espelho catalográfico; `tools/scripts/vault_sync.py` implementa
a sincronização bidirecional (status/diff/pull/push/sync).

---

## Terminologia obrigatória

- ENDURECIMENTO (nunca "hardening", nunca "embrutecimento")
- Contrato Sexual Visual (conceito original da tese — não atribuir a Pateman)
- Feminilidade de Estado (conceito original da tese — não atribuir a Mondzain)
- Zwischenraum (warburguiano — manter em alemão)
- Pathosformel (warburguiano — manter em alemão)
- Nachleben (warburguiano — manter em alemão)
- Mondzain → sempre edição 2002
- ABNT NBR 6023:2025 para todas as referências

---

## Tags canônicas do vault

```
corpus/candidato · corpus/sessao-scout · corpus/controle-negativo
pais/BR · pais/FR · pais/UK · pais/DE · pais/US · pais/BE
suporte/moeda · suporte/selo · suporte/monumento · suporte/estampa
suporte/frontispicio · suporte/papel-moeda · suporte/cartaz
regime/fundacional · regime/normativo · regime/militar
motivo/marianne · motivo/republica · motivo/justitia · motivo/britannia
motivo/columbia · motivo/germania · motivo/belgique
#verificar · #verificar-data · #verificar-autoria
#verificar-imagem · #sem-iiif · #possivel-duplicata
#protocolo · #decisao-metodologica
#acoplamento-imagem-norma · #colonialidade-do-ver
#contrato-racial-visual · #contra-alegoria · #ausencia-alegorica
#iconometria · #atlas/painel-I até #atlas/painel-VIII
```

---

## Ferramentas disponíveis para o agente

- `web_search` — busca em acervos e bases digitais
- `web_fetch` — acessa URLs de imagens IIIF e páginas de acervos
- `bash_tool` — salva notas em vault/, move arquivos, roda scripts
- `create_file` — cria notas .md em vault/candidatos/ e vault/sessoes/
- `tools/scripts/validate_schemas.py` — valida outputs JSON/JSONL do pipeline
- `tools/scripts/trace_evidence.py` — audita cadeia de evidências dos registros
- `tools/scripts/abnt_citations.py` — gera citações ABNT NBR 6023:2025
- `tools/scripts/code_purification.py` — codifica os 10 indicadores de purificação
- `tools/scripts/notion_sync.py` — scaffold de sync GitHub ↔ Notion
- `tools/scripts/extract_feminist_network.py` — extrai sub-rede Iconclass feminista
- `tools/scripts/batch_example.py` — gera lote demonstrativo do pipeline dual-agent

---

## Workflows operacionais

### 1. Busca scout

Fluxo padrão para descoberta iconográfica:

1. Executar `campanha N` ou `scout [query]`
2. Gerar até 8 notas candidatas em markdown
3. Registrar nota de síntese da sessão
4. Quando solicitado, `salvar` e depois `sessão`

### 2. QA e consolidação do pipeline

Fluxo padrão para pós-processamento e controle de qualidade:

1. Garantir ou atualizar `data/processed/records.jsonl`
2. Executar `validar [arquivo]`
3. Executar `rastreabilidade [arquivo]`
4. Executar `citacoes [arquivo]`
5. Reportar erros de schema, gaps de evidência e pendências ABNT

### 3. Codificação de purificação

Fluxo padrão para análise quantitativa:

1. Executar `purificacao status`
2. Executar `purificacao item [ID]` ou `purificacao lote [SIGLA]`
3. Salvar em `data/processed/purification.jsonl`
4. Executar `purificacao exportar` para atualizar `data/processed/corpus_dataset.csv`

### 4. Sync catalográfico

Fluxo padrão de espelhamento:

1. Confirmar existência de `NOTION_API_KEY` e `NOTION_CORPUS_DB_ID`
2. Executar `sync notion pull|push|sync`
3. Informar explicitamente que o script está em scaffolding quando esse for o caso

---

## Notas de sessão anteriores

Consultar vault/sessoes/ para contexto de buscas já realizadas
antes de iniciar nova campanha — evita duplicatas e orienta gaps.
