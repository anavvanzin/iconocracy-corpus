# Cookbook KIMI K3 — Manual de Trabalho para a ICONOCRACIA

Manual operacional para incorporar o Kimi K3 (Moonshot AI) ao fluxo de trabalho do doutorado: escrita da tese, protocolo de catalogação LPAI v2, estudos historiográficos, análise iconográfica e desenvolvimento web.

Autoria de referência: Ana Vitória Vanzin Mendes — PPGD/UFSC
Data de redação: 28 de julho de 2026
Versão: 1.0

---

## 0. Como usar este manual

Este documento não é uma lista de recursos. É um protocolo. Cada seção tem três camadas: o que o modelo é capaz de fazer, o que você deve pedir a ele, e o que você não deve delegar. A terceira camada é a mais importante — um modelo de 2,8 trilhões de parâmetros é excelente em produzir prosa plausível sobre iconografia jurídica, e prosa plausível é exatamente o risco metodológico central de uma tese que sustenta afirmações a partir de imagens e fontes primárias.

A regra que organiza tudo o que segue: **o K3 é um operador de corpus e de código, não uma autoridade sobre fontes.** Ele lê, classifica, escreve, refatora e audita. Ele não decide o que é verdadeiro sobre uma moeda de 1890 nem sobre um voto de um ministro. A autoridade permanece no `records.jsonl`, nos acervos digitais e nas suas leituras.

Cada receita traz um prompt pronto para copiar. Todos foram escritos em português porque o K3 é multilíngue nativo e porque sua tese é redigida em português — pedir em inglês para depois traduzir introduz uma camada de deformação conceitual desnecessária no vocabulário iconográfico (endurecimento, recusa, coexistência não têm equivalentes estáveis em inglês).

---

## 1. O que é o K3 e o que muda para o seu trabalho

O Kimi K3 foi lançado em 16 de julho de 2026 como modelo de arquitetura Mixture-of-Experts com 2,8 trilhões de parâmetros totais e 16 de 896 especialistas ativos por token, janela de contexto de 1.048.576 tokens e visão nativa ([Constellation Research](https://www.constellationr.com/insights/news/moonshot-ai-launches-kimi-k3)). A Moonshot o descreve como seu modelo de ponta para codificação de longo horizonte, trabalho de conhecimento e raciocínio profundo, com desempenho abaixo de Claude Fable 5 e GPT-5.6 Sol no agregado, mas acima de Opus 4.8 e GPT-5.5 em boa parte das suítes agênticas ([CNBC](https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html)). Os pesos completos foram programados para publicação em 27 de julho de 2026 sob licença MIT modificada ([Bloomberg](https://www.bloomberg.com/news/articles/2026-07-27/china-s-moonshot-to-release-breakthrough-ai-model-for-download)).

Quatro propriedades importam concretamente para a ICONOCRACIA.

**Janela de 1M tokens com preço plano.** Não há sobretaxa de contexto longo: US$ 3,00 por milhão de tokens de entrada sem cache, US$ 0,30 com cache, US$ 15,00 de saída ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Isso significa que os 328 registros do `records.jsonl`, o guia do Codificador B, o esqueleto da tese e três capítulos podem entrar na mesma conversa sem fragmentação. Pela primeira vez o modelo pode raciocinar sobre o corpus inteiro em vez de sobre amostras.

**Visão nativa, mas sem URL pública.** O K3 aceita imagens e vídeo por base64 ou por referências internas de arquivo da Moonshot; **não aceita URLs públicas de imagem** ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Isso inverte a restrição que hoje molda o Corpus Vision Pipeline, onde o Google Cloud Vision exigia links públicos temporários do Drive. Com o K3 a fase de publicação temporária no Drive deixa de ser necessária para a leitura iconográfica — envie os bytes locais direto. A fase do Drive continua útil apenas se você mantiver o Vision como segunda opinião de OCR.

**Somente esforço máximo de raciocínio.** No lançamento existe um único modo, "max", e todo traço de raciocínio é cobrado como token de saída ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Consequência prática: o K3 é lento e prolixo. É bom para lotes longos e ruim para edição interativa linha a linha.

**Enxame de agentes.** A variante K3 Swarm Max estende o Agent Swarm da Moonshot à escala do K3, coordenando grande número de subagentes paralelos; na geração anterior o K2.5 coordenava até 100 subagentes e cerca de 1.500 passos de ferramenta, com ganho de velocidade de até 4,5× sobre execução de agente único ([SiliconFlow](https://www.siliconflow.com/blog/kimi-k2.5-now-on-siliconflow-sota-on-visual-agentic-intelligence)). É a superfície natural para prospecção de acervos e revisão sistemática.

### Tabela de fatos operacionais

| Item | Valor |
|---|---|
| Base URL (OpenAI-compatível) | `https://api.moonshot.ai/v1` |
| Base URL (Anthropic-compatível) | `https://api.moonshot.ai/anthropic` |
| ID do modelo | `kimi-k3` |
| Contexto | 1.048.576 tokens (CLI própria: 256K) |
| Entrada sem cache / com cache | US$ 3,00 / US$ 0,30 por 1M |
| Saída | US$ 15,00 por 1M |
| Busca web via API | US$ 0,004 por chamada |
| Visão | base64 ou file reference; sem URL pública |
| Modos de raciocínio | apenas "max" |
| Velocidade da CLI | 180–260 tokens/s |

Fontes das colunas: [guia de setup Kimi K3](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide) e [guia completo Amplifi](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model).

---

## 2. Instalação e configuração

### 2.1 Chave e ambiente

Crie a chave na Moonshot Open Platform e guarde-a fora de qualquer repositório. Como seus repositórios são públicos (`anavvanzin.github.io`, `iconocracy-corpus`), o risco de vazamento de segredo é real e o PR #69 já estabeleceu higiene de fonte como parte do contrato de implantação.

```bash
# ~/.zshrc — nunca em arquivo versionado
export MOONSHOT_API_KEY="sk-..."
```

### 2.2 Kimi Code CLI (caminho recomendado)

A Moonshot recomenda usar um harness verificado, como a própria Kimi Code, porque o K3 é sensível ao histórico de raciocínio ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)).

```bash
curl -fsSL https://install.kimi.com/cli | bash
# alternativa: npm install -g kimi
kimi --version
```

Na primeira execução, dentro da sessão:

```
/login    # OAuth do Kimi Code ou chave da Open Platform
/init     # varre o projeto e gera AGENTS.md
```

O `AGENTS.md` é o análogo direto do `CLAUDE.md`; o `/init` escreve passos de build, convenções de código e contexto de fundo ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)). A CLI expõe o subcomando `kimi acp` para editores compatíveis com Agent Client Protocol (Zed, JetBrains).

