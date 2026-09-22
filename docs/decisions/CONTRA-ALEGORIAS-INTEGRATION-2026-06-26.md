# Integração de Contra-Alegorias — 2026-06-26

## Escopo

Triagem do Google Doc **Pesquisa de Contra-Alegorias Jurídicas** contra o estado
atual de `data/processed/records.jsonl`, `vault/candidatos/` e drafts da tese.
O objetivo é evitar duplicação de objetos já cobertos e separar episódios
aproveitáveis de referências fracas.

## Decisão

`§3.4` deve tratar contra-alegoria como disputa do corpo estatal, não como
catálogo amplo de vandalismo. A seção deve receber poucos casos fortes:
Justiça Popular portuguesa, Marianne/Femen, Deborah de Robertis, Marianne/Rude
no Arco do Triunfo e a sequência Ceschiatti/STF. Casos com URL problemática,
alvo alegórico impreciso ou prova apenas jornalística lateral ficam fora do
argumento principal.

Status operacional: decisão metodológica aceita para o sumário da tese. A
próxima etapa é criar candidatos apenas para os casos fortes com fonte visual
ou institucional verificável; os casos em `hold` não entram no argumento sem
novo episódio delimitado.

## Triagem dos 10 casos

- `CONTRA-001`: já coberto. `BR-009` cobre A Justiça de Ceschiatti, e os
  drafts já usam o ataque de 2023. A matéria abre; `image_url` direto retorna
  403. Ação: enriquecer `BR-009`, não criar candidato novo.
- `CONTRA-002`: novo e aproveitável. Migalhas abre e descreve a escultura
  interna de 1975; o relatório STF precisa verificação por navegador. Ação:
  criar candidato separado após confirmar fonte institucional.
- `CONTRA-003`: novo e forte. Episódio francês delimitado: Arco do Triunfo,
  2018, Marianne/Rude mutilada. Ação: promover para `§3.4` e fila de
  candidatos.
- `CONTRA-004`: novo e forte. Performance de Deborah de Robertis tem
  documentação fotográfica AFP/Getty; o Doc usa fontes secundárias fracas.
  Ação: promover como alegoria viva, com fonte visual melhor.
- `CONTRA-005`: já planejado. Draft Max Planck já inclui Marianne/Inna
  Shevchenko. Ação: sincronizar como caso de `§3.4`, sem tratar como descoberta
  nova.
- `CONTRA-006`: hold. Place de la Republique mistura episódios de 2016, 2018,
  Palestina e notícia de 2025. Ação: exigir episódio delimitado antes de
  entrar.
- `CONTRA-007`: hold. ResearchGate retorna 403; Itaú Cultural não prova o
  cartum específico. Ação: buscar Acervo Folha/edição exata.
- `CONTRA-008`: hold. Fontes comprovam vandalismo no tribunal de Portland, mas
  não Lady Justice como alvo visual específico. Ação: só entrar se houver
  imagem/prova do alvo alegórico.
- `CONTRA-009`: já coberto. Continuação da crise Ceschiatti/STF; G1 abre.
  Ação: enriquecer a sequência 2023-2024 de `BR-009`.
- `CONTRA-010`: escopo lateral. HUDOC é forte, mas o alvo é altar/marianismo
  religioso, não alegoria jurídica estatal. Ação: usar como nota sobre
  criminalização do corpo performático, fora do corpus central.

## Patch de tese aplicado

Atualizado o resumo de `§3.4` em:

- `vault/tese/drafts/sumario-iconocracia.md`
- `tese/manuscrito/sumario_iconocracia.md`

## Próximas entradas recomendadas

1. `CONTRA-002` como candidato novo, se o relatório do STF confirmar a peça e o
   episódio com fonte institucional.
2. `CONTRA-003` como candidato novo prioritário.
3. `CONTRA-004` como candidato novo prioritário, com fonte visual Getty/AFP ou
   equivalente arquivável.
