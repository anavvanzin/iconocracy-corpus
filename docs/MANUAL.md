# Manual de Instruções — Repositório Iconocracia

**Versão:** 1.2 · Novembro 2026
**Autora:** Ana Vanzin — PPGD/UFSC

---

## Sumário

1. [Visão geral do projeto](#1-visão-geral-do-projeto)
2. [Pré-requisitos e instalação](#2-pré-requisitos-e-instalação)
3. [Mapa do repositório](#3-mapa-do-repositório)
4. [Fluxos de trabalho diários](#4-fluxos-de-trabalho-diários)
   - 4.1 Catalogar uma imagem no corpus
   - 4.2 Codificar indicadores de purificação
   - 4.3 Escrever um capítulo da tese
   - 4.4 Compilar capítulos para DOCX/PDF
   - 4.5 Explorar o corpus pelo dashboard
   - 4.6 Criar nota de pesquisa
5. [Pipeline de dados](#5-pipeline-de-dados)
6. [Scripts disponíveis](#6-scripts-disponíveis)
7. [Esquemas e validação](#7-esquemas-e-validação)
8. [Notebooks de análise](#8-notebooks-de-análise)
9. [Convenções e boas práticas](#9-convenções-e-boas-práticas)
10. [Decisões arquiteturais (ADRs)](#10-decisões-arquiteturais-adrs)
11. [Resolução de problemas](#11-resolução-de-problemas)
12. [Prioridade terminológica e estratégia de publicação](#12-prioridade-terminológica-e-estratégia-de-publicação)

---

## 1. Visão geral do projeto

**Iconocracia** é a infraestrutura de pesquisa para a tese de doutorado *"Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"*.

O repositório integra:
- **Corpus iconográfico** — 337 IDs no export público e 328+ registros validados no ledger operacional (fotografias de out–nov/2026), com crescimento contínuo
- **Codificação quantitativa** — 10 indicadores ordinais de purificação (0–3) por item
- **Manuscrito da tese** — capítulos em Markdown, compiláveis para DOCX (ABNT) via Pandoc
- **Vault Obsidian** — fichas catalográficas, notas de pesquisa, diário
- **Dashboard interativo** — HTML autocontido com gráficos, filtros e busca
- **Pipeline de automação** — scripts Python para validação, exportação, release e backup

**Modelo operacional ativo:**

- `data/processed/records.jsonl` = ledger operacional canônico
- `corpus/corpus-data.json` = export público para browsers e releases
- `data/processed/purification.jsonl` = ledger canônico da codificação
- `vault/candidatos/` = espelho auxiliar
- Hugging Face = superfície pública de release

**Regimes em uso:** além dos regimes fundamentacional, normativo e militar, o regime **CONTRA-ALEGORIA** está ativo desde out/2026, com os casos `BR-051` (Justiça de Ceschiatti vandalizada no STF, sequência 2023–2024), `FR-100` (Marianne mutilada no Arco do Triunfo, 2018) e `FR-101` (Deborah de Robertis, *La Joconde de l'Histoire*, 2018), integrados à §3.4 do manuscrito.

**Objetivo:** que todos os materiais da tese — dados, análise, texto, figuras — vivam num único repositório rastreável.

---

## 2. Pré-requisitos e instalação

### Software necessário

| Software | Versão mínima | Para quê |
|----------|--------------|----------|
| Python | 3.10+ | Scripts, notebooks |
| Git | 2.30+ | Controle de versão |
| Pandoc | 3.0+ | Compilação Markdown → DOCX/PDF |
| Obsidian | 1.4+ | Vault de pesquisa (opcional) |

### Instalação rápida

```bash
# 1. Clonar o repositório
git clone https://github.com/anavvanzin/iconocracy-corpus.git
cd iconocracy-corpus

# 2. Criar ambiente Python (escolha uma opção)

# Opção A: conda
conda env create -f environment.yml
conda activate iconocracy

# Opção B: pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Verificar instalação
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/code_purification.py --status
python tools/scripts/vault_sync.py status
```

### Configuração do Obsidian

1. Abra o Obsidian
2. **Open folder as vault** → selecione `vault/`
3. Instale os plugins: **Dataview**, **Templates**
4. Em Settings → Templates → Template folder location: `_templates`

---

## 3. Mapa do repositório

```
iconocracy-corpus/
│
├── corpus/                         ← CORPUS PUBLICÁVEL
│   ├── corpus-data.json            ← Export público do corpus (337 IDs na fotografia de nov/2026)
│   ├── DASHBOARD_CORPUS.html       ← Dashboard interativo (abrir no browser)
│   ├── index.html                  ← Interface de busca simples
│   └── atlas-iconometrico.html     ← Atlas visual interativo (React app)
│
├── tese/                           ← MATERIAIS DA TESE
│   ├── manuscrito/                 ← Capítulos em revisão (Markdown)
│   │   ├── Introducao_rev.md       ← Introdução (revisão avançada)
│   │   ├── Capitulo1_rev.md        ← Cap. 1 (revisão avançada)
│   │   ├── sumario_iconocracia.md  ← Sumário anotado completo
│   │   └── LEIAME.md               ← Guia para o orientador
│   ├── revisoes/                   ← Documentos de revisão
│   ├── pesquisa/                   ← Notas de pesquisa e relatórios NotebookLM
│   ├── apresentacoes/              ← Apresentações de andamento (PPTX)
│   ├── Para_Orientador_Mar2026/    ← Artigos complementares para orientador
│   ├── ATLAS_ICONOCRACIA.pdf       ← Atlas imprimível (10 páginas)
│   └── ATLAS_ICONOCRACIA.docx      ← Fonte editável do atlas
│
├── vault/                          ← OBSIDIAN VAULT
│   ├── _templates/                 ← 4 templates (ficha, nota, capítulo, diário)
│   ├── corpus/                     ← Fichas catalográficas (1 nota = 1 item)
│   ├── tese/                       ← Capítulos Pandoc-ready + Makefile
│   ├── pesquisa/                   ← Notas de pesquisa
│   ├── diario/                     ← Diário de pesquisa
│   └── meta/                       ← Codebook, ADRs
│
├── atlas/                          ← ATLAS ICONOCRÁTICO (Obsidian)
│   ├── Iconocracia — Mapa Central.md       ← MOC principal do atlas
│   ├── Arquitetura Atlas e Tese — MOC.md   ← Atlas transnacional (1800–2000) × vertente da tese (Brasil 1822–1922)
│   └── stubs/                      ← Stubs documentais do atlas
│
├── data/                           ← DADOS
│   ├── raw/                        ← Manifestos e links (nunca arquivos brutos)
│   ├── interim/                    ← Dados em transformação
│   ├── processed/                  ← Dados prontos para análise
│   │   ├── purification.jsonl      ← Codificação de purificação (JSONL)
│   │   ├── corpus_dataset.csv      ← CSV completo (metadados + purificação)
│   │   └── feminist_network_48C51_pt.json
│   └── docs/                       ← Codebook, descrição do dataset
│
├── tools/                          ← FERRAMENTAS
│   ├── scripts/                    ← scripts Python de pipeline, release e backup
│   ├── schemas/                    ← JSON Schemas (master-record, iconocode, webscout)
│   ├── sql/                        ← Migrações SQL
│   └── atlas_lab/                  ← AtlasLab viewer (JSX)
│
├── notebooks/                      ← ANÁLISE (Cap. 6)
│   ├── 01_exploratory.ipynb        ← Distribuição dos indicadores
│   ├── 02_kruskal_wallis.ipynb     ← Regimes × morfologia
│   ├── 03_regression.ipynb         ← Regressão logística ordinal
│   └── 04_correspondence.ipynb     ← Análise de correspondência múltipla
│
├── docs/                           ← DOCUMENTAÇÃO TÉCNICA
│   ├── ICONOCRACIA_PROJETO.md      ← Documento do projeto
│   ├── scripts.md                  ← Referência de scripts
│   ├── adr/                        ← Decisões arquiteturais (5 ADRs)
│   ├── audits/                     ← Trilha de auditoria de reconciliação com catálogos (nov/2026)
│   ├── drive-structure.md          ← Organização do Google Drive
│   ├── OPERATING_MODEL.md          ← Modelo operacional vigente
│   ├── huggingface-release.md      ← Fluxo de release no Hugging Face
│   └── notion-schema.md            ← Arquivo histórico (Notion descontinuado)
│
├── sources/                        ← Materiais de referência e pesquisa salvos
├── examples/                       ← Saídas de exemplo do pipeline
├── website/                        ← Site Ius Gentium (GitHub Pages)
│
├── environment.yml                 ← Ambiente conda
├── requirements.txt                ← Dependências pip
├── CITATION.cff                    ← Metadados de citação
└── README.md
```

---

## 4. Fluxos de trabalho diários

### 4.1 Catalogar uma imagem no corpus

**Onde:** Obsidian (`vault/corpus/`) ou diretamente em `corpus/corpus-data.json`

**Via Obsidian (recomendado):**

1. No Obsidian, crie nova nota em `corpus/`
2. Aplique o template `ficha-catalografica` (Ctrl/Cmd+T)
3. Preencha os campos do frontmatter:
   ```yaml
   id: BR-011
   titulo: "Alegoria da República no Palácio Tiradentes"
   data: "1926"
   pais: Brasil
   suporte: Escultura
   acervo: Câmara dos Deputados
   url_imagem: https://...
   ```
4. Adicione descrição e notas no corpo da nota
5. O item precisará ser adicionado a `corpus/corpus-data.json` para aparecer no dashboard

**Via JSON direto:**

Adicione um objeto ao array em `corpus/corpus-data.json` seguindo o formato dos itens existentes. Campos obrigatórios: `id`, `title`, `date`, `country`, `medium`, `url`.

**Convenção de IDs (faixas em uso, nov/2026):**
- `BR-001` a `BR-051` — Brasil (inclui o caso Ceschiatti/STF)
- `FR-001` a `FR-101` — França (inclui as contra-alegorias de 2018)
- `DE-001` a `DE-NNN` — Alemanha
- `US-001` a `US-NNN` — EUA
- `UK-001` a `UK-NNN` — Reino Unido
- `BE-001` a `BE-NNN` — Bélgica
- `PT-001` a `PT-NNN` — Portugal
- `EU-001` a `EU-NNN` — Multi-país / Europeana
- `NL-001` a `NL-NNN` — Países Baixos

**Reconciliação com catálogos institucionais:** quando um registro é confrontado com catálogo oficial (ex.: MHN, Hemeroteca Nacional), o histórico **não é reescrito**: acrescenta-se um adendo à ficha SCOUT correspondente e um relatório datado em `docs/audits/` (ex.: `2026-10-31-reconciliacao-fontes-brasileiras.md`, que atualizou URLs/citações de `BR-019`, `BR-024` e `BR-041` e confirmou o inventário MHN `123275`). Decisões pendentes — como a possível duplicata de Villares ou a equivalência "A República" ↔ `Q117764760` — ficam **registradas, não fundidas**.

### 4.2 Codificar indicadores de purificação

**Ferramenta:** `code_purification.py` (CLI interativo)

```bash
# Ver progresso atual
python tools/scripts/code_purification.py --status

# Codificar todos os itens ainda não codificados
python tools/scripts/code_purification.py --resume

# Codificar um item específico
python tools/scripts/code_purification.py --item BR-001

# Codificar todos os itens de um país
python tools/scripts/code_purification.py --batch FR

# Exportar CSV completo para análise
python tools/scripts/code_purification.py --export-csv
```

**Durante a codificação:**

1. O CLI mostra os metadados do item e a URL da miniatura
2. **Abra a URL no navegador** para ver a imagem
3. Para cada um dos 10 indicadores, o CLI mostra a escala (0–3) do codebook
4. Digite `0`, `1`, `2` ou `3` para cada indicador
5. Digite `s` para pular um item, `q` para sair

**Referência rápida dos indicadores:**

| # | Indicador | O que mede |
|---|-----------|-----------|
| 1 | `desincorporacao` | Corpo carnal → forma abstrata |
| 2 | `rigidez_postural` | Movimento → hieratismo |
| 3 | `dessexualizacao` | Erotismo → gênero indeterminado |
| 4 | `uniformizacao_facial` | Retrato → máscara |
| 5 | `heraldizacao` | Atributos integrados → emblemas isolados |
| 6 | `enquadramento_arquitetonico` | Espaço aberto → nicho/selo |
| 7 | `apagamento_narrativo` | Cena narrativa → figura isolada |
| 8 | `monocromatizacao` | Policromia → monocromático |
| 9 | `serialidade` | Obra única → reprodução massiva |
| 10 | `inscricao_estatal` | Obra autônoma → dispositivo estatal |

**Saída:** `data/processed/purification.jsonl` (1 registro por linha, com timestamp e assinatura do codificador; 286 linhas validadas na fotografia de nov/2026)

**Dica:** codifique em blocos de 30 minutos (~10 itens por sessão). Tenha o codebook completo (`data/docs/codebook.md`) acessível.

### 4.3 Escrever um capítulo da tese

**Onde:** `vault/tese/capitulo-X.md` (Obsidian)

**Fluxo:**

1. Abra o capítulo no Obsidian (ex.: `vault/tese/capitulo-2.md`)
2. Consulte o sumário anotado (`tese/manuscrito/sumario_iconocracia.md`) para a estrutura
3. Use wiki-links para referenciar fichas do corpus: `[[BR-001]]`
4. Use wiki-links para notas de pesquisa: `[[NLM-panorama-sistemas-poder-visual-v1]]`
5. Citações em formato Pandoc: `[@pateman1988, p. 42]`
6. As referências vão em `vault/tese/references.bib` (formato BibTeX)

**Estrutura de um capítulo:**

```markdown
---
titulo: "Iconocracia: Economia da Imagem Soberana"
capitulo: 2
status: rascunho
palavras: 0
---

# Capítulo 2 — Iconocracia: Economia da Imagem Soberana

## 2.1 Mondzain: a economia do ícone

Texto aqui com citações [@mondzain2005, p. 15].

## 2.2 Feminilidade de Estado

Referência a item do corpus: ver [[BR-001]].
```

**Estrutura vigente do manuscrito (nov/2026):** Introdução + Capítulos 1–9 + Conclusão. Destaques: Cap. 3 (*A Colonialidade do Ver*), com §3.4 "Rupturas e contra-alegorias"; Cap. 9 (*Os 8 Painéis do Atlas Iconocrático*). Os onze espelhos Obsidian (introdução, caps. 1–9, conclusão) refletem os corpos do manuscrito.

### 4.4 Compilar capítulos para DOCX/PDF

```bash
cd vault/tese

# Compilar tese completa para DOCX (ABNT) — também é o alvo padrão de `make -C vault/tese`
make docx

# Compilar capítulo individual
make capitulo-2.docx

# Compilar para PDF (requer LaTeX)
make pdf

# Ver opções disponíveis
make setup
```

**Fontes e saídas:** a compilação lê `tese/manuscrito/`; capítulos em
`vault/tese/` são espelhos Obsidian. Bibliografia é obrigatória, e a
numeração editorial não recebe uma segunda camada automática.
Ver [compilação da tese](../vault/tese/README.md), incluindo requisitos de
fontes e mecanismo PDF.

**Infraestrutura de build (decisões de out/2026, PR #239):**

- O único Makefile é `vault/tese/Makefile`; o legado `tese/manuscrito/Makefile` foi **removido** (referia nomes de capítulos inexistentes).
- **Numeração única:** os títulos carregam a numeração editorial no próprio texto; o Pandoc não renumera (`--number-sections` removido). Remissões do Cap. 4 usam §§4.1–4.8.
- `references.bib` é **obrigatório**: o alvo `bib-check` bloqueia tese completa e capítulos individuais, em DOCX e PDF (97 entradas, IDs únicos, na fotografia de out/2026).
- PDF via **LuaLaTeX + TeX Gyre Termes**; `PDF_ENGINE` e `PDF_FONT` permitem alternativa explícita por ambiente (ex.: XeLaTeX + DejaVu Serif).
- `tese/tese_completa.pdf` é saída regenerável e **não é versionado** (`.gitignore`); `make pdf` gera em `vault/tese/output/` e copia. `tese/tese_completa.docx` continua versionado, mas **deve ser regenerado antes de distribuir** — a cópia corrente ainda antecede a correção de numeração (pendência conhecida, não regressão).
- O CI (`.github/workflows/validate.yml`) instala o Pandoc antes dos testes de compilação e ABNT.

**Requisito:** Pandoc 3.0+ e `pandoc-citeproc` (ou `citeproc` embutido).

**O que faz:** converte Markdown → DOCX com citações formatadas (autor-data ABNT), capa, sumário automático.

### 4.5 Explorar o corpus pelo dashboard

1. Abra `corpus/DASHBOARD_CORPUS.html` em qualquer navegador
2. Não precisa de servidor — tudo é autocontido
3. Funcionalidades:
   - **Galeria**: miniaturas com modal de detalhes
   - **Tabela**: ordenável e paginada
   - **Filtros**: país, período, suporte, acervo, busca livre
   - **Gráficos**: 6 visualizações Chart.js
   - **Citações**: copie ABNT ou Chicago diretamente do modal

### 4.6 Criar nota de pesquisa

**No Obsidian:**

1. Crie nota em `vault/pesquisa/`
2. Aplique template `nota-de-pesquisa`
3. Preencha:
   ```yaml
   fonte: "Mondzain, Marie-José. Image, Icon, Economy (2005)"
   capitulo: 2
   tags: [iconocracia, economia-do-icone, bizancio]
   data: 2026-03-24
   ```
4. Escreva resumo, citações-chave, conexões com a tese

---

## 5. Pipeline de dados

### Fluxo canônico

```
Google Drive (brutos)           ← fora do git
        │
        ▼
data/processed/records.jsonl    ← ledger operacional canônico
        │
        ├──► records_to_corpus.py ─► corpus/corpus-data.json
        │                                  │
        │                                  ├──► dashboards / sites / Hugging Face Space
        │                                  └──► build_hf_release.py ─► snapshot público
        │
        ├──► vault_sync.py ─────────► vault/candidatos/
        │
        └──► code_purification.py ─► data/processed/purification.jsonl
                                           │
                                           ▼
                                   data/processed/corpus_dataset.csv
                                           │
                                           ▼
                                   notebooks/*.ipynb  (Cap. 6)
```

### Formatos de dados

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `data/processed/records.jsonl` | JSONL | Ledger operacional canônico do corpus |
| `corpus/corpus-data.json` | JSON array | Export público para sites, dashboards e releases |
| `data/processed/purification.jsonl` | JSONL | Codificação dos 10 indicadores + composto + regime |
| `data/processed/corpus_dataset.csv` | CSV | Junção para notebooks/SPSS/R |

### Adicionar novo item ao pipeline

1. Atualizar ou criar o registro canônico
2. Revisar `python tools/scripts/vault_sync.py diff`
3. Exportar para `corpus/corpus-data.json` quando necessário
4. Codificar purificação: `python tools/scripts/code_purification.py --item XX-NNN`
5. Exportar CSV atualizado: `python tools/scripts/code_purification.py --export-csv`

---

## 6. Scripts disponíveis

Todos em `tools/scripts/`. Executar da raiz do repositório:

```bash
python tools/scripts/<nome>.py [argumentos]
```

| Script | O que faz | Exemplo |
|--------|-----------|---------|
| `code_purification.py` | Codificar indicadores de purificação | `--status`, `--batch FR`, `--export-csv` |
| `validate_schemas.py` | Validar registros contra JSON Schemas | `examples/batch_001/master_record_*.json` |
| `abnt_citations.py` | Gerar citações ABNT NBR 6023:2025 | — |
| `batch_example.py` | Demo do pipeline de processamento em lote | — |
| `extract_feminist_network.py` | Extrair sub-rede feminista do Iconclass | — |
| `trace_evidence.py` | Rastreabilidade de evidência por item | — |
| `vault_sync.py` | Sincronizar `records.jsonl` ↔ `vault/candidatos/` | `status`, `diff`, `pull`, `push`, `sync` |
| `vault_backup.py` | Criar backup local do vault fora do histórico do git | `--note`, `--dest`, `--keep` |
| `build_hf_release.py` | Gerar snapshot e dataset card para Hugging Face | `--note`, `--publish` |
| `sync_github_labels.py` | Aplicar conjunto mínimo de labels no GitHub | `--dry-run`, `--repo` |
| `make_index.py` | Índice de busca do Iconclass | — |
| `make_skos.py` | Vocabulário SKOS/RDF do Iconclass | — |
| `make_sqlite.py` | Banco SQLite do Iconclass | — |

**Documentação completa:** `docs/scripts.md`

---

## 7. Esquemas e validação

### JSON Schemas (`tools/schemas/`)

| Schema | Valida |
|--------|--------|
| `master-record.schema.json` | Registro completo do pipeline (inclui `purificacao`) |
| `webscout-output.schema.json` | Saída do agente WebScout |
| `iconocode-output.schema.json` | Saída do agente IconoCode |

### Validar registros

```bash
python tools/scripts/validate_schemas.py examples/batch_001/master_record_*.json
```

### Estrutura do bloco `purificacao` no schema

```json
{
  "purificacao": {
    "desincorporacao": 2,
    "rigidez_postural": 3,
    "dessexualizacao": 2,
    "uniformizacao_facial": 2,
    "heraldizacao": 1,
    "enquadramento_arquitetonico": 3,
    "apagamento_narrativo": 2,
    "monocromatizacao": 3,
    "serialidade": 3,
    "inscricao_estatal": 3,
    "purificacao_composto": 2.4,
    "regime_iconocratico": "normativo",
    "coded_by": "ana",
    "coded_at": "2026-03-24T14:30:00Z"
  }
}
```

---

## 8. Notebooks de análise

Em `notebooks/`. Correspondem às seções do Capítulo 6 da tese.

| Notebook | Seção | Método | Pré-requisito |
|----------|-------|--------|---------------|
| `01_exploratory.ipynb` | 6.1 | Distribuição dos 10 indicadores, histogramas, boxplots | `corpus_dataset.csv` com purificação |
| `02_kruskal_wallis.ipynb` | 6.2 | Teste Kruskal-Wallis: regimes × morfologia | Idem + ≥30 itens codificados |
| `03_regression.ipynb` | 6.3 | Regressão logística ordinal: preditores do endurecimento | Idem + ≥50 itens |
| `04_correspondence.ipynb` | 6.4 | Análise de correspondência múltipla: circulação transatlântica | Idem + cobertura multi-país |

**Nota sobre o N=145:** o Cap. 6, §6.3 documenta `N=145` como **congelamento analítico histórico**; não é o denominador dos percentuais atuais de §6.1 nem deve ser "corrigido" para os totais correntes do ledger. A distinção entre instantâneos e lotes é decisão metodológica registrada (PR #239).

**Para rodar:**

```bash
# Gerar CSV atualizado primeiro
python tools/scripts/code_purification.py --export-csv

# Abrir notebooks
jupyter notebook notebooks/
```

---

## 9. Convenções e boas práticas

### Nomeação de arquivos

- IDs de corpus: `XX-NNN` (código de país ISO-2 + sequencial com zero-fill de 3)
- Capítulos no vault: `capitulo-N.md` (hífen, sem acento)
- Capítulos no manuscrito: `CapituloN_rev.md` (versão para orientador)
- Notas de pesquisa: nome descritivo em minúsculas com hífens

### Git

- Commitar frequentemente com mensagens descritivas
- Nunca commitar arquivos de imagem brutos (referência por URL)
- `main` é reservado para commits intencionais e legíveis
- Use branches curtas (`codex/...`, `topic/...`) para trabalho novo
- Use `python tools/scripts/vault_backup.py` para backups automáticos do vault

### Citações

- No vault (Pandoc): `[@autor2020, p. 42]`
- No manuscrito (ABNT inline): `(AUTOR, 2020, p. 42)`
- Referências BibTeX: `vault/tese/references.bib`

### Codificação de purificação

- Sempre codificar com a imagem aberta no navegador
- Usar o codebook (`data/docs/codebook.md`) em caso de dúvida
- Registrar incertezas no campo `notes`
- Meta: ≥95% de concordância intra-codificador (retestar 10% após 2 semanas)
- Reconciliações com catálogos institucionais geram **adendo na ficha SCOUT + relatório em `docs/audits/`** — nunca edição silenciosa do ledger histórico

---

## 10. Decisões arquiteturais (ADRs)

Documentadas em `docs/adr/`:

| ADR | Decisão | Resumo |
|-----|---------|--------|
| 001 | Google Drive como armazém bruto | Imagens ficam no Drive; repositório tem apenas URLs e metadados |
| 002 | Notion como índice do corpus | Histórico; superado por ADR-004 |
| 003 | JSONL como formato canônico | 1 registro por linha; fácil de processar, versionar e validar |
| 004 | Vault como espelho catalográfico | Obsidian substitui Notion no fluxo ativo |
| 005 | GitHub/Hugging Face como superfícies | GitHub é backbone canônico; HF é release público |

> **Pendentes de ADR (out–nov/2026):** numeração editorial única no manuscrito (sem `--number-sections`); artefatos regeneráveis fora do versionamento com `bib-check` como gate; reconciliação com catálogos institucionais via trilha em `docs/audits/`. Candidatas a ADR-006+.

---

## 11. Resolução de problemas

### "Nenhum item para codificar"
```bash
python tools/scripts/code_purification.py --status
# Se todos codificados, --resume não mostra itens
# Use --item XX-NNN para recodificar um item específico
```

### Dashboard não carrega
- Abra `corpus/DASHBOARD_CORPUS.html` diretamente (File → Open)
- Não precisa de servidor web
- Se imagens não aparecem, verifique conexão à internet (thumbnails vêm dos acervos)

### Pandoc não compila
```bash
# Verificar versão
pandoc --version  # precisa 3.0+

# Verificar se references.bib existe (obrigatório desde out/2026)
ls vault/tese/references.bib

# Compilar com debug
cd vault/tese && make capitulo-1.docx PANDOC_ARGS="--verbose"
```

### validate_schemas.py falha
```bash
# Instalar dependência
pip install jsonschema

# Ou usar modo sem dependência (fallback interno)
python tools/scripts/validate_schemas.py --help
```

### Git: arquivo muito grande
- Imagens devem ser referenciadas por URL, nunca commitadas
- Se um arquivo grande foi adicionado por engano: `git rm --cached <arquivo>`
- `.gitignore` já exclui `*.zip`, `~$*`, `review/` e a saída regenerável `tese/tese_completa.pdf`

---

## 12. Prioridade terminológica e estratégia de publicação

Seção incorporada em nov/2026 a partir da avaliação bibliográfica sobre a revista *Iconocrazia* (Bari) e da revisão de originalidade da tese (relatórios de avaliação, nov/2026; a arquivar em `tese/pesquisa/`).

### 12.1 O termo "iconocracia": o que a tese pode e não pode afirmar

- **A tese não cunhou o termo.** *Iconocratie/iconocracy* é neologismo de Marie-José Mondzain — usos de 1984 e 1993 atestados indiretamente; definição verificada em "Iconic Space and the Rule of Lands" (*Hypatia*, 2000, p. 59): a "organization of the visible which provokes a belief", uma "submission to the gaze".
- **Relés jurídicos:** Goodrich (*Legal Emblems and the Art of Law*, 2013/2014, cap. 5) e Sherwin (2017) levaram o termo à teoria do Direito, ambos atribuindo-o a Mondzain.
- **Uso brasileiro anterior:** Franca Filho, *A cegueira da justiça* (Fabris, 2011) — "iconocracia — o governo das imagens" (página exata a verificar).
- **Uso italiano distinto:** a revista *Iconocrazia* (Univ. de Bari, ISSN 2240-760X, fundada em 2012) é kantorowicziana, não cita Mondzain, e não publicou trabalhos sobre Brasil, Justiça alegórica ou personificação latino-americana. A filiação entre os dois usos **não pode** ser afirmada.

**Fórmula defensável para o manuscrito:** adota-se o termo de Mondzain, que o cunhou para a "organização do visível que provoca crença" (2000, p. 59), levado à teoria jurídica por Goodrich, e redefine-se para a história jurídica da alegoria nacional — com reconhecimento do uso brasileiro anterior de Franca Filho e do uso italiano independente da revista de Bari.

**Contribuição original delimitada:** a pergunta histórico-jurídica (a alegoria como operador de legitimidade jurídica), o tratamento conjunto de Justiça, República e Nação na transição Império–República (1822–1922), o corpus documentado atrelado a fontes normativas, e o quadro de três regimes com a contra-alegoria como teste. **Não reivindicar** ineditismo do termo nem do estudo da alegoria feminina da República no Brasil (cf. Carvalho 1990; Lima Junior 2020; Nascimento & Batista 2022; e Gawryszewski 2018 para a Justiça na imprensa anarquista).

### 12.2 Chamada "Democrazie armate / Armed Democracies" (*Iconocrazia*, v. 1, n. 31, 2027)

- **Prazo:** 20 abr 2027 · **Idiomas:** IT/EN/FR/ES (**português não aceito**, embora a revista já tenha publicado texto em português) · **Limite:** 40.000 caracteres (espaços, notas e bibliografia incluídos) · **Resumos:** IT + EN, ≤1.000 caracteres cada, 5 keywords · **Envio:** info@iconocrazia.it
- ⚠️ O domínio `iconocrazia.it` exibia página de venda de domínio em 6 nov 2026: confirmar o endereço de submissão pela página de contato do OJS (`ojs.uniba.it/index.php/icon`) antes de enviar qualquer coisa. Taxas não informadas no site — verificar.
- **Aderência:** moderada no máximo. O regime "militar" do quadro teórico é iconográfico (figuras femininas armadas: Minerva, Bellona, a República com espada), não a remilitarização institucional que a chamada tematiza; qualquer submissão precisa construir explicitamente a ponte (ex.: a fundação armada da República, 1889–1894, e a Constituição de 1891).
- **Autoplágio:** um artigo sobre o 8 de janeiro / Ceschiatti não pode reciclar "Iconocracia Tropical" sem checagem contra o artigo publicado.

### 12.3 Verificações pendentes antes de afirmar no manuscrito

- Página exata de "iconocracia" em Franca Filho (2011); o artigo de 1984 de Baudinet-Mondzain (checar SUDOC); buscas em Gallica, Google Books e OED para usos pré-1984.
- BDTD, catálogo CAPES, USP Teses e SciELO com strings de busca registradas ("alegoria da justiça", "Têmis", "alegoria da República", "iconografia jurídica", "1822") — as ausências de precedentes ainda não são auditáveis.
- Status ANVUR (Area 14/12) e indexações da revista (DOAJ, Scopus, ERIH PLUS, Latindex) verificados diretamente nas fontes, não por snippets.

---

*Manual atualizado em 6 de novembro de 2026. Para a versão mais atualizada, consulte o repositório.*
