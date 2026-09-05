import streamlit as st
from calculations import calculate_ipr_vlp
from plotting import plot_nodal
from report import create_report

st.set_page_config(page_title="Z2", layout="wide", page_icon="🛢️")
st.title("🛢️ Z2 - Professional Well Analysis")
st.caption("Nodal Analysis with IPR Vogel + VLP for Two-Phase Flow")

with st.sidebar:
    st.header("1. Reservoir Data")
    Pr = st.number_input("Reservoir Pressure Pr (psi)", 1000.0, 15000.0, 5000.0, 100.0)
    Pb = st.number_input("Bubble Point Pb (psi)", 500.0, 10000.0, 3000.0, 100.0)
    PI = st.number_input("Productivity Index PI (STB/d/psi)", 0.1, 50.0, 8.22, 0.1)
    T_res = st.number_input("Reservoir Temp (°F)", 100.0, 400.0, 220.0, 5.0)
    
    st.header("2. Fluid PVT Data")
    GOR = st.number_input("GOR (scf/STB)", 100.0, 5000.0, 500.0, 50.0)
    API = st.number_input("Oil Gravity API", 10.0, 50.0, 35.0, 0.5)
    Gas_Gravity = st.number_input("Gas Gravity γg", 0.5, 1.5, 0.7, 0.01)
    WC = st.number_input("Water Cut %", 0.0, 100.0, 0.0, 1.0)
    
    st.header("3. Well & Tubing Data")
    Depth = st.number_input("Depth (ft)", 1000.0, 20000.0, 8000.0, 100.0)
    Tubing_ID = st.number_input("Tubing ID (in)", 1.0, 6.0, 2.88, 0.1)
    P_wh = st.number_input("Wellhead Pressure (psi)", 50.0, 5000.0, 500.0, 50.0)

    st.info("Note: For Pwf < Pb the flow is Two-Phase. VLP will use Hagedorn-Brown")

if st.button("Run Analysis", type="primary", use_container_width=True):
    
    if Pr <= 0 or PI <= 0:
        st.error("Pr and PI must be greater than 0")
        st.stop()
    
    # نجمع كل المدخلات في dict واحد
    inputs = {
        'Pr': Pr, 'Pb': Pb, 'PI': PI, 'T_res': T_res,
        'GOR': GOR, 'API': API, 'Gas_Gravity': Gas_Gravity, 'WC': WC,
        'Depth': Depth, 'Tubing_ID': Tubing_ID, 'P_wh': P_wh
    }
    
    with st.spinner("Calculating IPR + VLP... Please wait"):
        try:
            results = calculate_ipr_vlp(inputs)
        except Exception as e:
            st.error(f"Calculation Error: {e}")
            st.stop()
    
    st.success("Analysis Complete!")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("AOF", f"{results['Qmax']:,.0f} STB/d", help="Absolute Open Flow")
    col2.metric("Nodal Rate", f"{results['Q_nodal']:,.0f} STB/d")
    col3.metric("Nodal Pwf", f"{results['Pwf_nodal']:,.0f} psi")
    col4.metric("Drawdown", f"{Pr - results['Pwf_nodal']:,.0f} psi")
    
    st.markdown("---")
    st.subheader("Nodal Analysis Plot")
    fig = plot_nodal(results, inputs)
    st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("Download Report")
    
    # نجمع المدخلات + النتائج للتقرير
    report_data = {**inputs, **results}
    pdf_buffer = create_report(report_data, fig)
    
    st.download_button(
        label="📄 Download PDF Report", 
        data=pdf_buffer, 
        file_name=f"Z2_Report_{Pr:.0f}psi.pdf", 
        mime="application/pdf",
        use_container_width=True
    )

st.markdown("---")
st.caption("Developed by Arzaq | Vogel IPR + Hagedorn-Brown VLP")
