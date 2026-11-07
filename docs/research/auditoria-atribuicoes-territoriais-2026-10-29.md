# Auditoria de atribuições territoriais, políticas e institucionais

**Data:** 2026-10-29
**Estatuto:** inventário não destrutivo; decisões sobre objetos pendentes de exame documental e curadoria de Ana.
**Base:** `b1333ea46fe26c4c9671c74790dbffed5ce22c23`, cópia isolada em `/Users/anavanzin/Documents/Codex/2026-10-29/task-3/iconocracy-corpus`, criada a partir do checkout `/Users/anavanzin/Projetos/iconocracy-corpus`.

## 1. Objeto, alcance e limite da verificação

Ana determinou que a cautela indicada por Georges passe a integrar o workflow geral da tese. Nacionalidade do artista, lugar de produção, localização atual e assunto representado não autorizam, isoladamente, atribuir uma nacionalidade única à obra. Autoria ou produção estrangeira também não exclui relação documentada com o Brasil. Cada associação deve declarar qual vínculo afirma, sua data, sua fonte e a incerteza que permanece.

O núcleo analítico vigente é **Brasil, 1822–1922**, distinto do catálogo transnacional mais amplo e dos comparanda. Esta auditoria não redefine o recorte, não muda os estatutos catalográficos e não adjudica inclusões ou exclusões. Os três estratos de análise permanecem distintos: registro documental, filologia conceitual e hipótese iconológica. Uma indicação territorial em metadados não passa automaticamente de um estrato ao seguinte.

Foram lidos instruções do projeto, documentos de método e autoridade dos dados, schemas, trechos dos scripts indicados abaixo e os arquivos de dados locais. **“Fonte do registro” significa aqui o documento ou metadado encontrado no repositório; não comprova a verdade histórica da informação.** Não houve consulta externa aos acervos, inspeção das imagens dos exemplos nem verificação das referências bibliográficas nas fontes citadas. Os exemplos identificam perguntas de pesquisa e conflitos de representação do dado.

Nenhum objeto foi reclassificado ou excluído. Os ledgers, os valores legados, as projeções, as notas de candidatos e os checkouts de origem foram preservados. Nenhum cache de plugin, espelho ou serviço externo foi alterado. Este relatório não atesta correção integral do corpus.

## 2. Base escolhida e autoridade dos arquivos

Os três checkouts locais conferidos apontam para `https://github.com/anavvanzin/iconocracy-corpus.git`:

| Checkout | HEAD conferido | Data do commit |
|---|---|---|
| `/Users/anavanzin/Projetos/iconocracy-corpus` | `b1333ea46fe26c4c9671c74790dbffed5ce22c23` | 2026-10-24T20:39:21-03:00 |
| `/Users/anavanzin/kepler/repositories/iconocracy-corpus` | `84b256ce49a30050c28e113cb1b28b11c2982053` | 2026-10-15T01:31:48-03:00 |
| `/Users/anavanzin/Recuperacao/Projetos/iconocracy-corpus` | `5839bd057d1f27c75be2a70d90362bd0794a51a8` | 2026-10-04T23:08:49-03:00 |

O primeiro contém o commit mais recente **entre os três checkouts conferidos**. O remote identifica o repositório GitHub de referência; isso não demonstra, por si só, que o checkout local contenha o estado mais recente disponível na internet. A cópia isolada usada nesta revisão tem o mesmo HEAD e seu `origin` é o caminho local de `/Projetos`.

A comparação de conteúdo identificou `records.jsonl`, `corpus-data.json` e `records_to_corpus.py` diferentes entre `/Projetos` e os outros dois checkouts. `purification.jsonl`, `gemini.ts`, `ingest_research_candidates.py`, `hunt.py` e `ingest_fichas_lpai.py` eram idênticos nos três na comparação inicial. Esses resultados delimitam a versão auditada; não constituem autorização para sincronizar os checkouts.

[AGENTS.md](../../AGENTS.md), [README.md](../../README.md) e [ADR-006](../adr/006-canonical-field-ownership-and-projections.md) confirmam a autoridade por família de campos:

| Arquivo/superfície | Autoridade constatada |
|---|---|
| `data/processed/records.jsonl` | Identidade, evidência de fonte, metadados descritivos e claims IconoCode |
| `data/processed/purification.jsonl` | Observações de endurecimento e proveniência da codificação |
| `data/raw/drive-manifest.json` + Drive | Identidade e localização dos binários |
| `vault/candidatos/` | Espelho auxiliar de catalogação e navegação |
| `corpus-data.json`, SQLite, CSV, dashboards e releases | Projeções derivadas |

