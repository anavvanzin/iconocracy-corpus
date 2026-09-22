# Fila de integração auditável — SCOUT-575–624

## Resultado executivo

- Escopo: 50 notas consecutivas, SCOUT-575 a SCOUT-624.
- Decisão: **7 integrar**, **26 revisar**, **17 descartar**.
- Patch pronto: 7 novas linhas, exatamente os 7 itens classificados como `integrar`; não aplicado.
- Ledger real no início da geração: 328 registros; SHA-256 `e9d05d7c3147ed20a8937c6bc5b1a58d752f0f2a41a11f78f2508f18077cfc2f`.
- Baseline citado no plano (`d23056f3370df7c8543d1f38ca49bd4a62de7637697990ebc31b84f548719664`) estava defasado em relação ao `HEAD`; a auditoria adotou o baseline vivo, limpo e validado antes da escrita.
- CLIP: `skipped (runtime missing)`. A deduplicação textual cobriu `input_url`, `webscout.search_results[].url`, ARKs, inventários/object IDs, títulos normalizados, vault e o próprio lote.
- Imagens: as imagens institucionais dos sete itens prontos foram inspecionadas sem guardar binários no repositório.
- Fonte-base: snapshots de APIs institucionais gerados por `hunt.py` em 2026-07-25; consulta/auditoria em 2026-07-30. Firecrawl não foi usado como prova porque o serviço estava inacessível por DNS.

## Chave de leitura

Os quatro sinais na coluna “critérios” aparecem na ordem: figura alegórica feminina / função jurídico-política / período ou coorte / suporte aceito. `sim` = comprovado; `?` = incerto; `não` = falha comprovada. A evidência granular, os campos comprovados e os sinais de deduplicação estão no JSONL correspondente.

## Fila

