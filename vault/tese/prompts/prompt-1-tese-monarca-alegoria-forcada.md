# Prompt 1 — Tese: "A Monarca como Alegoria Forçada"
**Data:** 20 de Julho de 2026  
**Ideia base:** #1 do brainstorm de expansões — O Paradoxo da Monarca-Personificada  
**Status:** Em execução (scout direto do agente pai)

---

## Objetivo

Desenvolver o argumento de que a mulher real soberana, quando colocada em moedas/selos oficiais, sofre uma *alegorização forçada* que exige endurecimento corporal radical.

---

## Escopo IN

- Definir o que seria "endurecimento corporal" no codebook (indicadores que medem apagamento de biografia: rigidez postural, uniformização facial, dessexualização, monocromatização).
- Scout de 2–3 casos reais de monarcas femininas em suportes estatais (ex: Rainha Vitória em moedas britânicas, Maria I de Portugal, Isabel II atual).
- Extrair `endurecimento_score` (ou atribuir scores 0–3 nos 10 indicadores) para cada caso.
- Rascunhar um parágrafo argumentativo de ~500 palavras ligando os scores ao conceito de *Contrato Sexual Visual*.

---

## Escopo OUT

- Não incluir a antítese (regime monárquico distinto) — isso é do Prompt 2.
- Não escrever a síntese — isso é do Prompt 3.
- Não propor mudanças no codebook ainda — isso é do Prompt 3.

---

## Mínimo Empírico Antes de Escrever

- Pelo menos 2 casos scoutados com scores de endurecimento atribuídos.
- Pelo menos 1 imagem por caso para referência visual.

---

## Forma de Saída

- 1 parágrafo argumentativo (~500 palavras).
- 1 card por caso com: ID do corpus (ou placeholder), `endurecimento_score`, regime_iconocratico, URL da imagem, nota de atribuição.

---

## Perigos Conhecidos

- O corpus atual tem **zero** itens com `familia_alegorica = monarca-personificada`. O scout pode falhar ou encontrar casos de baixa resolubilidade. Se o scout retornar <2 casos codificáveis, o parágrafo deve ser suspenso até novo scout.
- Risco de anacronismo: não projetar categorias republicanas (alegoria) sobre monarquias sem justificar a transferência.

---

## Instrução de Roteamento

**NÃO despachar para subagente.** O scout em Numista/Colnect/Museus causa timeout silencioso em subagentes. Executar diretamente no agente pai usando `web_search_plus` + `web_extract`.
