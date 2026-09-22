---
documento: decisao
id: DEC-2026-07-28-COMPOSTO
data: "2026-07-28"
autor: Ana Vanzin
escopo: "instrumento LPAI v2 — estatuto do índice composto de purificação"
codebook_afetado: schema/codebook-MASTER.md
codebook_version_antes: 2.2.0
codebook_version_depois: 2.2.1
schemas_afetados:
  - tools/schemas/master-record.schema.json
  - tools/schemas/purification-record.schema.json
scripts_afetados:
  - tools/scripts/lpai_proxy_coder_k3.py
  - tools/scripts/compute_irr.py
status: vigente
migracao: concluida
licenca: CC-BY-4.0
---

# Aposentadoria do índice composto de purificação

## A divergência

O codebook MASTER v2.2.0 prescreve, no §12 e no passo 4 do master prompt
operacional (§16), o cálculo de `purificacao_composto` como média aritmética
simples dos 10 indicadores canônicos em escala 0–3. A virada qualitativa de
julho de 2026 removeu o escore agregado do fluxo de análise e passou a tratar
ENDURECIMENTO como lente qualitativa — inventário verbal de atributos —
justamente porque um número único apaga a heterogeneidade dos indicadores que o
compõem.

As duas orientações coexistiram por cerca de um mês. O instrumento pedia um
número que a análise havia decidido não usar. Esta decisão encerra a coexistência.

## Decisão

**O índice composto é aposentado como afirmação probatória e congelado como
artefato histórico.**

1. **Não se calcula composto para codificação nova.** Nem humana, nem proxy.
   O passo 4 do §16 passa a exigir inventário verbal de atributos no lugar da
   média.
2. **Os 10 indicadores permanecem.** Eles são capta ordinal previsto pelo
   schema, com critérios operacionais definidos, e continuam obrigatórios. A
   decisão recai sobre a agregação, não sobre a observação.
3. **Valores legados não são recalculados nem apagados.** Registros codificados
   em v2.2.0 conservam seu `purificacao_composto`. Reprocessá-los produziria
   série temporal falsa; deletá-los destruiria o rastro de como o corpus foi
   construído. O campo passa a `legacy_frozen`.
4. **Nenhuma afirmação da tese pode repousar sobre o composto.** Onde o
   argumento hoje se apoia em variação de escore, ele precisa ser reescrito como
   inventário comparado de atributos.
5. **Concordância entre codificadores migra para os indicadores.** O kappa por
   indicador e a distância ordinal permanecem métricas de confiabilidade. A
   diferença de composto entre codificadores continua sendo impressa por
   `compute_irr.py`, porém rotulada como diagnóstico legado, sem valor
   probatório.
6. **O composto não retorna sem nova decisão registrada.** Se algum dia houver
   justificativa para agregação, ela precisará de ponderação explícita,
   fundamentação teórica e um documento como este — não de uma média silenciosa.

## Razão

Três argumentos sustentam a aposentadoria.

O primeiro é de validade. Os 10 indicadores medem coisas incomensuráveis:
`monocromatizacao` é propriedade técnica do suporte, `inscricao_estatal` é fato
institucional, `dessexualizacao` é juízo iconográfico contestável. A média
trata como intercambiável o que a tese precisa manter distinto. Uma moeda
serial e monocromática por restrição de cunho recebe escore alto por razões que
nada dizem sobre endurecimento simbólico.

O segundo é de auditabilidade. O escore comprime dez decisões interpretativas
em um número, e o número é o que sobrevive na tabela. A auditoria de Panofsky
já havia registrado o sintoma: entradas com `endurecimento_score` calculado sem
o texto descritivo que o justificaria — a lacuna mais crítica apontada no
relatório francês. O inventário verbal não permite esse atalho.

O terceiro é de honestidade do argumento. Um dos painéis do atlas ainda afirma
trajetória cuja medida cresce monotonicamente no tempo. Se o composto não é
prova autônoma — e o próprio §12 sempre disse que não era — a afirmação de
monotonia precisa ser reformulada como montagem de casos, não como curva.

## Migração

Consumidores migrados. O módulo `tools/scripts/lpai_indicators.py` concentra a
leitura não agregadora dos indicadores (`attribute_inventory`,
`attribute_count`, `coding_coverage`, `is_uncoded`) e um acessor somente de
leitura para valores congelados (`legacy_composite`), que nunca calcula:

| Arquivo | Situação | Ação |
|---|---|---|
| `tools/scripts/lpai_proxy_coder_k3.py` | resolvido nesta decisão | não emite composto; `--emit-composto` removido |
| `tools/schemas/purification-record.schema.json` | resolvido | campo deixa de ser `required`, marcado `deprecated` |
| `tools/schemas/master-record.schema.json` | resolvido | campo marcado `deprecated` |
| `tools/scripts/compute_irr.py` | resolvido | seção de composto rotulada como legado diagnóstico |
| `tools/scripts/csv_to_records.py` | resolvido | não calcula composto; repassa valor legado quando existe; confiança passa a vir da cobertura do instrumento |
| `tools/scripts/iconocode_gemma4.py` | resolvido | `endurecimento_score` sai; entra `inventario_verbal` |
| `tools/scripts/e3_firecrawl_recode.py` | resolvido | fila selecionada por item não codificado, não por composto zero |
| `tools/audit/scripts/analyze_threads.py` e `_v2.py` | resolvido | ordenação, cadeias e rótulos por contagem de atributos |
| `tools/audit/mnemosyne/starter-8panels.json` | resolvido | tese do painel reescrita como inventário comparado |
| `tools/audit/reports/french-panofsky-audit.md` | resolvido | checklists pedem inventário verbal + Panofsky, não escore |
| `tools/audit/reports/systematic-review-conversation.md` | resolvido | idem |

## Efeito no instrumento

O codebook MASTER passa a 2.2.1, com o §12 e o passo 4 do §16 reescritos. Como
`tools/scripts/lpai_proxy_coder_k3.py` lê o §16 em tempo de execução, a mudança
do instrumento é automaticamente refletida na codificação de proxy, e cada linha
de staging registra `codebook_version: 2.2.1`. O que a codificação de julho fez
e o que a de agosto fará ficam distinguíveis por esse campo.
