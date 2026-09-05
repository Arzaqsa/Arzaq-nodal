from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime

def create_report(data, fig):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    # 1. Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Z2 - Well Analysis Report")
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    # 2. Input Data
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "1. Input Parameters")
    y -= 20
    c.setFont("Helvetica", 10)

    inputs = [
        f"Reservoir Pressure Pr: {data['Pr']:.0f} psi",
        f"Bubble Point Pb: {data['Pb']:.0f} psi",
        f"Productivity Index PI: {data['PI']:.2f} STB/d/psi",
        f"Reservoir Temp: {data['T_res']:.0f} °F",
        f"GOR: {data['GOR']:.0f} scf/STB",
        f"Oil API: {data['API']:.1f}",
        f"Gas Gravity: {data['Gas_Gravity']:.2f}",
        f"Water Cut: {data['WC']:.1f} %",
        f"Depth: {data['Depth']:.0f} ft",
        f"Tubing ID: {data['Tubing_ID']:.2f} in",
        f"Wellhead Pressure: {data['P_wh']:.0f} psi",
    ]
    for inp in inputs:
        c.drawString(70, y, f"• {inp}"); y -= 15
        if y < 100: # صفحة جديدة
            c.showPage(); y = height - 50

    y -= 10
    # 3. Results
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "2. Results")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(70, y, f"• AOF: {data['Qmax']:,.0f} STB/day"); y -= 15
    c.drawString(70, y, f"• Nodal Flow Rate: {data['Q_nodal']:,.0f} STB/day"); y -= 15
    c.drawString(70, y, f"• Nodal Pwf: {data['Pwf_nodal']:,.0f} psi"); y -= 15
    c.drawString(70, y, f"• Drawdown: {data['Pr'] - data['Pwf_nodal']:,.0f} psi"); y -= 25

    # 4. Plot
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "3. Nodal Analysis Plot")
    y -= 15
    
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight')
    img_buffer.seek(0)
    c.drawImage(ImageReader(img_buffer), 50, y-300, width=500, height=300)

    c.save()
    buffer.seek(0)
    return buffer
