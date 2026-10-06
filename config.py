import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    app_name: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )


settings = Settings()