| SCOUT | decisão | dedupe | critérios | justificativa | alvo dedupe | correções aplicadas | patch |
|---|---|---|---|---|---|---|---|
| SCOUT-575 | **revisar** | CLEAR | ?/?/?/? | Título sugere personagens alegóricos, mas a fonte capturada não comprova figura feminina, data, suporte ou função jurídico-política. | — | — | não |
| SCOUT-576 | **revisar** | CLEAR | sim/?/?/? | Justitia é nomeada, porém faltam data, suporte e contexto funcional do objeto. | — | — | não |
| SCOUT-577 | **revisar** | CLEAR | sim/?/?/? | Justitia é nomeada, mas a captura não fecha data, suporte nem função do objeto. | — | — | não |
| SCOUT-578 | **revisar** | CLEAR | ?/?/?/? | O título inclui magistratura, mas não comprova que a figura alegórica seja feminina nem o suporte/período. | — | — | não |
| SCOUT-579 | **revisar** | CLEAR | sim/?/?/? | Justitia é nomeada, porém data, suporte e função jurídico-política permanecem lacunas. | — | — | não |
| SCOUT-580 | **revisar** | CLEAR | sim/?/?/? | Justitia e Sapientia são nomeadas, mas faltam data, suporte e contexto funcional. | — | — | não |
| SCOUT-581 | **descartar** | DUPLICATE | sim/sim/sim/? | Duplicata exata do ARK e da fotografia Agence Rol de 1916 já incorporada ao registro canônico. | records.jsonl item 4d84fe99-7db7-5ea5-96cd-bca3bd57a189; vault SCOUT-433 | suporte: indeterminado → fotografia | não |
| SCOUT-582 | **revisar** | SIMILAR | sim/sim/sim/sim | Mesmo núcleo de título, autor e tipologia de item canônico, mas ARKs distintos; pode ser estado/variante. | records.jsonl item 442ad547-ffbb-5581-8290-7d514f87d0d4; vault SCOUT-465 | suporte: selo → estampa | não |
| SCOUT-583 | **revisar** | SIMILAR | sim/sim/sim/? | Fotografia/estado diferente da République de Clésinger já catalogada; requer adjudicação de variante. | records.jsonl item 81efcd9a-e5c1-5525-a2ed-6c4cbd0c3954; vault SCOUT-431/SCOUT-554 | suporte: indeterminado → fotografia | não |
| SCOUT-584 | **descartar** | CLEAR | não/não/sim/sim | Fotografia de pessoas chamadas “les Mariannes” antes de desfile, não personificação feminina do Estado. | — | suporte: indeterminado → fotografia | não |
| SCOUT-585 | **revisar** | CLEAR | ?/sim/sim/sim | Estampa revolucionária pré-1800 potencialmente elegível, mas a miniatura oficial é pequena demais para fechar a alegoria feminina. | — | suporte: selo → estampa | não |
| SCOUT-586 | **revisar** | SIMILAR | sim/sim/sim/sim | Provável variante de obra revolucionária já catalogada; ARK diferente impede descarte automático. | records.jsonl item b52f4742-c987-5a72-8b5d-720b39aa234d; vault SCOUT-432/SCOUT-555 | suporte: selo → estampa | não |
| SCOUT-587 | **revisar** | SIMILAR | sim/sim/sim/? | Vista fotográfica da mesma série monumental de 1889 já catalogada; possível variante. | records.jsonl item 942ef9d3-f17b-5ced-a36f-c2277a4018a1; vault SCOUT-435/SCOUT-556 | suporte: monumento → fotografia | não |
| SCOUT-588 | **revisar** | SIMILAR | sim/sim/sim/? | Segunda vista fotográfica da mesma série monumental de 1889; requer decisão de variante. | records.jsonl item 942ef9d3-f17b-5ced-a36f-c2277a4018a1; vault SCOUT-435/SCOUT-556 | suporte: monumento → fotografia | não |
| SCOUT-589 | **integrar** | CLEAR | sim/sim/sim/sim | Objeto único do Met; imagem oficial confirma alegoria feminina da abolição, contexto político, data e terracota escultórica. | — | suporte: monumento → escultura; citacao: inversão automática do nome institucional do autor → ANONYMOUS, French School, 19th Century | sim |
| SCOUT-590 | **descartar** | CLEAR | ?/não/?/sim | Alegoria sazonal do Inverno sem função jurídico-política documentada. | — | suporte: indeterminado → pintura | não |
| SCOUT-591 | **integrar** | CLEAR | sim/sim/sim/sim | Objeto único do Met; imagem e ficha confirmam Liberdade feminina revolucionária em estampa de ca. 1794. | — | — | sim |
| SCOUT-592 | **descartar** | CLEAR | não/não/?/não | Sepultura de pessoa chamada Marianne Lincke; falso positivo onomástico. | — | — | não |
| SCOUT-593 | **descartar** | CLEAR | não/não/?/não | Lápide de Marianne Willemer; pessoa biográfica, não alegoria. | — | — | não |
| SCOUT-594 | **descartar** | CLEAR | não/não/?/não | Lápide de Marianne Sonneborn; pessoa biográfica, não alegoria. | — | — | não |
| SCOUT-595 | **revisar** | CLEAR | sim/sim/?/? | Título promete Marianne da França, mas faltam data, suporte e descrição visual suficiente. | — | — | não |
| SCOUT-596 | **descartar** | CLEAR | não/não/?/não | Sepultura de Marianne Schadow; pessoa biográfica, não alegoria. | — | — | não |
| SCOUT-597 | **descartar** | CLEAR | não/não/?/não | Memorial de Paul e Marianne Ehrlich; falso positivo onomástico. | — | — | não |
| SCOUT-598 | **revisar** | SIMILAR | sim/sim/sim/sim | Moeda francesa de 1 franc/1849 semanticamente coincide com a Cérès republicana já canônica; requer confronto de tipo/denominação. | records.jsonl item 1444ee85-06cf-59c5-9070-6a2f684cb269; vault SCOUT-094 | — | não |
| SCOUT-599 | **descartar** | DUPLICATE | sim/sim/sim/? | Duplicata exata do ARK btv1b6952880n já registrado no ledger. | records.jsonl item 4d84fe99-7db7-5ea5-96cd-bca3bd57a189; vault SCOUT-471 | url: http://gallica.bnf.fr/ark:/12148/btv1b6952880n → https://gallica.bnf.fr/ark:/12148/btv1b6952880n; suporte: indeterminado → fotografia | não |
| SCOUT-600 | **descartar** | CLEAR | não/não/sim/? | Retrato de Marianne Vogelweid, pessoa identificada como esposa de Hans Vogelweid. | — | — | não |
| SCOUT-601 | **integrar** | CLEAR | sim/sim/sim/sim | Medalha espanhola de 1873, única; descrição e imagem oficiais confirmam matrona republicana, barrete frígio e nível. | — | pais: BR → ES; autoria: Grabador: García, J. → García, J. (grabador); citacao: J., Grabador: García, → GARCÍA, J. | sim |
| SCOUT-602 | **integrar** | CLEAR | sim/sim/sim/sim | Ficha numismática única; fonte e imagem confirmam República Francesa sentada, fasces, barrete frígio e lema de 1870. | — | pais: BR → FR; suporte: moeda → ficha | sim |
| SCOUT-603 | **revisar** | CLEAR | sim/?/?/? | Título confirma Respublica e Justitia, mas data, suporte e contexto institucional do objeto permanecem abertos. | — | — | não |
| SCOUT-604 | **integrar** | CLEAR | sim/sim/sim/sim | Relevo único de Córdoba; ficha e imagem oficiais confirmam figura feminina republicana com barrete frígio, balança e inscrição cívica. | — | pais: BR → ES; suporte: indeterminado → escultura; autoria: Moreno, Enrique com biografia embutida → Moreno, Enrique; citacao: entrada iniciada pela data de morte → MORENO, Enrique | sim |
| SCOUT-605 | **integrar** | CLEAR | sim/sim/sim/sim | Medalha única de Lyon; descrição e imagem oficiais confirmam cabeça feminina da República Francesa e data 1872. | — | pais: BR → FR; suporte: moeda → medalha | sim |
| SCOUT-606 | **revisar** | SIMILAR | ?/sim/sim/sim | Selo italiano de 1953 coincide semanticamente com a série Siracusana/Italia Turrita já canônica; precisa confronto de emissão/denominação. | records.jsonl item 5e332b45-467b-5e4a-b73a-07bab0a2493a; vault SCOUT-482 | titulo: multiline-invalid-yaml → Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950. Frimärke från Italien, 1953. Motiv av "Republica Italiana"; data_estimada:  → 1953; pais: BR → IT; suporte: indeterminado → selo | não |
| SCOUT-607 | **integrar** | CLEAR | sim/sim/sim/sim | Estampa satírica única; descrição e imagem oficiais confirmam jovem República expulsando um rei no contexto da queda de Napoleão III. | — | data_estimada:  → 1870; pais: BR → ES; suporte: moeda → estampa; autoria: Ortego y Vereda com locais/datas embutidos → Ortego y Vereda, Francisco (1833–1881), dibujante e editor; citacao: entrada iniciada pela data de morte → ORTEGO Y VEREDA, Francisco | sim |
| SCOUT-608 | **revisar** | CLEAR | ?/?/?/? | Veritas e justiça divina são nomeadas, mas gênero, data, suporte e função jurídico-política secular não estão fechados. | — | — | não |
| SCOUT-609 | **revisar** | SIMILAR | sim/?/?/? | Justitia é clara, mas há candidato semanticamente equivalente no vault e faltam data/suporte para decidir se é outro objeto. | vault SCOUT-347; sem alvo inequívoco no ledger | — | não |
| SCOUT-610 | **revisar** | CLEAR | ?/sim/?/? | Tema judicial é explícito, mas a captura não comprova alegoria feminina, data ou suporte. | — | — | não |
| SCOUT-611 | **revisar** | CLEAR | ?/?/?/? | Imagem da Justiça é mencionada, mas faltam gênero confirmado, data, suporte e função do objeto. | — | — | não |
| SCOUT-612 | **descartar** | CLEAR | sim/?/sim/não | Folha de Stammbuch manuscrita/desenhada de 1648; suporte fora do recorte de integração pronta. | — | data_estimada:  → 1648; suporte: indeterminado → manuscrito | não |
| SCOUT-613 | **descartar** | CLEAR | não/não/sim/sim | Pintura religiosa em madeira, 1701–1800, sem alegoria feminina ou função jurídico-política comprovadas. | — | data_estimada:  → 1701-1800; pais: FR → DE; suporte: indeterminado → pintura | não |
| SCOUT-614 | **revisar** | SIMILAR | ?/sim/sim/sim | Estado de estampa do 18 mars; imagem mostra cena coletiva e o lote contém outro estado muito próximo. | intra-lote SCOUT-616 | suporte: selo → estampa | não |
| SCOUT-615 | **descartar** | CLEAR | não/não/sim/sim | Imagem oficial mostra cena de gênero com mulher e homem, sem personificação jurídico-política. | — | titulo_yaml: double-quoted scalar with unescaped inner quotes → single-quoted scalar, same source text; suporte: selo → estampa | não |
| SCOUT-616 | **revisar** | SIMILAR | ?/sim/sim/sim | Outro estado da estampa 18 mars; similaridade intra-lote exige adjudicação antes de integrar. | intra-lote SCOUT-614 | titulo_yaml: double-quoted scalar with unescaped inner quotes → single-quoted scalar, same source text; suporte: selo → estampa | não |
| SCOUT-617 | **descartar** | CLEAR | não/não/sim/sim | Imagem oficial mostra cena social/narrativa, sem personificação jurídico-política. | — | titulo_yaml: double-quoted scalar with unescaped inner quotes → single-quoted scalar, same source text; suporte: selo → estampa | não |
| SCOUT-618 | **descartar** | CLEAR | não/não/sim/sim | Le lait é cena social, sem alegoria feminina jurídico-política documentada. | — | suporte: selo → estampa | não |
| SCOUT-619 | **revisar** | CLEAR | ?/sim/sim/sim | Estampa de auxílio nacional com função política/social, mas a fonte textual não confirma alegoria feminina. | — | suporte: selo → estampa | não |
| SCOUT-620 | **descartar** | CLEAR | não/?/sim/sim | O título identifica dois poilus, figuras masculinas; falha o critério de alegoria feminina. | — | suporte: selo → estampa | não |
| SCOUT-621 | **revisar** | CLEAR | ?/sim/sim/sim | Estampa de auxílio aos feridos com função político-social, mas alegoria feminina não confirmada. | — | suporte: selo → estampa | não |
| SCOUT-622 | **revisar** | CLEAR | ?/sim/sim/sim | Estampa de auxílio aos mutilados de guerra; função social confirmada, alegoria feminina ainda incerta. | — | suporte: selo → estampa | não |
| SCOUT-623 | **descartar** | CLEAR | não/não/sim/sim | Almanaque antijansenista de 1654; não há alegoria feminina ou função jurídico-política compatível comprovada. | — | suporte: selo → estampa | não |
| SCOUT-624 | **revisar** | CLEAR | ?/?/sim/sim | Frontispício de tese pré-1800 potencialmente genealógico; imagem/contexto da tese precisam confirmar alegoria e função jurídica. | — | suporte: selo → estampa | não |

