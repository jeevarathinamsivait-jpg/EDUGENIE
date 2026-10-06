from services.gemini_service import get_service


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie.

Explain the following topic to a beginner student.

Topic:

{topic}

Use this structure:

1. Simple definition
2. How it works
3. Simple real-world example
4. Important points
5. Short revision summary

Rules:

- Use simple English.
- Avoid unnecessary technical jargon.
- Explain difficult words.
- Make the explanation easy for a college student to understand.
"""

    return get_service().generate(
        prompt,
        temperature=0.35,
        max_output_tokens=1100
    )