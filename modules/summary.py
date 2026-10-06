from services.gemini_service import get_service


def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational content.

Requirements:

- Keep the important facts.
- Remove unnecessary repetition.
- Preserve important definitions.
- Preserve important relationships and conclusions.
- Use simple language.
- Use bullet points where useful.
- Do not add information that is not present in the original text.

Educational Content:

{text}
"""

    return get_service().generate(
        prompt,
        temperature=0.25,
        max_output_tokens=1000
    )