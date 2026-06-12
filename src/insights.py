import google.generativeai as genai

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def doctor_questions(report_text):

    prompt = f"""
    Generate 5 useful questions
    the patient should ask their doctor.

    Report:

    {report_text}
    """

    response = model.generate_content(prompt)

    return response.text