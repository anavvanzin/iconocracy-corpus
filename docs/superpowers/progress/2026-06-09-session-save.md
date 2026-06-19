# Sessão 2026-06-09 — ICONOCRACIA

**Modelo:** deepseek-v4-flash-free via OpenCode Zen
**Workspace:** ~/Research/hub/iconocracy-corpus
**Branch:** data/reacquire-images-batch2-iiif-20260609

---

## Feito hoje

### E1 Pathosformel (IMES)
- `tools/scripts/e1_pathosformel_batch.py` criado — batch runner Gemma-4 via Ollama
- Batch de 52 itens sem purificação rodado com sucesso (52/52, 0 erros)
- Output: `data/processed/pathosformel_index.jsonl` — 52 itens codificados
- **23 itens com scores válidos** (média 2.37)
- **29 itens com score 0.0** — descrições webscout insuficientes
- Schema validado: 10 indicadores int 0-3, purificacao_composto float, regime_iconocratico str

### E2 Recode dos 29 zeros
- Diagnóstico: summaries muito curtos (3-84ch)
- `tools/scripts/e1_recode_zeros.py` — tentativa com vault notes + thumbnails
- Falhou: thumbnails sem acesso, vault notes ainda insuficientes

### E3 Firecrawl Recode (rodando)
- `tools/scripts/e3_firecrawl_recode.py` criado
- Extrai descrições via Firecrawl CLI de cada URL
- Cacheia em `data/processed/fc_descriptions/`
- Re-codifica com Gemma-4 usando descrições reais
- Background: PID 16259, ~30 min restantes (proc_22c393ad7769)
- 5/29 cacheados até o momento

### Ferramentas
- **Firecrawl CLI** instalado (`npx -y firecrawl-cli@latest init --all --browser`)
- 30 skills Firecrawl instaladas
- `web_extract` e `web_search` funcionais
- Descrições extraídas com sucesso de: Met Museum, V&A, Wikimedia, Google Arts & Culture, MHN, Gallica

### Capítulo 6 — §6.1 Reescrito
- Arquivo: `vault/tese/capitulo-6.md`
- Substituído texto baseado em 145 itens por dados reais de **265 registros / 213 codificados**
- Distribuição geográfica atualizada: França 58, Brasil 35, EUA 25, Alemanha 21...
- Médias por regime: fundacional 0.76, normativo 0.89, militar 1.20, contra-alegoria 0.62
- Frontmatter: 1200 → **1580 palavras** (+380)
- Nota: as seções §6.2-6.6 ainda referenciam dados antigos — precisam de atualização

### IRR Re-run Design
- Documento criado: `docs/decisions/IRR-RE-RUN-DESIGN-2026-06-09.md`
- Especificações:
  - Amostra: 25-30 itens estratificada por regime
  - 100% imagens reais
  - Rater-2 cego com modelo cross-modelo (recomendado)
  - Krippendorff α ≥ 0.667 pooled + por indicador
  - Scripts a criar: `irr_sample.py` + `irr_rater2_batch.py`

### Firecrawl descriptions salvas
- `docs/superpowers/progress/2026-06-09-firecrawl-descriptions.md`

---

## Pendente (quando voltar)

1. **Verificar E3 recode** — se terminou, revisar scores dos 29 itens
2. **Se necessário, terceira passagem** com Firecrawl manual pros que ainda falharem
3. **Criar scripts IRR:**
   - `tools/scripts/irr_sample.py` — amostragem estratificada
   - `tools/scripts/irr_rater2_batch.py` — rater-2 cego em modelo alternativo
4. **Atualizar §6.2-§6.6** com dados do corpus expandido
5. **Validar schema** do `pathosformel_index.jsonl` com `validate_schemas.py`
6. **Responder 4 decisões pendentes** do plano mensal:
   - Cadência-âncora
   - Protocolo `#no-image`
   - Re-aquisição numismática
   - Pranchas E3

---

## Artefatos criados hoje

| Artefato | Local |
|----------|-------|
| E1 batch runner | `tools/scripts/e1_pathosformel_batch.py` |
| E2 recode (bugado) | `tools/scripts/e1_recode_zeros.py` |
| E3 recode (rodando) | `tools/scripts/e3_firecrawl_recode.py` |
| Pathosformel index | `data/processed/pathosformel_index.jsonl` |
| FC descriptions (cache) | `data/processed/fc_descriptions/*.txt` |
| FC extracted (ref) | `docs/superpowers/progress/2026-06-09-firecrawl-descriptions.md` |
| IRR re-run design | `docs/decisions/IRR-RE-RUN-DESIGN-2026-06-09.md` |
| Cap.6 §6.1 atualizado | `vault/tese/capitulo-6.md` |

---

## Notas técnicas

- Gemma-4 via Ollama: ~60s/item com modelo quente, usa `thinking` field se prompt longo
- Solução: prompt minimalista, `stream: false`, `num_predict: 2048`, temperature 0.1
- Python buffering em background: usar `PYTHONUNBUFFERED=1 python3 -u` ou `-u` flag
- `search_files` e `read_file` preferíveis a grep/cat em terminal
- API keys expostas acidentalmente: limpar memória imediatamente
