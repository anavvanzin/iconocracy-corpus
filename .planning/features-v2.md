# ICONOCRACIA · Companion App v2 — Especificação Técnica

> Data: 2026-09-04  
> Origem: notas de Ana (iconocracia.com)  
> Status: Especificação · aguarda confirmação para issues

---

## 1. Modo "Pathosformel" — linha do tempo por atributo

### Conceito
Selecionar um atributo alegórico (véu, balança, espada, olhos vendados, cetro, coroa, globo, cornucópia etc.) e visualizar sua trajetória diacrônica no corpus como uma **linha do tempo interativa**. Cada ponto na linha é uma imagem do corpus; ao clicar, abre um modal com a anotação Panofsky em três níveis (pré-iconográfico · iconográfico · iconológico).

### Dados existentes
- O schema `master-record.schema.json` já prevê `atributos_iconograficos: string[]` e `pathosformel: string`.
- O schema `iconocode-output.schema.json` define os 3 níveis Panofsky (`pre_iconographic`, `codes`, `interpretation`).
- O corpus remoto tem **335 itens** (`corpus/corpus-data.json`, health check 2026-08-31).
- O `purification.jsonl` tem **286 registros codificados** (85%), mas contém apenas os 10 indicadores de purificação + regime — **não** os dados Panofsky/Pathosformel.
- Débito técnico conhecido: apenas **2,6%** têm Panofsky completo; a grande maioria dos 286 itens codificados tem purificação mas **não** os 3 níveis Panofsky.
- O enriched JSON local (95 itens) é um snapshot defasado; precisa ser regenerado a partir do ledger atual.

### Pipeline de dados necessário
1. **Codificação Panofsky em lote** — rodar IconoCode sobre as entradas pendentes para gerar:
   - `pre_iconographic`: lista de motivos observados
   - `codes`: notações ICONCLASS + rótulos
   - `interpretation`: claims iconográficos com `confidence`
2. **Extração de atributos** — decompor `atributos_iconograficos` em vocabulário controlado (véu, balança, espada, olhos vendados, cetro, coroa, globo, cornucópia, fasces, caduceu, livro, espelho etc.).
3. **Derivação de Pathosformel** — para cada atributo, identificar a **fórmula de pathos** (gesto + objeto + contexto) que se repete e se transforma diacronicamente.
4. **Regeneração do enriched JSON** — merge dos resultados em `corpus-data-enriched.json` a partir dos 335 itens atuais.

### Interface (Companion)
- **Nova aba ou sub-modo** no companion (sugestão: toggle no header do Atlas ou nova aba "Fios").
- **Seletor de atributo**: lista deduplicada de todos `atributos_iconograficos` do corpus.
- **Timeline visual**: eixo horizontal = ano; pontos = itens; cor = regime (fundacional/normativo/militar/contra-alegoria); tamanho = score de endurecimento.
- **Modal de ponto**: imagem + painel Panofsky em 3 abas (pré-iconográfico, iconográfico, iconológico) + citação ABNT + link para o Atlas.
- **Export**: JSON da linha do tempo para importação no Warburg Atlas (formato `mnemosyne/starter-8panels.json`).

### Endpoints necessários (Worker)
- `GET /api/pathosformel/attributes` — lista de atributos únicos com contagem.
- `GET /api/pathosformel/timeline?attribute=velo&country=FR` — itens filtrados por atributo, com Panofsky inline.

---

## 2. Filtro "Gênero / Queer" — camada de contra-alegoria

### Conceito
Um **toggle real** no corpus que, ao ativar, destaca imagens que **desestabilizam a alegoria tradicional**: figuras andróginas, Justitias mães, Repúblicas envelhecidas, figuras masculinas em função atlanteana, substituições atributivas herculeas etc. Não é etiquetagem automática; é a **exposição das triagens de contra-alegoria já realizadas manualmente** como uma camada de leitura sobreposta.

### Dados existentes
- O schema `master-record.schema.json` prevê:
  - `regime_iconocratico: enum["fundacional", "normativo", "militar", "contra-alegoria"]` ✅
  - `genero_atribuido: enum["feminino", "masculino", "neutro", "hibrido", "ausente"]` ✅
  - `familia_alegorica: enum["Virtudes", "Continentes", "Oceanos/Rios", "Nacional", "Outra", "Masculino_Juridico"]` ✅
  - `funcao_atlanteana: boolean` ✅ (v2.3.0)
  - `funcao_da_figura_masculina` e `tipo_agencia_masculina` ✅ (v2.3.0)
  - `disjuncao_representa_governa: boolean` ✅
- O `purification.jsonl` (286 codificados) já contém **10 itens contra-alegoria** (health check 2026-08-31: fundacional 149, normativo 99, militar 28, **contra-alegoria 10**).
- O enriched JSON local (95 itens) **não reflete** esses 10 itens — é um snapshot defasado gerado antes da codificação contra-alegoria.

### Pipeline de dados necessário
1. **Regenerar o enriched JSON** a partir do `purification.jsonl` + `records.jsonl` atual para refletir os 335 itens e os regimes corretos (incluindo os 10 contra-alegoria).
2. **Expandir a codificação v2.3.0** — aplicar campos `genero_atribuido`, `familia_alegorica`, `disjuncao_representa_governa`, `funcao_atlanteana` etc. aos 10 itens já identificados e a candidatos adicionais (Justitia mãe, República velha, figuras andróginas etc.).
3. **Curadoria manual** — a Ana define a lista canônica de itens queer/contra-alegoria; não é tarefa de ML.
4. **Derivação de visual cues** — para cada item no filtro, gerar:
   - Badge "contra-alegoria" no card/thumbnail
   - Destaque de cor diferenciada (`var(--terracotta)`)
   - Tooltip explicando a desestabilização (ex.: "Justitia como mãe: fusão de função jurídica e maternal que quebra a neutra personificação republicana")

