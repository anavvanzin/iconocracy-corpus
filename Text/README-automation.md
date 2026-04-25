# Automation Scripts

Esta pasta contém scripts de automação para monitoramento de erros e extração de memória semântica.

## auto_issue.py

Monitora logs de erro e cria automaticamente issues no GitHub quando um erro se repete N vezes.

### Uso

```bash
# Modo dry-run (visualiza sem criar issues)
python tools/scripts/auto_issue.py --dry-run

# Criar issues para erros com 3+ ocorrências nas últimas 24h
python tools/scripts/auto_issue.py --log logs/errors.log --threshold 3

# Janela de tempo customizada (últimas 48 horas)
python tools/scripts/auto_issue.py --window 48

# Todas as opções
python tools/scripts/auto_issue.py \
  --log logs/errors.log \
  --threshold 5 \
  --window 24 \
  --dry-run
```

### Parâmetros

- `--log FILE`: Caminho do arquivo de log (padrão: `logs/errors.log`)
- `--threshold N`: Número mínimo de ocorrências para criar issue (padrão: 3)
- `--window HOURS`: Janela de tempo em horas (padrão: 24)
- `--dry-run`: Modo de visualização sem criar issues

### Pré-requisitos

- GitHub CLI (`gh`) instalado e autenticado
- Permissões para criar issues no repositório

### Comportamento

1. Parseia o arquivo de log e extrai tracebacks Python
2. Normaliza assinaturas de erro (remove caminhos e IDs variáveis)
3. Agrupa erros idênticos e conta ocorrências
4. Verifica se já existe issue para o padrão de erro
5. Cria issue com:
   - Título: assinatura normalizada
   - Body: resumo, ocorrências recentes, ações sugeridas
   - Labels: `bug`, `auto-generated`

## semantic_memory_to_schema.py

Extrai conceitos semânticos de notas Obsidian e gera schema JSON validado.

### Uso

```bash
# Extrair memória semântica do vault padrão
python tools/scripts/semantic_memory_to_schema.py

# Vault customizado com validação
python tools/scripts/semantic_memory_to_schema.py \
  --vault vault/tese \
  --output data/semantic-memory.json \
  --validate

# Apenas gerar schema (sem extração)
python tools/scripts/semantic_memory_to_schema.py \
  --schema-output tools/schemas/semantic-memory.schema.json
```

### Parâmetros

- `--vault PATH`: Caminho do vault Obsidian (padrão: `vault/`)
- `--output FILE`: Arquivo JSON de saída (padrão: `data/semantic-memory.json`)
- `--schema-output FILE`: Caminho do schema (padrão: `tools/schemas/semantic-memory.schema.json`)
- `--validate`: Validar saída contra schema
- `--version X.Y.Z`: String de versão (padrão: `1.0.0`)

### Formato de Extração

O script busca nos arquivos `.md` do vault por padrões como:

```markdown
## Conceito X

Definição: Um conceito representa...

Aliases: Conceito-X, conceito_x
```

Extrai automaticamente:
- **ID**: versão normalizada do label (`conceito-x`)
- **Label**: título do conceito
- **Definition**: texto após "Definição:" ou "Definition:"
- **Aliases**: sinônimos listados
- **Related Concepts**: wikilinks `[[outros conceitos]]`
- **Evidence**: citações/quotes no formato `> texto`
- **Source Note**: nome do arquivo `.md` de origem

### Schema Gerado

O schema JSON Draft 2020-12 valida:

- **version**: `string` no formato `X.Y.Z`
- **generated_at**: `string` formato ISO datetime
- **total_concepts**: `integer` ≥ 0
- **concepts**: array de objetos com:
  - `id`: `string` pattern `^[a-z0-9-]+$` (required)
  - `label`: `string` ≥ 1 caractere (required)
  - `definition`: `string` ≥ 10 caracteres (required)
  - `aliases`: array de strings
  - `related_concepts`: array de strings
  - `source_note`: `string` (required)
  - `evidence`: array de strings

### Integração com Pipeline

Esses scripts podem ser integrados ao pipeline de CI/CD:

```yaml
# .github/workflows/error-monitor.yml
name: Error Monitor
on:
  schedule:
    - cron: '0 */6 * * *'  # A cada 6 horas

jobs:
  check-errors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Monitor errors
        run: |
          python tools/scripts/auto_issue.py \
            --log logs/errors.log \
            --threshold 3
        env:
          GH_TOKEN: ${{ github.token }}
```

```yaml
# .github/workflows/semantic-memory.yml
name: Update Semantic Memory
on:
  push:
    paths:
      - 'vault/**/*.md'

jobs:
  update-memory:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Extract semantic memory
        run: |
          conda run -n iconocracy python tools/scripts/semantic_memory_to_schema.py --validate
      - name: Commit if changed
        run: |
          git add data/semantic-memory.json tools/schemas/semantic-memory.schema.json
          git diff --staged --quiet || git commit -m "chore: update semantic memory"
          git push
```

## Próximos Passos

1. **Testar scripts em branch de feature**
   ```bash
   git checkout -b feat/automation-scripts
   python tools/scripts/auto_issue.py --dry-run
   python tools/scripts/semantic_memory_to_schema.py --validate
   ```

2. **Criar log de teste para validação**
   ```bash
   mkdir -p logs
   # Adicionar tracebacks de teste em logs/errors.log
   ```

3. **Configurar GitHub Actions**
   - Criar workflows para monitoramento automatizado
   - Adicionar secrets necessários

4. **Documentar no AGENTS.md**
   - Adicionar seção sobre automação
   - Linkar para esta documentação