### 2.3 Reapontar o Claude Code para o K3

Útil quando você quer manter fluxos já treinados nas suas skills e apenas trocar o motor por um mais barato em cache.

```bash
export ANTHROPIC_BASE_URL="https://api.moonshot.ai/anthropic"
export ANTHROPIC_AUTH_TOKEN="$MOONSHOT_API_KEY"
export ANTHROPIC_MODEL="kimi-k3"
export ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k3"
export ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k3"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k3"
unset ANTHROPIC_API_KEY
claude
# dentro da sessão: /status deve mostrar moonshot e kimi-k3
```

Dois detalhes que economizam uma hora de depuração: sem o override de Haiku, as tarefas de fundo (geração de título, resumo de arquivo) tentam alcançar a Anthropic e falham; e uma variável `ANTHROPIC_API_KEY` remanescente conflita com o token de autenticação e produz erros de auth confusos ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)).

### 2.4 Ferramentas de formato OpenAI

Para Cline, Roo Code, Continue, Aider e qualquer cliente OpenAI, incluindo scripts Python do `tools/scripts/`:

```
Base URL: https://api.moonshot.ai/v1
API key:  $MOONSHOT_API_KEY
Model:    kimi-k3
```

```python
from openai import OpenAI
client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"],
                base_url="https://api.moonshot.ai/v1")
```

Funciona com os SDKs oficiais de Python e Node e com frameworks como LangChain, seguindo o esquema de function/tool call da OpenAI ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)).

### 2.5 Onde o K3 encosta na sua infraestrutura atual

| Camada existente | Papel do K3 |
|---|---|
| `iconocracy-corpus` (monorepo) | agente de codificação no terminal via Kimi Code, com AGENTS.md como contrato |
| MotherDuck | geração e revisão de SQL sobre `searchable_corpus`; nunca escrita direta sem revisão |
| Google Cloud Vision | mantido como OCR independente para checagem cruzada; o K3 faz a leitura iconográfica |
| Cloudflare Workers / Pages | geração de código de borda e revisão de wrangler/Actions |
| Obsidian (vault SCOUT) | redação de notas atômicas com frontmatter padronizado |
| Google Sheets (159 registros) | proposição de recodificações em CSV para revisão humana, jamais aplicação automática |

