# CLAUDE.md — Corpus Scout Agent
# ICONOCRACY · PPGD/UFSC · anavvanzin/iconocracy-corpus

## Papel deste projeto

Este é o ambiente de trabalho do agente CORPUS SCOUT para a tese
ICONOCRACY: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX).

Ao operar neste diretório, o Claude assume automaticamente o papel do
Corpus Scout conforme definido em SKILL.md. Não é necessário reintroduzir
o papel a cada sessão.

---

## Estrutura de diretórios esperada

```
iconocracy-corpus/
├── CLAUDE.md                  ← este arquivo
├── SKILL.md                   ← definição do agente
├── data/
│   ├── raw/                   ← symlinks → SSD (ver abaixo)
│   │   ├── BR/ → /Volumes/ICONOCRACIA/corpus/imagens/BR/
│   │   ├── FR/ → /Volumes/ICONOCRACIA/corpus/imagens/FR/
│   │   ├── UK/ → /Volumes/ICONOCRACIA/corpus/imagens/UK/
│   │   ├── DE/ → /Volumes/ICONOCRACIA/corpus/imagens/DE/
│   │   ├── US/ → /Volumes/ICONOCRACIA/corpus/imagens/US/
│   │   └── BE/ → /Volumes/ICONOCRACIA/corpus/imagens/BE/
│   ├── interim/               ← dados em processamento
│   └── processed/
│       └── records.jsonl      ← registros mestre do corpus
├── vault/                     ← notas Obsidian geradas pelo Scout
│   ├── candidatos/            ← notas SCOUT-XXX
│   └── sessoes/               ← notas SCOUT-SESSION-XXX
└── tools/
    └── scripts/               ← scripts de sync e processamento
```

---

## SSD externo ICONOCRACIA

As imagens brutas do corpus ficam no SSD externo (`/Volumes/ICONOCRACIA`),
acessíveis via symlinks em `data/raw/[PAIS]/`. O SSD também armazena:

- `corpus/imagens/` — imagens brutas por país (destino dos symlinks)
- `corpus/metadados/` — JSONs intermediários
- `referencias/zotero-storage/` — PDFs linkados do Zotero
- `backups/github/` — git mirror do repo
- `backups/vault/` — snapshots datados do vault

**Antes de salvar imagens em `data/raw/`**, verificar se o SSD está montado:
```bash
test -d /Volumes/ICONOCRACIA/corpus/imagens && echo "SSD montado" || echo "SSD ausente"
```

Se o SSD não estiver montado, salvar a imagem em `vault/assets/` temporariamente
e marcar com `#mover-para-ssd`.

**Backup manual:**
```bash
bash /Volumes/ICONOCRACIA/backups/backup-iconocracia.sh
```

---

## Comportamento padrão

Quando a pesquisadora digitar qualquer um dos seguintes, execute
diretamente sem pedir confirmação:

- `campanha N` → executa a campanha N conforme SKILL.md §7
- `scout [descrição livre]` → interpreta como query e executa
- `auditoria` → executa Campanha 16 com os arquivos em vault/candidatos/
- `lacunas` → idem

Quando a pesquisadora digitar `salvar`, grave a última nota gerada
em vault/candidatos/ com o nome correto (SCOUT-[ID] [título].md).

Quando a pesquisadora digitar `sessão`, grave a nota de síntese
em vault/sessoes/ com o nome SCOUT-SESSION-[data].md.

---

## Rastreabilidade — regra inviolável

Cada item do corpus deve ser rastreável em três pontos:

| Onde | O quê |
|---|---|
| `data/raw/[pais]/` | arquivo de imagem bruto (jpg/png/tif) |
| `vault/candidatos/` | nota Obsidian com metadados e análise |
| `data/processed/records.jsonl` | registro mestre em JSON |

O Scout gera as notas Obsidian. O sync para records.jsonl é feito
pelo script `tools/scripts/notion_sync.py` (a desenvolver).

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

## Pipeline de Ingestão (iconocracy-ingest/)

Pipeline OCR para material escaneado de acervos. Localizado em `iconocracy-ingest/`.

### Uso rápido

```bash
# Processar novo lote de digitalizações
python3 iconocracy-ingest/ingest.py /caminho/do/lote

# Preview sem processar
python3 iconocracy-ingest/ingest.py /caminho/do/lote --dry-run

# Threshold de confiança mais rigoroso
python3 iconocracy-ingest/ingest.py /caminho/do/lote --confidence 70 -v

# Bridge: CSV do ingest → corpus-data.json (dry run)
python3 -m iconocracy-ingest.modules.corpus_bridge

# Bridge: escrever no corpus
python3 -m iconocracy-ingest.modules.corpus_bridge --write
```

### Módulos

| Módulo | Função |
|--------|--------|
| `ingest.py` | CLI principal (--dry-run, --confidence, --no-copy, --verbose) |
| `config.py` | Configuração centralizada (SOURCE_CODES, thresholds) |
| `modules/file_utils.py` | Descoberta de arquivos, SHA-256, detecção de fonte |
| `modules/ocr_engine.py` | Detecção de idioma + Tesseract OCR com confiança por página |
| `modules/caption_extractor.py` | Extração multilíngue de legendas (PT, ES, FR, IT, EN) |
| `modules/renamer.py` | Renomeação: {SOURCE}_{YEAR}_{SEQ:04d}_{stem}.{ext} |
| `modules/csv_manager.py` | CSV mestre com deduplicação SHA-256 |
| `modules/quality_report.py` | Relatório HTML para páginas com baixa confiança OCR |
| `modules/corpus_bridge.py` | Bridge CSV → corpus-data.json com IDs automáticos |

### Fluxo completo

```
acervo digital → ingest.py → master CSV → corpus_bridge.py → corpus-data.json → IconoCode
```

Para adicionar nova instituição-fonte, editar `SOURCE_CODES` em `config.py`.

---

## Ferramentas disponíveis para o agente

- `web_search` — busca em acervos e bases digitais
- `web_fetch` — acessa URLs de imagens IIIF e páginas de acervos
- `bash_tool` — salva notas em vault/, move arquivos, roda scripts
- `create_file` — cria notas .md em vault/candidatos/ e vault/sessoes/

---

## Notas de sessão anteriores

Consultar vault/sessoes/ para contexto de buscas já realizadas
antes de iniciar nova campanha — evita duplicatas e orienta gaps.
