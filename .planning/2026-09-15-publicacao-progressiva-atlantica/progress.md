# Progresso

## 2026-09-15

- Plano de implementação aprovado pela responsável.
- Repositórios e worktree confirmados.
- Estado preexistente inventariado sem sobrescrever alterações.
- Criados os três arquivos persistentes de planejamento.
- Erro de exploração registrado: um comando Python inline falhou por conflito
  de aspas dentro de uma f-string; foi repetido com quoting seguro e não alterou
  arquivos.
- `SCOUT-625` promovido isoladamente pelo fluxo `vault_sync.py --item`, com ID
  canônico `324a90b6-403b-5b36-9bcf-d4c4db9efdc1`.
- Original fornecido armazenado na pasta sincronizada `Corpus Digital`, com
  caminho e SHA-256 registrados em `drive-manifest.json`.
- `BE-004` e `SCOUT-625` formalizados como `coded_by: ana`, sem novo composto.
- Ledger e export sincronizados com 336 registros; schemas válidos.
- Ficha comparativa das seis análises pendentes criada para adjudicação.
- No site, manifesto editorial migra os 95 itens e mantém os oito novos em
  `review`; geração de produção resulta em 95 e prévia em 103.
- Rota de constelação, contexto no acervo, análise expansível, aliases e total
  dinâmico implementados.
- Navegador real: 1440 e 390 px sem overflow; overflow de menu encontrado em
  320 px e corrigido. URL legada `FR-007` redireciona ao UUID canônico.

## Validações pendentes

- Corpus: lint Markdown e CI remoto do PR.
- Site: nova passagem em 320 px após a correção, idempotência final com o SHA
  do corpus integrado e CI remoto.
- Produção: deploy e verificação direta de iconocracia.com.

## Incidentes de implementação

- Uma tentativa de `apply_patch` que combinava remoção e recriação do mesmo
  arquivo foi rejeitada pelo executor. Nenhum arquivo foi alterado nessa
  tentativa; a operação foi refeita em duas etapas verificáveis.
