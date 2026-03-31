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
│   ├── raw/                   ← imagens brutas por país
│   │   ├── BR/
│   │   ├── FR/
│   │   ├── UK/
│   │   ├── DE/
│   │   ├── US/
│   │   └── BE/
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

## Ferramentas disponíveis para o agente

- `web_search` — busca em acervos e bases digitais
- `web_fetch` — acessa URLs de imagens IIIF e páginas de acervos
- `bash_tool` — salva notas em vault/, move arquivos, roda scripts
- `create_file` — cria notas .md em vault/candidatos/ e vault/sessoes/

---

## Notas de sessão anteriores

Consultar vault/sessoes/ para contexto de buscas já realizadas
antes de iniciar nova campanha — evita duplicatas e orienta gaps.
