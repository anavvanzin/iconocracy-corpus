# IMES Pipeline Design — Iconocracia Metodologia Estratificada

**Date:** 2026-06-05  
**Status:** Approved for implementation  
**Author:** Ana Vanzin + Hermes Agent  
**Related:** Apr 23 "MONGES ATLAS" session (Approach 3 selected)

---

## 1. Visão Geral

Pipeline de 5 estágios que transforma o corpus bruto (265 registros) em **pranchas-atlas validadas** prontas para compilação na tese, usando o protocolo IMES (Iconocracia como Dispositivo Metodológico Estratificado).

| Estágio | Nome | Entrada Principal | Saída Principal | Ferramenta |
|---------|------|-------------------|-----------------|------------|
| **E1** | Extração de Pathosformel | `corpus/corpus-data.json` | `data/processed/pathosformel_index.jsonl` | `iconocode-batch` skill |
| **E2** | Clustering → Regimes Visuais | `pathosformel_index.jsonl` + seeds | `data/processed/regimes_visuais.yaml` | `cluster_rv.py` (novo) |
| **E3** | Constelação de Pranchas | `regimes_visuais.yaml` + editor humano | `docs/pilots/pranchas/rv-XX-*.yaml` | `prancha-template.yaml` + editor |
| **E4** | Validação (Quality Gate) | Pranchas YAML | Relatório + status atualizado | `validate_pranchas.py` (novo) |
| **E5** | Exportação para Tese | Pranchas validadas | `vault/tese/cap-XX-pranchas.tex` + DOCX | `pranchas_to_latex.py` + `compilar-tese` |

---

## 2. E1 — Extração de Pathosformel (LLM Batch)

### 2.1 Objetivo
Preencher o campo `pathosformel` para **todos os 265 itens** do corpus, usando vocabulário livre (bottom-up).

### 2.2 Skill Base
`iconocode-batch` (já existe em `~/.hermes/skills/research/iconocode-batch/`) — orquestra `iconocode-analyze` em lotes paralelos de até 5 itens.

### 2.3 Entrada
`corpus/corpus-data.json` — campos por item:
```json
{
  "id": "BR-RS-JUST-1891-001",
  "title": "Alegoria da República",
  "date": "1896",
  "creator": "Manuel Lopes Rodrigues",
  "country": "BR",
  "support": "pintura-oleo",
  "url": "https://commons.wikimedia.org/...",
  "pathosformel": ""  // vazio → extrair; preenchido → pular
}
```

### 2.4 Processamento
- Para cada item sem `pathosformel`: chama `iconocode-analyze` (Nível 2 — iconográfico → extrai Pathosformel)
- Prioriza imagem IIIF; se falhar, usa metadados + descrição textual → marca `#verificar-imagem`
- Processa em paralelo (batches de 5), consolida resultados

### 2.5 Saída
`data/processed/pathosformel_index.jsonl` — uma linha por item:
```json
{
  "id": "BR-RS-JUST-1891-001",
  "pathosformel_raw": "NIKE-ARMADA em versão contida-estável — espada em repouso, potência performática contra o caos dos anos Prudente de Morais",
  "extracted_by": "iconocode-batch",
  "extracted_at": "2026-06-05",
  "image_accessible": true,
  "flags": []
}
```

### 2.6 Comando de Execução
```bash
cd /Users/ana/Research/hub/iconocracy-corpus
python tools/scripts/iconocode_batch_runner.py --all --output data/processed/pathosformel_index.jsonl
```

---

## 3. E2 — Clustering Semi-Supervisionado para Regimes Visuais

### 3.1 Conceito: Regime Visual (RV)
Configuração estável de práticas iconográficas que articula:
1. **Suporte material** (onde a imagem aparece)
2. **Posição de campo** (quem produz/consumo)
3. **Pathosformel dominante** (eco formal recorrente)
4. **Linha de fuga** (tensão interna ou transformação em curso)

### 3.2 Seeds Iniciais (Manuais — baseadas no piloto P01 + 4 estudos de caso da tese)

