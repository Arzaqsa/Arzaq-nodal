import streamlit as st
from calculations import calculate_ipr_vlp
from plotting import plot_nodal
from report import generate_pdf

st.set_page_config(page_title="Arzaq Nodal", layout="wide", page_icon="🛢️")
st.title("🛢️ Arzaq Nodal - Professional Well Analysis")

with st.sidebar:
    st.header("Reservoir Data")
    Pr = st.number_input("Pr (psi)", 5000.0)
    Pb = st.number_input("Pb (psi)", 3000.0)
    PI = st.number_input("PI", 8.22)
    st.header("Well Data")
    Depth = st.number_input("Depth (ft)", 8000.0)
    Tubing_ID = st.number_input("Tubing ID (in)", 2.875)
    GOR = st.number_input("GOR", 500.0)

if st.button("Run Analysis"):
    results = calculate_ipr_vlp(Pr, Pb, PI, Depth, Tubing_ID, GOR)
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodal Rate", f"{results['Q_nodal']:,.0f} STB/d")
    col2.metric("Nodal Pwf", f"{results['Pwf_nodal']:.0f} psi")
    col3.metric("AOF", f"{results['Qmax']:,.0f} STB/d")
    st.pyplot(plot_nodal(results, Pb))
    pdf_data = {"Pr":Pr, "Pb":Pb, "Q_nodal":results["Q_nodal"], "Pwf_nodal":results["Pwf_nodal"], "Qmax":results["Qmax"]}
    st.download_button("📄 Download PDF Report", generate_pdf(pdf_data), "Arzaq_Nodal_Report.pdf")
