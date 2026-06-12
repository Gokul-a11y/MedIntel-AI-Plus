from src.pdf_reader import extract_text

text = extract_text("data/reports/test.pdf")

print(text[:1000])