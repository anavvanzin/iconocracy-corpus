# Manual de Instruções — Repositório Iconocracia

**Versão:** 1.0 · Março 2026
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

---

## 1. Visão geral do projeto

**Iconocracia** é a infraestrutura de pesquisa para a tese de doutorado *"Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"*.

O repositório integra:
- **Corpus iconográfico** — ~300 imagens de alegorias femininas oficiais (selos, moedas, fachadas, monumentos) de 6 países, séculos XIX–XX
- **Codificação quantitativa** — 10 indicadores ordinais de purificação (0–3) por item
- **Manuscrito da tese** — capítulos em Markdown, compiláveis para DOCX (ABNT) via Pandoc
- **Vault Obsidian** — fichas catalográficas, notas de pesquisa, diário
- **Dashboard interativo** — HTML autocontido com gráficos, filtros e busca
- **Pipeline de automação** — scripts Python para citações, validação, exportação

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
python tools/scripts/validate_schemas.py
python tools/scripts/code_purification.py --status
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
│   ├── corpus-data.json            ← Dataset canônico (66 itens, JSON array)
│   ├── DASHBOARD_CORPUS.html       ← Dashboard interativo (abrir no browser)
│   └── index.html                  ← Interface de busca simples
│
├── tese/                           ← MATERIAIS DA TESE
│   ├── manuscrito/                 ← Capítulos em revisão (Markdown)
│   │   ├── Introducao_rev.md       ← Introdução (revisão avançada)
│   │   ├── Capitulo1_rev.md        ← Cap. 1 (revisão avançada)
│   │   ├── sumario_iconocracia.md  ← Sumário anotado completo
│   │   └── LEIAME.md               ← Guia para o orientador
│   ├── revisoes/                   ← Documentos de revisão
│   ├── pesquisa/                   ← Relatórios NotebookLM
│   └── ATLAS_ICONOCRACIA.pdf       ← Atlas imprimível (10 páginas)
│
├── vault/                          ← OBSIDIAN VAULT
│   ├── _templates/                 ← 4 templates (ficha, nota, capítulo, diário)
│   ├── corpus/                     ← Fichas catalográficas (1 nota = 1 item)
│   ├── tese/                       ← Capítulos Pandoc-ready + Makefile
│   ├── pesquisa/                   ← Notas de pesquisa
│   ├── diario/                     ← Diário de pesquisa
│   └── meta/                       ← Codebook, ADRs
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
│   ├── scripts/                    ← 10 scripts Python
│   ├── schemas/                    ← JSON Schemas (master-record, iconocode, webscout)
│   └── sql/                        ← Migrações SQL
│
├── notebooks/                      ← ANÁLISE (Cap. 6)
│   ├── 01_exploratory.ipynb        ← Distribuição dos indicadores
│   ├── 02_kruskal_wallis.ipynb     ← Regimes × morfologia
│   ├── 03_regression.ipynb         ← Regressão logística ordinal
│   └── 04_correspondence.ipynb     ← Análise de correspondência múltipla
│
├── docs/                           ← DOCUMENTAÇÃO TÉCNICA
│   ├── scripts.md                  ← Referência de scripts
│   ├── adr/                        ← Decisões arquiteturais (3 ADRs)
│   ├── drive-structure.md          ← Organização do Google Drive
│   └── notion-schema.md            ← Esquema do Notion
│
├── website/                        ← Site Ius Gentium (GitHub Pages)
├── examples/                       ← Saídas de exemplo do pipeline
├── sources/                        ← Resultados de pesquisa salvos
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

**Convenção de IDs:**
- `BR-001` a `BR-NNN` — Brasil
- `FR-001` a `FR-NNN` — França
- `DE-001` a `DE-NNN` — Alemanha
- `US-001` a `US-NNN` — EUA
- `UK-001` a `UK-NNN` — Reino Unido
- `BE-001` a `BE-NNN` — Bélgica
- `PT-001` a `PT-NNN` — Portugal
- `EU-001` a `EU-NNN` — Multi-país / Europeana
- `NL-001` a `NL-NNN` — Países Baixos

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

**Saída:** `data/processed/purification.jsonl` (1 registro por linha, com timestamp e assinatura do codificador)

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

### 4.4 Compilar capítulos para DOCX/PDF

```bash
cd vault/tese

# Compilar tese completa para DOCX (ABNT)
make docx

# Compilar capítulo individual
make capitulo-2.docx

# Compilar para PDF (requer LaTeX)
make pdf

# Ver opções disponíveis
make help
```

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
Acervo digital (Gallica, Europeana, Brasiliana...)
        │
        ▼
corpus/corpus-data.json          ← Metadados catalográficos (66 itens)
        │
        ├──► code_purification.py ──► data/processed/purification.jsonl
        │                                     │
        │                                     ▼
        └──► --export-csv ──────────► data/processed/corpus_dataset.csv
                                              │
                                              ▼
                                     notebooks/*.ipynb  (Cap. 6)
```

### Formatos de dados

| Arquivo | Formato | Conteúdo |
|---------|---------|----------|
| `corpus/corpus-data.json` | JSON array | Metadados base (id, título, data, país, suporte, URL, citações) |
| `data/processed/purification.jsonl` | JSONL | Codificação dos 10 indicadores + composto + regime |
| `data/processed/corpus_dataset.csv` | CSV | Junção dos dois acima (para notebooks/SPSS/R) |

### Adicionar novo item ao pipeline

1. Adicionar metadados a `corpus/corpus-data.json`
2. Codificar purificação: `python tools/scripts/code_purification.py --item XX-NNN`
3. Exportar CSV atualizado: `python tools/scripts/code_purification.py --export-csv`
4. (Opcional) Criar ficha Obsidian em `vault/corpus/`

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
| `notion_sync.py` | Sincronizar JSONL ↔ Notion | `pull`, `push`, `sync` |
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
- Branch principal: `main`
- Branches de feature: `claude/nome-da-feature-XXXXX`

### Citações

- No vault (Pandoc): `[@autor2020, p. 42]`
- No manuscrito (ABNT inline): `(AUTOR, 2020, p. 42)`
- Referências BibTeX: `vault/tese/references.bib`

### Codificação de purificação

- Sempre codificar com a imagem aberta no navegador
- Usar o codebook (`data/docs/codebook.md`) em caso de dúvida
- Registrar incertezas no campo `notes`
- Meta: ≥95% de concordância intra-codificador (retestar 10% após 2 semanas)

---

## 10. Decisões arquiteturais (ADRs)

Documentadas em `docs/adr/`:

| ADR | Decisão | Resumo |
|-----|---------|--------|
| 001 | Google Drive como armazém bruto | Imagens ficam no Drive; repositório tem apenas URLs e metadados |
| 002 | Notion como índice do corpus | Notion serve como interface de catalogação; GitHub é canônico |
| 003 | JSONL como formato canônico | 1 registro por linha; fácil de processar, versionar e validar |

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

# Verificar se references.bib existe
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
- `.gitignore` já exclui `*.zip`, `~$*`, `review/`

---

*Manual gerado em 23 de março de 2026. Para a versão mais atualizada, consulte o repositório.*