O [contrato metodológico de julho](../METHOD_CONTRACT_2026-07-31.md), linha 89 da base, e `CLAUDE.md`, linhas 141/151, já determinam que país é variável analítica e não gate de inclusão no catálogo. Isso não resolve o significado dos valores antigos de país nem justifica sua promoção ao núcleo brasileiro da tese.

## 3. Inventário de pontos do workflow a auditar

Linhas indicadas referem-se à base `b1333ea`, antes dos acréscimos desta revisão. “Pendente” significa que o mecanismo foi localizado por leitura, mas não executado nem corrigido por esta auditoria.

| Etapa / arquivo e localização | Mecanismo observado | Risco metodológico e tratamento proposto | Estado |
|---|---|---|---|
| Assistência à análise: `shared/services/gemini.ts:28,185` na base | Instrução pressupunha tensão entre tradição europeia e apropriação brasileira; `generateCorpusInference` pedia especular como o artefato influenciou a cultura jurídica brasileira no XIX usando título, era e Iconclass. | Exigir relação documental antes de formular ligação com o Brasil, distinguir hipótese e evidência e permitir declarar lacuna. Título, cronologia ou taxonomia não demonstram influência. | Corrigido no diff local desta revisão, conferido após edição paralela: WebScout/IconoCode recebem o critério; a função com apenas título/era/taxonomia retorna lacuna sem chamar modelo. Saídas anteriores não foram revistas. |
| Seleção: `tools/scripts/elicit_pipeline.py:81,449–466,574` | `country_hint` extrai o primeiro país encontrado por regex em título/resumo; grava `pais`, depois promovido a `input.place_hint`. | Tema de estudo pode virar país do objeto. Conservar como pista de busca identificada, sem promover a vínculo confirmado. | Pendente; script não executado. |
| Busca: `tools/scripts/hunt.py:883–894` | `make_candidate` atribui `country` a partir do país da campanha. | Parâmetro de consulta pode adquirir estatuto de metadado do objeto. Distinguir contexto da busca e vínculos documentados. | Pendente; script não executado. |
| Ingestão: `tools/scripts/ingest_fichas_lpai.py:183–185,266–267` | Prefixo do ID vira código de país e `place_hint`. | Convenção do identificador não comprova produção, jurisdição ou pertencimento. Preservar o ID e revisar a evidência separadamente. | Pendente; script não executado. |
| Seleção: `tools/scripts/ingest_research_candidates.py:69–72,169` | `in_scope` rejeita `country` fora de `ALLOWED_COUNTRIES`; mensagem anuncia seis países. | Gate legado contradiz a regra de inclusão vigente. Revisar o mecanismo e seus consumidores sem ampliar ou reduzir automaticamente o catálogo. | Pendente; script não executado. |
| Exportação: `tools/scripts/records_to_corpus.py:185–224` | `place_hint` produz `country`; em lista, toma o primeiro elemento. Mantém fallback legado quando falta o valor canônico. | Um rótulo de lugar pode aparentar nacionalidade única, e relações múltiplas podem ser comprimidas. Qualificar a semântica e revisar consumidores antes de migrar campos. | Pendente; exportação não executada nesta auditoria. |
| Registro: `tools/schemas/master-record.schema.json:61–63` | `place_hint` é texto, sem definição do vínculo. | Não separa produção, autoria, tema, encomenda, uso ou conservação. Não inserir campos novos no ledger sem contrato de schema aprovado e versionado. | Pendente de desenho compatível; schema preservado. |
| Codificação: `tools/schemas/purification-record.schema.json:132` | `country` é descrito como “Country code of origin”. | “Origem” não especifica relação nem momento. Preservar valor legado como pista auditável; não fazê-lo valer como fonte autônoma de territorialidade. | Pendente; ledger preservado. |
| Publicação: `tools/schemas/publication.schema.json:264` | Fato `country` singular tem `status` e `source_ids`. | Proveniência é avanço, mas precisa dizer que relação a fonte documenta; uma fonte de localização não demonstra produção ou jurisdição. | Pendente; schema preservado. |
| Vault: `tools/scripts/vault_sync.py:193–196,228,256,333–372` | `pais` e `place_hint` transitam entre nota e ledger, com tags e códigos nacionais. | Espelho pode consolidar uma ambiguidade. Revisar sem renomear IDs ou sobrescrever valores antigos. | Pendente; sync não executado. |
| Contexto político: `tools/scripts/regenerate_enriched.py:156–206,359,387,432,442` | País e ano geram classificação de período político. | Valor territorial ambíguo pode produzir contexto político indevido; limites de ano também exigem fonte e precisão. Não tratar heurística como jurisdição documentada. | Pendente; script não executado. |
| Análise e divulgação: `records_to_sqlite.py:246`; `code_purification.py:326–338`; `sync_companion.py:53–56`; `build_hf_release.py:80–103`; `lacunas.py:60–75` | Campos e contagens por país reproduzem rótulos existentes; `lacunas.py` trabalha com escopo de seis países. | Contagem de rótulos não equivale a distribuição de nacionalidades, jurisdições, circulação ou núcleo Brasil 1822–1922. Declarar a unidade e a semântica antes de usar na tese. | Pendente; consumidores não executados. |

