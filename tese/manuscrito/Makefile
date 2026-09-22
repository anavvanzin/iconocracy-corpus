# Makefile — compilação da tese ICONOCRACIA (Pandoc)
# Capítulos = prosa viva real (estrutura híbrida). Estenda CHAPTERS ao slotar casos.
PANDOC = pandoc
CSL = abnt.csl
BIB = references.bib
META = metadata.yaml
REF_DOC = template.docx
OUTPUT_DIR = output

CHAPTERS = Introducao_rev.md \
           Capitulo1_rev.md \
           Capitulo2_metodologia.md \
           Capitulo3_analise_quantitativa.md \
           conclusao.md

PANDOC_COMMON = --citeproc --number-sections --toc --toc-depth=3 \
                --metadata lang=pt-BR \
                --metadata title="Iconocracia: Alegoria Feminina na Historia da Cultura Juridica (Seculos XIX-XX)"
PANDOC_DOCX = $(PANDOC_COMMON) $(REF_DOC_FLAG)
PANDOC_PDF  = $(PANDOC_COMMON) -V geometry:margin=3cm -V fontsize=12pt -V documentclass=report -V mainfont="Times New Roman"

ifneq (,$(wildcard $(CSL)))
  PANDOC_COMMON += --csl=$(CSL)
endif
ifneq (,$(wildcard $(BIB)))
  PANDOC_COMMON += --bibliography=$(BIB)
endif
ifneq (,$(wildcard $(META)))
  PANDOC_COMMON += --metadata-file=$(META)
endif
ifneq (,$(wildcard $(REF_DOC)))
  REF_DOC_FLAG = --reference-doc=$(REF_DOC)
endif

.PHONY: docx pdf clean
all: docx
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)
docx: $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/tese_completa.docx $(CHAPTERS)
	@echo "OK $(OUTPUT_DIR)/tese_completa.docx"
pdf: $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/tese_completa.pdf $(CHAPTERS)
	@echo "OK $(OUTPUT_DIR)/tese_completa.pdf"
%.docx: %.md $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_DOCX) -o $(OUTPUT_DIR)/$@ $<
%.pdf: %.md $(OUTPUT_DIR)
	$(PANDOC) $(PANDOC_PDF) -o $(OUTPUT_DIR)/$@ $<
clean:
	rm -rf $(OUTPUT_DIR)
