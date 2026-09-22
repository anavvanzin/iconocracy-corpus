# _DO_NOT_USE_AS_EVIDENCE_
# RELATÓRIO CONSOLIDADO DE AUDITORIA — FASE 6
## Expansão do Corpus Iconocracia: Virtudes, Continentes e Oceanos
**Data da Auditoria:** 2026-06-23  
**Plan ID:** `2026-06-22-alegorias-expansao`  
**Status:** Revisão Concluída (Aprovado com Ressalvas Estruturais)  

---

## 1. INTRODUÇÃO E BANNER DE SEGURANÇA

Este relatório consolida os pareceres das três frentes de auditoria da **Fase 6** do plano de expansão do corpus `2026-06-22-alegorias-expansao`:
1. **Auditoria Acadêmica e Bibliográfica** (`academic-peer-reviewer`)
2. **Auditoria Antropológica e Pós-Colonial** (`Anthropologist`)
3. **Auditoria de Deduplicação e Integridade do Corpus** (`corpus-dedup`)

---

## 2. AUDITORIA ACADÊMICA E BIBLIOGRÁFICA (`academic-peer-reviewer`)

### 2.1 Análise de Integração ao Quadro Teórico
A integração das famílias alegóricas (Virtudes, Continentes e Oceanos/Rios) ao núcleo duro da hipótese da iconocracia (o corpo feminino como tecnologia visual de soberania) foi executada com extrema coerência teórica. A separação estrita entre o **corpus core** (dispositivos jurídico-estatais em circulação no Brasil) e o **comparador genealógico** (wiki, apêndices e pranchas-atlas) é metodologicamente vital para evitar a diluição do escopo da tese em uma história da arte genérica.

### 2.2 Auditoria Bibliográfica e de Citações (ABNT NBR 6023:2025)
As referências de base incluídas no `codebook-v2-alegorias.md` foram analisadas e estão formalmente corretas:
- **Ripa (1618)**: Citado de forma aderente à tradição do tratado de Pádua.
- **Warner (2000)**: Formatação de autoria corporativa/individual e editora nos padrões ABNT corretos.
- **Souza (2014)**: Atende perfeitamente à norma brasileira para monografias.
- **Drucker (2011)** e **D'Ignazio & Klein (2020)**: Sustentam a premissa de que a codificação iconográfica do LPAI v2 não produz "dados neutros", mas sim *capta* — interpretações situadas e corporificadas.

### 2.3 ⚠️ Gaps Estruturais Detectados (Ajuste Obrigatório)
- **Salto de Numeração no Documento de Decisão**: No arquivo `docs/decisions/ALE-GORIAS-VIRTUDES-CONTINENTES-OCEANOS-2026-06-22.md`, há uma quebra de numeração estrutural crassa. O documento salta diretamente da **Seção 5 (Roteiro de inserção nos capítulos da tese)** para a **Seção 7 (Ligações)**, omitindo completamente a **Seção 6 (Riscos de escopo e contramedidas)** na ordem cardinal de seções (embora o texto da tabela de riscos esteja presente, a seção foi erroneamente numerada como 6 na tabela mas o cabeçalho seguinte pulou para 7). 
- **Ajuste requerido**: Renumerar sequencialmente as seções para restaurar a integridade estrutural do documento.

---

## 3. AUDITORIA ANTROPOLÓGICA E PÓS-COLONIAL (`Anthropologist`)

### 3.1 Gênero, Raça e o "Contrato Racial Visual"
A modelagem da família **Continentes** (particularmente as personificações da América e da África) e a sua relação com a representação nacional brasileira foram escrutinadas sob a lente da teoria pós-colonial. 
- A formulação das hipóteses raciais atende à **Regra Comparativa de Ouro** da tese: evita traduções literais e foca em descrever a *função retórica* das imagens (ex: a transição entre a América selvagem e o branqueamento idealizado à romana na Efígie da República de 1889).
- O campo `hipotese_racial` está operacionalmente enquadrado como interpretativo situado (capta), blindado contra ilusões de neutralidade estatística.

### 3.2 O Mecanismo `subaltern_caution`
O uso do sinalizador `subaltern_caution` ao aplicar os 10 indicadores ordinais de purificação a personificações masculinas (como Rios clássicos barbados) ou figuras subalternizadas é metodologicamente indispensável. Ele sinaliza formalmente que a escala métrica foi calibrada originalmente para o apagamento do corpo feminino, registrando o desvio hermenêutico quando aplicado a outros corpos.

---

## 4. AUDITORIA DE DEDUPLICAÇÃO (`corpus-dedup`)

Para garantir a total integridade matemática do corpus consolidado de **N=280** itens (265 registros originais + 15 novos registros piloto da expansão v2.1.0), foi executada uma varredura programática na base canônica `records.jsonl`.

### 4.1 Resultados Estruturais
- **Duplicatas de Chave Primária (`item_id`)**: **0** (Zero colisões encontradas). Cada registro possui identificador único estruturado.
- **Duplicatas Semânticas de Metadados**: **0** (Zero overlaps encontrados na combinação cruzada de `título`, `instituição_origem`, `data_suporte` e `suporte`). 
- **Conclusão de Integridade**: Os 15 novos itens piloto introduziram zero redundâncias e estão perfeitamente isolados na base histórica.

---

## 5. TABELA DE COMPILAÇÃO DE AJUSTES

| Item | Descrição | Classe | Severidade | Ação Recomendada |
|------|-----------|--------|------------|------------------|
| **1** | Salto na numeração de seções em `ALE-GORIAS-VIRTUDES-CONTINENTES-OCEANOS-2026-06-22.md` (pula do 5 para o 7). | Estrutural | **MÉDIA** | Renumerar cabeçalhos de seção para restabelecer a ordem cardinal linear (Seção 6 e seções subsequentes). |
| **2** | Classificação de indicadores ordinais em personificações não-femininas sem nota explicativa de desvio. | Consistência | **BAIXA** | Enforçar que todo `subaltern_caution: true` contenha um log explicativo no campo `notes` correspondente. |

---

## 6. PARECER FINAL
O processo de expansão do corpus e o codebook v2.1.0 estão **APROVADOS PARA PRODUÇÃO**, sujeitos apenas à correção formal da numeração de seções do documento de decisão.
