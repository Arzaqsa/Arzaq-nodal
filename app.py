import streamlit as st
from calculations import calculate_ipr_vlp
from plotting import plot_nodal
from report import create_report

st.set_page_config(page_title="Arzaq Nodal", layout="wide")
st.title("🛢️ Z2 – Professional Well Analysis")

with st.sidebar:
    st.header("Reservoir Data")
    Pr = st.number_input("Pr (psi)", 5000.0)
    Pb = st.number_input("Pb (psi)", 3000.0)
    PI = st.number_input("PI", 8.22)
    st.header("Well Data")
    Depth = st.number_input("Depth (ft)", 8000.0)
    Tubing_ID = st.number_input("Tubing ID (in)", 2.88)
    GOR = st.number_input("GOR", 500.0)

if st.button("Run Analysis"):
    results = calculate_ipr_vlp(Pr, Pb, PI, Depth, Tubing_ID, GOR)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodal Rate", f"{results['Q_nodal']:.0f} STB/d")
    col2.metric("Nodal Pwf", f"{results['Pwf_nodal']:.0f} psi")
    col3.metric("AOF", f"{results['Qmax']:.0f} STB/d")
    
    fig = plot_nodal(results, Pb)  # احفظ الرسم
    st.pyplot(fig)
    
    # نجمع المدخلات + النتائج عشان نرسلها للتقرير
    report_data = {
        'Pr': Pr,
        'Pb': Pb,
        'PI': PI,
        'Depth': Depth,
        'TubingID': Tubing_ID,  # انتبه الاسم لازم TubingID بدون _
        'GOR': GOR,
        **results
    }
    
    pdf_buffer = create_report(report_data, fig)  # انشئ التقرير بالرسم
    
    st.download_button(
        "📄 Download PDF Report", 
        pdf_buffer, 
        "Z2_Report.pdf", 
        "application/pdf"
    )
