import numpy as np

def darcy_ipr(Pwf, Pr, PI):
    return PI * (Pr - Pwf)

def vogel_ipr(Pwf, Pr, Qmax):
    if Pwf >= Pr: return 0
    return Qmax * (1 - 0.2*(Pwf/Pr) - 0.8*(Pwf/Pr)**2)

def simple_vlp(Pwf, Q, Depth, Tubing_ID, GOR):
    friction = 0.00002 * Q**1.8 * Depth / (Tubing_ID**5)
    hydrostatic = 0.433 * Depth * (1 - GOR/5000)
    Pwh = Pwf - hydrostatic - friction
    return max(Pwh, 50)

def calculate_ipr_vlp(Pr, Pb, PI, Depth, Tubing_ID, GOR):
    Qmax = PI * Pr
    P_vals = np.linspace(0, Pr, 200)
    Q_ipr = [darcy_ipr(p, Pr, PI) if p >= Pb else vogel_ipr(p, Pr, Qmax) for p in P_vals]
    Q_test = np.linspace(100, Qmax*1.1, 200)
    Pwf_vlp = [simple_vlp(1000, q, Depth, Tubing_ID, GOR) + 0.433*Depth + 0.00002*q**1.8*Depth/(Tubing_ID**5) for q in Q_test]
    Q_ipr_interp = np.interp(Pwf_vlp, P_vals, Q_ipr)
    diff = np.abs(Q_ipr_interp - Q_test)
    nodal_idx = np.argmin(diff)
    return {"P_vals": P_vals, "Q_ipr": np.array(Q_ipr), "Q_test": Q_test, "Pwf_vlp": np.array(Pwf_vlp), "Q_nodal": Q_test[nodal_idx], "Pwf_nodal": Pwf_vlp[nodal_idx], "Qmax": Qmax}
