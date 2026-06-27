#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cronologia Visual das Moedas Brasileiras (1889–presente)
Da efígie de Dom Pedro II à figura da República.
Versão otimizada com layout flexível, cálculo dinâmico de alturas
e detecção de fontes compatível com macOS e Linux.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import sys

# ---- Detecção de Caminhos (Portável) ----
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()

# Usamos caminho relativo ao diretório do script
local_moedas = os.path.join(SCRIPT_DIR, "moedas")
BASE = local_moedas if os.path.exists(local_moedas) else SCRIPT_DIR

OUT = os.path.join(SCRIPT_DIR, "cronologia_moedas_brasil.png")

# ---- Paleta (sóbria, acadêmica) ----
BG       = (244, 241, 234)   # marfim
INK      = (33, 31, 28)      # quase-preto
SUB      = (92, 84, 74)      # marrom acinzentado
LINE     = (200, 192, 180)
IMPERIO  = (122, 30, 38)     # bordô imperial
PROCLAM  = (28, 74, 92)      # azul-petróleo
VARGAS   = (138, 96, 28)     # ocre/bronze
REAL     = (40, 92, 64)      # verde
ACCENT   = (176, 142, 66)    # dourado

W = 2400
MARGIN = 90

# ---- Fontes (Caminhos macOS + Linux) ----
def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    # Fallback genérico tentando carregar fontes do sistema por nome se Pillow suportar
    for name in ["Georgia", "Arial", "Helvetica", "DejaVu Serif", "DejaVu Sans"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

# Listas de caminhos ordenadas por preferência (macOS Supplemental / Library -> Linux share)
SERIF = [
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/Library/Fonts/Georgia.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
]
SERIF_B = [
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
]
SANS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]
SANS_B = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]
SANS_I = [
    "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    "/Library/Fonts/Arial Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"
]

f_title   = load_font(SERIF_B, 64)
f_sub     = load_font(SANS, 32)
f_period  = load_font(SERIF_B, 44)
f_years   = load_font(SANS_B, 30)
f_coin    = load_font(SANS_B, 28)
f_body    = load_font(SANS, 25)
f_attr_h  = load_font(SANS_B, 24)
f_attr    = load_font(SANS, 23)
f_foot    = load_font(SANS_I, 21)
f_lpai    = load_font(SANS, 20)

