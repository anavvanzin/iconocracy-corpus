---
plano: "23-junho-2026 — Elicit, artigos disciplinares e governança da tese"
criado: 2026-06-23
status: em_andamento
autor: "Hermes (com Ana)"
fonte_estado:
  - docs/research/elicit/elicit-literature-scout-2026-06-23.md
  - docs/research/elicit/elicit-literature-scout-2026-06-23.raw.json
  - vault/projeto/compression-plan-iconocracy.md
  - docs/decisions/DESENHO-2-0-ICONOCRACIA-2026-06-23.md
  - docs/methodology/codebook-v2-alegorias.md
repositorio: iconocracy-corpus
branch_publicacao: main
---

# Plano do dia — 23 de junho de 2026

Este documento registra o plano operacional do dia para que outros agentes possam continuar o trabalho a partir do mesmo estado. Ele consolida três frentes: busca bibliográfica via Elicit, preparação dos dois artigos disciplinares e governança da compressão da tese ICONOCRACIA.

## 1. Estado salvo hoje

### 1.1 Elicit configurado

- `ELICIT_API_KEY` foi configurada no ambiente Hermes, fora do repositório.
- A chave não foi escrita em arquivos versionados.
- A API do Elicit foi testada com sucesso via `POST /api/v1/search`.
- Observação de segurança: como a chave foi digitada no chat, ela deve ser tratada como temporária e rotacionada depois.

### 1.2 Resultados Elicit salvos

Arquivos versionados no repositório:

- `docs/research/elicit/elicit-literature-scout-2026-06-23.md`
- `docs/research/elicit/elicit-literature-scout-2026-06-23.raw.json`

Resumo do lote:

- 5 buscas Elicit.
- 40 registros retornados.
- Todas as requisições retornaram HTTP 200.
- Quota restante após o lote: 89 buscas.
- Nenhum relatório Elicit foi criado; apenas busca simples foi usada.

### 1.3 Compressão e governança da tese

Arquivo central:

- `vault/projeto/compression-plan-iconocracy.md`

Estado atual:

- A tese está sendo reorganizada como corpus em camadas, não como tese enciclopédica de seis países.
- Núcleo probatório: Brasil, França, Grã-Bretanha.
- Extensão comparativa: Bélgica, Alemanha, Estados Unidos.
- Comparador genealógico: Virtudes, Continentes, Oceanos/Rios.
- Atlas/contraexemplos: fissuras, iconoclasmos, reativações.
- Apêndice técnico: codebook, IRR, scripts, notebooks, schemas e reconciliações.

Regra metodológica ativa:

> Nesta etapa, uma Introdução densa é melhor do que uma Introdução fraca. A compressão é gate posterior, não poda prematura.

## 2. Leituras e decisões extraídas do Elicit

### 2.1 Tese — Brasil como âncora

Priorizar:

- Valéria Salgueiro, “Visual culture in Brazil's First Republic (1889–1930): allegories and elite discourse”.
- Carlos Rogério Lima Junior, “Marianne à brasileira: imagens republicanas e os dilemas do passado imperial”.
- “Entre Marianne e Clotilde”.
- Texto sobre o Paço dos Açorianos e positivismo castilhista.

Uso provável:

- Capítulo Brasil / Primeira República.
- Argumento sobre edifícios públicos, elites republicanas, alegoria feminina e visualidade de Estado.
- Reforço da tese de que o Brasil é âncora analítica, não apenas caso nacional em lista comparativa.

### 2.2 Comparadores — França e Grã-Bretanha

Priorizar:

- D. Outram, “Marianne into battle”.
- Antoine de Baecque, “The Allegorical Image of France, 1750–1800”.
- Frank Ejby Poulsen sobre Le Barbier, direitos, soberania e legalidade.
- Martin A. Kayman sobre Magna Carta e imagens fundacionais do direito britânico.
- “Britannia and Melita: Pseudomorphic Sisters”.

Uso provável:

- França e Grã-Bretanha devem funcionar como comparadores controlados.
- Não expandir o núcleo da tese para outros países apenas porque há bibliografia interessante.
- Espanha, Malta e iconografia socialista podem entrar apenas como genealogia ou nota de difusão, se servirem ao argumento central.

### 2.3 Artigo de História do Direito Penal

Resultado importante:

- O lote Elicit não encontrou diretamente Maria Gonçalves Cajada.
- Isso indica que o caso deve ser buscado fora do Elicit: ANTT, BN, Google Scholar, SciELO, CAPES, notas locais e acervos específicos.

Priorizar para enquadramento:

- Danielle Regina Wobeto de Araujo, “Feitiçaria na vila de Curitiba: direito e misoginia”.
- Narayan Pereira Porto, “Feitiçaria paulista: transcrição de processo-crime da Justiça Eclesiástica na América portuguesa do século XVIII”.
- Nilo Batista, “Andanças da Inquisição no Brasil”.
- Estudos sobre Luzia Soares, Maria Barbosa, Íria Álvares, povos indígenas e mulheres afro-atlânticas diante da Inquisição.

Tese provisória do artigo:

O artigo deve evitar depender de uma transposição genérica do Malleus. O caminho mais forte é estudar a feitiçaria como problema de procedimento, prova, segredo testemunhal, confissão, gênero, raça e circulação colonial da mentalidade inquisitorial.

