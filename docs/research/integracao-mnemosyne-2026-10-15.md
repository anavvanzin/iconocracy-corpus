---
tipo: nota-de-integracao
data: "2026-10-15"
status: registro-editorial
documento: tese/pesquisa/dossie-bilderatlas-mnemosyne-2026-10-15.md
commit_base: dc5363bbbfca3e572a6a0cb33e1133428056291f
---

# Integração do dossiê do Bilderatlas Mnemosyne

O [dossiê revisado](../../tese/pesquisa/dossie-bilderatlas-mnemosyne-2026-10-15.md) integra a pesquisa como estudo metodológico comparativo. Sua hipótese sobre a Feminilidade de Estado permanece proposta interpretativa, sujeita à demonstração por objeto, suporte e contexto institucional. Esta nota registra a revisão editorial e documental autorizada em 15 de outubro de 2026; não constitui nova decisão metodológica da tese.

## Proveniência da revisão

O texto de partida foi encaminhado pela pesquisadora na conversa de trabalho, com o título **“ICONOCRACIA Agent — Dossiê analítico do Bilderatlas Mnemosyne”**. O arquivo recebido, `Pasted text.txt`, tem 43.278 bytes e SHA-256:

```text
5358a11f153c2b93557ea6eb97f569f995bc3daabe1f831ee2469953e1c89195
```

O parecer produzido antes da autorização de integração tem SHA-256:

```text
fcb6b8a52601aa741e04f7aa3a63360a9579b9fe8e7eb8a8dc73bdd6f78f9fb0
```

