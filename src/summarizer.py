import google.generativeai as genai

genai.configure(
    api_key=""
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_summary(report_text):

    prompt = f"""
Summarize the following medical report
in simple patient-friendly language.

Report:
{report_text}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"""
⚠ Gemini API quota exceeded.

Error:
{str(e)}

Please try again later or use another API project.
"""