# Makefile para compilação da tese via Pandoc
#
# Uso:
#   make docx          — compila todos os capítulos em tese_completa.docx
#   make pdf           — compila todos os capítulos em tese_completa.pdf (requer LaTeX)
#   make capitulo-1.docx — compila capítulo individual
#   make clean         — remove artefatos de compilação

PANDOC = pandoc
CSL = abnt.csl
BIB = references.bib
META = metadata.yaml
REF_DOC = template.docx
OUTPUT_DIR = output

# Ordem dos capítulos na tese
CHAPTERS = ../../tese/manuscrito/Introducao_rev.md \
           ../../tese/manuscrito/Capitulo1_rev.md \
           ../../tese/manuscrito/Capitulo2_iconocracia.md \
           ../../tese/manuscrito/Capitulo3_colonialidade.md \
           ../../tese/manuscrito/Capitulo4_metodologia.md \
           ../../tese/manuscrito/Capitulo5_corpus.md \
           ../../tese/manuscrito/Capitulo6_analise_quantitativa.md \
           ../../tese/manuscrito/Capitulo7_analise_qualitativa.md \
           ../../tese/manuscrito/Capitulo8_atlas_principios.md \
           ../../tese/manuscrito/Capitulo9_paineis_atlas.md \
           ../../tese/manuscrito/Conclusao.md

PANDOC_COMMON = --citeproc \
                --number-sections \
                --toc \
                --toc-depth=3 \
                --metadata lang=pt-BR \
                --metadata title="Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"

PANDOC_DOCX = $(PANDOC_COMMON) \
              --reference-doc=$(REF_DOC)

PANDOC_PDF = $(PANDOC_COMMON) \
             -V geometry:margin=3cm \
             -V fontsize=12pt \
             -V documentclass=report \
             -V mainfont="Times New Roman"

# Adicionar CSL, BIB e metadata.yaml apenas se existirem
ifneq (,$(wildcard $(CSL)))
  PANDOC_COMMON += --csl=$(CSL)
endif
ifneq (,$(wildcard $(BIB)))
  PANDOC_COMMON += --bibliography=$(BIB)
endif
ifneq (,$(wildcard $(META)))
  PANDOC_COMMON += --metadata-file=$(META)
endif

.PHONY: docx pdf clean setup

all: docx

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Tese completa
docx: $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/tese_completa.docx $(CHAPTERS)
	cp $(OUTPUT_DIR)/tese_completa.docx ../../tese/tese_completa.docx
	@echo "✅ $(OUTPUT_DIR)/tese_completa.docx"
	@echo "✅ ../../tese/tese_completa.docx"

pdf: $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/tese_completa.pdf $(CHAPTERS)
	cp $(OUTPUT_DIR)/tese_completa.pdf ../../tese/tese_completa.pdf
	@echo "✅ $(OUTPUT_DIR)/tese_completa.pdf"
	@echo "✅ ../../tese/tese_completa.pdf"

# Capítulos individuais
%.docx: %.md $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/$@ $<
	@echo "✅ $(OUTPUT_DIR)/$@"

%.pdf: %.md $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/$@ $<
	@echo "✅ $(OUTPUT_DIR)/$@"

# Setup: baixar CSL ABNT e criar template
setup:
	@echo "Para configurar:"
	@echo "  1. Baixe abnt.csl de https://github.com/citation-style-language/styles"
	@echo "  2. Crie references.bib com suas referências"
	@echo "  3. (Opcional) Crie template.docx com estilos ABNT"
	@echo "  4. Execute: make docx"

clean:
	rm -rf $(OUTPUT_DIR)
	@echo "🧹 Artefatos removidos"