Nota sobre a Cloudflare: a Workers AI passou a servir modelos grandes começando pelo Kimi K2.5, com contexto de 256K, chamada de ferramentas em múltiplos turnos, entradas de visão e saídas estruturadas ([Cloudflare](https://blog.cloudflare.com/workers-ai-large-models/)). Isso te dá um caminho de inferência dentro da mesma plataforma onde `iconocracia.com` já vive — útil para tarefas de ingestão em fila, sem depender da API da Moonshot.

---

## 3. Política de roteamento de modelos

Não substitua sua pilha. Adicione o K3 onde ele é dominante e mantenha o resto.

| Tarefa | Modelo | Razão |
|---|---|---|
| Codificação LPAI em lote (dezenas de imagens) | K3 | visão nativa + cache barato + tolerância a lotes longos |
| Leitura iconográfica fina de uma imagem-chave | K3, depois segunda opinião de outro modelo | discordância entre codificadores é dado de refinamento, não fracasso |
| Escrita de painel de atlas a partir do corpus | K3 com corpus inteiro em contexto | 1M tokens elimina amostragem |
| Revisão de coerência entre capítulos 7, 8 e 9 | K3 | precisa de todos os três na mesma janela |
| Edição interativa de parágrafo | Claude/GPT | K3 é lento e prolixo por padrão |
| Front-end de `iconocracia.com` e `anavanzin.com` | K3 | #1 no Frontend Code Arena com 1679 pontos |
| Compreensão profunda de repositório em passada única | GPT-5.6 Sol / Fable 5 | ponto reconhecidamente mais fraco do K3 |
| Auditoria de citações ABNT | modelo distinto do que redigiu | auditoria precisa de independência de contexto |
| Prospecção paralela em acervos | K3 Swarm Max | orquestração de subagentes é o desenho do produto |

O critério geral: **use o K3 quando o gargalo é volume de contexto ou custo de loop longo; mantenha outro modelo quando o gargalo é latência ou julgamento final.**

---

## 4. O contrato: AGENTS.md do `iconocracy-corpus`

A Moonshot recomenda explicitar restrições no prompt de sistema ou no AGENTS.md quando são necessários limites mais estreitos, justamente porque o K3 tende à proatividade excessiva — toma decisões não solicitadas ao encontrar ambiguidade ou pequeno obstáculo ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Para um corpus de tese, proatividade não supervisionada é dano metodológico. Cole o bloco abaixo em `AGENTS.md` na raiz do repositório e ajuste os caminhos.

```markdown
# AGENTS.md — iconocracy-corpus

## Contexto
Corpus de tese de doutorado (PPGD/UFSC) sobre alegoria feminina na cultura
jurídica, séculos XIX–XX. 328 registros. O argumento se organiza em
Entradas, Recusas e Coexistências.

## Fonte canônica
- `records.jsonl` é a ÚNICA fonte de verdade. 328 registros.
- `corpus-data.json` e `companion-data.json` estão defasados: os campos
  aninhados `iconocode` e `purificacao` não são achatados corretamente.
  Nunca use esses arquivos para estatística.
- Campos aninhados relevantes: `purificacao.regime_iconocratico`,
  `iconocode.pre_iconographic.country`, `iconocode.pre_iconographic.medium`,
  `iconocode.validation.in_scope`.

## Proibições absolutas
1. Não altere `records.jsonl` sem instrução explícita e sem diff mostrado antes.
2. Não invente metadados. Data ausente permanece ausente. Suporte não
   classificado permanece não classificado. 119 datas ausentes e 76 suportes
   não classificados são estado conhecido, não bug a ser preenchido.
3. Não crie referência bibliográfica, DOI, editora, ano ou número de página.
   Se não houver fonte no repositório, escreva `[FONTE PENDENTE]`.
4. Não reintroduza `endurecimento_score` nem qualquer agregação numérica de
   indicadores iconográficos. ENDURECIMENTO é lente qualitativa: inventário
   verbal de atributos.
5. Não use UNK em codificação humana. UNK pertence ao proxy. Humanos usam NC
   com causa tipada.
6. Não aplique recodificações do conjunto de 159 registros de baixa confiança
   diretamente nos dados. Proponha em CSV para revisão manual.

## Convenções
- Prosa acadêmica em português, ABNT rigorosa, voz natural e pessoal em
  trechos reflexivos, sem polimento robótico.
- Toda afirmação sobre uma imagem cita o `record_id`.
- Toda alteração de dados passa por PR com resumo do diff no corpo.
- Scripts em `tools/scripts/`, auditorias em `tools/audit/scripts/`.

## Ao encontrar ambiguidade
Pare e pergunte. Não escolha por conta própria. Registre a ambiguidade em
`docs/QUESTOES-ABERTAS.md`.
```

Esse arquivo é o investimento de maior retorno de todo o cookbook. Ele transforma a proatividade do K3 de risco em disciplina.

---

## 5. Receitas — escrita da tese

### 5.1 Revisão de coerência entre capítulos (próximo passo declarado)

O capítulo 9 fechou os oito painéis com 7.965 palavras e a etapa seguinte é a revisão de coerência com os capítulos 7 e 8. Isso é exatamente o tipo de tarefa que a janela de 1M destrava: os três capítulos inteiros na mesma janela, sem resumo intermediário.

```
Anexei os capítulos 7, 8 e 9 completos da tese e o esqueleto argumentativo
(Entradas, Recusas, Coexistências).

Faça uma revisão de coerência estrutural, não de estilo. Produza cinco listas:

1. CONCEITOS COM DEFINIÇÃO DIVERGENTE — termos definidos de um modo em um
   capítulo e de outro modo em outro. Cite as duas passagens literalmente.
2. AFIRMAÇÕES EM TENSÃO — pares de afirmações que não podem ser ambas
   verdadeiras sem qualificação adicional. Localize por capítulo e parágrafo.
3. PROMESSAS NÃO CUMPRIDAS — passagens que anunciam demonstração posterior
   que não encontro nos três capítulos.
4. REPETIÇÕES ARGUMENTATIVAS — o mesmo movimento feito duas vezes em lugares
   diferentes, indicando que um deles deve virar remissão.
5. TRANSIÇÕES FALTANTES — pontos onde o leitor perde o fio entre painéis.

Não reescreva nada. Não sugira melhorias de prosa. Apenas diagnostique com
citação literal e localização.
```

O pedido de citação literal é a salvaguarda: obriga o modelo a ancorar cada achado no texto, o que torna o falso positivo visível de imediato.

### 5.2 Painel de atlas a partir do corpus

O `corpus_to_argument.py` já transforma `records.jsonl` em rascunhos de evidência. Use o K3 como camada de prosa sobre a saída desse script, nunca sobre o corpus cru sem passar pela ferramenta.

```
Anexei: (a) a saída de corpus_to_argument.py para o recorte
[país/período/suporte], (b) o guia do Codificador B, (c) dois painéis já
escritos do Capítulo 9 como referência de voz.

Escreva o painel "[TÍTULO]" com 900 a 1.200 palavras.

Regras:
- Cada afirmação empírica remete a um record_id entre parênteses.
- Nenhuma imagem citada que não esteja na saída anexada.
- Vocabulário: entrada, recusa, coexistência, endurecimento como lente
  qualitativa. Nada de escore, índice ou média.
- Voz: prosa disciplinada, vocabulário rico, sem descrição ornamental.
  A montagem entre casos é a prova; não construa progressão cronológica.
- Ao final, seção "LACUNAS" listando o que o recorte não permite afirmar.
```

A seção de lacunas ao final é deliberada. Ela dá ao modelo um lugar legítimo para colocar a incerteza, o que reduz a pressão de preencher vazios com invenção dentro do corpo do texto.

### 5.3 Apêndice metodológico e defesa de método

Você tem um rascunho de apêndice sobre Panofsky preparado para revisão antes do envio ao orientador. O K3 é bom para o papel de arguidor.

```
Você é membro de banca de doutorado em História do Direito, cético quanto ao
uso de método iconológico em pesquisa jurídica. Anexei o apêndice
metodológico sobre Panofsky e Warburg.

Formule as dez objeções mais difíceis que você faria na defesa. Para cada uma:
- a objeção em uma frase seca;
- a passagem exata do apêndice que a torna possível;
- o que a autora precisaria acrescentar para neutralizá-la;
- se a objeção é fatal, séria ou apenas incômoda.

Ordene da mais fatal para a menos. Não elogie o texto. Não proponha redação.
```

### 5.4 Artigos de disciplina em ABNT

Para os artigos vinculados às disciplinas do semestre, o padrão é: o K3 estrutura e redige, e a autoridade final de citação permanece na ABNT verificada manualmente. O PR #147 já separou itens de literatura obtidos via Consensus da autoridade final de citação — mantenha essa separação com o modelo.

```
Anexei: fichamentos, o corpus de literatura em evidence/ com DOI verificado,
e o edital da disciplina.

Redija o artigo em ABNT rigorosa, 8.000 palavras, com esta estrutura:
[estrutura].

Restrições invioláveis:
- Cite APENAS itens presentes no arquivo de literatura anexado.
- Para cada citação, use exatamente autor, ano e página do anexo.
- Onde eu precisaria de uma fonte que não está no anexo, escreva
  [FONTE PENDENTE: descrição do que falta] e siga.
- Nunca complete uma referência incompleta a partir de memória.

Ao final, liste todos os [FONTE PENDENTE] em uma tabela.
```

---

## 6. Receitas — protocolo de catalogação (LPAI v2)

### 6.1 Codificação em lote com saída estruturada

O K3 aceita imagens por base64 e segue esquema de tool call da OpenAI, o que permite saída estruturada validável. O script abaixo é o esqueleto de um codificador-proxy.

```python
import base64, json, os
from openai import OpenAI

client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"],
                base_url="https://api.moonshot.ai/v1")

SISTEMA = open("prompts/lpai_v2_codificador.md").read()  # guia do Codificador B

ESQUEMA = {
  "type": "object",
  "required": ["record_id", "familia_alegorica", "atributos",
               "regime_iconocratico", "confianca", "justificativa"],
  "properties": {
    "record_id": {"type": "string"},
    "familia_alegorica": {"type": "string",
      "description": "Justitia, Libertas, Respublica, Marianne, Germania, "
                     "Britannia, Columbia, outra, ou UNK"},
    "atributos": {"type": "array", "items": {"type": "string"},
      "description": "inventario verbal, sem escore"},
    "regime_iconocratico": {"type": "string"},
    "recusa": {"type": "string",
      "description": "substituicao_remasculinizante | negacao_pura | "
                     "feminino_esvaziado | substituicao_neutro_abstrata | nenhuma"},
    "confianca": {"type": "string", "enum": ["alta", "media", "baixa"]},
    "justificativa": {"type": "string",
      "description": "o que na imagem sustenta a classificacao"},
    "duvidas": {"type": "array", "items": {"type": "string"}}
  }
}

def codificar(caminho_img, record_id, metadados):
    b64 = base64.b64encode(open(caminho_img, "rb").read()).decode()
    r = client.chat.completions.create(
        model="kimi-k3",
        messages=[
            {"role": "system", "content": SISTEMA},
            {"role": "user", "content": [
                {"type": "text", "text":
                 f"record_id: {record_id}\nmetadados conhecidos: "
                 f"{json.dumps(metadados, ensure_ascii=False)}\n\n"
                 "Codifique conforme LPAI v2. Use UNK quando a evidencia "
                 "visual for insuficiente. Nao infira pais, data ou suporte "
                 "que nao estejam nos metadados."},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]}
        ],
        tools=[{"type": "function", "function": {
            "name": "registrar_codificacao",
            "parameters": ESQUEMA}}],
        tool_choice={"type": "function",
                     "function": {"name": "registrar_codificacao"}}
    )
    return json.loads(r.choices[0].message.tool_calls[0].function.arguments)
```

Três decisões embutidas nesse código merecem explicitação. Primeiro, o prompt de sistema é o guia do Codificador B, não uma paráfrase — a consistência entre codificadores depende de instrumento idêntico. Segundo, a saída vai para `proposed_class` como proxy, jamais para o campo de classe humana; a distinção entre codificação humana e proxy é o que sustenta o cálculo de kappa. Terceiro, o campo `duvidas` existe para capturar o que o modelo não deveria resolver sozinho, alimentando a fila de refinamento do protocolo.

### 6.2 Cálculo de concordância

O `compute_kappa.py` é gerador independente de relatório e assim deve permanecer. O papel do K3 é interpretar a saída, não produzi-la.

```
Anexei o relatório de compute_kappa.py comparando codificação humana cega e
proposed_class do K3 no golden set de 30 itens, equilibrado por regime, país
e mídia.

Produza:
1. Onde a discordância se concentra: por família alegórica, por país, por mídia.
2. Quais discordâncias são armadilhas conhecidas do protocolo
   (Justitia/Aequitas, Libertas/Marianne) e quais são novas.
3. Para cada categoria de discordância nova, proponha o refinamento mínimo
   da regra de decisão do LPAI v2 que a resolveria — uma frase por regra.
4. Quais itens deveriam sair do golden set por serem intrinsecamente NC.

Trate discordância como dado de refinamento do instrumento, não como erro
de codificador. Não calcule kappa novamente; use os números do relatório.
```

### 6.3 Fila de auditoria dos 159 registros de baixa confiança

O conjunto de revisão metodológica de 159 registros vive em Google Sheets, filtrado por `audit_recodification.py` sobre origens `vault-import`, `hermes-auto`, `migration` e `batch-tentative`. O K3 entra como proponente, nunca como aplicador.

```
Anexei o CSV dos 159 registros de baixa confiança e as imagens
correspondentes aos 20 primeiros.

Para cada registro produza uma linha de proposta com as colunas:
record_id | campo | valor_atual | valor_proposto | evidencia | confianca |
acao_recomendada

Regras:
- evidencia descreve o que na imagem ou nos metadados sustenta a proposta;
- se a evidência for insuficiente, valor_proposto = MANTER e
  acao_recomendada = "requer inspeção humana";
- nunca proponha data ou país sem elemento visual ou textual que os ancore;
- não toque em registros de origem iconocode-opus-4.6-metadata-refined.

Saída em CSV puro, pronto para colar na planilha de revisão.
```

### 6.4 Auditoria de saúde do corpus

A checagem semanal #155 registrou estado verde, 328 registros válidos, 85% da codificação de ENDURECIMENTO concluída, `ARQUITETURA FORENSE` sem itens, 76 suportes não classificados e 119 datas ausentes ou não parseáveis. Automatize o relatório e use o K3 para a leitura.

```
Anexei records.jsonl (328 registros) e a issue de health check da semana
anterior.

Produza o relatório desta semana com:
1. Contagens atuais por regime, país, suporte, década.
2. Delta em relação à semana anterior, campo por campo.
3. Lacunas estruturais: quais células da matriz país × período × suporte
   estão vazias e quais dessas ausências são substantivas (o objeto não
   existe) e quais são de coleta (o objeto existe e falta prospectar).
4. Estado de ARQUITETURA FORENSE e o que seria necessário para preenchê-lo.
5. Semáforo justificado: VERDE, AMARELO ou VERMELHO, com a razão.

Leia os campos aninhados corretamente: purificacao.regime_iconocratico,
iconocode.pre_iconographic.country, iconocode.pre_iconographic.medium,
iconocode.validation.in_scope. Não use corpus-data.json.
```

A distinção entre ausência substantiva e ausência de coleta no item 3 é o coração metodológico da tese: uma célula vazia pode ser uma recusa histórica ou apenas uma falha de prospecção, e confundir as duas produziria uma afirmação falsa sobre o Estado.

---

## 7. Receitas — estudos historiográficos

### 7.1 Revisão sistemática com enxame

O K3 Swarm Max é posicionado para revisões de literatura, pesquisa ampla, coleta de dados em larga escala e geração de relatórios longos ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Aplique com protocolo PRISMA, mantendo a triagem humana nas fases decisivas.

```
Tarefa de revisão sistemática, protocolo PRISMA.

Pergunta: [pergunta de revisão]
Bases: [Scielo, JSTOR, HeinOnline, Persée, Consensus, Elicit]
Janela: [período]
Idiomas: português, italiano, francês, inglês, espanhol

Para cada item recuperado registre: autores, ano, título, veículo, DOI ou
URL estável, idioma, tipo de fonte, resumo em três linhas, e uma
classificação de relevância (núcleo, periferia, descarte) com justificativa.

Não inclua item cujo DOI ou URL você não conseguiu abrir. Não complete
metadados por inferência. Ao final entregue o fluxograma PRISMA com as
contagens de cada fase e a lista de exclusões com motivo.

Saída: CSV para a planilha de triagem + relatório em markdown.
```

O resultado entra como evidência de pesquisa com gancho de capítulo e checagem cruzada de DOI/editora, separado dos metadados canônicos de imagem — a arquitetura que o PR #147 estabeleceu.

### 7.2 Auditoria de citações

Esta é a receita que você não deve rodar no mesmo modelo que escreveu o texto. Use o K3 para auditar o que outro modelo redigiu, e vice-versa. A independência de contexto é o mecanismo.

```
Você recebe um texto acadêmico e sua bibliografia. Sua única tarefa é
verificar integridade bibliográfica. Você não conhece o autor nem o
argumento e não deve avaliá-lo.

Para cada entrada da bibliografia, verifique na web:
1. A obra existe com esse título?
2. A autoria está correta e completa?
3. O ano e a edição conferem?
4. O veículo (editora, revista, volume, número) existe e confere?
5. A obra citada sustenta a afirmação do trecho em que é invocada?

Classifique cada entrada: VERIFICADA | ANO INCORRETO | AUTORIA INCORRETA |
VEÍCULO INCORRETO | NÃO ENCONTRADA | CONTEXTO INADEQUADO.

Para tudo que não seja VERIFICADA, mostre a evidência da checagem com URL.
Liste separadamente as citações no corpo do texto sem entrada correspondente
na bibliografia e as entradas nunca citadas.
```

### 7.3 Memorial de leitura

Para memoriais das disciplinas, o padrão é síntese, análise, evidência historiográfica, questões não resolvidas e, opcionalmente, uma camada crítica.

```
Anexei [texto/textos] e minhas notas de leitura.

Escreva um memorial de leitura em português, 1.800 a 2.500 palavras, nesta
ordem: síntese fiel do argumento; análise do aparato conceitual e das
fontes mobilizadas; situação historiográfica do texto (com quem dialoga,
contra quem escreve); questões que o texto deixa abertas; e uma seção final
"diabólica" com a objeção mais desconfortável que o texto merece.

Voz: calorosa mas rigorosa, primeira pessoa, sem polimento robótico e sem
argumentação excessiva. Não resuma o que eu já anotei — parta das minhas
notas e avance.
```

---

## 8. Receitas — análise iconográfica com visão

### 8.1 IconoCode em imagem única

```
Anexo uma imagem do corpus. Metadados conhecidos: [país, data, suporte,
instituição emissora, acervo].

Faça a leitura em três níveis, sem misturá-los:

NÍVEL PRÉ-ICONOGRÁFICO — apenas o que está visível. Figuras, posturas,
objetos, vestuário, inscrições transcritas literalmente, técnica, estado de
conservação. Nada de nomes de personificações neste nível.

NÍVEL ICONOGRÁFICO — identificação de tipos e atributos, com a regra que
os sustenta. Onde dois tipos concorrem (Justitia/Aequitas,
Libertas/Marianne), apresente ambos e o critério de decisão.

NÍVEL ICONOLÓGICO — hipótese sobre função jurídico-política, marcada
explicitamente como hipótese, com o que a confirmaria ou refutaria.

Ao final: classificação LPAI v2, regime iconocrático, tipologia de recusa
se houver, e um campo DÚVIDAS com o que a imagem não permite decidir.

Se a resolução for insuficiente para um atributo, diga NC com a causa.
Não infira o que não está visível.
```

A separação estrita dos três níveis não é formalidade panofskyana: é o que permite auditar depois qual camada falhou quando uma leitura se revela errada.

### 8.2 Rimas visuais e coexistências

Aqui a janela longa e a visão nativa se combinam de um modo que não existia antes: dezenas de imagens na mesma consulta.

```
Anexei 24 imagens do corpus, cada uma identificada pelo record_id no nome
do arquivo, mais o CSV de metadados.

Não classifique. Encontre relações:

1. RIMAS FORMAIS — pares ou grupos que compartilham solução visual
   (postura, enquadramento, atributo, tratamento do corpo), com descrição
   da rima e os record_id envolvidos.
2. COEXISTÊNCIAS — casos em que corpos alegóricos incompatíveis convivem
   no mesmo objeto ou na mesma série institucional.
3. SUBSTITUIÇÕES EM SÉRIE — sequências onde um corpo feminino é
   substituído, distinguindo remasculinização, negação pura, feminino
   esvaziado e substituição neutro-abstrata.
4. FALSAS RIMAS — semelhanças que provavelmente são coincidência técnica
   do suporte, não citação visual.

Para cada relação, indique a força da evidência e o que precisaria ser
verificado em outra fonte.
```

O item 4 é a salvaguarda. Sem ele, um modelo treinado para encontrar padrões encontra padrões onde há apenas restrição do meio — duas moedas se parecem porque são moedas.

### 8.3 Prospecção de acervos (SCOUT)

A campanha de julho alcançou 15 candidatos verificados visualmente no Brasil, França, Alemanha, Reino Unido, Bélgica e Estados Unidos, cobrindo moedas, papel-moeda, selos, gravuras, cartazes e monumentos, deixando material nativamente belga como a coluna fraca remanescente.

```
Campanha de prospecção. Alvo: material nativamente belga, 1880–1940,
alegoria feminina em contexto jurídico-estatal.

Acervos: Europeana, KBR, Gallica, British Museum, Numista, Colnect,
Library of Congress.

Para cada candidato entregue uma nota atômica pronta para Obsidian, com
frontmatter: id SCOUT-XXX, título, acervo, identificador estável, URL,
país, data, suporte, dimensões, licença, status de verificação visual.

Corpo da nota: leitura pré-iconográfica, hipótese iconográfica, regime
iconocrático provável, encaixe no capítulo, e o que falta verificar.

Não inclua candidato cuja imagem você não conseguiu ver. Não inclua
candidato sem identificador estável de acervo. Marque explicitamente
quando a atribuição de data for do acervo e quando for sua inferência.
```

---

## 9. Receitas — desenvolvimento web

O K3 debutou em primeiro lugar no Frontend Code Arena com 1679 pontos ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)) e traduz entradas visuais diretamente em código de produção, incluindo depuração de layout a partir de captura de tela ([SiliconFlow](https://www.siliconflow.com/blog/kimi-k2.5-now-on-siliconflow-sota-on-visual-agentic-intelligence)). Para as suas propriedades, isso vale muito.

### 9.1 Trabalho visual em `iconocracia.com` e `anavanzin.com`

O padrão mais produtivo é o loop de captura de tela: você mostra o estado atual e a referência, e o modelo corrige o CSS.

```
Anexo duas imagens: (1) captura da sala de pôsteres Tabula no estado atual,
(2) a referência de composição que quero.

Diagnostique as diferenças de grade, ritmo vertical, escala tipográfica e
peso visual. Depois produza o patch mínimo de CSS que aproxima (1) de (2).

Restrições:
- não introduza dependência nova nem framework;
- preserve a identidade acadêmica existente e o contraste acessível
  (WCAG AA como piso);
- a superfície deve ler como uma placa acadêmica composta, não como um
  rastro de gerenciamento de projeto;
- nada de arquivos internos de fluxo de trabalho ou caminhos locais
  chegando ao build público;
- mostre o diff, não o arquivo inteiro.
```

### 9.2 Workers, Pages e implantação

A arquitetura já está decidida: `anavanzin.com` como site pessoal estável no caminho Pages, `iconocracia.com` orientado a Workers quando precisa de APIs, Durable Objects, Queues ou ingestão. Peça ao K3 código que respeite essa divisão.

```
Contexto de infraestrutura: GitHub como fonte da verdade, Cloudflare como
DNS/borda, Pages para o caminho editorial estático, Workers para APIs e
filas. Um repositório por domínio.

Tarefa: [descrição].

Requisitos de implantação:
- GitHub Actions com Wrangler, ambientes de staging e produção separados;
- tokens Cloudflare de escopo mínimo, segredos por ambiente;
- restrição de branch e revisor obrigatório para produção;
- nenhuma credencial em arquivo versionado.

Entregue: wrangler.toml, workflow de Actions, código do Worker, e uma
seção "riscos" com o que pode quebrar na primeira implantação.
```

### 9.3 SQL sobre o MotherDuck

O esquema define `source_file`, `page`, `label`, `caption`, `thumbnail` e a view `searchable_corpus` que une OCR, rótulos e miniaturas por página.

```
Esquema anexado (source_file, page, label, caption, thumbnail,
view searchable_corpus).

Escreva a consulta que [pergunta]. Requisitos:
- DuckDB/MotherDuck dialect;
- comente cada CTE explicando o que ela isola;
- inclua contagem de linhas esperada e como eu verifico se o resultado
  está errado;
- não use SELECT *;
- se a pergunta não puder ser respondida com este esquema, diga qual
  campo falta em vez de inventar um.
```

---

## 10. Cadência semanal

O ritmo abaixo encaixa o K3 na disciplina de auditoria que você já mantém, sem criar cerimônia nova.

**Segunda — corpus.** Health check automatizado (receita 6.4), leitura do relatório, abertura da issue da semana. Vinte minutos.

**Terça e quarta — escrita.** Blocos longos de painel ou capítulo com o corpus em contexto (receitas 5.1 e 5.2). Uma sessão de K3, um painel. Encerre a sessão ao terminar o painel: sessões longas acumulam histórico de raciocínio e o K3 é sensível a isso.

**Quinta — catalogação.** Lote de codificação proxy (6.1), proposta de recodificação (6.3), e revisão humana das propostas na planilha. A revisão humana é intransferível.

**Sexta — historiografia e web.** Revisão sistemática incremental (7.1) ou trabalho de front-end (9.1). Sexta é o dia natural para auditoria de citações (7.2) do que foi escrito na semana.

**Sábado — prospecção.** Uma campanha SCOUT (8.3) por semana, priorizando a coluna fraca do momento — hoje, material belga.

**Domingo — nada.** O corpus continua lá.

---

## 11. Guardrails e antipadrões

**Alucinação bibliográfica.** É o risco existencial. Um modelo que produz prosa acadêmica fluente produz também referências fluentes e inexistentes. Contramedida: a proibição 3 do AGENTS.md, o marcador `[FONTE PENDENTE]`, e a auditoria de citações rodada em modelo distinto do redator.

**Preenchimento de lacuna.** As 119 datas ausentes e os 76 suportes não classificados são estado conhecido do corpus, e um modelo proativo tentará resolvê-los. Uma data inferida que entra no `records.jsonl` sem marcação contamina toda a análise temporal. Contramedida: proibição 2, e o campo `evidencia` obrigatório em qualquer proposta de recodificação.

**Retorno da aritmética.** O `endurecimento_score` foi removido por decisão metodológica; ENDURECIMENTO é lente qualitativa e inventário verbal. Modelos gostam de agregar em números porque números parecem rigor. Contramedida: proibição 4, e vigilância sobre qualquer tabela que apresente média, índice ou escore composto de atributos iconográficos.

**Sensibilidade ao histórico de raciocínio.** Se o harness não devolve o histórico de raciocínio corretamente, ou se uma sessão iniciada em outro modelo é trocada para K3 no meio da conversa, a qualidade da saída fica instável ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Contramedida: um modelo por sessão, sem troca no meio; prefira a Kimi Code CLI para trabalho agêntico longo.

**Deslize de identidade.** O K3 já foi observado se autodenominando Claude, descrita como marca de destilação ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)). Irrelevante para o resultado, mas útil saber que não é sinal de configuração errada.

