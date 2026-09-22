# Reconciliação metodológica para as fichas citáveis

Data: 2026-09-16. Estado: levantamento documental; deliberação autoral pendente.

Este documento registra a aplicação do plano mestre de registros confiáveis.
Não aprova o LPAI v3 nem recodifica os registros. A data mais recente de um
arquivo ou de uma interface não constitui autoridade conceitual.

## Matriz de autoridade e divergências

| Tema | Decisão/documento vigente | Proposta | Implementação existente | Apresentação pública | Encaminhamento |
| --- | --- | --- | --- | --- | --- |
| Escala | `METHOD_CONTRACT_2026-07-31.md`: 0–3, proibição expressa de 0–4 nos textos finais | Plano LPAI v3 ainda em deliberação | Schema canônico limita os dez indicadores a 0–3 | Site apresenta 0–4 | Corrigir a apresentação depois da revisão; preservar valores, sem conversão automática |
| Composto | Decisão de 2026-07-28: aposentado, valores históricos congelados | Nenhuma reativação aprovada identificada | Schema marca `purificacao_composto` como deprecated; builder HF ainda calcula média | Site descreve indicadores sem média | Retirar o cálculo de novas médias do caminho de publicação; manter os dados anteriores recuperáveis |
| Regimes | Decisão de 2026-07-31 conserva três regimes; contra-alegorias como teste crítico | Não foi localizada decisão que transforme o teste crítico em quarto regime equivalente | Schema aceita também `contra-alegoria` | Quatro categorias no site | Deliberação autoral necessária sobre estatuto e apresentação; não reclassificar automaticamente |
| Recorte | Contrato de 2026-07-31: 1800–2000 | Plano de transição não resolve por si a inclusão histórica | Ledger contém referências anteriores a 1800 | Galeria inclui essas referências | Deliberação autoral sobre corpus central e referências genealógicas |
| Rigor | Decisão de 2026-07-31 dispensa coeficientes intercodificador como requisito | LPAI v3 propõe revisão por afirmação | Dados legados nem sempre distinguem ausência e zero | Ficha pública pode sugerir completude | Exigir fonte consultada e revisão efetiva, sem impor concordância mecânica |
| Publicação | Plano mestre aprovado pela autora: fichas completas conforme tipo | Extensão técnica `publication` versão 1.0.0 em implementação | Schema opcional, validador de elegibilidade e testes novos | Ainda não implantada | Revisão dos casos precede promoção; `draft`, `review`, `published`, `archived` preservados |

## Fontes locais confrontadas

- [Contrato vigente](../METHOD_CONTRACT_2026-07-31.md).
- [Aposentadoria do composto](../decisions/2026-07-28-aposentadoria-do-indice-composto.md).
- [Consolidação metodológica](../decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md).
- [Integração das contra-alegorias](../decisions/CONTRA-ALEGORIAS-INTEGRATION-2026-06-26.md).
- [Plano LPAI v3, ainda proposta](plano-mestre-transicao-lpai-v3.md).
- Schema: `tools/schemas/master-record.schema.json`.
- Publicação HF: `tools/scripts/build_hf_release.py`.
- Site inspecionado: checkout `imagens-records-citable`, base
  `4199cff45c60d31a1cce758aac1a19ea024e08b0`.

## Migração técnica compatível

1. Acrescentar `publication` opcional ao ledger. Ausência desse objeto não é
   erro estrutural no corpus de trabalho e impede elegibilidade pública.
2. Manter UUID e campos legados. A revisão prepara metadados documentados
   separados; mudanças por campo exigem valor anterior, proposto, fontes,
   responsável, motivo e data ISO 8601 com fuso horário.
3. Vincular revisão a um hash do conteúdo efetivamente revisado. Alteração em
   fatos, fontes, método ou codificação invalida a revisão anterior.
4. Resolver aliases por superfície, nunca por substituição global de códigos.
   URLs compartilhadas continuam sendo candidatos à conferência de identidade.
5. Publicar apenas após implementar e testar exportação e consumidores comuns.
   Os 15 testes atuais verificam o contrato e a busca de vínculos, sem certificar
   fontes, imagens ou aprovação autoral.

## Deliberação pendente

Foi enviada à autora a escolha entre separar referências genealógicas/casos
críticos, ampliar documentalmente o contrato ou limitar a release ao recorte
vigente. A ausência de resposta não fecha esta etapa. A recodificação permanece
suspensa; identidade, fontes e infraestrutura podem avançar.
