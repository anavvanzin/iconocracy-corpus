# Design: iconocracy-ingest — Health Check Semanal

**Data:** 2026-04-11
**Status:** aprovado
**Autor:** Ana Vanzin + Claude

---

## Objetivo

Agente remoto agendado (Claude Code Scheduled Trigger) que roda semanalmente para verificar a saúde do repositório `iconocracy-corpus`. Valida schemas, verifica consistência de dados, reporta progresso do ENDURECIMENTO, e identifica lacunas no corpus. Entrega: uma GitHub Issue semanal com relatório consolidado.

## Decisões de Design

| Aspecto | Decisão | Justificativa |
|---------|---------|---------------|
| **Nome** | `iconocracy-ingest` | Nome original do trigger |
| **Modelo** | `claude-sonnet-4-6` | Suficiente para scripts + análise; custo menor |
| **Schedule** | `0 12 * * 1` (segunda 12h UTC = 9h BRT) | Início de semana para revisar saúde do projeto |
| **Entrega** | GitHub Issue com label `infra` | Visível no fluxo normal, rastreável, sem poluir git history |
| **Ambiente** | Default (Anthropic Cloud) | — |
| **Repo** | `https://github.com/anavvanzin/iconocracy-corpus` | Monorepo principal |
| **Ferramentas** | `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep` | Conjunto mínimo necessário |

## Escopo — Abordagem A (atual)

### Fase 1 — Validação de Schemas

1. Instalar dependências: `pip install -r requirements.txt`
2. Validar records.jsonl: `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`
3. Validar purification.jsonl: `python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record --verbose`
4. Verificar consistência: contar items em `records.jsonl` vs `corpus-data.json`

### Fase 2 — Status ENDURECIMENTO

5. Rodar `python tools/scripts/code_purification.py --status`
6. Capturar: total codificado, % progresso, items pendentes

### Fase 3 — Análise de Lacunas (básica)

7. Ler `corpus/corpus-data.json`
8. Calcular distribuição por:
   - País (FR, UK, DE, US, BE, BR)
   - Suporte (moeda, selo, monumento, estampa, frontispício, papel-moeda, cartaz)
   - Período (décadas dentro de 1800–2000, com foco em 1880–1920)
9. Identificar categorias sub-representadas (país < 5 items, suporte ausente, décadas sem cobertura)

### Fase 4 — Relatório (GitHub Issue)

10. Criar issue via `gh issue create` com:
    - **Título:** `🏥 Health Check Semanal — YYYY-MM-DD`
    - **Label:** `infra`
    - **Corpo:** seções Validação, Consistência, ENDURECIMENTO, Lacunas, Status Geral

### Semáforo

| Cor | Critério |
|-----|----------|
| 🟢 Verde | Schemas válidos, consistência ok, sem gaps críticos |
| 🟡 Amarelo | Validação ok mas gaps significativos ou ENDURECIMENTO < 50% |
| 🔴 Vermelho | Schema inválido ou inconsistência records↔corpus |

### Formato da Issue

```markdown
## Status Geral: 🟢 / 🟡 / 🔴

## Validação de Schemas
- records.jsonl: ✅/❌ N registros
- purification.jsonl: ✅/❌ N registros

## Consistência
- records.jsonl: N items
- corpus-data.json: N items
- Diferença: N

## ENDURECIMENTO
- Codificados: N/M (X%)
- Pendentes: N items

## Lacunas do Corpus
| País | Items | Período coberto | Gaps notáveis |
|------|-------|----------------|---------------|
| ... | ... | ... | ... |

## Suportes
| Suporte | Items | Observação |
|---------|-------|------------|
| ... | ... | ... |

---
*Gerado automaticamente por iconocracy-ingest*
```

## Extensão Futura — Abordagem B

O prompt pode ser estendido (via `RemoteTrigger update`) para incluir:

- Análise inteligente de gaps com recomendações de arquivos/coleções específicas
- Cruzamento com parâmetros do corpus (países, suportes, período prioritário 1880–1920)
- Sugestões de campanhas de scout baseadas nas lacunas
- Referência a coleções conhecidas (Münzkabinett, BnF Gallica, LOC, etc.)

A estrutura do trigger não muda — apenas o prompt é atualizado.

## Configuração do Trigger

```json
{
  "name": "iconocracy-ingest",
  "cron_expression": "0 12 * * 1",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "env_012MA5gRcvyQsca5c6cBZauB",
      "session_context": {
        "model": "claude-sonnet-4-6",
        "sources": [
          {"git_repository": {"url": "https://github.com/anavvanzin/iconocracy-corpus"}}
        ],
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
      },
      "events": [{ "data": { "uuid": "<generated>", "session_id": "", "type": "user", "parent_tool_use_id": null, "message": { "content": "<prompt>", "role": "user" }}}]
    }
  }
}
```

## Prompt do Agente

Ver seção separada no momento da criação do trigger — o prompt é a parte mais crítica e deve ser self-contained, incluindo:

- Contexto do projeto (o que é o corpus, quais scripts existem)
- Passos exatos a executar
- Formato esperado da issue
- Critérios do semáforo
- Instruções para usar `gh issue create`