**Confundir barato por token com barato por tarefa.** O K3 roda em esforço máximo, emite mais tokens de saída e demora mais; a latência por tarefa pode subir mesmo com preço por token menor ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)). Contramedida: não use K3 para edição interativa.

**Proatividade em ambiguidade.** O modelo decide sozinho quando encontra obstáculo pequeno. Contramedida: a cláusula final do AGENTS.md — pare, pergunte, registre em `docs/QUESTOES-ABERTAS.md`.

---

## 12. Custo: como pensar

A economia do K3 depende inteiramente de cache. Entrada em cache custa um décimo da entrada sem cache, e a Moonshot relata taxa de acerto acima de 90% em cargas de codificação na própria infraestrutura ([Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)). Um turno com 100 mil tokens em cache, 2 mil tokens novos de entrada e saída normal sai por cerca de oito centavos de dólar, aproximadamente 77% mais barato que o mesmo turno sem cache ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)).

Três táticas decorrem disso.

**Estabilize o prefixo.** Coloque o que não muda no início e sempre na mesma ordem: prompt de sistema, guia do Codificador B, esquema, AGENTS.md. A variação vai no fim. Prefixo estável é cache aproveitado.

**Agrupe por sessão temática.** Uma sessão por painel de atlas, uma por lote de catalogação, uma por campanha de prospecção. Sessões temáticas reaproveitam o mesmo contexto pesado dezenas de vezes.

