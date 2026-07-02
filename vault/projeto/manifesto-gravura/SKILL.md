---
name: manifesto-gravura
description: >
  Transforma um texto longo (manifesto, ensaio, capítulo, memorial, apresentação
  de projeto) mais um conjunto de ilustrações numa página HTML autônoma e
  hospedável, na estética de gravura editorial: papel creme, tinta sépia, vermelho
  oxblood, serifas Cormorant/EB Garamond, capitulares, pranchas de figuras com
  legendas e cartões de "ficha técnica". Aceita como fonte um PDF (ex.: export do
  Claude Design) do qual extrai o texto e as imagens embutidas, ou markdown/texto
  solto acompanhado de uma pasta de imagens. Use sempre que Ana pedir para
  "virar o manifesto em site/HTML", "usar as ilustrações que enviei", "fazer a
  página na estética de gravura", "montar o frontispício", "transformar o PDF do
  manifesto numa página", ou quando quiser dar forma editorial a prosa acadêmica
  já escrita usando iconografia real (moedas, selos, gravuras, esculturas). NÃO
  reescreve o texto da autora — preserva a voz e a prosa; NÃO inventa legendas nem
  fabrica atribuições de imagem.
---

# manifesto-gravura

Dá forma de **gravura editorial** a um texto longo já escrito, usando ilustrações
reais. O resultado é um `index.html` autônomo (mais uma pasta `images/`) que Ana
pode abrir localmente, guardar no vault ou hospedar (ex.: anavanzin.com).

Nasceu do manifesto ICONOCRACIA (frontispício em gravura + corpus histórico:
Ceres, Britannia, Seated Liberty, série Educational, Marianne de Rops, moeda da
República, Justiça do STF, monumento do Congo, Bruegel, Esslingen).

## Princípios (não-negociáveis)

- **Preservar a voz.** O corpo do texto é da autora. Copie a prosa verbatim; não
  reescreva para caber no template. Travessões e escolhas dela permanecem.
- **Sem fabricação.** Legenda e atribuição de cada imagem saem do texto-fonte ou
  de metadado confirmado. Se a identidade de uma imagem for incerta, use legenda
  neutra ("Estatuária alegórica") em vez de arriscar data/autor errados.
- **Imagens de uso livre ou da autora.** Domínio público (corpus histórico) ou
  ilustrações próprias. Registre a procedência no colofão do rodapé.
- **Cena de cor fixa.** A paleta é hardcoded de propósito; a página não inverte em
  dark mode.

## Fluxo

1. **Reunir a fonte.**
   - Se for um **PDF** (ex.: export de design): rode
     `scripts/extract-illustrations.sh <arquivo.pdf> <pasta-trabalho>`.
     Ele gera `raw/` (imagens cruas), `images/` (otimizadas), `texto.txt` (a prosa)
     e `contact.png` (mosaico rotulado).
   - Se já houver **markdown/texto + pasta de imagens**: rode o mesmo script
     apontando para a pasta de imagens (ele só otimiza + faz o contato).
   - Dependências: `poppler-utils` + ImageMagick. Em macOS o binário pode ser
     `magick` (v7) ou `convert` (v6) — o script detecta.

2. **Mapear imagem → seção.** Abra `contact.png` (ou use a ferramenta de leitura de
   imagem) e case cada figura com o trecho do texto que a menciona. Renomeie os
   `images/img-NN.jpg` para nomes semânticos (`hero.jpg`, `fr-ceres.jpg`, …).
   Confirme identidades ambíguas antes de escrever a legenda.

3. **Estruturar a prosa.** Separe: título + subtítulo; frontispício (1 imagem +
   legenda); seções numeradas (I, II, …); blocos conceituais numerados (opcional);
   pranchas de figuras por tema/família; frases de destaque (`blockquote`);
   cartões de ficha técnica (dados: corpus, indicadores, estatística…).

4. **Montar o HTML.** Parta de `assets/template.html` e `assets/manifesto.css`.
   - Para página **100% autônoma**, embuta o CSS num `<style>` em vez do `<link>`.
   - Padrões de prancha: `.plates.p2` (2 col), `.plates.p3` (3 col),
     `.plates.solo` (1 figura). Cada figura: `figure > .imgbox > img` + `figcaption`.
   - Rótulo de faixa entre pranchas: `<div class="regime"><span>País · regime</span></div>`.
   - Primeiro parágrafo de seção recebe capitular: classe `.lead`.
   - Legendas curtas em itálico; termos estrangeiros em `.foreign`.

5. **Verificar e entregar.** Abra o `index.html` no navegador (Playwright/Chrome),
   confira que as fontes do Google carregam, que toda `img` aparece e que as
   pranchas não quebram no mobile. Salve `index.html` + `images/` juntos (caminhos
   relativos) e apresente o `index.html`.

## Especificação estética (resumo — detalhes em `assets/manifesto.css`)

| Item | Valor |
| --- | --- |
| Papel | `#f4ecd9` (fundo), `#efe6d0` (cartões/imgbox) |
| Tinta | `#2a2622` (texto), `#5d5446` (secundário) |
| Vermelho oxblood | `#9c2b22` (acento), `#7d201c` (citação) |
| Filetes | `#cebf9d` |
| Display | Cormorant Garamond (título, legenda, citação) |
| Corpo | EB Garamond, 19px, entrelinha 1.78 |
| Colunas | `.frame` ≤940px; `.wrap` de texto ≤740px |

Fontes via Google Fonts (`fonts.googleapis.com`). Fallback serif embutido no
stack, então a página degrada bem offline.

## Otimização de imagem (receita)

```
convert ORIG.png -strip -colorspace sRGB -resize '1600x>' -quality 84 SAIDA.jpg
```
Moedas/selos ~600px de largura, cédulas/gravuras largas ~900–1000px, esculturas
altas ~700px, herói do frontispício ~1600px. Alvo total da pasta `images/`: 1–2 MB.

## Anti-exemplos (quando NÃO usar)

- UI de app / site responsivo com estado e navegação → `frontend-design`.
- Slides/pôster/póster acadêmico → skills de pptx/latex-posters.
- Escrever ou revisar o texto em si → `iconocracia-reviewer` / `academic-*`.
  Esta skill só **diagrama** prosa pronta.

## Arquivos

- `assets/manifesto.css` — folha de estilo completa.
- `assets/template.html` — esqueleto com placeholders `{{…}}`.
- `scripts/extract-illustrations.sh` — extração + otimização + contato.
