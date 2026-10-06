from services.gemini_service import get_service


def get_learning_recommendations(topic: str) -> dict:

    prompt = f"""
You are EduGenie's personalized learning-path generator.

Create a structured learning path for:

{topic}

Return ONLY valid JSON.

Use this format:

{{
    "topic": "Topic name",
    "goal": "Learning goal",
    "stages": [
        {{
            "level": "Beginner",
            "duration": "2 weeks",
            "topics": [
                "Topic 1",
                "Topic 2"
            ],
            "practice": [
                "Practice 1",
                "Practice 2"
            ],
            "resources": [
                "Official documentation",
                "Textbook",
                "Practice problems"
            ]
        }},
        {{
            "level": "Intermediate",
            "duration": "3 weeks",
            "topics": [],
            "practice": [],
            "resources": []
        }},
        {{
            "level": "Advanced",
            "duration": "4 weeks",
            "topics": [],
            "practice": [],
            "resources": []
        }}
    ],
    "study_tips": [
        "Tip 1",
        "Tip 2"
    ]
}}

Rules:

- Progress from beginner to advanced.
- Make the plan practical for a student.
- Include topics.
- Include practice activities.
- Include resource types.
- Do not invent specific URLs.
- Do not use Markdown.
"""

    data = get_service().generate_json(
        prompt,
        max_output_tokens=1800
    )

    if not isinstance(data, dict):

        raise ValueError(
            "Learning path response is invalid."
        )

    if not isinstance(
        data.get("stages"),
        list
    ):

        raise ValueError(
            "Learning path stages are missing."
        )

    return data