# ICONOCRACIA-CV

Aplicação da disciplina **INE410159 / TRV410001 — Visão Computacional
(2026.2)**, UFSC, Profs. Aldo von Wangenheim e Antonio Sobieranski.

- Página pública: <https://iconocracia-cv.pages.dev/>.
- OpenAI Sites: <https://iconocracia-cv.iconocracia-5216.chatgpt.site>.
- Freeze: [`../../output/huggingface/ICONOCRACIA-CV-2026-08-12/`](../../output/huggingface/ICONOCRACIA-CV-2026-08-12/).
- Pitch: [`../../docs/apresentacao-visao-computacional-2026-2.md`](../../docs/apresentacao-visao-computacional-2026-2.md).
- Protocolo técnico: [`../../docs/projeto-disciplina-visao-computacional-2026-2.md`](../../docs/projeto-disciplina-visao-computacional-2026-2.md).
- Auditoria de cobertura: [`../../docs/research/huggingface/regime-coverage-2026-08-13/`](../../docs/research/huggingface/regime-coverage-2026-08-13/).

## Fronteira desta aplicação

Esta pasta contém somente a superfície de apresentação e seus adaptadores de
deploy. Os dados e documentos canônicos permanecem nas áreas próprias do
monorepo e são lidos dali durante o build.

```text
deploy/iconocracia-cv/
├── site/          página estática
├── public/        imagem social
├── scripts/       build do Worker para OpenAI Sites
└── supabase/      registro e lotes da carga inicial do freeze
```

## Build

```bash
cd deploy/iconocracia-cv
npm run build
```

O build produz `dist/server/index.js` com a página e os artefatos públicos
necessários. O freeze completo não é incorporado ao Worker.