**Cuidado com a busca web.** Chamadas de busca são cobradas separadamente, US$ 0,004 cada ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)). Uma revisão sistemática com enxame pode fazer centenas delas. Isso é aceitável e barato, mas deve ser previsto, não descoberto na fatura.

Sobre autohospedagem: com 2,8 trilhões de parâmetros, a Moonshot recomenda servir em supernós com 64 ou mais aceleradores, e o piso realista em 4 bits fica em torno de 1,4 TB ([guia de setup](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)). Rodar o K3 localmente não é uma opção para você, e não precisa ser. A abertura dos pesos importa por auditabilidade e por longevidade do método, não por autohospedagem doméstica.

---

## 13. Primeira semana

**Dia 1.** Chave da Moonshot criada e exportada fora de repositório. Kimi Code CLI instalada, `/login` feito, `kimi --version` confirmado.

**Dia 2.** `AGENTS.md` da seção 4 colado no `iconocracy-corpus`, revisado e ajustado aos caminhos reais. Commit em branch própria, PR aberto. Este é o dia mais importante.

**Dia 3.** Teste de visão: cinco imagens já codificadas manualmente passam pela receita 8.1. Compare com sua codificação. Você está calibrando o instrumento, não avaliando o modelo.

**Dia 4.** Rode a receita 6.4 (saúde do corpus) e confira contra a issue #155. Se os números divergirem, o problema é leitura de campo aninhado, não o corpus.

