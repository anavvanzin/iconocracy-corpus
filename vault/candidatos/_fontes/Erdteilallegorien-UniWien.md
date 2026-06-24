---
tipo: fonte/base-de-dados
status: auditada
titulo: "Erdteilallegorien im Barockzeitalter — Forschungsdatenbank (Univ. Wien)"
url: https://erdteilallegorien.univie.ac.at/erdteilallegorien
instituicao: "Institut für Geschichte, Universität Wien"
financiamento: "FWF Austrian Science Fund — P23980"
direcao: "Wolfgang Schmale"
coordenacao_cientifica: "Marion Romberg (marion.romberg@uni-bonn.de)"
licenca: CC-BY-NC-ND
n_registros: 425
periodo_fonte: "Barroco (séc. XVII–XVIII)"
recorte_geografico: "Sul do Sacro Império (Suábia, Baviera, Vorarlberg, Tirol, Áustria, Boêmia)"
relevancia_tese: "matriz genealógica — Cap. 3 (Contrato Racial Visual) e Cap. 5.2 (Purificação Clássica)"
created: "2026-06-24"
updated: "2026-06-24"
tags:
  - fonte/base-de-dados
  - contrato-racial-visual
  - colonialidade-do-ver
  - regime/fundacional
  - motivo/erdteilallegorie
---

# Erdteilallegorien im Barockzeitalter (Univ. Wien) — Auditoria de Fonte

> [!info] Síntese
> Base de dados acadêmica com **425 registros** de alegorias dos quatro continentes
> (Europa, Ásia, África, América) na arte barroca do Sul do Sacro Império. Dirigida por
> **Wolfgang Schmale**, coordenação científica de **Marion Romberg** (FWF P23980).
> Licença **CC BY-NC-ND**. Sem API nem export em massa.

## Veredito de relevância

> [!warning] Descompasso de período
> Recorte da fonte = **Barroco (séc. XVII–XVIII)**; recorte da tese = **1800–2000**.
> **Não é fonte de itens diretos** para `records.jsonl`. É **matriz genealógica**.

Alta utilidade como antecedente iconográfico para:

- **Contrato Racial Visual** (Cap. 3) — a alegoria dos continentes é o dispositivo onde a
  "universalidade" branca neoclássica se constrói por contraste com Asia/Africa/America.
  Estampas de Ripa e Bergmüller são o antecedente direto dos modelos que migram para
  Marianne / Columbia / Germania no séc. XIX. → [[Cap3_analise_quantitativa]]
- **Purificação Clássica** (Cap. 5.2) — documenta o estágio `regime/fundacional` (corpo
  barroco vivo, sensual, narrativo) anterior ao endurecimento estatal do XIX. *Nachleben*
  warburguiano do motivo. → [[corpus-data]]
- **Metodologia** — indexa com **Iconclass** + glossário controlado e gera **citação
  automática** por registro: modelo comparável ao pipeline próprio.

## Estrutura de dados (modelo de 3 entidades)

`Orte` (locais/edifícios) ↔ `Allegorien` (obras) ↔ `Personen` (artistas/patronos).

Cada registro de alegoria: artista · patrono · assinatura · data · técnica · posição
(ex. "Decke/Fresko") · histórico de restauro · fontes textuais/visuais · interpretação
iconográfica · **códigos Iconclass** · termos de glossário · 10–20 imagens ordenadas
(exterior → interior).

Navegação: índices alfabéticos (`/erdteilallegorien`, `/personen`, `/orte`),
timeline (`/zeitleiste`), busca (`/suche`), mapa histórico, bibliografia (`/biblio`).

## Casos-âncora citáveis (precedentes iconográficos)

- Cesare Ripa, *Iconologia* (1603) — fonte-matriz dos atributos.
- Séries de **Gottfried Bernhard Göz** e **Johann Georg Bergmüller**.
- Naturhistorisches Museum (Viena) · Palais Liechtenstein · Schloss Laudon.

## Restrições de uso

> [!caution] Licença CC BY-NC-ND
> - Pode-se **citar e linkar**; **não** redistribuir imagens nem criar derivados sem permissão.
> - Reuso de fotografias **exige autorização prévia da equipe**.
> - **Não incluir imagens deles** no dataset HF/público — apenas referência + URL + crédito.
> - Sem API; várias subpáginas têm anti-bot (403). Coleta automatizada em escala violaria os
>   termos. Via correta: **contatar Marion Romberg** para colaboração de dados.

## Bibliografia de referência (→ `references.bib`)

- ROMBERG, Marion. *Die Welt im Dienst des Glaubens. Erdteilallegorien in Dorfkirchen auf
  dem Gebiet des Fürstbistums Augsburg im 18. Jahrhundert*. Stuttgart: Franz Steiner, 2017.
- ROMBERG, Marion (ed.). *The Language of Continent Allegories in Baroque Central Europe*.
  Stuttgart: Franz Steiner, 2016.
- ROMBERG, Marion. "Continent Allegories in the Baroque Age — A Database". *Journal18*,
  Issue 5 (Coordinates), Spring 2018.

## Próximos passos

- [ ] Mapear 5–10 casos-paradigma (Ripa, Bergmüller, Göz) como precedentes citados no Cap. 3
- [ ] Cruzar códigos Iconclass deles com o schema do corpus (Iconclass 48C51 + continentes)
- [ ] Inserir as 3 obras de Romberg no `references.bib` (skill `zotero-cite`)
- [ ] (Opcional) E-mailar Marion Romberg para acesso/colaboração de dados/imagens

## Conexões

- [[Guia — Obsidian Flavored Markdown]]
- [[corpus-data]]

%% Links externos apenas como Markdown; wikilinks para notas internas. Fonte auditada em 2026-06-24. %%
