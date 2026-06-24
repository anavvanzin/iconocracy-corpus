# Cookbook — Pesquisa Historiográfica e Iconográfica

**Projeto:** Iconocracia · Ana Vanzin · PPGD/UFSC · 2026
**Complementa:** `MANUAL.md` (ops), `OPERATING_MODEL.md` (modelo), `methodology.md` (método)
**Formato:** receitas de ação — o quê fazer, quando e como

---

## Índice

1. [Princípios de cozinha](#1-princípios-de-cozinha)
2. [Receita 1 — Descobrir uma nova fonte iconográfica](#2-receita-1--descobrir-uma-nova-fonte-iconográfica)
3. [Receita 2 — Analisar uma imagem (protocolo IconoCode)](#3-receita-2--analisar-uma-imagem-protocolo-iconocode)
4. [Receita 3 — Contextualizar historicamente uma imagem](#4-receita-3--contextualizar-historicamente-uma-imagem)
5. [Receita 4 — Incorporar uma imagem ao corpus](#5-receita-4--incorporar-uma-imagem-ao-corpus)
6. [Receita 5 — Pesquisa bibliográfica historiográfica](#6-receita-5--pesquisa-bibliográfica-historiográfica)
7. [Receita 6 — Ler e anotar uma fonte primária](#7-receita-6--ler-e-anotar-uma-fonte-primária)
8. [Receita 7 — Ler e anotar um texto secundário](#8-receita-7--ler-e-anotar-um-texto-secundário)
9. [Receita 8 — Escrever uma análise iconográfica](#9-receita-8--escrever-uma-análise-iconográfica)
10. [Receita 9 — Citar corretamente (ABNT e Chicago)](#10-receita-9--citar-corretamente-abnt-e-chicago)
11. [Receita 10 — Sessão de pesquisa: abertura e fechamento](#11-receita-10--sessão-de-pesquisa-abertura-e-fechamento)
12. [Referência rápida — Arquivos digitais](#12-referência-rápida--arquivos-digitais)
13. [Referência rápida — Iconclass](#13-referência-rápida--iconclass)
14. [Referência rápida — Terminologia Panofsky](#14-referência-rápida--terminologia-panofsky)

---

## 1. Princípios de cozinha

**Mise en place antes de cozinhar.** Antes de analisar uma imagem, garanta que você tem: resolução suficiente, data e local de produção, suporte material, encomendante. Análise sem contexto é especulação.

**Hierarquia de fontes.** Fonte primária > fonte secundária > enciclopédia/Iconclass. Nunca cite a enciclopédia como autoridade interpretativa.

**Registro imediato.** Toda descoberta vai para o vault *antes* de ser esquecida. Um registro imperfeito agora vale mais que um registro perfeito nunca.

**Separar descrição de interpretação.** O que *está* na imagem (nível 1–2 Panofsky) nunca mistura com o que a imagem *significa* (nível 3). Essa separação é metodológica, não estilística.

**Rastreabilidade antes de tudo.** Toda imagem no corpus precisa de URL persistente ou localização física verificável. Imagem sem procedência não entra.

---

## 2. Receita 1 — Descobrir uma nova fonte iconográfica

**Quando usar:** busca ativa em arquivos digitais, varredura de coleções, follow-up de referências bibliográficas.

### Ingredientes

- Acesso aos arquivos (ver §12)
- Conta Zotero ativa
- Terminal com `conda activate iconocracy`

### Passo a passo

**1. Formular a query de busca**

```
[sujeito alegórico] + [suporte] + [período] + [jurisdição]
```

Exemplos:
```
"Justiça" moeda Brasil 1900
"République" billet franc XIXe
allegory law seal United States 1870
```

Prefira operadores booleanos nos arquivos que suportam:
```
("alegoria" OR "allegory") AND ("direito" OR "lei" OR "justiça") AND (date:[1800 TO 1950])
```

**2. Verificar proveniência antes de registrar**

Antes de qualquer análise, confirme:
- [ ] Suporte físico identificado (moeda / selo / monumento / quadro / gravura)
- [ ] Data de produção (ao menos década)
- [ ] Jurisdição / emissor
- [ ] URL persistente ou referência de arquivo com número de catálogo

Se algum item não puder ser confirmado, registre como `status: candidato` e marque `provenance_uncertain: true` no record.

**3. Captura mínima**

```bash
# Criar nota candidata no vault (padrão XX-NNN)
# Exemplo: BR-165 para o 165º candidato brasileiro
touch ~/Research/iconocracy-corpus/vault/candidatos/BR-165\ Nome-da-Imagem.md
```

Campos obrigatórios na nota candidata:
```markdown
---
id: BR-165
status: candidato
suporte:
data_producao:
jurisdicao:
url_fonte:
data_captura: 2026-05-14
---
```

**4. Verificar duplicatas antes de continuar**

```bash
conda activate iconocracy
cd ~/Research/iconocracy-corpus
python tools/scripts/corpus_pipeline.sh check BR-165
# ou manualmente:
grep "BR-165\|Nome-da-Imagem" data/processed/records.jsonl | head -5
```

**5. Salvar imagem de alta resolução**

```bash
# Destino padrão (binários não versionados no git — ver ADR-001)
mkdir -p data/raw/images/BR-165/
# Baixar e nomear: {id}_{suporte}_{ano}.{ext}
wget -O data/raw/images/BR-165/BR-165_moeda_1900.jpg "URL_DA_IMAGEM"
```

---

## 3. Receita 2 — Analisar uma imagem (protocolo IconoCode)

**Quando usar:** a imagem passou pela Receita 1 e está pronta para análise formal.

### Os três níveis de Panofsky

| Nível | Nome | Pergunta | Produtos |
|-------|------|----------|---------|
| 1 | Pré-iconográfico | O que *vejo*? | Descrição factual de formas, cores, figuras, gestos |
| 2 | Iconográfico | O que *significa* cada elemento? | Identificação de atributos, convenções, alegorias |
| 3 | Iconológico | Qual o *sentido cultural* da obra? | Interpretação histórica, função social, ideologia |

### Passo a passo

**Nível 1 — Descrição pré-iconográfica**

Descreva sem nomear. Substitua "Justiça" por "figura feminina em pé, drapeado branco, olhos vendados, segurando balança na mão direita e espada apontada para baixo na esquerda." Teste: alguém sem cultura ocidental conseguiria desenhar a cena?

```markdown
## N1 — Descrição
Figura central: [gênero, postura, vestuário, gestos]
Elementos secundários: [objetos, animais, arquitetura, inscrições]
Composição: [enquadramento, perspectiva, hierarquia visual]
Suporte e técnica: [material, dimensão se disponível]
```

**Nível 2 — Análise iconográfica**

Identifique as convenções culturais em operação. Consulte:
- Iconclass (§13) para atributos convencionais
- Ripa, *Iconologia* (1593) para alegorias clássicas
- Fontes da época do objeto para convenções locais

```markdown
## N2 — Iconografia
Atributos identificados: [balança → Justiça; espada → poder executivo; venda → imparcialidade]
Iconclass: [48C7341 = Justice with scales and sword]
Variantes nacionais: [ausência de venda = tradição brasileira antes de 1900?]
Fontes iconográficas consultadas:
```

**Nível 3 — Interpretação iconológica**

Contextualize historicamente. Quem encomendou, para quê, em qual conjuntura política, para qual público.

```markdown
## N3 — Iconologia
Encomendante e contexto de produção:
Função original (circulação, exposição, uso ritual):
Conjuntura política:
O que a imagem naturaliza / apaga:
Relação com outros objetos do corpus:
```

**10 indicadores de endurecimento (escala 0–3)**

Após os três níveis, codar os indicadores do protocolo ICONOCRACY:

| # | Indicador | 0 | 1 | 2 | 3 |
|---|-----------|---|---|---|---|
| E1 | Militarização | nenhuma | insígnia sutil | arma presente | postura militar explícita |
| E2 | Nudez alegórica | sem nudez | ombros/braços | seios expostos | nudez total |
| E3 | Insígnia jurídica | nenhuma | 1 atributo | 2 atributos | conjunto completo |
| E4 | Hierarquia de gênero | figura masculina domina | paridade | figura fem. secundária | figura fem. central soberana |
| E5 | Emblema estatal | nenhum | brasão/armas | bandeira/coroa | múltiplos emblemas |
| E6 | Expressão corporal | neutra | submissa | assertiva | dominante |
| E7 | Pureza racial | não legível | ambíguo | eurocentrado | explicitamente branca |
| E8 | Inscrição textual | nenhuma | legenda | lema | texto doutrinário |
| E9 | Suporte de poder | objeto neutro | moeda/papel | monumento | espaço institucional |
| E10 | Temporalidade | atemporal | histórica | contemporânea | futura/utópica |

```bash
# Atualizar registro com codificação
python tools/scripts/code_purification.py --item BR-165 --indicators E1=2,E2=0,E3=3,...
```

---

## 4. Receita 3 — Contextualizar historicamente uma imagem

**Quando usar:** após N2, antes de escrever N3.

### Perguntas de contextualização

**Sobre o objeto:**
- Em que conjuntura política o objeto foi produzido?
- Que debate jurídico, constitucional ou político estava em curso?
- Quem financiou / encomendou / aprovou o design?
- Havia modelos concorrentes rejeitados? (procurar nos arquivos)

**Sobre a circulação:**
- Qual o suporte (moeda, selo, monumento) e o que isso implica sobre o público?
- O objeto foi reformado, substituído ou censurado? Quando e por quê?
- Existem versões de outros países do mesmo período para comparar?

**Sobre a tradição iconográfica:**
- De onde vem cada atributo? (linha Ripa → adaptações nacionais → versão local)
- A imagem cita conscientemente uma tradição ou rompe com ela?
- Existe um *Nachleben* (sobrevivência warburguiana) identificável?

### Fontes prioritárias para contextualização

```
1. Documentos de encomenda e atas de aprovação (arquivos nacionais)
2. Imprensa da época (Hemeroteca Digital BN, Gallica presse)
3. Debates parlamentares (Câmara, Senado — bases digitalizadas)
4. Outros objetos do corpus do mesmo período
5. Historiografia secundária especializada
```

---

## 5. Receita 4 — Incorporar uma imagem ao corpus

**Quando usar:** análise completa, procedência verificada, codificação feita.

```bash
conda activate iconocracy
cd ~/Research/iconocracy-corpus

# 1. Validar o record antes de adicionar
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record

# 2. Adicionar ao ledger canônico
# (editar records.jsonl diretamente ou usar o script de adição)
python tools/scripts/add_record.py --id BR-165 --file data/raw/BR-165_metadata.json

# 3. Sincronizar com vault
python tools/scripts/vault_sync.py sync

# 4. Exportar corpus público
python tools/scripts/records_to_corpus.py --diff   # preview
python tools/scripts/records_to_corpus.py          # aplicar

# 5. Validar export
python tools/scripts/validate_schemas.py corpus/corpus-data.json

# 6. Commit
git add data/processed/records.jsonl corpus/corpus-data.json vault/candidatos/
git commit -m "feat(corpus): add BR-165 [Nome] — [suporte], [ano]"
```

---

## 6. Receita 5 — Pesquisa bibliográfica historiográfica

**Quando usar:** início de um capítulo, revisão de literatura, auditoria de lacunas.

### Estratégia em camadas

**Camada 1 — Identificar os debates centrais**

Antes de buscar artigos, mapeie os *debates*, não os títulos:
```
Debate 1: [formulação da questão]
Debate 2: [posição A vs posição B]
Debate 3: [questão em aberto]
```

**Camada 2 — Busca sistemática**

Bases prioritárias para história do direito e iconografia:
```
JSTOR          — história, direito, história da arte
Google Scholar — cobertura ampla, citações
SciELO         — produção brasileira e latino-americana
Capes Periódicos — acesso institucional UFSC
Hemeroteca Digital BN — fontes primárias BR
Gallica BnF    — fontes primárias FR
```

Query padrão:
```
"[conceito-chave]" AND ("Brasil" OR "Brazil") AND [período]
```

**Camada 3 — Bola de neve**

Para cada artigo relevante encontrado:
1. Verificar a bibliografia (quem esse autor cita?)
2. Verificar quem cita esse artigo (Google Scholar → "citado por")
3. Identificar os autores que aparecem repetidamente (são os canônicos do debate)

**Camada 4 — Zotero**

```
Para cada texto selecionado:
□ Salvar no Zotero com metadados completos
□ Verificar: autor, ano, título, periódico, DOI/URL, página
□ Adicionar à coleção correta (Tese > Capítulo X > [subtema])
□ Tag: [debate-central] + [relevância: alta/media/baixa]
```

### Avaliar relevância antes de ler

Use este filtro rápido (2 minutos por texto):
1. Ler resumo/abstract
2. Ler introdução (primeiros 3 parágrafos)
3. Ler conclusão (últimos 3 parágrafos)
4. Verificar se as fontes primárias usadas se sobrepõem com o corpus

Só leia o texto completo se passou nos 4 pontos.

---

## 7. Receita 6 — Ler e anotar uma fonte primária

**Fonte primária:** documento, imagem, objeto produzido na época estudada.

### Antes de ler

- [ ] Identificar o gênero documental (lei, discurso, carta, panfleto, regulamento)
- [ ] Identificar quem produziu, para quem, em que contexto institucional
- [ ] Identificar o que *não* está dito / quem está ausente

### Durante a leitura

Anote em três colunas mentais:

| O que diz | O que implica | O que omite |
|-----------|---------------|-------------|
| Citação literal | Inferência direta | Silêncio significativo |

### Formatos de nota no vault

```markdown
---
tipo: fonte-primaria
id_vault: FP-001
titulo:
data_producao:
autor_institucional:
localizacao: [arquivo / URL]
data_consulta: 2026-05-14
---

## Transcrição / excertos relevantes

> "citação literal com referência de página"

## O que implica

## O que omite / apaga

## Relação com o corpus

## Citação ABNT
```

---

## 8. Receita 7 — Ler e anotar um texto secundário

**Texto secundário:** historiografia, análise, interpretação produzida por outro pesquisador.

### Antes de ler

Formule uma pergunta que o texto deve responder para a sua tese. Se não tiver uma pergunta, a leitura será passiva.

```
Pergunta: [O que este texto me diz sobre X que eu não encontro em outro lugar?]
```

### Estrutura da nota de leitura

```markdown
---
tipo: leitura-secundaria
zotero_key: [chave Zotero]
autor: Sobrenome, Nome
ano:
titulo:
argumento_central: [1 frase]
relevancia: [alta/media/baixa]
debate: [nome do debate no seu mapa]
---

## Argumento central

[1 parágrafo — nas suas palavras, não citação]

## O que este texto tem que outros não têm

## Pontos de concordância com a sua tese

## Pontos de tensão ou discordância

## Citações úteis

> "citação 1" (p. X)

> "citação 2" (p. Y)

## O que falta neste texto (lacunas)

## Citação ABNT completa
```

### Não fazer

- Não copie o resumo do autor como sua nota — escreva com as suas palavras
- Não cite sem indicar página
- Não marque como "lido" sem a nota de leitura preenchida

---

## 9. Receita 8 — Escrever uma análise iconográfica

**Quando usar:** transformar as notas de análise (Receitas 2–4) em texto acadêmico.

### Estrutura básica de um parágrafo de análise

```
[Ancoragem descritiva] → [Identificação iconográfica] → [Contextualização] → [Interpretação] → [Ligação ao argumento]
```

**Exemplo:**
> A figura feminina que ocupa o anverso da moeda de 500 réis emitida em 1889 [ancoragem] apresenta os atributos convencionais da *Iustitia* ocidental: balança e espada [identificação]. Sua produção coincide com a proclamação da República, quando o novo regime buscava uma iconografia de ruptura com a monarquia sem abandonar o repertório jurídico europeu [contextualização]. A ausência da venda — atributo que só se consolidaria nas representações brasileiras da Justiça na década de 1920 — sugere que a imparcialidade ainda não era o valor central a ser comunicado ao público em circulação [interpretação]. Essa escolha participa do padrão que denominamos endurecimento seletivo: a figura feminina é mobilizada como veículo de soberania estatal sem que seu corpo alegórico implique neutralidade ou abstração [ligação ao argumento].

### O que evitar

| Erro | Correto |
|------|---------|
| "A imagem mostra a Justiça" (sem descrever) | Descrever antes de nomear |
| "É evidente que..." | Fundamentar com fonte |
| Nível 3 sem passar pelo 1 e 2 | Respeitar a sequência Panofsky |
| Análise sem comparação | Sempre relacionar com outros itens do corpus |
| Interpretação sem fonte primária | Toda afirmação sobre intenção exige documento |

---

## 10. Receita 9 — Citar corretamente (ABNT e Chicago)

### ABNT NBR 6023:2025 — Formas mais usadas

**Livro:**
```
SOBRENOME, Nome. Título em itálico: subtítulo. Edição. Local: Editora, Ano.
```

**Artigo em periódico:**
```
SOBRENOME, Nome. Título do artigo. Nome do Periódico, Local, v. X, n. Y, p. Z–W, mês ano. DOI ou URL.
```

**Citação no texto (sistema autor-data):**
```
(CARVALHO, 1996, p. 45)
(CARVALHO, 1996, p. 45-47)
```

**Citação direta longa (mais de 3 linhas):**
```latex
\begin{citacao}
Texto da citação com recuo de 4 cm, fonte menor, sem aspas.
\end{citacao}
```

### Chicago 17th — Para textos em inglês

**Nota de rodapé (N):**
```
N: Nome Sobrenome, Título em Itálico (Local: Editora, Ano), páginas.
```

**Referência bibliográfica (B):**
```
B: Sobrenome, Nome. Título em Itálico. Local: Editora, Ano.
```

**Citação no texto (author-date):**
```
(Sobrenome Ano, página)
```

### Verificação antes de submeter

```bash
# Rodar auditor de citações ABNT
conda activate iconocracy
cd ~/Research/iconocracy-corpus
python tools/scripts/abnt_citations.py --file vault/tese/capitulos/cap-X.md
```

---

## 11. Receita 10 — Sessão de pesquisa: abertura e fechamento

### Abertura (5 minutos)

```bash
# 1. Ativar ambiente
conda activate iconocracy
cd ~/Research/iconocracy-corpus

# 2. Verificar estado do corpus
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record

# 3. Ver o que ficou pendente
git status
cat docs/T3-coding-queue.md | head -20   # fila de codificação
```

Definir **uma** pergunta para a sessão:
```
Hoje vou [descobrir / analisar / codificar / escrever] [X específico].
```

### Fechamento (10 minutos)

```bash
# 1. Sincronizar vault
python tools/scripts/vault_sync.py sync

# 2. Validar
python tools/scripts/validate_schemas.py data/processed/records.jsonl

# 3. Commit das mudanças
git add -p   # revisar cada mudança antes de adicionar
git commit -m "tipo(escopo): descrição em uma linha"

# 4. Registrar no vault o que ficou em aberto
```

**Nota de fechamento de sessão** (vault/sessoes/SCOUT-SESSION-YYYY-MM-DD.md):
```markdown
## O que fiz
## O que ficou em aberto
## Próxima sessão: começar por
```

---

## 12. Referência rápida — Arquivos digitais

| Arquivo | URL | Cobre | Busca avançada |
|---------|-----|-------|----------------|
| Hemeroteca Digital BN | hemeroteca.bn.gov.br | Imprensa BR 1800–1900 | Sim |
| Gallica BnF | gallica.bnf.fr | Fontes FR, coleções globais | Sim (CQL) |
| Europeana | europeana.eu | Acervos europeus agregados | Sim |
| Library of Congress | loc.gov | EUA, coleções globais | Sim |
| Numista | numista.com | Numismática mundial | Por país/período |
| Colnect | colnect.com | Selos e moedas | Por país/período |
| Archive.org | archive.org | Documentos digitalizados globais | Texto completo |
| Brasiliana USP | brasiliana.usp.br | Iconografia BR | Por tema |
| FGV CPDOC | cpdoc.fgv.br | Documentos BR séc. XX | Busca simples |

### Operadores comuns (Gallica/Europeana)

```
dc.title all "alegoria"
dc.date >= "1880" and dc.date <= "1920"
dc.subject all "justice" and dc.type all "image"
```

---

## 13. Referência rápida — Iconclass

**Iconclass** é o sistema de classificação iconográfica padrão internacional.

- Consulta online: iconclass.org
- Notação: código numérico hierárquico + letras de qualificação

### Códigos-chave para o projeto

| Código | Significado |
|--------|-------------|
| `11M` | Personificações e alegorias |
| `11M21` | Alegorias de virtudes |
| `11M31` | Justiça (Iustitia) |
| `11M31(+5)` | Justiça com atributos |
| `48C` | Governo, política, administração |
| `48C51` | Iconografia feminista |
| `48C7341` | Justiça com balança e espada |
| `25F` | Moedas, selos, medalhas |
| `41A` | Vestuário alegórico |

### Busca no Iconclass

```
# Busca por palavra-chave
iconclass.org/search?q=justice+allegory

# Busca por código (ver subclasses)
iconclass.org/11M31
```

---

## 14. Referência rápida — Terminologia Panofsky

| Termo | Definição |
|-------|-----------|
| **Motivo artístico** | Forma visual pura (linha, cor, volume) — nível 1 |
| **Imagem** | Motivo reconhecível como representação de algo — nível 2 |
| **Alegorias** | Figuras convencionais portadoras de conceitos abstratos — nível 2 |
| **Símbolo** | Valor intrínseco que a obra manifesta inconscientemente — nível 3 |
| **Iconografia** | Identificação e descrição de imagens e alegorias — disciplina |
| **Iconologia** | Interpretação do significado intrínseco — disciplina |
| **Pathosformel** | (Warburg) Fórmula expressiva de emoção, transmitida entre culturas |
| **Nachleben** | (Warburg) Sobrevivência de imagens e fórmulas em contextos novos |
| **Zwischenraum** | (Warburg) Espaço entre imagens num atlas; tensão produtiva |
| **Endurecimento** | (Vanzin) Processo de rigidificação iconográfica da figura feminina de Estado |
| **Contrato Sexual Visual** | (Vanzin) Pacto implícito de gênero inscrito na iconografia jurídica |
| **Feminilidade de Estado** | (Vanzin) Forma específica de representação da mulher como veículo de poder estatal |

---

*Última atualização: 2026-05-14 · Para sugerir receitas: abrir issue com label `docs`*
