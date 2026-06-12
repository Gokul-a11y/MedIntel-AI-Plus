import google.generativeai as genai

genai.configure(
    api_key=""
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_health_score(report_text):

    prompt = f"""
Analyze this medical report.

Provide:

1. Health Score out of 100
2. Risk Factors
3. Recommendations

Report:
{report_text}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
Health Score: 65/100

⚠ Gemini quota exceeded.
Showing demo score.
"""