Os hashes identificam os insumos recebidos e revisados; não lhes atribuem validação histórica. A versão original continha um endereço temporário de arquivo. O dossiê integrado utiliza o [registro editorial estável do HKW](https://archiv.hkw.de/en/media/publikationen/2020_publikationen/publikation_aby_warburg_bilderatlas_mnemosyne_the_original.php) e o ISBN 978-3-7757-4693-9 para identificar a edição de 2020.

O exame do protocolo e dos números de trabalho utiliza o commit-base [dc5363bbbfca3e572a6a0cb33e1133428056291f](https://github.com/anavvanzin/iconocracy-corpus/commit/dc5363bbbfca3e572a6a0cb33e1133428056291f), confirmado como `main` remoto durante a revisão. O instantâneo é identificável; o corpus permanece aberto.

O anexo recebido e o parecer permanecem na conversa de trabalho e não são versionados por esta integração. Os hashes permitem comparar cópias desses insumos; não permitem recuperá-los por si sós.

## Correções incorporadas

| Tema | Tratamento na versão revisada |
|---|---|
| Hipótese central | Gestão institucional de movimento, repouso, desejo e violência; pose isolada não demonstra agência ou submissão. |
| Referências | Notas de fonte válidas, caminhos relativos ao repositório e distinção entre fontes consultadas e documentos anteriores indisponíveis. |
| Dimensões | Divergência entre Cornell e a documentação especializada de 2020; separação entre suportes históricos e remontagem de 2019. |
| Cronologia | Distinção entre o início situado por Cornell em 1924 e o trabalho sistemático datado pelo Warburg Institute em fevereiro de 1927. |
| Prancha 47 | 28 entradas de imagem sob 26 grupos numerados no catálogo Cornell; identificação por imagem e subitem. |
| Prancha 61–64 | Numeração composta de uma prancha. |
| Estudo quantitativo | Alcance de 21 das 63 pranchas e 318 imagens; resultados exploratórios não demonstram ausência histórica de transmissão. |
| Caso do Benim | Registro de Warburg e identificação moderna proposta por Giovanna Targia, conforme resumo da palestra de 29/09/2026. |
| Esquema de dados | Ficha piloto explicitamente conceitual, sem alegar conformidade com `master-record` ou produzir observações de codificação. |
| Instrumento | Data de execução separada de versão; ausência de versão aplicada ou confiança fundamentada permanece declarada. |
| Endurecimento | Aposentadoria do índice composto e remoção posterior do campo; permanência de indicadores ordinais separados em 0–3, inventário verbal e proveniência. |
| Arquitetura do atlas | Os novos eixos são proposta alternativa a confrontar com os oito painéis já redigidos no capítulo 9. |

As formulações autorais do dossiê não devem circular como citações literais dos autores discutidos. O estudo não estabelece uma genealogia universal da Ninfa até a alegoria estatal nem demonstra inexistência de precedentes de atlas jurídico.

## Instantâneo documental

Contagens diretas dos arquivos no commit-base:

| Arquivo | Contagem | Natureza |
|---|---:|---|
| [`records.jsonl`](../../data/processed/records.jsonl) | 337 | Registros de itens |
| [`purification.jsonl`](../../data/processed/purification.jsonl) | 286 | Observações de codificação |
| [`corpus-data.json`](../../corpus/corpus-data.json) | 337 | Itens na projeção pública |

O [README](../../README.md#corpus-snapshot) já documenta esses números em um instantâneo de 04/10/2026. As contagens não certificam cobertura, qualidade ou disponibilidade das imagens. A [ADR-006](../adr/006-canonical-field-ownership-and-projections.md) distribui a autoridade por família de campos e admite várias observações por item.

Os antigos totais 335/328/95 não foram promovidos a descrição atual. Documentos históricos conservam sua própria data e versão. A adoção de quatro regimes é compatível com o esquema atual; hipóteses concorrentes de regime em uma prancha não equivalem a codificação aceita de cada objeto.

O [codebook MASTER](../methodology/codebooks/codebook-MASTER.md) declara 2.2.1, em estado `pre_freeze`; o [documento 2.3.0](../methodology/codebooks/codebook-v2.3.0.md) permanece piloto. O dossiê não atribui retrospectivamente uma versão única aos dados. A [decisão sobre a remoção do composto](../decisions/2026-09-24-remocao-definitiva-do-campo.md), incluindo a verificação de 29/09, rege o tratamento atual do endurecimento.

## Referências anteriores não recuperadas

O texto recebido indicava oito documentos por caminhos relativos que não estavam presentes nos destinos informados no checkout. Os números abaixo identificam as referências da versão recebida:

| Referência original | Destino informado | Tratamento |
|---|---|---|
| 1 | `proveniencia/prosa-citavel-4.4-montagem-warburguiana.md` | Não recuperada nesta revisão. |
| 4 | `proveniencia/prosa-citavel-4.1-epistemologia.md` | Não recuperada nesta revisão. |
| 5 | `proveniencia/relatorio-sintese-deep-research-cap4.md` | Não recuperada nesta revisão. |
| 7 | `collection_0ed13c45-6a9b-4fff-a7a4-48baae68ffa7/038d6770-d962-4398-8cf8-12136ec9c04b/master-iconographic-metadata-taxonomy.md` | Não recuperada nesta revisão. |
| 8 | `proveniencia/rastreador-proveniencia.md` | Não recuperada nesta revisão. |
| 18 | `proveniencia/ledger-claims-capitulo4.md` | Não recuperada nesta revisão. |
| 19 | `proveniencia/errata-curta-capitulo4.md` | Não recuperada nesta revisão. |
| 31 | `proveniencia/crosswalk.md` | Não recuperada nesta revisão. |

Documentos atuais são citados somente para as proposições que sustentam. Não são apresentados como cópias ou equivalentes integrais das fontes anteriores. A ausência no caminho informado não prova que esses documentos nunca existiram em outro ambiente.

## Alcance da integração

A contribuição entra em `tese/pesquisa`, com navegação pelo README. As hipóteses e o exemplo piloto não são inseridos nos ledgers, no catálogo de objetos ou nos dados do site. A organização dos capítulos permanece aquela da [compilação ativa](../../vault/tese/Makefile); os oito eixos propostos dependem de comparação com o [capítulo 9](../../tese/manuscrito/Capitulo9_paineis_atlas.md) antes de eventual adoção.

Não foi autenticada uma execução da skill externa mencionada na versão recebida, nem consultado integralmente o volume de 2020. As notas do dossiê identificam fontes institucionais e estudos selecionados. A bibliografia anterior não é certificada de forma exaustiva; a referência 23 do texto recebido não foi lida nesta rodada. O arquivo original e o parecer permanecem identificados pelos hashes acima, sem apresentar sua existência como substituto da crítica de fontes.
