from services.gemini_service import get_service


def generate_quiz(passage: str) -> dict:

    prompt = f"""
You are EduGenie's quiz generation system.

Create exactly 3 multiple-choice questions from the
educational passage below.

Return ONLY valid JSON.

Use this exact format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:

- Exactly 3 questions.
- Exactly 4 options per question.
- The correct_answer must exactly match one option.
- Questions must be based only on the supplied passage.
- Distractors should be plausible.
- Do not use Markdown.
- Do not add text outside JSON.

PASSAGE:

{passage}
"""

    data = get_service().generate_json(
        prompt,
        max_output_tokens=1800
    )

    if not isinstance(data, dict):

        raise ValueError(
            "Quiz response is not a JSON object."
        )

    questions = data.get("questions")

    if not isinstance(questions, list):

        raise ValueError(
            "Quiz response does not contain questions."
        )

    if len(questions) != 3:

        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    for question in questions:

        if not isinstance(question, dict):

            raise ValueError(
                "Invalid quiz question."
            )

        if not isinstance(
            question.get("question"),
            str
        ):

            raise ValueError(
                "Invalid question text."
            )

        options = question.get("options")

        if not isinstance(options, list):

            raise ValueError(
                "Invalid options."
            )

        if len(options) != 4:

            raise ValueError(
                "Each question must contain 4 options."
            )

        correct_answer = question.get(
            "correct_answer"
        )

        if correct_answer not in options:

            raise ValueError(
                "Correct answer does not match an option."
            )

    return {
        "questions": questions
    }