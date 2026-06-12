import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(summary_text):

    os.makedirs("data/summaries", exist_ok=True)

    pdf_path = "data/summaries/summary.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Medical Report Summary",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            summary_text.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_path