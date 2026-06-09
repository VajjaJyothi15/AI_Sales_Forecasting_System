from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
        file_path,
        insights):

    pdf = SimpleDocTemplate(
        file_path
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    elements.append(

        Paragraph(
            "Business Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    for item in insights:

        elements.append(

            Paragraph(
                item,
                styles["Normal"]
            )
        )

    pdf.build(elements)