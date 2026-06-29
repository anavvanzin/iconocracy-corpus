# Roadmap: Provenância Criptográfica com SciTeX Clew (ICONOCRACY)

**Status:** ARQUIVADO — plano estratégico, não ativo
**Horizonte de ativação:** pós-entrega do manuscrito completo ao orientador (~ago/set 2027)
**Contexto de decisão:** Avaliação realizada em 28/04/2026 após inspeção do repositório `scitex-python` (ver detalhes abaixo)

---

## 0. Por que isto existe

Durante a sessão de 28/04/2026, o pipeline ICONOCRACY foi mapeado contra a arquitetura `scitex.clew` (provenância criptográfica SHA-256) e `scitex.plt.io` (figrecipe + bundles). Foi concluído que:

- **Não vale a pena ativar agora** (corpus ainda mutante, notebooks exploratórios em fluxo).
- **Vale muito como artefato defensivo pré-defesa** (fim de 2027), quando o corpus estiver congelado e os notebooks finais identificados.

Este documento captura o desenho aprovado para ativação futura.

---

## 1. Objetivo

Produzir um DAG de provenância criptograficamente verificável ligando:

```
records.jsonl  →  corpus-data.json  →  notebooks finais  →  vault/tese/imagens/*  →  manuscrito
```

De modo que, na defesa, qualquer figura estatística citada possa ser tracada em segundos até sua fonte de dados bruta, com detecção automática de adulteração.

---

## 2. Pré-requisitos para ativação (gate checklist)

Pré-requisito | Critério de prontidão
|---|---|
| Corpora congelados | `corpus-data.json` e `purification.jsonl` em versão RC ou final (não mais mutantes a cada campanha)
| Notebooks finais identificados | Mapeamento figura→notebook→capítulo concluído ( provavelmente 05–08, excluindo 01–04 exploratórios)
| Padrão de nomes estável | `vault/tese/imagens/*` com convenção `figura_XX_descricao.ext` documentada
| Manuscrito em revisão final | Após entrega ao orientador, antes da defesa |

---

## 3. Arquitetura aprovada (Opção 1 com baseline)

### 3.1 Localização no monorepo

```
hub/iconocracy-corpus/
├── .gitignore              # ignora scitex-clew.db
├── scitex-clew.db          # SQLite append-only (NÃO versionado)
├── scitex-clew.log         # Log human-readable (versionado, opcional)
├── .clewignore             # Padrões a ignorar no tracking
└── tools/
    └── scripts/
        ├── clew_baseline.py   # Script de inicialização do baseline
        └── clew_audit.py      # Script de auditoria pré-defesa
```

### 3.2 Baseline (big bang)

Script único de inicialização:

```python
# tools/scripts/clew_baseline.py
import scitex as stx

stx.clew.start_tracking(
    session_id=f"iconocracy-baseline-{datetime.now().strftime('%Y%m%d')}",
    metadata={
        "records_hash": stx.clew.hash_file("data/processed/records.jsonl"),
        "corpus_hash": stx.clew.hash_file("corpus/corpus-data.json"),
        "purification_hash": stx.clew.hash_file("data/processed/purification.jsonl"),
    }
)
stx.clew.stop_tracking(status="success")
```

### 3.3 Padrão de instrumentação (notebooks finais)

Célula inicial:

```python
import scitex as stx
import uuid
from pathlib import Path

BASE = Path(__file__).parent

stx.clew.start_tracking(
    session_id=f"nb-08-{uuid.uuid4().hex[:6]}",
    parent_session="iconocracy-baseline-YYYYMMDD",  # referência ao baseline
    metadata={
        "notebook": "08_multidimensional_scoring.ipynb",
        "corpus_version": stx.clew.hash_file(BASE / "../../corpus/corpus-data.json"),
    }
)
```

Célula final:

```python
stx.clew.stop_tracking(status="success")
```

Para scripts `tools/scripts/`:

```python
@stx.session
def main():
    ...
```

### 3.4 CLI de consulta (uso pós-run)

```bash
# Status geral
scitex clew status

# Verificar integridade do DAG
scitex clew dag corpus/corpus-data.json

# Traçar provenância de uma figura
scitex clew chain vault/tese/imagens/figura_04_endurecimento.png

# Gerar diagrama Mermaid do DAG
scitex clew mermaid --output vault/tese/provenance-dag.md

# Verificar claim: "Figura 4 deriva de corpus-data.json"
scitex clew verify_claim \
    --file vault/tese/imagens/figura_04_endurecimento.png \
    --session iconocracy-baseline-YYYYMMDD
```

---

## 4. O que NÃO será instrumentado

| Não instrumentar | Motivo |
|---|---|
| Notebooks 01–04 (exploratórios) | Não alimentam figuras do manuscrito |
| Scripts de ingest (`iconocracy-ingest/ingest.py`) | Pipeline de aquisição, não análise |
| Arquivos temporários/cache | `.clewignore` exclui `*.tmp`, `__pycache__`, `.ipynb_checkpoints` |
| Vault/candidatos (notas markdown) | Provenância de texto não é o foco; é de figura estatística |

---

## 5. Expectativas honestas (limites conhecidos)

| Não espere | Por quê |
|---|---|
| Que o Clew escreva metodologia | Ele gera DAGs e hashes; interpretação é humana |
| Que o examinador peça por isso | Em defesas de história do direito penal, rastreabilidade criptográfica é exótica. É **escudo**, não **espada** |
| Proteção absoluta contra fraude | Detecta *alteração*, mas não *má intenção* |
| Sem custo de manutenção | O banco SQLite cresce com sessões; pode precisar de rotação após muitas runs |

---

## 6. Alternativa zero-custo (funciona hoje)

Se a defesa chegar e não houver tempo de ativar o Clew, o pipeline existente já fornece rastreabilidade **procedural** suficiente para a maioria dos tribunais acadêmicos:

- `records.jsonl` ↔ `corpus-data.json` via `records_to_corpus.py`
- `corpus-data.json` ↔ notebooks via convenção de nomes
- Notebooks ↔ figuras via `vault/tese/imagens/*`
- Releases HF como snapshots congelados
- `vault_sync.py`, `build_hf_release.py`, `validate_schemas.py` como gates documentados

O Clew seria upgrade de hardening, não correção de falha.

---

## 7. Gatilho de ativação

Ativar este plano somente quando TODOS forem verdadeiros:

1. [ ] Manuscrito entregue ao orientador (versão considerada "completa")
2. [ ] Corpus-data.json em versão RC ou final (não mais mutante)
3. [ ] Mapeamento figura→notebook→capítulo concluído
4. [ ] Decisão consciente de alocar 2–4h de trabalho para setup e instrumentação

---

## 8. Recursos de referência

- Repositório fonte: `/Users/ana/Research/scitex-python` (commit `1164fd6f`)
- Pacote principal: `scitex[all]` ou `scitex[plt,stats,scholar]`
- Dependência crítica: `scitex-clew>=0.2.5` (disponível via PyPI)
- Documentação: `examples/03_clew.ipynb`, `examples/_legacy/scitex/clew/`
- Licença: AGPL-3.0 (incompatível com distribuição proprietária, mas compatível com uso acadêmico interno)

---

*Arquivado em 28/04/2026. Revisar em ago/2027 ou no gatilho de ativação.*
