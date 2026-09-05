import matplotlib.pyplot as plt
import numpy as np
from calculations import vogel_ipr, hagedorn_brown_vlp_single

def plot_nodal(results, inputs):
    """
    يرسم IPR vs VLP ويحدد نقطة التشغيل
    inputs: dict فيه كل المدخلات من app.py
    """
    fig, ax = plt.subplots(figsize=(10,6))

    # 1. رسم IPR
    ax.plot(results['Q_ipr'], results['P_ipr'], 'b-', linewidth=2.5, label="IPR - Vogel")
    ax.axhline(y=inputs['Pb'], color='g', linestyle='--', linewidth=1.5, label=f"Pb = {inputs['Pb']:.0f} psi")

    # 2. رسم VLP
    Q_vlp = np.linspace(0, results['Qmax']*1.2, 100)
    P_vlp = []
    for q in Q_vlp:
        p = hagedorn_brown_vlp_single(
            q, 
            inputs['Depth'], 
            inputs['Tubing_ID'], 
            inputs['P_wh'], 
            inputs['T_res'], 
            inputs['GOR'], 
            inputs['WC'], 
            inputs['API'], 
            inputs['Gas_Gravity']
        )
        P_vlp.append(p)
    
    ax.plot(Q_vlp, P_vlp, 'r-', linewidth=2.5, label="VLP - Hagedorn-Brown")

    # 3. نقطة التشغيل
    ax.plot(results['Q_nodal'], results['Pwf_nodal'], 'ro', markersize=12, 
            label=f"Operating Point: {results['Q_nodal']:,.0f} STB/d @ {results['Pwf_nodal']:,.0f} psi")
    
    # 4. تنسيق الرسم
    ax.set_xlabel("Flow Rate Q (STB/day)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Pressure (psi)", fontsize=12, fontweight='bold')
    ax.set_title("Nodal Analysis - IPR vs VLP", fontsize=14, fontweight='bold')
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.invert_yaxis() # الضغط يقل لتحت
    ax.set_xlim(left=0)
    ax.set_ylim(top=inputs['Pr']*1.05, bottom=0)

    plt.tight_layout()
    return fig
