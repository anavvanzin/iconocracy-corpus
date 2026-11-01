# Reconciliação das cinco fontes brasileiras — 31/10/2026

Base examinada: `b1333ea46fe26c4c9671c74790dbffed5ce22c23` de `main`.
Relatório confrontado: [Acervos Históricos e Hemeroteca Nacional](https://docs.google.com/document/d/1zgyAuj7NkN1E2sR9Dg0U1_rGV7Ctxi24lH3MiGSr6Nc/edit), modificado em 31/10/2026. As observações HTTP possuem horários UTC no [registro de evidências](2026-10-31-fontes-brasileiras-evidence.json).

## Identidades e resultado

| Fonte | Identidade canônica (`item_id`) e projeção | Ficha/candidato localizado | Resultado |
|---|---|---|---|
| As Estátuas Fallando | `00a6bd05-0b74-54b4-9b93-604a012aaab6` / BR-007 | `vault/candidatos/SCOUT-437 As Estátuas Fallando (The Statues Speaking) — Justiça.md` | Localizador antigo ainda canônico; proposta 240 rejeitada; identificação do texto pendente. |
| Villares, Alegoria à Lei de 13 de Maio | `06ffa064-566d-5250-bb87-cb70c7ca6281` / BR-041 **e** `dfe19295-505c-5df1-866e-e8bb695dbc5f` | `vault/candidatos/SCOUT-553 Alegoria à Lei de 13 de Maio de 1888 (estudo).md` | Dois registros atuais; URL correta e inventário confirmados. Sem fusão. |
| Villares, A República | `e1d2e177-0905-a3bc-2e17-f6dd4f040db0` | Candidato `sq2-2026-05-19-republica-brasil-decio-villares-012` em `corpus/candidatos/2026-05-19/{candidatos-2026-05-19,sq2_candidates,hold-candidates}.json`; nenhuma ficha Markdown correspondente localizada em `vault/candidatos/` | Correspondência com Q117764760 não estabelecida; sem troca de identidade/data/URL principal. |
| Visconti, A Lei Áurea | `36e20300-49aa-5a7f-b626-70c8d058d5f8` / BR-024 | `vault/candidatos/SCOUT-408 Visconti Lei Aurea selo 1904.md` | Catálogo A813 confirmado; fonte e citação atualizadas. |
| O mundo às avessas | `4c2e84a1-6683-5e56-82a1-dc94c8b96afe` / BR-019 | `vault/candidatos/SCOUT-415 O mundo as avessas voto feminino.md` | 34623 abre edição 771/1917, posição 25; UFJF confirma data e assunto. URL/citação atualizadas, leitura do fac-símile pendente. |

São cinco fontes e seis registros, num ledger de 337 itens. O `records_item_id` histórico `67e8216b-dca2-5687-aa71-3c3161607899` da SCOUT-553 não existe no ledger atual. A nota não foi automaticamente ligada a apenas uma das duas identidades atuais.

## Conferência institucional e limites

### 1. BR-007 — proposta incorreta

Consulta direta ao [DocReader 702390/240](https://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=702390&PagFis=240) retornou HTTP 200, `PastaTxt=Ano 1827\Edição 00044`, `PagAtualTxt=5` e total de seis páginas. O catálogo identifica **Gazeta do Brasil: Quem quer ser livre, deve ser escravo da lei**, não simplesmente Brasil. A fórmula quatro páginas por edição usada no relatório não estabelece a equivalência entre paginação impressa e fotograma. O código 240 não comprova a edição 60 nem o texto pretendido.

O PDF proposto no domínio `.gov.br` retornou 404; a tentativa HTTPS no domínio legado retornou 503. Isso não demonstra descontinuação geral do domínio ou dos PDFs. Preservados o URL e a citação históricos; incluída pendência explícita. Próximo passo: localizar o diálogo no fascículo efetivo e conferir cabeçalho, data e páginas no fac-símile antes de retificar o título do periódico na citação canônica.

### 2. Alegoria abolicionista — ficha correta encontrada

[Ficha MHN /pintura-alegorica-11/](https://mhn.acervos.museus.gov.br/acervo-museologico/pintura-alegorica-11/): registro **123275**, título correspondente, autoria cadastrada como Décio Rodrigues Vilares, óleo/tela, produção **18--**, aquisição Processo 16/1941. Não há confirmação de dimensões na ficha consultada; `c. 1888` é uma estimativa histórica, não a transcrição da data institucional. Os dois `date_hint` anteriores foram preservados e a ressalva foi registrada na evidência e nas pendências.

O endereço [sem sufixo](https://mhn.acervos.museus.gov.br/acervo-museologico/pintura-alegorica/) identifica **Minha Terra (tríptico), Helios Seelinger, registro 6231**. Já [/pintura-alegorica-14/](https://mhn.acervos.museus.gov.br/acervo-museologico/pintura-alegorica-14/) identifica **Alegoria da Exposição Internacional do Centenário da Independência de 1922, Villares, registro 310906**, 105 × 74,5 cm. Nenhuma dessas duas fichas substitui o inventário 123275. A notícia usada por BR-041 redireciona atualmente ao aviso de defeso eleitoral; esse redirecionamento foi observado, sem apagar a referência histórica.

Aplicado o localizador correto às duas identidades atuais, com nova evidência e citação institucional. As duas linhas permanecem distintas; não houve deduplicação nem alteração de codificação.

### 3. A República — candidato documental, sem identidade automática

A [ficha Commons](https://commons.wikimedia.org/wiki/File:D%C3%A9cio_Villares_-_A_Rep%C3%BAblica_(MR).jpg) aponta para a [fotografia institucional do Museu da República](https://museudarepublica.museus.gov.br/wp-content/uploads/2013/12/galeria-36.jpg), acessível. A ficha colaborativa informa óleo sobre tela, **40,5 × 33 × 4 cm**, **data desconhecida**, Museu da República, Q117764760 e SHA-1 `92a3e253f9a8368129474047e2dcb076c699f453`. Q117764760 é identificador Wikidata, não número de inventário museológico. Não se comprovou que essas dimensões incluam moldura/chassi.

O candidato original representa um **conjunto** de estudos/obras e cita 1889–1931; a descrição visual canônica fala em barrete e túnica verdes, enquanto a fotografia proposta não permite assumir essa equivalência. A ligação a uma única tela exige cotejo com o binário adquirido e a sua proveniência. A data c. 1889 não é confirmada pela ficha Commons. Mantidos identidade, classificação de suporte (inclusive a inconsistência histórica `moeda`) e URL principal; registrada pendência. Não se afirma ausência geral de catálogo Tainacan apenas com base nessa busca.

### 4. Visconti — A813 confirmado, histórico do relatório corrigido

[Catálogo A813](https://eliseuvisconti.com.br/obra/a813/): c. 1903, guache e nanquim sobre papel; projeto vencedor em janeiro de 1904; original de localização desconhecida. O catálogo informa que os originais pertenciam à **Diretoria dos Correios ao menos até 1926** e que a imagem deriva de uma **miniatura hoje no acervo do Projeto Eliseu Visconti**. Portanto, não se sustenta a narrativa do relatório de permanência privada até 1926, nem a afirmação de desaparecimento desde aquela exposição. O catálogo confirma que os selos não foram executados; isso não autoriza inferir por si só a trajetória arquivística dos originais.

A data 1903 já estava no canônico e na SCOUT; A813 já estava embutido no nome do arquivo Commons. Faltavam o localizador institucional e a documentação da técnica, guarda e não execução, agora incluídos. Mantida a classificação analítica `selo`, distinguindo projeto e emissão efetiva nas notas. Citação revista sem inventar dimensões ou inventário. A transcrição da Imprensa Nacional nessa página contém `1988`; não foi reproduzida como data histórica.

### 5. O Malho — localizador corroborado com ressalva de leitura

[DocReader 116300/34623](https://memoria.bn.gov.br/DocReader/DocReader.aspx?bib=116300&PagFis=34623): HTTP 200; `PastaTxt=Ano 1917\Edição 0771`, `PagAtualTxt=25`, total 46. O [Arquivo Central da UFJF](https://www2.ufjf.br/arquivocentral/2023/02/26/24-de-fevereiro-dia-da-conquista-do-voto-feminino-no-brasil/) confirma a charge, a edição 771, **23/06/1917**, Maurício de Lacerda, Zé Povo e o diálogo. A SCOUT-415 já continha edição, p. 25 e data completa; o ledger tinha apenas 1917 e o URL 4346. A nova citação distingue posição no visualizador de página impressa.

Aplicado o URL 34623, com evidência institucional complementar. Não se afirma leitura integral da imagem da BN: o HTML do visualizador foi conferido; autoria gráfica e paginação impressa por inspeção do fac-símile permanecem pendentes. O PDF `.gov.br` retornou 404; a tentativa no domínio legado retornou 503. A suposta cadeia 34623 → 3462 → 4346 e a identificação exata do conteúdo de 4346 não foram comprovadas nesta reconciliação e não foram adotadas.

## Alterações e preservação

- Seis linhas canônicas: quatro receberam novas evidências prioritárias/localizadores/citações; duas receberam somente pendências e sinalização de auditoria. As entradas de evidência anteriores, com seus `evidence_id`, foram conservadas.
- Projeção `corpus-data.json` atualizada via funções do exportador existente, limitada às identidades em escopo. Mudanças de `creator` em quinze outras projeções, produzidas por regeneração global, foram excluídas do diff desta tarefa.
- Quatro notas SCOUT receberam adendos datados; conteúdo anterior e frontmatter foram mantidos como histórico. A lista gerada de agosto não foi reescrita como se fosse o catálogo atual.
- Preservados todos os `item_id`, `item_hash`, títulos, datas estimadas históricas, classificações, códigos, claims e inventário de atributos. O ledger `purification.jsonl` e os manifestos de binários não foram modificados.
- O timestamp histórico da linha não codificada `dfe19295…` foi mantido para impedir que o exportador o convertesse em nova data de codificação; a nova evidência possui data de verificação explícita.
- Nenhum download foi promovido a reprodução adquirida, nem atribuído novo arquivo ao manifesto. Sem merge ou publicação.

## Validação

Os resultados finais e os comandos reproduzíveis estão abaixo. A avaliação de rastreabilidade preexistente não equivale à confirmação histórica de todos os claims.

| Verificação executada | Resultado |
|---|---|
| `python tools/scripts/validate_schemas.py` | 337/337 válidos |
| `python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record` | 286/286 válidos |
| `python tools/scripts/check_corpus_export_idempotent.py` | Campos autoritativos coincidem |
| `python tools/scripts/records_to_corpus.py --diff` | 337/337, em sincronização por URL |
| `python -m pytest tests/test_corpus_export_idempotent.py tests/test_validate_schemas.py -q` | 11 aprovados |
| Comparação estrutural contra a base | Mesmos 337 IDs/hashes; seis linhas canônicas alteradas; quatro projeções alteradas somente em `url` e `citation_abnt`; toda evidência anterior preservada; códigos/classificações sem mudanças |
| `git diff --check` | Sem erros |
| `python tools/scripts/trace_evidence.py data/processed/records.jsonl --fail-on-high` | Exit 0; zero alta severidade, 641 médias e 40 baixas; os critérios amplos de cobertura do relatório **não** foram atingidos |

A checagem de rastreabilidade não valida os conteúdos históricos de cada claim e não autoriza declarar cobertura completa. Não foi executada a suíte inteira nem uma compilação da tese: não há alterações de código ou manuscrito nesta branch.