def text_wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def fit_coin(path, target_h):
    """
    Carrega e redimensiona a moeda mantendo a proporção de aspecto.
    Se o arquivo não existir, gera um placeholder cinza elegante com bordas arredondadas.
    """
    if not os.path.exists(path):
        # Fallback caso a imagem não exista no ambiente rodando o script
        placeholder = Image.new("RGBA", (target_h, target_h), (220, 216, 208, 255))
        draw_p = ImageDraw.Draw(placeholder)
        draw_p.ellipse([10, 10, target_h-10, target_h-10], outline=(150, 140, 130, 255), width=4)
        draw_p.text((target_h//2 - 40, target_h//2 - 15), "[Moeda]", fill=(120, 110, 100, 255), font=f_attr_h)
        return placeholder
        
    im = Image.open(path).convert("RGBA")
    r = target_h / im.height
    return im.resize((int(im.width*r), target_h), Image.Resampling.LANCZOS)

# ---- Conteúdo por período ----
periods = [
    {
        "color": IMPERIO,
        "name": "IMPÉRIO",
        "years": "Segundo Reinado · até 1889",
        "coin": "imperio_2000reis_pedroII.png",
        "coin_label": "2.000 Réis · 1889 · prata · Pedro II",
        "desc": "A última cunhagem imperial fixa a autoridade no corpo do soberano. "
                "O anverso traz o busto de Dom Pedro II, individualizado pela barba e pelos "
                "traços de retrato; o reverso, as Armas do Império coroadas.",
        "attrs": [
            ("Efígie", "Busto masculino, retrato individual de Pedro II"),
            ("Insígnia", "Coroa imperial; esfera armilar; Cruz da Ordem de Cristo"),
            ("Flora", "Ramos de café e tabaco — riqueza agrária"),
            ("Lema", "PETRUS II D.G.C. IMP. ET PERP. BRAS. DEF."),
            ("Autoridade", "Pessoal e dinástica — a face do monarca"),
        ],
        "lpai": "Regime Militar-Imperial · efígie do soberano · M.1 · G.2",
    },
    {
        "color": PROCLAM,
        "name": "PROCLAMAÇÃO",
        "years": "Primeira República · 1889–1942",
        "coin": "republica_1000reis_1889_museu.jpg",
        "coin_label": "1.000 Réis · 1889 · prata · República",
        "desc": "O Decreto nº 54-B (1889) manda abrir novos cunhos: a face do imperador "
                "cede à alegoria feminina da Liberdade-República, à maneira da Marianne. "
                "A autoridade desindividualiza-se e se torna princípio abstrato.",
        "attrs": [
            ("Efígie", "Busto feminino — a Liberdade / a República"),
            ("Insígnia", "Barrete frígio (pileus libertatis), gorro da liberdade"),
            ("Estrelas", "Cruzeiro do Sul + 21 estrelas (Estados da União)"),
            ("Lema", "ORDEM E PROGRESSO · 15 DE NOVEMBRO DE 1889"),
            ("Autoridade", "Impessoal e cívica — princípio republicano"),
        ],
        "lpai": "Respublica 312.4 · barrete frígio 211.1 · +610.3 positivista · G.1",
    },
    {
        "color": VARGAS,
        "name": "ERA VARGAS",
        "years": "Cruzeiro · 1942–1967",
        "coin": "vargas_1cruzeiro_mapa.png",
        "coin_label": "1 Cruzeiro · 1945 · mapa do Brasil",
        "desc": "O Cruzeiro (Decreto-Lei 4.791/1942) reorganiza a iconografia: a efígie de "
                "Getúlio Vargas ocupa os centavos, enquanto as moedas de cruzeiro exibem o "
                "mapa territorial e o Cruzeiro do Sul. A alegoria recua diante do território e do líder.",
        "attrs": [
            ("Efígie", "Getúlio Vargas (centavos); território nos cruzeiros"),
            ("Insígnia", "Mapa do Brasil — soberania territorial"),
            ("Estrelas", "Constelação do Cruzeiro do Sul; ramos de louro"),
            ("Lema", "GETÚLIO VARGAS · BRASIL (centavos)"),
            ("Autoridade", "Estado-nação e personalismo do Estado Novo"),
        ],
        "lpai": "Deslocamento da alegoria · território + efígie do chefe · M.1",
    },
    {
        "color": REAL,
        "name": "REAL",
        "years": "Real · desde 1994",
        "coin": "real_1real_1998.png",
        "coin_label": "1 Real · 1998 · bimetálica · Efígie da República",
        "desc": "O Real reentroniza a Efígie da República, agora como busto neoclássico "
                "esculpido, coroado de louros. O reverso retoma o Cruzeiro do Sul e as estrelas. "
                "A figura republicana volta ao centro do papel-moeda, classicizada e serena.",
        "attrs": [
            ("Efígie", "Busto feminino neoclássico — a Efígie da República"),
            ("Insígnia", "Coroa de louros (laurel); face classicizada"),
            ("Estrelas", "Cruzeiro do Sul sobre esfera (Pavilhão Nacional)"),
            ("Lema", "BRASIL · ORDEM E PROGRESSO (na faixa do reverso)"),
            ("Autoridade", "Cívica e institucional — permanência republicana"),
        ],
        "lpai": "Respublica 312.4 · louros 311.3 · classicizada B.4a · M.1 · P.1",
    },
]

# ---- Pré-processamento e Cálculo Dinâmico de Layout ----
ROW_PAD = 60
COIN_H = 300
img_tmp = Image.new("RGB", (10, 10))
d_tmp = ImageDraw.Draw(img_tmp)

col_text_x = MARGIN + 760           # Onde começa o bloco de texto à direita
text_w = W - col_text_x - MARGIN

# Carrega e ajusta todas as imagens primeiro para sabermos a altura exata
for p in periods:
    coin_path = os.path.join(BASE, p["coin"])
    coin = fit_coin(coin_path, COIN_H)
    # Limita largura se exceder
    maxcw = 700
    if coin.width > maxcw:
        r = maxcw / coin.width
        coin = coin.resize((maxcw, int(coin.height*r)), Image.Resampling.LANCZOS)
    p["coin_img"] = coin

row_heights = []
for p in periods:
    # 1. LADO ESQUERDO: Título, Subtítulo, Moeda e Legenda da Moeda
    # A moeda começa em 120px abaixo do topo do conteúdo (onde se iniciam os textos à direita)
    # A legenda da moeda precisa de espaço para ser desenhada: a fonte f_coin tem tamanho 28 (altura real de ~35px)
    # O espaçamento inferior e superior é dado por ROW_PAD na montagem final.
    h_left = 120 + p["coin_img"].height + 16 + 35
    
    # 2. LADO DIREITO: Descrição, Atributos e Barra LPAI
    desc_lines = text_wrap(d_tmp, p["desc"], f_body, text_w)
    h_desc = len(desc_lines) * 33
    
    # Simula a quebra de linha real dos valores dos atributos para saber a altura exata
    h_attrs_real = 0
    for k, v in p["attrs"]:
        kw = d_tmp.textlength(f"{k}:  ", font=f_attr_h)
        vlines = text_wrap(d_tmp, v, f_attr, text_w - kw - 10)
        h_attrs_real += (len(vlines) * 31) + 5
        
    # A altura necessária do lado direito é a soma de todos os blocos internos:
    # 56 (pad inicial) + h_desc + 18 (pad pós-desc) + 14 (divisória) + h_attrs_real + 6 (pad pré-lpai) + 40 (painel LPAI)
    h_right = 56 + h_desc + 18 + 14 + h_attrs_real + 6 + 40
    
    # A altura do bloco útil é a maior entre o lado esquerdo e o lado direito
    content_h_max = max(h_left, h_right)
    
    # Altura total do bloco com pads (top e bottom)
    rh = content_h_max + ROW_PAD * 2
    row_heights.append(rh)

header_h = 280
footer_h = 190
H = header_h + sum(row_heights) + footer_h + 40

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ---- Cabeçalho ----
draw.rectangle([0, 0, W, 8], fill=ACCENT)
draw.text((MARGIN, 70), "Cronologia Visual da Moeda Brasileira", font=f_title, fill=INK)
draw.text((MARGIN, 158),
          "Da efígie de Dom Pedro II à figura da República — a mudança de autoridade política no papel-moeda (1889–presente)",
          font=f_sub, fill=SUB)
draw.line([MARGIN, 240, W-MARGIN, 240], fill=LINE, width=2)

# ---- Renderização dos Períodos ----
y = header_h
for i, (p, rh) in enumerate(zip(periods, row_heights)):
    col = p["color"]
    top = y
    bottom = y + rh

    # Coordenadas da timeline contínua (timeline spine)
    spine_cx = MARGIN - 22
    node_y = top + ROW_PAD + 22  # Alinhado horizontalmente com o centro do título do período

    # Desenha a linha vertical da timeline
    if i == 0:
        # Primeiro período: começa no nó e vai até a base do bloco
        draw.rectangle([spine_cx - 4, node_y, spine_cx + 4, bottom], fill=col)
    elif i == len(periods) - 1:
        # Último período: vem do topo do bloco e vai até o nó
        draw.rectangle([spine_cx - 4, top, spine_cx + 4, node_y], fill=col)
    else:
        # Períodos intermediários: cruza todo o bloco de cima a baixo
        draw.rectangle([spine_cx - 4, top, spine_cx + 4, bottom], fill=col)

    # Desenha o nó do tempo (anel elegante: círculo colorido com miolo marfim)
    draw.ellipse([spine_cx - 16, node_y - 16, spine_cx + 16, node_y + 16], fill=col)
    draw.ellipse([spine_cx - 8, node_y - 8, spine_cx + 8, node_y + 8], fill=BG)

    # LADO ESQUERDO: Textos do período e Moeda
    draw.text((MARGIN+30, top+ROW_PAD), p["name"], font=f_period, fill=col)
    draw.text((MARGIN+30, top+ROW_PAD+54), p["years"], font=f_years, fill=SUB)

    # Renderiza a moeda pré-carregada
    coin = p["coin_img"]
    coin_x = MARGIN + 30
    coin_y = top + ROW_PAD + 120
    
    # Moldura suave da moeda
    fr = 6
    draw.rectangle([coin_x-fr, coin_y-fr, coin_x+coin.width+fr, coin_y+coin.height+fr],
                   outline=col, width=3)
    img.paste(coin, (coin_x, coin_y), coin)
    
    # Legenda da Moeda (segura contra corte e sem sobreposição com a linha divisória)
    draw.text((coin_x, coin_y+coin.height+16), p["coin_label"], font=f_coin, fill=INK)

    # LADO DIREITO: Bloco de texto e atributos
    tx = col_text_x
    ty = top + ROW_PAD
    
    # Descrição do período
    for ln in text_wrap(draw, p["desc"], f_body, text_w):
        draw.text((tx, ty), ln, font=f_body, fill=INK)
        ty += 33
    ty += 18

    # Linha divisória de atributos
    draw.line([tx, ty, tx+text_w, ty], fill=LINE, width=1)
    ty += 14
    
    # Atributos comparativos
    for k, v in p["attrs"]:
        draw.text((tx, ty), f"{k}:", font=f_attr_h, fill=col)
        kw = draw.textlength(f"{k}:  ", font=f_attr_h)
        vlines = text_wrap(draw, v, f_attr, text_w - kw - 10)
        draw.text((tx+kw, ty), vlines[0], font=f_attr, fill=INK)
        ty += 31
        for extra in vlines[1:]:
            draw.text((tx+kw, ty), extra, font=f_attr, fill=INK)
            ty += 31
        ty += 5

    # Faixa LPAI v2 com fundo colorido
    ty += 6
    draw.rectangle([tx, ty, tx+text_w, ty+40], fill=col)
    draw.text((tx+16, ty+8), "LPAI v2  ·  " + p["lpai"], font=f_lpai, fill=BG)

    # Separador horizontal entre os blocos dos períodos
    if i < len(periods)-1:
        draw.line([MARGIN, bottom, W-MARGIN, bottom], fill=LINE, width=2)

    y = bottom

# ---- Rodapé ----
fy = H - footer_h + 24
draw.line([MARGIN, fy-10, W-MARGIN, fy-10], fill=LINE, width=2)

foot1 = ("Fontes: Banco Central do Brasil (Museu de Valores; Cartilha 'Dinheiro no Brasil'); "
         "Decreto nº 54-B/1889 e Decreto-Lei nº 4.791/1942 (Planalto); "
         "Museu Histórico Numismático (numis.mus.br); Numista; Wikimedia Commons.")
foot2 = ("Nota iconográfica: o gravador das primeiras moedas republicanas (1889) foi Francisco J. P. Carneiro ('F.C.'); "
         "Décio Villares é o criador da figura alegórica positivista da República e do emblema 'Ordem e Progresso'.")

for ln in text_wrap(draw, foot1, f_foot, W-2*MARGIN):
    draw.text((MARGIN, fy), ln, font=f_foot, fill=SUB)
    fy += 26
fy += 4
for ln in text_wrap(draw, foot2, f_foot, W-2*MARGIN):
    draw.text((MARGIN, fy), ln, font=f_foot, fill=SUB)
    fy += 26

# Salva a imagem final
img.save(OUT, "PNG")
print(f"Sucesso! Cronologia gerada e salva em: {OUT} ({img.size[0]}x{img.size[1]} px)")
