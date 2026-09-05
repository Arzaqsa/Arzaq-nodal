import matplotlib.pyplot as plt
import numpy as np
from calculations import hagedorn_brown_vlp

def plot_nodal(results, Pb, P_wh):
    fig, ax = plt.subplots(figsize=(10,6))

    # IPR
    ax.plot(results['Q_ipr'], results['P_ipr'], 'b-', linewidth=2.5, label="IPR - Vogel")
    ax.axhline(y=Pb, color='g', linestyle='--', label=f'Pb = {Pb} psi')

    # VLP
    Q_vlp = np.linspace(0, results['Qmax']*1.2, 100)
    P_vlp = []
    for q in Q_vlp:
        p = hagedorn_brown_vlp(q, 8000, 2.88, P_wh, 220, 500, 0, 35, 0.7)[0] # لازم تمرر المدخلات الحقيقية
        P_vlp.append(p)
    ax.plot(Q_vlp, P_vlp, 'r-', linewidth=2.5, label="VLP")

    # Operating Point
    ax.plot(results['Q_nodal'], results['Pwf_nodal'], 'ro', markersize=12, label=f'Operating Point')

    ax.set_xlabel("Flow Rate Q (STB/day)")
    ax.set_ylabel("Pressure (psi)")
    ax.set_title("Nodal Analysis - IPR vs VLP")
    ax.legend()
    ax.grid(True)
    ax.invert_yaxis()
    return fig
