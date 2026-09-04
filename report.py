from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io
import datetime

def create_report(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # العنوان
    story.append(Paragraph("Arzaq Nodal - Professional Report", styles['Title']))
    story.append(Spacer(1, 12))
    
    # التاريخ
    story.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 12))

    # جدول المدخلات والمخرجات
    table_data = [
        ['Parameter', 'Value'],
        ['Reservoir Pressure Pr', f"{data['Pr']} psi"],
        ['Bubble Point Pb', f"{data['Pb']} psi"],
        ['PI', f"{data['PI']}"],
        ['Depth', f"{data['Depth']} ft"],
        ['Tubing ID', f"{data['TubingID']} in"],
        ['GOR', f"{data['GOR']}"],
        ['Nodal Rate', f"{data['NodalRate']:.0f} STB/d"],
        ['Nodal Pwf', f"{data['NodalPwf']:.0f} psi"],
        ['AOF', f"{data['AOF']:.0f} STB/d"],
    ]
    t = Table(table_data, hAlign='LEFT')
    story.append(t)
    story.append(Spacer(1, 20))

    # اضافة الرسم البياني
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='PNG', dpi=150)
    img_buffer.seek(0)
    story.append(Paragraph("Nodal Analysis Plot", styles['Heading2']))
    story.append(Image(img_buffer, width=6*inch, height=4*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer
