from reportlab.pdfgen import canvas


def lines_to_pdf(lines: list, pdf_file):
    canva = canvas.Canvas(pdf_file)

    y = 750  # Posición vertical inicial
    for line in lines:
        canva.drawString(50, y, line.strip())  # Escribir línea en el PDF
        y -= 12  # Desplazar hacia arriba para la siguiente línea

    canva.save()
