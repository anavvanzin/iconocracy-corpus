# CODEBOOK DE PROMPTS — ICONOCRACIA

**Projeto:** Iconocracia · Alegoria Feminina na Historia da Cultura Juridica (Seculos XIX-XX)
**Versao:** 1.1 · Marco 2026
**Uso:** Referencia rapida para interacao com Claude em qualquer etapa do projeto.
**Convencao:** `[VARIAVEL]` = substituir pelo valor concreto. `{campo}` = campo de dado.

---

## INDICE

1. [CORPUS — Ingestao e Catalogacao](#1-corpus--ingestao-e-catalogacao)
2. [CORPUS SCOUT — Busca em Acervos e Notas Atomicas](#2-corpus-scout--busca-em-acervos-e-notas-atomicas)
3. [CORPUS — Codificacao IconoCode](#3-corpus--codificacao-iconocode)
4. [CORPUS — Protocolo de 10 Indicadores](#4-corpus--protocolo-de-10-indicadores)
5. [CORPUS — Validacao e Qualidade](#5-corpus--validacao-e-qualidade)
6. [INFRAESTRUTURA — GitHub](#6-infraestrutura--github)
7. [INFRAESTRUTURA — Google Drive](#7-infraestrutura--google-drive)
8. [INFRAESTRUTURA — Notion](#8-infraestrutura--notion)
9. [INFRAESTRUTURA — Sincronizacao Tripartite](#9-infraestrutura--sincronizacao-tripartite)
10. [ANALISE QUANTITATIVA — Iconometria](#10-analise-quantitativa--iconometria)
11. [ANALISE QUANTITATIVA — Pipeline de Notebooks](#11-analise-quantitativa--pipeline-de-notebooks)
12. [ANALISE QUALITATIVA — Iconologia](#12-analise-qualitativa--iconologia)
13. [ATLAS ICONOCRATICO](#13-atlas-iconocratico)
14. [TEORIA — Conceitos Operativos](#14-teoria--conceitos-operativos)
15. [TEORIA — Anti-ENDURECIMENTO e Colapso de Regime](#15-teoria--anti-endurecimento-e-colapso-de-regime)
16. [ESCRITA — Capitulos e Prosa Academica](#16-escrita--capitulos-e-prosa-academica)
17. [ESCRITA — Artigos e Entregas Parciais](#17-escrita--artigos-e-entregas-parciais)
18. [ESCRITA — Compilacao da Tese](#18-escrita--compilacao-da-tese)
19. [BIBLIOGRAFICO — Referencias e ABNT](#19-bibliografico--referencias-e-abnt)
20. [GALLICA / APIs de Acervos](#20-gallica--apis-de-acervos)
21. [ICONCLASS](#21-iconclass)
22. [DECISOES METODOLOGICAS](#22-decisoes-metodologicas)
23. [APRESENTACOES E COMUNICACAO](#23-apresentacoes-e-comunicacao)
24. [WEBICONOCRACY — Aplicacao Web](#24-webiconocracy--aplicacao-web)
25. [OBSIDIAN — Gestao do Vault](#25-obsidian--gestao-do-vault)
26. [MANUTENCAO E AUDITORIA](#26-manutencao-e-auditoria)

---

## 1. CORPUS — Ingestao e Catalogacao

### P1.01 · Registrar novo item no corpus
```
Preciso registrar um novo item no corpus iconografico.
Dados:
- Titulo: [TITULO]
- Pais: [FR | UK | DE | US | BE | BR]
- Periodo: [ANO ou INTERVALO]
- Suporte: [moeda | selo | monumento | arquitetura forense | estampa | frontispicio | outro]
- Acervo de origem: [NOME DO ACERVO]
- URL de alta resolucao: [URL]
- Licenca: [dominio publico | CC-BY | outro]

Gere:
1. O registro em formato JSONL compativel com data/processed/records.jsonl
2. A ficha descritiva para o Notion DB1
3. O caminho sugerido em data/raw/ no GitHub
```

### P1.02 · Catalogar lote de imagens de um acervo
```
Tenho [N] imagens baixadas de [NOME DO ACERVO] na pasta data/raw/[PAIS]/[SUPORTE]/.
Os arquivos seguem o padrao de nomeacao: [PADRAO, ex: FR_SEL_1870_001.jpg].

Gere:
1. Um manifest CSV com colunas: filename, country, support_type, year_approx, source_archive, iiif_url, license, iconocode_status
2. O script Python para popular records.jsonl a partir desse CSV
3. A query para criar os registros correspondentes no Notion DB1
```

### P1.03 · Verificar duplicatas no corpus
```
Preciso verificar se ha duplicatas no corpus.
Criterios de duplicata: mesmo acervo + mesmo identificador de objeto, OU mesma URL IIIF.

Gere:
1. Script Python que le records.jsonl e identifica duplicatas por cada criterio
2. Relatorio com os pares duplicados encontrados
3. Instrucoes para remocao manual no Notion
```

### P1.04 · Importar metadados de um catalogo museografico
```
Tenho um catalogo/planilha de [ACERVO] com [N] registros em formato [CSV | XLSX | JSON].
Colunas disponiveis: [LISTAR COLUNAS].

Mapeie essas colunas para o schema do corpus:
- Quais campos mapeiam diretamente?
- Quais precisam de transformacao?
- Quais campos do schema ficam vazios (e como preencher)?

Gere o script de ETL que converte esse catalogo para records.jsonl.
```

### P1.05 · Classificar item por regime iconocratico
```
Este item pertence a qual regime iconocratico?

Dados do item:
- Pais: [PAIS]
- Ano: [ANO]
- Suporte: [SUPORTE]
- Contexto politico: [DESCRICAO BREVE]

Regimes possiveis: Fundacional, Normativo, Militar.
Justifique a classificacao com base nos criterios da tese.
```

### P1.06 · Gerar ficha catalografica completa
```
Gere uma ficha catalografica completa para:
- Objeto: [DESCRICAO]
- Acervo: [ACERVO]
- URL: [URL]

A ficha deve conter:
1. Dados de identificacao (titulo, autor/atribuicao, data, tecnica, dimensoes)
2. Dados de localizacao (acervo, numero de inventario, sala/colecao)
3. Dados de proveniencia digital (URL, IIIF manifest, licenca)
4. Classificacao IconoCode preliminar (nivel pre-iconografico)
5. Classificacao ICONCLASS candidata
6. Regime iconocratico atribuido
7. Citacao ABNT da fonte
```

---

## 2. CORPUS SCOUT — Busca em Acervos e Notas Atomicas

> Skill ativa: `/corpus-scout` em Claude Code. Dispara automaticamente ao mencionar alegorias, acervos, regimes, ENDURECIMENTO, ou figuras da tese (Marianne, Britannia, Germania, Columbia, La Belgique, A Republica).

### P2.01 · Buscar candidatos em acervos digitais
```
Busca [N] alegorias femininas de [PAIS] em [SUPORTE] entre [PERIODO]
no [ACERVO: BNDigital | Gallica | Europeana | LoC | British Museum | Numista | Colnect].

Para cada item encontrado, descreve:
- Postura do corpo (dinamica ou hieratica)
- Atributos visiveis (balanca, espada, fasces, barrete frigio, etc.)
- Presenca/ausencia de fasces ou barrete frigio

Classifica o regime (FUNDACIONAL | NORMATIVO | MILITAR).
Detecta grau de ENDURECIMENTO.
Retorna como notas Obsidian.
```

### P2.02 · Gerar Zwischenraum entre dois itens
```
Gera o Zwischenraum entre:
- [ITEM A: nome, pais, ano, suporte, regime]
- [ITEM B: nome, pais, ano, suporte, regime]

Painel comparativo sobre [TEMA: ENDURECIMENTO colonial | desmilitarizacao |
transicao de regime | captura transnacional | etc.].

Estrutura obrigatoria:
1. Dados Comparados (tabela com especificacoes materiais se mesmo suporte)
2. A Mutacao do ENDURECIMENTO (mapear indicadores de purificacao por polo)
3. O Contrato Sexual Visual
4. Sintese para a Tese
```

### P2.03 · Seguir proximos passos de sessao anterior
```
[Colar o bloco "proximos_passos" ou "Proximas buscas sugeridas" da sessao anterior]
```

### P2.04 · Zwischenraum tripolar
```
Gera Zwischenraum tripolar entre:
- Polo A: [ITEM, regime]
- Polo B: [ITEM, regime]
- Polo C: [ITEM, regime]

Mapeia o ciclo de vida de [ALEGORIA] entre tres estados morfologicos.
Inclui tabela comparada com tres colunas.
```

### P2.05 · Buscar variantes colonial vs. metropolitana
```
Busca a versao colonial e a versao metropolitana de [ALEGORIA]:
- Metropolitana: [ex.: Britannia no penny domestico]
- Colonial: [ex.: Britannia no British Trade Dollar]

Compara morfologia, atributos, e grau de ENDURECIMENTO.
O que muda quando a mesma alegoria cruza o oceano?
```

### P2.06 · Buscar medalhas e propaganda satirica
```
Busca medalhas satiricas ou dinheiro de emergencia (Notgeld) com
alegorias femininas no periodo [PERIODO] no contexto de [EVENTO:
ocupacao do Ruhr | hiperinflacao | Guerra dos Boeres | etc.].

Atencao especial a:
- Caricaturas de alegorias inimigas (Marianne vista pela Alemanha, etc.)
- Reversao satirica de atributos classicos
- Anti-ENDURECIMENTO (corpo re-erotizado ou grotesquizado)
```

### P2.07 · Buscar em JSON (alternativa a notas Obsidian)
```
[Mesma query de busca]
Retorna em JSON.
```

### P2.08 · Salvar notas e fazer deploy
```
Salva todas as notas desta sessao no vault Obsidian
em vault/corpus/scout-session-[DATA]/.

Depois, compila e faz deploy ao Cloudflare (/scout).
```

---

## 3. CORPUS — Codificacao IconoCode

### P3.01 · Codificar imagem nos tres niveis de Panofsky
```
Codifique esta imagem segundo o protocolo IconoCode (tres niveis de Panofsky adaptados para iconologia juridica):

Imagem: [DESCRICAO ou URL]
Pais/Ano: [PAIS] / [ANO]
Suporte: [SUPORTE]

Nivel 1 — Pre-iconografico: liste todos os motivos observados
Nivel 2 — Iconografico: identifique o tema e os codigos ICONCLASS correspondentes
Nivel 3 — Iconologico: interprete o significado no contexto juridico-politico

Formate a saida como JSON compativel com iconocode-output.schema.json.
```

### P3.02 · Atribuir codigos ICONCLASS
```
Para a seguinte imagem/descricao, sugira os codigos ICONCLASS mais adequados:
[DESCRICAO DA IMAGEM]

Considere especialmente:
- 48C514 (Justice, allegory)
- 31AA231 (woman standing)
- 44B62 (coat of arms)
- 44A3 (government, civil administration)

Para cada codigo sugerido, indique: Notacao, Label, Papel, Confianca (0-1).
```

### P3.03 · Gerar registro mestre (master record)
```
Monte o registro mestre completo para o item:
- ID do lote: [BATCH_ID]
- Arquivo de imagem: [FILENAME]
- Metadados catalograficos: [DADOS]

Formate como JSON compativel com master-record.schema.json.
```

### P3.04 · Revisar codificacao existente
```
Revise a codificacao IconoCode do item [ID].
Registro atual: [COLAR JSON]

Verifique completude, correcao dos codigos ICONCLASS, suporte evidencial,
gaps no claim_ledger, e coerencia do nivel de confianca.
Proponha correcoes justificadas.
```

### P3.05 · Comparar codificacoes inter-codificadores
```
Tenho duas codificacoes independentes do mesmo item:
Codificador A: [COLAR JSON ou RESUMO]
Codificador B: [COLAR JSON ou RESUMO]

Calcule concordancia simples, Kappa de Cohen, pontos de discordancia,
e recomendacao (qual adotar ou terceiro codificador).
```

---

## 4. CORPUS — Protocolo de 10 Indicadores

### P4.01 · Aplicar protocolo de 10 indicadores a uma imagem
```
Aplique o protocolo de 10 indicadores ordinais de purificacao classica:
[DESCRICAO DETALHADA DA IMAGEM ou URL]

Indicadores: desincorporacao, rigidez_postural, dessexualizacao,
uniformizacao_facial, heraldizacao, enquadramento_arquitetonico,
apagamento_narrativo, monocromatizacao, serialidade, inscricao_estatal.

Escala: 0 (ausente) a 3 (forte/dominante). Justifique cada valor.
```

### P4.02 · Calibrar indicador especifico
```
Preciso calibrar o indicador [NUMERO] — [NOME].
Problema: [DESCREVER AMBIGUIDADE]
Mostre: definicao atual, tres exemplos de pontuacao clara, proposta de ajuste.
```

### P4.03 · Gerar tabela de valores para um subconjunto
```
Gere tabela com os 10 indicadores para todos os itens do corpus que satisfacam:
- Pais: [PAIS], Periodo: [INTERVALO], Regime: [REGIME]
Formato: CSV. Fonte: records.jsonl.
```

### P4.04 · Proposta para Field 11 (acoplamento imagem-norma)
```
O Field 11 mede o "acoplamento imagem-norma" — grau em que a imagem esta
inscrita em suporte com eficacia juridica direta.

Preciso: definicao operacional, escala ordinal, criterios de codificacao,
interacao com a Matriz 3x2, impacto na Regressao do Cap. 6.
```

---

## 5. CORPUS — Validacao e Qualidade

### P5.01 · Auditoria de completude do corpus
```
Faca auditoria de completude do corpus a partir de records.jsonl:
campos obrigatorios, codificacao IconoCode, 10 indicadores, regime,
ICONCLASS, citacao ABNT. Gere relatorio com % de completude por campo.
```

### P5.02 · Verificar estratificacao da amostra
```
Verifique se a amostra esta estratificada: 6 paises x 4 suportes x 3 regimes x 1800-2000.
Gere tabela cruzada, identifique celulas vazias, recomende itens a buscar.
```

### P5.03 · Relatorio de rastreabilidade
```
Gere relatorio de rastreabilidade para [N] itens aleatorios.
Verifique cadeia: arquivo em data/raw/ → Google Drive → Notion DB1 → records.jsonl.
Sinalize qualquer quebra.
```

### P5.04 · Detectar inconsistencias Notion vs. GitHub
```
Compare registros do Notion DB1 com records.jsonl.
Busque: itens sem correspondente, campos divergentes, IDs duplicados.
Gere diff e proponha acao corretiva.
```

---

## 6. INFRAESTRUTURA — GitHub

### P6.01 · Estrutura de diretorios do monorepo
```
Mostre a estrutura de diretorios esperada do monorepo iconocracy-corpus
e verifique consistencia. Para cada diretorio: o que contem, quem atualiza, quando.
```

### P6.02 · Gerar script Python para tarefa especifica
```
Preciso de um script Python para: [DESCREVER TAREFA].
Salvar em tools/scripts/[NOME].py. Dependencias: pandas, requests, json, pathlib.
```

### P6.03 · Atualizar README do repositorio
```
Atualize o README.md para refletir o estado atual:
estrutura, status dos componentes, DMs em aberto, instrucoes de setup, licenca.
```

### P6.04 · Resolver DM-001 (API key exposta)
```
DM-001 (CRITICA): API key exposta no historico.
Verificar acessibilidade, gerar roteiro de remediacao (BFG),
listar commits afetados, confirmar .gitignore.
```

### P6.05 · Desenvolver notion_sync.py
```
Desenvolva tools/scripts/notion_sync.py: le records.jsonl, sincroniza com
Notion DB1, operacoes create/update/detect_conflicts, modo dry-run obrigatorio.
```

### P6.06 · Completar o gallica-mcp-server
```
Complete o gallica-mcp-server (TypeScript/MCP SDK):
inputSchemas, searchTools (SRU), itemTools (IIIF), index.ts, build, README.
```

---

## 7. INFRAESTRUTURA — Google Drive

### P7.01 · Mapear estrutura de pastas no Drive
```
Mapeie a estrutura de pastas esperada no Drive: dumps brutos por pais,
exports Notion, backups repo, capitulos da tese, imagens de alta resolucao.
Mapeie para GitHub e Notion.
```

### P7.02 · Buscar documento especifico no Drive
```
Busque no meu Google Drive: [DESCRICAO].
Mostre titulo exato, ultima modificacao, link, relacao com GitHub/Notion.
```

### P7.03 · Exportar dados do Drive para o pipeline
```
Tenho [TIPO] no Drive em [PASTA/NOME]. Defina: onde copiar no monorepo,
transformacao, registro no Notion, script necessario.
```

---

## 8. INFRAESTRUTURA — Notion

### P8.01 · Consultar Notion HQ
```
Consulte o Notion HQ (root: 322158101a0581568e58cfc997b7b727).
Preciso saber: [PERGUNTA].

DBs de referencia:
- DB1 Corpus: 68ba778cec304d11bc9ce369612a7e67
- DB9 Glossario: b38ae8baf2b7434e90d8e8078b9cfb78
- Decisoes Metodologicas: bf67ab4257c64adfb8773f370c8c74db
```

### P8.02 · Criar registro no DB1
```
Crie registro no DB1 com: [CAMPOS E VALORES].
Verifique: sem duplicata, valores controlados validos, correspondente em records.jsonl.
```

### P8.03 · Atualizar glossario (DB9)
```
Atualize o conceito [NOME] no DB9:
definicao operativa, fonte teorica, capitulo, status (original | mobilizado | adaptado).
```

### P8.04 · Registrar decisao metodologica
```
Registre DM-[NUMERO] no Notion:
titulo, prioridade, descricao, alternativas, decisao, justificativa, impacto, status.
```

### P8.05 · Gerar painel de status
```
Gere snapshot: corpus (total, % codificados), capitulos (status),
DMs (abertas/criticas), infraestrutura (componentes), duplicatas.
```

---

## 9. INFRAESTRUTURA — Sincronizacao Tripartite

### P9.01 · Diagrama de fluxo de dados
```
Desenhe o fluxo GitHub ↔ Drive ↔ Notion: o que flui, quem dispara, frequencia.
```

### P9.02 · Checklist de coerencia tripartite
```
Gere checklist: todo item Notion tem arquivo GitHub? Todo JSONL tem Notion?
Dumps Drive atualizados? Schema Notion = schema GitHub? DMs implementadas?
```

### P9.03 · Propor workflow de atualizacao
```
Quando adiciono [N] novos itens, qual o workflow completo?
Passo a passo: onde salvar, que script rodar, como sincronizar, que verificar.
```

---

## 10. ANALISE QUANTITATIVA — Iconometria

### P10.01 · Estatisticas descritivas do corpus
```
Gere estatisticas descritivas de records.jsonl:
distribuicao por pais, periodo, suporte, regime; cruzamentos;
medianas e IQR dos 10 indicadores; heatmap temporal.
```

### P10.02 · Teste de Kruskal-Wallis
```
Execute Kruskal-Wallis para cada indicador entre os tres regimes.
Para cada: H-statistic, p-value, eta-squared, post hoc Dunn se significativo.
Gere script Python e notebook Jupyter.
```

### P10.03 · Regressao Logistica Ordinal
```
Monte a Regressao Logistica Ordinal (Cap. 6.3):
VD: grau de ENDURECIMENTO. VIs: pais, periodo, regime, suporte.
Interacao: regime x tipo_suporte (Matriz 3x2).
Gere script, odds ratios com IC 95%, verificacao de pressupostos.
```

### P10.04 · Analise de Correspondencia Multipla
```
Execute MCA para as "familias alegoricas transatlanticas" (Cap. 6.4):
variaveis ativas (pais, periodo, regime, indicadores categorizados),
suplementares (suporte, acervo). Gere biplot, dendrograma, casos paradigmaticos.
```

### P10.05 · Validar hipotese da Matriz 3x2
```
Teste se o termo de interacao regime x tipo_suporte e significativo.
Confirmam as predicoes teoricas? Ha excecoes para estudo de caso?
```

### P10.06 · Gerar visualizacoes para o Capitulo 6
```
Gere: heatmap temporal, Sankey (pais→regime→suporte), boxplots por regime,
forest plot (odds ratios), biplot MCA. PNG 300dpi + SVG. Paleta sepia/bordeaux/navy.
```

---

## 11. ANALISE QUANTITATIVA — Pipeline de Notebooks

### P11.01 · Executar pipeline completo
```
Execute o pipeline sequencialmente:
1. 01_exploratory — descritivas e visualizacoes
2. 02_kruskal_wallis — teste de diferenca entre regimes
3. 03_regression — regressao logistica ordinal
4. 04_correspondence — analise de correspondencia multipla

Ambiente: conda activate iconocracy
Diretorio: iconocracy-corpus/notebooks/
Verifique que records.jsonl esta atualizado e outputs sao consistentes.
```

### P11.02 · Atualizar notebooks apos novos itens
```
Adicionei [N] novos itens ao corpus. Atualize:
1. records.jsonl (via code_purification.py --export-csv)
2. Re-execute 01_exploratory
3. Verifique se conclusoes de 02_kruskal_wallis mudam
4. Re-execute 03_regression com amostra expandida
5. Atualize 04_correspondence
Sinalize se alguma conclusao estatistica mudou significativamente.
```

---

## 12. ANALISE QUALITATIVA — Iconologia

### P12.01 · Estudo de caso: leitura iconologica
```
Realize leitura iconologica em profundidade (Cap. 7) de [IMAGEM/OBJETO].

Estrutura (Panofsky adaptado):
1. Pre-iconografico: descricao exaustiva
2. Iconografico: temas, tipos, fontes visuais
3. Iconologico juridico: contrato sexual visual, regime, economia da feminilidade de Estado

Articule com: Pateman, Goodrich, Mondzain, Warburg.
```

### P12.02 · Caso paradigmatico vs. desviante
```
Este item foi identificado como [paradigmatico | desviante] pela analise quantitativa.
Item: [DADOS]. Razao: [OUTLIER / CLUSTER INESPERADO].
Desenvolva analise qualitativa que explica por que confirma/desafia a hipotese.
```

### P12.03 · Analise comparada: Marianne vs. Britannia
```
Desenvolva analise comparada (Cap. 7): genealogia iconografica, diferencas
morfologicas nos 10 indicadores, regime correspondente, relacao com contrato
sexual, ENDURECIMENTO em conflito, caso Thatcher como contra-alegoria.
```

### P12.04 · Analise de arquitetura forense
```
Analise o programa iconografico de [EDIFICIO JURIDICO]:
inventario de figuras alegoricas, posicao no programa decorativo
(fachada, vestibulo, sala de audiencias, vitrais, murais),
relacao com funcao juridica, acoplamento imagem-norma, regime.
```

---

## 13. ATLAS ICONOCRATICO

### P13.01 · Propor composicao de painel
```
Proponha composicao do Painel [NUMERO] — [NOME].
Considere: quais imagens, qual Zwischenraum, como dispor (montagem warburguiana),
que Pathosformel conecta imagens de paises diferentes, que legenda acompanha.
```

### P13.02 · Justificar justaposicao no Atlas
```
No Painel [NUMERO], justapor Imagem A: [DESCRICAO] e Imagem B: [DESCRICAO].
Escreva justificativa: Zwischenraum, Pathosformel, contrato sexual visual.
Tom ensaistico-filosofico (Didi-Huberman / Goodrich).
```

### P13.03 · Gerar fichas tecnicas para o Atlas
```
Gere fichas tecnicas (Apendice F) para todas as imagens do Painel [NUMERO]:
numero no Atlas, titulo, autor, data, tecnica, dimensoes, acervo,
inventario, URL, ICONCLASS, regime, licenca.
```

---

## 14. TEORIA — Conceitos Operativos

### P14.01 · Definir conceito operativo
```
Defina operativamente [CONCEITO] para o Glossario:
definicao sintetica, genealogia teorica, como a tese mobiliza/originaliza,
relacao com outros conceitos, capitulo(s) onde opera.
Status: [original da tese | mobilizado | adaptado].

Conceitos nucleares: Iconocracia, Visiocracia, Contrato Sexual Visual,
Feminilidade de Estado, Zwischenraum, Purificacao Classica, ENDURECIMENTO,
Pathosformel, Regime Iconocratico, Acoplamento imagem-norma.
```

### P14.02 · Verificar atribuicao de conceito
```
Verifique a atribuicao de [CONCEITO]:
A quem atribuido? Correto? Risco de confusao com homonimos? Citacao precisa?

Atencao: "Pintura de alma" = construcao original (Legendre+Goodrich+Mondzain).
Feminilidade de Estado = original da tese. ENDURECIMENTO = sempre em portugues.
"desver" = Manoel de Barros (O livro das ignorancas, 1993).
```

### P14.03 · Articular triade teorica
```
Articule Pateman-Mondzain-Goodrich em relacao a [TEMA].
Mostre: contribuicao de cada, como a tese os conecta (Contrato Sexual Visual),
onde Warburg entra (Nachleben/Pathosformel), que lacuna essa articulacao preenche.
```

### P14.04 · Diferenciar conceitos proximos
```
Diferencie: [CONCEITO A] vs. [CONCEITO B].
Definicao de cada, o que os distingue, como se relacionam na argumentacao.

Pares frequentes: Iconocracia vs. Visiocracia, Contrato social vs. sexual,
Purificacao Classica vs. ENDURECIMENTO, Pathosformel vs. Nachleben.
```

---

## 15. TEORIA — Anti-ENDURECIMENTO e Colapso de Regime

### P15.01 · Analisar anti-ENDURECIMENTO
```
Analise o fenomeno de anti-ENDURECIMENTO no contexto de [EVENTO/PERIODO].

Tres destinos possiveis do corpo alegorico pos-colapso:
1. Persistencia fantasma — forma rigida, substancia vazia
   (ex.: vinhetas imperiais em cedulas de trilhoes de Marcos)
2. Reversao satirica — corpo re-erotizado/caricaturado
   (ex.: Stoffgeld de Bielefeld)
3. Weaponizacao — alegoria capturada pelo inimigo
   (ex.: Marianne de Goetz estrangulando alemao)

Articule com: hipotese do ENDURECIMENTO, indicadores de purificacao,
dependencia institucional do contrato sexual visual.
```

### P15.02 · Captura transnacional da alegoria
```
Analise a captura de [ALEGORIA] por [AGENTE INIMIGO].

Estrutura:
1. Alegoria no contexto original (quem emite, que funcao)
2. Alegoria capturada (quem reformata, como muda)
3. ENDURECIMENTO muda de agente — implicacoes
4. Contrato sexual visual e reversivel?
5. Fragilidade estrutural da iconocracia
```

### P15.03 · Diferenciar ENDURECIMENTO autoctone vs. hostil
```
Diferencie:
- Autoctone: Estado endurece sua propria alegoria (Piastre, Germania colonial)
- Hostil: inimigo endurece alegoria alheia (Goetz K-299, Notgeld anti-Marianne)

Quais indicadores se ativam em cada caso? Qual mais radical e por que?
```

### P15.04 · Regime em colapso: destino da alegoria
```
Quando regime colapsa (fim do Kaiserreich 1918, hiperinflacao 1923,
queda de Weimar 1933), o que acontece com o corpo alegorico?

Mapeie para [CASO]: substituicao? Persistencia degradada?
Ressignificacao? Vacuo alegorico?
```

---

## 16. ESCRITA — Capitulos e Prosa Academica

### P16.01 · Redigir secao de capitulo
```
Redija a secao [NUMERO] do Capitulo [NUMERO]: "[TITULO]".

Contexto: secao anterior tratou de [RESUMO]. Esta secao precisa [OBJETIVO].
Referencias a mobilizar: [AUTORES/OBRAS].

Diretrizes: tom ensaistico-filosofico, sem travessoes (usar virgulas),
sem sentencas sobre negativas, sem dois-pontos excessivos,
sem triparticoes automaticas, ENDURECIMENTO sempre em portugues,
Mondzain = edicao 2002, prosa densa mas legivel.
```

### P16.02 · Revisar secao existente
```
Revise esta secao: [COLAR TEXTO]
Verifique: coerencia argumentativa, ancoragem bibliografica,
consistencia terminologica, estilo, notas de rodape, transicoes.
```

### P16.03 · Converter anotacoes em prosa
```
Converta em prosa academica: [COLAR ANOTACOES]
Destino: Cap. [N], Secao [N]. Funcao: [O QUE DEMONSTRAR].
Mantenha citacoes com pagina, reformule em prosa continua.
```

### P16.04 · Escrever transicao entre capitulos
```
Transicao do Cap. [N] (encerra com [RESUMO]) para Cap. [N+1] (abre com [RESUMO]).
Recapitular sem repetir, criar expectativa, mostrar necessidade logica. Max 2 paragrafos.
```

### P16.05 · Redigir introducao de capitulo
```
Abertura do Cap. [NUMERO]: "[TITULO]".
Comecar com imagem-caso concreta, derivar problema teorico,
situar no argumento geral, anunciar estrutura. 3-5 paragrafos.
```

### P16.06 · Redigir conclusao parcial
```
Conclusao parcial do Cap. [NUMERO]. Demonstrou: [PONTOS].
Permite avancar para: [PROXIMO]. Contribuicao especifica: [CONTRIBUICAO].
Sintetica (2-3 paragrafos), projetar para frente.
```

---

## 17. ESCRITA — Artigos e Entregas Parciais

### P17.01 · Redigir artigo derivado da tese
```
Artigo do Cap. [NUMERO]. Titulo: [TITULO]. Periodico: [NOME/QUALIS].
Limite: [N] palavras. Lingua: [PT|EN|FR]. Autossuficiente mas coerente com a tese.
```

### P17.02 · Redigir entrega de disciplina
```
Produto para disciplina [CODIGO]: encontro [N], tipo [TIPO], data [DATA].
Instrucoes: [DO PROFESSOR]. Articular com a tese. Formato Markdown/Obsidian.
```

### P17.03 · Preparar abstract para evento
```
Abstract para [EVENTO/CONGRESSO]: GT [TEMA], [N] palavras, [LINGUA], foco [ASPECTO].
Conter: problema, referencial, metodo, resultados esperados, palavras-chave.
```

---

## 18. ESCRITA — Compilacao da Tese

### P18.01 · Compilar tese via Pandoc
```
Compile a tese: make -C vault/tese/

Verifique: capitulos presentes e na ordem, frontmatter Pandoc configurado,
citacoes Citeproc resolvem, imagens referenciadas e acessiveis, output PDF formatado.
```

### P18.02 · Gerar sumario atualizado
```
Gere sumario da tese com base em vault/tese/:
capitulo, titulo, secoes, status (rascunho|revisao|pronto),
contagem de palavras, total, estimativa de paginas.
```

### P18.03 · Verificar consistencia entre capitulos
```
Verifique: termos do glossario consistentes, referencias cruzadas validas,
numeracao de figuras/tabelas sequencial, itens mencionados no Apendice,
transicoes entre capitulos fluem.
```

---

## 19. BIBLIOGRAFICO — Referencias e ABNT

### P19.01 · Formatar referencia em ABNT
```
Formate em ABNT NBR 6023:2025: [DADOS DA REFERENCIA].
Tipo: [livro | capitulo | artigo | tese | documento eletronico | imagem | legislacao].
```

### P19.02 · Verificar referencia bibliografica
```
Verifique: [COLAR REFERENCIA]
Checar: nome do autor, titulo exato, edicao/ano (Mondzain = 2002),
paginacao, formato ABNT. Goodrich (2017) "Imago Decidendi" — paginacao pendente.
```

### P19.03 · Gerar lista de referencias de um capitulo
```
Gere lista ABNT para o Cap. [NUMERO]. Todas as obras citadas.
Sinalize [VERIFICAR] se incompleta. Ordem alfabetica.
```

### P19.04 · Localizar fonte primaria
```
Localize: [DESCRICAO DA FONTE].
Buscar em: Gallica, LoC, British Museum, Rijksmuseum, Europeana, HathiTrust, Internet Archive.
Para cada resultado: URL, alta resolucao, licenca, citacao ABNT.
```

---

## 20. GALLICA / APIs de Acervos

### P20.01 · Buscar imagens no Gallica
```
Busque no Gallica: tema [DESCRICAO], periodo [INTERVALO],
tipo [estampe|monnaie|photographie|affiche].
Use API SRU. Para cada: titulo, data, URL, URL IIIF, ark.
```

### P20.02 · Acessar imagem via IIIF
```
Acesse via IIIF: ARK [ark:/12148/XXXX], regiao [full|x,y,w,h],
tamanho [full|max|1500,|pct:50], rotacao [0-270], formato [jpg|png].
Monte URL e verifique acessibilidade.
```

### P20.03 · Buscar no Library of Congress
```
Busque no LoC: tema [DESCRICAO], colecao [Prints and Photographs|Chronicling America],
periodo [INTERVALO]. Para cada: titulo, data, URL, formato, licenca, ABNT.
```

### P20.04 · Buscar no Rijksmuseum / British Museum / Europeana
```
Busque no [ACERVO] via API: tema [DESCRICAO], periodo [INTERVALO], tipo [TIPO].
Resultados com: titulo, data, URL, imagem alta resolucao, licenca.
```

---

## 21. ICONCLASS

### P21.01 · Identificar notacao ICONCLASS
```
Notacao ICONCLASS para: [DESCRICAO]. Indique notacao principal,
secundarias (atributos), nivel de especificidade adequado.
```

### P21.02 · Explicar hierarquia ICONCLASS
```
Explique a hierarquia relevante: 44 (State), 44A (Government), 44B (heraldry),
48C514 (Justice allegory), 31AA (female figure).
Relacao com o protocolo IconoCode.
```

### P21.03 · Mapear ICONCLASS para indicadores
```
Mapeie notacoes frequentes no corpus para os 10 indicadores.
Ex.: 48C514 (Justice) tende a pontuar alto em quais?
```

---

## 22. DECISOES METODOLOGICAS

### P22.01 · Analisar DM em aberto
```
Analise DM-[NUMERO]: [TITULO/PROBLEMA].
Alternativas viaveis, pros/contras, impacto na tese e infraestrutura, recomendacao.
```

### P22.02 · Status das DMs abertas
```
Liste DMs abertas: DM-001 (API key, CRITICA), DM-002 (JSON feminista),
DM-003 (PostgreSQL SPEC-1). Status, proximo passo, deadline.
Ha novas DMs a registrar?
```

---

## 23. APRESENTACOES E COMUNICACAO

### P23.01 · Gerar apresentacao
```
Apresentacao sobre [TEMA] para [PUBLICO/EVENTO]:
[N] minutos, [N] slides, [PT|EN|FR], estilo [minimalista|elegante|academico].
Para Canva: frases densas unicas, remover diacriticos dos outlines.
```

### P23.02 · Preparar elevator pitch
```
Pitch (2 min) da tese para [PUBLICO: banca | congresso | colega | orientador].
Problema, hipotese, metodo, originalidade.
```

### P23.03 · Redigir email academico
```
Email para [DESTINATARIO] sobre [ASSUNTO]. Tom [formal|semiformal].
Objetivo: [O QUE QUERO]. Lingua: [PT|EN|FR].
```

---

## 24. WEBICONOCRACY — Aplicacao Web

### P24.01 · Desenvolver nova funcionalidade
```
Adicione [FUNCIONALIDADE] ao webiconocracy
(React 19 + TypeScript + Vite + Tailwind CSS 4 + Firebase).
Projeto: iconocracy-corpus/webiconocracy/
Requisitos: [DESCREVER]
```

### P24.02 · Atualizar dados do corpus na web app
```
Atualize corpus-data.json ([N] itens) no webiconocracy.
O que mudou: [NOVOS ITENS/CAMPOS]. Verificar compatibilidade de schema.
```

### P24.03 · Integrar achados SCOUT no webiconocracy
```
Integre candidatos SCOUT [IDs] e Zwischenraume [IDs] ao webiconocracy.
Adicione ao corpus-data.json e verifique exibicao.
```

### P24.04 · Deploy Cloudflare do companion
```
Compile achados e faca deploy ao worker iconocracia-companion:
npx wrangler deploy (de deploy/iconocracia-companion/).
Endpoints: /scout (HTML viewer), /api/scout (JSON), /api/diary (existente).
```

---

## 25. OBSIDIAN — Gestao do Vault

### P25.01 · Criar nota de pesquisa estruturada
```
Crie nota para o vault sobre [TEMA]:
template vault/_templates/nota-de-pesquisa, tags [LISTAR],
links [NOTAS RELACIONADAS], status [rascunho|revisao|consolidado].
```

### P25.02 · Gerar mapa de links do vault
```
Analise links entre notas: notas orfas, hubs, clusters tematicos, links quebrados.
```

### P25.03 · Consolidar notas SCOUT no vault
```
Consolide vault/corpus/scout-session-*:
atualizar _index.md, linkar Zwischenraume nos capitulos relevantes,
verificar tags canonicas, remover duplicatas entre sessoes.
```

---

## 26. MANUTENCAO E AUDITORIA

### P26.01 · Auditoria geral do projeto
```
Auditoria completa: corpus (completude, qualidade, rastreabilidade),
infraestrutura (coerencia tripartite), capitulos (status),
conceitos (glossario), DMs (registradas), bibliografico (pendencias),
atlas (paineis), timeline (defesa 2026 factivel?).
```

### P26.02 · Backup e versionamento
```
Estado dos backups: ultimo commit GitHub, exports Notion no Drive,
vault Obsidian sincronizado, Zotero atualizado.
```

### P26.03 · Gerar changelog
```
Changelog desde [DATA]: [DATA] · [ACAO] · [PLATAFORMA] · [STATUS].
Fontes: commits, Notion, conversas Claude, entregas.
```

### P26.04 · Preparar handoff para colaborador
```
Documentacao para colaborador que vai [TAREFA]:
visao geral (1 pag), onde encontrar o que, convencoes, workflow, contatos.
```

---

## APENDICE — Prompts Rapidos

```
Qual o status atual do Capitulo [N]?
Quantos itens do corpus estao sem codificacao IconoCode?
Formate esta citacao em ABNT: [DADOS]
Que imagem do corpus melhor ilustra [CONCEITO]?
Gere o frontmatter Obsidian para uma nota sobre [TEMA].
Traduza para [LINGUA], mantendo termos tecnicos em portugues: [TEXTO]
Verifique se [AFIRMACAO] tem suporte bibliografico.
Proponha 3 titulos alternativos para a secao [X.Y].
Qual a diferenca entre [CONCEITO A] e [CONCEITO B] no contexto da tese?
Gere um commit message para: [DESCRICAO]
Liste os itens do corpus do pais [PAIS] no regime [REGIME].
Resuma em 1 paragrafo o argumento do Cap. [N].
Que visualizacao melhor representa [DADO/RELACAO]?
Revise este paragrafo sem mudar o argumento: [PARAGRAFO]
Monte a URL IIIF para o item [ARK] em resolucao [TAMANHO].
Proponha a Pathosformel que conecta [IMAGEM A] e [IMAGEM B].
Esse conceito e original da tese ou mobilizado de outro autor?
Verifique a rastreabilidade do item [ID] entre GitHub, Drive e Notion.
Gere o JSON do registro mestre para o item [ID].
Qual campo do schema esta faltando neste registro? [COLAR JSON]
Busca [ALEGORIA] em [ACERVO] entre [PERIODO].
Gera Zwischenraum entre [ITEM A] e [ITEM B].
Segue os proximos passos: [colar]
Compara a versao metropolitana e colonial de [ALEGORIA].
Que medalhas satiricas de Karl Goetz tocam [TEMA]?
Salva as notas desta sessao no vault Obsidian.
Deploya os achados no Cloudflare.
Compila a tese: make -C vault/tese/
Status do pipeline de notebooks?
Quantos candidatos SCOUT temos sem URL verificada?
Consolida as sessoes SCOUT no _index.md do corpus.
Analisa o anti-ENDURECIMENTO em [CONTEXTO DE COLAPSO].
Quem capturou [ALEGORIA] e como a reformatou?
Roda o 01_exploratory com os dados atualizados.
Atualiza o webiconocracy com os novos candidatos.
```

---

*Codebook v1.1 · 28/03/2026. Secoes 2, 11, 15, 18, 24, 25 adicionadas na sessao de construcao da skill corpus-scout.*