### Interface (Companion)
- **Toggle global** no header do corpus: "Contra-alegoria 🏳️‍🌈" (ou ícone de quebra).
- Quando ativo:
  - Grid/Mapa/Atlas filtra para mostrar **apenas** itens com `regime: contra-alegoria` OU `genero_atribuido: hibrido` OU `disjuncao_representa_governa: true`.
  - Itens relevantes ganham borda/badge terracotta.
  - Painel lateral com **ensaiozinho curto** sobre a teoria (Pateman–Mondzain–Goodrich aplicado à figura).
- Quando inativo: corpus volta ao normal, mas itens contra-alegoria ainda mostram badge discreto.

### Endpoints necessários (Worker)
- `GET /api/corpus/data?filter=queer` — retorna itens marcados, com campos `genero_atribuido`, `disjuncao_representa_governa`, `regime_justificativa` inline.

---

## 3. Protocolo Metodológico Público — reprodutibilidade como DH

### Conceito
Publicar **não o texto da tese**, mas o "como reproduzir este corpus": schemas Ajv, scripts de validação, queries DuckDB, decision records de codebook. Isso legitima o trabalho como humanidades digitais e cria um modelo que outros projetos podem adaptar.

### Dados existentes
- **Schemas JSON** (`tools/schemas/`):
  - `master-record.schema.json` — record canônico com 60+ campos
  - `iconocode-output.schema.json` — Panofsky 3 níveis
  - `purification-record.schema.json` — 10 indicadores + regime
  - `webscout-output.schema.json` — metadados de acervo
- **Scripts de validação**: `tools/audit/scripts/validate_schemas.py` (referenciado no schema; verificar existência no repo remoto).
- **Datasets publicados**:
  - `corpus/corpus-data.json` (335 itens, canônico)
  - `data/processed/purification.jsonl` (286 itens, completo para purificação)
  - `data/processed/records.jsonl` (335 itens, metadados base)
  - `tools/audit/data/iconocracy-flags-263actions.json` (débito técnico)
- **Decision records**: `DEC-2026-07-28-COMPOSTO` (legacy `purificacao_composto` deprecado).
- **Taxonomia**: `tools/audit/taxonomy/taxonomy-v0.2-schema.json`.

### Entregáveis do protocolo
1. **`METHOD.md`** na raiz do repo — documento de ~3.000 palavras em inglês + português explicando:
   - Arquitetura do pipeline (WebScout → IconoCode → Purification → Enriched)
   - Versionamento do codebook (v0.1 → v0.2 → v2.2.1 → v2.3.0)
   - Inter-rater reliability e adjudication
   - Como rodar `validate_schemas.py` e `analyze_threads_v2.py`
   - Como citar o corpus (ABNT, Chicago, BibTeX)
2. **`reproducibility/`** — novo diretório com:
   - `schemas/` — cópia canônica dos 4 schemas (ou symlink)
   - `scripts/` — `validate.py`, `migrate.py`, `enrich.py`
   - `queries/` — queries DuckDB para análise exploratória do corpus
   - `decisions/` — ADRs em markdown (ex.: `adr-001-composto-deprecated.md`)
3. **Badge e DOI** — instruções para depositar no Zenodo com DOI e `CITATION.cff`.

### Interface (Companion)
- **Nova aba "Método"** no companion com:
   - Resumo visual do pipeline (diagrama SVG)
   - Download de `METHOD.md`, schemas, e starter notebook DuckDB
   - Contador de versão do codebook e última codificação
   - Link para o GitHub do corpus

---

## Mapeamento de dependências

| Feature | Blocado por | Pode começar agora |
|---------|-------------|-------------------|
| Pathosformel | Codificação Panofsky em lote (2,6% → 100% dos 335 itens) | Design da timeline + endpoint mock com dados stub |
| Filtro Queer | Regenerar enriched JSON a partir do ledger atual (286 codificados → 335 itens) | Toggle na UI + endpoint com flag (dados já existem no purification.jsonl) |
| Protocolo DH | Escrever METHOD.md | Documentar schemas e scripts existentes (trabalho paralelo) |

## Próximos passos sugeridos

1. **Issue #1**: "Regenerar `corpus-data-enriched.json` a partir do ledger atual (335 itens)" — fundação para todas as features; sincroniza enriched com `records.jsonl` + `purification.jsonl`.
2. **Issue #2**: "Implementar endpoint `/api/pathosformel/attributes` e timeline mock" — frontend-first, dados stub; pode ser feito em paralelo.
3. **Issue #3**: "Rodar IconoCode batch sobre entries sem Panofsky (de 2,6% para 100%)" — desbloqueia Pathosformel; priorizar entries francesas (FR-013 a FR-018) e contra-alegoria.
4. **Issue #4**: "Auditar e aplicar codificação v2.3.0 nos 10 itens contra-alegoria" — desbloqueia Filtro Queer; preencher `genero_atribuido`, `funcao_atlanteana`, `disjuncao_representa_governa`.
5. **Issue #5**: "Toggle 'Gênero/Queer' no companion com badge terracotta" — UI; depende da #1 e #4.
6. **Issue #6**: "Escrever METHOD.md + diretório `reproducibility/`" — documentação; trabalho paralelo.

---

*Especificação validada contra health check 2026-08-31. Dados: 335 itens no corpus, 286 codificados, 10 contra-alegoria, 2,6% Panofsky completo.*
