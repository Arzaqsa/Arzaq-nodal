import matplotlib.pyplot as plt

def plot_nodal(results, Pb):
    fig, ax = plt.subplots(figsize=(11,6))
    ax.plot(results["Q_ipr"], results["P_vals"], 'b-', linewidth=2.5, label="IPR Curve")
    ax.plot(results["Q_test"], results["Pwf_vlp"], 'r--', linewidth=2.5, label="VLP Curve")
    ax.plot(results["Q_nodal"], results["Pwf_nodal"], 'go', markersize=12, label=f"Nodal: {results['Q_nodal']:,.0f} STB/d")
    ax.axhline(y=Pb, color='orange', linestyle=':', label=f"Pb = {Pb} psi")
    ax.set_xlabel("Flow Rate Q (STB/day)"); ax.set_ylabel("Pressure (psi)")
    ax.set_title("Nodal Analysis - Arzaq Nodal"); ax.legend(); ax.grid(True); ax.invert_yaxis()
    return fig
