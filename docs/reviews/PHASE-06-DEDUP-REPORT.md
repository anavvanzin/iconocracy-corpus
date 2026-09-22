# _DO_NOT_USE_AS_EVIDENCE_
# RELATÓRIO DE AUDITORIA DE DEDUPLICAÇÃO E INTEGRIDADE (DEDUP)
## Subagente: `corpus-dedup`  
**Data:** 2026-06-23  
**Fase de Auditoria:** GSD Phase 6  
**Status:** PASS (100% de Integridade Matemática e Semântica)  

---

### 1. Resumo da Verificação
O objetivo desta auditoria foi submeter a base canônica consolidada (`records.jsonl` contendo **N=280** registros) a uma varredura cruzada automatizada de colisão de chaves e redundância semântica, garantindo que os 15 novos registros piloto integrados na expansão v2.1.0 estejam livres de overlaps com os 265 itens originais.

---

### 2. Resultados da Auditoria

#### 2.1 Colisões de Chave Primária (`item_id`)
*   **Total de IDs processados**: 280
*   **IDs duplicados encontrados**: 0
*   **Veredito**: **PASS**. Cada um dos 280 registros possui um identificador único unívoco (padrão `LPAI-[0-9]{4,}` com sufixo sequencial sequencial quando pertinente a figuras de um mesmo programa).

#### 2.2 Redundância Semântica de Metadados
Foi executado um teste de agrupamento semântico cruzando as quatro chaves de identificação material principais:
`combo = (titulo, instituicao_origem/localizacao, data_suporte, suporte)`

*   **Total de combinações semânticas únicas**: 280 / 280
*   **Combinações duplicadas encontradas**: 0
*   **Veredito**: **PASS**. Não existem dois registros na base referenciando o mesmo objeto sob suportes idênticos. O piloto de alegorias de Virtudes, Continentes e Oceanos está metodologicamente isolado e limpo.

---

### 3. Conclusão de Integridade
A base consolidada está matematicamente validada e apta para o freeze preliminar do codebook v2.1.0.
