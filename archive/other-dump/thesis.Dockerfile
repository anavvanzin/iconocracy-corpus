# thesis — Pandoc + LaTeX for compiling tese (vault/tese/Makefile)
# Build context: repo root. Run: docker compose run --rm thesis make docx
# NOTE: Times New Roman not in Alpine; PDF target may need TeX Gyre Termes substitute.
FROM pandoc/latex:3.5

# pandoc/latex is Alpine-based; provide make and minimal serif fonts
RUN apk add --no-cache make font-noto

WORKDIR /thesis
ENTRYPOINT []
CMD ["make", "docx"]
