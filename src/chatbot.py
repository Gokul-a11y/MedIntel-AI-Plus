import google.generativeai as genai
from src.rag_engine import retrieve_context

genai.configure(
    api_key=""
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_question(report_text, question):

    context = retrieve_context(question)

    if not context:
        context = report_text[:10000]

    prompt = f"""
You are a medical report assistant.

Medical Report Context:

{context}

Question:
{question}

Answer clearly using the report.

If the answer exists in the report,
provide it directly.

Only say "Not available in report"
if the information truly does not exist.
"""

    response = model.generate_content(
        prompt
    )

    return response.text