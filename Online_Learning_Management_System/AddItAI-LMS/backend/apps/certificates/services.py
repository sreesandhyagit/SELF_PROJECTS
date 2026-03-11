import os
from django.conf import settings
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

def generate_certificate(user,course,certificate):

    folder=os.path.join(settings.MEDIA_ROOT,"certificates")
    os.makedirs(folder,exist_ok=True)

    filename=f"{certificate.certificate_id}.pdf"
    path=os.path.join(folder,filename)

    width,height=landscape(A4)
    c=canvas.Canvas(path,pagesize=landscape(A4))

    #background border
    c.setStrokeColor(HexColor("#C9A227"))
    c.setLineWidth(8)
    c.rect(30,30,width - 60, height - 60)

    #logo
    logo_path=os.path.join(settings.MEDIA_ROOT,"assets","logo.png", mask='auto')

    if os.path.exists(logo_path):
        c.drawImage(logo_path,width/2 - 60, height - 120,120,60)

    #Title
    c.setFont("Helvetica-Bold",36)
    c.drawCentredString(width/2,height - 180,"Certificate of Completion")

    #student name
    c.setFont("Helvetica",30)
    c.drawCentredString(width/2,height - 260,user.username)

    #description
    c.setFont("Helvetica",18)
    c.drawCentredString(width/2,height - 310,"has successfully completed the course")

    #course title
    c.setFont("Helvetica-Bold",24)
    c.drawCentredString(width/2,height - 350,course.title)

    #date
    c.setFont("Helvetica",16)
    c.drawCentredString(width/2,height - 420,f"Issued on {certificate.issued_at.date()}")

    #signature
    signature_path=os.path.join(settings.MEDIA_ROOT,"assets","signature.png")
    if os.path.exists(signature_path):
        c.drawImage(signature_path,width/2 - 80, 100,160,50)

    c.setFont("Helvetica",14)
    c.drawCentredString(width/2,80,"Course Instructor")

    #certificate id
    c.setFont("Helvetica",10)
    c.drawCentredString(width/2,50,f"Certificate ID: {certificate.certificate_id}")
        
    c.save()

    return f"certificates/{filename}"

