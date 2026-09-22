#!/usr/bin/env bash
# extract-illustrations.sh — extrai imagens de um PDF (ou converte uma pasta de
# imagens) e otimiza para web na estética do manifesto-gravura.
#
# Dependências: poppler-utils (pdfimages, pdftotext) e ImageMagick (convert/montage).
#   macOS:  brew install poppler imagemagick
#   Debian: apt install poppler-utils imagemagick
# Nota: ImageMagick 7 usa `magick`; a v6 usa `convert`/`montage`/`identify`.
#       Este script detecta qual existe.
#
# Uso:
#   ./extract-illustrations.sh <origem.pdf|pasta-de-imagens> <pasta-saida>
#
# Saídas em <pasta-saida>:
#   raw/            imagens extraídas cruas (só no modo PDF)
#   images/         versões otimizadas para web (jpg)
#   contact.png     mosaico rotulado para você mapear cada imagem à seção
#   texto.txt       texto do PDF (só no modo PDF), para reaproveitar a prosa
set -u

SRC="${1:?origem (PDF ou pasta de imagens) obrigatória}"
OUT="${2:?pasta de saída obrigatória}"

# resolve binário do ImageMagick
if command -v magick >/dev/null 2>&1; then IM="magick"; MONTAGE="magick montage"; IDENT="magick identify"
elif command -v convert >/dev/null 2>&1; then IM="convert"; MONTAGE="montage"; IDENT="identify"
else echo "ERRO: ImageMagick não encontrado (magick/convert)."; exit 1; fi

mkdir -p "$OUT/images"

if [ -f "$SRC" ] && printf '%s' "$SRC" | grep -qiE '\.pdf$'; then
  command -v pdfimages >/dev/null 2>&1 || { echo "ERRO: pdfimages (poppler) não encontrado."; exit 1; }
  mkdir -p "$OUT/raw"
  echo "» extraindo imagens do PDF…"
  pdfimages -all "$SRC" "$OUT/raw/img"
  command -v pdftotext >/dev/null 2>&1 && pdftotext -layout "$SRC" "$OUT/texto.txt" && echo "» texto salvo em texto.txt"
  SRCDIR="$OUT/raw"
else
  SRCDIR="$SRC"   # pasta de imagens já existente
fi

echo "» otimizando para web (max 1600px, qualidade 84)…"
i=0
for f in "$SRCDIR"/*; do
  case "$f" in *.png|*.jpg|*.jpeg|*.tif|*.tiff|*.PNG|*.JPG|*.JPEG) ;; *) continue ;; esac
  base=$(printf 'img-%02d' "$i")
  $IM "$f" -strip -colorspace sRGB -resize '1600x>' -quality 84 "$OUT/images/$base.jpg" 2>/dev/null
  i=$((i+1))
done
echo "» $i imagens otimizadas em $OUT/images/"

echo "» gerando contato rotulado…"
$MONTAGE "$OUT/images"/*.jpg -tile 4x -geometry 320x320+8+8 \
  -background '#f4ecd9' -label '%f %wx%h' "$OUT/contact.png" 2>/dev/null \
  && echo "» contact.png pronto — abra para mapear cada imagem à seção/legenda."

echo
echo "Próximo passo: renomeie os images/img-NN.jpg para nomes semânticos"
echo "(ex.: hero.jpg, fr-ceres.jpg) e referencie no HTML a partir do template."