Os pontos acima são mecanismos de risco identificados. Sua existência não demonstra que todas as saídas estejam historicamente erradas. A revisão dos scripts restantes deve preservar compatibilidade, possuir diff próprio e verificar os consumidores pertinentes, sem executar chamadas pagas ou publicar automaticamente.

## 4. Fila inicial de registros, sem adjudicação

Os exemplos foram escolhidos por exporem relações diferentes no mesmo rótulo ou divergências internas. A formulação em aspas abaixo transcreve o registro local; não representa classificação aceita por esta auditoria.

### Item `48a9d6b2-6c5e-55cd-b594-d0c43e67d64e`

- **Título e localização:** *Female Allegory (Pierre Puvis de Chavannes)*; `data/processed/records.jsonl:47`; projeção `corpus/corpus-data.json:2732`.
- **Formulação legada:** `place_hint = "France (held in Austria)"`; data `"19th century"`.
- **Fundamento documental observado no registro:** URL Europeana `https://www.europeana.eu/en/item/15508/DG1918_7`; citação local nomeia Puvis de Chavannes e Albertina Museum. O próprio rótulo distingue “France” de “held in Austria”.
- **Lacuna:** o registro consultado não esclarece que fonte documenta cada vínculo, o momento da conservação, o local de produção, a encomenda, a jurisdição ou eventual circulação/recepção no Brasil.
- **Correção proposta para exame:** preservar o texto legado; desdobrar as afirmações somente conforme as fontes confirmarem autoria, produção e conservação. Registrar separadamente a justificativa de eventual uso no núcleo, como comparandum ou em outra função já prevista no projeto. Nacionalidade autoral e acervo atual não bastam para decidir.
- **Estado:** pendente de consulta ao registro de acervo, documentação disponível e curadoria. Nenhuma inclusão, exclusão ou atribuição territorial foi decidida.

### Item `6a70603a-9224-56ba-87f5-c10133b7706b`

- **Título e localização:** *Justitia (Jacob Matham)*; `data/processed/records.jsonl:76`; projeção `corpus/corpus-data.json:2597` (`EU-003`).
- **Formulação legada:** `place_hint = "Germany (Netherlands origin)"`; data `"c. 1600"`.
- **Fundamento documental observado no registro:** URL Europeana `https://www.europeana.eu/en/item/89/item_ZCR4KC47OMJN7DRRDFTIWRQS33M7PBN2`; citação local nomeia Jacob Matham e Herzog Anton Ulrich Museum; resumo local chama o autor de gravador neerlandês.
- **Lacuna:** não está determinado no material auditado se “Germany” indica conservação, produção ou outra relação, nem o sentido e a fonte de “Netherlands origin”. As denominações históricas e a jurisdição em torno de 1600 precisam de verificação. O eventual vínculo com o Brasil também não foi demonstrado.
- **Correção proposta para exame:** manter o valor e os identificadores; qualificar cada relação com data e fonte. Examinar sua função genealógica ou comparativa fora do núcleo Brasil 1822–1922 conforme o contrato e as decisões já vigentes, sem transformar a data ou o país em exclusão automática.
- **Estado:** pendente. A flag local `fora-do-escopo` foi observada e preservada; não foi ratificada ou removida por esta auditoria.

### Item `8d6151b3-9928-e42e-5dbc-713c10fe1a82`

