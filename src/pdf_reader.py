import pdfplumber

def extract_text(pdf_path):
    try:
        text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except Exception as e:
        return f"Error reading PDF: {e}"