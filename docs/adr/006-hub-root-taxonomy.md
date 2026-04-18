# ADR 006 — Hub Root Taxonomy and Derived Artifact Boundaries

Status: accepted
Data: 2026-04-17
Escopo: `/Users/ana/Research/hub/iconocracy-corpus`

## Contexto

O hub acumulou, no mesmo root:
- superfícies canônicas da tese
- symlinks de compatibilidade para outros buckets do workspace `Research/`
- artefatos derivados
- scripts one-off
- notas/guias de infraestrutura
- restos históricos com nomes pouco descritivos

Isso criou drift entre documentação, topologia real e política de geração de artefatos.

## Decisão

O root do hub passa a obedecer à seguinte taxonomia.

### 1. Superfícies canônicas
Devem permanecer no root e ser tratadas como parte do contrato operacional do hub:
- `corpus/`
- `data/`
- `docs/`
- `tese/`
- `tools/`
- `vault/`
- arquivos de governança e instrução (`README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `SCHEMA.md`, `CITATION.cff`, `LICENSE`, `SECURITY.md`)

### 2. Superfícies derivadas ou de pipeline
Podem permanecer no root se forem estáveis e documentadas, mas não são fonte primária:
- `deploy/`
- `examples/`
- `iconocracy-ingest/`
- artefatos derivados explícitos dentro de `corpus/` e `data/processed/`

### 3. Symlinks de compatibilidade
São permitidos no root apenas quando apontam para buckets canônicos do workspace `Research/` e devem ser sempre documentados como symlinks:
- `Atlas`
- `indexing`
- `iurisvision`
- `js-genai`

### 4. Superfícies experimentais documentadas
Podem permanecer no root se tiverem papel recorrente e documentação mínima:
- `concepts/`
- `entities/`
- `gallery/`
- `notebooks/`
- `shared/`
- `DOCKER_OPTIMIZATION_GUIDE.md`

### 5. Material legado ou one-off
Não deve ocupar o root com nomes ambíguos. Deve ser realocado para `archive/` ou para uma superfície canônica adequada.

Aplicações imediatas desta ADR:
- `PHD/` sai do root e vai para `archive/root-legacy/PHD/`
- `fix_records_schema.py` sai do root e vai para `archive/root-legacy/scripts/`
- `biblio/ICONOCRACY_Cap3.bib` sai do root e vai para `tese/bibliografia/`
- `companion-data.json` no root deixa de existir como duplicata; o ponto derivado canônico passa a ser `corpus/companion-data.json`

## Política de localização de documentos

### Planos
- `docs/plans/` é o local canônico para planos de implementação, refactor, comparação e decisão operacional.

### Specs/guias reutilizáveis
- `docs/superpowers/specs/` é reservado para specs, guias de avaliação, guias operacionais reutilizáveis e documentos de referência estruturados.

### Não usar
- `docs/superpowers/plans/` não é um local canônico do repositório.

## Política de artefatos derivados

1. Nenhum artefato derivado pode disputar semanticamente com o contrato canônico.
2. Se um artefato for necessário para app/release, ele deve ter um único local canônico documentado.
3. Duplicatas derivadas em múltiplos diretórios devem ser eliminadas.
4. Lockfiles e logs de execução só permanecem rastreados se houver justificativa explícita de reprodutibilidade.

## Consequências

### Positivas
- root menos ambíguo
- documentação convergente
- menor risco de tratar material experimental como canônico
- menor risco de drift em caminhos legados

### Custos
- algumas referências internas precisam ser atualizadas
- certos artefatos históricos continuam existindo, mas fora do root
- será necessário manter a política de artefatos gerados alinhada com `.gitignore` e `.dockerignore`

## Relação com outras decisões

- Esta ADR complementa `docs/OPERATING_MODEL.md`
- Esta ADR não altera o contrato de dados:
  - `data/processed/records.jsonl`
  - `corpus/corpus-data.json`
  - `data/processed/purification.jsonl`
  - `vault/candidatos/`
