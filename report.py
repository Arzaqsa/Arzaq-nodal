from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generate_pdf(data):
    buffer = BytesIO(); c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 18); c.drawString(50, 800, "Arzaq Nodal - Professional Report")
    c.setFont("Helvetica", 11)
    c.drawString(50, 770, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(50, 740, f"Reservoir Pressure Pr: {data['Pr']:.0f} psi")
    c.drawString(50, 720, f"Bubble Point Pb: {data['Pb']:.0f} psi")
    c.drawString(50, 700, f"Nodal Rate: {data['Q_nodal']:,.0f} STB/day")
    c.drawString(50, 680, f"Nodal Pwf: {data['Pwf_nodal']:.0f} psi")
    c.drawString(50, 660, f"AOF: {data['Qmax']:,.0f} STB/day")
    c.save(); buffer.seek(0); return buffer
