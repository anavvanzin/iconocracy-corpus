# Imagens dos casos

**As imagens reais já estão embutidas** nos slides de caso (domínio público, redimensionadas
para projeção, em `assets/`):

| Slide | Imagem | Proveniência |
|---|---|---|
| 11 — Contrato Racial Visual | `villares-republica.jpg` · `congo-100f-1912.jpg` | corpus ICONOCRACIA |
| 18 — Bélgica 1848 (lado francês) | `moitte-liberte-1792.jpg` | corpus ICONOCRACIA |
| 19 — Marianne | `delacroix-liberte.jpg` · `marianne-busto.jpg` | Wikimedia Commons |
| 21 — Contra-alegoria | `gill-anastasie.jpg` · `nast-liberty.jpg` · `keppler-looking-backward.jpg` | Wikimedia Commons |

O lado **belga** do slide 18 (Meganck, 1848) segue como placa tipográfica — não há boa fonte em
domínio público localizada. Para **trocar ou adicionar** qualquer imagem, use a tabela de referência
abaixo. Todas as obras são de **domínio público** (autor falecido há mais de 70 anos / anterior a 1928).
Mantenha imagens em `assets/` — nunca em `data/raw/` (ADR-001).

## Como trocar uma placa por uma foto (2 min)

1. Baixe a imagem e salve em `assets/` com o nome sugerido (ex.: `assets/delacroix-liberte.jpg`).
2. No `index.html`, encontre o slide do caso e **substitua** o bloco
   `<div class="visual">…</div>` por:
   ```html
   <div class="visual" style="padding:0">
     <img class="plate-img" src="assets/delacroix-liberte.jpg"
          alt="Delacroix — A Liberdade guiando o povo (1830)">
   </div>
   ```
   O estilo `.plate-img` já existe (cobre a área, recorta com elegância). A legenda abaixo permanece.

## Obras por slide

| Slide | Obra | Autor · data | Fonte sugerida (domínio público) | Salvar como |
|---|---|---|---|---|
| 18 | *Respect à la Constitution* (Constituição belga) | Meganck · 1848 | Wikimedia Commons / KBR (Bélgica) | `assets/belgica-meganck.jpg` |
| 18 | *La Liberté guidant le peuple* (par/contraste) | Delacroix · 1830 | Wikimedia Commons (Louvre) | `assets/delacroix-liberte.jpg` |
| 19 | *La Liberté guidant le peuple* | Delacroix · 1830 | Wikimedia Commons (Louvre) | `assets/delacroix-liberte.jpg` |
| 19 | Busto de Marianne (modelo de prefeitura) | séc. XX | Wikimedia Commons (cat. "Marianne busts") | `assets/marianne-busto.jpg` |
| 14 | *L'envoyé de la Justice* | Chifflart · 1859 | Gallica (BnF) | `assets/chifflart-justice.jpg` |
| 11 | *Alegoria da República* | Décio Villares · 1889 | Wikimedia Commons / Museu da República | `assets/villares-republica.jpg` |
| 11 | Nota 100 francos — Banque du Congo Belge | 1912 | Wikimedia Commons (numismática) | `assets/congo-100fr.jpg` |
| 20 | Marianne de guerra (gritando) | Steinlen · 1914–18 | Gallica / LOC (WWI posters) | `assets/steinlen-marianne.jpg` |
| 20 | Marianne-estátua / *Emprunt National* | Lelong · 1920 | Gallica (BnF, affiches) | `assets/lelong-emprunt.jpg` |
| 21 | *Madame Anastasie* (censura) | André Gill · 1874 | Wikimedia Commons (*L'Éclipse*) | `assets/gill-anastasie.jpg` |
| 21 | *Liberty Is Not Anarchy* | Thomas Nast · 1886 | Wikimedia Commons (*Harper's Weekly*) | `assets/nast-liberty.jpg` |
| 21 | *Looking Backward* | Joseph Keppler · 1893 | Wikimedia Commons (*Puck*) / LOC | `assets/keppler-looking-backward.jpg` |

### Bônus (caso queira slides extras)
- **Lady Justice, Old Bailey** — F. W. Pomeroy, 1907 (Wikimedia Commons) → `assets/oldbailey-justice.jpg`
- **Semeuse** — Oscar Roty, moeda 1 franco, 1898 (Wikimedia Commons, numismática) → `assets/roty-semeuse.jpg`
- **Palais de Justice de Bruxelles** — Poelaert, 1883 (Wikimedia Commons) → `assets/poelaert-palais.jpg`
- **Columbia entrega a espada a Dewey** — 1899 (LOC) → `assets/columbia-dewey.jpg`

> Dica: no Wikimedia Commons, use a página da obra → "Baixar" → resolução média (≈1200px de largura
> basta para projeção). Verifique sempre o nome exato do arquivo antes de baixar.
