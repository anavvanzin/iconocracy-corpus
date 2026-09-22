# CHANGELOG — corpus v2 (2026-07-24)

## Estatuto: POSSIBILIDADE / hipótese de trabalho

Esta versão NÃO é definitiva. Ela registra uma virada metodológica que **muda a
tese por completo** e deve ser tratada como direção de pesquisa a validar, não como
resultado fechado.

## O que mudou

### 1. Abandono do `endurecimento_score`
O campo `endurecimento_score` (média aritmética dos 10 indicadores) foi **removido
de todos os 328 registros**. Era um artefato do pipeline `hermes-auto` — os valores
0,0 (importação vazia) e 1,4 (fallback) nunca foram medições. Um conselho de três
modelos independentes (Gemini 3 Pro, GPT-5.5, Claude Opus) recomendou por
unanimidade não escalar a métrica; o diagnóstico de fundo, porém, foi da própria
pesquisadora: o ENDURECIMENTO havia sido tratado como definitivo quando era
exploratório.

### 2. ENDURECIMENTO: de métrica a lente
O ENDURECIMENTO deixa de ser escala 0–4 e passa a ser **lente comparativa
qualitativa** (Warburg/Panofsky). Os 10 indicadores sobrevivem como **inventário de
atributos** — grau em palavras (ausente/mínimo/moderado/pronunciado/extremo), nunca
somável. Os valores 0–4 originais permanecem em `indicadores` como dado bruto
auditável.

### 3. Novo eixo teórico: história do repertório disponível
A cronologia deixa de ser flecha (fundacional → normativo → militar) e passa a ser
a história das operações sobre um **repertório de corpos** que o Estado pode
convocar: entradas, recusas, coexistências.

### 4. Novo campo `recusa` + hipótese da REMASCULINIZAÇÃO
Varredura completa dos 328 em busca de recusas do corpo feminino de Estado. 26
candidatos triados, 13 confirmados por verificação visual. A hipótese da
remasculinização (quando o corpo feminino sai, entra masculino/masculino-animal)
**confirmou-se como UM de vários mecanismos, não como lei**:

- remasculinização por substituição: 6 (águia, rei, esqueleto, clero, mãos armadas)
- remasculinização por deslocamento (limítrofe): 1 (US-020)
- negação pura / vazio: 3 (corpo destruído, nada no lugar)
- feminino-esvaziado: 2 (Anastasie; reapropriação)
- neutro-abstrato: 1 (brasão do Brasil)

Os contra-exemplos definem os limites do padrão e são o material mais valioso.

## Correções de catalogação
- `DE-015`: eram dois meninos (Alsácia/Lorena), não mulheres. Não era recusa.
- `BR-019`: link morto (memoria.bn.br NXDOMAIN).
- `SCOUT-567`: sem elemento hídrico; azul celeste, não aquático.

## Arquivos
- `corpus/corpus-data.json` — ledger canônico recodificado (lista, 328 registros)
- `corpus/corpus-data.v2.json` — mesma base com envelope `_meta` de estatuto
- `corpus/docs/2026-07-24_varredura-recusas.md` — relatório da varredura
- `corpus/docs/2026-07-24_auditoria-piloto-iconocode.md` — piloto de recodificação
- `corpus/docs/2026-07-24_conselho-modelos-veredicto.md` — veredicto do conselho
