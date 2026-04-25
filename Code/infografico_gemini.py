import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

# Configurações de estilo
plt.rcParams['font.family'] = 'serif'
COLORS = {
    'fundacional': '#C9963B',
    'normativo': '#2B4C7E',
    'militar': '#8B1A1A',
    'contra': '#3A6B4C',
    'neutral': '#2B4C7E'
}

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes."""
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):
        name = 'radar'
        def fill(self, *args, closed=True, **kwargs):
            return super().fill(*args, **kwargs)

        def plot(self, *args, **kwargs):
            return super().plot(*args, **kwargs)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars, radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine_type = 'circle'
                verts = unit_poly_verts(theta)
                verts.append(verts[0])
                path = Path(verts)
                spine = Spine(self, spine_type, path)
                spine.set_transform(self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def unit_poly_verts(theta):
    """Return vertices of polygon for radar chart."""
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def create_infographic():
    fig = plt.figure(figsize=(18, 24), facecolor='white')
    gs = gridspec.GridSpec(5, 2, height_ratios=[0.5, 1.5, 1.5, 1.5, 1.5])
    plt.subplots_adjust(hspace=0.4, wspace=0.3, top=0.92, bottom=0.05, left=0.1, right=0.9)

    # --- CABEÇALHO ---
    ax_header = fig.add_subplot(gs[0, :])
    ax_header.axis('off')
    ax_header.text(0.5, 0.8, 'ICONOCRACIA', fontsize=44, fontweight='bold', ha='center', fontfamily='serif')
    ax_header.text(0.5, 0.55, 'Corpus de Alegorias Femininas na História da Cultura Jurídica', fontsize=20, ha='center', fontfamily='serif')
    ax_header.text(0.5, 0.3, '165 itens | 15 países | 1239-1975 | endurecimento médio 1.42', 
                  fontsize=16, ha='center', fontfamily='sans-serif', fontweight='bold', color='#444444')

    # --- PAINEL A: Distribuição por país ---
    ax_a = fig.add_subplot(gs[1, 0])
    countries = ['França', 'EUA', 'Alemanha', 'Brasil', 'Reino Unido', 'Bélgica', 'Itália', 'Países Baixos', 'Portugal', 'Espanha']
    values_a = [45, 24, 23, 15, 14, 9, 8, 8, 7, 4]
    y_pos = np.arange(len(countries))
    colors_a = plt.cm.Blues(np.linspace(0.9, 0.4, len(countries)))
    bars = ax_a.barh(y_pos, values_a, align='center', color=colors_a)
    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(countries, fontfamily='sans-serif')
    ax_a.invert_yaxis()
    ax_a.set_title('PAINEL A — Distribuição por país (Top 10)', fontsize=16, fontweight='bold', pad=20)
    for i, v in enumerate(values_a):
        ax_a.text(v + 0.5, i, str(v), color='black', va='center', fontweight='bold')
    ax_a.spines['top'].set_visible(False)
    ax_a.spines['right'].set_visible(False)

    # --- PAINEL B: Regimes Iconocráticos ---
    ax_b = fig.add_subplot(gs[1, 1])
    regimes = ['Fundacional', 'Normativo', 'Militar', 'Contra-alegoria']
    counts_b = [79, 45, 31, 10]
    colors_b = [COLORS['fundacional'], COLORS['normativo'], COLORS['militar'], COLORS['contra']]
    wedges, texts, autotexts = ax_b.pie(counts_b, labels=regimes, autopct='%1.1f%%', 
                                      colors=colors_b, startangle=140, pctdistance=0.85,
                                      textprops={'fontfamily': 'sans-serif', 'fontweight': 'bold'})
    center_circle = plt.Circle((0,0), 0.70, fc='white')
    ax_b.add_artist(center_circle)
    ax_b.text(0, 0, '165\nitens', ha='center', va='center', fontsize=20, fontweight='bold')
    ax_b.set_title('PAINEL B — Regimes iconocráticos', fontsize=16, fontweight='bold', pad=20)

    # --- PAINEL C: Distribuição temporal (Largo) ---
    ax_c = fig.add_subplot(gs[2, :])
    decades = ['Pré-1800', '1820s', '1830s', '1840s', '1850s', '1860s', '1870s', '1880s', '1890s', '1900s', '1910s', '1920s', '1930s', '1940s', '1950s', '1960s', '1970s']
    values_c = [48, 1, 4, 2, 4, 9, 9, 7, 10, 10, 32, 8, 2, 4, 4, 2, 2]
    # Nota: O prompt pede "barras empilhadas por regime", mas não forneceu a quebra por regime por década.
    # Vou usar uma cor gradiente baseada no regime predominante ou azul neutro.
    ax_c.bar(decades, values_c, color=COLORS['neutral'], alpha=0.8)
    ax_c.set_title('PAINEL C — Distribuição temporal por década', fontsize=16, fontweight='bold', pad=20)
    ax_c.set_xticklabels(decades, rotation=45, ha='right', fontfamily='sans-serif')
    ax_c.annotate('PICO (32 itens)', xy=(10, 32), xytext=(12, 35),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=12, fontweight='bold')
    ax_c.set_ylim(0, 45)
    ax_c.spines['top'].set_visible(False)
    ax_c.spines['right'].set_visible(False)

    # --- PAINEL D: endurecimento por regime ---
    ax_d = fig.add_subplot(gs[3, 0])
    regimes_d = ['Contra-alegoria', 'Fundacional', 'Militar', 'Normativo']
    scores_d = [0.72, 1.15, 1.76, 1.90]
    colors_d = [COLORS['contra'], COLORS['fundacional'], COLORS['militar'], COLORS['normativo']]
    bars_d = ax_d.bar(regimes_d, scores_d, color=colors_d)
    ax_d.set_title('PAINEL D — endurecimento por regime', fontsize=16, fontweight='bold', pad=20)
    ax_d.set_ylim(0, 2.5)
    ax_d.set_ylabel('Score Médio (0-3)', fontfamily='sans-serif')
    for bar in bars_d:
        height = bar.get_height()
        ax_d.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
    ax_d.spines['top'].set_visible(False)
    ax_d.spines['right'].set_visible(False)

    # --- PAINEL E: Distribuição por suporte ---
    ax_e = fig.add_subplot(gs[3, 1])
    supports = ['Gravura', 'Moeda', 'Cartaz', 'Pintura', 'Papel-moeda', 'Fotografia', 'Selo', 'Monumento']
    values_e = [62, 21, 19, 13, 9, 7, 6, 1]
    y_pos_e = np.arange(len(supports))
    ax_e.barh(y_pos_e, values_e, color=COLORS['neutral'])
    ax_e.set_yticks(y_pos_e)
    ax_e.set_yticklabels(supports, fontfamily='sans-serif')
    ax_e.invert_yaxis()
    ax_e.set_title('PAINEL E — Distribuição por suporte', fontsize=16, fontweight='bold', pad=20)
    for i, v in enumerate(values_e):
        ax_e.text(v + 0.5, i, str(v), color='black', va='center', fontweight='bold')
    ax_e.spines['top'].set_visible(False)
    ax_e.spines['right'].set_visible(False)

    # --- PAINEL F: Radar dos 10 indicadores de endurecimento ---
    indicators = ['Desincorporação', 'Rigidez postural', 'Dessexualização', 'Uniformização facial', 
                  'Heraldicização', 'Arq. Enquadramento', 'Apagamento narr.', 'Monocromatização', 
                  'Serialidade', 'Insc. Estatal']
    values_f = [1.01, 1.29, 1.48, 1.46, 1.29, 1.23, 1.26, 1.95, 1.68, 1.57]
    
    num_vars = len(indicators)
    theta = radar_factory(num_vars, frame='polygon')
    ax_f = fig.add_subplot(gs[4, :], projection='radar')
    ax_f.plot(theta, values_f, color=COLORS['normativo'], linewidth=2)
    ax_f.fill(theta, values_f, facecolor=COLORS['normativo'], alpha=0.25)
    ax_f.set_varlabels(indicators)
    ax_f.set_ylim(0, 3)
    ax_f.set_title('PAINEL F — Radar dos 10 indicadores de endurecimento (Escala 0-3)', 
                  fontsize=16, fontweight='bold', pad=30)
    
    # Destacar monocromatização
    ax_f.text(theta[7], values_f[7] + 0.3, 'MÁX: 1.95', color=COLORS['militar'], fontweight='bold', ha='center')

    # Salvar resultados
    plt.savefig('corpus/infografico_gemini.png', dpi=300, bbox_inches='tight')
    plt.savefig('corpus/infografico_gemini.pdf', bbox_inches='tight')
    print("Infográfico gerado com sucesso em corpus/infografico_gemini.png e .pdf")

if __name__ == '__main__':
    create_infographic()
