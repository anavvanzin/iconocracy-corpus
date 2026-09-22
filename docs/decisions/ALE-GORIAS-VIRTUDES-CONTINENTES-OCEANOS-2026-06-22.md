# Decisão metodológica: integração das alegorias de Virtudes, Continentes e Oceanos/Rios

**Data:** 2026-06-22  
**Autor:** Codex (piloto v2 codebook)  
**Status:** rascunho para revisão  
**Codebook:** `docs/methodology/codebook-v2-alegorias.md`  
**Plano de trabalho:** `.planning/2026-06-22-alegorias-expansao/task_plan.md`

## 1. Delimitação de corpus core vs. comparador genealógico

O problema central da tese permanece: por que o Estado moderno escolhe reiteradamente a forma feminina para corporificar seus valores mais altos enquanto exclui mulheres reais do exercício do poder?

A expansão para Virtudes, Continentes e Oceanos/Rios aprofunda a **genealogia** desse regime iconocrático, mas não alarga o escopo indiscriminadamente. Mantemos a regra:

> **Corpus core:** só entram alegorias de Virtudes, Continentes ou Oceanos/Rios quando aparecem em dispositivos estatais/jurídicos brasileiros (brasões, moedas, cédulas, selos postais, paratextos normativos, arquitetura forense, monumentos públicos).

Tudo que não atender a esse critério vai para:

- **Comparador genealógico:** wiki pages, fichas bibliográficas anotadas, pranchas-atlas.
- **Apêndice:** reproduções de Ripa, Ortelius, Collaert, Carriera, Warner, Souza.
- **Contra-alegoria/iconoclasmo:** casos como México 2021, pichações feministas no Brasil (2019–2021), usados como vetor de análise, não como corpus core.

## 2. Os três eixos teóricos

### Eixo 1 — Profundidade genealógica
O regime iconocrático não nasce com o Estado moderno; ele *herda* e *reativa* repertórios de longa duração (virtudes cardinais medievais, alegorias coloniais barrocas). A especificidade do século XIX é a **estatização** desse repertório: o Estado nacional o seculariza, monopoliza e inscreve em suportes circuláveis (moedas, selos, brasões).

### Eixo 2 — Dimensão racial da feminilidade de Estado
As alegorias de Continentes articulam gênero e raça de forma inseparável. A América alegórica é mulher, selvagem e colonizada. Quando o Brasil independente constrói sua alegoria nacional feminina, ele herda esse nó e precisa desfazê-lo ou reproduzi-lo. A Efígie da República brasileira (branca, à romana) é uma escolha iconográfica que é também uma escolha racial: **iconocracia tropical em operação**.

### Eixo 3 — Soberania hídrica e territorial
As alegorias de Oceanos e Rios articulam soberania sobre o território físico. A tradição clássica personifica grandes rios como homens barbados e fontes/cursos menores como ninfas. Para um país continental e costeiro como o Brasil, a pergunta é: quando o Estado iconografa seus corpos d'água (Atlântico, Amazônia), que gênero lhes atribui e como isso se articula com a soberania territorial?

## 3. Hipótese racial como eixo transversal

A hipótese racial não será um subcapítulo isolado. Ela atravessa os três eixos como lente de leitura:

- **Virtudes:** as virtudes barrocas brasileiras são figuras femininas brancas e idealizadas; a Iustitia republicana reproduz a mesma gramática.
- **Continentes:** a herança colonial da América alegorizada (seminua, selvagem, com traços caucasianos) é reformulada na Efígie da República, que branqueia o corpo nacional.
- **Oceanos/Rios:** a despersonalização dos corpos d'água no brasão da República evita tanto a personificação imperial masculina quanto qualquer feminização indígena do território.

O campo `hipotese_racial` no codebook v2 registra, para cada item, uma formulação curta dessa articulação.

## 4. Protocolo de decisão: quando um item entra no core

Um item entra no corpus core se, e somente se:

1. `familia_alegorica` ∈ {Virtudes, Continentes, Oceanos/Rios, Nacional}.
2. `funcao_juridica` indicar dispositivo estatal/jurídico brasileiro.
3. Houver evidência documental de circulação no Brasil (data, local, instituição).

Se falhar em (2) ou (3), o item é marcado como `corpus/comparador` ou `corpus/comparador-latam`.

## 5. Roteiro de inserção nos capítulos da tese

| Capítulo | Uso das novas famílias |
|----------|------------------------|
| Genealogia do visível | Virtudes (Ripa, Warner), Continentes (Ortelius, Souza), Oceanos/Rios (classical topos) |
| Colônia e Império | Virtudes em igrejas barrocas; América alegorizada circulada via Portugal |
| Primeira República | Efígie, cédula de 2.000 réis, selos, monumentos; diálogo com América alegorizada |
| Arquitetura forense | Iustitia em tribunais brasileiros (Resnik & Curtis + corpus) |
| Brasão e soberania | Brasão da República como dado negativo; elementos hídricos |
| Iconoclasmo tropical | México 2021; pichações feministas no Brasil; contra-alegorias |

## 6. Riscos de escopo e contramedidas

| Risco | Contramedida |
|-------|--------------|
| Escopo vazar para história da arte geral | Regra core rigorosa; wiki separa comparador de corpus |
| Inferência estatística antes do freeze | Todos os itens do piloto marcados `pre_freeze_sample: true` |
| Eurocentrismo nas categorias | `subaltern_caution: true` quando aplicado a objetos indígenas/negos; wiki pages enfatizam limites das categorias |
| Duplicação com itens existentes | `corpus-dedup` audita piloto contra `corpus-data.json` e `corpus-data-enriched.json` |
| Tratamento do LPAI como índice autoritário | Declaração de capta em todo registro; nota linkada a `schema/lpai-v2-as-capta.md` |

## 7. Ligações

- Codebook v2: [`docs/methodology/codebook-v2-alegorias.md`](../../docs/methodology/codebook-v2-alegorias.md)
- LPAI como capta: [`schema/lpai-v2-as-capta.md`](../../schema/lpai-v2-as-capta.md)
- Corpus piloto: [`corpus/piloto-v2-alegorias-final.json`](../../corpus/piloto-v2-alegorias-final.json)
- Integração Atlas: [`docs/decisions/ATLAS-REPORT-INTEGRATION-2026-06-16.md`](./ATLAS-REPORT-INTEGRATION-2026-06-16.md)
- Projeto de tese v3: [`docs/PROJETO-TESE-v3-RESUMO.md`](../../docs/PROJETO-TESE-v3-RESUMO.md)

## 8. Próximos passos

1. Revisão por `academic-peer-reviewer` sobre argumentação e citações.
2. Revisão por `Anthropologist` sobre colonialidade, raça e gênero.
3. Revisão por `corpus-dedup` sobre duplicação com corpus existente.
4. Ajustes críticos → freeze preliminar do codebook v2 → ingest formal no corpus.