### 2.4 Artigo de Direito Administrativo

Priorizar:

- “Explicabilidade e contraditório algorítmico nas decisões automatizadas no setor público”.
- “Big data, algoritmos e inteligência artificial na administração pública”.
- “Decisões algorítmicas na Administração Pública: entre a opacidade técnica e o dever de transparência”.
- Textos sobre LGPD, revisão de decisões automatizadas, LAI e processo administrativo digital.

Tese provisória do artigo:

A Administração Pública algorítmica deve ser analisada a partir da tradução de garantias administrativas clássicas em requisitos operacionais: motivação, publicidade, contraditório, explicabilidade, rastreabilidade, revisão humana significativa e controle institucional.

## 3. Plano operacional imediato

### Fase A — Fechar a bibliografia mínima verificável

- [ ] Verificar no Zotero / DOI / páginas editoriais os itens KEEP do relatório Elicit.
- [ ] Separar bibliografia por três coleções: Tese, Artigo Penal, Artigo Administrativo.
- [ ] Marcar cada item como: core, contextual, descartar, verificar.
- [ ] Não citar nada diretamente a partir de metadados Elicit sem verificação.

### Fase B — Artigo de História do Direito Penal

- [ ] Procurar Maria Gonçalves Cajada fora do Elicit.
- [ ] Confirmar se o caso existe nas notas locais ou em fonte primária/arquivo.
- [ ] Se o caso não aparecer, pivotar para um artigo sobre feitiçaria, prova e gênero em processos coloniais, com casos comparáveis.
- [ ] Montar matriz: caso / foro / acusação / prova / testemunhas / confissão / resultado / marcador de gênero-raça-condição.
- [ ] Decidir se o Malleus entra como horizonte doutrinário remoto ou se deve ser deixado em nota curta.

### Fase C — Artigo de Direito Administrativo

- [ ] Fazer matriz de garantias administrativas clássicas → requisito algorítmico correspondente.
- [ ] Mapear LGPD, LAI, Lei 14.129/2021 e processo administrativo.
- [ ] Selecionar 8–12 fontes principais.
- [ ] Esboçar problema: como contestar uma decisão administrativa automatizada quando a motivação é técnica, estatística ou opaca?
- [ ] Separar Brasil de literatura internacional: usar internacional para linguagem conceitual, Brasil para dogmática e normatividade.

### Fase D — Tese ICONOCRACIA

- [ ] Atualizar fila bibliográfica do capítulo Brasil com Salgueiro, Lima Junior e Entre Marianne e Clotilde.
- [ ] Usar França e Grã-Bretanha como comparadores controlados.
- [ ] Manter Introdução densa enquanto a arquitetura ainda está sendo estabilizada.
- [ ] Continuar auditoria de compressão por capítulo: Cap. 1, Cap. 2, Cap. 3, Atlas, Conclusão.
- [ ] Não cortar material ainda; apenas marcar KEEP, MERGE, MOVE, CUT ou HOLD no plano de compressão.

## 4. Decisões que Ana precisa tomar

1. O artigo penal deve insistir em Maria Gonçalves Cajada como caso central ou aceitar pivot para um conjunto de casos de feitiçaria colonial?
2. O artigo administrativo deve ser mais dogmático-normativo ou mais institucional/procedimental?
3. A tese deve tratar “Marianne à brasileira” como subcapítulo próprio ou como operador dentro do capítulo Brasil?
4. O próximo uso do Elicit deve continuar com buscas simples ou criar um relatório Elicit mais caro para uma das frentes?

## 5. Riscos

| Risco | Mitigação |
|---|---|
| Usar Elicit como se fosse bibliografia final | Verificar tudo em Zotero, DOI e editoras antes de citar |
| Expandir demais os comparadores | Manter Brasil-França-Grã-Bretanha como núcleo; demais casos só se servirem ao argumento |
| Diluir o artigo penal no Malleus | Manter foco em procedimento, prova, gênero, raça e circulação atlântica |
| Fazer artigo administrativo genérico sobre IA | Ancorar em processo administrativo, motivação, contraditório, LGPD, LAI e revisão humana |
| Cortar a Introdução cedo demais | Auditar agora; comprimir só depois que os capítulos absorverem as funções argumentativas |

## 6. Definition of Done do dia

- [x] Elicit API funcionando.
- [x] Segundo lote Elicit executado.
- [x] Resultados Elicit salvos em Markdown e JSON.
- [x] Resultados Elicit pushed para `main`.
- [x] Plano de compressão da tese atualizado previamente.
- [ ] Este plano do dia salvo e pushed para `main`.

## 7. Próximo comando recomendado para agentes

Ler, nesta ordem:

1. `docs/plans/2026-06-23-elicit-research-and-thesis-governance-plan.md`
2. `docs/research/elicit/elicit-literature-scout-2026-06-23.md`
3. `vault/projeto/compression-plan-iconocracy.md`
4. `docs/decisions/DESENHO-2-0-ICONOCRACIA-2026-06-23.md`

Depois escolher uma frente única:

- bibliografia Zotero;
- artigo penal;
- artigo administrativo;
- auditoria de compressão da tese.

Não tentar executar as quatro ao mesmo tempo.
