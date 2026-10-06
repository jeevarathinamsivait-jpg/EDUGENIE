import json
import re

from typing import Any

from google import genai
from google.genai import types

from config import settings


class GeminiServiceError(RuntimeError):

    pass


class GeminiService:

    def __init__(self):

        if not settings.gemini_api_key:

            raise GeminiServiceError(
                "GEMINI_API_KEY is not configured. "
                "Please add your Gemini API key to .env"
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.4,
        max_output_tokens: int = 1200
    ) -> str:

        try:

            response = self.client.models.generate_content(

                model=settings.gemini_model,

                contents=prompt,

                config=types.GenerateContentConfig(

                    temperature=temperature,

                    max_output_tokens=max_output_tokens
                )
            )

            text = getattr(
                response,
                "text",
                None
            )

            if not text:

                raise GeminiServiceError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except GeminiServiceError:

            raise

        except Exception as error:

            raise GeminiServiceError(
                f"Gemini API request failed: {error}"
            )


    def generate_json(
        self,
        prompt: str,
        *,
        max_output_tokens: int = 1800
    ) -> Any:

        raw = self.generate(

            prompt
            + """

IMPORTANT:
Return ONLY valid JSON.
Do not use Markdown code fences.
Do not add explanations outside JSON.
""",

            temperature=0.2,

            max_output_tokens=max_output_tokens
        )

        cleaned = clean_json_block(raw)

        try:

            return json.loads(cleaned)

        except json.JSONDecodeError as error:

            raise GeminiServiceError(
                "Gemini returned invalid JSON. "
                "Please try again."
            ) from error


def clean_json_block(text: str) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start_candidates = [

        index

        for index in (
            text.find("{"),
            text.find("[")
        )

        if index >= 0
    ]

    if not start_candidates:

        return text

    start = min(start_candidates)

    end = max(
        text.rfind("}"),
        text.rfind("]")
    )

    if end >= start:

        return text[
            start:
            end + 1
        ]

    return text


def get_service():

    return GeminiService()