# Publicação do dashboard

## Produção

- Plataforma: Cloudflare Pages (projeto `iconocracia-corpus`, conta warholana@msn.com).
- URL principal: <https://dashboard.iconocracia.com/>
- URL Pages: <https://iconocracia-corpus.pages.dev/>
- Primeira publicação: 2026-08-14.
- Fonte versionada: `corpus/DASHBOARD_CORPUS.html` (publicado como `index.html`).

A versão antiga na Vercel (`iconocracy-corpus.vercel.app`) está congelada em
jun/2026 e não é mais mantida.

## Republicar

```bash
# 1. Regenerar o bloco de dados (idempotente)
python tools/scripts/refresh_dashboard.py --corpus

# 2. Deploy (Wrangler autenticado)
publish_dir="$(mktemp -d)"
cp corpus/DASHBOARD_CORPUS.html "$publish_dir/index.html"
npx wrangler pages deploy "$publish_dir" \
  --project-name iconocracia-corpus \
  --branch main
rm -rf "$publish_dir"
```

## DNS / rotas (iconocracia.com)

- `dashboard.iconocracia.com` → CNAME para `iconocracia-corpus.pages.dev` (proxied).
- O Worker `iconocracia` (Mnemosyne Viva) usa rotas específicas
  `api.iconocracia.com/*` e `www.iconocracia.com/*` — **não** recriar a rota
  coringa `*.iconocracia.com`, que capturaria o subdomínio do dashboard
  (incidente de 2026-08-14).
