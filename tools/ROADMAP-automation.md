# Roadmap — Automação e Infraestrutura

Plano de melhorias para o ecossistema ICONOCRACIA após a implementação dos scripts de automação (`auto_issue.py`, `semantic_memory_to_schema.py`).

## Fase 1: Validação e Testes (atual → +1 semana)

### 1.1 Testar scripts em branch de feature
- [ ] Criar branch `feat/automation-testing`
- [ ] Gerar log de teste com tracebacks sintéticos
- [ ] Executar `auto_issue.py --dry-run` e validar formato das issues
- [ ] Executar `semantic_memory_to_schema.py --validate` no vault real
- [ ] Documentar edge cases e limitações encontradas

### 1.2 Integração com pipeline existente
- [ ] Adicionar hooks pós-validação em `validate_schemas.py`
- [ ] Criar script `tools/scripts/run_all_validations.sh` que chama:
  - `validate_schemas.py` (corpus JSON)
  - `semantic_memory_to_schema.py --validate` (memória semântica)
  - `auto_issue.py --dry-run` (relatório de erros pendentes)
- [ ] Testar integração com `make validate` no Makefile

### 1.3 Documentação expandida
- [ ] Adicionar seção "Automation" ao `AGENTS.md` do hub
- [ ] Criar exemplos de uso em `tools/scripts/examples/`
- [ ] Documentar padrões de log aceitos pelo parser de erros
- [ ] Adicionar FAQ sobre falsos positivos e normalização de erros

## Fase 2: CI/CD e GitHub Actions (+1–2 semanas)

### 2.1 Workflow de monitoramento de erros
```yaml
# .github/workflows/error-monitor.yml
- Trigger: schedule (cron: '0 */6 * * *')
- Jobs:
  - Parse logs/errors.log acumulados
  - Executar auto_issue.py com threshold 3
  - Postar resumo como comment em issue dedicada (#automation-log)
```

### 2.2 Workflow de atualização de memória semântica
```yaml
# .github/workflows/semantic-memory.yml
- Trigger: push em vault/**/*.md
- Jobs:
  - Extrair conceitos com semantic_memory_to_schema.py
  - Validar contra schema
  - Commit automático se houver mudanças
  - Criar PR se número de conceitos aumentar >10%
```

### 2.3 Workflow de release
```yaml
# .github/workflows/release.yml
- Trigger: tag vX.Y.Z
- Jobs:
  - Rodar todas as validações
  - Gerar semantic-memory.json versionado
  - Publicar artefatos em GitHub Releases
  - Sincronizar com Hugging Face (warholana/iconocracy-corpus)
```

## Fase 3: Melhorias nos Scripts (+2–4 semanas)

### 3.1 auto_issue.py — Features adicionais
- [ ] Suporte para múltiplos formatos de log (JSON, syslog, structured logging)
- [ ] Detecção de padrões além de Python tracebacks:
  - JavaScript stack traces
  - HTTP 500 errors
  - Database connection failures
  - Memory/disk full errors
- [ ] Integração com serviços de monitoring (Sentry, Datadog)
- [ ] Auto-atribuição de issues baseada em CODEOWNERS
- [ ] Priorização automática (critical/high/medium/low) baseada em frequência e impacto
- [ ] Detecção de regressão (erro que já foi resolvido voltou)

### 3.2 semantic_memory_to_schema.py — Features adicionais
- [ ] Extração de relacionamentos estruturados (is-a, part-of, related-to)
- [ ] Detecção de conceitos duplicados por similaridade semântica
- [ ] Geração de grafo de conhecimento (NetworkX → GraphML)
- [ ] Exportação para formato RDF/OWL para web semântica
- [ ] Integração com Iconclass (mapeamento automático de conceitos → códigos)
- [ ] Versionamento diferencial (diff entre versões de memória)
- [ ] Estatísticas de cobertura (% de notas com conceitos extraídos)

### 3.3 Novo script: knowledge_graph_viz.py
Gerar visualizações interativas do grafo de conhecimento:
- Força-directed layout (D3.js)
- Clusters por domínio (direito penal / iconografia / metodologia)
- Timeline de evolução conceitual
- Integração com Obsidian Graph View

## Fase 4: Infraestrutura de Produção (+4–8 semanas)

