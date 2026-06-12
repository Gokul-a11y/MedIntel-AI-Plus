from src.summarizer import generate_summary

sample_report = """
Patient Name: John Doe

Hemoglobin: 11 g/dL
Blood Sugar: 160 mg/dL
Cholesterol: 220 mg/dL

Observation:
Patient shows elevated blood sugar and cholesterol levels.
"""

result = generate_summary(sample_report)

print(result)