## Itens prontos

- **SCOUT-589** — `bb3fcce4-25b0-57ee-ae97-2980e1782f7f` — Sketch of an Allegory of the Abolition of Slavery
- **SCOUT-591** — `fd811e8e-9b73-5573-84ea-6e1afc4c7630` — La Liberté
- **SCOUT-601** — `539b8a82-4556-5407-8bce-98c087601f73` — Medalla
- **SCOUT-602** — `666a7b2a-aaac-5350-9f9f-171afb65e6c9` — Ficha
- **SCOUT-604** — `1db23347-0bfa-5ac6-a391-d6e5eb25df54` — Relieve de la República - Relieve
- **SCOUT-605** — `546bce0e-501e-564e-85c5-7c7b7c7851c7` — Exposición Universal de Lyon - Medalla
- **SCOUT-607** — `1f9ee8fb-0855-57e4-9a27-bc2c6f463c47` — Lo que puede suceder. - Estampa

## Garantias de escopo

- Nenhuma nota recebeu `records_item_id`.
- Nenhum campo `regime`, Iconclass, `endurecimento`, `purificacao` ou escore foi alterado.
- Itens `revisar` e `descartar` não aparecem no patch.
- `data/processed/records.jsonl` e `corpus/corpus-data.json` não são escritos por este gerador.
- A versão JSONL é a trilha probatória completa; este Markdown é a fila humana.
