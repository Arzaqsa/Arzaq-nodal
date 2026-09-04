from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
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
    story.append(Spacer(1, 20))

    # جدول النتائج فقط - لان results فيه 3 قيم بس
    table_data = [
        ['Parameter', 'Value'],
        ['Nodal Rate', f"{data['Q_nodal']:.0f} STB/d"],
        ['Nodal Pwf', f"{data['Pwf_nodal']:.0f} psi"],
        ['AOF', f"{data['Qmax']:.0f} STB/d"],
    ]
    
    t = Table(table_data, hAlign='LEFT', colWidths=[3*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # اضافة الرسم البياني
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    story.append(Paragraph("Nodal Analysis Plot", styles['Heading2']))
    story.append(Image(img_buffer, width=6*inch, height=4*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer
