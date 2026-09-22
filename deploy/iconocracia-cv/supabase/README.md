# Supabase — ICONOCRACIA 1.0

Projeto: `gcuxtaohtoomweyrgpgk` (us-east-1, free) ·
[Supabase](https://gcuxtaohtoomweyrgpgk.supabase.co)

- Tabela `public.corpus_items` — freeze ICONOCRACIA-CV-2026-08-12 (335 registros)
- RLS: leitura pública (anon), escrita bloqueada
- `year` é derivado do campo `date` (primeiro ano 1400–2099); 42 registros
  não têm ano derivável.
- `seed/batch-*.json` — lotes usados na carga inicial via PostgREST
  (`POST /rest/v1/corpus_items`).

Chave pública (read-only por RLS): variável `SUPABASE_KEY` com a chave
publicável do projeto.