- **Título e localização:** *La Justice et la Vengeance Divine poursuivant le Crime*; `data/processed/records.jsonl:264`; projeção `corpus/corpus-data.json:714–717`.
- **Formulação legada:** `place_hint = "United Kingdom"`; data `"1840–1878"`. A projeção reproduz `country = "United Kingdom"`.
- **Fundamento documental observado no registro:** URL `https://www.britishmuseum.org/collection/object/P_1878-0713-2311`; citação local nomeia Gusman, Prud'hon, Hadamard, número de inventário e British Museum, London. `ingest_research_candidates.py:58–60` contém override histórico para `"France"` no candidato Gusman, justificado por comentário sobre composição/reprodução francesa.
- **Lacuna:** a citação do acervo e o comentário do script não comprovam, nesta auditoria, qual relação territorial cada rótulo pretende expressar. Faltam conferência do registro de acervo, identificação precisa da reprodução em relação à composição e documentação de produção, encomenda, circulação ou recepção pertinente à tese.
- **Correção proposta para exame:** registrar o conflito entre rótulos sem substituir automaticamente Reino Unido por França ou o inverso. Distinguir objeto/composição/reprodução, instituição custodiante e demais relações que as fontes sustentarem; justificar separadamente qualquer relação com o núcleo brasileiro.
- **Estado:** pendente de pesquisa e curadoria. O override é evidência de uma decisão anterior de tratamento do dado, não confirmação histórica independente.

## 5. Critério para a revisão posterior dos registros

Cada ficha de revisão deve conservar o valor legado e identificar: ID estável; afirmação exata em exame; relação territorial, política ou institucional pretendida; data ou intervalo pertinente; jurisdição e denominação histórica quando pertinentes; fonte e localizador; o que essa fonte permite afirmar; lacuna ou conflito; redação proposta; decisão e responsável, quando houver adjudicação. A fila não destrutiva pode permanecer neste documento de pesquisa. Afirmações revistas podem usar `iconocode.interpretation` e `iconocode.validation.claim_ledger`, já existentes, sem inventar novos campos no ledger nem exigir migração de schema. Não é necessário preencher dimensões sem pertinência à afirmação.

Os vínculos a distinguir são autoria e suas qualificações pertinentes, produção, encomenda/patrocínio, tema representado, contexto político e jurisdição à época, instalação/uso, circulação, recepção e conservação atual. Um vínculo não prova os demais. “Desconhecido”, “não pesquisado”, “fonte indisponível” e “fontes conflitantes” exigem descrições distintas; nenhum deles autoriza preencher a lacuna por nacionalidade presumida.

Para cada decisão futura de inclusão no núcleo Brasil 1822–1922, a justificativa deve dizer qual relação documentada torna o objeto pertinente ao problema e à cronologia. Uma autoria estrangeira pode coexistir com encomenda, uso ou recepção documentada no Brasil. Uma referência temática ao Brasil, sozinha, não demonstra essas relações. Comparanda devem ter função e fundamento de comparação declarados. Nenhuma soma, pontuação agregada ou gate nacional substitui essa análise.

## 6. Verificações e pendências

Passaram a leitura e o parse JSON dos arquivos locais `records.jsonl`, `purification.jsonl` e `corpus-data.json`, a conferência das declarações de autoridade em AGENTS/README/ADR-006 e a comparação dos HEADs e conteúdos selecionados dos três checkouts. Essas verificações são estruturais e de proveniência local, não validação histórica das atribuições.

O daemon de fsmonitor falhou em uma chamada inicial de Git. As consultas de estado e diff com `git -c core.fsmonitor=false` concluíram; o checkout `/Projetos` permaneceu sem alterações durante a auditoria. Nenhuma configuração global ou de segurança foi modificada.

Não foram executados por esta auditoria ingestão, sync, exportação, publicação, modelos, testes de código ou revisão integral dos registros. O diff local de `shared/services/gemini.ts` foi conferido: acrescenta a separação de vínculos, impede a presunção de influência brasileira e mantém a assinatura de `generateCorpusInference`, que retorna uma lacuna sem chamar modelo. Os testes desse código pertencem à revisão paralela e devem ser relatados com seus resultados próprios; a leitura do diff não os substitui. A consulta externa aos acervos, a auditoria completa dos demais consumidores de `country` e a decisão sobre cada objeto permanecem pendentes. Uma eventual expansão futura do schema exige desenho próprio, mas não é pré-requisito deste critério. A correção dos prompts não implica revisão das saídas antigas.