| Seed ID | Regime Visual | Pathosformel Chave | País | Período | Itens Âncora |
|---------|---------------|-------------------|------|---------|--------------|
| `RV-01` | Justitia Monumental | NIKE-ARMADA | BR | 1889–1930 | 8 itens do P01 |
| `RV-02` | Marianne Republicana | MARIANNE-REVOLUCIONARIA | FR | 1789–1946 | A definir (corpus FR) |
| `RV-03` | Britannia Imperial | BRITANNIA-MAJESTAS | UK | 1800–1950 | A definir (corpus UK) |
| `RV-04` | Justitia Hierática (Tribunais) | JUSTITIA-HIERATICA | BR | 1891–presente | A definir (corpus BR-tribunais) |

### 3.3 Features para Similaridade

| Feature | Tipo | Dimensão | Peso |
|---------|------|----------|------|
| Pathosformel (embedding semântico) | vetor denso | 384 | 0.50 |
| Suporte material | one-hot categórico | 6 | 0.15 |
| Posição de campo | one-hot categórico | 4 | 0.10 |
| País / tradição | one-hot categórico | 5 | 0.10 |
| Período (década) | numérico normalizado | 1 | 0.05 |
| Regime iconocrático | one-hot categórico | 4 | 0.10 |

**Embedding model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384-d, multilíngue PT/FR/EN/DE)

### 3.4 Algoritmo de Atribuição

Para cada item **não-seed**:
1. Calcula similaridade Cosseno ponderada vs. cada seed
2. Aplica thresholds:
   - `sim ≥ 0.75` → **atribui** ao seed (RV definido)
   - `0.50 ≤ sim < 0.75` → **pool_revisao** (YAML para validação humana)
   - `sim < 0.50` → **nao_classificado** (candidato a novo seed)

### 3.5 Saída: `data/processed/regimes_visuais.yaml`
```yaml
seeds:
  RV-01:
    nome: "Justitia Monumental"
    pathosformel_chave: "NIKE-ARMADA"
    pais: "BR"
    periodo: "1889-1930"
    itens_ancora: ["BR-RS-JUST-1891-001", "BR-PA-MON-1897-002", "..."]
  RV-02:
    nome: "Marianne Republicana"
    pathosformel_chave: "MARIANNE-REVOLUCIONARIA"
    pais: "FR"
    periodo: "1789-1946"
    itens_ancora: ["FR-PA-MAR-1848-001", "..."]

atribuidos:
  "BR-DF-JUST-1923-007":
    rv: "RV-01"
    similaridade: 0.82
    features_usadas: {pathosformel: 0.78, suporte: 1.0, campo: 0.8, pais: 1.0, periodo: 0.9, regime: 0.7}

pool_revisao:
  "FR-PA-MAR-1848-012":
    candidatos:
      - {rv: "RV-02", sim: 0.68}
      - {rv: "RV-01", sim: 0.45}
    decisao_pendente: true

nao_classificados:
  - "BE-BRU-JUST-1900-003"
  - "DE-BER-JUST-1919-011"
```

### 3.6 Script Novo: `tools/scripts/cluster_rv.py`
```python
#!/usr/bin/env python3
"""
Clustering semi-supervisionado para Regimes Visuais (IMES E2).
Input: data/processed/pathosformel_index.jsonl + seeds manuais
Output: data/processed/regimes_visuais.yaml
"""
# TODO: implementar
```

---

## 4. E3 — Constelação de Pranchas (Editor Humano + Template)

### 4.1 Template: `templates/prancha-template.yaml`
```yaml
prancha_id: "rv-01"
regime_visual: "Justitia Monumental"
pathosformel_dominante: "NIKE-ARMADA"
periodo: "1889-1930"
suportes: ["pintura-oleo", "escultura-monumental", "moeda", "selo", "paratexto-normativo", "caricatura"]
imagens:
  - record_id: "BR-RS-JUST-1891-001"
    posicao: 1
    cjv_justificativa:
      - par: ["BR-RS-JUST-1891-001", "BR-DF-JUST-1923-007"]
        criterio: "CJV-1"
        descricao: "Espada invertida como Pathosformel compartilhado"
      - par: ["BR-RS-JUST-1891-001", "BR-PA-MON-1897-002"]
        criterio: "CJV-3"
        descricao: "Ambas encomendadas por comissoes de arte estaduais"
  - record_id: "BR-DF-JUST-1923-007"
    posicao: 2
    cjv_justificativa:
      - par: ["BR-DF-JUST-1923-007", "BR-PA-MON-1897-002"]
        criterio: "CJV-2"
        descricao: "Mesmo periodo de consolidacao republicana"
legenda_estratigrafica: |
  A constelacao revela a persistência da espada invertida
  como marca de transição do Império para a República...
nota_campo: |
  Encomendas da Comissão de Arte do TJRS (1891) e TJDF (1923).
documento_capta: |
  Ausência de registros 1892-1922 — lacuna documental ou mudança de comissão.
cjv_coverage: 0.87
status: "rascunho"  # rascunho | validado | rejeitado
created: "2026-06-05"
updated: "2026-06-05"
```

