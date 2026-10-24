# Makefile para compilação da tese via Pandoc
#
# Uso:
#   make docx          — compila todos os capítulos em tese_completa.docx
#   make pdf           — compila todos os capítulos em tese_completa.pdf (requer LaTeX)
#   make capitulo-1.docx — compila capítulo individual
#   make clean         — remove artefatos de compilação

.DEFAULT_GOAL := docx

PANDOC = pandoc
CSL = abnt.csl
BIB = references.bib
META = metadata.yaml
REF_DOC = template.docx
OUTPUT_DIR = output

# Numeração editorial nas fontes; não acrescentar --number-sections.
# Fontes canônicas, na ordem de leitura da tese.
CHAPTER_FILES = ../../tese/manuscrito/Capitulo1_rev.md \
           ../../tese/manuscrito/Capitulo2_iconocracia.md \
           ../../tese/manuscrito/Capitulo3_colonialidade.md \
           ../../tese/manuscrito/Capitulo4_metodologia.md \
           ../../tese/manuscrito/Capitulo5_corpus.md \
           ../../tese/manuscrito/Capitulo6_analise_quantitativa.md \
           ../../tese/manuscrito/Capitulo7_analise_qualitativa.md \
           ../../tese/manuscrito/Capitulo8_atlas_principios.md \
           ../../tese/manuscrito/Capitulo9_paineis_atlas.md

CHAPTERS = ../../tese/manuscrito/Introducao_rev.md $(CHAPTER_FILES) ../../tese/manuscrito/Conclusao.md

PANDOC_COMMON = --citeproc \
                --toc \
                --toc-depth=3 \
                --metadata lang=pt-BR \
                --metadata title="Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"

PANDOC_DOCX = $(PANDOC_COMMON) \
              --reference-doc=$(REF_DOC)

PDF_ENGINE = lualatex
PDF_FONT = TeX Gyre Termes

PANDOC_PDF = $(PANDOC_COMMON) \
             --pdf-engine=$(PDF_ENGINE) \
             -V geometry:margin=3cm \
             -V fontsize=12pt \
             -V documentclass=report \
             -V mainfont="$(PDF_FONT)"

# Adicionar CSL e metadata.yaml apenas se existirem
ifneq (,$(wildcard $(CSL)))
  PANDOC_COMMON += --csl=$(CSL)
endif
ifneq (,$(wildcard $(META)))
  PANDOC_COMMON += --metadata-file=$(META)
endif

# A bibliografia é obrigatória. Sem ela o --citeproc emite citações cruas e o
# build termina com sucesso, entregando um .docx com referências não formatadas.
# Por isso --bibliography é sempre passado e o alvo docx/pdf depende de bib-check.
PANDOC_COMMON += --bibliography=$(BIB)

.PHONY: bib-check
bib-check:
	@test -f $(BIB) || { echo "ERRO: $(BIB) não encontrado em $(CURDIR) — a bibliografia é obrigatória para o build ABNT." >&2; exit 1; }

.PHONY: docx pdf clean setup bib-check

all: docx

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Tese completa
docx: bib-check $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/tese_completa.docx $(CHAPTERS)
	cp $(OUTPUT_DIR)/tese_completa.docx ../../tese/tese_completa.docx
	@echo "✅ $(OUTPUT_DIR)/tese_completa.docx"
	@echo "✅ ../../tese/tese_completa.docx"

pdf: bib-check $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/tese_completa.pdf $(CHAPTERS)
	cp $(OUTPUT_DIR)/tese_completa.pdf ../../tese/tese_completa.pdf
	@echo "✅ $(OUTPUT_DIR)/tese_completa.pdf"
	@echo "✅ ../../tese/tese_completa.pdf"

# Capítulos individuais usam as mesmas fontes da tese completa.
capitulo-%.docx: bib-check | $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/$@ $(word $*,$(CHAPTER_FILES))
	@echo "✅ $(OUTPUT_DIR)/$@"

capitulo-%.pdf: bib-check | $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/$@ $(word $*,$(CHAPTER_FILES))
	@echo "✅ $(OUTPUT_DIR)/$@"

# Setup: baixar CSL ABNT e criar template
setup:
	@echo "Para configurar:"
	@echo "  1. Baixe abnt.csl de https://github.com/citation-style-language/styles"
	@echo "  2. Crie references.bib com suas referências"
	@echo "  3. Mantenha template.docx com estilos ABNT"
	@echo "  4. Execute: make docx"

clean:
	rm -rf $(OUTPUT_DIR)
	@echo "🧹 Artefatos removidos"
