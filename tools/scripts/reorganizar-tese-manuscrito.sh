#!/usr/bin/env bash
# reorganizar-tese-manuscrito.sh
# Fase A (mecânica, segura) da reconciliação do manuscrito ICONOCRACIA.
# Decisões registradas (2026-06-04):
#   - Estrutura: híbrida (front matter + casos)
#   - Lar canônico do manuscrito: tese/manuscrito/
#   - Compile (Makefile + abnt.csl) co-localizado com a prosa viva
#   - Cap2: "mantém ambos" (maio 2937w canônico; longos de abril → drafts/, nada arquivado)
#
# Garantias:
#   - DRY-RUN por padrão. Use --apply para executar de verdade.
#   - NÃO deleta nada. Duplicatas exatas vão para _archive/ datado (reversível).
#   - git mv quando o arquivo é tracked; mv quando untracked. Idempotente (pula ausentes).
#   - Roda validate_schemas.py antes e depois (teste de não-regressão).
#
# Uso:
#   bash tools/scripts/reorganizar-tese-manuscrito.sh            # dry-run
#   bash tools/scripts/reorganizar-tese-manuscrito.sh --apply    # executa

set -u

APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

STAMP="2026-06-04"
ARCHIVE_DIR="_archive/manuscrito-dups-${STAMP}"
HOME_DIR="tese/manuscrito"
DRAFTS_DIR="${HOME_DIR}/drafts"

# --- guards ---------------------------------------------------------------
if [ ! -d ".git" ] || [ ! -f "tools/scripts/validate_schemas.py" ]; then
  echo "ERRO: rode a partir da raiz do repo iconocracy-corpus." >&2
  exit 1
fi

PYBIN="$(command -v python3 || true)"
say()  { printf '%s\n' "$*"; }
run()  { if [ "$APPLY" -eq 1 ]; then eval "$@"; else say "  [dry-run] $*"; fi; }

MOVED=0; ARCHIVED=0; SKIPPED=0

# move <src> <dest>  — git mv se tracked, senão mv; cria dest dir; pula se src ausente
move() {
  local src="$1" dest="$2" destdir
  if [ ! -e "$src" ]; then SKIPPED=$((SKIPPED+1)); say "  skip (ausente): $src"; return; fi
  destdir="$(dirname "$dest")"
  run "mkdir -p \"$destdir\""
  if git ls-files --error-unmatch "$src" >/dev/null 2>&1; then
    run "git mv -f \"$src\" \"$dest\""
  else
    run "mv -f \"$src\" \"$dest\""
  fi
  MOVED=$((MOVED+1)); say "  move: $src -> $dest"
}

# archive <src>  — para _archive/<src> preservando caminho relativo
archive() {
  local src="$1" dest="${ARCHIVE_DIR}/$1"
  if [ ! -e "$src" ]; then SKIPPED=$((SKIPPED+1)); say "  skip (ausente): $src"; return; fi
  run "mkdir -p \"$(dirname "$dest")\""
  if git ls-files --error-unmatch "$src" >/dev/null 2>&1; then
    run "git mv -f \"$src\" \"$dest\""
  else
    run "mv -f \"$src\" \"$dest\""
  fi
  ARCHIVED=$((ARCHIVED+1)); say "  archive: $src"
}

# --- baseline validation --------------------------------------------------
say "== validate_schemas (baseline) =="
if [ -n "$PYBIN" ]; then "$PYBIN" tools/scripts/validate_schemas.py >/tmp/val_before.txt 2>&1 && say "  OK" || say "  AVISO: validação baseline retornou erro (ver /tmp/val_before.txt)"; fi

say ""; say "== modo: $( [ "$APPLY" -eq 1 ] && echo APPLY || echo DRY-RUN ) =="
run "mkdir -p \"$DRAFTS_DIR\" \"$ARCHIVE_DIR\""

# --- 1. preservar ÚNICOS (drafts) ----------------------------------------
say ""; say "== 1. preservar prosa única -> $DRAFTS_DIR =="
move "vault/tese/metodologia/capitulo-2-reescrito.md" "$DRAFTS_DIR/Capitulo2_metodologia-reescrito-7961w.md"
move "vault/tese/metodologia/capitulo-2-imes.md"      "$DRAFTS_DIR/Capitulo2_metodologia-imes-6713w.md"
move "Text/capitulo-2-reescrito.md"                   "$DRAFTS_DIR/Capitulo2_metodologia-reescrito-Text-3852w.md"
move "Text/Capitulo2_metodologia.md"                  "$DRAFTS_DIR/Capitulo2_metodologia-variante-Text-2901w.md"
move "vault/tese/drafts/capitulo-3-secao-3.2-DRAFT.md" "$DRAFTS_DIR/Capitulo3-secao-3.2-DRAFT.md"
move "vault/tese/drafts/capitulo-3-secao-3.3-DRAFT.md" "$DRAFTS_DIR/Capitulo3-secao-3.3-DRAFT.md"
move "vault/tese/capitulo-5.md"                        "$DRAFTS_DIR/capitulo-5-draft-1003w.md"
move "Text/Introducao_rev.md"                          "$DRAFTS_DIR/Introducao_rev-variante-Text-5318w.md"
# capítulos com conteúdo (caso?) — manter 1 cópia canônica em drafts
move "vault/tese/capitulo-2.md"                        "$DRAFTS_DIR/capitulo-2-draft-1590w.md"
move "vault/tese/capitulo-6.md"                        "$DRAFTS_DIR/capitulo-6-draft-1476w.md"
move "vault/tese/capitulo-6-sessao-2026-04-17.md"      "$DRAFTS_DIR/capitulo-6-sessao-2981w.md"
move "vault/tese/conclusao.md"                         "$HOME_DIR/conclusao.md"