### 4.2 Critérios de Justificação de Vizinhança (CJV)
Para cada **par adjacente** na prancha, mínimo **2 dos 3 critérios**:

| Critério | Descrição | Exemplo no P01 |
|----------|-----------|----------------|
| **CJV-1: Eco formal** | Pathosformel compartilhado (gesto, objeto, postura) | Duas Justitias com espada invertida |
| **CJV-2: Eco histórico** | Mesmo evento/transformação institucional | Abolição 1888 / Proclamação 1889 |
| **CJV-3: Eco de campo** | Mesma posição no campo jurídico-iconográfico | Ambas encomendadas por comissões de arte do TJ |

### 4.3 Fluxo do Editor Humano
1. Roda `cluster_rv.py` → obtém `regimes_visuais.yaml` com atribuições por RV
2. Para cada RV com itens atribuídos:
   - Copia `templates/prancha-template.yaml` → `docs/pilots/pranchas/rv-XX-nome.yaml`
   - Preenche `imagens` ordenando por **tensão/Nachleben** (NÃO cronologia)
   - Para cada par adjacente: preenche `cjv_justificativa` (mínimo 2 critérios)
   - Escreve `legenda_estratigrafica` (150–300 palavras), `nota_campo`, `documento_capta`
   - Salva com `status: "rascunho"`

---

## 5. E4 — Validação (Quality Gate)

### 5.1 Script: `tools/scripts/validate_pranchas.py`

### 5.2 Checks Obrigatórios

| Check | Regra | Severidade | Ação se Falha |
|-------|-------|------------|---------------|
| **CJV Coverage** | ≥ 80% dos pares adjacentes têm ≥2 critérios | Erro | `status: "rejeitado"` |
| **Completude** | Todos campos obrigatórios preenchidos | Erro | `status: "rejeitado"` |
| **Capta não-vazio** | `documento_capta` registra ausências/impassses | Warning | Log apenas |
| **IDs válidos** | Todos `record_id` existem no corpus | Erro | `status: "rejeitado"` |
| **Pathosformel consistente** | `pathosformel_dominante` aparece em ≥50% dos itens | Warning | Log apenas |

### 5.3 Saída
- Relatório: `logs/validate_pranchas_YYYY-MM-DD.json`
- Atualiza campo `status` no YAML da prancha (`validado` | `rejeitado`)

```json
{
  "prancha": "rv-01-justitia-monumental.yaml",
  "timestamp": "2026-06-05T14:30:00",
  "checks": {
    "cjv_coverage": {"passed": true, "value": 0.87, "threshold": 0.80},
    "completude": {"passed": true},
    "capta": {"passed": true, "warning": "capta curto"},
    "ids_validos": {"passed": true},
    "pathosformel_consistente": {"passed": true, "value": 0.75, "threshold": 0.50}
  },
  "status_final": "validado"
}
```

---

## 6. E5 — Exportação para Tese

### 6.1 Script Novo: `tools/scripts/pranchas_to_latex.py`
Lê todas as pranchas com `status: "validado"` em `docs/pilots/pranchas/` e gera:

1. **`vault/tese/cap-XX-pranchas.tex`** — LaTeX pronto para Pandoc:
   - Figuras (referenciando imagens no Google Drive / IIIF)
   - Legendas completas (legenda_estratigrafica + nota_campo + documento_capta)
   - Cross-refs automáticos: `claim:C1`, `idea:001`, `idea:003` do research wiki
   - Metadados ABNT NBR 6023:2025 para bibliografia

2. **Integração com `compilar-tese` skill:**
   ```bash
   make -C vault/tese/ docx   # inclui cap-XX-pranchas.tex
   make -C vault/tese/ pdf    # inclui cap-XX-pranchas.tex
   ```

