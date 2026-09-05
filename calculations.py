import numpy as np
from scipy.optimize import fsolve

def calculate_pvt(API, Gas_Gravity, T_res, GOR, WC):
    rho_o = 141.5 / (API + 131.5) * 62.4
    rho_g = Gas_Gravity * 0.0764
    rho_w = 62.4
    f_o = (1 - WC/100)
    f_w = WC/100
    rho_mix = f_o * rho_o + f_w * rho_w
    return rho_o, rho_g, rho_w, rho_mix

def vogel_ipr(Pr, Pb, PI, Pwf_array):
    Qmax = PI * Pr / 1.8
    Q = np.zeros_like(Pwf_array)
    for i, Pwf in enumerate(Pwf_array):
        if Pwf >= Pb:
            Q[i] = PI * (Pr - Pwf)
        else:
            Q_above = PI * (Pr - Pb)
            Q_below = Qmax * (1 - 0.2 * (Pwf/Pb) - 0.8 * (Pwf/Pb)**2)
            Q[i] = Q_above + Q_below
    return Q, Qmax

def hagedorn_brown_vlp_single(Q, Depth, Tubing_ID, P_wh, T_res, GOR, WC, API, Gas_Gravity):
    """نسخة ترجع رقم واحد فقط عشان fsolve"""
    _, rho_mix = calculate_pvt(API, Gas_Gravity, T_res, GOR, WC)
    A = np.pi * (Tubing_ID/12)**2 / 4
    v = Q * 5.615 / (A * 86400) if Q > 0 else 0.01
    P_vlp = P_wh + (rho_mix/144) * Depth + 0.001 * v**2 * Depth
    return P_vlp

def calculate_ipr_vlp(inputs):
    Pr = inputs['Pr']
    Pb = inputs['Pb']
    PI = inputs['PI']
    Depth = inputs['Depth']
    Tubing_ID = inputs['Tubing_ID']
    P_wh = inputs['P_wh']
    T_res = inputs['T_res']
    GOR = inputs['GOR']
    API = inputs['API']
    Gas_Gravity = inputs['Gas_Gravity']
    WC = inputs['WC']

    P_ipr = np.linspace(0, Pr, 100)
    Q_ipr, Qmax = vogel_ipr(Pr, Pb, PI, P_ipr)

    def objective(Q_guess):
        Pwf_guess = Pr - (Q_guess/PI)*1.8
        P_vlp = hagedorn_brown_vlp_single(Q_guess, Depth, Tubing_ID, P_wh, T_res, GOR, WC, API, Gas_Gravity)
        return Pwf_guess - P_vlp

    Q_nodal = fsolve(objective, Qmax/2)[0]
    Pwf_nodal = Pr - (Q_nodal/PI)*1.8
    Pwf_nodal = max(0, min(Pwf_nodal, Pr))

    results = {
        'P_ipr': P_ipr,
        'Q_ipr': Q_ipr,
        'Q_nodal': Q_nodal,
        'Pwf_nodal': Pwf_nodal,
        'Qmax': Qmax
    }
    return results