# --- 2. compile harness co-localizado ------------------------------------
say ""; say "== 2. mover harness de compile -> $HOME_DIR =="
move "vault/tese/abnt.csl" "$HOME_DIR/abnt.csl"
# Makefile antigo (lista stubs) -> arquivar; novo será escrito abaixo
archive "vault/tese/Makefile"

# --- 3. arquivar DUPLICATAS EXATAS (mesmo md5) ---------------------------
say ""; say "== 3. arquivar duplicatas exatas -> $ARCHIVE_DIR =="
for f in \
  "Text/Capitulo1_rev.md" \
  "Text/Capitulo1_original_v2.md" \
  "Text/Introducao_original_v2.md" \
  "wiki/tese/conclusao.md" \
  "Text/conclusao (2).md" \
  "wiki/tese/introducao.md" \
  "Text/introducao (2).md" \
  "vault/tese/introducao.md" \
  "wiki/tese/drafts/sumario-iconocracia.md" \
  "Text/sumario-iconocracia.md" \
  "vault/tese/drafts/sumario-iconocracia.md" \
  "Text/sumario_iconocracia (2).md" \
  "Text/sumario_iconocracia.md" \
  "wiki/tese/capitulo-2.md" \
  "Text/capitulo-2 (2).md" \
  "wiki/tese/capitulo-6.md" \
  "Text/capitulo-6 (2).md" \
  "wiki/tese/capitulo-6-sessao-2026-04-17.md" \
  "Text/capitulo-6-sessao-2026-04-17 (2).md" \
  "Text/capitulo-1 (2).md" \
  "vault/tese/capitulo-1.md" \
  "Text/capitulo-3 (2).md" \
  "vault/tese/capitulo-3.md" \
  "Text/capitulo-4 (2).md" \
  "vault/tese/capitulo-4.md" \
  "Text/capitulo-5 (2).md" \
  "wiki/tese/capitulo-5.md" \
  "Text/capitulo-7 (2).md" \
  "vault/tese/capitulo-7.md" \
  "Text/capitulo-8 (2).md" \
  "vault/tese/capitulo-8.md" \
  "Text/capitulo-9 (2).md" \
  "wiki/tese/capitulo-9.md" \
  "vault/tese/capitulo-9.md" \
  "vault/tese/_sumario.md" \
; do
  archive "$f"
done

# --- 4. novo Makefile apontando pra prosa viva ---------------------------
say ""; say "== 4. instalar Makefile corrigido em $HOME_DIR =="
if [ "$APPLY" -eq 1 ]; then
  cat > "$HOME_DIR/Makefile" <<'MAKEFILE_EOF'
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
PANDOC_DOCX = $(PANDOC_COMMON) --reference-doc=$(REF_DOC)
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
MAKEFILE_EOF
  git add "$HOME_DIR/Makefile" 2>/dev/null || true
  say "  escrito: $HOME_DIR/Makefile"
else
  say "  [dry-run] escreveria $HOME_DIR/Makefile (CHAPTERS = prosa viva)"
fi

# --- 5. validação pós ----------------------------------------------------
say ""; say "== validate_schemas (após) =="
if [ -n "$PYBIN" ]; then "$PYBIN" tools/scripts/validate_schemas.py >/tmp/val_after.txt 2>&1 && say "  OK" || say "  AVISO: validação pós retornou erro (ver /tmp/val_after.txt)"; fi

# --- resumo --------------------------------------------------------------
say ""; say "== RESUMO =="
say "  movidos:   $MOVED"
say "  arquivados:$ARCHIVED"
say "  pulados:   $SKIPPED"
if [ "$APPLY" -eq 0 ]; then
  say ""; say "Isto foi um DRY-RUN. Revise acima e rode com --apply para executar."
  say "Depois: cd $HOME_DIR && make docx   # compila a prosa viva"
else
  say ""; say "Feito. Próximo: cd $HOME_DIR && make docx  e revise o PDF/DOCX."
  say "Commit sugerido: git add -A && git commit -m \"refactor(tese): unifica manuscrito em tese/manuscrito, corrige compile, arquiva duplicatas\""
fi
