# Task: Iconocracy Predictor — API de Score de Endurecimento (ICONOCRACIA)

Expor o framework analítico da tese como serviço: usuária envia imagem de um monumento/alegoria política contemporânea → sistema devolve **Endurecimento Score (0–30)**, os 10 indicadores individuais (0–3) e classificação num dos 4 regimes. Demonstra a relevância contemporânea do framework como ferramenta de análise político-jurídica.

## Infra existente (verificada 2026-08-24, repo `iconocracy-corpus`)

- **Codebook canônico**: `data/docs/codebook.md` — definições ordinais 0–3 dos 10 indicadores (`desincorporacao`, `rigidez_postural`, `dessexualizacao`, `uniformizacao_facial`, `heraldizacao`, `enquadramento_arquitetonico`, `apagamento_narrativo`, `monocromatizacao`, `serialidade`, `inscricao_estatal`).
- **`tools/scripts/code_purification.py`**: CLI interativo de codificação humana; grava no ledger canônico `data/processed/purification.jsonl`.
- **Skill `iconocode-analyze`**: análise visual por agente (visão LLM + codebook + leitura Panofsky 3 níveis) que produz **draft JSON** compatível com `master-record.purificacao` — contrato a reutilizar.
- **Regimes**: `fundacional | normativo | militar | contra-alegoria` (enum real do corpus).
- Env Python: conda `iconocracy`, path version-agnostic `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python`.

## Requisitos

### Serviço
1. **FastAPI** mínimo (`tools/predictor/` no repo), 2 endpoints:
   - `POST /predict` — multipart imagem (ou JSON com URL de imagem) → resposta:
     ```json
     {
       "endurecimento_score": 0,
       "indicadores": {"desincorporacao": 0, "...": 0},
       "regime": "fundacional",
       "confidence": "low|medium|high",
       "panofsky": {"pre_iconografico": "…", "iconografico": "…", "iconologico": "…"},
       "disclaimer": "draft automatizado — não é codificação formal do corpus"
     }
     ```
   - `GET /health`.
2. **Motor**: visão LLM (API Anthropic — consultar skill `claude-api` para model id atual; chave via env var, nunca hardcoded) prompted com o codebook verbatim; score = soma dos 10 indicadores; regime inferido pelos mesmos critérios do codebook.
3. **UI demo opcional**: página HTML estática de upload consumindo a API (fase 2).

### Guardrails (inegociáveis)
- **NUNCA gravar em `data/processed/purification.jsonl`** nem em `corpus/corpus-data.json` — são ledgers canônicos (hooks protegem). Output é sempre draft efêmero devolvido ao cliente.
- Resposta sempre carrega o `disclaimer` de que codificação formal só acontece via `code_purification.py` com coder humano.
- Imagens enviadas não são persistidas no repo (hook bloqueia binários em `data/raw/`); processar em memória/tmp.

### Validação
- Testar contra ≥5 itens já codificados do corpus (ids conhecidos de `purification.jsonl`) e reportar concordância indicador-a-indicador (tolerância ±1) — baseline de sanidade, não IRR formal.

## Critérios de aceite
- `POST /predict` com imagem retorna JSON válido no schema acima em <60s.
- Score sempre = soma dos indicadores; regime sempre no enum de 4 valores.
- Nenhuma escrita nos ledgers canônicos em nenhum caminho de código.
- README curto em `tools/predictor/` com comando de run local (uvicorn) e exemplo curl.
