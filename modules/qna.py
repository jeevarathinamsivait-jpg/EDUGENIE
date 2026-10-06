from services.gemini_service import get_service


def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and concisely.

Requirements:

- Use simple student-friendly language.
- Give a direct answer first.
- Add a short explanation when useful.
- Use examples when appropriate.
- Do not unnecessarily make the answer long.
- If the question is ambiguous, clearly mention the assumption.

Student Question:

{question}
"""

    return get_service().generate(
        prompt,
        temperature=0.3,
        max_output_tokens=900
    )