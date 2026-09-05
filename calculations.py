import numpy as np
from scipy.optimize import fsolve

# ثوابت
SCF_TO_RB = 0.00504

def calculate_pvt(API, Gas_Gravity, T_res, GOR, WC):
    """حساب PVT مبسط"""
    # كثافة النفط
    rho_o = 141.5 / (API + 131.5) * 62.4 # lb/ft3
    # كثافة الغاز
    rho_g = Gas_Gravity * 0.0764 # lb/ft3 at SC
    # كثافة الماء
    rho_w = 62.4 # lb/ft3
    # كثافة المائع المختلط
    f_o = (1 - WC/100) / (1 - WC/100 + WC/100 * 1.0) # تقريبي
    f_w = 1 - f_o
    rho_mix = f_o * rho_o + f_w * rho_w

    return rho_o, rho_g, rho_w, rho_mix

def vogel_ipr(Pr, Pb, PI, Pwf_array):
    """معادلة Vogel للـ Two Phase"""
    Qmax = PI * Pr / 1.8
    Q = np.zeros_like(Pwf_array)

    for i, Pwf in enumerate(Pwf_array):
        if Pwf >= Pb:
            Q[i] = PI * (Pr - Pwf) # Darcy فوق Pb
        else:
            Q_above = PI * (Pr - Pb)
            Q_below = Qmax * (1 - 0.2 * (Pwf/Pb) - 0.8 * (Pwf/Pb)**2)
            Q[i] = Q_above + Q_below

    return Q, Qmax

def hagedorn_brown_vlp(Q, Depth, Tubing_ID, P_wh, T_res, GOR, WC, API, Gas_Gravity):
    """VLP مبسط - Hagedorn-Brown"""
    P_array = np.linspace(P_wh, 5000, 100)
    Q_array = np.full_like(P_array, Q)

    _, _, rho_mix = calculate_pvt(API, Gas_Gravity, T_res, GOR, WC)

    # نحسب ضغط الاحتكاك + الهيدروستاتيك تقريبي
    A = np.pi * (Tubing_ID/12)**2 / 4 # ft2
    v = Q_array * 5.615 / (A * 86400) # ft/s تقريبي

    P_vlp = P_wh + (rho_mix/144) * Depth + 0.001 * v**2 * Depth # معادلة مبسطة جدا

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

    # 1. نرسم IPR
    P_ipr = np.linspace(0, Pr, 100)
    Q_ipr, Qmax = vogel_ipr(Pr, Pb, PI, P_ipr)

    # 2. نلاقي نقطة التقاطع Nodal Point
    def objective(Q_guess):
        Pwf_guess = Pr - (Q_guess/PI)*1.8 # تقريب اولي
        P_vlp = hagedorn_brown_vlp(Q_guess, Depth, Tubing_ID, P_wh, T_res, GOR, WC, API, Gas_Gravity)[0]
        return Pwf_guess - P_vlp

    Q_nodal = fsolve(objective, Qmax/2)[0]
    Pwf_nodal = Pr - (Q_nodal/PI)*1.8
    Pwf_nodal = max(0, Pwf_nodal)

    results = {
        'P_ipr': P_ipr,
        'Q_ipr': Q_ipr,
        'Q_nodal': Q_nodal,
        'Pwf_nodal': Pwf_nodal,
        'Qmax': Qmax
    }
    return results