### 4.1 Logging estruturado centralizado
- [ ] Migrar de logs ad-hoc para structured logging (Python `logging` + JSON formatter)
- [ ] Centralizar logs em `logs/` com rotação automática
- [ ] Criar dashboard de observabilidade (Grafana + Loki ou ELK stack)

### 4.2 Testes automatizados
```
tests/
├── unit/
│   ├── test_auto_issue.py
│   └── test_semantic_memory.py
├── integration/
│   ├── test_full_pipeline.py
│   └── test_github_api.py
└── fixtures/
    ├── sample_errors.log
    └── sample_vault/
```

### 4.3 Performance e escalabilidade
- [ ] Benchmark extração de memória semântica em vault com 1000+ notas
- [ ] Paralelizar parsing de logs grandes (multiprocessing)
- [ ] Cache de conceitos extraídos (evitar re-parse de notas não modificadas)
- [ ] Compressão de logs antigos (gzip em logs/ após 30 dias)

### 4.4 Segurança
- [ ] Sanitização de dados sensíveis em logs (emails, tokens, paths absolutos)
- [ ] Validação de entrada para prevenção de injeção (gh CLI)
- [ ] Rate limiting para criação de issues (máx 10/hora)
- [ ] Assinatura criptográfica de releases (GPG)

## Fase 5: Integração Avançada (+8–12 semanas)

### 5.1 Agente autônomo de manutenção
Script `tools/scripts/maintenance_agent.py` que executa periodicamente:
1. Roda todas as validações
2. Detecta erros recorrentes via `auto_issue.py`
3. Sugere correções via LLM (Claude Code / GitHub Copilot)
4. Cria branch + PR com fix proposto
5. Espera aprovação humana para merge

### 5.2 Dashboard web
Interface em Streamlit/Gradio para:
- Status do corpus (145 items, última sync, cobertura)
- Logs de validação em tempo real
- Visualização do grafo de conhecimento
- Busca semântica por conceitos
- Admin: trigger manual de pipelines

### 5.3 MCP server dedicado
Criar `mcp-iconocracy-automation` com ferramentas:
- `validate_corpus` → roda todas as validações
- `extract_memory` → extrai memória semântica
- `check_issues` → lista issues auto-geradas
- `search_concepts` → busca no grafo de conhecimento
- `trigger_sync` → sincroniza com HF/GitHub

## Métricas de Sucesso

**Fase 1-2 (Fundação)**
- [ ] 100% dos scripts com testes unitários
- [ ] CI/CD rodando sem falhas por 2 semanas
- [ ] ≥5 conceitos únicos extraídos do vault

**Fase 3-4 (Maturidade)**
- [ ] Tempo de detecção de erro < 6h (via GitHub Actions)
- [ ] Taxa de falsos positivos < 5% (issues criadas inadequadamente)
- [ ] Cobertura de extração ≥80% das notas com definições

**Fase 5 (Excelência)**
- [ ] Agente autônomo cria ≥1 PR útil/mês
- [ ] Dashboard acessível publicamente
- [ ] MCP server integrado em ≥2 workflows

## Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| GitHub CLI rate limiting | Alto | Média | Implementar exponential backoff |
| Vault parsing quebrar em notas mal-formadas | Médio | Alta | Validação prévia + fallback gracioso |
| Conceitos duplicados | Baixo | Alta | Normalização + deduplicação por embedding |
| Logs gigantes | Médio | Média | Rotação + compressão + sampling |
| Dependência de APIs externas | Alto | Baixa | Cache local + modo offline |

## Próximos Passos Imediatos

1. **Esta semana**
   - [x] Criar `auto_issue.py` e `semantic_memory_to_schema.py`
   - [x] Documentar em `README-automation.md`
   - [ ] Testar em logs/vault reais
   - [ ] Criar branch `feat/automation-testing`

2. **Próxima semana**
   - [ ] Implementar testes unitários básicos
   - [ ] Criar workflow GitHub Actions inicial
   - [ ] Adicionar seção ao `AGENTS.md`

3. **Mês 1**
   - [ ] Rodar em produção com monitoramento
   - [ ] Iterar baseado em feedback
   - [ ] Planejar Fase 3

---

**Última atualização**: 2026-04-15  
**Responsável**: Ana Vanzin  
**Revisão**: trimestral
