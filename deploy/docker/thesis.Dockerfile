# thesis — Pandoc + LaTeX for compiling tese (vault/tese/Makefile)
# Build context: repo root. Run: docker compose run --rm thesis make docx
# PDF requires LuaLaTeX and TeX Gyre Termes (see vault/tese/README.md).
FROM pandoc/latex:3.5

# pandoc/latex is Alpine-based; provide make and minimal serif fonts
RUN apk add --no-cache make font-noto

WORKDIR /workspace/vault/tese
ENTRYPOINT []
CMD ["make", "docx"]
