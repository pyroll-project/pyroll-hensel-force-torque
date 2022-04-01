from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytask
from matplotlib.lines import Line2D

DATA_DIR = Path(__file__).parent / "data" / "deformation_resistance"


@pytask.mark.depends_on(DATA_DIR.glob("*.csv"))
@pytask.mark.produces("deformation_resistance_hensel.svg")
def task_deformation_resistance_hensel(produces):
    ad_am_data = np.linspace(0, 4, 100)

    box_box_data = pd.read_csv(DATA_DIR / "box_box.csv", index_col=False, header=0)

    diamond_square_data = pd.read_csv(DATA_DIR / "diamond_square.csv", index_col=False, header=0)

    hexagon_square_data = pd.read_csv(DATA_DIR / "hexagon_square.csv", index_col=False, header=0)

    oval_round_data = pd.read_csv(DATA_DIR / "oval_round.csv", index_col=False, header=0)

    oval_square_data = pd.read_csv(DATA_DIR / "oval_square.csv", index_col=False, header=0)

    square_diamond_data = pd.read_csv(DATA_DIR / "square_diamond.csv", index_col=False, header=0)

    square_hexagon_data = pd.read_csv(DATA_DIR / "square_hexagon.csv", index_col=False, header=0)

    square_oval_data = pd.read_csv(DATA_DIR / "square_oval.csv", index_col=False, header=0)

    def upper_curve(ad_am):
        return 1.09059021 + 0.03602259 * ad_am + 0.06653886 * ad_am ** 2 + 0.12977074 * np.exp(
            -0.0032585 * ad_am) + 1.62121323 * np.exp(
            -2.30014664 * ad_am ** 2)

    def mid_curve(ad_am):
        return 0.9901 + 0.106 * ad_am + 0.0283 * ad_am ** 2 + 1.5718 * np.exp(-2.4609 * ad_am) + 0.3117 * np.exp(
            -15.625 * ad_am ** 2)

    def lower_curve(ad_am):
        return 1.02186293 - 0.083184 * ad_am + 0.07559639 * ad_am ** 2 + 0.57900042 * np.exp(
            -3.701351047 * ad_am) + 0.74786599 * np.exp(
            -2.8666754 * ad_am ** 2)

    fig = plt.figure(figsize=(8.3, 6))
    grid = fig.add_gridspec(3, 1, height_ratios=[1, 0.3, 0.001])
    ax = fig.add_subplot(grid[0])
    fig.subplots_adjust(hspace=0)

    ax.plot(ad_am_data, upper_curve(ad_am_data), 'k', linestyle='--'),
    ax.plot(ad_am_data, mid_curve(ad_am_data), 'r'),
    ax.plot(ad_am_data, lower_curve(ad_am_data), 'k', linestyle='--')

    ax.scatter(box_box_data['ad_am'], box_box_data['kwm_kfm'], color='black', marker='s'),
    ax.scatter(diamond_square_data['ad_am'], diamond_square_data['kwm_kfm'], color='black', marker='x'),
    ax.scatter(hexagon_square_data['ad_am'], hexagon_square_data['kwm_kfm'], color='black', marker='1'),
    ax.scatter(oval_round_data['ad_am'], oval_round_data['kwm_kfm'], color='black', marker='2'),
    ax.scatter(oval_square_data['ad_am'], oval_square_data['kwm_kfm'], color='black', marker='.'),
    ax.scatter(square_diamond_data['ad_am'], square_diamond_data['kwm_kfm'], color='black', marker='+'),
    ax.scatter(square_hexagon_data['ad_am'], square_hexagon_data['kwm_kfm'], color='black', marker='v'),
    ax.scatter(square_oval_data['ad_am'], square_oval_data['kwm_kfm'], color='black', marker='*')

    textstr = '\n'.join((r'$v_w=0.1...10 \frac{m}{s}$', r'$\frac{b_k}{h_k}=1.25...4.4$', r'$\vartheta=800...1200°C$'))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.67, 0.97, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

    ax.set_xlabel(r'Flächenverhältnis $\frac{A_d}{A_{dm}}$')
    ax.set_ylabel(r'bezogener Umformwiderstand $\frac{k_{wm}}{k_fm}}$')

    _handles = [
        Line2D([], [], color='black', label='box $\\rightarrow$ box', ls='', marker='s'),
        Line2D([], [], color='black', label='diamond $\\rightarrow$ square', ls='', marker='x'),
        Line2D([], [], color='black', label='swedish oval $\\rightarrow$ square', ls='', marker='1'),
        Line2D([], [], color='black', label='oval $\\rightarrow$ round', ls='', marker='2'),
        Line2D([], [], color='black', label='oval  $\\rightarrow$ square', ls='', marker='.'),
        Line2D([], [], color='black', label='square $\\rightarrow$ diamond', ls='', marker='+'),
        Line2D([], [], color='black', label='square $\\rightarrow$ swedish oval', ls='', marker='v'),
        Line2D([], [], color='black', label='square $\\rightarrow$ oval', ls='', marker='*'),
        Line2D([], [], color='red', label='mean')
    ]

    fig.legend(handles=_handles, loc="lower center", bbox_to_anchor=(0.5, 0.07), ncol=3, frameon=True)

    fig.savefig(produces, dpi=300, orientation='landscape')
