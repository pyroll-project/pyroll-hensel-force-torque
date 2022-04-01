from pathlib import Path

import pytask
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.signal import savgol_filter

DATA_DIR = Path(__file__).parent / "data" / "lever_arm"


@pytask.mark.depends_on(DATA_DIR.glob("*.csv"))
@pytask.mark.produces("lever_arm_hensel.svg")
def task_lever_arm(produces):
    box_box_data = pd.read_csv(DATA_DIR / "box_box.csv", index_col=False, header=0)

    diamond_square_data = pd.read_csv(DATA_DIR / "diamond_square.csv", index_col=False, header=0)

    hexagon_square_data = pd.read_csv(DATA_DIR / "hexagon_square.csv", index_col=False, header=0)

    square_diamond_data = pd.read_csv(DATA_DIR / "square_diamond.csv", index_col=False, header=0)

    square_hexagon_data = pd.read_csv(DATA_DIR / "square_hexagon.csv", index_col=False, header=0)

    square_oval_data = pd.read_csv(DATA_DIR / "square_oval.csv", index_col=False, header=0)

    original_upper_curve = pd.read_csv(DATA_DIR / "upper_curve.csv", index_col=False, header=0)

    original_lower_curve = pd.read_csv(DATA_DIR / "lower_curve.csv", index_col=False, header=0)

    original_mid_curve = pd.read_csv(DATA_DIR / "mid_curve.csv", index_col=False, header=0)

    def smooth_curve(curve_data: pd.DataFrame):
        frame = curve_data
        ad_am = frame.iloc[:, 0].to_numpy()
        lever_arm = frame.iloc[:, 1].to_numpy()
        if len(lever_arm) % 2 == 0:
            filtered = savgol_filter(lever_arm, window_length=len(lever_arm) - 1, polyorder=9)
        else:
            filtered = savgol_filter(lever_arm, window_length=len(lever_arm), polyorder=9)

        return ad_am, filtered

    upper_curve = smooth_curve(original_upper_curve)
    mid_curve = smooth_curve(original_mid_curve)
    lower_curve = smooth_curve(original_lower_curve)

    fig = plt.figure(figsize=(8.3, 6))
    grid = fig.add_gridspec(3, 1, height_ratios=[1, 0.3, 0.001])
    ax = fig.add_subplot(grid[0])
    fig.subplots_adjust(hspace=0)

    ax.plot(upper_curve[0], upper_curve[1], 'k', linestyle='--')
    ax.plot(mid_curve[0], mid_curve[1], 'r')
    ax.plot(lower_curve[0], lower_curve[1], 'k', linestyle='--')

    ax.scatter(box_box_data['ad_am'], box_box_data['m'], color='black', marker='s'),
    ax.scatter(diamond_square_data['ad_am'], diamond_square_data['m'], color='black', marker='x'),
    ax.scatter(hexagon_square_data['ad_am'], hexagon_square_data['m'], color='black', marker='1'),
    ax.scatter(square_diamond_data['ad_am'], square_diamond_data['m'], color='black', marker='+'),
    ax.scatter(square_hexagon_data['ad_am'], square_hexagon_data['m'], color='black', marker='v'),
    ax.scatter(square_oval_data['ad_am'], square_oval_data['m'], color='black', marker='*')

    textstr = '\n'.join((r'$v_w=0.1...2 \frac{m}{s}$', r'$\frac{b_k}{h_k}=1.25...4.4$', r'$\vartheta=900...1000°C$'))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.67, 0.97, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

    ax.set_xlabel(r'cross section ratio $\frac{A_d}{A_{dm}}$')
    ax.set_ylabel(r'lever arm coefficient  $m$')

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