**Dia 5.** Rode a receita 5.1 nos capítulos 7, 8 e 9. Esse é o entregável que justifica a adoção.

**Dia 6.** Uma campanha SCOUT belga (8.3). Verifique visualmente cada candidato antes de aceitar.

**Dia 7.** Escreva em `docs/QUESTOES-ABERTAS.md` o que a semana revelou sobre onde o K3 ajuda e onde atrapalha. Atualize este cookbook. Um manual que não é revisado depois do primeiro contato com o material é ficção.

---

## 14. Fontes

- [Moonshot AI launches Kimi K3 — Constellation Research](https://www.constellationr.com/insights/news/moonshot-ai-launches-kimi-k3)
- [China's Moonshot AI unveils Kimi K3 — CNBC](https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html)
- [Moonshot claims Kimi K3 can rival OpenAI and Anthropic — BBC](https://www.bbc.com/news/articles/cy9w4q8pgp0o)
- [China's Moonshot releases breakthrough AI model for download — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-27/china-s-moonshot-to-release-breakthrough-ai-model-for-download)
- [Kimi K3: The Complete Guide to Moonshot AI's 2.8T Model — Amplifi Labs](https://www.amplifilabs.com/post/kimi-k3-the-complete-guide-to-moonshot-ais-2-8t-model)
- [Kimi K3 for Agentic Coding: Claude Code + CLI Setup Guide](https://avinashsangle.com/blog/kimi-k3-agentic-coding-guide)
- [Kimi K2.5 on SiliconFlow: SOTA on Visual Agentic Intelligence](https://www.siliconflow.com/blog/kimi-k2.5-now-on-siliconflow-sota-on-visual-agentic-intelligence)
- [Workers AI now runs large models, starting with Kimi K2.5 — Cloudflare](https://blog.cloudflare.com/workers-ai-large-models/)
- [Moonshot AI unveils Kimi K3, first open 3T-class AI model — ForkLog](https://forklog.com/en/moonshot-ai-unveils-kimi-k3-first-open-3t-class-ai-model/)
- [Kimi K3 Release: Open Frontier Intelligence at 2.8T Scale — Digital Applied](https://www.digitalapplied.com/blog/kimi-k3-open-frontier-model-release-2026)

Contexto interno de referência: `records.jsonl` (328 registros), guia do Codificador B (LPAI v2), [PR #139 — oito painéis do Atlas](https://github.com/anavvanzin/iconocracy-corpus/pull/139), [PR #147 — separação de sincronização de literatura](https://github.com/anavvanzin/iconocracy-corpus/pull/147), [issue #155 — health check semanal](https://github.com/anavvanzin/iconocracy-corpus/issues/155), [audit_recodification.py](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/scripts/audit_recodification.py), [corpus_to_argument.py](https://github.com/anavvanzin/iconocracy-corpus/blob/main/tools/audit/scripts/corpus_to_argument.py).
