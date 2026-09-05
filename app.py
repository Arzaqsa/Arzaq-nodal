import streamlit as st
from calculations import calculate_ipr_vlp
from plotting import plot_nodal
from report import create_report

st.set_page_config(page_title="Arzaq Nodal", layout="wide")
st.title("🛢️ Arzaq Nodal - Professional Well Analysis")
st.caption("Nodal Analysis with IPR Vogel + VLP for Two-Phase Flow")

with st.sidebar:
    st.header("1. Reservoir Data")
    Pr = st.number_input("Reservoir Pressure Pr (psi)", 1000.0, 15000.0, 5000.0, 100.0)
    Pb = st.number_input("Bubble Point Pb (psi)", 500.0, 10000.0, 3000.0, 100.0)
    PI = st.number_input("Productivity Index PI", 0.1, 50.0, 8.22, 0.1)
    T_res = st.number_input("Reservoir Temp (°F)", 100.0, 400.0, 220.0, 5.0) # جديد
    
    st.header("2. Fluid PVT Data") # جديد كامل
    GOR = st.number_input("GOR (scf/STB)", 100.0, 5000.0, 500.0, 50.0)
    API = st.number_input("Oil Gravity API", 10.0, 50.0, 35.0, 0.5) # جديد
    Gas_Gravity = st.number_input("Gas Gravity γg", 0.5, 1.5, 0.7, 0.01) # جديد
    WC = st.number_input("Water Cut %", 0.0, 100.0, 0.0, 1.0) # جديد
    
    st.header("3. Well & Tubing Data")
    Depth = st.number_input("Depth (ft)", 1000.0, 20000.0, 8000.0, 100.0)
    Tubing_ID = st.number_input("Tubing ID (in)", 1.0, 6.0, 2.88, 0.1)
    P_wh = st.number_input("Wellhead Pressure (psi)", 50.0, 5000.0, 500.0, 50.0) # جديد مهم للـ VLP

if st.button("Run Analysis", type="primary"):
    
    # نتأكد ان Pwf ما يكون اكبر من Pr
    if Pr <= Pb:
        st.warning("Note: Pr < Pb. This is already two-phase in reservoir")
    
    # نرسل كل المدخلات الجديدة للفانكشن
    inputs = {
        'Pr': Pr, 'Pb': Pb, 'PI': PI, 'T_res': T_res,
        'GOR': GOR, 'API': API, 'Gas_Gravity': Gas_Gravity, 'WC': WC,
        'Depth': Depth, 'Tubing_ID': Tubing_ID, 'P_wh': P_wh
    }
    
    with st.spinner("Calculating IPR + VLP..."):
        results = calculate_ipr_vlp(inputs) # لازم تعدل الفانكشن تقبل dict
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nodal Rate", f"{results['Q_nodal']:,.0f} STB/d")
    col2.metric("Nodal Pwf", f"{results['Pwf_nodal']:,.0f} psi")
    col3.metric("AOF", f"{results['Qmax']:,.0f} STB/d")
    col4.metric("Drawdown", f"{Pr - results['Pwf_nodal']:,.0f} psi")
    
    fig = plot_nodal(results, Pb, P_wh)  # ضفنا P_wh للرسم
    st.pyplot(fig)
    
    # نجمع المدخلات + النتائج للتقرير
    report_data = {**inputs, **results}
    
    pdf_buffer = create_report(report_data, fig)
    
    st.download_button(
        "📄 Download PDF Report", 
        pdf_buffer, 
        "Arzaq_Nodal_Report.pdf", 
        "application/pdf"
    )        