### 6.2 Estrutura do LaTeX Gerado
```latex
% Auto-gerado por pranchas_to_latex.py — NÃO EDITAR MANUALMENTE
\section*{Prancha RV-01: Justitia Monumental (1889--1930)}
\label{prancha:rv-01}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.45\textwidth]{images/BR-RS-JUST-1891-001.jpg}
  \includegraphics[width=0.45\textwidth]{images/BR-PA-MON-1897-002.jpg}
  \caption{Posição 1: Lopes Rodrigues, Alegoria da República (1896). Posição 2: Sansebastiano, Monumento à República (1897).}
\end{figure}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.45\textwidth]{images/BR-DF-JUST-1923-007.jpg}
  \includegraphics[width=0.45\textwidth]{images/BR-SE-SEL-1894-003.jpg}
  \caption{Posição 3: Justiça do TJDF (1923). Posição 4: Selo Madrugada Republicana (1894).}
\end{figure}

% ... demais posições ...

\textbf{Legenda Estratigráfica.} A constelação revela a persistência da espada invertida...

\textbf{Nota de Campo.} Encomendas da Comissão de Arte do TJRS (1891) e TJDF (1923).

\textbf{Documento de Capta.} Ausência de registros 1892--1922...

\textbf{Cobertura CJV.} 87\% (7/8 pares adjacentes com ≥2 critérios).
```

---

## 7. Estrutura de Arquivos Nova

```
iconocracy-corpus/
├── templates/
│   └── prancha-template.yaml              # NOVO
├── data/processed/
│   ├── pathosformel_index.jsonl           # E1 output
│   └── regimes_visuais.yaml               # E2 output
├── docs/pilots/pranchas/                  # NOVO dir
│   ├── rv-01-justitia-monumental.yaml
│   ├── rv-02-marianne-republicana.yaml
│   └── ...
├── tools/scripts/
│   ├── cluster_rv.py                      # NOVO (E2)
│   ├── validate_pranchas.py               # NOVO (E4)
│   ├── pranchas_to_latex.py               # NOVO (E5)
│   └── iconocode_batch_runner.py          # wrapper E1 (verificar se existe)
└── logs/
    └── validate_pranchas_*.json
```

---

## 8. Dependências Externas

| Dependência | Uso | Status |
|-------------|-----|--------|
| `sentence-transformers` | Embeddings multilíngues (E2) | `pip install sentence-transformers` |
| `pyyaml` | Parse/generate YAML (E2, E3, E4) | Já no `requirements.txt` |
| `pandas` | Manipulação tabular (E2) | Já no `requirements.txt` |
| `iconocode-batch` skill | E1 (LLM batch) | Já instalado |

---

## 9. Critérios de Sucesso (Definition of Done)

1. **E1 completo:** `pathosformel_index.jsonl` tem 265 linhas, uma por item do corpus
2. **E2 completo:** `regimes_visuais.yaml` tem 4 seeds + atribuições para ≥80% do corpus; pool_revisao < 20 itens
3. **E3 completo:** ≥4 pranchas YAML em `docs/pilots/pranchas/` com `status: "rascunho"`
4. **E4 completo:** Todas as pranchas passam validação → `status: "validado"`; relatório em `logs/`
5. **E5 completo:** `make -C vault/tese/ docx` compila sem erros e inclui as pranchas no capítulo correto

---

## 10. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| LLM extrai Pathosformel inconsistente (E1) | Média | Alto | Revisão manual de amostra (10%) antes de E2; prompt engineering no `iconocode-analyze` |
| Seeds insuficientes para cobertura (E2) | Baixa | Médio | Se pool_revisao > 30 itens → define novos seeds manuais e re-roda |
| CJV coverage < 80% nas pranchas (E4) | Média | Alto | Template força preenchimento; validação prévia pelo editor |
| Imagens não acessíveis para LaTeX (E5) | Baixa | Médio | `download_corpus_images.py` já existe; roda antes de E5 |

---

## 11. Próximos Passos (Implementation Plan)

A ser gerado pelo skill `writing-plans` após aprovação deste design.

---

**Design aprovado por:** Ana Vanzin  
**Data:** 2026-06-05  
**Próxima ação:** Invocar `writing-plans` para criar plano de implementação detalhado.